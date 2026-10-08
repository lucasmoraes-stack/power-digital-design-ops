# Image bank · Figma LAB (Jul to Sep 2026)

Source: Figma file Progressive Global LAB (`D8FpNuKI3uPGjCPqonIn3C`), page `t` (`407:656`), the 20 approved emails of July, August and September 2026. Exported 2026-10-06, read-only (nothing changed in Figma). Module inventory: `../../email-kit/inventory/figma-lab-modules.md`. Module screenshots: `../../email-kit/references/lab-*.png`.

## How to read this

- **Raw image fills** are byte-identical to the file uploaded in Figma: the SHA-1 of each file equals the Figma `imageHash` (first 8 characters in the Hash column). Deduplicated by hash: one file per image, every use listed.
- **Only fills that render are counted as used.** A fill that sits under an opaque fill on the same layer is marked *covered* (kept, never visible in the email). Image fills on hidden layers or in off-canvas frames (130 files: switched-off white-background duplicates, 300 to 512 px previews, a rainbow photo and similar) were downloaded for hashing but **not** exported.
- **Original px** is the uploaded size, not the display size. Every image is displayed at 2x of a 600px layout (Figma frames are 1200 wide).
- **Transparent**: yes = real alpha cut-out. `no (alpha channel, fully opaque)` = PNG with an alpha channel but no transparent pixel (white background baked in).
- **Also in Oct export**: the same hash already exists in `../../email-kit/assets/source/` (October inventory, VAZIO DRAFT file). Same bytes, different name.
- **Logo and social icons** are identical to the October export (same hashes `345d2351`, `671cac09`, `4955f8fe`; the X, Facebook, Instagram and TikTok vectors have the same size and position in all 26 emails), so nothing new was added to `email-kit/assets/`. Use `assets/logo-light.png`, `logo-dark.png`, `icon-*.png/.svg`, `social-row.*`. The raw logo/icon files are listed here for completeness.
- **Vector decoratives and seals** (last table) are not image fills: exported from the Figma node as SVG, the ancestor frame backgrounds that Figma adds to node exports were stripped, and each SVG was rasterized to a transparent PNG at 2x with headless Chrome. PNG px = 2x display size. Text in the seals is outlined (paths).

Counts: 108 raw image files (3 of them logo/icon duplicates of kit assets) and 19 vector decoratives (SVG + PNG each). Files in this folder: 146 + this index.

## Logo (same files as kit assets) (2)

| File | Kind | Product / subject | Original px | Transparent | Used in (email · node) | Hash | Also in Oct export | Note |
|---|---|---|---|---|---|---|---|---|
| `logo-toms-teal-header.png` | logo | Tom's of Maine 'The Original' logo, teal, transparent canvas with padding (header) | 1368x1056 | yes | all 20 emails, header 'image 1' (e.g. 7.1 408:7062) | `345d2351` | `logo-badge-teal-source.png` | shown cropped via imageTransform (visible ~732x594 px of the source) |
| `logo-toms-white-footer.png` | logo | Tom's of Maine logo, white (footer) | 780x629 | yes | all 20 emails, footer 'image 17' (e.g. 7.1 408:7227) | `671cac09` | `logo-badge-white-source.png` |  |

## Icon (same file as kit assets) (1)

| File | Kind | Product / subject | Original px | Transparent | Used in (email · node) | Hash | Also in Oct export | Note |
|---|---|---|---|---|---|---|---|---|
| `icon-pinterest-white.png` | icon | Pinterest glyph, white (footer social row; X, Facebook, Instagram, TikTok are vectors) | 389x512 | yes | all 20 emails, footer 'image 18' (e.g. 7.1 408:7247) | `4955f8fe` | `icon-pinterest-white-source.png` |  |

## Packshots, transparent cut-out (44)

