"""Build the Roku Design System review page.

    python build_ds.py <out.html>

Publish the output to the Roku Design System artifact (URL in clients/roku/README.md).
Rebuild from this script; never hand-edit the published HTML.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from rk_common import (ACCENT, CORE, HUB_URL, NEUTRAL, SCENE, BRAND, font_face, img_data,
                       lockup, wordmark)

INBOX = BRAND.parent / "00-inbox" / "2026-10-12-rku26013-previous-work"
DECK = BRAND.parent / "00-inbox" / "2026-10-12-rku26013-concept-deck"
JOB = BRAND.parent / "03-work" / "ads" / "2026-rku26013-sell-it-on-roku"


def lum(hexc):
    h = hexc.lstrip("#")
    out = []
    for i in (0, 2, 4):
        c = int(h[i:i + 2], 16) / 255
        out.append(c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4)
    return 0.2126 * out[0] + 0.7152 * out[1] + 0.0722 * out[2]


def ratio(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def chip(name, hexc, sub="", note=""):
    dark = lum(hexc) < 0.35
    return (f'<div class="sw{" sw-d" if dark else ""}" style="--c:{hexc}">'
            f'<div class="sw-c"></div><div class="sw-t"><b>{name}</b><span class="mono">{hexc}</span>'
            + (f'<span>{sub}</span>' if sub else "") + (f'<em>{note}</em>' if note else "") + '</div></div>')


def pair(fg, bg, fgn, bgn, use):
    r = ratio(fg, bg)
    grade = "AA" if r >= 4.5 else ("AA large" if r >= 3 else "Fails")
    cls = "ok" if r >= 4.5 else ("lg" if r >= 3 else "no")
    return (f'<div class="pr"><div class="pr-s" style="background:{bg};color:{fg}">Aa</div>'
            f'<div><b>{fgn} on {bgn}</b><span>{use}</span></div>'
            f'<span class="tag t-{cls}">{r:.1f}:1 · {grade}</span></div>')


def safe_box(w, h, label, t, r, b, l, note):
    """Format diagram drawn to scale: canvas + safe area (all values in px of the real canvas)."""
    sc = 220 / max(w, h) * (1.0 if h >= w else 1.25)
    W, H = w * sc, h * sc
    return (f'<figure class="fmt"><svg viewBox="0 0 {W:.0f} {H:.0f}" width="{W:.0f}" height="{H:.0f}" role="img" aria-label="{label} safe area">'
            f'<rect width="{W:.0f}" height="{H:.0f}" fill="var(--wall)"/>'
            f'<rect x="{l * sc:.1f}" y="{t * sc:.1f}" width="{(w - l - r) * sc:.1f}" height="{(h - t - b) * sc:.1f}" fill="none" stroke="var(--electric)" stroke-width="1.5" stroke-dasharray="4 3"/>'
            + (f'<rect width="{W:.0f}" height="{t * sc:.1f}" fill="var(--electric)" opacity=".14"/>' if t > 60 else "")
            + (f'<rect y="{(h - b) * sc:.1f}" width="{W:.0f}" height="{b * sc:.1f}" fill="var(--electric)" opacity=".14"/>' if b > 60 else "")
            + f'</svg><figcaption><b>{label}</b><span class="mono">{w} × {h}</span><span>{note}</span></figcaption></figure>')


HEADLINES = [
    ("Pet Supplies", "pet brand", "Put your pet brand in their living room.", ""),
    ("Beauty", "beauty brand", "Put your beauty brand in their living room.", ""),
    ("Food & Bev", "products", "Put your products in their living room.", ""),
    ("Wellness", "wellness brand", "Put your wellness brand in their living room.", ""),
    ("Fashion", "latest tech", "Put your latest tech in their living room.", "Brief pairs Fashion with a tech line. Confirm the industry or the copy."),
    ("Homegoods", "home brand", "Put your home brand in their living room.", ""),
]


def build():
    frame = img_data(JOB / "img" / "pet-1x1-review.jpg")
    ref1, ref2 = img_data(DECK / "deck-ref-1-review.jpg"), img_data(DECK / "deck-ref-2-review.jpg")

    core = "".join(chip(n, h, f"{rgb} · {pms}") for n, h, rgb, pms in CORE)
    core += chip("Deep Purple", "#2A0A6B", "Print only · Pantone Violet C", "No digital value in the guideline. Shown as an approximation.")
    acc = "".join(chip(n, h, f"{rgb} · {pms}") for n, h, rgb, pms in ACCENT)
    neu = "".join(chip(n, h) for n, h in NEUTRAL)
    scn = "".join(chip(n, h, use) for n, h, use in SCENE)

    pairs = "".join([
        pair("#14082B", "#E2DACD", "Ink", "the room's wall", "Headline above the windows"),
        pair("#4F01A3", "#E2DACD", "Primary Purple", "the room's wall", "The swapped industry word"),
        pair("#EC4AF0", "#E2DACD", "Pink", "the room's wall", "RKU26008's highlight color: too weak here"),
        pair("#FFFFFF", "#20004C", "White", "Midnight Purple", "Copy on the TV screen"),
        pair("#FFFFFF", "#4F01A3", "White", "Primary Purple", "Copy on brand purple"),
        pair("#FFFFFF", "#853DFF", "White", "Electric Purple", "Small copy on Electric: avoid"),
    ])

    rows = "".join(
        f'<tr{" class=flag" if note else ""}><td>{ind}</td><td class="hl">{full.replace(word, f"<mark>{word}</mark>")}</td>'
        f'<td>{note or "As briefed"}</td></tr>' for ind, word, full, note in HEADLINES)

    fmts = "".join([
        safe_box(1440, 1440, "Meta 1:1", 72, 72, 72, 72, "Feed. 72px working margin (5%), no platform band."),
        safe_box(1440, 1800, "Meta 4:5", 90, 72, 90, 72, "Feed. 72 / 90px working margin (5%)."),
        safe_box(1440, 2560, "Meta 9:16", 267, 72, 333, 72, "Stories and Reels. Nothing in the top 267px or bottom 333px."),
        safe_box(1920, 1080, "YouTube / CTV 16:9", 54, 96, 54, 96, "Title safe 90%: 96px sides, 54px top and bottom."),
    ])

    return f"""<title>Roku Design System</title>
