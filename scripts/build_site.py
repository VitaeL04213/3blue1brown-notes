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
    markup=pypandoc.convert_text(tex, "html5", format="latex", extra_args=["--mathml", "--wrap=none"])
    return re.sub(r'(<math display="inline".*?</math>)',r'<span class="math-inline">\1</span>',markup,flags=re.S)

from book_layout import shell as book_shell, REPO, PDF
from experiment_layout import widget, scripts as experiment_scripts
from walkthroughs import STEPS, EXPERIMENTS, PRINCIPLES, compose as compose_walkthrough
BOOK = json.loads((ROOT / "notes/book.json").read_text(encoding="utf-8"))

def plain(markup):
    markup = re.sub(r"<annotation\b[^>]*>.*?</annotation>", "", markup, flags=re.S)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", markup))).strip()

def split_exercise(tex):
    for match in re.finditer(r"[？?。]",tex):
        before=tex[:match.end()]
        if len(re.findall(r"(?<!\\)\$",before))%2==0 and before.count(r"\[")==before.count(r"\]"):
            if tex[match.end():].strip():
                return before,tex[match.end():].strip()
    return "先独立完成下面的自测，再展开核对。",tex

entries = {}
for chapter in sorted((ROOT / "notes/chapters").glob("*.tex")):
    source=chapter.read_text(encoding="utf-8")
    matches=list(re.finditer(r"\\lesson\{([^}]+)\}\{([^}]+)\}\{([^}]+)\}",source))
    for i,m in enumerate(matches):
        slug,title,theorem=m.groups()
        body=source[m.end():matches[i+1].start() if i+1<len(matches) else len(source)].split(r"\nextlesson")[0].strip()
        scope=re.search(r"\\leanpart\{(.*)\}\s*$",body,re.S)
        assert scope,slug
        chunks=re.split(r"\\(idea|mathpart|examplepart|pitfall|exercise)\b",body[:scope.start()])
        parts={chunks[j]:chunks[j+1].strip() for j in range(1,len(chunks),2)}
        assert len(parts)==5,slug
        guide=(ROOT/f"notes/guides/{slug}.tex").read_text(encoding="utf-8")
        question,answer=split_exercise(parts["exercise"])
        entries[slug]={"title":title,"theorem":theorem,"chapter":chapter.stem,
                       "guide_html":tex_html(guide),"parts":{k:tex_html(v) for k,v in parts.items()},
                       "question":tex_html(question),"answer":tex_html(answer),"scope":tex_html(scope[1]),
                       "guide_characters":len(re.findall(r"[\u4e00-\u9fff]",guide))}
assert set(entries)==set(LESSONS)==set(MEDIA)==set(STEPS)
chapter_slugs={cid:[s for s in entries if entries[s]["chapter"]==cid] for cid in GROUPS}
ordered=[]
for c,(cid,slugs) in enumerate(chapter_slugs.items(),1):
    for s,slug in enumerate(slugs,1):entries[slug]["number"]=f"{c}.{s}"
    ordered.extend(slugs)

sequence=[("index.html","扉页与阅读说明")]
for i,(cid,slugs) in enumerate(chapter_slugs.items(),1):
    sequence.append((f"chapters/{cid}.html",f"第 {i} 章　{GROUPS[cid][0]}"))
    sequence.extend((f"lessons/{s}.html",entries[s]["number"]+"　"+entries[s]["title"]) for s in slugs)
sequence.append(("references.html","来源与证明范围"))

def render(path,title,body,current,prefix="",kind="front",toc="",scripts=""):
    position=next((i for i,pair in enumerate(sequence) if pair[0]==path),None)
    prev=sequence[position-1] if position is not None and position>0 else None
    nxt=sequence[position+1] if position is not None and position+1<len(sequence) else None
    write(DOCS/path,book_shell(title,body,GROUPS,entries,chapter_slugs,prefix,current,prev,nxt,kind,scripts,toc))

def permalink(target):
    return f'<a class="permalink" href="#{target}" aria-label="本段永久链接">¶</a>'

def section_title(number,title,target):
    return f'<h2 id="{target}"><span class="section-number">{number}</span> {title}{permalink(target)}</h2>'

