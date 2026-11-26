"""Explicit live link audit. Does not run during offline asset generation."""
import concurrent.futures,json,urllib.request,urllib.error
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]

def check(url):
    try:
        req=urllib.request.Request(url,headers={'User-Agent':'Zylus-profile-link-audit'})
        with urllib.request.urlopen(req,timeout=30) as r:
            return {'url':url,'status':r.status,'destination':r.url}
    except urllib.error.HTTPError as e:return {'url':url,'status':e.code,'note':'HTTP response; may be access protection rather than a missing destination'}
    except (urllib.error.URLError,TimeoutError,OSError):return {'url':url,'status':None,'note':'Network verification unavailable'}

def main():
    urls=[p['url'] for p in json.loads((ROOT/'data/projects.json').read_text(encoding='utf-8'))]
    urls+=['https://github.com/Zylus08/Fault-tolerant-Compute-Scheduler','https://sakshamkumarmishra.cv','https://sakshamkumarmishra.cv/documents/Saksham_Mishra_CV.pdf','https://www.linkedin.com/in/saksham-mishra-ml/']
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:results=list(pool.map(check,urls))
    (ROOT/'reports/link-results.json').write_text(json.dumps(results,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps(results,indent=2))

if __name__=='__main__':main()
