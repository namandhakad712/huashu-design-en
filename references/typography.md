# Typography: a reasoning system for typesetting

> **This is not a font list; it is the reasoning rules for pairing and layout.** `design-styles.md` already gives each of the 40 styles its font names; this file answers "why pair them this way" and "given any content, how to derive font size / line length / weight." Goal: the same style label, applied to different content, should yield different typesetting outcomes — not the same font sizes copied every time.
>
> The standing discipline is unchanged: when there's a design context, lift the user's own fonts first (see `design-context.md`); everything in this file only kicks in when "the user has no font spec."

## 0. Typesetting decision order

Once you have content, reason in this order, each step determined by the previous one — never jump to "just pick a nice font":

1. **Content type** → long-form reading / data-dense / marketing display / UI interface; determines the scale ratio and body font size
2. **Language composition** → pure Chinese / mixed CJK-Latin / pure Latin; determines the fallback chain and line-height baseline
3. **Style temperature** (aligned with design-styles.md's quiet / neutral / bold three tiers) → determines the source of contrast in the font pairing
4. **Font names come last** → pick from the pairing table in Chapter 3 below, or from the corresponding style-library entry

Why: picking font names first makes "what the content is" have zero influence on typesetting — that's the root of the "everyone looks the same" disease.

## 1. Font size scale (modular scale)

Font sizes aren't guessed; they're derived by multiplying the body font size by a fixed ratio, level by level. The ratio determines the page's "drama":

| Ratio | Name | Character | Suited for |
|------|------|------|------|
| 1.2 | minor third | gentle, many levels without clamor | dashboards, doc sites, information-dense UI |
| 1.25 | major third | general-purpose, safe | most web pages, product landing pages |
| 1.333 | perfect fourth | headings clearly pop | editorial long-form, marketing pages, reports |
| 1.5 | perfect fifth | dramatic, very few levels | posters, slides, hero one-line-per-screen |

**Derivation rule**: set body at 16-18px (Chinese body recommended at 17-18px — hanzi have dense strokes and look more crowded than Latin at the same size), then scale up for headings and down for captions. More than 5 levels is out of control; cut.

| Level | Reference value at 1.25 ratio | Usage |
|------|--------------------|------|
| caption | 12-13px | figure captions, meta info, EXIF-style small print |
| small | 14px | helper notes, tables |
| body | 16-18px | body text, the baseline for everything |
| h3 | ≈1.25x | section headings |
| h2 | ≈1.56x | chapter headings |
| h1 | ≈1.95x | page headings |
| display | 3x-8x, free-form outside the scale | hero mega-type, decided by the layout rather than the scale |

**Fluid font size syntax** (required for the display tier, to avoid stiff big screens and overflowing small ones):

```css
/* clamp(min, preferred, max): preferred = base rem + viewport coefficient */
h1 { font-size: clamp(2rem, 1.2rem + 3.5vw, 4.5rem); }
.display { font-size: clamp(3rem, 1rem + 9vw, 9rem); }
/* body text shouldn't clamp with wide swings; a narrow 16→18 range is enough */
body { font-size: clamp(1rem, 0.95rem + 0.3vw, 1.125rem); }
```

Why display leaves the scale: hero mega-type is a layout element, not a text hierarchy level. Its size is decided by "what fraction of the viewport it occupies," so deriving it from vw is more reasonable than from the scale.

## 2. Line length and line height

### Line length (affects readability more than font choice)

| Language | Comfort zone | CSS implementation |
|------|--------|----------|
| Latin body | 45-75 characters, best at 66 | `max-width: 65ch` |
| Chinese body | 22-38 characters per line, best at 28-32 | `max-width: 36em` (em scales with font size) |
| Captions / sidebars | shorter, 15-20 Chinese characters | naturally constrained by narrow containers |

Why Chinese is shorter: hanzi are dense, space-free square characters that carry noticeably more information at the same width. With the same number of eye-saccades a Chinese reader takes in more content, and an over-long line makes it impossible to find the next line's start when wrapping.

### Line height tracks line length

Line height isn't a constant; it's a function of line length. The longer the line, the farther the eye travels back, needing more leading as a "track":

| Scenario | Latin | Chinese |
|------|------|------|
| display mega-type (1-2 lines) | 0.95-1.1 | 1.1-1.25 |
| headings (h1-h3) | 1.1-1.3 | 1.3-1.4 |
| short-line body (<30 chars/line) | 1.4-1.5 | 1.6-1.7 |
| long-line body (near the cap) | 1.6 | 1.8-2.0 |

Chinese runs about 0.2 higher across the board than Latin: hanzi are full-square blocks with none of the natural gaps between Latin lowercase letters, so insufficient leading smears into a blur.

### text-wrap (supported in all 2024+ browsers; free typesetting quality)

```css
h1, h2, h3 { text-wrap: balance; }  /* balanced line lengths across multi-line headings, kills orphan lines */
p { text-wrap: pretty; }            /* body text eliminates end-of-line orphans (pronounced in Latin, mild in Chinese) */
```

balance is only for headings of ≤4 lines (the algorithm caps at 6 lines and has a performance cost); pretty applies globally to body text with no side effects.

## 3. Ten open-source font pairings (Latin)

Three sources of contrast for a pairing; decide which one you're using before pairing:

- **Formal contrast**: serif display × sans-serif body (the classic — but x-heights must interlock, or the visual font size jumps)
- **Same-family interlock**: a superfamily sharing one design skeleton (zero risk, the cost is blandness)
- **Epoch contrast**: classical glyphs × modern glyphs (tension only appears at 200+ years of pedigree; a 50-year gap just looks messy)

| # | Pairing (display + body) | Pairing logic | Temperature | Where to get it |
|---|------------------------|----------|------|------|
| 1 | Newsreader + Geist | Formal contrast: screen-optimized transitional serif with a high x-height that interlocks well with Geist; **the legitimate Fraunces substitute** | quiet | Google Fonts / Vercel official repos |
| 2 | Source Serif 4 + Source Sans 3 | Same-family interlock: one Adobe design system, cap-height and weight rhythms fully aligned; reports and docs never fail | quiet | Google Fonts |
| 3 | EB Garamond + IBM Plex Sans | Epoch contrast: a 16th-century French old-style serif × a 2017 rational grotesque, 400 years of tension; note Garamond's low x-height — mixed usage at the same size needs size compensation (+8% is an experiential starting point; the systematic fix is `font-size-adjust`, see Chapter 4) | quiet·literary | Google Fonts |
| 4 | Lora + Hanken Grotesk | Formal contrast: Lora's brush-feel serif, medium contrast, pleasing on screen; Hanken is an open-source near-relative of the Söhne vibe | neutral | Google Fonts |
| 5 | Instrument Serif + Geist | Formal contrast: only one weight (400), natively display-only — body must go to a sans. ⚠️ On the road to being overused by AI tools; by 2026, be wary of using it when you "want to look distinctive" | neutral | Google Fonts |
| 6 | Schibsted Grotesk + Source Serif 4 | Inverted structure: the grotesque as display, the serif as body — a media feel; **the substitute after Space Grotesk became ubiquitous** (Norway's Schibsted newspaper group's custom open-source face, with newsroom pedigree) | neutral | Google Fonts |
| 7 | Bricolage Grotesque + Newsreader | Formal contrast: Bricolage's ink traps and irregular details only show at large sizes, natively display; paired with a quiet serif body it reads rough × refined | bold | Google Fonts |
| 8 | Archivo (Expanded/Black) + Inter | Poster structure: Archivo's wide black weights carry the pressure; Inter is just a 14-16px body workhorse (this is Inter's correct use — see the anti-patterns) | bold | Google Fonts |
| 9 | Cormorant Garamond + Work Sans | High-contrast luxury: Cormorant's hairlines are extremely thin; **it only works at ≥40px** — strokes break at small sizes; suited to fashion / cosmic catalog aesthetics | bold | Google Fonts |
| 10 | Geist Mono / JetBrains Mono + Geist | Mono as protagonist: command-line and engineering feel; mono only for labels / numbering / code — a full body paragraph in mono is a disaster (line length inflates 30%) | neutral·technical | Vercel / JetBrains official, both OFL |

