# Tom's of Maine · Module inventory · Figma LAB (Jul to Sep 2026)

Source: Figma file **Progressive Global LAB** (`D8FpNuKI3uPGjCPqonIn3C`), page `t` (`407:656`), the **20 approved emails of July, August and September 2026**. Read on 2026-10-06 through the Figma plugin API, read-only (nothing was changed in the file). Companion files:

- October inventory (other file, ids `T..`): `figma-modules.md` in this folder. Where a LAB module matches an October one, it says so.
- Module screenshots (600 wide, gitignored): `../references/lab-<module-id>-<mm-dd>.png`.
- Image bank (every raw image fill, deduplicated, plus vector seals and decoratives): `../../photos/figma-lab/` and its `index.md`.

## How to read this document

- Every Figma frame is **1200 px wide = 2x**. **Every px value below is already halved to the 600px email** unless it says "2x". Figma line heights in % are converted (e.g. NK 128/90% at 2x = 64/57.6 here).
- "rel y" = offset from the top of the module/band; "abs y" = offset from the top of the email.
- Font names: **NK** = New Kansas, **Rubik**, **Gotham** (legacy SFMC template, nav, footer and most hero CTAs).
- Emails are referred to by date (7.1 … 9/27) and node id. Only rendered layers were measured; hidden layers and off-canvas frames (`_Layer_`, `Frame 1410127836`, the 7.3/7.5/9/27 `Build My Bundle` buttons placed far below the frame) are ignored. Those are leftovers outside the clip, not part of the design.
- Effects named **GLASS** are Figma's glass effect (radius, depth, refraction 1, light angle -45, intensity 0.8, dispersion 1, splay 1). They exist only in Figma and are baked into the slice.
- Token names refer to `tokens.json`. "NEW" = not in tokens.json. Where the October inventory already proposed a name (`kicker_*`, `intro_*`, `card_name_*`, `text_card` …) the same name is reused.

## The 20 emails

| Date | Email | Frame | Content frame | Height (600) | Slices |
|---|---|---|---|---|---|
| 7.1 | Fourth of July Sale Early Access | `408:7058` | `408:7059` | 2528.5 | 8, header sliced |
| 7.3 | Fourth of July Sale Announcement | `408:7256` | `408:7257` | 2608.5 | 9, header sliced |
| 7.5 | Fourth of July Sale Last Call | `408:7395` | `408:7396` | 2842 | 9, header sliced |
| 7.8 | National Parks & Recreation Month | `408:7837` | `408:7838` | 2351.5 | 7 |
| 7.15 | National Clean Beauty Day | `408:7927` | `408:7928` | 2688.5 | 7 |
| 7.23 | Your Everyday Essentials, Bundled | `408:8029` | `408:8030` | 2796 | 9 |
| 7.28 | Stay Fresh Outside This Summer | `408:8137` | `408:8138` | 2728.5 | 9 (named `july_8-28_0n` by mistake) |
| 8/3 | Stay Fresh Outside This Summer | `408:5530` | `408:5531` | 2225.3 | 10 |
| 8/6 | National Fresh Breath Day | `408:5879` | `408:5880` | 3102 | 7 |
| 8/10 | Back to College Essentials | `408:6115` | `408:6116` | 3773.8 | 14 |
| 8/12 | Nature Never Takes a Vacation | `408:6257` | `408:6258` | 3073 | 7 |
| 8/15 | National Relaxation Day | `408:6452` | `408:6453` | 3448.5 (content ends 3285.7) | 7 |
| 8/20 | Stay Fresh, Naturally Confident | `408:6960` | `408:6961` | 3271.8 | 7 |
| 8/24 | End of Summer Reset | `408:6361` | `408:6362` | 2587 | 7 |
| 9/3 | Labor Day Early Access | `408:5076` | `408:5077` | 3266.5 (clips the footer) | 10 |
| 9/4 | Labor Day Sale Is Live | `408:4844` | `408:4845` (named "7.8 Email…") | 2923 | 9 |
| 9/7 | Labor Day Savings End Tonight | `408:4960` | `408:4961` | 3067.5 | 9 |
| 9/11 | National Gum Care Month | `408:4617` | `408:4619` (inside `408:4618` "Email - 3") | 3193 | 5 |
| 9/16 | Everyday Essentials, Naturally | `408:5423` | `408:5425` (inside `408:5424`) | 2789.5 | 7 |
| 9/22 | First Day of Fall | `408:5308` | `408:5309` | 2868.5 | 8 |
| 9/27 | Adventure Awaits | `408:5202` | `408:5203` (named "7.8 Email…") | 2929 | 8 |

Notes on frames: 9/4, 9/7, 9/22 and 9/27 outer frames are shorter than their content frame but do not clip, so they render whole. **9/3's outer frame clips at 3266.5**, cutting the footer legal bar (address, copyright and links lines are outside). 8/15's frame is 163 px taller than its content (empty below the footer).

---

## Module list

| ID | Module | Emails (node) | Freq. | October match |
|---|---|---|---|---|
| L01 | Header (logo + nav) | all 20 (`408:7060` …) | 20 | T01, identical |
| L02 | Announcement bar | 7.3 `408:7262` | 1 | none |
| L03a | Hero · photo + translucent navy panel, price-led | 7.1 `408:7064` | 1 | none |
| L03b | Hero · solid navy, price-led, rotated packshots | 7.3 `408:7264` | 1 | none |
| L03c | Hero · light silk texture, ruled kicker, product stage | 7.5 `408:7401` | 1 | none |
| L03d | Hero · glass card on photo | 7.8 `408:7843`, 8/15 `408:6458` | 2 | T02b |
| L03e | Hero · glass card, price-led | 9/4 `408:4851` | 1 | T02b variant |
| L03f | Hero · photo + overlapping teal tab panel | 7.15 `408:7933` + `408:8015` + `408:7937` | 1 | none |
| L03g | Hero · dark overlay on photo, product cluster straddling a dome | 7.23 `408:8035` | 1 | close to T02d |
| L03h | Hero · left-aligned text on photo, product on the right | 7.28 `408:8143`, 8/3 `408:5536` | 2 | none |
| L03i | Hero · light top fade on lifestyle photo, seal | 8/6 `408:5885` | 1 | none |
| L03j | Hero · gradient, headline top, photo left + text right | 8/10 `408:6121` | 1 | none |
| L03k | Hero · centered text on full photo, product cluster on the curve | 8/12 `408:6263`, 8/20 `408:6966`, 8/24 `408:6367` | 3 | T02d |
| L03l | Hero · price-led, left, light photo | 9/3 `408:5082` | 1 | none |
| L03m | Hero · sky, ghost price, product trio on a dome | 9/7 `408:4966` | 1 | none |
| L03n | Hero · text cap with wave over lifestyle photo, seal | 9/11 `408:4624` | 1 | none |
| L03o | Hero · aurora gradient, gradient headline, day icons | 9/16 `408:5430` (top part) | 1 | none |
| L03p | Hero · light top fade, product photo below | 9/22 `408:5314` | 1 | close to T02c |
| L03q | Hero · circle photo with leaf sprigs | 9/27 `408:5208` | 1 | T02a (no ring here) |
| L04 | Section heading (H2 + optional intro / subtitle) | 19 bands | 19 | T03 |
| L05 | Product card (grid tile), 6 skins | 14 emails | 14 | T04 |
| L06 | Product grid 2x2 | 7.1, 7.3, 7.5, 7.8, 8/10 (bundles), 8/20, 8/24, 9/27 | 8 | T05 (2x2 count) |
| L07 | Product grid 2x3 | 7.23, 7.28, 8/10, 9/3, 9/4, 9/7 | 6 | T05 |
| L08 | Product grid 2-up rows with day-part subheads | 9/22 `408:5337`, `408:5361` | 1 | none |
| L09 | Wide product card (odd last item) | 9/27 `408:5266` | 1 | none |
| L10 | Product row, alternating (split pill, product name + button) | 7.15 `408:7952` | 1 | T08 / T09 shell |
| L11 | Category row stack (split pill, "Shop category") | 8/15 `408:6622`, 9/16 `408:5441` | 2 | T09 |
| L12 | Comparison panel (dark container with 2 product cards) | 8/3 `408:5802` + `408:5803` | 1 | none |
| L13 | Claims grid 2x2 (benefit tiles with footnotes) | 8/3 `408:5827` | 1 | T10 (layout), T11 (content) |
| L14 | Review row (testimonial + product + button) | 8/6 `408:6037`, 8/12 `408:6280` | 2 | none |
| L15 | Routine steps (numbered outline cards, bleeding packshot) | 9/11 `408:4766`, `408:4782`, `408:4798` | 1 | T07 |
| L16 | Day-part subhead (icon + title) | 9/22 `408:5338`, `408:5362` | 1 | none |
| L17 | Offer intro with lifestyle photo (product highlight + offer + CTA) | 9/3 `408:5088` | 1 | none |
| L18 | SMS signup band | 8/15 `408:6658`, 8/20 `408:7014` | 2 | none |
| L19 | Band closing CTA | 19 emails (not 8/10) | 19 | T12 |
| L20 | Fine print "Excluding value bundles" | 7.1, 7.3, 7.5, 9/3, 9/4, 9/7 | 6 | none |
| L21 | Seals and badges (starburst seal, 15% off badge, step number) | 8/6, 8/15, 9/11; 7.1, 7.5; 9/11 | 6 | none |
| L22 | Dividers (wave, tall wave, dome/curve, scallop, arc stroke) | most emails | 17 | T13, T14 |
| L23 | Decor (leaves, ferns, fireworks, stars, sparkles, glows) | 11 emails | 11 | T15 |
| L24 | Kicker (eyebrow) treatments | all heroes | 20 | October "kicker" |
| L25 | Footer | all 20 | 20 | T18, identical |
| B01 | Button, standard | everywhere | | B01 |
| B02 | Button, small "shop now" | L05, L10, L11 | | B02 |
| B03 | Button, comparison (smaller) | 8/3 | 1 | none |

Screenshots: see each module. All are `../references/lab-*.png` at 600 wide.

---

## Slices per email (600 scale, top to bottom)

The emails ship as sliced images. Slices with a width of 300 are half-width card slices (cut on the 300 centreline, inside the gutter). **The footer is never sliced in any of the 20 emails. The header is sliced only in 7.1, 7.3 and 7.5**; in the other 17 the slices start at 110.5, so header and footer are presumably the fixed SFMC HTML wrapper.