| File | Kind | Product / subject | Original px | Transparent | Used in (email · node) | Hash | Also in Oct export | Note |
|---|---|---|---|---|---|---|---|---|
| `packshot-antiplaque-adult-soft-toothbrush.png` | packshot transparent | Antiplaque Adult Soft Toothbrush in package | 1800x1800 | yes | 9/11 408:4776 · 9/27 408:5251 | `e28775c8` | `packshot-antiplaque-adult-soft-toothbrush.png` |  |
| `packshot-antiplaque-spearmint-floss-a.png` | packshot transparent | Antiplaque Spearmint flat floss box | 512x512 | yes | 8/6 408:6040 | `081704ba` |  | other render: 9757ea59 |
| `packshot-antiplaque-spearmint-floss-b.png` | packshot transparent | Antiplaque Spearmint flat floss box | 512x512 | yes | 9/3 408:5136 · 9/4 408:4910 · 9/7 408:5018 · 9/11 408:4797 · 9/27 408:5259 | `9757ea59` | `packshot-antiplaque-spearmint-flat-floss.png` |  |
| `packshot-antiplaque-toothbrush-package-angled.png` | packshot transparent | Antiplaque toothbrush 2-pack, angled | 1800x1800 | yes | 7.3 408:7318 | `3f92595d` |  |  |
| `packshot-antiplaque-toothbrush-package.png` | packshot transparent | Antiplaque toothbrush 2-pack | 1800x1800 | yes | 8/15 408:6611, 408:6615, 408:6634 · 8/24 408:6382 | `e54a10e0` |  |  |
| `packshot-bar-soap-trio-cluster.png` | packshot transparent | Creamy Coconut, Orange Blossom and Fragrance Free bar soaps stacked | 1800x1800 | yes | 7.23 408:8127 | `6577139e` |  |  |
| `packshot-clean-coast-deodorant.png` | packshot transparent | Clean Coast deodorant stick | 600x600 | yes | 8/15 408:6655 | `8cdf3da4` |  |  |
| `packshot-creamy-coconut-bar-soap.png` | packshot transparent | Creamy Coconut bar soap box | 600x600 | yes | 8/6 408:6081 · 8/10 408:6178 (under lemon bergamot fill) | `36d4f943` |  |  |
| `packshot-cucumber-aloe-deodorant.png` | packshot transparent | Cucumber Aloe deodorant stick | 600x600 | yes | 7.5 408:7432 | `95e353d0` |  |  |
| `packshot-deep-forest-deodorant-a.png` | packshot transparent | Deep Forest Aluminum Free Deodorant stick | 1800x1800 | yes | 7.5 408:7730 · 7.28 408:8176 · 9/4 408:4886 · 9/7 408:4970 | `bc407300` |  | other render: 6d0674f9 |
| `packshot-deep-forest-deodorant-b.png` | packshot transparent | Deep Forest deodorant stick | 1800x1800 | yes | 8/24 408:6379, 408:6383 | `6d0674f9` |  |  |
| `packshot-deodorant-duo-creamy-coconut-cluster.png` | packshot transparent | Two deodorants + Creamy Coconut bar soap cluster | 1800x1800 | yes | 8/12 408:6274 | `8e2291a3` |  |  |
| `packshot-ff-antiplaque-whitening-peppermint-toothpaste.png` | packshot transparent | Fluoride-Free Antiplaque & Whitening Peppermint carton, flat | 1800x1800 | yes | 7.5 408:7664 | `bc4a6f3c` |  |  |
| `packshot-ff-antiplaque-whitening-spearmint-toothpaste.png` | packshot transparent | Fluoride-Free Antiplaque & Whitening Spearmint carton, upright | 1800x1800 | yes | 7.5 408:7697 | `45b8411c` |  |  |
| `packshot-fragrance-free-sensitive-bar-soap.png` | packshot transparent | Fragrance Free Sensitive bar soap box | 600x600 | yes | 8/15 408:6645 | `860191d1` |  |  |
| `packshot-fresh-mint-whole-care-mouthwash-a.png` | packshot transparent | Fresh Mint Whole Care Anticavity mouthwash bottle | 600x600 | yes | 7.3 408:7355 | `ce725e9f` |  |  |
| `packshot-fresh-mint-whole-care-mouthwash-b.png` | packshot transparent | Fresh Mint Whole Care mouthwash bottle | 600x600 | yes | 8/15 408:6609, 408:6613, 408:6632 · 9/3 408:5128 · 9/4 408:4902 · 9/7 408:4971, 408:5010 · 9/11 408:4812 · 9/22 408:5377 | `61e14b48` | `packshot-whole-care-fresh-mint-mouthwash.png` |  |
| `packshot-kids-wicked-cool-toothpaste.png` | packshot transparent | Wicked Cool! kids fluoride toothpaste tube | 600x600 | yes | 7.5 408:7435 | `ca4e1703` |  |  |
| `packshot-lavender-shea-bar-soap.png` | packshot transparent | Lavender & Shea bar soap box | 608x600 | yes | 9/22 408:5369 | `f74b3850` |  |  |
| `packshot-lemon-bergamot-bar-soap.png` | packshot transparent | Lemon Bergamot Natural Beauty Bar Soap box | 1800x1800 | yes | 7.1 408:7083, 408:7126 · 7.3 408:7319, 408:7339 · 7.5 408:7763 · 7.28 408:8168 · 8/10 408:6172, 408:6178 · 8/24 408:6380, 408:6384 · 9/3 408:5120 · 9/4 408:4894 | `274e54cd` | `packshot-lemon-bergamot-bar-soap.png` |  |
| `packshot-moonlit-meadow-deodorant-a.png` | packshot transparent | Moonlit Meadow Aluminum Free Deodorant stick | 1800x1800 | yes | 7.1 408:7085 · 7.5 408:7429 | `8b5b460a` |  | other render: 6c5c6b2d |
| `packshot-moonlit-meadow-deodorant-b.png` | packshot transparent | Moonlit Meadow deodorant stick | 1800x1800 | yes | 8/20 408:6979, 408:6983, 408:7008 · 9/27 408:5267 | `6c5c6b2d` | `packshot-moonlit-meadow-deodorant.png` |  |
| `packshot-mountain-spring-deodorant-a.png` | packshot transparent | Mountain Spring deodorant stick | 1800x1800 | yes | 7.8 408:7879 | `21c8909b` | `packshot-mountain-spring-deodorant.png` | other render: fda163e1 |
| `packshot-mountain-spring-deodorant-b.png` | packshot transparent | Mountain Spring deodorant stick | 1800x1800 | yes | 9/7 408:5002 | `fda163e1` |  |  |
| `packshot-north-woods-deodorant.png` | packshot transparent | North Woods deodorant stick | 1800x1800 | yes | 7.8 408:7871 · 7.28 408:8153 | `27ab12c5` |  |  |
| `packshot-sensitive-rapid-relief-toothpaste.png` | packshot transparent | Sensitive+ Rapid Relief toothpaste carton, upright | 1800x1800 | yes | 8/3 408:5808 | `1913d568` | `packshot-sensitive-rapid-relief-gentle-mint-toothpaste-box.png` |  |
| `packshot-sensitive-whitening-toothpaste.png` | packshot transparent | Sensitive+ Whitening toothpaste carton, upright | 1800x1800 | yes | 8/3 408:5816 | `7e87a7cd` |  |  |
| `packshot-travel-toothpaste-anticavity.png` | packshot transparent | Grab n' Go travel toothpaste, anticavity (green cap) | 600x600 | yes | 9/27 408:5235 | `5a0cd9df` |  |  |
| `packshot-travel-toothpaste-fluoride-free.png` | packshot transparent | Grab n' Go travel toothpaste, fluoride-free (blue cap) | 600x600 | yes | 9/27 408:5243 | `f97c2697` |  |  |
| `packshot-tropical-island-deodorant-a.png` | packshot transparent | Tropical Island deodorant stick | 1800x1800 | yes | 7.8 408:7863 | `a2f9ee86` | `packshot-tropical-island-deodorant.png` | other render: 9e0d0fa3 |
| `packshot-tropical-island-deodorant-b.png` | packshot transparent | Tropical Island deodorant stick | 1800x1800 | yes | 8/10 408:6152 · 8/20 408:6980, 408:6984, 408:6996 | `9e0d0fa3` |  |  |
| `packshot-twilight-breeze-deodorant-a.png` | packshot transparent | Twilight Breeze deodorant stick | 1800x1800 | yes | 7.28 408:8184 | `62170070` | `packshot-twilight-breeze-deodorant.png` | other renders: 2d352582, b3b79ec9 |
| `packshot-twilight-breeze-deodorant-b.png` | packshot transparent | Twilight Breeze deodorant stick | 1800x1800 | yes | 8/20 408:6978, 408:6982, 408:7002 · 9/3 408:5152 | `2d352582` |  |  |
| `packshot-twilight-breeze-deodorant-c.png` | packshot transparent | Twilight Breeze deodorant stick | 1356x1356 | yes | 9/7 408:5026 · 9/22 408:5354 | `b3b79ec9` |  |  |
| `packshot-unscented-deodorant-a.png` | packshot transparent | Unscented Aluminum Free Deodorant stick | 1800x1800 | yes | 7.3 408:7347 | `861a7c39` |  |  |
| `packshot-unscented-deodorant-b.png` | packshot transparent | Unscented deodorant stick (lilac label) | 1800x1800 | yes | 7.8 408:7887 | `b83428d9` | `packshot-unscented-deodorant.png` |  |
| `packshot-unscented-deodorant-c.png` | packshot transparent | Unscented deodorant stick | 1800x1800 | yes | 8/6 408:6059 · 8/10 408:6146 | `9eb0cf02` |  |  |
| `packshot-whiten-plus-deep-clean-peppermint-carton.png` | packshot transparent | Whiten+ Deep Clean Peppermint carton | 1800x1800 | yes | 9/7 408:4969, 408:4994 | `73a7cdbf` | `packshot-whiten-plus-deep-clean-peppermint-toothpaste-box.png` |  |
| `packshot-whiten-plus-deep-clean-spearmint-carton.png` | packshot transparent | Whiten+ Deep Clean Spearmint carton | 1800x1800 | yes | 8/10 408:6158 | `15b499b8` |  |  |
| `packshot-whiten-plus-deep-clean-spearmint-flat.png` | packshot transparent | Whiten+ Deep Clean Spearmint carton, flat front | 1011x300 | yes | 7.28 408:8160 · 9/3 408:5112 · 9/4 408:4918 | `00280410` |  |  |
| `packshot-whole-care-cinnamon-clove-toothpaste.png` | packshot transparent | Whole Care Cinnamon Clove toothpaste carton | 600x600 | yes | 7.3 408:7331 | `dae0b4c0` |  |  |
| `packshot-whole-care-peppermint-toothpaste.png` | packshot transparent | Whole Care Peppermint toothpaste carton | 600x600 | yes | 8/10 408:6165 · 9/4 408:4878 · 9/7 408:5034 | `cbc7dfd9` | `packshot-whole-care-peppermint-toothpaste-box.png` |  |
| `packshot-whole-care-toothpaste-carton-upright.png` | packshot transparent | Whole Care toothpaste carton upright, side view | 1000x1000 | yes | 8/15 408:6610, 408:6614, 408:6633 | `d8512d20` |  |  |
| `packshot-whole-care-wintermint-toothpaste.png` | packshot transparent | Whole Care Wintermint toothpaste carton | 600x600 | yes | 9/3 408:5144 · 9/22 408:5346 | `d4a31a30` |  |  |

