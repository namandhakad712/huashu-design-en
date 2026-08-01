# Slide Decks: HTML Slide Production Standards

Making slides is a high-frequency design scenario. This document explains how to make good HTML slides — from architecture selection and single-page design to the complete path for PDF/PPTX export.

**This skill's capabilities**:
- **HTML presentation version (base deliverable, always default and required)** → Each slide is an independent HTML file + `assets/deck_index.html` aggregation, keyboard page-turning and fullscreen presentation in the browser
- HTML → PDF export → `scripts/export_deck_pdf.mjs` / `scripts/export_deck_stage_pdf.mjs`
- HTML → Editable PPTX export → `references/editable-pptx.md` + `scripts/html2pptx.js` + `scripts/export_deck_pptx.mjs` (requires HTML written under 4 hard constraints)

> **⚠️ HTML is the foundation; PDF/PPTX are derivatives.** Regardless of the final delivery format, you **must** first build the HTML aggregated presentation (`index.html` + `slides/*.html`) — it is the "source" of the slide work. PDF/PPTX are snapshots exported from the HTML with a single command.
>
> **Why HTML-first**:
> - Best for live presentations (projector / shared screen goes straight to fullscreen, keyboard page-turning, no dependence on Keynote/PPT software)
> - During development, each page can be double-clicked open individually to verify — no need to re-run the export every time
> - It is the only upstream for PDF/PPTX export (avoids the death loop of "discovering the HTML must change after export and re-rendering everything")
> - Deliverables can be a "HTML + PDF" or "HTML + PPTX" double set — recipients use whichever they prefer
>
> 2026-04-22 moxt brochure real-world test: after finishing 13 pages of HTML + the index.html aggregation, `export_deck_pdf.mjs` exported the PDF with one command and zero changes. The HTML version is itself a directly deliverable, browser-presentable artifact.

---

## 🛑 Confirm the delivery format before starting (hardest checkpoint)

**This decision comes before "single file or multi-file".** 2026-04-20 options private board project real-world test: **not confirming the delivery format before starting = 2–3 hours of rework.**

### Decision tree (HTML-first architecture)

All deliveries start from the same set of HTML aggregated pages (`index.html` + `slides/*.html`). The delivery format only decides **the HTML writing constraints** and **the export command**:

```
【Always default · Required】 HTML aggregated presentation (index.html + slides/*.html)
   │
   ├── Browser presentation only / local HTML archive   → Done here, HTML has maximum visual freedom
   │
   ├── Also need PDF (print / send to group / archive)    → Run export_deck_pdf.mjs one-click output
   │                                          HTML writing is free, no visual constraints
   │
   └── Also need editable PPTX (colleague will edit text) → Write HTML under the 4 hard constraints from the first line
                                               Run export_deck_pptx.mjs one-click output
                                               Sacrifices gradients / web components / complex SVG
```

### Opening script (copy and use)

> Whatever the final delivery is — HTML, PDF or PPTX — I will first build an HTML aggregated version that can switch pages and be presented in the browser (`index.html` with keyboard page-turning) — this is the forever-default base deliverable. On top of that, I'll ask whether you also want a PDF/PPTX snapshot.
>
> Which export format do you need?
> - **HTML only** (presentation/archive) → fully free visuals
> - **Also PDF** → same as above, plus one export command
> - **Also editable PPTX** (colleagues will edit text in PPT) → I must write the HTML under the 4 hard constraints from the first line, which sacrifices some visual capabilities (no gradients, no web components, no complex SVG).

### Why "wanting PPTX means following the 4 hard constraints from the start"

The prerequisite for an editable PPTX is that `html2pptx.js` can translate the DOM element by element into PowerPoint objects. It requires **4 hard constraints**:

1. Body fixed at 960pt × 540pt (matches `LAYOUT_WIDE`, 13.333″ × 7.5″, not 1920×1080px)
2. All text wrapped in `<p>`/`<h1>`-`<h6>` (no text directly in a div, no `<span>` carrying main text)
3. `<p>`/`<h*>` themselves cannot have background/border/shadow (put them on an outer div)
4. `<div>` cannot use `background-image` (use the `<img>` tag)
5. No CSS gradients, no web components, no complex SVG decorations

**This skill's default HTML has high visual freedom** — lots of spans, nested flex, complex SVG, web components (such as `<deck-stage>`), CSS gradients — **almost none of it naturally passes the html2pptx constraints** (real-world test: visually-driven HTML fed straight into html2pptx passes at a rate < 30%).

### Cost comparison of the two real paths (real pitfall from 2026-04-20)

