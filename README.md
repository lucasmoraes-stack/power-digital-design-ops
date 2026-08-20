# PowerDigital Lab

PowerDigital Lab is a small team of AI agents that produces on-brand ad creatives for Power Digital's client brands — Meta/Instagram posts and Google Ads programmatic banners.

It exists to take the repetitive, manual side of design production off the team's plate: resizing the same creative across a dozen ad sizes, adapting copy across message variants, recoloring templates across a brand's palette. None of that needs creative judgment, it just takes time. Automating it frees up time for the work that actually needs a person — strategy, art direction, reviewing the output — while a dedicated brand agent and a human review step keep everything on-brand before it ships.

---

## Technical reference

The rest of this document is for whoever maintains the setup.

### The agent team

Defined in [.claude/agents/](.claude/agents/) — reusable and brand-agnostic, so the same 8 agents serve every client. Brand knowledge lives separately, under `clients/`, and never inside these definitions.

**Front**
- **Brand Guardian** (`design-brand-guardian.md`) — brand custody; enforces consistency across everything produced.
- **Studio Producer** (`project-management-studio-producer.md`) — receives the demand and distributes briefs to the execution agents.

**Meta creatives**
- **Content Creator** (`marketing-content-creator.md`) — copy and editorial calendar.
- **Instagram Curator** (`marketing-instagram-curator.md`) — aesthetic, grid, and formats.

**Banners (Google Ads programmatic)**
- **Ad Creative Strategist** (`paid-media-creative-strategist.md`) — creative copy, variations, testing.
- **Image Prompt Engineer** (`design-image-prompt-engineer.md`) — banner visuals.
- **Programmatic & Display Buyer** (`paid-media-programmatic-buyer.md`) — delivery on Google Display Network / DV360.
- **Tracking & Measurement Specialist** (`paid-media-tracking-specialist.md`) — conversion tracking.

### How branding flows into the agents

The brand is never pasted into every agent directly. It flows through a pipeline, so each agent only carries the slice it needs:

1. **One custodian owns the brand.** The brand guidelines (for Katapult, the official PDF brand book) are given to the Brand Guardian alone — the single source of truth.
2. **Distilled into one digest** — `clients/<brand>/01-brand/identity/brand-guidelines.md`: idea, positioning, voice, palette, typography, photography rules, disclaimer.
3. **Cut into per-agent briefs** under `clients/<brand>/02-agents/`, each containing only the slice that agent uses (copy agents get voice and approved phrasing; visual agents get palette, type, and photography; media/tracking agents get audience and brand-safety notes).
4. **Figma outranks the PDF** where the two disagree, since the live design system changes faster than the printed guidelines.
5. **References live next to the briefs** — layout examples, templates, production specs — under `clients/<brand>/01-brand/references/`.
6. **Every human correction becomes a standing rule**, written back into the briefs and references.

Katapult is currently the only brand with step 3 fully cut for all 8 agents; Akkermansia and Roku have step 2 done and are next in line.

### Repository structure

```
.claude/agents/               the reusable, brand-agnostic agent team (auto-loaded by Claude Code)
clients/
  <brand>/
    01-brand/
      identity/
        brand-guidelines.md  master digest (Brand Guardian's source of truth)
      references/            templates, layout specs, test imagery
    02-agents/               one focused brief per agent (once cut)
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
