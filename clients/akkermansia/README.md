# Akkermansia (The Akkermansia Company) — Professional (B2B) channel

Client onboarded under PowerDigital Lab. This is the **Professional (B2B)** channel of The Akkermansia Company: wholesale sales to healthcare practitioners who dispense to patients.

It is **not** the METAbiotics consumer (B2C) line, and it is **not** AKK PROBIO, which is a competing *Akkermansia muciniphila* strain (CGMCC No.20955) owned by Thankcome / Perfect Group and distributed in the US by Maypro. Do not source any brand material from those.

## Who the client is

The Akkermansia Company (formerly A-Mansia Biotech; part of Danone per public reporting). It owns the patented, pasteurized *Akkermansia muciniphila* **MucT®** strain, discovered by its founding scientists, and was the first next-generation bacterium to receive EFSA approval. The Professional channel sells finished products at wholesale to practitioners, bundled with clinical tools, samples, and protocol guidance.

Range referenced in the copy:
- **Akkermansia Essential** — foundational gut barrier integrity and immune resilience.
- **Healthy Weight with Glucose Control** — pasteurized MucT® plus green tea extract, for weight maintenance and glucose support.

## Current scope

First deliverable: the **Professional (B2B) Welcome Series**, 5 emails. Copy is final and supplied by PowerDigital (see `00-inbox/`). The work is to **build** the 5 emails, not to write copy.

- Copy source: [00-inbox/akkermansia-professional-b2b-welcome-series-copy.md](00-inbox/akkermansia-professional-b2b-welcome-series-copy.md)
- Build location (Figma): PD-DRAFT, page "Page 89" (node `2392:81`). Emails laid out left-to-right at x = 0 / 1312 / 2624 / 3936 / 5248.
- Status: **in build.** Email #1 and #2 built by the client (hand). Email #3, #4, #5 built by the agent as wireframes/mockups (real copy + layout, Poppins/Inter stand-in fonts, placeholder images) for the client to refine with imagery and the Kohinoor swap.

## Structure

```
akkermansia/
├── README.md            this file
├── brief.md             scope, decisions, open questions
├── 00-inbox/            final copy supplied by PowerDigital
├── 01-brand/
│   ├── identity/        brand-guidelines.md (digest); visual identity pending from Figma
│   ├── strategy/
│   └── references/
├── 03-work/
└── 04-deliverables/
    └── email/           the built welcome-series emails (output)
```

## Status / next steps

- [x] Visual identity ingested and recorded in `01-brand/identity/brand-guidelines.md`.
- [x] Emails #3–#5 built as wireframes in PD-DRAFT `2392:81` (agent), matching client-built #1–#2.
- [ ] Swap Poppins/Inter → Kohinoor Latin in the desktop app (or add Kohinoor as a Figma org shared font so the plugin can write it). See [brand-guidelines.md](01-brand/identity/brand-guidelines.md).
- [ ] Drop real imagery into the placeholders (#3 product tiles, #4 samples band; heros). Product box art available from the corporate site; can be uploaded via `upload_assets`.
- [ ] Resolve the open copy questions in `brief.md` (product naming, MucT® vs MucT™, footer content, confirm the disclaimer text).
