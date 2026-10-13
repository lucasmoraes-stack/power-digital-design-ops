# RKU26013 · Sell it on Roku · Update

Received 2026-10-12 (Concept Brief PDF). Slide deck: https://docs.google.com/presentation/d/1Px5i6cJfSyJ9PXmmbowRMgusZPKtnWhjmgofocrKQCg/edit
Previous work (RKU26008): https://www.figma.com/design/D8FpNuKI3uPGjCPqonIn3C/Progressive-Global---LAB?node-id=514-22 · local snapshots in `00-inbox/2026-10-12-rku26013-previous-work/`.

## Ask
- Hypothesis: creative that leans on Roku's recognition and streaming leadership makes Roku Ads Manager feel credible, familiar and worth trying (upper and lower funnel).
- Formats: Static + Animation. Meta 1x1, 4x5, 9x16 at 1440x1440 / 1440x1800 / 1440x2560. YouTube / CTV 16x9 at 1920x1080.
- Deliverables: 4 sizes x 5 variations = 20, plus one 16:9 that animates through all 5 (CTV spot).
- Copy (verbatim):

| Industry | Headline |
|---|---|
| Pet Supplies | Put your pet brand in their living room. |
| Beauty | Put your beauty brand in their living room. |
| Food & Bev | Put your products in their living room. |
| Wellness | Put your wellness brand in their living room. |
| Fashion | Put your latest tech in their living room. |
| Homegoods | Put your home brand in their living room. |

## Direction (call notes)
- RKU26008 was flagged as a direct ripoff of vibe.co, and Vibe recently did gen-AI claymation, so the deck references don't land.
- Client felt the work sat in a middle space (not real, not illustration, not genAI). Unanimous: lean illustrated, as a brand moment.
- Living room as an apartment inside Roku City, but no main brand-kit graphics (approval chain). Flat living room looking out on the city in silhouette.
- Lean into purples, keep it light. Table items can stay; show the brand ON the TV screen.
- Animation: mainly headline + TV screen; subtle keyframes in fore/background welcome.

## Open questions (for the account lead)
1. 5 or 6 industries? Copy table has 6, deliverable count says 5.
2. Fashion row carries "latest tech". Fashion copy, or a Tech industry?
3. Length: marked N/A with 15/20/30/60 ticked. CTV spot length? Do Meta sizes animate too? Working proposal: 3 s per industry, 15 s spot.

## Pages
- Design System: https://claude.ai/code/artifact/bc7915dd-8473-4414-a915-a25334150616 (`01-brand/build_ds.py`)
- Deliverables Hub, view `#rku26013`: https://claude.ai/code/artifact/39370946-f238-45ad-a924-31f30d9266dd (`04-deliverables/build_hub.py`)
- Rebuild from the scripts and republish from a fresh read of the artifact, never from the local HTML copy.

## Direction update (2026-10-12, Lucas)
Background must stay closer to the deck refs (concept deck slide 7, `00-inbox/2026-10-12-rku26013-concept-deck/p07-img1/2`): real room elements with an illustrated city behind. Images generated through Claude (Figma AI MCP, plan VAZIO DESIGN STUDIO, model gpt-image-2.5-sunburst), not Runway.

Pipeline: `img/raw/<ind>-plate-*.png` (room, TV off, empty wall) + `img/raw/<ind>-screen-*.png` (TV ad, no text) -> `compose.py` (drawn lilac skyline multiplied onto wall pixels only, ad on the glass, wall extended) -> `build.py` (headline, stacked lockup top right, on-screen copy; Chrome export to `export/`).
Done: Pet 1:1 V1 (for review). Next: other industries, then 4:5 / 9:16 / 16:9 plates per ratio.

## V2 (2026-10-12, Lucas feedback on V1)
- V1 was too identical to the deck reference in composition. A new version must have its own layout.
- Background illustrations must be pure illustration, not a wallpaper-like pattern on the wall.
V2: symmetric room with a floor-to-ceiling window wall (plate `img/raw/pet-plate-v2.png`, glass generated blown-out white), flat illustrated city keyed into the glass only (`compose.py` city()), TV centered, dog on armchair right, coffee table left, horizontal lockup + headline centered on the wall. V1 compositor archived in `_v1-wallpaper/`.

