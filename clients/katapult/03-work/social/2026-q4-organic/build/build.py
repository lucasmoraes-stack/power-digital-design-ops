"""Build the Katapult Q4 organic review page from copy.md + the approved DS.
Every on-art string is pulled from copy.md, never retyped."""
import re, html, pathlib

S = pathlib.Path(r"C:/Users/lucas/AppData/Local/Temp/claude/c--Users-lucas-OneDrive-Desktop-VAZIO-power-digital-ops/93dbe328-a65f-4b12-958f-086bc971a00c/scratchpad")
COPY = pathlib.Path(r"C:/Users/lucas/OneDrive/Desktop/VAZIO/power-digital-ops/clients/katapult/03-work/social/2026-q4-organic/copy.md")
OUT = S / "katapult-q4" / "index.html"

src = (S / "katapult-ds-src.html").read_text(encoding="utf-8").split("\n")
fonted = (S / "katapult-ds" / "index.html").read_text(encoding="utf-8").split("\n")
FONT_FACES = "\n".join(fonted[2:5])            # lines 3 to 5, verbatim, never printed
assert all(l.startswith("@font-face") for l in fonted[2:5])

# The DS web subset lacks glyphs the client copy uses (U+2260 "≠" in post 02). Re-subset each weight from the
# supplied OTF with the DS subset's own codepoints plus every character in copy.md, so no glyph falls back.
import base64, io
from fontTools.ttLib import TTFont
from fontTools import subset as _ft_subset
_ID = pathlib.Path(r"C:/Users/lucas/OneDrive/Desktop/VAZIO/power-digital-ops/clients/katapult/01-brand/identity")
_OTF = {"300": "Light", "500": "Medium", "700": "Bold"}
_copy_cps = {ord(c) for c in COPY.read_text(encoding="utf-8") if ord(c) > 31}
def _resubset(line):
    w = re.search(r"font-weight:(\d+)", line).group(1)
    b64 = re.search(r"base64,([A-Za-z0-9+/=]+)", line).group(1)
    old = set(TTFont(io.BytesIO(base64.b64decode(b64))).getBestCmap())
    font = TTFont(str(_ID / f"AktivGrotesk-{_OTF[w]}.otf"))
    want = (old | _copy_cps) & set(font.getBestCmap())
    opt = _ft_subset.Options(); opt.flavor = "woff"; opt.layout_features = ["*"]
    sub = _ft_subset.Subsetter(opt); sub.populate(unicodes=want); sub.subset(font)
    buf = io.BytesIO(); font.flavor = "woff"; font.save(buf)
    return line.replace(b64, base64.b64encode(buf.getvalue()).decode())
FONT_FACES = "\n".join(_resubset(l) for l in fonted[2:5])
_srct = "\n".join(src)
DS_CSS = _srct.split("<style>", 1)[1].split("</style>", 1)[0].split("\n", 4)[4]   # everything after the 3 font-face lines
SYMBOLS = re.search(r'<svg width="0" height="0".*?</svg>', _srct, re.S).group(0)
assert "V2 COMPONENTS" in DS_CSS and "k-check" in SYMBOLS
for _bad in ("k-support", "k-super", "k-seam", "k-arrow"):
    assert _bad not in SYMBOLS, _bad

# ---------------- parse copy.md ----------------
text = COPY.read_text(encoding="utf-8")
posts = {}
for m in re.finditer(r"^## Post (\d\d): (.+?)\n\nFormat: (.+?)\n\n```\n(.*?)\n```", text, re.S | re.M):
    num, title, fmt, body = m.group(1), m.group(2), m.group(3), m.group(4)
    lines = body.split("\n")
    def nxt(i):
        j = i + 1
        while lines[j].strip() == "":
            j += 1
        return j, lines[j]
    d = {"num": num, "title": title, "fmt": fmt, "slides": [], "options": []}
    cur = None
    i = 0
    while i < len(lines):
        l = lines[i]
        if re.fullmatch(r"Slide \d+", l):
            cur = {}
            d["slides"].append(cur)
        elif l == "Title:":
            i, v = nxt(i); cur["title"] = v
        elif l == "Subtext:":
            i, v = nxt(i); cur["sub"] = v
        elif l.startswith("HEADLINE: "):
            d["headline"] = l[len("HEADLINE: "):]
        elif l == "SUBTEXT:":
            i, v = nxt(i); d["sub"] = v
        elif l == "Question:":
            i, v = nxt(i); d["question"] = v
        elif l == "CTA:":
            i, v = nxt(i); d["cta"] = v
        elif l == "Prompt:":
            i, v = nxt(i); d["prompt_label"] = v
            i, v = nxt(i); d["prompt_line"] = v
        elif re.match(r"^[A-E]: ", l):
            d["options"].append(l)
        i += 1
    posts[num] = d
assert len(posts) == 15, len(posts)

E = lambda s: html.escape(s, quote=False)
def EC(s):
    """Escape an on-art copy string. Characters are untouched: hyphenated words get a no-break wrapper, and U+2026 gets a
    wrapper that paints it with three Aktiv periods (AktivGrotesk-Medium.otf ships a broken ellipsis glyph: middle dot misplaced)."""
    out = re.sub(r"(\S+-\S+)", r'<span class="kp-nw">\g<1></span>', E(s))
    return out.replace("…", '<span class="kp-ell">…</span>')

# =====================================================================
# v2 building blocks (art direction v2, 2026-09-28). No Bounce lines.
# Every on-art string comes from posts[...] (copy.md). Placeholder
# labels live only inside .kp-ph / .kp-cut / .kp-ico. The logo is the
# supplied artwork (#k-logo symbol in the DS sprite), an image, no text.
# =====================================================================
ON = ' class="on"'
SPAN = ' style="grid-column:1 / -1"'
LOGO = '<svg class="kp-logo" viewBox="0 0 521 116" role="img" aria-label="Katapult"><use href="#k-logo"/></svg>'
CHECK = '<svg viewBox="0 0 48 48" aria-hidden="true"><use href="#k-check"/></svg>'
SEND = ('<svg viewBox="0 0 48 48" aria-hidden="true"><path d="M8 24 H 38 M26 12 L 38 24 L 26 36" fill="none" stroke="currentColor" '
        'stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/></svg>')

def H(t, disp=False):
    return f'<h4 class="kp-headline{" kp-display" if disp else ""}">{EC(t)}</h4>'
def T(t):
    return f'<p class="kp-text">{EC(t)}</p>'
def SUB(t, style=""):
    st = f' style="{style}"' if style else ""
    return f'<p class="kp-sub"{st}>{EC(t)}</p>'
def CTA(t):
    return f'<span class="kp-cta wrap">{EC(t)}</span>'
def ico(tone, d, label, style=""):
    st = f"--d:{d}px;{style}" if isinstance(d, int) else f"--d:{d};{style}"
    return f'<div class="kp-ico t-{tone}" style="{st}" role="img" aria-label="Icon placeholder">Icon · {E(label)}</div>'
def ph(cls, style, label):
    return f'<div class="kp-ph {cls}" style="{style}" role="img" aria-label="Image placeholder"><span>{E(label)}</span></div>'
def cut(label, style=""):
    st = f' style="{style}"' if style else ""
    return f'<div class="kp-cut"{st} role="img" aria-label="Cutout placeholder">Cutout · {E(label)}</div>'
def A(style, inner="", cls=""):
    return f'<div class="kp-a {cls}" style="{style}">{inner}</div>'
def SH(style, inner="", cls=""):
    return f'<div class="kp-sh {cls}" style="{style}">{inner}</div>'
def UI(style, inner, cls=""):
    return f'<div class="kp-ui {cls}" style="{style}">{inner}</div>'
def STAGE(inner, cls=""):
    return f'<div class="kp-stage {cls}">{inner}</div>'
def COPY(title=None, sub=None, disp=False, extra=""):
    return ('<div class="kp-copy">' + (H(title, disp) if title else "") + (T(sub) if sub else "") + extra + '</div>')
def TRACK(k):
    return '<div class="kp-track" aria-hidden="true">' + "".join(f'<i{ON if i == k else ""}></i>' for i in range(5)) + '</div>'
def JOIN(s, boxes=0, bold_last=False):
    """One copy line set as stacked rows. Split only after sentence stops; every character stays, in order."""
    parts = re.split(r"(?<=\.) ", s)
    assert " ".join(parts) == s
    rows = []
    for i, p in enumerate(parts):
        box = '<i class="kp-box" aria-hidden="true"></i>' if i < boxes else ""
        b = " b" if bold_last and i == len(parts) - 1 else ""
        rows.append(f'<span class="kp-li{b}">{box}<span>{EC(p)}</span></span>')
    return '<p class="kp-join">' + " ".join(rows) + '</p>'
