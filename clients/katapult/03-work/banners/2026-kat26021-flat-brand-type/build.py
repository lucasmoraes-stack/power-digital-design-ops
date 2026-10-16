"""Inject the KAT26021 Flat Brand Type job into the Banners channel of the Katapult Deliverables Hub.

Usage: python build.py <published-hub.html> <out.html>

Always feed it the hub as just read from the artifact (never an old local copy).
Needs the KAT26019 injection (channel tabs + Banners channel) already in the hub.
Re-running replaces the previous K21 blocks.
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

# deliverables a previous K21 injection added to the tab count, so re-runs don't double-book it
DELIV = re.compile(r"<li><b>(\d+)</b> deliverables</li>")
prev = re.search(r"<!-- K21:START -->.*?<!-- K21:END -->", html, flags=re.S)
prev_n = int(DELIV.search(prev.group(0)).group(1)) if prev else 0

# drop a previous injection
html = re.sub(r"/\* K21:START \*/.*?/\* K21:END \*/\n?", "", html, flags=re.S)
html = re.sub(r"<!-- K21:START -->.*?<!-- K21:END -->\n?", "", html, flags=re.S)

css = (HERE / "k21.css").read_text(encoding="utf-8")
body = (HERE / "k21.html").read_text(encoding="utf-8")
js = (HERE / "k21.js").read_text(encoding="utf-8")
assert "</script" not in js.lower()

# channel tab: swap this job's old deliverable count for the new one, keep the other jobs' counts as published
new_n = int(DELIV.search(body).group(1))
def _tab(m):
    jobs, pieces = int(m.group(2)), int(m.group(3))
    return f"{m.group(1)}{jobs + (0 if prev_n else 1)} jobs · {pieces - prev_n + new_n}{m.group(4)}"
html, n = re.subn(r'(data-go="banners"[^>]*>Banners <small>)(\d+) jobs · (\d+)(</small>)', _tab, html, count=1)
assert n == 1, "Banners tab count not found"

style_end = html.index("</style>\n\n<svg")
html = html[:style_end] + "/* K21:START */\n" + css + "/* K21:END */\n" + html[style_end:]
# newest job first: right after the organic <main>, above the KAT26019 block
html = html.replace("</main>\n", "</main>\n<!-- K21:START -->\n" + body + "<!-- K21:END -->\n", 1)
html = html.rstrip("\n") + "\n<!-- K21:START -->\n<script>\n" + js + "</script>\n<!-- K21:END -->\n"

out.write_text(html, encoding="utf-8")
print(f"wrote {out} ({len(html):,} bytes)")
