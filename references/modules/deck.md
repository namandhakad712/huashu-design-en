# Module · Slides / PPT / Presentations

Slides, PPT, pitch decks, courseware, and report decks all go here. Cross SKILL.md's narrow bridge first (the three-direction gate included), then follow this manual.

## Delivery Chain (don't ask about format at kickoff)

HTML deck (the base deliverable, always built first) → on completion **automatically** produce the PDF → editable PPTX only when the user asks.

- PDF: multi-file architecture uses `scripts/export_deck_pdf.mjs`; single-file deck-stage uses `scripts/export_deck_stage_pdf.mjs`. Text stays vector and searchable — deliver it without asking.
- PPTX has two routes; pick by the HTML's state, and don't mix them:
  - HTML not written yet → write it under the 4 hard constraints, then run `scripts/export_deck_pptx.mjs` (internally calls `html2pptx.js`) → `references/editable-pptx.md`
  - HTML already written and visually driven, or the client demands their template be inherited → `scripts/pptx_from_rendered.py`, which reads the post-render coordinates, zero retrofit → `references/pptx-from-rendered-html.md`. After export it automatically diffs against the page's innerText and reports whether any text got lost
  - Never downgrade an already-written design to accommodate html2pptx's constraints — that is exactly why the second route exists

## Architecture (decide this first; get it wrong and you'll keep stepping on CSS-scoping pitfalls)

- **Default: multi-file + overview wall** (almost every deck). One standalone HTML per page (a 1920×1080 `<section>`), assembled with `assets/deck_index.html`: copy it straight in as `index.html`, edit the MANIFEST, and it works — **don't rewrite the overview logic** (the three pitfalls of tilt, click hit-testing, and clipping are already solved inside). Two adaptive overviews come built in (grid iframes / infinite gallery — the gallery needs `scripts/gen_deck_thumbs.mjs` run first to generate thumbnails), plus keyboard paging, zoom, unified page numbers, and print merging.
- **Single file**: use `assets/deck_stage.js` only for a ≤5-page minimal pitch, when the overview wall is explicitly not needed, or when JS state has to be shared across pages. The script must sit after `</deck-stage>`, and the section's `display: flex` must be written on `.active`.
- Before going single-file, confirm "really ≤5 pages and no overview wall needed" — a 13-page deck that went single-file and lost the overview wall is a pitfall hit in real testing.

Details, directory structure, the per-page skeleton, what goes into tokens: the "Decide the architecture first" section of `references/slide-decks.md`.

## Build Order

1. Three directions: each direction produces **2 representative pages** (the two that differ most in visual structure, e.g. cover + data page), doubling as the showcase. The three decks share one shell; only the visuals change.
2. After the user picks, a deck of ≥5 pages first locks those 2 showcase pages into the chosen direction's grammar, then batches out the rest. Skipping this = reworking N pages instead of 2 when the direction is wrong.
3. Answer the five form questions for each page first (see `references/workflow.md`), above all "narrative role": cover, transition, data, quote, closing — one role per page, and the layout changes with it.
4. Once everything is done, assemble `index.html` and produce the PDF.

## Hard Rules

- **Page content never carries its own page number or progress marker**; page numbers live in the shell alone (real testing once produced "02/03" and "6/16" page numbers fighting each other)
- Body text ≥24px, labels and annotations ≥16px, headlines 60–120px (full type-size table in the "Scale Standards" section of `references/content-guidelines.md`)
- Fixed-size content implements its own scaling + letterboxing (the shell already does)
- Playback position goes into localStorage and survives refresh
- At design-check time use the deck's type floors: `python3 "$HD/scripts/design_lint.py" check slides/*.html --viewport 1920x1080 --min-body 24 --min-label 16`. A single-file deck-stage can only check the page currently displayed — one more reason multi-file is the default

## Data Pages: Don't Default to "Three Big Numbers + a Bar Chart"

That's the template answer for a deck data page — it looks the same under every style. Ask first what relationship these numbers are telling: proportion (real objects scaled to the ratio), change (one narrative curve), composition (a whole taken apart), comparison (a left-right juxtaposition), scale (one oversized object). The data itself can be the page's lead material (`references/materials.md`).

## Related Files

| Want | Read |
|---|---|
| Architecture, directories, per-page skeleton, common pitfalls | `references/slide-decks.md` |
| Editable PPTX · Route A | `references/editable-pptx.md` + `scripts/html2pptx.js` |
| Editable PPTX · Route B (an already-written visual draft / the client's template) | `references/pptx-from-rendered-html.md` + `scripts/pptx_from_rendered.py` |
| Speaker notes, Tweaks tuning | `references/slide-decks.md`, `references/tweaks-system.md` |
| Style library and specimens (the seconds roulette's PPT section, plus the cross-medium Chinese & East Asian section) | `references/design-styles.md` |
