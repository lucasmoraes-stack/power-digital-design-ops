"""Build the Roku Deliverables Hub.

    python build_hub.py <out.html>

Same organization as the Katapult and Habit hubs: channel tabs, a jobs bar
(code · name · frame count), an index of job cards, and one view per job
opened by its hash (#rku26013, #reframe). Add a job by appending to JOBS and
writing its body function. Republish to the same URL from a fresh read.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "01-brand"))
from rk_common import DS_URL, font_face, img_data, lockup  # noqa: E402

INBOX = ROOT / "00-inbox" / "2026-10-12-rku26013-previous-work"
DECK = ROOT / "00-inbox" / "2026-10-12-rku26013-concept-deck"
JOB = ROOT / "03-work" / "ads" / "2026-rku26013-sell-it-on-roku"
REVIEW = JOB / "img" / "review"  # one JPEG per exported frame, named like the export
LAB_FIGMA = "https://www.figma.com/design/D8FpNuKI3uPGjCPqonIn3C/Progressive-Global---LAB?node-id=514-22"
REFRAME_FIGMA = "https://www.figma.com/design/pcf9QNPjvBBzqDPnBLefVS/Claude-Design-Ops---Lab"

INDUSTRIES = [
    ("Pet", "Pet Supplies", "pet brand", ""),
    ("Beauty", "Beauty", "beauty brand", ""),
    ("FoodBev", "Food & Bev", "products", ""),
    ("Wellness", "Wellness", "wellness brand", ""),
    ("Fashion-Tech", "Fashion", "latest tech", "Built as tech, per the copy. Confirm."),
    ("Homegoods", "Homegoods", "home brand", ""),
]
SIZES = [("1440x1440", "1:1", 1440, 1440, "Meta"), ("1440x1800", "4:5", 1440, 1800, "Meta"),
         ("1440x2560", "9:16", 1440, 2560, "Meta"), ("2560x1440", "16:9", 2560, 1440, "CTV")]


def fname(code, sz, plat):
    v = "V4"  # 2026-10-13: ChatGPT rooms, lilac panel layout in every size
    return f"RKU26013-SellItOnRoku-{sz}-Static-{plat}-{code}-{v}"


def slot(name, w, h, label, H=170):
    f = REVIEW / f"{name}.jpg"
    if not f.exists():
        return (f'<figure class="slot" title="{name}" style="width:{round(H * w / h)}px"><div class="slot-f" style="aspect-ratio:{w}/{h}">'
                f'<span class="st">Not started</span></div><figcaption>{label}</figcaption></figure>')
    return (f'<figure class="slot done" title="{name}" style="width:{round(H * w / h)}px"><button type="button" class="slot-f zoom" style="aspect-ratio:{w}/{h}" aria-label="Enlarge {name}">'
            f'<img src="{img_data(f)}" alt="{name}"></button><figcaption>{label}</figcaption></figure>')


def storyboard():
    sys.path.insert(0, str(JOB))
    from storyboard import FRAMES, PFX  # noqa: E402
    cards = []
    for n, (ind, t0, hold, _o, scene, action) in enumerate(FRAMES, 1):
        name = f"{PFX}-F{n:02d}-V4"
        cards.append(f'<figure class="sbf"><button type="button" class="zoom" aria-label="Enlarge frame {n}"><img src="{img_data(REVIEW / (name + ".jpg"))}" alt="Frame {n}, {scene}"></button>'
                     f'<figcaption><span class="tc">F{n:02d} · {t0:04.1f}s to {t0 + hold:04.1f}s</span><b>{scene}</b><span>{action}</span></figcaption></figure>')
    return "".join(cards)


def rku26013():
    rows, built = [], 0
    for code, name, word, note in INDUSTRIES:
        cells = "".join(slot(fname(code, sz, plat), w, h, r) for sz, r, w, h, plat in SIZES)
        built += sum((REVIEW / f"{fname(code, sz, plat)}.jpg").exists() for sz, _, _, _, plat in SIZES)
        rows.append(f'<div class="mx-row"><div class="mx-h"><b>{name}</b><span>Put your <mark>{word}</mark> in their living room.</span>'
                    + (f'<em>{note}</em>' if note else "") + f'</div><div class="mx-cells">{cells}</div></div>')
    reel = "".join(f'<img src="{img_data(REVIEW / (fname(c, "2560x1440", "CTV") + ".jpg"))}" alt="CTV frame, {n}" style="animation-delay:{i * 3 - 0.6:.1f}s">'
                   for i, (c, n, _, _) in enumerate(INDUSTRIES))
    prev = img_data(INBOX / "overview-review.jpg")
    opts = "".join(f'<div class="opt"><span class="opt-t">{name}</span><b>Put your <mark>{word}</mark> in their living room.</b></div>'
                   for _, name, word, _ in INDUSTRIES)
    return f"""
  <div class="jh">
    <span class="label">RKU26013 · Meta and YouTube / CTV · Full funnel · Sell it on Roku</span>
    <h2>Sell it on Roku</h2>
    <p class="idea">Roku is where people watch; this job sells it as the place businesses advertise. A bright, real apartment living room whose windows look out on our own flat illustrated city. A business ad plays on the TV, the room carries each industry's cue, and one word of the headline swaps per industry. In every size a light lilac panel carries the lockup, the headline and a Learn more button; the room fills the rest.</p>
    <ul class="counts"><li><b>{built}</b> frames built</li><li><b>6</b> industries</li><li><b>4</b> sizes</li><li><b>15s</b> CTV animatic</li><li><b>8</b> storyboard frames</li></ul>
    <div class="opts">{opts}</div>
    <p class="next"><b>For review, 2026-10-13 · V4.</b> Six industries in Meta 1:1, 4:5, 9:16 and CTV 16:9, all on one locked room and all in the panel layout. Click any frame to see it larger. The CTV storyboard and the 15-second animatic run on the same V4 rooms. Three answers still needed from the account lead, listed in the production notes.</p>
    <details class="more"><summary>Production notes</summary><div class="notes">
      <p><b>V4 · 2026-10-13:</b> one room for all six industries, generated in ChatGPT from the same reference (camera, window, TV, sideboard, plant, coffee table and armchair locked), so only the props and the TV ad change between industries. The TV ad is part of the generated image; the on-screen copy, its button and the "Ad · 0:15" tag are live type on the screen's empty left. The city is keyed into the glass as before. Layout: the 16:9 split strategy now runs in every size. Meta 1:1, 4:5 and 9:16 put the lilac panel on top (lockup, headline, CTA, left-aligned; on 9:16 all copy sits inside the 267px top and 333px bottom safe zones) and the room below, cropped close on the TV. Headlines: two lines at 118px on 1:1 and 4:5, three lines at most on 9:16 ("Put your / industry / in their living room."). The room is shorter and zoomed on the TV; the dog's head stays in frame. CTV 16:9 keeps the V3 split on the new room. V2 and V3 files are kept in <span class="mono">_superseded-v2-v3/</span>.</p>
      <p><b>Direction:</b> the client called RKU26008 a middle space, neither real nor illustrated, and it was flagged as close to vibe.co. The call agreed on a brand moment; the follow-up (2026-10-12) set the look: mixed media like the deck's slide 7 references, real room elements with illustration in the background, in a composition of our own.</p>
      <p><b>V2:</b> V1 copied the deck reference layout and its city read as wallpaper. V2 has its own composition (symmetric window wall, centered type, cue on the armchair, coffee table opposite) and the city is a pure flat illustration seen through the glass. Same city in every frame.</p>
      <p><b>V3 · CTV 16:9 only:</b> on 16:9 the headline was small and squeezed onto the wall. V3 splits the frame: a light lilac panel on the left carries the lockup, a much larger four-line headline and the CTA; the room fills the rest. The panel ends where the copy ends, with the same margin on the right of the headline as on its left, so its width changes slightly per industry. The room is the same square plate as the Meta 1:1, centered in the space right of the panel, so the whole scene shows (cue, coffee table, plant). Meta 1:1, 4:5 and 9:16 keep the V2 layout.</p>
      <p><b>CTV size:</b> built at 2560×1440 to match the 16x9 boards in the Figma file (all sizes ×4/3 from 1920×1080; export at 0.75x for 1920×1080). The headline is the same 146px, four lines, in every industry, and the HTML for Figma import has no script and a slightly wider headline box, so Figma's font metrics never re-wrap it.</p>
      <p><b>How it is made:</b> room plates and TV ads generated with Figma AI (not Runway), 18 room plates and 6 ads. The glass is found by flood-filling the blown-out white panes and keyed with closed-form matting, so fur, leaves and frames stay in front with clean edges (no white rims). A QA pass (qa_key.py) flags any white glass left next to the city; light objects touching the glass (white pots, cream sofas, a white sideboard top) are protected from lilac bleed. Headline, lockup, on-screen copy and CTA are live type, exported by Chrome.</p>
      <p><b>Storyboard props · 2026-10-13:</b> the coffee table shadows were redone. The old soft grey halo around every object is gone; each prop now has a thin contact line only where it really touches the table (read from the generated photo, so leaves and handles in the air cast nothing there), a soft pool around the base and a short, diffuse shadow toward the camera, as the light comes from the window behind. The beauty set is smaller and its candle about two thirds of its old size.</p>
      <p><b>Sideboard and TV stand · 2026-10-13:</b> shown straight on: every TV now has the same flat stand (taken from the Food 4:5 room) resting right on the sideboard's top edge, and the top surface is no longer seen. Food uses its 4:5 room in every size. Window, city, objects, dog and flowers are unchanged. Window posts run down to the sideboard and the leftovers of the old top are cleaned up. One room per industry, cropped for every size (Food uses its 4:5 room, cut square for CTV), and each stand is centred on its TV. Only the TV stands on the sideboard (vases, lamps and bowls removed), sofas have a crisp edge against the window.</p>
      <p><b>CTA:</b> "Learn more" button in Primary Purple, in the top block under the headline. The empty sky above the TV is cut from each plate so the TV sits right under the text. The TV ad copy (advertiser lines and its small button) is ours and fictional; only the headlines are the client's.</p>
      <p><b>Constraint:</b> no main graphics from the Roku brand kit. The city is our own illustration, not Roku City art.</p>
      <p><b>Retouch:</b> the V2 Homegoods 16:9 had a patch of real outdoor view behind the flowers. The V3 16:9 uses the square plate, which does not have it.</p>
      <p><b>Open 1 · count:</b> the brief says 4 sizes × 5 variations = 20, but the copy table has 6 industries. All 6 are built; which five ship?</p>
      <p><b>Open 2 · Fashion:</b> the Fashion row reads "Put your latest tech in their living room." Built as tech (headphones, tablet). Fashion copy or Tech industry?</p>
      <p><b>Open 3 · motion:</b> length is marked N/A with 15, 20, 30 and 60 seconds ticked. The animatic runs 15 seconds, 2.4 seconds per industry with a crossfade. Full animation (word swap, ad playing, city lights) follows once length is confirmed.</p>
    </div></details>
  </div>
  <section class="part" id="rku26013-matrix"><div class="ph"><h3>All frames</h3><p>Every file by industry and size. Click a frame to enlarge. Files are named <span class="mono">RKU26013-SellItOnRoku-1440x1440-Static-Meta-Pet-V4</span> (PNG, plus the HTML in <span class="mono">html/</span>) and sit in <span class="mono">04-deliverables/ads/2026-rku26013-sell-it-on-roku/</span>.</p></div>
    {"".join(rows)}
  </section>
  <section class="part" id="rku26013-storyboard"><div class="ph"><h3>CTV spot · storyboard</h3><p>Eight beats of the 15-second 16:9 spot at 2560×1440. One locked shot: the room is a single plate for the whole spot (same camera, window, TV and furniture) and the panel keeps one width, so nothing jumps between frames. Only the industry word, the props on the coffee table and the TV ad change. Each frame is a PNG and an HTML for Figma in <span class="mono">04-deliverables/ads/2026-rku26013-sell-it-on-roku/storyboard/</span>.</p></div>
    <div class="sb">{storyboard()}</div>
  </section>
  <section class="part" id="rku26013-ctv"><div class="ph"><h3>CTV spot · animatic</h3><p>The six V4 16:9 frames in sequence. The 15-second MP4 delivered with the frames is cut on the storyboard timing above (<span class="mono">RKU26013-SellItOnRoku-2560x1440-Animatic-CTV-AllIndustries-V4.mp4</span>).</p></div>
    <div class="reel" role="img" aria-label="CTV animatic: the six industry frames crossfading">{reel}</div>
  </section>
  <section class="part" id="rku26013-refs"><div class="ph"><h3>Deck references</h3><p>Concept deck, slide 7. Followed for the mixed-media look, not for the layout.</p></div>
    <div class="sk">
      <figure style="width:min(100%,250px)"><div><img class="fr" src="{img_data(DECK / "deck-ref-2-review.jpg")}" alt="Deck reference, pet"></div><figcaption>Deck reference · Pet</figcaption></figure>
      <figure style="width:min(100%,250px)"><div><img class="fr" src="{img_data(DECK / "deck-ref-1-review.jpg")}" alt="Deck reference, home"></div><figcaption>Deck reference · Home</figcaption></figure>
    </div>
  </section>
  <section class="part" id="rku26013-prev"><div class="ph"><h3>Previous round · RKU26008</h3><p>Seven industries in 1:1 and 9:16. Reference for layout and props, not for the look. <a href="{LAB_FIGMA}" target="_blank" rel="noopener">Open in Figma</a></p></div>
    <img class="prev" src="{prev}" alt="RKU26008: seven photoreal purple living rooms in square and story sizes">
  </section>"""


def reframe():
    secs = [("V1: MOF Ad - MOBITE", "Video storyboard", 23), ("V1: MOF Ad - CAROUSEL", "Static carousel", 7),
            ("V1: MOF Ad - CAROUSEL - Version 2", "Static carousel", 7), ("V2: BOF Retargeting Ad - MOBITE", "Video storyboard", 17),
            ("V2: BOF Retargeting Ad - CAROUSEL", "Static carousel", 7)]
    tr = "".join(f'<tr><td>{a}</td><td>{b}</td><td class="n">{c}</td><td class="n">{c * 2}</td></tr>' for a, b, c in secs)
    return f"""
  <div class="jh">
    <span class="label">Holiday MOF and BOF · CTV ad creative · Figma reframe · 2026-08</span>
    <h2>Holiday reframes</h2>
    <p class="idea">Approved 16:9 MOF and BOF holiday creative recomposed into 9:16 and 1:1 inside the Figma file. Copy and layout were fixed; backgrounds, text and decoration were rebuilt for each ratio.</p>
    <ul class="counts"><li><b>122</b> frames</li><li><b>61</b> scenes</li><li><b>5</b> sections</li><li><b>9:16 · 1:1</b></li></ul>
    <p class="next"><b>Delivered in Figma.</b> Two checks left: a pass in Figma desktop with Roku Display installed, and a human look at the scenes with an art-direction call. <a href="{REFRAME_FIGMA}" target="_blank" rel="noopener">Open the Figma file</a></p>
    <details class="more"><summary>Production notes</summary><div class="notes">
      <p><b>Sizes:</b> 9:16 at 1440 × 2560 and 1:1 at 1440 × 1440, on the same 1440 scale as the 2560 × 1440 masters.</p>
      <p><b>Safe area (9:16):</b> nothing in the top 267px or the bottom 333px.</p>
      <p><b>Naming:</b> frames sit under the 16:9 row of each section as "9x16 - Scene NN (src id)" and "1x1 - Scene NN (src id)", so every frame traces back to its master.</p>
    </div></details>
  </div>
  <section class="part" id="reframe-sections"><div class="ph"><h3>Sections</h3><p>Scenes per section, and frames added (two ratios each).</p></div>
    <div class="scroll"><table><thead><tr><th>Section</th><th>Format</th><th class="n">Scenes</th><th class="n">New frames</th></tr></thead><tbody>{tr}
    <tr class="tot"><td>Total</td><td></td><td class="n">61</td><td class="n">122</td></tr></tbody></table></div>
  </section>"""


def reframe_thumb():
    return ('<svg viewBox="0 0 400 250" role="img" aria-label="16:9 master reframed to 9:16 and 1:1">'
            '<rect width="400" height="250" fill="#20004C"/>'
            '<rect x="28" y="70" width="176" height="99" rx="4" fill="#4F01A3"/><text x="116" y="125" text-anchor="middle" font-family="Roku Display,sans-serif" font-weight="700" font-size="18" fill="#fff">16:9</text>'
            '<path d="M214 120h26" stroke="#853DFF" stroke-width="3"/><path d="M240 112l10 8-10 8z" fill="#853DFF"/>'
            '<rect x="262" y="40" width="62" height="110" rx="4" fill="#853DFF"/><text x="293" y="100" text-anchor="middle" font-family="Roku Display,sans-serif" font-weight="700" font-size="14" fill="#fff">9:16</text>'
            '<rect x="262" y="160" width="62" height="62" rx="4" fill="#B391FF"/><text x="293" y="196" text-anchor="middle" font-family="Roku Display,sans-serif" font-weight="700" font-size="14" fill="#20004C">1:1</text>'
            '<rect x="334" y="40" width="40" height="182" rx="4" fill="none" stroke="#853DFF" stroke-dasharray="3 3" opacity=".5"/></svg>')


JOBS = [
    # channel, id, code, title, desc, counts, badge, thumb, body
    ("paid", "rku26013", "RKU26013", "Sell it on Roku",
     "Six industries, four sizes: a real living room looking out on an illustrated lilac city, a business ad on the TV, Learn more.",
     ["<b>24</b> frames", "<b>15s</b> CTV animatic"], "V4 · all sizes", lambda: f'<img src="{img_data(REVIEW / "RKU26013-SellItOnRoku-1440x1440-Static-Meta-Pet-V4.jpg")}" alt="">', rku26013),
    ("reframe", "reframe", "Holiday MOF/BOF", "Holiday reframes",
     "Approved 16:9 holiday creative recomposed into 9:16 and 1:1, built directly in Figma.",
     ["<b>122</b> frames", "<b>61</b> scenes"], "Delivered · Figma", reframe_thumb, reframe),
]
CHANNELS = [("paid", "Paid Social + CTV", "Meta and YouTube / CTV ads, built and exported here."),
            ("reframe", "Figma reframes", "Aspect-ratio work delivered inside the client's Figma file.")]


def build():
    tabs, bars, index, views = [], [], [], []
    for ch, name, blurb in CHANNELS:
        js = [j for j in JOBS if j[0] == ch]
        tabs.append(f'<button type="button" class="tab" role="tab" id="tab-{ch}" data-go="{ch}" aria-selected="false">{name} <small>{len(js)} job{"s" if len(js) > 1 else ""}</small></button>')
        bars.append(f'<nav class="jobs" data-ch="{ch}" aria-label="{name} jobs"><b>Jobs</b>'
                    + "".join(f'<a href="#{j[1]}">{j[2]} {j[3]} · {j[5][0].replace("<b>", "").replace("</b>", "")}</a>' for j in js) + '</nav>')
        cards = "".join(
            f'<a class="card" href="#{j[1]}"><div class="thumb">{j[7]()}<span class="badge">{j[6]}</span></div>'
            f'<div class="cb"><span class="code">{j[2]}</span><h3>{j[3]}</h3><p>{j[4]}</p>'
            f'<div class="cm">{"".join(f"<span>{c}</span>" for c in j[5])}<span class="go">Open &rarr;</span></div></div></a>' for j in js)
        index.append(f'<section class="ix" data-ch="{ch}" data-view="index" aria-labelledby="ix-{ch}"><div class="ixh"><h2 id="ix-{ch}">{name}</h2><p>{blurb}</p></div><div class="cards">{cards}</div></section>')
        for j in js:
            views.append(f'<article class="job" id="{j[1]}" data-ch="{ch}" data-view="{j[1]}" hidden><a class="back" href="#">&larr; All {name} jobs</a>{j[8]()}</article>')

    return f"""<title>Roku Deliverables Hub</title>
