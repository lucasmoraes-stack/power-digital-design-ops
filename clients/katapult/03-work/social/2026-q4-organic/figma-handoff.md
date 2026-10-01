# Katapult Q4 organic: Figma foundation handoff

Built 2026-09-28 by Designer (foundation pass). For the builder agents that rebuild the 15 approved posts as editable frames.

- File: https://www.figma.com/design/D8FpNuKI3uPGjCPqonIn3C/Progressive-Global---LAB (file key `D8FpNuKI3uPGjCPqonIn3C`)
- Page: **Page 9** (`193:657`). Work only on this page. Do not touch other pages.
- Design source of truth (read, do not change): `scratchpad/katapult-q4/index.html` (built by `build.py`, components in `scratchpad/kp_v2.css`). Each slide in the page is `<article id="pNN-sN">`; match it by id. Base64 font lines 3 to 5 of index.html: never read them whole.
- Copy: `clients/katapult/03-work/social/2026-q4-organic/copy.md`, verbatim, pre-approved.

## Font actually used

**Aktiv Grotesk is NOT available in this Figma file** (`listAvailableFontsAsync` returns no Aktiv family). All text styles use **Inter** as a stand-in: Light (for Aktiv 300), Medium (500), Bold (700). Load them as `{family:'Inter', style:'Light'|'Medium'|'Bold'}`. A human swaps the `Katapult/*` text styles to Aktiv Grotesk in Figma desktop later; because every text node uses a style, that swap is one edit per style. Expect line breaks to shift slightly after the swap.

## Parallel work split (suggested)

- Builder A: posts 01, 02, 03, 04, 05
- Builder B: posts 06, 07, 08, 09, 10
- Builder C: posts 11, 12, 13, 14, 15

Each builder touches only its own sections. Never edit the Components section, variables or styles (ask the lead if something is missing). Never run two `use_figma` scripts that touch the same section.

## Variables

Collection **Katapult** (`VariableCollectionId:197:656`), one mode `Value`. Scopes: frame fill, shape fill, text fill, stroke. Bind fills/strokes with `figma.variables.setBoundVariableForPaint(paint,'color',variable)`.

| Variable | Hex | ID |
|---|---|---|
| color/Pink | #ED5370 | VariableID:197:657 |
| color/Logo Pink | #EC5370 (logo only) | VariableID:197:659 |
| color/Dark Blue | #131540 | VariableID:197:661 |
| color/Blue | #365488 | VariableID:197:663 |
| color/Light Blue | #9EB5C0 | VariableID:197:665 |
| color/Orange | #E48027 | VariableID:197:667 |
| color/Cream | #D4A574 | VariableID:197:669 |
| color/Surface | #EAEAE8 | VariableID:197:671 |
| color/White | #FFFFFF | VariableID:197:673 |
| color/Black | #000000 | VariableID:197:675 |
| color/Grey/Dark Grey | #4D4D4D | VariableID:197:677 |
| color/Grey/Medium Grey | #808285 | VariableID:197:679 |
| color/Grey/Grey | #A4A4A4 | VariableID:197:681 |
| color/Grey/Light Grey | #D8D8D8 | VariableID:197:683 |
| color/Grey/Lightest Grey | #F0F0F0 | VariableID:197:685 |

Paint styles with the same names under `Katapult/` (e.g. `Katapult/Pink`, `Katapult/Grey/Light Grey`), each bound to its variable. Prefer binding the variable directly; the styles exist for manual use.

## Text styles (Inter stand-in)

Apply with `await text.setTextStyleIdAsync(id)` (or `text.textStyleId = id`) after loading the font.

