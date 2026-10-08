# Tom's of Maine · Email kit

> Operational-only kit: copy arrives pre-approved by the client, so there is no Diagnostic Report, Strategy Report or strategy section (owner's decision, Lucas, 2026-10-06). Source of truth: the approved emails.
>
> **Production format (confirmed by the owner, 2026-10-06):** every Tom's email is designed at 1200px in Figma, exported as JPG and sliced. No HTML, no live text, no link URLs in our scope. Webfont licensing, Outlook fallbacks, dark mode and mobile type sizes do not apply.
>
> Flow: `email-ops/playbook.md` · Rules: `email-ops/rules.md` · Checklist: `email-ops/CHECKLIST.md`, part C.

## Status

| | |
|---|---|
| Status | **draft** · tokens extracted 2026-10-06, awaiting approval |
| Project owner | Lucas |
| Official visual source | **Main:** Figma "Progressive Global LAB", fileKey `D8FpNuKI3uPGjCPqonIn3C`, page `407:656`: 26 approved emails, July to October 2026 (inventory in progress). **Copy of October:** file VAZIO DRAFT, fileKey `8oGyJxpeGLPWNiH54vePwS`, page node `1482:2` (frames `1482:2752` 10/2, `1482:2979` 10/8, `1482:3` 10/13, `1482:2867` 10/20, `1482:3120` 10/22, `1482:3255` 10/27). Complement: guideline v4.3 (`../identity/brand-guidelines.md`) |
| Official or extracted | extracted from client-approved emails (Figma frames are 1200px = 2x; every value halved) |
| ESP | Salesforce Marketing Cloud (AMPscript `%%= v(@CurrentYear) =%%` appears in the footer text). We deliver sliced JPGs; no merge fields |
| Content language | English, US market |
| Module catalogue page | https://claude.ai/code/artifact/8d5dfa0e-25cd-4164-bc82-579de63a381f (built by `tools/build_module_catalog.py`) |
| Handoff / resume notes | `HANDOFF.md` |
| Token review page | https://claude.ai/code/artifact/ea41f86e-fbc5-48a6-b979-712207817de0 (source: `tokens-review.src.html`; the published page carries an embedded New Kansas subset) |

## Brand map

**Agents read this table first.** Real path of each item in this project (relative to the project root).

| Item | Path | Status |
|---|---|---|
| Diagnostic Report | n/a | waived, owner's decision (2026-10-06) |
| Strategy Report | n/a | waived, owner's decision (2026-10-06) |
| Style guide / toolbox | Figma `8oGyJxpeGLPWNiH54vePwS` node `1482:2` (approved emails) + `clients/toms-of-maine/01-brand/identity/brand-guidelines.md` | extracted / official v4.3 |
| Voice and compliance | n/a | copy pre-approved by the client |
| General brand context | `clients/toms-of-maine/README.md` | |
| Sent emails (structure and modules) | `clients/toms-of-maine/00-inbox/emails-enviados/` | 20 PNGs, heroes reviewed 2026-10-06, full inventory pending |
| Approved photo bank | `clients/toms-of-maine/01-brand/photos/figma-lab/` (Jul to Sep, `index.md`) + `email-kit/assets/source/` (Oct, `assets/figma-export.md`) · page: https://claude.ai/code/artifact/a617c37a-312f-4225-a9d3-38d39502c2c1 (built by `tools/build_image_bank.py`) | 172 assets from the 26 approved emails, 2026-10-06 |
| Product packshots | same as photo bank (kind "packshot") | 600x600 packshots flagged low-res |
| New Kansas fonts (.otf, 15 weights) | `clients/toms-of-maine/01-brand/identity/fonts/` | received 2026-10-06, kept out of git (licensed) |
| Logo | `email-kit/assets/logo-light.png`, `logo-dark.png` (raster from Figma; no vector in the files) | ask client for vector if needed |
| Email work folder | `clients/toms-of-maine/03-work/email/` | |
| Deliverables folder (final) | `clients/toms-of-maine/04-deliverables/email/` | |

## How to feed this kit

Each section has one right source. Never fill a section from the wrong source, never invent a value, never bring a value over from another brand.

| Kit section | Source | Rule |
|---|---|---|
| `tokens.json` → color, type, radius, spacing | **Approved emails** (Figma `1482:2`) | Exact value read from the layers. Guideline v4.3 is a complement only. Record the source of each value in the token tables below |
| `tokens.json` → mobile sizes and dark mode | Derived from the approved values | Marked "proposal" until approved. Check contrast |
| `assets/` | Vector logo + approved photo bank | Logo always rasterized from the vector, light and dark versions. Sizes in `assets/README.md` |
| Case, italics, button shape | Approved emails | What the brand actually ships wins over general rule defaults |
| Module sample text | Approved emails | Copied from sent emails; we never write copy for this brand |
| References | Project owner | Files in `references/`, one line each on what to reuse |

When a source changes (new approved emails, updated guideline): update the matching section, rerun `build_kit.py` if a token changed, log it in the changelog and set the status back to "draft" until re-approved.

## Tokens

Values in `tokens.json`, in px for a 600px email. Source of every value: the 6 approved emails in Figma (node `1482:2`), read through the Figma plugin API on 2026-10-06. "Proposal" = not in the Figma, needs approval.

### How the emails are built (what the Figma shows, not a rule)

The 6 Figma emails have export slices. In those 6, the hero (New Kansas SemiBold 64 headline, Rubik SemiBold 25 subtitle, intro, CTA in Gotham Bold) and the photo product cards sit inside image slices, while the nav bar, band heading, band intro, product name, card body, Rubik labels, buttons and footer are live text.

Since every email ships as a sliced JPG, "live text" here only means the element was outside an export slice in Figma; in production it is still an image. **This is not a rule for every email.** The 20 sent emails in `00-inbox/emails-enviados/` show other hero types: text over a flat or gradient teal band with a photo beside it (Back to College), text over a gradient with products below (Relaxation Day, Product Spotlight), price-led heroes ("20% OFF", Labor Day), full photo with text on top (Behind the Brand, Nature Never Takes a Vacation). Some of these may use live text in the hero. Which situations call for a live-text hero is an open item for the owner; the kit needs both a sliced-image hero and a live-text hero.

Seen in the sent emails but not in the 6 Figma emails: blue backgrounds (Relaxation Day, Labor Day Savings End Tonight, Stay Fresh Naturally Confident) and left-aligned heroes. Their hex values still need to be read from a source file.

### Color

| Token | Hex | Use | Source | Contrast |
|---|---|---|---|---|
| `color.primary` / `text` | `#05453D` | headings, body, dark button | emails (~90% of text). `#044D44` shows up on a few headings and is treated as the same color | on white 10.9:1 · on `#E8E8E8` 8.9:1 |
| `color.heading_accent` / `accent_1` | `#008D83` | highlighted word in a heading ("routine", "Coconut Oil"), upright | emails | on white 4.1:1: **headings ≥24px bold only** |
| `color.nav` / `card_line_values` | `#00867D` | header nav, values card outline | emails (≈ guideline Tom's Teal `#00857A`) | on white 4.46:1, borderline for 14px bold nav |
| `color.line` | `#55B5AC` | 2px outline on ingredient / routine cards | emails | decorative |
| `color.surface` / `surface_alt` | `#FFFFFF` / `#E8E8E8` | light bands (white → `#E8E8E8` gradient) | emails | |
| `color.accent_2` | `#0CAB97` | end of the white → teal gradient | emails | white on it 2.88:1: **fails**, white text must never sit at the end of this gradient |
| `color.dark` / `footer_bar` | `#295791` / `#24436F` | footer (block + legal bar). Navy only here | emails; exception confirmed 2026-08-31. Replaces the `#015695` candidate | white 7.3:1 / 10.0:1 |
| `color.accent_on_dark` | `#CCFFFA` | light detail on deep teal | emails | on `#05453D` 10.0:1 |
| `color.photo_fallback` | `#06554B` | foliage / background behind photos | emails (leaf texture color) | |
| Gradients | see `color.gradient_*` | `#008D83→#55B5AC`, `#05453D→#38A698→#05453D`, white→`#E8E8E8`, white→`#0CAB97` | emails | solid fallback required (Outlook) |

Dark mode: proposal, derived from `#05453D` (page `#021F1B`, surface `#032B26`, band `#05453D`, text white / `#E6F5F3`).

No navy buttons in any of the 6 emails; buttons are `#05453D` or white.

### Typography

| Role | Size desktop / mobile | Weight | Note |
|---|---|---|---|
| Hero (in image in the Figma 6) | 64/58 (variant 76/69) / n/a | New Kansas SemiBold | tracking -2% (-7% on the variant). Accent in `#008D83` |
| Hero subtitle (in image in the Figma 6) | 25/25 | Rubik SemiBold | uppercase |
| Band heading | 42/44 · mobile 32/34 (proposal) | New Kansas Bold | `#05453D` or white |
| Band subtitle | 22/29 | Rubik Bold | uppercase |
| Band intro | 20/24 | New Kansas Medium | tracking -1% |
| Card title / product name | 24/29 (variants 16, 18) | New Kansas SemiBold | tracking -1% |
| Card body | 18/22 | New Kansas Medium | tracking -3% |
| Card label | 24/24 (or 18) | Rubik Bold | uppercase. The guideline says "never Rubik for headlines"; the approved emails use it this way on cards, and the approved emails win |
| Header nav | 14/20 | Gotham Bold | uppercase, `#00867D` |
| Footer | 14/20 and 14/28 · legal 10/14 | Gotham Bold | white |

Families: New Kansas (.otf in `identity/fonts/`), Rubik, Gotham (nav and footer). Everything is rendered into the JPG, so no web fallbacks are needed. **Case rule:** sentence case for New Kansas; Rubik always uppercase.

### Button and spacing

Button: rounded rectangle, 12px radius, Rubik Bold 20 uppercase, line 30, ~50px tall. `#05453D` with white text on light bands; white with `#05453D` text on dark or photo bands. Small product button: Rubik Bold 18, 10px radius, 139x43 in Figma, raised to 44px in the kit. **One button color per email.**

Spacing (measured): band 60px top and bottom; heading → intro 24px; intro → button 24px; card title → body 15px; body / product name → button 24px; side gutter ~65px for centered blocks, ~40px for cards. Cards: 20px radius + 2px `#55B5AC` outline (32px padding), or 22px radius + 2px `#00867D` outline (values). White header, 110px tall.

## Assets

| File | Use | Origin |
|---|---|---|
| `assets/logo-light.png` · `logo-dark.png` | light header / dark background and dark mode | pending: vector logo |

Every other file in `assets/` is still a template placeholder.

## Modules → the 7 bands

| Band (rules §3) | Modules |
|---|---|
| 2 · Logo | E01 Header |
| 3 · Hero | E02 Hero Photo · E03 Hero Statement · E04 Hero Product · E15 Hero Photo Card · E16 Hero Photo Block |
| 4 · Proof or structure (only one) | E06 Steps · E07 Photo Rows · E08 Proof · E09 Detail Lines |
| 5 · Change of angle | E12 Letter · E10 Feature Photo · E05 Text Block |
| 6 · Last call | E11 CTA |
| 7 · Footer | E13 Closing Band + E14 Legal Footer (always together) |

Template module list, not yet adapted to Tom's. It gets replaced by the brand's own modules after the inventory of sent emails; a new module enters this table only after approval.

## Brand-only rules

Complement `email-ops/rules.md`.

- **Navy:** footer only (`#295791` / `#24436F`). Never in hero, band backgrounds or headings.
- **Copy:** always arrives pre-approved; never edit or write it.
- **Photo / price / sign-off / social / legal review:** to be filled from the sent-email inventory.

## Open items

- [[CONFIRMAR]] Blue backgrounds seen in the sent emails: when they are allowed (guideline v4.3 deprecates the old Sky). Exact hex comes from the LAB Figma inventory
- [[CONFIRMAR]] Gotham in nav and footer (as in every approved email) vs the guideline's Rubik: keep as approved?
- Module inventory in progress: `inventory/figma-modules.md` (October, VAZIO DRAFT), `inventory/figma-lab-modules.md` (July to September, LAB), `inventory/sent-emails.md` (20 sent PNGs)

## Changelog

- 2026-10-06: kit created; tokens extracted from the 6 approved Oct 2026 emails (Figma `1482:2`); New Kansas .otf received; token review page published; docs switched to English
