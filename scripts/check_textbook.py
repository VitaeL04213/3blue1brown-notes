"""Structural integrity checks, not a substitute for editorial/math review."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json, re
from walkthroughs import STEPS, EXPERIMENTS, PRINCIPLES

ROOT=Path(__file__).resolve().parents[1]
catalog=json.loads((ROOT/"sources/catalog.json").read_text(encoding="utf-8"))
lessons={l["slug"]:l for c in catalog["courses"] for l in c["lessons"]}
media=json.loads((ROOT/"media/teaching.json").read_text(encoding="utf-8"))
assert set(lessons)==set(media)
class Links(HTMLParser):
    def __init__(self):super().__init__();self.urls=[];self.videos=[];self.math=0;self.ids=set();self.turns={}
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if "id" in d:
            assert d["id"] not in self.ids,f"Duplicate anchor: {d['id']}"
            self.ids.add(d["id"])
        if d.get("rel") in ("prev","next"):self.turns[d["rel"]]=d["href"]
        for a in ("href","src","poster","data-src"):
            if a in d:self.urls.append(d[a])
        if "data-video" in d:self.videos.append(d["data-video"])
        if tag=="math":self.math+=1
total_math=0
pages={}
for page in (ROOT/"docs").rglob("*.html"):
    parser=Links();parser.feed(page.read_text(encoding="utf-8"));pages[page.resolve()]=parser
for page in (ROOT/"docs").rglob("*.html"):
    raw=page.read_text(encoding="utf-8")
    assert "<title>" in raw and 'lang="zh-CN"' in raw,page
    parser=pages[page.resolve()];total_math+=parser.math
    for url in parser.urls:
        u=urlsplit(url)
        if u.scheme or u.netloc:continue
        target=(page.parent/unquote(u.path)).resolve() if u.path else page.resolve()
        assert target.is_relative_to(ROOT/"docs"),f"Link escapes Pages root: {page}: {url}"
        assert target.exists(),f"Broken link: {page}: {url}"
        if u.fragment and target.suffix==".html":
            fragment=unquote(u.fragment)
            dynamic_lab=target.name=="lab.html" and fragment in EXPERIMENTS
            assert dynamic_lab or fragment in pages[target].ids,f"Broken anchor: {page}: {url}"
    for video in parser.videos:assert re.fullmatch(r"[A-Za-z0-9_-]{11}",video)
    assert not re.search(r'<span class="math[^"]*">\\[([]',raw),"Unrendered TeX: "+str(page)
for slug in lessons:
    guide=ROOT/f"notes/guides/{slug}.tex"
    text=guide.read_text(encoding="utf-8")
    assert len(re.findall(r"[\u4e00-\u9fff]",text))>=300,slug
    assert text.count(r"\subsection*")>=2,slug
    assert len(text.split("\n\n"))>=4,slug
    assert (ROOT/f"notes/media/{slug}.tex").exists()
    assert (ROOT/f"docs/lessons/{slug}.html").exists()
    data=STEPS[slug]
    assert len(data['steps'])==3 and len(data['presets'])==3,slug
    assert all(p in EXPERIMENTS[data['demo']]['presets'] for p in data['presets']),slug
    assert all(len(re.findall(r'[\u4e00-\u9fff]',text))>=60 for _,text in data['steps']),slug
    assert (ROOT/f'notes/intuition/{slug}.tex').exists(),slug
    raw=(ROOT/f'docs/lessons/{slug}.html').read_text(encoding='utf-8')
    assert raw.count('class="step-play"')==3 and raw.count('id="experiment-root"')==1,slug
    assert 'iframe class="inline-lab"' not in raw,slug
    if lessons[slug].get("video"):
        assert lessons[slug]["video"] in (ROOT/f"docs/lessons/{slug}.html").read_text(encoding="utf-8")
assert len(list((ROOT/"docs/media").glob("*.mp4")))==9
assert len(list((ROOT/"docs/media").glob("*.gif")))==9
assert len(list((ROOT/"notes/figures").glob("*.png")))==9
assert total_math>500,total_math
assert len(list((ROOT/"docs/chapters").glob("*.html")))==6
current=(ROOT/"docs/index.html").resolve();visited=[]
while True:
    assert current not in visited,"Navigation cycle"
    visited.append(current)
    following=pages[current].turns.get("next")
    if not following:break
    target=(current.parent/following).resolve()
    assert (target.parent/pages[target].turns["prev"]).resolve()==current,"Previous/next mismatch"
    current=target
assert len(visited)==74 and current.name=="references.html",len(visited)
assert sum(p.parent.name=="lessons" for p in visited)==66
index=json.loads((ROOT/"docs/assets/search-index.js").read_text(encoding="utf-8").removeprefix("window.BookSearch = ").strip().removesuffix(";"))
assert len(index)==66 and len({entry['number'] for entry in index})==66
assert {entry['slug']:entry['number'] for entry in index}['entropy']=='6.1'
assert {entry['slug']:entry['number'] for entry in index}['cross-entropy']=='6.2'
print(json.dumps({"lessons":len(lessons),"rendered_math_expressions":total_math,
 "manim_animations":9,"interactive_experiments":len(EXPERIMENTS),"linked_steps":sum(len(s['steps']) for s in STEPS.values()),
 "paper_arguments":len(PRINCIPLES),"broken_local_links":0,"unrendered_math":0,"continuous_reading_pages":len(visited)}))
