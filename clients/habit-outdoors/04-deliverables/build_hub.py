"""Build the Habit Outdoors Deliverables Hub (one self-contained HTML page, published as an Artifact).

Usage: python build_hub.py            -> writes deliverables-hub.html next to this file

Each campaign below points at a 03-work/email/<campaign>/ folder. Every email HTML is embedded with its
images; images are de-duplicated across all emails and re-encoded to WebP (lossy for JPEG and PNG
alike), so 10 emails fit well under the Artifact's 16 MB limit. Card thumbnails are cropped from the
680px renders (renders/<file>-680.png; run email-ops/tools/render.py first).

To add a campaign: append to CAMPAIGNS (newest first), render it, run this script, republish.
"""
from __future__ import annotations

import base64
import datetime as dt
import hashlib
import html
import io
import json
import re
import sys
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
BRAND = HERE.parent
sys.path.insert(0, str(ROOT / "email-ops" / "tools"))
import build_preview as bp  # noqa: E402  (parse_meta, SRC_RE, URL_RE, SKIP_PREFIXES)

WORK = BRAND / "03-work" / "email"
OUT = HERE / "deliverables-hub.html"
LOGO = BRAND / "01-brand" / "identity" / "logo" / "habit-logotype-white.svg"

CAMPAIGNS = [
    {
        "id": "november",
        "tab": "November",
        "folder": "2026-11-broadcasts",
        "label": "November 2026 broadcasts",
        "status": ("qa", "Round 6 · QA passed, ready for your review"),
        "idea": "Five one-off broadcasts from the client's November copy doc. The copy goes in exactly as the "
                "client wrote it, including the lines flagged below. Structure comes from seven Duck Camp "
                "reference emails; colour, type, buttons and footer come from the Habit email kit v0.5.",
        "counts": [("5", "emails"), ("3", "copy approved"), ("2", "copy needs edit"), ("6", "QA rounds"), ("12", "people photos")],
        "emails": [
            ("01-womens-cedar-branch.html", "2026-11-05", "Women's Cedar Branch Bib + Parka", "approved",
             "People hero (family in Realtree), big products crossing the torn edges, closing photo bleeding off the edge"),
            ("02-gift-guide-1.html", "2026-11-10", "Gift Guide #1, top apparel", "edit",
             "Overlapping five-photo collage crossing the tear, six rows of large cut-outs on Patriot (no cards), cap in front of a boat photo"),
            ("03-buck-hollow-2.html", "2026-11-19", "Buck Hollow 2.0 Jacket & Pant", "approved",
             "Full-bleed photo hero with the title on it, system shot with callouts, three-hunters strip, jacket and pant as a staggered pair"),
            ("04-heavyweight-flannel.html", "2026-11-27", "Heavyweight Soft Flannel", "approved",
             "Single-product story: barn photo, detail mosaic, both colourways large and overlapping on Patriot"),
            ("05-gift-guide-2.html", "2026-11-30", "Gift Guide #2, gifts by price", "edit",
             "One layout per price tier with torn tier labels: open 2x2 grid, lead product plus group and price list, matching set plus highlight"),
        ],
        "sections": [
            ("For the client", "Placed as written, not fixed", [
                "Nov 30: the hero button says “Shop Flannel” in a gift guide.",
                "Nov 30: Men's Outdoor Hybrid Hoodie sits under “Under $30” but costs $49.99 at the store.",
                "Nov 30: Men's Waterproof Insulated Bib is on sale at $111.98 (was $159.99). If the sale ends before Nov 30 it leaves the “Under $120” tier.",
                "Nov 27: the subheadline “Rain-Factor tech meets soft tricot” repeats the Buck Hollow line and does not describe a cotton flannel.",
                "Nov 10: “inbox..” has a double period; the doc title says top 5 but lists 6 products.",
                "Nov 10 and Nov 30 are still marked Needs Edit in the client's doc, so their copy can change.",
            ]),
            ("Your call", "Decisions before send", [
                "Rounds 4 to 6 answer your reviews: people in every email (12 photos, none repeated), large products crossing the torn edges, clean cut-outs, and every photo-to-band transition is now a tear (rule R8, no gradients).",
                "All five are now under the 800 KB image guide (Nov 30: 787 KB desktop).",
                "Nov 10: the angler on the boat photo (cap row) looks like the same model as one collage photo, same shoot. Keep, or swap for a bank photo without him.",
                "Nov 19 reuses the three-hunters sunrise photo that opened the Oct 6 email. Swap it if the library brings a new one tomorrow.",
                "Kit v0.5 and v0.6 (E35 to E41, rules R1 to R15) plus the round 4 variants (product crossing the tear, product rising out of a card, photo hero bleeding off the edge) need approval before anything goes to Omnisend.",
                "Provisional photos (crop-sent-*, orig-*) and the store model shots (Nov 10 cap, Nov 19 jacket) still need release.",
            ]),
            ("Before send", "Checklist", [
                "Replace URL placeholders such as {{WOMENS_URL}}, {{GIFT_GUIDE_URL}} and {{BUCK_HOLLOW_URL}}.",
                "Confirm the Omnisend footer adds address and unsubscribe (CAN-SPAM) in a test send.",
                "Re-check every price on its send date.",
                "Test in Outlook desktop and the Gmail app (iOS, Android), light and dark.",
            ]),
        ],
        "files": "clients/habit-outdoors/03-work/email/2026-11-broadcasts/ · brief.md, qa-r1.md, qa-r2.md, qa-r4.md, copy-source.md",
    },
    {
        "id": "october",
        "tab": "October",
        "folder": "2026-10-broadcasts",
        "label": "October 2026 broadcasts",
        "status": ("review", "Round 2, rebuilt from your revisions"),
        "idea": "Five broadcasts rebuilt from your revised designs (rev-oct-01 to 05). The kit v0.5 decisions "
                "come from this round: white button text, Prompt body, the two-voice headline and the product box.",
        "counts": [("5", "emails"), ("5", "copy approved"), ("2", "build rounds")],
        "emails": [
            ("01-cedar-branch-bibs.html", "2026-10-06", "Men's Cedar Branch Insulated Bibs", "approved",
             "Label-box headline on a full-bleed photo, one customer review, photo closing band"),
            ("02-youth-season.html", "2026-10-09", "Youth season", "approved",
             "Three framed product cards on colour panels, tilted photo closing"),
            ("03-heavy-weight-hoodie.html", "2026-10-13", "Heavy Weight Full Zip Hoodie", "approved",
             "One panel per colour on camo paper, image and text alternating"),
            ("04-crater-valley.html", "2026-10-22", "Crater Valley layers", "approved",
             "Left-aligned hero with model, framed card rows, sunset photo band"),
            ("05-shadow-series.html", "2026-10-29", "Shadow Series late season", "approved",
             "Photo hero, 2x2 attribute cards, product checkerboard on topo gradient"),
        ],
        "sections": [
            ("Notes", "From the round 2 review", [
                "Button text is white, as in your revisions: 2.97:1 contrast, below AA, recorded as your exception.",
                "Address and unsubscribe are not in the HTML: the Omnisend footer has to add both (CAN-SPAM).",
                "Not copied from the revisions: “Youth Cedar Branch” on card 1 of Oct 22 (it is the Crater Valley Performance Hoodie) and “Insulated Bib” on card 3 of Oct 29.",
                "Provisional 1x photos cropped from the revisions (Oct 13 hero, Oct 6 archer, Oct 22 sunset, Oct 9 boy) need the originals. Oct 29 keeps the earlier hero photo.",
                "Oct 6 has one review only; Oct 22 drops the GIF and has five buttons, as in the revisions.",
                "Rust #774727 and slate #4F5C5F panels from Oct 9 are now kit v0.5 colours.",
            ]),
            ("Your call", "Open", [
                "Oct 22: 731 KB of images on desktop, 1,027 KB counting the mobile versions Gmail downloads. Decide whether the card photos are unified.",
            ]),
        ],
        "files": "clients/habit-outdoors/03-work/email/2026-10-broadcasts/ · brief.md, revision-r2.md, qa-r2.md",
    },
]


