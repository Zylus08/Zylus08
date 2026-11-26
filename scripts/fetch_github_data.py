"""Fetch public metadata and GitHub's public calendar. Fail closed, publish atomically."""
import argparse, datetime as dt, hashlib, json, os, re, sys, time
import urllib.request, urllib.error
from html.parser import HTMLParser
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OWNER='Zylus08'
FIELDS=['name','html_url','description','fork','archived','private','language','stargazers_count','forks_count','pushed_at','default_branch']

def request(url,opener=urllib.request.urlopen,sleeper=time.sleep):
    headers={'User-Agent':'Zylus-observatory/2.0','Accept':'application/vnd.github+json' if 'api.github.com/' in url else 'text/html','X-GitHub-Api-Version':'2022-11-28'}
    token=os.environ.get('GH_TOKEN')
    if token and url.startswith('https://api.github.com/'):
        headers['Authorization']='Bearer '+token
    for attempt in range(3):
        try:
            with opener(urllib.request.Request(url,headers=headers),timeout=30) as response:
                return response.read()
        except urllib.error.HTTPError as e:
            if e.code not in (403,429,500,502,503,504) or attempt==2: raise RuntimeError(f'HTTP {e.code}; existing snapshot retained') from None
            delay=min(60,max(2**attempt,int(e.headers.get('Retry-After','0')) if e.headers.get('Retry-After','').isdigit() else 0))
            sleeper(delay)
        except (urllib.error.URLError,TimeoutError,OSError):
            if attempt==2: raise RuntimeError('Network unavailable; existing snapshot retained') from None
            sleeper(2**attempt)

class Calendar(HTMLParser):
    def __init__(self):
        super().__init__();self.cells={};self.tips={};self.key=None;self.words=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if 'data-date' in a and 'id' in a:
            if a['id'] in self.cells: raise ValueError('Duplicate calendar cell')
            self.cells[a['id']]=a['data-date']
        if tag=='tool-tip':self.key=a.get('for');self.words=[]
    def handle_data(self,data):
        if self.key:self.words.append(data)
    def handle_endtag(self,tag):
        if tag=='tool-tip' and self.key:
            self.tips[self.key]=''.join(self.words).strip();self.key=None

def parse_calendar(html):
    p=Calendar();p.feed(html); days=[]
    for key,date in p.cells.items():
        tip=p.tips.get(key,'');m=re.match(r'(No|[\d,]+) contributions? on ',tip)
        if not m: raise ValueError('Missing or changed contribution count markup')
        count=0 if m[1]=='No' else int(m[1].replace(',',''))
        days.append({'date':date,'count':count})
    days.sort(key=lambda x:x['date'])
    validate_days(days)
    # Public markup includes week-padding days. Display exactly the latest 365.
    return days[-365:]

def validate_days(days):
    if not 350<=len(days)<=371:raise ValueError('Incomplete calendar window')
    dates=[]
    for day in days:
        dates.append(dt.date.fromisoformat(day['date']))
        if type(day['count']) is not int or day['count']<0:raise ValueError('Invalid contribution count')
    if any((b-a).days!=1 for a,b in zip(dates,dates[1:])):raise ValueError('Duplicate or missing calendar date')

def validate_snapshot(s):
    if s.get('schema')!=1 or s.get('owner')!=OWNER:raise ValueError('Invalid snapshot identity')
    dt.datetime.fromisoformat(s['fetched_at'].replace('Z','+00:00'))
    validate_days(s['calendar']['days'])
    if len(s['calendar']['days'])!=365:raise ValueError('Expected 365 days')
    repos=s['repositories']
    if not repos or len({r['name'] for r in repos})!=len(repos):raise ValueError('Missing or duplicate repositories')
    for r in repos:
        if r.get('private') is not False:raise ValueError('Private repository rejected')
        for key in ['stargazers_count','forks_count']:
            if type(r.get(key)) is not int or r[key]<0:raise ValueError('Invalid repository count')
        for key in ['fork','archived']:
            if type(r.get(key)) is not bool:raise ValueError('Missing repository filter')
        if not r['html_url'].startswith(f'https://github.com/{OWNER}/'):raise ValueError('Unexpected repository URL')

def collect():
    repos=[]
    for page in range(1,101):
        batch=json.loads(request(f'https://api.github.com/users/{OWNER}/repos?type=owner&per_page=100&page={page}'))
        if not isinstance(batch,list):raise ValueError('Invalid REST response')
        repos.extend({k:r[k] for k in FIELDS} for r in batch if not r['private'])
        if len(batch)<100:break
    else:raise ValueError('Pagination did not terminate')
    html=request(f'https://github.com/users/{OWNER}/contributions').decode()
    return make_snapshot(repos,html,'GitHub REST /users/Zylus08/repos (paginated)')

def make_snapshot(repos,html,source):
    days=parse_calendar(html)
    now=dt.datetime.now(dt.timezone.utc)
    if abs((now.date()-dt.date.fromisoformat(days[-1]['date'])).days)>1:raise ValueError('Stale calendar response')
    s={'schema':1,'owner':OWNER,'fetched_at':now.isoformat(timespec='seconds').replace('+00:00','Z'),'repository_source':source,'repositories':sorted(repos,key=lambda r:r['name'].lower()),'calendar':{'source':f'https://github.com/users/{OWNER}/contributions','visibility':'Public profile calendar; may include anonymized private contributions if owner enables them. No private repository details.','raw_sha256':hashlib.sha256(html.encode()).hexdigest(),'days':days}}
    validate_snapshot(s);return s

def publish(s,destination):
    validate_snapshot(s)
    if destination.exists():
        old=json.loads(destination.read_text(encoding='utf-8'))
        if old.get('repositories')==s['repositories'] and old.get('calendar',{}).get('days')==s['calendar']['days']:
            print('No meaningful data changes; retain published timestamp');return False
    destination.parent.mkdir(parents=True,exist_ok=True)
    tmp=destination.with_suffix('.tmp');tmp.write_text(json.dumps(s,indent=2)+'\n',encoding='utf-8',newline='\n');tmp.replace(destination)
    return True

def main():
    p=argparse.ArgumentParser();p.add_argument('--bootstrap',action='store_true');p.add_argument('--output',type=Path,default=ROOT/'data/github_snapshot.json');a=p.parse_args()
    try:
        s=make_snapshot(json.loads((ROOT/'data/repositories.json').read_text()),(ROOT/'.dist/recon/contributions.html').read_text(encoding='utf-8'),'Connected GitHub REST: public repository search + individual /repos/Zylus08/{repo} metadata; 2026-11-26') if a.bootstrap else collect()
        publish(s,a.output);print('Valid snapshot:',len(s['repositories']),'public repos;',sum(d['count'] for d in s['calendar']['days']),'contributions')
    except (ValueError,KeyError,RuntimeError,json.JSONDecodeError) as e:
        print('Refresh failed:',str(e),file=sys.stderr);return 1
    return 0

if __name__=='__main__':sys.exit(main())
