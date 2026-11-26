"""One-off public-source capture; not part of scheduled generation."""
import json, re, urllib.request, concurrent.futures, hashlib
from pathlib import Path
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / '.dist/recon'
OUT.mkdir(parents=True, exist_ok=True)

def get(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Zylus-profile-research'})
    return urllib.request.urlopen(req, timeout=30).read().decode('utf-8')

class Links(HTMLParser):
    def __init__(self):
        super().__init__(); self.links=[]
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if tag=='a' and 'href' in a: self.links.append(a['href'])

def main():
    s=get('https://sakshamkumarmishra.cv')
    (OUT/'portfolio.html').write_text(s, encoding='utf-8')
    p=Links(); p.feed(s)
    links=sorted(set(x for x in p.links if any(t in x for t in ['linkedin','mailto:','documents/','leetcode'])))
    (ROOT/'data/contacts.json').write_text(json.dumps(links,indent=2)+'\n',encoding='utf-8')
    print('Contacts:', json.dumps(links))
    s=get('https://github.com/users/Zylus08/contributions')
    (OUT/'contributions.html').write_text(s,encoding='utf-8')
    print('Calendar saved:', len(s))
    refs=['abhinav29102005','JeevantVerma','Anay0305','AnshikaM17','MankiratSingh1315','anuraghazra','sindresorhus','athul','DenverCoder1','gautamkrishnar','jstrieb','lowlighter','simonw','rahuldkjain','antonkomarev']
    def reference(n):
        try:
            s=get(f'https://github.com/{n}/{n}')
            (OUT/(n+'.html')).write_text(s,encoding='utf-8')
            return {'name':n,'url':f'https://github.com/{n}/{n}','bytes':len(s),'sha256':hashlib.sha256(s.encode()).hexdigest()}
        except Exception as e: return {'name':n,'error':str(e)}
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool: results=list(pool.map(reference,refs))
    (ROOT/'data/reference_manifest.json').write_text(json.dumps(results,indent=2)+'\n',encoding='utf-8')
    print('Reference captures:', len([r for r in results if 'bytes' in r]))

if __name__=='__main__': main()
