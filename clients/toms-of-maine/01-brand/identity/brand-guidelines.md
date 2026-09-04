# Tom's of Maine branding

Digest of `_NEW_Tom's of Maine - Brand Universe Guidelines - Client copy 11.11.25.pdf` (Version 4.3, dated 2025-11-11) — the source PDF is 28MB and won't open directly in most tools; this digest was extracted via `pdftotext -layout` and is the working reference. Brand Guardian reads this file in full. Tom's of Maine is a Colgate-Palmolive brand (design contact in the PDF: frank_yang@colpal.com; marketing: shilpa_nayak@tomsofmaine.com).

## Color palette — verified from the PDF text, page 49-51

- **Tom's Teal** (hero color, ~75% of any application): Pantone 3282C · CMYK 100/0/54/15 · RGB 0/133/122 · **HEX `#00857A`**
- **Tom's Tint** (Tom's Teal at 70%, ~15% of application): Pantone 3282C 70% · RGB 72/158/152 · **HEX `#489E98`**
- **White** (~10% of application): no HEX given in the PDF text; pairs with teal to "keep our identity strong."
- Target ratio: 75% Teal / 15% Tint / 10% White (the guideline's own "squint test").

**Explicitly deprecated — do not use**: "old Sky or Navy accents," anywhere (logo, typography, combined with other variants, or stacked on top of each other). The guideline calls this out four separate times on the color-palette-don'ts page (p.51). No hex is given for old Sky/Navy in the PDF text extract — if needed for legacy-asset comparison only, don't source it from the PDF.

**Navy — scoped exception, confirmed 2026-08-31 by the user (not written in the PDF).** For email specifically, dark navy is approved for the **footer background** and **occasionally CTA buttons** — nowhere else (not hero banners, section backgrounds, headlines, or general content blocks, which stay Teal/Tint/White per the PDF above). Exact hex not independently verified yet — the Figma section's `#015695` is the closest known candidate but should be spot-checked against a recently-sent real email before it's locked into a template.

**Still open**: the Figma Library's existing `Tom's of Maine Style Guide` section (node 199:1052) lists a 5-color palette including "Tom's Accent Navy" `#015695`, "Tom's Accent Sky" `#02A4EB`, and "Tom's Accent Yellow" `#FDD000` (the last two not mentioned anywhere in this PDF and not part of the scoped navy exception above), and even its "Tom's Green"/"Tom's Green Light" entries (`#04857B` / `#4EA9A2`) are slightly off from this PDF's verified `#00857A` / `#489E98`. That Figma section needs correcting to match this digest — don't treat it as authoritative until then. See `clients/toms-of-maine/README.md` status list.

## Typography — page 53-58

- **New Kansas** — primary typeface, headlines and body copy. 70s-inspired serif, "playful," carries the brand's warmth/personality. Sentence case. Weights seen: Regular, SemiBold, Bold ("Large Bold" tier).
- **Rubik** (Bold) — secondary typeface, *functional information only* (labels, legal, claims-adjacent text) — never headlines. Upper case, Bold weight.
- Don'ts: no color other than white on Tom's Teal, no stretching/distortion, no wide tracking, no rotation, no italics, never use Rubik for headlines.
- Exact point sizes aren't in the extracted text (the hierarchy page is mostly a visual chart) — pull from the PDF's page 56-57 visuals directly if a batch needs precise scale.

## Foliage texture (graphic device) — page 60-64

"Komorebi"-style (dappled light through leaves) foliage shadow texture, Tom's Teal colored, applied with Multiply blend mode at 50% opacity over a Tom's Teal background — the brand's signature background treatment. A lighter variant sits behind product packaging specifically. Don't recolor it, don't put it inside the logo, don't use any texture outside the approved set, don't use the dark variant behind packaging.

## Claims (badges) — page 66-69

Circular badges, always white text, minimum 13mm, typically bottom-right (flexible, not a strict rule). Two kinds: core-value claims (brand-wide) and product-benefit claims (per-SKU). Don't recolor, stretch/skew, over-rotate, or overcrowd a single application with claims.

## Photography — page 70-84

Stock imagery in the PDF is reference-only pending an original brand photoshoot. Three modes: **Tom's in Nature** (product placed organically among real ingredients, logo centered), **Tom's in Teal** (product + Komorebi foliage shadow over teal), **Tom's at Home** (product in a real bathroom setting + foliage shadow). Products are placed "as if naturally grown," never sterile/staged-studio.

## Tom's Split layout (design system) — page 85-91

A two-panel system: **Flexed** side (lifestyle / ingredient / nature photography, artist's choice) + **Fixed** side (product shot, must occupy ~50% of the canvas). Logo centered at the seam, message text split as Text A / Text B, optional claim in the bottom quarter. Validated at extreme ad formats: 728×90, 250×250, 120×600, 300×600, 420×280 — this is effectively Tom's of Maine's banner-ad system (relevant if this account ever takes on banner work, not needed for the current email-only scope). In owned channels (Instagram, etc.) the split device is optional — full-bleed imagery is fine since the audience already knows they're in a Tom's environment.

## Files

- `_NEW_Tom's of Maine - Brand Universe Guidelines - Client copy 11.11.25.pdf` — the source file (v4.3).
- This digest is the operation's working source given the PDF's size.

## Where Tom's of Maine's rules live in the agent team

- **Brand Guardian** reads this file in full.
- **Designer** carries the condensed palette/type/graphic-language facts in its own "## Tom's of Maine" section in [.claude/agents/designer.md](../../../../.claude/agents/designer.md) — currently flagged not-yet-onboarded pending the navy question above.
- **Copywriter** is not used for this brand (copy arrives pre-approved) — see its own "## Tom's of Maine" section.