def cell(area, inner="", fill="var(--k-white)", cls="", style=""):
    return f'<div class="kp-cell {cls}" style="grid-area:{area};--f:{fill};{style}">{inner}</div>'

W, DB, PK, CR, LB, BL, OR, SF = ("var(--k-white)", "var(--k-dark-blue)", "var(--k-pink)", "var(--k-cream)",
                                 "var(--k-light-blue)", "var(--k-blue)", "var(--k-orange)", "var(--k-surface)")

def art(sid, theme, lay, bg="", ratio="4x5", cls=""):
    b = f'<div class="kp-bg">{bg}</div>' if bg else ""
    return f'<article class="kp-post kp-r-{ratio} kp-theme-{theme} kp-v2 {cls}" id="{sid}">{b}<div class="kp-lay">{lay}</div></article>'

def photo_card_slide(sid, theme, s, photo_label, photo_cls, head_extra="", body_extra="", plate="plate-p", icon=None):
    """UI: full-bleed photo, solid White card at the bottom carries the copy."""
    bg = ph(photo_cls, "inset:0;place-items:start center;padding-top:150px", photo_label)
    head = (f'<div class="kp-ui-head">{icon or ""}{H(s["title"])}{head_extra}</div>' if (icon or head_extra) else H(s["title"]))
    card = UI("flex:none", head + T(s["sub"]) + body_extra, cls=plate)
    return art(sid, theme, STAGE("") + card, bg=bg)

# ---------------------------------------------------------------------
def p01(p):
    s = p["slides"]; o = []
    o.append(("COL · editorial type with collage", "darkblue", LOGO + COPY(s[0]["title"], s[0]["sub"], disp=True) + STAGE(
        SH("left:0;top:16cqh;width:56cqh;height:56cqh;--f:var(--k-pink)", cut("TV, transparent PNG", "color:var(--k-white)"), "o")
        + SH("left:31cqw;top:2cqh;width:54cqh;height:54cqh;--f:var(--k-light-blue);transform:rotate(-6deg)", cut("sofa, transparent PNG"), "r")
        + SH("left:60cqw;top:30cqh;width:44cqw;height:66cqh;--f:var(--k-cream);transform:rotate(6deg)", cut("refrigerator, transparent PNG"), "r"),
        "bl-b bl-r")))
    cells = "".join(cell("auto", cut(x) + (f'<span class="kp-dot corner">{CHECK}</span>' if i == 1 else ""), W, "sel" if i == 1 else "")
                    for i, x in enumerate(["TV", "sofa", "laptop", "mattress", "washer", "tires"]))
    o.append(("PICK · product picker, one tile selected", "light", COPY(s[1]["title"], s[1]["sub"]) + STAGE(
        f'<div class="kp-grid" style="inset:0;grid-template-columns:repeat(3,1fr);grid-template-rows:repeat(2,1fr)">{cells}</div>')))
    o.append(("UI · photo with a floating card", "darkblue", None))
    o.append(("CTRL · progress segments card", "light", COPY(s[3]["title"], s[3]["sub"]) + STAGE(
        SH("left:60cqw;top:26cqh;width:58cqh;height:58cqh;--f:var(--k-pink)", "", "o")
        + UI("position:absolute;left:0;right:5cqw;bottom:10cqh;padding:84px 48px",
             f'<div class="kp-row" style="gap:26px">{ico("s", 150, "calendar")}'
             '<div class="kp-segs kp-grow" style="gap:10px">' + "".join(f'<i{ON if i < 6 else ""} style="height:110px"></i>' for i in range(10)) + '</div>'
             f'{ico("p", 150, "house")}</div>',
             "plate-db"))))
    o.append(("TRI · triangle, three corner icons", "darkblue", COPY(s[4]["title"], s[4]["sub"]) + STAGE(
        A("left:50%;top:0;height:min(100cqh,80cqw);aspect-ratio:1.16;transform:translateX(-50%)",
          '<div class="kp-tri" style="inset:10% 9% 7% 9%;--f:var(--k-blue)"></div>'
          + A("left:50%;top:0;transform:translateX(-50%)", ico("p", 170, "tag, purchase"))
          + A("left:0;bottom:0", ico("w", 170, "loop, keep leasing"))
          + A("right:0;bottom:0", ico("c", 170, "return arrow"))))))
    out = []
    for i, (name, theme, lay) in enumerate(o):
        sid = f"p01-s{i+1}"
        if lay is None:
            a = photo_card_slide(sid, theme, s[2], "Photo · real person smiling at their phone, just approved · plain solid Light Blue background · face in the upper half, uncropped",
                                 "lb", icon=ico("s", 120, "check"), plate="plate-p")
        else:
            a = art(sid, theme, lay)
        out.append((sid, name, a))
    return out

def p02(p):
    s = p["slides"]; out = []
    venn = ('<div class="kp-venn" style="--vd:min(60cqw,100cqh);--vw:calc(var(--vd) * 1.62)">'
            '<div class="c l" style="--f:var(--k-blue)"></div>'
            '<div class="c r" style="--f:var(--k-pink)"><div class="lens" style="--f:var(--k-dark-blue);left:calc(var(--vd) - var(--vw))"></div></div>'
            + A("left:calc(var(--vd) * .16);top:50%;transform:translateY(-50%)", ico("w", 150, "credit card"))
            + A("right:calc(var(--vd) * .16);top:50%;transform:translateY(-50%)", ico("p", 150, "product")) + '</div>')
    out.append(("VENN · two circles, two paths", "light", COPY(s[0]["title"], s[0]["sub"]) + STAGE(venn)))
    card = (A("left:50%;top:52%;width:52cqw;aspect-ratio:1.586;transform:translate(-38%,-58%) rotate(7deg);background:var(--k-white);border-radius:40px")
            + A("left:50%;top:52%;width:56cqw;aspect-ratio:1.586;transform:translate(-60%,-46%) rotate(-8deg);background:var(--k-dark-blue);border-radius:44px",
                SH("left:9%;top:26%;width:17%;height:24%;--f:var(--k-cream);border-radius:14px")
                + A("left:9%;right:9%;bottom:16%;display:flex;gap:5%",
                    "".join('<i style="flex:1;height:30px;border-radius:15px;background:var(--k-light-blue)"></i>' for _ in range(4)))
                + SH("right:9%;top:22%;width:22%;height:14%;--f:var(--k-pink);border-radius:999px")))
    out.append(("BLOCK · top panel with a card object", "blue", STAGE(SH("inset:0;--f:var(--k-light-blue)") + card, "bl-t bl-x") + COPY(s[1]["title"], s[1]["sub"])))
    pills = "".join(UI("flex:1 1 0;max-height:20cqh;flex-direction:row;align-items:center;padding:0 30px;border-radius:999px;box-shadow:none;gap:24px",
                       ico("s", "min(96px,13cqh)", "calendar") + '<span class="kp-grow"></span>'
                       + (f'<span class="kp-box on">{CHECK}</span>' if i < 2 else '<span class="kp-box"></span>'))
                    for i in range(4))
    out.append(("STACK · product plus a stack of payments", "pink", COPY(s[2]["title"], s[2]["sub"]) + STAGE(
        SH("left:0;top:50%;height:min(100cqh,48cqw);aspect-ratio:1;transform:translateY(-50%);--f:var(--k-cream)", cut("sofa in use, transparent PNG"), "o")
        + A(f"right:0;top:0;bottom:0;width:46cqw;display:flex;flex-direction:column;justify-content:center;gap:3cqh", pills))))
    out.append(("BLOCK · unequal blocks, small score vs full picture", "darkblue", COPY(s[3]["title"], s[3]["sub"]) + STAGE(
        SH("left:0;bottom:0;width:27cqw;height:27cqw;--f:var(--k-pink)",
           UI("position:absolute;inset:26% 18%;padding:0 14%;box-shadow:none;border-radius:16px;justify-content:center;gap:12px",
              '<div class="kp-bar db"></div><div class="kp-bar" style="width:60%"></div>'), "r")
        + ph("cr", "left:31cqw;top:0;bottom:0;right:0;border-radius:36px;place-items:start center;padding-top:60px",
             "Portrait · real person, uplifted, the full picture of their life · plain solid Cream background · face in the upper half, uncropped")
        + A("left:35cqw;bottom:4cqh;display:flex;gap:18px", ico("w", 112, "home") + ico("w", 112, "briefcase") + ico("w", 112, "heart")))))
    radios = ('<div class="kp-row" style="gap:24px"><span class="kp-radio"></span>' + ico("s", 104, "credit card")
              + '<span style="width:34px"></span><span class="kp-radio on"></span>' + ico("s", 104, "product") + '</div>')
    out.append(("UI + CTRL · photo, floating card with two radios", "light", None))
    res = []
    for i, (name, theme, lay) in enumerate(out):
        sid = f"p02-s{i+1}"
        if lay is None:
            a = photo_card_slide(sid, theme, s[4], "Photo · real shopper at checkout, smiling, phone in hand · plain solid Cream background · face in the upper half, uncropped",
                                 "cr", body_extra=radios, plate="plate-db")
        else:
            a = art(sid, theme, lay)
        res.append((sid, name, a))
    return res

