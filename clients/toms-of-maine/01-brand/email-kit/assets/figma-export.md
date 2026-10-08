# Figma export log · Tom's of Maine email kit

Source: Figma file VAZIO DRAFT (`8oGyJxpeGLPWNiH54vePwS`), page `1482:2`, the 6 approved Oct 2026 emails. Exported 2026-10-06 (read-only access, nothing changed in Figma).

Conventions:
- **Display** = size at the 600px email (Figma frames are 1200px = 2x; every value halved).
- **2x file** = the PNG/JPG to use in a 600px layout (2x of display).
- Raw originals in `source/` are byte-identical to the image uploaded in Figma: the SHA-1 of each file equals the Figma `imageHash` (first 8 chars listed), so any file can be traced back to its fill.
- The emails ship as **sliced JPGs** (designed in Figma, exported, sliced). Assets below are for composing new emails in the same way.

## 1. Logo

No vector logo exists on the page: both logos are **raster PNG fills** (`image 1` in the header, `image 17` in the footer). An SVG could not be exported. The vector should come from the client's brand files (see open questions in `../inventory/figma-modules.md`).

| File | Source node | Original px | Display | 2x file | Use |
|---|---|---|---|---|---|
| `logo-light.png` | `1482:2756` (header, same image in all 6 headers: `1482:2983`, `1482:7`, `1482:2871`, `1482:3124`, `1482:3259`) | 1368x1056, hash `345d2351` | box 126.5x102.5 (visible badge 94.5x76 inside, offset 15.75 / 16) | 253x205, transparent | header logo on white. Built from the raw PNG with the layer's CROP transform (crop box x 302 to 1034, y 193 to 787 of the source), so it keeps the exact Figma box and padding |
| `logo-light-hires.png` | same | same | same box | 732x593 (about 5.8x), transparent | same crop at full source resolution, for larger uses |
| `logo-dark.png` | `1482:2837` (footer, same image in all 6 footers: `1482:3086`, `1482:2724`, `1482:2953`, `1482:3225`, `1482:3503`) | 780x629, hash `671cac09` | 101.4x82 | 203x164, transparent, white badge | footer logo on navy, dark mode |
| `source/logo-badge-teal-source.png` | `1482:2756` | 1368x1056 | | raw | teal badge "The Original Tom's of Maine", lots of transparent padding |
| `source/logo-badge-white-source.png` | `1482:2837` | 780x629 | | raw | white badge, tight bounds |

The template's `logo-light.png` / `logo-dark.png` samples were replaced. Every other template sample (`sample-*.jpg`, `portrait-*.jpg`, `product-1.png`, `texture-*.jpg`) was kept untouched.

## 2. Social icons (footer)

Five 32x32 cells (display) in a row, no gap between cells, white glyphs. Order: X, Facebook, Instagram, TikTok, Pinterest. X, Facebook, Instagram, TikTok are vectors; **Pinterest is a raster PNG** in Figma (`image 18`), so there is no SVG for it.

| File | Source node | Display | 2x file | Note |
|---|---|---|---|---|
| `icon-x.svg` / `icon-x.png` | cell `1482:2844`, glyph `1482:2845` | cell 32x32, glyph 23.1x21.1 | 64x64 | white |
| `icon-facebook.svg` / `.png` | cell `1482:2846`, glyph `1482:2847` | cell 32x32, glyph 11.7x20.9 | 64x64 | white |
| `icon-instagram.svg` / `.png` | cell `1482:2848`, glyph group `1482:2849` | cell 32x32, glyph 21x21.1 | 64x64 | white. The standalone glyph SVG was re-wrapped into the 64 cell at the exact offset read from the group export (11.28, 11.00 at 2x) |
| `icon-tiktok.svg` / `.png` | cell `1482:2854`, glyph `1482:2855` | cell 32x32, glyph 18.3x21.1 | 64x64 | white |
| `icon-pinterest.png` | cell `1482:2856`, image `1482:2857` | cell 32x32, glyph 15.6x20.8 | 64x64 | rebuilt from the raw PNG at the layer offset (15.8, 13.8 at 2x); raster only |
| `source/icon-pinterest-white-source.png` | `1482:2857` | | 389x512 raw, hash `4955f8fe` | |
| `social-row.svg` / `social-row.png` | group `1482:2843` | 160x32 | 320x64 | the whole row; the SVG embeds the Pinterest PNG. The grey `#989898` background that Figma adds to exports was removed |

