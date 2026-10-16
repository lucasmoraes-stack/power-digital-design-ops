"""RKU26012 storyboard as static, Figma-safe HTML (+ PNG): one file per beat and size, frozen at that time.

Each file is self-contained (fonts and images as data URIs, no script) and built for Figma's HTML
import, which (checked 2026-10-15 on the LAB file, page "roku") breaks on:
  - pages without a fixed width: imported 1920 wide, so Meta frames got a dark strip
  - the TV shot: the camera is a scaled + translated layer inside an overflow clip; Figma drops the
    clip and the frame grew to the whole 2880 px room
  - SVG gradients referenced by id (the blimp body came in flat)
  - right-aligned text: Figma sets Roku Display a little wider than Chrome
So per frame: html/body get the canvas size; the city, the blimp and the TV shot are rasterised in
place (exact pixels, positioned absolutely); every element invisible at that time is dropped;
right-aligned figures get a fixed right-aligned box.

    python -I storyboard_html.py   -> 04-deliverables/ads/2026-rku26012-tv-ads-3-steps/storyboard/<size>/
                                      + storyboard-html-all/ (every HTML in one folder, for Figma import)
"""
import base64
import re
import shutil
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from anim import CANVAS, PLAT, SIZES  # noqa: E402

COMP = HERE / "hf" / "compositions"
DELIV = HERE.parents[2] / "04-deliverables" / "ads" / "2026-rku26012-tv-ads-3-steps"
OUT, ALL = DELIV / "storyboard", DELIV / "storyboard-html-all"
VER = "V2"
# (time, beat) - same beats as the hub storyboard
BEATS = [(1.4, "Intro"), (3.3, "Step 1 · Set Your Budget"), (4.8, "Step 1 · $5,000"), (7.4, "Step 2 · Interests"),
         (8.6, "Step 2 · Age"), (9.8, "Step 2 · ZIP"), (12.4, "Step 3 · Upload"), (14.2, "Step 3 · Launch"),
         (15.4, "The ad, full frame"), (17.3, "Camera pulls back to the living room"), (19.0, "CTA end frame")]
MIME = {".otf": "font/otf", ".png": "image/png", ".jpg": "image/jpeg", ".svg": "image/svg+xml"}
GUIDE = {17.3: (15.4, 17.4)}   # beat time -> (move start, move end) for the camera guide overlay
RASTER = ["city", "blimp"]                                # layers turned into a picture when visible

JS_PREP = """([W, H]) => {
  for (const el of [document.documentElement, document.body]) {
    el.style.width = W + 'px'; el.style.height = H + 'px'; el.style.overflow = 'hidden'; el.style.margin = '0';
  }
  const pc = document.getElementById('v-pc');             // right-aligned figure: fixed box with slack
  if (pc) { pc.style.display = 'inline-block'; pc.style.minWidth = '96px'; pc.style.textAlign = 'right'; pc.style.marginRight = '8px'; }
}"""

JS_BOX = """([id, W, H]) => {
  const el = document.getElementById(id);
  if (!el) return null;
  const cs = getComputedStyle(el);
  if (cs.display === 'none' || cs.visibility === 'hidden' || parseFloat(cs.opacity) === 0) return null;
  const r = el.getBoundingClientRect(), s = document.getElementById('st').getBoundingClientRect();
  const x0 = Math.max(0, Math.floor(r.left - s.left)), y0 = Math.max(0, Math.floor(r.top - s.top));
  const x1 = Math.min(W, Math.ceil(r.right - s.left)), y1 = Math.min(H, Math.ceil(r.bottom - s.top));
  return x1 > x0 && y1 > y0 ? [x0, y0, x1 - x0, y1 - y0, parseFloat(cs.opacity)] : null;
}"""

JS_SOLO = """([id, on]) => {
  const st = document.getElementById('st'), el = document.getElementById(id);
  if (on) {
    st.dataset.bg = st.getAttribute('style') || '';
    st.style.background = 'transparent'; document.body.style.background = 'transparent';
    document.documentElement.style.background = 'transparent';
    for (const c of st.children) if (c !== el) { c.dataset.vis = c.style.visibility || ''; c.style.visibility = 'hidden'; }
    el.dataset.op = el.style.opacity; el.style.opacity = 1;
  } else {
    st.setAttribute('style', st.dataset.bg); delete st.dataset.bg;
    document.body.style.background = ''; document.documentElement.style.background = '';
    for (const c of st.children) if (c !== el) { c.style.visibility = c.dataset.vis; delete c.dataset.vis; }
    el.style.opacity = el.dataset.op; delete el.dataset.op;
  }
}"""

