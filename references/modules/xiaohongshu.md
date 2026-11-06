# Module · Xiaohongshu Image-Text Posts / Covers / Carousels

A set of roughly 3:4 vertical images read by swiping sideways on Xiaohongshu — this also covers making just a single cover (the head image). The first image crowds in with everyone else's covers in the two-column feed and decides whether anyone taps open; each image after it is one page. Cross SKILL.md's narrow bridge first, then follow this manual. A single tall vertical image with data as the protagonist goes to `infographic.md`.

## Specs

- Canvas 1242×1660 (the near-3:4 Xiaohongshu commonly uses; exact 3:4 is 1080×1440, also fine, with type sizes converted proportionally). At most 18 images per post.
- Type-size floors (1242-wide canvas): body text ≥42px, labels ≥32px — equivalent to 36/28 at 1080 wide. A cover title gets only about one-third of a screen's width in the feed, so it needs ≥100px and must finish within two lines.
- Platform limits get written into the design: no external links, QR codes, WeChat IDs, or emails in the images; to point people somewhere, write "search xxx on GitHub" or "drop a comment below"; no absolute claims like "the best", "No. 1 in the industry", "the only one" (ordinals such as "step one" or "my first webpage" don't count; the user's verbatim "the best money I ever spent" becomes a concrete phrasing like "worth every penny"); when AI-generated imagery is used, make the content disclosure the platform requires at posting time; for CC BY-type images, write the author and license on the image or at the end of the post body.

## Pick the Paradigm First (what the three-direction gate looks like here)

Three directions = three paradigms, each producing "cover + the one hardest inner page", presented to the user side by side via `xhs_render.py`'s sheet.jpg; when the job is a single cover, each direction produces one cover. The six candidates are conceived per `directions.md`, with the seconds roulette drawing from these 8 paradigms; the three finally picked must land on three different paradigms. The paradigm pool is the "Xiaohongshu Image-Text (8)" section of `design-styles.md`, overview at `assets/style-specimens/sheet-xhs.jpg`.

| Content | Think first of |
|---|---|
| Your own product, something people should recognize as yours at a glance | 02 Product Notebook (borrows the product UI's paper, controls, and assets) |
| Content that lines up in a row: a set of objects, a timeline, a pipeline | 04 Panorama Strip (several images join into one) |
| Nature, knowledge, and culture long-form writing that needs authority and a magazine feel | 01 Specimen Journal |
| Numeric conclusions, rankings, lists | 03 Index Ink, 08 Area Infographic |
| "Events" like a launch, a retrospective, a method write-up | 05 Daily Paper |
| One item per card, collectible: species, products, people, tools | 06 Trading Cards |
| Slow content, stories, a close-up on a single object | 07 Blank & Vertical |

A paradigm gives you a skeleton and nothing more. Colors are taken from the content or the brand via the color derivation protocol; materials are the user's own real things (`references/materials.md`); the three directions' skeletons must differ.

## Start From the Template

The eight specimens double as templates: copy `$HD/assets/style-specimens/xhs/<number>.html` together with `_kit/xhs.css` and `_kit/xhs.js` into the project (put them under the project's own `_kit/` and the paths need no editing), then change the copy, swap the images, and edit the colors in `:root`. Opened in a browser window at 1200×750 it's the side-by-side specimen view; at any other width it lays out at true size.

- One page per `<section class="xhs-page">`; a continuous panorama strip uses `<section class="xhs-strip" style="--n:3">`, width 1242×N.
- `_kit/xhs.js`: `XHS.number(total)` writes the page numbers (add `data-pageno="off"` on the cover); `XHS.wire()` draws one line that runs continuously across the images, `XHS.perch()` stands an object on the line, `XHS.straddle()` straddles an object across a given seam.
- `_kit/stickers/` and `birds.js` are the demo bird stickers, licensed PolyForm Shield — different from this repo's MIT: wherever the templates reference them, swap in the user's own images and data, and don't carry them into the project.
- The templates pull Google Fonts externally, with system-font fallbacks in the font stacks; offline, deleting the `<link>` still lays out fine — only the letterforms change, so give it one look before rendering.

## Laying Out a Set

- Cover: one hook (a number, a conclusion, or a contrast) + one hero visual, with a title of eight to fourteen characters. Don't cram a table of contents into the cover.
- The second image answers "what is this"; each middle image tells exactly one thing, one headline to one picture; the last image lands on the next step (where to find it, how to use it, what to say in the comments).
- The whole set is one system: the same headers, page numbers, colors, and fonts; adjacent images rotate composition (big image, list, numbers, comparison, taking turns).
- Panorama strip: the protagonist straddles the seam (about 2/3 showing on the left image, about 1/3 on the right), clicking into place only when swiped right; every image still needs a title and must hold up on its own; continuous lines and horizons are drawn by one shared function — don't draw a separate segment per image.

## Rendering and Design Check

```bash
# $HD = this skill's root directory (the one containing SKILL.md), not the user's project directory
python3 "$HD/scripts/xhs_render.py" note.html --out images/ --jpg
```

The script outputs `01.png`… page by page, auto-slices the panorama strip, then assembles one `sheet.jpg`. It checks: type below the floors, text escaping the page, text crossing a panorama seam, two text blocks pressed together (those four are ✗, exit code 1); text covered by an image or a color block, or text squeezed against a small color block, are !: fix it, or write in the delivery notes why it stays. Deliberately overlapped elements get `data-overlap-ok`. The general design check still runs — for the vertical format, give the full viewport: `design_lint.py check … --viewport 1242x1660 --min-body 42 --min-label 32` (`compare` and `ledger check` also take `--viewport 1242x1660`); long labels like credits and captions only count as labels when their class name carries `caption` or `credit`. No ✗ doesn't mean deliverable — the script can't see layout collapse (a grid squeezed into one column, a chart that never drew): open each full-size png and look, then look at sheet.jpg — an orphan word on a title's last line, bottom-of-page components colliding with the page number, one-line body text that slipped past on the label floor, whether the whole set's rhythm is the same on every image.

## Pitfalls Hit in Practice

- High-contrast serifs like Bodoni lose their thin strokes below 100px on phones — "4" reads as "1". Switch small numbers to a Song serif or a sans. The cover shrinks to about one-third again inside the feed, so high-contrast numbers on covers are sized as ≥200px.
- Cards and number bars at the bottom of a page collide most easily with the page number and footer — check the last image especially.
- Specimen mode scales the whole page, so measure widths with `offsetWidth` in scripts, never `getBoundingClientRect()` — otherwise the panorama strip's line draws only a third of itself.
- Don't use `top` or `name` as variable names in page scripts — they collide with browser globals and blank out a whole block without a single error.
- If a small cell can't fit 32px text, merge it into "the remaining N" or keep the image only — don't shrink the text to cram it in.

## Related Files

| Want | Read |
|---|---|
| The eight paradigms explained, with specimens | `references/design-styles.md`'s "Xiaohongshu Image-Text" + `assets/style-specimens/sheet-xhs.jpg` |
| Template source and shared parts | `assets/style-specimens/xhs/`, `assets/style-specimens/xhs/_kit/README.md` |
| A single data long-form image | `references/modules/infographic.md` |
| Covers that need generated imagery (not HTML layout) | `references/scene-templates.md`'s "Xiaohongshu (RED) Images" |
| Fonts and Chinese typography | `references/typography.md` |
