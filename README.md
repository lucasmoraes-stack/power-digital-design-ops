# PowerDigital Lab

PowerDigital Lab is a small team of AI agents that produces on-brand creative for Power Digital's client brands — Meta/Instagram posts, Google Ads programmatic banners, and email marketing (through a dedicated email operation, see below).

It exists to take the repetitive, manual side of design production off the team's plate: resizing the same creative across a dozen ad sizes, adapting copy across message variants, recoloring templates across a brand's palette. None of that needs creative judgment, it just takes time. Automating it frees up time for the work that actually needs a person — strategy, art direction, reviewing the output — while a dedicated brand agent and a human review step keep everything on-brand before it ships.

---

## Technical reference

The rest of this document is for whoever maintains the setup.

### The agent team

Defined in [.claude/agents/](.claude/agents/) — a small, fixed team of 4, scoped to *making the creative*. Media buying and conversion tracking are out of scope on purpose — a different team's job once a brand is live.

- **Briefing Analyst** (`briefing-analyst.md`) — receives the demand, identifies the brand and the ask, hands off to the right specialist.
- **Brand Guardian** (`design-brand-guardian.md`) — holds the full brand, checks everything before it ships.
- **Copywriter** (`copywriter.md`) — copy for Meta creatives and banner ads, plus testing angles. Sits out brands whose copy arrives pre-approved (e.g. Tom's of Maine).
- **Designer** (`designer.md`) — visual direction for Meta creatives and AI image-prompt generation for banners. Email moved to the email operation (below).

Copywriter and Designer are brand-agnostic in structure but brand-aware in content: each carries a `## <Brand>` section, right inside its own file, for every onboarded client. Briefing Analyst hands off by naming the brand, it doesn't re-explain it.

### How an agent works (cheat sheet)

An agent = one markdown file in `.claude/agents/`: YAML frontmatter + a system prompt. No code, no build step.

| Frontmatter field | Does |
|---|---|
| `name` / `description` | Routes the request here. Vague description = broken routing |
| `tools` | Limits what it can touch (omit = full access) |
| *(body text)* | The actual instructions |

**Two styles in this repo:**

| | Template-heavy | Fact-heavy |
|---|---|---|
| Example | `design-brand-guardian.md` | `copywriter.md`, `designer.md`, `briefing-analyst.md` |
| Origin | Near-verbatim from [agency-agents](https://github.com/msitarzewski/agency-agents) | Written for this repo |
| Holds | Persona, rules, output templates | Real hex codes, approved lines, do/don't per brand |
| Why it works | Reads `clients/<brand>/01-brand/identity/` live, no facts baked in | Real facts beat generic advice once you have them |

**The flow:**

```mermaid
flowchart LR
    A[Briefing Analyst<br/>routes] --> B[Copywriter<br/>copy]
    A --> C[Designer<br/>visuals]
    B --> D[Brand Guardian<br/>checks vs. source of truth]
    C --> D
```

Fixed at 4 agents on purpose: a new brand or format means teaching the existing agents, not adding a 5th. The one exception is email, which runs as its own packaged operation (below) because it has its own medium, method and gate.

### The email operation

Email runs as its own packaged operation in [email-ops/](email-ops/), with three dedicated agents. It is brand-agnostic by design: the agents carry **no brand sections**. Each brand gets an **email kit** instead (tokens, assets, an approved module library), built once from the brand's own sources, and every email is composed from that kit in **real email HTML**, so what gets reviewed is what ships.

- **Email Designer** (`design-email-designer.md`): builds the brand's email kit (Mode A) and composes the emails from it (Mode B).
- **Email QA Reviewer** (`design-email-qa-reviewer.md`): PASS/BLOCK gate before any email leaves, with line-level fixes.
- **Email Marketing Strategist** (`marketing-email-strategist.md`): flow strategy only (trigger, cadence, segment, metrics, deliverability).
- **Copywriter** joins when the copy does not arrive from the client (subjects, preheaders, copy checks).

**Once per brand, the kit:**

```mermaid
flowchart LR
    A[Brand sources<br/>Diagnostic + Strategy<br/>+ style guide] --> K[Email Designer<br/>builds the kit]
    R[Sent emails +<br/>reference emails] --> K
    P[Store catalog<br/>packshots + prices] --> K
    K --> V[Kit review page<br/>owner approves]
```

**Every batch or flow, the emails:**

```mermaid
flowchart LR
    C[Client copy] --> W[Copywriter<br/>subjects + checks]
    C --> B[Email Designer<br/>brief]
    W --> B
    B --> H[Email Designer<br/>HTML emails]
    H --> Q[Email QA Reviewer<br/>PASS / BLOCK]
    Q --> RV[Review page<br/>owner comments]
    RV --> F[Figma copy<br/>or ESP]
```

Two designers can build in parallel (e.g. emails 01-02 and 03-04 of a batch); the brief keeps them aligned.

**What lives where:**

| Path | What it is |
|---|---|
| `email-ops/playbook.md` · `rules.md` · `CHECKLIST.md` | the method in 8 stages, the rules of every email, the full checklist |
| `email-ops/templates/email-kit/` | the kit template (tokens, 15 base modules, asset spec) |
| `email-ops/tools/` | `build_kit.py` (new kit), `render.py` (PNG at 680/375/dark), `build_preview.py` (one-page review), `fetch_shopify_catalog.py` (packshots and prices from the store), `export.py` (copy the operation to another project) |
| `clients/<brand>/01-brand/email-kit/` | the brand's kit: README with the brand map and every owner decision, `components.html`, `assets/`, `references/`, `tools/compose.py` |
| `clients/<brand>/01-brand/photos/` | image bank originals: `products/`, `lifestyle/`, `backgrounds/` (kept out of git) |
| `clients/<brand>/03-work/email/<batch>/` | copy source, brief, HTML emails, QA reports |

**Hard rules:** no kit, no email · only kit modules (a new module enters the kit first) · never invent a number, price or claim · live text, never text baked into images · no em dashes in any copy · nothing ships without QA PASS.

### First brand on email: Habit Outdoors

Onboarded 2026-09-24, from a brand identity PDF, the live Shopify site and the team's last five hand-made emails.

- **Kit v0.2 approved**, v0.3 and v0.4 pending: palette measured from the sent emails, vector logo rebuilt from the PDF, 26 modules including rustic ones (full-bleed photo hero, textured bands, torn paper edges, product fans, product crossing a torn edge, photo collage).
- **First batch:** 4 broadcast emails (`clients/habit-outdoors/03-work/email/2026-broadcasts/`), built in two rounds and QA-passed as review drafts.

**Learning loop, captured for Habit:**
- The team's recent sent emails are the source of truth for brand info; the PDF guide only fills gaps.
- Whatever the sent emails don't have, the kit doesn't use (no address line, no first-name merge).
- Round 1 followed the kit to the letter and read as timid. Round 2 rule: no flat band, every border torn, full-bleed photo heroes, products with weight. Written down in `art-direction-r2.md`.
- Overlap, bleed, torn edges and collage can't be done with CSS in email: they are composed as one image by script, with the band colors baked into the edges, and text stays live around them.
- Product names, prices and packshots come from the store catalog, never typed by hand.

### Building a new agent: checklist

- [ ] `name` + `description` that says **when** to call it
- [ ] `tools` scoped to what it actually needs
- [ ] Role in one sentence
- [ ] Scope: what it does / does not do
- [ ] Real, verified facts, not generic advice
- [ ] Short do/don't rules
- [ ] "Don't guess, flag a human" rule
- [ ] Handoff: who gets the output next

<details>
<summary>Minimal skeleton</summary>

```markdown
---
name: AgentName
description: When to call this agent
tools: Read, Write, Edit
---
# AgentName
[Role in one line]

## Scope
Does / does not (→ who does)

## Facts
- ...

## Missing info
Flag it, don't guess.

## Handoff
→ next agent
```
</details>

### How branding flows into the agents

- **Brand Guardian owns the full guidelines** — distilled into one digest at `clients/<brand>/01-brand/identity/brand-guidelines.md`. For tokens and basic elements (color, type, logo), the shared [Figma Library](https://www.figma.com/design/pcf9QNPjvBBzqDPnBLefVS/Claude-Design-Ops---Lab?node-id=74-7766) — one style-guide section per brand — outranks the PDF and this digest wherever they disagree.
- **The same Figma Library also holds reusable design templates per brand**, not just tokens — Katapult's live under [node 251:480](https://www.figma.com/design/pcf9QNPjvBBzqDPnBLefVS/Claude-Design-Ops---Lab?node-id=251-480) ("/templates - Katapult"), 11 branded layout patterns, on-brand with real approved copy already in place. Designer starts here before building a new layout from scratch. (An older node, `178:1377`, was cited here previously — confirmed gone as of 2026-09-10, don't use it.)
- **Copywriter and Designer get only their slice**, written directly into their own `## <Brand>` section — voice and approved phrasing for Copywriter, palette and photography rules for Designer.
- **References** (templates, layout specs) live alongside the digest, under `01-brand/references/`.
- **Every human correction becomes a standing rule**, written back into the relevant brand section.

Katapult's sections are fully written from its brand guidelines. Roku's are partial — visual facts observed while reframing existing creative, with voice and audience flagged as not yet captured rather than guessed at.

### Repository structure

```
.claude/agents/               the 4-agent creative team + 3 email agents (auto-loaded by Claude Code)
email-ops/                    the email operation package: playbook, rules, checklist, kit template, tools
CLAUDE.md                     project instructions (routing, folder conventions)
clients/
  <brand>/
    01-brand/
      identity/
        brand-guidelines.md  master digest (Brand Guardian's source of truth)
      references/            templates, layout specs, test imagery
      strategy/              Diagnostic Report, Strategy Report (required for email)
      email-kit/             the brand's email kit (email-ops)
    03-work/email/<flow>/    email briefs and HTML in progress
    00-inbox/                incoming demands
    04-deliverables/
      social/                Meta creatives produced
      banners/               banner creatives produced
      email/<flow>/          final email HTML for the ESP
```

### Learning loop — examples already captured for Katapult

- The product mockup bleeds off a frame edge and sits high to fill the space, never floating.
- Headlines run large and are scaled to the format, never timid.
- The legal disclaimer is white with a thin black outline so it stays legible over a photo, and is dropped on the smallest units.
- Color variations are produced by recoloring a single template across the brand palette.
- Reframing to a new aspect ratio (4:5/16:9/9:16) needs per-ratio composition judgment, not a uniform scale-down — see `designer.md`'s Figma-execution discipline notes for the safe-zone and balance rules a real reframe test (2026-09-10) surfaced.
- A Figma `.clone()` can silently reparent to the wrong container — always verify a new node's actual parent, and verify success by screenshotting the container it should appear in, not just the node itself.