| Email | Slices (y ranges) |
|---|---|
| 7.1 | 0-110 header · 110-916 hero · 916-1059 curve + heading · 4 x 300x375 cards (1059-1809) · 1809-1941.5 CTA · footer 1941.5 |
| 7.3 | 0-110.5 · 110.5-160.5 bar · 160.5-908 hero · 908-1134 hero bottom + heading · 4 x 300x373 (1134-1880) · 1880-2013 CTA (8.5 unsliced before the footer at 2021.5) |
| 7.5 | 0-110 · 110-710 · 710-1224 · 1224-1383.5 heading · **gap 6** · 4 x 300x388 (1389.5-2166) · 2166-2285 CTA (**overlaps the footer by 30**, footer at 2255) |
| 7.8 | 110.5-787.5 hero + dome · 787.5-927.5 heading · 300x356 x2 · 300x339 x2 (927.5-1622.5) · 1622.5-1764.5 CTA |
| 7.15 | 110.5-985.5 hero + tab + teal band · 985.5-1164 heading · 4 rows 1164-1361, -1566, -1771, -1976 · 1976-2101.5 CTA |
| 7.23 | 110.5-830.5 · 830.5-1004.5 · 300x340 x2 · 300x365 x2 · 300x350 x2 (1004.5-2059.5) · 2059.5-2209 |
| 7.28 | 111-747.5 · 747.5-891.5 · 300x376 x2 · 300x365 x2 · 300x350 x2 (891.5-1982.5) · 1982.5-2140.5 |
| 8/3 | 110.5-618 hero · 618-816.5 panel top · 300x343.5 x2 (816.5-1160) · 1160-1331 panel bottom + heading · 300x97 x2 · 300x98 x2 (1331-1526) · 1526-1638.5 CTA |
| 8/6 | 110.5-786 · 786-1008 · rows 1008-1350, -1697, -2042, -2385.5 · 2385.5-2515 |
| 8/10 | 110.5-700.5 · 700.5-924.5 · 300x382 x2 · 300x347 x2 · 300x381 x2 (924.5-2034.5) · 2034.5-2169.5 · 2169.5-2382.5 · 300x382 x2 · 300x422 x2 (2382.5-3186.5) |
| 8/12 | 110.5-910.5 · 910.5-1121 · rows 1121-1464, -1809, -2156, -2498 · 2498-2628 |
| 8/15 | 110.4-883 · 883-1114.9 · rows 1114.9-1385.6, -1656.2, -1951.9 · 1951.9-2099.9 · 2099.9-2698.7 SMS |
| 8/20 | 110.5-854 · 300x387 x2 · 300x417 x2 (854-1658) · 1658-1825.8 · 1825.8-2684.8 SMS |
| 8/24 | 110.4-896.6 · 896.6-1105 · 300x387 x2 · 300x417 x2 (1105-1909) · 1909-2000 |
| 9/3 | 111-920.5 · 920.5-1326.5 · 1326.5-1555.5 · 300x365.5 x2 · 300x367 x2 · 300x352.5 x2 (1555.5-2640.5) · 2640.5-2773.5 |
| 9/4 | 110.5-919 · 919-1117 · 300x365 x2 · 300x367 x2 · 300x352 x2 (1117-2201) · 2201-2336 |
| 9/7 | 110.5-1087.5 · 1087.5-1270 · 300x365 x2 · 300x367 x2 · 300x350.5 x2 (1270-2352.5) · 2352.5-2480.5 |
| 9/11 | 110.5-923 · 923-1542.5 step 1 · 1542.5-2024.5 step 2 · 2024.5-2484 step 3 · 2484-2606 CTA |
| 9/16 | 110.5-778 · 778-997 · rows 997-1268, -1538.5, -1809, -2064.5 · 2064.5-2203 |
| 9/22 | 110.3-1087.8 · 1087.8-1352.8 · 300x350.5 x2 · 1703.3-1800.8 subhead · 300x350.5 x2 (1800.8-2151.3) · 2151.3-2281.8 |
| 9/27 | 110.3-1060.3 · 1060.3-1282.8 · 300x365 x2 · 300x345.5 x2 · 1993.3-2213.8 wide card · 2213.8-2341.8 |

Pattern: the hero slice usually runs past the hero band and includes the curve/wave and sometimes the section heading. Half-width card slices start exactly at the grid top and end at the midpoint of the 15 row gap.

---

## L01 Header

All 20 emails, e.g. 7.1 `408:7060`. Screenshot `lab-L01-header-07-01.png`. **Identical to October T01** (same image hash, same positions).

| Element | Spec (600) |
|---|---|
| Band | 600 x 110.5, white `#FFFFFF` (rectangle `Rectangle 1`) |
| Logo | raster PNG `345d2351` (1368x1056 teal "The Original Tom's of Maine"), layer box **126.5 x 102.5 at x 43, y 7.5**, CROP transform scale 0.535/0.562, offset 0.221/0.183 (visible crop ≈ 732x594 of the source). Use `assets/logo-light.png` (253x205, already cropped) |
| Nav | one text layer, fixed box 325.5 x 22.5 at **x 252, y 53.5**, left aligned, **Gotham Bold 14 / auto, uppercase, `#00867D`** (`color.nav`, `type.nav_size`). Content `OUR MISSION      PRODUCTS      SHOP NOW`: items separated by **6 spaces** (no separate layers, no separators) |
| Divider under header | none |
| Variations | none across the 20 emails. Sliced as one image (0-110) only in 7.1, 7.3, 7.5 |

## L02 Announcement bar

7.3 `408:7262`, between header and hero. Screenshot `lab-L02-announcement-bar-07-03.png`.

- 600 x 50.5, fill **`#6EA1E0`** (NEW, July sky blue), clips content.
- Text: Rubik SemiBold **23.5/23.5** (47/100% at 2x), uppercase, white, centered, 535.5 box at x 32, y 16.5 rel. Copy: "The 4th of July Sale Is Officially Live". Token: NEW (closest `subtitle_size` 22).
- Own slice (110.5-160.5).

---

## L03 Hero family

Common to all heroes:
- Full width 600. Hero headline is New Kansas SemiBold, tracking -1% to -7%, line 80 to 100%. Body is NK Medium 19.5/23.4 (or 20/24), tracking -1% (`body_*` / October `intro_*`).
- Hero CTA is **B01** (50.3 to 50.5 tall, radius 11.7). **Label font: Gotham Bold 20.7/29.6 uppercase on 16 heroes; Rubik Bold 20.7/29.6 on 8/3 and 8/10.** White fill on every hero except 7.5 (`#24436F` fill).
- Several heroes end with a white or colored curve/dome/wave (L22) that is part of the hero slice.
- "Excluding value bundles" (L20) sits 11.5 under the CTA on sale heroes.

### L03a Photo + translucent navy panel, price-led (7.1 `408:7064`)
Screenshot `lab-L03a-hero-photo-navy-panel-price-07-01.png`. Hero 110.5-936 (825.5 tall).
- Background: photo `9b600841` poppy field (`lifestyle-poppy-wildflower-field.png`), CROP. (Bottom fill `5e961c38` rainbow field is covered.)
- Panel: 535.5 x 608.5 at x 32, rel y 57.5, `#295791` at **90% opacity**, radius **35**.
- Stack inside the panel (centered): 5 white stars 126 x 22 (each 22, gap 4) rel y 94 → kicker Rubik SemiBold **20/20** uppercase white rel y 136.5 ("4th of July early access unlocked") → price headline **NK SemiBold 120.4/96.3, -7%**, white, 2 lines, rel y 172.5, box 505.5 x 190 ("15% OFF / sitewide": "OFF" uppercase via text case) → sub **NK SemiBold 41.9/46.1, -5%** white rel y 375.5 ("before the sale goes live") → body NK Medium 19.5/23.4 -1% white, 481.5 wide, 4 lines, rel y 442.5 → CTA white **322 x 50.5**, rel y 557.5, Gotham Bold 20.7/29.6 **`#285488`** (NEW) "Shop Early Access" → L20 fine print white rel y 619.5.
- Packshots bleeding off both edges, each with a 5-layer soft drop shadow toward bottom-left (offsets (-2.8,3.4) blur 9.5 30%, (-11.1,13.4) blur 17.2 ~20%, (-24.5,30) blur 23.3 ~10%, (-43.9,53.4) blur 27.8, (-68.4,83.4) blur 30, last two under 5%): Lemon Bergamot bar 182 x 152 rotated -26.8° at x 472, rel y 210.5; Moonlit Meadow deodorant 275 x 275 FIT rotated -30.1° at x -112.5, rel y 193.5.
- Bottom: white ellipse (2933.5 diameter) whose top sits at rel y 767 → white curve into the next band (L22 dome).

### L03b Solid navy, price-led, rotated packshots (7.3 `408:7264`)
Screenshot `lab-L03b-hero-navy-price-packshots-07-03.png`. Hero 161-1011 (850).
- Background: solid `#24436F` (fill on top of covered photo `5e961c38`).
- Decor: 3 fern line-art drawings `#CCFFFA` (Vrstva_1: 153.5x233.5 left, 478x517.5 top, 217.5x220 right). Same family as October fern sprig.
- Stack (centered): 5 stars rel y 190.5 → headline **NK SemiBold 120/108 (90%), last line 96 (80%), -7%**, white, 3 lines "Enjoy / 15% OFF / sitewide", rel y 234.5, box 505.5 x 301 → body NK Medium 19.5/23.4 white 390.5 wide rel y 556 → CTA white 322 x 50.5 rel y 647.5, Gotham `#285488` "Save Now" → L20 rel y 714.5.
- Packshots with the same 5-layer shadow: Antiplaque toothbrush pack 372.5 x 515 rotated 24.7° top-right (x 358.5, rel y -18), Lemon Bergamot bar 260.5 x 172 rotated 8.4° top-left (x -27, rel y 32.5).
- Bottom: ellipse `#6EA1E0` 2223 x 1666.5 with top at rel y 783.5 (curve into the blue band) + a second ellipse with **1px white stroke** 21.5 lower (thin white arc line, L22).

### L03c Light silk texture, ruled kicker, product stage (7.5 `408:7401`)
Screenshot `lab-L03c-hero-light-framed-eyebrow-product-stage-07-05.png`. Hero 110.5-1205.5 (1095).
- Background: white + `texture-white-silk.png` (`342be518`) at **40%**. White glow ellipse 460.5 x 295, layer blur 107, behind the headline.
- Ruled kicker: two rules **442.5 x 1.5 `#295791`** at rel y 71 and 111.5; text Rubik SemiBold **22/22** uppercase **`#24436F`**, left aligned in a 419.5 box at x 90.5, rel y 85.5 ("Your 4th of July Savings End Soon").
- Headline **NK SemiBold 74.5/68.5 (92%), -6%**, `#295791`, with "15% OFF" in **`#6EA1E0`** uppercase, 4 lines, rel y 138.5, 509 wide.
- Body NK Medium 19.5/23.4 `#295791` 414.5 wide rel y 429 → CTA **`#24436F` fill**, 322 x 50.5, rel y 511, Gotham label **`#EFEFEF`** (NEW) "Last Chance To Save" → L20 in `#24436F` rel y 576.5.
- Decor: 4 fireworks bursts (`#4A96D0`+`#295791`, `#295791`+`#6EA1E0`, red `#C00000`), 4-point sparkles `#295791` (14.5 and 27).
- Product stage: photo `37cfc1e9` (fireworks at night) 521.5 x 277.5, radius **35.5**, at x 41, rel y 671. Three packshots stand on it and overflow its top edge: Moonlit Meadow deodorant 126.5 x 237 (x 113), Wicked Cool! kids toothpaste 187 x 376.5 (x 212, from rel y 614), Cucumber Aloe deodorant 126.5 x 237 (x 356.5). Each has a black ellipse shadow (opacity 90%, layer blur 38.75) under its base.
- Bottom: standard wave (L22) `#295791`, 603.6 x 62.9, rel y 1032, into the navy grid band.

### L03d Glass card on photo (7.8 `408:7843`, 8/15 `408:6458`) · October T02b
Screenshots `lab-L03d-hero-glass-card-07-08.png`, `lab-L03d-hero-glass-card-08-15.png`.

