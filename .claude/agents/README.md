# PowerDigital Lab — agent team

The reusable, brand-agnostic team behind this operation. Auto-loaded by Claude Code from this folder. Brand-specific knowledge for each client lives under `clients/{client}/01-brand/` and `clients/{client}/02-agents/` (per-agent briefs), never inside these definitions.

## Front

- **Brand Guardian** (`design-brand-guardian.md`) — holds the active client's brand and enforces consistency across everything the other agents produce. Reactivate with the relevant `clients/{client}/02-agents/brand-guardian.md` brief at the start of a project.
- **Studio Producer** (`project-management-studio-producer.md`) — receives the creative demand and distributes focused briefs to the execution agents below.

## Meta creatives

- **Content Creator** (`marketing-content-creator.md`) — copy and editorial calendar.
- **Instagram Curator** (`marketing-instagram-curator.md`) — aesthetic, grid, and formats.

## Banners (Google Ads programmatic)

- **Ad Creative Strategist** (`paid-media-creative-strategist.md`) — creative copy, variations, testing.
- **Image Prompt Engineer** (`design-image-prompt-engineer.md`) — banner visuals.
- **Programmatic & Display Buyer** (`paid-media-programmatic-buyer.md`) — delivery on Google Display Network / DV360.
- **Tracking & Measurement Specialist** (`paid-media-tracking-specialist.md`) — conversion tracking.

## How branding flows into these agents

See the root [README.md](../../README.md#how-branding-is-set-up-inside-the-agents) for the full pipeline: one client brand goes into the Brand Guardian, gets distilled into `clients/{client}/01-brand/identity/brand-guidelines.md`, then cut into a focused per-agent brief under `clients/{client}/02-agents/`. These 8 agent definitions stay generic on purpose — never paste one client's brand into them directly.