| Style | Spec | ID |
|---|---|---|
| Katapult/4:5/Headline 88 | Medium 88, lh 104%, ls -1.2% | S:d79b9447e3cdacf42cca884788a674329aa41d5c, |
| Katapult/4:5/Display 104 | Medium 104, lh 100%, ls -1.2% | S:1731e50bd675cc85f99f700f5b2fb1150e558711, |
| Katapult/4:5/Subhead 40 | Bold 40, lh 120% | S:85973174d163c5c7dc2ac36b927264a1bd7036d5, |
| Katapult/4:5/Body 36 | Light 36, lh 130% | S:728603d178a0b7c322451c9b4a6df0ca1c414a10, |
| Katapult/4:5/CTA 34 | Bold 34 | S:871dc9769ff661e13e3cd9676a600dcada02104f, |
| Katapult/4:5/Option-Tile 30 | Bold 30, lh 115% | S:90296de66f29fdba9147bb6a7b63ad1578b59803, |
| Katapult/4:5/Prompt 66 | Medium 66, ls -1.2% | S:67c07f09e21eed4e49827e498ec608d03364fd6d, |
| Katapult/9:16/Headline 96 | Medium 96, lh 104%, ls -1.2% | S:748e4746a0fabb461396ce7b4868fb8137029ff2, |
| Katapult/9:16/Body 38 | Light 38, lh 130% | S:9119aecda244980920f7ea56b6f767746dddbfa5, |
| Katapult/9:16/Subhead 42 | Bold 42, lh 120% | S:5241cda476740c309d5bc8817de96b4ff9df2ff7, |

Mapping from the page CSS: `.kp-headline` = Headline (Display when the page uses `disp=True`, i.e. `--kp-display`); `.kp-text` = Body; `.kp-sub` = Subhead; `.kp-cta` = CTA; `.kp-opt` / `.kp-tile` = Option-Tile. Text colors follow the slide theme (below). Small placeholder labels inside components are raw Inter Bold, not styles; do not add other text.

## Components (section "Components", `198:656`, at page 0,0)

Create instances with `(await figma.getNodeByIdAsync(variantId)).createInstance()`, or `importComponentByKeyAsync(key)` is not needed (same file). Set variants on an instance with `instance.setProperties({'Color':'White'})`; text props with the full property key shown.

**Logo** (set `198:678`), prop `Color`. Supplied SVG imported as vector (5 paths), fills bound to variables, 250x55.66, aspect locked. 9:16: scale instance to 280 wide (`instance.rescale(280/250)`).
- Color=Pink `198:657` key `37aa77867a4ee57666924b5a559264024e1eb48a` (Logo Pink, light grounds, inside cards, Dark Blue ground)
- Color=White `198:664` key `6721817b29e0bb25c3fb910d6812615307f025c9` (Pink, Blue grounds)
- Color=Dark Blue `198:671` key `70b91fc245ac4215353b861874baf071b6ef9892` (Cream, Orange grounds)

**Photo placeholder** (set `198:697`), prop `Fill`, text prop `Description#198:0`. Default 600x600, resize freely; dashed outline stays inset 20.
- Fill=Light Blue `198:679` key `23ee0bcc6a02fa4bf44bf0e612220cb6bc31d669` · Cream `198:682` key `27d33e4f79915374a1137e56ac79fde5ef7b1d24` · Pink `198:685` key `aef098457a1b4da7205cb745a82b7581016cb777` · Blue `198:688` key `ce6e15b1fa1012eaba879c6a681af91d45f44942` · Orange `198:691` key `f25cf7cedf8c82092566a1f0395bbe554990a9fa` · White `198:694` key `c023da45ca7e1fd06c18f548bca44c0099a0db85`
- Page class mapping: `.kp-ph.lb/.cr/.pk/.bl/.or/.wh`. Description = the page's photo label text for that slide.

**Cutout placeholder** `198:698` key `61842e29584a36a5bbac694137dc067f23a454fd`, text prop `Label#198:7`. 300x300 dashed Dark Blue box, radius 24. Place it inset 14% on top of its colored slot shape.

