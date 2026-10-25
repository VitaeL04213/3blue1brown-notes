"""Build the Chinese LaTeX book with Tectonic or XeLaTeX."""
import argparse
import shutil
import subprocess
import sys
from pathlib import Path
from pdf_text import write_searchable

ROOT=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser()
parser.add_argument('--tectonic',help='Absolute path to Tectonic, if not on PATH')
args=parser.parse_args()
out=ROOT/'build/pdf'
out.mkdir(parents=True,exist_ok=True)
compiler=args.tectonic or shutil.which('tectonic')
if compiler:
    command=[compiler,'-X','compile','--outdir',str(out),'--print','--untrusted','main.tex']
    rounds=1
else:
    compiler=shutil.which('xelatex')
    if not compiler:
        sys.exit('Install Tectonic 0.17.0 or XeLaTeX with ctex, Fandol, amsmath, TikZ and hyperref.')
    command=[compiler,'-interaction=nonstopmode','-halt-on-error','-output-directory='+str(out),'main.tex']
    rounds=3
logs=[]
for _ in range(rounds):
    result=subprocess.run(command,cwd=ROOT/'notes',capture_output=True,text=True,encoding='utf-8',errors='replace')
    logs.append(result.stdout+'\n'+result.stderr)
    (ROOT/'build/latex.log').write_text('\n'.join(logs),encoding='utf-8')
    if result.returncode:
        print(logs[-1][-6000:])
        sys.exit(result.returncode)
if not (out/'main.pdf').exists(): sys.exit('Compiler returned without a PDF.')
if 'Missing character:' in '\n'.join(logs): sys.exit('Missing glyphs detected; inspect build/latex.log.')
dest=ROOT/'dist/3blue1brown-notes-zh.pdf'
dest.parent.mkdir(parents=True,exist_ok=True)
mapped=write_searchable(out/'main.pdf',dest,compiler if args.tectonic or shutil.which('tectonic') else None)
print('Unicode text maps: '+str(mapped))
print('PDF built: '+str(dest))
