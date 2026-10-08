"""Inject the KAT26022 Trusted job into the Banners channel of the Katapult Deliverables Hub.

Usage: python build.py <published-hub.html> <out.html>

Always feed it the hub as just read from the artifact (never an old local copy): the
hub is edited in parallel (Figma syncs, the NAV card index), and everything outside
the K22:START/END blocks is passed through untouched.
Needs KAT26019 (channels + jobs bar) and KAT26021 already in the hub.

Idempotent: re-running on its own output gives the same file. Every K22 block, the
#k22 jobs-bar entry and the Banners tab count are removed or set to fixed values,
never incremented.
Scope: 8 sizes x 2 options (A centered badge, B photo and seam badge) = 16 frames.
"""
import re, sys
from pathlib import Path

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

# drop every previous injection (css, markup, script)
html = re.sub(r"/\* K22:START \*/.*?/\* K22:END \*/\n?", "", html, flags=re.S)
html = re.sub(r"<!-- K22:START -->.*?<!-- K22:END -->\n?", "", html, flags=re.S)
assert 'class="hub-ch-k22"' not in html, "a K22 block outside the markers survived"

css = (HERE / "k22.css").read_text(encoding="utf-8")
body = (HERE / "k22.html").read_text(encoding="utf-8")
js = (HERE / "k22.js").read_text(encoding="utf-8")
assert "</script" not in js.lower()

# frame counts per job, fixed: KAT26019 16, KAT26021 8, KAT26022 8 sizes x 2 options
K22_FRAMES = 16
BANNERS_TOTAL = 16 + 8 + K22_FRAMES

# Banners tab count, set (not incremented)
html, n = re.subn(
    r'(data-go="banners"[^>]*>Banners <small>)[^<]*(</small>)',
    rf"\g<1>3 jobs · {BANNERS_TOTAL}\g<2>",
    html, count=1,
)
assert n == 1, "Banners tab not found"

# jobs bar: drop every previous K22 entry, K21 loses aria-current, KAT26022 goes first
html = re.sub(r'\s*<a href="#k22"[^>]*>KAT26022[^<]*</a>', "", html)
html = html.replace('href="#k21" aria-current="true"', 'href="#k21"')
anchor = '<div class="q4-wrap kb-jobs">\n    <b>Jobs</b>'
assert html.count(anchor) == 1, "jobs bar anchor not found"
html = html.replace(anchor, anchor + f'\n    <a href="#k22" aria-current="true">KAT26022 Trusted · {K22_FRAMES}</a>', 1)

# injected blocks
style_end = html.find("/* NAV:START */")
if style_end < 0:
    style_end = html.index("</style>\n\n<svg")
html = html[:style_end] + "/* K22:START */\n" + css + "/* K22:END */\n" + html[style_end:]
# newest job first: right after the organic <main>, above the KAT26021 block
assert "</main>\n" in html
html = html.replace("</main>\n", "</main>\n<!-- K22:START -->\n" + body + "<!-- K22:END -->\n", 1)
# the script runs before the NAV router (if present), so the router finds rendered frames
nav = html.find("<!-- NAV:START -->\n<script>")
block = "<!-- K22:START -->\n<script>\n" + js + "</script>\n<!-- K22:END -->\n"
if nav > -1:
    html = html[:nav] + block + html[nav:]
else:
    html = html.rstrip("\n") + "\n" + block

assert html.count("<!-- K22:START -->") == 2 and html.count("/* K22:START */") == 1
assert html.count('href="#k22"') == 1, "duplicate #k22 jobs-bar entry"
out.write_text(html, encoding="utf-8", newline="\n")
print(f"wrote {out} ({len(html):,} bytes)")
