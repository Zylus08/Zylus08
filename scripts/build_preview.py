"""Local GitHub-like layout approximation, not a claim of sanitizer equivalence."""
import markdown,subprocess
from visual import ROOT,save
CSS='''*{box-sizing:border-box}body{margin:0;font:16px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Arial,sans-serif;background:var(--bg);color:var(--fg)}article{max-width:1024px;margin:0 auto;padding:32px}img{max-width:100%;height:auto;vertical-align:middle}p{margin:0 0 20px}p:has(>a>img),p:has(>img){line-height:2}h2{font-size:24px;border-bottom:1px solid var(--border);padding-bottom:.3em;margin:32px 0 16px}a{color:var(--link);text-decoration:none}table{border-collapse:collapse}td,th{border:1px solid var(--border);padding:6px 13px}sub{font-size:12px}picture{display:block;margin-bottom:20px}body.light{--bg:#fff;--fg:#1f2328;--border:#d1d9e0;--link:#0969da}body.dark{--bg:#0d1117;--fg:#e6edf3;--border:#30363d;--link:#58a6ff}@media(max-width:600px){article{padding:16px}}'''

def main():
    before=subprocess.check_output(['git','show','fe017b6:README.md']).decode('utf-8')
    for name in ['banner','telemetry']:
        save('reports/preview/v1-'+name+'.svg',subprocess.check_output(['git','show',f'fe017b6:assets/{name}.svg']).decode('utf-8'))
        before=before.replace('assets/'+name+'.svg','reports/preview/v1-'+name+'.svg')
    for version,source in [('before',before),('after',(ROOT/'README.md').read_text(encoding='utf-8'))]:
        body=markdown.markdown(source,extensions=['tables'])
        for theme in ['light','dark']:
            html=f'<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><base href="{ROOT.as_uri()}/"><style>{CSS}</style><title>Zylus {version} / {theme} preview</title></head><body class="{theme}"><article>{body}</article></body></html>'
            save(f'reports/preview/{version}-{theme}.html',html)
    print('Local light/dark before/after previews built')

if __name__=='__main__':main()