| | 7.8 | 8/15 |
|---|---|---|
| Hero | 110.5-728 (617.5) | 110.5-883 (772.5) |
| Photo | forest trail `71d4a31f`, + `#05453D` 20% + linear top→bottom `#101E2F` 0% at 55% → 100% at 100%, whole layer 80% | sand dunes at purple sunset `557bac04`, no overlay |
| Glass card | 488.5 x 506 at x 56, rel y 46, fill **`#24436F` 20%**, radius 22.4, GLASS (radius 22 at 600, depth 100) | 529.5 x 374 at x 35, rel y 78, same fill/radius/effect |
| Kicker | none | Rubik Bold 20/20 uppercase white, rel y 115 |
| Headline | NK SemiBold **73.4/66.1, -4%**, white, 4 lines, rel y 86.5, 467.5 wide | NK SemiBold **64/57.6, -6%**, white, 2 lines, rel y 153 |
| Body | NK Medium 19.5/23.4 white 439.5 wide, rel y 367 | same, 408.5 wide, rel y 280 |
| CTA | white 262.6 x 50.3, rel y 458, Gotham **`#037E75`** | white 235 x 50.3, rel y 365, Gotham `#05453D` |
| Below the card | teal dome (L22) `#037E75` from rel y 629.5 | product group 186 wide (mouthwash, Whole Care carton, toothbrush pack, multi-layer shadows) centered under the card, seal L21 "National Relaxation Day" 189.6 rotated -18° right, 4 solid leaves `#00867D` (L23), standard wave `#E9F6FD` at rel y 709.7 |

### L03e Glass card, price-led (9/4 `408:4851`) · October T02b variant
Screenshot `lab-L03e-hero-glass-price-card-09-04.png`. Hero 110.5-917.5 (807).
- Photo: tropical leaves `9d582d8e` (`texture-tropical-leaves.jpg`) + linear top→bottom `#000000` 0% at 22% → `#05453D` 100% (end at 120%).
- Glass card 488.5 x 425.6 at x 56, rel y 53.5: rectangle radius 22.4 GLASS 22, under a Boolean subtract layer fill white 10%, stroke white 10% 1px, GLASS 50.
- Ruled kicker: rules **437 x 1.7 white** at rel y 84 and 132.5; Rubik SemiBold **25.2/25.2** uppercase white, left in the box, rel y 100 ("Time to restock the good stuff"). = October `kicker_*`.
- Price: two text layers "20%" and "OFF", **NK SemiBold 185.6/167 (90%), -4%**, white, centered, rel y 169.5 and 317.5 (line pitch 148).
- Below the card: body NK Medium 19.5/23.4 white with a bold run (NK Bold 19.5 "20% off sitewide.") 437.7 wide rel y 531.5 → CTA white 286 x 50.3 **Rubik** `#05453D` "Pack Your Essentials" rel y 640 → L20 rel y 714.5.
- Decor: 2 fern drawings `#CCFFFA` (163.5 x 192 left, 157.5 x 173.5 right). Bottom: standard wave white, rel y 745.5.

### L03f Photo + overlapping teal tab panel (7.15)
Screenshot `lab-L03f-hero-photo-teal-tab-panel-07-15.png`. Photo band 110.5-557.5, teal band 557.5-962.5.
- Photo: `d2c1268b` man applying North Woods deodorant (`lifestyle-man-applying-deodorant-forest.png`), 600 x 447, FILL.
- Tab panel `408:8015`: 517 x 234 at x 41.5, abs y 460.5 (overlaps the photo by 97), **`#00857A`**, radius **35**, GLASS 42. Headline NK SemiBold **53/47.7 (90%), 0%**, white, 3 lines, 482 wide, abs y 500.3. Kicker row abs y 656: white dash 21.9 x 3 left (x 33) + Rubik Bold **17.8/17.8** uppercase white ("Everyday routines made simple and effective") + dash right (x 545).
- Teal band `408:7937`: fill `#00857A` (texture `444d5db8` underneath, covered). Body NK Medium **20/24** -1% white 510.5 wide abs y 698 → CTA white **409.6 x 50.3**, abs y 800.5, Gotham **`#00857A`** "discover feel-good products".
- Bottom: ellipse `#F3F3F3` (top at abs y 928) → grey curve into the grey band.
- The panel color `#00857A` is guideline v4.3 "Tom's Teal" exactly (tokens use `#00867D` for nav).

### L03g Dark overlay on photo, product cluster straddling a dome (7.23 `408:8035`)
Screenshot `lab-L03g-hero-overlay-product-cluster-07-23.png`. Hero 110.5-708 (597.5) + cluster to 860.
- Photo: forest stream wide `83b7ff3e` + full rectangle `#05453D` **80%** with GLASS 2.
- Headline NK SemiBold **64.9/58.4, -5%**, white, 2 lines, 544.5 wide, rel y 70 → kicker *under* the headline: Rubik Bold **19.15/19.15** uppercase white rel y 194.5 → body 19.5/23.4 white 467.5 wide rel y 237 → CTA white 244 x 50.5 rel y 308.5, Gotham `#037E75` "shop bundles".
- Dome: ellipse 2239.5 x 2933.5, linear `#539D97` 0% → `#327B75` 10% → `#115953` 100% (top to bottom), top at rel y 475.5.
- Product cluster: `6577139e` three bar soaps, 569.5 x 375.5 at x 14, abs y 484.5 (straddles hero and green band); reflection strip = `1016e7ef` at **30%**, 569.5 x 25.5 at abs y 784.5.

### L03h Left-aligned text on photo, product on the right (7.28 `408:8143`, 8/3 `408:5536`)
Screenshots `lab-L03h-hero-left-aligned-photo-07-28.png`, `lab-L03h-hero-left-aligned-photo-08-03.png`.

| | 7.28 | 8/3 |
|---|---|---|
| Hero | 110.5-747.5 (637) | 110.5-618 (507.5), same frame continues into L12 |
| Photo | sunlit grass `d5e1e3b2` + linear `#332B0E` 0% at 71% → 90% at 100% (from bottom center toward top-left) + `#05453D` 20% | Whiten+ Coconut tube in water `8d329d2d` (subject right) + linear left→right `#044D44` 0% → `#079B89` 50% at 60% → `#09B39E` 0% at 66% + linear top→bottom `#008D84` 0% at 35% → 100% at 64% |
| Text column | x 53.5 | x 41 |
| Kicker | **above** headline: Rubik Bold 20/20 upper white, rel y 73.5, text shadows (0,2) blur 12 30% + blur 57 40% | **under** headline: Rubik Bold 20/20 upper white, 287 wide, abs y 327 |
| Headline | NK SemiBold **76.9/61.5 (80%), -7%**, white, left, 3 lines, rel y 117.5, 492.5 wide, drop shadow blur 47 40% | NK SemiBold **57/45.6 (80%), -4%**, white, left, 3 lines, abs y 171.3, 472 wide |
| Body | NK Medium 19.5/23.4 white left 351.5 wide rel y 325 (stacked drop shadows) | NK Medium **18/21.6** -1% white left 313 wide abs y 385 |
| CTA | white 308.6 x 50.3 at x 53.5 rel y 416, Gotham `#05453D`, **label left-aligned** in the button | white 263.6 x 50.3 at x 41 abs y 508, **Rubik** `#05453D` |
| Product | North Woods deodorant packshot 144 x 357 at x 402, abs y 363, straddling the white curve | in the photo |
| Bottom | white ellipse curve, top at abs y 674.5 | none (flows into L12 on the same teal) |
| Decor | none | leaf line-art `#3DA79D` 173.8 (right) and 124.8 (top-left) |

### L03i Light top fade on lifestyle photo, seal (8/6 `408:5885`)
Screenshot `lab-L03i-hero-light-fade-seal-08-06.png`. Hero 110.5-786 (675.5).
- Photo: woman laughing among wildflowers `e41a6bed` + linear top→bottom **`#E8E6E7` 100% to 27% → 80% at 51% → 0% at 64%** (solid light top for the text).
- Kicker **above**: Rubik Bold **26.7/26.7** uppercase **`#00867D`** rel y 43.5, 484 wide ("The MVP Of Your Summer Routine").
- Headline NK SemiBold **75/60 (80%), -1%**, `#00867D`, 2 lines, rel y 82, 495 wide (GLASS on the text layer).
- Body NK Medium 19.5/23.4 `#00867D` 407 wide rel y 223.5 → CTA white 230.6 x 50.3 rel y 336, Gotham `#05453D` "Shop Oral Care". White button on a light-grey zone (low contrast edge).
- Seal L21 "National Fresh Breath Day" 160 (319.8 at 2x), rotated -11.9°, at x 441, abs y 430.5.
- Bottom: ellipse `#008D83`, top at abs y 748 → teal curve.

### L03j Gradient, headline top, photo left + text right (8/10 `408:6121`)
Screenshot `lab-L03j-hero-split-gradient-photo-text-08-10.png`. Hero 110.5-702.5 (592).
- Background: linear top→bottom `#008D83` → `#05453D` (end at 125% of the height).
- Headline NK SemiBold **69.15/62.2 (90%), 0%**, white, centered, 2 lines, 528 wide, rel y 43.5 (GLASS on the text). Kicker under: Rubik Bold **24/24** uppercase white, 2 lines, 342 wide, rel y 174.5.
- Split row at rel y 243.5: photo `33f1fef4` backpack, **218 x 270.5, radius 12**, at x 35.7; gap 28; text column x 282, 286 wide: body NK Medium 19.5/23.4 white **left**, 264 wide, rel y 273.8 → CTA white **286 x 50.3** (full column width), rel y 433, Rubik `#05453D` "Pack Your Essentials".
- Bottom: standard wave `#05453D` at abs y 642 (wave rising into the dark band).

### L03k Centered text on full photo, product cluster on the curve (8/12, 8/20, 8/24) · October T02d
Screenshots `lab-L03k-hero-photo-centered-product-straddle-08-12.png`, `-08-20.png`, `-08-24.png`.

| | 8/12 `408:6263` | 8/20 `408:6966` | 8/24 `408:6367` |
|---|---|---|---|
| Hero | 110.5-925 (814.5) | 110.5-814 (703.5) | 110.5-933.5 (823) |
| Photo | forest trail warm light `2c8ddb1e`, no overlay | beach + dunes `2080f378` (covered `dd75fecb` under it) | pastel sunset sea `3164af2f` |
| Text color | white | white | **`#008D83`** (dark text on light sky) |
| Kicker | under headline, Rubik Bold 20/20 upper, rel y 294 | under headline, **ruled**: rules 465.5 x 1.2 white at rel y 184.5 and 217.5, Rubik SemiBold **17.8/17.8** upper, rel y 195.5 | under headline, Rubik Bold 20/20 upper, rel y 202 |
| Headline | NK SemiBold **64/57.6, -7%**, 2 lines, 436 wide, rel y 167 | NK SemiBold **60.25/55.4 (92%), -6%**, 2 lines, 505 wide, rel y 66 | NK SemiBold **74.5/68.5, -6%**, 2 lines, 492.5 wide, rel y 56.5 |
| Body | 19.5/23.4, 338.5 wide, rel y 332 | 19.5/23.4, 420 wide, rel y 245.5 | 19.5/23.4, 493 wide, rel y 243.5 |
| CTA | white 235 x 50.3 Gotham `#05453D`, rel y 417 | **none** | white 235 x 50.3 Gotham `#05453D`, rel y 347.5 |
| Product | cluster `8e2291a3` (2 deodorants + Creamy Coconut bar) 347 x 347 at x 126.5, abs y 578 | trio: Twilight Breeze 308.3, **Tropical Island 331.4 (front, center)**, Moonlit Meadow 304.4, in a 481.4 x 331.4 group at x 60.8, abs y 472; duplicated bottom strip carries a 5-layer grounding shadow (0,2.5 blur 6 30% … 0,67.5 blur 19) | toothbrush pack (rot 25.7°), Deep Forest deodorant 133 x 328, Lemon Bergamot bar 197.5 x 116, group 297.7 x 385 at x 151, abs y 483, same grounding shadow |
| Bottom | white curve (ellipse top abs y 736.5) | **tall wave** `#05453D` 603.6 x 166.9 at abs y 715.5 | ellipse `#008D83`, top abs y 732.5 |

