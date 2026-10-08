"""Inject KAT26019 proposal 2 (knolling flat-lay) into the KAT26019 view of the hub.

Usage: python build_kn.py <published-hub.html> <out.html>

Always feed it the hub as just read from the artifact (never an old local copy).
Idempotent: every KN block is dropped and re-added. Only the KN blocks change;
everything else passes through untouched.

The markup goes inside the KAT26019 block (.hub-ch-banners), right above its V1
section, because the hub's router shows one job view at a time and hides anything
outside it. Note: build.py (KB) rewrites that block, so run this again after it.
Cutouts come from img-knolling/{item}.png (cutout.py), only the ones the layout uses.
"""
import base64, io, json, re, sys
from pathlib import Path

from PIL import Image

HERE = Path(__file__).parent
src, out = Path(sys.argv[1]), Path(sys.argv[2])
html = src.read_text(encoding="utf-8")

# a read returns the page inside the publish skeleton; publish wants the page only
if html.lstrip().lower().startswith("<!doctype"):
    html = html[html.index("<body>") + len("<body>"):].lstrip("\n")
html = re.sub(r"\s*</body>\s*</html>\s*$", "\n", html)

html = re.sub(r"/\* KN:START \*/.*?/\* KN:END \*/\n?", "", html, flags=re.S)
html = re.sub(r"<!-- KN:START -->.*?<!-- KN:END -->\n?", "", html, flags=re.S)
assert 'id="kn"' not in html, "a KN block outside the markers survived"

css = (HERE / "kn.css").read_text(encoding="utf-8")
body = (HERE / "kn.html").read_text(encoding="utf-8")
js = (HERE / "kn.js").read_text(encoding="utf-8")

used = set(re.findall(r"'(\w+)'", re.search(r"rows:\[(.*?)\]\}", js, re.S).group(1)))
photos = {}
for p in sorted((HERE / "img-knolling").glob("*.png")):
    if p.stem not in used:
        continue
    im = Image.open(p).convert("RGBA")
    im.thumbnail((720, 720), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "WEBP", quality=88, method=6)
    photos[p.stem] = {"src": "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode(), "w": im.width, "h": im.height}
assert used <= set(photos), f"missing cutouts: {sorted(used - set(photos))}"
js = js.replace("var KN_PHOTOS={};", "var KN_PHOTOS=" + json.dumps(photos) + ";")
assert "</script" not in js.lower()

# css: with the other job blocks, before the NAV styles
nav_css = html.index("/* NAV:START */")
html = html[:nav_css] + "/* KN:START */\n" + css + "/* KN:END */\n" + html[nav_css:]

# markup: inside the KAT26019 block, above its V1 section
anchor = '  <section class="kb-part" id="kb-v1"'
assert html.count(anchor) == 1, "KAT26019 V1 section not found"
html = html.replace(anchor, "<!-- KN:START -->\n" + body + "<!-- KN:END -->\n" + anchor, 1)

# script: before the NAV router, so the router finds the rendered frame
nav = html.index("<!-- NAV:START -->\n<script>")
html = html[:nav] + "<!-- KN:START -->\n<script>\n" + js + "</script>\n<!-- KN:END -->\n" + html[nav:]

assert html.count("<!-- KN:START -->") == 2 and html.count("/* KN:START */") == 1
out.write_text(html, encoding="utf-8", newline="\n")
print(f"wrote {out} ({len(html):,} bytes, {len(photos)} cutouts)")
