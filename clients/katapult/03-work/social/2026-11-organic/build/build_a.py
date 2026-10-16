"""Builder A: writes the HTML frames for posts 01, 02, 04, 05, 08, 11 (Katapult November 2026 organic).
usage: python build_a.py   (then render.py on build/frames/<post>)
Copy comes from copy.md verbatim; class "k" marks the accent word(s).
Grounds follow feed-plan.md; no frame may reuse an October layout, mechanic or photo."""
import math
import pathlib

ROOT = pathlib.Path(__file__).parent
FR = ROOT / "frames"

# ---------- drawn vectors ----------
ICONS = {
    "arrow": '<path d="M8 32H54M38 16L54 32L38 48"/>',
    "calendar": '<rect x="8" y="12" width="48" height="44" rx="10"/><path d="M21 5V18M43 5V18M8 27H56"/>',
    "check": '<path d="M15 33L27 45L50 20"/>',
    "house": '<path d="M9 31L32 10L55 31"/><path d="M16 25V54H48V25"/><path d="M27 54V41H37V54"/>',
    "tag": '<path d="M34 8H54V28L30 52C28 54 25 54 23 52L10 39C8 37 8 34 10 32Z"/><circle cx="44" cy="18" r="3.5"/>',
    "key": '<circle cx="21" cy="43" r="11"/><path d="M29 35L53 11M45 19L51 25M39 25L44 30"/>',
    "bulb": '<path d="M25 48H39M27 56H37"/><path d="M32 8C21.5 8 14 15.6 14 25C14 31.5 17.5 35.3 20.5 38.3C22.5 40.3 23.5 42 23.5 44H40.5C40.5 42 41.5 40.3 43.5 38.3C46.5 35.3 50 31.5 50 25C50 15.6 42.5 8 32 8Z"/>',
    "bag": '<path d="M13 22H51L48 56H16Z"/><path d="M24 22V18C24 12.5 27.6 9 32 9C36.4 9 40 12.5 40 18V22"/>',
    "unlock": '<rect x="12" y="28" width="40" height="28" rx="7"/><path d="M22 28V19C22 13 26.5 9 32 9C36 9 39.5 11.5 41 15"/><path d="M32 39V45"/>',
}

def icon(name, size, color, sw=5.5):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 64 64" fill="none" stroke="{color}" '
            f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</svg>')

def cal(n, size, color):
    """Calendar with n filled marks in its first row: 4 = weekly, 2 = every other week, 1 = monthly (no words)."""
    xs = {4: [15, 25, 35, 45], 2: [15, 35], 1: [15]}[n]
    marks = "".join(f'<rect x="{x}" y="34" width="7" height="7" rx="1.5" fill="{color}" stroke="none"/>' for x in xs)
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 64 64" fill="none" stroke="{color}" stroke-width="5" '
            f'stroke-linecap="round" stroke-linejoin="round">{ICONS["calendar"]}{marks}</svg>')

def dots(x0, y0, dx, dy, n, r=10.5, color="#ED5370"):
    return "".join(f'<circle cx="{x0+i*dx:.1f}" cy="{y0+i*dy:.1f}" r="{r}" fill="{color}"/>' for i in range(n))

def accent(path_d, dot_svg, sw=21, color="#ED5370"):
    """Line accent: a thick line that turns a rounded corner, then a row of dots."""
    return (f'<svg class="acc" viewBox="0 0 1080 1350"><path d="{path_d}" fill="none" stroke="{color}" '
            f'stroke-width="{sw}"/>{dot_svg}</svg>')

LOGO = (ROOT / "logo.svg").read_text(encoding="utf-8")
LOGO = LOGO[LOGO.index("<svg"):].replace('fill="#EC5370"', 'fill="currentColor"').replace('width="521" height="116"', 'width="250" height="55.66"', 1)

def logo(cls="", style=""):
    """Supplied logo artwork, inlined so it can be Pink (default), White or Dark Blue via currentColor."""
    st = f' style="{style}"' if style else ""
    return f'<span class="lg {cls}"{st}>{LOGO}</span>'

