---
name: katapult-banners
description: Katapult banner and static-ad patterns approved by Lucas in Figma (KAT26019 Top Items knolling, KAT26020 Holiday Disaster, KAT26021 Flat Brand Type, KAT26022 Trusted), with measured sizes, colors per pattern, and where each job's code lives. Load for any new Katapult PMAX or programmatic banner, or when editing one of these jobs. Use together with banner-craft.
---

# Katapult banners

Source of truth: Figma "Progressive Global - LAB", page node `547:1720` (file `D8FpNuKI3uPGjCPqonIn3C`). Lucas reworked all four jobs there on 2026-10-13; the HTML in the Deliverables Hub was rebuilt to match frame by frame the same day. Start any new Katapult banner from the closest of these four patterns.

Every job ships 8 sizes: PMAX 1200x1200, 1200x628, 960x1200 and programmatic 300x600, 300x250, 160x600, 728x90, 320x50. Type is Aktiv Grotesk (embedded in the hub at 300/400/500/700; there is no SemiBold in the licensed family, so Figma "SemiBold" headlines render at 500).

## Colors as used in the approved Figma

| Use | Hex | Note |
|---|---|---|
| Dark Blue | `#131540` | matches guideline |
| Pink | `#ED5370` | matches guideline |
| "Light Blue" (lavender) | `#AFB3CC` | Figma style name says Light Blue; guideline digest says `#9EB5C0` |
| "Blue" | `#364488` | guideline says `#365488` |
| "Cream" | `#EAD0B6` | guideline says `#D4A574` |

The three off-guideline values are what Lucas's Figma library uses and what shipped. Until he confirms which side is right, use the Figma values for banners and flag the conflict rather than silently "correcting" either side.

## Pattern 1: Knolling flat-lay (KAT26019 Top Items)

Paper-texture ground (`img-knolling/ground.jpg`), copy top left (logo, headline, subhead, CTA), products packed in the lower ~55%. 1:1: headline 95px / 90 line height, subhead 36px, 13 product layers in the bottom 540px. 11 products at true scale: fridge, washer, bed, couch, TV, tire, laptop, console, nightstand, vacuum, necklace. Laptop/TV/vacuum rotate 90° to fill slots. 320x50: headline on one line on top, small CTA under it, logo bottom center, 7 tiny products on the right. V2 animates as a build-up (copy first, big pieces first, last scene = V1).

## Pattern 2: Photo + highlight-bar headline (KAT26020 Holiday Disaster)

Full-bleed original (ungraded) photo of a comic mishap; no color band. Headline as two bars low on the photo: setup on Cream `#EAD0B6` with Dark Blue type, punchline Dark Blue bar with Pink type. Big Pink CTA pill under the bars, White logo top right (~18% of width), one-line White legal at the bottom. Black scrims for legibility (corner gradient ~39% behind logo, bottom gradient ~40 to 44% behind legal, or flat 10%). 1:1 headline 119px (V1) / 97px (V2), CTA 44px in a 90px pill, legal 17px. Narrow sizes: check the White logo's legibility on the actual crop (160x600 V2 living room failed and was fixed 2026-10-14). Leaderboards: Dark Blue ground, Pink logo left, bars left, photo as hard-edged block on the right (mirrored so the subject faces in), pill overlapping the photo edge.

## Pattern 3: Flat brand type (KAT26021 Cyber)

Type only. V1 Dark Blue ground: first sentence White with accent word in lavender `#AFB3CC`, second sentence Pink with accent word lavender. V2 Cream `#EAD0B6` ground: first sentence Blue `#364488`, accents Dark Blue, second sentence Pink, subhead Dark Blue. Logo Pink on both. 1:1: headline 151px Bold, breaks "The deals / won't wait. / And now you / don't have to.", subhead 63px Regular, CTA 45px Medium in a 577x87 pill, logo 270px wide at bottom right (52px from right, 63px from bottom). 300x600 and 160x600 are centered stacks; 728x90 and 320x50 CTAs wrap to two lines.

## Pattern 4: Proof badge (KAT26022 Trusted)

Dark Blue ground, centered Trustpilot card with a Cream offset plate. Option A: half-circle in a lighter navy behind the card, small review cards around it, all straight with one shared light blur (3px on 1:1). Option B: real lifestyle photo on top (library `laptop-woman-window-desk-06.jpg`, Adobe Stock 410115591), badge sitting on the photo seam. Headline 124px on 1:1, subhead `#AFB3CC`, CTA "See Why Shoppers Love Katapult" (no period). 1.91:1 splits into copy column left and visual right. Subhead dropped on 728x90 and 320x50.