**Icon disc** (set `198:710`), prop `Tone`, text prop `Label#198:8`. Default 120; scale uniformly to the page's `--d`.
- t-w `198:700` key `64e5fb1903f76aa5ef5a9b1114784664c8b1847b` · t-s `198:702` key `3ad3e801c12b95308b8663bf3ba2a867bd3805bd` · t-c `198:704` key `5309a359698c8a5f9f233ba8d08f1dd82ae761ad` · t-p `198:706` key `6f08f5a3e96047da838db84c09ee03d269278832` · t-db `198:708` key `ef9501776a3add9bb84741c9189869284aeddea2`

**UI card** (set `198:739`), prop `Plate`. Structure: component (auto layout, hug) > `Offset plate` (absolute, +16/+16, stretch) + `Card` (vertical auto layout, White, radius 36, padding 44/48, gap 22, width 760) > `Content slot (replace)`. To use: instance, `detachInstance()`, delete the slot, append rows into `Card`. Resize `Card` width as needed; plate follows.
- Plate=Dark Blue `198:711` key `1dcea146622c360d3d1982e57eb921c5a009034e` · Pink `198:715` key `d8fa1337dcdd74946ab0a6b7f6cc5b50a4a0bb2f` · Cream `198:719` key `d7c6497cb264abbae6e599843e11bcbf9c4ceda8` · Light Blue `198:723` key `226b3f5681d27735895cc4947e10778c627d04ba` · Blue `198:727` key `24e1131fe655a009448a87a05381d20ffa5329ae` · Orange `198:731` key `465ac3f40a8a6686b78be371006379c052881fd6` · White `198:735` key `ae6d1b9da1dcf31665e6275709521726fca7da6a`

**Input field** `199:656` key `b6b9e205f6e1b902b34b7438b07999b8da0912e9` (600x96, radius 22, Lightest Grey, 4px Light Grey stroke, Pink caret; set FILL in a row). **Send button** `199:658` key `80b5d9e78d0328c7045a06ed63e01ad59c794aef` (96px Pink circle, white arrow).

**CTA pill** (set `199:665`), prop `Theme`, text prop `Label#199:0`. Hug width, 88h, padding 0/52, CTA 34 style.
- Theme=Pink `199:661` key `e81990fed2051dd2d7bd02717e3f73d8bf85af9a` (Surface, Dark Blue, Blue grounds) · Theme=Dark Blue `199:663` key `c0e46c40f22e25ab2b8b17f656f05b24e7d9159f` (Pink, Cream, Orange grounds)
- Katapult rule: after any resize of a pill instance, re-set `cornerRadius = Math.min(width,height)/2` and screenshot; a resize can zero the radius override.

**Checkbox** (set `199:686`), props `Ink` (Dark Blue/White) x `State` (Off/On). Off ink Dark Blue `199:666` · On `199:668` · White Off `199:676` · White On `199:678`. 58px; checklist rows use 50px (rescale).
**Radio** (set `199:687`): DB Off `199:667` · DB On `199:671` · White Off `199:677` · White On `199:681`.
**Track square** (set `199:688`), `Ink` x `State` (Off/On/On Alt): DB Off `199:673` · DB On `199:674` · DB On Alt `199:675` · White Off `199:683` · White On `199:684` · White On Alt `199:685`. On Alt (Dark Blue) is for Pink and Orange grounds. Row gap 14.
**Toggle** (set `199:693`): Off `199:689` · On `199:691`.
**Progress segment** (set `199:696`): Off `199:694` · On `199:695`. Row of FILL segments, gap 12.
**Safe zone guide** (set `199:701`): Ratio=4:5 `199:697` key `1f768dd6c692e581d2ab35e2b732f31e58d3a26e` (90 top/bottom, 80 sides) · Ratio=9:16 Story `199:699` key `fd4a12dc767a84178c0290369d4a04ca9c678a8e` (250 top/bottom, 120 sides).

Control variants are listed by node ID only; inside this file the ID is all you need (`getNodeByIdAsync(id).createInstance()`).

