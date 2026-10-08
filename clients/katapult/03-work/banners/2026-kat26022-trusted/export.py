"""Export every KAT26022 frame (8 sizes x 2 options = 16) as a standalone HTML file.

Usage: python export.py <built-hub.html> <out-dir>

<built-hub.html> is the output of build.py (or the hub as synced locally after a
publish). Headless Chrome renders the hub, the banner canvas is serialized at 1:1
with the brand fonts, the logo artwork and the canvas CSS inlined, so the file
opens (or imports into Figma) alone, with no dependency on the hub page.
"""
import json, re, subprocess, sys, tempfile
from pathlib import Path

CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
HERE = Path(__file__).parent
hub, out = Path(sys.argv[1]), Path(sys.argv[2])
page = hub.read_text(encoding="utf-8")

fonts = "\n".join(re.findall(r'@font-face\{font-family:"Aktiv Grotesk";[^}]*\}', page))
logo = re.search(r'<symbol id="k-logo"[^>]*>(.*?)</symbol>', page, re.S).group(1).strip()
css = (HERE / "k22.css").read_text(encoding="utf-8")
canvas_css = css[css.index("/* ============ Banners channel: KAT26022 Trusted"):css.index("/* safe zone overlay */")]

dump = """<script>
(document.fonts?document.fonts.ready:Promise.resolve()).then(function(){ setTimeout(function(){
  var out={};
  [].forEach.call(document.querySelectorAll('.hub-ch-k22 .kb-fig'),function(f){
    var src=f.querySelector('.k22'), k=src.cloneNode(true); k.style.transform='';
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
assert m, "frame not dumped"
import html as _h
frames = json.loads(_h.unescape(m.group(1)))

out.mkdir(parents=True, exist_ok=True)
files = []
for name, body in frames.items():
    w, h = map(int, re.search(r"-(\d+)x(\d+)-", name).groups())
    body = body.replace('<use href="#k-logo"></use>', logo)
    doc = ('<!doctype html>\n<html><head><meta charset="utf-8"><title>' + name + "</title>\n<style>\n"
           ':root{--font-brand:"Aktiv Grotesk","Helvetica Neue",Helvetica,Arial,sans-serif}\n' + fonts + "\n"
           f"html,body{{margin:0;padding:0;width:{w}px;height:{h}px;overflow:hidden;background:#131540}}\n"
           + canvas_css + "</style></head><body>\n" + body + "\n</body></html>\n")
    f = out / (name + ".html")
    f.write_text(doc, encoding="utf-8")
    files.append(f)
print(f"wrote {len(files)} frame(s) to {out}")