## Where the code lives

`clients/katapult/03-work/banners/2026-kat260NN-<slug>/`: `kNN.css` (canvas + theme), `kNN.html` (hub section), `kNN.js` (per-size values taken from Figma), `build.py` (injects the job into the hub, idempotent), `export.py` (one standalone HTML per frame + zip). KAT26019 knolling uses `kn.*`, `build_kn.py`, `export_kn.py`. Workflow for syncing Figma edits: see the `figma-banner-sync` skill.

Exports: `clients/katapult/04-deliverables/banners/<job>/html/V1|V2/` plus the zip. Hub: Katapult Deliverables Hub, https://claude.ai/code/artifact/2abbbef7-4ac3-4e9c-a431-7c37b8e05dcf.

## Open with Lucas (as of 2026-10-13)

- The three color conflicts above.
- KAT26020 728x90 V1: the Figma photo is stretched about 24% vertically; the HTML keeps true proportions.
- KAT26019: the bed is stretched 8 to 15% horizontally in three Figma frames; reproduced as is.
- KAT26021: subhead now ends with a period (Figma); `brief.md` still says none.
- KAT26019 V2 middle scenes for 300x250, 160x600, 728x90, 320x50 were built on the 300x600 pattern (Figma only had first and last frame).

## Organic social (monthly OS run), learned 2026-10-16

The approved organic look is Lucas's October finals in Figma (file D8FpNuKI3uPGjCPqonIn3C, page "kat os", node 598:7579), not the September v2 HTML:
- Headlines sentence case, Aktiv Grotesk Medium 500 (Figma SemiBold), one key word in Pink. On Cream or Pink grounds the accent word is White or Dark Blue (Pink on Cream fails contrast).
- Logo on the cover and the closing slide only. No CTA pill and no disclaimer on organic art.
- White cards with a solid offset plate (Dark Blue or Pink), line icons in Pink discs, product cutouts on White tiles or flat palette shapes.
- The Pink line that turns a rounded corner and continues as a row of dots is back, once per frame, behind the visual. Leave it out on Pink grounds.
- October's light Cream ground samples #EAD0B6 (shapes stay #D4A574); Blue ground #364488.
- Don't repeat a photo inside the same month; check across all builders before rendering.
- Chat bubbles: square tail corner with a curved wedge tail (~38x44px), or it reads as a glitch.
- Headless Chrome: screenshot paths must be absolute; CSS masks don't load from file:// (inline the logo SVG with currentColor).
- Phone-in-hand (T03): the hand photo lives inside its Pink panel, which crops it; the arm must leave the frame through an edge with skin touching the edge along its whole width. The source photo's own crop edge must sit outside the frame (raw cut otherwise; Lucas flagged it on Nov 01).
- Every frame needs one visual idea that fills it (October standard): no empty covers, no text floating under a photo (anchor it in a White card overlapping the photo), no products sliced by the frame edge (only shapes and bands bleed), diagrams centred and balanced with ~75px gaps. Don't reuse an October mechanic 1:1 in a later month.
- Poll/quiz Stories: never draw the options or a fake poll card. Leave one clean zone (about 880 x 760, centred, inside the 250/250 safe area) for Instagram's native sticker; options go in the post notes. Native poll/quiz stickers take up to 4 options.
- New month = plan grounds and layout families for the whole feed first (see 03-work/social/2026-11-organic/feed-plan.md): whole palette as grounds (Blue, Orange, light Cream, Surface, not only Dark Blue/Pink), feed neighbours never share ground or family, and check every frame and every photo against all earlier months before rendering (Lucas, 2026-10-16).
- Spacing scale and composition rules for organic frames: 03-work/social/2026-11-organic/spacing.md (logo 80 top, logo to headline 40, headline to body 20, body to visual 56, card padding 40/44, list gaps 28; cutouts centred on their shape at 70 to 80%; icon groups in one element with one primary). Reels ship as the edited MP4 plus the storyboard (one frame per beat + storyboard.md); Lucas decided 2026-10-16.
- Photos: only Image Library photos never used in earlier posts or banner jobs (Lucas, 2026-10-16). Check by image comparison against past finals (Figma raw images) and banner job images, not by eye; audit lives in 03-work/social/2026-11-organic/photo-audit.md. No photo twice in the same month.
- Figma hand-off: build/figma_export.py writes figma-import/ (one self-contained HTML per frame: CSS, fonts, images inlined, fixed page size, logo without clip-path; img/ with the photos; reels/ with storyboard PNGs + MP4).
