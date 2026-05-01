# Slide Decks: HTML Slide Production Standards

Making slides is a high-frequency design scenario. This document explains how to make good HTML slides — from architecture selection, single-page design, to the complete path for PDF/PPTX export.

**This skill's capabilities**:
- **HTML presentation version (base deliverable, always default)** → Each slide independent HTML + `assets/deck_index.html` aggregation, keyboard page-turning in browser, fullscreen presentation
- HTML → PDF export → `scripts/export_deck_pdf.mjs` / `scripts/export_deck_stage_pdf.mjs`
- HTML → Editable PPTX export → `references/editable-pptx.md` + `scripts/html2pptx.js` + `scripts/export_deck_pptx.mjs` (requires HTML following 4 hard constraints)

> **⚠️ HTML is the foundation, PDF/PPTX are derivatives.** Regardless of final delivery format, **must** first create HTML aggregated presentation (`index.html` + `slides/*.html`), which is the slide work's "source". PDF/PPTX are snapshots exported from HTML with one command.
>
> **Why HTML-first**:
> - Best for presentation live (projector/shared screen direct fullscreen, keyboard page-turn, no dependency on Keynote/PPT software)
> - During development, each page can be individually double-clicked to verify, no need to re-run export every time
> - The only upstream for PDF/PPTX export (avoids "found issues after export, need to modify HTML and re-export" death loop)
> - Deliverables can be "HTML + PDF" or "HTML + PPTX" dual份, recipient uses whichever they prefer
>
> 2026-04-22 moxt brochure实测: After completing 13-page HTML + index.html aggregation, `export_deck_pdf.mjs` one-line export to PDF, zero modifications. HTML version itself is directly deliverable for browser presentation.

---

## 🛑 Confirm Delivery Format Before Starting (Hardest Checkpoint)

**This decision comes before "single file or multi-file".** 2026-04-20 期权私董会 project实测: **Not confirming delivery format before starting = 2-3 hours rework.**

### Decision Tree (HTML-first Architecture)

All deliveries start from the same HTML aggregated pages (`index.html` + `slides/*.html`). Delivery format only determines **HTML writing constraints** and **export command**:

```
【Always Default · Must Do】 HTML Aggregated Presentation (index.html + slides/*.html)
   │
   ├── Only need browser presentation / local HTML archive   → Done here, HTML visual freedom max
   │
   ├── Also need PDF (print / send to group / archive)        → Run export_deck_pdf.mjs one-click output
   │                                          HTML writing free, visual unconstrained
   │
   └── Also need editable PPTX (colleague wants to edit text) → From first line of HTML write with 4 hard constraints
                                               Run export_deck_pptx.mjs one-click output
                                               Sacrifice gradients / web components / complex SVG
```

### Starting Script (Copy and Use)

> Regardless of final delivery is HTML, PDF or PPTX, I'll first create an HTML aggregated version that can switch and present in browser (`index.html` with keyboard page-turning) — this is the always default base deliverable. On top of that, I'll ask if you want additional PDF/PPTX snapshots.
>
> Which export format do you need?
> - **HTML only** (presentation/archive) → completely free visuals
> - **Also PDF** → same as above, plus one export command
> - **Also editable PPTX** (colleague will edit text in PPT) → I must write from first line of HTML with 4 hard constraints, will sacrifice some visual capabilities (no gradients, no web components, no complex SVG).

### Why "Need PPTX Means Following 4 Hard Constraints from Start"

The prerequisite for PPTX editability is that `html2pptx.js` can translate DOM element-by-element into PowerPoint objects. It requires **4 hard constraints**:

1. Body fixed at 960pt × 540pt (matches `LAYOUT_WIDE`, 13.333″ × 7.5″, not 1920×1080px)
2. All text wrapped in `<p>`/`<h1>`-`<h6>` (no div with direct text, no `<span>` for main text)
3. `<p>`/`<h*>` themselves cannot have background/border/shadow (put on outer div)
4. `<div>` cannot use `background-image` (use `<img>` tag)
5. No CSS gradients, no web components, no complex SVG decorations

**This skill's default HTML has high visual freedom** — lots of spans, nested flex, complex SVG, web components (like `<deck-stage>`), CSS gradients — **almost none naturally pass html2pptx constraints** (tested: visually-driven HTML directly to html2pptx, pass rate <30%).

### Two Real Path Cost Comparison (2026-04-20 Real Pitfall)

| Path | Approach | Result | Cost |
|------|------|------|------|
| ❌ **Write HTML freely first, fix PPTX after** | Single file deck-stage + lots of SVG/span decorations | For editable PPTX only two roads left:<br>A. Manually write pptxgenjs hundreds of lines hardcode coordinates<br>B. Rewrite 17 pages HTML to Path A format | 2-3 hours rework, and manually written version **has perpetual maintenance cost** (HTML changes one word, PPTX needs manual sync again) |
| ✅ **Follow Path A constraints from step one** | Each slide independent HTML + 4 hard constraints + 960×540pt | One command exports 100% editable PPTX, also browser fullscreen presentation (Path A HTML is standard playable HTML in browser) | Spend 5 extra minutes thinking "how to wrap text in `<p>`", zero rework |

### What About Mixed Delivery

User says "I want HTML presentation **and** editable PPTX" — **this is not mixed**, PPTX requirement overrides HTML. Write according to Path A, the HTML itself can browser fullscreen presentation (add `deck_index.html` combiner). **No extra cost.**

