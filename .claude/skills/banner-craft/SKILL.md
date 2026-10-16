---
name: banner-craft
description: Visual quality rules for static ads and banners (Meta, PMAX 1:1 / 1.91:1 / 4:5, IAB programmatic 300x250 / 300x600 / 160x600 / 728x90 / 320x50), learned from Lucas's own corrections. Load before designing, reframing or reviewing any banner or social static, for any brand. Brand-agnostic; the brand's own section or skill still decides colors, fonts and logo use.
---

# Banner craft

These rules come from comparing what the agents built with what Lucas corrected by hand in Figma (Katapult KAT26019 to KAT26022, October 2026) and from earlier reviews (Roku RKU26013, Habit emails). Each rule is something he actually changed. Treat a violation as a defect, not a style choice.

Brand facts (palette, type family, logo variants, legal line) always come from the brand. These rules only cover how to compose with them.

## 1. Go big

- **Headline fills its column.** Size up until the headline nearly fills the copy area (about 70 to 80% of the frame width on 1:1). Lucas's corrections went 110 → 124px, 84 → 95px, 42 → 53px on 300x600. Timid type is the most common defect.
- **Subhead is a real second voice, not body grey.** About 0.4x the headline size (63px under a 151px headline on 1:1), Regular weight, in an accent color of the palette, set in a clean two-line rag.
- **CTA text about 0.3x the headline on PMAX**, in a generous pill (vertical padding about 0.5x the font size, horizontal about 1.15x). The pill can run 60 to 65% of the width on photo layouts. No punctuation on a button ("Shop Now", not "Shop Now.").
- **Logo is sized as a share of the frame**, about 18 to 23% of the width on PMAX, anchored to a corner or to the top/bottom of the copy column. Never a tiny afterthought.
- **The logo must read in every size and version.** Check its contrast against what is actually behind it in each crop (Katapult KAT26020 160x600 V2 failed on the living-room photo). Move it, switch its color variant or add a scrim.
- **CTA lives with the copy.** Logo, headline and CTA form one block. A CTA floating on its own at the far end of the frame was rejected (Roku RKU26013).
- **No dead space.** A big empty gap between the visual and the copy, or white space with no job, reads as unresolved. Enlarge the headline, zoom the image or tighten the block. When a layout fights for room, try a split: image on one side, a colored panel with the copy on the other, panel margins equal to the text margins.

## 2. Break lines on meaning

- Set line breaks by hand per size. Break on phrases ("And now you / don't have to."), never wherever the width runs out ("And now / you don't / have to.").
- Fewer, longer lines at the same size read faster. Keep tall stacks (5 lines) only where the frame is genuinely tall (4:5, skyscrapers).
- **Never leave a short word dangling at the end of a line.** Pronouns, prepositions and articles go down with the phrase they belong to: "Select Katapult / at checkout.", "Apply and verify / your information". Lucas corrected "your", "you" and "at" one by one on the November Reels.
- Set a line budget per format and hold it: Roku RKU26013 = 9:16 at most 3 lines, 1:1 and 4:5 in 2 lines at a bigger size.
- When rebuilding from code, check that the per-size line breaks still spell the exact approved copy.

## 3. Photos

- **Full-bleed.** The photo covers the whole frame; don't fade it into a solid color band to hold the CTA and logo. Text sits on the photo.
- **Readability comes from soft black scrims, not regrading or color fills.** Use a corner gradient behind the logo (black ~40% → 0), a bottom gradient behind the legal (black ~40% → 0 over the lowest 25 to 30%), or a flat ~10% veil. Keep the photo's original grade; don't brighten it then fight the brightness. Exception: when the photo reads too dark, especially in cutdowns where the subject fills the frame, lift the image slightly overall and raise the mids and shadows on the subject itself (Katapult client feedback on the turkey version, 2026-10-14).
- **Zoom in rather than leave empty wall.** Crop closer on the hero (TV, couple) while keeping the essential elements of the scene in frame (the dog, the plant, the props).
- **Real people over placeholders.** If the brand's approved photo library has a fitting image, use it. A "photo placeholder" box never ships to review.
- **Re-crop per size, never shrink one crop.** Each ratio gets its own crop that keeps the face and the subject (portrait strip on 1.91:1, narrow column on 160x600). Each version can have its own crop and zoom; don't force V1 and V2 to share a layout.
- **One master image per concept** when a set has many sizes: refine one plate and crop it for all sizes, so a fix happens once and every size shows the same scene.
- **Hide something by changing the viewpoint with real pixels**, not by painting over it. Painted fills read as fake immediately.
- On leaderboards (728x90, 320x50) the photo becomes a hard-edged block or a rounded tile at one end, mirrored if needed so the subject faces the copy. No fade.

