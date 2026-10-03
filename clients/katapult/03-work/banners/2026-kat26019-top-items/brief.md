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
Headline, subhead and CTA on every size except 728x90, 320x50, 160x600 and 300x250, which carry headline + CTA only (user decision, 2026-10-02). On 160x600 the CTA sits right under the headline.
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

## Open

1. Item list: confirm with the client which items are "the most popular". The copy says couches and TVs, but the cutouts show an armchair and a monitor.
2. Cutouts: generate per `image-prompts.md`, or the client sends packshots.
3. The headline does not say "Cyber". The Cyber hook is in the subhead and the CTA.
4. Concept deck: share access to check the reference board.

## Files

- Generator: `build.py` (injects the Banners channel into the Katapult Deliverables Hub artifact).
- Fragment sources: `kb.css`, `kb.html`, `kb.js`.
- Published: Katapult Deliverables Hub https://claude.ai/artifact/HTkyaVvtPH72dpT6RUNSrP, channel Banners (v9, 2026-10-02). Local copy of the published page: `04-deliverables/deliverables-hub.html`. Rebuild from a fresh read of the artifact, never from that copy.
