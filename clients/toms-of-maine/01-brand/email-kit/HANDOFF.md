# Tom's of Maine email kit · handoff (2026-10-06)

Where the work stopped, and what is left. Read this first when resuming. Treat every published artifact as possibly edited since: re-read before changing (global rule in `~/.claude/CLAUDE.md`).

## FROZEN (2026-10-06, owner's call)

The big module-library setup below is frozen: too many tokens, and the reference JPGs alone were not convincing. Current path: build real emails one at a time, directly in HTML, using the inventories as spec.

- November broadcast (copy: `00-inbox` PDF "Tom's _November Broadcast - Copy 2026", 8 emails 11/3 to 12/1): `clients/toms-of-maine/03-work/email/2026-11-november/`.
- 11/3 Rooted in Nature built as the test: `01-rooted-in-nature.html` → `python ../render_email.py 01-rooted-in-nature.html --slices` (1200px JPG + slices).
- Deliverables page: https://claude.ai/code/artifact/3c9ef9d8-e89c-4f48-a015-1554d5516a02 · rebuild with `python build_deliverables.py <out.html>` (edit EMAILS list) and republish to the same URL.
- Next: owner reviews 11/3; then 11/9 onward, one at a time.

### 2026-10-07: calibration done, 11/3 hero concepts

- **10/8 fidelity rebuild:** `03-work/email/_fidelity/10-08-ingredient-spotlight.html` (values from Figma `get_design_context`, halved from the 2x file). Same height as the Figma export (8165 at 2x), mean pixel difference 3.4/255, headings/images/buttons/rows at 0 px offset. Lessons: Figma inside strokes do not push auto-layout padding (subtract the border in CSS); the 10/8 hero background is rotated 90° in its crop (rotated copy + exact row crops in `assets/source/figma-10-08/`); the glass effect is approximated with `backdrop-filter`; nav/footer off by 1 to 2 px until Gotham arrives.
- **11/3 hero concepts** A autumn glass (T02b), B still life on top (T02c), C forest + lineup on arc (T02d): `03-work/email/2026-11-november/build_0103_concepts.py` → `01-rooted-in-nature-{a,b,c}.html`. Category rows now use the exact Figma crops (top-cropped to 200, as 10/27). Hero CTA in Rubik for all three (open question 4).
- Review page: https://claude.ai/code/artifact/20c9caff-f1c6-42a8-a096-661619457501 · rebuild `python build_0103_review.py <out.html>`.
- Next: owner picks A, B or C → finalize 11/3 (slices, deliverables page) → 11/9.

### 2026-10-07 (later): all 8 November layouts

