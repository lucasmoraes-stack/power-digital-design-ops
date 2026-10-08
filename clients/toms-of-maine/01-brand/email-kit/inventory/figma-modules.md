# Tom's of Maine · Figma module inventory

Source: Figma file VAZIO DRAFT (`8oGyJxpeGLPWNiH54vePwS`), page `1482:2`, the 6 approved October 2026 emails. Read on 2026-10-06 through the Figma plugin API (read-only) and checked against renders of every module.

| Email | Top frame | Inner frame | Height at 600 |
|---|---|---|---|
| 10/2 World Smile Day | `1482:2752` | `1482:2753` | 3014.5 |
| 10/8 Ingredient Spotlight | `1482:2979` | `1482:2980` | 4082.5 |
| 10/13 Toothpaste by Need | `1482:3` | `1482:4` | 3550 |
| 10/20 Fall Routine Reset | `1482:2867` | `1482:2868` | 3440 (frame clips the last 52.5 of the footer, see open questions) |
| 10/22 Product Spotlight | `1482:3120` | `1482:3121` | 3312.5 |
| 10/27 Behind the Brand | `1482:3255` | `1482:3256` | 3905.5 |

## How to read this document

- **All values are at 600px** (Figma value / 2). Positions are `x, y` from the top-left of the email's inner frame unless stated as "from band top" or "inside card".
- **Production is sliced JPG only** (owner, 2026-10-06): the whole email is designed in Figma, exported and sliced. There is no HTML and no live text, so this document specifies how to rebuild the modules **in Figma**; slice boundaries are listed per email because they decide what each link covers.
- **Leading trim.** Almost every text layer uses `leadingTrim: CAP_HEIGHT` (exceptions: hero CTA labels in Gotham, values card titles, header nav, footer texts). So a text box height is cap-top to last baseline, and every **gap below is the visual gap** between cap-top / baseline edges, which is exactly what you match when composing in Figma.
- Line heights are given as the Figma value (percent) and its px result.
- **Type tokens** refer to `tokens.json` → `type.*`. "NEW" means no existing token covers it.
- Families: NK = New Kansas, Rubik, Gotham.
- No price, discount badge, strikethrough price, promo code or offer pill exists in any of the 6 emails. The only offer signal is CTA copy ("Stock Up & Save", 10/2). There is also no 3-up grid and no standalone single product card: product cards only appear in the 2-up grid.

## Subject lines and preheaders (text layers on the page)

| Email | Node | Subject (SL) | Preheader (PH) |
|---|---|---|---|
| 10/2 | `1482:3116` | Your Smile Wants More Credit 😁 | Small habits, big smile energy |
| 10/8 | `1482:3117` | Meet The Ingredients Doing The Real Work 🌿 | Transparency looks good on us |
| 10/13 | `1482:3118` | There's A Tom's For Every Smile 🪥 | Find the one that fits your routine |
| 10/20 | `1482:3119` | Small swaps, fresh start 🍂 | Your Routine Could Use A Season Update |
| 10/22 | `1482:3532` | Freshness That Keeps Up With You 🌿 | 48 hour protection, naturally |
| 10/27 | `1482:3533` | The Story Behind Every Tom's Product 🌿 | More than what meets the label |

Matched to emails by x position on the canvas. Subjects use one emoji at the end and mostly Title Case.

## Module list

| ID | Module | Emails (node ids) |
|---|---|---|
| T01 | Header | all 6: `1482:2754`, `1482:2981`, `1482:5`, `1482:2869`, `1482:3122`, `1482:3257` |
| T02a | Hero · circle portrait on texture | 10/2 `1482:2758` |
| T02b | Hero · glass card on photo with floating packshots | 10/8 `1482:2985` |
| T02c | Hero · scene on top, giant headline below (blue) | 10/13 `1482:9` |
| T02d | Hero · text on photo, product cluster on white arc | 10/20 `1482:2873` |
| T02e | Hero · product scene with claims ring | 10/22 `1482:3126` |
| T02f | Hero · full-bleed scene, text at the bottom | 10/27 `1482:3261` |
| T03 | Section intro (band heading + intro, optional Rubik subtitle) | every body band |
| T04 | Product card (grid tile) | 10/2 `1482:2784` …, 10/22 `1482:3172` … |
| T05 | Product grid 2-up (2 columns x 3 rows) | 10/2 `1482:2783`, 10/22 `1482:3171` |
| T06 | Ingredient spotlight (outline card + packshot + product + Shop Now) | 10/8 `1482:3001`, `1482:3020` |
| T07 | Routine step (outline card + bleeding packshot + Rubik product name + button) | 10/20 `1482:2895`, `1482:2912`, `1482:2925`, `1482:2938` |
| T08 | Need row (label pill + split product card) | 10/13 `1482:2657`, `1482:2672`, `1482:2688`, `1482:2703` |
| T09 | Category row stack (half photo / half panel, alternating) | 10/8 `1482:3042`, 10/27 `1482:3457` |
| T10 | Values grid 2x2 (icon cards) | 10/27 `1482:3279` |
| T11 | Claims ring (check icon + claim) | 10/22 inside hero `1482:3130` to `1482:3149` |
| T12 | Band closing CTA | 10/2 `1482:2832`, 10/8 `1482:3081`, 10/13 `1482:2719`, 10/22 `1482:3220`, 10/27 `1482:3446`, `1482:3498` |
| T13 | Wave divider | 10/8, 10/13, 10/20, 10/22, 10/27 (11 instances) |
| T14 | Scallop divider | 10/2 `1482:2771` |
| T15 | Decor: leaf sprig, fern sprig, sparkle | 10/8, 10/13, 10/22 |
| T16 | Leaf-vein texture band background | 10/13 `1482:68` / `1482:69` |
| T17 | Circular portrait with ring | 10/2 `1482:2764` |
| T18 | Footer (+ disclaimer variant) | all 6: `1482:2834`, `1482:3083`, `1482:2721`, `1482:2950`, `1482:3222`, `1482:3500` |
| B01 | Button, standard | everywhere |
| B02 | Button, small "shop now" | T04, T08, T09 |

Screenshots: `../references/figma-<id>-<name>-<mm-dd>.png` (2x).

---

## Slices per email

Slices are top-level SLICE nodes in each email frame. In all 6 emails **the slices cover everything between the header and the footer; the header (0 to 110.5) and the footer are never inside a slice** of these frames (see open questions). Pattern: the hero is one slice, every clickable unit (each grid card, each row, each closing CTA) gets its own slice, and the band intro rides with the first unit below it.

