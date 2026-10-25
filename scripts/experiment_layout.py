"""Native, responsive figure shared by lesson spreads and the experiment index."""
from html import escape
import json

def widget(demo, definition, prefix='', number=None, initial=None):
    initial = escape(json.dumps(initial or {}, ensure_ascii=False), quote=True)
    label = f'交互图 {number}.1' if number else '交互实验'
    return f'''<section id="experiment-root" data-demo="{escape(demo)}" data-initial="{initial}" aria-label="可操作的数学图形">
<div class="figure-heading"><p class="figure-label">{label}</p><h2 id="lab-title">{escape(definition['title'])}</h2><a class="open-lab" href="{prefix}lab.html#{demo}" target="_blank" rel="noopener">独立打开 ↗</a></div>
<p id="step-status" class="step-status" role="status">从左侧选择一步，或自由探索</p>
<div class="plot-surface"><div class="plot-toolbar"><span>拖拽 · 缩放 · 参数探索</span><div class="view-tools" aria-label="图形视角"><button id="zoom-in" aria-label="放大图形">＋</button><button id="zoom-out" aria-label="缩小图形">−</button><button id="reset-view">复位视角</button></div></div><canvas id="plot" width="700" height="340" tabindex="0" role="img" aria-label="可交互数学图形"></canvas></div>
<p id="equation" class="live-equation"></p><p id="readout" class="readout" role="status" aria-live="polite"></p>
<div class="parameter-heading"><strong>改变参数</strong><div class="figure-actions"><button id="play" aria-pressed="false">播放变化</button><button id="reset">重置参数</button></div></div>
<div class="controls" id="controls"></div>
<details class="figure-help"><summary>操作说明与预设情形</summary><p id="plot-hint">{escape(definition['hint'])}</p><p>拖动空白处平移；空间图则旋转视角。先点击画布，再用滚轮缩放。下方选定端点后，可聚焦画布并用方向键移动。</p><label id="drag-tools">键盘操作对象 <select id="drag-target" aria-label="选择可移动端点"></select></label><div class="presets" id="presets"></div><p>位置与颜色配合文字标记使用；改变视角不改变数学量。数值用于核对图形，严格结论以正文条件为准。</p></details>
<details class="animation-details" id="movie-area"{' hidden' if not definition.get('scene') else ''}><summary>配套 Manim 动画</summary><video id="movie" controls playsinline preload="none" aria-label="配套原创 Manim 动画，无音频"></video><p class="caption">动画演示一个固定情形；上方交互图可以改变参数。</p></details>
<noscript>交互操作需要 JavaScript。左侧正文、推导与原课程链接仍可阅读。</noscript>
</section>'''

def scripts(prefix=''):
    return ''.join(f'<script src="{prefix}assets/{name}.js" defer></script>' for name in ('models','experiments','experiment'))