### L03l Price-led, left, light photo (9/3 `408:5082`)
Screenshot `lab-L03l-hero-price-left-light-09-03.png`. Hero 110.5-745.5 (635).
- Fills: `#EEEFF5` + photo `12e03f86` (Whiten+ tube squeezing foam, subject right) + linear left→right `#EEEFF5` 100% at 29% → 0% at 42% + linear top→bottom `#EEEFF5` 100% at 22% → 0% at 33%.
- Left column x 43: kicker Rubik Bold 20/20 upper `#05453D` 2 lines 247 wide, rel y 56 → price **NK SemiBold 183.85/147.1 (80%), -7%**, `#05453D`, left, "20% / OFF", rel y 109 (GLASS on text) → "sitewide" **NK SemiBold 54.35/48.9, -7%** rel y 406 → fine print **Rubik Italic 10/12, -1%**, `#05453D`, rel y 463.5.
- Solid leaf `#008D83` 192 x 192 rotated 155.9° bottom-right (L23).
- **No CTA in the hero**: the CTA is in the next band (L17).

### L03m Sky, ghost price, product trio on a dome (9/7 `408:4966`)
Screenshot `lab-L03m-hero-sky-price-product-trio-09-07.png`. Hero 110.5-1087.5 (977).
- Photo: blue sky with clouds `9bf67fbc`.
- Kicker Rubik Bold 20/20 upper white rel y 64.5 ("Tonight Your Savings Disappear") → short rule **45.8 x 2, white, radius 36**, centered, rel y 102.5 → pre-line NK SemiBold **45.85/41.3, -7%, white 60%** rel y 128.5 → price "20%OFF" **NK SemiBold 125.25/112.7, -3%, white 50%** (GLASS) rel y 177 → "sitewide" NK SemiBold **80.2/72.2, -7%, white 60%** rel y 282 → body NK Bold + Medium 19.5/23.4 white ("Your 20% off ends tonight" bold) 467.5 wide rel y 363 → CTA white 303 x 50.3 Gotham `#05453D` rel y 424.5 → L20 white rel y 499.
- Product trio 572.6 x 400.4 at x 19.6, rel y 548.5: Whiten+ Peppermint carton rotated -75° (left), Fresh Mint mouthwash 405 x 400.4 radius 15.65 (center), Deep Forest deodorant rotated -15° (right).
- Dome: ellipse `#05453D` 1778 x 1208, top at rel y 667.5.

### L03n Text cap with wave over lifestyle photo, seal (9/11 `408:4624`)
Screenshot `lab-L03n-hero-text-cap-wave-photo-seal-09-11.png`. Hero 110.5-923 (812.5).
- Photo: man smiling holding toothpaste `597c86e3`.
- Cap: rectangle linear top→bottom **`#FFFFFF` → `#CCFFFA`**, 710 x 222.5 (clipped, covers hero top to abs y 311.3), ending in a standard wave `#CCFFFA` at abs y 311.3.
- Headline NK SemiBold **48/48 (100%), -7%**, `#05453D`, 2 lines, 460 wide, abs y 169.5 → kicker under: Rubik Bold 20/20 upper `#05453D` abs y 275.5. **No CTA.**
- Seal L21 "National Gum Care Month" 242 (484 at 2x), rotated -13.7°, at x 335.5, abs y 548.5.
- Bottom: standard wave **`#053832`** rotated 180° (hanging) at abs y 860.

### L03o Aurora gradient, gradient headline, day icons (9/16 `408:5430`, top part)
Screenshot `lab-L03o-hero-aurora-gradient-text-09-16.png`. Hero area 110.5-778 (one 2092-tall frame continues into L11).
- Background: linear `#24436F` → `#000B1A` (handles at 57%,57% → 100%,94%, so mostly `#24436F`), plus two blurred ellipses top-left: `#008D83` and **`#91FFF5`**, layer blur 204 (aurora glow).
- Kicker row abs y 175.8: sun icon 44.4 (`#C8EEEB` ring) + Rubik Bold **26.2/26.2** upper white, 2 lines, 278 wide + moon icon 44.4.
- Headline NK SemiBold **74.9/67.4, -7%** with a **gradient fill `#FFFFFF` → `#55B5AC`** (diagonal), 3 lines, 472 wide, abs y 252.3.
- Body NK Medium 20/24 -1% white 437 wide abs y 473 → CTA white **399 x 50.3** Gotham `#05453D` "Explore Everyday Essentials" abs y 615.
- From abs y 706 a giant wave-topped panel (`408:5435`, 741 x 1497, linear white 27% → `#008D83` 100%) covers the rest of the frame: L11 rows sit on it.

### L03p Light top fade, product photo below (9/22 `408:5314`) · close to October T02c
Screenshot `lab-L03p-hero-light-top-fade-product-photo-09-22.png`. Hero 110.5-1087.5 (977).
- Photo: three Whiten+ tubes standing with droplets `afe10c3f` + linear **`#9FD5F1` 100% to 39% → 0% at 43%** (hard edge, slightly diagonal): solid light-blue top for the text.
- Headline NK SemiBold **76.45/68.8, -2%**, `#05453D`, 2 lines, 606 wide, abs y 163 → kicker under Rubik Bold **20/26 (130%)** upper `#05453D`, 2 lines, 207 wide, abs y 315.3 → body in **two paragraphs** NK Medium 20/24 `#05453D` (abs y 384.3 and 442.3, gap 20) → CTA white 308.6 x 50.3 Gotham `#05453D` abs y 509.3.
- Bottom: scallop divider `#55B5AC` (L22) at abs y 1015.4.

### L03q Circle photo with leaf sprigs (9/27 `408:5208`) · October T02a (without the ring)
Screenshot `lab-L03q-hero-circle-photo-09-27.png`. Hero 110.5-1058.5 (948).
- Background: sunset sky `14d60c6e` + ellipse 1258 diameter, linear `#008D83` 100% → 0% at 61% (teal glow from the top).
- Headline NK SemiBold **76.45/68.8, -7%**, `#05453D`, 2 lines, 540 wide, abs y 164.
- Circle photo: ellipse **371 diameter** at x 115, abs y 322.5, image `3819e794` hiker backpack. **No ring** (October T02a has a 6.5 `#00867D` ring).
- Leaf sprigs `#05453D` 189 x 212.6, rotated -11° (x -30.5, abs y 275) and 169° (x 441, abs y 515).
- Ruled kicker under the circle: rules **327 x 1.7 `#05453D`** at abs y 727.8 and 801; Rubik SemiBold **25.2/25.2** upper `#05453D`, centered, 2 lines, 371 wide, abs y 744.
- Body NK Medium 20/24 `#05453D` 461 wide abs y 826.8 → CTA white 301 x 50.3 Gotham `#05453D` abs y 912.8.
- Bottom: standard wave `#05453D` rising, abs y 997.3.

---

## L04 Section heading

Every body band except 8/20's grid band. Screenshots `lab-L04-section-heading-07-01.png`, `lab-L04-section-heading-08-12.png`. October T03.

- H2: **NK Bold 42/44.1 (84/105%), tracking 0**, centered (`h2_*`). Text layers are often typed in Title Case and shown in sentence case through text case (first character UPPER segment + LOWER segment), e.g. 7.3 "Refresh your shelf with everyday favorites".
- H2 colors: `#24436F` (7.1, 7.3), white (7.5, 7.8, 7.23, 8/3, 8/6, 8/10, 8/24, 9/3, 9/7, 9/11, 9/22, 9/27), `#05453D` (7.28, 9/4), **`#00857A`** (7.15), `#044D44` (8/12, 8/15), `#008D83` (9/16).
- Intro (optional): NK Medium 20/24 -1% (most) or 19.5/23.4, same color as the H2 or `#05453D`, centered, 280 to 525 wide.
- Rubik subtitle (8/3 panel only): Rubik Bold **22.3/29 (130%)** upper white (`subtitle_*`).
- Spacing: band top → H2 **0 to 60** (7.1: 21.5, 7.8: 81, 8/12: 0, 9/4: 81, 9/27: 41.5); H2 → intro **20** (8/12, 9/3), 15 (7.15), 24 (9/22); intro or H2 → first card/row **23 to 45.5** (7.1: 45.5 from H2; 8/12: 40 from intro; 9/3: 35.5).

---

## L05 Product card (grid tile) · October T04

One spec, **6 skins**. All cards are 2-column grid tiles, radius 20 (S1: 15), image on top, product name, button. Screenshots in L06/L07.

### Geometry (Rubik-name cards and mint NK cards: 7.1, 7.3, 7.5, 7.8, 7.23, 7.28, 9/3, 9/4, 9/7, 9/22, 9/27)
- Card **253 wide**, height 330 to 368 (cards in one row can differ by 2 to 5).
- Padding top **26.5** (image top), bottom **26.5** (button bottom to card bottom).
- Image box centered: **169.5 x 167.5** for boxes and sticks (FILL), **212 x 167.5** for wide cartons (FIT), 169.5 x 169.5 for mouthwash/floss (mouthwash radius 12), 230 x 149 or 236 x 147 (7.1, 7.3 wide cartons), 253 x 169.5 full-bleed carton (7.28 whiten).
- Gap image → name **20**. Name column 220.5 wide.
- Gap name → button **10.75**.
- Button: B02 small 139 x 42.8, centered (wide label "SHOP 15% OFF" in 7.3: **165 x 42.8**).

### Geometry (white NK cards: 8/10, 8/20, 8/24)
- Card **243.5 wide**, gutter **10.3**, row gap **10** (grid 497.3 wide at x 51.35), radius 20, height 336 to 377.
- Image 168.5 square (FILL) top inset **33**; or **221.5 square** inset 17.4 (bundle cards 8/10, 8/20, 8/24); flat cartons 168.5 x 73 pushed down to rel y 80.7.
- Gap image → name **18**, name → button **17.8**, button **B01 144 x 50.3** radius 11.7 (Rubik Bold 20.7/29.6 "SHOP NOW"), bottom padding 33.5.

### Skins