class ImageStore:
    """Replaces every local image reference with hubimg:<id>; each file is encoded once."""

    def __init__(self) -> None:
        self.by_path: dict[Path, str] = {}
        self.data: dict[str, str] = {}
        self.missing: list[str] = []
        self.raw = 0

    def ref(self, ref: str, base: Path) -> str | None:
        clean = html.unescape(ref.strip())
        if not clean or clean.lower().startswith(bp.SKIP_PREFIXES):
            return None
        from urllib.parse import unquote
        path = (base / unquote(clean.split("#", 1)[0].split("?", 1)[0])).resolve()
        if path in self.by_path:
            return "hubimg:" + self.by_path[path]
        if not path.is_file():
            self.missing.append(f"{ref} ({base.name})")
            return None
        raw = path.read_bytes()
        self.raw += len(raw)
        uri = encode(path, raw)
        key = hashlib.sha1(uri.encode()).hexdigest()[:10]
        self.by_path[path] = key
        self.data[key] = uri
        return "hubimg:" + key

    def inline(self, source: str, base: Path) -> str:
        def attr(m: re.Match) -> str:
            r = self.ref(m.group(3), base)
            return f"{m.group(1)}{m.group(2)}{r}{m.group(2)}" if r else m.group(0)

        def css(m: re.Match) -> str:
            r = self.ref(m.group(3), base)
            return f"{m.group(1)}'{r}'{m.group(4)}" if r else m.group(0)

        return bp.URL_RE.sub(css, bp.SRC_RE.sub(attr, source))


