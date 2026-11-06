# Visual Draft HTML → Editable PPTX: Read the Rendered Result, Don't Touch the HTML

`references/editable-pptx.md` covers **the html2pptx path**: HTML written to the 4 hard constraints from the
very first line, only then convertible. That document's conclusion — "**never force html2pptx on HTML
already written for visual freedom**, in practice the pass rate is < 30%" — comes with two fallbacks:
produce a PDF, or rewrite an editable HTML.

**This document covers the third path, and it makes that fallback unnecessary.**

The core difference in one sentence: **html2pptx reads the source code; this script reads the coordinates
after the browser has finished rendering.**

Flex, centering, word wrap — the browser has already computed all of it into absolute positions, so
"bare text in a div", "uses flex", "background on a p" aren't problems at all here — to
`getBoundingClientRect` they are all just one rectangle.

---

## Pick the Path First: Choose One of Three

| Situation | Which path | Why |
|---|---|---|
| **HTML not written yet**, you're building the deck from scratch | `scripts/html2pptx.js` (see `editable-pptx.md`) | PPTX written under the 4 constraints comes out with the cleanest structure — text-frame merging and paragraph hierarchy are both friendlier to later editing |
| **HTML already written**, and visually driven (flex / centering / bare text / background images / SVG charts) | **`scripts/pptx_from_rendered.py` (this document)** | Converts as-is, zero refactoring. Rewriting 20 pages of HTML to appease the constraints costs far more than just measuring |
| **The client demands "you must use our template"** | **Only this document's path works** | pptxgenjs creates files from scratch and can't take an existing pptx as the base to inherit its masters; python-pptx can |

⚠️ **Don't mix the two paths in the same project.** Pick one and stay on it to the end, or the two coordinate systems will fight.

---

## Usage

```bash
python3 scripts/pptx_from_rendered.py deck.html -o deck.pptx --selector ".slide"
```

Inheriting the client's official template (the most common commercial-job scenario):

```bash
python3 scripts/pptx_from_rendered.py deck.html -o deck.pptx \
    --selector ".slide" \
    --template 客户官方模板.pptx \
    --layout "内页" \
    --skip-class logo \
    --bg 05070B
```

Dependencies: `playwright` (with chromium), `python-pptx`, `Pillow`.
Adding `--dump-json dom.json` dumps the measured element inventory to disk — very useful when debugging position problems.

---

## Inheriting the Client's Template: Their Master Edits Take Effect Deck-Wide

The most common rework reason on commercial jobs isn't "not good-looking" — it's "**you didn't use our
template**". When the client says that, they usually want two concrete things: ① the logo is the latest
version; ② **when they edit the master, your pages follow along**.

A PPT of one full-page image per slide delivers neither; and even built from text frames, a file created
from scratch by pptxgenjs carries none of their masters. The way to do it is to use their `.pptx` as the base:

1. Open it with `Presentation(客户模板.pptx)`
2. **Delete the template's own sample slides**, leaving master / layouts / theme / palette each untouched (`strip_slides`)
3. Each page: `add_slide(official layout)`, and remove the empty placeholders the layout drops onto the slide
4. **Don't draw shared elements like logos into the content layer** — let the layouts provide them. At render
   time, `--skip-class logo` skips that logo in the HTML, so the slide holds only your content and the logo
   comes from the layout. This way, when the client edits the master/layout, every page follows at once.

⚠️ **Pitfall: the layout may hide a solid rectangle covering the full screen**, same color and same size as
the layout background (a redundant mask). Leave it there, and anything placed below it on the slide gets
covered. The script's `unblock_layout` deletes it; deleting it doesn't change the layout's appearance.

**Canvas size follows the template, not `editable-pptx.md`'s 960×540pt.** However big the client template is,
that's what you use (26.67×15 inch seen in practice); with mismatched sizes, merging files rescales the whole
thing. The script automatically computes the scale as `slide width pt ÷ HTML canvas width px`; with a 1920px
HTML canvas paired with 1920pt the ratio is exactly 1.0, **1 CSS px = 1 PowerPoint pt** — you don't even
need to do the arithmetic in your head.

---

## Six Typesetting Traps (Every One of Them Has Caused a Real Failure)

None of these are covered in `editable-pptx.md`, because that document assumes the HTML was freshly written
to the constraints. When reading rendered results, every one of the below crashes the export outright if
left unhandled:

### 1. Newlines and Indentation in the HTML Source Become Real Line Breaks in the PPTX

```html
<div>
    <em>68</em>
    <span>个项目，我装了每天的数据采集</span>
</div>
```

The newlines and indentation between tags are **real text nodes**. The browser collapses them under
`white-space: normal` (consecutive whitespace → one space, leading and trailing dropped); PPTX has no such
rule — that `\n` gets carried over as-is, becomes a real line break in PowerPoint, and pushes everything
after it onto the next line, on top of other elements.

**Fix**: do the HTML whitespace collapsing at extraction time, and drop runs that end up empty after collapsing.

### 2. A Container's font-size Is Usually Inherited — Don't Compute Margins or Line Spacing From It

That div's `computedStyle.fontSize` may be a mere 16px (inherited from body) while it holds a 132px number
inside. Compute the text frame's margins and line spacing from 16px and everything comes out wrong.

**Fix**: take the **largest** font size among the `runs` as the base size.

### 3. Counting Lines: You Can't Deduplicate Rectangles by Their top

`Range.getClientRects()` returns multiple rectangles for runs of different font sizes sitting in the same
line — they're baseline-aligned, but their top edges are far apart. Deduplicate by `top`, and one line gets
counted as several (one line counted as 4, in practice).

**Fix**: cluster by whether the y-ranges overlap.

