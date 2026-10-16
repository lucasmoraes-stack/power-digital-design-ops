"""Inject the KAT26022 Trusted job into the Banners channel of the Katapult Deliverables Hub.

Usage: python build.py <published-hub.html> <out.html>

Always feed it the hub as just read from the artifact (never an old local copy): the
hub is edited in parallel (other jobs, Figma syncs, the NAV router), and everything
outside the K22:START/END blocks is passed through untouched.

Pass 8 (2026-10-13): the K22 blocks are replaced IN PLACE when they already exist.
The earlier version always re-inserted them at "newest job" positions and reset the
Banners tab to "3 jobs · 40" and the jobs bar to KAT26022-first, which, once KAT26020
landed, would have broken the tab count (4 jobs · 56), the jobs-bar order and given
two entries aria-current. Now the tab count, the jobs bar order and the NAV job list
belong to whichever job was built last; this script only refreshes the #k22 entry's
frame count. The first-insert branch (hub without K22) is kept for a clean rebuild.

Photo: img/laptop-woman-window-desk-06.jpg (Katapult library, Adobe Stock 410115591,
the photo Figma uses in every Option B frame), embedded as WebP.
Idempotent: re-running on its own output gives the same file.
Scope: 8 sizes x 2 options (A centered badge, B photo and seam badge) = 16 frames.
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

assert "hub-ch-banners" in html, "Banners channel (KAT26019 build) missing"
assert "kb-jobs-bar" in html, "jobs bar (KAT26019 build) missing"
assert "hub-ch-k21" in html, "KAT26021 block missing"

css = (HERE / "k22.css").read_text(encoding="utf-8")
body = (HERE / "k22.html").read_text(encoding="utf-8")
js = (HERE / "k22.js").read_text(encoding="utf-8")

# the shopper photo, 1600px wide is enough for the largest crop (1200x800 in the 1x1)
im = Image.open(HERE / "img" / "laptop-woman-window-desk-06.jpg").convert("RGB")
im = im.resize((1600, round(1600 * im.height / im.width)), Image.LANCZOS)
buf = io.BytesIO()
im.save(buf, "WEBP", quality=84, method=6)
photo = {"src": "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode(), "w": im.width, "h": im.height}
assert js.count("var K22_PHOTO={};") == 1
js = js.replace("var K22_PHOTO={};", "var K22_PHOTO=" + json.dumps(photo) + ";")
assert "</script" not in js.lower()

K22_FRAMES = 16
css_block = "/* K22:START */\n" + css + "/* K22:END */\n"
body_block = "<!-- K22:START -->\n" + body + "<!-- K22:END -->\n"
js_block = "<!-- K22:START -->\n<script>\n" + js + "</script>\n<!-- K22:END -->\n"

css_re = re.compile(r"/\* K22:START \*/.*?/\* K22:END \*/\n?", re.S)
html_re = re.compile(r"<!-- K22:START -->.*?<!-- K22:END -->\n?", re.S)
existing = html_re.findall(html)

if len(css_re.findall(html)) == 1 and len(existing) == 2:
    # in place: css, markup, script each keep their slot
    html = css_re.sub(lambda m: css_block, html, count=1)
    blocks = iter([body_block, js_block])
    html = html_re.sub(lambda m: next(blocks), html)
    assert 'href="#k22"' in html, "#k22 jobs-bar entry missing"
    html = re.sub(r'(<a href="#k22"[^>]*>KAT26022 Trusted · )\d+(</a>)', rf"\g<1>{K22_FRAMES}\g<2>", html, count=1)
else:
    # first insert into a hub that has never had K22
    html = css_re.sub("", html)
    html = html_re.sub("", html)
    assert 'class="hub-ch-k22"' not in html, "a K22 block outside the markers survived"
    style_end = html.find("/* NAV:START */")
    if style_end < 0:
        style_end = html.index("</style>\n\n<svg")
    html = html[:style_end] + css_block + html[style_end:]
    assert "</main>\n" in html
    html = html.replace("</main>\n", "</main>\n" + body_block, 1)
    nav = html.find("<!-- NAV:START -->\n<script>")
    html = (html[:nav] + js_block + html[nav:]) if nav > -1 else (html.rstrip("\n") + "\n" + js_block)
    anchor = '<div class="q4-wrap kb-jobs">\n    <b>Jobs</b>'
    assert html.count(anchor) == 1, "jobs bar anchor not found"
    html = re.sub(r'\s*<a href="#k22"[^>]*>KAT26022[^<]*</a>', "", html)
    html = html.replace(anchor, anchor + f'\n    <a href="#k22">KAT26022 Trusted · {K22_FRAMES}</a>', 1)
    print("note: K22 inserted fresh; check the Banners tab count and the NAV job list by hand")

assert html.count("<!-- K22:START -->") == 2 and html.count("/* K22:START */") == 1
assert html.count('href="#k22"') == 1, "duplicate #k22 jobs-bar entry"
out.write_text(html, encoding="utf-8", newline="\n")
print(f"wrote {out} ({len(html):,} bytes, photo {len(photo['src']) // 1024} KB)")