| Path | Approach | Result | Cost |
|------|------|------|------|
| ❌ **Write HTML freely first, patch PPTX afterwards** | Single-file deck-stage + lots of SVG/span decoration | Only two roads remain to an editable PPTX:<br>A. Hand-write hundreds of lines of pptxgenjs hardcoded coordinates<br>B. Rewrite the 17 pages of HTML into Path A format | 2–3 hours of rework, and the hand-written version carries **permanent maintenance cost** (every word changed in HTML has to be manually synced into the PPTX again) |
| ✅ **Write under Path A constraints from step one** | Each slide independent HTML + 4 hard constraints + 960×540pt | One command exports a 100% editable PPTX, and it can also be presented fullscreen in the browser (Path A HTML is standard browser-playable HTML) | Spend 5 extra minutes while writing the HTML thinking "how to wrap the text in `<p>`", zero rework |

### What about mixed delivery

If the user says "I want HTML presentation **and** editable PPTX" — **this is not a mix**; the PPTX requirement covers the HTML requirement. HTML written under Path A is itself able to be presented fullscreen in the browser (just add a `deck_index.html` combiner). **No extra cost.**

If the user says "I want PPTX **and** animation / web components" — **this is a genuine contradiction**. Tell the user: an editable PPTX means sacrificing these visual capabilities. Let them make the trade-off; don't secretly hand-write a pptxgenjs solution (it becomes permanent maintenance debt).

### What if you only find out you need PPTX afterwards (emergency recovery)

Rare cases: the HTML is already written when you discover PPTX is needed. Recommended to follow the **fallback process** (full explanation at the end of `references/editable-pptx.md`, "Fallback: existing visual draft but the user insists on an editable PPTX"):

1. **First choice: produce a PDF** (visuals 100% preserved, cross-platform, recipients can view and print) — if what the recipient actually needs is "presentation/archive", PDF is the best deliverable
2. **Second choice: the AI rewrites an editable HTML version based on the visual draft** → export an editable PPTX — preserves the design decisions of color/layout/copy, sacrifices gradients, web components, complex SVG and other visual capabilities
3. **Not recommended: hand-writing a pptxgenjs rebuild** — positions, fonts, and alignment all need manual tuning, maintenance cost is high, and any subsequent word change in the HTML requires another manual sync

Always present the choice to the user and let them decide. **Never start hand-writing pptxgenjs as your first reaction** — that is the last-resort fallback.

---

## 🛑 Before batch production: do a 2-page showcase first to fix the grammar

**As long as the deck is ≥ 5 pages, never write straight from page 1 to the last page.** The correct order validated in the 2026-04-22 moxt brochure real-world build:

1. Pick **the 2 page types with the biggest visual difference** and make a showcase first (e.g., "cover" + "emotion/quote page", or "cover" + "product showcase page")
2. Screenshot and let the user confirm the grammar (masthead / fonts / color / spacing / structure / Chinese-English bilingual ratio)
3. Once the direction is approved, batch out the remaining N−2 pages, each page reusing the established grammar
4. When everything is done, compose the HTML aggregation + PDF/PPTX derivatives together

**Why**: writing all 13 pages straight through → user says "wrong direction" = 13 reworks. A 2-page showcase first → wrong direction = 2 reworks. Once the visual grammar is established, the decision space for the remaining N pages narrows dramatically, leaving only "how to fit the content in".

**Showcase page selection principle**: pick the two pages with the most different visual structures. If those two pass = all the intermediate states pass.

| Deck type | Recommended showcase page combination |
|-----------|---------------------|
| B2B brochure / product promotion | Cover + content page (philosophy/emotion page) |
| Brand launch | Cover + product highlights page |
| Data report | Big-data-visual page + analysis conclusions page |
| Tutorial courseware | Chapter cover page + specific knowledge-point page |

---

## 📐 Publication grammar template (validated reusable in moxt)

Suitable for B2B brochures / product promotion / long-report-style decks. Every page reusing this structure = 13 pages visually identical, 0 rework.

### Per-page skeleton

```
┌─ masthead (top strip + horizontal rule) ────────┐
│  [logo 22-28px] · A Product Brochure                Issue · Date · URL │
├──────────────────────────────────────────┤
│                                          │
│  ── kicker (short green dash + uppercase label)   │
│  CHAPTER XX · SECTION NAME                 │
│                                          │
│  H1 (Chinese Noto Serif SC 900)             │
│  Key words individually in brand primary color                      │
│                                          │
│  English subtitle (Lora italic, subtitle)   │
│  ─────────── divider ──────────            │
│                                          │
│  [specific content: two columns 60/40 / 2x2 grid / list] │
│                                          │
├──────────────────────────────────────────┤
│ section name                     XX / total │
└──────────────────────────────────────────┘
```

### Style conventions (copy directly)