| Email | Slices (y from, to; width) |
|---|---|
| 10/2 | S1 110.4 to 949.9 (hero incl. its CTA) · S2 949.9 to 1209.9 (scallop edge + intro) · S3/S4 1209.9 to 1574.9, left 0 to 300 / right 300 to 600 (cards row 1) · S5/S6 1574.9 to 1941.9 (row 2) · S7/S8 1941.9 to 2329.4 (row 3) · S9 2329.4 to 2427.4 (closing CTA) |
| 10/8 | S1 110.5 to 871.5 (hero) · S2 871.5 to 1533.5 (intro + Coconut Oil card + product + Shop Now) · S3 1533.5 to 2012 (Sea Salt block) · S4 2012 to 2292.5 (wave + "Transparency" intro) · S5 to S8: one per category row (2292.5 / 2563 / 2833.5 / 3104.5 / 3400) · S9 3400 to 3495.5 (closing CTA) |
| 10/13 | S1 110.5 to 1122.5 (hero) · S2 1122.5 to 1690 (intro + Cavity row) · S3 1690 to 2071.5 (Whitening) · S4 2071.5 to 2452 (Sensitivity) · S5 2452 to 2831 (Fresh Breath) · S6 2831 to 2963 (closing CTA) |
| 10/20 | S1 110.5 to 1001.5 (hero) · S2 1001.5 to 1572.5 (intro + step 1) · S3 1572.5 to 2022 (step 2) · S4 2022 to 2471 (step 3) · S5 2471 to 2905.5 (step 4) |
| 10/22 | S1 110.5 to 1227.5 (hero) · S2 1227.5 to 1452.5 (intro) · S3/S4 1452.5 to 1836.5 halves · S5/S6 1836.5 to 2222.5 · S7/S8 2222.5 to 2593.5 · S9 2593.5 to 2725.5 (closing CTA) |
| 10/27 | S1 110.5 to 1098.5 (hero) · S2 1098.5 to 2043 (whole values band incl. its CTA) · S3 2043 to 2334.5 (wave + intro) · S4 to S7 one per category row (2334.5 / 2549.5 / 2764.5 / 2979.5 / 3219.5) · S8 3219.5 to 3318.5 (closing CTA) |

Notes: in 10/20 each routine band (two possible targets: card copy and Shop Now) is a single slice, so one link per band. In 10/27 S2 the values band CTA shares the slice with the 4 cards.

---

## T01 Header

Nodes: `1482:2754` (10/2) and identical copies in all 6. Screenshot `figma-T01-header-10-02.png`.

- Band: 600 x 110.5, white `#FFFFFF` rectangle.
- Logo: raster image `image 1` (teal badge "The Original Tom's of Maine"), layer box **126.5 x 102.5 at x 43.2, y 7.5** (box bottom sits on the header bottom edge, 110). The PNG has transparent padding: the **visible badge is 94.5 x 76 at x 59, y 23.6** (measured from the alpha of the cropped source). Asset: `assets/logo-light.png` (253x205 = the exact layer box at 2x).
- Nav: one single text layer, not three: `OUR MISSION      PRODUCTS      SHOP NOW` (six spaces between items), Gotham Bold 14, line auto, tracking 0, uppercase via text case, color `#00867D`, left aligned, box x 252.2, y 53.5, 325.5 x 22.5 (right edge 577.7, so 22.3 right margin). Token: `type.nav_*` + `color.nav`.
- Vertical: nav cap-line sits slightly below the visual centre of the badge (badge centre y 61.6, nav box centre y 64.75).
- No variations across the 6 emails.

## T02 Hero family

Shared rules measured across the six heroes:
- Width 600, background photo or texture filling the frame (frame clips content).
- Text stack is centred; auto layout gap **24** between headline, kicker, body and CTA in 10/13, 10/20, 10/22, 10/27; **25** in 10/8 (inside the glass card); **29** in 10/2 (manual).
- Headline: NK SemiBold, line 90% (97% in 10/27), sentence case. Two size families: **64** (`type.display_*`, tracking -2% in 10/2 and 10/8, -3% in 10/27, **-7% in 10/20**) and **76.4** (`type.display_compact_*`, tracking -7%, 10/13 and 10/22).
- Body: NK Medium 20/120% (24) tracking -1% (10/2, 10/13, 10/22, 10/27) or 19.5/120% (23.4) (10/8, 10/20). Token `type.body_*` (19.5 is a variant, see token proposals).
- Hero CTA: B01 at 50.3 tall. **Label family differs**: Gotham Bold in 10/2, 10/13, 10/20, 10/22, 10/27; Rubik Bold in 10/8.
- Each hero ends with a transition: scallop (10/2), wave (10/8, 10/13, 10/22, 10/27) or a white ellipse arc (10/20).

### T02a Circle portrait on texture (10/2, `1482:2758`)

Screenshot `figma-T02a-hero-circle-portrait-10-02.png`.
- Frame 600 x 890 (y 110.5 to 1000.5). Background: image `bg-white-cream-swirl-texture.jpg` (CROP), no overlay.
- Stack (frame `1482:2761`), from hero top:
  - +67.5 Headline `1482:2762`, box 434 wide, 160.5 tall (3 lines), NK SemiBold 64/90% (57.6), tracking -2%, centre. Colors: `#05453D` with "routine" and "behind it" in `#008D83` (`color.heading_accent`). A drop shadow (blur 68.8, y 18, `#000000` 13%) exists on the layer but is **switched off**.
  - gap 29 → Kicker `1482:2763` "Today We Celebrate What Keeps Yours Going": Rubik Bold 20/130% (26), uppercase, `#05453D`, 271 wide (2 lines, 40 tall). NEW token (see proposals).
  - gap 29 → T17 circular portrait 279.3 x 279.3.
  - gap 29 → Body `1482:2768`, 450 wide, 4 lines (86), NK Medium 20/120%, -1%, `#05453D`.
  - gap 29 → CTA `1482:2769` 332.6 x 50.3, fill `#05453D`, radius 11.7, label "Find Your Smile Routine" Gotham Bold 20.7/29.6 white uppercase.
- CTA bottom at +799.6; scallop T14 starts at +839.5; hero ends at +890.
- Image vs bleed: everything inside the frame, nothing bleeds.

### T02b Glass card on photo with floating packshots (10/8, `1482:2985`)

Screenshot `figma-T02b-hero-glass-card-10-08.png`.
- Frame 600 x 759 (y 110.5 to 869.5). Background `bg-green-leaf-macro.jpg` (CROP).
- Glass card `1482:2989`: x 40.5, +102.5 from hero top, **521 x 439.3, radius 20**, Figma **GLASS effect** (radius 50, refraction 1, depth 100, light angle -45°, intensity 0.8, dispersion 1, splay 1). Its white 50% fill is switched off. Auto layout vertical, padding 36 top and bottom, 0 sides, gap 25; inner column 459.5 wide.
  - Headline "What's inside matters" NK SemiBold 64/90% -2% **white**, 260 wide (3 lines, 160.5).
  - Kicker "Let's Talk About It" Rubik Bold 20.3/100% white uppercase.
  - Body NK Medium 19.5/120% -1% white, 459.5 wide (2 lines with a forced break).
  - CTA 232.1 x 50.3, **white fill**, label "See What's Inside" **Rubik** Bold 20.7/29.6 `#05453D`.
