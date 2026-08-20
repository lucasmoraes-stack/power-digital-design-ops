# PowerDigital Lab

PowerDigital Lab is a small team of AI agents that produces on-brand ad creatives for Power Digital's client brands — Meta/Instagram posts and Google Ads programmatic banners.

It exists to take the repetitive, manual side of design production off the team's plate: resizing the same creative across a dozen ad sizes, adapting copy across message variants, recoloring templates across a brand's palette. None of that needs creative judgment, it just takes time. Automating it frees up time for the work that actually needs a person — strategy, art direction, reviewing the output — while a dedicated brand agent and a human review step keep everything on-brand before it ships.

---

## Technical reference

The rest of this document is for whoever maintains the setup.

### The agent team

Defined in [.claude/agents/](.claude/agents/) — a small, fixed team of 4, scoped to *making the creative*. Media buying and conversion tracking are out of scope on purpose — a different team's job once a brand is live.

- **Briefing Analyst** (`briefing-analyst.md`) — receives the demand, identifies the brand and the ask, hands off to the right specialist.
- **Brand Guardian** (`design-brand-guardian.md`) — holds the full brand, checks everything before it ships.
- **Copywriter** (`copywriter.md`) — copy for Meta creatives and banner ads, plus testing angles.
- **Designer** (`designer.md`) — visual direction for Meta creatives and AI image-prompt generation for banners.

Copywriter and Designer are brand-agnostic in structure but brand-aware in content: each carries a `## <Brand>` section, right inside its own file, for every onboarded client. Briefing Analyst hands off by naming the brand — it doesn't re-explain it.

### How branding flows into the agents

- **Brand Guardian owns the full guidelines** — distilled into one digest at `clients/<brand>/01-brand/identity/brand-guidelines.md`. Figma outranks the PDF where they disagree.
- **Copywriter and Designer get only their slice**, written directly into their own `## <Brand>` section — voice and approved phrasing for Copywriter, palette and photography rules for Designer.
- **References** (templates, layout specs) live alongside the digest, under `01-brand/references/`.
- **Every human correction becomes a standing rule**, written back into the relevant brand section.

Katapult's sections are fully written from its brand guidelines. Roku's are partial — visual facts observed while reframing existing creative, with voice and audience flagged as not yet captured rather than guessed at.

### Repository structure

```
.claude/agents/               the fixed 4-agent team (auto-loaded by Claude Code)
clients/
  <brand>/
    01-brand/
      identity/
        brand-guidelines.md  master digest (Brand Guardian's source of truth)
      references/            templates, layout specs, test imagery
    00-inbox/                incoming demands
    04-deliverables/
      social/                Meta creatives produced
      banners/               banner creatives produced
```

### Learning loop — examples already captured for Katapult

- The product mockup bleeds off a frame edge and sits high to fill the space, never floating.
- Headlines run large and are scaled to the format, never timid.
- The legal disclaimer is white with a thin black outline so it stays legible over a photo, and is dropped on the smallest units.
- Color variations are produced by recoloring a single template across the brand palette.