def encode(path: Path, raw: bytes) -> str:
    ext = path.suffix.lower()
    if ext in (".png", ".jpg", ".jpeg"):
        im = Image.open(io.BytesIO(raw))
        im.load()
        alpha = im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info)
        im = im.convert("RGBA" if alpha else "RGB")
        buf = io.BytesIO()
        im.save(buf, "WEBP", quality=82 if alpha else 78, method=6)
        if buf.tell() < len(raw):
            return "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode()
    mime = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".gif": "image/gif",
            ".svg": "image/svg+xml"}.get(ext, "application/octet-stream")
    return f"data:{mime};base64," + base64.b64encode(raw).decode()


def thumb(render: Path) -> str:
    im = Image.open(render).convert("RGB")
    w = im.width
    im = im.crop((0, 0, w, min(im.height, int(w * 1.25))))
    im = im.resize((360, int(360 * im.height / w)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "WEBP", quality=72, method=6)
    return "data:image/webp;base64," + base64.b64encode(buf.getvalue()).decode()


def nice_date(iso: str) -> str:
    d = dt.date.fromisoformat(iso)
    return d.strftime("%a, %b ") + str(d.day)


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def build() -> None:
    store = ImageStore()
    camps = []
    total_emails = 0
    for c in CAMPAIGNS:
        folder = WORK / c["folder"]
        emails = []
        for i, (fname, date, title, copy_status, structure) in enumerate(c["emails"], 1):
            src = (folder / fname).read_text(encoding="utf-8")
            meta = bp.parse_meta(src)
            render = folder / "renders" / (Path(fname).stem + "-680.png")
            emails.append({
                "n": f"{i:02d}", "file": fname, "date": date, "dateLabel": nice_date(date), "title": title,
                "copy": copy_status, "structure": structure,
                "subject": meta.get("Subject", ""), "preheader": meta.get("Preheader", ""),
                "thumb": thumb(render) if render.is_file() else "",
                "html": store.inline(src, folder),
            })
        total_emails += len(emails)
        d0, d1 = emails[0]["date"], emails[-1]["date"]
        camps.append({**{k: c[k] for k in ("id", "tab", "label", "idea", "counts", "files")},
                      "status": list(c["status"]), "sections": [list(s) for s in c["sections"]],
                      "range": f"{nice_date(d0)} to {nice_date(d1)}", "emails": emails})

    logo = "data:image/svg+xml;base64," + base64.b64encode(LOGO.read_bytes()).decode()
    page = PAGE.replace("__LOGO__", logo)
    page = page.replace("__TOTAL__", str(total_emails)).replace("__NCAMP__", str(len(camps)))
    page = page.replace("__DATA__", json.dumps(camps, ensure_ascii=False).replace("</", "<\/"))
    page = page.replace("__IMG__", json.dumps(store.data))
    page = page.replace("__UPDATED__", dt.date.today().isoformat())
    OUT.write_text(page, encoding="utf-8")
    size = OUT.stat().st_size
    print(f"{OUT} · {size / 1e6:.2f} MB · {len(store.data)} unique images "
          f"(raw {store.raw / 1e6:.1f} MB) · {total_emails} emails")
    if store.missing:
        print("missing:", *store.missing, sep="\n  ")
    if size > 15.5e6:
        sys.exit("too big for an Artifact (16 MB)")


PAGE = r"""<title>Habit Outdoors Deliverables Hub</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@900&family=Prompt:wght@400;500;700;800&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
/* Layout: Tap Shoe masthead with the kit's two-voice headline, campaign tabs, then per campaign a
   briefing head, a card grid of its emails, and one viewer (desktop + mobile) for the open email. */
:root{
  --tapshoe:#2A2B2D; --orange:#FF6400; --paper:#E2DDD9; --aluminum:#A39A8C; --brown:#483F39; --patriot:#202944;
  --bg:#EFECE9; --panel:#FFFFFF; --panel-2:#F6F4F1; --ink:#2A2B2D; --ink-2:#5C5249; --rule:#DCD6CF; --rule-strong:#B9B0A5;
  --mast:#2A2B2D; --mast-ink:#FFFFFF; --mast-2:#CFC8BF; --mast-rule:rgba(207,200,191,.28);
  --ok-bg:#E4E8D8; --ok-ink:#3F4A1F; --warn-bg:#FBE3C9; --warn-ink:#7A3A00; --qa-bg:#DDE1EE; --qa-ink:#202944;
  --frame:#E6E1DB; --focus:#FF6400;
  --f-serif:"Playfair Display",Georgia,"Times New Roman",serif;
  --f-sans:"Prompt",Helvetica,Arial,sans-serif;
  --f-mono:"IBM Plex Mono",ui-monospace,Menlo,Consolas,monospace;
  --gutter:clamp(16px,4vw,40px);
  color-scheme:light;
}
@media (prefers-color-scheme: dark){
  :root:not([data-theme="light"]){
    --bg:#1B1C1E; --panel:#25262A; --panel-2:#2D2E33; --ink:#F1EEEB; --ink-2:#C2BAB0; --rule:#3A3B40; --rule-strong:#55565C;
    --mast:#121315; --mast-rule:rgba(207,200,191,.18);
    --ok-bg:#2F3524; --ok-ink:#D3DDB4; --warn-bg:#3E2A16; --warn-ink:#FFC48C; --qa-bg:#262C42; --qa-ink:#C9D1F0;
    --frame:#151618; color-scheme:dark;
  }
}
:root[data-theme="dark"]{
  --bg:#1B1C1E; --panel:#25262A; --panel-2:#2D2E33; --ink:#F1EEEB; --ink-2:#C2BAB0; --rule:#3A3B40; --rule-strong:#55565C;
  --mast:#121315; --mast-rule:rgba(207,200,191,.18);
  --ok-bg:#2F3524; --ok-ink:#D3DDB4; --warn-bg:#3E2A16; --warn-ink:#FFC48C; --qa-bg:#262C42; --qa-ink:#C9D1F0;
  --frame:#151618; color-scheme:dark;
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font:400 15px/1.55 var(--f-sans);-webkit-font-smoothing:antialiased}
h1,h2,h3{margin:0;text-wrap:balance;line-height:1.05}
p{margin:0}
.wrap{max-width:1320px;margin-inline:auto;padding-inline:var(--gutter)}
.eyebrow{font:700 12px/1.3 var(--f-sans);letter-spacing:.14em;text-transform:uppercase;color:var(--ink-2)}
.mono{font-family:var(--f-mono);font-size:12.5px}
button{font:inherit}
:focus-visible{outline:2px solid var(--focus);outline-offset:2px}

/* masthead */
.mast{background:var(--mast);color:var(--mast-ink)}
.mast .wrap{padding-block:34px 0;display:grid;gap:18px}
.mast-top{display:flex;align-items:center;justify-content:space-between;gap:16px;flex-wrap:wrap}
.mast-top img{height:30px;width:auto;display:block}
.mast-top .eyebrow{color:var(--mast-2)}
.mast h1{display:grid;gap:4px}
.mast h1 .sans{font:800 clamp(18px,2.4vw,26px)/1 var(--f-sans);letter-spacing:.06em;text-transform:uppercase;color:var(--mast-2)}
.mast h1 .serif{font:900 clamp(44px,7.4vw,92px)/.92 var(--f-serif);text-transform:uppercase;letter-spacing:-.005em}
.mast h1 .serif em{font-style:normal;color:var(--orange)}
.lede{max-width:62ch;color:var(--mast-2);font-size:16px}
.pills{display:flex;flex-wrap:wrap;gap:8px 10px;list-style:none;padding:0;margin:0}
.pills li{font-size:13.5px;font-weight:500;border:1px solid var(--rule-strong);border-radius:999px;padding:3px 12px;color:var(--ink-2)}
.pills li b{color:var(--ink);font-weight:800;font-variant-numeric:tabular-nums}
.mast .pills li{border-color:var(--mast-rule);color:var(--mast-2)}
.mast .pills li b{color:var(--mast-ink)}
.tabs{display:flex;flex-wrap:wrap;gap:8px 10px;padding-block:22px 22px;border-top:1px solid var(--mast-rule);margin-top:8px}
.tab{color:var(--mast-2);background:transparent;border:1px solid var(--mast-rule);border-radius:999px;padding:8px 18px;cursor:pointer;display:inline-flex;gap:10px;align-items:baseline;font-weight:800;font-size:14px;letter-spacing:.06em;text-transform:uppercase}
.tab small{font:500 12px var(--f-sans);letter-spacing:0;text-transform:none;opacity:.85}
.tab:hover{border-color:var(--orange);color:var(--mast-ink)}
.tab[aria-selected="true"]{background:var(--orange);border-color:var(--orange);color:var(--tapshoe)}
.theme-btn{color:var(--mast-2);background:transparent;border:1px solid var(--mast-rule);border-radius:999px;padding:5px 12px;font-size:12.5px;cursor:pointer}
.theme-btn:hover{color:var(--mast-ink)}
.mast-links{display:flex;gap:8px;flex-wrap:wrap}
a.theme-btn{text-decoration:none}

/* campaign head */
.camp{padding-block:40px 72px;display:grid;gap:34px}
.camp-head{display:grid;gap:16px;grid-template-columns:minmax(0,1.5fr) minmax(0,1fr);align-items:start}
.camp-head .intro{display:grid;gap:14px}
.camp-head h2{display:grid;gap:2px}
.camp-head h2 .sans{font:800 clamp(16px,1.8vw,20px)/1.1 var(--f-sans);letter-spacing:.08em;text-transform:uppercase;color:var(--ink-2)}
.camp-head h2 .serif{font:900 clamp(38px,5vw,64px)/.95 var(--f-serif);text-transform:uppercase}
.camp-head .idea{max-width:64ch;font-size:16px}
.state{display:inline-flex;align-items:center;gap:8px;justify-self:start;font-weight:700;font-size:13px;border-radius:999px;padding:4px 12px 4px 10px}
.state::before{content:"";width:8px;height:8px;border-radius:50%;background:currentColor}
.state.qa{background:var(--qa-bg);color:var(--qa-ink)}
.state.review{background:var(--warn-bg);color:var(--warn-ink)}
.how{background:var(--panel);border:1px solid var(--rule);border-radius:12px;padding:18px 20px;display:grid;gap:10px;font-size:14px}
.how h3{font:800 13px/1.2 var(--f-sans);letter-spacing:.1em;text-transform:uppercase}
.how ol{margin:0;padding-left:20px;display:grid;gap:6px;color:var(--ink-2)}
.how ol b{color:var(--ink);font-weight:500}

/* email cards */
.grid{display:grid;gap:16px;grid-template-columns:repeat(auto-fill,minmax(min(100%,220px),1fr))}
.card{display:flex;flex-direction:column;text-align:left;background:var(--panel);color:inherit;border:1px solid var(--rule);border-radius:12px;overflow:hidden;padding:0;cursor:pointer;transition:border-color .15s,transform .15s,box-shadow .15s}
.card:hover{border-color:var(--orange);transform:translateY(-2px);box-shadow:0 10px 22px rgba(42,43,45,.14)}
.card[aria-current="true"]{border-color:var(--orange);box-shadow:0 0 0 2px var(--orange)}
.thumb{aspect-ratio:4/5;background:var(--tapshoe);overflow:hidden;position:relative}
.thumb img{width:100%;height:100%;object-fit:cover;object-position:top;display:block}
.thumb .n{position:absolute;top:10px;left:10px;font:800 12px/1 var(--f-sans);letter-spacing:.08em;background:var(--orange);color:var(--tapshoe);border-radius:4px;padding:5px 7px}
.card-body{padding:12px 14px 14px;display:flex;flex-direction:column;gap:6px;flex:1}
.date{font:500 12.5px var(--f-mono);color:var(--ink-2);font-variant-numeric:tabular-nums}
.card-title{font:700 16px/1.2 var(--f-sans);margin:0}
.subj{font-size:13.5px;color:var(--ink-2)}
.card-foot{display:flex;align-items:center;justify-content:space-between;gap:8px;margin-top:auto;padding-top:6px}
.chip{font-size:11.5px;font-weight:700;letter-spacing:.04em;border-radius:999px;padding:2px 9px}
.chip.approved{background:var(--ok-bg);color:var(--ok-ink)}
.chip.edit{background:var(--warn-bg);color:var(--warn-ink)}
.go{font-size:13px;font-weight:700}
.card:hover .go,.card[aria-current="true"] .go{color:var(--orange)}

/* viewer */
.viewer{background:var(--panel);border:1px solid var(--rule);border-radius:14px;padding:22px clamp(16px,2.4vw,28px) 28px;display:grid;gap:20px;scroll-margin-top:16px}
.viewer-head{display:flex;flex-wrap:wrap;justify-content:space-between;align-items:flex-start;gap:12px 24px}
.viewer-head h3{font:900 clamp(26px,3vw,36px)/1 var(--f-serif);text-transform:uppercase}
.viewer-nav{display:flex;gap:8px;flex-wrap:wrap}
.btn{border:1px solid var(--rule-strong);background:var(--panel);color:var(--ink);border-radius:999px;padding:6px 14px;font-size:13px;font-weight:500;cursor:pointer}
.btn:hover{border-color:var(--orange)}
.btn[aria-pressed="true"]{background:var(--tapshoe);color:#fff;border-color:var(--tapshoe)}
.meta{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,240px),1fr));gap:12px 26px;margin:0}
.meta div{display:flex;flex-direction:column;gap:3px;padding-top:9px;border-top:3px solid var(--rule)}
.meta div:first-child{border-top-color:var(--orange)}
.meta dt{font:700 11.5px var(--f-sans);letter-spacing:.09em;text-transform:uppercase;color:var(--ink-2)}
.meta dd{margin:0;font-size:15px;font-weight:500;line-height:1.35;overflow-wrap:anywhere}
.meta .count{font:400 12px var(--f-mono);color:var(--ink-2);margin-left:6px}
.views{display:flex;flex-wrap:wrap;gap:24px;align-items:flex-start}
.view{min-width:0;max-width:100%;display:grid;gap:8px}
.view h4{margin:0;font:500 11.5px var(--f-mono);text-transform:uppercase;letter-spacing:.08em;color:var(--ink-2)}
.scroller{overflow-x:auto;max-width:100%;border:1px solid var(--rule);border-radius:10px;background:var(--frame)}
.scroller iframe{display:block;border:0;height:900px;background:#EFECE9;color-scheme:light}
.email-dark .scroller iframe{color-scheme:dark;background:#1E1F21}

/* notes */
.notes{display:grid;gap:16px;grid-template-columns:repeat(auto-fit,minmax(min(100%,320px),1fr))}
.note{border-top:3px solid var(--tapshoe);padding-top:12px;display:grid;gap:8px;align-content:start}
.note:first-child{border-top-color:var(--orange)}
.note h3{font:800 14px/1.2 var(--f-sans);letter-spacing:.1em;text-transform:uppercase}
.note .eyebrow{font-size:11px;letter-spacing:.1em}
.note ul{margin:0;padding-left:18px;display:grid;gap:7px;font-size:14.5px}
.files{font-size:13.5px;color:var(--ink-2)}
.files code{font-family:var(--f-mono);font-size:12.5px;background:var(--panel-2);border-radius:4px;padding:1px 5px}
footer{border-top:1px solid var(--rule);padding-block:20px 40px;color:var(--ink-2);font-size:13px}
[hidden]{display:none!important}

@media (max-width:860px){ .camp-head{grid-template-columns:1fr} }
@media (prefers-reduced-motion:reduce){ .card{transition:none} .card:hover{transform:none} }
</style>

<header class="mast">
  <div class="wrap">
    <div class="mast-top">
      <img src="__LOGO__" alt="Habit Outdoors">
      <span class="eyebrow">Email broadcasts · updated __UPDATED__</span>
      <span class="mast-links"><a class="theme-btn" href="https://claude.ai/code/artifact/f33018ee-a734-4183-83d0-79d046c9c60d" target="_blank" rel="noopener">← Design System</a>
      <a class="theme-btn" href="https://claude.ai/code/artifact/4006b37f-7efb-4d33-9d00-99c119d08a88" target="_blank" rel="noopener">Image Library →</a>
      <button class="theme-btn" id="theme-btn" type="button">Switch page theme</button></span>
    </div>
    <h1><span class="sans">Email campaigns</span><span class="serif">Deliverables <em>Hub</em></span></h1>
    <p class="lede">Every email campaign in one place. Pick a month, open an email, and see it at desktop and phone width with its subject line, preheader and open points.</p>
    <ul class="pills"><li><b>__NCAMP__</b> campaigns</li><li><b>__TOTAL__</b> emails</li><li>Omnisend · 600px HTML · kit v0.6</li></ul>
    <nav class="tabs" role="tablist" aria-label="Campaigns" id="tabs"></nav>
  </div>
</header>

<main id="app"></main>
<footer><div class="wrap">Page theme does not change the emails; use “Email dark mode” in the viewer. Left and right arrow keys move between emails. Built by <code class="mono">04-deliverables/build_hub.py</code>.</div></footer>

<script type="application/json" id="hub-data">__DATA__</script>
<script type="application/json" id="hub-img">__IMG__</script>
<script>
(function(){
  const CAMPS = JSON.parse(document.getElementById('hub-data').textContent);
  const IMG = JSON.parse(document.getElementById('hub-img').textContent);
  const app = document.getElementById('app'), tabs = document.getElementById('tabs');
  const esc = s => String(s).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
  const COPY = {approved:'Copy approved', edit:'Copy needs edit'};
  let state = {camp: CAMPS[0].id, email: CAMPS[0].emails[0].n, dark: false};

  try { const t = localStorage.getItem('habit-hub-theme'); if (t) document.documentElement.dataset.theme = t; } catch(e) {}
  document.getElementById('theme-btn').addEventListener('click', () => {
    const cur = document.documentElement.dataset.theme || (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    const next = cur === 'dark' ? 'light' : 'dark';
    document.documentElement.dataset.theme = next;
    try { localStorage.setItem('habit-hub-theme', next); } catch(e) {}
  });

  tabs.innerHTML = CAMPS.map(c => `<button class="tab" role="tab" type="button" data-camp="${c.id}" aria-selected="false">${esc(c.tab)} <small>${c.emails.length} emails · ${esc(c.range)}</small></button>`).join('');
  tabs.addEventListener('click', e => { const b = e.target.closest('.tab'); if (b) go(b.dataset.camp, null, true); });

  function emailHtml(e){ return e.html.replace(/hubimg:([0-9a-f]{10})/g, (m, k) => IMG[k] || m); }

  function renderCamp(c){
    const cards = c.emails.map(e => `
      <button class="card" type="button" data-n="${e.n}" aria-label="Open ${esc(e.dateLabel)}, ${esc(e.title)}">
        <span class="thumb">${e.thumb ? `<img src="${e.thumb}" alt="" loading="lazy">` : ''}<span class="n">${e.n}</span></span>
        <span class="card-body">
          <span class="date">${esc(e.dateLabel)}</span>
          <span class="card-title">${esc(e.title)}</span>
          <span class="subj">${esc(e.subject)}</span>
          <span class="card-foot"><span class="chip ${e.copy}">${COPY[e.copy]}</span><span class="go">Open →</span></span>
        </span>
      </button>`).join('');
    const notes = c.sections.map(([h, sub, items]) => `
      <section class="note"><span class="eyebrow">${esc(sub)}</span><h3>${esc(h)}</h3><ul>${items.map(i => `<li>${esc(i)}</li>`).join('')}</ul></section>`).join('');
    app.innerHTML = `
      <div class="wrap camp">
        <div class="camp-head">
          <div class="intro">
            <span class="state ${c.status[0]}">${esc(c.status[1])}</span>
            <h2><span class="sans">${esc(c.range)}</span><span class="serif">${esc(c.label)}</span></h2>
            <p class="idea">${esc(c.idea)}</p>
            <ul class="pills">${c.counts.map(([n, t]) => `<li><b>${esc(n)}</b> ${esc(t)}</li>`).join('')}</ul>
          </div>
          <aside class="how" aria-label="How to review">
            <h3>How to review</h3>
            <ol>
              <li><b>Open an email</b> from the cards below. It loads in the viewer at 640px and 375px.</li>
              <li><b>Read the strip above it</b>: send date, subject line, preheader and the structure used.</li>
              <li><b>Check both themes</b> with “Email dark mode”.</li>
              <li><b>Go through the notes</b> at the bottom: what goes back to the client, what is your call, what to do before send.</li>
            </ol>
          </aside>
        </div>
        <div class="grid" id="cards">${cards}</div>
        <section class="viewer" id="viewer" aria-live="polite"></section>
        <div class="notes">${notes}</div>
        <p class="files">Working files: <code>${esc(c.files)}</code></p>
      </div>`;
    app.querySelector('#cards').addEventListener('click', e => { const b = e.target.closest('.card'); if (b) go(c.id, b.dataset.n, true, true); });
  }

  function renderViewer(c, e){
    const i = c.emails.indexOf(e);
    const prev = c.emails[i-1], next = c.emails[i+1];
    const v = app.querySelector('#viewer');
    v.className = 'viewer' + (state.dark ? ' email-dark' : '');
    v.innerHTML = `
      <div class="viewer-head">
        <div><span class="eyebrow">${esc(e.n)} · ${esc(e.dateLabel)}</span><h3>${esc(e.title)}</h3></div>
        <div class="viewer-nav">
          <button class="btn" type="button" data-nav="prev" ${prev ? '' : 'disabled'}>← Previous</button>
          <button class="btn" type="button" data-nav="next" ${next ? '' : 'disabled'}>Next →</button>
          <button class="btn" type="button" id="dark-btn" aria-pressed="${state.dark}">Email dark mode</button>
        </div>
      </div>
      <dl class="meta">
        <div><dt>Subject line</dt><dd>${esc(e.subject)}<span class="count">${[...e.subject].length} chars</span></dd></div>
        <div><dt>Preheader</dt><dd>${esc(e.preheader)}</dd></div>
        <div><dt>Client copy</dt><dd>${COPY[e.copy]}</dd></div>
        <div><dt>Structure</dt><dd>${esc(e.structure)}</dd></div>
        <div><dt>File</dt><dd class="mono">${esc(e.file)}</dd></div>
      </dl>
      <div class="views">
        <div class="view"><h4>Desktop · 640px</h4><div class="scroller"><iframe title="${esc(e.title)}, desktop" width="640" style="width:640px"></iframe></div></div>
        <div class="view"><h4>Phone · 375px</h4><div class="scroller"><iframe title="${esc(e.title)}, phone" width="375" style="width:375px"></iframe></div></div>
      </div>`;
    const doc = emailHtml(e);
    v.querySelectorAll('iframe').forEach(f => {
      f.addEventListener('load', () => fit(f));
      f.srcdoc = doc;
    });
    v.querySelector('[data-nav="prev"]').addEventListener('click', () => prev && go(c.id, prev.n, true));
    v.querySelector('[data-nav="next"]').addEventListener('click', () => next && go(c.id, next.n, true));
    v.querySelector('#dark-btn').addEventListener('click', () => { state.dark = !state.dark; renderViewer(c, e); });
    app.querySelectorAll('.card').forEach(b => b.setAttribute('aria-current', b.dataset.n === e.n ? 'true' : 'false'));
  }

  function fit(f){
    try {
      const d = f.contentDocument; if (!d) return;
      const set = () => { f.style.height = Math.max(400, d.documentElement.scrollHeight) + 'px'; };
      set();
      if (d.fonts) d.fonts.ready.then(set);
      setTimeout(set, 800);
      new ResizeObserver(set).observe(d.body);
    } catch(err) {}
  }

  function go(campId, n, push, scroll){
    const c = CAMPS.find(x => x.id === campId) || CAMPS[0];
    const changed = c.id !== state.camp || !app.querySelector('#cards');
    state.camp = c.id;
    const e = c.emails.find(x => x.n === n) || c.emails[0];
    state.email = e.n;
    tabs.querySelectorAll('.tab').forEach(b => b.setAttribute('aria-selected', b.dataset.camp === c.id ? 'true' : 'false'));
    if (changed) renderCamp(c);
    renderViewer(c, e);
    const h = `#${c.id}-${e.n}`;
    if (push && location.hash !== h) history.replaceState(null, '', h);
    if (scroll) app.querySelector('#viewer').scrollIntoView({behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'auto' : 'smooth', block: 'start'});
  }

  document.addEventListener('keydown', ev => {
    if (ev.target.closest && ev.target.closest('input,textarea')) return;
    if (ev.key !== 'ArrowLeft' && ev.key !== 'ArrowRight') return;
    const c = CAMPS.find(x => x.id === state.camp); const i = c.emails.findIndex(x => x.n === state.email);
    const t = c.emails[i + (ev.key === 'ArrowRight' ? 1 : -1)]; if (t) go(c.id, t.n, true);
  });

  const m = location.hash.match(/^#([a-z]+)-(\d\d)$/);
  go(m ? m[1] : CAMPS[0].id, m ? m[2] : null, false);
})();
</script>
"""

if __name__ == "__main__":
    build()
