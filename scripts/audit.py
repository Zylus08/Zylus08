"""Local release audit: workflow YAML, icon integrity, contrast and secret patterns."""
import hashlib,json,re,subprocess
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[1]

def luminance(hex):
    a=[int(hex[i:i+2],16)/255 for i in (1,3,5)]
    a=[v/12.92 if v<=.04045 else ((v+.055)/1.055)**2.4 for v in a]
    return sum(x*y for x,y in zip(a,[.2126,.7152,.0722]))

def main():
    workflows=[]
    for p in (ROOT/'.github/workflows').glob('*.yml'):
        obj=yaml.load(p.read_text(),Loader=yaml.BaseLoader)
        assert 'on' in obj and 'jobs' in obj and 'permissions' in obj and 'concurrency' in obj
        for job in obj['jobs'].values():
            assert 'timeout-minutes' in job
            for step in job['steps']:
                if 'uses' in step:assert re.search(r'@[0-9a-f]{40}$',step['uses'])
        workflows.append(p.name)
    manifest=json.loads((ROOT/'assets/technology/icons/manifest.json').read_text())
    for item in manifest:
        # Git normalizes SVG newlines; compare canonical LF to download bytes.
        data=(ROOT/f'assets/technology/icons/{item["name"]}.svg').read_bytes()
        assert hashlib.sha256(data).hexdigest()==item['sha256'],item['name']
    patterns=[r'gh[pousr]_[A-Za-z0-9]{30,}',r'github_pat_[A-Za-z0-9_]{40,}',r'AKIA[0-9A-Z]{16}',r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----']
    files=subprocess.check_output(['git','ls-files','--cached','--others','--exclude-standard'],cwd=ROOT).decode().splitlines()
    scanned=0
    for name in files:
        p=ROOT/name
        if not p.is_file() or p.suffix=='.png':continue
        s=p.read_text(encoding='utf-8');scanned+=1
        assert not any(re.search(pattern,s) for pattern in patterns),f'Credential pattern in {name}'
    colors=json.loads((ROOT/'config/design_tokens.json').read_text())['colors'];ratios={}
    for fg in ['paper','muted','cyan','blue','orange','lavender']:
        ratio=(luminance(colors[fg])+.05)/(luminance(colors['panel'])+.05)
        assert ratio>=4.5,(fg,ratio);ratios[fg]=round(ratio,2)
    report={'workflows_yaml_and_policy':workflows,'icons_hash_verified':len(manifest),'secret_pattern_files_scanned':scanned,'text_contrast_on_panel':ratios,'note':'Pattern scan is not proof of absence of every possible secret; YAML check is not an actionlint or live workflow result.'}
    (ROOT/'reports/audit-results.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
