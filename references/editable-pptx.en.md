# Editable PPTX Export: HTML Hard Constraints + Size Decision + Common Errors

This document covers the path of using `scripts/html2pptx.js` + `pptxgenjs` to translate HTML element-by-element into truly editable PowerPoint text boxes, also the only path supported by `export_deck_pptx.mjs`.

> **Core prerequisite**: To follow this path, HTML must be written with the following 4 constraints from the first line. **Not "write then convert"** — retroactive fix triggers 2-3 hours rework (2026-04-20 期权私董会 project real pitfall).
>
> For scenarios prioritizing visual freedom (animations/web components/CSS gradients/complex SVG) please switch to PDF path (`export_deck_pdf.mjs` / `export_deck_stage_pdf.mjs`), **don't** expect pptx export to balance visual fidelity and editability — this is a physical constraint of PPTX file format itself (see end "Why 4 Constraints Are Not Bugs But Physical Constraints").

---

## Canvas Size: Use 960×540pt (LAYOUT_WIDE)

PPTX units are **inches** (physical size), not px. Decision principle: body's computedStyle size should **match presentation layout's inch size** (±0.1", enforced by `html2pptx.js`'s `validateDimensions`).

### 3 Candidate Size Comparison

| HTML body | Physical size | Corresponding PPT layout | When to choose |
|---|---|---|---|
| **`960pt × 540pt`** | **13.333″ × 7.5″** | **pptxgenjs `LAYOUT_WIDE`** | ✅ **Default recommended** (modern PowerPoint 16:9 standard) |
| `720pt × 405pt` | 10″ × 5.625″ | Custom | Only when user specifies "legacy PowerPoint Widescreen" template |
| `1920px × 1080px` | 20″ × 11.25″ | Custom | ❌ Non-standard size, fonts appear abnormally small after projection |

**Don't think of HTML size as resolution.** PPTX is a vector document; body size determines **physical size**, not clarity. Super large body (20″×11.25″) won't make text clearer — only makes font size pt relatively smaller to canvas, looks worse projected/printed.

### Body Writing Three Options (Equivalent)

```css
body { width: 960pt;  height: 540pt; }    /* Most clear, recommended */
body { width: 1280px; height: 720px; }    /* Equivalent, px habit */
body { width: 13.333in; height: 7.5in; }  /* Equivalent, inches intuition */
```

配套的 pptxgenjs 代码：

```js
const pptx = new pptxgen();
pptx.layout = 'LAYOUT_WIDE';  // 13.333 × 7.5 inch, no custom needed
```

---

## 4 Hard Constraints (Violations Error Directly)

`html2pptx.js` translates HTML DOM element-by-element into PowerPoint objects. PowerPoint's format constraints projected onto HTML = 4 rules below.

### Rule 1: Cannot Write Direct Text in DIV — Must Use `<p>` or `<h1>`-`<h6>`

```html
<!-- ❌ Wrong: text directly in div -->
<div class="title">Q3 Revenue up 23%</div>

<!-- ✅ Correct: text in <p> or <h1>-<h6> -->
<div class="title"><h1>Q3 Revenue up 23%</h1></div>
<div class="body"><p>New users are the main driver</p></div>
```

**Why**: PowerPoint text must exist in text frame, text frame corresponds to HTML paragraph-level elements (p/h*/li). Bare `<div>` has no corresponding text container in PPTX.

**Also can't use `<span>` for main text** — span is inline element, can't independently align as text frame. Span can **only be inside p/h\*** for local styling (bold, color change).

### Rule 2: No CSS Gradients — Only Solid Colors

```css
/* ❌ Wrong */
background: linear-gradient(to right, #FF6B6B, #4ECDC4);

/* ✅ Correct: solid color */
background: #FF6B6B;

/* ✅ If must have multi-color stripes, use flex children each with solid */
.stripe-bar { display: flex; }
.stripe-bar div { flex: 1; }
.red   { background: #FF6B6B; }
.teal  { background: #4ECDC4; }
```

**Why**: PowerPoint's shape fill only supports solid/gradient-fill two types, but pptxgenjs's `fill: { color: ... }` only maps solid. Gradient goes through PowerPoint native gradient requires separate structure, currently toolchain doesn't support.

### Rule 3: Background/Border/Shadow Only on DIV, Not on Text Tags

```html
<!-- ❌ Wrong: <p> has background -->
<p style="background: #FFD700; border-radius: 4px;">Key content</p>

<!-- ✅ Correct: outer div carries background/border, <p> only handles text -->
<div style="background: #FFD700; border-radius: 4px; padding: 8pt 12pt;">
  <p>Key content</p>
</div>
```

**Why**: In PowerPoint, shape (box/rounded rectangle) and text frame are two objects. HTML's `<p>` only translates to text frame, background/border/shadow belong to shape — must be on **div wrapping text**.

### Rule 4: DIV Cannot Use `background-image` — Use `<img>` Tag

```html
<!-- ❌ Wrong -->
<div style="background-image: url('chart.png')"></div>

<!-- ✅ Correct -->
<img src="chart.png" style="position: absolute; left: 50%; top: 20%; width: 300pt; height: 200pt;" />
```

**Why**: `html2pptx.js` only extracts image paths from `<img>` elements, doesn't parse CSS `background-image` URLs.

---

## Path A HTML Template Skeleton

Each slide one independent HTML file, scopes isolated (avoid single-file deck CSS pollution).

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    width: 960pt; height: 540pt;           /* ⚠️ Match LAYOUT_WIDE */
    font-family: system-ui, -apple-system, sans-serif;
    background: #FEFEF9;                    /* Solid, no gradients */
    overflow: hidden;
  }
  /* DIV handles layout/background/border */
  .card {
    position: absolute;
    background: #1A4A8A;                    /* Background on DIV */
    border-radius: 4pt;
    padding: 12pt 16pt;
  }
  /* Text tags only handle font styles, no background/border */
  .card h2 { font-size: 24pt; color: #FFFFFF; font-weight: 700; }
  .card p  { font-size: 14pt; color: rgba(255,255,255,0.85); }
</style>
</head>
<body>

  <!-- Title area: outer div positions, inner text tag -->
  <div style="position: absolute; top: 40pt; left: 60pt; right: 60pt;">
    <h1 style="font-size: 36pt; color: #1A1A1A; font-weight: 700;">Title uses declarative sentence, not topic</h1>
    <p style="font-size: 16pt; color: #555555; margin-top: 10pt;">Subtitle additional explanation</p>
  </div>

  <!-- Content card: div handles background, h2/p handles text -->
  <div class="card" style="top: 130pt; left: 60pt; width: 240pt; height: 160pt;">
    <h2>Key Point One</h2>
    <p>Brief explanation text</p>
  </div>

  <!-- List: use ul/li, don't manually type • symbols -->
  <div style="position: absolute; top: 320pt; left: 60pt; width: 540pt;">
    <ul style="font-size: 16pt; color: #1A1A1A; padding-left: 24pt; list-style: disc;">
      <li>First key point</li>
      <li>Second key point</li>
      <li>Third key point</li>
    </ul>
  </div>

  <!-- Illustrations: use <img> tag, not background-image -->
  <img src="illustration.png" style="position: absolute; right: 60pt; top: 110pt; width: 320pt; height: 240pt;" />

</body>
</html>
```

---

## Common Error Quick Reference

| Error Message | Cause | Fix |
|---------|------|---------|
| `DIV element contains unwrapped text "XXX"` | Bare text in div | Wrap text in `<p>` or `<h1>`-`<h6>` |
| `CSS gradients are not supported` | Used linear/radial-gradient | Change to solid color, or use flex children for segments |
| `Text element <p> has background` | `<p>` tag has background color | Wrap in outer `<div>` for background, `<p>` only has text |
| `Background images on DIV elements are not supported` | Div used background-image | Change to `<img>` tag |
| `HTML content overflows body by Xpt vertically` | Content exceeds 540pt | Reduce content or shrink font size, or `overflow: hidden` to crop |
| `HTML dimensions don't match presentation layout` | Body size doesn't match pres layout | Body use `960pt × 540pt` with `LAYOUT_WIDE`; or defineLayout custom size |
| `Text box "XXX" ends too close to bottom edge` | Large font `<p>` too close to body bottom | Move up, leave enough margin; PPT bottom itself gets covered |

---

## Basic Workflow (3 Steps to PPTX)

### Step 1: Write Each Slide Independent HTML by Constraints

```
MyDeck/
├── slides/
│   ├── 01-cover.html    # Each file is complete 960×540pt HTML
│   ├── 02-agenda.html
│   └── ...
└── illustration/        # All <img> referenced images
    ├── chart1.png
    └── ...
```

### Step 2: Write build.js Calling `html2pptx.js`

```js
const pptxgen = require('pptxgenjs');
const html2pptx = require('../scripts/html2pptx.js');  // This skill's script

(async () => {
  const pres = new pptxgen();
  pres.layout = 'LAYOUT_WIDE';  // 13.333 × 7.5 inch, matches HTML's 960×540pt

  const slides = ['01-cover.html', '02-agenda.html', '03-content.html'];
  for (const file of slides) {
    await html2pptx(`./slides/${file}`, pres);
  }

  await pres.writeFile({ fileName: 'deck.pptx' });
})();
```

### Step 3: Open and Check

- Open exported PPTX in PowerPoint/Keynote
- Double-click any text should be directly editable (if image, 说明 rule 1 violated)
- Verify overflow: each page should be within body bounds, not cropped

---

## This Path vs Other Options (When to Choose What)

| Need | Choose What |
|------|------|
| Colleague will edit PPTX text / send to non-technical to continue editing | **This path** (editable, need write HTML from start following 4 constraints) |
| Just for presentation/archive, no more edits | `export_deck_pdf.mjs` (multi-file) or `export_deck_stage_pdf.mjs` (single-file deck-stage), output vector PDF |
| Visual freedom priority (animations, web components, CSS gradients, complex SVG), accept non-editable | **PDF** (same as above) — PDF preserves fidelity and cross-platform, more suitable than "image PPTX" |

**Never run html2pptx on visually free HTML expecting it to pass** — tested: visually-driven HTML pass rate on html2pptx <30%, remaining pages need改造 slower than rewriting. For such scenarios should output PDF, not force PPTX.

---

## Fallback: Have Visual Draft But User Insists on Editable PPTX

Occasionally encounter this: You/user already have a visually-driven HTML (gradients, web components, complex SVG all used), PDF is most suitable originally, but user clearly says "no, must be editable PPTX".

**Don't hard-run `html2pptx` hoping it passes** — tested: visually-driven HTML on html2pptx pass rate <30%, remaining 70% will error or distort. Correct fallback is:

### Step 1 · State Limitations First (Transparent Communication)

One sentence to user explaining three things:

> "Your current HTML uses [list specifically: gradients / web components / complex SVG / ...], directly converting to editable PPTX will fail. I have two options:
> - A. **Output PDF** (recommended) — 100% visual preserved, recipient can view/print but not edit text
> - B. **Rewrite based on visual draft as blueprint, create editable HTML** (retain color system/layout/copy design decisions, but **sacrifice** gradients/web components/complex SVG etc visual capabilities) → then export editable PPTX
>
> Which do you choose?"

Don't describe B option lightly — explicitly tell **what will be lost**. Let user make the choice.

### Step 2 · If User Chooses B: AI，主动 rewrite, not require user to write themselves

Doctrine here: **User gives design intent, you are responsible for translating to compliant implementation.** Not let user learn 4 constraints then rewrite themselves.

Rewrite principles:
- **Retain**: Color system (primary/secondary/neutral), information hierarchy (title/subtitle/body/notes), core copy, layout skeleton (top-middle-bottom/columns/grid), page rhythm
- **Downgrade**: CSS gradient → solid or flex segments, web component → paragraph-level HTML, complex SVG → simplified `<img>` or solid geometry, shadow → delete or downgrade to very weak, custom font → converge to system fonts
- **Rewrite**: Bare text → wrap in `<p>`/`h*>`, `background-image` → `<img>` tag, background/border on `<p>` → outer div carries

### Step 3 · Output Comparison List (Transparent Delivery)

After rewrite, give user a before/after comparison, let them know which visual details were simplified:

```
Original design → Editable version adjustments
- Title area purple gradient → Primary color #5B3DE8 solid background
- Data card shadow → Deleted (changed to 2pt border for separation)
- Complex SVG line chart → Simplified to <img> PNG (generated from HTML screenshot)
- Hero area web component animation → Static first frame (web component can't translate)
```

### Step 4 · Export & Dual Format Delivery

- `editable` version HTML → run `scripts/export_deck_pptx.mjs` output editable PPTX
- **Recommend also keep** original visual draft → run `scripts/export_deck_pdf.mjs` output high-fidelity PDF
- Dual format delivery to user: visual PDF + editable PPTX, each serves its purpose

### When to Directly Reject B Option

In some scenarios rewrite cost too high, should persuade user to give up editable PPTX:
- HTML core value is animation or interaction (after rewrite only static first frame, info loss 50%+)
- >30 pages, rewrite cost exceeds 2 hours
- Visual design deeply depends on precise SVG/custom filters (after rewrite almost unrelated to original)

Tell user: "This deck rewrite cost too high, recommend PDF not PPTX. If recipient really needs pptx format, accept significant visual simplification — want to switch to PDF?"

---

## Why 4 Constraints Are Not Bugs But Physical Constraints

These 4 are not `html2pptx.js` author being lazy — they are **PowerPoint file format (OOXML) constraints themselves** projected onto HTML:

- In PPTX, text must be in text frame (`<a:txBody>`), corresponds to paragraph-level HTML elements
- In PPTX, shape and text frame are two objects, cannot have background and write text on same element
- PPTX's shape fill has limited gradient support (only certain preset gradients, not CSS arbitrary angle gradients)
- PPTX's picture object must reference real image file, not CSS property

Understanding this, **don't expect tool to get smarter** — HTML writing should adapt to PPTX format, not the other way around.