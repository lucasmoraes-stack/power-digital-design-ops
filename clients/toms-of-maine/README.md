# Tom's of Maine — client of Power Digital

Client onboarded under PowerDigital Lab. Health/personal-care brand. Recurring **monthly email marketing cycles**, run in batches.

## Current scope

- **Format: email creative only.** No Meta/Instagram or programmatic banner work identified for this brand yet — if that changes, onboard it the same way (a `## Tom's of Maine` section in the relevant agent).
- **Cadence**: monthly, split into multiple batches.
- **Copy and offers arrive pre-approved.** The team's job here is the art only — Copywriter is not in the loop for this brand's email work. If a batch ever needs original copy (a new angle, a missing line, a testing variant), that's a scope change, not a default — flag it to a human rather than drafting it.

## Status / next steps

- [x] **Brand guidelines captured** — `_NEW_Tom's of Maine - Brand Universe Guidelines - Client copy 11.11.25.pdf` (v4.3, 2025-11-11) dropped in `01-brand/identity/`, digested into `01-brand/identity/brand-guidelines.md`, and summarized in Designer's `## Tom's of Maine` section.
- [x] **Palette question resolved (2026-08-31).** Navy is a confirmed, scoped exception for email only — footer background, and occasionally CTA buttons. Everything else (hero banners, section backgrounds, headlines, general content) stays Teal `#00857A` / Tint `#489E98` / White per the v4.3 guideline. Exact navy hex still needs spot-checking against a real recent send before it's locked into a template (see Designer's Tom's of Maine section).
- [ ] **Figma Library section needs correction, not just addition.** Node 199:1052's Color Palette has slightly-off Teal/Tint hex values and its Typography frame still shows unrelated leftover placeholder content ("Gotham," "More ways to drink easy" — not this brand). Also hit a Figma MCP tool-call rate limit on this file mid-session ("View seat on the Professional plan") — the owning plan/org for that seat isn't actually known, don't guess which one. This same file has hit this quota before in past sessions; it was only unblocked by the user sorting real access on their end, not by retrying.
- [ ] **No email layout system yet.** The guideline's own design system ("Tom's Split") is a banner-ad spec (728×90, 250×250, etc.), not an email one — needs a purpose-built modular email block library. Nothing built yet, pending the palette-conflict decision above.

## Structure

```
toms-of-maine/
├── README.md                this file
├── 00-inbox/                 incoming monthly batch demands (approved copy, offers, briefs)
├── 01-brand/
│   ├── identity/             brand guidelines (captured — see Status)
│   └── references/           templates, past approved email creative
├── 03-work/                  in-progress batch work
└── 04-deliverables/
    └── email/                finished email creative, by batch
```
