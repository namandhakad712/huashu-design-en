# Workflow: From Receiving Task to Delivery

The more senior the designer, the earlier they align — because they know better what rework costs. This file is the main workflow after the three directions are picked, plus how to ask questions before starting.

## Standard Workflow (after the three directions are picked)

1. **Understand the requirement**: when a specific product, technology, or event is involved, the first action is a WebSearch to verify existence, release status, version, and specs, written into the project's `product-facts.md` — this step comes before asking questions. Anything already asked in the three-direction Phase 1 isn't asked again; new tasks that didn't go through the three-direction gate (e.g. after a direction exemption) get one round of questions; small fixes skip it.
2. **Explore resources, extract core assets**: read the design system, links, screenshots, code. For specific brands follow the Core Asset Protocol, producing `brand-spec.md`. Before starting, confirm core assets are in place: physical products have product photos, digital products have logos and UI screenshots, color values extracted from real HTML/SVG. If anything's missing, stop and fill the gap.
3. **Answer the five form questions before planning the system** (before each page, screen, or shot starts):
   - **Narrative role**: hero / transition / data / quote / ending?
   - **Viewer distance**: 10cm phone / 1m laptop / 10m projection? Determines font size and density
   - **Visual temperature**: quiet / excited / calm / authoritative / gentle / sad?
   - **Capacity estimate**: sketch 3 five-second thumbnails, check whether the content actually fits
   - **Visual motif**: what visual element, structure, or metaphor is unique to this content and wouldn't appear for any other subject? If you can't answer, you're still drawing straws from style labels

   Only after answering, state the design system (color, type, layout rhythm, component patterns) — the system serves the answers. At delivery, write one line on "where the form grew out of the content".
   🛑 Say the five answers + the system out loud, and wait for the user's nod before writing code.
