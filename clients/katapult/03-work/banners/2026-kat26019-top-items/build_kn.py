"""Inject KAT26019 proposal 2 (knolling flat-lay) into the KAT26019 view of the hub.

Usage: python build_kn.py <published-hub.html> <out.html>

Always feed it the hub as just read from the artifact (never an old local copy).
Idempotent: every KN block is dropped and re-added. Only the KN blocks change;
everything else passes through untouched.

The markup goes inside the KAT26019 block (.hub-ch-banners), right above its V1
section, because the hub's router shows one job view at a time and hides anything
outside it. Note: build.py (KB) rewrites that block, so run this again after it.
Cutouts come from img-knolling/{item}.png, only the ones the layout uses: the cutout.py
ones (fridge, tv, tire, laptop, washer, console) and the Figma round-2 ones (couch, bed,
nightstand, vacuum, necklace). The ground is img-knolling/ground.jpg (Figma's paper).
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

# every id placed in a size's items list: ['couch', 254, ...]
used = set(re.findall(r"\['(\w+)',-?[\d.]", js))
photos = {}
for p in sorted((HERE / "img-knolling").glob("*.png")):
    if p.stem not in used:
        continue
    im = Image.open(p).convert("RGBA")
    ow, oh = im.size
    # trim the empty alpha around the cutout (Figma's image rects refer to the whole
    # original, so the trimmed box goes along as fractions: tb)
    a = im.getchannel("A").point(lambda v: 255 if v > 3 else 0)
    box = a.getbbox() or (0, 0, ow, oh)
    im.putalpha(Image.composite(im.getchannel("A"), Image.new("L", im.size, 0), a))
    im = im.crop(box)
    im.thumbnail((720, 720), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "WEBP", quality=88, method=6)
    photos[p.stem] = {"src": "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode(),
                      "ow": ow, "oh": oh, "tb": [round(box[0] / ow, 5), round(box[1] / oh, 5), round(box[2] / ow, 5), round(box[3] / oh, 5)]}
assert used <= set(photos), f"missing cutouts: {sorted(used - set(photos))}"
js = js.replace("var KN_PHOTOS={};", "var KN_PHOTOS=" + json.dumps(photos) + ";")

# the ground texture (Figma's paper), once, in the canvas CSS
g = Image.open(HERE / "img-knolling" / "ground.jpg").convert("RGB")
buf = io.BytesIO()
g.save(buf, "JPEG", quality=82, optimize=True)
css = css.replace("KN_GROUND", "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode())
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
