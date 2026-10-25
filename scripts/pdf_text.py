"""Add missing ToUnicode maps from the exact Fandol fonts used by the compiler.

Only text extraction metadata changes. Embedded glyphs, page contents, links and
outlines are preserved. CID names are read from the actual embedded CFF subset.
"""
from io import BytesIO
from pathlib import Path
import re, subprocess
from fontTools.ttLib import TTFont
from fontTools.cffLib import CFFFontSet
from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject, DecodedStreamObject

def cmap_stream(pairs):
    lines=["/CIDInit /ProcSet findresource begin","12 dict begin","begincmap",
           "/CIDSystemInfo << /Registry (Adobe) /Ordering (UCS) /Supplement 0 >> def",
           "/CMapName /TextbookUnicode def","/CMapType 2 def",
           "1 begincodespacerange","<0000> <FFFF>","endcodespacerange"]
    pairs=sorted(pairs)
    for start in range(0,len(pairs),100):
        batch=pairs[start:start+100];lines.append(f"{len(batch)} beginbfchar")
        lines.extend(f"<{cid:04X}> <{chr(code).encode('utf-16-be').hex().upper()}>" for cid,code in batch)
        lines.append("endbfchar")
    lines.extend(["endcmap","CMapName currentdict /CMap defineresource pop","end","end"])
    stream=DecodedStreamObject();stream.set_data(("\n".join(lines)+"\n").encode("ascii"))
    return stream

def write_searchable(source, destination, tectonic=None):
    reader=PdfReader(source);writer=PdfWriter();writer.clone_document_from_reader(reader)
    seen=set();repaired=[];maps={}
    for page in writer.pages:
        for ref in page["/Resources"].get("/Font",{}).values():
            font=ref.get_object();name=str(font.get("/BaseFont",""))
            if name in seen:continue
            seen.add(name)
            if "Fandol" not in name or font.get("/ToUnicode"):continue
            match=re.search(r"(Fandol[A-Za-z]+-(?:Regular|Bold))",name)
            if not match:raise ValueError(f"Unrecognized Fandol font: {name}")
            family=match[1]
            if family not in maps:
                filename=family+".otf"
                if tectonic:
                    command=[str(tectonic),"-X","bundle","cat",filename]
                    data=subprocess.run(command,check=True,capture_output=True).stdout
                else:
                    location=subprocess.run(["kpsewhich",filename],check=True,capture_output=True,text=True).stdout.strip()
                    data=Path(location).read_bytes()
                full=TTFont(BytesIO(data));reverse={}
                # Kangxi radicals and compatibility ideographs may share glyphs
                # with ordinary Chinese. Prefer unified ideographs for search.
                def priority(item):
                    code=item[0]
                    return (0x2E80<=code<=0x2FDF or 0xF900<=code<=0xFAFF,code)
                for code,glyph in sorted(full.getBestCmap().items(),key=priority):reverse.setdefault(glyph,code)
                maps[family]=reverse
            descendant=font["/DescendantFonts"][0].get_object()
            embedded=CFFFontSet()
            embedded.decompile(BytesIO(descendant["/FontDescriptor"]["/FontFile3"].get_data()),None)
            glyphs=embedded.topDictIndex[0].charset
            pairs=[]
            for glyph in glyphs:
                if glyph==".notdef":continue
                if not glyph.startswith("cid") or glyph not in maps[family]:
                    raise ValueError(f"Missing Unicode mapping: {family} / {glyph}")
                pairs.append((int(glyph[3:]),maps[family][glyph]))
            font[NameObject("/ToUnicode")]=writer._add_object(cmap_stream(pairs))
            repaired.append({"font":family,"mapped_glyphs":len(pairs)})
    writer.write(destination)
    return repaired