## Packshots on white / in package, opaque (20)

| File | Kind | Product / subject | Original px | Transparent | Used in (email · node) | Hash | Also in Oct export | Note |
|---|---|---|---|---|---|---|---|---|
| `packshot-adult-holiday-brush-rinse-bundle.png` | packshot on white | Adult Holiday Brush & Rinse Bundle | 1800x1800 | no | 7.23 408:8052 | `02f199fc` |  | opaque white background |
| `packshot-back-to-nature-bundle-white-bg.png` | packshot on white | Back to Nature Bundle, 2 deodorants + bar soap | 1800x1800 | no | 7.23 408:8084 | `a3d939aa` |  | alt render: 12ea5973 |
| `packshot-back-to-nature-bundle.png` | packshot on white | Back to Nature Bundle | 1800x1800 | no (alpha channel, fully opaque) | 8/10 408:6198 · 8/24 408:6406 | `12ea5973` |  | alpha channel opaque |
| `packshot-best-sellers-bar-trio-white-bg.png` | packshot on white | Best Sellers Beauty Bar Trio, 3 boxes stacked | 1800x1800 | no | 7.23 408:8068 · 7.23 408:8126 (30% reflection strip) | `1016e7ef` |  | opaque white background |
| `packshot-best-sellers-bar-trio.png` | packshot on white | Best Sellers Beauty Bar Trio | 1800x1800 | no (alpha channel, fully opaque) | 8/10 408:6210 | `6c093137` |  | alpha channel opaque |
| `packshot-brush-rinse-bundle.png` | packshot on white | Brush & Rinse Bundle | 1800x1800 | no (alpha channel, fully opaque) | 8/24 408:6394 | `0f3cb3b6` |  | alpha channel opaque |
| `packshot-creamy-coconut-bar-soap-white-bg.png` | packshot on white | Creamy Coconut Natural Beauty Bar Soap box | 600x600 | no | 7.1 408:7159 | `eb90598b` |  | transparent version: 36d4f943 |
| `packshot-ff-antiplaque-whitening-fennel-toothpaste.png` | packshot on white | Fluoride-Free Antiplaque & Whitening Fennel carton, angled | 600x600 | no (alpha channel, fully opaque) | 8/6 408:6062 | `2239f306` |  | alpha channel opaque |
| `packshot-fragrance-free-sensitive-bar-soap-angled.png` | packshot on white | Fragrance Free Sensitive bar soap box, angled | 600x600 | no (alpha channel, fully opaque) | 8/12 408:6302 | `d39a088c` |  | alpha channel opaque |
| `packshot-fresh-mint-whole-care-mouthwash-white-bg.png` | packshot on white | Fresh Mint Whole Care mouthwash | 600x600 | no (alpha channel, fully opaque) | 8/12 408:6283 | `6a7f68ae` |  | alpha channel opaque |
| `packshot-kids-holiday-brush-rinse-bundle.png` | packshot on white | Kids Holiday Brush & Rinse Bundle | 1800x1800 | no | 7.23 408:8060 | `af1d21b3` |  | opaque white background |
| `packshot-kids-toothpaste-variety-pack.png` | packshot on white | Kids Natural Toothpaste Variety Pack, 3 tubes | 600x600 | no | 7.23 408:8076 | `a547ee82` |  | opaque white background |
| `packshot-most-loved-deodorant-bundle.png` | packshot on white | Most-Loved Deodorant Bundle, 3 sticks | 1800x1800 | no (alpha channel, fully opaque) | 8/10 408:6192 · 8/20 408:6990 · 8/24 408:6412 | `39e60f5b` |  | alpha channel opaque |
| `packshot-sensitive-skin-smile-bundle-white-bg.png` | packshot on white | Sensitive Skin & Smile Bundle | 1800x1800 | no | 7.23 408:8092 | `a1a3a1a4` |  | alt render: 8ad51d37 |
| `packshot-sensitive-skin-smile-bundle.png` | packshot on white | Sensitive Skin & Smile Bundle | 1800x1800 | no (alpha channel, fully opaque) | 8/10 408:6204 · 8/24 408:6400 | `8ad51d37` |  | alpha channel opaque |
| `packshot-travel-toothpaste-tube.png` | packshot on white | Grab n' Go travel toothpaste tube | 600x600 | no (alpha channel, fully opaque) | 8/12 408:6324 | `44d59b7c` |  | alpha channel opaque |
| `packshot-whiten-plus-coconut-oil-toothpaste-angled.png` | packshot on white | Whiten+ Coconut Oil carton, angled | 1800x1800 | no (alpha channel, fully opaque) | 8/12 408:6305 | `792a1290` |  | alpha channel opaque |
| `packshot-whiten-plus-deep-clean-peppermint-flat.png` | packshot on white | Whiten+ Deep Clean Peppermint carton, flat front | 1721x535 | no (alpha channel, fully opaque) | 7.28 408:8200 | `369a3750` |  | alpha channel present but fully opaque |
| `packshot-whiten-plus-deep-clean-spearmint-toothpaste-white-bg.png` | packshot on white | Whiten+ Deep Clean Spearmint toothpaste carton | 1800x1800 | no | 7.1 408:7093 | `9ed6f29a` |  | opaque white background |
| `packshot-whole-care-peppermint-toothpaste-white-bg.png` | packshot on white | Whole Care Peppermint toothpaste carton | 600x600 | no | 7.1 408:7192 · 7.28 408:8192 | `80c0b643` | `packshot-whole-care-peppermint-toothpaste-box-white-bg.png` | transparent version: cbc7dfd9 |

