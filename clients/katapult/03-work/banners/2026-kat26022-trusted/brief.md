# KAT26022 Trusted: brief

Brand: Katapult. Channel: PMAX + Google programmatic banners. Funnel: TOF. Triage: 2026-10-05.
Source: client brief PDF "KAT26022 - Trusted" (sent in chat 2026-10-05).
Concept deck (Google Slides, Concept 4: Trusted): https://docs.google.com/presentation/d/1FhRaA27DeDIIe-oM2R3BCH96vUpVjEqUWNFEZqDAbTc/edit?slide=id.g3f8f2d9fdd4_1_61#slide=id.g3f8f2d9fdd4_1_61

## The ask

Hypothesis: social proof from third-party reviews beats brand-voiced creative on engagement with first-time prospects, because unfamiliarity with lease-to-own is the main trust barrier and a Trustpilot rating answers it faster than any claim Katapult can make.
Creative: bold type headline over a graphic wall of real 5-star Trustpilot review cards (star ratings + short customer quotes stacked to show volume). The Trustpilot rating and the Katapult logo anchor the frame.
Focus: lean on the volume of trusted reviews first, individual reviews later.

Original brief: 8 sizes x 1 iteration = 8 deliverables. Static only. Testing variable: none.

**Scope now (2026-10-05): 8 sizes x 2 options = 16 deliverables.** Option A "Centered badge" and Option B "Photo and seam badge" are both built in all 8 sizes. Pending: the account lead picks A or B for final delivery.

| Platform | Sizes |
|---|---|
| PMAX static | 1200x628 (1.91:1), 1200x1200 (1:1), 960x1200 (4:5) |
| Google programmatic static | 300x600, 320x50, 300x250, 160x600, 728x90 |

## Copy (client, verbatim, no edits)

- Headline: Don't take our word for it.
- Subhead: Real people, real reviews. There's a reason why thousands rate Katapult 5 stars.
- CTA: See Why Shoppers Love Katapult.

No em/en dash in the copy already (operation-wide rule, nothing to fix here). Apostrophes kept straight, as the brief has them.

## Blocking item: the review cards need real content

The brief calls for a wall of **real** 5-star Trustpilot review cards with real customer quotes, plus the Trustpilot rating, anchoring the frame. We don't have that content in the repo, and it can't be invented: a fabricated quote attributed to a "real" customer, or a made-up TrustScore/review count, would be a false testimonial, not a placeholder detail.

So both options ship with the layout and direction only: no quote anywhere, no TrustScore or review-count figure in-frame (the subhead's "thousands rate Katapult 5 stars" already carries that idea without a number baked into the art). The one trust element is a single Trustpilot badge, stars and wordmark only, text-built in Trustpilot's green, not their official logo asset, since we don't have that file. Option A surrounds it with blurred white cards carrying a star row only, unreadable texture, never a quote. Option B's shopper photo is a labeled placeholder until the real photo arrives.

**Before this can go to final deliverables we need from the client/Katapult:**
1. Real Trustpilot review quotes (short, screenshot or exported text) approved for ad use.
2. The current TrustScore and review count, if those are meant to appear on the creative.
3. Katapult's official Trustpilot badge asset (SVG/PNG), if the exact badge is required rather than a reconstruction.
4. For Option B: the real shopper photo, cleared for ad use (the Figma frame 387:14518 has one; in the coded frames it's a placeholder on purpose until it's swapped in by another route).

## What each size carries

Copy is law: whatever appears is verbatim, nothing added, nothing dropped, per size, without asking (see the Katapult copy rule).
Headline, subhead, CTA, logo and Trustpilot badge on every size, both options. On 728x90 and 320x50 the frame collapses to one row (logo, copy, badge, CTA) and Option A's halo shrinks or goes, type takes priority.

Open question: KAT26019 and KAT26021 drop the subhead at 728x90 and 320x50. This brief puts it on every size, so it stays (11px and 6px); at 320x50 it isn't really readable. Dropping it needs the account lead's OK.

## Design

Reference: the two 1200x1200 frames the account lead adjusted in Figma (Progressive Global - LAB, page "kat"), synced into the hub 1:1. Every other size follows their language.

- Ground: Dark Blue #131540, full bleed (keeps the CTA pink pill working, per the house banner rule).
- Headline: Aktiv Grotesk Medium, White, leading 1.0. Subhead: Regular, Light Blue #9EB5C0.
- CTA: Katapult pink pill, white text, medium weight (house banner rule).
- Logo: Katapult pink, bottom-right corner, never on a photo.
- Trustpilot badge: white card, flat cream offset plate (#D4A574, never a blurred shadow), "Trustpilot" wordmark + five #00B67A stars. No quote, no number.
- **Option A, Centered badge** (Figma 383:14304): copy centered at the top, a #282B60 circle rising from the bottom behind the badge, the badge inside a halo of blurred white cards with a star row only.
- **Option B, Photo and seam badge** (Figma 387:14518): photo band (top, or left on 1200x628) with rounded inner corners, the badge card bridging the photo's edge on the right, copy stacked left on the Dark Blue panel. Photo is the brand's placeholder (Light Blue, dashed Dark Blue outline, "Photo placeholder") until the real one is in.
- Safe zones: 5% inset on PMAX, 4 to 12px on programmatic.
- Type never under the higher of KAT26019 / KAT26021 at the same size.

## Status: 16 of 16 built, A or B to be chosen

All 8 sizes x 2 options built and verified by rendering (headless Chrome, real Aktiv Grotesk, every element measured: safe zone, overlaps, type floors, verbatim copy), then screenshotted. Notes with the numbers: pass 7 in [k22.html](k22.html).

## Build

Generator: [build.py](build.py) injects k22.css / k22.html / k22.js into a fresh read of the Katapult Deliverables Hub (artifact HTkyaVvtPH72dpT6RUNSrP), as the newest job inside the Banners channel, above KAT26021. Idempotent: it replaces the K22 blocks, sets the Banners tab count and the #k22 jobs-bar entry to fixed values. [export.py](export.py) writes the 16 standalone frame HTMLs.
