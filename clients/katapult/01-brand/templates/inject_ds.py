"""Put the social templates into the Katapult Design System page.

Usage: python inject_ds.py <ds_in.html> <ds_out.html>
  ds_in may be the file the Artifact tool saves on read (viewer skeleton is stripped) or the local copy.
Replaces section#templates with ds-templates-section.html, points the handoff section at T01-T10 instead of the
retired .kp-tpl-* layouts, and drops the standalone "Social Templates" link from the Katapult family bar.
"""
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SECTION = (HERE / "ds-templates-section.html").read_text(encoding="utf-8")
OLD_TPL_ARTIFACT = "https://claude.ai/code/artifact/2b191289-c639-44c6-9dfd-a71ec98df407"

src, dst = sys.argv[1], sys.argv[2]
page = Path(src).read_text(encoding="utf-8")
if page.startswith("<!doctype html>"):
    first, page = page.split("\n", 1)
    assert first.endswith("<body>")
    page = re.sub(r"\s*</body></html>\s*$", "\n", page)

# 1. Templates section
start = page.index('<section class="block" id="templates">')
end = page.index('<section class="block" id="carousel">')
page = page[:start] + SECTION + "\n\n" + page[end:]

# 2. Family bar: no standalone templates page any more
page = re.sub(r'<a href="' + re.escape(OLD_TPL_ARTIFACT) + r'"[^>]*>Social Templates</a>', "", page, count=1)

# 3. Carousel intro referred to the old template components
page = page.replace("Same tokens, ratio classes, themes and safe zones as the templates above.",
                    "Same tokens, ratio classes, themes and safe zones as the rest of this system.")

# 4. Handoff: the four retired layouts become the ten social templates
rows_old = re.compile(r'\s*<tr><td class="mono">\.kp-tpl-(benefits|hero|product-row|top-card)</td>.*?</tr>')
page, n = rows_old.subn("", page)
assert n == 4, n
first_row = '<tr><td class="mono">.kp-slide</td>'
new_rows = (
    '<tr><td class="mono">T01 to T10 · html/tNN-ratio.html</td><td>Social templates (see Templates above), one standalone '
    'frame per layout and ratio in <code>clients/katapult/01-brand/templates/html/</code></td><td>Copy the frame into the job '
    'folder, swap copy and image <code>src</code>, keep every position and size. Headlines Aktiv Grotesk Regular; button '
    'instance 446px wide; logo and disclaimer where the template puts them</td></tr>\n          ')
page = page.replace(first_row, new_rows + first_row, 1)
old_pre = re.compile(r'<pre><code>&lt;article class="kp-post kp-r-4x5 kp-theme-darkblue kp-tpl-benefits"&gt;.*?</code></pre>', re.S)
page, n = old_pre.subn(
    '<pre><code>&lt;!-- social post: start from a template frame --&gt;\n'
    'cp clients/katapult/01-brand/templates/html/t06-4x5.html clients/katapult/03-work/social/&lt;job&gt;/01-4x5.html\n'
    '&lt;!-- edit the headline, subline and button text in place; point the photo img at the approved file --&gt;\n'
    'chrome --headless=new --hide-scrollbars --force-device-scale-factor=1 --window-size=1080,1350 \\\n'
    '  --screenshot=01-4x5.png file:///.../01-4x5.html</code></pre>', page)
assert n == 1, n
page = page.replace("Every post is one <code>article.kp-post</code>",
                    "Single posts start from a social template frame (T01 to T10). Carousels and organic patterns are one <code>article.kp-post</code>", 1)

# 5. Stale notes about the templates and the Regular weight
page = page.replace("safe zones, four post templates, and carousel", "safe zones, ten social templates in four ratios, and carousel")
page = page.replace("<h3>Two font weights missing</h3>", "<h3>SemiBold still missing</h3>")
page = page.replace("Figma headlines use Aktiv Grotesk SemiBold and body copy calls for Regular. Neither OTF is in the kit. Medium stands in for SemiBold, Light for Regular.",
                    "Aktiv Grotesk Regular is in the kit since 2026-10-13 and sets every social template headline. SemiBold is still not in the kit; carousel patterns keep Medium in its place.")

Path(dst).write_text(page, encoding="utf-8")
print(dst, f"{len(page) / 1e6:.2f} MB")
