# Design Style Library: Web 20 + PPT 20 + Infographic 20 + App 12 + Chinese & East Asian 12 + Xiaohongshu 8 (HTML-native first, a specimen for every style)

> **2026-06 restructure**. Reverse-engineered from research on the world's top 10 website types + top 10 presentation types, using the top-5 widely recognized best designs for each (100 real cases total).
> The fatal flaw of the old 20-style "graphic/installation designer philosophy" library: the bold styles were almost all AI-generation-only (particles/light effects/hand-drawn), so **when users have no image-generation capability by default and everything falls back to HTML, the bold half is wiped out entirely, leaving only minimalism — this is the root cause of "default looks identical everywhere"**. Every style in this library is tagged with its **fidelity** under "pure HTML/CSS, no image generation".
>
> ⚖️ **But remember the positioning**: this is **"ammunition to flip through when you have no ideas", not a "must-pick-from-here" checklist**. When the user provides content/brand/reference, the design unfolds from there — don't force the library onto it. The skill's job is to help users avoid the worst, not to dictate what good design must look like — good design grows out of the user's real needs.

## How to use this library

0. **Look at the specimen first, then read the text.** Every section has one overview sheet `assets/style-specimens/sheet-<web|ppt|info|app|east|xhs>.jpg`, and the "Specimen" at the end of each style entry is a single large image (the same-named .html is the source — open it and read the CSS to learn how it's done). The text tells you what a style is; the specimen shows you what it looks like done right — a model that goes by the name alone builds its average impression of the style. The subjects and numbers in the specimens are fictional; what you borrow is the layout and the temperament, not the content.
1. **Pick the section by output type first**: webpage/landing page/corporate site → Web 20; PPT/deck/presentation → PPT 20; infographic/data visualization/single tall image → Infographic 20; App/mobile prototype → App 12; Xiaohongshu image posts/covers/carousels → Xiaohongshu 8 (every specimen doubles as a template). **The Chinese & East Asian 12 are cross-medium** — any output shape can draw from them, and it's especially worth it for Chinese-language content.
   - The criterion is **output shape, not subject**: clickable sites go to the Web section; things you page through go to the PPT section; **an image (or set of images) with data as the protagonist, readable on its own without interaction, goes to the Infographic section**.
   - Two common judgment calls: dashboard prototypes go to the Web section (it's product UI); a data page embedded in a deck still goes to the PPT section (it gets paged through).
2. **Temperature system**: every style is tagged `Bold / Neutral / Quiet`. **Bold styles deliberately make up the majority** — the model's determinism bias naturally leans quiet-minimalist, so the library's ratio pushes it toward bold.
   - This library is the pool the three-direction "seconds roulette" draws from (see `references/directions.md`); when the best-designer and real-world-reference logics run dry, you can flip through it too.
   - ❌ Don't let all three directions land on the same temperament (e.g. all "cream white + whitespace + one accent color").
3. **Fidelity**: ≥90% — build it with your eyes closed; 70-90% — the main body is doable, a few details downgrade; <70% (e.g. Memphis aged textures) — you must **explicitly flag in the output which parts are downgraded to flat color blocks**; don't pretend you can reproduce the original texture.
4. **Fonts**: every style lists open-source substitutes (Inter/Geist/Manrope/Space Grotesk/Fraunces/Playfair etc.); never specify paid fonts (Söhne/Circular etc.).
5. Companions: the three-direction "seconds roulette" draws from this library (`references/directions.md`); styles that need real photos (dark gallery, white-box gallery, maps-as-protagonist, etc.) use honest placeholders in their specimens — fetch real images first when you build for real.

---

## Color Derivation Protocol (run these three steps before using any style)

> ⚠️ **The hex values in all the style entries below are example anchors, not formulas.** The same style applied to different content should derive different color values through this protocol — directly copying an entry's hex is just producing slop with better taste. Why: a hard-coded formula hands 100 users 100 identically-colored outputs and the information in color drops to zero; derivation makes the color evidence that is unique to this content.
>
> **The same goes for fonts**: the font names in the entries are example anchors too. After picking a style, run the display+body pairing through the pairing logic and the "overused list" in `references/typography.md` first — **when the list conflicts with an entry, typography.md wins** (e.g. if an entry says Fraunces, swap in the substitute the list names).

### Three-step method: Sample → Converge → Justify

| Step | What to do | Why |
|------|--------|--------|
| **1. Sample** | The primary color comes from three sources, not invented from thin air: ① brand assets (eyedrop straight from the logo/existing VI) ② real images from the content (dominant colors in product screenshots/photography) ③ cultural context (the color memory the content's theme carries, see the table below) | Picking a color out of thin air = drawing lots from the model's priors, and you'll always draw one of the same few internet-trendy colors; colors sampled from content come with a built-in "why" |
| **2. Converge** | Use oklch to compress the palette to **2-3 chromatic colors + 1 neutral set**. Write the neutrals as a lightness sequence (e.g. L 0.15/0.35/0.65/0.92/0.98), and keep chromatic colors apart by oklch hue angle H ≥60° or a lightness L gap ≥0.3 | Too many colors always means chaos; oklch's L channel is perceptually uniform, so a lightness sequence written out is a hierarchy system you can reason with — unlike a pile of isolated hexes |
| **3. Justify** | Write one sentence of "why this color" and put it in the output comments or the delivery notes. E.g.: "Primary color taken from the ochre of the user's logo, chroma pushed down to 0.08 to simulate ink" | **If you can't write that sentence, you're copying a formula.** The justification is a self-check gate against slop, not a ritual |

### Print color texture: why low saturation reads more premium than pure screen colors

Ink on paper can never reach the maximum saturation of a screen's RGB — CMYK's gamut is narrower, paper absorbs ink, and ambient light bounces back, all of which "gray down" the color. The "premium feel" human eyes have been trained on by decades of print is, at root, this layer of physical grayness. So deliberately pushing chroma down in screen design borrows the texture memory of print.

| Use | oklch chroma reference | Effect |
|------|------------------|------|
| Large background areas | 0.01–0.04 | Paper feel, not harsh |
| Brand primary/accent | 0.08–0.15 | Ink feel, eye-catching but not plasticky |
| Small-area highlights (buttons/links) | 0.15–0.22 | Keeps the energy, small areas only |
| >0.25 full-bleed wash | Use with caution | Screen-phosphor look, only suits deliberately "electronically native" styles like Wrapped/candy |

### Cultural context quick reference: same hue, different contexts

Choosing a color isn't just choosing a hue, it's choosing the cultural coordinates behind it. The same "red" can land miles apart:

| Hue | Context A | Context B | What differs |
|------|--------|--------|--------|
| Red | Forbidden City vermilion (orange-leaning, gray-tinged, oklch low L low C, darker and muddier than cola red) → traditional/dignified | Cola red (high-saturation true red) → consumer/excitement | Drop the chroma and it jumps from a store shelf to a palace wall |
| Blue | Japanese indigo/lapis navy (deep, purplish-gray) → handcrafted/calm | Tech blue #0066FF family → SaaS/efficiency | The latter is the model's favorite default blue — before using it, ask yourself whether you're drawing lots |
| Green | Matcha/moss green (yellow-leaning, low saturation) → natural/Japanese | Neon green #39FF14 → terminal/hacker | Same green, but one drinks tea and the other writes code |
| Yellow | Gamboge/mustard (brown-gray tinge) → vintage print | Warning yellow/Mailchimp yellow → eye-catching/playful | The grayness decides whether it's an old book page or a hard hat |
| White | Cream paper white #F5F0E8 → publication/warm | Pure white #FFF → laboratory/Swiss | A 2% color-temperature gap in the background is a temperament divide |

---

## Web Style Library (20 styles)

#### Bold

**Media-Grade Editorial Brutalism (giant Helvetica pressing down small body text)** `Bold · 98% fidelity`
- Reference: Bloomberg Businessweek (Richard Turley 2010-2014 redesign, executed by Code and Theory); Neue Haas Grotesk lineage
- Fits: media/content publishing, AI product launches, brand-site heroes, research report covers, long-opinion-piece headers
- Visual DNA: pure black #000 + pure white #FFF + hyperlink blue #0000EE, accented with signal orange-red #FF433D / terminal green #00A33E. Type Helvetica/Neue Haas Grotesk, 120px+ giant left-aligned headlines with tight tracking pressing directly onto 14px body text, extreme size contrast. Layout modular grid + 1px rule lines dividing columns, high information density with deliberately no whitespace. Signature elements: rule-line column dividers, underlined hyperlink blue, large black/white color blocks.
- HTML implementation: pure CSS can reproduce it 1:1. CSS Grid for the modular grid + border for the rule-line dividers, clamp() for oversized responsive type + tightened letter-spacing, system Helvetica/Arial stack or Inter fallback, hyperlinks directly #0000EE underlined. Zero asset dependency.
- Fonts: Inter (replacing Helvetica/Neue Haas Grotesk), Geist Mono for code
- Specimen: assets/style-specimens/web/01-editorial-brutalism.jpg

**Neo-Brutalism Clashing Info Stream (thick black-outline cards + high-saturation clashing colors)** `Bold · 95% fidelity`
- Reference: The Verge 2022 redesign (in-house team, PolySans + Mānuka)
- Fits: media/content sites, AI product aggregation pages, event landing pages, community ranking pages, Xiaohongshu-style info cards
- Visual DNA: electric purple #5200FF ~ magenta #E1306C high-saturation primaries + bright yellow #F8E000 accent + pure black #08080D + white, large clashing color blocks deliberately unsoftened. Type geometric sans-serif headlines + serif body contrast. Layout card-based feed, 2-4px thick black outlines, hard color-block zones, nearly no rounded corners. Signature elements: thick-outline cards with clashing hover color inversion, unfinished-interface vibe.
- HTML implementation: a pure CSS strength. border:3px solid #000 thick outlines + box-shadow hard offset shadow (4px 4px 0 #000) + grid/flex card streams + :hover background clashing inversion. No 3D/light-effect obstacles.
- Fonts: Space Grotesk (replacing PolySans) + any serif like Fraunces
- Specimen: assets/style-specimens/web/02-neo-brutalism.jpg

**Memphis Maximalism (clashing color blocks + offset overlaps + vintage type)** `Bold · 72% fidelity`
- Reference: Gucci Vault concept store (Alessandro Michele); the Memphis design movement / Sagmeister's rebellious DNA
- Fits: e-commerce concept stores, creative event pages, brand experiment campaigns, Y2K retro themes, holiday marketing pages
- Visual DNA: vintage red/mustard yellow/royal blue/purple/olive green large clashing color blocks juxtaposed on an aged cream warm base, intensely and deliberately inharmonious. Type vintage serifs mixed with decorative faces, print texture, breaking the grid with offset overlaps. Layout anti-grid collage curation, modules of varying sizes offset and stacked, like wandering through a digital room. Signature elements: clashing color blocks, offset overlaps, unconventional nav easter eggs.
- HTML implementation: transform:rotate() for offset overlaps + position:absolute stacking + high-saturation background color blocks + vintage Google Fonts. Real aged textures can't be reproduced in CSS, downgraded to flat color blocks + mix-blend-mode/contrast filters to simulate texture; the geometric collage version holds up, the archival aged version downgrades.
- Fonts: DM Serif Display + Bungee (decorative) + Space Mono
- Specimen: assets/style-specimens/web/03-memphis-maximalism.jpg

**Friendly Geometric Candy (candy-color raised 3D buttons, gamified)** `Bold · 85% fidelity`
- Reference: Duolingo (Johnson Banks + Monotype, Feather Bold typeface); anti-Silicon-Valley minimalism
- Fits: education/language learning, consumer app landings, gamified products, mass-friendly products, event signup pages
- Visual DNA: Duo green #58CC02 + duck yellow #FFC800 + sky blue #1CB0F6 candy high saturation + white base, rounded and friendly. Type extra-bold rounded faces (Feather Bold feel). Layout large rounded cards, raised 3D buttons (hard bottom shadow = pressable feel), mascot slot + progress bubbles. Signature elements: 3px solid-shadow raised buttons, press-down motion on click, super-rounded corners.
- HTML implementation: pure CSS. box-shadow:0 4px 0 hard bottom shadow for raised buttons + :active translateY(4px) shadow removal to simulate pressing, large border-radius, flat color blocks. Without image generation, use CSS geometric shapes or emoji as the mascot placeholder (slight downgrade).
- Fonts: Baloo 2 / Nunito (extra-bold rounded, replacing Feather)
- Specimen: assets/style-specimens/web/04-friendly-candy.jpg

**Pure-CSS Geometric Illustration + Responsive Morphing Easter Eggs (Pure-CSS Art)** `Bold · 80% fidelity`
- Reference: Lynn Fisher (lynnandtonic.com, pure-CSS art legend, covered in an Adobe feature)
- Fits: personal homepages, creative 404/easter-egg pages, playful brand landings, tech blog headers, designer self-promotion
- Visual DNA: 2-4 high-contrast flat colors (palette changes at each breakpoint). Type bold geometric sans-serif headlines. Layout centers on "art that morphs with the viewport" — a set of CSS shapes recomposing into different pictures at different breakpoints (e.g. a building whose floors change with screen width). Signature elements: pure-CSS geometric illustrations, breakpoint-driven rearrangement easter eggs, zero images.
- HTML implementation: the playground of pure CSS showmanship, zero assets is an advantage. Stack geometric shapes from div + border-radius/clip-path/transform/box-shadow, use @media breakpoints to change shape size/position for morphing. The difficulty is in the design thinking rather than the technique, but each shape needs careful hand-crafting.
- Fonts: Rubik / Archivo (bold geometric, replacing custom)
- Specimen: assets/style-specimens/web/05-pure-css-art.jpg

**Bold Big-Type Editorial, Giant High-Contrast Black-and-White Fashion Poster** `Bold · 88% fidelity`
- Reference: Jacquemus official site / Rik Oostenbroek / Domestika; fashion-magazine big-type posters
- Fits: e-commerce fashion, portfolios, media features, brand manifesto pages, video course covers, large-type versions of research reports
- Visual DNA: minimalist black-and-white + a single restrained accent (blush pink #E8C4C0 or true red). Type oversized display sans/serif with high contrast, headlines filling the entire screen. Layout full-bleed grid, giant type wrestling with negative space, 1:1 text/image split. Signature elements: screen-filling giant headlines, luxury-grade whitespace, left-right counterpoint layout.
- HTML implementation: pure CSS reproduces it perfectly. clamp() giant type + CSS Grid full-bleed splits + generous padding whitespace + vh units so headlines fill the viewport. Without images, use flat color blocks/text blocks as placeholders for the fashion photography (slight downgrade, but the layout holds).
- Fonts: Archivo Expanded / Anton (Display) + Playfair Display (high-contrast serif)
- Specimen: assets/style-specimens/web/06-bold-big-type.jpg

**Cosmic Retro-Futurism, Vintage Future Space Catalog** `Bold · 75% fidelity`
- Reference: Perplexity Comet browser launch site (The Brand Identity: Black/Blue/Cream; 2001: A Space Odyssey vibes)
- Fits: AI product launch sites, tech brand manifesto pages, event countdown pages, futuristic landings, concept launch events
- Visual DNA: pure black #0A0A0A + cream paper white #F0EAD8 + a touch of cobalt-peacock blue #2B4F91, low saturation like vintage astronomy catalogs. Type high-contrast serif (classical astronomy-atlas feel) + whitespace. Layout line-drawn orbital/parabolic SVG, planetary dots, cream base with black text, old-book typography. Signature elements: SVG celestial orbit lines, cream+blue+black tri-color, vintage serif large type, astronomy-catalog texture.
- HTML implementation: pure CSS+SVG reproduces about 80% of the static version's character. SVG path for orbital parabolas + CSS radial positioning for planetary dots + tri-color variables + high-contrast serif. The gap: the full-screen video transition of "space falling to Earth" (the soul part) — downgraded to CSS scroll parallax + SVG orbit rotation as an approximation.
- Fonts: Cormorant Garamond / EB Garamond (high-contrast serif) + Space Mono
- Specimen: assets/style-specimens/web/07-cosmic-retro-futurism.jpg

**Cinematic Sound-Viz Dark (cinematic sound-wave visualization)** `Bold · 72% fidelity`
- Reference: ElevenLabs; film title sequences (Saul Bass-style minimalist motion) × audio engineering interfaces
- Fits: audio/voice AI products, music tech sites, podcast platforms, media release pages, cinema-grade brand heroes
- Visual DNA: pure black #000 base + pure white text + blue-purple gradient accent waveforms. Type large sans-serif headlines in Saul Bass-style minimalism. Layout full-bleed dark field, sound-wave/spectrum visualization running throughout, giant titles pressing onto waveforms, card function zones. Signature elements: colored audio-waveform bands, movie-title-style minimalism, high-contrast black-and-white + a single gradient, sound-visualization motif.
- HTML implementation: pure CSS+SVG reproduces 70% of the character (the skeleton is perfect, the waveform is the downgrade point). SVG polyline for static waveforms or arrays of unequal-height div bars + CSS animation for a 'fake waveform' bouncing approximation. Gap: Web Audio/Canvas spectrums that jump with the sound in real time can't be done in pure CSS — the static version looks right, the dynamic soul can't be restored.
- Fonts: Inter / Sora (large sans-serif)
- Specimen: assets/style-specimens/web/08-cinematic-sound-viz.jpg

**Pixel-Game Side-Scroller, 8-bit Narrative** `Bold · 70% fidelity`
- Reference: Robby Leonardi's interactive resume (8/16-bit platform-action-game narrative, a tribute to the Nintendo SNES)
- Fits: creative resumes/portfolios, playful brand campaigns, gamified landings, event easter-egg pages, personal fun homepages
- Visual DNA: retro-game multi-zone palette — forest green #4CAF50 grass + sky blue #5DADE2, transitioning to space purple #2C2A4A, volcano orange-red #E8743B, seabed cyan #1ABC9C, each 'level' getting its own high-saturation cartoon palette. Type pixel fonts (8-bit feel) + bold sans-serif. Layout horizontal/vertical scrolling through level-by-level scenes, parallax layers, scroll-triggered displacement. Signature elements: per-level color changes, pixel aesthetics, parallax scrolling, game HUD-style UI.
- HTML implementation: pure CSS + a little JS reproduces the skeleton (the original is itself HTML+CSS+jQuery, no WebGL). Parallax layers via position + scroll displacement, image-rendering:pixelated, CSS frame-by-frame background-position sprite animation, segmented background colors. Gap: original hand-drawn character/scene pixel illustrations — without image generation, assemble simple pixel icons from CSS blocks as substitutes (art downgrade, not technique).
- Fonts: Press Start 2P / VT323 (pixel) + Inter
- Specimen: assets/style-specimens/web/09-pixel-side-scroller.jpg


#### Neutral

**Bauhaus Geometric (geometric logo + flat illustration system)** `Neutral · 90% fidelity`
- Reference: Khan Academy rebrand (hexagon + petal logomark + the Wonder Blocks design system); Bauhaus geometric composition
- Fits: education course sites, brand logo systems, infographics, children-friendly products, event key visuals
- Visual DNA: primary-color-spectrum palette — Bauhaus red #E63946 / yellow #FFB703 / blue #0077B6 + black and white, flat color block assembly. Type geometric sans-serif (rounded, geometric feel). Layout circle/triangle/square basic geometric units building illustrations, aligned to a grid, modular puzzle. Signature elements: pure-geometry logomarks, flat no-gradient illustrations, primary color block composition.
- HTML implementation: pure CSS is all-powerful with geometry. border-radius:50% for circles, clip-path/border triangles, square divs assembling geometric illustrations, CSS Grid for grid alignment, flat fills need no assets. Hand-craft the illustrations from CSS shapes or inline SVG geometric paths.
- Fonts: Poppins / Manrope (rounded geometry, replacing Wonder Blocks)
- Specimen: assets/style-specimens/web/10-bauhaus-geometric.jpg

**Dark Editorial, two-color sidebar dev portfolio (deep base + single neon accent + mono type)** `Neutral · 96% fidelity`
- Reference: Brittany Chiang (brittanychiang.com v4, the de-facto dev portfolio standard)
- Fits: portfolio personal sites, developer-facing products, tech brand sites, resume pages, AI tool landings
- Visual DNA: deep ink-green/navy base #0A192F + slate gray text #8892B0 + a single neon cyan-green accent #64FFDA. Type sans-serif body + mono (numbers/labels). Layout fixed left sidebar nav + right scrolling main area, two columns, section numbers 01/02, hover underline slide-in on links. Signature elements: single accent color, mono number labels, sidebar anchor highlighting.
- HTML implementation: pure CSS reproduces it fully. position:sticky for the fixed sidebar + CSS Grid two columns + single-accent variable + mono labels + :hover underline transform slide-in. Zero assets, pure layout and micro-interactions.
- Fonts: Inter + JetBrains Mono (mono)
- Specimen: assets/style-specimens/web/11-dark-editorial.jpg

**Warm Editorial (cream paper base + terracotta orange + serif/sans mixed)** `Neutral · 97% fidelity`
- Reference: Anthropic / Claude (DBCo + Geist Studio, Styrene×Tiempos); Penguin/Pelican paperback typography
- Fits: AI product sites, brand corporate sites, long-form reading pages, orange-cover ebooks, research reports, training materials
- Visual DNA: cream paper base #F5F0E8 + terracotta orange #CC785C/#D97757 accents + near-black text #191919, warm and low saturation. Type serif headlines (Tiempos feel) × sans-serif body (Styrene feel) mixed. Layout book-like single-column reading flow, comfortable line height, restrained dividers. Signature elements: paper-feel warm base, terracotta orange, publication-grade typographic rhythm.
- HTML implementation: pure CSS 100% reproduction, zero assets. Background color variable + serif/sans font-stack mixing + max-width to cap the reading width + line-height 1.7 comfortable leading.
- Note: this is also the look the model drops into most thoughtlessly (it's Claude's own palette, see `references/content-guidelines.md`). Using it is fine — provided you chose it rather than slid into it: don't let all three directions crowd in here, and if the look ledger says it appeared recently, pick something else.
- Fonts: Fraunces / Newsreader (replacing Tiempos serif) + Inter (replacing Styrene)
- Specimen: assets/style-specimens/web/12-warm-editorial.jpg

**Linear dark glow + Bento grid (Glassmorphism Bento)** `Neutral · 85% fidelity`
- Reference: Linear / Cursor (the phenomenon-grade 'The Linear Look' school, Frontend Horse has the code recipe)
- Fits: SaaS/AI product sites, developer tools, tech brand heroes, product feature showcases, dark dashboard demos
- Visual DNA: near-black base #08090A + desaturated blue-purple brand #5E6AD2 + low-saturation cyan-purple glow gradient #4EA7FC→#B59AFF. Type geometric sans-serif with tight negative tracking. Layout bento-box grid blocks, hairline dividers, glassmorphism cards. Signature elements: dark-base glowing gradient borders, bento blocks, streamers, frosted glass.
- HTML implementation: pure CSS strong reproduction. box-shadow/filter blur + radial-gradient for the glow halos, backdrop-filter:blur for glassmorphism, conic/linear-gradient borders, CSS Grid to assemble the bento. The only gap: "real product UI screenshots" — substitute a simplified fake UI assembled from color blocks + text (that part downgrades).
- Fonts: Inter / Geist (negative tracking) + Geist Mono
- Specimen: assets/style-specimens/web/13-glassmorphism-bento.jpg

**Angled Fluid Gradient (slanted fluid gradient bands)** `Neutral · 92% fidelity`
- Reference: Stripe (the iconic angled gradient banner, Klim's custom Söhne typeface)
- Fits: SaaS/fintech landing pages, brand-site heroes, product launch pages, event banners, AI product marketing pages
- Visual DNA: multi-color fluid gradient (indigo #635BFF→cyan→pink→warm orange) as the hero background + pure white content area + near-black text. Type refined sans-serif (Söhne feel). Layout slanted color-block sections (skew-cut zones), the gradient hero pressing over a structured grid body. Signature elements: angled cut boundaries, multi-color fluid gradients, rational grid over expressive gradients.
- HTML implementation: pure CSS. transform:skewY() or clip-path:polygon() for the slanted sections, linear-gradient multi-color stacking (optionally CSS animation for slow flow) for the fluid gradient band, Grid for the structured body below. Zero assets.
- Fonts: Inter / Hanken Grotesk (replacing Söhne)
- Specimen: assets/style-specimens/web/14-angled-fluid-gradient.jpg

**Utility-First Colorful Docs (pragmatic rainbow-coded documentation)** `Neutral · 98% fidelity`
- Reference: Tailwind CSS Docs (Sky/Cyan brand color + function-category rainbow hue bars)
- Fits: technical documentation, API references, design system sites, tutorial sites, developer knowledge bases, SaaS help centers
- Visual DNA: Sky blue #38BDF8 brand + teal→cyan→sky cyan-blue gradient + Slate gray scale #0F172A/#64748B/#F8FAFC; docs use rainbow hue bars to separate functional categories (pink #EC4899 / purple #A855F7 / green #10B981 / orange). Type clean sans-serif + mono code. Layout three columns — left sidebar nav + center content + right TOC — color-highlighted code blocks, category color labels. Signature elements: cyan-blue gradient hero, rainbow category colors, three-column docs skeleton, syntax-highlighted code blocks.
- HTML implementation: pure CSS 98% reproduction (it's a CSS framework's own docs). Grid three columns + linear-gradient cyan hero + category color variables + code-block syntax colors via span coloring. Inter is open source; only dark-mode toggle/copy needs light JS. Zero light effects/3D/hand-drawing.
- Fonts: Inter + JetBrains Mono / Fira Code (code)
- Specimen: assets/style-specimens/web/15-utility-colorful-docs.jpg

**Terminal-Core Soft-Futurism (mono type + isometric cubes)** `Neutral · 80% fidelity`
- Reference: Cursor (Anysphere); developer terminal aesthetics × Teenage Engineering industrial minimalism
- Fits: AI coding tool sites, CLI product landings, developer infrastructure, tech brand heroes, terminal-type products
- Visual DNA: charcoal black #0B0D14 base + warm white text #F2F0EF + a restrained blue-purple gradient accent on buttons and glows. Type mono as the protagonist (command-line feel) + sans-serif support. Layout command-line/code-block foreground, bento sections, 2.5D isometric cube diagrams. Signature elements: mono command lines, isometric-projected cubes, warm white × charcoal, restrained gradient glows, industrial minimalism.
- HTML implementation: pure CSS 80% reproduction. Mono code blocks + dark bento + box-shadow glows; 2.5D isometric cubes hand-built with CSS 3D transforms (rotateX/Y + skew) or SVG isometric projection. Gap: a clickable multi-interface demo needs JS + fake UI assembly. No hard WebGL requirement.
- Fonts: Geist Mono / JetBrains Mono (protagonist) + Inter (support)
- Specimen: assets/style-specimens/web/16-terminal-core.jpg


#### Quiet

**Functional Brutalism (gray-line dividers + system fonts + blue links, grid community)** `Quiet · 98% fidelity`
- Reference: Are.na / Lobsters / Quartz; Müller-Brockmann grids landing digitally + Tufte information density
- Fits: community/UGC platforms, content aggregation sites, documentation knowledge bases, mobile-first content feeds, geek-oriented products
- Visual DNA: near-white base #FBFBFB + black text + 1px gray dividers #E0E0E0 + classic link blue #0000EE / visited purple. Type system font stack (-apple-system, undecorated). Layout high-density information lists, thin gray-line columns, minimal whitespace, compact line spacing. Signature elements: hairline gray dividers, blue links, system fonts, information-density-first.
- HTML implementation: the easiest to reproduce in pure CSS, this is Brutalist Web's native look. border-bottom:1px gray-line lists + system-ui font stack + compact padding + blue links. Needs almost no assets or JS, pure structure.
- Fonts: system-ui system font stack / IBM Plex Sans (fallback)
- Specimen: assets/style-specimens/web/17-functional-brutalism.jpg

**Gallery Dark (deep black negative space + single-column large images + EXIF small type)** `Quiet · 75% fidelity`
- Reference: Glass (glass.photo) / Bottega Veneta; gallery darkroom + Apple Photos content-first
- Fits: photography portfolios, luxury e-commerce, immersive visual content display, personal gallery pages, premium product displays
- Visual DNA: pure black base #0A0A0A + the artwork itself supplying the only color + very faint gray EXIF small type #666. Type ultra-thin sans-serif small type. Layout single-column centered large images, huge negative-space framing, metadata small type under each image. Signature elements: darkroom black base, content-first UI receding, EXIF-style small-type captions, large images owning the viewport.
- HTML implementation: pure CSS reproduces the layout skeleton. Pure black base + centered max-width single column + generous padding frame whitespace + small metadata type. The gap is "real photography" itself — placeholders/flat color blocks lose the soul, but the darkroom atmosphere and layout are 100% buildable.
- Fonts: Inter (light weight 300) / Cormorant (optional serif luxury feel)
- Specimen: assets/style-specimens/web/18-gallery-dark.jpg

**Swiss Monochrome (Vercel-style pure black-and-white + Geist + razor-sharp corners)** `Quiet · 98% fidelity`
- Reference: Vercel / Next.js Docs (their in-house Geist, now open source); Massimo Vignelli's less-is-more
- Fits: developer tool documentation, tech brand corporate sites, AI product sites, SaaS landing pages, minimalist research reports
- Visual DNA: pure black #000 + pure white #FFF + gray scale #888, zero color or just a touch of blue links. Type Geist geometric sans-serif + Geist Mono. Layout razor-sharp right angles (no or minimal rounding), high contrast, precise grids, restrained whitespace. Signature elements: pure black-and-white, sharp corners, Geist type, triangle/arrow geometric markers.
- HTML implementation: pure CSS 100% reproduction, Geist is open source and directly importable. CSS Grid precise grids + pure black/white variables + border-radius:0 sharp corners + hairline borders. This is HTML's most comfortable minimalist home turf, zero asset dependency.
- Fonts: Geist + Geist Mono (Vercel's open-source originals)
- Specimen: assets/style-specimens/web/19-swiss-monochrome.jpg

**Kenya Hara White Gallery (Japanese-style white box gallery)** `Quiet · 80% fidelity`
- Reference: Cosmos (cosmos.so) / the Aesop official site; the emptiness of Kenya Hara's 'white' + a Swiss grid hybrid
- Fits: high-end e-commerce, creative galleries, content curation platforms, designer portfolios, brand boutiques, moodboard sites
- Visual DNA: near-all-white #FAFAFA base + pure black text #0A0A0A + very faint gray dividers #EFEFEF, content images supplying all the color, UI receding into the background. Type minimalist system/geometric sans-serif small type, wide tracking. Layout masonry waterfall grid, extreme whitespace, faint gray hairline separators, Eastern emptiness. Signature elements: white-box aesthetics, luxury whitespace, content-first UI receding, waterfall curation.
- HTML implementation: pure CSS reproduces the static layout (distinguished from the dark gallery by the 'white'). CSS columns or Grid for masonry + near-white variables + generous padding whitespace + faint gray dividers. The gap is Lenis/GSAP silky inertial scrolling and image entrance easing (60% of the premium feel lives there); CSS only does basic transitions, so the motion layer downgrades.
- Fonts: Inter (light weight) / Cooper Hewitt (Aesop's same open-source typeface)
- Specimen: assets/style-specimens/web/20-kenya-hara-white-gallery.jpg


## PPT Style Library (20 styles)

#### Bold

**Neo-Swiss Billboard Editorial** `Bold · 98% fidelity`
- Reference: the Big-Number Editorial school of AI/SaaS pitch decks like Scribe's $75M and Flock Safety's $47M; Bloomberg Businessweek infographics; Pentagram
- Fits: fundraising pitches, QBR/business reviews, annual trend retrospectives, key pages of product launches
- Visual DNA: Palette = pure white (#FFFFFF) or near-black (#0A0A0A) base + a single high-saturation accent (electric blue #2D5BFF / neon green #00E676 / brand orange #FF6B2C) + neutral grid lines #E5E5E5. Typography = extra-large bold sans-serif, headline claiming half the screen, numbers in tabular-nums, equal-width, tracking tightened. Master layouts = ① large color-block section page with a single word ② giant number claiming half the screen (3.2x) + a small caption ③ left-right split comparison ④ full-bleed flat line/bar charts. Signature = billboarding giant type, strict baseline grid, large color-block section pages
- HTML implementation: clamp() for oversized numbers; CSS Grid for the strict grid; background-color for large color-block section pages; line/bar charts as pure div+CSS or inline SVG (sharper than pasted images); font-variant-numeric:tabular-nums for number alignment. Zero illustration, zero 3D
- Fonts: Inter / Geist / Söhne replacing Neue Haas Grotesk; Geist Mono for numbers
- Specimen: assets/style-specimens/ppt/01-neo-swiss-billboard.jpg

**Black Big-Number Stage (giant numbers on black)** `Bold · 97% fidelity`
- Reference: Steve Jobs' 2007 iPhone keynote, the Xiaomi SU7 Ultra Lei Jun launch, Spotify Wrapped, Presentation Zen (Garr Reynolds)
- Fits: product-launch keynotes, thought-leadership talks, all-hands town halls, emotionally-driven annual reviews
- Visual DNA: Palette = pure black #000000 base + pure white #FFFFFF type at maximum contrast, one brand accent highlight per page (Xiaomi orange #FF6900 / Spotify green #1ED760 / Apple blue #2997FF). Typography = geometric sans-serif bold, one word per screen or one giant number filling the view, tracking tightened. Master layouts = ① title page, black base, one centered line of giant type ② data-climax page with a giant number + unit + one-line caption ③ left-right parameter comparison in two columns (accent color vs gray) ④ single-slide slogan. Massive negative space
- HTML implementation: black base with white type takes a few lines of CSS; clamp() + flex centering for giant numbers; a standalone span for the accent highlight; two CSS Grid columns + bar highlight for the left-right comparison; tabular-nums. Drop the product photos and go pure text — that actually lands closer to Zen's essence
- Fonts: Geist / Inter / Source Han Sans replacing SF Pro
- Specimen: assets/style-specimens/ppt/02-black-big-number-stage.jpg

**Mono-Brand Type-as-Hero (high-saturation monochrome brand poster)** `Bold · 96% fidelity`
- Reference: the Spotify Wrapped visual system, Mailchimp Brand Book (Collins), Netflix red-black modern revival, COLLINS brand systems
- Fits: brand/marketing strategy, campaign pitches, town-hall culture pages, event key visuals
- Visual DNA: Palette = a single brand primary color laid edge-to-edge (Spotify green #1ED760 / Mailchimp yellow #FFE01B / Netflix red #E50914) + black or white contrasting type, two clashing layers. Typography = oversized type as the hero visual (type-as-hero), floor to ceiling. Master layouts = ① full color-block base + reverse-white giant type ② two color blocks split top/bottom or left/right ③ giant numbers filling the frame. Signature = monochrome full-bleed, type as image, high-contrast clashing
- HTML implementation: full-bleed background-color; clamp() for oversized type filling the frame; two 100vh color blocks for the split; type-as-image via font-weight 900 + negative letter-spacing. Pure color blocks, zero assets — HTML native at its most satisfying
- Fonts: Inter / Manrope / Archivo (extra-bold) replacing Circular/Cavendish
- Specimen: assets/style-specimens/ppt/03-mono-brand-type-hero.jpg

**Full-Bleed Gradient Manifesto** `Bold · 82% fidelity`
- Reference: Zuora's "Tell a Different Story" sales deck (Andy Raskin's breakdown), Nike's "Just Do It" campaign, National Geographic double-page spreads
- Fits: vision pages of sales proposals, brand manifestos, keynote pivot pages, mission/vision single slides
- Visual DNA: Palette = full-bleed CSS gradients (warm orange → magenta / deep blue → cyan) or flat color bleed + reverse-white manifesto giant type + hashtag slogans (#shifthappens). Typography = heavy sans-serif, all-caps slogans running across the frame. Master layouts = ① full-bleed gradient + centered reverse-white manifesto ② promised-land vision page ③ customer logo wall. Signature = full-bleed bleeding, reverse-white giant slogans, hashtag slogans
- HTML implementation: linear-gradient/radial-gradient full-bleed (no particles/light effects — pure CSS gradients are allowed); centered positioning for the reverse-white type; a grid of grayscale SVG/text placeholders for the logo wall. The parts that originally leaned on documentary big photos downgrade to a CSS gradient base + giant type; the missing photography drops fidelity by about 15%
- Fonts: Archivo / Anton / Manrope (extra-bold)
- Specimen: assets/style-specimens/ppt/04-full-bleed-gradient-manifesto.jpg

**Candy-Color Lecture Stage (CS50 single-concept stage)** `Bold · 94% fidelity`
- Reference: Harvard CS50 (David Malan), the Lessig Method / Takahashi style, Presentation Zen
- Fits: educational courseware, tech lectures, concept explanations, code teaching
- Visual DNA: Palette = deep black base #0A0A0A + high-saturation candy colors rotating through the giant type (magenta #FF2D95 / cyan #00E5FF / bright yellow #FFD500 / green #39FF14). Typography = oversized sans-serif floating centered, one concept per screen, minimal text. Master layouts = ① deep-black base with a single candy-color giant word ② monospaced code block with syntax highlighting ③ stage-spotlight giant type. Signature = candy-color giant type floating on deep black, mono code highlighting, strong stage spotlight, minimal text
- HTML implementation: deep-black background + single-color giant type with clamp() centered; code blocks as pre + monospace + colored spans for syntax highlighting; a very faint radial-gradient vignette for the spotlight feel (not particle light effects). High fidelity
- Fonts: Inter extra-bold + JetBrains Mono (code)
- Specimen: assets/style-specimens/ppt/05-candy-lecture-stage.jpg

**Playful Maximalist Editorial (Collins-style)** `Bold · 75% fidelity`
- Reference: Mailchimp Brand Book (Collins 2018), New Yorker cartoon sensibility, Cooper rounded serifs, Cavendish fluorescent yellow
- Fits: decks for brands with attitude, creative-agency pitches, culture-flavored town halls, marketing pages that push back against SaaS minimalism
- Visual DNA: Palette = Cavendish fluorescent yellow #FFE01B in large fields + black + a little clashing color, anti-SaaS-minimalism. Typography = Cooper-style rounded serif headlines (playful) + magazine-style whitespace composition. Master layouts = ① fluorescent-yellow full base + whimsical headline ② magazine-style irregular whitespace layout ③ giant type with meme copy. Signature = fluorescent yellow, rounded serifs, playful composition, whimsical hand-drawn character (downgraded to geometric color blocks / emoji replacing real illustration)
- HTML implementation: fluorescent yellow background; rounded-serif font-family; asymmetric Grid for the magazine whitespace. The hand-drawn gorilla/illustration — the core element — cannot be done without AI image generation; it downgrades to CSS geometric color blocks + large emoji + irregularly transform-rotated text blocks. Missing illustration drops fidelity by about 20%
- Fonts: Fraunces (adjustable roundness) / Bree Serif replacing Cooper; Inter for body
- Specimen: assets/style-specimens/ppt/06-playful-collins-editorial.jpg

**Irreverent Pop (Reddit-style)** `Bold · 80% fidelity`
- Reference: Reddit Ads sales deck (listed by Dock as the most characterful), David Carson-style irreverent typography, 90s web retro, Memphis playfulness
- Fits: Gen-Z brands, meme-marketing decks, community/creator audiences, proposals that dare to be unserious
- Visual DNA: Palette = Reddit orange-red #FF4500 + clashing colors, 90s web retro palette. Typography = David Carson-style mixed, grid-breaking typography, meme-flavored colloquial copy. Master layouts = ① fun pages with meme giant type ② facts pages pivoting into serious data ③ colloquial headlines. Signature = grid-breaking mixed type, orange-red, meme colloquialism, fun→facts rhythm reversal, retro web texture
- HTML implementation: deliberately break the grid with transform rotations / overlapping positioning / mixed font sizes; orange-red + clashing color blocks; retro texture via thick black borders + hard box-shadows (no blur). Custom meme illustrations downgrade to emoji + geometric collage, but the mixed typography itself is HTML-reproducible
- Fonts: Archivo / Space Grotesk + mixed-in Inter for contrast
- Specimen: assets/style-specimens/ppt/07-irreverent-pop.jpg

**Maximalist 3D-Type (Wrapped-style Y2K inflated giant type)** `Bold · 78% fidelity`
- Reference: Spotify Wrapped 2022/2023/2025, Memphis clashing colors, Y2K/Maximalism, duotone portrait gradients
- Fits: annual reviews (emotion-driven virality), personalized data cards, vertical social-sharing cards, brand year-end
- Visual DNA: Palette = high-saturation clashing full-bleed background (magenta + cyan + orange) + Spotify green as the finishing touch + duotone two-color gradients. Typography = floor-to-ceiling giant numbers, years/numbers given 3D inflation / metallic finish. Master layouts = ① clashing full-bleed + giant inflated number ② duotone portrait/color-block base + reverse-white giant type ③ vertical shareable card. Signature = giant inflated 3D numbers, clashing full-bleed, duotone gradients, metallic year texture, vertical story cards
- HTML implementation: clashing full-bleed background; 3D inflated numbers via layered CSS text-shadow + transform:perspective, or SVG + stroke for dimensionality (not real 3D rendering); duotone via mix-blend-mode + gradient layered over a grayscale placeholder block. The metallic finish downgrades to gradient-filled text via background-clip:text, dropping fidelity by about 15%
- Fonts: Archivo Black / Anton extra-bold + Clash Display for numbers
- Specimen: assets/style-specimens/ppt/08-y2k-inflated-wrapped.jpg


#### Neutral

**Bento Grid** `Neutral · 95% fidelity`
- Reference: the Apple keynote Bento Grid era, the new generation of MBB Bento/Big-Type decks (2024-2026), Stripe annual-report metric-card matrices, Pitch.com QBR templates
- Fits: product feature roundups, consulting/QBR data reports, sales results pages, town-hall metric pages
- Visual DNA: Palette = light gray/cream base (#F5F5F7/cream) or near-black base + brand primary + 1-2 accents, cards on light tinted panel bases + rounded corners + hairline borders/subtle shadows. Typography = oversized display headlines + regular body, strong weight contrast, KPI numbers in tabular figures. Master layouts = ① title page with a giant single sentence + whitespace ② bento page of 2×2/3-column unequal-height cards, one insight per card (number / line icon / sparkline) ③ one-insight oversized-number page. Signature = unequal-height card grid, rounded corners with hairline borders, breathing room
- HTML implementation: CSS Grid's grid-template-areas for unequal-height bento; cards with border-radius + subtle box-shadow + 1px hairline; inline SVG for sparklines; inline SVG stroke for line icons. Zero pasted images
- Fonts: Inter / Geist + Geist Mono for numbers
- Specimen: assets/style-specimens/ppt/09-bento-grid.jpg

**Dark Hairline Terminal (Neo-Swiss dark terminal aesthetics)** `Neutral · 94% fidelity`
- Reference: the Linear pitch deck, Vercel design language, CS50 deep-black stage courseware; typefaces Inter Tight + JetBrains Mono
- Fits: developer-tool/tech product launches, tech roadshows, engineering-flavored reporting
- Visual DNA: Palette = near-black base (#0D0D0F/#111113) + hairline #262629 grid + a single purple-blue accent (#5B5BD6/#7C7CFF). Typography = Inter Tight for headlines + JetBrains Mono for labels/data. Master layouts = ① ultra-minimal title page, one sentence + small mono label ② hairline-divided data grid ③ feature list with mono labels. Signature = 1px hairline grid, monospaced mono labels, extreme whitespace, near-black rather than pure black
- HTML implementation: near-black background + border:1px solid hairline grid; monospace font-family for mono labels; a very faint box-shadow/border highlight for subtle glow instead of real light effects (a downgrade that dodges the cyber-neon forbidden zone). Watch out for the #0D1117 deep-blue forbidden zone — use neutral near-black
- Fonts: Inter Tight + JetBrains Mono / IBM Plex Mono
- Specimen: assets/style-specimens/ppt/10-dark-hairline-terminal.jpg

**Two-Font Consulting (Bower-style)** `Neutral · 90% fidelity`
- Reference: McKinsey 2019 brand system (designed by Wolff Olins, Bower serif + sans), BCG Executive Perspectives, deep-blue thin-line patterns
- Fits: consulting reports, executive briefings, industry research, proposals from authoritative institutions
- Visual DNA: Palette = deep blue (#051C2C, McKinsey deep blue) × white as a binary + a single brand-color highlight (BCG green #00805A), warm-gray base with breathing room. Typography = characterful serif headlines (Bower-style) juxtaposed against sans-serif body at high contrast. Master layouts = ① conclusion-style action title in the top-left corner ② deep-blue thin-line pattern decoration ③ magazine-style left/right division of labor (conclusion text + visuals) ④ big-number data-point card. Signature = serif × sans high contrast, deep-blue thin-line patterns, action titles, warm-gray premium feel
- HTML implementation: two font-families juxtaposed (serif headlines + sans body); thin-line patterns via repeating-linear-gradient or SVG lines; data-point cards in pure CSS; the grayscale photo treatment is skippable when there are no photos. The blue-purple edge shimmer downgrades to a flat color edge
- Fonts: Playfair Display / Fraunces serif headlines + Inter body (replacing Bower)
- Specimen: assets/style-specimens/ppt/11-two-font-consulting.jpg

**Diagram-Driven Isotype (enterprise diagram arrows)** `Neutral · 88% fidelity`
- Reference: Salesforce sales decks, the Isotype (Otto Neurath) lineage, Gene Zelazny's *Say It With Charts*, Hans Rosling/Gapminder
- Fits: platform/architecture explainers, customer journeys, process methodologies, ecosystem maps
- Visual DNA: Palette = enterprise-blue color blocks + per-product-line color coding + iconified capability grids. Typography = clean sans-serif. Master layouts = ① horizontal customer-journey arrow flow ② layered platform-architecture diagram ③ iconified capability grid ④ 2×2/waterfall/pyramid structure diagrams. Signature = arrow flows, layered architecture boxes, Isotype icon grids, process as narrative
- HTML implementation: arrow flows via Flexbox + CSS clip-path triangles or SVG arrows; architecture layers as nested bordered divs; icons as inline SVG with unified stroke; waterfall/pyramid via Grid + slanted cuts; bubble charts with CSS circles + positioning. Pure vector drawing
- Fonts: Inter / IBM Plex Sans (chart-friendly)
- Specimen: assets/style-specimens/ppt/12-diagram-isotype.jpg

**Diagrammatic Minimalism (single master diagram concept)** `Neutral · 95% fidelity`
- Reference: Simon Sinek's Golden Circle TED talk, Bauhaus geometric abstraction, the information-architecture creed of "one diagram rules the room"
- Fits: explaining theoretical frameworks, TED-style idea dissemination, visualizing models/methodologies, single-concept keynotes
- Visual DNA: Palette = minimal white/light base + black + 1 accent color, flat geometric color. Typography = sans-serif, labels in uppercase, embedded in the shapes. Master layouts = ① a single geometric master diagram (concentric circles / triangle / matrix) carrying the entire concept ② inside-out arrows ③ contrasting cases. Signature = a single geometric master diagram, nested concentric circles/triangles, uppercase labels, one diagram carrying the concept
- HTML implementation: concentric circles as border-radius:50% nested divs or SVG circles; triangles via clip-path/SVG polygon; arrows with SVG markers; labels absolutely positioned onto the shapes. Pure geometry — HTML reproduces it perfectly
- Fonts: Manrope / Futura family (open-source Jost) for the geometric feel
- Specimen: assets/style-specimens/ppt/13-diagrammatic-minimalism.jpg

**Narrative Sparkline (Duarte-style)** `Neutral · 91% fidelity`
- Reference: Nancy Duarte's sparkline narrative maps in *Resonate*, Al Gore's *An Inconvenient Truth*, Duarte Inc. data storytelling
- Fits: presentation structure design, change narratives, before/after comparisons, data story arcs
- Visual DNA: Palette = dark or white base + brand orange accenting the turning points + grayed-out comparisons. Typography = sans-serif, with annotation callouts at the points. Master layouts = ① an oscillating wave line running across the full screen ② text annotation points pinned on the wave ③ vertically juxtaposed comparison waves ④ a single data line hanging alone on an all-black base ⑤ progressive reveal. Signature = the across-the-screen wave line, annotation points on the wave, orange turning points, comparison waves, curves climbing out of the frame
- HTML implementation: the wave line as an inline SVG path (smooth Béziers); annotation points as SVG circle + text positioning; two paths stacked for the comparison waves; reveal via CSS animation on stroke-dashoffset. Pure SVG drawing, zero assets
- Fonts: Inter + Geist Mono for numbers
- Specimen: assets/style-specimens/ppt/14-narrative-sparkline.jpg


#### Quiet

**Assertion-Evidence / Tufte Information Design** `Quiet · 93% fidelity`
- Reference: Michael Alley's Assertion-Evidence (empirically validated at Penn State), McKinsey/BCG action titles, Edward Tufte's data-ink ratio, Barbara Minto's Pyramid Principle
- Fits: academic/engineering reports, data-rigorous consulting pages, policy research reports, technical reviews
- Visual DNA: Palette = white/very light gray base + black body text + a single restrained accent (deep blue / brick red). Typography = full-sentence titles (not noun phrases), one dedicated chart under the title, text annotations embedded inside the chart. Master layouts = ① full-sentence action title ② single-chart evidence under the title ③ zero bullets. Signature = full-sentence titles, single-chart evidence, embedded annotations, zero chartjunk, high data-ink ratio
- HTML implementation: full-sentence titles via typographic hierarchy; charts drawn in pure CSS/inline SVG as minimal line/scatter plots (gridlines and legends stripped out, annotations positioned as text right beside the data points); zero decoration. Tufte's restraint is exactly where HTML shines
- Fonts: Source Serif / Lora headlines + Inter body (dual-font, reading-grade)
- Specimen: assets/style-specimens/ppt/15-assertion-evidence.jpg

**Institutional Swiss Minimal** `Quiet · 96% fidelity`
- Reference: Sequoia's official 10-page pitch template, Airbnb's 2009 seed-round deck, Müller-Brockmann grids, Massimo Vignelli
- Fits: investor roadshows, standard business proposals, problem-solution narratives, decoration-free brand proposals
- Visual DNA: Palette = pure white base + black/gray body text + a single brand accent (Airbnb coral #FF5A3C / neutral blue). Typography = Helvetica-family sans, medium-size bold one-sentence headline, body in short sentences with generous spacing. Master layouts = ① centered logo + slogan ② top one-sentence title band + three balanced columns below (Problem/Solution, three points each) ③ TAM big numbers in layers ④ 2×2 competitor matrix. Signature = the top title band, three-column antithesis, monochrome accent, 2×2 matrix
- HTML implementation: Flexbox for the three-column antithesis; the 2×2 matrix in pure CSS Grid + borders; TAM layers as nested divs or concentric squares; one message per slide. Almost pure typographic gridwork — HTML's ideal subject
- Fonts: Inter / Helvetica Now replacing Helvetica; Inter for body
- Specimen: assets/style-specimens/ppt/16-institutional-swiss.jpg

**Editorial Longform (magazine long-form flow)** `Quiet · 95% fidelity`
- Reference: the Stripe Annual Letter ($1.9T), Amazon six-page narrative memos, Benedict Evans' "X eats the world", Stripe Press
- Fits: annual letters/retrospective narratives, long-form thought pieces, internal updates, research-report-style reading
- Visual DNA: Palette = cream/off-white base (#FBFAF8) + deep ink text + brand color as punctuation (Stripe purple #635BFF). Typography = serif or high-quality sans-serif, prose paragraphs + inline data cards, oversized display numbers interspersed. Master layouts = ① masthead giant headline ② multi-column prose + inline metric cards ③ oversized-number paragraph anchors. Signature = the reading rhythm of a publication, inline data cards, restrained whitespace, prose rather than bullets
- HTML implementation: multi-column via column-count or Grid; inline data cards as float/inline-block embedded in the text; serif body with max-width holding lines to about 65ch; oversized numbers interspersed. Pure typography, zero assets
- Fonts: Newsreader / Source Serif body + Inter as support; tabular numbers
- Specimen: assets/style-specimens/ppt/17-editorial-longform.jpg

**Humanist Rounded Cards (Khan-style)** `Quiet · 80% fidelity`
- Reference: Khan Academy's Wonder Blocks design system, Source Serif Pro serifs, forest-green branding, friendly humanism
- Fits: education products, approachable courseware, nonprofit/public-interest decks, warm brand proposals
- Visual DNA: Palette = forest green #14BF96/#0A5C4B + cream base + warm auxiliary colors, soft on the eyes. Typography = Source Serif headlines (humanist) + sans-serif body. Master layouts = ① groups of rounded card components ② serif headline + approachable body ③ slots for real photography (downgraded to green-family geometric/rounded color blocks). Signature = forest green, serif headlines, big rounded cards, human warmth, an imperfect, approachable texture
- HTML implementation: large border-radius cards + soft box-shadow; serif font-family for headlines; warm cream base. Real teacher-and-student photography is out of reach without AI image generation, downgraded to green-family geometric illustration blocks / large rounded flat placeholders + emoji figures; missing photography drops fidelity by about 18%
- Fonts: Source Serif 4 headlines + Nunito Sans / Inter body (Nunito's roundness echoes the humanism)
- Specimen: assets/style-specimens/ppt/18-humanist-rounded-cards.jpg

**Dense Research Report (Meeker-style)** `Quiet · 92% fidelity`
- Reference: Mary Meeker's *Internet Trends* (BOND), CB Insights' *State of AI*, McKinsey Global Institute's *Year in Charts*, FT/Bloomberg data journalism
- Fits: trend research reports, industry data retrospectives, dense data briefings, market maps
- Visual DNA: Palette = white base + brand color (BOND/CB Insights bright blue #0066FF) as a stepped monochrome highlight with everything else grayed out, almost zero whitespace. Typography = conclusion-style sentence titles, one chart per page at full density, tiny source footnotes. Master layouts = ① conclusion-sentence title + full-page single chart ② logo-grid market map ③ big-number KPI cards ④ dense multi-chart grid + footnotes. Signature = conclusion-sentence titles, zero-whitespace research-report feel, stepped monochrome highlights, logo market maps, source footnote conventions
- HTML implementation: every dense chart drawn in pure CSS/inline SVG (bars/lines/stacks/scatter); the logo market map as Grid + text/SVG placeholder cells; KPI cards in CSS; footnotes in small type. Extreme information density is exactly what HTML excels at — zero assets
- Fonts: Inter + IBM Plex Sans + tabular Geist Mono for numbers
- Specimen: assets/style-specimens/ppt/19-dense-research-report.jpg

**All-Text Manifesto (Netflix/Amazon-style)** `Quiet · 97% fidelity`
- Reference: the Netflix Culture Deck (2009, 125 pages), Amazon six-page narrative memos (Bezos), Tufte's anti-PowerPoint stance, Matthew Carter's reading-grade typography
- Fits: culture manifestos, values talks, deep memos, anti-PPT pure-document presentations
- Visual DNA: Palette = pure white or pure black base + a single accent (Netflix red #E50914) as the only highlight, extreme restraint. Typography = reading-grade typesetting, one viewpoint per slide — golden-quote assertions or pure prose, zero bullets, zero images. Master layouts = ① full-bleed base + golden-quote assertion ② candid conversational paragraphs ③ institutional-term highlights (Keeper Test) ④ six pages of prose + appendix table. Signature = pure text, one viewpoint per slide; zero images, zero bullets; single-color highlighted golden quotes; conversational candor; a silent-read document feel
- HTML implementation: pure typography: golden quotes in large clamp() type with a left-aligned hierarchy; prose with max-width controlling line length; the one accent color as a span highlighting key phrases; an ultra-minimal table for the appendix. Zero assets, zero images — pure text is HTML's most reliable reproduction
- Fonts: Newsreader / Source Serif (reading-grade) or Inter (manifesto-style); Archivo extra-bold for titles
- Specimen: assets/style-specimens/ppt/20-all-text-manifesto.jpg


---

## Infographic Style Library (20 styles)

> **New in 2026-08**. Until now this library had only the web and deck halves, yet "infographics/visualization" is one of the four scenarios in the SKILL — when you were making an infographic, the roulette could only land in the web half, you'd draw a community-site or landing-page style, and force-fit it. This half fills exactly that hole.
> The criterion: **the output is one image (or a set of images) with data as the protagonist, readable on its own without interaction** — it goes here. A clickable site goes to the web section; something meant to be paged through goes to the PPT section.

#### Bold

**Personal Annual Report (Feltron-style)** `Bold · 94% fidelity`
- Reference: Nicholas Felton's *Feltron Annual Report*, 2005–2014 (the 2006–2011 volumes are in MoMA's permanent collection); Stefanie Posavec; Bloomberg Businessweek annual specials
- Fits: personal or team annual summaries, quantified-self, product year-in-review, Wrapped-style retrospectives, long-cycle self-audits
- Visual DNA: uncoated-paper warm white base + a single vermilion running through everything as the accent + slate blue as the second data series + a third color bound to exactly one meaning, never reused. Type Helvetica-family tight setting, giant numbers pressing down from the top, dense small-type footnotes. The four-piece master set: ① giant-number module strips ② polar period charts (24h/12 months) ③ calendar heat grids ④ a time or geography band running the full width. Signature elements: the contrast of treating trivial personal data like a corporate annual report, modular print grids, 1px dividers, still readable printed in black and white.
- HTML implementation: CSS Grid splits the modules + 1px borders slice the grid; the polar charts as inline SVG with the angles hand-computed (no chart library pulled in); the calendar as Grid + child elements filled by height. Pure typography + SVG, zero assets — an extreme strong suit of HTML.
- Fonts: Archivo / Helvetica Neue (tight-set giant numbers) + Inter (small-type footnotes)
- Specimen: assets/style-specimens/info/01-personal-annual-report.jpg

**Explanation Graphics (Nigel Holmes-style)** `Bold · 76% fidelity`
- Reference: Nigel Holmes (TIME graphics director 1978–1994, founded Explanation Graphics in 1994); championed explaining abstract numbers with pictures and humor — and became the bullseye of the chartjunk debate
- Fits: popular-science explainers, walking laypeople through complex concepts, mass-media column art, children's and educational material
- Visual DNA: three or four high-saturation flat colors + black outlines. Type rounded sans + handwritten-feel annotations. Layout the chart itself drawn as a physical metaphor (banknotes stacked into columns, a thermometer as a gauge, a running track as a progress bar). Signature elements: skeuomorphic charts, humor, little human figures, thick outlines, zero gradients.
- HTML implementation: the chart skeleton is CSS/SVG doable, **but the soul is the hand-drawn illustration** — under pure HTML it can only degrade into geometric color blocks, and the degradation must be explicitly flagged; when image generation is available, use huashu-gpt-image to generate illustration elements and composite them in
- Fonts: Nunito / Baloo 2 (rounded) + Caveat (handwritten annotations)
- Specimen: assets/style-specimens/info/02-explanation-graphics.jpg

**Cross-Section Epic (SCMP Arranz-style)** `Bold · 55% fidelity`
- Reference: Adolfo Arranz (senior graphics editor at SCMP, multiple gold medals at Malofiej, best known for the Kowloon Walled City cross-section *City of Anarchy*); the Malofiej awards are called the Pulitzers of infographics
- Fits: architecture/history/machine anatomy, a single long sheet that holds ten minutes of reading, museum-grade science communication
- Visual DNA: dark ground (deep ink or deep brown) + warm highlights + aged-paper texture. Composition: one giant sheet, isometric or straight cross-section view, dense callout lines ringing the subject. Signature elements: hand-drawn detail, callout lines, the cross-section view, one image telling the whole story.
- HTML implementation: 🔴 **pure HTML cannot draw a hand-drawn cross-section** — this style demands illustration assets; without them, don't fake it. HTML only carries the callout layer and the zoom/scroll interaction. If you can't get the assets, switch styles.
- Fonts: Source Serif (titles) + Inter (callouts)
- Specimen: assets/style-specimens/info/03-cross-section-epic.jpg

**Magazine Pop Data (Businessweek-style)** `Bold · 90% fidelity`
- Reference: Bloomberg Businessweek (the Richard Turley years), WIRED chart pages, The Economist's Graphic Detail column
- Fits: business/tech-media charts, opinion-column art, square social-media images, data charts embedded in official-account posts
- Visual DNA: two clashing primaries (fluorescent yellow + black, magenta + navy) + paper-white breathing room, no third color to soften them. Type super-heavy condensed display headlines + tiny caption type, size contrast above 10×. Layout one chart, one argument — the chart itself is the layout's protagonist, and the headline states the conclusion outright. Signature elements: extreme size contrast, clashing colors, charts bleeding past the type area, conclusion-style headlines.
- HTML implementation: pure CSS reproduces it fully; charts as inline SVG or CSS Grid bars; the bleed comes from negative margins. Zero assets.
- Fonts: Archivo Black / Anton (condensed heavy) + IBM Plex Sans (captions)
- Specimen: assets/style-specimens/info/04-magazine-pop-data.jpg

**ISOTYPE Pictorial Statistics / Neurath–Arntz** `Bold · 88% fidelity`
- Reference: the ISOTYPE picture-education system Otto Neurath and Gerd Arntz built in 1920s Vienna
- Fits: population/social/public-policy data, public communication aimed at low-literacy audiences, educational posters
- Visual DNA: a limited spot-color set (black + red + blue + ochre) flat-filled, no gradients, no shadows. Layout the same icon repeated N times to show quantity — **enlarging an icon to mean "more" is wrong**; that rule is the heart of the system. Signature elements: silhouette icon arrays, horizontal rows, text labels on the left, an extreme sense of order.
- HTML implementation: icons as inline SVG silhouettes + CSS repeat layout — HTML is a natural fit. The icons can be self-drawn geometric silhouettes, no external assets needed
- Fonts: Jost / Archivo (Futura substitutes)
- Specimen: assets/style-specimens/info/05-isotype.jpg

**Data Humanism (Lupi-style)** `Bold · 80% fidelity`
- Reference: Giorgia Lupi (Pentagram partner) and Stefanie Posavec's *Dear Data*; Lupi's Data Humanism manifesto holds that "data is people, not numbers"
- Fits: personal, emotional data; small-sample thick description; turning private experience into a legible atlas; subjects rich in non-quantified dimensions
- Visual DNA: journal-beige base + 4–5 soft colors each bound to its own meaning (coral / pine green / mustard / ink-violet), **not one of them decorative**. Master layouts ① fix a visual language first (size / shape / spikes / tail, each encoding one dimension) ② always pair it with a legend that teaches the reader to decode ③ elements arranged along organic paths, no grid. Signature elements: decodable custom symbols, a legend always included, organic arrangement.
- HTML implementation: symbols generated parametrically as inline SVG (radius / spike count / tail length bound to data fields); paths as Bézier curves threaded through the points. Pure SVG, zero assets; the only thing it can't do is a true hand-drawn stroke
- Fonts: Georgia / Source Serif (titles) + Inter (legends)
- Specimen: assets/style-specimens/info/06-data-humanism.jpg

**Scrollytelling (The Pudding-style)** `Bold · 85% fidelity`
- Reference: The Pudding (data-journalism magazine), NYT The Upshot, Reuters Graphics scroll features
- Fits: complex arguments that need revealing step by step, long data stories, web-native features
- Visual DNA: the palette switches by chapter but one accent runs throughout. Layout text steps forward on the left, the graphic morphs on the right as you scroll; each screen advances exactly one variable. Signature elements: the graphic never gets swapped, only morphed; text and graphic strictly bound; chapter color shifts; a full panorama at the end.
- HTML implementation: IntersectionObserver triggers the state switches + CSS transitions or SVG attribute interpolation — pure front-end reproduces it fully. ⚠️ The deliverable must be a web page — **exporting to PDF/PNG loses the entire narrative**; don't pick it when the user wants a static image
- Fonts: Inter / Source Serif (long-form readability first)
- Specimen: assets/style-specimens/info/07-scrollytelling.jpg

**Cartographic Lead (Stamen-style)** `Bold · 65% fidelity`
- Reference: Stamen Design (founded in San Francisco by Eric Rodenbeck in 2001, clients include National Geographic); its Watercolor and Toner map tiles are public classics
- Fits: geographic distribution data, urban/transit/environmental subjects, content where location is the narrative
- Visual DNA: the basemap sets the tone (watercolor or monochrome Toner) + the data layer in high-contrast points and lines. Layout the map fills the type area, data overlaid as point density or flow lines, the legend tiny and pressed into a corner. Signature elements: a basemap with authorship, a restrained data layer, geography's shapes as the composition itself.
- HTML implementation: 🔴 **needs real geographic data (GeoJSON) and a basemap** — pure HTML cannot conjure correct terrain out of thin air; no data, switch styles, **and never hand-draw a fake map**. With data in hand, draw it as an inline SVG projection
- Fonts: Inter / IBM Plex Sans (place labels take a lot of small type)
- Specimen: assets/style-specimens/info/08-cartographic-lead.jpg

#### Neutral

**Newsroom Chart System (FT-style)** `Neutral · 96% fidelity`
- Reference: the Financial Times' Chart Doctor team and its public Visual Vocabulary (pick the chart by relationship: Deviation / Correlation / Ranking / Distribution / Change-over-Time / Part-to-Whole / Magnitude / Spatial)
- Fits: finance and industry data, anywhere "the right chart type" matters more than "pretty," series of charts that need one unified standard
- Visual DNA: the signature pink-orange newsprint ground + an ordered color scale (a single-hue ramp for continuous quantities, a contrasting two-tone pair for deviations). Master layouts ① the headline is the takeaway ② a subtitle stating the definitions ③ the chart body stripped of frames and gridlines ④ the data source always credited bottom-left. Signature elements: choose the chart type from the data relationship before talking aesthetics, the source line is non-negotiable, minimal axes.
- HTML implementation: pure CSS/SVG for lines and bars; the key is **to consult the Visual Vocabulary and pick the right chart type before** you start. Zero assets
- Fonts: Inter / Source Sans (body) + a monospace for the figures
- Specimen: assets/style-specimens/info/09-newsroom-chart.jpg

**Computational Portrait (Fathom-style)** `Neutral · 78% fidelity`
- Reference: Ben Fry and his Boston studio Fathom Information Design (Fry co-created Processing and wrote *Visualizing Data*; work shown at the Whitney Biennial)
- Fits: very large datasets, subjects that need "letting the data grow its own shape," genetics/transit/time series
- Visual DNA: white or near-black ground + hairline strokes + one hue's transparency stacking up density. Layout no summaries — the full data presented, the figure forming from the stacked density of a mass of fine elements. Signature elements: hairlines, transparency stacking, no decoration, shape decided by the algorithm rather than the layout.
- HTML implementation: Canvas or swarms of SVG paths drawn programmatically; at large data volumes, Canvas is mandatory. **Requires the real full dataset** — a small sample can't produce this style's feel of density
- Fonts: Inter / Roboto Mono (data labels)
- Specimen: assets/style-specimens/info/10-computational-portrait.jpg

**Beautiful Information (McCandless-style)** `Neutral · 90% fidelity`
- Reference: David McCandless's *Information is Beautiful* and the site of the same name, famous for "turning big datasets into color graphics you can compare at a glance"
- Fits: popular-science comparisons, rankings, mass-audience data aggregation, charts built to travel on social media
- Visual DNA: many colors, but a harmonized ring of equal lightness and saturation (not random clashes). Layout "area means quantity" chart types dominate — bubbles / treemaps / Sankeys — with labels pressed straight onto the color blocks. Signature elements: area encoding, tonal multicolor, legends embedded, dozens of entries in one image.
- HTML implementation: treemaps and bubbles via CSS Grid or computed SVG layout (you write a simple packing algorithm yourself); Sankeys via SVG Béziers. Zero assets
- Fonts: Nunito Sans / Inter
- Specimen: assets/style-specimens/info/11-beautiful-information.jpg

**Open Research Data (Our World in Data-style)** `Neutral · 94% fidelity`
- Reference: Our World in Data (Oxford's Global Change Data Lab); the rules: charts are interactive, the definitions are written out, the data is downloadable
- Fits: rigorous subjects, data displays that must survive scrutiny, long-horizon trend comparisons
- Visual DNA: white ground + a set of categorical colors that separate well without shouting + gray for the series that don't matter. Master layouts ① a one-sentence takeaway as the headline ② definitions and time range in the subtitle ③ labels set directly at the line ends inside the chart (no legend) ④ source and license noted at the bottom. Signature elements: end-of-line labels instead of legends, graying out the non-essential, transparent definitions, restraint.
- HTML implementation: pure SVG lines + text positioned at the ends — HTML's most rock-solid genre. Zero assets
- Fonts: Inter / Lato
- Specimen: assets/style-specimens/info/12-open-research-data.jpg

**Speculative Tech Diagram (Takram-style)** `Neutral · 84% fidelity`
- Reference: Takram (a design-engineering studio in Tokyo and London, a speculative design practice spanning design and engineering)
- Fits: technology concept diagrams, future-scenario exploration, research white-paper art, product-architecture narratives
- Visual DNA: a warm-gray sandy base + low-saturation natural colors (moss green / terracotta) + one touch of metallic gray. Type light weights, wide tracking, considered Chinese–English mixed setting. Layout charts arranged like artworks, generous whitespace, geometry with a precision-instrument feel. Signature elements: a soft sense of tech, precision geometry, restrained natural colors, charts as installations.
- HTML implementation: pure CSS/SVG reproduces it; the keys are the whitespace ratio and line-weight restraint (0.5–1px). Zero assets
- Fonts: Inter (light weights) / Noto Sans JP + Cormorant (optional for titles)
- Specimen: assets/style-specimens/info/13-speculative-tech-diagram.jpg

**Pictogram System (Otl Aicher-style)** `Neutral · 92% fidelity`
- Reference: Otl Aicher's pictogram system for the 1972 Munich Olympics and the Ulm school's grid method
- Fits: flowcharts, wayfinding and guide-type infographics, multilingual settings, whenever a whole icon set must stay consistent
- Visual DNA: a restricted palette (the Olympic set: light blue / green / silver) + black. Layout every icon shares one grid and one set of stroke angles (only 0/45/90°), icons always paired with short labels. Signature elements: strict angle constraints, system consistency, short sans-serif labels, the grid left visible.
- HTML implementation: icons self-drawn as inline SVG under the 45° constraint; the grid via CSS Grid. Zero assets, but the angle discipline is yours to keep
- Fonts: Jost / Archivo (Univers substitutes)
- Specimen: assets/style-specimens/info/14-pictogram-system.jpg

#### Quiet

**Tufte Small Multiples** `Quiet · 95% fidelity`
- Reference: Edward Tufte's small multiples and sparkline concepts from *Envisioning Information*
- Fits: comparisons across many dimensions, grouped time series, one variable's behavior across dozens of slices
- Visual DNA: white ground + black lines + one accent flagging the anomaly. Layout the same small chart repeated N times, only the data changing, **all sharing one axis range — mismatched ranges destroy comparability, the one fatal error of this school**; labels tiny beside each chart. Signature elements: gridded repeated small charts, shared scales, zero legends, zero gridlines, high data-ink ratio.
- HTML implementation: CSS Grid arranges the small charts + an inline SVG line in each cell. Always unify the domain. Zero assets
- Fonts: Source Serif (titles) + Inter (small labels)
- Specimen: assets/style-specimens/info/15-small-multiples.jpg

**Topological Transit Map (Beck/Vignelli-style)** `Quiet · 86% fidelity`
- Reference: Harry Beck's 1933 London Underground map, Massimo Vignelli's 1972 New York Subway map
- Fits: flows and relationship networks, org charts, system topologies, any diagram where "the connections matter more than the real distances"
- Visual DNA: white or light ground + one high-saturation solid color per line. Layout every segment runs only 0/45/90°, stations evenly spaced — **sacrificing geographic accuracy for readability is this school's reason for being**; transfer points as hollow circles. Signature elements: the eight-direction constraint, equidistant nodes, solid-color lines, hollow nodes.
- HTML implementation: inline SVG polylines with the angles strictly constrained; nodes as circles. Pure geometry — HTML fits perfectly
- Fonts: Jost / Inter (station names can be all caps)
- Specimen: assets/style-specimens/info/16-topological-transit-map.jpg

**Ma & Emptiness (Kenya Hara-style)** `Quiet · 82% fidelity`
- Reference: Kenya Hara (原研哉)'s *White* and the MUJI visual system — "whitespace is not emptiness; it is the vessel that holds the imagination"
- Fits: brand annual reports, slow-paced narratives, a small amount of important data, occasions that call for gravity
- Visual DNA: pure white or rice-paper white + very pale gray + one very small dot of ink or vermilion. Layout one data point per screen, vast whitespace, elements placed near the edge or at golden positions, never filling the frame. Signature elements: extreme whitespace, single-point emphasis, lines so fine they barely exist, an Eastern sense of interval.
- HTML implementation: pure CSS typesetting. 🔴 **the highest-risk style in this library** — the whitespace must be composition (with a clear visual anchor); push it too far and it reads as "the page failed to render"; body text still ≥14px — no shrinking the type for the mood
- Fonts: Noto Serif SC / Source Han Serif + Inter
- Specimen: assets/style-specimens/info/17-ma-emptiness.jpg

**Bookcraft Data (Irma Boom-style)** `Quiet · 80% fidelity`
- Reference: Irma Boom (Dutch book designer, work in MoMA's permanent collection, known for extreme typography and material experiments)
- Fits: long data reports, annual reports meant to be kept like publications, deep image-and-text content
- Visual DNA: paper color + one or two ink colors, color blocks pressing across whole pages. Type the typography itself as protagonist — an extreme size spread, asymmetric margins, text that can run vertical or rotated. Layout data embedded in the text flow, chapter pages separated by full-bleed color blocks. Signature elements: an asymmetric type area, extreme size spread, typographic experiments, the feel of a publication.
- HTML implementation: CSS multi-column + writing-mode for vertical setting; the asymmetric type area via Grid. **What can't be done is paper stock and trim**; on screen, typographic tension has to compensate
- Fonts: Fraunces / EB Garamond + Archivo (contrast)
- Specimen: assets/style-specimens/info/18-bookcraft-data.jpg

**Scientific Figure Plate** `Quiet · 96% fidelity`
- Reference: the figure conventions of Nature and Science, public scientific plates from the USGS and NASA
- Fits: research findings, method comparisons, rigorous data that needs a peer-review texture, multi-panel figures
- Visual DNA: white ground + a colorblind-safe palette (blue-orange contrast instead of red-green) + grayscale. Master layouts: subfigures labeled (a)(b)(c), captions as paragraphs beneath the figure, error bars and sample sizes always marked, axes with tick marks. Signature elements: panel numbers, long captions under the figure, error bars, colorblind-safe, zero decoration.
- HTML implementation: CSS Grid arranges the panels + SVG draws the plots and error bars; captions as small-type paragraphs. Zero assets — HTML handles it completely
- Fonts: Inter / Source Sans + Roboto Mono (figures)
- Specimen: assets/style-specimens/info/19-scientific-figure-plate.jpg

**Swiss Grid Report (Müller-Brockmann-style)** `Quiet · 97% fidelity`
- Reference: Josef Müller-Brockmann's *Grid Systems in Graphic Design*, the Ulm school, the Swiss International Style annual-report tradition
- Fits: corporate annual reports, institutional reports, document series meant to reuse one layout for years
- Visual DNA: white ground + black + a single accent. Layout a strict modular grid (often 12 columns), every element snapped to the column rules, flush left with a ragged right, generous breathing whitespace that never reads as empty. Signature elements: visible grid logic, the Helvetica family, non-centered setting, hierarchy through size and spacing rather than decoration.
- HTML implementation: CSS Grid maps straight onto the column grid — the most isomorphic with HTML in this library. Zero assets
- Fonts: Inter / Archivo (Helvetica substitutes)
- Specimen: assets/style-specimens/info/20-swiss-grid-report.jpg

---

## App Style Library (12 styles)

> New in 2026-10. Use this section when making App / mobile prototypes (before, you could only borrow from the web section, and the roulette drew landing-page styles). The specimen is a display board: two or three phone screens, with the composition itself as part of the demonstration (see "display board" in `references/app-prototype.md`).

#### Bold

**Hardware Panel (Teenage Engineering style — the interface language of the OP-1 / EP-133)** `Bold · 85% fidelity`
- Reference: Teenage Engineering OP-1 / EP-133 K.O. II (orange, black and gray palette, the "super segment hybrid display" hybrid dot-matrix screen, square keys and knobs laid out on a grid, silkscreen-style labels)
- Fits: audio/creation tools, samplers, metronomes, recording and hardware-companion apps, geeky little utilities
- Visual DNA: palette — near-black #0B0B0B screen + signal orange #FF5A1F + off-white #E9E9E4 keys, a light-gray #D8D8D4 faceplate with fine grid lines. Type — dot-matrix/monospace, numbers like LCD readouts, labels like silkscreen (all caps + wide tracking). Layout — a strict square grid: a 4×4 key array, round knobs with single-color pointers, faders with orange tick marks; the keys get their physicality from a "pressed-in thickness" (an inset 4px bottom-edge shadow). Signature elements: giant dot-matrix readouts, square keys, silkscreened small labels, exactly one accent color per screen — orange.
- HTML implementation: CSS Grid for the key array + aspect-ratio:1; knobs via radial-gradient + a pseudo-element pointer rotated in; faders as absolutely positioned bars; the dot-matrix font is Doto, falling back to Space Mono; the board background uses a repeating grid to imitate the faceplate. Keep orange for "currently active" only — don't flood the screen with it.
- Fonts: Doto (dot-matrix readouts) + Space Mono (labels); Chinese labels in Noto Sans SC
- Specimen: assets/style-specimens/app/01-hardware-panel.jpg

**Liquid Glass (Apple's new design language in iOS 26)** `Bold · 70% fidelity`
- Reference: Apple's Liquid Glass, announced at WWDC 2025 and shipping with iOS 26 / macOS Tahoe 26; Apple describes it as a translucent material that refracts the content around it and responds dynamically to touch, used across controls, navigation, icons and widgets
- Fits: native-feel weather/fitness/media apps, system-styled utilities, interfaces that want "content first, controls floating," concept demos
- Visual DNA: palette — decided by the background content itself: a high-saturation gradient ground (coral orange→magenta→indigo, or teal→mint) with the controls as translucent white glass. Type — the system sans, big numbers with tight tracking. Layout — content fills the screen edge to edge; controls (back button, tab bar, bottom panel) "float" over it as rounded capsules / big-radius panels, the tab bar a floating capsule rather than a full-width strip glued to the bottom. Signature elements: white gradient highlight strokes, top inner highlights, background blur + saturation boost, circular/capsular controls.
- HTML implementation: backdrop-filter:blur(22px) saturate(180%) + a translucent white gradient background + a 1px white stroke + inset highlight shadows — that's the core; the background must be a gradient with real color depth or the glass can't be seen — on a flat ground, glass reads as a gray block. Refraction and specular light effects are beyond CSS; they downgrade to highlight strokes, and the output must say so.
- Fonts: Inter (standing in for SF Pro) + Noto Sans SC
- Specimen: assets/style-specimens/app/02-liquid-glass.jpg

**Playful Tactile (the Not Boring series, Andy Works)** `Bold · 70% fidelity`
- Reference: the (Not Boring) app series (Andy Works, founders Andy Allen and Mark Dawson; Weather, Calculator, Timer, Habits); (Not Boring) Habits won a 2022 Apple Design Award; the signature is saturated color, tactile feedback and 3D animation — turning plain utilities into "bold, brash" experiences
- Fits: small utilities — timers/habits/weather/calculators; light tools for a young audience; apps that want one feature "fun enough to get screenshotted"
- Visual DNA: palette — one full-bleed saturated primary per screen (orange #FF7A2D, lavender #B6A2FF, acid green #D4FF3F) paired with near-black #1B1330 text. Type — chunky rounded giant numbers, tight tracking. Layout — one protagonist per screen (a giant dial / thermometer tube / switch) with everything else orbiting it; cards tilted slightly, screens staggered at different rotations. Signature elements: buttons with real thickness (a solid hard shadow on the bottom edge), raised dials with highlights, switches that visibly "press in."
- HTML implementation: layered box-shadow builds the thickness (a solid bottom edge + inner highlight + outer soft shadow), radial-gradient for spherical highlights, rotate for the stagger. A static image can only carry the material; haptics and motion exist in HTML as transitions only — label that honestly.
- Fonts: Bricolage Grotesque (800) + Noto Sans SC (900)
- Specimen: assets/style-specimens/app/03-playful-3d.jpg

**Friendly Fintech (Monzo style — high-saturation brand color + big corner radii)** `Bold · 90% fidelity`
- Reference: Monzo (brand primary Hot Coral, roughly #FF4F40, from the iconic translucent coral bank card; paired with deep navy #091723–#14233C, a rounded humanist sans, capsule buttons, conversational copy)
- Fits: personal bookkeeping, saving/budgeting, payments and transfers, finance products for young users, anything that needs to talk about "serious money" in a friendly voice
- Visual DNA: palette — coral red #FF4F40 laid large across the top + white rounded panels below; pots/categories in pastel blocks (yellow #FFD66B, blue #9AD8FF, green #C8F0CE, pink #F9B9E8, purple #D8CBFF). Type — a rounded geometric/humanist sans, balances in 58px+ bold. Layout — the colored top zone holds the balance and three capsule actions; the white panel below lifts up like a drawer; budgets are two columns of big-radius squares — the "pots." Signature elements: full-bleed brand color, 34px+ corner radii, capsule buttons, initial-letter/color-block icons, conversational subheads ("where the money went").
- HTML implementation: pure CSS reproduces it 1:1. border-radius:28~34px, a two-column grid, flat color blocks, progress bars as two-layer divs. The icons draw no literal pictures — a single letter on darker/lighter tints of the same hue.
- Fonts: Figtree (standing in for Monzo's own Monzo Sans) + Noto Sans SC
- Specimen: assets/style-specimens/app/04-friendly-fintech.jpg

**Pro Camera (Halide style — dark base + yellow accent + dense scales)** `Bold · 85% fidelity`
- Reference: Halide (Lux Optics, an Apple Design Award winner; an interface designed for one-handed operation and inspired by the controls of professional camera bodies; its custom typeface Ambrotype imitates the etched lettering on film-camera bodies; it offers pro views like histogram, waveform, colored zebras (the highlight-clipping warning), and focus peaking)
- Fits: pro tools — camera/recording/measurement/oscilloscope; interfaces that need "read the numbers at a glance, adjust one-handed"; apps used in low light
- Visual DNA: palette — pure black #000 ground + bright yellow #FFCC00 accent (reserved for "the currently selected parameter" and the center scale line) + gray-white #EDEDED readouts. The yellow is this entry's own orientation, not a claim about Halide's actual palette. Type — monospace digits, parameter labels small with wide tracking. Layout — viewfinder up top, the bottom fixed as "parameter row (shutter/ISO/exposure/white balance) + horizontal scale + shutter button"; the scale fades out at both ends with one yellow line at center. Signature elements: dense ruler scales, zebra-stripe highlight warnings, the translucent histogram, exactly one yellow focal point per screen.
- HTML implementation: repeating-linear-gradient draws the ticks (short ticks 2px/14px, long ticks 2px/70px in two layers), mask-image fades the ends; zebra stripes as a repeating-linear-gradient at 135deg; the viewfinder zone is a gradient placeholder marked "photo goes here." Keep yellow to three places at most.
- Fonts: JetBrains Mono (digits and scales) + Noto Sans SC (labels)
- Specimen: assets/style-specimens/app/05-pro-camera.jpg

#### Neutral

**Topo Outdoor (Gaia GPS / AllTrails-style contours and tracks)** `Neutral · 90% fidelity`
- Reference: Gaia GPS (known for the contour-and-hillshade Gaia Topo basemap); AllTrails (its trail pages put distance, difficulty and elevation gain first)
- Fits: hiking/cycling/trail-running routes, outdoor logging, camping and map tools, mobile interfaces that need "the map as protagonist"
- Visual DNA: palette — parchment #EFEBDA ground + contour brown #C09A68 (every fifth line bolded as an index contour) + light woodland green #D8E4C4 + pale water blue #BFDDE6, tracks in high-contrast orange-red #E4572E with a white casing. Type — condensed digits (big readouts) + a Chinese sans. Layout — the map fills the screen, a white panel at the bottom holds three big numbers — distance/elevation gain/time — and the elevation profile; every list card carries a mini contour thumbnail + a difficulty color chip (yellow/green/red). Signature elements: contours, white-cased track lines, the elevation-profile area chart, difficulty color chips.
- HTML implementation: SVG paths draw the contours (nested irregular closed curves, index contours with a heavier stroke), the track as two path layers (a thick white line under a thin orange one); the board background carries the same set of contours. The contours must be irregular curves — concentric circles/ellipses read as fake at a glance.
- Fonts: Barlow Condensed (readouts) + Noto Sans SC
- Specimen: assets/style-specimens/app/06-topo-outdoor.jpg

**Feed Waterfall (Xiaohongshu-style two-column card stream)** `Neutral · 92% fidelity`
- Reference: Xiaohongshu's home-page "Explore" two-column waterfall (cards staggered at their true aspect ratios — image on top, a two-line title, author and likes below; channel tabs at the top; the bottom nav with a red plus in the middle)
- Fits: content communities, discovery/guide/local-review apps, e-commerce content feeds, any Chinese product whose decision entry is "cover image + title"
- Visual DNA: palette — white cards #FFF on a light-gray ground #F5F5F7; brand red #FF2442 reserved for the selected underline, the plus button, "follow," and the liked state. Type — the system Chinese sans, titles 15px, clamped to two lines. Layout — two columns, a 6px gutter, cards with 10px radii; cover ratios all different (about 1:1 to 3:4) for the stagger; a fixed row at the card bottom — author avatar + handle + like count. Signature elements: staggered cover heights, two-line titles, the avatar+handle+likes row, the red plus.
- HTML implementation: flex with two columns, each flex-direction:column, cards flex:none; covers are gradient placeholders of different heights labeled "photo goes here"; titles use -webkit-line-clamp:2; avatars are initial-letter dots, no portraits drawn.
- Fonts: Noto Sans SC
- Specimen: assets/style-specimens/app/07-feed-waterfall.jpg

**Command Palette (Raycast-style)** `Neutral · 90% fidelity`
- Reference: Raycast (near-black ground around #07080A, 1px hairline borders around #242728, Inter body with monospace keycaps; commands marked by small solid-color icons, shortcuts right-aligned; hierarchy through tonal steps rather than shadows)
- Fits: developer tools, productivity tools, command-line companion apps, internal ops panels, any product where "search is the action"
- Visual DNA: palette — near-black #07080A canvas + panels #121315 + selected row #202225; command icons as saturated little color blocks (red #FF6363, blue #52A9FF, green #59D499, purple #8A63F5, yellow #FFC531). Type — Inter body + monospace keycaps/logs. Layout — an input field at the top (the cursor a red bar), below it a single-line list grouped by "suggestions/commands," each row: small color-block icon + name + gray subtitle + right-aligned keycap; a fixed action bar at the bottom ("open command ↵" / "more actions ⌘K"). Signature elements: gradient keycaps, group subheads, the selected row's light-gray highlight, the bottom action bar. Raycast itself is a desktop app; the specimen renders it as "a crop of the desktop panel + a phone adaptation."
- HTML implementation: flex rows + hairline borders; keycaps get a gradient background + a darker border-bottom + a 0 2px 0 shadow; no big shadows anywhere — one deep drop shadow on the outer layer only.
- Fonts: Inter + JetBrains Mono (keycaps and logs) + Noto Sans SC
- Specimen: assets/style-specimens/app/08-command-palette.jpg

**Health Color-Code (Apple Health / Oura-style)** `Neutral · 92% fidelity`
- Reference: Apple's Health/Activity rings (three concentric rings — red, green, blue — on a black ground, for Move, Exercise and Stand); Oura (Readiness/Sleep/Activity as three 0–100 scores; blue means on track, yellow so-so, red needs attention)
- Fits: health/sleep/fitness/vitals products, any dashboard that compresses a pile of metrics into "how was today," companion apps for wearables
- Visual DNA: palette — pure black #000 ground + cards #1C1C1E; status-semantic colors (blue #3498FF best, yellow #FFCC00 middling, red #FF453A attention) and ring colors (#FA114F, #92E82A, #1EEAEF). Type — huge bold scores (76px+) + small gray labels. Layout — one big ring/score as the protagonist at top, cards below: component bars, sleep-stage columns, a trend line riding a normal-range band; beside each figure a small status pill (good / low / high). Signature elements: ring progress, status pills, the translucent "normal range" band, color as the conclusion.
- HTML implementation: SVG circle + stroke-dasharray for the rings (the track is the same hue at low brightness); bars as two-layer divs; the range band a translucent rect; status pills = translucent ground + same-hue text. In one screen, keep the status colors and ring colors in separate lanes — don't blend them into a rainbow.
- Fonts: Inter + Noto Sans SC
- Specimen: assets/style-specimens/app/09-health-color-code.jpg

#### Quiet

**Native Polish (Things 3 style, Cultured Code)** `Quiet · 95% fidelity`
- Reference: Things 3 (Cultured Code, Stuttgart, Germany; two Apple Design Awards; the site quotes a review calling its interface "like a clean, crisp sheet of paper"; "Today" has a "This Evening" section, lists can take titled separators, tasks expand into cards, and the draggable Magic Plus button sits in the bottom-right corner)
- Fits: native productivity apps — tasks/to-dos/notes/calendars; personal tools in heavy daily use; products chasing "no fatigue even after long use"
- Visual DNA: palette — pure white #FFF + near-black text #1D1D1F + one blue #3478F6 (only for checkmarks, links and the plus button); a yellow star #F6C21B for "Today"; gray #8A8F9B for secondary information. Type — the system sans, large titles 32px bold with tight tracking. Layout — lists dominate, an indented hairline between rows (starting right of the checkbox), group titles in small bold + underline; a task expands into a floating card with a large shadow holding notes, checklists, tags and deadlines. Signature elements: the rounded-square checkbox, indented hairlines, the "This Evening" moon section, floating task cards, the blue circular plus.
- HTML implementation: pure CSS covers it. Checkboxes as border:2px + border-radius:7px, the completed state a gray fill + a pseudo-element check; row separators via a left-indented :after; task cards with two shadow layers (0 2px 6px + 0 26px 60px). Motion (expanding, checking) can't show in a static image — build the structure only.
- Fonts: Inter (for an iOS feel it may drop to the system stack) + Noto Sans SC
- Specimen: assets/style-specimens/app/10-native-polish.jpg

**Gentle Encouragement (Gentler Streak style, dark variant)** `Quiet · 80% fidelity`
- Reference: Gentler Streak (Gentler Stories, Slovenia; winner of the 2024 Apple Design Award in the Social Impact category; it stresses personal progress over comparison with others, and its core visual is the "Activity Path" — the day's state rendered as a range from "rest" to "active," in soft blue-green tones). Note: the officially described main interface is bright and airy; this entry's deep-night blue ground is a dark variant built on its soft blue-green, rounded, non-judgmental tone
- Fits: fitness/recovery/sleep/mindfulness apps; habit products for people who "give up easily"; anywhere that wants to turn "falling behind" from guilt into understanding
- Visual DNA: palette — a deep-night blue gradient #18213A→#202C4A, cards #26335A, accents in soft mint #9BE0CC, lavender #BAC3FA, peach #F4D0A8 (all three low-saturation pastels). Type — a rounded sans; big headlines use suggestion phrasing like "today is a good day for…", never "X% completed." Layout — nothing but 28px-radius cards stacked vertically; the core card is a round-capped gradient curve path + one white location dot; the monthly view is a dot calendar with rest days in peach — the streak never shown broken. Signature elements: round-capped curve paths, pastel status pills, dot calendars, copy in the spirit of "the streak isn't broken — rest is part of the plan."
- HTML implementation: SVG path for the path (a dark base track + a gradient stroke above, cut with stroke-dasharray); the dot calendar via grid + border-radius:50%. The key is the tone of the copy: statements and suggestions throughout — no red, no exclamation marks, no rankings.
- Fonts: Nunito (rounded) + Noto Sans SC
- Specimen: assets/style-specimens/app/11-gentle-encouraging.jpg

**Editorial Reader (Matter / Readwise Reader-style)** `Quiet · 90% fidelity`
- Reference: Matter (about ten reading typefaces including New York, Valkyrie, Lyon and Literata, multiple themes; a queue home page with restrained spacing and type sizes; press-and-drag to highlight); Readwise Reader (double-tap a paragraph to highlight; highlights and notes stay in sync)
- Fits: read-it-later, long-form reading, notes and highlight management, podcast/article aggregation, any content product whose goal is "finished reading"
- Visual DNA: palette — warm paper white #FBF8F1 + ink black #26221C + one ochre red #B5532A (source names, progress bars, settings values); highlights in highlighter yellow #F4D35E. Type — serif body (18px/line-height 1.85), UI labels in small sans + wide tracking. Layout — the reading queue is pure-text entries — source/duration, serif title, two-line summary, one thin progress line, no thumbnails; the reading page is a narrow centered column where selecting text floats up a small dark tool bar (highlight/note/copy); a highlight can be expanded on its own into a card with notes. Signature elements: serif titles, highlighter-style underline highlights, the dark selection tool bar, thin progress lines.
- HTML implementation: mark with linear-gradient(transparent 12%, yellow 12%, yellow 92%, transparent 92%) to imitate a highlighter — closer to a hand-drawn sweep than a flat background color; white-space:nowrap on the tool bar so a long Chinese label doesn't wrap it into a vertical stack; serif Chinese in Noto Serif SC
- Fonts: Literata + Noto Serif SC (body), Inter (labels)
- Specimen: assets/style-specimens/app/12-editorial-reader.jpg

---

## Chinese & East Asian Design (12 styles)

> New in 2026-10. A cross-medium section: web pages, decks, posters, covers, infographics — all can use it, and each style's "Fits" line says what it suits. Every seconds-roulette spin draws one style from here in addition to the one it draws from the section matching the output form. Chinese-language content especially deserves a flip through this section: Western references applied to a Chinese layout usually leave nothing but the color scheme.

> The premise of this section: Chinese layout has its own grammar — vertical setting, the type area, column rules, title slips, Hanzi structure — it is not "Western style + swap in a Chinese font". Usage is the same as the other sections: open the specimen first, run the color derivation protocol first.
> Fidelity notes: handwritten title slips, aged paper, real photographs, the texture of lead type or woodblock prints — pure HTML/CSS can't do any of these; all get the honest-downgrade treatment, spelled out in each style's "HTML implementation" line.
> Fact-checking: designers and works appear only where a source was verified; each style's "Visual DNA" is a synthesis of that style's layout language, not a pixel-by-pixel description of any single page.

**Lü Jingren Bookcraft** `Quiet · 85% fidelity`
- Reference: Lü Jingren (吕敬人) (Chinese book designer, called the "master of the book jacket"); *Zhu Xi's Thousand Character Classic* (《朱熹千字文》, paper texture carrying the breath of a stele rubbing), *China Memories: Treasures of 5,000 Years of Civilization* (《中国记忆——五千年文明瑰宝》, honorable mention at Best Book Design from All Over the World 2009), *Elegant Objects in the Sleeve: Suzhou Folding Fans* (《怀袖雅物——苏州折扇》, China's Most Beautiful Book 2010). He treats book design as a systems project in dialogue with the text — editing, binding, and printing working as one — not just a cover.
- Fits: art-book/annual-report spreads, long-form feature pages, oral history and archival content, exhibition catalogs, deep content that asks to be "read slowly"; on the web it suits long-form reading pages, in decks it suits chapter title pages
- Visual DNA: warm paper base (around #F4EFE4), deep ink-black body text, **cinnabar red used in exactly one place** (one large character or one seal). The signature layout move is "letting the type area breathe": the type area isn't centered — it rides high and hugs the gutter, head margin small, foot margin very large; a narrow margin-note column along the fore-edge carries annotations; a chapter title page carries one large character plus one line of title, everything else whitespace. A gradient at the gutter simulates the dent of the binding. Line-height above 2; page numbers and running heads tiny.
- HTML implementation: CSS Grid/absolute positioning lays two 560px pages side by side, the gutter gets a linear-gradient shadow running dark to light; the margin-note column is its own absolutely positioned column; the cinnabar seal is a solid color block + one character. Paper fibers, foil stamping, slipcases, physically turning pages can't be done — downgraded to flat paper color + shadow.
- Fonts: Noto Serif SC (Chinese headings, body; Latin and digits also use its built-ins) + Noto Sans SC (small text like running heads and margin-note labels)
- Specimen: assets/style-specimens/east/01-lu-jingren-bookcraft.jpg

**Song Block-Print Leaf** `Quiet · 80% fidelity`
- Reference: the leaf format of Song dynasty woodblock editions — the frame (Northern Song mostly double-ruled left and right; Southern Song gradually adds a thin black fold line and ear tabs), the ruled column grid, the fish-tail marks in the center seam (Southern Song sees single black, double black, and floral fish tails) carrying the short title and leaf number; Zhejiang editions neat and orderly, Sichuan editions stately and vigorous in letterform with airy pages; book collectors' vermilion collations as the layer old books commonly carry.
- Fits: observation/archival/source-document content pages, a research report's "raw record" pages, content pages for culture brands, a deck's quote pages, features that need an "ancient-book feel"
- Visual DNA: one full leaf centered, framed on all four sides with a border thick outside and thin inside (double outside single inside, or thick outside thin inside), vertical text with a thin rule between columns; the center seam (the central strip) sits mid-leaf, black fold lines above and below with an inverted-triangle fish tail between them, the abbreviated title and leaf number set vertically, the carver's name at the bottom; paper a faint yellow (around #EDE0BC) + ink black; **vermilion annotations** as small red characters set vertically in the head margin, a red ring beside key sentences (doable with text-emphasis). No ornament anywhere on the leaf — every bit of information lives inside the rules.
- HTML implementation: writing-mode:vertical-rl with one div per column, a row-reverse flex to guarantee right-to-left reading; column rules via border-left; the fish tail via a clip-path triangle; the red ring via text-emphasis. Uneven ink density from the carving, irregular stroke weights, damaged paper can't be done — downgraded to uniform ink and a pale yellow paper tone.
- Fonts: Noto Serif TC (traditional-character woodblock body text, the closest skeleton to a Song cut); simplified content uses Noto Serif SC. English barely appears; if needed, stay in the body family
- Specimen: assets/style-specimens/east/02-song-block-print.jpg

**Republic-Era Book Jacket** `Neutral · 70% fidelity`
- Reference: book and magazine covers from the generation of Lu Xun (鲁迅) and Tao Yuanqing (陶元庆). Tao Yuanqing designed for Lu Xun *Wandering* (《彷徨》, 1926), *The Grave* (《坟》), *Dawn Blossoms Plucked at Dusk* (《朝花夕拾》), *Tales of the Tang and Song* (《唐宋传奇集》), and more; Lu Xun designed covers himself too (e.g. *Call to Arms* (《呐喊》)), mostly type-driven, spare and understated.
- Fits: book covers and flat-lay book spreads, covers for albums/script collections/travelogues, the hero of a culture landing page, exhibition posters, cultural-creative packaging
- Visual DNA: low-saturation earthy-yellow/gray-green paper base, ink black + a touch of vermilion — three colors in all; a **white title slip** pasted on the cover, the book title set vertically; a fine double-line border around it; motifs are flat-filled geometric shapes (mountains, sun, water ripples), not realistic, with hatching; large areas of whitespace; cover, spine, and back cover laid out flat.
- HTML implementation: flex lays out back cover/spine/front cover as three columns; the double-line frame via border + pseudo-elements; the title slip a light block with a fine border; motifs via SVG geometric polygons and lines. **A handwritten title slip can't be done** — downgraded to LXGW WenKai (a handwritten kai); aged paper, foil stamping, misregistered color layers can't be done — downgraded to flat paper color.
- Fonts: book titles and title slips in LXGW WenKai (alternative: Ma Shan Zheng, heavier and rougher-brushed); authors and captions in Noto Serif SC; English barely appears
- Specimen: assets/style-specimens/east/03-republic-book-jacket.jpg

**Shanghai Moderne Deco** `Bold · 78% fidelity`
- Reference: yuefenpai — the calendar-poster advertising paintings that rose in late-Qing Shanghai and peaked in the 1920s–30s; representative painters include Zheng Mantuo (郑曼陀), Hang Zhiying (杭穉英), and Xu Yongqing (徐咏青), working in "carbon-dust watercolor"; Shanghai's Art Deco of the 1930s–40s was read as "modeng" (摩登, moderne), shaping architecture and commercial art.
- Fits: posters, brand promotion pages, coffee/tea/food packaging and campaign pages, retro-themed landings, calendars and seasonal materials
- Visual DNA: deep ink-green #17352F + gold #C9A24A + vermilion #9E2A1D + cream paper; symmetric geometry of **radiating fans (suns) + stepped ziggurat towers**; a double frame (gold outer + dark inner line); headlines in heavy display lettering with solid offset shadows; a **calendar** panel embedded on the right (a yuefenpai is, at heart, an ad + a calendar); a vermilion strip across the bottom carrying the shop name and address.
- HTML implementation: SVG draws the fans, concentric circles, and stepped rectangles; the headline gets its offset solidity from text-shadow; the calendar is a seven-column CSS Grid. The carbon-dust watercolor portraits and textures unique to yuefenpai can't be done (portraits shouldn't be drawn in SVG anyway) — downgraded to pure geometry + flat fills; a geometrized coffee cup stands in for the human figure.
- Fonts: ZCOOL XiaoWei (display lettering for headlines) + Noto Serif SC 900 (subheads) + Noto Sans SC (calendar and small text, with Latin digits riding along in it; for a stronger Deco flavor, swap the Latin to Josefin Sans)
- Specimen: assets/style-specimens/east/04-shanghai-deco-calendar.jpg

**Experimental Hanzi Poster** `Bold · 85% fidelity`
- Reference: the lineage of contemporary Chinese graphic designers building layouts out of Hanzi structure. Two verified: Han Jiaying (韩家英) (b. 1961 in Tianjin, AGI member; his early posters systematically present his understanding of Hanzi "from stroke to structure, from character to page, from surface to space"; work held by the V&A and others); Kan Tai-keung (靳埭强) (b. 1942, Hong Kong, fusing Hanzi form with ink wash; the Bank of China logo takes its image from an ancient coin). The common thread of this lineage: treating Hanzi as structural material that can be taken apart.
- Fits: exhibition/event posters, brand manifesto pages, deck covers or section pages, the hero of a feature long-image, course covers
- Visual DNA: **one character blown up to fill half the frame**, broken by stroke into independent geometric blocks, some strokes displaced or swapped for a slash of high-saturation color (vermilion #E4351E); on the right, small stroke-breakdown diagrams (strokes numbered 1–5) make the "taking apart" legible; black + paper white + one accent color, everything else the fine rules and small type of the info column; the title is a heavy sans, emphasis words switch color.
- HTML implementation: each stroke is hand-built from SVG rects/paths, so the letterform is your own construction (confirm the stroke count and stroke order are correct first); the breakdown diagrams reuse the same paths with a single stroke highlighted. Complex characters don't suit this — pick ones with 4–6 strokes.
- Fonts: Noto Sans SC 900 (titles) + Noto Serif SC (the lead-in); the giant character uses no font — it's built from geometric blocks
- Specimen: assets/style-specimens/east/05-hanzi-experimental-poster.jpg

**Hong Kong Street Signs** `Bold · 80% fidelity`
- Reference: the visual language of Hong Kong's handwritten and neon signs. The 1940s–70s favored sign lettering in the "Beiwei" style (北魏体) — square forms with crisp entries, exits, and turns — popularized by calligraphers such as Au Kin-kung (区建公), Su Shijie (苏世杰), and Cheuk Siu-hang (卓少衡); signs are often vertical, stacked and packed, mixing Chinese and English; the Hong Kong Neon Signs archive has documented 400+ surviving neon signs since 2015.
- Fits: retail/F&B/record store/night market brand pages, event posters, promo landing pages, urban nightlife features, the deck pages that need a "live on the street" feel
- Visual DNA: a midnight wall as the base, signs **stacked floor upon floor** on a building: one vertical sign pinning the next, horizontal signs layered one on another; each sign a high-saturation solid ground (red, yellow, blue, green — this palette is a synthesis of night-scene signage, not sourced sign by sign) framed in cream white with an outer glow; lettering in heavy traditional sans with hard drop shadows; one small red LED board; a handwritten chalkboard price list at the bottom; power lines crossing the frame. Dense information, big type, signs occluding one another.
- HTML implementation: absolutely positioned block by block; box-shadow for the lightbox glow, text-shadow for hard lettering shadows, writing-mode:vertical-rl for vertical signs. Real Beiwei brushwork and the bends of neon tubes can't be done — downgraded to heavy Noto Sans paired with Noto Serif display weights.
- Fonts: Noto Sans TC 900 (heavy traditional sans for vertical and small signs) + Noto Serif TC 900 (main titles on horizontal signs) + Archivo Black (English subheads)
- Specimen: assets/style-specimens/east/06-hk-street-signs.jpg

**Traditional Chinese Colors · Solar-Term Palette** `Neutral · 90% fidelity`
- Reference: *Traditional Colors of China: The Aesthetics of Color in the Forbidden City* (《中国传统色：故宫里的色彩美学》, by Guo Hao (郭浩) and Li Jianming (李健明); the table of contents follows the four seasons, 384 traditional colors collected, plus a set of 24 solar-term color cards); the Beginning of Spring maps to traditional color names such as piaobi (缥碧, pale jade blue), huangbaiyou (黄白游, drifting yellow-white), songhua (松花, pine pollen), xiangye (缃叶, pale leaf yellow), and haitianxia (海天霞, sea-sky sunset glow).
- Fits: web heroes, seasonal/time-based products, a deck's contents page, travel and outdoors content, brand palette pages, infographics with a built-in timeline
- Visual DNA: the whole palette organized by **traditional color names**, not "red green blue": 24 vertical color bars running across the bottom of the page, each labeled with its solar term and color name; the bar of the current solar term rises, widens, and becomes the accent color of the whole page; body content on a warm paper base + ink, with pattern restrained to almost nothing. "Solar term = navigation" is the layout move unique to this style.
- HTML implementation: flex splits 24 equal color bars, the current one gets flex:1.6 + extra height; text picks dark or light automatically per the bar's luminance. The hex values are approximations of each color name (sources differ slightly on the hex for the same name) — in a real project, go by the colors you source yourself; don't treat this as a standard color card.
- Fonts: Noto Serif SC (titles, color names, body) + Noto Sans SC (nav, small labels)
- Specimen: assets/style-specimens/east/07-traditional-colors-solar-terms.jpg

**Sugiura Information Mandala** `Bold · 72% fidelity`
- Reference: Kohei Sugiura (杉浦康平) (b. 1932, Tokyo; Japanese graphic designer and researcher of Asian imagery). His research centers on mandalas and Asian cosmology; he calls the world of traditional Asian imagery one of "all things reflecting one another" (万物照应); he has designed some 5,000 books, including about 1,700 covers for Kodansha's Gendai Shinsho (现代新书) paperback series; his *Time-Distance Map* diagram experiments and his "Mandala" exhibition (1980).
- Fits: infographics, event posters, annual/cyclical data pages, popular-science features, a deck's overview page
- Visual DNA: **a concentric ring chart centered** — the outer ring carries solar terms and tick marks, the middle ring colored sectors, the inner ring small moon-phase circles, and at the center one red dot; around it, numbered dots with leader lines and captions, a large vertical title, and a time-distance map — high information density, but every block maps to a position on the disc. Palette: near-black warm base + gold + vermilion + off-white. Vertical and horizontal setting coexisting is a common Asian layout (this point is a synthesis; no page-by-page source found this time).
- HTML implementation: a script generates the SVG sectors, tick marks, and text rotated along the circumference; captions absolutely positioned, leader lines as SVG paths. Sugiura's overprints, special inks, and designs that run across the book spine can't be done — downgraded to flat color fills.
- Fonts: Noto Serif SC (the large vertical title and text on the rings) + Noto Sans SC (captions and the time map)
- Specimen: assets/style-specimens/east/08-sugiura-info-mandala.jpg

**Ikko Tanaka Geometric** `Neutral · 90% fidelity`
- Reference: Ikko Tanaka (田中一光) (1930–2002). He fused Japanese tradition with the International Style; the *Nihon Buyo* (Japanese Dance) poster (1981 — a geisha's coiffure and face built from squares and rectangles on a grid) is the signature work; from 1973 he designed posters for the Seibu Theatre, from 1975 he was creative director of the Seibu Group, and from 1980 he helped found MUJI and long led its visual identity; the style draws on Rinpa (琳派).
- Fits: exhibition/film-festival/performance posters, brand manifesto pages, deck covers, cultural institutions' web heroes
- Visual DNA: **squares, circles, and quarter-circles on a grid** assembled into an abstract hero image, red #D9381E / black / mustard yellow / a touch of steel blue on a rice-paper ground; a large vertical title in heavy Song serif; on the right, information grouped under small red labels ("Dates / Venue / Theme / Tickets"); a thin black rule at the bottom. Fans, the round sun, and stripes (theater curtains) are traditional motifs transcribed into geometry.
- HTML implementation: a 560px square grid on a 70px unit; quarter-circles and semicircles via border-radius; stripes via repeating-linear-gradient. Silkscreen color registration and paper grain can't be done — downgraded to flat fills.
- Fonts: Noto Serif SC 900 (the large vertical title) + Noto Sans SC (info) + Zen Kaku Gothic New (small English text)
- Specimen: assets/style-specimens/east/09-tanaka-geometric-poster.jpg

**Hattori Playful Offset** `Bold · 75% fidelity`
- Reference: Kazunari Hattori (服部一成) (b. 1964, Tokyo; art director and professor at Tama Art University). Representative work includes the Kewpie Half ads, art direction of *Ryūkō Tsūshin* (《流行通信》), and the Mitsubishi Ichigokan Museum logo; he received the Yusaku Kamekura Award in 2004; one signature device is **replacing the print halftone dot with stripes** (from his 2007 "Flag" poster on).
- Fits: posters, covers, event and media brand pages, weather/lifestyle content that should feel "not serious but very deliberate"
- Visual DNA: one character set enormous, filled with two layers of **horizontal stripes** in different colors and offset by a few pixels (like a misregistered overprint) — the stripes themselves are the texture; beside it, tilted solid blocks (yellow, black, a coral-red circle) and one thick hand-drawn wavy line; title characters feel handwritten, each riding higher or lower than the last; the info column, by contrast, is set dead straight. The playfulness concentrates in one place and doesn't spread.
- HTML implementation: the giant character gets its stripes from background-clip:text + repeating-linear-gradient, duplicated on a shifted layer; the blocks rotate; the thick line is SVG stroke-linecap:round. True brushwork and ink overprint can't be done — downgraded to round-capped thick lines and offset stripes. Pick a low-stroke-count character for the giant one (水 "water", 山 "mountain", 云 "cloud"); complex characters turn to mush.
- Fonts: Noto Sans SC 900 (giant characters and digits) + ZCOOL KuaiLe (playful titles) + Noto Sans SC (info column)
- Specimen: assets/style-specimens/east/10-hattori-playful-offset.jpg

**Sato Minimal Symbol** `Neutral · 92% fidelity`
- Reference: Kashiwa Sato (佐藤可士和, creative director). His 2006 rebrand of UNIQLO: a red square + heavy white lettering + katakana, red and white chosen to evoke the Japanese flag; he was also art director of the Cupnoodles Museum. His claim: a brand needs one strong symbol (as compiled from a Design Singapore interview).
- Fits: brand launch pages, product landings, deck covers, app splash screens, startup homepages' heroes
- Visual DNA: **one character (or one symbol) takes half the page**, a solid color full-bleed (around #E60012); the other half pure white, an info zone with almost no ornament; headlines in heavy sans; a small four-color swatch block (red/black/white/blue) hinting at the system; data rows divided by thick top rules in three colors. At most three colors on the page.
- HTML implementation: two columns, flex-centered giant character; zero images, zero gradients. Almost nothing to downgrade — the difficulty is restraint, not implementation.
- Fonts: Noto Sans SC 900 (Chinese headlines and logotype characters) + Archivo 800/900 (Latin and digits)
- Specimen: assets/style-specimens/east/11-sato-minimal-symbol.jpg

**Japanese Lifestyle Magazine Dense** `Neutral · 78% fidelity`
- Reference: POPEYE (founded 1976, Magazine House, subtitle "Magazine for City Boys") and BRUTUS (founded 1980); both magazines' logos came from art director Seiichi Horiuchi (堀内诚一) — POPEYE's logo was his 1976 design, and through the 70s he did every single issue. Horiuchi was also the art director of an・an.
- Fits: annual-report/data-feature spreads, city and lifestyle content, a deck's data pages, guide-and-checklist long images, infographics
- Visual DNA: black on white, **high-density diagrams**: the left page carries a big headline (yellow marker underline) + a route map with numbered dots and **handwritten red/blue pen annotations**; the right page is a 3×3 data grid (heavy black rules, one or two cells accented yellow or black) + a heatmap + a how-to-read note; running heads and page numbers in condensed Latin, spanning both pages. The "handwritten annotations + diagrams" trait is a synthesis of this kind of page; no page-by-page source was found — don't take it as a reproduction of any particular POPEYE issue.
- HTML implementation: two 600px pages side by side; CSS Grid for the data cells, SVG for the route map, the heatmap a 24×7 Grid of cells. The real magazine's photo collages and halftone dots can't be done — photo slots are honestly marked out with color blocks.
- Fonts: Noto Serif SC 900 (big headlines) + Noto Sans SC (body and data) + Long Cang (handwritten annotations) + Archivo Narrow (running heads, page numbers, big data digits)
- Specimen: assets/style-specimens/east/12-japan-magazine-dense.jpg

---

## Xiaohongshu Image-Text (8 styles)

> New in 2026-10. A set of 3:4 vertical images (1242×1660, at most 18) read by swiping sideways, the first image being the cover. For usage, see `references/modules/xiaohongshu.md`. The source is one real post: "open-sourced bird stickers" was produced as all eight of these versions, and the specimens are that set's cover + one inner page — so the subject is identical across all eight; what's borrowed is the layout.
> Every specimen doubles as a template: `assets/style-specimens/xhs/<number>.html` opened at 1200×750 is the specimen view; opened at true size, hand it to `scripts/xhs_render.py` to slice into pages. Type sizes follow the floors for a 1242-wide canvas (body ≥42px, labels ≥32px) — when you swap in real content, don't shrink below them.
> The sample colors are the Mingji (鸣迹) app's paper white, ink black, and sun yellow; for a real job, run the color derivation protocol and take colors from the user's brand or content.

**Specimen Journal** `Neutral · 90% fidelity`
- Reference: the grammar of natural-history plates and nature-magazine covers: a fine-rule masthead, oversized serif digits, one hero specimen taking half the page, a sidebar of small data
- Fits: nature, popular-science, and culture long-form; knowledge notes that need authority and a magazine feel
- Visual DNA: dot-grid paper base; an extra-large Song-serif title; one 300px-class high-contrast serif digit as the protagonist of the layout; the hero sticker sits underneath the digit and breaks out of the column rule; two or three sidebar entries of "big number + two-line caption"; inner pages use a numbered list + same-numbered dots marked on the hero, with a scale ruler giving positions
- HTML implementation: everything absolutely positioned; numbered dots via CSS counters; the scale ruler is one thin line plus two absolutely positioned markers. No downgrades
- Fonts: Noto Serif SC 900 (titles and small digits) + Bodoni Moda (only for digits above 100px) + Noto Sans SC (body)
- Specimen: assets/style-specimens/xhs/01-specimen-journal.jpg

**Product Notebook** `Neutral · 95% fidelity`
- Reference: the product's own interface (here: the Mingji app's paper surface, capsule buttons, and stickers); Xiaohongshu-native journals and collage notes
- Fits: your own product, app, or brand content — for when readers should recognize "that's the thing" at one glance; friendly, collectible
- Visual DNA: the app's paper and dot grid serve directly as the base; black capsules as labels and step numbers; a 2×3 sticker grid with names; a white card slightly rotated, a strip of translucent tape carrying the big title; the inner page is a white-card "review checklist" — checkbox rows + a ring score + two number cards
- HTML implementation: absolutely positioned cards + drop-shadow warm-brown shadows; the tape is a translucent color block. No downgrades
- Fonts: Figtree 900 (digits) + Noto Sans SC 700/900 (Chinese)
- Specimen: assets/style-specimens/xhs/02-sticker-notebook.jpg

**Index Ink** `Bold · 95% fidelity`
- Reference: Swiss-style index pages and data annual reports: an ink ground, one monochrome accent, an even grid, numbered rows
- Fits: numeric conclusions, rankings, lists, comparisons; a cover that has to stand out from afar in the feed
- Visual DNA: the cover on an ink ground, a 340px yellow digit taking the upper part, small images laid into a 5×3 hairline grid below; the inner page on paper, one giant black digit + two lines of title, numbered table rows, and at the bottom a proportion bar — part solid, part hatch-filled
- HTML implementation: CSS Grid for the grid; hatching via repeating-linear-gradient; the proportion bar flexed by real values. No downgrades
- Fonts: Figtree 900 + Noto Sans SC 900
- Specimen: assets/style-specimens/xhs/03-index-ink.jpg

**Panorama Strip** `Bold · 90% fidelity`
- Reference: horizontal handscrolls and continuous picture books; the "several images joining into one picture" swipe experience of a Xiaohongshu carousel
- Fits: content that lines up in a row: a set of objects, a timeline, a pipeline, a route — made to keep people swiping right the whole way
- Visual DNA: three images are one picture, one through-running power line (or horizon) linking them all; the protagonist straddles the seam, about 2/3 showing on the left image, about 1/3 on the right; each image carries its own big digit or title and holds up on its own; page numbers are just 01 02 03
- HTML implementation: one 3726px-wide `.xhs-strip`; `XHS.wire()` draws the line as a cosine curve (the period spans two images, the low point never lands on a seam), `XHS.perch()` stands the sticker on the line at its claw position; `xhs_render.py` auto-slices the pages and checks for text crossing a seam. The sticker's claw position has to be measured by hand once
- Fonts: Figtree 900 + Noto Sans SC 700/900
- Specimen: assets/style-specimens/xhs/04-panorama-strip.jpg

**Daily Paper** `Neutral · 80% fidelity`
- Reference: a newspaper front page: masthead, double rules, headline, column-set body text, drop cap, halftone grayscale photo, a news-in-brief box
- Fits: "event" content: launches, retrospectives, deep method write-ups, year-end summaries
- Visual DNA: newsprint ground with fine noise; a Song-serif masthead with wide letter-spacing; a double rule separating masthead from body; one digit in the headline swept through with a yellow highlighter; images desaturated and contrast-boosted; a body column with a drop cap; the inner page carries a boxed big score, with a row of small grayscale images as diagrams at the bottom
- HTML implementation: the noise is an inline SVG feTurbulence background; halftone images are approximated with grayscale + contrast filters — true halftone dots can't be done; the drop cap is ::first-letter
- Fonts: Noto Serif SC 900/500 (masthead, headlines, body) + Bodoni Moda (the English masthead name and the big score)
- Specimen: assets/style-specimens/xhs/05-daily-paper.jpg

**Trading Cards** `Bold · 85% fidelity`
- Reference: collectible card games and illustrated-guide cards: gold-bordered frames, rarity tags, numbering, stat bars
- Fits: one item per card, collectible lists: species, products, people, tools, cities
- Visual DNA: a dark tabletop in a radial gradient; gold gradient borders wrapping paper-faced card cores; on the cover, one big card over a smaller tilted card; on each card, the name, Latin name, rarity tag, a dot-grid image window, a # number, and two stat bars; the inner page is a 3×3 card pack sorted by one real value
- HTML implementation: the card frame is padding + a linear-gradient background; stat-bar widths are computed from real values. Foil-stamped reflections can't be done — approximated with multi-stop gradients
- Fonts: Figtree 800/900 (digits) + Noto Sans SC 700/900
- Specimen: assets/style-specimens/xhs/06-trading-cards.jpg

**Blank & Vertical** `Quiet · 90% fidelity`
- Reference: vertically set Chinese books and seals; art books that put a single thing on a page
- Fits: slow content, stories, close-ups of a single object, quotable lines; slip one or two into a set to let readers breathe
- Visual DNA: vast blank space; a large vertical Song-serif title aligned right; a vertical subtitle, thin and long; one vermilion seal; the subject small and isolated, landing lower left; one line of numbering at top left, a short rule plus the Latin name at the bottom
- HTML implementation: writing-mode:vertical-rl; the vermilion seal is a red block plus vertical characters. No downgrades. The whitespace comes from the layout, not from shrinking the type: vertical body text also stays ≥42px
- Fonts: Noto Serif SC 900/500
- Specimen: assets/style-specimens/xhs/07-blank-vertical.jpg

**Area Infographic** `Neutral · 95% fidelity`
- Reference: treemaps (proposed by Ben Shneiderman in the early 1990s) and waffle charts
- Fits: conclusion pages with a set of hard numbers whose proportions must read at a glance; composition, distribution, target-completion rates
- Visual DNA: the cover is a treemap where area equals quantity — big cells embed the hero sticker, small cells carry just a name and a number, smaller still merge into "the remaining N"; the inner page's waffle chart has each cell standing for a fixed quantity, four color tiers, and a legend below written with real numbers
- HTML implementation: the squarify algorithm, roughly 20 lines of JS, is inlined in the template; the waffle chart is CSS Grid. No downgrades
- Fonts: Figtree 900 + Noto Sans SC 900
- Specimen: assets/style-specimens/xhs/08-area-infographic.jpg

---

## ⚠️ AI Image-Generation-Only Styles (only recommend when the user is confirmed to have image generation; not selectable by default)

The soul of these styles lies in **dynamically generated visuals / 3D / particles / cinematic lighting / hand-drawn illustration**. Under pure HTML/CSS without image generation they can only produce severely degraded mocks, so they're **excluded from the default recommendation pool**. Only when the user clearly has image generation (via `huashu-gpt-image`) do they become candidates:

| Style | Soul | Why HTML can't do it |
|------|------|------------------|
| Active Theory (WebGL particles) | 3D particle systems/real-time rendering | Impossible in pure CSS |
| Field.io (generative art) | Algorithmically generated graphics | Static SVG can only make rigid simplified versions |
| Resn (illustrative interaction) | Character illustration + gamification | Depends on hand-drawn assets |
| Zach Lieberman (real-time generation) | creative coding brushwork | Depends on real-time generation |
| Raven Kwok (fractal parameters) | Recursive fractals | CSS can't reach the complexity |
| Ash Thorp (cinematic lighting) | Cinema-grade volumetric light/concept art | CSS lighting is a degradation |
| Territory Studio (FUI holograms) | Sci-fi holographic interfaces | Depends on many layered glow assets |
| Neo Shen (ink wash bleed) | Organic ink-wash bleeding | CSS gradients ≠ ink wash |
| Sagmeister & Walsh (color explosion) | Handmade objects + experimental layout | The clashing-color skeleton is doable (already merged into web 'Memphis Maximalism' and PPT 'Mono-Brand Type-as-Hero'), but the handmade texture can't be done |

> These aren't "bad", they're "wrong medium" — their native medium is AI-direct images, not the browser DOM.

---

## Default Aesthetic No-Go Zone (users may override per their own brand)

- ❌ **GitHub-dark lazy fix**: uniform deep-blue base (#0D1117) + generic cyan/purple neon glow — only this one overused combination is banned, not "all dark styles"
- ✅ **Not in the no-go zone**: cinematic dramatic lighting, warm cyberpunk (Ash Thorp orange/cyan), sports-poetry dark-field narratives — dark styles with authorial intent stay (this library's 'Linear dark glow', 'Black Big-Number Stage', and 'CS50 Candy Stage' are all legitimate dark styles)
- ❌ The aggressive purple-gradient universal formula, emoji-as-icon, rounded cards + left colored border accent (unless the brand itself uses it)
- ❌ Personal signatures/watermarks on cover images

---

## Prompt-Craft Essentials When Image Generation Is Available (Mood, Not Layout)

> Only applies when going the AI image generation route; on the HTML route, just write code per each style's "HTML implementation" above.

Short prompts > long prompts. Describing mood and content beats stacking 30 lines of layout detail.

| Writes that kill diversity | Writes that spark creativity |
|----------------|----------------|
| Specifying color ratios (60%/25%/15%) | Describing mood ("warm like Sunday morning") |
| Dictating layout positions | Citing a specific aesthetic ("Pentagram editorial feel") |
| Listing every visual element | Describing what the audience should feel |

Full AI image generation methodology → `huashu-gpt-image` skill.

---

**Version**: v3.2 (2026-06 restructured as an HTML-native library; 2026-08 filled in the infographic section, 40 → 60 styles; 2026-10 added the App and Chinese & East Asian sections, every style with a specimen, 60 → 84 styles; 2026-10 added the Xiaohongshu section, 84 → 92 styles)
**Applies to**: the default HTML path for all visual design — web/PPT/PDF/infographics/covers/Apps etc.