## 3. Decorative elements

| File | Source node(s) | Display | 2x file | Use |
|---|---|---|---|---|
| `wave.svg` | `1482:2998` (path identical on every wave in the 6 emails) | 603.6x62.9 (overhangs the 600 frame by 3.6) | 1207x126 | band transition. Fill is the band below; one SVG, recolor via `fill` |
| `wave-white-up.png` / `wave-white-down.png` | white: `1482:2998` (up, 10/8 hero), `1482:3008`, `1482:2907`, `1482:2923`, `1482:2937`, `1482:3273` (down = rotated 180°) | 603.6x62.9 | 1207x126 | |
| `wave-05453d-up.png` / `-down.png` | `1482:3162` (up, 10/22 hero), `1482:3027` (down, 10/8) | same | same | |
| `wave-008d83-up.png` / `-down.png` | `1482:25` (up, 10/13 hero) | same | same | down variant not used in Figma, rendered for completeness |
| `wave-3da79d-up.png` / `-down.png` | `1482:3448` (down, 10/27) | same | same | up variant not used in Figma |
| `divider-scallop.svg` / `divider-scallop-white.png` | `1482:2771` (5 white circles, 201.7 diameter, 121.7 apart) | visible strip 600x50.5 (hero clips the circles) | 1200x101 | bottom edge of the 10/2 hero (cloud / scallop edge into the next white band) |
| `ring-portrait.svg` / `ring-portrait.png` | `1482:2766` | 279.3 outer diameter, stroke 6.5 `#00867D` | 559x559 | ring around the circular portrait in the 10/2 hero |
| `leaf-sprig.svg`, `leaf-sprig-008d83.png` | `1482:2999`, `1482:3000`, `1482:3019`, `1482:3033` (10/8) | 163.5x194.3 (also used at 121.6x144.5) | 327x389 | line-art leaf sprig, `#008D83`, rotated freely (158°, 42°, 135°, 11°) |
| `leaf-sprig-05453d.png` | `1482:3160`, `1482:3161` (10/22) | 147.9x175.7 and 157.9x187.6 | 327x389 | same sprig drawing in `#05453D` (10/22 SVG `s3126_b` is the same path, scaled) |
| `leaf-sprig-fern-soft-light.svg`, `leaf-sprig-fern-ccfffa.png` | `1482:10`, `1482:42`, `1482:55` "Vrstva_1" (10/13) | 128.7x195.8 frame (rotated 2°, -108°, -178°) | 244x383 | different, finer sprig. `#CCFFFA`, blend **soft light** in Figma; the PNG is rendered in normal blend, so on a photo it reads brighter than in Figma |
| `sparkle-soft-light.svg`, `sparkle-ccfffa.png` | `1482:37` to `1482:41` (10/13) | 10.2x13.7 | 20x27 | 4-point sparkle, `#CCFFFA`, opacity 80%, soft light |
| `icon-check-soft-light.svg`, `icon-check-white.png` | `1482:3131` (5 instances, 10/22) | 36.4x36.4 (glyph 27.3) | 73x73 | white filled circle with cut-out check ("lets-icons:check-fill"), blend soft light |
| `icon-value-leaves-naturally-high-standards.svg/.png` | `1482:3283` | 55.7 circle | 111x111 | `#008D84` circle + white glyph (the glyph is ~200 tiny vector fragments, hence the 277 KB SVG) |
| `icon-value-shield-certified-b-corp.svg/.png` | `1482:3419` | 55.7 | 111x111 | |
| `icon-value-cash-ten-percent-profits.svg/.png` | `1482:3427` | 55.7 | 111x111 | |
| `icon-value-recycle-designed-for-planet.svg/.png` | `1482:3437` | 55.7 | 111x111 | |
| `texture-leaf-veins.svg`, `texture-leaf-veins-06554b.png` | group `1482:69` (2579 vectors, rotated 90°) | covers the 10/13 band from 229.5 below its top to its bottom | 1200x3226, transparent | leaf-vein line texture, `#06554B`, blend soft light over the teal gradient. Exported texture-only (normal blend) |
| `bg-band-teal-gradient-leaf-veins.jpg` | band `1482:68` fill + `1482:69` | 600x1613 (lower 1613 of the 1842.5 band) | 1200x3226 JPG 78 | the 10/13 band background as Figma renders it: gradient `#008D83` → `#55B5AC` with the texture in soft light |