def p03(p):
    s = p["slides"]; res = []
    step = '<i style="width:44%;aspect-ratio:1;border-radius:10px;background:var(--k-white)"></i>'
    big = {  # (row, col): (fill, icon tone, icon label)
        (1, 1): (SF, "w", "phone"), (1, 4): (DB, "db", "check"), (3, 5): (CR, "c", "shopping bag"),
        (5, 3): (BL, "w", "calendar"), (5, 7): (OR, "w", "three paths")}
    path = [(1, c) for c in range(1, 8)] + [(2, 7)] + [(3, c) for c in range(7, 0, -1)] + [(4, 1)] + [(5, c) for c in range(1, 8)]
    cells = ""
    for (r, c) in path:
        if (r, c) in big:
            f, t, lab = big[(r, c)]
            cells += cell(f"{r}/{c}", ico(t, "min(96px,15cqh)", lab), f, style="--cr:20px")
        else:
            cells += cell(f"{r}/{c}", step, "transparent")
    board = f'<div class="kp-grid" style="inset:0;grid-template-columns:repeat(7,1fr);grid-template-rows:repeat(5,1fr);--gap:12px">{cells}</div>'
    res.append(("BOARD · the whole game board", "pink", LOGO + COPY(s[0]["title"], s[0]["sub"], disp=True) + STAGE(board)))
    fields = '<div class="kp-field"><span class="kp-caret"></span></div><div class="kp-field"></div><div class="kp-field"></div><div class="kp-btn"></div>'
    res.append(("IN · input card over a phone", "light", TRACK(0) + COPY(s[1]["title"], s[1]["sub"], disp=True) + STAGE(
        ph("lb", "left:48cqw;right:0;top:4cqh;bottom:0;border-radius:64px 64px 0 0;place-items:start center;padding:70px 40px",
           "Phone mockup · real Katapult application screen, client supplied · crop tight so it reads · bleeds off the bottom edge")
        + UI("position:absolute;left:0;width:60cqw;top:26cqh;gap:24px", fields, "plate-p"), "bl-b")))
    front = UI("position:absolute;left:3cqw;right:3cqw;top:24cqh;gap:26px",
               f'<div class="kp-ui-head">{ico("s", 140, "check")}<div class="kp-grow" style="display:flex;flex-direction:column;gap:18px">'
               '<div class="kp-segs"><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i><i class="on"></i></div>'
               '<div class="kp-bar db" style="width:70%"></div></div></div>', "plate-p")
    res.append(("STACK · fanned notification cards", "darkblue", TRACK(1) + COPY(s[2]["title"], s[2]["sub"], disp=True) + STAGE(
        '<div class="kp-fan" style="--f:var(--k-light-blue);left:8cqw;right:8cqw;top:6cqh;height:60cqh;transform:rotate(-8deg)"></div>'
        '<div class="kp-fan" style="--f:var(--k-cream);left:5cqw;right:5cqw;top:12cqh;height:60cqh;transform:rotate(-4deg)"></div>' + front)))
    tiles = "".join(A(f"left:{x}cqw;bottom:24cqh;width:26cqw;height:58cqh;background:var(--k-white);border-radius:28px 28px 0 0", cut(lab))
                    for x, lab in ((9, "TV"), (37, "armchair"), (65, "washer")))
    res.append(("PICK · shelf of three categories", "cream", TRACK(2) + COPY(s[3]["title"], s[3]["sub"], disp=True) + STAGE(
        SH("left:0;right:0;bottom:0;height:24cqh;--f:var(--k-dark-blue)") + tiles
        + A("right:9cqw;bottom:6cqh", ico("p", "min(120px,13cqh)", "shopping bag")), "bl-x bl-b")))
    pinkcells = {(1, 5), (3, 5), (5, 5)}
    cal = "".join(f'<i style="border-radius:14px;background:{PK if (r, c) in pinkcells else SF};display:grid;place-items:center">'
                  + (f'<span style="width:60%;height:60%;color:var(--k-white);display:grid">{CHECK}</span>' if (r, c) in pinkcells else "") + '</i>'
                  for r in range(1, 6) for c in range(1, 8))
    res.append(("CAL · calendar card, every second week", "blue", TRACK(3) + COPY(s[4]["title"], s[4]["sub"], disp=True) + STAGE(
        UI("position:absolute;inset:0;padding:0;gap:0;overflow:hidden",
           '<div style="flex:none;height:13cqh;background:var(--k-pink)"></div>'
           f'<div style="flex:1;display:grid;grid-template-columns:repeat(7,1fr);grid-template-rows:repeat(5,1fr);gap:12px;padding:26px">{cal}</div>', "plate-db")
        + A("left:22cqw;top:-26px;width:30px;height:13cqh;border-radius:15px;background:var(--k-dark-blue)")
        + A("right:22cqw;top:-26px;width:30px;height:13cqh;border-radius:15px;background:var(--k-dark-blue)"))))
    doors = "".join(SH(f"left:{x}cqw;bottom:0;width:29cqw;height:{h}cqh;--f:{f};border-radius:44px 44px 0 0",
                       A("left:50%;top:34px;transform:translateX(-50%)", ico(t, 150, lab)))
                    for x, h, f, t, lab in ((0, 70, DB, "db", "tag, purchase"), (35.5, 82, CR, "c", "loop, keep leasing"), (71, 94, W, "w", "return arrow")))
    res.append(("BLOCK · three doors", "orange", TRACK(4) + COPY(s[5]["title"], s[5]["sub"], disp=True) + STAGE(doors, "bl-b")))
    return [(f"p03-s{i+1}", n, art(f"p03-s{i+1}", t, l)) for i, (n, t, l) in enumerate(res)]

def p04(p):
    s = p["slides"]; res = []
    card = UI("position:absolute;left:0;width:66cqw;top:50%;transform:translateY(-50%);padding:46px 44px", JOIN(s[0]["sub"], boxes=3, bold_last=True), "plate-p")
    res.append(("CHECK · notes card checklist", "cream", LOGO + COPY(s[0]["title"]) + STAGE(
        ph("lb", "left:50cqw;right:0;top:0;bottom:0;border-radius:40px 0 0 40px;padding-left:18cqw",
           "Portrait · real person, uplifted, taking life in stride · plain solid Light Blue background · face in the right half, uncropped") + card, "bl-r")))
    rem = UI("position:absolute;right:7cqw;bottom:-30px;width:46cqw;flex-direction:row;align-items:center;gap:24px;padding:26px 30px",
             ico("s", 100, "refrigerator") + '<div class="kp-grow" style="display:flex;flex-direction:column;gap:16px"><div class="kp-bar db" style="width:80%"></div><div class="kp-bar" style="width:50%"></div></div>'
             + f'<span class="kp-box on">{CHECK}</span>', "plate-p")
    res.append(("BLOCK · photo band over a color panel, reminder card", "darkblue", STAGE(
        ph("lb", "inset:0;border-radius:0 0 48px 48px;place-items:start start;padding:140px 90px",
           "Photo · real person smiling beside their new refrigerator, the fix, never the breakdown · plain solid Light Blue background · face in the left half, uncropped") + rem,
        "bl-t bl-x") + COPY(s[1]["title"], s[1]["sub"])))
    grid = ('<div class="kp-grid" style="inset:0;grid-template-columns:1fr 1.3fr 1fr;grid-template-rows:1fr 1fr">'
            + cell("1/1", ico("s", 130, "tire"), W) + cell("2/1", ico("p", 130, "road"), PK)
            + cell("1/2/3/3", ph("lb", "inset:0", "Photo · real person, happy, next to a fresh set of new tires · plain solid Light Blue background · face uncropped"), LB)
            + cell("1/3", ico("db", 130, "map pin"), DB) + cell("2/3", ico("s", 130, "car"), W) + '</div>')
    res.append(("GRID · photo in an icon grid", "cream", COPY(s[2]["title"], s[2]["sub"]) + STAGE(grid)))
    res.append(("UI + CTRL · photo, floating card with a toggle", "darkblue", None))
    blocks = (SH("left:0;bottom:4cqh;width:38cqh;height:38cqh;--f:var(--k-pink);transform:rotate(-6deg)", cut("refrigerator", "color:var(--k-white)"), "r")
              + SH("left:28cqw;bottom:18cqh;width:50cqh;height:50cqh;--f:var(--k-light-blue)", cut("new tires"), "r")
              + SH("left:57cqw;bottom:32cqh;width:62cqh;height:62cqh;--f:var(--k-white);transform:rotate(6deg)", cut("desk chair"), "r"))
    res.append(("COL · the three fixes, climbing", "cream", COPY(s[4]["title"], s[4]["sub"]) + STAGE(blocks, "bl-b bl-r")))
    out = []
    for i, (n, t, l) in enumerate(res):
        sid = f"p04-s{i+1}"
        if l is None:
            a = photo_card_slide(sid, t, s[3], "Photo · real person enjoying their upgraded home office setup · plain solid Light Blue background · face in the upper half, uncropped",
                                 "lb", head_extra='<span class="kp-tog on" aria-hidden="true"></span>', plate="plate-p")
        else:
            a = art(sid, t, l)
        out.append((sid, n, a))
    return out

