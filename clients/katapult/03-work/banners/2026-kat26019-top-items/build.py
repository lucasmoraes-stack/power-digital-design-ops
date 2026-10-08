"""Inject the KAT26019 Banners channel into the Katapult Deliverables Hub.

Usage: python build.py <published-hub.html> <out.html>

Always feed it the hub as just read from the artifact (never an old local copy).
Re-running on an already-injected hub replaces the previous Banners blocks.
Cutouts in img/{item}.png (see image-prompts.md) replace the grid placeholders.
"""
import base64, json, re, sys
from pathlib import Path

HERE = Path(__file__).parent
src, out = Path(sys.argv[1]), Path(sys.argv[2])
html = src.read_text(encoding="utf-8")

# a read returns the page inside the publish skeleton; publish wants the page only
if html.lstrip().lower().startswith("<!doctype"):
    html = html[html.index("<body>") + len("<body>"):].lstrip("\n")
html = re.sub(r"\s*</body>\s*</html>\s*$", "\n", html)

# drop a previous injection
html = re.sub(r"/\* KB:START \*/.*?/\* KB:END \*/\n?", "", html, flags=re.S)
html = re.sub(r"<!-- KB:START -->.*?<!-- KB:END -->\n?", "", html, flags=re.S)

css = (HERE / "kb.css").read_text(encoding="utf-8")
body = (HERE / "kb.html").read_text(encoding="utf-8")
js = (HERE / "kb.js").read_text(encoding="utf-8")

# the hub ships Light/Medium/Bold; the subhead is set in Regular (client review, 2026-10-05)
reg = base64.b64encode((HERE / "fonts" / "aktiv-grotesk-400.woff").read_bytes()).decode()
css = ('@font-face{font-family:"Aktiv Grotesk";font-weight:400;font-style:normal;font-display:swap;'
       'src:url(data:font/woff;base64,' + reg + ') format("woff")}\n') + css

import io
from PIL import Image

photos = {}
for p in sorted((HERE / "img").glob("*.png")) if (HERE / "img").exists() else []:
    im = Image.open(p).convert("RGBA")
    im = im.crop(im.getchannel("A").getbbox())  # trim transparent margin
    im.thumbnail((640, 640), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "WEBP", quality=86, method=6)
    photos[p.stem] = "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode()
js = js.replace("var PHOTOS={};", "var PHOTOS=" + json.dumps(photos) + ";")
assert "</script" not in js.lower()

tabs = """<nav class="hub-tabs" aria-label="Channels">
  <div class="q4-wrap" role="tablist">
    <button type="button" class="hub-tab" role="tab" data-go="banners" aria-selected="true">Banners <small>2 jobs · 24</small></button>
    <button type="button" class="hub-tab" role="tab" data-go="organic" aria-selected="false">Organic Social <small>Q4 2026 · 15 posts</small></button>
  </div>
</nav>
<nav class="kb-jobs-bar" aria-label="Banner jobs" data-ch="banners">
  <div class="q4-wrap kb-jobs">
    <b>Jobs</b>
    <a href="#k21" aria-current="true">KAT26021 Flat Brand Type · 8</a>
    <a href="#kb-title">KAT26019 Top Items · 16</a>
  </div>
</nav>
"""


def sub_once(old, new):
    global html
    assert html.count(old) >= 1, f"anchor not found: {old[:60]!r}"
    html = html.replace(old, new, 1)


# one-time structural edits (skipped when already applied)
if "hub-ch-organic" not in html:
    sub_once("Katapult · Facebook and Instagram organic · Q4 2026", "Katapult · Organic Social and Banners · Q4 2026")
    sub_once('    <ul class="q4-counts">', '    <div class="hub-ch-organic" data-ch="organic">\n    <ul class="q4-counts">')
    sub_once("\n    </div>\n  </div>\n</header>", "\n    </div>\n    </div>\n  </div>\n</header>")
    sub_once('<div class="q4-bar">', '<div class="q4-bar" data-ch="organic">')
    sub_once("<main>", '<main data-ch="organic">')

# injected blocks
style_end = html.index("</style>\n\n<svg")
html = html[:style_end] + "/* KB:START */\n" + css + "/* KB:END */\n" + html[style_end:]
sub_once("</header>\n", "</header>\n<!-- KB:START -->\n" + tabs + "<!-- KB:END -->\n")
# KAT26021 (K21) sits above this job when present
k21_end = "</div>\n<!-- K21:END -->\n"
anchor = k21_end if k21_end in html else "</main>\n"
sub_once(anchor, anchor + "<!-- KB:START -->\n" + body + "<!-- KB:END -->\n")
html = html.rstrip("\n") + "\n<!-- KB:START -->\n<script>\n" + js + "</script>\n<!-- KB:END -->\n"

out.write_text(html, encoding="utf-8")
print(f"wrote {out} ({len(html):,} bytes, {len(photos)} cutouts)")