- Packshots (both bleed off the 600 edge and are clipped by the hero):
  - Sea Salt mouthwash `1482:2996`, 292.5 x 386.5 at x -93.6, y 142.5, rotated -26°.
  - Whiten Plus Coconut Oil box `1482:2997`, 302.4 x 243.4 at x 317.3, y 571.4, rotated 33°.
  - Both carry a 5-layer drop shadow (mouthwash: blur 14.5 / 26 / 35 / 41.5 / 45.5, offsets (4,5) (16.5,20) (36.5,45.5) (65.5,80.5) (102,126), black at 29 / 26 / 15 / 4 / 1%; box: blur 13.5 / 24.5 / 33 / 39.5 / 43, black 54 / 47 / 28 / 8 / 1%, similar offsets).
- Decor: two `#008D83` leaf sprigs (T15): `1482:2999` 163.5 x 194.3 rotated 158° top right (partly hidden above the hero top), `1482:3000` rotated 42° bottom left.
- Exit: white wave `1482:2998` (up) at y 808.5.

### T02c Scene on top, giant headline below (10/13, `1482:9`)

Screenshot `figma-T02c-hero-product-top-10-13.png`.
- Frame 600 x 1010 (y 110.5 to 1120.5). Fills, bottom to top: solid `#97DCFB`; image `hero-bg-heart-gel-whiten-plus-tube-blue.jpg` (CROP); linear gradient top to bottom `#97DCFB` 0% opacity at 36% → `#3697D6` at 100%.
- Stack `1482:27` starts **+465.5** from hero top (below the product scene), 486.5 wide, gap 24:
  - Headline "Your perfect toothpaste match exists" NK SemiBold **76.4/90% (68.8), tracking -7%**, `#05453D`, 540 box (3 lines, 192.5).
  - Ruled kicker `1482:29`, 327 wide: rule 1.7 `#05453D` · gap 14.6 · "Let's Find It Together" Rubik SemiBold 25.2/100% uppercase `#05453D` · gap 14.6 · rule 1.7. Rules are as wide as the kicker frame.
  - Body NK Medium 20/120% -1% `#05453D`, 370.5 wide, 4 lines.
  - CTA 239.1 x 50.3 white fill, "Find Your Match" Gotham Bold 20.7/29.6 `#05453D`.
- Decor (T15), all blend **soft light**: three `#CCFFFA` fern sprigs `1482:10` (bottom right, rotated 2°), `1482:42` (left, -108°), `1482:55` (top right, -178°); five sparkles 10.2 x 13.7 `#CCFFFA` at 80% opacity (`1482:37` to `1482:41`).
- Exit: `#008D83` wave `1482:25` (up) at y 1059.5, matching the teal band below.
- An empty rectangle "AdobeStock_203268966 2" with blend Screen and no fill sits in this hero (and in 10/22, 10/27); it renders nothing.

### T02d Text on photo, product cluster on white arc (10/20, `1482:2873`)

Screenshot `figma-T02d-hero-text-top-product-cluster-10-20.png`.
- Frame 600 x 891 (y 110.5 to 1001.5). Background `bg-autumn-leaf-macro-orange.jpg` (FILL). A glass rectangle (`1482:2874`, 509.5 x 385, radius 22.4, black 20% gradient) is **hidden**.
- Stack `1482:2877` at **+66**, 435.9 wide, gap 24, all white:
  - Headline "Fall into a better routine" NK SemiBold 64/90% **tracking -7%**, 403 box (2 lines, 103).
  - Ruled kicker 398 wide (rules 1.7 white, gaps 14.6), "The Seasonal Shift You Need" Rubik SemiBold 25.2 uppercase.
  - Body NK Medium 19.5/120% -1%, 424 wide, 3 lines (forced break).
  - CTA 308.6 x 50.3 white fill, "Refresh Your Routine" Gotham Bold `#05453D`.
- White ellipse `1482:2886`, diameter 2933.5, top at y 804.5: draws a shallow white arc over the bottom 197 of the hero.
- Product cluster `1482:2891` (435 x 425.5 at x 117, y 523.5) sitting across the arc, with a duplicate `1482:2887` carrying a 5-layer drop shadow (blur 9.5 / 17.5 / 24 / 28 / 31, black 29 / 26 / 15 / 4 / 1%):
  - North Woods deodorant 321 x 321 at x 15.5, y 605.5 (left, behind),
  - Whole Care mouthwash 431 x 425.5 at x 86, y 523.5 (centre, front),
  - Lemon Bergamot soap 194.5 x 111 at x 357.5, y 797.5 (right).
- No wave: the arc is the exit into the white band.

### T02e Product scene with claims ring (10/22, `1482:3126`)

Screenshot `figma-T02e-hero-claims-10-22.png`.
- Frame 600 x 1114.5 (y 110.5 to 1225). Fills: image `hero-bg-north-woods-deodorant-rock-sunset.jpg` (CROP) + linear gradient top to bottom `#00535B` solid at 13% → `#00535B` 0% at 46% (darkens the top for white text).
- Stack `1482:3152` at **+70**, 503 wide, gap 24, white:
  - Headline "Stay fresh, feel confident" NK SemiBold 76.4/90% -7%, forced line break, 540 box (2 lines, 123.5).
  - Ruled kicker 503 wide, "Odor Protection Inspired By Nature" Rubik SemiBold 25.2 uppercase.
  - Body NK Medium 20/120% -1%, 414 wide, 3 lines.
- T11 claims ring around the product (product is part of the photo).
- Two `#05453D` leaf sprigs: `1482:3160` (147.9 x 175.7, rotated 97°, left, y 809.5) and `1482:3161` (157.9 x 187.6, rotated 160°, right, y 779.8).
- CTA `1482:3150` at y 1079.5 (bottom of hero, over the rock), 298.6 x 50.3 white, "EXPLORE DEODORANTS" (typed in caps) Gotham Bold `#05453D`.
- Exit: `#05453D` wave `1482:3162` (up) at y 1164.5 into the `#05453D` band.

### T02f Full-bleed scene, text at the bottom (10/27, `1482:3261`)

