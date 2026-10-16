---
name: motion-ads
description: Standard pipeline for animated ads and motion (UI explainers, CTV spots, Meta 1x1/4x5/9x16 video, Instagram Reels) for any brand, plus the storyboard rules Lucas set in October 2026. The ad is built in code (one HyperFrames composition per size, a paused GSAP timeline driving a pure seek(t)), rendered locally for free, reviewed from stills and MP4 frames, and delivered as MP4 plus storyboard. Load whenever a request involves video, animation, motion, a Reel, an animatic or a storyboard, before suggesting any paid tool.
---

# Motion ads

Proven on Roku RKU26012 (20 s Ads Manager demo, 4 sizes, 2026-10-15; Lucas: "estou IMPACTADO") and on the Katapult November Reels. Template job: `clients/roku/03-work/ads/2026-rku26012-tv-ads-3-steps/` (`anim.py`, `timeline.js`, `render.py`, `sheet.py`, `hub_media.py`, `storyboard_html.py`, `motion_notes.py`).

**Tool:** HyperFrames (Apache 2.0, free, renders locally with Chrome + ffmpeg, telemetry off). Remotion (paid above 3 people), CoAnimator, Motion.so and Fotor were evaluated and ruled out. Don't suggest a paid tool unless Lucas asks. Generated imagery only enters as an asset inside the composition (see `image-compositing`).

## Principles

- **One composition per size**, never one layout stretched. 9x16 keeps copy inside the Meta safe zone (top ~250, bottom ~340 on 1080 wide; 267/333 on 1440).
- **`seek(t)` is a pure function of time.** No state between frames, no `Date.now()`, `Math.random()`, CSS transitions or CSS animations. That's what makes preview and render identical and lets frames split across workers.
- **All timings at the top of `timeline.js`.** Retiming is one edit.
- **Brand comes from the brand** (`clients/<brand>/01-brand/`). Embed the brand font: system fonts render differently in preview and render.
- **Copy check:** every on-screen string matches the approved copy word for word. Anything invented (UI microcopy, dropdown options, file names) is listed for approval. Line breaks follow `banner-craft` §2.

## Steps

1. **Brief:** goal, length, sizes and channel, approved copy verbatim, direction, sound. Beat table (time, scene, what happens). Reference pacing: intro 2 to 2.5 s, each step 4 to 5 s, end card still for 2.5 s.
2. **Stills first:** one still per beat, per size, on a sheet. Get the stills right before polishing motion.
3. **Timeline:** short staggered entrances (0.1 to 0.2 s), exits together, next scene starts while the previous one leaves. **Never an empty frame at a cut.**
4. **Render and review:** `render.py stills all` → `sheet.py <size>` and look at every sheet; then `render.py video all` (4 workers, delivery quality); then pull frames from the MP4 around every cut (−0.3 to +0.3 s) and look for blanks, jumps, elements vanishing early, clipping.
5. **Deliver:** see below. New round = bump the version, never overwrite an approved MP4. A fix asked for one size applies to every size unless Lucas says otherwise.

## Storyboards (Lucas's rules)

- **The set doesn't move between frames.** Same background, camera and framing; only the elements that animate change. Jumps between storyboard frames read as errors.
- **Make the motion legible in the still.** If something moves but looks static (the Roku blimp read as a logo signature), add one simple arrow on it, on its own hideable layer.
- **Notes are minimal:** one short plain sentence under each frame ("Card slides up into place. Cursor clicks the budget field."). No numbered markers, dashed boxes, timing tables or note panels. "Que loucura, não precisa de tantas notas."
- Frames are named with beat, time and title ("F04 · 7.4 s · Step 2 · Interests").
- **Reels and animated posts ship as MP4 plus storyboard** (one frame per beat + `storyboard.md`). The storyboard frames and the MP4 must match.
- For Figma, storyboard frames are exported as Figma-safe HTML: see `figma-handoff`.

## Delivery

- Final MP4s in `clients/<brand>/04-deliverables/<channel>/<job>/`, named `{JOB}-{WxH}-Animation-{PLAT}-{DUR}s-{VER}.mp4`. Give Lucas clickable paths; he shares them with the team.
- Preview MP4s and posters (`hub_media.py`) go into the brand's Deliverables Hub as **published files** of the artifact, never data URIs, following the artifact rule in `~/.claude/CLAUDE.md`.

## Pitfalls already hit

- Windows long paths: HyperFrames writes temp files next to the output and breaks 260 characters in deep client folders. `render.py` renders to a short temp path and moves the file.
- No `node_modules` per job inside OneDrive. `npx` with a pinned version is enough.
- A long, slow drift (blimp moving ~180 px in 20 s) looks static in stills. Either make the move visible in the video or mark it on the storyboard.