| Skin | Emails | Card fill / stroke | Name | Button |
|---|---|---|---|---|
| S1 outline navy + badge | 7.1 `408:7092` … | no fill, **stroke 1.5 `#24436F`**, radius 15 | Rubik Bold **18.1/18.1** upper **`#295791`** | B02 `#295791` |
| S2 lavender sheen | 7.3 `408:7330` … | linear `#578CFF` → `#E1EBEB` (covered) under **linear `#FFFFFF` 0% → `#ECEEFF` 51% → `#FFFFFF` 100%** (diagonal, handles 103%,6% → -11%,104%), no stroke | Rubik Bold 18.1 upper `#295791` | B02 wide `#295791` "SHOP 15% OFF" |
| S3 white | 7.5 `408:7663` …, 7.23 `408:8051` … | white (7.5: base gradient `#578CFF`→`#E1EBEB` covered by solid white) | Rubik Bold 18.1 upper `#295791` (7.5) / **`#29776F`** (7.23) | B02 `#295791` (7.5) / `#05453D` (7.23) |
| S4 mint sheen (= October T04) | 7.8, 9/3, 9/4, 9/7, 9/22, 9/27 | `#7DCDC5` → `#E1EBEB` (covered) under **`#FFFFFF` 0% → `#C8EEEB` 51% → `#FFFFFF` 100%**, same diagonal | 7.8: Rubik Bold 18.1 upper `#05453D`; Sep: **NK Medium 18/21.6 -1% `#044D44`**, sentence case (October `card_name_*`) | B02 `#05453D` |
| S5 outline teal | 7.28 `408:8159` … | no fill, **stroke 1.5 `#00867D`** | Rubik Bold 18.1 upper `#29776F` | B02 `#05453D` |
| S6 white, NK name, big button | 8/10 `408:6144` …, 8/20 `408:6988` …, 8/24 `408:6392` … | white, no stroke | **NK Medium 18/21.6 -1% `#044D44`** (one 17/20.4 in 8/20) | **B01 144 x 50.3** `#05453D` |

- Card heights follow the name length; names run 1 to 3 lines.
- S1 cards carry the **"15% OFF" badge** (L21) 91.6 x 40.85 at card x +150, y +7.5 (top-right, overlapping the image area). 7.5 S3 cards carry the same badge.

## L06 Product grid 2x2

Screenshots `lab-L06-grid-2x2-outline-navy-badge-07-01.png`, `lab-L06-grid-2x2-gradient-lavender-07-03.png`, `lab-L06-grid-2x2-white-on-navy-band-07-05.png`, `lab-L06-grid-2x2-mint-on-teal-dome-07-08.png`, `lab-L06-grid-2x2-white-bundle-nk-08-10.png`, `lab-L06-grid-2x2-white-deodorant-nk-08-20.png`.

- Grid **521 wide at x 39.5, 2 columns of 253, gutter 15, row gap 15** (S1 to S5). S6 grids: 497.3 wide at x 51.35, 243.5 columns, gutter 10.3, row gap 10.
- Band backgrounds by email:

| Email | Band | Fill | Heading | Closing CTA |
|---|---|---|---|---|
| 7.1 | `408:7087` 936-1941.5 | white | `#24436F` "Stay fresh all season long" | `#295791` 360 x 50.5 "Refresh Your Routine" |
| 7.3 | `408:7323` 1011-2021.5 | **`#6EA1E0`** + white ellipse 540.5 x 165 at 60% with layer blur 152 (glow under the curve) | `#24436F` | `#295791` 360 x 50.5 "Stock Up & Save" |
| 7.5 | `408:7659` 1205.5-2255 | **`#295791`** | white + intro white | **white** 360 x 50.5, label `#295791` "Shop Before It's Gone" |
| 7.8 | `408:7855` 728-1764.5 | photo `71d4a31f` + `#05453D` 20% + linear `#101E2F` 80% at 3% → `#00867D` 100% (whole fill 90%) under teal dome `#037E75` | white | white 360 x 50.5, label `#037E75` "Shop Outdoor Essentials" |
| 8/10 (bundles) | `408:6186` 2165-3187 | `#008D83`, dark wave hanging at the top | white | none |
| 8/20 | `408:6985` 814-1768 | `#05453D`, no heading | none | white 283 x 50.3 "shop all deodorants" |
| 8/24 | `408:6385` 933.5-2000 | `#008D83` | white + intro | white 242.6 x 50.3 "see more bundles" |

## L07 Product grid 2x3

Screenshots `lab-L07-grid-2x3-white-rubik-07-23.png`, `lab-L07-grid-2x3-outline-teal-07-28.png`, `lab-L07-grid-2x3-white-nk-leaves-08-10.png`, `lab-L07-grid-2x3-mint-gradient-band-09-03.png`, `lab-L07-grid-2x3-mint-white-band-09-04.png`.

Same geometry as L06 with 3 rows (6 products).

| Email | Band | Fill | Card skin | Closing CTA |
|---|---|---|---|---|
| 7.23 | `408:8045` 708-2209 | linear top→bottom **`#539D97` → `#327B75` 50% → `#115953`** (two stacked copies, plus `#F3F3F3`/`#539D97` underneath) | S3 white, `#29776F` names | white 360 x 50.5 label `#037E75` "Bundle & Save" |
| 7.28 | `408:8154` 747.5-2140.5 | white | S5 outline teal | **`#037E75`** 222 x 50.5 white label "Stay Fresh" |
| 8/10 | `408:6138` 702.5-2165 | `#05453D` + solid leaves `#91C9C6` top-left and bottom-right | S6 | white 136 x 50.3 "Shop All" |
| 9/3 | `408:5104` 1326.5-2773.5 | linear top→bottom **`#05453D` → `#0CAB97`** | S4 NK | `#05453D` 216.6 x 50.5 "Stock Up & Save" |
| 9/4 | `408:4871` 917.5-2336 | white | S4 NK | `#05453D` 379.6 x 50.5 "Explore Everyday Essentials" |
| 9/7 | `408:4986` 1087.5-2480.5 | `#05453D` → `#0CAB97` | S4 NK | white 200.6 x 50.5 "Don't Miss Out" |

## L08 Product grid 2-up rows with day-part subheads (9/22)

Screenshot `lab-L08-grid-2up-day-part-subheads-09-22.png`. Band `408:5331` 1087.5-2281.5, linear top→bottom **`#55B5AC` 0% → `#00867D` 30% → `#295791` 63% → `#24436F` 100%** (teal into navy).
- H2 white "Everything you need for the season ahead" + intro white 303 wide.
- Two blocks (`408:5337`, `408:5361`), each = L16 subhead + one row of two S4 NK cards (253 x 350, gutter 15). Block 1 at abs y 1290.8, block 2 at 1738.6 (gap 35.5 between the cards of block 1 and subhead 2).
- Closing CTA white 320.6 x 50.5 "Explore Fall Essentials".

## L09 Wide product card (odd last item) (9/27 `408:5266`)

Screenshot `lab-L09-grid-2x2-plus-wide-card-09-27.png` (whole band). Band `408:5227` 1058.5-2342, linear top→bottom `#05453D` → `#008D83`.
- 2x2 S4 NK grid, then one **521 x 220.5** card (radius 20, same mint sheen) at abs y 1993.3: image 169.5 x 167.5 at card x +55.5, y +26.5; text column 220.5 wide at card x +245, vertically centered: name NK Medium 18/21.6 `#044D44` centered + B02 `#05453D` 10.75 below.
- Own full-width slice (1993.3-2213.8).

## L10 Product row, alternating (7.15 `408:7952`) · October T08/T09 shell

Screenshot `lab-L10-product-row-alternating-07-15.png`. Band `408:7947` `#F3F3F3`, 962.5-2101.5.
- 4 rows **498.5 x 189.5, radius 40, clip**, at x 50.75, gap 15 (abs y 1164, 1368.5, 1573, 1777.5).
- Photo half: product still life 264.5 to 279.5 wide (layer overhangs and is clipped): `2e5990f7` North Woods with lavender, `4b14fa13` Tropical Island with coconut, `4753eafc` Whole Care on stones, `be419ad1` Whiten+ in leaves.
- Panel half 234 to 264.5 wide, mint sheen gradient (S4). Centered: name Rubik Bold 18.1/18.1 upper `#05453D` (2 to 4 lines) → gap 15.75 → B02 `#05453D`.
- Alternation: photo left (rows 1, 3), photo right (rows 2, 4). One slice per row (1200 x 394 to 410 at 2x).
- Closing CTA **`#00857A`** 196 x 50.5 white label "shop all".

## L11 Category row stack (8/15 `408:6622`, 9/16 `408:5441`) · October T09

Screenshots `lab-L11-category-row-08-15.png`, `lab-L11-category-row-09-16.png`.
- Rows **498.5 x 255.6, radius 40, clip**, at x 50.75, gap 15 (3 rows in 8/15, 4 in 9/16). Split at x 314.8: photo 279.5 wide (layer starts 15 outside, clipped), panel 234 to 264.5.
- Panel content centered: "SHOP / Category" Rubik Bold 18.1/18.1 upper (2 lines) → 15.8 → B02.

| | 8/15 | 9/16 |
|---|---|---|
| Band | `408:6617`, linear top→bottom **`#E9F6FD` → `#B9EBFF`** (sky), H2 + intro `#044D44` | on the 9/16 wave panel (white → `#008D83`), H2 + intro **`#008D83`** |
| Panel | **`#05453D`**, white label, **B02 white fill, `#05453D` label** | mint sheen (S4), `#05453D` label, B02 `#05453D` |
| Photo | lifestyle, one per row (visible top fill): man brushing (`8cbf9588`, transparent cut-out on light), hand + bar soap (`da223180`), woman with deodorant (`6a953e40`) | one bathroom-shelf photo `60b7101c` with a different CROP per row; Value Bundles row `cba61179` |
| Packshot over the seam | yes: oral-care group 119.5 x 184 (mouthwash + carton + brush), Fragrance Free bar 168 x 168, Clean Coast deodorant 184.5 x 185 | no |
| Rows | Oral Care, Bath & Body, Deodorant & Antiperspirant | Oral Care, Bath & Body, Deodorant & Antiperspirant, Value Bundles |
| Closing CTA | `#05453D` 317.6 x 50.5 "Make Time For Self-Care" | white 254 x 50.3 "SHOP ALL PRODUCTS" |

## L12 Comparison panel (8/3 `408:5802` + `408:5803`)

Screenshot `lab-L12-comparison-panel-2up-08-03.png`. Sits on the 8/3 hero teal (abs y 618-1160).
- Container: **520 x 542, radius 24, `#044D44`**, at x 40.5, abs y 618.
- H2 NK Bold 42/44.1 white, 377 wide, rel y 40 ("Relief, whitening or both?") → subtitle **Rubik Bold 22.3/29 (130%)** upper white, 311.5 wide, rel y 134.
- Two cards **231.85 x 327.2, radius 18.35**, mint sheen (S4), at x 61.75 and 307.35 (**gap 13.75**), rel y 198.5. Card: image 207.3 x 155.6 FIT (inset 12.3 sides, 24.3 top) → name **NK Medium 16/19.2 -1% `#044D44`** sentence case, 202 wide, card rel y 198 → **B03** button 127.5 x 39.2, radius 9.25, `#05453D`, Rubik Bold **16.6/16.6** upper white, card rel y 263.7 → bottom padding 24.3.
- Container padding: 21 sides to the cards, 40 top, 24.3 bottom.

## L13 Claims grid 2x2 (8/3 `408:5827`) · October T10 layout, T11 content