def proof_block(entry):
    name=entry["theorem"]
    if name=="not-applicable":return '<section class="remark" id="proof"><h3>阅读说明</h3>'+entry["scope"]+'</section>'
    module,theorem=name.split(".",1)
    source=(ROOT/f"ThreeBlueOneBrown/{module}.lean").read_text(encoding="utf-8")
    match=re.search(r"^theorem "+re.escape(theorem)+r"\b.*?(?=\n(?:theorem |end |/\*|/--|/-)|\Z)",source,re.M|re.S)
    assert match,name
    line=source[:match.start()].count("\n")+1
    return f'''<details class="knowl proof" id="proof" data-print-open><summary>Lean 对照 {entry["number"]}.1 <span>命题、证明与适用边界</span></summary>
<div class="knowl-content">{entry["scope"]}<p class="proof-name">{esc(name)}</p><pre><code class="language-lean">{esc(match[0].strip())}</code></pre>
<p><a href="{REPO}/blob/main/ThreeBlueOneBrown/{module}.lean#L{line}">查看完整定义与上下文 ↗</a> · <a href="../references.html#formalization">全书证明范围</a></p></div></details>'''

search=[]
for slug in ordered:
    entry,lesson,cfg=entries[slug],LESSONS[slug],MEDIA[slug]
    number=entry["number"]; cid=entry["chapter"]; prompt=cfg[0]; demo=STEPS[slug]['demo']
    walkthrough,principle,intuition_tex=compose_walkthrough(slug,entries,tex_html)
    write(ROOT/f"notes/intuition/{slug}.tex",intuition_tex)
    vid=lesson.get("video"); assert not vid or re.fullmatch(r"[A-Za-z0-9_-]{11}",vid)
    headings=[]
    def numbered_heading(match):
        index=len(headings)+1; anchor=f"idea-{index}"; title=plain(match[1]);headings.append((anchor,title))
        return section_title(f"{number}.{index}",title,anchor)
    guide=re.sub(r'<h2\b[^>]*>(.*?)</h2>',numbered_heading,entry["guide_html"],flags=re.S)
    video=f'''<p>{esc(prompt)}</p><p><a href="{esc(lesson['url'])}" target="_blank" rel="noopener">官方课程与图示 ↗</a>'''
    if vid:
        video+=f''' · <a href="{esc(lesson['youtube'])}" target="_blank" rel="noopener">原视频 ↗</a></p><button class="load-video" data-video="{vid}">加载原课程播放器</button><div class="embed-slot"></div><p class="caption">点击后连接 YouTube；播放器不可用时可通过上方原链接观看。</p>'''
    else:video+='</p><p class="caption">本条目在官方目录中未单列视频，参照上述官方图文阅读。</p>'
    media=f'<details class="knowl original-course" id="original"><summary>原课对照 <span>观课问题、视频与图示</span></summary><div class="knowl-content">{video}</div></details>'
    initial=EXPERIMENTS[demo]['presets'][STEPS[slug]['presets'][0]]
    experiment=widget(demo,EXPERIMENTS[demo],'../',number,initial)
    parts=entry["parts"]
    related=''
    if slug in ('gradient-descent','backpropagation','gpt','diffusion-models'):
        related='<p class="related-reading">延伸阅读：<a href="cross-entropy.html">6.2 交叉熵</a>解释概率模型的训练代价。</p>'
    if slug=='cross-entropy':
        related='<p class="related-reading">本节也属于神经网络的延伸阅读，可结合<a href="gradient-descent.html">3.2 梯度下降</a>理解训练目标。</p>'
    body=f'''<div class="breadcrumbs"><a href="../index.html">本书</a><span>›</span><a href="../chapters/{cid}.html">第 {number.split('.')[0]} 章　{GROUPS[cid][0]}</a></div>
<header class="section-header"><p class="section-label">第 {number} 节</p><h1><span>{number}</span> {esc(entry["title"])}</h1><p class="section-intro">{esc(prompt)}</p></header>
<div class="section-tools"><a href="#example">例题</a><a href="#exercise">练习</a><a href="#proof">Lean 对照</a><a href="#original">原课</a><button class="expand-knowl" aria-pressed="false">展开本节例题与解答</button></div>
<div class="lesson-grid"><div class="reading-column"><article class="lesson-prose">{walkthrough}{guide}{principle}
<section class="statement" id="statement"><h3>数学表述 {number}.1{permalink("statement")}</h3>{parts["idea"]}{parts["mathpart"]}</section>
<details class="knowl example" id="example" data-print-open><summary>例 {number}.1 <span>把概念用于具体计算</span></summary><div class="knowl-content">{parts["examplepart"]}</div></details>
<aside class="remark" id="pitfall"><h3>辨析 {number}.1</h3>{parts["pitfall"]}</aside>
<section class="exercise" id="exercise"><h3>练习 {number}.1{permalink("exercise")}</h3>{entry["question"]}<details class="knowl solution" data-print-open><summary>展开解答与检查</summary><div class="knowl-content">{entry["answer"]}</div></details></section>
{proof_block(entry)}{related}{media}</article></div><aside class="experiment-pane" id="interactive" aria-label="本节同步实验">{experiment}<a class="return-step" href="#walkthrough">返回文字讲解 ↓</a></aside></div>'''
    items=headings+([("interactive","交互图")] if demo else [])+[("statement","数学表述"),("example","例题"),("exercise","练习"),("proof","Lean 对照"),("original","原课对照")]
    local='<nav class="page-outline" aria-label="本节导航"><h2>本节内容</h2>'+''.join(f'<a href="#{a}">{esc(t)}</a>' for a,t in items)+'</nav>'
    render(f"lessons/{slug}.html",number+" "+entry["title"],body,slug,"../","lesson",local,scripts=experiment_scripts('../'))
    search.append({"slug":slug,"number":number,"title":entry["title"],"chapter":GROUPS[cid][0],"english":lesson["title"],
                   "text":plain(walkthrough+entry["guide_html"]+principle+''.join(parts.values())+entry["scope"])})
    # Keep the PDF's media fragments stable; webpage and PDF share the same TeX prose.
    tex="\\begin{quote}\\small\\textbf{观课提示}\\quad "+prompt+"\n\n"
    tex+="\\href{"+lesson.get("youtube",lesson["url"])+"}{"+("原课程视频" if vid else "官方图文课程")+"}\\quad\\href{"+BASE+"/lessons/"+slug+".html}{本节网页与媒体}"
    if demo:tex+="\\quad\\href{"+BASE+"/lab.html\\#"+demo+"}{参数实验}"
    tex+="\n\\end{quote}\n"
    if len(cfg)>2:
        scene=cfg[2]
        tex+=("\\begin{figure}[htbp]\\centering\n\\includegraphics[width=0.98\\linewidth]{figures/"+scene+".png}\n"
              "\\caption{"+CAPTIONS[scene]+"本项目原创 Manim 动画关键帧；完整动画与操作入口见本节网页。}\n\\end{figure}\n")
    write(ROOT/f"notes/media/{slug}.tex",tex)