<style>
{font_face()}
/* Layout: masthead on Midnight like a TV at night, then a light lilac floor for the work; index of cards, one job per view */
:root{{
  --wall:#F5F0FF; --paper:#FFFFFF; --ink:#1B0B3A; --muted:#5D5376; --line:#E2D8F5;
  --primary:#4F01A3; --electric:#853DFF; --midnight:#20004C; --lilac:#D2BCFF; --warn:#B23A00;
  --display:"Roku Display","Helvetica Neue",Arial,sans-serif;
  --mono:ui-monospace,"Cascadia Mono",Consolas,monospace;
  color-scheme:light;
}}
html{{background:var(--wall)}}
body{{background:var(--wall);color:var(--ink);font-family:var(--display);font-size:16px;line-height:1.55;padding-block:0 96px}}
.w{{max-width:1180px;margin:0 auto;padding-inline:clamp(16px,4vw,48px)}}
h1,h2,h3{{margin:0;text-wrap:balance}}
p{{margin:0;max-width:68ch}}
a{{color:var(--primary)}}
a:focus-visible,button:focus-visible,summary:focus-visible{{outline:2px solid var(--electric);outline-offset:3px}}
.mono{{font-family:var(--mono);font-size:12px}}
mark{{background:none;color:var(--electric)}}
.mast{{background:var(--midnight);color:#fff;padding-block:56px 0}}
.mast .w{{display:flex;flex-direction:column;gap:16px}}
.mast .lk{{width:200px;height:auto}}
.mast .label{{font-weight:700;font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--lilac)}}
.mast h1{{font-weight:700;font-size:clamp(40px,6.4vw,80px);line-height:.98;letter-spacing:-.02em}}
.mast h1 span{{color:#B391FF}}
.mast p{{color:#D9CCF5;font-size:18px}}
.tabs{{display:flex;gap:6px;flex-wrap:wrap;margin-top:24px}}
.tab{{font:inherit;font-weight:500;font-size:15px;border:0;cursor:pointer;padding:12px 18px;border-radius:12px 12px 0 0;background:rgba(255,255,255,.08);color:#fff}}
.tab small{{opacity:.7;font-size:12px;margin-left:6px}}
.tab[aria-selected="true"]{{background:var(--wall);color:var(--primary)}}
.jobs{{display:flex;flex-wrap:wrap;gap:8px 10px;align-items:center;padding-block:16px;border-bottom:1px solid var(--line);font-size:14px}}
.jobs b{{font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted);margin-right:4px}}
.jobs a{{text-decoration:none;font-weight:500;padding:6px 12px;border-radius:999px;background:var(--paper);border:1px solid var(--line)}}
.jobs a[aria-current="true"]{{background:var(--primary);border-color:var(--primary);color:#fff}}
main{{display:flex;flex-direction:column;gap:48px;padding-top:36px}}
.ixh{{display:flex;flex-direction:column;gap:8px;margin-bottom:22px}}
.ixh h2{{font-size:clamp(28px,3.4vw,40px);font-weight:700;color:var(--primary);letter-spacing:-.01em}}
.ixh p{{color:var(--muted)}}
.cards{{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:20px}}
.card{{display:flex;flex-direction:column;text-decoration:none;color:inherit;background:var(--paper);border:1px solid var(--line);border-radius:14px;overflow:hidden;transition:transform .15s,box-shadow .15s}}
.card:hover{{transform:translateY(-2px);box-shadow:0 18px 40px -24px rgba(79,1,163,.5)}}
.thumb{{position:relative;aspect-ratio:16/10;background:var(--midnight);display:grid;place-items:center;overflow:hidden}}
.thumb svg{{width:100%;height:100%;object-fit:cover;display:block}}
.badge{{position:absolute;top:12px;left:12px;background:var(--primary);color:#fff;font-size:12px;font-weight:500;padding:4px 10px;border-radius:999px}}
.cb{{display:flex;flex-direction:column;gap:8px;padding:18px 20px 20px}}
.code{{font-family:var(--mono);font-size:12px;color:var(--muted)}}
.cb h3{{font-size:21px;font-weight:700;color:var(--primary)}}
.cb p{{font-size:15px;color:var(--muted)}}
.cm{{display:flex;gap:14px;flex-wrap:wrap;align-items:center;font-size:14px;margin-top:4px}}
.cm .go{{margin-left:auto;font-weight:700;color:var(--primary)}}
.back{{display:inline-block;margin-bottom:20px;font-weight:500;text-decoration:none}}
.jh{{display:flex;flex-direction:column;gap:16px}}
.jh .label{{font-weight:700;font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}}
.jh h2{{font-size:clamp(34px,4.6vw,56px);font-weight:700;color:var(--primary);letter-spacing:-.015em;line-height:1}}
.idea{{font-size:18px}}
.counts{{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:8px 22px;color:var(--muted);font-size:15px}}
.counts b{{color:var(--ink);font-variant-numeric:tabular-nums}}
.opts{{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:10px}}
.opt{{background:var(--paper);border:1px solid var(--line);border-radius:10px;padding:12px 14px;display:flex;flex-direction:column;gap:4px}}
.opt-t{{font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);font-weight:700}}
.opt b{{font-weight:700;color:var(--primary);line-height:1.3}}
.next{{background:var(--paper);border-left:3px solid var(--electric);padding:12px 16px;border-radius:0 10px 10px 0}}
.more summary{{cursor:pointer;font-weight:700;color:var(--primary)}}
.notes{{display:flex;flex-direction:column;gap:10px;padding-top:12px;font-size:15px}}
.part{{display:flex;flex-direction:column;gap:18px;margin-top:44px;border-top:2px solid var(--primary);padding-top:20px}}
.ph{{display:flex;flex-direction:column;gap:6px}}
.ph h3{{font-size:22px;font-weight:700}}
.ph p{{color:var(--muted)}}
.sk{{display:flex;gap:20px;flex-wrap:wrap;align-items:flex-end}}
.sb{{display:grid;grid-template-columns:repeat(auto-fill,minmax(min(100%,300px),1fr));gap:24px}}
.sbf{{margin:0;display:flex;flex-direction:column;gap:10px}}
.sbf button{{padding:0;border:0;background:none;cursor:zoom-in;display:block}}
.sbf img{{display:block;width:100%;height:auto;border-radius:4px;box-shadow:0 14px 34px -22px rgba(79,1,163,.6)}}
.sbf figcaption{{display:flex;flex-direction:column;gap:4px;font-size:13px;line-height:1.45}}
.sbf .tc{{font-variant-numeric:tabular-nums;font-size:12px;color:#646464}}
.sk figure{{margin:0;display:flex;flex-direction:column;gap:8px}}
.sk .fr{{display:block;width:100%;height:auto;border-radius:4px;box-shadow:0 14px 34px -22px rgba(79,1,163,.6)}}
.slot.done .slot-f{{border:0;padding:0;overflow:hidden}}
.slot.done img{{width:100%;height:100%;object-fit:cover;display:block}}
.zoom{{cursor:zoom-in;border:0;background:none;font:inherit}}
.reel{{position:relative;width:min(100%,760px);aspect-ratio:16/9;border-radius:6px;overflow:hidden;background:var(--midnight)}}
.reel img{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:0;animation:reel 18s infinite}}
.reel img:first-child{{opacity:1}}
@keyframes reel{{0%{{opacity:0}}3%{{opacity:1}}17%{{opacity:1}}20%{{opacity:0}}100%{{opacity:0}}}}
@media (prefers-reduced-motion:reduce){{.reel img{{animation:none}}}}
.lb{{position:fixed;inset:0;z-index:50;background:rgba(20,8,43,.88);display:grid;place-items:center;padding:24px;cursor:zoom-out}}
.lb img{{max-width:100%;max-height:100%;border-radius:4px;box-shadow:0 20px 60px rgba(0,0,0,.5)}}
.slot.done figcaption{{color:var(--electric);font-weight:500}}
.thumb img{{width:100%;height:100%;object-fit:cover;object-position:50% 30%;display:block}}
.sk figcaption{{font-size:13px;color:var(--muted)}}
.mx-row{{display:grid;grid-template-columns:220px 1fr;gap:20px;padding-block:18px;border-bottom:1px solid var(--line)}}
.mx-h{{display:flex;flex-direction:column;gap:4px}}
.mx-h b{{font-size:17px}}
.mx-h span{{font-size:14px;color:var(--muted)}}
.mx-h em{{font-style:normal;font-size:13px;color:var(--warn)}}
.mx-cells{{display:flex;gap:16px;align-items:flex-end;flex-wrap:wrap}}
[hidden]{{display:none!important}}
.slot{{margin:0;display:flex;flex-direction:column;gap:6px;max-width:100%}}
.slot-f{{width:100%;border:1.5px dashed var(--lilac);border-radius:6px;background:var(--paper);display:flex;flex-direction:column;justify-content:center;align-items:center;gap:4px;padding:8px;text-align:center}}
.slot-f .st{{font-size:12px;font-weight:700;color:var(--electric)}}
.slot-f .dim{{font-size:11px;color:var(--muted)}}
.slot figcaption{{color:var(--muted);font-size:12px}}
.prev{{width:100%;border-radius:10px;display:block}}
@media (max-width:680px){{.mx-row{{grid-template-columns:1fr}}}}
.scroll{{overflow-x:auto}}
table{{border-collapse:collapse;width:100%;min-width:560px;background:var(--paper);border:1px solid var(--line)}}
th,td{{text-align:left;padding:11px 14px;border-bottom:1px solid var(--line);font-size:15px}}
th{{font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:var(--muted)}}
.n{{text-align:right;font-variant-numeric:tabular-nums}}
tr.tot td{{font-weight:700}}
.dspill{{position:fixed;top:calc(12px + env(safe-area-inset-top,0px));right:12px;z-index:20;background:#fff;color:var(--primary);text-decoration:none;font-weight:500;font-size:13px;padding:8px 14px;border-radius:999px;box-shadow:0 4px 14px -4px rgba(32,0,76,.5)}}
@media (prefers-reduced-motion:reduce){{.card{{transition:none}}}}
</style>
<a class="dspill" href="{DS_URL}" target="_blank" rel="noopener">&larr; Design System</a>
<header class="mast"><div class="w">
  {lockup("lk", "#FFFFFF", "#FFFFFF")}
  <span class="label">Roku Ads Manager · Paid social, CTV and Figma reframes · Q4 2026</span>
  <h1>Roku <span>Deliverables Hub</span></h1>
  <p>Pick a channel, then open a job. Each card takes you to its frames, copy and notes.</p>
  <div class="tabs" role="tablist">{"".join(tabs)}</div>
</div></header>
<div class="w">{"".join(bars)}</div>
<main class="w">{"".join(index)}{"".join(views)}</main>
<script>
(function(){{
  var JOB_CH={{{",".join(f"'{j[1]}':'{j[0]}'" for j in JOBS)}}};
  var cur='{CHANNELS[0][0]}';
  function show(){{
    var h=(location.hash||'').slice(1), job=JOB_CH[h]?h:null;
    if(job) cur=JOB_CH[job];
    document.querySelectorAll('.tab').forEach(function(t){{t.setAttribute('aria-selected',String(t.dataset.go===cur));}});
    document.querySelectorAll('[data-ch]').forEach(function(el){{
      var v=el.dataset.view, on=el.dataset.ch===cur;
      if(v) on=on&&(job?v===job:v==='index');
      el.hidden=!on;
    }});
    document.querySelectorAll('.jobs a').forEach(function(a){{a.setAttribute('aria-current',String(a.getAttribute('href')==='#'+job));}});
    if(job) window.scrollTo(0,0);
  }}
  document.querySelectorAll('.tab').forEach(function(t){{t.addEventListener('click',function(){{cur=t.dataset.go; if(location.hash) history.pushState('',document.title,location.pathname+location.search); show();}});}});
  window.addEventListener('hashchange',show);
  var lb=document.createElement('div'); lb.className='lb'; lb.hidden=true; var lbi=document.createElement('img'); lb.appendChild(lbi); document.body.appendChild(lb);
  lb.addEventListener('click',function(){{lb.hidden=true;}});
  document.addEventListener('keydown',function(e){{if(e.key==='Escape') lb.hidden=true;}});
  document.querySelectorAll('.zoom').forEach(function(b){{b.addEventListener('click',function(){{var i=b.querySelector('img'); lbi.src=i.src; lbi.alt=i.alt; lb.hidden=false;}});}});
  show();
}})();
</script>
"""


if __name__ == "__main__":
    out = Path(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).parent / "deliverables-hub.html")
    out.write_text(build(), encoding="utf8")
    print(out, round(out.stat().st_size / 1024), "KB")
