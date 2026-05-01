# Design Critique In-Depth Guide

> Phase 7 detailed reference. Provides scoring criteria, scenario focus, common issues checklist.

---

## Scoring Criteria Explained

### 1. Philosophy Alignment

| Score | Criteria |
|------|------|
| 9-10 | Design perfectly embodies chosen philosophy's core spirit, every detail has philosophical basis |
| 7-8 | Overall direction correct, core features in place, individual details deviate |
| 5-6 | Intent visible, but other style elements mixed in during execution, not pure |
| 3-4 | Only surface imitation, philosophy kernel not understood |
| 1-2 | Basically unrelated to chosen philosophy |

**Critique points**:
- Did it use that designer/agency's signature techniques?
- Do colors, fonts, layout follow that philosophical system?
- Any "self-contradicting" elements? (e.g., chose Kenya Hara but packed with content)

### 2. Visual Hierarchy

| Score | Criteria |
|------|------|
| 9-10 | User's eye naturally flows along designer's intent, zero friction in information acquisition |
| 7-8 | Primary/secondary relationship clear, occasional 1-2 fuzzy layers |
| 5-6 | Can distinguish title from body, but middle layers chaotic |
| 3-4 | Information laid flat, no clear visual entry point |
| 1-2 | Chaotic, user doesn't know where to look first |

**Critique points**:
- Is title vs body font size contrast sufficient? (at least 2.5×)
- Do color/weight/size establish 3-4 clear layers?
- Does whitespace guide the eye?
- "Squint test": when squinting, are layers still clear?

### 3. Craft Quality

| Score | Criteria |
|------|------|
| 9-10 | Pixel-perfect, alignment, spacing, color flawless |
| 7-8 | Overall refined, 1-2 minor alignment/spacing issues |
| 5-6 | Basic alignment, but inconsistent spacing, unsystematic color use |
| 3-4 | Obvious alignment errors, chaotic spacing, too many colors |
| 1-2 | Rough, looks like draft |

**Critique points**:
- Using unified spacing system? (e.g., 8pt grid)
- Are spacing consistent among similar elements?
- Is color count controlled? (usually no more than 3-4)
- Font family unified? (usually no more than 2)
- Edge alignment precise?

### 4. Functionality

| Score | Criteria |
|------|------|
| 9-10 | Every design element serves purpose, zero redundancy |
| 7-8 | Clear functional orientation, small amount of removable decoration |
| 5-6 | Basically usable, but obvious decorative elements distract |
| 3-4 | Form over function, user needs to work to find information |
| 1-2 | Completely drowned in decoration, lost ability to convey information |

