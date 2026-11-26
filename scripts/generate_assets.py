"""Generate the static profile experience. Pure local inputs, reproducible SVG."""
import json, math, re, xml.etree.ElementTree as ET
from visual import ROOT,C,text,rect,line,path,svg,save,grid,attractor

def hero(mobile=False):
    w,h=(480,610) if mobile else (960,510)
    b=text(28,35,'00 / SIGNAL ACQUIRED',14,C['cyan'],mono=True)
    b+=text(28,68,'INDEPENDENT COMPUTATIONAL OBSERVATORY',12,C['muted'],mono=True)
    b+=text(19,180 if mobile else 247,'ZYLUS',111 if mobile else 224,weight=900,spacing=-6)
    if mobile:
        b+=attractor(100,220,340,205)+text(28,469,'SAKSHAM KUMAR MISHRA',23,weight=700)
        b+=text(28,511,'Building the machinery',28,weight=700)+text(28,547,'beneath the abstraction.',28,weight=700)
        b+=text(28,584,'SYSTEMS / INTELLIGENCE / QUANT',13,C['cyan'],mono=True)
    else:
        b+=line(28,280,932,280)+text(30,320,'SAKSHAM KUMAR MISHRA',25,weight=700)
        b+=text(28,374,'Building the machinery',38,weight=700)+text(28,419,'beneath the abstraction.',38,weight=700)
        b+=attractor(655,302,270,147)+text(28,479,'SYSTEMS ENGINEERING / MACHINE INTELLIGENCE / QUANTITATIVE RESEARCH',13,C['cyan'],mono=True)
    b+=rect(w-8,0,8,h,C['cyan'])
    save('assets/hero/'+('mobile' if mobile else 'hero')+'.svg',svg(w,h,b,'ZYLUS — Saksham Kumar Mishra. Building the machinery beneath the abstraction.'))

def diagram(kind,color):
    b=''
    if kind=='Axiom':
        nodes=[(55,203,'SCAN'),(165,203,'FILTER'),(275,203,'JOIN'),(385,203,'SORT')]
        for i,(x,y,label) in enumerate(nodes):
            if i<3:b+=line(x+28,y,x+82,y,color,2)
            b+=rect(x-28,y-22,56,44,C['ink'],color)+text(x-23,y+5,label,12,color,mono=True)
        for i in range(5): b+=rect(44+i*76,247,55,5+i*2,color)
        b+=text(28,287,'SCAN → PLAN → EXECUTE → SPILL',13,C['muted'],mono=True)
    elif kind=='PRAXIS':
        nodes=[(230,170),(130,215),(330,215),(75,265),(180,265),(290,265),(395,265)]
        for a,d in [(0,1),(0,2),(1,3),(1,4),(2,5),(2,6)]:b+=line(*nodes[a],*nodes[d],color,1.5)
        for i,(x,y) in enumerate(nodes):b+=rect(x-15,y-12,30,24,C['panel'],color)+text(x-6,y+5,['T','f','{}','x','+','&','T'][i],14,color,mono=True)
    elif kind=='FORGE':
        for row in range(5):
            for col in range(14):
                v=(math.sin(col*.65+row*.8)+1)/2
                b+=f'<rect x="{29+col*29}" y="{166+row*23}" width="24" height="18" fill="{color}" opacity="{.15+.85*v:.2f}"/>'
        b+=text(28,299,'OPERATOR FUSION / SCHEMATIC',13,C['muted'],mono=True)
    else:
        for k in range(3):
            for row in range(5):
                for col in range(5):b+=rect(32+k*139+col*18,169+row*18,14,14,color if col<=row else C['grid'])
            b+=text(61+k*139,283,['Q','K','V'][k],20,color,700,True)
        b+=line(98,293,372,293,color)
    return b

def projects():
    ps=json.loads((ROOT/'data/projects.json').read_text(encoding='utf-8'))
    for i,p in enumerate(ps):
        accent=C[p['accent']]; system=p['domain']=='systems'; h=414 if system else 178
        b=rect(0,0,4,h,accent)+text(28,31,f'{"SYS" if system else "SCI" if p["domain"]=="intelligence" else "QNT"} / {i+1:02d}',13,accent,mono=True)
        name_size=58 if system else (23 if len(p['name'])>20 else 32)
        b+=text(25,99 if system else 77,p['name'],name_size,weight=900,spacing=-1)
        b+=text(28,132 if system else 108,p['description'],17)
        if system:
            b+=diagram(p['repo'],accent)+line(28,318,432,318)
            b+=text(28,344,p['highlights'],15,C['muted'])+text(28,372,p['status'].upper(),13,accent,mono=True)
            b+=text(28,396,p['language']+'  /  OPEN DOSSIER ↗',13,C['muted'],mono=True)
        else:
            b+=text(28,136,p['highlights'],14,C['muted'])+text(28,161,p['status'].upper()+'  ↗',12,accent,mono=True)
        save(f'assets/projects/{p["repo"]}.svg',svg(460,h,b,p['name']+': '+p['description']+' '+p['limitation'],C['panel']))