Screenshot `figma-T02f-hero-text-bottom-10-27.png`.
- Frame 600 x 986 (y 110.5 to 1096.5). Fills: image `hero-bg-whiten-plus-tubes-forest-log.jpg` (CROP) + gradient top to bottom `#031311` 0% at 72% → `#031311` at 98%.
- Stack `1482:3265` at **+505**, 503 wide, gap 24, white:
  - Headline "There's more to Tom's of Maine than you think" NK SemiBold 64/**97%** (62.1), tracking **-3%**, 3 lines (169.5).
  - Kicker (no rules) "And We Love Talking About It." Rubik SemiBold 25.2 uppercase.
  - Body NK Medium 20/120% -1%, 461 wide, 3 lines.
  - CTA 228.6 x 50.3 white, "Get To Know Us" Gotham Bold `#05453D`.
- Exit: white wave `1482:3273` (down orientation) at y 1035.5.

## T03 Section intro

Used at the top of every body band. Centred.

| Element | Spec | Token |
|---|---|---|
| Heading | NK Bold 42/105% (44.1), tracking 0, centre, `#05453D` on light, white on dark; 1 or 2 lines | `type.h2_*` |
| Accent | one phrase in `#008D83` ("Tom's of Maine", 10/27) | `color.heading_accent` |
| Optional subtitle | Rubik Bold 22.3/130% (29) uppercase `#05453D`, gap 20 below heading (10/27 values band) | `type.subtitle_*` |
| Intro | NK Medium **19.5**/120% (23.4), tracking -1%, centre, same color as heading | `type.body_*` (19.5 variant) |
| Gap heading → intro | **24** (auto layout) in 10/8, 10/13, 10/20, 10/22, 10/27; **35.5** in 10/2 (manual) | `space.heading_to_body` |
| Gap intro → first content | **40** in 10/8, 10/13, 10/22, 10/27; 35.5 in 10/2; 10/20 has 36 (card at 1181.2 after intro ending 1145) | NEW `space.section_gap` |
| Text widths | heading 343.5 to 498.5; intro 321.6 to 521.5 (each set by hand to control line breaks) | |

Band top padding (band top → heading cap) measured: 47.4 (10/2), 53 (10/8 band 1), 45 (10/8 deep band), 54 (10/13), 31.5 (10/20, right under the hero arc), 52 (10/22), **60** (10/27 values band, auto layout padding 60), 55.5 (10/27 category band). Bottom padding (last element → band bottom): 47.7, 45.2, 41.7, 41.6, 48.7. The `space.band_y` token (60) only matches the 10/27 values band.

## T04 Product card (grid tile)

Screenshots `figma-T04-product-card-medium-name-10-02.png`, `figma-T04-product-card-semibold-name-10-22.png`.

| Property | 10/2 (`1482:2784` …) | 10/22 (`1482:3172` …) |
|---|---|---|
| Size | 253 x 350 (two cards 352) | 253 x 369 (two cards 371) |
| Radius | 20 | 20 |
| Fill | two opaque linear gradients; the top one covers the bottom one, so what shows is **`#FFFFFF` 0% → `#C8EEEB` 51% → `#FFFFFF` 100%, diagonal** (gradientTransform `[[-0.39,0.57,0.37],[-0.57,-0.66,1.12]]`). Hidden underneath: `#7DCDC5` → `#E1EBEB` | same |
| Stroke / shadow | none | none |
| Layout | absolute; same measures as 10/22 | auto layout vertical, padding 26.5 top/bottom, 20.5 sides, gap 20 |
| Image box | 212 x 167.5 for boxes (CROP/FILL), 169.5 x 169.5 for upright items (mouthwash, radius 12), 212 x 169.5 floss (FIT), 169.5 x 167.5 toothbrush; top at +26.5 | 169.5 x 167.5 (or 169.5 square), centred, top +26.5 |
| Image type | transparent packshot | transparent packshot |
| Gap image → name | 20 | 20 |
| Product name | NK **Medium 18/120%** (21.6), tracking -1%, `#044D44`, centre, 3 lines (56) in a 220.5 column | NK **SemiBold 24/120%** (28.8), tracking -1%, `#05453D`, centre, 3 lines (75) |
| Gap name → button | 10.7 | 10.8 |
| Button | B02 small, `#05453D`, white label | same |
| Bottom padding | 26.5 | 26.5 |
| Token | name = NEW `type.card_name_*` (18/21.6, Medium, -1%, `#044D44`) | name = `type.item_*` |

## T05 Product grid 2-up

Screenshots `figma-T05-product-grid-2up-band-10-02.png`, `figma-T05-product-grid-2up-band-10-22.png`.

- Grid width **521**, starting at x 38.8 to 39.3 (side margin about 39.5).
- **2 columns of 253, column gutter 15, row gap 15**. 3 rows in both emails (6 products).
- Cards in a row can differ by 2 px in height (350/352, 369/371); not aligned to a common height.
- Band variations:
  - 10/2 `1482:2777`: band gradient top to bottom **`#FFFFFF` 0% → `#E8E8E8` 43%**, T03 intro dark text, closing CTA dark (`#05453D`) "Stock Up & Save".
  - 10/22 `1482:3163`: band solid **`#05453D`**, T03 intro white, closing CTA white "Explore All Products". Auto layout: content column 498.5 wide, gap 40 between intro, grid and CTA.
- Slicing: each card is its own half-width slice (300 wide, cut on the 300 centreline, inside the 15 gutter).

## T06 Ingredient spotlight

Band `1482:3001` (centred variant) and `1482:3020` (side variant), 10/8. Screenshots `figma-T06-ingredient-spotlight-centered-10-08.png`, `figma-T06-ingredient-spotlight-side-10-08.png`, `figma-T06-ingredient-outline-card-10-08.png`.

Bands: gradient top to bottom `#FFFFFF` → `#E8E8E8`; the band frames do **not** clip, so packshots bleed into the neighbouring band.

**Outline card** (`1482:3002`, `1482:3021`): 521 wide at x 40.5, stroke **2 inside `#008D83`**, radius 20, no fill, auto layout padding **40 top/bottom, 32 sides**, gap 15.
- Ingredient name: NK SemiBold 24/120% -1% **`#008D83`** ("Coconut Oil", "Sea Salt"). Token `type.item_*` + `color.heading_accent`.
- Description: NK Medium 18/120% (21.6) **-3%** `#05453D`. Token `type.caption_*`.

**Centred variant** (`1482:3001`, band 869.5 to 1596.5, height 727):
- T03 intro at +53 (heading 2 lines + intro 2 lines).
- Card at +228.5 (gap 40 after intro), 521 x 205, text centred (448.5 column).
- Packshot `1482:3014` (Whiten Plus Coconut Oil box) 385.5 x 128.5 at x 110, **overlapping the card's bottom edge by 67** (packshot top 1236, card bottom 1303).
- Gap 40 → product name NK SemiBold 24/120% -1% `#05453D`, centre, 2 lines (460.5 box).
- Gap 24 → Shop Now B01 144.1 x 50.3, `#05453D` fill, Rubik label.
- Leaf sprig `1482:3019` `#008D83` 121.6 x 144.5 rotated 135°, right edge, at the button line.
- Exit: white wave (down) at the band bottom.