JS_SWAP = """([id, box, src]) => {
  const el = document.getElementById(id), img = document.createElement('img');
  const [x, y, w, h, op] = box;
  // own id: the layer's CSS (e.g. the blimp drop-shadow) is already in the pixels; Figma would add it again as a box shadow
  img.src = src; img.id = id + '-img'; img.alt = '';
  img.style.cssText = `position:absolute;left:${x}px;top:${y}px;width:${w}px;height:${h}px;opacity:${op};margin:0;filter:none`;
  el.replaceWith(img);
}"""

JS_DUMP = """() => {
  for (const el of [...document.getElementById('st').querySelectorAll('*')]) {
    if (!el.isConnected) continue;
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden' || parseFloat(cs.opacity) === 0) el.remove();
  }
  return document.documentElement.outerHTML;
}"""


def data_uri(path):
    if path.name == "tv-ad-home.png":                     # the TV ad is a photo: JPEG q92 keeps files light
        import io
        from PIL import Image
        buf = io.BytesIO()
        Image.open(path).convert("RGB").save(buf, "JPEG", quality=92)
        return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
    return f"data:{MIME[path.suffix.lower()]};base64," + base64.b64encode(path.read_bytes()).decode()


def inline_urls(html):
    """../assets/... (fonts) -> data URIs, so the file stands alone."""
    cache = {}

    def sub(m):
        rel = m.group(2)
        if rel not in cache:
            cache[rel] = data_uri((COMP / rel).resolve())
        return f"{m.group(1)}{cache[rel]}{m.group(3)}"
    return re.sub(r'''(url\(["']?|src=")(\.\./assets/[^"')]+)(["']?\)|")''', sub, html)


def _jpeg(png):
    import io
    from PIL import Image
    buf = io.BytesIO()
    Image.open(io.BytesIO(png)).convert("RGB").save(buf, "JPEG", quality=94)
    return buf.getvalue()


def name(size, n):
    return f"RKU26012-TVAdvertising3Steps-{CANVAS[size]}-Storyboard-{PLAT[size]}-F{n:02d}-{VER}"


def load(pg, size, t):
    pg.goto((COMP / f"{size}.html").as_uri())
    pg.evaluate("window.ready")
    pg.wait_for_timeout(200)
    pg.evaluate(f"seek({t})")


# camera guide: where the shot starts (TV glass at the start zoom), mapped into the current framing,
# with arrows out to the frame corners and two labels. Own layer, easy to hide in Figma.
JS_GUIDE = """([t, a, b]) => {
  const R = C.room, [x0, y0, x1, y1] = R.screen, s0 = Math.max(W, H) / R.size, z0 = W * 1.02 / ((x1 - x0) * s0);
  const view = z => { const sc = s0 * z, vw = W / sc, vh = H / sc;
    return { sc, vw, vh, fx: clamp((x0 + x1) / 2 - vw / 2, 0, R.size - vw), fy: clamp((y0 + y1) / 2 - vh / 2, 0, R.size - vh) }; };
  const e = view(mix(z0, 1, io(lin(t, T.tv[0] + .35, T.cta + .1)))), s = view(z0);
  const L = (s.fx - e.fx) * e.sc, Tp = (s.fy - e.fy) * e.sc, Wd = s.vw * e.sc, Ht = s.vh * e.sc;
  const u = Math.min(W, H) / 1080, col = '#1BCECB', sw = 4 * u;
  const corners = [[L, Tp, 0, 0], [L + Wd, Tp, W, 0], [L, Tp + Ht, 0, H], [L + Wd, Tp + Ht, W, H]];
  let arrows = '';
  for (const [cx, cy, fx, fy] of corners) {
    const ax = cx + (fx - cx) * .18, ay = cy + (fy - cy) * .18, bx = cx + (fx - cx) * .62, by = cy + (fy - cy) * .62;
    const ang = Math.atan2(by - ay, bx - ax), h = 22 * u;
    arrows += `<path d="M${ax} ${ay}L${bx} ${by}" stroke="${col}" stroke-width="${sw}" stroke-linecap="round" fill="none"/>`
      + `<path d="M${bx} ${by}L${bx - h * Math.cos(ang - .45)} ${by - h * Math.sin(ang - .45)}L${bx - h * Math.cos(ang + .45)} ${by - h * Math.sin(ang + .45)}Z" fill="${col}"/>`;
  }
  const g = document.createElement('div');
  g.id = 'motion-guide';
  g.style.cssText = `position:absolute;left:0;top:0;width:${W}px;height:${H}px;z-index:50`;
  const pill = (txt, x, y, big) => `<div style="position:absolute;left:${x}px;top:${y}px;font-family:'Roku Display',sans-serif;font-weight:700;`
    + `font-size:${(big ? 30 : 24) * u}px;line-height:1.2;color:#20004C;background:${col};padding:${10 * u}px ${18 * u}px;border-radius:${10 * u}px;white-space:nowrap">${txt}</div>`;
  g.innerHTML = `<svg width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" style="position:absolute;left:0;top:0">`
    + `<rect x="${L}" y="${Tp}" width="${Wd}" height="${Ht}" fill="none" stroke="${col}" stroke-width="${sw}" stroke-dasharray="${18 * u} ${12 * u}"/>${arrows}</svg>`
    + pill(`CAMERA PULLS BACK · ${a.toFixed(1)} → ${b.toFixed(1)} s`, 40 * u, 40 * u, true)
    + pill('Shot starts here: the ad full screen', L + 12 * u, Tp + 12 * u, false);
  document.getElementById('st').appendChild(g);
}"""


