"""Builder B: writes the HTML frames for posts 03, 06, 09, 10, 12, 13, 14 into build/frames/<post>/<name>.html.
Run: python b_build.py   then   python render.py frames/<post> <deliverables>/png/<post>
Copy on the art comes from ../copy.md, verbatim. <span class="a"> marks the [pink] word(s)."""
import pathlib
HERE = pathlib.Path(__file__).parent
FR = HERE / "frames"
IMG = "../../img/"

# ---------- helpers ----------
def page(ground, body, tall=False):
    cls = "frame r9x16" if tall else "frame"
    return ('<!doctype html><html><head><meta charset="utf-8">'
            '<link rel="stylesheet" href="../../kit.css"><link rel="stylesheet" href="../../b.css"></head>'
            f'<body><div class="{cls} {ground}">\n{body}\n</div></body></html>\n')

def logo(x, y, white=False):
    return f'<img class="b-logo{" w" if white else ""}" src="../../logo.svg" style="left:{x}px;top:{y}px">'

def hl(x, y, size, html, color=None, lh=1.0, extra=""):
    c = f"color:{color};" if color else ""
    return f'<div class="b-hl" style="left:{x}px;top:{y}px;font-size:{size}px;line-height:{lh};{c}{extra}">{html}</div>'

def body(x, y, html, size=36, color=None, bold=False, extra=""):
    c = f"color:{color};" if color else ""
    return f'<div class="b-body{" b-bold" if bold else ""}" style="left:{x}px;top:{y}px;font-size:{size}px;{c}{extra}">{html}</div>'

def plate(x, y, w, h, color, r=40, rot=0):
    t = f"transform:rotate({rot}deg);" if rot else ""
    return f'<div class="b-plate" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:{color};border-radius:{r}px;{t}"></div>'

def photo(x, y, w, h, src, pos="50% 50%", r=40, plate_color=None, off=20, zoom=1, origin=None):
    p = plate(x + off, y + off, w, h, plate_color, r) if plate_color else ""
    z = f"transform:scale({zoom});transform-origin:{origin or pos};" if zoom != 1 else ""
    return p + (f'<div class="b-photo" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;border-radius:{r}px">'
                f'<img src="{IMG}{src}" style="object-position:{pos};{z}"></div>')

def prod(src, x, y, w, rot=0, extra=""):
    t = f"transform:rotate({rot}deg);" if rot else ""
    return f'<img class="b-prod" src="{IMG}{src}" style="left:{x}px;top:{y}px;width:{w}px;{t}{extra}">'

def shape(x, y, w, h, color, r=40, rot=0, extra=""):
    t = f"transform:rotate({rot}deg);" if rot else ""
    return f'<div class="b-x" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:{color};border-radius:{r};{t}{extra}"></div>'

def accent(W, H, path, dots, sw=20, dot=21, color="var(--pink)"):
    """path: SVG path d of the solid line; dots: list of (cx, cy)."""
    ds = "".join(f'<circle cx="{x}" cy="{y}" r="{dot/2}"/>' for x, y in dots)
    return (f'<svg class="b-accent" width="{W}" height="{H}" viewBox="0 0 {W} {H}" style="color:{color}">'
            f'<path d="{path}" fill="none" stroke="currentColor" stroke-width="{sw}" stroke-linecap="butt" stroke-linejoin="round"/>'
            f'<g fill="currentColor">{ds}</g></svg>')

def dotrow(x0, y, n, pitch, step=1):
    return [(x0 + step * i * pitch, y) for i in range(n)]

def dotcol(x, y0, n, pitch, step=1):
    return [(x, y0 + step * i * pitch) for i in range(n)]

