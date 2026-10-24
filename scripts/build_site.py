"""Build HTML and PDF media links from shared TeX sources; pypandoc_binary==1.15."""
from pathlib import Path
import json, re, html, shutil
import pypandoc

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
BASE = "https://vitael04213.github.io/3blue1brown-notes"
CAT = json.loads((ROOT / "sources/catalog.json").read_text(encoding="utf-8"))
MEDIA = json.loads((ROOT / "media/teaching.json").read_text(encoding="utf-8"))
LESSONS = {l["slug"]: l for c in CAT["courses"] for l in c["lessons"]}
GROUPS = {
 "linear-algebra": ("线性代数", "从位移到矩阵，再到换基与特征方向。"),
 "calculus": ("微积分", "从局部变化到累积，以误差控制连接直觉与定义。"),
 "neural-networks": ("神经网络", "追踪计算、损失与梯度，走进注意力和生成模型。"),
 "differential-equations": ("微分方程", "用局部规则描述演化，用模式拆解复杂运动。"),
 "lockdown-math": ("基础数学", "重新连接代数、三角、复数、指数与对数。"),
 "compression": ("压缩与智能", "把概率转成编码长度，再理解模型失配的代价。")}
DEMO_NAMES = dict(linear="矩阵与面积", derivative="割线与切线", integral="累积与积分",
 gradient="学习率实验", attention="注意力权重", heat="傅里叶与热扩散",
 complex="复平面旋转", entropy="熵与交叉熵", taylor="泰勒近似")
SCENES = dict(linear="LinearMap", derivative="Derivative", integral="Integral",
 gradient="GradientDescent", attention="Attention", heat="FourierHeat",
 complex="ComplexRotation", entropy="Entropy", taylor="Taylor")
CAPTIONS = {
 "LinearMap": "剪切后的网格与单位方形。两列控制基向量去向；继续压扁时面积归零。",
 "Derivative": "平方函数的割线（黄）与切线（白色虚线）。非零步长缩小时，割线斜率趋向切线斜率。",
 "Integral": "平方函数的左端点矩形和。切分变细时，累积面积逐渐接近积分。",
 "GradientDescent": "二次损失上的更新轨迹；这里学习率为 0.2。网页可改用过大步长观察发散。",
 "Attention": "两个值的加权汇总。柱高表示权重，白点表示输出；这是标量玩具模型。",
 "FourierHeat": "周期边界下，低频（蓝）与高频（黄）以不同速度衰减，白线为总和。",
 "ComplexRotation": "单位圆上的位置（蓝）与切向速度方向（黄）；纯旋转保持模长。",
 "Entropy": "二元熵在公平概率处达到一位；接近确定事件时下降。",
 "Taylor": "指数函数（蓝）与逐阶泰勒多项式（黄）；精度需要结合离中心距离判断。"}

def esc(x):
    return html.escape(str(x), quote=True)

def write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")

def tex_html(tex):
    tex = re.sub(r"\{\\rm\s+([^}]+)\}", lambda m: "{\\mathrm{"+m[1]+"}}", tex)
    for key, val in {"R": r"\mathbb{R}", "C": r"\mathbb{C}", "dd": r"\,\mathrm{d}",
                     "e": r"\mathrm{e}", "ii": r"\mathrm{i}"}.items():
        tex = re.sub(r"\\" + key + r"\b", lambda _: val, tex)
    tex = re.sub(r"\\ref\{lesson:([^}]+)\}", r"\\href{\1.html}{对应课程}", tex)
    return pypandoc.convert_text(tex, "html5", format="latex", extra_args=["--mathml", "--wrap=none"])

entries = {}
for chapter in sorted((ROOT / "notes/chapters").glob("*.tex")):
    source = chapter.read_text(encoding="utf-8")
    matches = list(re.finditer(r"\\lesson\{([^}]+)\}\{([^}]+)\}\{([^}]+)\}", source))
    for i, match in enumerate(matches):
        slug, title, theorem = match.groups()
        body = source[match.end():matches[i+1].start() if i+1 < len(matches) else len(source)]
        body = body.split(r"\nextlesson")[0].strip()
        scope = re.search(r"\\leanpart\{(.*)\}\s*$", body, re.S)
        assert scope, slug
        recap = body[:scope.start()]
        for cmd, heading in {"idea":"要点回看", "mathpart":"数学表述", "examplepart":"完整算例",
                             "pitfall":"检查误区", "exercise":"自测与答案"}.items():
            recap = recap.replace("\\"+cmd, "\\subsection*{"+heading+"}")
        recap += "\n\\subsection*{Lean 证明与边界}\n" + scope[1]
        guide = (ROOT / f"notes/guides/{slug}.tex").read_text(encoding="utf-8")
        entries[slug] = {"title":title, "theorem":theorem, "chapter":chapter.stem,
                         "guide_html":tex_html(guide), "recap_html":tex_html(recap),
                         "guide_characters":len(re.findall(r"[\u4e00-\u9fff]", guide))}