def p05(p):
    s = p["slides"]; res = []
    prints = "".join(A(f"left:{x}cqw;top:{y}cqh;width:40cqw;height:88cqh;transform:rotate({r}deg);--plate:{pl}",
                       ph(c, "", lab), "kp-print")
                     for x, y, r, pl, c, lab in ((0, 8, -7, CR, "cr", "Photo · a new home: real family settling in with new furniture · plain solid Cream background · faces uncropped"),
                                                 (60, 8, 7, PK, "pk", "Photo · a new goal: real person with the thing they have been wanting · plain solid Pink background · face uncropped"),
                                                 (30, 2, 0, LB, "lb", "Photo · a new routine: real person with new tech in their day · plain solid Light Blue background · face uncropped")))
    res.append(("STACK · three prints fanned", "darkblue", LOGO + COPY(s[0]["title"], s[0]["sub"]) + STAGE(prints)))
    plan = ('<div class="kp-a" style="inset:0;background:var(--k-dark-blue);border-radius:30px;padding:14px;display:grid;grid-template-columns:2fr 1.2fr 1.2fr;grid-template-rows:1fr 1fr;gap:14px">'
            + cell("1/1/3/2", ico("w", 150, "sofa"), PK, style="--cr:16px") + cell("1/2/2/4", ico("w", 130, "refrigerator"), CR, style="--cr:16px")
            + cell("2/2", ico("w", 120, "lamp"), LB, style="--cr:16px") + cell("2/3", ico("s", 120, "plant"), W, style="--cr:16px") + '</div>')
    res.append(("BLOCK · floor plan of color blocks", "light", COPY(s[1]["title"], s[1]["sub"]) + STAGE(plan)))
    icons = {(1, 1): "coffee", (2, 3): "laptop", (3, 5): "headphones", (1, 6): "dumbbell"}
    pink = {(1, 4), (2, 6), (3, 2), (2, 1)}
    wk = "".join(f'<i style="border-radius:16px;background:{PK if (r, c) in pink else SF};display:grid;place-items:center">'
                 + (ico("w", "min(88px,11cqh)", icons[(r, c)]) if (r, c) in icons else "") + '</i>' for r in range(1, 4) for c in range(1, 8))
    hdr = "".join('<i style="height:18px;border-radius:9px;background:var(--k-dark-blue)"></i>' for _ in range(7))
    res.append(("CAL · week planner", "darkblue", COPY(s[2]["title"], s[2]["sub"]) + STAGE(UI(
        "position:absolute;inset:0;padding:32px;gap:22px",
        f'<div style="display:grid;grid-template-columns:repeat(7,1fr);gap:12px;padding-inline:18%">{hdr}</div>'
        f'<div style="flex:1;display:grid;grid-template-columns:repeat(7,1fr);grid-template-rows:repeat(3,1fr);gap:12px">{wk}</div>', "plate-p"))))
    ttt = "".join(cell("auto", ico("p", "min(130px,16cqh)", lab) if lab else "", PK if lab else SF, style="--cr:20px")
                  for lab in ("laptop", None, None, None, "bike", None, None, None, "guitar"))
    res.append(("GRID · tic-tac-toe, three in a row", "light", COPY(s[3]["title"], s[3]["sub"]) + STAGE(
        f'<div class="kp-grid" style="left:50%;top:0;height:100cqh;max-width:100cqw;aspect-ratio:1;transform:translateX(-50%);grid-template-columns:repeat(3,1fr);grid-template-rows:repeat(3,1fr);--gap:16px;background:var(--k-dark-blue);padding:16px;border-radius:30px">{ttt}</div>')))
    steps = "".join(SH(f"left:{x}cqw;bottom:0;width:10cqw;height:{h}cqh;--f:{f};border-radius:22px 22px 0 0")
                    for x, h, f in ((70, 22, DB), (80.5, 44, W), (91, 66, CR)))
    res.append(("COL · portrait with stepping squares", "pink", COPY(s[4]["title"], s[4]["sub"]) + STAGE(
        ph("cr", "left:0;width:66cqw;top:0;bottom:0;border-radius:40px 40px 0 0",
           "Portrait · real person, uplifted, moving forward · plain solid Cream background · face uncropped") + steps, "bl-b")))
    return [(f"p05-s{i+1}", n, art(f"p05-s{i+1}", t, l)) for i, (n, t, l) in enumerate(res)]

def p06(p):
    s = p["slides"]; res = []
    fan = "".join(f'<div class="kp-fan" style="--f:{f};left:32cqw;width:36cqw;bottom:-16cqh;height:96cqh;transform:rotate({r}deg)">'
                  + A("left:50%;top:44px;transform:translateX(-50%)", ico(t, 150, lab)) + '</div>'
                  for f, r, t, lab in ((DB, -17, "db", "credit card"), (CR, 17, "c", "cash"), (PK, 0, "p", "another way to pay")))
    res.append(("STACK · a hand of option cards", "light", LOGO + COPY(s[0]["title"], s[0]["sub"]) + STAGE(fan, "bl-b")))
    ppl = [("pk", "Pink", "young adult"), ("lb", "Light Blue", "parent"), ("cr", "Cream", "older adult"), ("bl", "Blue", "student"), ("or", "Orange", "retiree"), ("wh", "White", "young professional")]
    g = "".join(cell("auto", ph(c, "inset:0;padding:22px;font-size:16px", f"Portrait · real {who}, uplifted · plain solid {nm} background · face uncropped"), "transparent")
                for c, nm, who in ppl)
    res.append(("GRID · six different shoppers", "darkblue", COPY(s[1]["title"], s[1]["sub"]) + STAGE(
        f'<div class="kp-grid" style="inset:0;grid-template-columns:repeat(3,1fr);grid-template-rows:repeat(2,1fr)">{g}</div>')))
    cols = "".join(f'<div style="position:relative;flex:1 1 0;height:{h}%;background:{f};border-radius:28px 28px 0 0">'
                   + A("left:50%;top:0;transform:translate(-50%,-50%)", ico(t, 112, lab)) + '</div>'
                   for h, f, t, lab in ((72, PK, "p", "score card"), (72, DB, "db", "home"), (72, W, "w", "briefcase"), (72, BL, "w", "heart"), (72, OR, "w", "phone")))
    res.append(("BLOCK · columns, many sides of one story", "cream", COPY(s[2]["title"], s[2]["sub"]) + STAGE(
        A("left:0;right:0;top:9cqh;bottom:0;display:flex;align-items:flex-end;gap:3cqw", cols), "bl-b")))
    rows = '<div class="kp-rule"></div>'.join(
        f'<div class="kp-row" style="padding:26px 0">{ico("s", 116, lab)}<span class="kp-grow"></span><span class="kp-tog{" on" if on else ""}"></span></div>'
        for lab, on in (("calendar", True), ("wallet", False), ("product", True)))
    res.append(("CTRL · three toggles", "pink", COPY(s[3]["title"], s[3]["sub"]) + STAGE(
        UI("position:absolute;left:0;right:0;top:50%;transform:translateY(-50%);gap:0;padding:18px 52px", rows, "plate-db"))))
    res.append(("BLOCK · one mark, split panel", "blue", STAGE(
        SH("inset:0;--f:var(--k-pink);border-radius:0 0 48px 48px")
        + A("left:50%;top:56%;width:min(56cqh,46cqw);aspect-ratio:1;transform:translate(-50%,-50%);border-radius:50%;background:var(--k-white);display:grid;place-items:center;color:var(--k-pink)",
            f'<span style="width:56%;height:56%;display:grid">{CHECK}</span>'), "bl-t bl-x") + COPY(s[4]["title"], s[4]["sub"])))
    return [(f"p06-s{i+1}", n, art(f"p06-s{i+1}", t, l)) for i, (n, t, l) in enumerate(res)]