# line icons, 24 grid
ICONS = {
    "pin": '<path d="M12 21.5s-7-6.3-7-11.8a7 7 0 0 1 14 0c0 5.5-7 11.8-7 11.8z"/><circle cx="12" cy="9.6" r="2.6"/>',
    "cash": '<rect x="2.5" y="6" width="19" height="12" rx="2.2"/><circle cx="12" cy="12" r="2.8"/><path d="M6 9.5v0M18 14.5v0"/>',
    "card": '<rect x="2.5" y="5" width="19" height="14" rx="2.2"/><path d="M2.5 9.8h19M6.5 15h4"/>',
    "loop": '<path d="M19.5 11a7.5 7.5 0 0 0-13.4-4.2L4.5 8.6"/><path d="M4.5 4.2v4.4h4.4"/><path d="M4.5 13a7.5 7.5 0 0 0 13.4 4.2l1.6-1.8"/><path d="M19.5 19.8v-4.4h-4.4"/>',
    "gift": '<rect x="3.5" y="8.5" width="17" height="4" rx="1"/><path d="M5 12.5v8h14v-8M12 8.5v12"/><path d="M12 8.5C10 5 6.5 5 6.5 7.2S10 8.5 12 8.5zM12 8.5c2-3.5 5.5-3.5 5.5-1.3S14 8.5 12 8.5z"/>',
    "info": '<circle cx="12" cy="12" r="9.5"/><path d="M12 11v5.6"/><path d="M12 7.6v.1"/>',
}
def icon(name, size, color, sw=1.8):
    return (f'<svg class="b-ico" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" '
            f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</svg>')

STAR = '<path d="M12 2.6l2.85 5.95 6.55.85-4.8 4.55 1.2 6.5L12 17.3l-5.8 3.15 1.2-6.5-4.8-4.55 6.55-.85z"/>'
def stars(x, y, size, gap, color="var(--pink)"):
    s = "".join(f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" style="margin-right:{gap}px" fill="{color}" stroke="{color}" stroke-width="1.2" stroke-linejoin="round">{STAR}</svg>' for _ in range(5))
    return f'<div class="b-x" style="left:{x}px;top:{y}px;display:flex">{s}</div>'

def disc_letter(x, y, d, bg, letter, color="#fff", size=None):
    size = size or int(d * 0.56)
    return (f'<div class="b-disc" style="left:{x}px;top:{y}px;width:{d}px;height:{d}px;background:{bg}">'
            f'<span style="font-size:{size}px;font-weight:500;color:{color};line-height:1;transform:translateY(2px)">{letter}</span></div>')

def disc_icon(x, y, d, bg, name, color, isz=None, sw=1.8):
    isz = isz or int(d * 0.5)
    return (f'<div class="b-disc" style="left:{x}px;top:{y}px;width:{d}px;height:{d}px;background:{bg}">'
            f'{icon(name, isz, color, sw)}</div>')

def write(post, name, html):
    d = FR / post; d.mkdir(parents=True, exist_ok=True)
    (d / f"{name}.html").write_text(html, encoding="utf-8")

P, DB, LB, CR, OR, W = "var(--pink)", "var(--dblue)", "var(--lblue)", "var(--cream)", "var(--orange)", "var(--white)"
BL = "var(--b-blue)"

# ===== Round 3 (Lucas, 2026-10-16): spacing.md applied to every frame =====
# 4:5: logo top 80, logo to headline 40 (headline box at 176), headline to body 20, body to visual 56, visual to closing line 48,
# bottom margin 80. Story: logo at the 250 safe line, text 120 from the sides. Cutouts centred on their shape at 70 to 80%.
LOGO_Y, HL_Y = 80, 176

def shape_prod(x, y, w, h, color, radius, rot, src, css):
    """Flat shape with a product centred on it (optical centre); shape and product share one rotation."""
    return (f'<div class="b-x" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:{color};border-radius:{radius};'
            f'transform:rotate({rot}deg);display:flex;align-items:center;justify-content:center">'
            f'<img src="{IMG}{src}" style="display:block;{css}"></div>')

# ---------- 03 holiday wishlist · IG story ----------
# Poll Stories never draw the options. ZONE x 100..980, y 640..1400 (880 x 760) stays plain Cream, nothing in it.
# The five wishlist products sit on shapes along the bottom (one shared rotation), centred at about 75% of each shape.
ZONE03 = (100, 640, 880, 760)
def f03():
    rot = -6
    items = [(LB, "40px", "b-fridge.png", "height:186px"), (P, "50%", "b-couch-green.png", "width:186px"),
             (CR, "40px", "b-bed.png", "width:186px"), (DB, "50%", "b-headphones.png", "height:176px"),
             (OR, "40px", "b-tire-stack.png", "width:186px")]
    row = "".join(shape_prod(-24 + i * 218, 1450 + (24 if i % 2 else 0), 248, 248, c, r, rot, s, css)
                  for i, (c, r, s, css) in enumerate(items))
    b = "\n".join([
        accent(1080, 1920, "M392 600 H600", dotrow(32, 600, 7, 53.3)),
        logo(120, 250),
        hl(120, 346, 106, 'What&rsquo;s at the top<br>of your <span class="a">wishlist?</span>', lh=1.0),
        row,
    ])
    write("03-holiday-wishlist", "03-holiday-wishlist_ig-story-9x16", page("b-creaml", b, tall=True))

# ---------- 06 customer testimonial · IG story ----------
QUOTE_MARK = '<path d="M6 17h3l2-4V7H5v6h3zm8 0h3l2-4V7h-6v6h3z"/>'  # drawn shape, not a typed character
def f06():
    quote = ("This is an awesome pay as you go for something you want to purchase right now and you can pay off early "
             "or as you go with a little interest. But overall it helped me get new tires before winter arrives here on Colorado.")
    st = "".join(f'<svg width="76" height="76" viewBox="0 0 24 24" style="margin-right:14px" fill="var(--pink)" stroke="var(--pink)" stroke-width="1.2" stroke-linejoin="round">{STAR}</svg>' for _ in range(5))
    card = (f'<div class="b-card" style="left:120px;top:346px;width:840px;padding:64px 60px 150px;box-shadow:20px 20px 0 0 var(--pink)">'
            f'<div style="display:flex">{st}</div>'
            f'<div style="margin-top:40px;font-size:54px;line-height:1.26;color:var(--dblue);letter-spacing:-0.005em">{quote}</div>'
            f'<div style="margin-top:48px;font-size:46px;font-weight:700;color:var(--dblue)">Panson Williams</div></div>')
    qm = (f'<svg class="b-x" style="left:770px;top:262px;transform:rotate(180deg)" width="200" height="200" viewBox="0 0 24 24" '
          f'fill="var(--pink)">{QUOTE_MARK}</svg>')
    b = "\n".join([
        accent(1080, 1920, "M392 1600 H700", dotrow(32, 1600, 7, 53.3)),
        logo(120, 250),
        card,
        qm,
        shape(536, 1210, 520, 520, LB, "50%"),
        prod("b-tire.png", 586, 1260, 420, -8),
    ])
    write("06-customer-testimonial", "06-customer-testimonial_ig-story-9x16", page("g-dblue", b, tall=True))

# ---------- shared: gift tag (13), polaroid (12) ----------
CHECK = '<path d="M6 12.5l4 4 8-9" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>'
def check_disc(x, y, d=64, bg="var(--pink)"):
    return (f'<div class="b-disc" style="left:{x}px;top:{y}px;width:{d}px;height:{d}px;background:{bg}">'
            f'<svg width="{int(d*.62)}" height="{int(d*.62)}" viewBox="0 0 24 24">{CHECK}</svg></div>')

def gift_tag(x, y, w, rows, rot=-5, plate="var(--dblue)", hole="var(--dblue)", check=64):
    """White gift tag (clipped top corners, string hole at top centre) holding product tiles, products centred on their tiles.
    rows: [(tile_height, [(src, tile_bg, img_css), ...]), ...]; the first tile carries a Pink check disc."""
    pad, top, gap = 28, 88, 16
    inner, cy, h, first = w - 2 * pad, top, "", True
    for th, items in rows:
        n = len(items); tw = (inner - gap * (n - 1)) / n; cx = pad
        for src, bg, css in items:
            h += (f'<div class="b-x" style="left:{cx:.0f}px;top:{cy}px;width:{tw:.0f}px;height:{th}px;border-radius:22px;background:{bg};'
                  f'display:flex;align-items:center;justify-content:center"><img src="{IMG}{src}" style="display:block;{css}"></div>')
            if first:
                h += check_disc(cx + tw - check * .72, cy - check * .3, check)
                first = False
            cx += tw + gap
        cy += th + gap
    H = cy - gap + pad
    clip = f"clip-path:polygon(70px 0,{w-70}px 0,{w}px 70px,{w}px {H}px,0 {H}px,0 70px)"
    hole_html = f'<div class="b-x" style="left:{w/2-18:.0f}px;top:26px;width:36px;height:36px;border-radius:50%;background:{hole}"></div>'
    html = (f'<div class="b-x" style="left:{x}px;top:{y}px;width:{w}px;height:{H}px;transform:rotate({rot}deg);transform-origin:{w/2:.0f}px 44px">'
            f'<div class="b-x" style="left:18px;top:18px;width:{w}px;height:{H}px;background:{plate};border-radius:30px;{clip}"></div>'
            f'<div class="b-x" style="left:0;top:0;width:{w}px;height:{H}px;background:#fff;border-radius:30px;{clip}">{h}{hole_html}</div></div>')
    return html, x + w / 2, y + 44, H

def polaroid(x, y, w, h, src, pos="50% 50%", rot=0, zoom=1):
    z = f"transform:scale({zoom});transform-origin:{pos};" if zoom != 1 else ""
    return (f'<div class="b-x" style="left:{x}px;top:{y}px;padding:16px 16px 52px;background:#fff;border-radius:10px;transform:rotate({rot}deg)">'
            f'<div style="width:{w}px;height:{h}px;overflow:hidden;border-radius:4px">'
            f'<img src="{IMG}{src}" style="width:100%;height:100%;object-fit:cover;object-position:{pos};display:block;{z}"></div></div>')

# ---------- 09 Q and A · carousel 2 ----------
# Pair: disc at (80,176), headline at 358, card block 670..1270 with a 20px plate. Q on Surface, A on Dark Blue.
def f09():
    s1 = "\n".join([
        logo(80, LOGO_Y),
        disc_letter(80, HL_Y, 150, P, "Q"),
        hl(80, 358, 80, "Can I have more than one<br>lease with Katapult at<br>the same time?", lh=1.04, color="var(--dblue)"),
        photo(80, 670, 900, 580, "ai-phone-man-kitchen-thinking-01.jpg", "50% 30%", plate_color=DB),
    ])
    write("09-q-and-a", "09-q-and-a_carousel-4x5_01", page("g-surface", s1))
    s2 = "\n".join([
        disc_letter(80, HL_Y, 150, P, "A"),
        hl(80, 358, 64, '<span class="a">Yes!</span> Eligible customers may<br>qualify for additional approval<br>amounts to enter into another<br>lease agreement.', lh=1.08),
        plate(100, 690, 900, 580, P),
        f'<div class="b-card" style="left:80px;top:670px;width:900px;height:580px">'
        + disc_icon(56, 72, 164, P, "info", "var(--dblue)", 88, 1.9)
        + '<div class="b-x" style="left:56px;top:276px;white-space:nowrap;font-size:60px;line-height:1.24;color:var(--dblue)">'
          'Keep in mind that changes<br>to your existing lease may<br>affect your eligibility.</div></div>',
    ])
    write("09-q-and-a", "09-q-and-a_carousel-4x5_02", page("g-dblue", s2))

# ---------- 10 discover where you can shop · static ----------
# Round 4 (Lucas): calm top-down map on a strict grid. Map card (White streets, all 28px) with 2x3 flat blocks
# (Blue, Cream, one Light Blue park), one Pink route along the streets with its dots, five equal Pink pins, each
# inside its own block (never touching streets, route, card edge or text), product centred in the White head disc.
PIN = '<path d="M100 252C72 206 0 168 0 100a100 100 0 0 1 200 0c0 68-72 106-100 152z"/>'
def map_pin(cx, top, src, css, w=170):
    h = w * 252 / 200; d = w * 0.78
    return (f'<div class="b-x" style="left:{cx-w/2:.0f}px;top:{top:.0f}px;width:{w}px;height:{h:.0f}px">'
            f'<svg class="b-x" style="left:0;top:0" width="{w}" height="{h:.0f}" viewBox="0 0 200 252" fill="var(--pink)">{PIN}</svg>'
            f'<div class="b-disc" style="left:{(w-d)/2:.0f}px;top:{(w-d)/2:.0f}px;width:{d:.0f}px;height:{d:.0f}px;background:#fff">'
            f'<img src="{IMG}{src}" style="display:block;{css}"></div></div>')

def f10():
    X0, Y0, S, BW, BH = 80, 634, 28, (920 - 4 * 28) / 3, 276
    tones = {(0, 0): BL, (0, 1): CR, (0, 2): BL, (1, 0): LB, (1, 1): BL, (1, 2): CR}
    prods = {(0, 0): ("b-couch-green.png", "width:98px"), (0, 1): ("b-tv.png", "width:98px"), (0, 2): ("b-washer.png", "height:96px"),
             (1, 1): ("b-tire.png", "width:96px"), (1, 2): ("b-headphones.png", "height:96px")}
    blocks, pins = "", ""
    for (r, c), col in tones.items():
        bx, by = X0 + S + c * (BW + S), Y0 + S + r * (BH + S)
        blocks += shape(round(bx), by, round(BW), BH, col, "18px")
        if (r, c) in prods:
            src, css = prods[(r, c)]
            pins += map_pin(bx + BW / 2, by + (BH - 214) / 2, src, css)
    yh = Y0 + S + BH + S / 2                     # middle street centre
    xv2 = X0 + S + 2 * BW + S + S / 2            # second vertical street centre
    yt = Y0 + S / 2                              # top street centre
    route = accent(1080, 1350, f"M{X0+S+150:.0f} {yh:.0f} H{xv2-40:.0f} Q{xv2:.0f} {yh:.0f} {xv2:.0f} {yh-40:.0f} V{yt+40:.0f} "
                               f"Q{xv2:.0f} {yt:.0f} {xv2+40:.0f} {yt:.0f} H{X0+920-60:.0f}",
                   dotrow(X0 + 30, yh, 4, 36), sw=12, dot=14)
    b = "\n".join([
        logo(80, LOGO_Y, white=True),
        hl(80, HL_Y, 96, 'Your favorite stores<br>might be <span class="a">closer<br>than you think.</span>', lh=1.0, color="var(--dblue)"),
        body(80, 484, "Explore participating retailers and discover<br>where you can shop with Katapult.", color="var(--dblue)"),
        shape(X0, Y0, 920, 636, W, "40px"),
        blocks, route, pins,
    ])
    write("10-discover-where-you-can-shop", "10-discover-where-you-can-shop_static-4x5", page("g-pink", b))

# ---------- 12 thanksgiving · static ----------
# Light Cream, one large photo card + three tilted prints (four photo boxes); footnote 48 below the visual.
def f12():
    b = "\n".join([
        accent(1080, 1350, "M1032 346 V420 Q1032 470 982 470 H920", dotcol(1032, 40, 7, 47.5), sw=18, dot=19),
        logo(80, LOGO_Y),
        hl(80, HL_Y, 96, 'A little gratitude<br>goes a <span class="a">long way</span>', lh=1.0),
        body(80, 388, "Here&rsquo;s to the people and moments that<br>make this season special."),
        photo(80, 538, 600, 500, "ai-together-thanksgiving-table-01.jpg", "50% 34%", r=36, plate_color=P),
        polaroid(716, 536, 262, 210, "b-together-friends-cooking-07.jpg", "50% 35%", 5, 1.6),
        polaroid(722, 850, 262, 210, "b-together-family-homework-sofa-03.jpg", "60% 40%", -4, 1.3),
        polaroid(330, 930, 300, 190, "b-together-couple-tablet-mug-05.jpg", "68% 35%", 3, 1.25),
        body(80, 1223, "Happy Thanksgiving from Katapult", bold=True),
    ])
    write("12-thanksgiving", "12-thanksgiving_static-4x5", page("b-creaml", b))

# ---------- 13 black friday · carousel 4: one gift-guide system ----------
def _tag_slide(photo_src, pos, tag_rows, string_color, photo_plate, top, zoom=1, tag_y=830):
    tag, hx, hy, H = gift_tag(56, tag_y, 420, tag_rows, -5, DB, "var(--dblue)")
    return "\n".join([
        photo(80, top, 920, 1250 - top, photo_src, pos, plate_color=photo_plate, zoom=zoom),
        accent(1080, 1350, f"M190 {top-28} H{hx-40:.0f} Q{hx:.0f} {top-28} {hx:.0f} {top+12} V{hy:.0f}",
               dotrow(30, top - 28, 4, 47.5), sw=16, dot=17, color=string_color),
        tag])

def f13():
    # s1 cover: the gift tag is the hero, a 2x2 grid of the picks, hanging from the Pink line
    tag, hx, hy, H = gift_tag(220, 560, 640, [(296, [("b-tv.png", "var(--grey-xl)", "width:226px"), ("b-laptop-open.png", LB, "width:222px")]),
                                             (296, [("b-bed.png", CR, "width:226px"), ("b-headphones.png", "var(--grey-xl)", "height:210px")])],
                              -4, P, "var(--dblue)", 84)
    s1 = "\n".join([
        logo(80, LOGO_Y),
        hl(80, HL_Y, 104, 'Black Friday <span class="a">picks</span>', lh=1.0),
        hl(80, 300, 54, "for the one who&rsquo;s been building<br>their wishlist", lh=1.12),
        body(80, 441, "Ideas for home, tech, and everyday essentials.", size=34),
        accent(1080, 1350, f"M872 516 H{hx+40:.0f} Q{hx:.0f} 516 {hx:.0f} 556 V{hy:.0f}", dotrow(1052, 516, 4, 47.5, -1), sw=16, dot=17),
        tag,
    ])
    write("13-black-friday", "13-black-friday_carousel-4x5_01", page("g-dblue", s1))
    s2 = "\n".join([
        hl(80, LOGO_Y, 88, "for the one who loves<br>a good movie night", lh=1.02),
        body(80, 280, "Think couches, TVs, and everything you need<br>for a night in."),
        _tag_slide("ai-together-friends-movie-night-01.jpg", "50% 28%",
                   [(170, [("b-tv.png", "var(--grey-xl)", "width:240px")]),
                    (140, [("b-couch-green.png", LB, "width:140px"), ("b-headphones.png", CR, "height:104px")])],
                   "var(--dblue)", DB, 430),
    ])
    write("13-black-friday", "13-black-friday_carousel-4x5_02", page("g-pink", s2))
    s3 = "\n".join([
        hl(80, LOGO_Y, 88, "for the one who&rsquo;s<br>upgrading their tech", lh=1.02),
        body(80, 280, "From laptops to monitors, find your next<br>everyday essential."),
        _tag_slide("b-phone-man-call-tablet-sofa-06.jpg", "30% 40%",
                   [(170, [("b-laptop-open.png", LB, "width:230px")]),
                    (140, [("b-headphones.png", "var(--grey-xl)", "height:104px"), ("b-monitor.png", CR, "width:140px")])],
                   "var(--pink)", P, 430),
    ])
    write("13-black-friday", "13-black-friday_carousel-4x5_03", page("b-creaml", s3))
    s4 = "\n".join([
        logo(80, LOGO_Y, white=True),
        hl(80, HL_Y, 88, "for the one who loves<br>being home", lh=1.02),
        body(80, 376, "Think mattresses, bedroom furniture, and other<br>home essentials."),
        _tag_slide("b-at-home-woman-dishwasher-05.jpg", "80% 30%",
                   [(150, [("b-bed.png", CR, "width:250px")]),
                    (124, [("b-nightstand.png", LB, "height:96px")])],
                   "var(--pink)", P, 526, tag_y=868),
    ])
    write("13-black-friday", "13-black-friday_carousel-4x5_04", page("b-blueg", s4))

# flat illustrations for 14 s2 (palette only), viewBox 220x180
def _cal():
    out = ('<rect x="36" y="24" width="148" height="146" rx="16" fill="#fff" stroke="#131540" stroke-width="6"/>'
           '<path d="M36 40a16 16 0 0 1 16-16h116a16 16 0 0 1 16 16v20H36z" fill="#131540"/>'
           '<rect x="70" y="10" width="10" height="28" rx="5" fill="#ED5370"/><rect x="140" y="10" width="10" height="28" rx="5" fill="#ED5370"/>')
    for j in range(2):
        for i in range(3):
            done = j * 3 + i < 4
            out += f'<rect x="{56+i*40}" y="{76+j*44}" width="30" height="30" rx="7" fill="{"#ED5370" if done else "#F0F0F0"}"/>'
            if done:
                out += f'<path d="M{63+i*40} {91+j*44}l6 6 11-12" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>'
    return out

ILLO = {
    "cash": ('<rect x="34" y="34" width="170" height="98" rx="14" fill="#9EB5C0" transform="rotate(-8 119 83)"/>'
             '<rect x="18" y="56" width="170" height="98" rx="14" fill="#fff" stroke="#131540" stroke-width="6"/>'
             '<circle cx="103" cy="105" r="23" fill="none" stroke="#131540" stroke-width="6"/>'
             '<circle cx="46" cy="80" r="6" fill="#ED5370"/><circle cx="160" cy="130" r="6" fill="#ED5370"/>'),
    "card": ('<rect x="18" y="34" width="184" height="120" rx="16" fill="#131540"/>'
             '<rect x="40" y="64" width="40" height="30" rx="7" fill="#D4A574"/>'
             '<rect x="40" y="116" width="84" height="12" rx="6" fill="#9EB5C0"/>'
             '<circle cx="158" cy="122" r="14" fill="#ED5370"/><circle cx="178" cy="122" r="14" fill="#E48027"/>'),
    "loop": _cal(),
}

def option_pill(x, y, selected="loop", big=128, small=88, bg="#fff"):
    """One White element with the three payment options in a row: the selected one big and Pink, the others smaller in Dark Blue."""
    cells = ""
    for ic in ["cash", "card", "loop"]:
        if ic == selected:
            cells += (f'<div class="b-disc" style="position:relative;width:{big}px;height:{big}px;background:var(--pink)">'
                      f'{icon(ic, int(big*.56), "#fff", 1.9)}</div>')
        else:
            cells += (f'<div style="width:{small}px;height:{small}px;display:flex;align-items:center;justify-content:center">'
                      f'{icon(ic, small, "var(--dblue)", 1.7)}</div>')
    return (f'<div class="b-x" style="left:{x}px;top:{y}px;height:{big+40}px;padding:0 24px 0 40px;border-radius:{(big+40)//2}px;background:{bg};'
            f'display:flex;align-items:center;gap:36px">{cells}</div>')

# ---------- 14 more ways to shop · carousel 3 ----------
def f14():
    # s1 round 3: photo is the strong visual, full width from 56 below the body to the bottom edge; ONE White option pill on it
    s1 = "\n".join([
        logo(80, LOGO_Y),
        hl(80, HL_Y, 104, 'More ways to <span class="a">shop</span>', lh=1.0, color="var(--dblue)"),
        body(80, 300, "Because not every purchase looks the same", color="var(--dblue)"),
        f'<div class="b-x" style="left:0;top:403px;width:1080px;height:947px;overflow:hidden">'
        f'<img src="{IMG}b-together-couple-sofa-phone-laptop-01.jpg" style="width:100%;height:100%;object-fit:cover;object-position:60% 50%;transform:scale(1.3);transform-origin:62% 72%"></div>',
        option_pill(80, 1090),
    ])
    write("14-more-ways-to-shop", "14-more-ways-to-shop_carousel-4x5_01", page("g-surface", s1))
    # s2: Orange ground (Dark Blue text, accent White), three equal option cards filling the height
    cards = ""
    CT, CH, D = 489, 600, 168
    for i, (ic, pc) in enumerate([("cash", DB), ("card", P), ("loop", CR)]):
        x = 80 + i * (288 + 28)
        cards += plate(x + 16, CT + 16, 288, CH, pc, 36)
        cards += (f'<div class="b-card" style="left:{x}px;top:{CT}px;width:288px;height:{CH}px;border-radius:36px">'
                  f'<svg class="b-x" style="left:14px;top:150px" width="260" height="213" viewBox="0 0 220 180">{ILLO[ic]}</svg></div>')
        cards += (f'<div class="b-disc" style="left:{x + 144 - D//2 - 8}px;top:{CT + CH - D//2 - 30}px;width:{D + 16}px;height:{D + 16}px;'
                  f'background:var(--dblue);border:8px solid var(--orange)">{icon(ic, 92, "var(--pink)", 1.8)}</div>')
    s2 = "\n".join([
        accent(1080, 1350, "M372 1270 H490 Q540 1270 540 1220 V1160", dotrow(30, 1270, 7, 47.5), sw=18, dot=19, color="var(--dblue)"),
        hl(80, LOGO_Y, 100, 'It&rsquo;s not just about<br><span class="a">what you buy</span>', lh=1.0, color="var(--dblue)"),
        body(80, 300, "It&rsquo;s also about how you pay. Paying upfront, using credit,<br>and lease-to-own each come with different terms,<br>costs, and considerations.", size=34, color="var(--dblue)"),
        cards,
    ])
    write("14-more-ways-to-shop", "14-more-ways-to-shop_carousel-4x5_02", page("g-orange", s2))
    # s3 round 3: photo circle, one White option pill (segmented) overlapping its lower-left, aligned to the copy column
    s3 = "\n".join([
        logo(80, LOGO_Y, white=True),
        hl(80, HL_Y, 96, 'Find the option<br><span class="a">that fits</span>', lh=1.0),
        body(80, 388, "Consider the total cost, payment schedule, and ownership<br>terms before deciding what works for you.", size=34),
        body(80, 496, "Explore more ways with Katapult.", size=34, bold=True),
        f'<div class="b-x" style="left:260px;top:596px;width:900px;height:900px;border-radius:50%;overflow:hidden">'
        f'<img src="{IMG}ai-phone-man-city-shopping-01.jpg" style="width:100%;height:100%;object-fit:cover;object-position:50% 20%"></div>',
        option_pill(80, 1090),
    ])
    write("14-more-ways-to-shop", "14-more-ways-to-shop_carousel-4x5_03", page("g-pink", s3))

if __name__ == "__main__":
    for f in (f03, f06, f09, f10, f12, f13, f14):
        f()
    print("ok")