### 4. Different Font Sizes in One Frame Can't All Take the Same Line Spacing

PowerPoint's line spacing is **paragraph-level**, while visual drafts routinely put lines of different font
sizes into the same div:

```html
<div>我投入最多的那个<br>做了一周多，四万行代码<br><em class="big">没跑出来</em></div>
```

Apply one line spacing to the whole frame, and the small-type lines get stretched while the big-type line
gets crushed — in practice, two adjacent lines end up stacked directly on top of each other.

**Fix**: **split on `<br>`, each segment becomes its own text frame**, with its own position and line
height. The number of text frames grows (137 → 175, measured in practice), but that's the necessary price
of correctness.

### 5. Flex Shrink-Wrapped Frames Have Zero Slack — the Last Character Drops to a New Line

A flex child under `align-items: center` shrinks its width down to the text's actual width — **not a bit of
slack to spare**. Move that into PowerPoint, and the slightest difference in font metrics squeezes the last
character onto the next line (in practice, the 了 of "⋯⋯被用起来了" and the 力 of "稀缺的是判断力" have
both dropped).

**Fix**: measure whether that run actually wrapped in the HTML; for the ones that were single-line to begin
with, **turn word wrap off outright** in the PPT (`word_wrap = False`) — wrapping becomes impossible at the
root. Measured in practice: 150 of the 175 frames were this kind.

### 6. Don't Set Exact Line Spacing on Single-Line Paragraphs

The measured line-box height is larger than the actual line gap (that's the **font's line box**, not CSS
line spacing; 185 vs 148, measured in practice). Use it as exact line spacing, and the text gets pushed down
as a whole.

**Fix**: set line spacing only on paragraphs that wrapped on their own; leave single-line paragraphs to
PowerPoint's natural font-size layout — the text hugs the top of the frame, and the position actually comes
out the most accurate.

---

## 🔴 Verification: Verify Your Verification Tool First

**This is the biggest lesson on this path — worth more than all the technical detail above.**

The same PPTX can come out completely different from different renderers. With the wrong tool, none of traps
1, 3, 4, and 6 above **ever surfaces** — all 20 pages look right, the client opens it, and things overlap.

| Tool | Can it be trusted | Notes |
|---|---|---|
| **macOS `qlmanage -t` thumbnails** | ❌ **No** | Takes a simplified rendering path, far more forgiving about line spacing than real PowerPoint. In practice it let 4 text-overlap bugs through |
| **LibreOffice (macOS)** | ⚠️ Layout trustworthy, Chinese may vanish entirely | It can't get at macOS's system Chinese fonts and renders tofu blocks, even blanks |
| **Keynote + AppleScript** | ✅ **First pick for automation** | Real presentation-engine typesetting; scriptable to export a PDF, then rasterize page by page |
| **Opening in WPS / PowerPoint** | ✅ **Final confirmation** | The client mostly uses one of these. Human review |

**Keynote automation (the only route on this machine that is both fully automatic and trustworthy)**:

```bash
osascript <<'EOF'
tell application "Keynote"
  activate
  set d to open POSIX file "/abs/path/deck.pptx"
  delay 4
  export d to POSIX file "/abs/path/out.pdf" as PDF
  close d saving no
  quit
end tell
EOF
pdftoppm -png -r 54 out.pdf page     # then compare page by page, side by side, with the original HTML
```

**To judge whether a renderer can be trusted, run a controlled experiment**: feed the **client's original
template** to the same renderer. If Chinese also vanishes when it renders the official template, the problem
is the environment, not your file — this one step can save hours of debugging in the wrong direction.

⚠️ **Don't use System Events to inject keystrokes for page-flipping screenshots.** The keystrokes land in
whatever window the user is typing in right now.

**Also run the mechanical checks** (they depend on no renderer):

- Lost-text check: **runs automatically by default after the script exports** (`verify_text()`); compares
  the page's rendered `innerText` against the text inside the pptx, page by page (whitespace stripped,
  case-insensitive), and if anything is missing prints "⚠️ 丢字校验" plus the missing fragments. It's on by
  default because lost text is silent — it raises no error, and a check that depends on a human remembering
  to run it is no check at all
- Count comparison: image counts and shape counts aligned page by page

**The comparison source must be independent of the extraction logic — never compare against the
`--dump-json` inventory.** The inventory and the pptx both come from the same DOM extraction: any text the
extraction stage missed (mixed content of "`<svg>` + bare text" inside one element once went missing
wholesale) is absent from both sides, so the comparison necessarily passes — the verification tool and the
thing being verified share the same blind spot. `innerText` is the text the browser itself rendered (already
including `text-transform`); it never passes through any extraction code, which is exactly why it can see
what extraction missed.
Exclusions: elements skipped by `--skip-class` get reported missing (expected); text inside svg/canvas is
exported as image and already excluded from the comparison.

---

## Fonts: Delivery Font ≠ Layout Font

Client brand specs often specify a font you don't have on your machine (Microsoft YaHei, for instance — a
commercial font licensed with Windows). **Don't rewrite the HTML's `font-family` for its sake** — it isn't
installed locally, previews and PDFs will fall back, and **the layout shifts on the spot** (in practice, a
whole row of digits got pushed onto the next line).

The right approach is **splitting the two sides**:

- HTML / PDF typeset in a font actually installed on your machine — what you see is what you get
- The PPTX carries the font name the client's spec dictates (their machines have it)

**What makes the split safe is CJK full-width characters being monospace** — swapping the font doesn't
change the character count per line or the wrap positions; the differences live only in Latin text and
punctuation. Chinese-dominant decks can split with confidence; Latin-dominant decks need separate
verification.
