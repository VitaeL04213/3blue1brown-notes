"""Render nine original Manim scenes and PDF key frames."""
from pathlib import Path
import subprocess, sys, shutil, json, hashlib
ROOT=Path(__file__).resolve().parents[1]
SCENES=["LinearMap","Derivative","Integral","GradientDescent","Attention",
        "FourierHeat","ComplexRotation","Entropy","Taylor"]
subprocess.run([sys.executable,"-m","manim","-qm","--disable_caching",
 "--media_dir","build/manim","media/scenes.py",*SCENES],cwd=ROOT,check=True)
records=[]
for scene in SCENES:
    source=ROOT/f"build/manim/videos/scenes/720p30/{scene}.mp4"
    video=ROOT/f"docs/media/{scene}.mp4";video.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(source,video)
    poster=ROOT/f"notes/figures/{scene}.png";poster.parent.mkdir(parents=True,exist_ok=True)
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-ss","3.5",
                    "-i",str(video),"-frames:v","1",str(poster)],check=True)
    shutil.copy2(poster,ROOT/f"docs/media/{scene}.png")
    gif=ROOT/f"docs/media/{scene}.gif"
    subprocess.run(["ffmpeg","-hide_banner","-loglevel","error","-y","-i",str(video),
      "-filter_complex","fps=12,scale=600:-1:flags=lanczos,split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse",
      "-loop","0",str(gif)],check=True)
    meta=json.loads(subprocess.check_output(["ffprobe","-v","error","-show_entries",
      "stream=width,height,r_frame_rate:format=duration","-of","json",str(video)],text=True))
    records.append({"scene":scene,"video":video.relative_to(ROOT).as_posix(),
      "poster":poster.relative_to(ROOT).as_posix(),"poster_seconds":3.5,
      "gif":gif.relative_to(ROOT).as_posix(),
      "sha256":hashlib.sha256(video.read_bytes()).hexdigest(),"probe":meta})
(ROOT/"media/manifest.json").write_text(json.dumps({"generator":"Manim Community 0.19.0",
 "source":"media/scenes.py","ownership":"Original mathematical visualizations by this project.",
 "videos":records},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
