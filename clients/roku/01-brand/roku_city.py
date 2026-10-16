"""Roku City silhouette: a flat skyline band (hills, towers, palms, Ferris wheel, bridge, water)
for dark purple backgrounds. Reusable across Roku jobs (first used in RKU26012).

Drawn in code, seeded, so every build gives the same city. Colors are parameters so the same
city can sit on Midnight Purple (default) or on a lighter ground.

    python -I roku_city.py            -> illustration/roku-city-silhouette.svg (3840 x 1100)
    from roku_city import city_svg     -> city_svg(w, h, ...) string, any size
"""
import math
import random
from pathlib import Path

OUT = Path(__file__).resolve().parent / "illustration"

DARK = {   # on Midnight Purple #20004C .. Primary Purple #4F01A3 gradients
    "haze": "#3A0F7E",      # far hills
    "back": "#2C0A66",      # far towers
    "front": "#1B0545",     # near towers, palms, wheel, bridge
    "win": ("#FFB98F", "#C9A6FF", "#FFE2C2"),   # lit windows: warm, lilac, pale
    "water": "#16033A",
}


def _f(v):
    return f"{v:.1f}".rstrip("0").rstrip(".")


def _tower(x, top, w, ground, c, rnd, crown=True):
    """A tower with an optional stepped crown or spire. Returns svg path data."""
    d = f"M{_f(x)} {_f(ground)}V{_f(top)}"
    kind = rnd.random() if crown else 1
    if kind < .25:                                   # stepped crown
        s = w * .18
        d += f"H{_f(x + s)}V{_f(top - w * .25)}H{_f(x + w - s)}V{_f(top)}"
    elif kind < .4:                                  # spire
        d += f"H{_f(x + w * .42)}L{_f(x + w * .5)} {_f(top - w * 1.1)}L{_f(x + w * .58)} {_f(top)}"
    elif kind < .52:                                 # slanted roof
        d += f"L{_f(x + w)} {_f(top - w * .35)}"
        return f'<path d="{d}V{_f(ground)}Z" fill="{c}"/>'
    d += f"H{_f(x + w)}V{_f(ground)}Z"
    return f'<path d="{d}" fill="{c}"/>'


def _palm(x, ground, h, c, rnd):
    """Curved trunk + 7 fronds."""
    lean = rnd.uniform(-.18, .18) * h
    tx, ty = x + lean, ground - h
    out = [f'<path d="M{_f(x - h * .025)} {_f(ground)}Q{_f(x + lean * .2)} {_f(ground - h * .5)} {_f(tx - h * .012)} {_f(ty)}'
           f'L{_f(tx + h * .012)} {_f(ty)}Q{_f(x + lean * .2 + h * .03)} {_f(ground - h * .5)} {_f(x + h * .025)} {_f(ground)}Z" fill="{c}"/>']
    for a in (-170, -140, -110, -70, -40, -10, -90):
        r = math.radians(a)
        L = h * rnd.uniform(.38, .5)
        ex, ey = tx + math.cos(r) * L, ty + math.sin(r) * L * .55 + L * .32
        mx, my = tx + math.cos(r) * L * .5, ty + math.sin(r) * L * .5 - L * .12
        w = h * .045
        out.append(f'<path d="M{_f(tx)} {_f(ty)}Q{_f(mx)} {_f(my - w)} {_f(ex)} {_f(ey)}Q{_f(mx)} {_f(my + w)} {_f(tx)} {_f(ty)}Z" fill="{c}"/>')
    return "".join(out)


def _wheel(cx, ground, r, c):
    cy = ground - r - r * .28
    s = max(2.0, r * .035)
    out = [f'<circle cx="{_f(cx)}" cy="{_f(cy)}" r="{_f(r)}" fill="none" stroke="{c}" stroke-width="{_f(s * 1.4)}"/>',
           f'<circle cx="{_f(cx)}" cy="{_f(cy)}" r="{_f(r * .86)}" fill="none" stroke="{c}" stroke-width="{_f(s * .7)}"/>']
    for i in range(16):
        a = i * math.pi / 8
        out.append(f'<line x1="{_f(cx)}" y1="{_f(cy)}" x2="{_f(cx + math.cos(a) * r)}" y2="{_f(cy + math.sin(a) * r)}" stroke="{c}" stroke-width="{_f(s * .6)}"/>')
        out.append(f'<rect x="{_f(cx + math.cos(a) * r - r * .06)}" y="{_f(cy + math.sin(a) * r)}" width="{_f(r * .12)}" height="{_f(r * .1)}" rx="{_f(r * .02)}" fill="{c}"/>')
    out.append(f'<path d="M{_f(cx - r * .55)} {_f(ground)}L{_f(cx)} {_f(cy)}L{_f(cx + r * .55)} {_f(ground)}" fill="none" stroke="{c}" stroke-width="{_f(s * 2)}"/>')
    out.append(f'<circle cx="{_f(cx)}" cy="{_f(cy)}" r="{_f(r * .07)}" fill="{c}"/>')
    return "".join(out)


