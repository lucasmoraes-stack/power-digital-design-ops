# KAT26020 Holiday Disaster: brief

Brand: Katapult. Channel: PMAX + Google programmatic banners. Funnel: MOF/BOF. Triage: 2026-10-08.
Source: client brief PDF (sent in chat 2026-10-08; the file was misnamed "KAT26005 - Katapult is For", the job is KAT26020 Holiday Disaster). Figma: Progressive Global - LAB, page "kat", node 470:3151 (brief board + empty PMAX/Programmatic V1/V2 frames + the two photos).
Concept deck (Google Slides, Concept 2: Holiday Disaster): https://docs.google.com/presentation/d/1FhRaA27DeDIIe-oM2R3BCH96vUpVjEqUWNFEZqDAbTc/edit?slide=id.g3f8f2d9fdd4_1_27

## The ask

Hypothesis: pairing a relatable holiday appliance disaster with an immediate lease-to-own fix will outperform benefit-led creative on engagement.
Creative: a bold, slightly comedic headline over images of holiday chaos; the CTA pivots from panic to relief.
Focus: test disaster images without landing emotionally on people (mild comedy).

8 sizes x 2 iterations = 16 deliverables. Static only. Testing variable: imagery (V1 kitchen vs V2 living room).

| Platform | Sizes |
|---|---|
| PMAX static | 1200x628 (1.91:1), 1200x1200 (1:1), 960x1200 (4:5) |
| Google programmatic static | 300x600, 320x50, 300x250, 160x600, 728x90 |

(The Figma board's spec cards say "Iterations V1, V2, V3"; the brief's total is 8 x 2 = 16 and the Figma frames are V1/V2 only. Built 16.)

## Copy (client, verbatim, no edits)

- V1 kitchen. Headline: The turkey's fine. The oven isn't. CTA: Shop Appliances. Lease to Own.
- V2 living room. Headline: Cyber deals are here. Let Katapult help. CTA: Lease new furniture before family arrives

No em/en dash. V2 CTA has no period, as written.

Disclaimer: not in the brief's copy. The account lead placed this one in both Figma 4x5 frames (470:3236, 470:3241), carried verbatim on the three PMAX sizes only:
> Lease-purchase service. Total cost exceeds cash price. Approval required. Not available in MN, NJ, WI, WY. See katapult.com.

Open: confirm with the account lead whether programmatic should carry it too (no legible room under 300x600; KAT26019/21/22 ran without one).

## Creative direction (from the brief) and how it was answered

**Round 3 (2026-10-08, current): centered.** Same full-bleed system, everything on one centered axis: headline strips across the top, CTA, logo and disclaimer stacked centered on the solid Dark Blue at the bottom (logo no longer in the corner). Headline pushed to the full safe width, capped only by the longest line so V1 and V2 still match. Leaderboards unchanged (one row). Round 2 left-aligned version kept in `_fullbleed-left/`.

**Round 2 (2026-10-08): full-bleed.** Lucas asked for a fullscreen layout after round 1.
- The photo fills the frame, cover-cropped around the mishap (`FOCUS` in k20.js) so the turkey / the tree land mid-frame, clear of the type.
- The brief warns against "just putting type on top" of the images, so the headline is set as solid label strips: sentence 1 on a White strip in Dark Blue #131540, sentence 2 on a Dark Blue strip in Pink #ED5370. Readable on any part of the photo; the color break is the punchline. Aktiv Grotesk Bold, as large as fits both versions per size.
- The photo fades into solid Dark Blue at the bottom; CTA (pink pill, white text), disclaimer and logo sit on the solid part, so the logo is never on the photo. 728x90 and 320x50: the photo is a right-end panel fading left into the Dark Blue that carries logo, headline and CTA.
- Round 1 (photo cropped into a circle on a Dark Blue field, Light Blue Bounce ring) is kept in `_circle-v1/` for reference.

Both rounds:
- "The client likes these images, but they need to be lightened/brightened some." → Not regenerated. [grade.py](grade.py) lifts midtones and shadows, adds back a little contrast, trims the orange cast. Means 78→104 (kitchen) and 92→125 (living room).
- Same layout and headline size for V1 and V2 per size, so the test isolates imagery and copy.

Safe zones: 5% on PMAX, 4 to 12px on programmatic. `k20Check` in k20.js (reported by export.py) checks every frame: inside the safe zone, no overlaps, nothing covering the mishap, logo/CTA/disclaimer on the solid part of the fade.

## Files

- Photos: `img/raw/` (as received, from chat; the Figma copies are only 928x1152), `img/kitchen.jpg`, `img/livingroom.jpg` (graded).
- Fragment sources: `k20.css`, `k20.html`, `k20.js`. Generator: `build.py` (injects the job into the Katapult Deliverables Hub, first in the Banners channel; also registers it in the NAV router's job list). Exporter: `export.py` (16 standalone HTMLs with the photo crop + fade baked at 2x, PNG proofs, zip) → `04-deliverables/banners/2026-kat26020-holiday-disaster/`.
- Published: Katapult Deliverables Hub https://claude.ai/code/artifact/2abbbef7-4ac3-4e9c-a431-7c37b8e05dcf, view `#k20`. Rebuild from a fresh read of the artifact, never from the local copy.

## Status

Round 1 (circle) published 2026-10-08; replaced the same day by round 2 (full-bleed) and round 3 (centered), 16 of 16, for review.
