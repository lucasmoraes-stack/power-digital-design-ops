# PowerDigital Lab — agent team

A small, fixed team of 4 agents, auto-loaded by Claude Code from this folder. Every agent is brand-agnostic in *structure* but brand-aware in *content*: Copywriter and Designer each carry a section per onboarded client brand right inside their own file. Adding a brand means teaching these agents its rules — never spinning up a new set of per-brand files.

## The team

- **Briefing Analyst** (`briefing-analyst.md`) — receives the creative demand, identifies the brand and the ask, and hands off to Copywriter and/or Designer.
- **Brand Guardian** (`design-brand-guardian.md`) — holds the full brand (from `clients/<brand>/01-brand/identity/`) and checks everything against it before it ships.
- **Copywriter** (`copywriter.md`) — copy for Meta creatives and programmatic banner ads, plus creative-testing angles. Carries every onboarded brand's voice.
- **Designer** (`designer.md`) — visual direction for Meta creatives and AI image-prompt generation for banners. Carries every onboarded brand's palette, photography rules, and graphic language.

## Why this shape

This used to be split into per-role, per-brand files (a generic agent plus a separate brand "brief" for each client) — it worked for one brand, but every new brand meant a new file per role, and updating how the team handles a discipline meant touching several files at once. Fusing related disciplines into fewer agents, and baking each onboarded brand's rules directly into that agent's own file, keeps the team size fixed regardless of how many brands join.

## Onboarding a new brand

1. Capture the brand in `clients/<brand>/01-brand/` (the standard structure — see the root README).
2. Add a section for it inside `copywriter.md` and `designer.md`, following the pattern of the existing brand sections.
3. Brand Guardian and Briefing Analyst need no changes — they already read whichever brand is active from `clients/<brand>/`.

## Source of truth for tokens

For color, type, and other basic brand elements, the shared [Figma Library](https://www.figma.com/design/pcf9QNPjvBBzqDPnBLefVS/Claude-Design-Ops---Lab?node-id=74-7766) file — one style-guide section per brand — outranks the PDF/brand-notes digest wherever they disagree. Designer's brand sections cite the exact node checked and the date.

## Scope note

This team makes the creative asset. It does not buy media or build conversion tracking — that's out of scope for this design-ops repo by design; it's a different team's job once a brand is live.