def contents_list(cid,prefix=''):
    links=''.join(f'<li><a href="{prefix}lessons/{s}.html"><span>{entries[s]["number"]}</span>{esc(entries[s]["title"])}</a></li>' for s in chapter_slugs[cid])
    return '<ol class="section-list">'+links+'</ol>'

for i,(cid,(name,desc)) in enumerate(GROUPS.items(),1):
    meta=BOOK[cid]
    review=tex_html((ROOT/f"notes/reviews/{cid}.tex").read_text(encoding="utf-8"))
    review=re.sub(r'<h1\b[^>]*>(.*?)</h1>',r'<h2>\1</h2>',review)
    related='<p class="related-reading">本章也参照 <a href="../lessons/cross-entropy.html">6.2 交叉熵</a>，共用第六章的完整讲解。</p>' if cid=='neural-networks' else ''
    body=f'''<div class="breadcrumbs"><a href="../index.html">本书</a><span>›</span>第 {i} 章</div><header class="section-header"><p class="section-label">第 {i} 章</p><h1>{name}</h1><p class="chapter-subtitle">{meta["subtitle"]}</p></header>
<article class="chapter-introduction">{''.join('<p>'+esc(p)+'</p>' for p in meta['paragraphs'])}<div class="objectives"><h2>本章学习目标</h2><ul>{''.join('<li>'+esc(g)+'</li>' for g in meta['goals'])}</ul><p><strong>准备知识：</strong>{esc(meta['prerequisites'])}</p></div>
<h2 id="sections">本章各节{permalink("sections")}</h2>{contents_list(cid,'../')}{related}
<section class="chapter-review" id="review">{review}</section></article>'''
    render(f"chapters/{cid}.html",f"第 {i} 章 {name}",body,cid,"../","chapter")