Not built as components (build from shapes with variables, as the page does): bars (`.kp-bar`), dots (`.kp-dot`), rules, grids/cells, Venn circles, triangle, fanned cards, prints (use UI card or White rect + plate), phone frame, slider, picker rows, tiles. Keep them flat: palette fills only, no tints, no shadows, no blur.

## Layout scaffold (calendar order, top to bottom, x = 0)

Every section: slides left to right at x = 160 + i*1160, y = 160 (80 gap between slides), frames clip content, ground fill bound to the variable. Each frame already contains one child: `Safe zone guide` instance (hidden, locked). Keep it as the **last (top) child**: after appending your layers, move it back on top with `frame.appendChild(guide)`, and keep it hidden and locked.

| Section | Section ID | Frames (ID, ground) |
|---|---|---|
| 01 · What Is Lease-to-Own? · Carousel 4:5 · 5 slides | 200:656 | p01-s1 200:657 Dark Blue · s2 200:660 Surface · s3 200:663 Dark Blue · s4 200:666 Surface · s5 200:669 Dark Blue |
| 02 · Lease-to-Own vs. Traditional Credit · Carousel 4:5 · 5 slides | 200:672 | p02-s1 200:673 Surface · s2 200:676 Blue · s3 200:679 Pink · s4 200:682 Dark Blue · s5 200:685 Surface |
| 03 · How Katapult Works · Carousel 4:5 · 6 slides | 200:688 | p03-s1 200:689 Pink · s2 200:692 Surface · s3 200:695 Dark Blue · s4 200:698 Cream · s5 200:701 Blue · s6 200:704 Orange |
| 04 · When You Need It, You Need It · Carousel 4:5 · 5 slides | 200:707 | p04-s1 200:708 Cream · s2 200:711 Dark Blue · s3 200:714 Cream · s4 200:717 Dark Blue · s5 200:720 Cream |
| 05 · Your Next Chapter Starts With What You Need · Carousel 4:5 · 5 slides | 200:723 | p05-s1 200:724 Dark Blue · s2 200:727 Surface · s3 200:730 Dark Blue · s4 200:733 Surface · s5 200:736 Pink |
| 06 · More Choices Can Make a Difference · Carousel 4:5 · 5 slides | 200:739 | p06-s1 200:740 Surface · s2 200:743 Dark Blue · s3 200:746 Cream · s4 200:749 Pink · s5 200:752 Blue |
| 07 · What Would You Replace First? · IG Story 9:16 · 1 slide | 200:755 | p07-s1 200:756 Cream (1080x1920) |
| 08 · Finish the Sentence · Static 4:5 · 1 slide | 200:759 | p08-s1 200:760 Pink |
| 09 · What Matters Most at Checkout? · IG Story 9:16 · 1 slide | 200:763 | p09-s1 200:764 Dark Blue (1080x1920) |
| 10 · Get What You Need. Pay Over Time. · Static 4:5 · 1 slide | 200:767 | p10-s1 200:768 Surface |
| 11 · Shop More Retailers With Katapult · Static 4:5 · 1 slide | 200:771 | p11-s1 200:772 Cream |
| 12 · Know Your Buying Power · Static 4:5 · 1 slide | 200:775 | p12-s1 200:776 Dark Blue |
| 13 · More Than a Payment Option · Carousel 4:5 · 5 slides | 200:779 | p13-s1 200:780 Pink · s2 200:783 Dark Blue · s3 200:786 Pink · s4 200:789 Dark Blue · s5 200:792 Pink |
| 14 · Built for Shoppers. Built for Retailers. · Carousel 4:5 · 5 slides | 200:795 | p14-s1 200:796 Surface · s2 200:799 Pink · s3 200:802 Dark Blue · s4 200:805 Cream · s5 200:808 Blue |
| 15 · Why Katapult Exists · Carousel 4:5 · 5 slides | 200:811 | p15-s1 200:812 Dark Blue · s2 200:815 Cream · s3 200:818 Pink · s4 200:821 Surface · s5 200:824 Blue |

