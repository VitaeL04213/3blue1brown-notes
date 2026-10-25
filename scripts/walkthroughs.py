"""Shared explanatory steps and named arguments, authored once for HTML and TeX."""
from pathlib import Path
from html import escape
import json
ROOT=Path(__file__).resolve().parents[1]
EXPERIMENTS=json.loads((ROOT/'media/experiments.json').read_text(encoding='utf-8'))
PRINCIPLES=json.loads((ROOT/'notes/principles.json').read_text(encoding='utf-8'))
STEPS={}
for path in sorted((ROOT/'notes').glob('intuition-*.json')):
    data=json.loads(path.read_text(encoding='utf-8'))
    assert not STEPS.keys() & data.keys(),path
    STEPS.update(data)

def compose(slug, entries, convert):
    data=STEPS[slug]; demo=data['demo']; number=entries[slug]['number']
    assert len(data['steps'])==len(data['presets'])==3
    items=[]; tex=[r'\subsection*{一步一步建立直观}']
    for i,((title,prose),preset) in enumerate(zip(data['steps'],data['presets']),1):
        assert preset in EXPERIMENTS[demo]['presets'],(slug,preset)
        items.append(f'''<section class="intuition-step" id="step-{i}"><h3><span class="step-index">{i:02d}</span>{escape(title)}</h3>{convert(prose)}<button class="step-play" data-demo="{demo}" data-preset="{preset}" data-step="step-{i}" aria-pressed="false">演示第 {i} 步 →</button></section>''')
        tex.extend([r'\paragraph{'+str(i)+'. '+title+'}',prose,''])
    steps='<section class="walkthrough" id="walkthrough"><h2>一步一步建立直观</h2><p class="walkthrough-intro">先预测，再点“演示本步”核对右图。每一步都重设到指定情形，随后可以自由修改参数。</p>'+''.join(items)+'</section>'
    p=PRINCIPLES[demo]
    if p['lesson']==slug:
        principle=f'''<section class="definition-block" id="definition"><h3>定义 {number}.1　{escape(p['definition_title'])}</h3>{convert(p['definition'])}</section>
<section class="proposition-block" id="principle"><h3>命题 {number}.1　{escape(p['claim_title'])}</h3>{convert(p['claim'])}</section>
<details class="paper-proof" data-print-open><summary>证明 · 展开纸笔推导</summary>{''.join(convert(t) for t in p['proof'])}<p class="proof-end">□</p></details>'''
        tex.extend([r'\subsection*{定义、命题与证明}',r'\paragraph{定义：'+p['definition_title']+'}',p['definition'],r'\paragraph{命题：'+p['claim_title']+'}',p['claim'],r'\begin{proof}', '\n\n'.join(p['proof']),r'\end{proof}'])
    else:
        anchor=p['lesson']; related=entries[anchor]
        principle=f'<p class="principle-link">与本图相连的定义与证明：<a href="{anchor}.html#principle">{related["number"]} · {escape(p["claim_title"])}</a>。本节的具体条件与形式化范围见下文。</p>'
    return steps,principle,'\n\n'.join(tex)+'\n'