Screenshot `lab-L13-claims-grid-2x2-08-03.png`. Band `408:5823` **`#008D84`**, abs y 1195-1638.3.
- H2 white "Sensitive care made for real life" 381.75 wide, rel y 32.
- Tiles **255 x 92.5, radius 22.4**, fill linear top→bottom **`#7DCDC5` → `#FFFFFF`** (start 77% above the top, so mostly pale), no stroke. Grid 520 wide at x 40, **gutter 10, row gap 10** (rows at abs y 1331, 1433.5).
- Claim: **NK Medium 15/18 -1% `#05453D`**, centered, 202.6 wide (169 for the 3-line one), tile rel y 32 (or 23 when 3 lines).
- Footnote under the claim: **NK Medium 7.5/9 -1% `#05453D`** ("*with continued use", "*Calcium Carbonate"), tile rel y 79. **Below any legal minimum** (open question).
- CTA white 368.6 x 50.3 Rubik `#05453D` "Explore Sensitive Solutions", abs y 1556.

## L14 Review row (8/6 `408:6037`, 8/12 `408:6280`)

Screenshots `lab-L14-review-row-light-08-06.png`, `lab-L14-review-row-teal-08-12.png`.
- Row **521 x 338.1, radius 20**, stacked with **gap 8** (4 rows), at x 39.5.
- Image box **145.5 x 274.1, radius 12**, white fill + packshot (CROP), padding **32** from the row edge.
- Text column 293 wide (313.5 in 8/12), **gap 20** from the image. Stack: product name **Rubik Bold 20/20 upper** (2 to 3 lines) → 20 → quote **NK Medium 18/21.6 -3%** with curly quotes (`caption_*`) → 20 → reviewer **Rubik Bold 16/16 upper**, prefixed "- " (e.g. "- lsgtorie") → 20 → B01 144 x 50.3 `#05453D` Rubik "shop now".
- Alternation: image left (rows 1, 3), image right (rows 2, 4).

| | 8/6 | 8/12 |
|---|---|---|
| Band | `#008D83`, H2 white "Loved by thousands of smiles" + intro white | white, H2 + intro `#044D44` "The reviews came along for the ride" |
| Row fill | linear top→bottom **`#E9F6FD` → `#B9EBFF`** | solid **`#008D84`** |
| Text color | `#044D44` | white |
| Image right inset | 32 | **10** (asymmetric, image at x 405 vs 71.5 on the left rows) |
| Closing CTA | white 332.6 x 50.3 "shop customer favorites" | `#05453D` 248.6 x 50.3 "Pack Your Routine" |

## L15 Routine steps (9/11) · October T07

Screenshot `lab-L15-steps-routine-09-11.png`. Three bands, one slice each (abs y 923-1541.5, 1541.5-2024.5, 2024.5-2606).
- Each band: linear top→bottom **`#05453D` 0% to 57% → `#0CAB97` 100%** (band 1 adds black 20%). Each band ends with a standard wave `#05453D` rotated 180° hanging into the next band.
- Band 1 H2 white "3 steps your gums will thank you for", 398.5 wide.
- Step card: **521 wide, no fill, stroke 2 `#008D84`, radius 20**, height 195.5 / 174 / 198, padding **32**.
  - Number badge: scalloped star **39 x 39 `#70D8CE`**, radius 5.85, numeral Rubik Bold **19/19** `#05453D` → gap 4 → step title **Rubik Bold 24.35/24.35 upper `#70D8CE`** (`label_*` size, NEW color).
  - Gap 15 → body **NK Medium 18/21.6 -3% white**, 332.5 wide (299 in step 2).
- Below each card (outside it): product name **Rubik Bold 24.35/24.35 upper white**, 2 to 3 lines, 36 below the card → 24 → B01 white 144 x 50.3 Rubik `#05453D` "Shop Now".
- Bleeding packshot on the side opposite the text: toothbrush pack 637 square rotated -25.7° (right), floss 332.5 square rotated 20.4° (left, text column shifts to x 196.5 / 253), mouthwash 409.5 x 404.6 (right).
- Closing CTA white 386.6 x 50.5 "Explore Oral Care Essentials".

## L16 Day-part subhead (9/22 `408:5338`, `408:5362`)

Shown inside `lab-L08-grid-2up-day-part-subheads-09-22.png`.
- Icon **50.2 x 50.2** (sun-and-cloud or moon, `#C8EEEB` line icon in a ring) + gap 12.2 + **NK SemiBold 30.35/27.3 (90%), 0%, `#C8EEEB`** ("Start your morning", "Wrap up your day"). Row centered (351 / 325.7 wide). Gap to the cards below: 12.2.
- The same two icons (44.4) frame the 9/16 hero kicker (L03o).

## L17 Offer intro with lifestyle photo (9/3 `408:5088`) · product highlight + offer

Screenshot `lab-L17-offer-intro-photo-block-09-03.png`. Band 745.5-1326.5 (581), fill **`#EFF0F5`**, with a giant soft glow group behind (`#7FF4EC`, `#55C5BD`).
- Body NK Medium **20/24** -1% `#05453D`, 2 lines, 407 wide, centered, band top → 0 ("Summer may be taking its final bow, / but your routine deserves an encore.").
- Gap 24 → offer line **NK Bold 20/24 -1% `#05453D`** ("Here's your early access to 20% off sitewide.").
- Gap 24 → B01 `#05453D` 251.6 x 50.3, Rubik white "Shop Early Access".
- Gap 24 → lifestyle photo **521.5 x 344, radius 20**, `56c9357e` hand with bar soap at a tap (fill `37cfc1e9` underneath, covered).
- Bottom: scallop divider `#05453D` (L22) into the dark gradient band.
- Slices: 920.5-1326.5 is one slice (photo + scallop); the text and CTA ride in the hero slice (111-920.5).

## L18 SMS signup band (8/15 `408:6658`, 8/20 `408:7014`)

Screenshots `lab-L18-sms-signup-band-08-15.png`, `lab-L18-sms-signup-band-08-20.png`. Frames named **"GIF-1"**: likely animated GIF slices (open question).

| | 8/15 | 8/20 |
|---|---|---|
| Size | 599.5 x 656.5 | 599.5 x 916.5 |
| Photo | Whiten+ tube on moss `c2c44c00` | Whiten+ tube with gel swoosh on sky blue `8f3d87b7` |
| Overlay | linear top→bottom `#044D44` 0% at 64% → 100% at 81% (dark bottom) | linear `#97DCFA` 100% → 0% at 40% (within 26% to 36% of the height: light top) |
| Top edge | standard wave `#B9EBFF` hanging (from the sky band above) | standard wave `#05453D` hanging |
| Icon | phone 47.7 (`#008D83` circle, white glyph) at rel y 71 | none |
| Headline | NK SemiBold **43.9/39.5, -4%** white, 2 lines, rel y 154 | NK **Bold 57.85/46.3 (80%), 0%** `#05453D`, 3 lines, rel y 115 |
| Body | NK Medium 19.5/23.4 white 433 wide, rel y 490 (near the bottom) | NK Medium 19.5/23.4 `#05453D` 524.5 wide rel y 281.5 |
| CTA | white 213.6 x 50.3 Rubik `#05453D` "Sign Up For SMS", rel y 556 | white 238.6 x 50.3 "Join The Text List", rel y 351 |
| Decor | leaf line-art `#008D83` (123, 108.5) | none |

## L19 Band closing CTA · October T12

Screenshots `lab-L19-closing-cta-07-05.png`, `lab-L19-closing-cta-08-12.png`.
- One B01 button centered at the end of the last body band, own full-width slice (1200 x 238 to 316 at 2x).
- Width hugs the label (+35): 196 to 386.6; July sale and 7.8 use a fixed **360** (720 at 2x).
- Spacing: last card → button **35.5 to 41**; button → band end / footer **45 to 59**.
- Fill/label pairs seen: `#295791`/white (7.1, 7.3), white/`#295791` (7.5), white/`#037E75` (7.8, 7.23), `#00857A`/white (7.15), `#037E75`/white (7.28), white/`#05453D` (8/3, 8/6, 8/10, 8/20, 8/24, 9/7, 9/11, 9/16, 9/22, 9/27), `#05453D`/white (8/12, 8/15, 9/3, 9/4). Label Rubik Bold 20.7/29.6 upper.

## L20 Fine print "Excluding value bundles"

Screenshot `lab-L20-fine-print-07-01.png`. 7.1, 7.3, 7.5, 9/4, 9/7 under the hero CTA; 9/3 under "sitewide".
- **Rubik Italic 14.5/17.4 (29/120% at 2x), -1%**, centered, 160.5 wide box, **11.5 below the CTA**. Color white, or `#24436F` on the light 7.5 hero.
- 9/3 variant: **Rubik Italic 10/12**, -1%, `#05453D`, left aligned.
- Token: NEW `fineprint_*`.

## L21 Seals and badges

Exports: `../../photos/figma-lab/seal-*.svg/.png`, `badge-*.svg/.png`. Screenshots `lab-L21-seal-08-06.png`, `lab-L21-seal-08-15.png`, `lab-L21-seal-09-11.png`.

**Starburst seal** (8/6 `408:5898`, 8/15 `408:6474`, 9/11 `408:4633`):
- Star polygon (many points, corner radius 2 to 3) with a linear gradient; inner star outline (stroke `#3DA79D`, 0.3 / 1.1 / 1.5) inset 10 to 15; small leaf icon `#55B5AC` (25 to 38.6) above the text; text **NK SemiBold, 90% line, -4%, white**, centered, 3 to 4 lines.
- Sizes and rotation: 8/6 **160**, -11.9°, text 17.4; 8/15 **189.6**, -18°, text 19.4; 9/11 **242**, -13.7°, text 25.9.
- Gradients: 8/6 `#05453D` 24% → `#0CAB97` 48% → `#05453D` 68% (diagonal, handles 19%,-27% → 134%,102%); 8/15 `#171849` → `#295791` → `#171849`; 9/11 `#05453D` → `#295791` → `#171849`.
- Copy: "National Fresh Breath Day", "National Relaxation Day" (layer text lacks the space: "RelaxationDay"), "National Gum Care Month".

**"15% OFF" badge** (7.1 S1 cards, 7.5 cards): hand-drawn oval 91.6 x 40.85, radial gradient `#C2DDFF` → `#6EA1E0`, ink outline and lettering `#24436F` (vector, not live text), small highlights `#DBE5E5`.

**Step number badge** (9/11, L15): scalloped star 39 `#70D8CE` + Rubik Bold 19 numeral `#05453D`.

**Stars row** (7.1, 7.3): five white 5-point stars 22 each, gap 4, row 126 x 22.

## L22 Dividers · October T13, T14

Screenshots `lab-L22-divider-wave-08-10.png`, `lab-L22-divider-dome-curve-07-15.png`, `lab-L22-divider-scallop-09-03.png`, `lab-L22-divider-dome-teal-07-08.png`, `lab-L22-divider-arc-stroke-07-03.png`.