chapter_rows=''.join(f'<li><a href="chapters/{cid}.html"><span>第 {i} 章</span><strong>{name}</strong><small>{BOOK[cid]["subtitle"]}</small></a></li>' for i,(cid,(name,_)) in enumerate(GROUPS.items(),1))
front=f'''<section class="titlepage"><p class="book-kicker">一本可以阅读、操作与验证的数学教材</p><h1>从直觉到证明</h1><p class="book-subtitle">3Blue1Brown 官方课程序列 · 中文导学教材</p><p class="book-edition">LaTeX · Lean · Manim</p><div class="title-rule"></div><p class="book-description">从向量与变化出发，连接微积分、神经网络与数学建模。<br>让一幅图引出一个问题，让一段推导回答它。</p><p class="cover-actions"><a class="primary-link" href="chapters/linear-algebra.html">开始阅读第一章 →</a><a id="resume-reading" hidden>继续上次阅读</a></p><p class="edition-note">课程目录快照：2026 年 10 月 24 日 · 独立编写，非官方译本</p></section>
<section class="front-section" id="reading"><h2>如何阅读这本书</h2><p>先沿着正文中的问题推进，尝试在下一段揭示结果前完成推理。遇到交互图，先预测参数改变后的现象，再动手检验。例题、练习解答与 Lean 证明可按需展开；这让阅读、练习和核对各有自己的节奏。</p><p>左侧目录显示全书六章，页首与页末可以连续翻页。检索框支持中文概念与原课英文标题。正文中的编号和段落链接可以直接引用；手机上使用“目录与搜索”打开导航。</p><p>初学者可先从第五章补齐代数、三角与复数，再依次学习第一、二章。已经掌握这些基础的读者可以直入第三、四章，遇到交叉熵时转到第六章。</p></section>
<section class="front-section"><h2>全书六章</h2><ol class="chapter-list">{chapter_rows}</ol><p><a href="contents.html">查看展开的完整目录 →</a></p></section>
<section class="front-section"><h2>图像、论述与证明</h2><p>66 个独立课程条目共用 LaTeX 正文，配有 198 段逐步讲解、18 类可操作实验和 9 组原创 Manim 动画。宽屏左侧阅读，右侧同步操作；点击每一步的演示按钮，图形便回到对应情形。原课程通过 61 个视频入口与 5 个图文入口引用。交叉熵统一在第 6.2 节讲解。</p><p>18 组定义、命题与纸笔证明把观察连接到推理。67 个 Lean 命题的形式化范围在各节另行标明；新增纸笔论证没有自动获得 Lean 校验。<a href="references.html">阅读来源与证明范围</a>。</p><p class="design-credit">写作组织参考 <a href="https://ladr.pretext.plus/frontmatter.html">Linear Algebra Done Right</a> 的定义、命题与证明结构；交互形式参考 <a href="https://github.com/VitaeL04213/gt-linalg">gt-linalg</a> 的向量拖拽、输入输出视图及参数控制。章节导航继续参考 <a href="https://textbooks.math.gatech.edu/ila/">Interactive Linear Algebra</a>。内容与图形程序独立编写。</p></section>'''
render("index.html","扉页与阅读说明",front,"index")
toc='<header class="section-header"><p class="section-label">全书目录</p><h1>从直觉到证明</h1><p>按章展开的完整阅读路径。每一节同时保留原课程入口与证明对照。</p></header>'
for i,(cid,(name,_)) in enumerate(GROUPS.items(),1):
    toc+=f'<section class="contents-chapter"><h2><a href="chapters/{cid}.html">第 {i} 章　{name}</a></h2>{contents_list(cid)}</section>'