**Side variant** (`1482:3020`, band 1596.5 to 2072, height 475.5):
- No intro. Card at +45, 521 x 170.5, text **left aligned** in a 273 column (left half).
- Packshot `1482:3032` (Sea Salt mouthwash) 534.9 box rotated 27°, anchored right, bleeding off the right edge and up into the previous band.
- Product name (3 lines, 269.5 box) and Shop Now centred in a 313.5 column at x 143.
- Leaf sprig `1482:3033` 121.6 x 144.5 rotated 11°, left edge.
- Exit: **`#05453D` wave** (down) into the deep gradient band.

## T07 Routine step

Four bands in 10/20: `1482:2895` (with T03 intro), `1482:2912`, `1482:2925`, `1482:2938`. Screenshots `figma-T07-routine-step-1-intro-10-20.png` … `-4-`, `figma-T07-routine-outline-card-10-20.png`.

Band: gradient top to bottom **`#FFFFFF` → `#0CAB97`** (`color.gradient_teal_light`); bands do not clip; each band ends with a white wave (down) except the last.

**Outline card** (`1482:2896` …): 521 wide at x 40.4 to 40.6, stroke **2 inside `#55B5AC`** (`color.line`), radius 20, no fill, auto layout padding **32** all sides, gap 15. Heights 152, 176.5, 173.5, 176.5.
- Step label: **Rubik Bold 24.3/100% uppercase `#05453D`, left aligned** ("Upgrade Your Brush", "Rethink Your Toothpaste", "Add A Rinse", "Refresh Your Freshness"). Token `type.label_*`.
- Body: NK Medium 18/120% -3% `#05453D`, left. Token `type.caption_*`. Column 248.5 to 302 wide; forced line breaks in step 3.
- Text sits in the left half (steps 1 and 3) or right half (steps 2 and 4; the auto layout gets a **244 left padding**, text column starts at x 316.4).

**Product block** (outside the card, below it, same side as the card text):
- Product name: **Rubik Bold 24.3/100% uppercase `#05453D`, left aligned**, 2 to 3 lines (41.5 to 66). Token `type.label_*`.
- Gap 24 → Shop Now B01 144.1 x 50.3, **white fill, `#05453D` Rubik label**.
- Card bottom → product name: 36 (step 1: 1333.2 → 1369.5), 36 (step 2), 35 (step 3), 36 (step 4).

**Packshot** on the opposite side, large, overlapping the card edge:

| Step | Product | Box | Rotation | Position |
|---|---|---|---|---|
| 1 | Antiplaque Adult Soft Toothbrush | 463 x 463 | -18° | right, from x 213.5 |
| 2 | Whiten Plus Deep Clean Spearmint box | 332.5 x 199.5 | 17° | left, bleeds off x -32.2 |
| 3 | Whole Care Fresh Mint mouthwash | 431 x 425.5 | 0° | right, from x 242.5 |
| 4 | North Woods deodorant | 321 x 321 | 0° | left, from x 3 |

Alternation: text left / product right (steps 1, 3), text right / product left (steps 2, 4). Band heights 569 (with intro), 451.5, 447.5, 436. Card top from band top: 179.7 (after intro), 35.5, 37.2, 35.5.

## T08 Need row

10/13 band `1482:68`. Rows `1482:2657`, `1482:2672`, `1482:2688`, `1482:2703`. Screenshots `figma-T08-need-rows-band-10-13.png`, `figma-T08-need-row-10-13.png`.

Band: gradient top to bottom `#008D83` → `#55B5AC` (`color.gradient_teal`) + T16 leaf-vein texture; T03 intro white; rows stacked with **gap 40**; closing CTA `#05453D` fill, white label.

Each row (521 wide at x 39.3, auto layout vertical, **gap 8**):
1. **Label pill** 521 x 77 (75.5 last), radius 20, stroke **3 inside `#91FFF5`**, padding 16 top/bottom, 32 sides, gap 15. Fill steps lighter down the list: **`#0C9389`** (Cavity Protection, Whitening), **`#30A39A`** (Sensitivity Relief), **`#41ACA3`** (Fresh Breath).
   - Title NK SemiBold 24/120% -1% white, centre. Token `type.item_*`.
   - One-liner NK Medium 18/120% -3% white, centre (16 in Fresh Breath, to fit one line). Token `type.caption_*`.
2. **Split product card** 521 x 255.6, radius 20, clips content, fill **`#A0E0FB`** (light blue half).
   - Dark half: `#05453D` panel, 260.5 wide (the panel layer is drawn 286.5 to 301 wide and clipped at the card edge, so the split sits at x 299.5, about 50/50).
   - Product name NK SemiBold 16/120% -1% white, centre, 193.5 column, 2 to 3 lines. Token `type.product_name_*`.
   - Gap 15.8 → B02 small button, **white fill, `#05453D` label**.
   - Light half: transparent packshot 212 x 167.5 (Sensitive box upright 212 x 227.5), centred in the half.
   - Alternation: packshot left / panel right (rows 1 and 3), panel left / packshot right (rows 2 and 4).
- `Sensitivity Relief` one-liner carries an asterisk; the matching disclaimer goes in the footer (T18 variant).

## T09 Category row stack

10/8 `1482:3042` (in deep band `1482:3034`) and 10/27 `1482:3457` (in band `1482:3449`). Screenshots `figma-T09-category-rows-band-10-08.png`, `figma-T09-category-rows-band-10-27.png`, `figma-T09-category-row-image-left-10-08.png`, `figma-T09-category-row-short-10-27.png`.

- Stack: 4 rows, **498.5 wide** at x 50.5, **gap 15**.
- Row: radius **40**, clips content. Row height **255.6 (10/8)** or **200 (10/27, same layers cropped)**.
- Split line always at x 314.8: left part 264.3, right part 234.2.
  - Photo part: lifestyle shelf scene (`lifestyle-tile-shelf-oral-care-deodorant-soap.jpg`, a different CROP per row; Value Bundles uses `lifestyle-tile-shelf-value-bundle.png`). The photo layer is 279.5 wide and starts 15 outside the row on the left rows (clipped).
  - Panel part: vertical gradient `#FFFFFF` → `#E8E8E8`. Content centred: category name **NK Bold 24/120% -1% `#044D44`** (1 or 2 lines), gap 15.8, B02 small button `#05453D` fill, white label.
- Alternation: photo left (rows 1, 3) / photo right (rows 2, 4). Row order and names: Oral Care, Bath & Body, Deodorant & Antiperspirant, Value Bundles (same in both emails).
- Band variations:
  - 10/8: band gradient top to bottom `#05453D` 0% → `#38A698` 51% → `#05453D` 100% (`color.gradient_deep`; gradientTransform `[[0,1,0],[-0.42,0,0.73]]`, so the light middle is compressed), intro white, closing CTA white "Explore All Products" 293.1 wide.
  - 10/27: band gradient top to bottom **`#3DA79D` → `#C8EEEB`**, intro `#05453D`, rows 200 tall, closing CTA white "Explore Everyday Essentials" 379.6 wide.

## T10 Values grid 2x2