def p13(p):
    s = p["slides"]; res = []
    score = UI("position:absolute;left:0;top:12cqh;width:28cqw;padding:26px 28px;gap:14px",
               '<div class="kp-bar db"></div><div class="kp-bar" style="width:60%"></div>', "plate-db")
    res.append(("COL · portrait with a small score card", "pink", LOGO + COPY(s[0]["title"], s[0]["sub"]) + STAGE(
        ph("cr", "left:12cqw;right:0;top:0;bottom:0;border-radius:40px 40px 0 0;padding-left:16cqw",
           "Portrait · real person, uplifted, full of life · plain solid Cream background · face centered right, uncropped") + score, "bl-b")))
    labs = ["home", "briefcase", "paycheck", "heart", None, "phone", "cart", "calendar", "car"]
    g = ""
    for i, lab in enumerate(labs):
        corner = i in (0, 2, 6, 8)
        if lab is None:
            g += cell("auto", ph("lb", "inset:0;padding:16px;font-size:15px;outline-offset:-10px", "Portrait · real shopper · Light Blue background · face uncropped"), LB, style="--cr:22px")
        else:
            g += cell("auto", ico("p" if corner else "w", "min(118px,15cqh)", lab), PK if corner else BL, style="--cr:22px")
    res.append(("GRID · life factors around the person", "darkblue", COPY(s[1]["title"], s[1]["sub"]) + STAGE(
        f'<div class="kp-grid" style="left:50%;top:0;height:100cqh;max-width:100cqw;aspect-ratio:1;transform:translateX(-50%);grid-template-columns:repeat(3,1fr);grid-template-rows:repeat(3,1fr);--gap:16px">{g}</div>')))
    res.append(("UI · photo with a floating card", "pink", None))
    slider = (f'<div class="kp-row" style="justify-content:space-between">{ico("s", 190, "tag, purchase")}{ico("p", 190, "loop, keep leasing")}{ico("s", 190, "return arrow")}</div>'
              '<div class="kp-slider" style="--v:50%;margin:0 95px"><span class="fill"></span><span class="knob" style="width:120px;height:120px"></span></div>')
    res.append(("CTRL · slider with three stops", "darkblue", COPY(s[3]["title"], s[3]["sub"]) + STAGE(
        UI("position:absolute;left:0;right:3cqw;top:6cqh;bottom:8cqh;justify-content:space-evenly;padding:50px 52px", slider, "plate-p"))))
    col = (ph("cr", "left:0;top:6cqh;width:42cqw;height:84cqh;border-radius:32px;transform:rotate(-6deg);padding:30px;font-size:17px",
              "Portrait · real person, uplifted · plain solid Cream background · face uncropped")
           + UI("position:absolute;right:0;top:8cqh;width:34cqw;padding:30px 32px;gap:14px;transform:rotate(6deg)",
                '<div class="kp-bar db"></div><div class="kp-bar" style="width:60%"></div>', "plate-db")
           + UI("position:absolute;left:64%;top:58%;transform:translate(-50%,-50%);width:58cqw;padding:130px 40px;align-items:center", LOGO, "plate-db")  # never rotated: it carries the logo
           + A("left:28cqw;top:84cqh", ico("w", 150, "home"))
           + A("right:0;top:calc(58% + 110px)", ico("db", 140, "check")))
    res.append(("COL · logo at the center of the pieces", "pink", COPY(s[4]["title"], s[4]["sub"]) + STAGE(col)))
    out = []
    for i, (n, t, l) in enumerate(res):
        sid = f"p13-s{i+1}"
        if l is None:
            a = photo_card_slide(sid, t, s[2], "Photo · real person unboxing a new product at home, delighted · plain solid Light Blue background · face in the upper half, uncropped",
                                 "lb", icon=ico("s", 120, "key"), plate="plate-db")
        else:
            a = art(sid, t, l)
        out.append((sid, n, a))
    return out

def p14(p):
    s = p["slides"]; res = []
    tri = A("left:50%;top:0;height:min(100cqh,80cqw);aspect-ratio:1.16;transform:translateX(-50%)",
            '<div class="kp-tri" style="inset:12% 11% 8% 11%;--f:var(--k-light-blue)"></div>'
            + ph("pk", "left:50%;top:0;width:36%;aspect-ratio:1;border-radius:50%;transform:translateX(-50%);padding:18px;font-size:14px;outline-offset:-10px",
                 "Portrait · real shopper, smiling · Pink background · face centered, uncropped")
            + A("left:0;bottom:0", ico("db", 176, "storefront")) + A("right:0;bottom:0", ico("c", 176, "chip, technology")))
    res.append(("TRI · shoppers, retailers, technology", "light", LOGO + COPY(s[0]["title"], s[0]["sub"]) + STAGE(tri)))
    pc = "".join(cell("auto", cut(x) + (f'<span class="kp-dot corner" style="--d:54px">{CHECK}</span>' if i == 1 else ""), SF, "sel" if i == 1 else "", style="--cr:22px")
                 for i, x in enumerate(["TV", "sofa", "laptop", "tires"]))
    phone = (f'<div class="kp-phone" style="left:50%;width:min(60cqw,560px);top:3cqh;bottom:-60px;transform:translateX(-50%)"><div class="scr"><span class="notch"></span>'
             f'<div class="kp-grid" style="left:7%;right:7%;top:12%;bottom:12%;grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr;--gap:16px">{pc}</div></div></div>')
    res.append(("PICK · product picker in a phone", "pink", COPY(s[1]["title"], s[1]["sub"]) + STAGE(phone, "bl-b")))
    awn = A("left:4cqw;right:4cqw;top:2cqh;height:17cqh;display:flex",
            "".join(f'<i style="flex:1;background:{PK if i % 2 == 0 else W};border-radius:0 0 60px 60px"></i>' for i in range(6)))
    store = (SH("left:6cqw;right:6cqw;top:19cqh;bottom:0;--f:var(--k-blue)") + awn
             + ph("lb", "left:11cqw;width:52cqw;top:26cqh;bottom:10cqh;border-radius:24px;font-size:18px;padding:28px",
                  "Photo · real store associate helping a smiling customer · plain solid Light Blue background · faces uncropped")
             + SH("left:67cqw;right:11cqw;top:32cqh;bottom:0;--f:var(--k-cream);border-radius:26px 26px 0 0",
                  A("left:14%;top:50%;width:26px;height:26px;border-radius:50%;background:var(--k-dark-blue)")))
    res.append(("BLOCK · storefront built from color blocks", "darkblue", COPY(s[2]["title"], s[2]["sub"]) + STAGE(store, "bl-b bl-x")))
    def plate(x, y, f, t, lab, bar):
        return A(f"left:{x}cqw;top:{y}cqh;width:68cqw;height:32cqh;background:{f};border-radius:36px;display:flex;align-items:center;gap:30px;padding:0 40px",
                 ico(t, "min(130px,20cqh)", lab) + f'<div style="flex:1;display:flex;flex-direction:column;gap:18px"><i style="height:22px;border-radius:11px;background:{bar};width:70%"></i><i style="height:22px;border-radius:11px;background:{bar};width:45%"></i></div>')
    res.append(("STACK · exploded layers", "cream", COPY(s[3]["title"], s[3]["sub"]) + STAGE(
        plate(0, 64, DB, "db", "phone, in store", LB) + plate(16, 34, BL, "w", "storefront, online", W) + plate(32, 4, W, "s", "cloud, integrations", DB))))
    venn = ('<div class="kp-venn" style="--vd:min(60cqw,100cqh);--vw:calc(var(--vd) * 1.62)">'
            '<div class="c l">' + ph("pk", "inset:0;padding:0 44% 0 12%;font-size:17px", "Portrait · real shopper, smiling · plain solid Pink background · face in the left half of the circle, uncropped") + '</div>'
            '<div class="c r">' + ph("cr", "inset:0;padding:0 12% 0 44%;font-size:17px", "Portrait · real store associate · plain solid Cream background · face in the right half of the circle, uncropped")
            + '<div class="lens" style="--f:var(--k-dark-blue);left:calc(var(--vd) - var(--vw))"></div></div>'
            + A("left:50%;top:50%;transform:translate(-50%,-50%)", f'<span class="kp-dot" style="--d:88px">{CHECK}</span>') + '</div>')
    res.append(("VENN · two experiences, one overlap", "blue", COPY(s[4]["title"], s[4]["sub"]) + STAGE(venn)))
    return [(f"p14-s{i+1}", n, art(f"p14-s{i+1}", t, l)) for i, (n, t, l) in enumerate(res)]