<style>
{font_face()}
/* Layout: one light reading column on a lilac wall, specimens laid out like a brand sheet; the sketch is the only big image */
:root{{
  --wall:#F5F0FF; --paper:#FFFFFF; --ink:#1B0B3A; --muted:#5D5376; --line:#E2D8F5;
  --primary:#4F01A3; --electric:#853DFF; --midnight:#20004C; --pink:#EC4AF0; --orange:#FF8553;
  --display:"Roku Display","Helvetica Neue",Arial,sans-serif;
  --body:"Roku Display","Helvetica Neue",Arial,sans-serif;
  --mono:ui-monospace,"Cascadia Mono",Consolas,monospace;
  color-scheme:light;
}}
html{{background:var(--wall);scroll-padding-top:calc(env(safe-area-inset-top,0px) + 64px)}}
body{{background:var(--wall);color:var(--ink);font-family:var(--body);font-weight:400;font-size:16px;line-height:1.55;padding-inline:clamp(16px,4vw,48px);padding-block:0 96px}}
.wrap{{max-width:1180px;margin:0 auto;display:flex;flex-direction:column;gap:72px}}
h1,h2,h3{{margin:0;font-family:var(--display);text-wrap:balance}}
h1{{font-weight:700;font-size:clamp(44px,7vw,88px);line-height:.95;letter-spacing:-.02em;color:var(--primary)}}
h1 span{{color:var(--electric)}}
h2{{font-weight:700;font-size:clamp(28px,3.4vw,40px);line-height:1.05;letter-spacing:-.01em;color:var(--primary)}}
h3{{font-weight:700;font-size:18px;line-height:1.3}}
p{{margin:0;max-width:66ch}}
a{{color:var(--primary)}}
a:focus-visible{{outline:2px solid var(--electric);outline-offset:3px}}
.mono{{font-family:var(--mono);font-size:12.5px}}
.eyebrow{{font-weight:700;font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}}
.lede{{font-size:19px;color:var(--muted)}}
.top{{display:grid;grid-template-columns:minmax(0,1.05fr) minmax(0,1fr);gap:clamp(24px,4vw,56px);align-items:center;padding-block:56px 8px}}
.top .t{{display:flex;flex-direction:column;gap:18px}}
.top .lk{{width:220px;height:auto}}
.top figure{{margin:0;display:flex;flex-direction:column;gap:10px}}
.top figure img{{width:100%;height:auto;display:block;border-radius:6px;box-shadow:0 24px 60px -30px rgba(79,1,163,.45)}}
.top figcaption{{font-size:13px;color:var(--muted)}}
.meta{{display:flex;flex-wrap:wrap;gap:6px 18px;font-size:14px;color:var(--muted)}}
@media (max-width:820px){{.top{{grid-template-columns:1fr}}}}
.nav{{position:sticky;top:env(safe-area-inset-top,0px);z-index:5;background:color-mix(in srgb,var(--wall) 92%,transparent);backdrop-filter:blur(8px);border-bottom:1px solid var(--line);margin-inline:calc(-1*clamp(16px,4vw,48px));padding:12px clamp(16px,4vw,48px);overflow-x:auto}}
.nav ul{{list-style:none;margin:0 auto;padding:0;display:flex;gap:4px;max-width:1180px}}
.nav a{{display:block;padding:6px 12px;border-radius:999px;text-decoration:none;font-weight:500;font-size:14px;color:var(--ink);white-space:nowrap}}
.nav a:hover{{background:var(--paper)}}
section{{display:flex;flex-direction:column;gap:24px}}
.sh{{display:flex;flex-direction:column;gap:10px;border-top:2px solid var(--primary);padding-top:20px}}
.grid{{display:grid;gap:16px}}
.g2{{grid-template-columns:repeat(auto-fit,minmax(300px,1fr))}}
.g3{{grid-template-columns:repeat(auto-fit,minmax(240px,1fr))}}
.g4{{grid-template-columns:repeat(auto-fit,minmax(220px,1fr))}}
.note{{background:var(--paper);border:1px solid var(--line);border-radius:12px;padding:18px 20px;display:flex;flex-direction:column;gap:8px}}
.note p{{font-size:15px}}
.note .k{{font-weight:700;font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:var(--electric)}}
.note.warn .k{{color:#B23A00}}
ul.rules{{margin:0;padding-left:1.1em;display:flex;flex-direction:column;gap:8px;max-width:72ch}}
ul.rules li::marker{{color:var(--electric)}}
.sw{{display:flex;flex-direction:column;border-radius:12px;overflow:hidden;background:var(--paper);border:1px solid var(--line)}}
.sw-c{{height:92px;background:var(--c)}}
.sw-t{{display:flex;flex-direction:column;gap:2px;padding:12px 14px;font-size:13px;color:var(--muted)}}
.sw-t b{{color:var(--ink);font-size:15px}}
.sw-t em{{font-style:normal;color:#B23A00}}
.sub{{font-weight:700;font-size:13px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}}
.pr{{display:grid;grid-template-columns:64px 1fr auto;gap:14px;align-items:center;background:var(--paper);border:1px solid var(--line);border-radius:12px;padding:10px 14px 10px 10px}}
.pr-s{{height:52px;border-radius:8px;display:grid;place-items:center;font-family:var(--display);font-weight:700;font-size:26px;border:1px solid var(--line)}}
.pr b{{display:block;font-size:15px}}
.pr span{{font-size:13px;color:var(--muted)}}
.tag{{font-size:12px;font-weight:500;padding:4px 10px;border-radius:999px;white-space:nowrap;font-variant-numeric:tabular-nums}}
.t-ok{{background:#E5F7EE;color:#11643A}} .t-lg{{background:#FFF1DE;color:#8A4B00}} .t-no{{background:#FDE6E6;color:#A11B1B}}
.grad{{height:110px;border-radius:12px;display:flex;align-items:flex-end;padding:12px 14px;color:#fff;font-size:13px;font-weight:500}}
.spec{{display:flex;flex-direction:column;gap:18px;background:var(--paper);border:1px solid var(--line);border-radius:12px;padding:24px}}
.spec .row{{display:grid;grid-template-columns:140px 1fr;gap:16px;align-items:baseline;border-bottom:1px solid var(--line);padding-bottom:16px}}
.spec .row:last-child{{border-bottom:0;padding-bottom:0}}
.spec .row>span{{font-size:13px;color:var(--muted)}}
.spec .row>div{{font-family:var(--display);color:var(--primary);overflow-wrap:anywhere}}
@media (max-width:560px){{.spec .row{{grid-template-columns:1fr}}}}
.logos{{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:16px}}
.lg{{border-radius:12px;display:grid;place-items:center;height:150px;padding:24px;border:1px solid var(--line)}}
.lg svg{{width:72%;max-width:260px;height:auto}}
.cap{{font-size:13px;color:var(--muted);margin-top:8px}}
.dd{{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:16px}}
.dd .note h3{{display:flex;gap:8px;align-items:center}}
.ok-t{{color:#11643A}} .no-t{{color:#A11B1B}}
.prev{{margin:0;display:flex;flex-direction:column;gap:10px}}
.refs{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:16px}}
.refs figure{{margin:0;display:flex;flex-direction:column;gap:8px}}
.refs img{{width:100%;border-radius:8px;display:block;border:1px solid var(--line)}}
.refs figcaption{{font-size:13px;color:var(--muted)}}
.fmts{{display:flex;flex-wrap:wrap;gap:24px;align-items:flex-end}}
.fmt{{margin:0;display:flex;flex-direction:column;gap:10px}}
.fmt svg{{display:block;max-width:100%;height:auto;border-radius:4px;border:1px solid var(--line)}}
.fmt figcaption{{display:flex;flex-direction:column;gap:2px;font-size:13px;color:var(--muted);max-width:240px}}
.fmt figcaption b{{color:var(--ink);font-size:15px}}
.lay{{display:flex;flex-wrap:wrap;gap:20px;align-items:flex-end}}
.lay figure{{margin:0;display:flex;flex-direction:column;gap:8px}}
.lay svg{{display:block;height:auto;border-radius:4px;border:1px solid var(--line)}}
.lay figcaption{{font-size:13px;color:var(--muted)}}
.tv169{{width:min(100%,520px)}}
.scroll{{overflow-x:auto}}
table{{border-collapse:collapse;width:100%;min-width:620px;background:var(--paper);border:1px solid var(--line);border-radius:12px;overflow:hidden}}
th,td{{text-align:left;padding:12px 16px;border-bottom:1px solid var(--line);font-size:15px;vertical-align:top}}
th{{font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);font-weight:700}}
td.hl{{font-family:var(--display);font-weight:700;color:var(--primary);font-size:17px}}
td mark{{background:none;color:var(--electric)}}
tr.flag td:last-child{{color:#B23A00}}
ol.steps{{margin:0;padding-left:1.3em;display:flex;flex-direction:column;gap:10px;max-width:74ch}}
.hubpill{{position:fixed;top:calc(12px + env(safe-area-inset-top,0px));right:12px;z-index:20;background:var(--primary);color:#fff;text-decoration:none;font-weight:500;font-size:13px;padding:8px 14px;border-radius:999px;box-shadow:0 4px 14px -4px rgba(32,0,76,.5)}}
@media (prefers-reduced-motion:no-preference){{html{{scroll-behavior:smooth}}}}
</style>
<a class="hubpill" href="{HUB_URL}" target="_blank" rel="noopener">Deliverables Hub &rarr;</a>
<header class="top">
  <div class="t">
    {lockup("lk")}
    <span class="eyebrow">Roku Ads Manager · Meta and CTV · Updated 2026-10-12</span>
    <h1>Roku <span>Design System</span></h1>
    <p class="lede">The working sheet for Roku Ads Manager paid social and CTV. Brand tokens from the 2024 guideline, plus the mixed-media living-room direction for RKU26013, Sell it on Roku: a real room that looks out on an illustrated city.</p>
    <div class="meta"><span>Font: Roku Display</span><span>Canvas: 1440 grid, 1920 for CTV</span><span>Next job: RKU26013</span></div>
  </div>
  <figure><img src="{frame}" alt="RKU26013 Pet 1:1: a bright real living room, a goldendoodle watching a purple pet-food ad on the TV, a flat illustrated lilac city seen through the floor-to-ceiling windows"><figcaption>RKU26013, Pet 1:1, V2 for review. Real room and TV ad generated with Figma AI; the city outside the windows is our own flat illustration.</figcaption></figure>
</header>
<nav class="nav" aria-label="Sections"><ul>
  <li><a href="#status">Status</a></li><li><a href="#color">Color</a></li><li><a href="#type">Type</a></li>
  <li><a href="#logo">Logo</a></li><li><a href="#illustration">Illustration</a></li><li><a href="#formats">Formats</a></li>
  <li><a href="#layout">Layout</a></li><li><a href="#copy">Copy</a></li><li><a href="#motion">Motion</a></li><li><a href="#handoff">Build handoff</a></li>
</ul></nav>
<main class="wrap">

<section id="status">
  <div class="sh"><span class="eyebrow">Status</span><h2>What this page is built on</h2>
  <p>Tokens come from the Roku 2024 Brand Guidelines as captured in the Figma Library style guide (Claude Design Ops - Lab, node 74:8964). The RKU26013 look follows the concept deck's own references (slide 7, Sell It On Roku), as asked on 2026-10-12.</p></div>
  <div class="grid g3">
    <div class="note"><span class="k">In place</span><h3>Roku Display, the real face</h3><p>Installed on the build machine and embedded here. The written guideline names Gotham; the team note on the style guide says not to use it.</p></div>
    <div class="note"><span class="k">In place</span><h3>Logo from the source vectors</h3><p>Roku wordmark and the Roku Ads Manager lockup, exported from the Figma Library. Never redrawn.</p></div>
    <div class="note"><span class="k">In place</span><h3>Previous round on file</h3><p>RKU26008, 7 industries in 1:1 and 9:16 (LAB file, node 514:22). It is the starting layout and the look we move away from.</p></div>
    <div class="note warn"><span class="k">Off limits</span><h3>No brand-kit graphics</h3><p>Main brand graphics (Roku City art, brand illustration library) trigger a long approval chain. The city in our frames is our own drawing.</p></div>
    <div class="note warn"><span class="k">To confirm</span><h3>Five or six industries</h3><p>The brief counts 4 sizes × 5 variations = 20, but its copy table lists 6 industries. Fashion carries a tech line.</p></div>
    <div class="note warn"><span class="k">To confirm</span><h3>Animation length</h3><p>The brief marks length N/A while ticking 15, 20, 30 and 60 seconds. We need the CTV spot length and whether Meta gets motion too.</p></div>
  </div>
</section>

<section id="color">
  <div class="sh"><span class="eyebrow">Color</span><h2>Purple first, kept light for this job</h2>
  <p>Primary Purple leads. Midnight Purple only steps in where Primary fails contrast. Accents add energy in small doses. For RKU26013 the client asked for purples that stay light: the drawn city uses the lilac tints, the room keeps its own warm whites and oak, and purple shows up in props, the throw and the TV ad.</p></div>
  <span class="sub">Core</span><div class="grid g3">{core}</div>
  <span class="sub">Accent</span><div class="grid g4">{acc}</div>
  <span class="sub">Neutrals</span><div class="grid g4" style="grid-template-columns:repeat(auto-fit,minmax(150px,1fr))">{neu}</div>
  <span class="sub">RKU26013 lilac tints · drawn city and accents</span><div class="grid g4">{scn}</div>
  <span class="sub">Pairings, text on background</span><div class="grid g2">{pairs}</div>
  <span class="sub">Gradients</span>
  <div class="grid g3">
    <div class="grad" style="background:linear-gradient(135deg,#853DFF,#20004C)">Diagonal</div>
    <div class="grad" style="background:linear-gradient(90deg,#853DFF,#20004C)">Horizontal</div>
    <div class="grad" style="background:linear-gradient(180deg,#853DFF,#20004C)">Vertical</div>
  </div>
  <p>Diagonal, horizontal and vertical gradients are allowed. Copy and the logo sit over the darkest part. On RKU26013 gradients live only on the TV screen and in the window light.</p>
</section>

<section id="type">
  <div class="sh"><span class="eyebrow">Type</span><h2>Roku Display, sized for a 1440 canvas</h2>
  <p>One family for everything. Bold for headlines, Medium for on-screen TV copy, Regular for small print. Sizes below are in canvas pixels at 1440 wide; CTV scales by 1920 / 1440.</p></div>
  <div class="spec">
    <div class="row"><span>Headline · Bold 118 / 130, −1.8%</span><div style="font-weight:700;font-size:clamp(30px,5vw,56px);line-height:1.1;letter-spacing:-.018em;color:#14082B">Put your <span style="color:var(--primary)">pet brand</span><br>in their living room.</div></div>
    <div class="row"><span>TV ad · Bold 45 / 48, on the screen</span><div style="font-weight:700;font-size:26px;line-height:1.2;color:var(--midnight)">More tail wags. Better days.</div></div>
    <div class="row"><span>Small print · Regular 24 / 32</span><div style="font-weight:400;font-size:16px;color:var(--muted)">Roku Ads Manager. Self-serve TV advertising.</div></div>
    <div class="row"><span>Weights on file</span><div style="display:flex;gap:28px;flex-wrap:wrap;font-size:30px"><span style="font-weight:400">Regular</span><span style="font-weight:500">Medium</span><span style="font-weight:700">Bold</span><span style="font-weight:900">Black</span></div></div>
  </div>
  <ul class="rules">
    <li>Headline is two lines, centered on the wall above the windows: Ink for the line, Primary Purple for the industry word.</li>
    <li>RKU26008 set the swapped word in Pink. On the light wall Pink drops under 3:1, so it stays Primary Purple.</li>
    <li>All headlines share one size per format, set by the longest line (wellness brand), so the six variations match.</li>
    <li>No Gotham, no stand-in faces in production files.</li>
  </ul>
</section>

<section id="logo">
  <div class="sh"><span class="eyebrow">Logo</span><h2>Supplied artwork, two marks</h2>
  <p>Roku Ads Manager signs every frame: the horizontal lockup, centered above the headline. Supplied vectors, Primary Purple and Gray 1.</p></div>
  <div class="logos">
    <div><div class="lg" style="background:var(--wall)">{lockup("", "#4F01A3", "#646464")}</div><p class="cap">Lockup on light: Primary Purple and Gray 1. Use on the RKU26013 wall.</p></div>
    <div><div class="lg" style="background:var(--midnight)">{lockup("", "#FFFFFF", "#FFFFFF")}</div><p class="cap">Lockup on dark: all White.</p></div>
    <div><div class="lg" style="background:var(--primary);color:#fff">{wordmark()}</div><p class="cap">Wordmark White on Primary or on the TV screen.</p></div>
    <div><div class="lg" style="background:var(--paper);color:var(--primary)">{wordmark()}</div><p class="cap">Wordmark Primary Purple on White.</p></div>
  </div>
  <div class="dd">
    <div class="note"><h3 class="ok-t">Do</h3><ul class="rules"><li>Horizontal lockup centered, 380px wide at 1440, 72px from the top.</li><li>Keep the height of the wordmark clear on every side.</li><li>Logo over the darkest part of a gradient.</li></ul></div>
    <div class="note"><h3 class="no-t">Don't</h3><ul class="rules"><li>Recolor outside Primary, White or Black.</li><li>Place the lockup over the windows or the TV.</li><li>Rebuild the mark in a font.</li></ul></div>
  </div>
</section>

<section id="illustration">
  <div class="sh"><span class="eyebrow">Imagery · RKU26013</span><h2>A real room, an illustrated city outside</h2>
  <p>Mixed media, as the concept deck's references do, in our own composition: a bright, real apartment living room whose floor-to-ceiling windows look out on a pure flat illustration of the city. The room and the TV ad are generated with Figma AI. The city is our own illustration (sky, sun, clouds, three depths of towers, lit windows), keyed into the glass only, so frames, plants and furniture stay in front of it. It is a view outside, never a pattern on the wall.</p></div>
  <div class="refs">
    <figure><img src="{ref1}" alt="Deck reference: Put your home brand in their living room, real living room with a lilac skyline on the wall"><figcaption>Deck reference, slide 7 · Home</figcaption></figure>
    <figure><img src="{ref2}" alt="Deck reference: Put your pet brand in their living room, dog watching a pet-food ad, lilac skyline behind"><figcaption>Deck reference, slide 7 · Pet</figcaption></figure>
    <figure><img src="{frame}" alt="Our RKU26013 Pet 1:1 frame"><figcaption>RKU26013 · Pet 1:1 · V2</figcaption></figure>
  </div>
  <div class="dd">
    <div class="note"><h3 class="ok-t">Do</h3><ul class="rules">
      <li>Real room: warm white walls, a wall of black-framed windows, light oak console, cream boucle seating, lavender textiles, a plant, soft daylight, symmetrical front-on camera.</li>
      <li>TV switched off in the plate, then the ad composited onto the glass: purple set, one product, copy on the left third.</li>
      <li>The city is a pure illustration: flat fills, crisp edges, no photo texture, no blending with the room. Three lilac depths, a warm sun, flat clouds, a few lit windows. The same city in every industry.</li>
      <li>One living cue per industry in the room (the dog for Pet) and purple props on the coffee table.</li>
      <li>Plates are generated with blown-out white glass so the illustration keys in cleanly, edges included. Keep the wall above the windows empty for the headline.</li>
    </ul></div>
    <div class="note"><h3 class="no-t">Don't</h3><ul class="rules">
      <li>Moody, dark rooms like RKU26008, or a purple cast over the whole photo.</li>
      <li>Claymation or 3D-toy looks (the vibe.co problem).</li>
      <li>Roku City artwork, brand illustration library pieces or brand icons.</li>
      <li>Readable brand names or fake logos inside generated images; on-screen copy is set in type.</li>
      <li>City printed on the wall like wallpaper, or tinted into the photo. It lives behind the glass.</li><li>Copying the deck reference layout: this is a new version, with its own camera, furniture and type placement.</li>
    </ul></div>
  </div>
  <div class="grid g3">
    <div class="note"><span class="k">Room cue · Pet</span><p>Dog watching the TV, rope toy and kibble bowl on the table.</p></div>
    <div class="note"><span class="k">Room cue · Beauty</span><p>Skincare bottles and a candle on the table.</p></div>
    <div class="note"><span class="k">Room cue · Food &amp; Bev</span><p>Pastries, coffee cups, a snack bowl.</p></div>
    <div class="note"><span class="k">Room cue · Wellness</span><p>Rolled yoga mat, water bottle, towel.</p></div>
    <div class="note"><span class="k">Room cue · Fashion or Tech</span><p>Pending the copy answer: shopping bag and shoe box, or headphones and a tablet.</p></div>
    <div class="note"><span class="k">Room cue · Homegoods</span><p>New cushion and throw, a vase, a lamp.</p></div>
  </div>
</section>

<section id="formats">
  <div class="sh"><span class="eyebrow">Formats</span><h2>Four canvases, one safe area each</h2>
  <p>Meta runs on the 1440 grid. The CTV spot is 1920 × 1080. Diagrams are drawn to scale; the shaded bands are platform UI.</p></div>
  <div class="fmts">{fmts}</div>
</section>

<section id="layout">
  <div class="sh"><span class="eyebrow">Layout</span><h2>Lockup, headline, TV, room, CTA</h2>
  <p>One top block on the wall: lockup, headline, then the Learn more button, all centered. The window glass starts right under it and the TV sits just below the glass top: the empty sky band above the TV is cut from the plate so text and TV read as one unit. Room cues fill the foreground corners.</p></div>
  <div class="grid g3">
    <div class="note"><span class="k">CTA</span><p>"Learn more" with a chevron, Roku Display Bold, white on Primary Purple, radius 0.35 × type size, soft Midnight shadow. Part of the top block, centered under the headline, never over the TV or the window.</p></div>
    <div class="note"><span class="k">1:1 · 1440 × 1440</span><p>Lockup 340px at 60px, headline 104px in two lines at 118px, CTA 34px type at 370px, window top at 492px, TV 64px below it. Room zoomed 1.14×.</p></div>
    <div class="note"><span class="k">4:5 · 1440 × 1800</span><p>Vertical plate. Lockup at 72px, headline 112px at 136px, CTA 36px type at 402px, window top at 540px, TV 84px below it. Room zoomed 1.08×.</p></div><div class="note"><span class="k">9:16 · 1440 × 2560</span><p>Vertical plate, scaled to the height. The block starts at 300px, clear of the top 267px: lockup, headline 120px at 372px, CTA 42px type at 660px, window top at 800px.</p></div>
    <div class="note"><span class="k">16:9 CTV</span><p>Wide plate. Lockup 250px at 48px, headline 66px on one line at 84px, CTA 24px type at 176px, window top at 262px. The six industry frames run as one 15-second spot.</p></div>
  </div>
</section>

<section id="copy">
  <div class="sh"><span class="eyebrow">Copy</span><h2>One line, the industry word swaps</h2>
  <p>Client copy, placed exactly as written. No dashes in any line. The highlighted word is the only thing that changes.</p></div>
  <div class="scroll"><table><thead><tr><th>Industry</th><th>Headline</th><th>Note</th></tr></thead><tbody>{rows}</tbody></table></div>
</section>

<section id="motion">
  <div class="sh"><span class="eyebrow">Motion</span><h2>Headline and screen move, the room breathes</h2>
  <p>From the brief: animation is mainly the headline and the TV screen, with subtle keyframes in the foreground or background for quality.</p></div>
  <div class="grid g3">
    <div class="note"><span class="k">Headline</span><p>The industry word swaps in place: old word slides up and out, new word rises in. Line two stays still.</p></div>
    <div class="note"><span class="k">TV screen</span><p>Roku wordmark fades up, the line types on, the progress bar runs. The screen glow pulses once on each swap.</p></div>
    <div class="note"><span class="k">Ambient</span><p>City windows blink at random, lamp light breathes, the plant sways a few degrees, the skyline drifts a little for parallax.</p></div>
  </div>
  <p>Timing proposal until length is confirmed: 3 seconds per industry, so five industries make a 15-second CTV spot with an end hold on the lockup.</p>
</section>

<section id="handoff">
  <div class="sh"><span class="eyebrow">Build handoff</span><h2>How a frame is made and named</h2></div>
  <ol class="steps">
    <li>Generate the room plate (white blown-out window glass, TV off, empty wall, no text) and the TV ad with Figma AI into <span class="mono">img/raw/</span> of <span class="mono">clients/roku/03-work/ads/2026-rku26013-sell-it-on-roku/</span>.</li>
    <li>Run <span class="mono">compose.py</span> (illustrated city keyed into the window glass, ad on the TV, wall extended), then <span class="mono">build.py</span> (headline, lockup and on-screen copy in HTML, exported by Chrome).</li>
    <li>Check every frame: lockup and headline inside the safe area, nothing on the platform bands, headline size equal across industries, no white fringe around plants, fur or the TV.</li>
    <li>Export PNG (static) and MP4 (animated) to <span class="mono">04-deliverables/ads/2026-rku26013-sell-it-on-roku/</span>.</li>
    <li>Name files <span class="mono">RKU26013-SellItOnRoku-1440x1440-Static-Meta-Pet-V1.png</span>; CTV is <span class="mono">RKU26013-SellItOnRoku-1920x1080-Animated-CTV-AllIndustries-V1.mp4</span>.</li>
    <li>Add the job to the Roku Deliverables Hub and republish it from a fresh read.</li>
  </ol>
</section>
</main>
"""


if __name__ == "__main__":
    out = Path(sys.argv[1] if len(sys.argv) > 1 else BRAND / "roku-design-system.html")
    out.write_text(build(), encoding="utf8")
    print(out, round(out.stat().st_size / 1024), "KB")
