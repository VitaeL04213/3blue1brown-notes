"""Check coverage, theorem links, and absence of unfinished proof constructs.

This structural audit complements (and never replaces) `lake build`.
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser()
parser.add_argument('--write-index',action='store_true')
args=parser.parse_args()
catalog=json.loads((ROOT/'sources/catalog.json').read_text(encoding='utf-8'))
lessons={l['slug']:l for c in catalog['courses'] for l in c['lessons']}
found={}
for p in sorted((ROOT/'notes/chapters').glob('*.tex')):
    source=p.read_text(encoding='utf-8')
    matches=list(re.finditer(r'\\lesson\{([^}]+)\}\{([^}]+)\}\{([^}]+)\}',source))
    for i,m in enumerate(matches):
        slug,title,theorem=m.groups()
        assert slug not in found, f'Duplicate lesson {slug}'
        body=source[m.end():matches[i+1].start() if i+1<len(matches) else len(source)]
        for part in ['idea','mathpart','examplepart','pitfall','exercise','leanpart']:
            assert '\\'+part in body, f'Missing {part}: {slug}'
        scoped_body=body.split('\\nextlesson')[0]
        scope=re.search(r'\\leanpart\{(.*)\}',scoped_body,re.S)
        assert scope, f'Missing formalization boundary: {slug}'
        found[slug]={'title_zh':title,'note':p.relative_to(ROOT).as_posix(),
                     'theorem':theorem,'scope_tex':scope[1].strip()}
assert set(found)==set(lessons),f'Coverage mismatch: {set(lessons)^set(found)}'
found={slug:found[slug] for slug in lessons}
theorems={}
for p in sorted((ROOT/'ThreeBlueOneBrown').glob('*.lean')):
    source=p.read_text(encoding='utf-8')
    # Strip comments before the guard; audited source does not nest block comments.
    clean=re.sub(r'/\-.*?\-/','',source,flags=re.S)
    clean=re.sub(r'--[^\n]*','',clean)
    forbidden=re.search(r'\b(sorry|admit|axiom|native_decide)\b',clean)
    assert not forbidden, f'Forbidden construct in {p}: {forbidden[0]}'
    for m in re.finditer(r'^theorem\s+(\w+)',source,re.M):
        name=p.stem+'.'+m[1]
        theorems[name]={'file':p.relative_to(ROOT).as_posix(),'line':source[:m.start()].count('\n')+1}
for slug,entry in found.items():
    if entry['theorem']=='not-applicable':
        assert slug=='lockdown-math-announcement'
    else:
        assert entry['theorem'] in theorems,f"Missing theorem {entry['theorem']}"
        entry.update(theorems[entry['theorem']])
if args.write_index:
    (ROOT/'sources/coverage.json').write_text(json.dumps(found,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    lines=['# 逐课目录','',f"目录快照：{catalog['snapshot_date']}。6 组课程，67 个目录位置，66 节独立课。",'',
           '交叉熵在两组目录中共享同一份笔记。章节次序按官网主题目录保留，不强行套用不同年代视频的章号。','']
    for c in catalog['courses']:
        lines += [f"## {c['title']}",'','| 课 | 中文笔记 / 源码 | 原课 | 视频 |','|---|---|---|---|']
        for i,l in enumerate(c['lessons'],1):
            f=found[l['slug']]
            lines.append(f"| {i} | [{f['title_zh']}]({f['note']}) | [{l['title'].replace('|','/ ')}]({l['url']}) | "+(f"[YouTube]({l['youtube']})" if l.get('youtube') else '官网正文')+' |')
        lines.append('')
    (ROOT/'COURSES.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    lines=['# 形式化覆盖','',
           '所有名称均在 `ThreeBlueOneBrown` 命名空间内。这里列出实际被 Lean 检查的命题边界；一般定理、特例和局部恒等式不能互相替代。','',
           '通过 `lake build` 才算证明编译通过；本表由源码生成，单凭此表不是通过凭证。','',
           '| 课 | 定理 / 代码 | 校验边界 |','|---|---|---|']
    for slug,e in found.items():
        scope=e['scope_tex'].replace('\n',' ')
        scope=re.sub(r'\\texttt\{([^}]+)\}',r'`\1`',scope).replace('\\_','_').replace('|','\\|')
        scope=re.sub(r'\\ref\{[^}]+\}','对应章节',scope)
        target=(f"[`{e['theorem']}`]({e['file']}#L{e['line']})" if e['theorem']!='not-applicable' else '不适用（公告）')
        lines.append(f"| {e['title_zh']} | {target} | {scope} |")
    lines += ['', '补充命题：', '']
    linked={e['theorem'] for e in found.values()}
    for name,e in theorems.items():
        if name not in linked: lines.append(f"- [`{name}`]({e['file']}#L{e['line']})")
    (ROOT/'FORMALIZATION.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    audit=['import ThreeBlueOneBrown','']
    audit += ['#print axioms ThreeBlueOneBrown.'+n for n in theorems]
    (ROOT/'scripts/AxiomAudit.lean').write_text('\n'.join(audit)+'\n',encoding='utf-8')
summary={'unique_lessons':len(lessons),'notes':len(found),'theorems':len(theorems),
         'lessons_with_formal_counterpart':sum(e['theorem']!='not-applicable' for e in found.values()),
         'announcement_pages':1,'unfinished_proof_constructs':0}
print(json.dumps(summary,ensure_ascii=False))