def p15(p):
    s = p["slides"]; res = []
    chips = "".join('<i style="flex:1;height:64px;border-radius:999px;border:4px solid var(--k-grey-light)"></i>' for _ in range(3))
    card = UI("position:absolute;left:0;right:0;top:50%;transform:translateY(-50%);gap:26px",
              f'<div class="kp-row"><div class="kp-field kp-grow"><span class="kp-caret"></span></div><span class="kp-send">{SEND}</span></div>'
              f'<div class="kp-row" style="gap:16px">{chips}</div>', "plate-p")
    res.append(("IN · the question as an empty input", "darkblue", LOGO + COPY(s[0]["title"]) + STAGE(card) + COPY(sub=s[0]["sub"])))
    gap = {(2, 4), (2, 5), (3, 4), (3, 5)}
    g = "".join(cell(f"{r}/{c}", ico("w", "min(104px,19cqh)", "shopper"), "transparent") for r in range(1, 5) for c in range(1, 7) if (r, c) not in gap)
    g += cell("2/4/4/6", "", "transparent", style="box-shadow:inset 0 0 0 6px var(--k-pink)")
    res.append(("GRID · shoppers with a gap", "cream", COPY(s[1]["title"], s[1]["sub"]) + STAGE(
        f'<div class="kp-grid" style="inset:0;grid-template-columns:repeat(6,1fr);grid-template-rows:repeat(4,1fr);--gap:14px">{g}</div>')))
    blocks = [("3/1/5/3", DB, ("db", "home")), ("4/3/5/5", W, None), ("2/3/4/4", CR, ("c", "check")), ("2/4/4/6", BL, ("w", "key")),
              ("4/5/5/7", W, None), ("1/5/2/7", DB, None), ("2/6/4/7", CR, None)]
    b = "".join(cell(a, ico(i[0], "min(120px,20cqh)", i[1]) if i else "", f, style="--cr:22px") for a, f, i in blocks)
    res.append(("BLOCK · building blocks fill the gap", "pink", COPY(s[2]["title"], s[2]["sub"]) + STAGE(
        f'<div class="kp-grid" style="inset:0;grid-template-columns:repeat(6,1fr);grid-template-rows:repeat(4,1fr);--gap:14px">{b}</div>')))
    dec = UI("position:absolute;left:0;top:34cqh;width:40cqw;flex-direction:row;align-items:center;gap:22px;padding:26px 28px",
             ico("s", 96, "check") + '<div class="kp-grow" style="display:flex;flex-direction:column;gap:16px"><div class="kp-bar db"></div>'
             '<div class="kp-segs"><i class="on" style="height:26px"></i><i class="on" style="height:26px"></i><i class="on" style="height:26px"></i><i class="on" style="height:26px"></i></div></div>', "plate-p")
    res.append(("UI · device with floating chips", "light", COPY(s[3]["title"], s[3]["sub"]) + STAGE(
        ph("lb", "left:30cqw;width:40cqw;top:6cqh;bottom:0;border-radius:56px 56px 0 0;place-items:start center;padding:60px 36px",
           "Phone mockup · real Katapult app screen, client supplied · crop tight so it reads · bleeds off the bottom edge")
        + dec + A("right:1cqw;top:8cqh", ico("db", 150, "storefront")) + A("right:10cqw;top:54cqh", ico("c", 136, "cloud")), "bl-b")))
    opts = "".join(UI(f"flex:none;flex-direction:row;align-items:center;gap:22px;padding:22px 26px;border-radius:999px;{'' if sel else 'box-shadow:none'}",
                      f'<span class="kp-radio{" on" if sel else ""}"></span>' + ico("s", 100, lab) + '<span class="kp-grow"></span>', "plate-p")
                   for lab, sel in (("tag, purchase", False), ("loop, keep leasing", True), ("return arrow", False)))
    res.append(("CTRL + COL · portrait and three options", "blue", COPY(s[4]["title"], s[4]["sub"]) + STAGE(
        ph("lb", "left:0;width:44cqw;top:0;bottom:0;border-radius:36px", "Portrait · real person, uplifted · plain solid Light Blue background · face uncropped")
        + A("left:50cqw;right:0;top:0;bottom:0;display:flex;flex-direction:column;justify-content:center;gap:5cqh", opts))))
    return [(f"p15-s{i+1}", n, art(f"p15-s{i+1}", t, l)) for i, (n, t, l) in enumerate(res)]

# ---------------- singles ----------------
def s07(p):
    thumbs = [PK, LB, CR, DB, W]
    labs = ["sofa", "TV", "mattress", "tires", "refrigerator"]
    li = "".join(f'<li class="kp-opt"{SPAN if i == 4 else ""}><span class="kp-thumb" style="--f:{thumbs[i]}">{cut(labs[i])}</span>{EC(x)}</li>'
                 for i, x in enumerate(p["options"]))
    bg = (SH("right:-120px;top:-170px;width:500px;height:370px;--f:var(--k-pink);border-radius:64px;transform:rotate(8deg)")
          + SH("left:-130px;top:-110px;width:320px;height:320px;--f:var(--k-light-blue)", "", "o")
          + SH("right:-90px;bottom:-150px;width:420px;height:330px;--f:var(--k-dark-blue);border-radius:64px;transform:rotate(-6deg)"))
    card = UI("flex:none;gap:18px;padding:30px 30px 32px", SUB(p["question"]) + f'<ul class="kp-pick">{li}</ul>', "plate-p")
    lay = (COPY(p["headline"], p["sub"]) + card + SUB(p["cta"])
           + '<div class="kp-sticker-zone" role="img" aria-label="Empty zone reserved for the native sticker"><span>Native sticker zone · keep empty</span>'
             '<small>The sticker is added in the app at posting time.</small></div>')
    return [("p07-s1", "PICK + UI · picker card with cutout thumbs", art("p07-s1", "cream", lay, bg=bg, ratio="9x16", cls="kp-tpl-story-poll kp-tight"))]

def s09(p):
    fills = [(PK, "p", "calendar"), (CR, "c", "toggles"), (OR, "w", "shopping bag"), (W, "s", "key")]
    li = "".join(f'<li class="kp-tile" style="--f:{f}">{ico(t, 92, lab)}<span>{EC(x)}</span></li>' for (f, t, lab), x in zip(fills, p["options"]))
    bg = (SH("left:-130px;top:-110px;width:340px;height:340px;--f:var(--k-pink)", "", "o")
          + SH("right:-170px;bottom:-170px;width:620px;height:500px;--f:var(--k-blue);border-radius:80px;transform:rotate(-8deg)"))
    lay = (COPY(p["headline"], p["sub"]) + SUB(p["question"]) + f'<ul class="kp-tiles">{li}</ul>' + SUB(p["cta"])
           + '<div class="kp-sticker-zone" role="img" aria-label="Empty zone reserved for the native sticker"><span>Native sticker zone · keep empty</span>'
             '<small>The sticker is added in the app at posting time.</small></div>')
    return [("p09-s1", "GRID · 2x2 priority tiles", art("p09-s1", "darkblue", lay, bg=bg, ratio="9x16", cls="kp-tpl-story-poll"))]

def s08(p):
    card = UI("position:absolute;left:0;right:0;top:50%;transform:translateY(-50%);gap:24px;box-shadow:none;padding:46px 50px",
              SUB(p["prompt_label"]) + f'<p class="kp-prompt-line">{EC(p["prompt_line"])}</p>'
              f'<div class="kp-row"><div class="kp-field kp-grow"><span class="kp-caret"></span></div><span class="kp-send">{SEND}</span></div>')
    stage = ('<div class="kp-fan" style="--f:var(--k-dark-blue);left:5cqw;right:5cqw;top:5cqh;bottom:5cqh;transform:rotate(-5deg);transform-origin:50% 50%"></div>'
             '<div class="kp-fan" style="--f:var(--k-cream);left:3cqw;right:3cqw;top:7cqh;bottom:7cqh;transform:rotate(3.5deg);transform-origin:50% 50%"></div>' + card)
    lay = LOGO + COPY(p["headline"], p["sub"]) + STAGE(stage) + SUB(p["cta"])
    return [("p08-s1", "IN + STACK · input card on a stack", art("p08-s1", "pink", lay))]

