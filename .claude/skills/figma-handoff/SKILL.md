---
name: figma-handoff
description: How to hand HTML creatives to Figma (Figma-safe standalone HTML for the html.to.design import) and how to organize the imported frames on Lucas's boards (sections, names, layer names), learned from Roku and Katapult in October 2026. Load whenever Lucas asks for "os htmls pra importar no Figma", or to organize, rename or tidy deliverables in a Figma file.
---

# Figma hand-off

Lucas finishes most work in Figma (file `D8FpNuKI3uPGjCPqonIn3C`, "Progressive Global - LAB"). The HTML we build has to arrive there intact, and the board has to follow his layout. For the opposite direction (Figma edits back into HTML), see `figma-banner-sync`.

## 1. Figma-safe HTML

Every frame becomes one standalone HTML that imports without breaking:

- **Fixed page size** equal to the frame (`html, body` width and height set). Without it, Figma imports at 1920 wide.
- **No scripts and no CSS scaling.** Bake the final size of every element into the file. Text sized by JS or a scaled wrapper re-wraps differently in Figma. Export at the board's native size (Roku 16x9 boards are 2560x1440: export at 2560, never at 1920 for Figma to scale).
- **Everything inlined:** CSS, fonts, images as base64. The file works with nothing next to it.
- **Only what is visible** in that frame. Hidden layers get imported too.
- Known breakers to avoid or rasterize: SVG gradients referenced by id, gradient-clipped text (use a solid color), scale/translate inside an overflow clip (the clip is dropped), CSS shadows on images (become box shadows), a CSS drop-shadow on a tightly captured raster (the shadow is cut into a visible box; pad the capture or use a native Figma shadow), right-aligned text in fonts Figma measures wider (Roku Display), logos with `clip-path`.
- Keep big rasters as JPEG where there is no alpha, to keep files light.

Working generators: Roku `storyboard_html.py` (RKU26012), Katapult `build/figma_export.py` (November organic).

## 2. Delivering the package

- **All HTMLs in one folder** (plus the matching PNGs as reference if useful) and a zip one level up. Names sort by size, then frame (`...-1440x1440-...-F01`).
- Always hand over the folder as a **clickable markdown link** and say which files changed since the last import ("reimport only F09 and F10").
- Animated pieces don't become layers. Their storyboard frames do. Put the MP4s next to them in a `reels/` or `video/` folder.

## 3. Organizing the board

- **Follow the frames Lucas drew.** If he left empty template frames or boards on the page, they are the layout spec: copy their sizes, order and naming.
- **Default layout:** one section per size, stacked in this order: 1x1, 4x5, 9x16, 16x9. Frames sit side by side inside each section (200 px gap, 100 px padding). Section names look like "1x1 · Meta · 1440×1440". One section per frame or beat was rejected.
- Take frames **out of the import's loose sections** and delete those sections when done.
- **Name frames** by size or by beat ("F04 · 7.4 s · Step 2 · Interests"). **Rename layers** to the file's convention (Roku: `Panel`, `Logo / Roku Ads Manager`, `Headline`, `CTA > Button > Chevron`, `Room`, `TV ad > Ad tag / TV copy`). No generic "Container" or "Heading 1" left.
- **Match the existing month or job in the same file.** A new Katapult organic month is organized exactly like the October sections on the "kat os" page, including the logo color rule (White on Pink and Blue, Dark Blue on Cream and Orange).
- From then on, **Figma is the reference.** When the PNGs or the hub differ from Figma because of a fix made there, say so; the next export comes from Figma.

## 4. Verify, and believe Lucas

- After moving or scaling anything through the plugin API, screenshot **each whole section**, not single nodes.
- Plugin-side `rescale()` of hundreds of layers is fragile. If frames look cropped or half-scaled, regenerate the HTML at native size and reimport instead of scaling in Figma.
- **If Lucas says frames are broken, they are broken.** Don't answer that they look fine on your side or blame cache. Look at the specific frames he flagged, find the cause, fix it.
- Fonts that are not available to the plugin (Roku Display) can't have `characters` or `resize()` changed; `appendChild` and `rescale()` still work. Tell Lucas which text edits need his desktop app.
