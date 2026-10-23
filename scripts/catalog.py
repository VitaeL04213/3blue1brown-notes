"""Extract public lesson metadata; never execute downloaded JavaScript."""
from pathlib import Path
import re
import json
import hashlib
import sys
import urllib.request
import argparse
from datetime import date
sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser()
parser.add_argument('--refresh',action='store_true',help='Fetch the live official catalogue before extraction')
parser.add_argument('--snapshot-date',default='2026-10-24',help='Date of this metadata snapshot (YYYY-MM-DD)')
args=parser.parse_args()
asset_urls={'metadata_asset':'https://www.3blue1brown.com/assets/lessons-D6OVIHdp.js',
            'topic_asset':'https://www.3blue1brown.com/assets/Header-D97eyjMR.js'}
if args.refresh or not (ROOT/'build/lessons.js').exists():
    def get(url):
        return urllib.request.urlopen(url,timeout=60).read().decode('utf-8')
    base='https://www.3blue1brown.com'
    home=get(base+'/')
    route=re.search(r'/assets/Home-[\w-]+\.js',home)
    if not route: raise RuntimeError('Official site structure changed; review the extractor before continuing.')
    route_js=get(base+route[0])
    for stem,key,dest in [('lessons','metadata_asset','lessons.js'),('Header','topic_asset','Header.js')]:
        match=re.search(r'\./'+stem+r'-[\w-]+\.js',route_js)
        if not match: raise RuntimeError('Official site asset naming changed: '+stem)
        asset_urls[key]=base+'/assets/'+match[0][2:]
        target=ROOT/'build'/dest
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_text(get(asset_urls[key]),encoding='utf-8')
    if args.snapshot_date=='2026-10-24': args.snapshot_date=date.today().isoformat()
s = (ROOT / 'build/lessons.js').read_text(encoding='utf-8-sig')
header = (ROOT / 'build/Header.js').read_text(encoding='utf-8-sig')
modules = dict(re.findall(r'var ([\w$]+)=t\(\{default:\(\)=>[\w$]+,frontmatter:\(\)=>([\w$]+)\}\)', s))
paths = re.findall(r'"\./(\d{4})/([^/]+)/index\.mdx":([\w$]+)', s)
lessons = {}
for year, slug, module in paths:
    name = modules.get(module)
    if not name:
        continue
    m = re.search(re.escape(name) + r'=\{', s)
    if not m:
        continue
    end = s.find('};function', m.start())
    raw = s[m.start():end]
    d = dict(re.findall(r'(title|date|video|source):`((?:\\.|[^`])*)`', raw))
    chapter = re.search(r'chapter:([\d.]+)', raw)
    if chapter:
        d['chapter'] = float(chapter[1])
    d.update(slug=slug, year=int(year), url='https://www.3blue1brown.com/lessons/'+slug+'/')
    if d.get('video'):
        d['youtube'] = 'https://www.youtube.com/watch?v='+d['video']
    lessons[slug] = d
topics = {}
pattern = r'(?:"([\w-]+)"|([\w-]+)):\{title:`([^`]+)`,description:`([^`]+)`,lessons:\[([^\]]*)\]'
for m in re.finditer(pattern, header):
    key = m[1] or m[2]
    topics[key] = {'title':m[3], 'slugs': re.findall(r'`([^`]+)`',m[5])}
selected = ['linear-algebra','calculus','neural-networks','differential-equations','lockdown-math']
out = {'snapshot_date':args.snapshot_date,'catalog_url':'https://www.3blue1brown.com/',
       **asset_urls,
       'metadata_sha256':hashlib.sha256(s.encode()).hexdigest(),
       'scope':'Five course-style topic sequences on the official website, plus the explicitly numbered Compression & Intelligence series.',
       'courses':[]}
for key in selected:
    t=topics[key]
    out['courses'].append({'id':key,'title':t['title'],'lessons':[lessons[x] for x in t['slugs']]})
out['courses'].append({'id':'compression','title':'Compression & Intelligence',
                       'lessons':[lessons[x] for x in ['entropy','cross-entropy']]})
(ROOT/'build/all-metadata.json').write_text(json.dumps({'topics':topics,'lessons':lessons},ensure_ascii=False,indent=2),encoding='utf-8')
(ROOT/'sources/catalog.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
for c in out['courses']:
    print(c['id'],len(c['lessons']))
    for l in c['lessons']:
        print(' ',l['slug'],'|',l.get('chapter','-'),'|',l['title'])