def s10(p):
    card = UI("position:absolute;left:0;bottom:0;width:74cqw;gap:26px;padding:34px 40px 40px",
              f'<div class="kp-row"><span class="kp-thumb-lg">{cut("new product")}</span><div class="kp-grow" style="display:flex;flex-direction:column;gap:18px">'
              '<div class="kp-bar db" style="width:70%"></div><div class="kp-segs"><i class="on"></i><i class="on"></i><i></i><i></i><i></i><i></i></div></div></div>'
              + CTA(p["cta"]), "plate-p")
    lay = LOGO + COPY(p["headline"], p["sub"]) + STAGE(
        ph("lb", "left:14cqw;right:0;top:0;bottom:14cqh;border-radius:40px;place-items:start end;padding:50px 60px",
           "Photo · one real person, uplifted, with a new product in use · plain solid Light Blue background · face in the upper right, uncropped") + card)
    return [("p10-s1", "UI + CTRL · photo with a floating checkout card", art("p10-s1", "light", lay))]

def s11(p):
    labs = ["electronics", "furniture", "appliance", "mattress", "automotive"]
    g = ""
    for i, lab in enumerate(labs):
        dark = i % 2 == 1
        pin = A("left:14px;top:14px", ico("p", 70, "map pin")) if i == 0 else ""
        g += cell("auto", cut(lab, "color:var(--k-white);inset:12%" if dark else "inset:12%") + pin, DB if dark else W)
    g += cell("auto", ico("p", "min(120px,40cqh)", "plus, and more"), PK)
    lay = LOGO + COPY(p["headline"], p["sub"], extra=CTA(p["cta"])) + STAGE(
        f'<div class="kp-grid" style="inset:0;grid-template-columns:repeat(3,1fr);grid-template-rows:repeat(2,1fr);--gap:16px">{g}</div>')
    return [("p11-s1", "GRID · category tiles", art("p11-s1", "cream", lay))]

def s12(p):
    calc = UI("position:absolute;left:0;right:0;top:0;bottom:-40px;gap:22px;border-radius:40px 40px 0 0;padding:40px 44px",
              f'<div class="kp-field">{ico("s", 64, "price tag")}</div><div class="kp-field">{ico("s", 64, "map pin")}</div>'
              '<div class="kp-segs"><i style="height:70px"></i><i class="on" style="height:70px"></i><i style="height:70px"></i></div><div class="kp-btn"></div>', "plate-p")
    lay = LOGO + COPY(p["headline"], p["sub"], extra=CTA(p["cta"])) + STAGE(calc, "bl-b")
    return [("p12-s1", "IN + CTRL · price calculator card", art("p12-s1", "darkblue", lay))]

BUILDERS = {"01": p01, "02": p02, "03": p03, "04": p04, "05": p05, "06": p06, "07": s07, "08": s08, "09": s09,
            "10": s10, "11": s11, "12": s12, "13": p13, "14": p14, "15": p15}
META = [("01", "Educational"), ("02", "Educational"), ("03", "Educational"), ("04", "Inspirational"), ("05", "Inspirational"), ("06", "Inspirational"),
        ("07", "Engaging"), ("08", "Engaging"), ("09", "Engaging"), ("10", "Promotional"), ("11", "Promotional"), ("12", "Promotional"),
        ("13", "Brand storytelling"), ("14", "Brand storytelling"), ("15", "Brand storytelling")]
IDEA = {
 "01": "The explainer in five objects: collage, picker, approval card, progress bar, triangle of choices.",
 "02": "Two circles, two paths: the Venn's Blue and Pink circles each get a slide, Dark Blue where they meet.",
 "03": "The Katapult board game: the cover shows the board, each step carries the track and takes its tile's color.",
 "04": "Life's to-do list: surprises arrive as a checklist, real people show the fix.",
 "05": "Building the next chapter: prints, a floor plan, a week planner, tic-tac-toe, a step up.",
 "06": "One more card in the hand: each option card's color becomes a slide and a different choice control.",
 "07": "Product picker Story: every option has its own cutout thumb.",
 "08": "Fill-in UI card: the prompt line on a White input card, empty field, send button.",
 "09": "Priority tiles Story: four color-blocked tiles, each with its icon.",
 "10": "Photo with a floating checkout card carrying the CTA.",
 "11": "Category grid: five retail categories and one for everything else.",
 "12": "Price calculator UI: empty fields, pay-frequency control, estimate bar.",
 "13": "The full picture: the score shrinks to a small card, the person fills the frame.",
 "14": "The triangle: shoppers, retailers, technology each get a slide, then meet in a Venn.",
 "15": "An origin story in blocks: a typed question, a gap, blocks that fill it, options.",
}
COLOR_NAME = {"darkblue": "Dark Blue", "light": "Surface", "pink": "Pink", "cream": "Cream", "blue": "Blue", "orange": "Orange"}
COLOR_HEX = {"darkblue": "#131540", "light": "#EAEAE8", "pink": "#ED5370", "cream": "#D4A574", "blue": "#365488", "orange": "#E48027"}

blocks, rhythm, counts, total = [], [], {"Carousel": 0, "Static": 0, "Story": 0}, 0
for num, ctheme in META:
    p = posts[num]
    arts = BUILDERS[num](p)
    fmt = p["fmt"]
    kind = "Carousel" if fmt.startswith("Carousel") else ("Story" if "Story" in fmt else "Static")
    if kind == "Carousel":
        assert len(arts) == len(p["slides"]), (num, len(arts), len(p["slides"]))
    counts[kind] += 1; total += len(arts)
    themes = [re.search(r"kp-theme-(\w+)", a).group(1) for _, _, a in arts]
    figs = []
    for sid, name, a in arts:
        n = sid.split("-s")[1]
        fcls = "f-9x16" if "kp-r-9x16" in a else "f-4x5"
        figs.append(f'<figure class="q4-slide"><div class="kp-frame {fcls}">{a}</div>'
                    f'<figcaption><span class="mono">{sid}</span><span>{E(name)}</span>'
                    f'<button type="button" class="q4-view" data-view="{sid}">View slide {n} at 100%</button></figcaption></figure>')
    rhythm.append(f'<li><a href="#post-{num}"><i style="background:{COLOR_HEX[themes[0]]}"></i><span>{num}</span></a></li>')
    sw = "".join(f'<i title="{COLOR_NAME[t]}" style="background:{COLOR_HEX[t]}"></i>' for t in themes)
    fmt_label = "Carousel 4:5" if kind == "Carousel" else ("IG Story 9:16" if kind == "Story" else "Static 4:5")
    blocks.append(f'''<section class="q4-post" id="post-{num}" aria-labelledby="h-{num}">
  <div class="q4-post-head">
    <span class="q4-num">{num}</span>
    <h2 id="h-{num}">{E(p["title"])}</h2>
    <p class="q4-idea">{E(IDEA[num])}</p>
    <dl class="q4-meta"><div><dt>Theme</dt><dd>{ctheme}</dd></div><div><dt>Colors</dt><dd class="q4-sw">{sw}</dd></div><div><dt>Format</dt><dd>{fmt_label}</dd></div><div><dt>Slides</dt><dd>{len(arts)}</dd></div></dl>
  </div>
  <div class="q4-strip">{"".join(figs)}</div>
</section>''')
    if kind != "Carousel":
        pass