| Divider | Spec | Where |
|---|---|---|
| Standard wave (= October T13, same path) | 603.6 x 62.9, fill = color of the band it leads into; "up" or rotated 180° "down" | 7.5 `#295791`; 8/10 `#05453D` up + `#05453D` down; 8/15 `#E9F6FD` up, `#B9EBFF` down; 9/4 white down; 9/11 `#CCFFFA` up, `#053832` down, 3 x `#05453D` down; 9/27 `#05453D` up |
| Tall wave | 603.6 x 166.9, `#05453D` | 8/20 `408:6967` |
| Dome / curve | huge ellipse clipped by the band, top edge = a shallow arc across 600 (white 2933.5 diameter in 7.1, 7.28, 8/12; `#F3F3F3` 7.15; `#008D83` 8/6, 8/24; `#6EA1E0` 2223 x 1666.5 in 7.3; `#037E75` 1778 x 1208 in 7.8; `#05453D` 1778 x 1208 in 9/7; green gradient 2239.5 x 2933.5 in 7.23) | 9 emails |
| Thin arc stroke | second ellipse, white 1px stroke (0.5 at 600), 21.5 below the dome edge | 7.3 |
| Scallop (cloud) edge | 688.6 x 201.7 vector group (5 circles), `#05453D` (9/3) or `#55B5AC` (9/22) | 9/3 `408:5098`, 9/22 `408:5325` (October T14 is the white version) |
| Wave panel | 741 x 1497 shape with wavy top edge, linear white 27% → `#008D83` | 9/16 `408:5435` |

## L23 Decor · October T15

- Fern sprig line-art `#CCFFFA` (7.3, 9/4): same family as October `leaf-sprig-fern-ccfffa.png`.
- Leaf branch line-art `#05453D` (9/27) 189 x 212.6, rotated.
- Leaf line-art cluster `#3DA79D` (8/3), faint.
- Solid double leaf with speckle texture: `#91C9C6` (8/10, 132 x 132.5), `#00867D` (8/15, x4, 132 to 146), `#008D83` (9/3, 192).
- Leaf line-art cluster `#008D83` (8/15 SMS band).
- Fireworks: `#4A96D0`+`#295791`, `#295791`+`#6EA1E0`, red `#C00000` (7.5); 4-point sparkles `#295791` (7.5).
- Glows: white ellipse with layer blur 107 to 152 (7.3, 7.5); `#7FF4EC` / `#55C5BD` group (9/3); `#008D83` / `#91FFF5` blur 204 (9/16).
- Multi-layer drop shadows on floating packshots (7.1, 7.3, 8/15, 8/20, 8/24): 5 stacked black shadows, opacity 30 → ~1%, growing offset and blur.

## L24 Kicker (eyebrow) treatments

| Treatment | Spec | Emails |
|---|---|---|
| Plain, above headline | Rubik Bold 20/20 upper (7.28, 8/15, 9/7); Rubik SemiBold 20/20 (7.1); Rubik Bold 26.7 (8/6); Rubik Bold 26.2 with icons (9/16) | 6 |
| Plain, under headline | Rubik Bold 20/20 upper (8/3, 8/12, 8/24, 9/11), 19.15 (7.23), 24/24 (8/10), 20/26 (9/22), 20/20 2 lines above (9/3) | 9 |
| Ruled (two full-width hairlines) | Rubik SemiBold 22/22 (7.5, rules 1.5), 25.2/25.2 (9/4, 9/27, rules 1.7), 17.8/17.8 (8/20, rules 1.2) | 4 |
| Dashes either side | Rubik Bold 17.8 + 21.9 x 3 dashes (7.15) | 1 |
| Short rule under | 45.8 x 2 radius 36 rule below the kicker (9/7) | 1 |

Tokens: October proposed `kicker_*` (Rubik SemiBold 25 upper) and `kicker_small_*` (Rubik Bold 20). LAB confirms both and adds the 17.8 to 26.7 range.

## L25 Footer · October T18

All 20 emails, e.g. 7.1 `408:7224` (group "Group 12"). Screenshot `lab-L25-footer-07-01.png`. **Identical in all 20 emails** (texts, image hashes and fills read on every email; full positions read on 7.1, 7.3 and 9/27, identical) and identical to the October footer. Never sliced. 587 tall.

| Element | Spec (600, rel y from footer top) |
|---|---|
| Block | `#295791` (`color.dark`), 599.5 x 455.5 at **x 0.5** (0.5 hairline gap on the left, as in October) |
| Bottom bar | `#24436F` (`color.footer_bar`), 600 x 131.5, rel y 455.5 |
| Link line | "Learn what we mean by natural on our website." Gotham Bold **14/20 underlined** white, centered in a 471.6 box at x 64.5, rel y 79 (box has a trailing empty line) |
| Logo | white raster PNG `671cac09` (780x629), **101.4 x 82** at x 249.8, rel y 126.5 (`assets/logo-dark.png`) |
| Social row | 159.9 x 32 at **x 220.3, rel y 238.5**: 5 cells **32 x 32, no gap**, order **X, Facebook, Instagram, TikTok, Pinterest**, white glyphs (X 23 x 21, Facebook 11.7 x 20.9, Instagram 21 x 21.1, TikTok 18.3 x 21, Pinterest raster 15.6 x 20.8). Use `assets/icon-*.png/svg`, `social-row.*` |
| Nav | 4 lines "Our Mission / Products / Shop Now / Blog", Gotham Bold **14/28** white, centered, rel y 294 (117 tall) |
| Address | "Tom's of Maine · 2 Storer Street, Suite 302 · Kennebunk, ME 04043 · USA", Gotham Bold **10/28** white, centered, 535.5 box at x 32.5, rel y 470 |
| Copyright | "©%%= v(@CurrentYear) =%% Tom's of Maine, Inc." same style, rel y 503.5 |
| Legal links | "Privacy Policy  l  Terms of Sale  l   Terms of Use  l  Unsubscribe" same style, rel y 541. Separator is a lowercase **"l"** with 2 spaces each side (3 before "Terms of Use") |
| Differences between months | **none**. No disclaimer variant in LAB (October T18 has one on 10/13) |

## B01 Button, standard · October B01

- **50.3 to 50.5 tall, radius 11.7**, width hugs the label (+35, 17.5 each side) or fixed (360 on July closing CTAs, 286 in the 8/10 hero column).
- Label 20.7/29.6 uppercase, tracking 0. **Hero CTAs: Gotham Bold** (16 heroes); **Rubik Bold** on 8/3 and 8/10 heroes, every band CTA and every review/step/S6 card button.
- Label alignment: centered; **left** on 7.28 (Gotham, left-aligned text inside the button, matching the left hero).
- Fills: white, `#05453D`, `#295791`, `#24436F`, `#037E75`, `#00857A`. Label colors: white, `#05453D`, `#285488`, `#295791`, `#037E75`, `#00857A`, `#EFEFEF`.
- Card size: 144 x 50.3 ("shop now" / "SHOP NOW").

## B02 Button, small · October B02

- **139 x 42.8, radius 10**, fixed width; label box 95 x 18 centered; Rubik Bold **18.1/18.1** upper ("shop now" typed lowercase). `compact_*` tokens.
- Wide variant **165 x 42.8** "SHOP 15% OFF" (7.3).
- Fills: `#295791` (July sale), `#05453D` (others), white with `#05453D` label (8/15 category rows).

## B03 Button, comparison (8/3)

- **127.5 x 39.2, radius 9.25**, `#05453D`, Rubik Bold **16.6/16.6** upper white "shop now". Below the 44 minimum.

---

## Type mapping summary (600 scale)

| Text | Spec | Token |
|---|---|---|
| Hero headline | NK SemiBold 48 to 76.9, line 80 to 100%, tracking 0 to -7% (64/57.6 = `display_*`; 74.5 to 76.9 = `display_compact_*`) | `display_*`, `display_compact_*`; sizes 48, 53, 57, 60.25, 64.9, 69.15, 73.4, 74.5, 75 are NEW variants |
| Price headline | NK SemiBold **120 to 185.6**, line 80 to 90%, -3 to -7% | NEW `price_*` (L03a/b 120.4; L03l 183.85; L03e 185.6; L03m 125.25) |
| Price companion ("sitewide", "before the sale goes live", "There's still time to enjoy") | NK SemiBold 41.9 to 80.2, -5 to -7% | NEW `price_sub_*` |
| Kicker | Rubik SemiBold/Bold 17.8 to 26.7 upper, line 100% (130% when 2 lines in 9/22) | October `kicker_*` / `kicker_small_*` |
| Hero/intro body | NK Medium 19.5/23.4 or 20/24, -1% (18/21.6 in 8/3) | `body_*` / October `intro_*` |
| Offer line | NK **Bold** 20/24 -1% (9/3), or bold run inside body (9/4, 9/7) | NEW `body_strong` (weight 700) |
| Section heading | NK Bold 42/44.1 | `h2_*` |
| Subtitle | Rubik Bold 22.3/29 upper | `subtitle_*` |
| Announcement | Rubik SemiBold 23.5/23.5 upper | NEW |
| Product name, Rubik | Rubik Bold 18.1/18.1 upper | `label_small_size` 18 (NEW line 18) |
| Product name, serif | NK Medium 18/21.6 -1% `#044D44` | October `card_name_*` |
| Comparison product name | NK Medium 16/19.2 -1% `#044D44` | `product_name_*` size, NEW weight 500 |
| Review product name | Rubik Bold 20/20 upper | NEW `label_md` 20 |
| Review quote / step body | NK Medium 18/21.6 -3% | `caption_*` |
| Reviewer | Rubik Bold 16/16 upper | NEW |
| Step title / step product | Rubik Bold 24.35/24.35 upper | `label_*` |
| Step numeral | Rubik Bold 19/19 | NEW |
| Claim | NK Medium 15/18 -1% | NEW `claim_sm_*` (October `claim_*` is SemiBold 19.8) |
| Claim footnote | NK Medium 7.5/9 -1% | NEW, below legal minimum |
| Day-part subhead | NK SemiBold 30.35/27.3 `#C8EEEB` | NEW `subhead_*` |
| Seal text | NK SemiBold 17.4 to 25.9 / 90%, -4%, white | NEW (inside the seal asset) |
| Fine print | Rubik Italic 14.5/17.4 -1% (10/12 in 9/3) | NEW `fineprint_*` |
| Button | Gotham Bold or Rubik Bold 20.7/29.6 upper | `button.*` |
| Small button | Rubik Bold 18.1/18.1 upper | `button.compact_*` |
| Comparison button | Rubik Bold 16.6/16.6 upper | NEW |
| Nav | Gotham Bold 14/auto upper `#00867D` | `nav_*` |
| Footer | Gotham Bold 14/20 underline; 14/28; 10/28 | `nav_*`, `legal_size` (line 28) |

## Colors seen that are not in tokens.json