def page(post, name, ground, body, extra_css=""):
    html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>{name}</title>
<link rel="stylesheet" href="../../kit.css"><link rel="stylesheet" href="../../a.css">
<style>{extra_css}</style></head>
<body><div class="frame {ground}">
{body}
</div></body></html>
"""
    d = FR / post
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{name}.html").write_text(html, encoding="utf-8")

def photo(src, left, top, w, h, pos="50% 50%", radius="36px", extra=""):
    return (f'<div class="ph" style="left:{left}px;top:{top}px;width:{w}px;height:{h}px;border-radius:{radius};{extra}">'
            f'<img src="../../img/{src}" style="object-position:{pos}"></div>')

# =====================================================================
# Spacing follows spacing.md: logo top 80, logo->headline 40 (headline top 176 under a logo, 80 without),
# headline->body 20, body->visual 56, card padding 40/44, list gap 28, bottom margin 80.
# =====================================================================

# =====================================================================
# 01 How Katapult works : static, light Cream, family D
# step cards in one column (numbers on one axis, 28 gaps) overlapping a person photo that bleeds off the right edge
# =====================================================================
def p01():
    steps = [("1", "APPLY", "Apply in seconds without affecting your credit score."),
             ("2", "SHOP THE APP", "Explore hundreds of your favorite stores using the Katapult App."),
             ("3", "CHECK OUT", "Select Katapult at checkout to start your lease-to-own journey.")]
    cards = "".join(f'<div class="stepcard"><div class="num">{n}</div><div class="lab">{lab}</div><div class="tx">{tx}</div></div>'
                    for n, lab, tx in steps)
    body = f"""
{photo("phone-woman-kitchen-phone-12.jpg", 600, 324, 480, 826, "47% 35%", "36px 0 0 36px")}
{logo("dblue at-tl")}
<div class="h c-dblue" style="position:absolute;left:80px;top:176px;width:920px">How Katapult <span class="k">works</span></div>
<div class="col" style="top:324px;width:580px;gap:28px">{cards}</div>
<div class="c-dblue" style="position:absolute;left:80px;bottom:80px;font-weight:700;font-size:48px;line-height:1.1;letter-spacing:-0.01em">Ready to get started?</div>
"""
    page("01-how-katapult-works", "01-how-katapult-works_static-4x5", "g-lcream", body)

# =====================================================================
# 02 Why choose lease-to-own : carousel 5
# =====================================================================
def p02():
    post = "02-why-choose-lease-to-own"
    n = lambda i: f"{post}_carousel-4x5_0{i}"

    # s1 cover, Pink, family C: type-led headline + a fan of three product cards turning round one pivot;
    # the Dark Blue dotted line leads from the sentence into the fan
    def fan(rot, bg, img, istyle):
        return (f'<div style="position:absolute;left:375px;top:660px;width:330px;height:430px;border-radius:36px;background:{bg};'
                f'transform:rotate({rot}deg);transform-origin:165px 820px;display:flex;align-items:center;justify-content:center">'
                f'<img src="../../img/{img}" style="display:block;{istyle}"></div>')
    body = f"""
{logo("dblue at-tl")}
<div class="h c-dblue on-pink" style="position:absolute;left:80px;top:176px;width:940px;font-size:136px;line-height:1.0;letter-spacing:-0.02em;white-space:nowrap">Why choose<br><span class="k">lease-to-own?</span></div>
<div class="c-dblue" style="position:absolute;left:80px;top:468px;display:flex;align-items:center;gap:22px">
  <span class="b l" style="font-size:44px;line-height:56px">Here's why it's worth considering</span>{icon("arrow", 62, "#131540", 6)}</div>
{accent("M486 590H640C700 590 740 630 740 690V900", dots(80, 590, 46, 0, 9, color="#131540"), color="#131540")}
{fan(-22, "var(--cream)", "couch.webp", "width:250px")}
{fan(22, "var(--dblue)", "headphones-trim.webp", "width:200px")}
{fan(0, "var(--white)", "fridge.webp", "height:330px")}
"""
    page(post, n(1), "g-pink on-pink", body)

    # s2 flexibility, Dark Blue, family D: photo card + one White card with one control:
    # three schedule tiles, the selected one large and Pink, the two others small and grey (no words)
    def tile(size, on):
        bg = "#ED5370" if on else "#F0F0F0"
        ic = icon("calendar", int(size * 0.5), "#FFFFFF" if on else "#131540", 5)
        chk = (f'<div class="disc db" style="right:-14px;top:-14px;width:64px;height:64px;border:5px solid #fff">{icon("check", 34, "#FFFFFF", 7)}</div>' if on else "")
        return (f'<div style="position:relative;width:{size}px;height:{size}px;border-radius:{size//5}px;background:{bg};'
                f'display:flex;align-items:center;justify-content:center;flex:none">{ic}{chk}</div>')
    body = f"""