10/27 band `1482:3274`. Screenshots `figma-T10-values-grid-2x2-band-10-27.png`, `figma-T10-values-card-10-27.png`.

- Band: gradient `#FFFFFF` → `#E8E8E8`, auto layout padding **60 top/bottom, 5 sides**, content column 520 wide, gap **30** (heading block → grid → CTA).
- Heading block (gap 20): T03 heading "What makes us Tom's of Maine" with "Tom's of Maine" in `#008D83`; subtitle Rubik Bold 22.3/130% uppercase `#05453D` (321.6 wide).
- Grid: **2 columns of 255, gutter 10, row gap 10**, 520 wide at x 40.
- Card: 255 x 296.5 (297 bottom row), **stroke 2 inside `#00867D`** (`color.card_line_values`), radius **22.4**, transparent fill, auto layout padding **28 top/bottom, 25 sides**; inner stack gap 20 (icon+title block → body), icon → title gap 12.
  - Icon: circle 55.7, fill **`#008D84`**, white glyph (leaves, shield-check, cash, recycle). Assets `icon-value-*.png`.
  - Title: Rubik Bold 18.1/100% uppercase `#044D44`, centre, 2 lines. Token `type.label_small_*`. Leading trim off on these.
  - Body: NK Medium 18/120% **-1%** `#044D44`, centre. Text widths vary by card (181 to 241.7), set by hand. Token `type.caption_*` with -1% (variant).
  - Bottom-right card is taller in content and the icon block starts higher (+16 instead of +26 from the card top) because the card keeps 297 height; content is not vertically centred consistently.
- Closing CTA `#05453D`, "Learn About Our Mission" 321.1 wide.
- Exit: `#3DA79D` wave (down) into the 10/27 category band.

## T11 Claims ring

10/22 hero. Five items around the product, each: check icon 36.4 (white circle with cut-out check, blend **soft light**) → gap 14.9 → claim in NK SemiBold **19.8**/120% -1% `#05453D` (18.3 for the two long claims), centre.

| Claim | Item box | Position |
|---|---|---|
| Natural | 88.5 x 65.3 | top centre, x 255.5, y 501.5 |
| Aluminum Free | 146.7 x 89.3 | left, x 31, y 524 |
| Dermatologically/Dermatologist-Tested | 199.3 x 108.3 | left, x 4.5, y 638.8 |
| 100% Recyclable | 204.3 x 89.3 | right, x 391, y 524 |
| No Artificial Dyes, Flavors, or Preservatives | 187 x 108.3 | right, x 399.5, y 638.8 |

Column centres: left about 104 to 105, right about 493. Claim text uses dark `#05453D` over the bright sky part of the photo. NEW token `type.claim_*`.

## T12 Band closing CTA

Last element of a band, centred, B01. Gap above it: 40 (auto layout bands) or 35.5 (10/2). Fill follows the band: `#05453D` with white label on light bands (10/2, 10/13 teal band, 10/27 values), white with `#05453D` label on dark or saturated bands (10/8 deep, 10/22 `#05453D`, 10/27 teal). Labels: Stock Up & Save (216.6 wide), Explore All Products (293.1), Learn About Our Mission (321.1), Explore Everyday Essentials (379.6). Always Rubik.

## T13 Wave divider

One path for every wave (`assets/wave.svg`), 603.6 x 62.9, placed at the bottom of a band (it overhangs the right edge by 3.6). "Up" = fill below the curve (as drawn); "down" = the same layer rotated 180°. Fill = color of the adjoining band.

| Email | Node | Color | Orientation | Where |
|---|---|---|---|---|
| 10/8 | `1482:2998` | white | up | hero bottom |
| 10/8 | `1482:3008` | white | down | Coconut Oil band bottom |
| 10/8 | `1482:3027` | `#05453D` | down | Sea Salt band bottom, into deep band |
| 10/13 | `1482:25` | `#008D83` | up | hero bottom, into teal band |
| 10/20 | `1482:2907`, `1482:2923`, `1482:2937` | white | down | routine band bottoms |
| 10/22 | `1482:3162` | `#05453D` | up | hero bottom |
| 10/27 | `1482:3273` | white | down | hero bottom |
| 10/27 | `1482:3448` | `#3DA79D` | down | values band bottom |

## T14 Scallop divider

10/2 `1482:2771`: five white circles, diameter 201.7, centres 121.7 apart, row starting at x -45.9, top at y 950 (50.5 above the hero bottom). The hero clips them, so only a **50.5 tall scalloped white strip** shows, merging into the white top of the next band. Asset `divider-scallop-white.png` (1200x101).

## T15 Decor

- **Leaf sprig** (line art, one drawing): `#008D83` in 10/8 (163.5 x 194.3 and 121.6 x 144.5, rotations 158°, 42°, 135°, 11°), `#05453D` in 10/22 (147.9 x 175.7, 157.9 x 187.6, rotations 97°, 160°). Always cut by the email edge, one per side, never over text.
- **Fern sprig** (finer drawing, "Vrstva_1"): `#CCFFFA`, blend soft light, 128.7 x 195.8 frame, 10/13 hero only.
- **Sparkle**: 4-point, 10.2 x 13.7, `#CCFFFA` 80%, soft light, 10/13 hero only.
- Every hero frame also contains two empty frames named "_Layer_" (58.5 x 63 and 31.5 x 40) placed outside the visible area; they render nothing.

## T16 Leaf-vein texture

10/13 band `1482:68`: band gradient `#008D83` → `#55B5AC` plus group `1482:69` (2579 vector strokes, `#06554B`, rotated 90°, blend **soft light**) covering the band from 229.5 below its top. Assets `texture-leaf-veins.svg`, `texture-leaf-veins-06554b.png` (texture only) and `bg-band-teal-gradient-leaf-veins.jpg` (texture composited on the gradient as in Figma).

## T17 Circular portrait

10/2 `1482:2764`, 279.3 x 279.3: photo ellipse 245.3 diameter (FILL, `lifestyle-man-smiling-holding-toothpaste-blue-sky.jpg`), centred; ring ellipse 279.3 outer diameter, **stroke 6.5 `#00867D`** (centre stroke), no fill. Gap between ring inner edge and photo: 10.4. Asset `ring-portrait.png`.

## T18 Footer

All 6 emails, group "Group 12" (`1482:2834` and copies), 600 x 587. Screenshots `figma-T18-footer-10-02.png`, `figma-T18-footer-disclaimer-10-13.png`, `figma-T18-footer-social-row-10-02.png`. Identical in 5 emails; 10/13 adds a disclaimer line.

**Background blocks**
- Main block `Rectangle 8`: `#295791`, **599.5 x 455.5 at x 0.5** (leaves a 0.5 px sliver at the left edge; visible as a hairline in the renders).
- Legal bar `Rectangle 9`: `#24436F`, 600 x 131.5, from footer y 455.5 to 587.