assert set(entries) == set(LESSONS) == set(MEDIA)
for chapter_id in GROUPS:
    chapter_lessons=[s for s in LESSONS if entries[s]["chapter"]==chapter_id]
    review=(ROOT/f"notes/reviews/{chapter_id}.tex").read_text(encoding="utf-8")
    entries[chapter_lessons[-1]]["recap_html"]+=tex_html(review)
for name in SCENES.values():
    shutil.copy2(ROOT / f"notes/figures/{name}.png", DOCS / f"media/{name}.png")
    assert (DOCS / f"media/{name}.mp4").stat().st_size > 1000

def shell(title, body, prefix="", scripts=""):
    return f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)} · 3Blue1Brown 中文导学</title><meta name="description" content="通过引导推导、原课程视频、原创 Manim 动画与参数实验重建数学理解。">
<link rel="stylesheet" href="{prefix}assets/style.css"></head>
<body><a class="skip" href="#main">跳到正文</a>{body}
<footer>独立中文导学教材 · 原课程：Grant Sanderson / 3Blue1Brown 及署名合作者 ·
<a href="https://github.com/VitaeL04213/3blue1brown-notes">源码与 Lean 证明</a> ·
原创讲解与图示采用 MIT；外部原视频的权利归原作者。</footer>{scripts}</body></html>'''

nav = '<a href="../index.html">教材目录</a><a href="../lab.html">交互实验室</a><a href="https://raw.githubusercontent.com/VitaeL04213/3blue1brown-notes/main/dist/3blue1brown-notes-zh.pdf">下载 PDF</a>'
ordered = list(LESSONS)
for n, slug in enumerate(ordered):
    entry, lesson, cfg = entries[slug], LESSONS[slug], MEDIA[slug]
    prompt, demo = cfg[0], cfg[1] if len(cfg)>1 else None
    vid = lesson.get("video")
    assert not vid or re.fullmatch(r"[A-Za-z0-9_-]{11}", vid), f"Invalid official video: {slug}"
    video = f'''<section class="media-panel" aria-label="原课程视频">
<h2>带着问题看原课</h2><p>{esc(prompt)}</p>
<p><a href="{esc(lesson.get('youtube',''))}" target="_blank" rel="noopener">在 YouTube 打开原视频 ↗</a> ·
<a href="{esc(lesson['url'])}" target="_blank" rel="noopener">官方课程页面 ↗</a></p>
<button class="load-video" data-video="{vid}">加载原课程播放器</button>
<div class="embed-slot"></div><small>点击后加载 YouTube 播放器，需要网络；若无法播放，可使用上方原链接。</small></section>''' if vid else f'''<section class="media-panel"><h2>带着问题读原课</h2><p>{esc(prompt)}</p><p><a href="{esc(lesson['url'])}" target="_blank" rel="noopener">打开官方图文与图示 ↗</a></p><small>官方目录未给本条目单列视频 ID；这里直接引用官方图文课，不另造视频对应关系。</small></section>'''
    experiment = ""
    if demo:
        scene = SCENES[demo]
        experiment = f'''<section class="media-panel"><h2>先预测，再动手验证</h2>
<p><a class="button" href="../lab.html#{demo}">打开 {DEMO_NAMES[demo]} →</a></p>
<h3>原创 Manim 动画</h3>
<video controls playsinline preload="none" poster="../media/{scene}.png" aria-label="{esc(CAPTIONS[scene])}">
<source src="../media/{scene}.mp4" type="video/mp4">请使用支持 MP4 的浏览器。</video>
<p class="caption">{esc(CAPTIONS[scene])} 无音频；画面中的文字与此说明提供等价信息。</p>
<a href="../media/{scene}.mp4" download>下载 MP4</a> · <a href="../media/{scene}.gif" download>下载 GIF 动图</a></section>'''
    prev = f'<a href="{ordered[n-1]}.html">← {esc(entries[ordered[n-1]]["title"])}</a>' if n else ""
    nxt = f'<a href="{ordered[n+1]}.html">{esc(entries[ordered[n+1]]["title"])} →</a>' if n+1<len(ordered) else ""
    theorem = entry["theorem"]
    proof = ("公告页不设数学命题" if theorem == "not-applicable" else
             f'<a href="https://github.com/VitaeL04213/3blue1brown-notes/blob/main/ThreeBlueOneBrown/{theorem.split(".")[0]}.lean">{esc(theorem)}</a>')
    body = f'''<header class="topbar"><a class="brand" href="../index.html">3B1B <span>中文导学</span></a><nav>{nav}</nav></header>