<div class="pad">
  <div class="h c-white" style="width:900px">More <span class="k">flexibility</span> with your payments</div>
  <div class="b c-white hb" style="width:900px">Spread the cost of eligible purchases across scheduled lease payments instead of paying the full retail price upfront.</div>
</div>
{photo("ai-laptop-woman-sofa-phone-01.jpg", 400, 479, 600, 791, "50% 30%")}
<div class="card plate-pk" style="left:80px;top:760px;padding:40px 44px;display:flex;align-items:center;gap:28px">
  {tile(110, False)}{tile(210, True)}{tile(110, False)}
</div>
{accent("M-20 580H170C230 580 260 610 260 670V690", dots(260, 734, 0, 0, 1))}
"""
    page(post, n(2), "g-dblue", body)

    # s3 possibilities, Surface, family E: products on two Dark Blue shelf bands that bleed off both edges;
    # products whole inside the margins, a Pink tag disc marks one item
    def item(f, x, base, w=None, h=None):
        size = f"width:{w}px" if w else f"height:{h}px"
        return f'<img src="../../img/{f}" style="position:absolute;left:{x}px;bottom:{1350-base}px;{size};display:block">'
    body = f"""
<div class="pad">
  <div class="h c-black" style="width:920px">More <span class="k">possibilities</span> for your shopping list</div>
  <div class="b c-black hb" style="width:920px">Explore a variety of eligible products across participating retailers, from home essentials to electronics.</div>
</div>
{item("tv.webp", 80, 726, w=400)}
{item("laptop-open.webp", 508, 726, w=270)}
{item("headphones-trim.webp", 806, 726, h=220)}
<div style="position:absolute;left:-20px;right:-20px;top:726px;height:26px;border-radius:13px;background:var(--dblue)"></div>
{item("fridge.webp", 80, 1244, h=440)}
{item("washer.webp", 384, 1244, h=300)}
{item("couch.webp", 612, 1244, w=388)}
<div style="position:absolute;left:-20px;right:-20px;top:1244px;height:26px;border-radius:13px;background:var(--dblue)"></div>
<div class="disc pk" style="left:300px;top:790px;width:104px;height:104px">{icon("tag", 54, "#FFFFFF", 5.5)}</div>
"""
    page(post, n(3), "g-surface", body)

    # s4 ownership, light Cream (accent word Blue, never Pink text on Cream): full-width photo arch bleeding off the bottom,
    # one primary Pink key disc on the arch edge
    body = f"""
<div class="pad">
  <div class="h c-dblue" style="width:920px">A path to <span class="k">ownership</span></div>
  <div class="b c-dblue hb" style="width:900px">Complete your lease payments or explore an available early purchase option to make the item yours.</div>