## 4. Headline over photo: highlight bars

When a headline sits on a photo, set it as stacked highlight bars: each bar hugs its own line, bars touch with no gap, centered, placed low over a quiet part of the image (starting about 58 to 64% down on square and tall frames, 42 to 50% on 1.91:1) with the subject left clear above. Setup line: light warm bar with dark type. Punchline: dark bar with the accent color. The color break carries the joke. CTA sits right under the bars; logo alone in a corner; legal alone at the bottom edge: three separate reading zones.

## 5. Products and flat-lays

- **True relative scale.** A fridge is taller than a washer, a bed bigger than a sofa. Never give every product in a row the same height.
- **Pack the product zone tight**, 5 to 10px gaps, big pieces interlocking with small ones. Even gutters and centered rows read as a spreadsheet.
- **Products get at least half the frame** when they are the hero. Copy above, products below.
- **Mix scales and categories** (furniture, appliances, small electronics, jewelry) so the set reads as "everything you want", not "three appliances".
- **Rotate a product 90° to fill a slot; never squash or stretch it.**
- **Let edge products bleed** slightly past the margin or off the frame, so it reads as a crop of a bigger table.
- **Real ground texture** (photographed paper, surface) and shadows that follow the cutout's shape (`filter: drop-shadow`, not `box-shadow`), all from one light direction.
- **Clean alpha.** Zoom every keyed edge at 100% (fur, foliage, white objects next to the key) before showing anything. Use a real matte, not a brightness threshold. Check overlaps of anything pasted, not just keyed edges.

## 6. Decorative proof elements

Background review cards, badges and similar decor stay straight and share one gentle treatment (one blur value per frame, e.g. 3px on 1:1). Mixed rotations (−18° to +24°) and mixed blur (0 to 8px) read as clutter. Decor goes only in free space, never over faces or copy.

## 7. Per-format composition

- **1.91:1** is a left/right split with comparable weight on both halves (copy column left, photo or visual cluster right), not a squashed square.
- **Skyscrapers (300x600, 160x600)** use a centered vertical stack: headline, subhead, CTA, logo, even gaps (about 24px on 160x600). Don't copy the left-aligned PMAX layout.
- **On narrow formats the CTA wraps to two lines rather than shrinking** ("Shop Cyber / Deals Now" at 16px instead of 13px on one line).
- **Drop the subhead where it would fall under about 10px** (usually 728x90 and 320x50). Keep it on 160x600 when it fits as a short three-line block.
- **Recompose the smallest sizes; don't shrink the big one.** 320x50 gets its own arrangement (headline on one line, small CTA, logo moved, a few tiny products or a photo tile).
- Social stories: keep logo, headline, CTA and disclaimer inside the safe middle band (top and bottom ~250px of 1080x1920 are covered by UI).

## 8. Motion (animated storyboards)

Animate as a build-up: copy first (or bare ground), then elements arrive in batches with the big pieces first, CTA with or after them, last scene equals the static. Nothing changes position between scenes. Full pipeline and storyboard rules: `motion-ads` skill. Generated or composited images: `image-compositing`. HTML for Figma: `figma-handoff`.

## 9. Rounds, versions and sets

- **"Replicate on V2" means everything.** When Lucas adjusts V1 and asks to carry it over, every change goes to every V2 at the same values (CTA size included; Lucas, 2026-10-09). If something truly doesn't fit, solve the layout (shorter break, wider pill, two lines) instead of keeping the old value and explaining why.
- **A font swap stays inside the grid.** After changing a typeface (e.g. Futura Std → Lato for subhead and body), re-check every frame: nothing crosses the margins or safe zones. If it doesn't fit, scale the whole text block, not one line.
- **A fix asked on one piece applies to every piece with the same problem**, all sizes and variants, unless Lucas limits it ("o split deve ser apenas no 16x9").
- **"Less grotesque, more refined" means go back and polish**, not add. When Lucas prefers an earlier proposal, return to it and refine proportions, weight and spacing; don't stack more decoration on the new one.
- **Vary a set.** Pieces in a series (a month of posts, a carousel) change layout family and ground color from one to the next. Same layout and same tone everywhere reads as "mais do mesmo".
- **Icons and grouped elements need hierarchy:** one primary item, the rest secondary, aligned in one group. Loose icons scattered around read as a mess.

## 10. Verify against the render

- Compare your render with the reference image side by side at the same size, frame by frame, before showing anything. Match the rendered ink, not node coordinates: browser glyph placement and Figma's node padding can disagree by up to 11px.
- After any copy change, re-check fixed siblings (footer, logo, legal) for collisions.
- Run an independent review pass before Lucas sees a layout.