def technology():
    groups=[('01','LANGUAGES',[('python','Python'),('cplusplus','C++'),('rust','Rust'),('go','Go')]),('02','SYSTEMS & INFRASTRUCTURE',[('cmake','CMake'),('docker','Docker'),('git','Git'),('githubactions','Actions')]),('03','MACHINE & SCIENTIFIC COMPUTING',[('pytorch','PyTorch'),('numpy','NumPy'),('pandas','pandas'),('scikitlearn','scikit-learn')]),('04','APPLICATION ENGINEERING',[('react','React'),('vite','Vite'),('typescript','TypeScript'),('javascript','JavaScript')])]
    manifest=[]
    for num,title,items in groups:
        b=text(28,32,num+' / CAPABILITY MAP',13,C['cyan'],mono=True)+text(28,65,title,18,weight=700)+line(28,84,432,84)
        for i,(slug,label) in enumerate(items):
            x=28+(i%2)*210; y=108+(i//2)*64
            icon=ET.parse(ROOT/f'assets/technology/icons/{slug}.svg').getroot()
            icon.set('x',str(x+6));icon.set('y',str(y+6));icon.set('width','28');icon.set('height','28')
            # Prefix icon IDs to prevent gradient/clip collisions in a composite.
            raw=ET.tostring(icon,encoding='unicode')
            for identifier in re.findall(r'id="([^"]+)"',raw):
                raw=raw.replace(f'id="{identifier}"',f'id="{slug}-{identifier}"').replace(f'#{identifier}',f'#{slug}-{identifier}')
            b+=rect(x,y,40,40,C['paper'])+raw+text(x+52,y+26,label,17)
            manifest.append({'name':label,'icon':slug,'domain':title})
        save(f'assets/technology/matrix-{num}.svg',svg(460,235,b,title+': '+', '.join(v for _,v in items),C['panel']))
    save('data/technologies.json',json.dumps(manifest,indent=2)+'\n')

def miscellany():
    for name,label in [('portfolio','01  PORTFOLIO ↗'),('repositories','02  REPOSITORIES ↗'),('linkedin','03  LINKEDIN ↗'),('cv','04  RESEARCH CV ↗'),('email','05  EMAIL ↗')]:
        b=rect(0,0,184,43,C['panel'],C['grid'])+rect(0,42,184,2,C['cyan'])+text(13,27,label,13,mono=True)
        save('assets/navigation/'+name+'.svg',svg(184,44,b,label))
    b=text(28,35,'04 / QUANTITATIVE LABORATORY',15,C['orange'],mono=True)+text(28,98,'UNCERTAINTY,',60,weight=900)+text(28,162,'MADE EXPLICIT.',60,weight=900)
    for k in range(7):
        pts=[(570+i*3,170-110*math.exp(-((i-55-k*3)/(18+k*3))**2)) for i in range(110)]
        b+=path(pts,C['orange'],1,.25+k*.1)
    b+=text(28,204,'RISK / REGIMES / EXECUTION',15,C['muted'],mono=True)+text(570,204,'GAUSSIAN STUDY · NOT MARKET DATA',11,C['muted'],mono=True)
    save('assets/research/quant.svg',svg(960,235,b,'Uncertainty, made explicit. Gaussian mathematical illustration, not market or strategy performance.'))
    b=text(28,32,'04 / QUANTITATIVE LABORATORY',13,C['orange'],mono=True)+text(25,95,'UNCERTAINTY,',45,weight=900)+text(25,150,'MADE EXPLICIT.',45,weight=900)
    for k in range(7):b+=path([(30+i*3.7,295-100*math.exp(-((i-55-k*3)/(18+k*3))**2)) for i in range(110)],C['orange'],1,.25+k*.1)
    b+=text(28,332,'GAUSSIAN STUDY / NOT MARKET DATA',12,C['muted'],mono=True)
    save('assets/research/quant-mobile.svg',svg(480,355,b,'Gaussian mathematical illustration; not measured strategy performance.'))
    for mobile in [False,True]:
        w,h=(480,530) if mobile else (960,430)
        b=text(28,35,'08 / COMPUTATIONAL FRONTIERS',14,C['lavender'],mono=True)
        b+=text(28,100,'Order from',48,weight=900)+text(28,155,'observation.',48,weight=900)
        b+=attractor(40 if mobile else 470,210 if mobile else 70,400 if mobile else 450,240 if mobile else 275,C['lavender'])
        if not mobile:
            b+=text(28,220,'Nonlinear dynamics.',21)+text(28,251,'Scientific machine learning.',21)+text(28,282,'Interpretable physical laws.',21)
        b+=text(28,h-45,'LORENZ / σ=10 / ρ=28 / β=8/3',14,C['lavender'],mono=True)+text(28,h-20,'RK4 · Δt=0.008 · X–Z PROJECTION',12,C['muted'],mono=True)
        save('assets/research/'+('frontiers-mobile' if mobile else 'frontiers')+'.svg',svg(w,h,b,'Research interests: nonlinear dynamics and learning physical laws. Numerically integrated Lorenz attractor.'))
    b=rect(0,0,460,8,C['cyan'])+text(28,49,'09 / END OF TRANSMISSION',13,C['ink'],mono=True)+text(25,112,'Understand',47,C['ink'],900)+text(25,166,'the abstraction.',47,C['ink'],900)+text(28,213,'Then build what lies beneath it.',23,C['ink'],700)+text(28,264,'ZYLUS / ENGINEERING AS INQUIRY',13,C['ink'],mono=True)
    save('assets/footer/signature.svg',svg(460,292,b,'Understand the abstraction. Then build what lies beneath it.',C['paper']))

def main():
    hero();hero(True);projects();technology();miscellany()
    print('Static assets generated')

if __name__=='__main__':main()
