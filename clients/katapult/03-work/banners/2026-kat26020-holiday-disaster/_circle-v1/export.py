"""Export every KAT26020 frame (8 sizes x 2 iterations = 16) as a standalone HTML file (+ PNG proofs).

Usage: python export.py <built-hub.html> <out-dir> [--png <png-dir>] [--issues]

<built-hub.html> is the output of build.py. Headless Chrome renders the hub, each banner
canvas is serialized at 1:1 with the brand fonts, the logo artwork and the canvas CSS
inlined. The circle photo is baked per frame: the exact crop, at 2x, as a JPEG filling
the circle, so the file opens (or imports into Figma) alone without the full photo.
Writes <out-dir>/V1, <out-dir>/V2 and KAT26020-HolidayDisaster-html.zip next to <out-dir>.
"""
import base64, html as _h, io, json, re, subprocess, sys, tempfile, zipfile
from pathlib import Path

from PIL import Image

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
HERE = Path(__file__).parent
args = sys.argv[1:]
png_dir = None
if "--png" in args:
    i = args.index("--png"); png_dir = Path(args[i + 1]).resolve(); del args[i:i + 2]
hub, out = Path(args[0]), Path(args[1])
page = hub.read_text(encoding="utf-8")

fonts = "\n".join(re.findall(r'@font-face\{font-family:"Aktiv Grotesk";[^}]*\}', page))
logo = re.search(r'<symbol id="k-logo"[^>]*>(.*?)</symbol>', page, re.S).group(1).strip()
css = (HERE / "k20.css").read_text(encoding="utf-8")
canvas_css = css[css.index("/* banner canvas"):css.index("/* safe zone overlay */")]

dump = """<script>
(document.fonts?document.fonts.ready:Promise.resolve()).then(function(){ setTimeout(function(){
  if(window.k20Check) k20Check();
  var out={};
  [].forEach.call(document.querySelectorAll('.hub-ch-k20 .kb-fig'),function(f){
    var k=f.querySelector('.k20').cloneNode(true); k.style.transform='';
    var im=k.querySelector('.k20-pic img'); if(im) im.setAttribute('src','K20CROP');
    out[f.querySelector('figcaption .mono').textContent]=k.outerHTML;
  });
  var t=document.createElement('textarea'); t.id='k20dump'; t.textContent=JSON.stringify({frames:out,issues:JSON.parse(document.querySelector('.hub-ch-k20').dataset.k20Issues||'[]')}); document.body.appendChild(t);
},600); });
</script>"""

with tempfile.TemporaryDirectory() as tmp:
    src = Path(tmp) / "hub.html"
    src.write_text('<!doctype html><html><head><meta charset="utf-8"></head><body>\n' + page + dump + "</body></html>", encoding="utf-8")
    dom = subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--virtual-time-budget=20000", "--dump-dom", src.as_uri() + "#k20"],
                         capture_output=True, timeout=240).stdout.decode("utf-8")
m = re.search(r'<textarea id="k20dump">(.*?)</textarea>', dom, re.S)
assert m, "frames not dumped"
data = json.loads(_h.unescape(m.group(1)))
frames, issues = data["frames"], data["issues"]
print("layout issues:", len(issues))
for i in issues:
    print("  ", i)

SRC = {n: Image.open(HERE / "img" / f"{n}.jpg").convert("RGB") for n in ("kitchen", "livingroom")}


def crop(spec):
    """The circle's square, cut from the graded photo at 2x the circle's display size."""
    name, fx, fy, s, d = spec.split(",")
    fx, fy, s, d = float(fx), float(fy), float(s), float(d)
    im = SRC[name]
    sq = im.crop((round(fx - s / 2), round(fy - s / 2), round(fx + s / 2), round(fy + s / 2)))
    px = max(8, min(round(d * 2), round(s)))
    sq = sq.resize((px, px), Image.LANCZOS)
    buf = io.BytesIO()
    sq.save(buf, "JPEG", quality=88, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


out.mkdir(parents=True, exist_ok=True)
files = []
for name, body in frames.items():
    w, h = map(int, re.search(r"-(\d+)x(\d+)-", name).groups())
    body = body.replace('<use href="#k-logo"></use>', logo)
    # the photo: one <img> exactly filling the circle, rounded itself (Figma imports radius on the image)
    def bake(mm):
        spec = re.search(r'data-crop="([^"]+)"', mm.group(0)).group(1)
        d = float(spec.split(",")[-1])
        return (f'<img alt="" width="{round(d)}" height="{round(d)}" src="{crop(spec)}" '
                f'style="left:0px;top:0px;width:{d}px;height:{d}px;border-radius:50%">')
    body, n = re.subn(r'<img[^>]*src="K20CROP"[^>]*>', bake, body)
    assert n == 1, name
    doc = ('<!doctype html>\n<html><head><meta charset="utf-8"><title>' + name + "</title>\n<style>\n"
           ':root{--font-brand:"Aktiv Grotesk","Helvetica Neue",Helvetica,Arial,sans-serif}\n' + fonts + "\n"
           f"html,body{{margin:0;padding:0;width:{w}px;height:{h}px;overflow:hidden;background:#131540}}\n"
           + canvas_css + "</style></head><body>\n" + body + "\n</body></html>\n")
    f = out / ("V2" if name.endswith("-V2") else "V1") / (name + ".html")
    f.parent.mkdir(exist_ok=True)
    f.write_text(doc, encoding="utf-8")
    files.append((f, w, h))
print(f"wrote {len(files)} frames to {out}")

if png_dir:
    png_dir.mkdir(parents=True, exist_ok=True)
    for f, w, h in files:
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--virtual-time-budget=3000",
                        f"--window-size={w},{h}", f"--screenshot={png_dir / (f.stem + '.png')}", f.resolve().as_uri()],
                       capture_output=True, timeout=60)
    print(f"proofs in {png_dir}")

zp = out.parent / "KAT26020-HolidayDisaster-html.zip"
with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
    for f, _, _ in sorted(files):
        z.write(f, f.relative_to(out).as_posix())
print(f"zipped {zp}")
