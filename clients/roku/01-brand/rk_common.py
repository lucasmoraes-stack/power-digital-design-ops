"""Shared pieces for the Roku review pages (design system + deliverables hub).

Fonts, logos and the RKU26013 direction sketch are built here once so both
pages embed exactly the same assets.
"""
import base64
import re
from pathlib import Path

BRAND = Path(__file__).resolve().parent
ID = BRAND / "identity"

DS_URL = "https://claude.ai/code/artifact/bc7915dd-8473-4414-a915-a25334150616"
HUB_URL = "https://claude.ai/code/artifact/39370946-f238-45ad-a924-31f30d9266dd"

# Official Roku palette (Roku 2024 Brand Guidelines, captured in the Figma Library style guide 74:8964)
CORE = [
    ("Primary Purple", "#4F01A3", "RGB 79 1 163", "Pantone Medium Purple C"),
    ("Midnight Purple", "#20004C", "RGB 32 0 76", "Pantone 2755 C"),
]
ACCENT = [
    ("Electric Purple", "#853DFF", "RGB 133 61 255", "Pantone 2665 C"),
    ("Pink", "#EC4AF0", "RGB 236 74 240", "Pantone 238 C"),
    ("Orange", "#FF8553", "RGB 255 133 83", "Pantone 164 C"),
    ("Teal", "#1BCECB", "RGB 27 206 203", "Pantone 319 C"),
]
NEUTRAL = [
    ("Black", "#000000"), ("Gray 1", "#646464"), ("Gray 2", "#969696"),
    ("Gray 3", "#C8C8C8"), ("White", "#FFFFFF"),
]
# RKU26013 scene tints: proposal, derived from Primary / Electric for the "light purples" ask
SCENE = [
    ("Lilac 50", "#F5F0FF", "wall, sky top"),
    ("Lilac 100", "#E9DEFF", "far skyline, rug"),
    ("Lilac 200", "#D2BCFF", "near skyline, sofa"),
    ("Lilac 300", "#B391FF", "shadows, props"),
    ("Electric Purple", "#853DFF", "TV glow, props"),
    ("Primary Purple", "#4F01A3", "headline, TV frame"),
    ("Midnight Purple", "#20004C", "TV screen ground"),
    ("Orange", "#FF8553", "lamp light, one warm note"),
]


def font_face():
    out = []
    for w, n in [(400, "Regular"), (500, "Medium"), (700, "Bold"), (900, "Black")]:
        b = base64.b64encode((ID / "fonts" / f"RokuDisplay-{n}.subset.woff").read_bytes()).decode()
        out.append(
            f'@font-face{{font-family:"Roku Display";font-weight:{w};font-style:normal;'
            f'font-display:block;src:url(data:font/woff;base64,{b}) format("woff")}}'
        )
    return "\n".join(out)


def _paths(svg_file):
    return re.findall(r'<path d="[^"]+"[^>]*/>', (ID / svg_file).read_text(encoding="utf8"))


def wordmark(cls="", label="Roku"):
    """Roku wordmark, inherits color from CSS (fill=currentColor)."""
    return (f'<svg class="{cls}" viewBox="0 0 628 196" role="img" aria-label="{label}">'
            + "".join(_paths("roku-wordmark.svg")) + "</svg>")


def lockup(cls="", rk="#4F01A3", am="#646464"):
    """Roku Ads Manager lockup. rk = wordmark color, am = 'Ads Manager' color."""
    p = _paths("roku-ads-manager.svg")
    p = [re.sub(r'fill="[^"]+"', f'fill="{c}"', x) for x, c in zip(p, (rk, am))]
    return f'<svg class="{cls}" viewBox="0 0 499 57" role="img" aria-label="Roku Ads Manager">' + "".join(p) + "</svg>"


def img_data(path, mime="image/jpeg"):
    return f"data:{mime};base64," + base64.b64encode(Path(path).read_bytes()).decode()