</div>
{photo("unboxing-woman-unboxing-sofa-02.jpg", 80, 342, 920, 1100, "56% 20%", "460px 460px 0 0")}
<div class="disc pk" style="left:80px;top:760px;width:190px;height:190px;border:10px solid var(--lcream)">{icon("key", 98, "#FFFFFF", 5.5)}</div>
"""
    page(post, n(4), "g-lcream", body)

    # s5 closing, Blue: large round photo with one Pink check disc on its rim, centred headline and text, White logo at the foot
    body = f"""
{photo("ai-together-couple-living-room-01.jpg", 180, 80, 720, 720, "50% 35%", "50%")}
<div class="disc pk" style="left:150px;top:590px;width:160px;height:160px;border:10px solid var(--blue2)">{icon("check", 84, "#FFFFFF", 6.5)}</div>
<div style="position:absolute;left:80px;top:856px;width:920px;text-align:center">
  <div class="h c-white">Find what <span class="k">works</span><br>for you</div>
  <div class="b c-white hb">Explore your lease-to-own options with Katapult.</div></div>
{logo("white at-foot")}
"""
    page(post, n(5), "g-blue2", body)

# =====================================================================
# 04 Pay over time : carousel 4, chat bubbles on real photos
# =====================================================================
def p04():
    post = "04-pay-over-time"
    n = lambda i: f"{post}_carousel-4x5_0{i}"

    # s1 cover: Blue, White logo, photo card, two bubbles as a thread, text card overlapping the photo's lower edge
    body = f"""
{logo("white at-tl")}
{photo("phone-woman-card-phone-05.jpg", 80, 176, 920, 980, "30% 30%")}
<div class="bub w tl" style="left:130px;top:770px">Get What You Want</div>
<div class="bub p tr" style="right:130px;top:928px">Pay Over Time</div>
<div class="card plate-pk" style="left:80px;top:1116px;padding:40px 44px">
  <div class="b" style="font-size:40px;line-height:52px">A different way to bring home what you need.</div></div>
"""
    page(post, n(1), "g-blue2", body)

    # s2: full-bleed photo (family A), Pink bubble on the open wall, White card for the text
    body = f"""
<div class="ph" style="inset:0"><img src="../../img/ai-phone-woman-new-headphones-01.jpg" style="object-position:50% 30%"></div>
<div class="bub p tr" style="right:110px;top:880px">Enjoy it now.</div>
<div class="card plate-db" style="left:80px;bottom:96px;padding:40px 44px">
  <div class="b l" style="font-size:44px;line-height:56px">Make scheduled lease<br>payments over time.</div>
</div>
"""
    page(post, n(2), "g-dblue", body)

    # s3: Surface, full-width photo card, Dark Blue bubble, text card overlapping the photo's lower edge
    body = f"""
{photo("laptop-woman-blanket-laptop-03.jpg", 80, 80, 920, 1060, "50% 6%")}
<div class="bub d tl" style="left:110px;top:140px">Want to own it sooner?</div>
<div class="card plate-db" style="left:80px;top:1078px;padding:40px 44px">
  <div class="b l" style="font-size:42px;line-height:54px">Explore early purchase options that<br>may help reduce your total lease cost.</div></div>
"""
    page(post, n(3), "g-surface", body)

    # s4 closing: Orange (Dark Blue text), photo card, White bubble lower right, text card overlapping the photo, logo at the foot
    body = f"""
{photo("laptop-woman-desk-laptop-02.jpg", 80, 80, 920, 940, "62% 40%")}
<div class="bub w tr" style="right:110px;top:660px;white-space:normal">Your purchase.<br>Your plan.</div>
<div class="card plate-db" style="left:80px;top:960px;padding:40px 44px">
  <div class="b" style="font-size:40px;line-height:52px">Review your lease terms and<br>explore your options with Katapult.</div></div>
{logo("dblue at-foot")}
"""
    page(post, n(4), "g-orange", body)

# =====================================================================
# 05 POV : static, family B: Orange top band (Dark Blue type, accent phrase on White highlight bars),
# kitchen photo below, a scalloped sticker seal overlapping the band edge and the photo's top right corner
# =====================================================================
def seal(cx, cy, r, bumps, depth):
    pts = []
    for i in range(720):
        a = 2 * math.pi * i / 720
        rr = r + depth * math.cos(bumps * a)
        pts.append(f"{cx + rr * math.cos(a):.1f},{cy + rr * math.sin(a):.1f}")
    return "M" + " L".join(pts) + " Z"

def p05():
    body = f"""