**Main block content** (y from footer top, all centred on the 600 axis, all white)
| y | Element | Spec |
|---|---|---|
| 32 | (10/13 only) disclaimer "*For rapid relief, apply the product directly to the sensitive tooth with a fingertip and gently massage for 1 minute." | **Gotham Medium 10/100%**, white, centre, box 310 x 20 at x 145 (2 lines). NEW token |
| 79 | "Learn what we mean by natural on our website." | Gotham Bold 14/20, **underlined**, box 471.6 wide at x 64.4 (box is 76 tall because the layer ends with an empty line; the visible line is the first 20) |
| 126.5 | Logo | white badge, raster `image 17`, **101.4 x 82 at x 249.8** (centred). Asset `logo-dark.png` |
| 238.5 | Social row | 5 cells of **32 x 32, no gap**, row 160 wide at x 220.3: X (glyph 23.1 x 21.1), Facebook (11.7 x 20.9), Instagram (21 x 21.1), TikTok (18.3 x 21.1), Pinterest (15.6 x 20.8). White. X, Facebook, Instagram, TikTok are vectors; Pinterest is a raster PNG |
| 294 | Nav list | "Our Mission / Products / Shop Now / Blog", one text layer with line breaks, **Gotham Bold 14/28**, sentence case (not uppercase), box 471.6 x 117 at x 64.4 |

Gaps: logo bottom (208.5) → social top 30; social bottom (270.5) → nav top 23.5; nav last line ends about 406, block ends 455.5.

**Legal bar content** (y from footer top; each line is its own text layer, 535.6 wide at x 32.5, Gotham Bold 10/28 white, centre)
| y | Text |
|---|---|
| 470 | Tom's of Maine · 2 Storer Street, Suite 302 · Kennebunk, ME 04043 · USA |
| 503.5 | ©%%= v(@CurrentYear) =%% Tom's of Maine, Inc. |
| 541 | Privacy Policy  l  Terms of Sale  l   Terms of Use  l  Unsubscribe |

The separator in the links line is a **lowercase letter "l" typed with two spaces each side** (three spaces before "Terms of Use"), not a pipe or a vector rule. The copyright line carries the SFMC AMPscript year in the design itself.

Token check: footer texts match `type.nav_size`/`legal_size` but the **legal line height is 28 in Figma** (token `legal_line` is 14).

## B01 Button, standard

- Height **50.3**, radius **11.7**, auto layout padding 17.5 (Rubik labels), width hugs the label (+35). Hero buttons in Gotham are not auto layout in 10/2 but follow the same box.
- Label 20.7/29.6, uppercase, tracking 0. **Hero CTAs use Gotham Bold** (5 of 6 heroes), **band CTAs and Shop Now buttons use Rubik Bold**.
- Fills: `#05453D` + white label, or white + `#05453D` label. No other fills, no stroke, no shadow.
- Shop Now size: 144.1 x 50.3.
- Screenshots `figma-B01-button-hero-gotham-dark-10-02.png`, `figma-B01-button-rubik-white-10-08.png`.

## B02 Button, small

- **139 x 42.8, radius 10.1**, fixed width (label box 95 x 18 centred, not hugging).
- Label "shop now" typed lowercase, shown uppercase via text case: Rubik Bold 18.1/100%.
- `#05453D` fill + white label (T04, T09), or white fill + `#05453D` label (T08).
- Screenshot `figma-B02-button-small-10-02.png`.

---

## Type mapping summary

| Text | Spec (600px) | Token |
|---|---|---|
| Hero headline | NK SemiBold 64/90%, -2% (-3% at 97% line in 10/27, -7% in 10/20) | `display_*` (tracking and line variants are NEW) |
| Hero headline large | NK SemiBold 76.4/90% (68.8), -7% | `display_compact_*` (76/69) |
| Hero kicker, ruled | Rubik SemiBold 25.2/100% uppercase | NEW `kicker_*` (README mentions it, tokens.json has no key) |
| Hero kicker, small | Rubik Bold 20 to 20.3, line 130% (10/2) or 100% (10/8), uppercase | NEW `kicker_small_*` |
| Hero body | NK Medium 20/120% -1% (19.5 in 10/8, 10/20) | `body_*` |
| Band heading | NK Bold 42/105% (44.1) | `h2_*` |
| Band subtitle | Rubik Bold 22.3/130% uppercase | `subtitle_*` |
| Band intro | NK Medium 19.5/120% (23.4) -1% | `body_*` at 19.5: NEW `intro_*` |
| Item / ingredient / product title | NK SemiBold 24/120% (28.8) -1% | `item_*` |
| Category name | NK **Bold** 24/120% -1% `#044D44` | NEW `item_bold` (or `item_weight` variant 700) |
| Card product name (10/2) | NK Medium 18/120% -1% `#044D44` | NEW `card_name_*` |
| Need-row product name | NK SemiBold 16/120% (19.2) -1% | `product_name_*` |
| Card body / description | NK Medium 18/120% (21.6) -3% | `caption_*` (values cards use -1%) |
| Rubik label (routine step, routine product) | Rubik Bold 24.3/100% uppercase | `label_*` |
| Rubik small label (values title) | Rubik Bold 18.1/100% uppercase | `label_small_size` |
| Claim | NK SemiBold 19.8/120% -1% (18.3 long) | NEW `claim_*` |
| Button label | Rubik Bold or Gotham Bold 20.7/29.6 uppercase | `button.font_size` 20 / `line_height` 30 |
| Small button label | Rubik Bold 18.1/100% uppercase | `button.compact_*` |
| Header nav | Gotham Bold 14/auto uppercase `#00867D` | `nav_*` |
| Footer link / nav | Gotham Bold 14/20 underlined; 14/28 | `nav_*` |
| Footer legal | Gotham Bold 10/28 | `legal_size` (line differs) |
| Footer disclaimer | Gotham Medium 10/100% | NEW `disclaimer_*` |

## Colors seen that are not in tokens.json

| Hex | Where |
|---|---|
| `#044D44` | product names (10/2 cards), category names, values cards (README treats it as `#05453D`; it is used consistently on these card texts) |
| `#0C9389`, `#30A39A`, `#41ACA3` | need-row label pills, darker to lighter |
| `#91FFF5` | need-row pill stroke (3 px) |
| `#A0E0FB` | need-row card light half |
| `#97DCFB`, `#3697D6` | 10/13 hero base fill and gradient |
| `#C8EEEB` | product card sheen stop; end of the 10/27 category band gradient |
| `#7DCDC5`, `#E1EBEB` | product card base gradient (fully covered, invisible) |
| `#3DA79D` | 10/27 category band gradient start and its wave |
| `#00535B` | 10/22 hero top overlay |
| `#031311` | 10/27 hero bottom overlay |
| `#008D84` | values icon circles (1 step off `#008D83`) |
| `#489E98` | 10/8 inner frame fill (guideline Tint), never visible behind the sections |