def scene_svg(w=1440, h=1440, headline=("Put your ", "pet brand", " in their living room."),
              show_text=True, cls="scene", props="pet", uid="s"):
    """RKU26013 direction sketch: flat illustrated apartment living room that looks
    out on a city skyline in silhouette, brand on the TV screen. Built on a 1440 grid
    and re-composed per ratio (the room scales to width; headline zone grows on tall frames)."""
    if h < w:
        raise ValueError("16:9 is drawn as a schematic, not with this sketch")
    # tall frames: enlarge the room and crop its sides so the TV keeps its weight
    f = 1.0 if h <= w else (1.12 if h / w < 1.5 else 1.42)
    k = w / 1440.0 * f
    ox = (w - 1440 * k) / 2
    top = h - 1440 * k  # extra height goes to the wall/headline zone
    s = k

    def X(v): return round(ox + v * s, 1)
    def Y(v): return round(top + v * s, 1)
    def S(v): return round(v * s, 1)

    g = []
    U = uid
    g.append(f'<defs>'
             f'<linearGradient id="{U}sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F5F0FF"/><stop offset=".65" stop-color="#EBDDFF"/><stop offset="1" stop-color="#FFD9C8"/></linearGradient>'
             f'<linearGradient id="{U}scr" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#4F01A3"/><stop offset=".7" stop-color="#20004C"/></linearGradient>'
             f'<radialGradient id="{U}glow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#853DFF" stop-opacity=".55"/><stop offset="1" stop-color="#853DFF" stop-opacity="0"/></radialGradient>'
             f'<radialGradient id="{U}lamp" cx=".5" cy=".3" r=".6"><stop offset="0" stop-color="#FF8553" stop-opacity=".35"/><stop offset="1" stop-color="#FF8553" stop-opacity="0"/></radialGradient>'
             f'<clipPath id="{U}win"><rect x="{X(110)}" y="{Y(470)}" width="{S(1220)}" height="{S(560)}"/></clipPath>'
             f'</defs>')
    # wall
    g.append(f'<rect width="{w}" height="{h}" fill="#F5F0FF"/>')
    # window
    g.append(f'<rect x="{X(96)}" y="{Y(456)}" width="{S(1248)}" height="{S(588)}" rx="{S(10)}" fill="#E4D6FF"/>')
    g.append(f'<g clip-path="url(#{U}win)"><rect x="{X(110)}" y="{Y(470)}" width="{S(1220)}" height="{S(560)}" fill="url(#{U}sky)"/>')
    # far skyline
    far = [(110, 120, 250), (230, 90, 300), (320, 140, 230), (460, 80, 330), (540, 150, 260), (690, 110, 300),
           (800, 130, 220), (930, 95, 320), (1025, 140, 250), (1165, 100, 290), (1265, 70, 240)]
    for x, bw, bh in far:
        g.append(f'<rect x="{X(x)}" y="{Y(1030 - bh)}" width="{S(bw)}" height="{S(bh)}" fill="#DCC9FF"/>')
    g.append(f'<path d="M{X(470)} {Y(700)} l{S(40)} {S(-70)} l{S(40)} {S(70)}z" fill="#DCC9FF"/>')
    g.append(f'<rect x="{X(508)} " y="{Y(560)}" width="{S(4)}" height="{S(80)}" fill="#DCC9FF"/>')
    # near skyline
    near = [(110, 150, 170), (255, 110, 210), (360, 170, 150), (525, 120, 230), (640, 160, 180), (795, 120, 240),
            (910, 170, 160), (1075, 120, 210), (1190, 150, 180)]
    for i, (x, bw, bh) in enumerate(near):
        g.append(f'<rect x="{X(x)}" y="{Y(1030 - bh)}" width="{S(bw)}" height="{S(bh)}" fill="#C4A8FF"/>')
        for r in range(3):
            for c in range(3):
                if (i + r + c) % 3 == 0:
                    g.append(f'<rect x="{X(x + 22 + c * (bw - 44) / 3)}" y="{Y(1030 - bh + 26 + r * 40)}" width="{S(12)}" height="{S(16)}" fill="#F5F0FF" opacity=".85"/>')
    g.append('</g>')
    # mullions
    for mx in (512, 928):
        g.append(f'<rect x="{X(mx)}" y="{Y(470)}" width="{S(16)}" height="{S(560)}" fill="#E4D6FF"/>')
    g.append(f'<rect x="{X(96)}" y="{Y(1030)}" width="{S(1248)}" height="{S(14)}" fill="#D2BCFF"/>')
    # floor
    g.append(f'<rect x="0" y="{Y(1044)}" width="{w}" height="{max(0, h - Y(1044)) + 2}" fill="#E9DEFF"/>')
    g.append(f'<ellipse cx="{X(720)}" cy="{Y(1330)}" rx="{S(640)}" ry="{S(130)}" fill="#DCC9FF"/>')
    # lamp glow + lamp (right)
    g.append(f'<circle cx="{X(1240)}" cy="{Y(820)}" r="{S(260)}" fill="url(#{U}lamp)"/>')
    g.append(f'<rect x="{X(1236)}" y="{Y(800)}" width="{S(8)}" height="{S(260)}" fill="#4F01A3"/>')
    g.append(f'<path d="M{X(1180)} {Y(800)} L{X(1300)} {Y(800)} L{X(1275)} {Y(720)} L{X(1205)} {Y(720)}z" fill="#FFB596"/>')
    g.append(f'<rect x="{X(1205)}" y="{Y(1056)}" width="{S(70)}" height="{S(10)}" rx="{S(5)}" fill="#4F01A3"/>')
    # plant (left)
    g.append(f'<path d="M{X(150)} {Y(1060)} L{X(250)} {Y(1060)} L{X(238)} {Y(970)} L{X(162)} {Y(970)}z" fill="#B391FF"/>')
    for ang, ln in [(-38, 150), (-14, 190), (10, 170), (34, 140), (-60, 110), (58, 105)]:
        g.append(f'<ellipse cx="{X(200)}" cy="{Y(970 - ln / 2)}" rx="{S(26)}" ry="{S(ln / 2)}" fill="#853DFF" opacity=".75" transform="rotate({ang} {X(200)} {Y(970)})"/>')
    # TV glow, console, TV
    g.append(f'<ellipse cx="{X(720)}" cy="{Y(700)}" rx="{S(470)}" ry="{S(300)}" fill="url(#{U}glow)"/>')
    g.append(f'<rect x="{X(400)}" y="{Y(920)}" width="{S(640)}" height="{S(130)}" rx="{S(12)}" fill="#B391FF"/>')
    g.append(f'<rect x="{X(420)}" y="{Y(940)}" width="{S(290)}" height="{S(90)}" rx="{S(6)}" fill="#C4A8FF"/>')
    g.append(f'<rect x="{X(730)}" y="{Y(940)}" width="{S(290)}" height="{S(90)}" rx="{S(6)}" fill="#C4A8FF"/>')
    g.append(f'<rect x="{X(430)}" y="{Y(530)}" width="{S(580)}" height="{S(340)}" rx="{S(14)}" fill="#20004C"/>')
    g.append(f'<rect x="{X(442)}" y="{Y(542)}" width="{S(556)}" height="{S(316)}" rx="{S(6)}" fill="url(#{U}scr)"/>')
    g.append(f'<rect x="{X(700)}" y="{Y(870)}" width="{S(40)}" height="{S(50)}" fill="#20004C"/>')
    # brand on the screen
    g.append(f'<g transform="translate({X(472)} {Y(568)}) scale({round(S(84) / 628, 4)})" fill="#FFFFFF">'
             + "".join(_paths("roku-wordmark.svg")).replace('fill="currentColor"', '') + '</g>')
    if show_text:
        g.append(f'<text x="{X(720)}" y="{Y(690)}" text-anchor="middle" font-family="Roku Display, sans-serif" font-weight="500" font-size="{S(40)}" fill="#FFFFFF">Your business</text>')
        g.append(f'<text x="{X(720)}" y="{Y(738)}" text-anchor="middle" font-family="Roku Display, sans-serif" font-weight="500" font-size="{S(40)}" fill="#FFFFFF">ad is playing</text>')
    g.append(f'<path d="M{X(476)} {Y(806)} l{S(18)} {S(11)} l{S(-18)} {S(11)}z" fill="#FFFFFF"/>')
    g.append(f'<rect x="{X(510)}" y="{Y(815)}" width="{S(460)}" height="{S(5)}" rx="{S(2.5)}" fill="#FFFFFF" opacity=".3"/>')
    g.append(f'<rect x="{X(510)}" y="{Y(815)}" width="{S(170)}" height="{S(5)}" rx="{S(2.5)}" fill="#FFFFFF"/>')
    # coffee table + props
    g.append(f'<rect x="{X(300)}" y="{Y(1250)}" width="{S(840)}" height="{S(40)}" rx="{S(10)}" fill="#4F01A3"/>')
    g.append(f'<rect x="{X(340)}" y="{Y(1290)}" width="{S(26)}" height="{S(140)}" fill="#4F01A3"/>')
    g.append(f'<rect x="{X(1074)}" y="{Y(1290)}" width="{S(26)}" height="{S(140)}" fill="#4F01A3"/>')
    if props == "pet":
        g.append(f'<rect x="{X(400)}" y="{Y(1150)}" width="{S(300)}" height="{S(100)}" rx="{S(50)}" fill="#853DFF"/>')
        g.append(f'<rect x="{X(430)}" y="{Y(1140)}" width="{S(240)}" height="{S(50)}" rx="{S(25)}" fill="#B391FF"/>')
        g.append(f'<path d="M{X(760)} {Y(1250)} L{X(780)} {Y(1110)} L{X(880)} {Y(1110)} L{X(900)} {Y(1250)}z" fill="#B391FF"/>')
        for px, py, pr in [(830, 1178, 18), (808, 1150, 9), (830, 1142, 9), (852, 1150, 9)]:
            g.append(f'<circle cx="{X(px)}" cy="{Y(py)}" r="{S(pr)}" fill="#4F01A3"/>')
        g.append(f'<circle cx="{X(985)}" cy="{Y(1218)}" r="{S(32)}" fill="#FF8553"/>')
        g.append(f'<rect x="{X(930)}" y="{Y(1238)}" width="{S(120)}" height="{S(12)}" rx="{S(6)}" fill="#20004C" opacity=".15"/>')
    # headline
    if headline and show_text:
        a, b, c = headline
        # wall zone above the window: 0 .. Y(456). 9:16 keeps clear of the top 267px Meta UI band.
        z0 = 267 if h >= 2560 else 0
        z1 = Y(456)
        fs = 104 * w / 1440
        lk_h = 40 * w / 1440
        block = lk_h + 70 * w / 1440 + fs * 2.1
        y0 = z0 + (z1 - z0 - block) / 2
        lw = lk_h * 499 / 57
        p = _paths("roku-ads-manager.svg")
        p = [re.sub(r'fill="[^"]+"', f'fill="{col}"', x) for x, col in zip(p, ("#4F01A3", "#646464"))]
        g.append(f'<g transform="translate({round(w / 2 - lw / 2, 1)} {round(y0, 1)}) scale({round(lk_h / 57, 4)})">' + "".join(p) + '</g>')
        b1 = y0 + lk_h + 70 * w / 1440 + fs * .8
        common = f'text-anchor="middle" font-family="Roku Display, sans-serif" font-weight="700" font-size="{round(fs, 1)}" letter-spacing="{round(-fs * .01, 2)}" fill="#4F01A3"'
        g.append(f'<text x="{w / 2}" y="{round(b1, 1)}" {common}>{a}<tspan fill="#853DFF">{b}</tspan></text>')
        g.append(f'<text x="{w / 2}" y="{round(b1 + fs * 1.08, 1)}" {common}>{c.strip()}</text>')
    return f'<svg class="{cls}" viewBox="0 0 {w} {h}" role="img" aria-label="Direction sketch: illustrated living room looking out on a city skyline, brand on the TV">' + "".join(g) + "</svg>"