4:5 frames are 1080x1350; Stories 1080x1920. Section positions: 01 at y 6326, then each next section 400 below the previous one.

## Coordinate conventions

- All positions you set inside a slide are **relative to the slide frame** (0,0 = its top-left). Never set page-absolute coordinates.
- Safe area (from the page CSS): 4:5 top 90, bottom 90, sides 80 (content box 920 wide, x 80 to 1000, y 90 to 1260). Story: sides 120, top 250, bottom 250 (the approved page sets .kp-tpl-story-poll to a 250 safe bottom; the guide component matches). **Correction 2026-09-28:** ignore the earlier 420/y 1500 note; Story content may run to y 1670.
- Stage bleeds (`.bl-b`, `.bl-t`, `.bl-x`, `.bl-r` in the page) mean the visual runs to the frame edge on that side; the frame clips it.
- Theme ink per ground (from kp themes): Surface: headline Black, subhead Dark Blue, logo Pink, CTA Pink/Dark Blue text. Dark Blue: headline White, subhead Light Blue, logo Pink, CTA Pink. Pink: text Dark Blue, logo White, CTA Dark Blue. Cream and Orange: text Dark Blue, logo Dark Blue, CTA Dark Blue. Blue: text White, logo White, CTA Pink. Inside a UI card: Dark Blue text, Pink logo.
- Layout inside a slide: one auto-layout frame `Layout` at the safe area (vertical, gap 34; 24 on `.kp-tight` slides), holding in order what the page's `.kp-lay` holds: Track?, Logo?, Copy (vertical auto layout, gap 22, hug), Stage (the visual, fills the rest). Stage children can be absolutely positioned inside the Stage frame.

## Working rules

1. Build **inside the existing frames only**. Do not create, rename, move or resize sections or slide frames. Do not add frames outside them.
2. Use the components and styles above. Bind every fill/stroke to a Katapult variable. No hardcoded hex, no tints, no shadows, no blur, no opacity tricks.
3. Text blocks in auto layout (`figma.createAutoLayout`), wrapping text with `textAutoResize='HEIGHT'` and a fixed or FILL width. Every text node uses a `Katapult/*` text style.
4. Copy **verbatim** from copy.md: same words, case, punctuation, symbols and emoji. No retyping from memory, no edits. Only the text the page shows for that slide. **No extra text** (no captions, labels, numbers or UI text that the page does not have). Placeholder labels in Photo/Cutout/Icon components use the page's own label for that slot.
5. **No Bounce lines**: no arcs, no dotted or solid support lines. Motion comes from composition.
6. **Logo never on a photo**: only on a solid ground or inside a solid card. Use only the Logo component variants, never redraw or recolor. Keep clear space of its x-height (about 32px at 250 wide) on every side.
7. Name every layer (`Layout`, `Copy`, `Headline`, `Subhead`, `Body`, `CTA`, `Stage`, `Card`, `Photo · ...`). No "Frame 123" or "Rectangle 4".
8. Keep essential content inside the safe area; unhide the guide to check, then hide and re-lock it.
9. Figma mechanics (from the Designer discipline notes): after resizing/rotating anything, screenshot to confirm; after `.clone()` check `.parent.id`; verify by screenshotting the **section** (container), not just your node; never call resize on a section; after any text change, recheck fixed-position siblings for collisions; prefer the template's full type size over shrinking text to fit.
10. Return the node IDs you create. When done, screenshot each of your sections and compare side by side with the page's slide.


## Frame count check

The approved page has 52 canvases: p01 5, p02 5, p03 6, p04 5, p05 5, p06 5, p07 1, p08 1, p09 1, p10 1, p11 1, p12 1, p13 5, p14 5, p15 5. The scaffold reported 53 frames: each builder checks its sections and deletes any frame that is not in this list.
