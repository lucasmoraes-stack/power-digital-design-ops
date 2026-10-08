# Tom's of Maine — client of Power Digital

Client onboarded under PowerDigital Lab. Health/personal-care brand. Recurring **monthly email marketing cycles**, run in batches.

## Current scope

- **Format: email creative only.** No Meta/Instagram or programmatic banner work identified for this brand yet — if that changes, onboard it the same way (a `## Tom's of Maine` section in the relevant agent).
- **Cadence**: monthly, split into multiple batches.
- **Copy and offers arrive pre-approved.** The team's job here is the art only — Copywriter is not in the loop for this brand's email work. If a batch ever needs original copy (a new angle, a missing line, a testing variant), that's a scope change, not a default — flag it to a human rather than drafting it.

## Status / next steps

- [x] **Brand guidelines captured** — `_NEW_Tom's of Maine - Brand Universe Guidelines - Client copy 11.11.25.pdf` (v4.3, 2025-11-11) dropped in `01-brand/identity/`, digested into `01-brand/identity/brand-guidelines.md`, and summarized in Designer's `## Tom's of Maine` section.
- [x] **Palette question resolved (2026-08-31), navy hex locked (2026-10-06).** Navy is a confirmed, scoped exception for email only. The approved Oct 2026 emails use it on the footer only: `#295791` block + `#24436F` legal bar (the `#015695` candidate is not used). No navy buttons in those emails.
- [ ] **Figma Library section needs correction, not just addition.** Node 199:1052's Color Palette has slightly-off Teal/Tint hex values and its Typography frame still shows unrelated leftover placeholder content ("Gotham," "More ways to drink easy" — not this brand). Also hit a Figma MCP tool-call rate limit on this file mid-session ("View seat on the Professional plan") — the owning plan/org for that seat isn't actually known, don't guess which one. This same file has hit this quota before in past sessions; it was only unblocked by the user sorting real access on their end, not by retrying.
- [ ] **Email kit in progress** (`01-brand/email-kit/`). Operational-only kit (copy arrives pre-approved, no strategy reports). Tokens extracted 2026-10-06 from the 6 approved Oct 2026 emails in Figma (file `8oGyJxpeGLPWNiH54vePwS`, page `1482:2`); review page: https://claude.ai/code/artifact/ea41f86e-fbc5-48a6-b979-712207817de0 . Next: owner review of tokens and open items, sent-email inventory, logo and assets, modules.
- [x] **New Kansas .otf received** (2026-10-06), in `01-brand/identity/fonts/`, kept out of git (licensed).

## Structure

```
toms-of-maine/
├── README.md                this file
├── 00-inbox/                 incoming monthly batch demands (approved copy, offers, briefs)
├── 01-brand/
│   ├── identity/             brand guidelines (captured, see Status) + fonts/ (licensed, not in git)
│   ├── email-kit/            email kit: tokens.json, README, assets, components.html
│   └── references/           templates, past approved email creative
├── 03-work/                  in-progress batch work
└── 04-deliverables/
    └── email/                finished email creative, by batch
```
