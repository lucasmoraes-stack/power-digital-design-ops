# Email kit assets

The files in this folder are still the template's **neutral samples**: grey bands with a monospace label (`HERO 600x380`, `PORTRAIT 1`...) and a `BRAND` text logo. They exist only so the template renders. Every one of them gets replaced with a real Tom's of Maine file before the kit goes to approval.

To swap an asset: save the real file under the same name **or** save it under a new name and update the path in the `assets` group of `tokens.json`. Then rerun `build_kit.py`.

## Required list

File size is always **2x** the display size.

| Token (`assets.`) | Sample file | Display | File (2x) | Format | Max weight | Used in |
|---|---|---|---|---|---|---|
| `logo_light` | `logo-light.png` | 120x50 | 240x100 or larger, same ratio | transparent PNG | 30 KB | E01 (light background) |
| `logo_dark` | `logo-dark.png` | 120x50 and 200x84 | 400x167 | transparent PNG | 30 KB | E01 in dark mode, E13 |
| `hero_photo` | `sample-hero.jpg` | 600x380 | 1200x760 | JPG 70-80 | 150 KB | E02 |
| `hero_photo_card` | `sample-card.jpg` | 560x600 | 1120x1200 | JPG 70-80 | 150 KB | E15 |
| `feature_photo` | `sample-feature.jpg` | 600x350 | 1200x700 | JPG 70-80 | 150 KB | E10 |
| `texture_light` | `texture-light.jpg` | 600x440 | 1200x880 | JPG 70-80 | 60 KB | E03 |
| `texture_dark` | `texture-dark.jpg` | 600x400 | 1200x800 | JPG 70-80 | 60 KB | E13 |
| `portrait_1..3` | `portrait-1.jpg` ... `portrait-3.jpg` | 112x112 and 44x44 | 240x240, square | JPG 70-80 | 20 KB | E07, E12 |
| `product_1` | `product-1.png` | 180x180 and 104x104 | 400x400, square | transparent PNG | 80 KB | E04, E07 |

Ceiling for a whole email: about **800 KB** across all images. If an email goes over, recompress before cutting a module.

Tom's of Maine note: the approved emails ship the hero and photo cards as full-width image slices (1200px wide files, shown at 600px), so the sizes above will be revised once the module list is adapted to the brand.

## Light and dark logo

- Always both versions, rasterized from the **official vector** (never from a screenshot or JPG).
- `logo_light`: the logo color for light backgrounds. `logo_dark`: the version for dark backgrounds (usually white or the official light color).
- Same width, height and clear space on both, so the dark-mode swap doesn't shift the layout.
- Transparent background, no shadow, no border. Gmail inverts colors on its own: a dark transparent logo with no light version disappears in dark mode.
- Ratio other than 120x50: adjust `logo_width`, `logo_height`, `logo_large_width` and `logo_large_height` in `tokens.json`.

## Photography

- Only photos from the brand's approved bank, following the photography rule in the kit README (source: guideline v4.3 and the approved emails).
- No generic AI-looking stock, no decorative illustration, no clip art.
- Crop to the module's exact size.
- Every `alt` describes the real photo (`*_alt` token in `tokens.json`); decorative images use `alt=""`.
- No approved photo yet: keep the striped labeled placeholder, never a "sample" photo that could go live.

## Textures and gradients

- A brand gradient behind live text needs a solid fallback color in `tokens.json` (`color.texture_fallback`, `color.texture_dark_fallback`) that keeps the text readable on its own, because Outlook ignores CSS gradients.

## Names

- kebab-case, English, no spaces or accents: `logo-light.png`, `hero-fall-reset.jpg`, `product-whole-care-peppermint.png`.
- Delete the `sample-*` files once the real ones are in, so no placeholder gets exported by mistake.
- On export to the ESP, the relative `assets/...` paths become absolute ESP CDN URLs.