**The overused list** (fingerprints of AI-generated pages; using them is self-incrimination):

| Overused | Why it's overused | Substitute |
|--------|----------|------|
| Fraunces as display | the default "tasteful" option in every 2023-2025 AI design tool | Newsreader, Libre Caslon Text |
| Inter as display | Inter was designed for small UI text; at large sizes it's uniform and expressionless | Archivo, Anton, Schibsted Grotesk |
| Space Grotesk | the lazy answer to "techy feel," flooded across crypto/AI landing pages | Schibsted Grotesk, Familjen Grotesk |
| Playfair Display | the lazy answer to "elegance," wedding-invitation vibes | Cormorant (more extreme), DM Serif Display (more wholesome) |

## 4. Chinese typesetting (the weightiest chapter here)

Latin typesetting has a century of mature tooling; Chinese doesn't. AI design tools collectively phone it in on Chinese (defaulting to system fonts, applying Latin rules wholesale) — this is where the differentiation lives.

### 4.1 Map of open-source / free-for-commercial-use Chinese fonts

| Font | Category | Character | Temperature | Where to get it |
|------|------|------|------|------|
| Noto Serif SC | serif (Songti) | publishing-canonical, all 7 weights; Heavy works as display | quiet-neutral | Google Fonts, OFL |
| Noto Sans SC | sans-serif (Heiti) | the Inter of the Chinese world: reliable, expressionless; fine as a default body but with no personality | fallback for all temperatures | Google Fonts, OFL |
| LXGW WenKai | kai (script) | handwritten warmth, friendly; suited to literary / educational / personal-blog body text and quotations | quiet·warm | GitHub lxgw/LxgwWenKai, OFL |
| LXGW Neo XiHei | sans-serif (Heiti) | a leaner, more breathable screen sans than Noto Sans; comfortable for long reading | quiet | GitHub lxgw/LxgwNeoXiHei |
| Smiley Sans | italic sans | **one of the rare natively italic faces in the Chinese world**, sporty, heading-only; using it for body text will dizzy you | bold | GitHub atelier-anchor/smiley-sans, OFL |
| Huiwen Mingchao Ti | old-form Ming type | old metal-type print feel, vintage publishing; suited to book covers and cultural display | neutral-bold·vintage | MaoKen web / GitHub, free for commercial use |
| Jinghua Laosong Ti | old Song | a blocky, hard-stroked heading Song with a newspaper-masthead feel | bold·vintage | MaoKen web, free for commercial use |
| Yuanliu Ming Ti / Yuan Yang Ming Ti | Ming type (traditional-leaning) | re-engravings of Noto Serif that preserve traditional glyph details; the first choice for traditional-Chinese content | quiet·classical | GitHub ButTaiwan, OFL |
| Glow Sans | geometric sans | a modern geometric sans derived from Noto Sans, multi-width (Compressed works as narrow tall display) | neutral-bold·modern | GitHub welai/glow-sans, OFL |
| MiSans / HarmonyOS Sans / OPPO Sans | vendor UI sans | UI sans with slightly more personality than Noto Sans; right for app prototypes | neutral | each vendor's official site, free for commercial use |

