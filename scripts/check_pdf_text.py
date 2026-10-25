"""Check searchable Chinese text, shared lesson numbering, and font metadata."""
from pathlib import Path
import json,re
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parents[1]
reader=PdfReader(ROOT/'dist/3blue1brown-notes-zh.pdf')
text='\n'.join(page.extract_text() or '' for page in reader.pages)
compact=re.sub(r'\s+','',text)
chinese=lambda s:''.join(re.findall(r'[\u4e00-\u9fff]',s))
index=json.loads((ROOT/'docs/assets/search-index.js').read_text(encoding='utf-8').removeprefix('window.BookSearch = ').strip().removesuffix(';'))
assert len(chinese(text))>40000,'Chinese text is not decoded correctly'
assert '中文导学教材' in compact and compact.count('定义、命题与证明')==18
outlines={}
def inspect(items):
    for item in items:
        if isinstance(item,list):inspect(item)
        else:
            match=re.match(r'^(\d+\.\d+)\s+(.*)',item.title)
            if match:outlines[match[1]]=match[2]
inspect(reader.outline)
for entry in index:
    assert chinese(entry['title']) in chinese(text),entry['slug']
    assert entry['number'] in outlines,entry['number']
    assert chinese(outlines[entry['number']])==chinese(entry['title']),(entry['number'],outlines[entry['number']],entry['title'])
fonts=set()
for page in reader.pages:
    for ref in page['/Resources'].get('/Font',{}).values():
        font=ref.get_object()
        if 'Fandol' in str(font.get('/BaseFont')):
            assert font.get('/ToUnicode'),font.get('/BaseFont')
            fonts.add(str(font.get('/BaseFont')))
assert '??' not in text and '\ufffd' not in text
result={'pages':len(reader.pages),'searchable_chinese_characters':len(chinese(text)),
        'lesson_numbers_matched_to_web':len(index),'named_argument_groups':18,
        'cjk_fonts_with_unicode_maps':len(fonts)}
(ROOT/'validation/pdf-text.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result))
