# RKU26012 · TV Advertising in 3 Steps

Received 2026-10-15 (Concept Brief PDF). Slide deck: https://docs.google.com/presentation/d/1Px5i6cJfSyJ9PXmmbowRMgusZPKtnWhjmgofocrKQCg/edit
Victor (lead) storyboarded three AI frames as inspiration ("use as inspiration or come with your own, double check copy, add CTA frame"): `00-inbox/2026-10-15-rku26012-concept/`.

## Ask
- Hypothesis: a branded explainer demo engages and dispels the myth that launching an ad on Ads Manager is complex. Bonus: the $5,000 budget fill can filter low-spender, low-value leads (Ben's comment).
- Creative summary: a stylized Roku-branded Ads Manager screen moves through the steps, then cuts to the finished ad playing full screen on a living-room TV. Animated UI is the hero, no stock footage.
- Format: animation, 20 s. Meta 1x1 / 4x5 / 9x16 at 1440x1440 / 1440x1800 / 1440x2560, YouTube / CTV 16x9 at 1920x1080. 4 sizes x 1 variation = 4.
- Copy (verbatim): Headline "Advertise on TV in 3 Simple Steps". Subhead "Set Your Budget. Pick Your Audience. Upload Your Content." CTA "Start your first campaign".
- UI copy: budget $5,000 (not 500). Audience: interests dropdown, age options 18-24 / 25-34 / 35-50, ZIP code 90210. Upload: upload button + 0-100% bar.
- Direction: dark purple background with a very subtle Roku City silhouette. UI feels like the Roku brand, not the real Ads Manager UI: purple inner shadows on fields. Build reusable pieces: pointer, typing caret, blank field, age radios.

## Copy check (Victor's AI frames vs the brief)
- Step order follows the subhead: Budget → Audience → Upload. (The creative summary says "upload, target and launch"; the approved subhead wins. Launch is the last click of step 3.)
- Brief says "have the animation select 35-34", which is not an option. Built **25-34** (the AI frame's pick, and 2/3 are next to each other on the keyboard). **Confirm.**
- Dropped the AI-written helper lines ("Choose how much you want to spend on your campaign.", "Choose your interests, age range, and location to reach the right viewers.", "Add your video and we'll take care of the rest.", "MP4, MOV, or WebM up to 2GB"). They are not in the brief, and the file formats and 2GB limit are product claims nobody has checked.
- Dropped the blimp with "Roku" written on it. The brief asks for a subtle silhouette; a logo in the background competes with the lockup.
- UI microcopy added (needs a nod): field labels "Campaign budget", "Interests", "Age range", "ZIP code"; card titles "Your Budget / Your Audience / Your Content"; stepper "Budget / Audience / Content"; buttons "Next", "Upload Content", "Launch Campaign"; dropdown options "Food & Drink, Home & Garden, Pets, Sports & Fitness, Travel"; file "TV_Ad.mp4". Interest picked: Home & Garden, which matches the home-goods ad on the TV.
- TV ad on screen reuses the RKU26013 Homegoods ad ("Comfort, styled your way." / "Furniture and decor made to last." / "Shop now", "Ad · 0:15").

## Build (V1, 2026-10-15)
- `anim.py` writes `build/<size>.html` (layout per size), `timeline.js` = deterministic `seek(t)`; `render.py` steps 600 frames (30 fps) in headless Chrome and pipes them to ffmpeg. `render.py stills <size>` + `sheet.py` for review sheets.
- Beats: 0-2.4 intro (lockup, headline, three steps) · 2.4-6 step 1 ($5,000 typed) · 6-10.8 step 2 (dropdown, 25-34, 90210) · 10.8-15 step 3 (upload 0-100%, Launch Campaign, flash) · 15-17.4 cut to the ad full frame, pull back to the living room · 17.4-20 CTA end frame (lockup, headline, "Start your first campaign" pressed).
- Background: Roku City silhouette, `01-brand/roku_city.py` → `01-brand/illustration/roku-city-silhouette.svg` (towers, palms, Ferris wheel, bridge, water reflection), drifting slowly.
- Room: RKU26013 V4 Homegoods room (`img/room-home.png`), sharp ad on the glass (`img/tv-ad-home.png`) so the zoom holds.
- Layouts: 16:9 copy left / card right. 1:1 and 4:5 copy on top, card below. 9:16 copy + card centred in the 267/333 safe zones; the copy rides on the card top as the card changes height.
- Exports: `export/RKU26012-TVAdvertising3Steps-<size>-Animation-<Meta|CTV>-20s-V1.mp4`.

## Open questions
1. Age pick: 25-34 (built) or 35-50?
2. UI microcopy and dropdown options OK?
3. No music / SFX in the brief. Silent for now.

## V2 (2026-10-15, Lucas)
- Headlines (intro, steps, end frame) in Roku Display Regular instead of Black. UI stays bold.
- Roku blimp with the wordmark back in the background (as in Victor's frames), drifting across the top in every size: `01-brand/roku_city.py` `blimp_svg()`.
- Render moved to HyperFrames (heygen-com/hyperframes, Apache 2.0, free; telemetry disabled). Project in `hf/`: `anim.py` writes `hf/compositions/<size>.html` + copies `hf/assets/` (fonts, room, ad, timeline.js, gsap.min.js). A paused GSAP timeline registered on `window.__timelines` calls `seek(t)` from a tween modifier, so the timeline logic is unchanged. `render.py video all` runs `npx hyperframes render -q delivery` (about 30 s per size, 4 workers). Review stills still via `render.py stills`.
- Exports `export/*-V2.mp4`. Hub view #rku26012 on V2.

## Storyboard round 2 (2026-10-16, Juan's Figma comments)
- "Remove the background from the logo": he read the Roku blimp as a logo lockup. It is the blimp from Victor's frames and it flies right to left for the whole 20 s, so the storyboard now draws its flight path in every frame where it shows (dashed path, end position "BLIMP AT 20 s", label "BLIMP FLIES RIGHT → LEFT · 0 → 20 s"). Animation unchanged.
- "Add specific motion notes about these elements and how to transition them, so the editors get it right. Apply to all": every frame on the Figma board (LAB file, page "roku", all 4 sections) got a `Motion guide` layer (teal numbered markers on the moving elements, easy to hide) and a `Motion notes · Fnn` panel under it with timings and easing. Text and marker boxes come from `motion_notes.py` → `build/motion_notes.json` (timings copied from `timeline.js`; keep both in sync if the timeline changes).
- Same day, Lucas: too much. Cut to a dashed arrow on the blimp (layer `Blimp path`) and one short caption per frame (`Note · Fnn`). No markers, boxes or timing tables. `motion_notes.py` stays only as a reference for exact timings if an editor asks.
- Juan's "remove the background from the logo" was literal: the blimp raster had its drop shadow cut at the image edge, a visible box behind it. Figma board: every blimp is now the vector (`Roku blimp`, from `blimp_svg()`) with a native drop shadow. `storyboard_html.py` now pads the blimp capture so the shadow fades out.