## Lifestyle and scene photography (28)

| File | Kind | Product / subject | Original px | Transparent | Used in (email · node) | Hash | Also in Oct export | Note |
|---|---|---|---|---|---|---|---|---|
| `lifestyle-backpack-deodorant-desk.png` | lifestyle | Backpack on desk with deodorant in side pocket | 896x1200 | no (alpha channel, fully opaque) | 8/10 408:6132 | `33f1fef4` |  |  |
| `lifestyle-bathroom-counter-products.jpg` | lifestyle | Bathroom counter with Tom's products | 3259x4096 | no | 8/15 408:6624 (covered) · 9/16 408:5443, 408:5459, 408:5461 (covered) | `53fda3f7` | `lifestyle-bathroom-counter-oral-care.jpg` | never visible in render |
| `lifestyle-bathroom-shelf-bundle.png` | lifestyle | Bathroom shelf with bundle products on tile | 1201x1309 | no | 9/16 408:5479 | `cba61179` | `lifestyle-tile-shelf-value-bundle.png` |  |
| `lifestyle-bathroom-shelves-tile.jpg` | lifestyle | Bathroom shelves on teal tile with Tom's products | 4096x2732 | no | 9/16 408:5443, 408:5459, 408:5461 (visible, cropped per row) | `60b7101c` | `lifestyle-tile-shelf-oral-care-deodorant-soap.jpg` |  |
| `lifestyle-beach-dunes-blue-sky.jpg` | lifestyle | Beach and green dunes, deep blue sky | 2731x4096 | no | 8/20 408:6966 (visible) | `2080f378` |  |  |
| `lifestyle-blue-sky-clouds.jpg` | lifestyle | Deep blue sky with clouds | 3072x4096 | no | 9/7 408:4966 | `9bf67fbc` |  |  |
| `lifestyle-deodorant-in-snow.png` | lifestyle | Deodorant stick in snow, blue sky | 1024x2220 | no | 7.15 408:7937 (covered by #00857A) | `444d5db8` |  | never visible in render |
| `lifestyle-dunes-purple-sunset.jpg` | lifestyle | Sand dunes under purple sunset sky | 3420x4096 | no | 8/15 408:6458 | `557bac04` |  |  |
| `lifestyle-field-rainbow-sky.jpg` | lifestyle | Rainbow over autumn field | 2730x4096 | no | 7.1 408:7064 (bottom fill, covered) · 7.3 408:7264 (covered by #24436F) | `5e961c38` |  | never visible in render |
| `lifestyle-fireworks-night-sky.png` | lifestyle | Fireworks in night sky | 1600x1160 | no | 7.5 408:7426 (visible) · 9/3 408:5097 (covered) | `37cfc1e9` |  |  |
| `lifestyle-forest-stream-wide.jpg` | lifestyle | Forest with stream, wide format | 4096x1754 | no | 7.23 408:8035 | `83b7ff3e` |  |  |
| `lifestyle-forest-trail-golden-light.jpg` | lifestyle | Dirt forest trail in warm light | 2731x4096 | no | 8/12 408:6263 | `2c8ddb1e` |  |  |
| `lifestyle-forest-trail-green.jpg` | lifestyle | Green forest trail | 2000x2997 | no | 7.8 408:7843, 408:7855 | `71d4a31f` |  |  |
| `lifestyle-hand-bar-soap-dish.jpg` | lifestyle | Hand placing bar soap on wooden dish | 1080x1920 | no | 8/15 408:6644 | `da223180` |  |  |
| `lifestyle-hand-bar-soap-sink.jpg` | lifestyle | Hand with bar soap at running tap | 3277x4096 | no | 9/3 408:5097 (visible) | `56c9357e` |  |  |
| `lifestyle-hands-holding-deodorant.jpg` | lifestyle | Hands holding deodorant stick | 3277x4096 | no | 8/15 408:6647 (covered) | `207b5b8d` |  | never visible in render |
| `lifestyle-hiker-backpack-products.jpg` | lifestyle | Hiker backpack seen from behind with Tom's products | 3277x4096 | no | 9/27 408:5214 | `3819e794` |  |  |
| `lifestyle-man-applying-deodorant-forest.png` | lifestyle | Shirtless man applying North Woods deodorant at a forest campsite | 2632x1800 | no | 7.15 408:7933 | `d2c1268b` |  |  |
| `lifestyle-man-smiling-toothpaste-sky.jpg` | lifestyle | Man smiling holding toothpaste tube against blue sky | 3277x4096 | no | 9/11 408:4624 | `597c86e3` |  |  |
| `lifestyle-pastel-sunset-sea.jpg` | lifestyle | Calm sea at pastel sunset | 2731x4096 | no | 8/24 408:6367 | `3164af2f` |  |  |
| `lifestyle-poppy-wildflower-field.png` | lifestyle | Red poppy and cornflower field | 2000x2203 | no | 7.1 408:7064 (hero background) | `9b600841` |  |  |
| `lifestyle-sunlit-meadow-grass.jpg` | lifestyle | Sun through tall grass and pines | 2000x1333 | no | 7.28 408:8143 | `d5e1e3b2` |  |  |
| `lifestyle-sunset-sky-gradient.jpg` | lifestyle | Sunset sky, teal to orange | 2731x4096 | no | 9/27 408:5208 | `14d60c6e` |  |  |
| `lifestyle-tropical-beach-turquoise.jpg` | lifestyle | Turquoise beach with palms | 2730x4096 | no | 8/20 408:6966 (covered) | `dd75fecb` |  | never visible in render |
| `lifestyle-woman-applying-deodorant.jpg` | lifestyle | Woman applying deodorant, arm raised | 3277x4096 | no | 8/15 408:6647 (covered) | `1d35a3da` |  | never visible in render |
| `lifestyle-woman-brushing-teeth.jpg` | lifestyle | Woman smiling while brushing teeth | 3257x4096 | no | 8/15 408:6624 (covered) · 9/16 (covered) | `3302f94f` | `lifestyle-woman-brushing-teeth.jpg` | never visible in render |
| `lifestyle-woman-holding-deodorant-smiling.jpg` | lifestyle | Woman smiling holding deodorant to her cheek | 3277x4096 | no | 8/15 408:6647 (visible top fill) | `6a953e40` |  |  |
| `lifestyle-woman-laughing-wildflowers.jpg` | lifestyle | Woman laughing among wildflowers, low angle | 2731x4096 | no | 8/6 408:5885 | `e41a6bed` |  |  |

## Lifestyle cut-outs (transparent) (2)

| File | Kind | Product / subject | Original px | Transparent | Used in (email · node) | Hash | Also in Oct export | Note |
|---|---|---|---|---|---|---|---|---|
| `lifestyle-couple-smiling-deodorant-cutout.png` | lifestyle cutout | Couple smiling holding deodorant, transparent background | 640x512 | yes | 9/16 408:5443, 408:5459, 408:5461 (covered) | `cd3b140e` | `lifestyle-couple-smiling-holding-deodorant.png` | never visible in render |
| `lifestyle-man-brushing-teeth-cutout.png` | lifestyle cutout | Man smiling brushing teeth, transparent background | 2401x4074 | yes | 8/15 408:6624 (visible top fill) · 9/16 (covered) | `8cbf9588` | `lifestyle-man-brushing-teeth-tile-wall.png` |  |

## Product still life (product styled in a set) (9)

| File | Kind | Product / subject | Original px | Transparent | Used in (email · node) | Hash | Also in Oct export | Note |
|---|---|---|---|---|---|---|---|---|
| `still-life-north-woods-deodorant-lavender-teal.png` | lifestyle product still life | North Woods deodorant with pine and lavender on teal | 1800x1800 | no | 7.15 408:7954 | `2e5990f7` |  |  |
| `still-life-three-whiten-plus-tubes-droplets.jpg` | lifestyle product still life | Three Whiten+ tubes standing with water droplets, light blue | 3277x4096 | no | 9/22 408:5314 | `afe10c3f` |  |  |
| `still-life-tropical-island-deodorant-coconut-teal.png` | lifestyle product still life | Tropical Island deodorant with coconut on teal | 1800x2153 | no | 7.15 408:7970 | `4b14fa13` |  |  |
| `still-life-whiten-plus-coconut-tube-in-water.jpg` | lifestyle product still life | Whiten+ Coconut Oil tube in water with leaves | 4096x2868 | no | 8/3 408:5536 | `8d329d2d` |  |  |
| `still-life-whiten-plus-toothpaste-leaves.png` | lifestyle product still life | Whiten+ toothpaste carton among leaves | 1264x987 | no | 7.15 408:7988 | `be419ad1` |  |  |
| `still-life-whiten-plus-tube-foam.jpg` | lifestyle product still life | Whiten+ tube squeezing foam, light grey | 3277x4096 | no | 9/3 408:5082 | `12e03f86` |  |  |
| `still-life-whiten-plus-tube-gel-sky-blue.jpg` | lifestyle product still life | Whiten+ tube with gel swoosh on sky blue | 2437x3046 | no | 8/20 408:7014 (SMS band) | `8f3d87b7` |  |  |
| `still-life-whiten-plus-tube-on-moss.jpg` | lifestyle product still life | Whiten+ tube lying on moss | 3276x4096 | no | 8/15 408:6658 (SMS band) | `c2c44c00` |  |  |
| `still-life-whole-care-toothpaste-stream-stones.png` | lifestyle product still life | Whole Care toothpaste carton on stones by a stream | 1492x1054 | no | 7.15 408:7972 | `4753eafc` |  |  |

## Textures (2)

| File | Kind | Product / subject | Original px | Transparent | Used in (email · node) | Hash | Also in Oct export | Note |
|---|---|---|---|---|---|---|---|---|
| `texture-tropical-leaves.jpg` | texture | Large green tropical leaves | 2731x4096 | no | 9/4 408:4851 | `9d582d8e` |  |  |
| `texture-white-silk.png` | texture | White silk fabric | 1200x777 | no | 7.5 408:7401 (hero fill at 40% over white) | `342be518` |  |  |

## Vector decoratives, seals and badges (19, SVG + PNG 2x)

| File | Kind | Subject | PNG px (2x) | Transparent | Used in (email · node) |
|---|---|---|---|---|---|
| `seal-national-fresh-breath-day.svg` / `seal-national-fresh-breath-day.png` | seal-badge | Starburst seal, linear gradient #05453D 24% / #0CAB97 48% / #05453D 68%, inner star stroke #3DA79D, leaf icon #55B5AC, New Kansas SemiBold white "National Fresh Breath Day" (text outlined) | 318x320 | yes | 8/6 408:5898 (rotated -11.9 deg) |
| `seal-national-relaxation-day.svg` / `seal-national-relaxation-day.png` | seal-badge | Starburst seal, gradient #171849 / #295791 / #171849, inner stroke #3DA79D, leaf icon #55B5AC, "National Relaxation Day" | 380x380 | yes | 8/15 408:6474 (rotated -18 deg) |
| `seal-national-gum-care-month.svg` / `seal-national-gum-care-month.png` | seal-badge | Starburst seal, gradient #05453D / #295791 / #171849, inner stroke #3DA79D, leaf icon #55B5AC, "National Gum Care Month" | 484x484 | yes | 9/11 408:4633 (rotated -13.7 deg) |
| `badge-15-off-cloud.svg` / `badge-15-off-cloud.png` | seal-badge | Hand-drawn oval "15% OFF" badge, radial #C2DDFF to #6EA1E0, ink #24436F, highlights #DBE5E5 | 184x82 | yes | 7.1 408:7100, 408:7133, 408:7166, 408:7199 · 7.5 408:7671, 408:7704, 408:7737, 408:7770 |
| `badge-step-number-70d8ce.svg` / `badge-step-number-70d8ce.png` | seal-badge | Scalloped number badge #70D8CE with Rubik Bold numeral #05453D (shown: "1"; steps 2 and 3 use the same shape) | 78x78 | yes | 9/11 408:4770, 408:4786, 408:4802 |
| `stars-row-5-white.svg` / `stars-row-5-white.png` | decorative | Five white 5-point stars, 44 px each at 2x, 8 px gaps | 252x44 | yes | 7.1 408:7077 · 7.3 408:7309 |
| `firework-burst-sky-navy.svg` / `firework-burst-sky-navy.png` | decorative | Firework burst #4A96D0 + #295791 (cropped at the hero edge as in Figma) | 185x372 | yes | 7.5 408:7445 |
| `firework-burst-navy-light-blue.svg` / `firework-burst-navy-light-blue.png` | decorative | Firework burst #295791 + #6EA1E0 (cropped at the hero edge) | 186x396 | yes | 7.5 408:7502 (same drawing 408:7559) |
| `firework-burst-red.svg` / `firework-burst-red.png` | decorative | Firework burst #C00000 (cropped at the hero edge) | 179x120 | yes | 7.5 408:7616 |
| `sparkle-4pt-navy.svg` / `sparkle-4pt-navy.png` | decorative | 4-point sparkle #295791 | 19x19 | yes | 7.5 408:7653 to 408:7658 |
| `leaf-line-art-3da79d.svg` / `leaf-line-art-3da79d.png` | decorative | Leaf line-art cluster #3DA79D (reads faint, used over photo) | 302x349 | yes | 8/3 408:5539, 408:5667 |
| `leaf-solid-91c9c6.svg` / `leaf-solid-91c9c6.png` | decorative | Two solid leaves with speckle texture, #91C9C6 (same drawing in #00867D on 8/15 and #008D83 on 9/3) | 226x232 | yes | 8/10 408:6184, 408:6185 · 8/15 408:6469, 408:6470, 408:6472, 408:6473 · 9/3 408:5086 |
| `leaf-sprig-05453d-lab.svg` / `leaf-sprig-05453d-lab.png` | decorative | Line-art leaf branch #05453D | 302x324 | yes | 9/27 408:5216, 408:5217 |
| `leaf-sprig-ccfffa-lab.svg` / `leaf-sprig-ccfffa-lab.png` | decorative | Line-art fern sprig #CCFFFA | 243x364 | yes | 9/4 408:4869, 408:4870 · 7.3 408:7268, 408:7281, 408:7294 (same family) |
| `divider-scallop-05453d.svg` / `divider-scallop-05453d.png` | decorative | Scalloped (cloud) edge divider #05453D, 1200 wide at 2x | 1200x404 | yes | 9/3 408:5098 · 9/22 408:5325 (same shape in #55B5AC) |
| `wave-tall-05453d.svg` / `wave-tall-05453d.png` | decorative | Tall wave divider #05453D, 1207x334 at 2x (the standard wave is 126 tall) | 1200x334 | yes | 8/20 408:6967 |
| `icon-sun-c8eeeb.svg` / `icon-sun-c8eeeb.png` | decorative | Sun-and-cloud icon in a ring, #C8EEEB | 89x89 | yes | 9/16 408:5484 · 9/22 408:5339 |
| `icon-moon-c8eeeb.svg` / `icon-moon-c8eeeb.png` | decorative | Moon icon in a ring, #C8EEEB | 89x89 | yes | 9/16 408:5489 · 9/22 408:5363 |
| `icon-phone-008d83.svg` / `icon-phone-008d83.png` | decorative | Phone icon in a #008D83 circle (SMS band) | 96x96 | yes | 8/15 408:6922 |

## Not exported, with reason

- Standard wave divider (path 1207.2x125.7 at 2x; 7.5, 8/10, 8/15, 9/4, 9/11, 9/27): same path as the October `assets/wave.svg`. LAB colors: #295791 (7.5), #05453D (8/10, 9/11, 9/27), #E9F6FD and #B9EBFF (8/15), #FFFFFF (9/4), #CCFFFA and #053832 (9/11). Recolor `wave.svg`.
- Dome and curve dividers are very large ellipses (up to 5867 px diameter) clipped by the band. They only exist inside the slice.
- 9/16 giant wave panel (`408:5435`, gradient #FFFFFF to #008D83, 1482x2994) and the blurred glow ellipses (layer blur 214 to 409): baked into the slice.
- Glass panels (Figma GLASS effect) render only composited in the slice; no standalone asset is possible.
- The 7.3 navy hero fireworks line art (`Vrstva_1`, #CCFFFA) is the same fern family as `leaf-sprig-ccfffa-lab` and the October `leaf-sprig-fern-ccfffa.png`.