Figma node exports (`download_assets` export renders) come composited on a grey `#989898` background, so every transparent PNG above was rebuilt from the raw source or rasterized from the SVG (headless Chrome, transparent background).

## 4. Photos and packshots (image bank) → `source/`

Every raw image fill used across the 6 emails: 42 files, about 95 MB. "Hidden fill" = an image fill that exists on the layer but is switched off (invisible in the email); they are the white-background versions of the same packshots, kept because they are useful for other layouts. "Stacked, covered" = visible fill sitting under an opaque fill on the same layer, so it never shows.

Kinds: **packshot transparent** (cut-out PNG), **packshot white bg**, **lifestyle** (people or in-use scene), **scene** (product styled in a set, used full-bleed), **texture** (background surface), **logo / icon**.

| # | File (`source/`) | Hash | Original px | Product / subject | Kind | Used in (node, email, display box) |
|---|---|---|---|---|---|---|
| 1 | `logo-badge-teal-source.png` | `345d2351` | 1368x1056 | Tom's of Maine badge, teal | logo | header of all 6 (`1482:2756` …), 126.5x102.5 CROP |
| 2 | `logo-badge-white-source.png` | `671cac09` | 780x629 | Tom's of Maine badge, white | logo | footer of all 6 (`1482:2837` …), 101.4x82 |
| 3 | `icon-pinterest-white-source.png` | `4955f8fe` | 389x512 | Pinterest glyph, white | icon | footer of all 6 (`1482:2857` …), 15.6x20.8 |
| 4 | `bg-white-cream-swirl-texture.jpg` | `afd723ae` | 2326x2907 | white cream / paste swirl macro | texture | 10/2 hero background `1482:2758`, 600x890 CROP |
| 5 | `lifestyle-man-smiling-holding-toothpaste-blue-sky.jpg` | `0ed6b63c` | 3277x4096 | man smiling, holding a Tom's toothpaste tube, blue sky | lifestyle | 10/2 hero circle `1482:2765`, 245.3 circle FILL |
| 6 | `packshot-whole-care-peppermint-toothpaste-box.png` | `cbc7dfd9` | 600x600 | Whole Care Peppermint Natural Toothpaste with Fluoride (box) | packshot transparent | 10/2 card `1482:2785` 212x167.5; 10/13 Cavity row `1482:2671` 212x167.5 |
| 7 | `packshot-whole-care-peppermint-toothpaste-box-white-bg.png` | `80c0b643` | 600x600 | same, white background | packshot white bg | hidden fill under `1482:2785`, `1482:2801`, `1482:2671`, `1482:2702`, `1482:2718` |
| 8 | `packshot-whiten-plus-deep-clean-peppermint-toothpaste-box.png` | `73a7cdbf` | 1800x1800 | Whiten Plus Deep Clean Whitening Peppermint Natural Toothpaste (box) | packshot transparent | 10/2 card `1482:2793` 212x167.5; 10/13 Whitening row `1482:2687` 212x167.5 |
| 9 | `packshot-whiten-plus-deep-clean-peppermint-toothpaste-box-white-bg.png` | `ef9cdb5a` | 1800x1800 | same, white background | packshot white bg | hidden fill under `1482:2793`, `1482:2687` |
| 10 | `packshot-wicked-fresh-spearmint-ice-toothpaste-box.png` | `9895c599` | 600x600 | Wicked Fresh! Spearmint Ice Fluoride Natural Toothpaste (box) | packshot transparent | 10/2 card `1482:2801` 212x167.5; 10/13 Fresh Breath row `1482:2718` 212x167.5 |
| 11 | `packshot-wicked-fresh-spearmint-ice-toothpaste-box-white-bg.png` | `a2fbe88b` | 600x600 | same, white background | packshot white bg | hidden fill under `1482:2801`, `1482:2718` |
| 12 | `packshot-whole-care-fresh-mint-mouthwash.png` | `61e14b48` | 600x600 | Fresh Mint Whole Care Anticavity Natural Mouthwash | packshot transparent | 10/2 card `1482:2809` 169.5x169.5 (radius 12); 10/20 hero cluster `1482:2890`/`1482:2894` 431x425.5; 10/20 step 3 `1482:2936` 431x425.5 |
| 13 | `packshot-antiplaque-spearmint-flat-floss.png` | `9757ea59` | 512x512 | Antiplaque Spearmint Natural (flat) Floss | packshot transparent | 10/2 card `1482:2817` 212x169.5 FIT |
| 14 | `packshot-antiplaque-spearmint-flat-floss-alt.png` | `78d741c0` | 512x512 | same, white background | packshot white bg | hidden fill under `1482:2817` |
| 15 | `packshot-antiplaque-adult-soft-toothbrush.png` | `e28775c8` | 1800x1800 | Antiplaque Adult Soft Toothbrush (in pack) | packshot transparent | 10/2 card `1482:2825` 169.5x167.5 CROP; 10/20 step 1 `1482:2902` 463x463 rotated -18° |
| 16 | `bg-green-leaf-macro.jpg` | `f9f65fdc` | 2600x1950 | green tropical leaf macro | texture | 10/8 hero background `1482:2985`, 600x759 CROP |
| 17 | `packshot-sea-salt-mouthwash.png` | `02bc01e6` | 600x600 | Refreshing Mint Sea Salt Fluoride-Free Natural Mouthwash (layer name `US05684A_primary`) | packshot transparent | 10/8 hero `1482:2996` 292.5x386.5 rotated -26°; 10/8 Sea Salt `1482:3032` 534.9x534.9 rotated 27° |
| 18 | `packshot-sea-salt-mouthwash-white-bg.png` | `2b15490b` | 600x600 | same, white background | packshot white bg | hidden fill under `1482:2996`, `1482:3032` |
| 19 | `packshot-whiten-plus-coconut-oil-gentle-mint-toothpaste-box.png` | `af44e3c9` | 1800x1800 | Whiten Plus Coconut Oil Fluoride Free Gentle Mint Natural Toothpaste (box; layer name `61046035_Packshot_Front`) | packshot transparent | 10/8 hero `1482:2997` 302.4x243.4 rotated 33°; 10/8 Coconut Oil `1482:3014` 385.5x128.5 CROP |
| 20 | `packshot-whiten-plus-coconut-oil-gentle-mint-toothpaste-box-white-bg.png` | `6f941ddf` | 1800x1800 | same, white background | packshot white bg | hidden fill under `1482:2997`, `1482:3014` |
| 21 | `lifestyle-bathroom-counter-oral-care.jpg` | `53fda3f7` | 3259x4096 | bathroom counter with Tom's oral care products | scene | stacked, covered: fill 1 of 5 on category rows `1482:3044`, `1482:3060` (10/8), `1482:3459`, `1482:3476` (10/27) |
| 22 | `lifestyle-woman-brushing-teeth.jpg` | `3302f94f` | 3257x4096 | woman brushing teeth, smiling | lifestyle | stacked, covered: fill 2 of 5 on the same rows |
| 23 | `lifestyle-man-brushing-teeth-tile-wall.png` | `8cbf9588` | 2401x4074 | man brushing teeth against a white tile wall | lifestyle | stacked, covered: fill 3 of 5 on the same rows |
| 24 | `lifestyle-couple-smiling-holding-deodorant.png` | `cd3b140e` | 640x512 | couple smiling, holding Tom's deodorant | lifestyle | stacked, covered: fill 4 of 5 on the same rows |
| 25 | `lifestyle-tile-shelf-oral-care-deodorant-soap.jpg` | `60b7101c` | 4096x2732 | teal tile wall, wood shelves with mouthwash, toothpaste, deodorant, bar soap, frame | scene | **visible** top fill of the category rows (different CROP per row: Oral Care, Bath & Body, Deodorant & Antiperspirant): `1482:3044`, `1482:3060`, `1482:3062` (10/8), `1482:3459`, `1482:3476`, `1482:3479` (10/27); box 279.5x255.5 (10/8) or 279.5x200 visible (10/27) |
| 26 | `lifestyle-tile-shelf-value-bundle.png` | `cba61179` | 1201x1309 | teal tile shelf with a bundle (toothpaste box, deodorant, lemon bergamot soap) | scene | Value Bundles row: `1482:3080` (10/8) 264.5x255.6, `1482:3497` (10/27) |
| 27 | `hero-bg-heart-gel-whiten-plus-tube-blue.jpg` | `b616923f` | 1882x3344 | Whiten Plus Deep Clean tube on a heart of clear gel, light blue ground | scene | 10/13 hero `1482:9`, 600x1010 CROP (under a blue gradient) |
| 28 | `packshot-sensitive-rapid-relief-gentle-mint-toothpaste-box.png` | `1913d568` | 1800x1800 | Fluoride-Free Rapid Relief Sensitive Gentle Mint Natural Toothpaste (box, upright) | packshot transparent | 10/13 Sensitivity row `1482:2702` 212x227.5 |
| 29 | `bg-autumn-leaf-macro-orange.jpg` | `e642c9e4` | 2731x4096 | orange autumn leaf macro, veins | texture | 10/20 hero `1482:2873`, 600x891 FILL |
| 30 | `packshot-north-woods-deodorant.png` | `70a001b1` | 1800x1800 | North Woods Aluminum Free Deodorant (layer name `61028964_hero`) | packshot transparent | 10/20 hero cluster `1482:2888`/`1482:2892` 321x321; 10/20 step 4 `1482:2949` 321x321; 10/22 card `1482:3181` 169.5x167.5 |
| 31 | `packshot-north-woods-deodorant-white-bg.png` | `24d6df70` | 1800x1800 | same, white background | packshot white bg | hidden fill under `1482:2888`, `1482:2892`, `1482:2949`, `1482:3181` |
| 32 | `packshot-lemon-bergamot-bar-soap.png` | `274e54cd` | 1800x1800 | Lemon Bergamot Natural Bar Soap with aloe vera (box) | packshot transparent | 10/20 hero cluster `1482:2889`/`1482:2893` 194.5x111 |
| 33 | `packshot-whiten-plus-deep-clean-spearmint-toothpaste-box.png` | `8142ccb1` | 1800x1800 | Whiten Plus Deep Clean Whitening Spearmint Natural Toothpaste (box) | packshot transparent | 10/20 step 2 `1482:2924` 332.5x199.5 rotated 17° |
| 34 | `hero-bg-north-woods-deodorant-rock-sunset.jpg` | `fc63776b` | 1882x3344 | North Woods deodorant standing on a rock by water at sunset | scene | 10/22 hero `1482:3126`, 600x1114.5 CROP (under a top gradient) |
| 35 | `packshot-mountain-spring-deodorant.png` | `21c8909b` | 1800x1800 | Mountain Spring Aluminum Free Deodorant | packshot transparent | 10/22 card `1482:3173` 169.5x167.5 |
| 36 | `packshot-mountain-spring-deodorant-white-bg.png` | `aac161e6` | 1800x1800 | same, white background | packshot white bg | hidden fill under `1482:3173` |
| 37 | `packshot-moonlit-meadow-deodorant.png` | `6c5c6b2d` | 1800x1800 | Moonlit Meadow Aluminum Free Deodorant | packshot transparent | 10/22 card `1482:3189` 169.5x167.5 FIT |
| 38 | `packshot-twilight-breeze-deodorant.png` | `62170070` | 1800x1800 | Twilight Breeze Aluminum Free Deodorant | packshot transparent | 10/22 card `1482:3197` 169.5x169.5 |
| 39 | `packshot-tropical-island-deodorant.png` | `a2f9ee86` | 1800x1800 | Tropical Island Aluminum Free Deodorant | packshot transparent | 10/22 card `1482:3205` 169.5x167.5 |
| 40 | `packshot-unscented-deodorant.png` | `b83428d9` | 1800x1800 | Unscented Aluminum Free Deodorant | packshot transparent | 10/22 card `1482:3213` 169.5x169.5 |
| 41 | `packshot-unscented-deodorant-white-bg.png` | `18a26586` | 1800x1800 | same, white background | packshot white bg | hidden fill under `1482:3213` |
| 42 | `hero-bg-whiten-plus-tubes-forest-log.jpg` | `8609249e` | 2185x4096 | three Whiten Plus tubes (Peppermint, Spearmint, Coconut Oil) on a log, forest and ferns | scene | 10/27 hero `1482:3261`, 600x986 CROP (under a bottom gradient) |

Notes:
- The 600x600 packshots (#6, #10, #12, #17) are low resolution: at the 2x display size of the 10/20 hero (431x425.5 → 862x851) the mouthwash #12 is upscaled. Ask the client for the high-res originals before reusing them large.
- `lifestyle-man-brushing-teeth-tile-wall.png` and `lifestyle-couple-smiling-holding-deodorant.png` are PNGs with an alpha channel but read as photos.
- Product names come from the product-name text in the emails; the packaging in each image matches.