<main id="main" class="reading"><div class="eyebrow">{esc(GROUPS[entry["chapter"]][0])} / {n+1:02d}</div>
<h1>{esc(entry["title"])}</h1><p class="lead">{esc(prompt)}</p>
<article>{entry["guide_html"]}</article>{experiment}{video}
<article>{entry["recap_html"]}</article><p class="proof-link">证明源码：{proof}</p>
<nav class="pagination">{prev}{nxt}</nav></main>'''
    write(DOCS / f"lessons/{slug}.html", shell(entry["title"], body, "../",
        '<script src="../assets/reader.js" defer></script>'))
    tex = "\\begin{quote}\\small\\textbf{观课提示}\\quad "+prompt+"\n\n"
    tex += "\\href{"+lesson.get("youtube",lesson["url"])+"}{"+("原课程视频" if vid else "官方图文课程")+"}\\quad\\href{"+BASE+"/lessons/"+slug+".html}{本节网页与媒体}"
    if demo: tex += "\\quad\\href{"+BASE+"/lab.html\\#"+demo+"}{参数实验}"
    tex += "\n\\end{quote}\n"
    if len(cfg)>2:
        scene=cfg[2]
        tex += ("\\begin{figure}[htbp]\\centering\n\\includegraphics[width=0.98\\linewidth]{figures/"+scene+".png}\n"
                "\\caption{"+CAPTIONS[scene]+"本项目原创 Manim 动画关键帧；完整动画与操作入口见本节网页。}\n\\end{figure}\n")
    write(ROOT / f"notes/media/{slug}.tex", tex)

sections = []
for cid, (name, desc) in GROUPS.items():
    slugs = [s for s in ordered if entries[s]["chapter"] == cid]
    if cid=="neural-networks":
        slugs.insert(slugs.index("diffusion-models"),"cross-entropy")
    links = "".join(f'<li><a href="lessons/{s}.html">{esc(entries[s]["title"])}</a></li>' for s in slugs)
    sections.append(f'<section class="course"><h2>{name}</h2><p>{desc}</p><ol>{links}</ol></section>')
body = f'''<header class="topbar"><a class="brand" href="index.html">3B1B <span>中文导学</span></a><nav>
<a href="lab.html">交互实验室</a><a href="https://raw.githubusercontent.com/VitaeL04213/3blue1brown-notes/main/dist/3blue1brown-notes-zh.pdf">下载 PDF</a>
<a href="https://github.com/VitaeL04213/3blue1brown-notes">GitHub</a></nav></header>
<main id="main"><section class="hero"><div class="eyebrow">从看懂，到自己推出来</div>
<h1>把数学直觉<br>连成一条推理的路。</h1>
<p>从问题开始，跟随图像与文字一步步建立概念，再用算例、练习和 Lean 命题检查理解。</p>
<a class="button" href="lessons/vectors.html">开始阅读 →</a> <a class="text-link" href="lab.html">先做一个实验</a>
<div class="stats"><span><b>6</b> 组课程</span><span><b>66</b> 个条目</span><span><b>9</b> 组动画与实验</span><span><b>67</b> 个 Lean 定理</span></div></section>
<section class="reading-guide"><h2>一节课，四次主动思考</h2><p>先阅读问题与引导推导；暂停并预测图形会怎样变化；观看原课或调整实验参数；最后遮住答案完成自测，再检查形式化命题的条件。</p>
<p>本书依据课程主题独立组织中文讲解、例子与推导，不是逐字字幕译文。官方目录快照为 2026-10-24；交叉熵在两组课程中共享，公告页作为导读。Lean 只覆盖逐课标明的命题。</p></section>
<div class="course-grid">{''.join(sections)}</div></main>'''
write(DOCS/"index.html",shell("从直觉到证明",body))
write(DOCS/".nojekyll","")
write(ROOT/"validation/textbook-structure.json",json.dumps({
 "lesson_pages":len(entries),"guides":len(entries),"original_video_links":sum(bool(l.get("video")) for l in LESSONS.values()),
 "manim_animations":len(SCENES),"interactive_experiments":len(SCENES),
 "guided_prose_characters":sum(e["guide_characters"] for e in entries.values()),
 "minimum_guided_prose_characters":min(e["guide_characters"] for e in entries.values()),
 "per_lesson":{s:e["guide_characters"] for s,e in entries.items()},
},ensure_ascii=False,indent=2)+"\n")
print(f"Built {len(entries)} reading pages, PDF media links, and index.")