## V2 all variations (2026-10-12)
- CTA added: "Learn more ›", Primary Purple, centered bottom (inside 9:16 safe area).
- Built 6 industries × 4 sizes = 24 statics (`make.py`, detection in `detect.py`, city in `compose.py`), + 15 s CTV animatic MP4 (ffmpeg crossfade). Finals in `04-deliverables/ads/2026-rku26013-sell-it-on-roku/`.
- Images: 18 room plates (`img/raw/<ind>-plate-{1x1,tall,wide}.png`) + 6 TV ads (`<ind>-screen.png`), Figma AI gpt-image-2.5-sunburst, plan VAZIO.
- Fashion built as tech (copy says "latest tech"), file code `Fashion-Tech`. Pending answer.
- Retouch: Homegoods 16:9, lower-left pane has a patch of real outdoor view behind the flowers (not keyed).

## V3: split layout, CTV 16:9 only (2026-10-12, Lucas)
V2 16:9 felt unresolved (headline small and squeezed onto the wall). Tested a split on all sizes in purple and lilac; Lucas kept it for 16:9 only, lilac panel. Meta 1:1 / 4:5 / 9:16 stay V2.
- `split.py`: lilac `#EFE6FF` panel left with lockup, 4-line headline (124px, shrinks to fit) and CTA. The panel is cut to the copy: right margin of the longest line = left margin (112px), so panel width varies per industry.
- Room = the square plate (same as Meta 1:1) scaled to 1080 high and centered in the space right of the panel (Lucas, 2026-10-12: keep the dog and the scene whole). Homegoods 16:9 retouch note no longer applies (wide plate not used).
- Exports `export/*-1920x1080-Static-CTV-*-V3.png`, animatic `...-Animatic-CTV-AllIndustries-V3.mp4` (3 s holds, 0.6 s crossfade, 15 s). V2 16:9 removed from `04-deliverables`, still in `export/`. Hub republished.

## Key QA pass (2026-10-12, Lucas: white rim on the Pet dog, "pente fino")
Found across all 12 plates: white rims on fur and leaves, white specks of glass inside foliage, a ghost of the city on the light wall beside the window (Food 1:1), shaded glass under the TV left as a pale band, lilac bleed onto white pots and cream sofas, on Tech the white sideboard top half keyed, and on Tech tall a whole piece of a pane left white because a big leaf cut it off from the fill seeds (already in V2).
Fix in `make.py` `glass_mask` (shared by `make.py`, `split.py`, `qa_key.py`): trimap (sure glass = blown-out >= 242 connected to the panes, plus leaf gaps >= 246 inside the window opening; unknown = 6 px band plus cool shaded glass) solved with closed-form matting (`pymatting`), light objects and flat wood capped by a per-pixel unmix, solid light surfaces cut crisply, fill seeded over the full TV height. Cached in `img/cache/`. `qa_key.py` reports leftover white glass per plate; remaining flags are the real light bevels of the mullions.
All 18 Meta + 6 CTV frames and the animatic re-exported.

## Sideboard and TV fix (2026-10-12, Lucas: sideboard top looked strange, reflection on it too; TV ad over the dog's head)
- Sideboard: the white top meets the blown-out glass with almost no contrast, so the matte smeared lilac over it. `make._stand_line`: beside the TV the glass (254) steps down to the top (230-242) on one row; nothing below that row is keyed across the sideboard width (grown out from the TV edges), and the thin glass strip under the TV is keyed crisply (light and neutral only, so fur and feet stay).
- TV: the ad was pasted over the whole TV rectangle, covering the dog's head where it overlaps the TV. `make.put_screen` now pastes only on the black TV glass connected to the screen centre (soft edge), shared by `make.py`, `split.py`.

