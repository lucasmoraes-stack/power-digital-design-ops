# KAT26019 Top Items: brief

Brand: Katapult. Channel: PMAX + Google programmatic banners. Funnel: TOF. Triage: 2026-10-02.
Source: client brief PDF "KAT26019 - Top Items" (sent in chat 2026-10-02, not saved in the repo). Concept deck (Google Slides) not accessible from here, only the reference crop in the PDF.

## The ask

Hypothesis: a clear Cyber headline over an array of items educates people about lease-to-own.
Creative: Cyber Week deal headline + a knolling-style grid of the most popular lease-to-own items.

8 sizes x 2 iterations = 16 deliverables.

| Platform | Sizes |
|---|---|
| PMAX static | 1200x628 (1.91:1), 1200x1200 (1:1), 960x1200 (4:5) |
| Google programmatic static | 300x600, 320x50, 300x250, 160x600, 728x90 |

Testing variable: V1 static vs V2 animated (the animation swaps the images around in the grid).
V2 ships as a **3-scene storyboard** per size (house rule, every brand): S01 logo + grid, S02 grid swapped + headline, S03 end frame = the V1 static.

## Copy (client, verbatim, no edits)

- Headline: Your Whole Wish List, Lease-to-Own.
- Subhead: From couches to TVs to tires, lease-to-own the big stuff at thousands of retailers this Cyber Week.
- CTA: Shop Cyber Deals. Lease to Own.

No em/en dash in the copy. "Lease-to-Own" uses hyphens, which is fine.

## What each size carries

**Law (user, 2026-10-02): no copy is altered.** Whatever copy appears is verbatim. Nothing is added: no disclaimer, since the brief's copy has none.
Headline, subhead and CTA on every size except 728x90 and 320x50, which carry headline + CTA only (user decision, 2026-10-02). 160x600 and 300x250 got the subhead back in the client review (2026-10-05).
CTA: Katapult pink pill, white text, medium weight. Vertical formats: the grid runs from under the copy down to the CTA, with no dead whitespace. Grid edge columns sit flush with the side margins.

| Size | Grid |
|---|---|
| 1200x628 | 3x3 |
| 1200x1200 | 4x2 |
| 960x1200 | 3x2 |
| 300x600 | 2x3 |
| 160x600 | 2x3 |
| 300x250 | 2x3 |
| 728x90 | 3x1 |
| 320x50 | 1x1 |

## Safe zones

PMAX: 5% inset on every edge. Programmatic: 4 to 12px depending on size. Copy, logo, CTA and the grid sit fully inside.

## Grid items (cutouts in img/, 2026-10-02)

The file name is the slot and the content is what's actually in the photo: sofa.png = armchair, tv.png = curved monitor, tire.png = stacked tires, fridge.png = refrigerator, mattress.png = bed, laptop.png, washer.png = dishwasher, console.png = game controller, grill.png = gas grill.

## Client review round 2 (Ximena Gomez, Figma comments, applied 2026-10-05)

- Headline and subhead in one color: Katapult Dark Blue `#131540` (the headline was black). Subhead in **Regular** (was Bold). Regular isn't in the repo's font files; it's subset from the installed `AktivGrotesk-Regular.otf` into `fonts/aktiv-grotesk-400.woff` and injected by `build.py`.
- Subhead and CTA larger on every size that carries them (1x1 36/36, 4x5 34/34, 1.91:1 26/28, 300x600 15/17).
- 1200x1200: the grid now spans the full 1080px (it was capped at the 1000px text column, leaving 140px on the right vs 60px on the left).
- 1200x628: logo and copy travel as one block, vertically centered on the frame.
- 300x250 and 160x600: subhead added. 160x600 headline 20 to 24px; "Lease-to-Own." may only break after "to-".
- Cutout images now size to the visible product (no object-fit), so edge alignment holds when the HTML is imported into Figma.
- V2 storyboards and programmatic follow the same rules automatically.

## Proposal 2: knolling flat-lay (2026-10-07, 8 sizes V1 + V2, for review)

Feedback (direct from the client): lean into the knolling shot, not things floating on white. Neutral matte ground that lives in the brand colors (very light salmon or grey), gen AI or sourced images silhouetted so the concept lands.

- Eight products regenerated with AI (Figma `generate_image`, gpt-image model) as top-down shots on white: sofa, TV, tire, refrigerator, bed, laptop, washing machine, game console (grill generated too, cropped at the bottom, not used). Raw files in `img-knolling/raw/`.
- `cutout.py` silhouettes them and keeps each product's own contact shadow as semi-transparent black, so they sit on any ground: `img-knolling/{item}.png`.
- 1:1 built in `kn.css` / `kn.js` / `kn.html`: ground `#F6E6DE` with fine grain, two rows edge to edge across the safe width (couch, TV, tire on top), same copy and type sizes as round 2.
- `build_kn.py` injects it into the hub inside the KAT26019 view, above V1 (`#kn`). Re-run it after `build.py`, which rewrites that block.
- All 8 V1 sizes built on the same system (logo, type and CTA sizes from the approved V1). 8 products on PMAX and 300x600, 4 on 160x600 and 300x250, 3 on 728x90, the sofa alone on 320x50.
- Layout (fixed 2026-10-07 after products overlapped the copy in the hub viewer): logo, copy, product area and CTA are one browser-laid column inside each frame; the products fill the area's real size and re-fit on any reflow. Nothing is measured outside the frame.
- `export_kn.py` writes the standalone frames for Figma import: `04-deliverables/banners/2026-kat26019-top-items/html-knolling/V1` (8) and `/V2` (24) + `KAT26019-TopItems-Knolling-html.zip`. The ground is baked into a JPEG layer in these files, since Figma's HTML import can't read the CSS gradient + SVG grain.
- V2 animated storyboards, all 8 sizes (S01 logo + products, S02 swap + headline, S03 = V1). A product only trades places with one of a similar shape (wide / square-ish / tall), so the rows keep their proportions between scenes.

## Open

1. Item list: confirm with the client which items are "the most popular". The copy says couches and TVs, but the cutouts show an armchair and a monitor.
2. Cutouts: generate per `image-prompts.md`, or the client sends packshots.
3. The headline does not say "Cyber". The Cyber hook is in the subhead and the CTA.
4. Concept deck: share access to check the reference board.

## Files

- Generator: `build.py` (injects the Banners channel into the Katapult Deliverables Hub artifact).
- Fragment sources: `kb.css`, `kb.html`, `kb.js`.
- Exporter: `export.py` (headless Chrome, writes the 32 standalone HTMLs + zip in `04-deliverables/banners/2026-kat26019-top-items/`).
- Published: Katapult Deliverables Hub https://claude.ai/artifact/HTkyaVvtPH72dpT6RUNSrP, channel Banners (v11, 2026-10-05). Local copy of the published page: `04-deliverables/deliverables-hub.html`. Rebuild from a fresh read of the artifact, never from that copy.
