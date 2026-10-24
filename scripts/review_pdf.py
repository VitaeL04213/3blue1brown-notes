"""Render all pages and prepare contact sheets for visual review."""
from pathlib import Path
import json, re, subprocess, hashlib
from pypdf import PdfReader
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parents[1]
pdf=ROOT/"dist/3blue1brown-notes-zh.pdf"
out=ROOT/"build/textbook-review";out.mkdir(parents=True,exist_ok=True)
reader=PdfReader(pdf)
texts=[p.extract_text() or "" for p in reader.pages]
report={"pages":len(texts),"text_characters":sum(map(len,texts)),
 "empty_pages":[i+1 for i,t in enumerate(texts) if not t.strip()],
 "replacement_characters":sum(t.count("\ufffd") for t in texts),
 "undefined_references":sum(t.count("??") for t in texts),
 "pdf_sha256":hashlib.sha256(pdf.read_bytes()).hexdigest(),
 "embedded_images":sum(len(p.images) for p in reader.pages)}
assert not report["empty_pages"] and not report["replacement_characters"] and not report["undefined_references"]
(ROOT/"validation/pdf.json").write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
subprocess.run(["pdftoppm","-scale-to","720","-png",str(pdf),str(out/"page")],check=True,capture_output=True)
images=[out/f"page-{i:0{len(str(len(texts)))}}.png" for i in range(1,len(texts)+1)]
assert all(path.exists() for path in images)
for start in range(0,len(images),20):
    sheet=Image.new("RGB",(880,1650),"#dae0e4");draw=ImageDraw.Draw(sheet)
    for j,path in enumerate(images[start:start+20]):
        im=Image.open(path);im.thumbnail((210,300))
        x=(j%4)*220+5;y=(j//4)*330+5
        sheet.paste(im,(x,y));draw.text((x,y+302),str(start+j+1),fill="black")
    sheet.save(out/f"contact-{start//20+1}.jpg",quality=90)
print(json.dumps(report))
