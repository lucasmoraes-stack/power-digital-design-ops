"""Build the published Design System page from components.html.

Usage: python tools/build_ds_page.py     -> writes design-system.html in the kit folder

components.html stays the source (relative assets/ paths, copy-ready markup). The published page is the
same document with: every local image embedded (re-encoded to WebP, which browsers render; email clients
never see this page), each stored once and filled in on load, the artifact title, and the navigation pills to the Deliverables Hub and the Image
Library. WebP keeps the page under the Artifact's 16 MB limit as modules are added.
"""
from __future__ import annotations

import base64
import json
import io
import re
import sys
from pathlib import Path

from PIL import Image

KIT = Path(__file__).resolve().parents[1]
SRC = KIT / "components.html"
OUT = KIT / "design-system.html"
HUB = "https://claude.ai/code/artifact/70778e63-a022-4658-9d99-3c68be5815ee"
LIB = "https://claude.ai/code/artifact/4006b37f-7efb-4d33-9d00-99c119d08a88"
REF = re.compile(r"""(?<![\w/])(assets/[A-Za-z0-9_.\-]+\.(?:png|jpe?g|gif))""")

PILL = ('<div style="position:fixed;top:12px;right:12px;z-index:999999;pointer-events:none;display:flex;gap:8px;'
        "font:600 12px/1.3 -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Arial,sans-serif;\">"
        + "".join(f'<a href="{u}" target="_blank" rel="noopener" style="pointer-events:auto;display:inline-flex;align-items:center;'
                  'gap:6px;background:#141413;color:#faf9f5;text-decoration:none;padding:8px 14px;border-radius:999px;'
                  f'box-shadow:0 2px 10px rgba(0,0,0,.35);white-space:nowrap;">{t}</a>'
                  for u, t in ((LIB, "Image Library &rarr;"), (HUB, "Deliverables Hub &rarr;")))
        + "</div>")


# Each image is embedded once; this fills every reference (img src, td background, inline and <style> CSS)
# on load, so an asset used by twenty modules costs its bytes once.
FILL = """<script type="application/json" id="ds-img">__MAP__</script>
<script>(function(){var M=JSON.parse(document.getElementById('ds-img').textContent);
var R=/dsimg:(k\d+)/g,f=function(s){return s.replace(R,function(_,k){return M[k]||_;});};
document.querySelectorAll('[src^="dsimg:"]').forEach(function(e){e.setAttribute('src',f(e.getAttribute('src')));});
document.querySelectorAll('[background^="dsimg:"]').forEach(function(e){e.setAttribute('background',f(e.getAttribute('background')));});
document.querySelectorAll('[style*="dsimg:"]').forEach(function(e){e.setAttribute('style',f(e.getAttribute('style')));});
document.querySelectorAll('style').forEach(function(e){if(e.textContent.indexOf('dsimg:')>-1)e.textContent=f(e.textContent);});
})();</script>
"""


def encode(path: Path) -> str:
    raw = path.read_bytes()
    if path.suffix.lower() in (".png", ".jpg", ".jpeg"):
        im = Image.open(io.BytesIO(raw))
        im.load()
        alpha = im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info)
        im = im.convert("RGBA" if alpha else "RGB")
        buf = io.BytesIO()
        im.save(buf, "WEBP", quality=82 if alpha else 80, method=6)
        if buf.tell() < len(raw):
            return "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode()
    mime = {".png": "image/png", ".gif": "image/gif"}.get(path.suffix.lower(), "image/jpeg")
    return f"data:{mime};base64," + base64.b64encode(raw).decode()


def main() -> None:
    src = SRC.read_text(encoding="utf-8")
    cache: dict[str, str] = {}
    missing = set()

    def sub(m: re.Match) -> str:
        rel = m.group(1)
        if rel not in cache:
            p = KIT / rel
            if not p.is_file():
                missing.add(rel)
                return rel
            cache[rel] = encode(p)
            keys[rel] = f"k{len(keys)}"
        return "dsimg:" + keys[rel]

    keys: dict[str, str] = {}
    page = REF.sub(sub, src)
    data = json.dumps({keys[r]: u for r, u in cache.items()})
    page = page.replace("</body>", FILL.replace("__MAP__", data) + "</body>", 1)
    page = re.sub(r"<title>.*?</title>", "<title>Habit Outdoors Design System</title>", page, count=1, flags=re.S)
    page = re.sub(r'(<body\b[^>]*>)', lambda m: m.group(1) + PILL, page, count=1)
    OUT.write_text(page, encoding="utf-8")
    size = OUT.stat().st_size
    print(f"{OUT} · {size / 1e6:.2f} MB · {len(cache)} assets embedded")
    if missing:
        print("missing:", *sorted(missing), sep="\n  ")
    if size > 15.5e6:
        sys.exit("too big for an Artifact (16 MB)")


if __name__ == "__main__":
    main()