def _bridge(x0, x1, ground, h, c, lamp):
    """Arched bridge from x0 to x1, deck at ground - h, arches down to the water."""
    deck = ground - h
    out = [f'<rect x="{_f(x0)}" y="{_f(deck)}" width="{_f(x1 - x0)}" height="{_f(h * .16)}" fill="{c}"/>',
           f'<rect x="{_f(x0)}" y="{_f(deck - h * .14)}" width="{_f(x1 - x0)}" height="{_f(h * .04)}" fill="{c}"/>']
    span = h * 1.5
    n = max(1, int((x1 - x0) // span))
    span = (x1 - x0) / n
    for i in range(n):
        a = x0 + i * span
        b = a + span
        out.append(f'<path d="M{_f(a)} {_f(deck)}H{_f(b)}V{_f(ground)}H{_f(b - span * .08)}Q{_f((a + b) / 2)} {_f(deck + h * .08)} {_f(a + span * .08)} {_f(ground)}H{_f(a)}Z" fill="{c}"/>')
    for i in range(int((x1 - x0) // (h * .5)) + 1):
        lx = x0 + i * h * .5
        out.append(f'<rect x="{_f(lx)}" y="{_f(deck - h * .14)}" width="{_f(h * .03)}" height="{_f(h * .14)}" fill="{c}"/>')
        if i % 2 == 0:
            out.append(f'<circle cx="{_f(lx + h * .015)}" cy="{_f(deck - h * .2)}" r="{_f(h * .025)}" fill="{lamp}"/>')
    return "".join(out)


def city_svg(w=3840, h=1100, seed=7, col=None, water=.2, windows=True, uid="rc"):
    """Skyline band w x h. The ground line sits at h * (1 - water); below it, the water with a
    faded reflection of the skyline. Fill the background yourself; this is transparent."""
    c = dict(DARK, **(col or {}))
    rnd = random.Random(seed)
    ground = h * (1 - water)
    sky = ground                                     # skyline drawn above this line
    k = h / 1100                                     # sizes are tuned on a 1100 px band
    g_back, g_front, g_win = [], [], []

    # far hills
    pts = [(0, ground - 260 * k)]
    x = 0
    while x < w:
        x += rnd.uniform(220, 420) * k
        pts.append((x, ground - rnd.uniform(180, 380) * k))
    d = f"M0 {_f(ground)}L" + "L".join(f"{_f(a)} {_f(b)}" for a, b in pts) + f"L{_f(w)} {_f(ground)}Z"
    hills = f'<path d="{d}" fill="{c["haze"]}"/>'

    # far towers: a denser cluster around the centre-left downtown
    x = -20 * k
    while x < w:
        bw = rnd.uniform(50, 120) * k
        dist = abs((x / w) - .42)
        hmax = (560 - dist * 520) * k
        bh = rnd.uniform(.45, 1) * max(160 * k, hmax)
        g_back.append(_tower(x, sky - bh, bw, ground, c["back"], rnd))
        x += bw + rnd.uniform(-6, 18) * k

    # near towers, avoid the wheel / bridge zone on the right
    x = -10 * k
    while x < w * .80:
        bw = rnd.uniform(60, 150) * k
        dist = abs((x / w) - .36)
        hmax = (430 - dist * 520) * k
        bh = rnd.uniform(.4, 1) * max(110 * k, hmax)
        top = sky - bh
        g_front.append(_tower(x, top, bw, ground, c["front"], rnd))
        if windows:
            cols, rows = int(bw // (18 * k)), int(bh // (26 * k))
            for r_ in range(rows - 1):
                for c_ in range(cols):
                    if rnd.random() < .16:
                        wx = x + (bw - cols * 18 * k) / 2 + c_ * 18 * k + 5 * k
                        wy = top + 18 * k + r_ * 26 * k
                        g_win.append(f'<rect x="{_f(wx)}" y="{_f(wy)}" width="{_f(7 * k)}" height="{_f(10 * k)}" fill="{rnd.choice(c["win"])}" opacity="{rnd.uniform(.5, .95):.2f}"/>')
        x += bw + rnd.uniform(10, 70) * k

    # palms along the waterfront
    palms = []
    x = rnd.uniform(10, 60) * k
    while x < w * .78:
        for _ in range(rnd.choice((1, 2, 3))):
            palms.append(_palm(x, ground, rnd.uniform(150, 250) * k, c["front"], rnd))
            x += rnd.uniform(40, 80) * k
        x += rnd.uniform(220, 520) * k

    # right side: low blocks, Ferris wheel, bridge into the water
    right = []
    x = w * .78
    while x < w * .93:
        bw = rnd.uniform(50, 110) * k
        right.append(_tower(x, sky - rnd.uniform(90, 200) * k, bw, ground, c["front"], rnd, crown=False))
        x += bw + rnd.uniform(4, 30) * k
    right.append(_wheel(w * .885, ground, 190 * k, c["front"]))
    right.append(_bridge(w * .80, w * 1.02, ground, 110 * k, c["front"], c["win"][0]))

    skyline = hills + "".join(g_back) + "".join(g_front) + "".join(palms) + "".join(right) + "".join(g_win)
    # water + reflection
    wat = (f'<defs><linearGradient id="{uid}f" x1="0" y1="0" x2="0" y2="1">'
           f'<stop offset="0" stop-color="#fff" stop-opacity=".55"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
           f'<mask id="{uid}m"><rect x="0" y="{_f(ground)}" width="{_f(w)}" height="{_f(h - ground)}" fill="url(#{uid}f)"/></mask></defs>'
           f'<rect x="0" y="{_f(ground)}" width="{_f(w)}" height="{_f(h - ground)}" fill="{c["water"]}"/>'
           f'<g mask="url(#{uid}m)" opacity=".5"><g transform="translate(0 {_f(2 * ground)}) scale(1 -1)">{skyline}</g></g>')
    lines = "".join(
        f'<rect x="{_f(rnd.uniform(0, w))}" y="{_f(ground + rnd.uniform(6, h - ground - 4))}" width="{_f(rnd.uniform(30, 160) * k)}" height="{_f(2 * k)}" fill="{rnd.choice(c["win"])}" opacity="{rnd.uniform(.12, .35):.2f}"/>'
        for _ in range(int(60 * w / 3840)))
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {_f(w)} {_f(h)}" width="{_f(w)}" height="{_f(h)}">'
            + wat + skyline + lines + "</svg>")


def blimp_svg(w=600, uid="bl", body=("#5A22B8", "#2E0A72", "#1E0552"), mark="#B48CFF"):
    """Roku City blimp with the Roku wordmark on the envelope, nose to the left, w x 0.42w.
    body = (highlight, mid, shadow). Wordmark paths come from identity/roku-wordmark.svg."""
    import re
    wm = re.findall(r'<path d="[^"]+"', (Path(__file__).resolve().parent / "identity" / "roku-wordmark.svg").read_text(encoding="utf8"))
    hi, mid, lo = body
    h = 252
    # envelope 600 x 200 centred at (300, 100); fins on the right; gondola under the belly
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 640 {h}" width="{w}" height="{round(w * h / 640)}">'
            f'<defs><linearGradient id="{uid}g" x1="0" y1="0" x2="0" y2="1">'
            f'<stop offset="0" stop-color="{hi}"/><stop offset=".55" stop-color="{mid}"/><stop offset="1" stop-color="{lo}"/></linearGradient>'
            f'<clipPath id="{uid}c"><ellipse cx="300" cy="104" rx="280" ry="92"/></clipPath></defs>'
            # fins
            f'<path d="M520 104 L612 22 Q628 18 626 36 L598 104 L626 172 Q628 190 612 186 Z" fill="{lo}"/>'
            f'<path d="M548 104 L612 70 L606 104 L612 138 Z" fill="{mid}"/>'
            # gondola
            f'<path d="M248 186 h104 q14 0 12 14 l-6 22 q-3 10 -14 10 h-88 q-11 0 -14 -10 l-6 -22 q-2 -14 12 -14z" fill="{lo}"/>'
            + "".join(f'<rect x="{262 + i * 22}" y="198" width="14" height="10" rx="2" fill="#FFB98F" opacity=".7"/>' for i in range(4))
            # envelope + panel seams + wordmark
            + f'<ellipse cx="300" cy="104" rx="280" ry="92" fill="url(#{uid}g)"/>'
            f'<g clip-path="url(#{uid}c)" fill="none" stroke="{lo}" stroke-opacity=".35" stroke-width="2">'
            + "".join(f'<ellipse cx="300" cy="104" rx="{r}" ry="92"/>' for r in (210, 130, 50))
            + '</g>'
            f'<ellipse cx="250" cy="58" rx="170" ry="22" fill="#fff" opacity=".08"/>'
            f'<g transform="translate(176 66) scale({248 / 628:.4f})" fill="{mark}">'
            + "".join(p + "/>" for p in wm) + "</g></svg>")


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    p = OUT / "roku-city-silhouette.svg"
    p.write_text(city_svg(), encoding="utf8")
    print(p, p.stat().st_size // 1024, "KB")