**Critique points**:
- If removing any element, does design get worse? (if not, should delete)
- Is CTA/key information in most prominent position?
- Any "added because it looks good" elements?
- Does information density match carrier? (PPT shouldn't be too dense, PDF can be denser)

### 5. Originality

| Score | Criteria |
|------|------|
| 9-10 | Refreshing, found unique expression within that philosophical framework |
| 7-8 | Has own thinking, not simple template application |
| 5-6 | Conventional, looks like template |
| 3-4 | Heavy use of clichés (e.g., gradient spheres representing AI) |
| 1-2 | Complete template or asset collage |

**Critique points**:
- Avoiding common clichés? (see "Common Issues Checklist" below)
- Has personal expression while following design philosophy?
- Any "unexpected but reasonable" design decisions?

---

## Scenario Critique Focus

Different output types have different critique priorities:

| Scenario | Most Important | Second Important | Can Relax |
|------|-----------|--------|--------|
| WeChat cover/illustration | Originality, Visual Hierarchy | Philosophy Alignment | Functionality (single image no interaction) |
| Infographic | Functionality, Visual Hierarchy | Craft Quality | Originality (accuracy first) |
| PPT/Keynote | Visual Hierarchy, Functionality | Craft Quality | Originality (clarity first) |
| PDF/Whitepaper | Craft Quality, Functionality | Visual Hierarchy | Originality (professional first) |
| Landing page/website | Functionality, Visual Hierarchy | Originality | — (full requirements) |
| App UI | Functionality, Craft Quality | Visual Hierarchy | Philosophy Alignment (usability first) |
| Xiaohongshu image | Originality, Visual Hierarchy | Philosophy Alignment | Craft Quality (atmosphere first) |

---

## Top 10 Common Design Issues

### 1. AI Tech Clichés
**Problem**: Gradient spheres, digital rain, blue circuit boards, robot faces
**Why it's a problem**: Users already visually fatigued, can't distinguish you from others
**Fix**: Use abstract metaphors instead of literal symbols (e.g., "conversation" metaphor instead of chat bubble icon)

### 2. Insufficient Type Hierarchy
**Problem**: Title and body font sizes too close (<2.5×)
**Why it's a problem**: Users can't quickly locate key information
**Fix**: Title at least 3× body (e.g., body 16px → title 48-64px)

### 3. Too Many Colors
**Problem**: Using 5+ colors, no primary/secondary
**Why it's a problem**: Visual chaos, weak brand identity
**Fix**: Limit to 1 primary + 1 secondary + 1 accent + grays

### 4. Inconsistent Spacing
**Problem**: Element spacing random, no system
**Why it's a problem**: Looks unprofessional, visual rhythm chaotic
**Fix**: Establish 8pt grid system (spacing only use 8/16/24/32/48/64px)

### 5. Insufficient White Space
**Problem**: All space filled with content
**Why it's a problem**: Information crowding causes reading fatigue,反而 reduces information delivery efficiency
**Fix**: White space at least 40% of total area (60%+ for minimal style)

### 6. Too Many Fonts
**Problem**: Using 3+ fonts
**Why it's a problem**: Visual noise, undermines unity
**Fix**: Max 2 fonts (1 title + 1 body), create variation with weight and size

### 7. Inconsistent Alignment
**Problem**: Some left-aligned, some centered, some right-aligned
**Why it's a problem**: Breaks visual sense of order
**Fix**: Choose one alignment (recommend left-aligned), unify globally

### 8. Decoration Over Content
**Problem**: Background patterns/gradients/shadows steal main content spotlight
**Why it's a problem**: Backwards, users come for information not decoration
**Fix**: "If removing this decoration, does design get worse?" If not, delete

### 9. Cyber Neon Abuse
**Problem**: Dark blue background (#0F1117) + neon glow effects
**Why it's a problem**: Default aesthetic forbidden zone (this skill's taste baseline), and has become one of the biggest clichés — users can override with their own brand
**Fix**: Choose more distinctive color scheme (reference 20-style color systems)

### 10. Information Density Mismatch with Carrier
**Problem**: Full page of text in PPT / 10 elements in cover image
**Why it's a problem**: Different carriers have different optimal information densities
**Fix**:
- PPT: 1 core point per slide
- Cover image: 1 visual focal point
- Infographic: layered display
- PDF: can be denser, but needs clear navigation

---

## Critique Output Template

```
## Design Critique Report

**Overall Score**: X.X/10 [Excellent(8+)/Good(6-7.9)/Needs Improvement(4-5.9)/Fail(<4)]

**Component Scores**:
- Philosophy Alignment: X/10 [one sentence]
- Visual Hierarchy: X/10 [one sentence]
- Craft Quality: X/10 [one sentence]
- Functionality: X/10 [one sentence]
- Originality: X/10 [one sentence]

### Strengths (Keep)
- [Specifically point out what was done well, use design language]

### Issues (Fix)
[Sorted by severity]

**1. [Issue Name]** — ⚠️Critical / ⚡Important / 💡Optimize
- Current: [describe现状]
- Problem: [why this is a problem]
- Fix: [specific action, with values]

### Quick Wins
If only 5 minutes, prioritize these 3:
- [ ] [Most impactful fix]
- [ ] [Second most important fix]
- [ ] [Third most important fix]
```

---

**Version**: v1.0
**Update date**: 2026-02-13