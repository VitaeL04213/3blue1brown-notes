"""Structural integrity checks, not a substitute for editorial/math review."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json, re

ROOT=Path(__file__).resolve().parents[1]
catalog=json.loads((ROOT/"sources/catalog.json").read_text(encoding="utf-8"))
lessons={l["slug"]:l for c in catalog["courses"] for l in c["lessons"]}
media=json.loads((ROOT/"media/teaching.json").read_text(encoding="utf-8"))
assert set(lessons)==set(media)
class Links(HTMLParser):
    def __init__(self):super().__init__();self.urls=[];self.videos=[];self.math=0
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        for a in ("href","src","poster"):
            if a in d:self.urls.append(d[a])
        if "data-video" in d:self.videos.append(d["data-video"])
        if tag=="math":self.math+=1
total_math=0
for page in (ROOT/"docs").rglob("*.html"):
    raw=page.read_text(encoding="utf-8")
    assert "<title>" in raw and 'lang="zh-CN"' in raw,page
    parser=Links();parser.feed(raw);total_math+=parser.math
    for url in parser.urls:
        u=urlsplit(url)
        if u.scheme or u.netloc or not u.path:continue
        target=(page.parent/unquote(u.path)).resolve()
        assert target.is_relative_to(ROOT/"docs"),f"Link escapes Pages root: {page}: {url}"
        assert target.exists(),f"Broken link: {page}: {url}"
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
    if lessons[slug].get("video"):
        assert lessons[slug]["video"] in (ROOT/f"docs/lessons/{slug}.html").read_text(encoding="utf-8")
assert len(list((ROOT/"docs/media").glob("*.mp4")))==9
assert len(list((ROOT/"docs/media").glob("*.gif")))==9
assert len(list((ROOT/"notes/figures").glob("*.png")))==9
assert total_math>500,total_math
print(json.dumps({"lessons":len(lessons),"rendered_math_expressions":total_math,
 "manim_animations":9,"broken_local_links":0,"unrendered_math":0}))