<div class="ph" style="left:0;top:540px;width:1080px;height:810px">
  <img src="../../img/together-senior-couple-kitchen-06.jpg" style="position:absolute;left:-540px;top:-70px;width:1620px;height:auto;object-fit:fill"></div>
<div style="position:absolute;left:0;top:0;width:1080px;height:540px;background:var(--orange)"></div>
{logo("dblue at-tl")}
<div class="h c-dblue" style="position:absolute;left:80px;top:176px;width:920px;line-height:1.1">POV: you finally got<br>the fridge you've<br>been eyeing</div>
<div class="card" style="left:420px;top:462px;width:520px;padding:44px 52px 52px;border-radius:28px;
     box-shadow:10px 10px 0 0 var(--dblue);transform:rotate(-4deg);transform-origin:50% 50%">
  <div style="width:44px;height:6px;border-radius:3px;background:var(--pink);margin-bottom:22px"></div>
  <div style="font-weight:500;font-size:40px;line-height:1.15;letter-spacing:0.04em;color:var(--dblue)">AND GROCERY DAY<br>HIT DIFFERENT</div>
</div>
"""
    page("05-pov", "05-pov_static-4x5", "g-orange", body)

# =====================================================================
# 08 More ways to buy : static, Dark Blue, family F:
# three White speech-bubble chips (Pink icon disc each) stepping diagonally into one large Pink circle
# =====================================================================
def p08():
    chips = [(80, 176, "unlock", "More Access"), (200, 356, "calendar", "More Flexibility"), (300, 536, "bag", "More Possibility")]
    html = ""
    for x, y, ic, txt in chips:
        html += (f'<div class="bub w tl" style="left:{x}px;top:{y}px;display:flex;align-items:center;gap:22px;'
                 f'padding:24px 48px 24px 24px;font-size:58px">'
                 f'<span class="disc pk" style="position:relative;width:104px;height:104px;flex:none">{icon(ic, 58, "#FFFFFF", 5.5)}</span>{txt}</div>')
    body = f"""
{accent("M-20 820H120C180 820 210 850 210 910V950C210 1010 240 1040 300 1040H330", dots(376, 1040, 46, 0, 4))}
{logo("at-tl")}
<div class="ball" style="left:540px;top:640px;width:460px;height:460px;background:var(--pink);color:#fff;font-size:76px">
  <span style="display:block;padding-bottom:6px">More Ways<br>to Buy</span></div>
{html}
<div class="b c-white" style="position:absolute;left:80px;bottom:80px;width:920px">Connecting shoppers, retailers, and technology to create a more flexible path.</div>
"""
    page("08-more-ways-to-buy", "08-more-ways-to-buy_static-4x5", "g-dblue", body)

# =====================================================================
# 11 Did you know : static, Blue, family C (type-led) + White note card
# =====================================================================
def p11():
    body = f"""
{accent("M1100 900H1010C950 900 920 930 920 990V1180C920 1230 890 1250 840 1250H500", dots(454, 1250, -46, 0, 9))}
{logo("white at-tl")}
<div class="h c-white" style="position:absolute;left:80px;top:176px;width:760px;font-size:196px;line-height:0.98;letter-spacing:-0.02em">Did you<br><span class="k">know?</span></div>
<div class="disc pk" style="left:830px;top:176px;width:170px;height:170px">{icon("bulb", 100, "#FFFFFF", 4.6)}</div>
<div class="sub c-white" style="position:absolute;left:80px;top:604px;width:900px">A lower monthly payment doesn't always mean a better deal.</div>
<div class="card plate-pk" style="left:80px;top:776px;width:904px;padding:40px 44px">
  <div class="b" style="font-size:42px;line-height:1.3">When comparing payment options, look beyond the amount due each month. The total cost, payment schedule, and terms all matter when deciding what works for your budget.</div>
</div>
"""
    page("11-did-you-know", "11-did-you-know_static-4x5", "g-blue2", body)

if __name__ == "__main__":
    for f in (p01, p02, p04, p05, p08, p11):
        f()
    print("built")
