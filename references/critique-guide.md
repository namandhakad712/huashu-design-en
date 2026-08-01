# Design Review In-Depth Guide

> Phase 7 detailed reference. Provides scoring criteria, scenario focus, common issues checklist.

---

## Scoring Criteria Explained

### 0. Concept (Concept) · Highest weight

First ask "does this design have an idea", then look at how well it's done. Why it's in position 0: execution is an amplifier — amplifying an empty concept only makes it emptier.

| Score | Criteria |
|------|------|
| 9-10 | A unique idea that grows out of the user's content, with a visual motif that can't be replaced |
| 7-8 | Has clear intent; the motif relates to the content but would barely survive swapping in a similar theme |
| 5-6 | Style but no concept: it looks nice but says nothing |
| 3-4 | Generic template reskinned, concept layer is zero |
| 1-2 | Didn't even pick the style right, pure decorative pile-up |

**Core question checklist**:
- What does this design say? Can you state its idea in one sentence? If you can't, it doesn't have one
- Cover up all text and logos — can you still recognize the theme? If not, the visuals aren't doing any of the expression (except type-as-motif layout design, where instead ask: would this typographic treatment still hold under a different theme)
- Would it still hold with a different client/product name? **If yes = template, this dimension is capped at ≤5 points**
- Does the form have a unique visual motif derived from the content? (echoing SKILL.md's form derivation: form should be derived from content, not drawn from a style library)

**One-vote-veto rule**: when Concept scores ≤5, the overall score is capped at 6.0 (the floor of the Good tier). The other five dimensions are all execution — no matter how refined the execution, it can't pull back a design without an idea; that's just polishing a template shinier.

### 1. Philosophy Alignment

| Score | Criteria |
|------|------|
| 9-10 | The design perfectly embodies the core spirit of the chosen philosophy; every detail has a philosophical basis |
| 7-8 | Overall direction is right, core features are in place, a few details drift |
| 5-6 | Intent is visible, but elements of other styles got mixed in during execution — not pure enough |
| 3-4 | Surface imitation only, the philosophical core isn't understood |
| 1-2 | Essentially unrelated to the chosen philosophy |

**Review points**:
- Are the signature techniques of that designer/agency used?
- Do color, typography, and layout conform to that philosophical system?
- Any "self-contradictory" elements? (e.g. picking Kenya Hara but stuffing it full of content)

### 2. Visual Hierarchy

| Score | Criteria |
|------|------|
| 9-10 | The user's gaze flows naturally along the designer's intent, zero friction in information access |
| 7-8 | Primary/secondary relationships are clear, with 1-2 occasional spots of blurred hierarchy |
| 5-6 | Headlines and body can be told apart, but the middle levels are muddled |
| 3-4 | Information laid out flat, no clear visual entry point |
| 1-2 | Chaotic, the user doesn't know where to look first |

**Review points**:
- Is the size contrast between headlines and body sufficient? (at least 2.5x)
- Do color/weight/size establish 3-4 clear levels?
- Is whitespace guiding the eye?
- The "squint test": squint and check whether the hierarchy stays clear?

### 3. Craft Quality

| Score | Criteria |
|------|------|
| 9-10 | Pixel-level precision, zero flaws in alignment, spacing, color |
| 7-8 | Polished overall, with 1-2 tiny alignment/spacing issues |
| 5-6 | Basically aligned, but spacing isn't consistent and color use isn't systematic enough |
| 3-4 | Obvious alignment errors, messy spacing, too many colors |
| 1-2 | Rough, looks like a draft |

**Review points**:
- Is a unified spacing system used (e.g. an 8pt grid)?
- Is spacing between like elements consistent?
- Is the number of colors controlled? (usually no more than 3-4)
- Is the typeface family unified? (usually no more than 2)
- Is edge alignment precise?

### 4. Functionality

| Score | Criteria |
|------|------|
| 9-10 | Every design element serves the goal, zero redundancy |
| 7-8 | Clearly function-oriented, with a little trimmable decoration |
| 5-6 | Basically usable, but obvious decorative elements distract attention |
| 3-4 | Form over function, users have to work to find information |
| 1-2 | Completely drowned in decoration, lost the ability to communicate information |

**Review points**:
- Delete any element — does the design get worse? (If not, it should be deleted)
- Are CTAs/key information in the most visible position?
- Any elements added "because it looks good"?
- Does information density match the medium? (PPT shouldn't be too dense, PDF can be denser)

### 5. Originality

| Score | Criteria |
|------|------|
| 9-10 | Refreshing, found a distinctive expression within that philosophical framework |
| 7-8 | Has its own thinking, not a simple template application |
| 5-6 | Middle of the road, looks like a template |
| 3-4 | Heavy use of clichés (e.g. gradient spheres representing AI) |
| 1-2 | Entirely assembled from templates or stock assets |

**Review points**:
- Are common clichés avoided? (see the "Top 10 Common Design Problems" below)
- Is there personal expression while following the design philosophy?
- Are there "unexpected but sensible" design decisions?

---

## Scenario Review Priorities

Different output types have different review priorities (the Concept dimension isn't in the table: it's the first gate for every scenario and doesn't participate in priority trade-offs):

| Scenario | Most important dimension | Secondary | Can relax |
|------|-----------|--------|--------|
| Official account (WeChat) cover/images | Originality, Visual Hierarchy | Philosophy Alignment | Functionality (single images don't involve interaction) |
| Infographic | Functionality, Visual Hierarchy | Craft Quality | Originality (accuracy first) |
| PPT/Keynote | Visual Hierarchy, Functionality | Craft Quality | Originality (clarity first) |
| PDF/White paper | Craft Quality, Functionality | Visual Hierarchy | Originality (professionalism first) |
| Landing page/corporate site | Functionality, Visual Hierarchy | Originality | — (all-around requirements) |
| App UI | Functionality, Craft Quality | Visual Hierarchy | Philosophy Alignment (usability first) |
| Xiaohongshu images | Originality, Visual Hierarchy | Philosophy Alignment | Craft Quality (atmosphere first) |

---

## Top 10 Common Design Problems

### 1. AI tech clichés
**Problem**: gradient spheres, digital rain, blue circuit boards, robot faces
**Why it's a problem**: users are already fatigued by these visuals — they can't tell you apart from anyone else
**Fix**: replace literal symbols with abstract metaphors (e.g. the metaphor of "conversation" rather than a chat bubble icon)

### 2. Insufficient type-size hierarchy
**Problem**: too small a gap between titles and body (<2.5x)
**Why it's a problem**: users can't quickly locate key information
**Fix**: titles at least 3x the body (e.g. body 16px → title 48-64px)

### 3. Too many colors
**Problem**: using 5+ colors with no primary/secondary structure
**Why it's a problem**: visual chaos, weak brand feel
**Fix**: limit to 1 primary + 1 secondary + 1 accent + gray scale

### 4. Inconsistent spacing
**Problem**: element spacing is arbitrary, no system
**Why it's a problem**: looks unprofessional, visual rhythm is chaotic
**Fix**: establish an 8pt grid system (spacing only 8/16/24/32/48/64px)

### 5. Insufficient whitespace
**Problem**: all space filled with content
**Why it's a problem**: cramped information causes reading fatigue, actually lowering communication efficiency
**Fix**: whitespace at least 40% of the total area (60%+ for minimalist styles)

### 6. Too many typefaces
**Problem**: using 3+ typefaces
**Why it's a problem**: visual noise, weakens cohesion
**Fix**: at most 2 typefaces (1 title + 1 body), create variation with weight and size

### 7. Inconsistent alignment
**Problem**: some left-aligned, some centered, some right-aligned
**Why it's a problem**: breaks the sense of visual order
**Fix**: pick one alignment (left alignment recommended) and apply it globally

### 8. Decoration over content
**Problem**: background patterns/gradients/shadows steal the spotlight from the main content
**Why it's a problem**: the cart before the horse — users come for information, not decoration
**Fix**: "if you delete this decoration, does the design get worse?" If not, delete it

### 9. Cyber-neon abuse
**Problem**: deep-blue base (#0D1117) + neon glow effects
**Why it's a problem**: a default aesthetic forbidden zone (this skill's taste baseline), and already one of the biggest clichés — users may override per their own brand
**Fix**: pick a more distinctive color scheme (refer to the color systems of the 20 styles)

### 10. Information density not matching the medium
**Problem**: a whole page of text in a PPT / 10 elements crammed into a cover image
**Why it's a problem**: different mediums have different optimal information densities
**Fix**:
- PPT: 1 core viewpoint per page
- Cover image: 1 visual focus
- Infographic: layered presentation
- PDF: can be denser, but needs clear navigation

---

## Review Output Template

```
## Design Review Report

**Overall score**: X.X/10 [Excellent (8+)/Good (6-7.9)/Needs improvement (4-5.9)/Failing (<4)]
(When Concept ≤5 the overall score caps at 6; fix the concept before talking about execution)

**Dimension scores**:
- Concept: X/10 [what is this design's idea? state it in one sentence]
- Philosophy Alignment: X/10 [one-sentence explanation]
- Visual Hierarchy: X/10 [one-sentence explanation]
- Craft Quality: X/10 [one-sentence explanation]
- Functionality: X/10 [one-sentence explanation]
- Originality: X/10 [one-sentence explanation]

### Strengths (Keep)
- [point out what's done well specifically, described in design language]

### Problems (Fix)
[sorted by severity]

**1. [Problem name]** — ⚠️Fatal / ⚡Important / 💡Improvement
- Current state: [describe the current situation]
- Problem: [why this is a problem]
- Fix: [specific actions, with values]

### Quick Wins Checklist
If you only have 5 minutes, do these 3 things first:
- [ ] [the highest-impact fix]
- [ ] [the second-most-important fix]
- [ ] [the third-most-important fix]
```

---

**Version**: v1.0
**Updated**: 2026-02-13
