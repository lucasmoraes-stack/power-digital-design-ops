# Katapult branding

Brand source of truth, fed from the Katapult Brand Guidelines (v1.3, June 2022) and, for tokens and basic elements, the [Figma Library style guide](https://www.figma.com/design/pcf9QNPjvBBzqDPnBLefVS/Claude-Design-Ops---Lab?node-id=74-7772) — which wins where the two disagree.

The same Figma Library also holds ready-made design templates for Katapult, under [node 178:1377](https://www.figma.com/design/pcf9QNPjvBBzqDPnBLefVS/Claude-Design-Ops---Lab?node-id=178-1377) — layout families (Full-image BG, Solid BG, Before & After, Products) each in four aspect ratios, on-brand with placeholder copy standing in for real headline/body/CTA text. Designer's brand section links to this.

## Files

- `identity/brand-guidelines.md` — master digest of the full guidelines. Brand Guardian reads this directly.
- `references/` — layout references. Holds the ad banner templates (1:1 and 9:16) and `banner-layout.md`, the spec for the banner sequence. (Separate from the Figma Library templates above — these are the original IAB-banner-specific spec, from a different Figma file.)

## Where Katapult's rules live in the agent team

Katapult isn't cut into separate per-agent brief files — its rules are baked directly into the "## Katapult" section of each relevant agent, in [.claude/agents/](../../../.claude/agents/):

- **Brand Guardian** reads this folder's `identity/brand-guidelines.md` in full.
- **Copywriter** carries Katapult's voice, message, proof points, and testing angles in its own "## Katapult" section.
- **Designer** carries Katapult's palette, photography rules, graphic language, and banner production spec in its own "## Katapult" section.

The `brand-guidelines.md` digest is the operation's working source. To keep the original on hand, drop the source PDF (Katapult Brand Guidelines v1.3, June 2022) into a `source/` folder here when available.
