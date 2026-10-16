---
name: katapult-banner-craft
description: Composition rules for Katapult static ads, banners and social statics (Meta, PMAX 1:1 / 1.91:1 / 4:5, programmatic 300x250 / 300x600 / 160x600 / 728x90 / 320x50), learned from the art director's corrections. Use when planning, filling or reviewing any Katapult frame, together with katapult-patterns.
---

# Banner craft

These rules come from comparing what was first built with what the art director corrected by hand in Figma (Katapult KAT26019 to KAT26022, October 2026). Each rule is something that was actually changed. Treat a violation as a defect, not a style choice.

In Katapult Social Studio the layouts already carry the positions, sizes and colours, so most of these rules are built in. What is left to you: line breaks, which layout, which photo, which crop, which products and at what scale, and the review.

## 1. Go big

- **The headline fills its column.** Timid type is the most common defect. In the Studio this means: never step a size down with `data-size` while a better line break exists.
- **The subhead is a real second voice**, about 0.4x the headline, in a clean two-line rag.
- **No punctuation on a button** you write ("Shop Now", not "Shop Now."). Client copy keeps its own.
- **The logo is sized as a share of the frame** and anchored to a corner or the copy column; the layouts already do it.

## 2. Break lines on meaning

- Set line breaks by hand per size. Break on phrases ("And now you / don't have to."), never wherever the width runs out ("And now / you don't / have to.").
- Fewer, longer lines at the same size read faster. Keep tall stacks (five lines) only where the frame is tall (4:5, 300x600, 160x600).
- After any copy change, check that the breaks still spell the exact approved copy, word for word.

## 3. Photos

- **Full bleed.** The photo covers its box; readability comes from the layout's scrims and bars, never from fading the photo into a colour band or regrading it.
- **Real people over placeholders.** A "photo placeholder" never goes to review.
- **Re-crop per size, never shrink one crop.** Each size gets its own `data-pos` that keeps the face and the subject (a portrait strip on 1.91:1, a narrow column on 160x600).
- **One master image per concept** across all sizes of a job, so a fix happens once and every size shows the same scene.
- On leaderboards (728x90, 320x50) the photo is a block at one end; choose a photo whose subject reads at that size.

## 4. Headline over a photo: highlight bars (P2)

The setup line sits on the light warm bar in dark type, the punchline on the dark bar in Pink. The colour break carries the joke, so the setup must be the first sentence and the payoff the second. The bars sit low on the photo; pick a photo and a crop where the subject is clear above them. CTA under the bars, logo alone in a corner, legal alone at the bottom: three reading zones.

## 5. Products and flat-lays

- **True relative scale.** A fridge is taller than a washer, a bed bigger than a sofa. Never give every product the same height: use `data-scale`.
- **Products get at least half the frame** when they are the hero.
- **Mix scales and categories** (furniture, appliances, small electronics, jewelry) so the set reads as "everything you want", not "three appliances".
- **Never squash or stretch a product.**
- **Clean alpha.** Only use cutouts from the kit or files with a real transparent background; a cutout with a white box around it is a defect.

## 6. Decorative proof elements

Background review cards and badges stay straight and share one gentle treatment. Decor goes only in free space, never over faces or copy. Never a real-looking quote, rating or count that the client did not supply.

## 7. Per-format composition (built into the layouts)

- **1.91:1** is a left and right split with comparable weight on both halves.
- **Skyscrapers (300x600, 160x600)** are a centered vertical stack: headline, subhead, CTA, logo.
- **On narrow formats the CTA wraps to two lines rather than shrinking** ("Shop Cyber / Deals Now").
- **The subhead drops where it would fall under about 10px** (728x90 and 320x50).
- **The smallest sizes are recomposed, not shrunk**: 320x50 has its own arrangement. Keep its copy to the headline and a short CTA.
- **Stories (9:16):** logo, headline, CTA and legal stay in the safe middle band; the templates already keep the top 250px and bottom 250px clear.

## 8. Motion (storyboards)

Animate as a build-up: copy first or bare ground, then elements arrive in batches with the big pieces first, CTA with or after them, and the last scene equals the static. Nothing changes position between scenes.

## 9. Verify against the render

- Look at every frame in the Studio before handing anything on: a frame can pass every check and still read badly (a face under the headline, a product too small).
- After any copy change, read the fixed elements again (legal, logo) for collisions; the Studio flags overlaps between text blocks.
