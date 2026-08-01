# Multi-Perspective Parallel Experiment · Case Study

> huashu-md-html v2.0 launch film project · 2026-05-11
> A parallel experiment of 6 artist perspectives: director's notes + HTML + keyframes

---

## Background

When the user asked to "produce a 30-second upgrade promo film for huashu-md-html v2.0", the main thread first produced the v5 baseline (Anthropic / Penguin Classics publisher taste). But the user believed it could be better and gave a critical instruction:

> "Call different subagents to generate 6 entirely different versions of the expression and visual design. You can try enabling different directors and artists. Then, once all are done, judge and review them."

This was the first systematic "multi-perspective parallel director's notes" experiment, validating a reusable workflow.

---

## Selection Logic for the 6 Perspectives

Don't just pick 6 designers arbitrarily — they must have **extremely high visual differentiation** to avoid convergence.

The 6 perspectives ultimately chosen (with reasons):

| Perspective | Genre | Aesthetic Anchor | Difference from Other Perspectives |
|------|------|---------|----------------|
| **v5 Baseline** | Modern publishing | Anthropic terracotta orange + Penguin Classics serif + Vignelli grid | Safe "tasteful" choice |
| **v5a Wes Anderson** | Film chapter aesthetics | The French Dispatch magazine feel + 1960 Olivetti industrial catalogues | Symmetric composition + chapter cards + decorative borders |
| **v5b Saul Bass** | 60s film title art | cut-paper + Trajan caps + flowing geometry | Paper-cut silhouette + big type + strong diagonals |
| **v5c Wong Kar-wai** | Hong Kong New Wave | *In the Mood for Love* / *2046* letterboxing + Chinese serif | Slow pacing + hazy glow + Chinese-first |
| **v5d Massimo Vignelli** | 1970 modernism | Knoll identity manual + NYC Subway map | Strict grid + 3-color rule + rejection of ornament |
| **v5e Kenya Hara** | Minimalist Japanese | MUJI posters + *White* | White-space philosophy + no chrome + *ma* (interval) |
| **v5f Yayoi Kusama** | Installation art | Infinity Mirror Rooms + Polka Dot Obsession | obsessive repetition + single strong color + dots |

**Selection principles**:
1. **3 different geographic cultures** (Western film / Japanese design / Hong Kong Chinese)
2. **3 different eras** (1960s / 1970s / 2010s+)
3. **3 different media** (film / graphic design / installation art)
4. **Each has a visual signature that is "the exact opposite of the generic SaaS aesthetic in the training corpus"**

---

## Execution Workflow

### Step 1 · Write an independent brief for each perspective (~15 minutes)

Each brief contains 8 fixed fields:

```
1. Project background (same for all)
2. Required reading (the same v5-director-notes.md as the methodology template)
3. What you need to do (4-item deliverable checklist)
4. That artist's DNA (6 core fields):
   - Color palette (specific HEX)
   - Typography (specific names + fallbacks)
   - Visual language (a few core rules)
   - Signature elements (identifiable signatures)
   - Rhythm (how it differs from other perspectives)
   - Anti-AI slop, hardened version (the forbidden zones in the context of this style)
5. 30-second structure reference (draft of 4-6 shots)
6. destination cards design requirements (keep them real and readable)
7. Key constraints (30s / 1920×1080 / file:// / Google Fonts CDN)
8. Output verification checklist + completion report format
```

**Key**: Every brief must stress "**do not repeat v5's aesthetic**" — otherwise the subagents will be influenced by the v5 director's notes and converge.

### Step 2 · Launch 6 subagents in parallel (6 Agent tool calls in the same message)

```js
Agent({ subagent_type: "general-purpose", run_in_background: true, name: "v5a-anderson", ... })
Agent({ subagent_type: "general-purpose", run_in_background: true, name: "v5b-bass", ... })
// ... 6 in total
```

Runs in the background; expect 30-60 minutes.

### Step 3 · Idle work while waiting

Don't poll agent status. Subagents automatically send a task notification when done. While waiting:

- Fix the main thread's v5 baseline bugs
- Write the review framework (scoring dimensions / Q&A for each version)
- Distill the methodology into the skill (this is exactly what this case study came from)
- Prepare the final summary document skeleton

### Step 4 · Failure handling (~16% failure rate, acceptable)

Observed in practice: about 1 out of 6 subagents fails due to network issues or token limits (Bass failed with a socket error on the first round). Handling:

1. When a completion notification arrives, **immediately check** that agent's output folder
2. Missing key deliverables → restart that agent (same brief; you can note "the previous run failed, please re-execute")
3. Partially complete (e.g., has HTML but no screenshots) → have the main thread fill in the Playwright screenshots; don't restart the agent

### Step 5 · Systematic review once all 6 versions are done

Review framework (5 dimensions + 3 top-level questions + use case assignment):

```
5-dimension scoring (each dimension 1-10):
- Distinctiveness (visual differentiation)
- Coherence (aesthetic consistency)
- Anti-slop (anti-AI slop execution)
- Story arc (rhythm and narrative arc)
- Pause-and-look (detail density)

3 top-level questions:
- Q1 Screenshot-worthy? (triggers a pause and share on social platforms)
- Q2 Memorable in one line? (leaves a proposition-level memory)
- Q3 Timeless? (won't look cheap when revisited 5 years later)

use case assignment (by platform and audience):
- WeChat Official Account / X / Bilibili / Moments / Dribbble / client demos / private traffic / ...
```

See the REVIEW.md that sits in the same directory as `assets/director-notes-samples/launch-film-30s-sample.md`.

---

## Experiment Output (Facts)

### Documentation Volume

- v5 baseline director's notes: 11,500 characters
- Each of the 6 perspective director's notes: 4,000-12,000 characters
- Total documentation: ~55,000-70,000 characters
- All 5 major section structures complete: 6/6 versions

### HTML Implementation

- Each version has its own animation.html, 30 seconds, 1920×1080
- File size 28-74KB
- All open via file:// (no server dependency)

### Keyframes

- 10-18 PNGs per version, covering the full 30-second story arc
- Total screenshots: 80+
- Average PNG size: 100-200KB

### Duration

- 6 subagents running in parallel: ~12-15 minutes (per duration_ms)
- Main thread parallel idle work (fixing v5 + writing methodology): completed in the same window
- Overall, "from launching the 6 perspectives to all deliverables in place": ~60 minutes

---

## Key Insights (for huashu-design's future users)

### Insight 1 · The "write tens of thousands of characters of director's notes first" methodology is **fully reproducible**

All 6 subagents produced complete specs of 4,000-12,000 characters following the 5-major-section structure, and all reached marketing-ready quality when implementing the HTML. This proves the methodology itself doesn't depend on the talent of any single executor — **as long as the brief is clear, multiple independent executors can produce consistently high-quality results**.

### Insight 2 · A "perspective" must be concrete down to "work + year"

Each brief lists concrete works to reference:
- Anderson → *The French Dispatch* (2021) + *Moonrise Kingdom* (2012) + Penguin Classics dust jackets + 1960s Olivetti catalogues
- WKW → *In the Mood for Love* (2000) + *2046* (2004)
- Vignelli → 1972 NYC Subway map + Knoll identity manual + *The Vignelli Canon*
- Hara → MUJI brand 1995-2023 + *White* + Junya Ishigami transparency
- Kusama → Infinity Mirrored Rooms (2013-2023) + the Polka Dot Obsession installation

**Result in practice**: All subagents accurately captured that work's core visual DNA rather than the "average" of the genre.

### Insight 3 · The "style-hardened version" of anti-AI slop is the key

Generic anti-slop (purple gradients / emoji / SVG people) applies to all versions. But **each style also needs its own "dedicated anti-slop"** rules:

- Bass: no Helvetica (too clean; Bass is rugged)
- Vignelli: no rounded corners (all corners 90°)
- Hara: no gradients at all + no sans-serif display type
- Kusama: no modern SaaS look
- Anderson: no cyber color schemes
- WKW: no Inter (WKW uses serifs)

With these in place, the 6 versions had extremely high stylistic purity, with none converging toward another.