Selection reasoning: **body text only picks among serif / sans / kai** (everything else is display type; whole paragraphs in them tire the eye). Reach for Smiley Sans / old Song / Ming type only when display needs personality. One Chinese font equals ten Latin ones (a single file is 5-15MB), and a page allows at most two Chinese font families — for both load and consistency reasons.

### 4.2 Mixed CJK-Latin rules

**The fallback chain is the first lever**: the Latin glyphs bundled in Chinese fonts are generally ugly (Noto Sans SC's Latin is staid). Put the Latin font first so Latin letters and digits get caught by it, and hanzi automatically fall through to the Chinese font behind it:

```css
/* Latin first, Chinese after, system Chinese as fallback, generic to finish */
font-family: "Geist", "Noto Sans SC", "PingFang SC", "Microsoft YaHei", sans-serif;
/* same for serif */
font-family: "Newsreader", "Noto Serif SC", "Songti SC", serif;
```

Why this order: font-family matches character by character. A Latin font contains no CJK codepoints, so hanzi naturally fall through to the Chinese font. Written the other way (Chinese first), every Latin character gets eaten by the Chinese font — the pairing is wasted.

**Size compensation**: at the same font size, Latin lowercase looks smaller (x-height only fills half the em, while hanzi fill the whole square). Two solutions:

```css
/* Solution one: font-size-adjust normalizes the fallback font by x-height (Chrome 127+/FF/Safari 17+) */
:root { font-size-adjust: from-font; }
/* Solution two: pick a Latin face with a tall x-height (Geist/Inter/Source Sans are all tall), and mixed setting lines up naturally */
```

**Baseline alignment**: when CJK and Latin baselines differ, the symptom is English words "sinking" inside Chinese lines. Prefer switching to a taller-x-height Latin face; in specific display scenarios use `vertical-align: -0.02em~-0.06em` to nudge Latin spans — but not in body text (maintenance cost outweighs the benefit).

**Number rules**: digits always go through the Latin font (the fallback chain guarantees it), and data tables must add `font-variant-numeric: tabular-nums`, otherwise 1 and 8 have different widths and columns shiver.

**No space between Chinese and English**: this is the repository norm (the original author explicitly rejects Pangu spacing); the whitespace comes from the fonts' own side-bearings in the fallback chain, not from hand-typed spaces.

### 4.3 Chinese has no italics

Chinese glyphs have no italic tradition. When a browser hits `font-style: italic`, it mechanically shears hanzi (faux italic), deforming strokes — extremely ugly. Substitution table for emphasis:

| Latin habit | Chinese substitute | CSS |
|----------|----------|-----|
| italic emphasis | switch weight | `font-weight: 600` (only if the font actually has that weight) |
| italic book titles / quotes | background highlight | `background: linear-gradient(transparent 60%, #FFE9A8 60%)` — highlighter style |
| italic quotation blocks | switch font | the whole quotation becomes LXGW WenKai; the kai script is Chinese's native "quotation voice" |
| italic proper names | color / emphasis dots | `text-emphasis: dot` (emphasis dots, a native Chinese emphasis, support is usable now) |

Fuse: `font-synthesis: none;` globally disables synthetic italic and synthetic bold — better no emphasis than deformed glyphs.

### 4.4 Punctuation rules

| Rule | Approach | Why |
|------|------|--------|
| Quotation marks | corner brackets 「」『』, not curly quotes "" | curly quotes in Chinese fonts are full-width placeholders with Latin shapes — they look like they float; 「」 is this repository's hard norm |
| Line-break rules | `line-break: strict;` | forbids periods/commas at line start and opening quotes at line end; the baseline of Chinese typesetting |
| Hanging punctuation | `hanging-punctuation: first allow-end;` (Safari only); cross-browser, use `text-indent: -0.5em` for paragraph-opening quotes | an un-hung opening quote makes the first line look indented half a character — the left edge isn't flush |
| Consecutive-punctuation compression | `font-feature-settings: "halt";` (line-end compression) or `"palt"` (full proportional width, requires letter-spacing) | a run of full-width punctuation (e.g. 「)。」) leaves a half-character hole; halt narrows it |