def figma_html(pg, size, S, t):
    """Figma-safe HTML of the frame at t (modifies the page; reload before the next frame)."""
    W, H = S["W"], S["H"]
    load(pg, size, t)
    pg.evaluate(JS_PREP, [W, H])
    if pg.evaluate(JS_BOX, ["tv", W, H]):                 # TV shot (room + flash): the frame is one picture
        png = pg.screenshot(clip={"x": 0, "y": 0, "width": W, "height": H})
        pg.evaluate("""(src) => { const st = document.getElementById('st'); st.replaceChildren();
            const img = document.createElement('img'); img.src = src; img.alt = '';
            img.style.cssText = 'position:absolute;left:0;top:0;width:100%;height:100%'; st.appendChild(img); }""",
                    "data:image/jpeg;base64," + base64.b64encode(_jpeg(png)).decode())
    for lid in RASTER:
        box = pg.evaluate(JS_BOX, [lid, W, H])
        if not box:
            continue
        if lid == "blimp":                                # room for the drop shadow, or it is cut into a visible box
            x0, y0 = max(0, box[0] - 40), max(0, box[1] - 30)
            box = [x0, y0, min(W, box[0] + box[2] + 40) - x0, min(H, box[1] + box[3] + 60) - y0, box[4]]
        pg.evaluate(JS_SOLO, [lid, True])
        png = pg.screenshot(clip={"x": box[0], "y": box[1], "width": box[2], "height": box[3]}, omit_background=True)
        pg.evaluate(JS_SOLO, [lid, False])
        pg.evaluate(JS_SWAP, [lid, box, "data:image/png;base64," + base64.b64encode(png).decode()])
    if t in GUIDE:
        pg.evaluate(JS_GUIDE, [t, *GUIDE[t]])
    html = pg.evaluate(JS_DUMP)
    html = re.sub(r"<script\b[^>]*>.*?</script>", "", html, flags=re.S)       # frozen: no timeline
    return inline_urls(html)


def main():
    ALL.mkdir(parents=True, exist_ok=True)               # clear the files, keep the folder (it may be open in Explorer)
    for f in ALL.glob("*.html"):
        f.unlink()
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome", args=["--allow-file-access-from-files"])
        for size, S in SIZES.items():
            out = OUT / size
            out.mkdir(parents=True, exist_ok=True)
            pg = b.new_page(viewport={"width": S["W"], "height": S["H"]})
            for n, (t, beat) in enumerate(BEATS, 1):
                html = figma_html(pg, size, S, t)
                pg.screenshot(path=str(out / f"{name(size, n)}.png"), clip={"x": 0, "y": 0, "width": S["W"], "height": S["H"]})
                html = re.sub(r"<title>.*?</title>", f"<title>RKU26012 {size} F{n:02d} {t:.1f}s · {beat}</title>", html, count=1)
                f = out / f"{name(size, n)}.html"
                f.write_text("<!doctype html>\n" + html, encoding="utf8")
                shutil.copy2(f, ALL / f.name)
            pg.close()
            print(size, len(BEATS), "frames")
        b.close()


if __name__ == "__main__":
    main()
