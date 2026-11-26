"""Render authentic repository metrics and isometric daily contributions."""
import argparse, datetime as dt, json, math
from collections import Counter
from pathlib import Path
from visual import ROOT,C,text,rect,line,path,svg,save
from fetch_github_data import validate_snapshot

def streaks(days):
    best=run=0
    for d in days:
        run=run+1 if d['count'] else 0;best=max(best,run)
    end=len(days)-1
    if not days[end]['count']:end-=1
    current=0
    while end>=0 and days[end]['count']:
        current+=1;end-=1
    return current,best

def render(s,out=ROOT):
    validate_snapshot(s)
    def write(name,data):
        dest=out/name;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(data,encoding='utf-8',newline='\n')
    repos=[r for r in s['repositories'] if not r['fork'] and not r['archived'] and r['name'].lower()!='zylus08']
    days=s['calendar']['days'];current,longest=streaks(days);stamp=s['fetched_at'].replace('T',' ').replace('Z',' UTC')
    b=text(28,32,'06 / ENGINEERING TELEMETRY',14,C['cyan'],mono=True)
    for i,(n,label) in enumerate([(len(repos),'PUBLIC ORIGINALS'),(sum(r['stargazers_count'] for r in repos),'STARS'),(sum(r['forks_count'] for r in repos),'FORKS RECEIVED')]):
        x=28+i*144;b+=text(x,107,n,54,weight=900)+text(x,135,label,11,C['muted'],mono=True)
    b+=line(28,155,432,155)+text(28,187,'PRIMARY LANGUAGE / REPOSITORIES',12,C['muted'],mono=True)
    langs=Counter(r['language'] or 'Unclassified' for r in repos)
    for i,(lang,count) in enumerate(langs.most_common(4)):
        y=216+i*28;b+=text(28,y,lang,15)+rect(160,y-11,210,9,C['grid'])+rect(160,y-11,210*count/max(1,len(repos)),9,C['cyan'])+text(389,y,count,14,mono=True)
    b+=text(28,335,stamp,12,C['muted'],mono=True)
    write(Path('assets/telemetry/repositories.svg'),svg(460,360,b,'Public original non-archived repositories excluding profile: '+str(len(repos))+'. Stars '+str(sum(r['stargazers_count'] for r in repos))+'. Snapshot '+stamp,C['panel']))
    b=text(28,32,'PUBLIC PROFILE / 365-DAY WINDOW',13,C['lavender'],mono=True)+text(25,108,sum(d['count'] for d in days),64,weight=900)+text(28,139,'CONTRIBUTIONS IN DISPLAYED WINDOW',12,C['muted'],mono=True)
    for i,(n,label) in enumerate([(sum(d['count']>0 for d in days),'ACTIVE DAYS'),(current,'CURRENT STREAK'),(longest,'LONGEST IN WINDOW')]):
        x=28+i*144;b+=text(x,202,n,36,weight=700)+text(x,225,label,10,C['muted'],mono=True)
    b+=text(28,250,'CONTRIBUTIONS / 7-DAY BINS',10,C['muted'],mono=True)
    weekly=[sum(d['count'] for d in days[i:i+7]) for i in range(0,len(days),7)]
    for i,n in enumerate(weekly):b+=rect(28+i*7.6,302-50*n/max(1,max(weekly)),5,50*n/max(1,max(weekly)),C['lavender'])
    b+=text(28,335,days[0]['date']+' → '+days[-1]['date'],13,C['muted'],mono=True)
    write(Path('assets/telemetry/activity.svg'),svg(460,360,b,'365-day public profile activity: '+str(sum(d['count'] for d in days))+' contributions; current streak '+str(current)+'; longest in window '+str(longest)+'. Snapshot '+stamp,C['panel']))
    for mobile in [False,True]:write(Path('assets/skyline/'+('mobile' if mobile else 'skyline')+'.svg'),skyline(s,mobile))
    active=sorted(repos,key=lambda r:r['pushed_at'],reverse=True)[:5]
    md='<!-- Generated from the same validated snapshot. -->\n\n'
    md+='Snapshot: **'+stamp+'**. '+str(len(repos))+' public original, non-archived repositories; '+str(sum(r['stargazers_count'] for r in repos))+' stars; '+str(sum(r['forks_count'] for r in repos))+' forks received.\n\n'
    md+=f"Calendar: {days[0]['date']}–{days[-1]['date']}; {sum(d['count'] for d in days)} contributions; {sum(d['count']>0 for d in days)} active days; current streak {current}; longest in this window {longest}.\n\nRecent repository pushes (not necessarily authored commits):\n\n"
    md+='\n'.join(f"- [{r['name']}]({r['html_url']}) · {r['pushed_at'][:10]}" for r in active)+'\n'
    write(Path('data/telemetry.md'),md)

