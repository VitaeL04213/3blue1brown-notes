"""Cache official lesson pages for review; caches are excluded from Git."""
import concurrent.futures
import json
import re
import sys
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path(__file__).resolve().parents[1]
class Text(HTMLParser):
    def __init__(self):
        super().__init__(); self.skip=0; self.chunks=[]
    def handle_starttag(self,tag,attrs):
        if tag in ('script','style','svg'): self.skip+=1
        if tag in ('p','h1','h2','h3','li','br'): self.chunks.append('\n')
    def handle_endtag(self,tag):
        if tag in ('script','style','svg'): self.skip-=1
    def handle_data(self,data):
        if not self.skip: self.chunks.append(data)
def fetch(l):
    path=ROOT/'build/source-text'/f"{l['slug']}.txt"
    path.parent.mkdir(parents=True,exist_ok=True)
    try:
        raw=urllib.request.urlopen(l['url'],timeout=45).read().decode('utf-8')
        p=Text(); p.feed(raw)
        text='\n'.join(x.strip() for x in ''.join(p.chunks).splitlines() if x.strip())
        path.write_text(text,encoding='utf-8')
        return {'slug':l['slug'],'url':l['url'],'ok':True,'characters':len(text),'review_basis':'official page and independently derived mathematics'}
    except Exception as e:
        return {'slug':l['slug'],'url':l['url'],'ok':False,'error':str(e)}
catalog=json.loads((ROOT/'sources/catalog.json').read_text(encoding='utf-8'))
lessons={l['slug']:l for c in catalog['courses'] for l in c['lessons']}
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
    results=list(pool.map(fetch,lessons.values()))
(ROOT/'sources/retrieval.json').write_text(json.dumps({'retrieved':'2026-10-24','pages':results},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('retrieved',sum(x['ok'] for x in results),'/',len(results))
for x in results:
    if not x['ok']: print(x)
