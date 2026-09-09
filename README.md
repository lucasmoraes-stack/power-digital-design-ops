# PowerDigital Lab

PowerDigital Lab is a small team of AI agents that produces on-brand creative for Power Digital's client brands — Meta/Instagram posts, Google Ads programmatic banners, and email marketing creative.

It exists to take the repetitive, manual side of design production off the team's plate: resizing the same creative across a dozen ad sizes, adapting copy across message variants, recoloring templates across a brand's palette. None of that needs creative judgment, it just takes time. Automating it frees up time for the work that actually needs a person — strategy, art direction, reviewing the output — while a dedicated brand agent and a human review step keep everything on-brand before it ships.

---

## Technical reference

The rest of this document is for whoever maintains the setup.

### The agent team

Defined in [.claude/agents/](.claude/agents/) — a small, fixed team of 4, scoped to *making the creative*. Media buying and conversion tracking are out of scope on purpose — a different team's job once a brand is live.

- **Briefing Analyst** (`briefing-analyst.md`) — receives the demand, identifies the brand and the ask, hands off to the right specialist.
- **Brand Guardian** (`design-brand-guardian.md`) — holds the full brand, checks everything before it ships.
- **Copywriter** (`copywriter.md`) — copy for Meta creatives and banner ads, plus testing angles. Sits out brands whose copy arrives pre-approved (e.g. Tom's of Maine).
- **Designer** (`designer.md`) — visual direction for Meta creatives, AI image-prompt generation for banners, and email creative layout.

Copywriter and Designer are brand-agnostic in structure but brand-aware in content: each carries a `## <Brand>` section, right inside its own file, for every onboarded client. Briefing Analyst hands off by naming the brand, it doesn't re-explain it.

### Anatomy of an agent file

Each agent under `.claude/agents/` is a markdown file: YAML frontmatter followed by a system prompt in plain text. There is no code behind it. `name` and `description` are used for routing (deciding which agent handles an incoming ask), `tools` restricts what the agent can touch (least privilege; if omitted, it inherits full access), and the body is the actual instructions.

`design-brand-guardian.md` is close to a raw copy of the "Brand Guardian" agent from [agency-agents](https://github.com/msitarzewski/agency-agents), a large external multi-division agent library; only the first few lines were adapted to this repo. Its structure shows the classic pattern for this kind of prompt: a persona ("you are an expert brand strategist"), critical rules stated as short imperatives, explicit output templates with placeholders, a step by step workflow, and a few example phrasings for tone. This works because it compresses domain discipline into something the model can follow consistently across runs, not because the words themselves carry expertise.

Brand Guardian stays generic on purpose. It does not need a brand section baked into its own file because it reads `clients/<brand>/01-brand/identity/` in full, live, every time it runs. Its brand awareness comes from that external source of truth, not from content frozen in the agent file.

Briefing Analyst, Copywriter, and Designer went the other way: most of the generic scaffolding was stripped out and replaced with real, verified facts (exact hex codes, approved lines, do and don't lists) written directly into a `## <Brand>` section inside each file. Once real facts exist, generic scaffolding stops adding value. A model does not need to be told to "write engaging copy," it needs the actual approved phrasing and the actual rule about what not to say.

The four agents form a router, specialists, reviewer pattern common to effective multi-agent setups: Briefing Analyst reads the ask and routes it, Copywriter and Designer produce (each fusing two disciplines so the same brand does not drift across formats), Brand Guardian checks the result against the real source of truth before anything ships. This keeps the team fixed at four regardless of how many brands or formats get added; growth happens by teaching the existing agents new facts, not by creating new agents.

### Building a new agent from scratch

Technically simple: an agent is a text file, there is no build step. The real cost is not writing the prompt, it is verifying the domain facts that go inside it against a real source (a brand guideline, a Figma file, an approved phrase list).

Minimum ingredients:

- `name` and `description` in the frontmatter. `description` should say when to use the agent, not just what it is; a vague description breaks routing.
- `tools`, restricted to what the agent actually needs. Omit only if it genuinely needs full access.
- A role stated in one sentence.
- An explicit scope: what it does, and just as important, what it does not do (and who handles that instead).
- Concrete, verified facts, not general principles. This is where most of the value is.
- Do and don't rules, short and imperative.
- A rule for missing information: stop and flag a human, never guess (see how Roku's copy section is handled in `copywriter.md`).
- A handoff: who receives its output next.

Template:

```markdown
---
name: AgentName
description: One sentence describing WHEN to call this agent
tools: Read, Write, Edit
---

# AgentName

[Role, one sentence.]

## Scope
Does: ...
Does not: ... (point to who does)

## What it knows (verified facts, not principles)
- Fact 1 (with source and date if it comes from an external doc)
- Rule: never do X

## When information is missing
Do not guess. Flag it to [a human or another agent] and say what is missing.

## Handoff
Passes to [next agent] before [final step].
```

Common mistakes:

- A generic description that breaks routing.
- Copying a template agent (like an agency-agents persona) without replacing the placeholders with real facts; this produces something that sounds like an expert without acting like one.
- Leaving `tools` unset when the agent only needs to read and write text, granting more access than the job requires.
- No "do not guess" rule, the most common cause of a brand voice or fact being invented instead of flagged.
- Creating a new agent when an existing one just needed a new brand section (the reason this team stayed at four agents instead of growing one file per brand).

### How branding flows into the agents

- **Brand Guardian owns the full guidelines** — distilled into one digest at `clients/<brand>/01-brand/identity/brand-guidelines.md`. For tokens and basic elements (color, type, logo), the shared [Figma Library](https://www.figma.com/design/pcf9QNPjvBBzqDPnBLefVS/Claude-Design-Ops---Lab?node-id=74-7766) — one style-guide section per brand — outranks the PDF and this digest wherever they disagree.
- **The same Figma Library also holds reusable design templates per brand**, not just tokens — Katapult's live under [node 178:1377](https://www.figma.com/design/pcf9QNPjvBBzqDPnBLefVS/Claude-Design-Ops---Lab?node-id=178-1377), as layout families (Full-image BG, Solid BG, Before & After, Products) × aspect ratios (1x1, 4x5, 9x16, 16x9), on-brand with placeholder copy. Designer starts here before building a new layout from scratch.
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
      email/                 email creatives produced (batch-based brands, e.g. Tom's of Maine)
```

### Learning loop — examples already captured for Katapult

- The product mockup bleeds off a frame edge and sits high to fill the space, never floating.
- Headlines run large and are scaled to the format, never timid.
- The legal disclaimer is white with a thin black outline so it stays legible over a photo, and is dropped on the smallest units.
- Color variations are produced by recoloring a single template across the brand palette.
