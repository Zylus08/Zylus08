"""Small deterministic SVG vocabulary. No external fonts, CSS or image requests."""
import json
from pathlib import Path
from html import escape
ROOT=Path(__file__).resolve().parents[1]
TOKENS=json.loads((ROOT/'config/design_tokens.json').read_text())
C=TOKENS['colors']

def text(x,y,s,size=16,color=None,weight=400,mono=False,spacing=0):
    font=TOKENS['fonts']['mono' if mono else 'display']
    return f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" font-weight="{weight}" letter-spacing="{spacing}" fill="{color or C["paper"]}">{escape(str(s))}</text>'

def rect(x,y,w,h,fill,stroke=None):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"'+(f' stroke="{stroke}"' if stroke else '')+'/>'

def line(x,y,xx,yy,color=None,width=1):
    return f'<path d="M{x} {y}L{xx} {yy}" stroke="{color or C["grid"]}" stroke-width="{width}" fill="none"/>'

def path(points,color,width=1,opacity=1):
    return '<polyline points="'+' '.join(f'{x:.2f},{y:.2f}' for x,y in points)+f'" fill="none" stroke="{color}" stroke-width="{width}" opacity="{opacity}"/>'

def svg(w,h,body,title,bg=None):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title"><title id="title">{escape(title)}</title>'+rect(0,0,w,h,bg or C['ink'])+body+'</svg>\n'

def save(name,content):
    p=ROOT/name; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(content,encoding='utf-8',newline='\n')

def grid(x,y,w,h,step=32):
    return ''.join(line(i,y,i,y+h) for i in range(x,x+w+1,step))+''.join(line(x,j,x+w,j) for j in range(y,y+h+1,step))

def lorenz():
    p=TOKENS['math']; v=p['initial'][:]; out=[]; dt=p['dt']
    def f(v):
        x,y,z=v
        return [p['sigma']*(y-x),x*(p['rho']-z)-y,x*y-p['beta']*z]
    for i in range(p['steps']):
        a=f(v); b=f([v[j]+dt*a[j]/2 for j in range(3)])
        c=f([v[j]+dt*b[j]/2 for j in range(3)]); d=f([v[j]+dt*c[j] for j in range(3)])
        v=[v[j]+dt*(a[j]+2*b[j]+2*c[j]+d[j])/6 for j in range(3)]
        if i>=p['burn_in']: out.append(v[:])
    return out

def attractor(x,y,w,h,color=None):
    points=lorenz(); xs=[v[0] for v in points]; zs=[v[2] for v in points]
    pts=[(x+(a-min(xs))/(max(xs)-min(xs))*w,y+h-(z-min(zs))/(max(zs)-min(zs))*h) for a,_,z in points]
    return ''.join(path(pts[i:i+181],color or C['cyan'],0.9,0.55+(i%360)/800) for i in range(0,len(pts)-1,180))

def concepts():
    b=grid(32,32,896,352)+text(48,70,'A / MISSION CONTROL',16,C['cyan'],mono=True)
    b+=text(48,152,'ZYLUS',82,weight=900)+text(48,195,'SYSTEMS / INTELLIGENCE / QUANT',18,mono=True)
    b+=attractor(540,78,330,250)+rect(48,270,400,80,C['panel'],C['grid'])+text(68,314,'OBSERVATION → EXPERIMENT',19)
    save('reports/concepts/01-control.svg',svg(960,416,b,'Concept A: mission control dominant'))
    b=text(30,45,'B / DIGITAL BRUTALISM',16,C['ink'],mono=True)+text(20,222,'ZYLUS',215,C['ink'],900)
    b+=rect(32,258,580,110,C['ink'])+text(52,302,'BUILD BENEATH',38,weight=900)+text(52,347,'THE ABSTRACTION.',38,weight=900)+attractor(670,258,240,110,C['ink'])
    save('reports/concepts/02-brutalism.svg',svg(960,416,b,'Concept B: digital brutalism dominant',C['cyan']))
    b=attractor(325,30,580,350,C['lavender'])+text(32,48,'C / COMPUTATIONAL RENAISSANCE',16,C['lavender'],mono=True)
    b+=text(32,165,'Order.',66,weight=900)+text(32,230,'Chaos.',66,weight=900)+text(32,295,'Inquiry.',66,weight=900)
    b+=text(32,386,'ZYLUS / A STUDY IN COMPUTATION',16,mono=True)
    save('reports/concepts/03-renaissance.svg',svg(960,416,b,'Concept C: computational renaissance dominant'))

if __name__=='__main__': concepts()
