# Banner layout reference and production spec — Katapult

Authoritative spec for Katapult ad banners. The **Figma file is the primary source of truth**, above the PDF guidelines. Source: Figma `HgYaoi2oKw63WR0eeGwYhT`, `design-components` (the V1 1:1 and 9:16 templates) and the KAT26014 briefing.

Reference images in this folder: `template-meta1-1x1.png`, `template-meta1-9x16.png`, `template-meta2-1x1.png`, `template-meta2-9x16.png`, `test-imagery.png`, `figma-styleguide-overview.png`.

## Templates (two in the design system)

The `design-components` in Figma now hold two templates, each as a 1x1 and a 9x16 variant.

**meta 1 — phone mockup.** Headline (Aktiv Grotesk SemiBold, black) plus the hand-holding-phone mockup that bleeds off an edge. This is the template the KAT26014 banner set was built from. See the composition rules below.

**meta 2 — photo + benefits.** Photo-led, no phone mockup. Structure: a real product or lifestyle **photo filling one edge** (top on 1x1, bottom on 9x16, bleeding off that edge), a centered headline (Semi Bold, black, scaled so it matches the pill width), **three benefit pills** (rounded outline in `#ec5370`, each with a check icon and short copy in **Bold**), the Katapult logo, and a **Bounce arc** graphic in the corner. Background `#eaeae8`. Disclaimer sits over the photo, white text with a thin black outline. Color variations recolor the whole system across the palette (Dark Blue, Pink, Cream): background, headline, pill stroke and copy, check, and logo swap together, with the logo color following the brand's logo-on-background rules.

**Test imagery** (`test-imagery.png`): the phone mockup plus four lifestyle photos added for testing meta 2, spanning the categories Katapult finances (furniture/sofa, laptop/workspace, auto/tires, outdoor patio). Drop these into the meta 2 photo slot.

## Source-of-truth values (from Figma, override the PDF)

- Background: `#eaeae8` (warm light gray). Not the PDF's `#f4f4f4`.
- Headline: black `#000000`, font **Aktiv Grotesk SemiBold**. Not Dark Blue, not Oakes Grotesk.
- Accent / logo: Katapult Pink `#ec5370`. (PDF said `#ed5370`; use the Figma value.)
- Disclaimer: Aktiv Grotesk Medium, black.
- Logo: the pink wordmark vector, supplied artwork, never on top of the photo.
- Hero: the hand-holding-phone mockup, a transparent PNG.

Font note: Aktiv Grotesk is licensed and may not load in headless or MCP tooling. When building via tooling, use **Inter** as a stand-in and swap to Aktiv Grotesk in Figma desktop (where it is embedded). Select all text and change the family in one pass.

## Layout zones

Logo, headline (the message), hero mockup, optional disclaimer. The pink uppercase tagline from the template is dropped when a brief tests headline messaging (see KAT26014).

## Composition rules (learned from production)

1. The hero is a transparent PNG, so it must **bleed off a frame edge**, never float with margin all around. Vertical and square formats bleed off the bottom; landscape and short formats bleed off the right (and bottom).
2. Position the hero **high**, right under the headline, so it fills the whitespace. Bigger is better: let the phone dominate the lower two-thirds. In verticals, anchor it to the left (x near 0 or slightly negative).
3. Headline is **as large as the text zone allows, and vertically centered** on short and wide formats. Never timid. Reference sizes (shorter copy goes larger): 970x250 about 58 to 70px; 728x90 about 40px; 160x600 about 42px; 320x50 about 17px. On short and wide units (728x90, 970x250, 320x50) center the headline vertically in the available band.
4. Hero is pushed **aggressively up and left and made large**. In verticals it rises almost to the headline and anchors left (x near 0 or negative); on wide formats it grows and bleeds off the top and right (970x250 hero about 247x545). Fill the space.
5. Disclaimer is **white text with a thin black outline** (white fill, ~0.5px black stroke, OUTSIDE), at a **small size (5 to 7px)**. It must **fit within the bottom margin** (compute its height and anchor it above the bottom edge: y = frameHeight - margin - textHeight) so it never overflows or clips, and its **width is constrained to stay clear of the hero** (do not let it run under the phone; on 970x250 the disclaimer is about 385px wide, left of the hero). Black-only text loses legibility over the hand. It appears on medium and large formats and is **removed on the smallest leaderboards (320x50 and 728x90)**, where the legal terms live on the landing page.

## Disclaimer copy (verbatim where used)

> This is an advertisement for a lease-purchase or lease-to-own service. The path to ownership will cost more than the merchant's cash price. Certain items available at participating locations. Not available in MN, NJ, WI, WY.

## IAB sizes (KAT26014 set)

300x250, 300x600, 160x600, 320x480, 480x320, 320x50, 728x90, 970x250. Two messaging iterations per size (V1, V2) = 16 deliverables.

- Vertical (300x600, 160x600, 320x480): logo top-left, headline below, hero high and left-anchored bleeding off the bottom, disclaimer bottom.
- Square / medium rectangle (300x250): logo and headline left, hero bleeding in from the right, disclaimer bottom-left.
- Landscape (480x320, 970x250): text left, hero filling the right and bleeding off right and bottom, disclaimer bottom-left.
- Short leaderboards (728x90, 320x50): logo left, headline beside it, a slice of the phone bleeding from the right, no disclaimer.

## For the agents

- Image Prompt Engineer: reproduce the bleed-and-fill treatment, exact hex values, no filters; the logo is placed artwork, never AI-rendered, never on the photo.
- Ad Creative Strategist: headline carries the tested message; default CTA "Leap Forward" unless a brief says otherwise; carry the disclaimer except on the smallest units.
- Instagram Curator: the 1:1 and 9:16 frames double as Meta creatives.
