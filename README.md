# PowerDigital Lab

A lean, agent-run operation for producing Meta creatives and programmatic ad banners, one brand at a time.

The first brand is **Katapult**, the pilot. Once the model is proven, the same structure is replicated for other brands, each in its own folder under `clients/`.

## What this operation is

A small team of specialist AI agents that takes a creative demand and a brand, and turns them into on-brand, production-ready ad creatives. Instead of one generalist doing everything, the work is split: one agent guards the brand, one translates the demand into briefs, and the rest execute (copy, visuals, media delivery, measurement). The agents were selected from a public agent library and configured for this specific operation.

## Pilot scope

- **Meta creatives** (Instagram / Facebook)
- **Google Ads programmatic** banners (Display / DV360)

## How the operation works

Work enters through a front that receives the demand and the brand, then distributes briefs to the execution agents.

```
Demand + Branding
        │
        ▼
  Brand Guardian   holds the brand, enforces consistency ──┐
        │                                                   │
        ▼                                                   │
  Studio Producer  translates the demand into briefs ───────┤
        │                                                   │
        ├──► Content Creator ───────► Meta creatives (copy)  │
        ├──► Instagram Curator ─────► Meta creatives (visual)│
        ├──► Ad Creative Strategist ► banners (copy)         │ brand
        ├──► Image Prompt Engineer ─► banners (visual)       │ consistency
        ├──► Programmatic Buyer ────► GDN delivery           │
        └──► Tracking Specialist ───► measurement            │
                                                             │
        all consume the brand defined by ◄───────────────────┘
```

## How branding is set up inside the agents

This is the heart of the operation. The brand is not pasted into every agent. It flows in through a clear pipeline, so each agent only carries the slice it needs and everything stays consistent.

**Step 1. Feed the brand to one custodian.** The brand guidelines (for Katapult, the official PDF brand book) are given to a single agent, the **Brand Guardian**. It owns the brand and is the only source of truth for it.

**Step 2. Distill into a master digest.** The guidelines are condensed into one working file, `clients/katapult/01-brand/identity/brand-guidelines.md`: what the brand is, its idea, positioning, voice, color palette (with hex values), typography, photography rules, and the disclaimer. This digest is what the Brand Guardian enforces.

**Step 3. Cut per-agent briefs.** Each execution agent gets a focused brief in `clients/katapult/02-agents/`, containing only the part of the brand it actually uses:
- the copy agents get voice, tone, and approved phrases;
- the visual agents get palette, type, photography, and the graphic language;
- the media and tracking agents get audience, positioning, and brand-safety notes.

This keeps each agent lean and prevents one agent from drifting into another's job.

**Step 4. Figma is the source of truth, above the PDF.** Brands change in the design file faster than in the PDF. So where they disagree, the live Figma design system wins. The digest records the corrections pulled from Figma (for Katapult: background `#eaeae8`, black Aktiv Grotesk headlines, pink `#ec5370`).

**Step 5. Keep references next to the briefs.** Layout references, template screenshots, and the production spec live in `clients/katapult/01-brand/references/`, so agents build against real examples, not guesses.

**Step 6. Every correction becomes a rule.** When a human adjusts a creative, the change is written back into the briefs and references as a standing rule. The agents get better with each test instead of repeating mistakes (see "The learning loop" below).

## The agents

In [.claude/agents/](.claude/agents/). The agent definitions stay brand-agnostic so they can be reused for future brands; the brand knowledge lives under `clients/`.

### Front
- **Brand Guardian** (`design-brand-guardian.md`): brand custody. Holds the branding and enforces consistency across everything produced.
- **Studio Producer** (`project-management-studio-producer.md`): receives the demand and distributes briefs to the execution agents.

### Meta creatives
- **Content Creator** (`marketing-content-creator.md`): copy and editorial calendar.
- **Instagram Curator** (`marketing-instagram-curator.md`): aesthetic, grid, and formats.

### Banners (Google Ads programmatic)
- **Ad Creative Strategist** (`paid-media-creative-strategist.md`): creative copy and variations, testing.
- **Image Prompt Engineer** (`design-image-prompt-engineer.md`): banner visuals.
- **Programmatic & Display Buyer** (`paid-media-programmatic-buyer.md`): delivery on Google Display Network / DV360.
- **Tracking & Measurement Specialist** (`paid-media-tracking-specialist.md`): conversion tracking.

## Repository structure

```
.claude/agents/               the reusable, brand-agnostic agent team (auto-loaded by Claude Code)
clients/
  katapult/
    01-brand/
      identity/
        brand-guidelines.md  master digest (Brand Guardian's source of truth)
      references/            templates, layout spec, test imagery
    02-agents/               one focused brief per agent
    00-inbox/                demands translated by the Studio Producer
    04-deliverables/
      social/                Meta creatives produced
      banners/               banner creatives produced
```

## The learning loop

The pilot ran in tight cycles: the agents produce a set, a human reviews and adjusts in Figma, and each adjustment is captured as a rule for the next round. Examples already captured for Katapult:
- the product mockup bleeds off a frame edge and sits high to fill the space, never floating;
- headlines run large and are scaled to the format, never timid;
- the legal disclaimer is white with a thin black outline so it stays legible over a photo, and is dropped on the smallest units;
- color variations are produced by recoloring a single template across the brand palette.

## Status

Two test batches were produced for Katapult in Figma:
- **Test 1 (KAT26014):** the phone-mockup template (meta 1) reframed into 8 IAB sizes by 2 messages, 16 programmatic banners.
- **Test 2 (KAT25008):** the photo-led template (meta 2) with 4 messaging versions in 1x1 and 9x16, plus three brand-palette color variations of each.

## Next steps

Wire outputs back into `clients/katapult/04-deliverables/`, and when a new brand joins, copy the `clients/<brand>/` structure and repeat the branding setup above.
