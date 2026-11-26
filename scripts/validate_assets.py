"""Structural release gates. Browser rendering is a separate, explicit QA step."""
import argparse,json,re,sys,xml.etree.ElementTree as ET
from pathlib import Path
from html.parser import HTMLParser
from fetch_github_data import validate_snapshot
ROOT=Path(__file__).resolve().parents[1]

def svg_check(p):
    raw=p.read_text(encoding='utf-8');r=ET.fromstring(raw)
    assert r.tag.endswith('svg'),p
    assert 'viewBox' in r.attrib,p
    assert not re.search(r'<(?:script|foreignObject)\b|onload=|javascript:|@import',raw,re.I),p
    assert not re.search(r'(?:href|src)=["\']https?://',raw),p
    assert not any(bad in raw for bad in ['Ã','â€','�']),f'Mojibake in {p}'

class References(HTMLParser):
    def __init__(self):super().__init__();self.paths=[]
    def handle_starttag(self,tag,attrs):
        a=dict(attrs)
        if tag=='img':assert a.get('alt','').strip(),'Missing image alternative'
        for attr in ['src','srcset','href']:
            if attr in a and not re.match(r'(https?:|mailto:|#)',a[attr]):self.paths.append(a[attr])

def check_telemetry(root):
    s=json.loads((root/'data/github_snapshot.json').read_text(encoding='utf-8'));validate_snapshot(s)
    for p in ['assets/telemetry/repositories.svg','assets/telemetry/activity.svg','assets/skyline/skyline.svg','assets/skyline/mobile.svg']:
        svg_check(root/p)
    assert (root/'data/telemetry.md').is_file()

def main():
    p=argparse.ArgumentParser();p.add_argument('--telemetry-root',type=Path);a=p.parse_args()
    if a.telemetry_root:check_telemetry(a.telemetry_root);print('Staged telemetry valid');return
    check_telemetry(ROOT)
    for path in (ROOT/'data').glob('*.json'):json.loads(path.read_text(encoding='utf-8'))
    assets=list((ROOT/'assets').rglob('*.svg'))
    for path in assets:svg_check(path)
    readme=(ROOT/'README.md').read_text(encoding='utf-8');refs=References();refs.feed(readme)
    for path in refs.paths:assert (ROOT/path).is_file(),f'Missing asset: {path}'
    for path in re.findall(r'\]\(([^)]+)\)',readme):
        if not re.match(r'(https?:|mailto:|#)',path):assert (ROOT/path).is_file(),path
    projects=json.loads((ROOT/'data/projects.json').read_text(encoding='utf-8'))
    public={r['html_url'] for r in json.loads((ROOT/'data/repositories.json').read_text(encoding='utf-8'))}
    assert all(p['url'] in public and p['evidence'] and p['limitation'] for p in projects)
    for name in ['Axiom','PRAXIS','FORGE','VECTRA']:assert (ROOT/f'assets/projects/{name}.svg').is_file()
    assert len(list((ROOT/'assets/technology').glob('matrix-*.svg')))==4
    size=sum(p.stat().st_size for p in assets)
    assert size<2_000_000,f'Asset budget exceeded: {size}'
    print(f'PASS: {len(assets)} SVGs; {len(refs.paths)} local HTML references; {len(projects)} evidenced projects; {size:,} SVG bytes')

if __name__=='__main__':main()
