"""Explicit maintenance command; pinned Devicon originals, MIT license."""
import json, urllib.request, hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
REV='32fe1d3b3f36ad11f90ab94f7db59738139c2bf6'
ICONS=['python','cplusplus','rust','go','cmake','docker','git','githubactions','pytorch','numpy','pandas','scikitlearn','react','vite','typescript','javascript']

def main():
    out=ROOT/'assets/technology/icons'; out.mkdir(parents=True,exist_ok=True)
    manifest=[]
    for name in ICONS:
        url=f'https://raw.githubusercontent.com/devicons/devicon/{REV}/icons/{name}/{name}-original.svg'
        data=urllib.request.urlopen(url,timeout=30).read()
        (out/(name+'.svg')).write_bytes(data)
        manifest.append({'name':name,'url':url,'sha256':hashlib.sha256(data).hexdigest()})
    data=urllib.request.urlopen(f'https://raw.githubusercontent.com/devicons/devicon/{REV}/LICENSE',timeout=30).read()
    (out/'LICENSE').write_bytes(data)
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print('Vendored',len(manifest),'icons at',REV)

if __name__=='__main__': main()