User says "I want PPTX **and** animation/web component" — **This is real conflict**. Tell user: editable PPTX means sacrificing these visual capabilities. Let them choose, don't secretly do manual pptxgenjs solution (becomes perpetual maintenance debt).

### What If Only Find Out Need PPTX After HTML Written (Emergency Fix)

Very rare: HTML already written,才发现 need PPTX. Recommended to follow **fallback process** (full explanation in `references/editable-pptx.md` end "Fallback: Have visual draft but user insists on editable PPTX"):

## 🛑 Decide Architecture First (Hardest Checkpoint)

This decision is before "multi-file or single-file". Wrong choice = repeatedly hitting CSS specificity/scope pitfalls throughout entire project.

### Multi-File (Default, ≥10 pages / Academic/Courseware / Multi-agent Parallel)

**When**:
- ≥10 slides
- Academic/courseware with heavy content
- Multiple agents writing different slides in parallel

**Approach**:
```
project/
├── index.html                    # Aggregator (deck_index.html copy, edit MANIFEST)
└── slides/
    ├── slide-01.html             # Each slide independent, no cross-pollution
    ├── slide-02.html
    └── ...
```

**Workflow**:
1. Copy `assets/deck_index.html` → `index.html` (or rename)
2. Edit MANIFEST array to list all slides
3. Each slide in `slides/` folder as independent HTML
4. Keyboard navigation in browser: ← → arrows, space for next
5. Fullscreen: F11 or browser menu

**Advantages**:
- Each slide CSS scope isolated, no bleeding
- Multi-agent parallel writing without conflict
- Independent debugging per slide
- Export one-click: `node export_deck_pdf.mjs` or `node export_deck_pptx.mjs`

### Single-File (≤10 pages / Pitch Deck / Need Cross-Slide Shared State)

**When**:
- ≤10 slides, content not too heavy
- Pitch deck needing consistent state across slides
- Simple one-person production

**Approach**:
```
project/
└── deck.html                    # All slides in one HTML, using deck_stage.js
```

**Usage**:
- Use `<deck-stage>` web component (from `assets/deck_stage.js`)
- Slides as `<section class="slide">`, display controlled by JS
- Auto-scale built-in: fits any screen size
- Keyboard navigation: ← → space
- Speaker notes: `data-notes` attribute on section

**Constraints** (two hard rules):
1. **`<script>` must be after `</deck-stage>`** — if script runs before component defined, fails
2. **`.active` style must be on `.slide` itself, not child** — display:none vs display:flex collision

### Decision Tree

| Scenario | Recommended |
|----------|-------------|
| ≥10 slides | Multi-file |
| Academic/courseware | Multi-file |
| Multi-agent parallel | Multi-file |
| ≤10 slides, simple | Single-file |
| Pitch deck | Either |
| Need cross-slide state | Single-file |
| Not sure | Default to multi-file (safer) |

---

## Slide Layout Fundamentals

### Basic Composition Zones

```
┌─────────────────────────────────────────────┐
│ HEADER (title + page number)                │ ← top 15%
├─────────────────────────────────────────────┤
│                                             │
│ CONTENT                                     │ ← middle 75%
│ (text / images / charts)                    │
│                                             │
├─────────────────────────────────────────────┤
│ FOOTER (source + date)                      │ ← bottom 10%
└─────────────────────────────────────────────┘
```

### Common Layouts

**Title Only** (section divider):
- Title centered vertically and horizontally
- 80%+ whitespace ratio

**Title + Bullet Points**:
- Title: top 15%
- Body: left 10%, width 80%
- Bullet points: `ul > li`, not manually typed "•"

**Two Columns**:
- Left/right ratio: 4:6 or 5:5
- Each column follow basic composition

**Image + Caption**:
- Image: 60-70% area
- Caption: bottom of image, smaller font

---

## Typography Rules

### Font Size Hierarchy

| Element | Size | Weight |
|---------|------|--------|
| Slide Title | 40-48pt | 700 (bold) |
| Section Title | 32-36pt | 600 |
| Body Text | 20-24pt | 400 (regular) |
| Caption/Notes | 14-16pt | 400 |
| Page Number | 12pt | 400 |

### Line Height

- Body: 1.4-1.6
- Title: 1.1-1.2

### Character Limits

- Title: ≤20 characters
- Body per bullet: ≤50 characters
- Total per slide: ≤300 characters

---

## Quality Checklist Before Delivery

### Visual Check
- [ ] Colors consistent with brand
- [ ] Font sizes hierarchical clear
- [ ] Alignment consistent
- [ ] Images have alt text or captions
- [ ] No broken links or placeholders

### Interaction Check
- [ ] Keyboard navigation works (← → space)
- [ ] Fullscreen works
- [ ] Auto-scale matches different screen sizes

### Export Check
- [ ] PDF export clean
- [ ] PPTX export clean (if needed)
- [ ] File sizes reasonable

---

## Common Issues and Solutions

### Issue: CSS Bleeding Between Slides

**Cause**: Global styles in single HTML affect all slides
**Solution**: Use multi-file architecture, each slide isolated

### Issue: Images Not Showing in Export

**Cause**: Relative paths wrong after export
**Solution**: Use absolute paths or verify before export

### Issue: Font Missing in PDF

**Solution**: Embed fonts or use system fonts; don't rely on custom fonts

### Issue: Layout Broken in Different Viewports

**Solution**: Test in multiple viewports; use responsive units

---

**Version**: v1.0
**Update date**: 2026-04-20