- **Owner rule: product-card type = LAB `407:3817`** (scent grid): name New Kansas SemiBold 24/120%, -1%, `#05453D`, centred, 10.76 to the B02 button; card 253 wide, radius 20, padding 26.5/20.5, sheen `#FFFFFF` → `#C8EEEB` → `#FFFFFF` (225°). Applied to every product card and to the category-row names.
- **Owner direction:** product packshots real; every other image is a marked placeholder (striped box, "Image placeholder · …") until the owner sends options. Goal now: 8 consistent layouts with varied blocks.
- Builder: `03-work/email/2026-11-november/build_november.py` (shared CSS + blocks, one function per email; 11/3 heroes still come from `build_0103_concepts.py`). Packshots: `prep_assets.py` → `./assets/` (6 deodorants downloaded from 407:3817 into `assets/source/figma-lab-407-3817/`).
- Missing packshots: Everyday Essentials Starter Pack, Whole Care Oral Health Bundle.
- Deliverables page updated (same URL): https://claude.ai/code/artifact/3c9ef9d8-e89c-4f48-a015-1554d5516a02 · `python build_deliverables.py <out.html>`.
- **Owner rule: product names always fill a 2-line box**, one size per email, the largest of 24/22/20/18 that fits every name (script in `page()` of `build_november.py`; text column 240 in grid cards, 317 in wide cards). Result: 24 in 11/27 to 12/1, 18 in 11/9 and 11/18. 11/18 uses wide cards because its names run to 62 characters.
- Reference emails from the owner go in `clients/toms-of-maine/00-inbox/refs-html/` (gitignored). Next round: make the layouts less like the Jul to Oct emails, using those refs.
- Round 2 (refs Burt's Bees, Each & Every, Kinship in `00-inbox/refs-html/`, notes in its README): 11/9 seal + split-card checkerboard, 11/18 framed hero + editorial persona list, 11/28 photo-top hero + bundle rows. New blocks in `build_november.py`: `seal()`, `split_card()`, `lrow()`, `brow()`.
- 11/3 hero = **A** (owner, 2026-10-07); product group recomposed on the wave.
- **Gate before any delivery:** `python 03-work/email/lint_layout.py <html...>` must be clean, then an Email QA Reviewer pass on the renders (round of 2026-10-07 needed 3 passes to reach sign-off).
- Open for the owner: footer `©%%= v(@CurrentYear) =%%` will ship as literal text in a sliced-JPG footer unless the footer goes out as live HTML in SFMC.
- Not done yet: slicing (the renderer cuts only horizontally; side-by-side cards need half-width slices), QA pass.

## Decisions from the owner (Lucas), 2026-10-06

- **Operational-only kit:** copy arrives pre-approved; no Diagnostic/Strategy Report, no strategy section, never write copy.
- **Delivery format:** every email is a 1200px design (2x of 600) exported as JPG and sliced. No HTML to the ESP, no live text, no link URLs, no webfont licensing, no dark mode or mobile type.
- **Production happens here, not in Figma:** modules in HTML/CSS, rendered at 2x in headless Chrome, exported to JPG, sliced. Figma only for small one-off tweaks, by importing our HTML (Figma MCP `generate_figma_design`). Email-client constraints don't apply (modern CSS is fine).
- **Docs in English** (chat with Lucas in PT-BR).
- **Image bank** as its own page (done).
- Patterns from a sample are findings, not rules: check all approved emails before writing "always".

## Sources

- Figma **Progressive Global LAB** `D8FpNuKI3uPGjCPqonIn3C`, page `407:656`: 26 approved emails, July to October 2026 (main source).
- Figma **VAZIO DRAFT** `8oGyJxpeGLPWNiH54vePwS`, page `1482:2`: copy of the 6 October emails.
- 20 sent PNGs: `clients/toms-of-maine/00-inbox/emails-enviados/`.
- Guideline v4.3 digest: `../identity/brand-guidelines.md`. New Kansas .otf: `../identity/fonts/` (gitignored).

## Done

| Item | Where |
|---|---|
| Kit created, tokens extracted and consolidated | `tokens.json`, `README.md` (token tables with sources) |
| Token review page (v2, English; predates the module work) | https://claude.ai/code/artifact/ea41f86e-fbc5-48a6-b979-712207817de0 · source `tokens-review.src.html` |
| Module inventory, October (T01..T18, B01, B02) | `inventory/figma-modules.md`, screenshots `references/figma-*.png` |
| Module inventory, July to September (L01..L25, B01..B03) | `inventory/figma-lab-modules.md`, screenshots `references/lab-*.png` |
| Module catalogue page (screenshots + specs from both inventories) | https://claude.ai/code/artifact/8d5dfa0e-25cd-4164-bc82-579de63a381f · built by `tools/build_module_catalog.py` |
| Assets: logos, social icons, waves, sprigs, value icons, textures | `assets/`, log in `assets/figma-export.md` |
| Image bank: 172 assets from the 26 emails | `assets/source/` (Oct) + `../photos/figma-lab/` (Jul to Sep, `index.md`) · page https://claude.ai/code/artifact/a617c37a-312f-4225-a9d3-38d39502c2c1 · built by `tools/build_image_bank.py` |
| `.gitignore`: `assets/source/` excluded (95 MB) | repo `.gitignore` |

## In progress when the session stopped

An Email Designer agent was building the HTML production system. Files it had written: `render/tokens.css`, `render/fonts.css`, `render/kit.css`, `tools/build_css.py`, `tools/kitlib.py`, `03-work/email/_fidelity/` (empty or partial). Check what exists before continuing; nothing was reviewed yet.

A second Email Designer agent was cataloguing the 20 sent PNGs into `inventory/sent-emails.md` (cross-check only; the LAB Figma has exact values for the same emails). Use it if it exists.

## Left to do, in order

1. **Finish the module system** (brief below), in `email-kit/`:
   - consolidate tokens from both inventories into `tokens.json` (most recent emails win: Oct > Sep > Aug > Jul; conflicts go to open questions), `tools/build_css.py` → `render/tokens.css`;
   - one consolidated module set M01.. with a mapping table to T../L.. ids: header; every hero family as variants (scene/photo with text, circle portrait, glass card, product cluster on arc, price-led incl. navy and sky, left-aligned, split gradient, text at bottom); section intro; product card (6 skins); grids 2-up, 2x2, 2x3, odd-item wide card, alternating rows; category rows; ingredient spotlight; routine steps; need rows with pill; values grid 2x2; claims grid with footnotes; comparison panel; product highlight / offer intro; review rows; SMS band; closing CTA; fine print; seals/badges; wave, scallop, leaves; announcement bar; full footer (logo, social row, nav, legal bar, optional disclaimer);
   - `components.html` review page (every module and variant at 600px, sample copy from the approved emails, spec panel) + `components.publish.html` with inlined, compressed assets;
   - `tools/compose.py` (JSON spec → 600px email HTML in `03-work/email/<campaign>/`);
   - `tools/export_jpg.py` (render at 2x → JPG → slices at `data-slice` marks → `04-deliverables/email/<campaign>/<email>/`);
   - fidelity proof: rebuild 10/8 Ingredient Spotlight (VAZIO DRAFT `1482:2979`) and 9/3 Labor Day Early Access (LAB `408:5076`), compare with Figma renders side by side + diff in `03-work/email/_fidelity/`;
   - README module table, compose/export/Figma-import docs, `tools/README.md`.
2. **Audit:** Email QA Reviewer (fidelity, slicing, image weight) + Brand Guardian (kit vs guideline v4.3 and the approved emails).
3. **Publish** the module library page for module-by-module review; owner marks ok / adjust.
4. **Status → approved** in the README after review; then first real campaign.

## Published pages

| Page | URL | Rebuild |
|---|---|---|
| Module catalogue (reference, not the library) | %s | `python tools/build_module_catalog.py <out.html>` |
| Image bank | https://claude.ai/code/artifact/a617c37a-312f-4225-a9d3-38d39502c2c1 | `tools/build_image_bank.py` (edit paths at top) + `tools/image-bank.tpl.html` |
| Token review (v2, superseded by the catalogue for modules) | https://claude.ai/code/artifact/ea41f86e-fbc5-48a6-b979-712207817de0 | `tokens-review.src.html` + New Kansas subset embed |

Republish rule: same URL (pass `url`), re-read the live version first.

## Waiting on the owner

- **Gotham Bold and Medium .otf** → `../identity/fonts/gotham/`. Used in header nav, footer and most hero CTAs; until then renders fall back to Montserrat (not production-accurate).
- Answers to the open questions below.

## Open questions (consolidated from both inventories)

1. Navy outside the footer in the July 4th emails (panels, cards, headings, buttons) and in two seals: seasonal exception?
2. Product-name style: Rubik Bold uppercase (July) vs New Kansas Medium/SemiBold sentence case (August on). Which is current? Also two 2-up name styles in October (10/2 Medium 18 vs 10/22 SemiBold 24).
3. Product-name colors `#29776F`, `#295791`, `#05453D`, `#044D44`: normalise to one?
4. Hero CTA font: Gotham (most heroes) vs Rubik (10/8 hero, 8/3, 8/10, all band CTAs). Rule?
5. Small buttons are 42.8 and 39.2 tall: keep as approved or raise to 44?
6. Blue backgrounds (Relaxation Day, Labor Day Ends Tonight, Stay Fresh): allowed when? Guideline v4.3 deprecates the old Sky.
7. Header and footer are not inside export slices in most emails: how are they delivered (separate slices)?
8. Frames that cut off the footer legal bar (10/20, 9/3) and other slice errors (7.3, 7.5, 8/15, 7.28 names): approved as is or mistakes?
9. Low-res 600x600 packshots: can the client send high-res originals?
10. Heading case: several headings typed in Title Case display as sentence case. Which is the approved copy?
11. 8 covered photos in the LAB file: approved for the bank?
12. Navy footer block starts at x 0.5 (0.5px line): fix in new emails?