## CTV at 2560x1440 for Figma (2026-10-12, Lucas)
The Figma import of the 16x9s broke: Figma measures Roku Display slightly wider than Chrome, so headlines in fixed-width boxes re-wrapped to 5 lines over the CTA (the font can't be edited through the plugin API). `split.py` now builds natively at 2560x1440 (the board size in the LAB file), bakes the fit script into plain CSS (`bake`), and gives the headline box 12% slack. Headline: always 4 lines, 146px in every industry (no per-industry shrink). Exports and HTML renamed 2560x1440; animatic 2560x1440.

## CTV spot storyboard (2026-10-12, Lucas: storyboards were missing)
`storyboard.py`: 8 frames of the 15 s CTV spot at 2560x1440, built with `split.py` (options: headline lines shown, CTA off/on/pressed, TV off/on, fixed panel width = Wellness so the split never jumps). Beats: F01 open (TV off, "Put your") 0-1 s, F02 TV on Pet 1-3, F03-F07 Beauty/Food/Wellness/Tech/Home word swaps (2.4 s each, Home 1.6), F08 end with Learn more pressed 14.2-15. Animatic MP4 is cut on this timing (0.4 s crossfades). Frames: PNG + static HTML in `04-deliverables/.../storyboard/`; Hub section "CTV spot · storyboard".
Note: brief marks MOBITE (Meta animation) as checked but deliverables only list the CTV spot animating; Meta motion still an open question.

## Storyboard: one locked room (2026-10-12, Lucas: no jumps or framing breaks between frames)
Each industry plate was a different generated room, so camera, window, TV and furniture jumped between frames. Now the spot uses ONE base room (`img/raw/spot-plate-base.png`, Figma AI, empty table and armchair) and `spot.py` cuts each industry's props out of its own 1x1 plate (GrabCut + closed-form matting + colour unmix, contact shadow) onto the base coffee table -> `img/raw/spot-plate-<ind>.png`. `storyboard.py` sets `split.PLATE` to those. Verified by pixel diff: between frames only the TV area and the table props change. Dropped: the dog (spot crops the armchair at the frame edge), Beauty's lavender vase and Food's flower vase (did not cut cleanly from white glass).

## V4: ChatGPT rooms + panel layout in every size (2026-10-13, Lucas)
- Images: Lucas generated one room per industry in ChatGPT (`prompts-gpt.md`, refs in `img/gpt-refs/<ind>/`: locked room, current props, approved TV ad) -> `img/raw/<ind>-plate-gpt.png`. Same framing in all six; the ad is already on the TV.
- `v4.py`: finds the lit screen, keys the city into the glass (`make.glass_mask`; no `recolor_top`, it broke the TV foot on these rooms), sets the on-screen copy in HTML on the screen's empty left.
- Layout: the V3 16:9 strategy everywhere. Meta 1:1 / 4:5 / 9:16 = lilac panel on top (lockup, headline, CTA, left-aligned; 9:16 copy inside the 267/333 safe zones), room below cropped closer on the TV (zoom 1.08-1.1) keeping plant, table props and armchair. CTV 16:9 = `split.py` on the V4 room.
- Exports `export/*-V4.png` (24). Overview `img/review/v4-overview.jpg`. In `04-deliverables` (PNG + HTML) since 2026-10-13; V2/V3 statics moved to `_superseded-v2-v3/`. Hub republished (version 22). Storyboard and animatic MP4 still V3, to rebuild on V4 after approval.
- Adjust (2026-10-13, Lucas): 9:16 headline max 3 lines ("Put your / industry / in their living room.", 142px); 1:1 and 4:5 headline 118px in 2 lines (fits "Put your wellness brand"), panel taller, room shorter and zoomed on the TV (1.25; 9:16 1.35 shifted 30 px right so the dog's head stays). 16:9 unchanged. Hub version 23.
- Key fix (2026-10-13, Lucas: white wedge left at the sideboard corners): make.top_geometry sits 6-8 px high on the GPT rooms, so glass beside the top's slanted ends stayed white. `v4.fix_stand_ends` re-finds the glass in a band around the top (bright neutral pixels connected to the open glass, never the top surface or its bright front lip). Also `fill_slivers` (thin light lines between city and city/post become city) and `close_posts` (the light seam inside the double window posts takes the post colour). All 24 re-exported, Hub version 24.
- Figma (2026-10-13): V4 HTML imports placed in the LAB file page "roku" (node 514:2), replacing the old frames inside the six industry sections (Pet Supplies 516:931, Beauty 516:936, Food and Bev 516:941, Wellness 516:946, Fashion 516:951, Homegoods 516:956), same positions, frames named 1x1 / 4x5 / 9x16 / 16x9, layers renamed to the file convention (Panel, Logo / Roku Ads Manager, Headline, CTA > Button > Chevron, Room, TV ad > Ad tag, TV copy > TV headline / TV body / TV button). Loose import sections removed.
- Storyboard + animatic V4 (2026-10-13): `storyboard_v4.py` rebuilds the 8 beats (same timing as storyboard.py) on the V4 rooms via split.py, panel fixed at the Wellness width, F01 with the TV glass switched off. Exports `*-Storyboard-CTV-F0n-V4.png` + HTML and `*-Animatic-CTV-AllIndustries-V4.mp4` (15 s). In 04-deliverables (V3 versions in _superseded-v2-v3/), Hub version 25.
- Figma final (2026-10-13): the six industry sections re-filled from the latest import (after the sideboard corner fix); new section "CTV Spot · Storyboard (15s)" (542:657) right of Homegoods, F01-F08 in two rows of four, frames named "F0n · timing · beat", layers renamed to the file convention. Page "roku" now holds only the seven sections.
