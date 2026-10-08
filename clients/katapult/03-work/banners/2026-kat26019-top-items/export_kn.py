"""Export the KAT26019 proposal 2 (knolling) frames as standalone HTML files (+ PNG proofs).

Usage: python export_kn.py <built-hub.html> <out-dir> [--png <png-dir>]

<built-hub.html> is the output of build_kn.py (or the hub as synced locally after a
publish). Headless Chrome renders the hub, each knolling canvas is serialized at 1:1
with the brand fonts, the logo artwork, the cutouts and the canvas CSS inlined, so the
file opens (or imports into Figma) alone. Writes <out-dir>/V1, <out-dir>/V2 and a zip next to it.
"""
import base64, html as _h, io, json, re, subprocess, sys, tempfile, zipfile

import numpy as np
from PIL import Image
from pathlib import Path

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
HERE = Path(__file__).parent
args = sys.argv[1:]
png_dir = None
if "--png" in args:
    i = args.index("--png"); png_dir = Path(args[i + 1]); del args[i:i + 2]
hub, out = Path(args[0]), Path(args[1])
page = hub.read_text(encoding="utf-8")

fonts = "\n".join(re.findall(r'@font-face\{font-family:"Aktiv Grotesk";[^}]*\}', page))
logo = re.search(r'<symbol id="k-logo"[^>]*>(.*?)</symbol>', page, re.S).group(1).strip()
css = (HERE / "kn.css").read_text(encoding="utf-8")
canvas_css = css[css.index("/* banner canvas"):css.index("/* safe zone overlay */")]

dump = """<script>
(document.fonts?document.fonts.ready:Promise.resolve()).then(function(){ setTimeout(function(){
  if(window.knFitAll) knFitAll();
  var out={};
  [].forEach.call(document.querySelectorAll('.kn-part .kb-fig'),function(f){
    var k=f.querySelector('.kn').cloneNode(true); k.style.transform='';
    if(!k.querySelector('.kn-item')) throw new Error('frame without products: '+f.querySelector('figcaption .mono').textContent);
    /* bake each cutout's size on the img itself: Figma importers ignore 100% sizing */
    [].forEach.call(k.querySelectorAll('.kn-item'),function(it){
      var w=parseFloat(it.style.width), h=parseFloat(it.style.height), im=it.querySelector('img');
      if(im){ im.setAttribute('width',Math.round(w)); im.setAttribute('height',Math.round(h)); im.style.cssText='width:'+w+'px;height:'+h+'px'; }
    });
    out[f.querySelector('figcaption .mono').textContent]=k.outerHTML;
  });
  var t=document.createElement('textarea'); t.id='kndump'; t.textContent=JSON.stringify(out); document.body.appendChild(t);
},400); });
</script>"""

with tempfile.TemporaryDirectory() as tmp:
    src = Path(tmp) / "hub.html"
    src.write_text('<!doctype html><html><head><meta charset="utf-8"></head><body>\n' + page + dump + "</body></html>", encoding="utf-8")
    dom = subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--virtual-time-budget=15000", "--dump-dom", src.as_uri() + "#kn"],
                         capture_output=True, timeout=180).stdout.decode("utf-8")
m = re.search(r'<textarea id="kndump">(.*?)</textarea>', dom, re.S)
assert m, "frames not dumped"
frames = json.loads(_h.unescape(m.group(1)))



def ground(w, h):
    """The matte ground baked into an image. Figma's HTML import can't read the canvas CSS
    (a radial-gradient light plus an SVG-filter grain) and turns it into a dark block, so the
    standalone files carry the same ground as a picture: #F6E6DE, the soft lift at top left
    (120% x 90% ellipse at 18% 6%, white .26 fading out by 62%) and a fine warm grain."""
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    d = np.sqrt(((xx - .18 * w) / (1.2 * w)) ** 2 + ((yy - .06 * h) / (.9 * h)) ** 2)
    lift = np.clip(1 - d / .62, 0, 1) * .26
    base = np.array([0xF6, 0xE6, 0xDE], np.float32)
    img = base + (255 - base) * lift[..., None]
    grain = np.random.default_rng(19).random((h, w), np.float32) * .07
    img = img * (1 - grain[..., None]) + np.array([.45, .32, .28], np.float32) * 255 * grain[..., None]
    buf = io.BytesIO()
    Image.fromarray(img.clip(0, 255).astype(np.uint8)).save(buf, "JPEG", quality=88, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


out.mkdir(parents=True, exist_ok=True)
files = []
for name, body in frames.items():
    w, h = map(int, re.search(r"-(\d+)x(\d+)-", name).groups())
    body = body.replace('<use href="#k-logo"></use>', logo)
    body = re.sub(r'(<div class="kn"[^>]*>)', lambda m: m.group(1) + f'<img class="kn-ground" alt="" width="{w}" height="{h}" src="{ground(w, h)}" style="left:0;top:0;width:{w}px;height:{h}px">', body, count=1)
    assert 'kn-ground' in body
    doc = ('<!doctype html>\n<html><head><meta charset="utf-8"><title>' + name + "</title>\n<style>\n"
           ':root{--font-brand:"Aktiv Grotesk","Helvetica Neue",Helvetica,Arial,sans-serif}\n' + fonts + "\n"
           f"html,body{{margin:0;padding:0;width:{w}px;height:{h}px;overflow:hidden;background:#F6E6DE}}\n"
           + canvas_css + ".kn{background-image:none}\n</style></head><body>\n" + body + "\n</body></html>\n")
    f = out / ("V2" if "-V2-" in name else "V1") / (name + ".html")
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

zp = out.parent / "KAT26019-TopItems-Knolling-html.zip"
with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
    for f, _, _ in sorted(files):
        z.write(f, f.relative_to(out).as_posix())
print(f"zipped {zp}")