4. **Create the folder**: put the main HTML and needed assets under `project-name/` (don't bulk-copy >20 files).
5. **Alignment pass**: write assumptions + placeholders + reasoning comments at the top of the HTML. 🛑 Show the user early (even if it's just gray blocks with labels), and wait for feedback before writing components.
6. **Full pass**: fill placeholders, make variations, add Tweaks. Show the user once more halfway through.
7. **Verify**: Playwright screenshots, check console errors, `python3 "$HD/scripts/design_lint.py" check` (red lights must be fixed). 🛑 Before delivery, eyeball it in the browser yourself — AI-written interactions are often buggy.
8. **Deliver and feed back**: the summary says only caveats and next steps; `design_lint.py ledger add` logs the look ledger; `learn.py harvest` checks what's worth remembering (`references/evolution.md`).

**Checkpoint principle**: when you hit a 🛑, stop, spell out "I've done X, next I plan Y — confirm?" and actually wait. "Continue" authorizes moving to the next step, not skipping the gate inside the current one.

## Exception Handling

| Scenario | What to do |
|---|---|
| Requirement too vague to start | List 3 possible directions (e.g. "landing page / Dashboard / product detail page") for the user to pick — don't fire 10 questions directly |
| User says "stop asking, just do it" | The questions can be skipped (fill in assumptions yourself), but the three-direction gate still runs; only when the user explicitly says "don't show three versions / one version is enough" do you drop to 1 main + 1 variant, recording the verbatim words in `direction-approved.md` |
| Reference images conflict with brand specs | Stop, point out the specific contradiction ("the screenshot is serif, the spec says sans-serif"), let the user pick |
| Starter components fail to load | Check the error table in `references/react-setup.md` first; if that doesn't fix it, downgrade to pure HTML+CSS |
| Time pressure, "needed within 30 minutes" | Skip the alignment pass and go straight to full pass with a single option, labeling the delivery "not early-confirmed" |
| A single HTML >1000 lines | Split into multiple jsx per `references/react-setup.md`, sharing via `Object.assign(window, …)` at the end |
| The restraint principle conflicts with the product's information density | When the product's selling point is AI, data, or context-awareness (Dashboard, Tracker, Copilot, health, expense tracking), go high-density: at least 3 pieces of differentiated, content-bearing information per screen; decorative icons are still out |

When something goes off-script, first tell the user in one sentence what happened, then handle it per the table — never decide silently.

## The Art of Asking Questions

Ask exactly one round per project: tasks going through the three-direction gate ask in Phase 1 (at most 3 questions + one request for all reference materials). The checklist below is a question bank — pick the ones that most affect the outcome, don't ask every single one. This isn't going through the motions; you genuinely need to understand the requirement. But don't ask to pad the count — what you can infer, decide yourself and note the basis. If the user doesn't respond, fill in assumptions on your best judgment and keep going; replace follow-up questions with something visible.

**When must ask**: New tasks, vague tasks, no design context, user gave only one vague requirement.

**When can skip**: Small fixes, follow-up tasks, user already gave clear PRD + screenshots + context.

**How to ask**: Most agent environments don't have structured question UI — just ask using a markdown list in conversation. **List all questions at once for user to answer in batch**, don't ask one-by-one back-and-forth — that wastes user's time and interrupts their thinking.

## Must-Ask Checklist

For every design task, clarify these 5 categories:

### 1. Design Context (Most Important)

- Have existing design system, UI kit, component library? Where?
- Have brand guidelines, color specs, typography specs?
- Have reference screenshots of existing products/pages to reference?
- Have codebase to read?

**If user says "none"**:
- Help find — check project directory, look for reference brands
- Still none? Say explicitly: "I'll work from generic intuition, but that usually doesn't produce work matching your brand. Consider whether to provide some references first?"
- If must proceed, follow `references/design-context.md` fallback strategy

### 2. Variations Dimensions

- Beyond the three directions, on which dimensions does the user want to see variants? (The three directions themselves are fixed — no need to ask how many)

### 3. Fidelity and Scope

- How high fidelity? Wireframe / mockup / full hi-fi with real data?
- How much flow coverage? One screen / one flow / entire product?
- Any specific "must include" elements?

### 4. Tweaks

- Which parameters want real-time adjustment? (color/font size/spacing/layout/copy/feature flag)
- Should user continue tweaking after you're done?

### 5. Task-Specific (at least 4)

Ask 4+ details for specific task. For example:

**Making landing page**:
- What's the target conversion action?
- Primary audience?
- Competitor references?
- Who provides copy?

**Making iOS App onboarding**:
- How many steps?
- What does user need to do?
- Skip path?
- Target retention rate?

**Making animation**:
- Duration?
- Final use (video asset/website/social)?
- Rhythm (fast/slow/segmented)?
- Keyframes that must appear?

## Question Template Example

When encountering a new task, you can copy this structure to ask in conversation:

```markdown
Before starting, want to align on a few questions — list them all at once for you to answer together:

**Design Context**
1. Do you have a design system/UI kit/brand specs? If so, where?
2. Have reference screenshots of existing products or competitors?
3. Project has codebase to read?

**Variations**

**Fidelity**
6. Fidelity: wireframe / mockup / full hi-fi with real data?
7. Scope: one screen / one full flow / whole product?

**Tweaks**
8. Which parameters want to be adjustable after completion?

**Specific task**
9. [Task-specific question 1]
10. [Task-specific question 2]
...
```

## Early Alignment Mode

This is the most important part of the entire workflow. **Don't dive in headfirst when receiving a task**. Steps:

### Pass 1: Assumptions + Placeholders (5-15 minutes)

At the top of the HTML file, write your **assumptions + reasoning comments**, like a junior reporting to a manager:

```html
<!--
My assumptions:
- This is for XX audience
- Overall tone I understand as XX (based on user's "professional but not serious")
- Main flow is A→B→C
- Color I want to use brand blue + warm gray, not sure if you want accent color

Unresolved questions:
- Where does data for step 3 come from? Using placeholder first
- Background image: abstract geometry or real photo? Placeholder for now

If you see this and think direction is wrong, now is the lowest cost time to change.
-->

<!-- Then structure with placeholders -->
<section class="hero">
  <h1>[Main title spot - waiting for user]</h1>
  <p>[Subtitle spot]</p>
  <div class="cta-placeholder">[CTA button]</div>
</section>
```

**Save → show user → wait for feedback before next step**.

### Pass 2: Real Components + Variations (main workload)

After user approves direction, start filling. At this point:
- Write React components to replace placeholders
- Make variations (use design_canvas or Tweaks)
- If slides/animation, use starter components to begin

**Show again halfway through** — don't wait until fully done. Wrong direction late in design means showing equals wasted work.

### Pass 3: Detail Polish

After user satisfied with overall, polish:
- Font size/spacing/contrast micro-adjustments
- Animation timing
- Edge cases
- Tweaks panel refinement

### Pass 4: Verify + Deliver

- Use Playwright to screenshot (see `references/verification.md`)
- Open browser to visually confirm
- Summary **extremely minimal**: only say caveats and next steps

## Variations: Deep Logic

Giving variations isn't creating choice paralysis for user — it's **exploring possibility space**. Let user mix and match to final version.

### What good variations look like

- **Clear dimensions**: Each variation varies on different dimension (A vs B only changes color, C vs D only changes layout)
- **Has gradient**: From "by-the-book conservative" to "bold novel" progressively
- **Has labels**: Each variation has short label explaining what it's exploring

### Implementation

**Pure visual comparison** (static):
→ Use `assets/design_canvas.jsx`, grid layout side-by-side. Each cell with label.

**Multiple options/interaction differences**:
→ Build complete prototype, use Tweaks to switch. For example login page, "layout" as one Tweaks option:
- Left copy + right form
- Top logo + center form
- Full-screen background image + floating form

User toggles Tweaks to switch, no need to open multiple HTML files.

### Exploration Matrix Thinking

Each design, mentally go through these dimensions, pick 2-3 to give variations:

- Visual: minimal / editorial / brutalist / organic / futuristic / retro
- Color: monochrome / dual-tone / vibrant / pastel / high-contrast
- Typography: sans-only / sans+serif contrast / all serif / monospace
- Layout: symmetric / asymmetric / irregular grid / full-bleed / narrow column
- Density: sparse breathing / medium / information dense
- Interaction: minimal hover / rich micro-interaction / exaggerated large animation
- Material: flat / layered shadows / texture / noise / gradient

## When Encountering Uncertainty

- **Don't know how to do**: Be honest you don't know, ask user, or make placeholder to continue. **Don't fabricate**.
- **User's description contradicts**: Point out contradiction, let user pick one direction.
- **Task too big to handle at once**: break it into steps, do the first step for the user to see, then proceed.
- **User's required effect technically difficult**: State technical boundaries, provide alternatives.

## Summary Rules

At delivery, summary **very short**:

```markdown
✅ Slides complete (10 pages), with Tweaks to switch "night/day mode".

Notes:
- Page 4 data is fake, wait for your real data for replacement
- Animation uses CSS transition, no JS needed

Next step: open in your browser first, tell me which page has issues.
```

Don't:
- List every page's content
- Repeat what tech you used
- Praise your own design

Caveats + next steps, end.