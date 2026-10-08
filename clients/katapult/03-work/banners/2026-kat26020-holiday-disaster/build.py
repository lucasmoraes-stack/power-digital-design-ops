"""Inject the KAT26020 Holiday Disaster job into the Banners channel of the Katapult Deliverables Hub.

Usage: python build.py <published-hub.html> <out.html>

Always feed it the hub as just read from the artifact (never an old local copy): the
hub is edited in parallel, and everything outside the K20:START/END blocks is passed
through untouched, except the fixed values listed below.
Needs KAT26019 (channels + jobs bar), KAT26021, KAT26022 and the NAV card index in the hub.

Idempotent: re-running on its own output gives the same file. The K20 blocks, the #k20
jobs-bar entry, the k20 row of the NAV job list, the Banners tab count and the index
intro are removed or set to fixed values, never incremented.
Photos: img/{kitchen,livingroom}.jpg (grade.py), embedded as WebP.
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

for need in ("hub-ch-banners", "kb-jobs-bar", "hub-ch-k21", "hub-ch-k22", "<!-- NAV:START -->\n<script>"):
    assert need in html, f"{need} missing from the hub"

html = re.sub(r"/\* K20:START \*/.*?/\* K20:END \*/\n?", "", html, flags=re.S)
html = re.sub(r"<!-- K20:START -->.*?<!-- K20:END -->\n?", "", html, flags=re.S)
assert 'class="hub-ch-k20"' not in html, "a K20 block outside the markers survived"

css = (HERE / "k20.css").read_text(encoding="utf-8")
body = (HERE / "k20.html").read_text(encoding="utf-8")
js = (HERE / "k20.js").read_text(encoding="utf-8")

photos = {}
for name in ("kitchen", "livingroom"):
    im = Image.open(HERE / "img" / f"{name}.jpg").convert("RGB")
    buf = io.BytesIO()
    im.save(buf, "WEBP", quality=84, method=6)
    photos[name] = {"src": "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode(), "w": im.width, "h": im.height}
assert js.count("var K20_PHOTOS={};") == 1
js = js.replace("var K20_PHOTOS={};", "var K20_PHOTOS=" + json.dumps(photos) + ";")
assert "</script" not in js.lower()

# frame counts per job, fixed: KAT26019 16, KAT26021 8, KAT26022 16, KAT26020 8 sizes x 2 iterations
K20_FRAMES = 16
BANNERS_TOTAL = 16 + 8 + 16 + K20_FRAMES

html, n = re.subn(r'(data-go="banners"[^>]*>Banners <small>)[^<]*(</small>)', rf"\g<1>4 jobs · {BANNERS_TOTAL}\g<2>", html, count=1)
assert n == 1, "Banners tab not found"

# jobs bar: KAT26020 goes first and takes aria-current
html = re.sub(r'\s*<a href="#k20"[^>]*>KAT26020[^<]*</a>', "", html)
html = re.sub(r'(<a href="#k2[12]") aria-current="true"', r"\1", html)
anchor = '<div class="q4-wrap kb-jobs">\n    <b>Jobs</b>'
assert html.count(anchor) == 1, "jobs bar anchor not found"
html = html.replace(anchor, anchor + f'\n    <a href="#k20" aria-current="true">KAT26020 Holiday Disaster · {K20_FRAMES}</a>', 1)

# NAV router: register the job first in its list (the router only shows listed views)
html = re.sub(r"\n\s*\{id:'k20',[^\n]*\},?", "", html)
nav_jobs = "  var JOBS=[\n"
assert html.count(nav_jobs) == 1, "NAV job list not found"
html = html.replace(nav_jobs, nav_jobs + "    {id:'k20', box:document.querySelector('.hub-ch-k20'), thumbs:2, badge:'New · for review'},\n", 1)
html = re.sub(r"Detail views: one banner job \([^)]*\)", "Detail views: one banner job (#k20, #k22, #k21, #k19)", html, count=1)

# banners index intro + reading note, set to fixed text
html, n = re.subn(r"<p>[A-Z][a-z]+ jobs for PMAX and Google programmatic\. Open one", "<p>Four jobs for PMAX and Google programmatic. Open one", html, count=1)
assert n == 1, "banners index intro not found"
html = html.replace("<p><b>Copy</b> is the client's, placed exactly as written. No disclaimer, because the briefs have none.</p>",
                    "<p><b>Copy</b> is the client's, placed exactly as written. No disclaimer unless the job's Figma carries one (KAT26020, PMAX only).</p>", 1)

# css with the other job blocks, before the NAV styles
nav_css = html.index("/* NAV:START */")
html = html[:nav_css] + "/* K20:START */\n" + css + "/* K20:END */\n" + html[nav_css:]
# newest job first: right after the organic <main>
assert "</main>\n" in html
html = html.replace("</main>\n", "</main>\n<!-- K20:START -->\n" + body + "<!-- K20:END -->\n", 1)
# script before the NAV router, so the router finds rendered frames
nav = html.index("<!-- NAV:START -->\n<script>")
html = html[:nav] + "<!-- K20:START -->\n<script>\n" + js + "</script>\n<!-- K20:END -->\n" + html[nav:]

assert html.count("<!-- K20:START -->") == 2 and html.count("/* K20:START */") == 1
assert html.count('href="#k20"') == 1 and html.count("{id:'k20'") == 1
out.write_text(html, encoding="utf-8", newline="\n")
print(f"wrote {out} ({len(html):,} bytes)")