## Proposed token additions

```json
{
  "type": {
    "kicker_size": 25, "kicker_line": 25, "kicker_weight": 600, "kicker_transform": "uppercase",
    "kicker_rule_weight": "1.7px", "kicker_rule_gap": "14.6px",
    "kicker_small_size": 20, "kicker_small_line": 26, "kicker_small_weight": 700,
    "intro_size": 19.5, "intro_line": 23.4, "intro_weight": 500, "intro_tracking": "-0.01em",
    "display_line_alt": "97%", "display_tracking_tight": "-0.07em", "display_tracking_alt": "-0.03em",
    "card_name_size": 18, "card_name_line": 21.6, "card_name_weight": 500, "card_name_tracking": "-0.01em",
    "item_bold_weight": 700,
    "claim_size": 19.8, "claim_line": 23.8, "claim_weight": 600, "claim_size_long": 18.3,
    "disclaimer_size": 10, "disclaimer_line": 10, "disclaimer_family": "Gotham Medium",
    "legal_line_measured": 28
  },
  "color": {
    "text_card": "#044D44",
    "need_pill_1": "#0C9389", "need_pill_2": "#30A39A", "need_pill_3": "#41ACA3", "need_pill_line": "#91FFF5",
    "need_card_light": "#A0E0FB",
    "hero_sky": "#97DCFB", "hero_sky_deep": "#3697D6",
    "card_sheen": "#C8EEEB",
    "teal_mid": "#3DA79D",
    "overlay_teal": "#00535B", "overlay_forest": "#031311",
    "icon_circle": "#008D84",
    "gradient_card": "linear-gradient(135deg,#FFFFFF 0%,#C8EEEB 51%,#FFFFFF 100%)",
    "gradient_band_light_43": "linear-gradient(180deg,#FFFFFF 0%,#E8E8E8 43%)",
    "gradient_mint": "linear-gradient(180deg,#3DA79D 0%,#C8EEEB 100%)",
    "gradient_sky": "linear-gradient(180deg,rgba(151,220,251,0) 36%,#3697D6 100%)"
  },
  "button": { "hero_family": "Gotham Bold", "band_family": "Rubik Bold", "height": 50.3, "compact_width": 139, "compact_height": 42.8 },
  "radius": { "row": "40px", "values_card": "22.4px", "pill": "20px", "button": "11.7px", "button_compact": "10.1px" },
  "space": {
    "section_gap": "40px", "grid_gutter": "15px", "values_gutter": "10px", "row_gap": "15px",
    "need_row_gap": "40px", "pill_to_card": "8px", "hero_stack_gap": "24px",
    "card_pad_product": "26.5px 20.5px", "card_gap_product": "20px", "name_to_button": "10.8px",
    "card_pad_ingredient": "40px 32px", "card_pad_routine": "32px", "card_pad_values": "28px 25px",
    "grid_width": "521px", "row_stack_width": "498.5px", "content_side": "39.5px"
  },
  "size": {
    "product_card": "253x350 to 371", "product_image": "212x167.5 / 169.5x169.5",
    "need_card": "521x255.6", "category_row": "498.5x255.6 (or 200)", "category_split_x": 314.8,
    "values_card": "255x296.5", "value_icon": 55.7, "check_icon": 36.4,
    "social_cell": 32, "footer_logo": "101.4x82", "header_logo_box": "126.5x102.5", "header_logo_visible": "94.5x76",
    "wave": "603.6x62.9", "ring_stroke": 6.5, "portrait": 245.3, "portrait_ring": 279.3
  }
}
```

`gradient_card` angle (135deg) is an approximation of the Figma gradientTransform `[[-0.39,0.57,0.37],[-0.57,-0.66,1.12]]`, not a measured value; the stops are exact.

Also adjust: `assets.logo_width` / `logo_height` (tokens say 120x50; the real header box is 126.5x102.5, visible badge 94.5x76, ratio about 1.24, not 2.4), `space.band_y` (60 only in one band; most bands are 45 to 55 top), `space.header_height` 110.5, `type.legal_line` 28.

## Open questions

1. **Header and footer slicing.** None of the slices cover the header (0 to 110.5) or the footer. Are they a fixed HTML wrapper in SFMC, or exported as separate images outside these frames? This decides whether the footer links (natural page, 4 nav links, 5 social icons, legal links) need their own slices.
2. **10/20 frame height.** The 10/20 inner frame is 3440 tall and clips the footer at 3440, cutting the last 52.5 (the Privacy / Terms / Unsubscribe line). Approved as is, or a frame-size slip?
3. **Vector logo.** The only logos in the file are raster PNGs (1368x1056 teal, 780x629 white). Is there an official SVG/AI from the client? Needed for crisp larger uses.
4. **Pinterest icon** is a raster PNG while the other four social icons are vectors. Keep, or replace with a vector glyph?
5. **Hero CTA family.** Gotham Bold on 5 hero CTAs and Rubik Bold on the 10/8 hero CTA and every band CTA. Is Gotham the rule for hero CTAs, or is 10/8 the newer standard?
6. **Two product-name styles in the 2-up grid** (10/2 Medium 18 `#044D44`, 10/22 SemiBold 24 `#05453D`). Which is the standard? 10/2 fits 3 lines of long names at 18; 10/22 needs 24 for short deodorant names.
7. **`#044D44` vs `#05453D`.** `#044D44` is used consistently on card texts (product names, category names, values cards). Keep it as its own token (`text_card`) or normalise to `#05453D`?
8. **Footer hairline.** The navy block starts at x 0.5 (599.5 wide), leaving a 0.5 px light line at the left in every footer. Fix in new emails?
9. **Low-res packshots.** Whole Care Peppermint box, Wicked Fresh box, Fresh Mint mouthwash and Sea Salt mouthwash are 600x600 sources but are displayed up to 431 (862 at 2x) and 534.9 rotated. Higher resolution originals from the client?
10. **Hidden white-background packshots** are attached under most cut-outs. Treat them as approved alternates for the image bank?
11. **Glass effect (10/8 hero).** Figma's GLASS effect renders only in Figma; exports bake it. Fine for the sliced workflow, but any non-Figma tool cannot reproduce it.
12. **Band padding.** Top padding varies 31.5 to 60 by email. Standardise (proposal: 50) or keep per email?
13. **`assets/source/` weight.** The 42 originals total about 95 MB and the folder is not covered by `.gitignore` (only `01-brand/photos/**` and `email-kit/references/*.png` are). Add `clients/*/01-brand/email-kit/assets/source/` to `.gitignore` before committing?

## What could not be extracted

- **Logo SVG**: no vector logo in the page (raster only).
- **Pinterest SVG**: raster only in Figma.
- **Figma GLASS effect** and **soft light** blends cannot be reproduced in SVG/PNG exactly; the soft-light assets are exported in normal blend and flagged.
- Footer link URLs: not needed (owner).