def skyline(s,mobile=False):
    days=s['calendar']['days'];w,h=(480,650) if mobile else (960,490)
    b=text(28,32,'07 / ACTIVITY TOPOGRAPHY',14,C['cyan'],mono=True)+text(28,79,'A year, in relief.',33 if mobile else 42,weight=900)
    b+=text(28,109,days[0]['date']+' → '+days[-1]['date'],14,C['muted'],mono=True)
    maxcount=max(d['count'] for d in days)
    # Calendar columns are weeks; rows Sunday–Saturday. Height is linear in daily count.
    start=dt.date.fromisoformat(days[0]['date']);offset=(start.weekday()+1)%7
    groups=[(0,27,163),(27,54,388)] if mobile else [(0,54,175)]
    sx,sy=(12,2.6) if mobile else (14.5,3.2)
    for first,last,y0 in groups:
        buildings=[]
        for i,d in enumerate(days):
            week,weekday=divmod(i+offset,7)
            if not first<=week<last:continue
            x=(99 if mobile else 132)+(week-first-weekday)*sx;y=y0+(week-first+weekday)*sy
            height=90*d['count']/max(1,maxcount);dx=sx*.82;dy=sy*.82
            top=[(x,y-height),(x+dx,y+dy-height),(x,y+2*dy-height),(x-dx,y+dy-height)]
            def poly(points,fill):return '<polygon points="'+' '.join(f'{a:.2f},{c:.2f}' for a,c in points)+f'" fill="{fill}" stroke="{C["ink"]}" stroke-width=".5"/>'
            piece=''
            if d['count']:
                piece+=poly([top[3],top[2],(x,y+2*dy),(x-dx,y+dy)],'#176266')
                piece+=poly([top[2],top[1],(x+dx,y+dy),(x,y+2*dy)],'#258F95')
            piece+=poly(top,C['cyan'] if d['count'] else C['grid'])
            buildings.append((week+weekday,week,piece))
        b+=''.join(v for _,__,v in sorted(buildings))
        b+=text(28,y0+145,'WEEKS '+str(first+1).zfill(2)+'–'+str(min(last,53)),12,C['muted'],mono=True)
    b+=line(28,h-94,w-28,h-94)+text(28,h-64,f'HEIGHT = DAILY COUNT / MAX {maxcount}',13,C['cyan'],mono=True)
    b+=text(28,h-39,'SUNDAY → SATURDAY / LEFT → RIGHT: WEEKS',11,C['muted'],mono=True)
    b+=text(28,h-17,'SNAPSHOT '+s['fetched_at'],11,C['muted'],mono=True)
    return svg(w,h,b,'Isometric GitHub contribution calendar. Building height is proportional to actual daily contributions; maximum '+str(maxcount)+'. '+days[0]['date']+' through '+days[-1]['date'])

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--snapshot',type=Path,default=ROOT/'data/github_snapshot.json');p.add_argument('--output',type=Path,default=ROOT);a=p.parse_args()
    render(json.loads(a.snapshot.read_text(encoding='utf-8')),a.output);print('Telemetry and skyline generated')
