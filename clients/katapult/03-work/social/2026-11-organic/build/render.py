"""Render frame HTML files to PNG at native size with headless Chrome.
usage: python render.py <frames_dir> <out_dir>   (each *.html becomes <out_dir>/<same name>.png; size from the name: *9x16* = 1080x1920, else 1080x1350)"""
import pathlib, subprocess, sys
CHROME = r"C:/Program Files/Google/Chrome/Application/chrome.exe"
src, out = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2])
out.mkdir(parents=True, exist_ok=True)
for f in sorted(src.rglob("*.html")):
    h = 1920 if "9x16" in f.name else 1350
    png = out / f.relative_to(src).with_suffix(".png")
    png.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run([CHROME, "--headless=new", "--hide-scrollbars", "--force-device-scale-factor=1",
                    "--virtual-time-budget=3000", f"--window-size=1080,{h}", f"--screenshot={png}", f.resolve().as_uri()],
                   check=True, capture_output=True)
    print(png)