### 4.5 Chinese letter-spacing ranges

| Scenario | Range | Why |
|------|------|------|
| Body text | 0 to 0.05em | a touch of tracking improves breathability; beyond 0.05em word wholes shatter and reading speed drops |
| Headings (24-48px) | 0 | hanzi's square forms are naturally evenly spaced; no Latin-style tracking adjustments needed |
| Display mega-type (>60px) | -0.02em to 0 | at large sizes the gaps between glyph faces get amplified; slight tightening is more compact; going more negative collides strokes |
| All-caps Latin micro-labels | 0.08-0.15em | the only scenario needing wide positive tracking, and it only applies to uppercase Latin |

**Never apply the Latin habit of "-0.05em tracking on display" to Chinese**: hanzi are full-square designs; negative tracking directly smashes strokes together.

### 4.6 Chinese display mega-type

Chinese has no display-font ecosystem like Latin's Ultra Thin through Black; the drama of big type must be manufactured by reasoning:

- **Weight contrast is the primary weapon**: Noto Serif SC Heavy 900 against Light 300 — two extreme weights of the same font on one screen carries more tension than swapping fonts, at zero load cost
- **Stroke density sets the usable-size floor**: faces with thin / high-contrast strokes (Song's fine horizontals, Cormorant-style) only hold up at large sizes; below 24px fine strokes start to break, and body text must return to a Heiti / medium stroke
- **The reverse also holds**: heavy-stroke faces (Heiti Black, old Song) carry too much ink at extreme sizes — the ink-mass gap between 「一」and「灥」gets amplified, so uneven-density headings should step down a weight
- **Vertical writing is a display weapon unique to Chinese**: `writing-mode: vertical-rl` makes book-spine headings, poems, and indexes — something Latin can't do; for Latin and digits inside vertical text use `text-orientation: upright` or `text-combine-upright: all` (two-digit numbers combine upright)

## 5. Anti-pattern checklist

| ❌ Anti-pattern | Why it's wrong |
|-----------|----------|
| Inter everywhere (display + body in one go) | Inter is a UI small-text tool; as display it's uniform and expressionless; the #1 fingerprint of "AI-generated pages" |
| Chinese delegated to the `sans-serif` system default | Windows falls to SimSun/SimHei, macOS to PingFang — the same page wears two completely different faces across devices, which is designing not at all |
| faux italic / faux bold | browser-synthesized deformation: italics twist hanzi, synthetic bold smears strokes into ink blobs; cut it off at the root with `font-synthesis: none` |
| Oversized heading tracking | Latin display needs tightening (large-size gaps get amplified); AI often does the opposite and adds +0.05em, leaving headings loose like temporary placeholders |
| Runaway line length (no max-width) | 60 hanzi per line on a big screen, and the reader is guaranteed to get lost rewrapping; runaway line length is the #1 readability problem — it hurts more than a wrong font |
| More than 6 font-size levels | hierarchy devalues and the reader can't tell what matters; the whole point of a scale is forced restraint |
| Only 400/700 two weights | hierarchy carried entirely by size — the page goes flat; in the variable-font era, 300-900 are all free expressive dimensions |
| Tables/data without tabular-nums | digits have unequal widths, columns shake left-right, and data credibility drops directly |
| Chinese body text set in display fonts (whole paragraphs of Smiley Sans / old Song) | a display font's personality becomes reading friction in body text; fatigue sets in after 200 characters |
| Chinese font first in the mixed fallback chain | every Latin character gets eaten by the bundled ugly Latin of the Chinese font, and the carefully paired Latin face never gets its turn |

## 6. CSS implementation notes

```css
:root {
  /* 1. fallback chain: Latin → Chinese → system Chinese → generic (order is the rule, see 4.2) */
  --font-body: "Geist", "Noto Sans SC", "PingFang SC", "Microsoft YaHei", sans-serif;
  --font-display: "Newsreader", "Noto Serif SC", "Songti SC", serif;

  /* 2. ban synthesis: refuse browser-forged italics/bold (mandatory for Chinese scenarios) */
  font-synthesis: none;

  /* 3. Chinese line-breaking baseline */
  line-break: strict;        /* line-break rules */
  overflow-wrap: break-word; /* long URLs/Latin strings don't burst the container */
}

body {
  font-family: var(--font-body);
  font-size: 17px;           /* Chinese body baseline, see Chapter 1 */
  line-height: 1.8;          /* Chinese line-height baseline, see Chapter 2 */
  /* body text enables standard ligatures, disables fancy features */
  font-feature-settings: "liga" 1, "calt" 1;
}

/* data scenarios: tabular digits + slashed zero (0 and O don't confuse) */
.data, table { font-variant-numeric: tabular-nums slashed-zero; }

/* Latin micro-labels: the only legal scenario for all-caps + wide tracking */
.label { text-transform: uppercase; letter-spacing: 0.1em; font-size: 12px; }

/* punctuation compression: narrow the holes of full-width punctuation in Chinese display mega-type */
.display-cjk { font-feature-settings: "halt" 1; }
```

**Loading Chinese fonts** (a single file is 5-15MB; linking the full set directly destroys first paint):

- Prefer Google Fonts' Noto SC family (already auto-split into hundreds of unicode-range chunks; browsers only download the glyphs in use)
- Self-hosted personality fonts (Wenkai / Smiley Sans, etc.) must be subset first: `cn-font-split` or fonttools' `pyftsubset`; body fonts subset to the ~3500 common characters, display fonts to the characters that actually appear (a poster often has only ~20 characters, and a subset can compress under 50KB)
- `font-display: swap` as a safety net — Chinese fonts download slowly, and blank-screening while waiting on the font is the worst experience
