# Akkermansia Professional (B2B) — Brand digest

Source so far: the welcome-series copy supplied by PowerDigital, plus public company background. This is the working brand reference for the operation. It covers positioning, audience, voice, and claims discipline.

> **The Figma file is the primary source of truth for the visual identity, above this digest.** Palette, typography, logo lockups, email width, section layout, and button styles are to be pulled from PD-DRAFT node `2373-92` when the build is unlocked. The "Visual identity" section below is a placeholder until then. Do not invent colors or fonts.

---

## What this is

The **Professional (B2B) channel** of The Akkermansia Company: a wholesale program that sells the company's finished postbiotic products to healthcare practitioners, who then dispense them to patients. The channel bundles wholesale pricing, technical assets, practice samples, and clinical protocol guidance.

Distinct from two look-alikes, which must never be used as a source:
- **METAbiotics** (theakkermansiacompany.com) is the same company's B2C consumer line.
- **AKK PROBIO** (akkprobio.com) is a competing strain (CGMCC No.20955) from Thankcome / Perfect Group, distributed by Maypro.

## The product

Patented, pasteurized *Akkermansia muciniphila* **MucT®** strain, discovered by the company's founding scientists. Positioned as a postbiotic, not a live probiotic. Range in the copy:

- **Akkermansia Essential** (also written "Akkermansia Metabolic Essential" in the copy): foundational gut barrier integrity and immune resilience. 30-day supply cases.
- **Healthy Weight with Glucose Control:** pasteurized MucT® plus green tea extract, for the weight-maintenance phase, insulin resistance, and post-GLP-1 weight maintenance.

## Positioning

The only patented, pasteurized *Akkermansia muciniphila* MucT® strain. First next-generation bacterium to receive EFSA approval. The pasteurization angle is the core differentiator: the patented process keeps the functional Amuc_1100 surface protein accessible and stable, versus live probiotics that degrade in gastric acid or oxygen.

## Audience

Healthcare practitioners buying at wholesale for their practice. They care about clinical evidence, regulatory status, patient selection, dosing protocols, ease of integration (no refrigeration, once-daily), and margin / wholesale value. The end beneficiary is the patient, but the reader is the clinician.

## Voice and tone

Clinical, credentials-forward, and practitioner-to-practitioner. Authority without retail hype. Recurring vocabulary from the copy: *metabolic resilience, root-cause, gut barrier / gut permeability, patient outcomes, protocols, dispensing, deploy, clinically shown*. Sentences are declarative and confident. It sells evidence and ease of adoption, not lifestyle.

## Proof points (as stated in the supplied copy)

- Only patented, pasteurized *Akkermansia muciniphila* MucT® strain.
- First next-generation bacterium with EFSA approval.
- Backed by 20 years of research.
- Validated by 5 published clinical studies.
- Functional Amuc_1100 surface protein kept accessible by patented pasteurization.
- Practical: no refrigeration, once-daily dosing, 30-day supply cases.

Use these only as the copy states them. Do not upgrade numbers or invent new claims.

## Claims and compliance (important)

This is a regulated supplement category. Health claims in the copy carry a "*" tied to a disclaimer (structure-function / FDA style). Rules for anything we build or touch:

- Keep every claim exactly as supplied. Do not add, strengthen, or reword health claims.
- Preserve the "*" on every claim that carries one, and render the disclaimer text with it (exact wording pending from client).
- "Clinically shown" and outcome language (healthy weight, blood sugar, blood pressure) stay verbatim.

## Visual identity (ingested from PD-DRAFT + the corporate site)

Source of truth for the welcome-series look is the client's hand-built Email #1 and #2 in Figma (PD-DRAFT, page "Page 89", node `2392:81`). Tokens below were read directly from those nodes. Product/logo imagery comes from theakkermansiacompany.com (the same company; the two products have "‑Professional" variants for this channel).

**Color**
- Navy (primary text / dark-theme background): `#081933`
- Magenta (accent, CTAs, links, dividers): `#d01482`
- Cream (light-theme background): `#f9f6f5`
- Greige (light-theme secondary section / decorative ellipse): `#c6b7b2` (used as a soft `#efe9e6` section fill in the wireframes)
- Subject-strip background: `#ebebeb`; subject text `#282828`
- Product accents on packaging: Essential = light blue band; Healthy Weight = magenta band

**Typography** (brand fonts)
- Headlines: **Kohinoor** Bold, ~77.5px, center, 120% line-height
- Subheadline: **Kohinoor** Medium, ~48px
- Body: **Kohinoor** Regular, ~40px, 120%
- CTA label: **Kohinoor** Semibold, ~35px
- Subject strip / footer copyright: **Helvetica Neue LT Pro**
- Installed family on disk: `Kohinoor Latin` (styles Black/Bold/Book/Demi/Light/Medium + italics) in `kohinoor-font-family/`. Note the style mapping: Regular↔Book, Semibold↔Demi.
- **Figma-MCP limitation:** neither Kohinoor nor Helvetica Neue LT Pro can be loaded by the `use_figma` plugin (it runs in Figma's cloud font environment, which only exposes Google/shared fonts — a local OS install does NOT reach it). See [[figma-mcp-locked-font-reframe]]. Agent-built emails use **Poppins** (headlines/body) + **Inter** (subject/copyright) as stand-ins at the same sizes; swap to Kohinoor Latin in the desktop app, or add Kohinoor as a Figma org shared font.

**Layout system** (email = 1200px wide)
- Stack: subject strip (`#ebebeb`) → Hero → body → Footer.
- Themes alternate: #1 light, #2 dark, #3 light, #4 dark, #5 light.
- Hero (light): cream bg + navy circular logo + big taupe decorative ellipse. Hero (dark): navy bg + reversed white logo.
- CTA = fully-rounded magenta pill (cornerRadius ~119, padding 30×60), white label.
- Comparison cards (#2): rounded 20, 4px border (magenta = highlighted, white = neutral).
- Product tiles (#3): rounded card, border, product image + name + magenta "Shop Now" link.
- Footer: navy, Instagram + Facebook icons + "Copyright © 2026".

**Logo assets** (image fills already in PD-DRAFT, reusable by `imageHash`)
- Navy on light: `792ebdc46b7105b692cb557b06cbb1087417b5af`
- Reversed white (for navy): `67afd1d2a9069637bd558db989f8c39a9b6289b8`

**Product images** (from theakkermansiacompany.com)
- Akkermansia Essential: `Akkermansia_Horizontal-Box_RGB.png`
- Healthy Weight with Glucose Control: `Akkermansia_Vertical-Box_RGB.png`

**Disclaimer** (proposed, from the product packaging — confirm with client)
- "* These statements have not been evaluated by the Food and Drug Administration. This product is not intended to diagnose, treat, cure, or prevent any disease."
- Attach to every claim carrying a `*` (Email #1 block 2, #2 block 1, #3 product tiles).
