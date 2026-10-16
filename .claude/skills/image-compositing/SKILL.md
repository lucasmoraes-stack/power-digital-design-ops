---
name: image-compositing
description: Craft rules for generated or composited ad imagery (AI-generated rooms and scenes, keyed windows or skies, pasted screens, props added to a plate, illustration mixed with photo), learned from Lucas's corrections on Roku RKU26013 in October 2026. Load before generating, compositing, retouching or reviewing any image that is not a straight photo, for any brand.
---

# Image compositing

Every rule here is something Lucas rejected on Roku RKU26013 (Sell it on Roku, 2026-10-12 to 10-13), sometimes three rounds in a row. His words for the failures were "amador", "bizarrice", "podre", "o cliente vomitaria". Treat each rule as a ship blocker.

## 1. Where images come from

- **Generate inside the session**, with Figma AI through the Figma MCP (`generate_image`, plan VAZIO DESIGN STUDIO; `gpt-image-2.5-sunburst` worked for photoreal rooms). Never Runway.
- **When Lucas generates outside** (ChatGPT etc.), give him one unified prompt per variant, ready to paste (base and variant merged, never "paste the base, then this"), plus the reference images already saved in one folder per variant with numbered names (`1-room.png`, `2-props.png`, `3-tv-ad.png`) and the clickable path. Say where to save the results.
- **Never copy the reference composition.** A reference sets the mood and the ingredients. A new version needs its own layout, camera and arrangement.
- **Illustration stays pure illustration**: crisp, opaque, flat (a drawn city seen through a window). Never a "wallpaper" look blended or printed onto a wall.

## 2. One master plate per concept

- A set with many sizes uses **one refined image per category**, cropped for every size. Pick the framing so every crop works (keep the hero, e.g. the dog, whole). A different generated image per size means every fix is done three times and the sizes drift apart.
- A shared element (TV stand, sofa, window) comes from one approved reference and repeats identically. If one variant got it right ("the 4x5 base is perfect"), it becomes the model for all of them.
- In a storyboard or animatic **the set is locked**: same room, camera and framing in every frame. Only the props and the screen content change. No jumps between frames.

## 3. Physical plausibility

- **Contact:** objects touch what they stand on. A TV foot sits on the stand's top edge, centered on its own base. No floating, no gap.
- **Scale:** props at real-world size against the furniture (a candle is not a third of a 1 m table; a watch band is not 35 cm). Compare against a known object before showing.
- **Light:** props match the room's light direction. Front-lit props in a back-lit room read as pasted. Add contact shadows and a dark occlusion line where an object meets its surface; no pale rings or white ticks at the base.
- **Continuity:** structures keep going behind objects (a window mullion runs down to the back of the sideboard, not stopping in mid-air or ending in a pale "foot").
- **Restraint:** three props read better than five. Remove anything Lucas asked to remove in every variant, and don't let unreadable lumps or debris survive.

## 4. Keying and pasting

- Use a real matte (trimap + closed-form matting, e.g. pymatting), not a brightness threshold. Thresholds leave halos on fur, foliage and anything white near the key.
- **Light surfaces next to blown-out glass** need a hard geometric line, not a soft matte (otherwise the sideboard top turns lilac).
- **Paste screens only where the screen pixels are**, never the whole rectangle. Anything in front of the TV (a dog's head) stays in front.
- **Decontaminate edge color** on anything cut against the new background (no purple fringe on an armchair edge, no smoky cutout on a sofa or tree).
- No leftovers from earlier passes: no smudges, ghosts of removed objects or blurred bands above a retouched area.

## 5. Fix by changing the view, never by painting

When Lucas asks to "not show" or "simplify" a surface, move or crop real pixels to change the viewpoint (e.g. lift the stand's front face to the TV foot so the top is seen edge-on). Never paint a synthetic fill over it: flat fills read as cardboard immediately. Change nothing else in the image. If unsure, show one plate before rebuilding every frame.

## 6. QA before Lucas sees it

1. Zoom every keyed or pasted edge at 100% (fur, leaves, white objects, posts, screen borders), every variant and every size.
2. Run an automatic leftover check where one exists (Roku: `qa_key.py`) plus tiled 4x crops of the worst areas.
3. Send the frames to an independent reviewer agent (Brand Guardian or Designer as art-direction QA) and fix until it says shippable. Report what it still flags instead of hiding it.
4. When you list known defects, fix them first if you can. "Visible only at zoom" is not a reason to ship a defect Lucas will see in Figma.

Reference job: `clients/roku/03-work/ads/2026-rku26013-sell-it-on-roku/` (`brief.md` has every round; `v4.py`, `make.py`, `qa_key.py`, `prompts-gpt.md`, `img/gpt-refs/`).
