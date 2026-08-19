# Roku — visual identity notes

Not a full brand-guidelines ingestion — just what was observed working across 61 ad scenes (MOF and BOF holiday campaigns) in Figma during the aspect-ratio reframe session. Treat as a starting point; confirm against Roku's actual brand guidelines if/when those are supplied.

## Palette

- Dark purple base: `rgb(0.1255, 0, 0.298)` ≈ `#20004C` — the solid background under most gradient scenes.
- Purple → magenta/pink glow: large blurred ellipses (blur radius commonly ~876px at 2560×1440 scale), usually positioned to bleed mostly off-frame so only the soft glow edge shows inside the crop. This is a deliberate technique, not a mispositioned layer — see the playbook for how to tell the difference.
- White / light-lavender cards for "product UI" beats (Roku Ads Manager screenshots, budget/reach copy).

## Type

- Headline font: **"Roku Display"** (Bold / Medium weights seen). This is a licensed font **not available in the Figma Plugin API sandbox** — `figma.loadFontAsync` fails and `listAvailableFontsAsync` doesn't list it in that environment. It is presumably installed in the Figma desktop app / org font library, since the source scenes render it correctly there. Any automated Figma work touching this file must treat the font as locked — see `03-work/figma-reframe-playbook.md` for the workaround pattern (never call `resize()`/edit `characters` on an unloaded-font text node; clone + reposition, or wrap in a group and `rescale()` the group).

## Logo / lockup

- "Roku Ads Manager" wordmark — a `GROUP` node, typically named `Group 2` or `Group 3` depending on the scene.
- Recurring end-card pattern: logo + a short CTA tagline (`Frame 17`) + one large glow ellipse anchored in the bottom-right corner. That ellipse's raw coordinates look like they place it almost entirely off-canvas — it isn't; it carries `scaleY: -1` (a vertical mirror, not a genuine 180° rotation), which puts its real bounding box back inside the frame. Read `relativeTransform`, not the raw `rotation`/`x`/`y` fields, before trusting a shape's position.

## Icon style

- Hand-drawn holiday-themed line icons (snowflake, gift box, mittens, champagne glasses, camera) — all named generically **"Isolation_Mode"** in the file. The name carries no meaning; identify which icon is which by looking at the actual vectors (geometry / vector count / a screenshot), not by node name.
- Small shopping accent icons (cart, bag, cursor/arrow) built as `Union` boolean-operation nodes near CTAs.
- A small circular badge/counter icon, reused across many scenes under the literal name `Frame 1410128240`.
- A few icon-frames carry a mangled name like `_Ã Ã°_1` — this is an emoji (e.g. 🎁 / 🛍️) that lost its Unicode encoding somewhere upstream; treat it as a decorative emoji accent, not a bug to fix.

## Recurring hero asset

- **"MOF 13"** — a real photo/mockup (a family watching TV, a Roku ad visible on the screen), used as the hero image across several "biggest screen in the home" scenes. It's a photograph, not an illustration — when rescaling, preserve its aspect ratio and let `rescale()` carry its `cornerRadius` and drop-shadow along proportionally rather than touching those properties by hand.
