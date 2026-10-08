"""Export every KAT26019 frame as a standalone HTML file (+ PNG proof), one per deliverable.

Usage: python export.py <built-hub.html> <out-dir> [--png <png-dir>]

<built-hub.html> is the output of build.py. Headless Chrome renders the hub, each
banner canvas is serialized at 1:1 and written to <out-dir>/V1 and <out-dir>/V2 with
the brand fonts and canvas CSS inlined, so the file opens (or imports into Figma) alone.
"""
import json, re, subprocess, sys, tempfile, zipfile
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
css = (HERE / "kb.css").read_text(encoding="utf-8")
canvas_css = css[css.index("/* ============ Banner canvas"):css.index("/* safe zone overlay */")]

dump = """<script>
(document.fonts?document.fonts.ready:Promise.resolve()).then(function(){ setTimeout(function(){
  var out={};
  [].forEach.call(document.querySelectorAll('.hub-ch-banners .kb-fig'),function(f){
    var src=f.querySelector('.kb'), k=src.cloneNode(true); k.style.transform='';
    /* bake the laid-out image size: Figma importers ignore auto + max-width/max-height and stretch the photo */
    var a=src.querySelectorAll('.kb-cell img'), b=k.querySelectorAll('.kb-cell img');
    [].forEach.call(a,function(im,i){
      var w=Math.round(im.offsetWidth), h=Math.round(im.offsetHeight);
      b[i].setAttribute('width',w); b[i].setAttribute('height',h);
      b[i].style.cssText='width:'+w+'px;height:'+h+'px;max-width:none;max-height:none;flex:none';
    });
    out[f.querySelector('figcaption .mono').textContent]=k.outerHTML;
  });
  var t=document.createElement('textarea'); t.id='kbdump'; t.textContent=JSON.stringify(out); document.body.appendChild(t);
},400); });
</script>"""

with tempfile.TemporaryDirectory() as tmp:
    src = Path(tmp) / "hub.html"
    src.write_text('<!doctype html><html><head><meta charset="utf-8"></head><body>\n' + page + dump + "</body></html>", encoding="utf-8")
    dom = subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--virtual-time-budget=15000", "--dump-dom", src.as_uri()],
                         capture_output=True, timeout=180).stdout.decode("utf-8")
m = re.search(r'<textarea id="kbdump">(.*?)</textarea>', dom, re.S)
assert m, "frames not dumped"
import html as _h
frames = json.loads(_h.unescape(m.group(1)))

out.mkdir(parents=True, exist_ok=True)
files = []
for name, body in frames.items():
    w, h = map(int, re.search(r"-(\d+)x(\d+)-", name).groups())
    body = body.replace('<use href="#k-logo"></use>', logo)
    doc = ('<!doctype html>\n<html><head><meta charset="utf-8"><title>' + name + "</title>\n<style>\n"
           ':root{--font-brand:"Aktiv Grotesk","Helvetica Neue",Helvetica,Arial,sans-serif}\n' + fonts + "\n"
           f"html,body{{margin:0;padding:0;width:{w}px;height:{h}px;overflow:hidden;background:#EAEAE8}}\n"
           + canvas_css + "</style></head><body>\n" + body + "\n</body></html>\n")
    f = out / ("V1" if "-V1" in name else "V2") / (name + ".html")
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

zp = out.parent / "KAT26019-TopItems-html.zip"
with zipfile.ZipFile(zp, "w", zipfile.ZIP_DEFLATED) as z:
    for f, _, _ in sorted(files):
        z.write(f, f.relative_to(out).as_posix())
print(f"zipped {zp}")