- **H1**: Chinese Noto Serif SC 900, font size 80–140px depending on information volume, key words individually in brand primary color (don't pile color onto the whole line)
- **English subtitle**: Lora italic 26–46px, brand signature words (e.g., "AI team") bold + primary color italic
- **Body**: Noto Serif SC 17–21px, line-height 1.75–1.85
- **Accent highlights**: mark key words in the body with the primary color + bold, no more than 3 per page (too many and they lose their anchor function)
- **Background**: warm cream base #FAFAFA + an extremely faint radial-gradient noise (`rgba(33,33,33,0.015)`) to add a paper feel

### The visual protagonist must be differentiated

If all 13 pages are "text + one screenshot", it gets too monotonous. **Rotate the type of visual protagonist per page**:

| Visual type | Suitable section |
|---------|---------------|
| Cover typography (large type + masthead + pillar) | Home / chapter cover |
| Single-character portrait (e.g., one oversized momo) | Introducing a single concept/character |
| Multi-character group photo / avatar cards side by side | Team / user case studies |
| Timeline cards advancing | Showing "long-term relationship", "evolution" |
| Knowledge graph / connected-node diagram | Showing "collaboration", "flow" |
| Before/After comparison cards + middle arrow | Showing "change", "difference" |
| Product UI screenshot + outlined device frame | Specific feature showcase |
| Large big-quote (half-page large type) | Emotion page / problem page / quote page |
| Real-person avatars + testimonial cards (2×2 or 1×4) | User testimonials / use cases |
| Large-type back cover + URL ellipse button | CTA / ending |

---

## ⚠️ Common pitfalls (moxt real-world summary)

### 1. Emoji doesn't render when exporting via Chromium / Playwright

Chromium doesn't ship with a colored emoji font by default, so during `page.pdf()` or `page.screenshot()` emoji display as empty boxes.

**Countermeasure**: use Unicode text symbols (`✦` `✓` `✕` `→` `·` `—`) instead, or switch to plain text ("Email · 23" rather than "📧 23 emails").

### 2. `export_deck_pdf.mjs` reports `Cannot find package 'playwright'`

Cause: ESM module resolution walks upward from the script's location to find `node_modules`. The script lives at `~/.claude/skills/huashu-design/scripts/`, where there are no dependencies.

**Countermeasure**: copy the script into the deck project directory (e.g., `brochure/build-pdf.mjs`), run `npm install playwright pdf-lib` at the project root, then `node build-pdf.mjs --slides slides --out output/deck.pdf`.

### 3. Screenshot taken before Google Fonts finish loading → Chinese renders as the system default sans

Wait at least `wait-for-timeout=3500` before the Playwright screenshot/PDF so the webfonts can download and paint. Or self-host the fonts in `shared/fonts/` to reduce network dependence.

### 4. Information density imbalance: content pages crammed full

The first version of the moxt philosophy page used 2×2 = 4 paragraphs + 3 credos at the bottom = 7 blocks of content — crowded and repetitive. Switching to 1×3 = 3 paragraphs immediately brought the breathing room back.

**Countermeasure**: keep each page to "1 core message + 3–4 supporting points + 1 visual protagonist"; anything more gets split onto a new page. **Less is more** — a viewer looks at a page for 10 seconds; one memory point is easier to remember than four.

---

## 🛑 Decide the architecture first: single-file or multi-file?

**This choice is the first step of making a slide deck; get it wrong and you'll keep hitting pitfalls. Read this whole section before starting.**

### Comparison of the two architectures

| Dimension | Single file + `deck_stage.js` | **Multi-file + `deck_index.html` combiner** |
|------|--------------------------|--------------------------------------|
| Code structure | One HTML file, all slides are `<section>` | Each page is an independent HTML, `index.html` combines them with iframes |
| CSS scope | ❌ Global, one page's styles can affect all pages | ✅ Naturally isolated, each iframe is its own world |
| Verification granularity | ❌ Need a JS goTo to switch to a page | ✅ Double-click a single page file to view it in the browser |
| Parallel development | ❌ One file, multiple agents editing cause conflicts | ✅ Multiple agents can work on different pages in parallel, zero-conflict merge |
| Debugging difficulty | ❌ One CSS error takes down the whole deck | ✅ A broken page only affects itself |
| Embedded interaction | ✅ Cross-page shared state is simple | 🟡 iframes need postMessage |
| Print to PDF | ✅ Built-in | ✅ Combiner's beforeprint iterates iframes |
| Keyboard navigation | ✅ Built-in | ✅ Combiner built-in |

### Which one to choose? (decision tree)

```
│  Question: roughly how many pages is the deck?
├── ≤10 pages, needs in-deck animation or cross-page interaction, pitch deck → single-file
└── ≥10 pages, academic lecture, courseware, long deck, multi-agent parallel → multi-file (recommended)
```

**Default to the multi-file path.** It is not a "fallback option"; it is the **main path for long decks and team collaboration**. Reason: every advantage of the single-file architecture (keyboard navigation, printing, scale) also exists in multi-file, while multi-file's scope isolation and verifiability are what single-file can't make up for.

### Why is this rule so hard? (real incident record)

The single-file architecture once hit four pitfalls in a row while producing an AI psychology lecture deck:

1. **CSS specificity override**: `.emotion-slide { display: grid }` (specificity 10) crushed `deck-stage > section { display: none }` (specificity 2), causing all pages to render stacked simultaneously.
2. **Shadow DOM slot rules suppressed by outer CSS**: `::slotted(section) { display: none }` couldn't hold off the outer rule's override, so sections refused to hide.
3. **localStorage + hash navigation race**: after a refresh it didn't jump to the hash position but stopped at the old position recorded in localStorage.
4. **High verification cost**: you had to run `page.evaluate(d => d.goTo(n))` to capture a page, twice as slow as directly `goto(file://.../slides/05-X.html)`, and it often errored.

The root cause of all of them is **a single global namespace** — the multi-file architecture eliminates these problems at the physical level.

---

## Path A (default): multi-file architecture

### Directory structure

```
MyDeck/
├── index.html              # copied from assets/deck_index.html, edit the MANIFEST
├── shared/
│   ├── tokens.css          # shared design tokens (palette/font sizes/common chrome)
│   └── fonts.html          # <link> to load Google Fonts (include in every page)
└── slides/
    ├── 01-cover.html       # each file is a complete 1920×1080 HTML page
    ├── 02-agenda.html
    ├── 03-problem.html
    └── ...
```

### Template skeleton for each slide

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>P05 · Chapter Title</title>
<link href="https://fonts.googleapis.com/css2?family=..." rel="stylesheet">
<link rel="stylesheet" href="../shared/tokens.css">
<style>
  /* Styles unique to this page. Any class name won't pollute other pages. */
  body { padding: 120px; }
  .my-thing { ... }
</style>
</head>
<body>
  <!-- 1920×1080 content (locked by the body's width/height in tokens.css) -->
  <div class="page-header">...</div>
  <div>...</div>
  <div class="page-footer">...</div>
</body>
</html>
```

**Key constraints**:
- `<body>` is the canvas; lay out directly on it. Don't wrap it in `<section>` or other wrappers.
- `width: 1920px; height: 1080px` is locked by the `body` rule in `shared/tokens.css`.
- Import `shared/tokens.css` for shared design tokens (palette, font sizes, page-header/footer, etc.).
- Write the font `<link>` on each page yourself (importing fonts separately is cheap and guarantees each page can be opened independently).

### Combiner: `deck_index.html`

**Copy it directly from `assets/deck_index.html`**. You only need to change one thing — the `window.DECK_MANIFEST` array, listing all slide filenames and human-readable labels in order:

```js
window.DECK_MANIFEST = [
  { file: "slides/01-cover.html",    label: "Cover" },
  { file: "slides/02-agenda.html",   label: "Agenda" },
  { file: "slides/03-problem.html",  label: "Problem statement" },
  // ...
];
```

The combiner already has built-in: keyboard navigation (←/→/Home/End/number keys/P for print), scale + letterbox, bottom-right counter, localStorage memory, hash jump-to-page, and print mode (iterates the iframes and outputs a PDF page by page).

#### Two overview modes (adaptive + pitfall-proof, rewritten 2026-06)

Opening the deck defaults to **overview**; when the user hasn't specified, it's randomized by seconds: **grid 60% / infinite gallery 40%** (can be pinned with the URL `?ov=grid|gallery` or `window.DECK_OVERVIEW='grid'|'gallery'`).

- **Grid (default primary)**: renders the **real child pages in iframes** (sharp, what-you-see-is-what-you-get, no thumbnails needed). **Adaptive**: if it all fits on one screen → tilt diagonally and center to fill; if there are too many pages → cards keep a comfortable size with **vertical scrolling** (never cram dozens of pages onto one screen shrunk to postage stamps).
- **Infinite gallery**: all pages **tile seamlessly and infinitely + slow drift + subtle breathing scale**, one tile per page (shuffled layout, repeats only after seeing every page). With many tiles, **you must use `<img>` thumbnails** to carry the performance (see below); when there's no thumb it falls back to iframes.

🛑 **Three hard constraints from real-world use (read before editing this file, or you'll repeat past mistakes)**:
1. **Never use `transform-style: preserve-3d` for the overview wall of cards**. In a preserve-3d scene, the browser's hit-testing for the "cards receding backward" (top row) is unreliable → top row can't be clicked, middle row works intermittently. **Correct approach**: make the whole wall a **single plane tilted in 3D** (no preserve-3d), all cards coplanar, clicks unprojected onto one plane → reliable. Use 2D `scale` for hover, not `translateZ`.
2. **Adaptive for any page count**: fixed column counts + a hard-coded strong tilt for the whole wall → once pages overflow, corners collapse / perspective distorts. Compute the column count from the page count + viewport, flatten the tilt as rows grow, and scroll when one screen can't hold everything.
3. **Don't set thumbnail resolution too low**: gallery thumbnails < 1000px go blurry when zoomed on hover. Default is 1600px.

**Generating thumbnails for the gallery**: use `scripts/gen_deck_thumbs.mjs` (playwright captures each page + sharp downsampling):
```bash
npm install playwright sharp
node gen_deck_thumbs.mjs --slides slides --out thumbs --width 1600
```
Then add `thumb: "thumbs/<same-name>.jpg"` to each MANIFEST entry. Grid mode ignores thumb (always iframe); only gallery mode uses it.

### Per-page verification (the killer advantage of the multi-file architecture)

Every slide is an independent HTML file. **Double-click it in the browser as soon as you finish it**:

```bash
open slides/05-personas.html
```

Playwright screenshots also just `goto(file://.../slides/05-personas.html)` directly — no JS page-jumping needed, and no interference from other pages' CSS. This drives the "change a bit, verify a bit" workflow cost to near zero.

### Parallel development

Split each slide's task across different agents and run them simultaneously — the HTML files are independent of each other, so merges have no conflicts. For long decks, this parallel approach compresses production time to 1/N.

### What belongs in `shared/tokens.css`

Only put in things that are **truly shared across pages**:

- CSS variables (palette, font-size scale, spacing scale)
- Canvas locking like `body { width: 1920px; height: 1080px; }`
- Chrome like `.page-header` / `.page-footer` that every page uses identically

**Don't** cram single-page layout classes in — that degenerates back into the global-pollution problem of the single-file architecture.

---

## Path B (small decks): single file + `deck_stage.js`

For ≤10 pages, cases that need cross-page shared state (e.g., a React tweaks panel controlling all pages), or extremely compact scenarios like a pitch deck demo.

### Basic usage

1. Read the contents from `assets/deck_stage.js` and embed them in the HTML's `<script>` (or `<script src="deck_stage.js">`)
2. Wrap the slides with `<deck-stage>` in the body
3. 🛑 **The script tag must come after `</deck-stage>`** (see the hard constraint below)

```html
<body>

  <deck-stage>
    <section>
      <h1>Slide 1</h1>
    </section>
    <section>
      <h1>Slide 2</h1>
    </section>
  </deck-stage>

  <!-- ✅ Correct: script after deck-stage -->
  <script src="deck_stage.js"></script>

</body>
```

### 🛑 Script position hard constraint (real pitfall from 2026-04-20)

**You can't put `<script src="deck_stage.js">` in the `<head>`.** Even though defining `customElements` in `<head>` works, the parser fires `connectedCallback` the moment it reaches the `<deck-stage>` start tag — at that point the child `<section>`s haven't been parsed yet, so `_collectSlides()` gets an empty array, the counter shows `1 / 0`, and all pages render stacked simultaneously.

**Three compliant forms** (pick any one):

```html
<!-- ✅ Most recommended: script after </deck-stage> -->
</deck-stage>
<script src="deck_stage.js"></script>

<!-- ✅ Also fine: script in head with defer -->
<head><script src="deck_stage.js" defer></script></head>

<!-- ✅ Also fine: module scripts are naturally deferred -->
<head><script src="deck_stage.js" type="module"></script></head>
```

`deck_stage.js` itself already has a built-in `DOMContentLoaded` deferred-collection defense, so even a head script won't completely blow up — but `defer` or placing the script at the bottom of the body is still the cleaner approach, avoiding reliance on the defense branch.

### ⚠️ CSS pitfalls in the single-file architecture (must read)

The most common pitfall of the single-file architecture — **the `display` property gets stolen by per-page styles**.

Common wrong form 1 (writing display: flex directly on a section):

```css
/* ❌ External CSS specificity 2 overrides the shadow DOM's ::slotted(section){display:none} (also 2) */
deck-stage > section {
  display: flex;            /* All pages render stacked simultaneously! */
  flex-direction: column;
  padding: 80px;
  ...
}
```

Common wrong form 2 (a section with a higher-specificity class):

```css
.emotion-slide { display: grid; }   /* specificity: 10, even worse */
```

Both make **all slides render stacked simultaneously** — the counter may show `1 / 10` pretending to be fine, but visually the first page is covering the second, which is covering the third.

### ✅ Starter CSS (copy at the start, no pitfalls)

**The `<section>` itself** only handles "visible/invisible"; **layout (flex/grid, etc.) goes on `.active`**:

```css
/* section only defines non-display common styles */
deck-stage > section {
  background: var(--paper);
  padding: 80px 120px;
  overflow: hidden;
  position: relative;
  /* ⚠️ Don't write display here! */
}

/* Lock "hidden unless active" — specificity + weight double insurance */
deck-stage > section:not(.active) {
  display: none !important;
}

/* Only the active page writes the display + layout it needs */
deck-stage > section.active {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

/* Print mode: all pages must show, overriding :not(.active) */
@media print {
  deck-stage > section { display: flex !important; }
  deck-stage > section:not(.active) { display: flex !important; }
}
```

Alternative: **write the single-page flex/grid on an inner wrapper `<div>`**, with the section itself always just a `display: block/none` switcher. This is the cleanest approach:

```html
<deck-stage>
  <section>
    <div class="slide-content flex-layout">...</div>
  </section>
</deck-stage>
```

### Custom dimensions

```html
<deck-stage width="1080" height="1920">
  <!-- 9:16 vertical -->
</deck-stage>
```

---

## Slide Labels

Both deck_stage and deck_index label every page (shown by the counter). Give them **more meaningful** labels:

**Multi-file**: write `{ file, label: "04 Problem statement" }` in the `MANIFEST`
**Single-file**: add `<section data-screen-label="04 Problem Statement">` to the section

**Key: slide numbering starts at 1, not 0**.

When the user says "slide 5", they mean the 5th slide, never array position `[4]`. Humans don't speak 0-indexed.

---

## Speaker Notes

**Not added by default**, only when the user explicitly asks.

With speaker notes you can reduce the text on the slides to a minimum and focus on impactful visuals — the notes carry the full script.

### Format

**Multi-file**: write it in the `<head>` of `index.html`:

```html
<script type="application/json" id="speaker-notes">
[
  "Script for slide 1...",
  "Script for slide 2...",
  "..."
]
</script>
```

**Single-file**: same position.

### Notes writing essentials

- **Complete**: not an outline, but the actual words to say
- **Conversational**: like everyday speech, not written language
- **Corresponding**: the Nth entry of the array corresponds to the Nth slide
- **Length**: 200-400 characters is best
- **Emotional arc**: mark emphases, pauses, stress points

---

## Slide design patterns

### 1. Establish a system (required)

After exploring the design context, **first state the system you'll use out loud**:

```markdown
Deck system:
- Background colors: at most 2 (90% white + 10% dark section dividers)
- Typography: Instrument Serif for display, Geist Sans for body
- Rhythm: section dividers use full-bleed color + white text, regular slides white background
- Imagery: hero slides use full-bleed photos, data slides use charts

I'll build it according to this system; tell me if anything is wrong.
```

Only continue after the user confirms.

### 2. Common slide layouts

- **Title slide**: solid background + huge title + subtitle + author/date
- **Section divider**: colored background + section number + section title
- **Content slide**: white background + title + 1-3 bullet points
- **Data slide**: title + big chart/number + brief explanation
- **Image slide**: full-bleed photo + small caption at the bottom
- **Quote slide**: whitespace + huge quote + attribution
- **Two-column**: left-right comparison (vs / before-after / problem-solution)

Use at most 4-5 layouts in a deck.

### 3. Scale (emphasized again)

- Body text minimum **24px**, ideal 28-36px
- Titles **60-120px**
- Hero type **180-240px**
- Slides are viewed from 10 meters away; the type needs to be big enough

### 4. Visual rhythm

A deck needs **intentional variety**:

- Color rhythm: mostly white backgrounds + occasional colored section dividers + occasional dark stretches
- Density rhythm: a few text-heavy pages + a few image-heavy pages + a few quote pages with whitespace
- Size rhythm: normal titles + occasional giant hero text

**Don't make every slide look the same** — that's a PPT template, not design.

### 5. Breathing room (must-read for data-dense pages)

**The pitfall beginners trip into most**: stuffing every piece of information you can into one page.

Information density ≠ effective information transfer. Academic/presentation decks especially need restraint:

- List/matrix pages: don't draw all N elements at the same size. Use **hierarchical emphasis** — enlarge the 5 points you're discussing today as protagonists, shrink the remaining 16 into background hints.
- Big-number pages: the number itself is the visual protagonist. Keep the surrounding caption to no more than 3 lines, otherwise the viewer's eyes bounce back and forth.
- Quote pages: leave whitespace between the quote and the attribution; don't glue them together.

Run the two self-audits — "is the data the protagonist?" and "is the text squished together?" — and keep adjusting until the whitespace makes you slightly uneasy.

---

## Print to PDF

**Multi-file**: `deck_index.html` already handles the `beforeprint` event and outputs the PDF page by page.

**Single-file**: `deck_stage.js` handles it too.

The print styles are already written; no extra `@media print` CSS needed.

---

## Export to PPTX / PDF (self-service scripts)

HTML-first is first-class. But users often need PPTX/PDF deliverables. Provide two generic scripts, **usable by any multi-file deck**, located under `scripts/`:

### `export_deck_pdf.mjs` — export vector PDF (multi-file architecture)

```bash
node scripts/export_deck_pdf.mjs --slides <slides-dir> --out deck.pdf
```

**Features**:
- Text stays **vector** (copyable, searchable)
- 100% visual fidelity (rendered by Playwright's embedded Chromium, then printed)
- **No need to change a single word of the HTML**
- Each slide gets its own `page.pdf()`, then merged with `pdf-lib`

**Dependencies**: `npm install playwright pdf-lib`

**Limitation**: a PDF can't have its text edited — to change it, go back to the HTML.

### `export_deck_stage_pdf.mjs` — for single-file deck-stage architecture ⚠️

**When to use**: when the deck is a single HTML file + a `<deck-stage>` web component wrapping N `<section>`s (i.e., Path B architecture). In that case, the "one `page.pdf()` per HTML" approach of `export_deck_pdf.mjs` won't work; use this dedicated script.

```bash
node scripts/export_deck_stage_pdf.mjs --html deck.html --out deck.pdf
```

**Why export_deck_pdf.mjs can't be reused** (real pitfall record from 2026-04-20):

1. **Shadow DOM beats `!important`**: deck-stage's shadow CSS contains `::slotted(section) { display: none }` (only the active slide is `display: block`). Even `@media print { deck-stage > section { display: block !important } }` in the light DOM can't suppress it — once `page.pdf()` triggers the print media, Chromium's final render only shows the active slide, so **the whole PDF is only 1 page** (a repeat of the current active slide).

2. **Looping goto still produces only 1 page**: the intuitive fix "navigate to each `#slide-N`, then `page.pdf({pageRanges:'1'})`" also fails — because once the print CSS outside the shadow DOM (a `deck-stage > section { display: block }` rule) is overridden, the final render is always the first section in the list (not the page you navigated to). Result: 17 loop iterations produce 17 copies of the P01 cover.

3. **Absolutely-positioned children spill to the next page**: even if you succeed in rendering all sections, a section with `position: static` will have its absolutely-positioned `cover-footer`/`slide-footer` positioned relative to the initial containing block — when print forces the section to 1080px tall, the absolute footer can be pushed to the next page (showing up as a PDF with one more page than the number of sections, the extra page containing only the orphaned footer).

**Fix strategy** (already implemented in the script):

```js
// After opening the HTML, use page.evaluate to pull the sections out of the deck-stage slot
// and mount them directly under a plain div in the body, with inline styles ensuring position:relative + fixed dimensions
await page.evaluate(() => {
  const stage = document.querySelector('deck-stage');
  const sections = Array.from(stage.querySelectorAll(':scope > section'));
  document.head.appendChild(Object.assign(document.createElement('style'), {
    textContent: `
      @page { size: 1920px 1080px; margin: 0; }
      html, body { margin: 0 !important; padding: 0 !important; }
      deck-stage { display: none !important; }
    `,
  }));
  const container = document.createElement('div');
  sections.forEach(s => {
    s.style.cssText = 'width:1920px!important;height:1080px!important;display:block!important;position:relative!important;overflow:hidden!important;page-break-after:always!important;break-after:page!important;background:#F7F4EF;margin:0!important;padding:0!important;';
    container.appendChild(s);
  });
  // Disable page-break on the last page to avoid a trailing blank page
  sections[sections.length - 1].style.pageBreakAfter = 'auto';
  sections[sections.length - 1].style.breakAfter = 'auto';
  document.body.appendChild(container);
});

await page.pdf({ width: '1920px', height: '1080px', printBackground: true, preferCSSPageSize: true });
```

**Why this works**:
- Pulling the sections from the shadow DOM slot into a plain light-DOM div completely bypasses the `::slotted(section) { display: none }` rule
- Inline `position: relative` makes absolutely-positioned children position relative to the section, so nothing overflows
- `page-break-after: always` makes the browser put each section on its own page when printing
- `:last-child` without a page-break avoids a trailing blank page

**When validating with `mdls -name kMDItemNumberOfPages`, note**: macOS Spotlight metadata is cached; after rewriting the PDF you need to run `mdimport file.pdf` to force a refresh, otherwise it shows the old page count. Counting files with `pdfinfo` or `pdftoppm` is the true count.

---

### `export_deck_pptx.mjs` — export editable PPTX

```bash
# Only mode: text frames are natively editable (fonts will fall back to system fonts)
node scripts/export_deck_pptx.mjs --slides <dir> --out deck.pptx
```

How it works: `html2pptx` reads computedStyle element by element and translates the DOM into PowerPoint objects (text frame / shape / picture). Text becomes real text frames, double-click editable in PPT.

**Hard constraints** (the HTML must satisfy them, otherwise that page gets skipped; see `references/editable-pptx.md` for details):
- All text must be inside `<p>`/`<h1>`-`<h6>`/`<ul>`/`<ol>` (no bare-text divs)
- The `<p>`/`<h*>` tags themselves can't have background/border/shadow (put them on an outer div)
- Don't use `::before`/`::after` to insert decorative text (pseudo-elements can't be extracted)
- Inline elements (span/em/strong) can't have margin
- No CSS gradients (not renderable)
- Divs don't use `background-image` (use `<img>`)

The script has a built-in **automatic preprocessor** — it auto-wraps "bare text in leaf divs" into `<p>` (preserving classes). This solves the most common violation (bare text). But other violations (border on p, margin on span, etc.) still require compliance at the HTML source.

**Font fallback caveat**:
- Playwright measures text-box sizes with webfonts; PowerPoint/Keynote renders with local fonts
- When the two differ you get **overflow or misalignment** — visually review every page
- Recommend installing the HTML's fonts on the target machine, or falling back to `system-ui`

**Don't take this path for visual-first scenarios** → use `export_deck_pdf.mjs` to produce a PDF instead. PDF is 100% visually faithful, vector, cross-platform, and text-searchable — the true destination for a visual-first deck, not some "non-editable compromise".

### Make the HTML export-friendly from the start

For the most robust deck: **write the HTML under the editable 4 hard constraints from the very beginning**. Then `export_deck_pptx.mjs` passes everything directly. The extra cost is small:

```html
<!-- ❌ Not good -->
<div class="title">Key findings</div>

<!-- ✅ Good (wrapped in p, class inherited) -->
<p class="title">Key findings</p>

<!-- ❌ Not good (border on p) -->
<p class="stat" style="border-left: 3px solid red;">41%</p>

<!-- ✅ Good (border on the outer div) -->
<div class="stat-wrap" style="border-left: 3px solid red;">
  <p class="stat">41%</p>
</div>
```

### When to choose which

| Scenario | Recommended |
|------|------|
| Archiving for organizers / records | **PDF** (universal, high fidelity, searchable text) |
| Sending to collaborators to fine-tune text | **PPTX editable** (accepting font fallback) |
| Live presentation, content not changed | **PDF** (vector fidelity, cross-platform) |
| HTML is the primary presentation medium | Play directly in the browser; export is just a backup |

## Deep path for editable PPTX export (long-lived projects only)

If your deck will be maintained long-term, revised repeatedly, and worked on by a team — recommend **writing the HTML under the html2pptx constraints from the start**, so `export_deck_pptx.mjs` passes everything directly. See `references/editable-pptx.md` (4 hard constraints + HTML template + common-errors quick reference + the fallback process for existing visual drafts).

---

## Frequently asked questions

**Multi-file: a page in the iframe won't open / white screen**
→ Check whether the `file` paths in the `MANIFEST` are correct relative to `index.html`. Use browser DevTools to see whether the iframe's src is directly accessible.

**Multi-file: one page's styles conflict with another page**
→ Impossible (iframe isolation). If it feels like a conflict, that's the cache — Cmd+Shift+R hard refresh.

**Single-file: multiple slides render stacked simultaneously**
→ CSS specificity problem. See the "CSS pitfalls in the single-file architecture" section above.

**Single-file: scaling looks wrong**
→ Check whether all slides hang directly under `<deck-stage>` as `<section>`s. You can't wrap a `<div>` in between.

**Single-file: want to jump to a specific slide**
→ Add a hash to the URL: `index.html#slide-5` jumps to the 5th slide.

**Both architectures: text position is inconsistent across screens**
→ Use fixed dimensions (1920×1080) and `px` units; don't use `vw`/`vh` or `%`. Scaling is handled uniformly.

---

## Verification checklist (must pass after finishing a deck)

1. [ ] Open `index.html` directly in the browser (or the main HTML); check that the first page has no broken images and fonts are loaded
2. [ ] Page through every slide with the → key; no blank pages, no layout misalignment
3. [ ] Press P for print preview; each page is exactly one A4 (or 1920×1080) with nothing cropped
4. [ ] Randomly pick 3 pages, Cmd+Shift+R hard refresh; localStorage memory works correctly
5. [ ] Playwright batch screenshots (multi-page architecture: iterate `slides/*.html`; single-file architecture: switch with goTo), manually eyeball them all
6. [ ] Search for leftover `TODO` / `placeholder` and confirm they're all cleaned up