| Hex | Where |
|---|---|
| `#6EA1E0` | July sky blue: 7.3 announcement bar and grid band, 7.5 headline accent "15% OFF", fireworks, badge gradient end |
| `#285488` | July hero CTA label (7.1, 7.3), 1 step off `#295791` |
| `#295791` / `#24436F` | **used far beyond the footer in July**: panel (90%), headings (`#24436F`), card text and buttons (`#295791`), card stroke (`#24436F`), 7.5 band; also 8/15 and 9/11 seal gradients, 9/22 band gradient. Tokens scope them to the footer |
| `#C2DDFF`, `#DBE5E5` | "15% OFF" badge |
| `#578CFF`, `#E1EBEB`, `#ECEEFF` | 7.3 lavender card sheen (`#578CFF` layer covered) |
| `#4A96D0`, `#C00000` | 7.5 fireworks |
| `#EFEFEF` | 7.5 hero CTA label on `#24436F` |
| `#037E75` | CTA label/fill (7.8, 7.23, 7.28), 7.8 teal dome |
| `#101E2F`, `#142A2A` | 7.8 photo overlays / band base |
| `#00857A` | 7.15 tab panel, band, CTA, H2 (= guideline Tom's Teal) |
| `#F3F3F3` | 7.15 grey band |
| `#29776F` | product names 7.23, 7.28 |
| `#539D97`, `#327B75`, `#115953` | 7.23 green gradient (dome and band) |
| `#332B0E` | 7.28 warm photo overlay (0 → 90%) |
| `#044D44` | product names (Aug/Sep), 8/3 comparison panel, 8/12 H2 (October proposes `text_card`) |
| `#079B89`, `#09B39E`, `#008D84` | 8/3 hero fades; `#008D84` also 8/3 claims band, 8/12 review rows, 9/11 step outline |
| `#7DCDC5`, `#C8EEEB` | mint card sheen, claims tiles; `#C8EEEB` also day-part icons and subheads |
| `#3DA79D`, `#55B5AC` | seal inner stroke / leaf icon; leaf line-art; `#55B5AC` 9/16 gradient text end, 9/22 band start and scallop |
| `#E8E6E7` | 8/6 hero top fade |
| `#E9F6FD`, `#B9EBFF` | 8/6 review rows, 8/15 band (sky gradient) |
| `#91C9C6` | 8/10 solid leaves |
| `#171849` | seal deep navy (8/15, 9/11) |
| `#97DCFA` | 8/20 SMS top fade (October has `#97DCFB`) |
| `#EEEFF5`, `#EFF0F5` | 9/3 hero base and offer band |
| `#7FF4EC`, `#55C5BD` | 9/3 glow |
| `#9FD5F1` | 9/22 hero top fade |
| `#053832` | 9/11 hanging wave |
| `#70D8CE` | 9/11 step badge and step titles |
| `#000B1A`, `#91FFF5` | 9/16 aurora gradient end and glow |
| `#CCFFFA` (token `accent_on_dark`) | ferns, 9/11 cap gradient end and wave |

## Proposed token additions

```json
{
  "type": {
    "price_size": 120, "price_line": 108, "price_tracking": "-0.07em", "price_weight": 600,
    "price_xl_size": 185, "price_xl_line": 148, "price_xl_tracking": "-0.04em",
    "price_sub_size": 54, "price_sub_line": 49, "price_sub_tracking": "-0.07em",
    "hero_sizes_seen": [48, 53, 57, 60.25, 64, 64.9, 69.15, 73.4, 74.5, 75, 76.45, 76.9],
    "kicker_size": 25, "kicker_line": 25, "kicker_weight": 600, "kicker_transform": "uppercase",
    "kicker_small_size": 20, "kicker_small_line": 20, "kicker_small_weight": 700,
    "kicker_rule_weight": "1.5px to 1.7px",
    "announce_size": 23.5, "announce_line": 23.5, "announce_weight": 600,
    "body_strong_weight": 700,
    "card_name_size": 18, "card_name_line": 21.6, "card_name_weight": 500, "card_name_tracking": "-0.01em",
    "card_name_rubik_size": 18, "card_name_rubik_line": 18, "card_name_rubik_weight": 700, "card_name_rubik_transform": "uppercase",
    "label_md_size": 20, "label_md_line": 20,
    "reviewer_size": 16, "reviewer_line": 16,
    "claim_sm_size": 15, "claim_sm_line": 18, "claim_sm_weight": 500,
    "footnote_size": 7.5, "footnote_line": 9,
    "subhead_size": 30, "subhead_line": 27, "subhead_weight": 600,
    "fineprint_size": 14.5, "fineprint_line": 17.4, "fineprint_style": "italic", "fineprint_family": "Rubik",
    "legal_line_measured": 28
  },
  "color": {
    "july_sky": "#6EA1E0", "july_cta_label": "#285488", "july_badge_light": "#C2DDFF",
    "firework_blue": "#4A96D0", "firework_red": "#C00000",
    "teal_cta": "#037E75", "toms_teal": "#00857A", "grey_band": "#F3F3F3",
    "text_card": "#044D44", "text_card_alt": "#29776F",
    "green_1": "#539D97", "green_2": "#327B75", "green_3": "#115953",
    "card_sheen": "#C8EEEB", "card_base_mint": "#7DCDC5", "card_sheen_lavender": "#ECEEFF",
    "sky_1": "#E9F6FD", "sky_2": "#B9EBFF", "sky_fade": "#9FD5F1",
    "leaf_soft": "#91C9C6", "teal_mid": "#3DA79D", "step_accent": "#70D8CE",
    "seal_navy": "#171849", "offwhite_band": "#EFF0F5", "teal_deep": "#053832",
    "gradient_card_mint": "#FFFFFF 0% / #C8EEEB 51% / #FFFFFF 100%, diagonal (handles 103%,6% to -11%,104%)",
    "gradient_card_lavender": "#FFFFFF 0% / #ECEEFF 51% / #FFFFFF 100%, same diagonal",
    "gradient_band_deep_teal": "linear-gradient(180deg,#05453D 0%,#0CAB97 100%)",
    "gradient_band_steps": "linear-gradient(180deg,#05453D 57%,#0CAB97 100%)",
    "gradient_band_dark_teal": "linear-gradient(180deg,#05453D 0%,#008D83 100%)",
    "gradient_band_green": "linear-gradient(180deg,#539D97 0%,#327B75 50%,#115953 100%)",
    "gradient_band_fall": "linear-gradient(180deg,#55B5AC 0%,#00867D 30%,#295791 63%,#24436F 100%)",
    "gradient_sky": "linear-gradient(180deg,#E9F6FD 0%,#B9EBFF 100%)",
    "gradient_hero_teal": "linear-gradient(180deg,#008D83 0%,#05453D 80%)",
    "gradient_claim_tile": "linear-gradient(180deg,#7DCDC5 -77%,#FFFFFF 100%)",
    "gradient_cap_mint": "linear-gradient(180deg,#FFFFFF 0%,#CCFFFA 100%)"
  },
  "button": { "comparison_height": 39.2, "comparison_width": 127.5, "comparison_radius": "9.25px", "comparison_font_size": 16.6, "compact_wide_width": 165 },
  "radius": { "row": "40px", "panel": "24px", "tab_panel": "35px", "stage_photo": "35.5px", "glass": "22.4px", "review_image": "12px", "claim_tile": "22.4px" },
  "space": {
    "grid_width": "521px", "grid_gutter": "15px", "grid_row_gap": "15px",
    "grid_width_s6": "497.3px", "grid_gutter_s6": "10.3px",
    "card_pad_y": "26.5px", "image_to_name": "20px", "name_to_button": "10.75px",
    "review_row_gap": "8px", "review_pad": "32px", "review_stack_gap": "20px",
    "step_pad": "32px", "claim_gutter": "10px",
    "fineprint_gap": "11.5px", "cta_after_grid": "35.5px to 41px", "cta_to_band_end": "45px to 59px"
  },
  "size": {
    "product_card": "253 x 330 to 368", "product_card_s6": "243.5 x 336 to 377",
    "product_image": "169.5x167.5 / 212x167.5 / 221.5 square (bundles)",
    "wide_card": "521 x 220.5", "review_row": "521 x 338.1", "review_image": "145.5 x 274.1",
    "product_row": "498.5 x 189.5", "category_row": "498.5 x 255.6",
    "comparison_panel": "520 x 542", "comparison_card": "231.85 x 327.2",
    "claim_tile": "255 x 92.5", "step_badge": 39, "day_icon": 50.2,
    "seal": "160 / 189.6 / 242", "discount_badge": "91.6 x 40.85", "star": 22,
    "circle_photo": 371, "wave_tall": "603.6 x 166.9", "scallop": "688.6 x 201.7"
  }
}
```

Gradient angles written as CSS are read from the Figma handles (start/end in % of the layer); the diagonal sheen is quoted as handles, not as a CSS angle.

## Open questions

1. **Navy beyond the footer.** July 4th emails use `#295791` / `#24436F` for panels, headings, card text, strokes and buttons, and `#6EA1E0` sky blue; 8/15 and 9/11 seals and the 9/22 band gradient use navy too. Kit rule says navy is footer only. Seasonal (July 4th) exception, or a broader allowance?
2. **Header and footer slicing.** Header sliced only in the three July 4th emails; footer never sliced. Confirms the October question: fixed SFMC wrapper?
3. **Product name style.** Rubik Bold 18.1 upper (July, 7.15, category rows) vs NK Medium 18 sentence case `#044D44` (8/3, 8/10 onward). The switch happens in August: is the serif style the current standard?
4. **Product name color** `#29776F` (7.23, 7.28) vs `#295791` (July sale) vs `#05453D` (7.8) vs `#044D44`. Normalise?
5. **Card button.** B02 small 139 x 42.8 (most grids) vs B01 144 x 50.3 (S6 cards, reviews, steps). B02 and B03 (39.2 tall) are under the 44 minimum.
6. **Hero CTA font.** Gotham Bold on 16 heroes, Rubik Bold on 8/3 and 8/10. Same question as October.
7. **Footnote at 7.5 px** (8/3 claims "*with continued use", "*Calcium Carbonate"). Below any readable/legal minimum: approved as is?
8. **Slice gaps and overlaps**: 7.3 leaves 8.5 unsliced before the footer; 7.5 has a 6 gap (1383.5-1389.5) and the last slice overlaps the footer by 30; 9/3 frame clips the footer legal bar; 8/15 frame is 163 taller than its content; 7.28 slices are named `july_8-28_0n`.
9. **8/12 review rows**: image inset 10 on the right rows vs 32 on the left rows. Intended?
10. **"GIF-1" frames** (8/15, 8/20 SMS bands): are these slices exported as animated GIFs? No frames/variants of the animation exist on the page.
11. **Glass effect** (7.8, 7.15, 7.23, 8/15, 9/4, and on text layers in 8/6, 8/10, 9/3, 9/7): Figma-only, baked in the slice. Fine for the sliced workflow.
12. **Covered and hidden images.** Rainbow field, deodorant in snow, beach turquoise and others sit under opaque fills; white-background packshots and low-res previews sit on hidden layers (130 files, not exported). Should the covered ones count as approved bank photos?
13. **"15% OFF" badge** is hand-lettered vector art with the number baked in. For other percentages, redraw or use live text?
14. **Title Case in layers vs sentence case on screen** (text case LOWER segments, e.g. 7.3, 7.8, 7.15, 7.23 headings). Which is the approved copy when the text is reused?
15. **9/16 and 9/11 content frames** sit inside an 8149-tall "Email - 3" frame (empty below): leftover from a template copy, safe to ignore?

## What could not be extracted

- **Animated GIF content** for the two "GIF-1" frames: only one static state exists in Figma.
- **GLASS and blur effects** as standalone assets: they only exist composited.
- **Exact CSS angles** for diagonal gradients: recorded as Figma handle positions instead.
- **Link URLs**: not needed (owner).
- Nothing was blocked by rate limits; every email was dumped and every visible image fill was exported.