### Insight 4 · The real value of multi-perspective isn't "picking a winner"

The original idea was an A/B test to pick the best version. In the actual review, we found that **each of the 6 versions has a clear use case**:
- v5 baseline → product page / WeRead (high information density)
- Anderson → WeChat Official Account long-article hero image (strong magazine-flipping feel)
- WKW → Bilibili / Chinese cultural content (nostalgic warmth)
- Vignelli → design community / Dribbble (every frame is a print poster)
- Hara → client demos / static screenshots (minimalist philosophy)
- Kusama → X short videos / viral spread (visual impact)

**Conclusion**: Marketing isn't a single shot; it's platform-specific multiplexing. The real value of 6 perspectives running in parallel is **giving one project 6 differentiated weapons**, not making 5 versions unfit for the stage.

### Insight 5 · A subagent failure rate of ~16% is acceptable

1 out of 6 failed (Bass's first-round socket error). Cost of handling: restart + a 5-minute simplified brief, then another 12-15 minutes of waiting. **Compare that with waiting for a single agent to run all 6 versions sequentially (90+ minutes)** — parallel execution with retry is clearly more economical.

### Insight 6 · The main thread must do substantive idle work while waiting

Subagents take 12-15 minutes to finish. During that time the main thread should never sit idle:

- **Fix the main version bugs** (ones the user already reported)
- **Write the review framework** (to be filled in during review)
- **Distill the methodology into the skill** (like this case study)
- **Prepare the final summary** (so it's clear at a glance when the user returns)

This is the "main thread responsibility" in a parallel multi-agent workflow — not a PM waiting for results, but an orchestrator advancing in sync.

---

## When to Enable "Multi-Perspective Parallel"

| Scenario | Enable? | Reason |
|------|---------|------|
| User explicitly says "I want to see different directions" or "make a few more versions" | ✅ Enable immediately | Direct request |
| First version done, user is unhappy but can't say what they want | ✅ Enable | A/B selection beats "let me guess what you want" |
| Project is heading for multi-platform distribution (X / WeChat Official Account / Bilibili / Moments) | ✅ Enable | One version per platform |
| Client hasn't locked in a style but has budget (time + tokens) | ✅ Enable | Repeated revisions = 5x the cost |
| User has already given clear style references and only wants 1 version | ❌ Don't enable | Wasteful |
| The task is a simple motion graphic / icon animation | ❌ Don't enable | Over-engineering |
| Tight deadline < 30 minutes | ❌ Don't enable | Subagents won't finish in time |

---

## Full Methodology Flowchart

```
User brief (including quality expectations)
       ↓
[Main thread] Write v5 baseline director's notes (5 major sections, tens of thousands of characters)
       ↓
[Main thread] Implement v5 HTML + capture keyframes (marketing baseline)
       ↓
[Decision point] Enable multi-perspective?
       ↓ YES
[Main thread] Choose 6 differentiated perspectives + write 6 independent briefs (8 fields each)
       ↓
[6 subagents in parallel]
   ├── v5a brief → director-notes + html + keyframes + README
   ├── v5b brief → ...
   ├── v5c brief → ...
   ├── v5d brief → ...
   ├── v5e brief → ...
   └── v5f brief → ...
       ↓
[Main thread in sync] Fix v5 bugs · write review framework · distill methodology
       ↓
[All 6 notifications arrive]
       ↓
[Main thread] Failure detection + retry / fill in screenshots
       ↓
[Main thread] 5-dimension scoring + 3 top-level questions + use case assignment
       ↓
[Main thread] Write the final REVIEW.md
       ↓
[Deliver] 6 complete versions + review + platform distribution recommendations
```

---

## Related Documents

- Full methodology: `references/launch-film-director-notes.md`
- Single-perspective sample: `assets/director-notes-samples/launch-film-30s-sample.md` (v5 baseline)
- Live project location: the original author's local demos directory (contains the full 6 + 1 perspective file set; not distributed with the repo)
- Review: the original author's local REVIEW.md (not distributed with the repo)

---

*Last updated: 2026-05-11*
*Real case study: huashu-md-html v2.0 launch film 6-perspective parallel experiment*
