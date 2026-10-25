"""Shared, static textbook navigation. No external UI or math dependencies."""
from html import escape

REPO = "https://github.com/VitaeL04213/3blue1brown-notes"
PDF = "https://raw.githubusercontent.com/VitaeL04213/3blue1brown-notes/main/dist/3blue1brown-notes-zh.pdf"

def e(value):
    return escape(str(value), quote=True)

def navigation(groups, entries, chapter_slugs, prefix, current):
    rows=[]
    for i,(cid,(name,_)) in enumerate(groups.items(),1):
        active=current==cid or current in chapter_slugs[cid]
        children=[]
        for slug in chapter_slugs[cid]:
            entry=entries[slug]
            selected=' aria-current="page"' if current==slug else ''
            children.append(f'<li><a href="{prefix}lessons/{slug}.html"{selected}><span class="toc-number">{entry["number"]}</span><span>{e(entry["title"])}</span></a></li>')
        if cid=='neural-networks':
            children.append(f'<li class="toc-related"><a href="{prefix}lessons/cross-entropy.html"><span class="toc-number">6.2</span><span>延伸：交叉熵</span></a></li>')
        children.append(f'<li class="toc-review"><a href="{prefix}chapters/{cid}.html#review">本章综合练习</a></li>')
        rows.append(f'<details class="toc-chapter" {"open" if active else ""}><summary><span class="toc-chapter-number">{i}</span>{e(name)}</summary><a class="chapter-overview" href="{prefix}chapters/{cid}.html" {"aria-current=page" if current==cid else ""}>本章导言与学习目标</a><ol>{"".join(children)}</ol></details>')
    return f'''<aside id="book-sidebar" class="book-sidebar" aria-label="全书目录">
<div class="sidebar-heading"><a href="{prefix}contents.html">全书目录</a><button class="close-contents" aria-label="关闭目录">×</button></div>
<label class="search-label" for="book-search">检索全书</label><div class="search-box"><input id="book-search" type="search" placeholder="输入概念、公式名称或英文标题" autocomplete="off"><button id="clear-search" aria-label="清空搜索" hidden>×</button></div>
<p id="search-status" class="search-status" role="status" aria-live="polite"></p><ol id="search-results" class="search-results" hidden></ol>
<nav id="book-toc" aria-label="章节目录"><a class="front-link" href="{prefix}index.html" {"aria-current=page" if current=="index" else ""}>扉页与阅读说明</a>{"".join(rows)}
<div class="toc-back"><a href="{prefix}lab.html">交互图索引</a><a href="{prefix}references.html">来源、证明范围与许可</a></div></nav>
<p class="sidebar-note">6 章 · 66 个条目<br>LaTeX 正文 · Lean 证明</p></aside>'''

def pagination(prev, nxt, prefix="", position="bottom"):
    links=[]
    for key,item,arrow in [("prev",prev,"←"),("next",nxt,"→")]:
        if item:
            url,title=item
            label="上一页" if key=="prev" else "下一页"
            links.append(f'<a rel="{key}" href="{prefix}{url}"><small>{label}</small><span>{arrow} {e(title)}</span></a>')
        else:links.append('<span></span>')
    return f'<nav class="page-turn {position}" aria-label="{"页首" if position=="top" else "页末"}翻页">{"".join(links)}</nav>'

def shell(title, body, groups, entries, chapter_slugs, prefix="", current="index", prev=None, nxt=None, page_type="front", scripts="", local_toc=""):
    sidebar=navigation(groups,entries,chapter_slugs,prefix,current)
    return f'''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)} · 从直觉到证明</title><meta name="description" content="3Blue1Brown 官方课程序列的独立中文导学教材：连续论述、交互图、原课程与 Lean 证明。">
<link rel="stylesheet" href="{prefix}assets/style.css"><link rel="stylesheet" href="{prefix}assets/spread.css"><script>if(new URLSearchParams(location.search).get('embed')==='1')document.documentElement.classList.add('lab-embedded');</script></head>
<body data-prefix="{prefix}" data-page="{e(current)}" data-type="{page_type}"><a class="skip" href="#main">跳到正文</a>
<header class="book-header"><a class="book-brand" href="{prefix}index.html"><span>从直觉到证明</span><small>3Blue1Brown 中文导学教材</small></a><nav aria-label="全书工具"><a href="{prefix}contents.html">目录</a><a href="{PDF}">PDF</a><a href="{REPO}">GitHub</a></nav></header>
<div class="reading-toolbar"><button id="toggle-contents" aria-controls="book-sidebar" aria-expanded="true">☰ <span>目录与搜索</span></button><div class="toolbar-location">{e(title)}</div><button id="print-page" aria-label="打印当前小节">打印</button></div>
<div class="sidebar-shade" hidden></div>{sidebar}
<div class="book-body"><main id="main" class="book-content {page_type}" tabindex="-1">{pagination(prev,nxt,prefix,"top")}{body}{pagination(prev,nxt,prefix)}</main>{local_toc}
<footer class="book-footer">独立中文伴读教材 · 原课程：3Blue1Brown 及署名合作者<br><a href="{prefix}references.html">来源与许可</a> · <a href="{REPO}/issues">反馈与勘误</a></footer></div>
<script src="{prefix}assets/search-index.js" defer></script><script src="{prefix}assets/reader.js" defer></script>{scripts}</body></html>'''