render("contents.html","全书目录",toc,"contents")
references=f'''<header class="section-header"><p class="section-label">附录</p><h1>来源、证明范围与许可</h1></header><article>
<h2 id="sources">原课程与编写方式</h2><p>本书围绕 <a href="https://www.3blue1brown.com/">3Blue1Brown</a> 的官方课程序列独立组织中文讲解、例子与推导。原作者为 Grant Sanderson 与署名合作者；扩散模型客座课程署名 Stephen Welch / Welch Labs。</p><p>每节“原课对照”保留对应的官方页面、视频和观课问题。未单列视频的条目直接链接官方图文，不另造视频对应关系。原视频按需连接外部播放器；教材正文、原创动画和实验可随仓库离线阅读。</p>
<h2 id="formalization">Lean 证明的范围</h2><p>65 节数学课有形式化对照，公告页作为导读。67 个命名定理经过 Lean 检查，没有未完成证明或自设公理。某些命题是一般定理，某些是局部恒等式或特例；每节展开框明确说明已经证明什么，以及哪些内容仍是纸笔推导。</p><p>例如幂塔命题说明收敛时的极限满足不动点条件，不独自保证迭代收敛；热方程的有限模式计算不替代任意初值的存在性或傅里叶收敛理论。网络机制的代数关系也不等于对生成质量和泛化能力的保证。</p><p><a href="{REPO}/blob/main/FORMALIZATION.md">逐课形式化清单</a> · <a href="{REPO}/blob/main/VALIDATION.md">验证记录</a> · <a href="{REPO}/actions">自动构建结果</a></p>
<h2 id="editions">网页与 PDF</h2><p>网页把教材组织成六章与连续编号的小节。宽屏使用左文右图布局，66 节各有三步可复位演示，18 类图形支持参数修改、拖拽和视角控制。PDF 与网页共用逐步讲解及 18 组新增纸笔论证；动画和参数操作通过书中的链接进入网页。</p><p><a href="{PDF}">下载 PDF 教材</a> · <a href="{REPO}">下载 LaTeX、Lean 与 Manim 源码</a></p>
<h2 id="license">署名与许可</h2><p>本项目的原创讲解、证明、动画和实验采用 MIT 许可。外部视频与原课图示的权利归原作者，通过官方播放器和原链接引用。本书与原课程没有官方隶属关系。</p><p>章节阅读形式参考 Dan Margalit 与 Joseph Rabinoff 的 <a href="https://textbooks.math.gatech.edu/ila/">Interactive Linear Algebra</a>；定义、命题、证明的写作组织参考 Sheldon Axler 的 <a href="https://ladr.pretext.plus/frontmatter.html">Linear Algebra Done Right</a>。图形交互参考用户 fork 的 <a href="https://github.com/VitaeL04213/gt-linalg">gt-linalg</a> 中 twobytwo、vector-add 与 compose3d 等示例。</p><p>这些参考用于组织形式与操作设计。本书没有复制其正文、图像或程序代码；没有使用 PreTeXt、MathBox 或该仓库旧版运行环境。交互图是本项目独立实现的二维与空间投影示意，假设和简化范围在逐步讲解中说明。</p><p><a href="{REPO}/issues">反馈与勘误</a></p></article>'''
render("references.html","来源与证明范围",references,"references")

lab='''<header class="section-header lab-intro"><p class="section-label">交互图索引</p><h1>数学实验室</h1><p>先预测，再改变一个参数，用正文中的公式解释结果。拖动端点改变数学对象，拖动空白处改变观察视角。</p></header><div class="lab-layout"><nav class="lab-menu" aria-label="实验选择" id="lab-menu"></nav>'''+widget('',EXPERIMENTS['linear'])+'</div>'
render("lab.html","交互图索引",lab,"lab",kind="lab",scripts=experiment_scripts())
write(DOCS/'assets/experiments.js','window.BookExperiments = '+json.dumps(EXPERIMENTS,ensure_ascii=False,separators=(',',':'))+';\n')
write(DOCS/"assets/search-index.js","window.BookSearch = "+json.dumps(search,ensure_ascii=False,separators=(',',':'))+";\n")
write(DOCS/".nojekyll","")
for name in SCENES.values():
    shutil.copy2(ROOT/f"notes/figures/{name}.png",DOCS/f"media/{name}.png")
    assert (DOCS/f"media/{name}.mp4").stat().st_size>1000
write(ROOT/"validation/textbook-structure.json",json.dumps({
 "lesson_pages":len(entries),"chapter_pages":6,"guides":len(entries),"numbered_sections":len(entries),
 "original_video_links":sum(bool(l.get("video")) for l in LESSONS.values()),
 "manim_animations":len(SCENES),"interactive_experiments":len(EXPERIMENTS),
 "inline_experiment_locations":len(STEPS),"guided_steps":sum(len(s['steps']) for s in STEPS.values()),
 "named_paper_arguments":len(PRINCIPLES),
 "step_prose_characters":sum(len(re.findall(r'[\u4e00-\u9fff]',p)) for s in STEPS.values() for _,p in s['steps']),
 "guided_prose_characters":sum(e["guide_characters"] for e in entries.values()),
 "minimum_guided_prose_characters":min(e["guide_characters"] for e in entries.values()),
 "per_lesson":{s:e["guide_characters"] for s,e in entries.items()},
},ensure_ascii=False,indent=2)+"\n")
print(f"Built {len(entries)} lesson spreads, 198 linked steps, {len(EXPERIMENTS)} experiments, and shared TeX arguments.")
