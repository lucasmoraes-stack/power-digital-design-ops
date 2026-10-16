---
name: katapult-patterns
description: The four approved Katapult banner patterns (P1 Knolling flat-lay, P2 Photo + highlight bars, P3 Flat brand type, P4 Proof badge) and the ten social templates, with when each fits a brief and how to fill it. Use for any new Katapult PMAX, programmatic or Meta job, together with katapult-banner-craft.
---

# Katapult patterns

The art director reworked the four 2026 banner jobs in Figma on 2026-10-13; every new Katapult banner starts from the closest of these four patterns, used across all eight sizes. Social posts start from the ten templates (T01 to T10). Codes are the ones Katapult Social Studio uses.

## Choosing

| The brief says | Pattern |
|---|---|
| An array, a grid or a wish list of products; "the big stuff"; category breadth | **P1** Knolling flat-lay |
| A situation, a moment, humour, before and after, a photo of people or a scene | **P2** Photo + highlight bars |
| Text only, a lockup, brand colours, a deal message, "no imagery" | **P3A** (Dark Blue) or **P3B** (Cream) |
| Trust, reviews, ratings, social proof, "don't take our word for it" | **P4A** (centered badge) or **P4B** (photo seam) |
| An organic or Meta post, a carousel, a Story | a template, T01 to T10 |

When two fit, prefer the one the brief's reference image resembles. When none fits, say so and name the closest.

## P1 Knolling flat-lay (KAT26019 Top Items)

Salmon paper ground, copy top left (logo, headline, subhead, CTA), eleven products packed at true scale in the lower half: fridge, washer, bed, couch, TV, tire, laptop, console, nightstand, vacuum, necklace. The products are fixed in the layout (they cannot be swapped in the Studio); the slots are the copy. Fits any "everything you can lease" message. Headline Dark Blue, CTA Pink pill. 320x50: headline on one line, small CTA, a few tiny products.

## P2 Photo + highlight bars (KAT26020 Holiday Disaster)

Full-bleed photo, no colour band. The headline is two bars low on the photo: setup on the Cream bar in Dark Blue, punchline on the Dark Blue bar in Pink. Big Pink CTA pill under the bars, White logo top right, one-line legal at the bottom on the PMAX sizes. Leaderboards: Dark Blue ground, Pink logo left, bars, photo as a block at the right end.
- The copy must split into a setup and a payoff. A one-sentence headline does not fit P2.
- Photo: one Library photo for all sizes (or an `upload:` scene from the client), each size with its own `data-pos` keeping the subject above the bars.

## P3 Flat brand type (KAT26021 Cyber)

Type only. **P3A** Dark Blue ground: first sentence White, second sentence Pink, one accent word per sentence in lavender. **P3B** Cream ground: first sentence Blue, second Pink, accents and subhead Dark Blue. Pink logo bottom right.
- Built for a two-sentence headline ("The deals won't wait. And now you don't have to."). Mark lines of sentence one `t1`, sentence two `t2`, one accent word per sentence `ta`.
- On 1200x1200 the headline sets in four lines; keep the line count of the sample at every size.

## P4 Proof badge (KAT26022 Trusted)

Dark Blue ground, a Trustpilot card (stars, wordmark) with a Cream offset plate. **P4A**: the card centered over a lighter navy half-circle, small blurred review cards around it with stars only. **P4B**: a photo band with the badge on the photo's edge; copy on the Dark Blue panel.
- The badge has no rating number and no quote, on purpose. Real quotes, a TrustScore or a review count only when the client supplies them, and then they are a request to the art director (no slot exists for them).
- P4B photo: a person with a phone or laptop reads as "a real shopper"; `laptop-woman-window-desk-06` was the approved choice.

## Templates (social)

| Code | Fits |
|---|---|
| T01 Full image | One strong lifestyle photo, short headline at the bottom |
| T02 Split panel, image | A three-beat headline ("Your home. Your upgrade. Your move.") and a tall photo |
| T03 Split, phone in hand | App, how it works, apply on your phone |
| T04 Product row, 3-up | Category or gear: three products |
| T05 Hero product, bleed | One hero product, conversational headline, Cream |
| T06 Top block, photo card | Home and lifestyle, photo as proof, Pink |
| T07 Top block, product on circle | One product launch or tech message, Pink |
| T08 Typographic statement | Brand, manifesto, carousel covers; last line Pink |
| T09 Hero photo, full width | Big photo, short headline, last words Pink |
| T10 Product trio, circles | Roundups with exactly three products |

Every template carries the legal line and the "Leap Forward"-style pill; both stay. Headline sizes are large on purpose; match the sample's line count.

## Known open points (as of 2026-10-13)

- Three banner colours differ between the 2022 guideline and the approved Figma (lavender `#AFB3CC` vs Light Blue `#9EB5C0`, Blue `#364488` vs `#365488`, Cream `#EAD0B6` vs `#D4A574`). The layouts use the approved Figma values; don't raise it per job.
- The Bounce arcs from the 2022 guideline are retired.