FIRST = [re.search(r"background:(#\w+)", r).group(1) for r in rhythm]
assert all(a != b for a, b in zip(FIRST, FIRST[1:])), "neighbouring posts open with the same color"
PAGE_CSS = r"""
/* ============ Q4 review page ============ */
.q4-wrap{max-width:1400px;margin-inline:auto;padding-inline:max(16px,var(--gutter))}
.q4-mast{background:var(--k-dark-blue);color:var(--k-white);position:relative;overflow:hidden}
.q4-mast .q4-wrap{position:relative;z-index:1;padding-block:40px 32px;display:flex;flex-direction:column;gap:14px}
.q4-mast h1{font-size:clamp(34px,5.5vw,56px);letter-spacing:-.015em;line-height:1}
.q4-mast h1 span{color:var(--k-pink)}
.q4-mast p{max-width:70ch;color:var(--k-grey-light);font-size:16px}
.q4-counts{display:flex;flex-wrap:wrap;gap:8px 12px;list-style:none;padding:0;margin:0}
.q4-counts li{font-size:14px;font-weight:500;color:var(--k-light-blue);border:1px solid rgba(158,181,192,.4);border-radius:999px;padding:3px 12px}
.q4-counts li b{color:var(--k-white);font-weight:700}
.q4-bar{position:sticky;top:env(safe-area-inset-top,0px);z-index:30;background:var(--bg);border-bottom:1px solid var(--rule)}
.q4-bar .q4-wrap{display:flex;flex-wrap:wrap;align-items:center;gap:10px 24px;padding-block:10px}
.q4-rhythm{list-style:none;margin:0;padding:0;display:flex;gap:4px;overflow-x:auto;max-width:100%;scrollbar-width:thin}
.q4-rhythm a{display:flex;flex-direction:column;align-items:center;gap:2px;text-decoration:none;font-size:11px;font-weight:700;color:var(--ink-2)}
.q4-rhythm i{display:block;width:22px;height:14px;border-radius:2px;outline:1px solid var(--rule)}
.q4-rhythm-label{font-size:12px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-2)}
.q4-post{padding-block:36px;border-bottom:1px solid var(--rule)}
.q4-post > *{max-width:1400px;margin-inline:auto;padding-inline:max(16px,var(--gutter))}
.q4-post-head{display:flex;flex-wrap:wrap;align-items:baseline;gap:8px 18px;margin-bottom:18px}
.q4-num{font-size:34px;font-weight:500;color:var(--accent);line-height:1;font-variant-numeric:tabular-nums}
.q4-post-head h2{font-size:clamp(21px,2.6vw,28px);letter-spacing:-.01em;flex:1 1 280px}
.q4-meta{display:flex;flex-wrap:wrap;gap:6px 20px;margin:0;width:100%}
.q4-meta div{display:flex;gap:6px;align-items:center;font-size:14px}
.q4-meta dt{font-size:11.5px;font-weight:700;letter-spacing:.07em;text-transform:uppercase;color:var(--ink-2)}
.q4-meta dd{margin:0;font-weight:500;display:inline-flex;align-items:center;gap:6px}
.q4-meta dd i{width:14px;height:14px;border-radius:2px;outline:1px solid var(--rule-strong);display:inline-block}
.q4-strip{display:flex;overflow-x:auto;padding-bottom:12px;scrollbar-width:thin}
.q4-slide{flex:none;display:flex;flex-direction:column;gap:8px;margin:0}
.q4-slide .kp-frame{--s:.3;outline:none;box-shadow:0 0 0 1px var(--rule)}
.q4-slide figcaption{display:flex;flex-direction:column;gap:2px;font-size:13px;padding:0 10px 0 2px;max-width:324px}
.q4-slide figcaption .mono{color:var(--ink-2);font-size:12px}
.q4-view{align-self:flex-start;margin-top:4px;font:inherit;font-size:13px;font-weight:700;color:var(--ink);background:var(--panel);border:1px solid var(--rule-strong);border-radius:999px;padding:4px 12px;cursor:pointer}
.q4-view:hover{border-color:var(--accent)}
.q4-toggle{display:inline-flex;align-items:center;gap:8px;font-size:14px;font-weight:500;cursor:pointer}
.q4-toggle input{width:18px;height:18px;accent-color:var(--k-pink)}
.q4-notes{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px 28px;font-size:14px;color:var(--k-grey-light)}
.q4-notes b{color:var(--k-white)}
.q4-viewer{position:fixed;inset:0;z-index:100;background:var(--bg);display:flex;flex-direction:column}
.q4-viewer-bar{display:flex;flex-wrap:wrap;align-items:center;gap:8px 12px;padding:calc(10px + env(safe-area-inset-top,0px)) 16px 10px;border-bottom:1px solid var(--rule);background:var(--panel)}
.q4-viewer-bar b{font-size:15px;margin-right:auto}
.q4-viewer-bar button{font:inherit;font-size:14px;font-weight:700;color:var(--ink);background:var(--bg);border:1px solid var(--rule-strong);border-radius:999px;padding:6px 14px;cursor:pointer}
.q4-viewer-stage{flex:1 1 auto;overflow:auto;padding:24px 16px calc(24px + env(safe-area-inset-bottom,0px))}
.q4-viewer-stage > .kp-post{margin-inline:auto;box-shadow:0 0 0 1px var(--rule)}

.q4-idea{flex:1 1 100%;margin:0;font-size:15.5px;color:var(--ink-2);max-width:90ch}
.q4-sw{display:inline-flex!important;gap:3px}
.q4-sw i{width:16px!important;height:16px!important}
"""

JS = r"""
(function(){
  var app=document.getElementById('q4-app');
  var t=document.getElementById('q4-safe');
  function applySafe(){ app.classList.toggle('show-safe', t.checked); }
  t.addEventListener('change', applySafe); applySafe();
  var ids=[].map.call(document.querySelectorAll('.q4-strip article.kp-post'),function(a){return a.id;});
  var v=document.getElementById('q4-viewer'), stage=document.getElementById('q4-stage'), lab=document.getElementById('q4-vlabel');
  var cur=-1, opener=null;
  function show(i){
    cur=(i+ids.length)%ids.length;
    var src=document.getElementById(ids[cur]);
    var c=src.cloneNode(true); c.removeAttribute('id'); c.setAttribute('data-src',ids[cur]);
    stage.replaceChildren(c); stage.scrollTop=0; stage.scrollLeft=0;
    var h=src.classList.contains('kp-r-9x16')?'1080 × 1920':'1080 × 1350';
    lab.textContent=ids[cur]+' · 100% · '+h;
  }
  function open(id,btn){ opener=btn||null; v.hidden=false; show(ids.indexOf(id)); document.getElementById('q4-vclose').focus(); }
  function close(){ v.hidden=true; stage.replaceChildren(); if(opener) opener.focus(); }
  document.addEventListener('click',function(e){
    var b=e.target.closest('[data-view]'); if(b){ open(b.getAttribute('data-view'),b); return; }
    var f=e.target.closest('.q4-strip .kp-frame'); if(f){ var a=f.querySelector('article'); if(a) open(a.id,null); }
  });
  document.getElementById('q4-vclose').addEventListener('click',close);
  document.getElementById('q4-vprev').addEventListener('click',function(){show(cur-1);});
  document.getElementById('q4-vnext').addEventListener('click',function(){show(cur+1);});
  document.addEventListener('keydown',function(e){
    if(v.hidden) return;
    if(e.key==='Escape') close();
    else if(e.key==='ArrowRight') show(cur+1);
    else if(e.key==='ArrowLeft') show(cur-1);
  });
})();
"""

carousel_slides = total - counts["Static"] - counts["Story"]
page = f"""<title>Katapult Q4 Organic</title>
<style>
{FONT_FACES}
{DS_CSS}
{PAGE_CSS}
</style>

{SYMBOLS}

<div id="q4-app">
<header class="q4-mast">
  <div class="q4-wrap">
    <span class="label" style="color:var(--k-light-blue)">Katapult · Facebook and Instagram organic · Q4 2026</span>
    <h1>Katapult Q4 <span>Organic</span></h1>
    <ul class="q4-counts">
      <li><b>15</b> posts</li>
      <li><b>{counts["Carousel"]}</b> carousels 4:5 · {carousel_slides} slides</li>
      <li><b>{counts["Static"]}</b> statics 4:5</li>
      <li><b>{counts["Story"]}</b> IG Stories 9:16</li>
      <li><b>{total}</b> canvases</li>
    </ul>
    <div class="q4-notes">
      <p><b>Copy</b> is the client's approved copy, placed exactly as written.</p>
      <p><b>Placeholders:</b> blocks with a dashed inner line are photos (filled with their planned background color), dashed rounded boxes are product cutouts, discs with a dashed ring are line icons. Every placeholder label goes when the real asset drops in.</p>
      <p><b>Logo</b> is the client's supplied artwork (logo-katapuklt.svg), never redrawn: Pink #EC5370 on the surface, on Dark Blue and on White cards; White on Pink and Blue; Dark Blue on Cream and Orange. Its x-height is kept clear on every side, and it never sits on a photo.</p>
      <p><b>v2, 2026-09-28:</b> no Bounce line graphics, and every slide has its own visual mechanic (art-direction-v2.md). Built on the Katapult social design system plus its v2 components. No disclaimer placed.</p>
    </div>
  </div>
</header>

<div class="q4-bar">
  <div class="q4-wrap">
    <label class="q4-toggle" for="q4-safe"><input type="checkbox" id="q4-safe"> Show safe zones</label>
    <span class="q4-rhythm-label">Feed rhythm</span>
    <ol class="q4-rhythm" aria-label="Post color rhythm in calendar order">{"".join(rhythm)}</ol>
  </div>
</div>

<main>
{chr(10).join(blocks)}
</main>

<div class="q4-viewer" id="q4-viewer" hidden role="dialog" aria-modal="true" aria-labelledby="q4-vlabel">
  <div class="q4-viewer-bar"><b id="q4-vlabel"></b><button type="button" id="q4-vprev">Previous</button><button type="button" id="q4-vnext">Next</button><button type="button" id="q4-vclose">Close</button></div>
  <div class="q4-viewer-stage" id="q4-stage"></div>
</div>
</div>

<script>{JS}</script>
"""
OUT.write_text(page, encoding="utf-8")
print("wrote", OUT, len(page.encode("utf-8")), "bytes;", total, "canvases", counts)
