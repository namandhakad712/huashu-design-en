# Editable PPTX Export: HTML Hard Constraints + Size Decisions + Common Errors

This document covers the path of using `scripts/html2pptx.js` + `pptxgenjs` to translate HTML element-by-element into truly editable PowerPoint text boxes — the only path supported by `export_deck_pptx.mjs`.

> **Core prerequisite**: To follow this path, the HTML must be written with the following 4 constraints from the very first line. **Not "convert after writing"** — retroactive fixes trigger 2-3 hours of rework (burned in practice on the 2026-04-20 Options Private Board Meeting project).
>
> For scenarios that prioritize visual freedom (animations / web components / CSS gradients / complex SVG), switch to the PDF path instead (`export_deck_pdf.mjs` / `export_deck_stage_pdf.mjs`), and **don't** expect the PPTX export to combine visual fidelity with editability — this is a physical constraint of the PPTX file format itself (see "Why the 4 Constraints Are Not Bugs But Physical Constraints" at the end).

---

## Canvas Size: Use 960×540pt (LAYOUT_WIDE)

PPTX units are **inches** (physical size), not px. Decision principle: the body's computedStyle size must **match the presentation layout's inch size** (±0.1", enforced by `html2pptx.js`'s `validateDimensions`).

### 3 Candidate Size Comparison

| HTML body | Physical size | Corresponding PPT layout | When to choose |
|---|---|---|---|
| **`960pt × 540pt`** | **13.333″ × 7.5″** | **pptxgenjs `LAYOUT_WIDE`** | ✅ **Default recommended** (standard on modern PowerPoint 16:9) |
| `720pt × 405pt` | 10″ × 5.625″ | Custom | Only when the user specifies a "legacy PowerPoint Widescreen" template |
| `1920px × 1080px` | 20″ × 11.25″ | Custom | ❌ Non-standard size, fonts look abnormally small when projected |

**Don't think of HTML size as resolution.** PPTX is a vector document; the body size determines **physical size**, not clarity. An oversized body (20″×11.25″) won't make text clearer — it only makes the pt font size smaller relative to the canvas, which actually looks worse when projected or printed.

### Body: One of Three Equivalent Ways

```css
body { width: 960pt;  height: 540pt; }    /* clearest, recommended */
body { width: 1280px; height: 720px; }    /* equivalent, px habit */
body { width: 13.333in; height: 7.5in; }  /* equivalent, inches intuition */
```

Matching pptxgenjs code:

```js
const pptx = new pptxgen();
pptx.layout = 'LAYOUT_WIDE';  // 13.333 × 7.5 inch, no custom definition needed
```

---

## 4 Hard Constraints (Violations Error Immediately)

`html2pptx.js` translates the HTML DOM element-by-element into PowerPoint objects. PowerPoint's format constraints projected onto HTML = the 4 rules below.

### Rule 1: No Direct Text Inside a DIV — Must Be Wrapped in `<p>` or `<h1>`-`<h6>`

```html
<!-- ❌ Wrong: text directly in a div -->
<div class="title">Q3 revenue up 23%</div>

<!-- ✅ Correct: text in <p> or <h1>-<h6> -->
<div class="title"><h1>Q3 revenue up 23%</h1></div>
<div class="body"><p>New users are the main driver</p></div>
```

**Why**: PowerPoint text must exist inside a text frame, and a text frame corresponds to paragraph-level HTML elements (p/h*/li). A bare `<div>` has no corresponding text container in PPTX.

**Nor can `<span>` carry the primary text** — span is an inline element and can't be independently aligned as a text box. Span can only be **sandwiched inside p/h\*** for local styling (bold, color change).

### Rule 2: No CSS Gradients — Solid Colors Only

```css
/* ❌ Wrong */
background: linear-gradient(to right, #FF6B6B, #4ECDC4);

/* ✅ Correct: solid color */
background: #FF6B6B;

/* ✅ If multi-color stripes are required, use flex children each with a solid color */
.stripe-bar { display: flex; }
.stripe-bar div { flex: 1; }
.red   { background: #FF6B6B; }
.teal  { background: #4ECDC4; }
```

**Why**: PowerPoint's shape fill supports only solid/gradient-fill, but pptxgenjs's `fill: { color: ... }` maps only to solid. Using PowerPoint's native gradient requires writing separate structures, which the current toolchain doesn't support.

### Rule 3: Background/Border/Shadow Only on DIV, Not on Text Tags

```html
<!-- ❌ Wrong: <p> has a background -->
<p style="background: #FFD700; border-radius: 4px;">Key content</p>

<!-- ✅ Correct: the outer div carries the background/border, <p> only handles text -->
<div style="background: #FFD700; border-radius: 4px; padding: 8pt 12pt;">
  <p>Key content</p>
</div>
```

**Why**: In PowerPoint, a shape (box/rounded rectangle) and a text frame are two separate objects. HTML's `<p>` translates only to a text frame; background/border/shadow belong to the shape — they must be written on the **div wrapping the text**.

### Rule 4: DIV Cannot Use `background-image` — Use an `<img>` Tag

```html
<!-- ❌ Wrong -->
<div style="background-image: url('chart.png')"></div>

<!-- ✅ Correct -->
<img src="chart.png" style="position: absolute; left: 50%; top: 20%; width: 300pt; height: 200pt;" />
```

**Why**: `html2pptx.js` only extracts image paths from `<img>` elements; it doesn't parse `background-image` URLs in CSS.

---

## Merged Text Boxes (`data-pptx-merge`)

**Default behavior**: every `<p>`/`<h1>`-`<h6>` in the HTML becomes an **independent text box** in PPTX. Write 3 `<p>`s in a card → 3 text boxes stacked in the PPT; while editing you can't press Enter to add a new paragraph within a block, and you have to adjust font size/alignment box by box.

**Solution**: add `data-pptx-merge="true"` to the outer div, and all `<p>/<h*>` inside the container merge into **one editable text box**, separated by paragraph breaks — in PowerPoint you keep editing paragraph by paragraph.

```html
<!-- ✅ Merged: all 4 paragraphs live in a single text box -->
<div class="card" data-pptx-merge="true"
     style="position: absolute; top: 60pt; left: 60pt; width: 420pt;
            background: #1A4A8A; border-radius: 8pt; padding: 20pt 24pt;">
  <h2 style="font-size: 24pt; color: #FFFFFF;">Title</h2>
  <p  style="font-size: 14pt; color: #DDEEFF;">First paragraph body text.</p>
  <p  style="font-size: 14pt; color: #FFD166;">Second paragraph: color change as emphasis.</p>
  <p  style="font-size: 14pt; color: #DDEEFF;">Third paragraph: keep writing in the same text box.</p>
</div>
```

**Styles retained** (written per-paragraph as run options): `font-size`, `color`, `font-family`, `font-weight` (bold), `font-style` (italic), `text-decoration: underline`, and inline styles from `<b>/<i>/<u>/<strong>/<em>/<span>`.

**Taken from the first paragraph, applied uniformly to the whole box**: `text-align`, `line-height`. Because PowerPoint's alignment and line spacing are paragraph/textbox-level — a box can only have one alignment. If paragraphs have different alignments, don't use merge; let them stay independent.

**The container's own `background`/`border`/`box-shadow`/`border-radius`** still render as a shape, behaving exactly like a normal div — in other words, the blue card background + text remains a "shape + text frame" two-layer structure; only the text layer collapses from 3-4 text boxes into 1.

**Limitations**:
- `data-pptx-merge` can't be nested (it will error).
- The container can't use `background-image` (same as hard constraint Rule 4).
- Don't put child divs with `background`/`border` inside the container — they'll still render as independent shapes, but their text has already been merged away, which can cause visual misalignment.

**When to use**: scenarios where content will be revised repeatedly and you'll keep editing in PowerPoint. For one-time export-and-archive, no need to add it; behavior stays the same.

---

## Path A HTML Template Skeleton

Each slide is a standalone HTML file, scopes isolated (avoiding the CSS pollution of a single-file deck).

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body {
    width: 960pt; height: 540pt;           /* ⚠️ Match LAYOUT_WIDE */
    font-family: system-ui, -apple-system, "PingFang SC", sans-serif;
    background: #FEFEF9;                    /* solid color, no gradients */
    overflow: hidden;
  }
  /* DIV handles layout/background/border */
  .card {
    position: absolute;
    background: #1A4A8A;                    /* background on the DIV */
    border-radius: 4pt;
    padding: 12pt 16pt;
  }
  /* Text tags only handle font styles, no background/border */
  .card h2 { font-size: 24pt; color: #FFFFFF; font-weight: 700; }
  .card p  { font-size: 14pt; color: rgba(255,255,255,0.85); }
</style>
</head>
<body>

  <!-- Title area: the outer div positions, the inner text tags write -->
  <div style="position: absolute; top: 40pt; left: 60pt; right: 60pt;">
    <h1 style="font-size: 36pt; color: #1A1A1A; font-weight: 700;">Titles should be assertive sentences, not topics</h1>
    <p style="font-size: 16pt; color: #555555; margin-top: 10pt;">Subtitle adds supplementary explanation</p>
  </div>

  <!-- Content card: div handles the background, h2/p handle the text -->
  <div class="card" style="top: 130pt; left: 60pt; width: 240pt; height: 160pt;">
    <h2>Key Point One</h2>
    <p>Brief description text</p>
  </div>

  <!-- List: use ul/li, no manual • symbols -->
  <div style="position: absolute; top: 320pt; left: 60pt; width: 540pt;">
    <ul style="font-size: 16pt; color: #1A1A1A; padding-left: 24pt; list-style: disc;">
      <li>First key point</li>
      <li>Second key point</li>
      <li>Third key point</li>
    </ul>
  </div>

  <!-- Illustration: use an <img> tag, not background-image -->
  <img src="illustration.png" style="position: absolute; right: 60pt; top: 110pt; width: 320pt; height: 240pt;" />

</body>
</html>
```

---

## Common Error Quick Reference

| Error message | Cause | Fix |
|---------|------|---------|
| `DIV element contains unwrapped text "XXX"` | Bare text in a div | Wrap the text in `<p>` or `<h1>`-`<h6>` |
| `CSS gradients are not supported` | Used linear/radial-gradient | Switch to a solid color, or use flex children for segments |
| `Text element <p> has background` | `<p>` tag has a background color | Wrap it in an outer `<div>` to carry the background; `<p>` only holds text |
| `Background images on DIV elements are not supported` | Div uses background-image | Switch to an `<img>` tag |
| `HTML content overflows body by Xpt vertically` | Content exceeds 540pt | Reduce content or font size, or use `overflow: hidden` to crop |
| `HTML dimensions don't match presentation layout` | Body size doesn't match the presentation layout | Use `960pt × 540pt` for body with `LAYOUT_WIDE`; or defineLayout for a custom size |
| `Text box "XXX" ends too close to bottom edge` | Large-font `<p>` less than 0.5 inch from the body's bottom edge | Move it up, leave enough bottom margin; the bottom of the PPT is partially covered anyway |

---

## Basic Workflow (3 Steps to PPTX)

### Step 1: Write Each Slide as Standalone HTML Following the Constraints

```
My Deck/
├── slides/
│   ├── 01-cover.html    # each file is a complete 960×540pt HTML
│   ├── 02-agenda.html
│   └── ...
└── illustration/        # images referenced by all <img> tags
    ├── chart1.png
    └── ...
```

### Step 2: Write build.js Calling `html2pptx.js`

```js
const pptxgen = require('pptxgenjs');
const html2pptx = require('../scripts/html2pptx.js');  // script from this skill

(async () => {
  const pres = new pptxgen();
  pres.layout = 'LAYOUT_WIDE';  // 13.333 × 7.5 inch, matches the HTML's 960×540pt

  const slides = ['01-cover.html', '02-agenda.html', '03-content.html'];
  for (const file of slides) {
    await html2pptx(`./slides/${file}`, pres);
  }

  await pres.writeFile({ fileName: 'deck.pptx' });
})();
```

### Step 3: Open and Check

- Open the exported PPTX in PowerPoint/Keynote
- Double-click any text — it should be directly editable (if it renders as an image, rule 1 was violated)
- Verify overflow: every page should stay within the body bounds, nothing cropped

---

## This Path vs Other Options (When to Choose What)

| Need | Choose |
|------|------|
| A colleague will edit the text in the PPTX / hand off to non-technical people to keep editing | **This path** (editable; requires writing the HTML from scratch following the 4 constraints) |
| Presentation-only / send for archive, no more edits | `export_deck_pdf.mjs` (multi-file) or `export_deck_stage_pdf.mjs` (single-file deck-stage), produces vector PDF |
| Visual freedom first (animations, web components, CSS gradients, complex SVG), accepting non-editability | **PDF** (same as above) — PDF is both faithful and cross-platform, more suitable than an "image PPTX" |

**Never force html2pptx on HTML already written for visual freedom** — in practice, visually-driven HTML has a pass rate of < 30%, and retrofitting the remaining pages one by one is slower than rewriting. Such scenarios should produce a PDF, not a forced PPTX.

---

## Fallback: A Visual Draft Already Exists But the User Insists on Editable PPTX

Occasionally you'll hit this scenario: you/the user have already written a visually-driven HTML (gradients, web components, complex SVG all in use), where producing a PDF would have been most appropriate, but the user explicitly says "no, it must be an editable PPTX".

**Don't hard-run `html2pptx` expecting it to pass** — in practice, visually-driven HTML has a pass rate of < 30% on html2pptx; the remaining 70% will error or render incorrectly. The correct fallback is:

### Step 1 · State the Limitations First (Transparent Communication)

In one breath, tell the user three things:

> "Your current HTML uses [list specifically: gradients / web components / complex SVG / ...], so converting directly to an editable PPTX will fail. I have two options:
> - A. **Output a PDF** (recommended) — 100% of the visuals preserved; the recipient can view and print but not edit text
> - B. **Rewrite an editable HTML using the visual draft as the blueprint** (keep the color/layout/copy design decisions, but reorganize the HTML structure per the 4 hard constraints, **sacrificing** visual capabilities such as gradients, web components, and complex SVG) → then export an editable PPTX
>
> Which one would you like?"

Don't talk about Option B as if it's no big deal — explicitly state **what will be lost**. Let the user make the trade-off.

### Step 2 · If the User Chooses B: The AI Rewrites Proactively, Not the User

The doctrine here: **the user provides design intent; you're responsible for translating it into a compliant implementation**. It's not about having the user learn the 4 hard constraints and rewrite it themselves.

Principles to follow when rewriting:
- **Retain**: color system (primary/secondary/neutral), information hierarchy (title/subtitle/body/annotation), core copy, layout skeleton (top-middle-bottom / left-right columns / grid), page rhythm
- **Downgrade**: CSS gradient → solid color or flex segments, web component → paragraph-level HTML, complex SVG → simplified `<img>` or solid-color geometry, shadows → removed or reduced to nearly nothing, custom fonts → aligned toward system fonts
- **Rewrite**: bare text → wrapped in `<p>` / `<h*>`, `background-image` → `<img>` tag, background/border on `<p>` → carried by the outer div

### Step 3 · Produce a Comparison Checklist (Transparent Delivery)

After the rewrite, give the user a before/after comparison so they know which visual details were simplified:

```
Original design → Editable version adjustments
- Title area purple gradient → primary color #5B3DE8 solid background
- Data card shadow → removed (changed to a 2pt border for separation)
- Complex SVG line chart → simplified to an <img> PNG (generated from an HTML screenshot)
- Hero area web component animation → static first frame (web components can't be translated)
```

### Step 4 · Export & Deliver in Both Formats

- `editable` HTML → run `scripts/export_deck_pptx.mjs` to produce the editable PPTX
- **Also recommend keeping** the original visual draft → run `scripts/export_deck_pdf.mjs` to produce a high-fidelity PDF
- Deliver both formats to the user: the visual draft's PDF + the editable PPTX, each serving its own purpose

### When to Outright Reject Option B

In certain scenarios the rewrite cost is too high, and you should persuade the user to give up the editable PPTX:
- The HTML's core value is animation or interactivity (after rewriting, only a static first frame remains; 50%+ of the information is lost)
- More than 30 pages, and the rewrite cost exceeds 2 hours
- The visual design deeply depends on precise SVG / custom filters (after rewriting, it's almost unrelated to the original)

At that point tell the user: "This deck's rewrite cost is too high; I recommend producing a PDF rather than a PPTX. If the recipient truly needs the pptx format, accept that the visuals will be significantly simplified — want to switch to PDF?"

---

## Why the 4 Constraints Are Not Bugs But Physical Constraints

These 4 constraints aren't the `html2pptx.js` author being lazy — they are **the constraints of the PowerPoint file format (OOXML) itself** projected onto HTML:

- In PPTX, text must live in a text frame (`<a:txBody>`), corresponding to paragraph-level HTML elements
- In PPTX, a shape and a text frame are two separate objects; you can't draw a background and write text on the same element
- PPTX shape fills have limited gradient support (only certain preset gradients; arbitrary-angle CSS gradients are not supported)
- A PPTX picture object must reference a real image file, not a CSS property

Once you understand this, **don't expect the tool to get smarter** — it's the HTML that must adapt to the PPTX format, not the other way around.
