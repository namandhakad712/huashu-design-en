# Design Style Library: 20 for Web + 20 for PPT (HTML-Native First)

> **2026-06 restructure**. Reverse-engineered from research on the world's top 10 website types + top 10 presentation types, using the top-5 widely recognized best designs for each (100 real cases total).
> The fatal flaw of the old 20-style "graphic/installation designer philosophy" library: the bold styles were almost all AI-generation-only (particles/light effects/hand-drawn), so **when users have no image-generation capability by default and everything falls back to HTML, the bold half is wiped out entirely, leaving only minimalism — this is the root cause of "default looks identical everywhere"**. Every style in this library is tagged with its **fidelity** under "pure HTML/CSS without image generation".
>
> ⚖️ **But remember the positioning**: this is **"ammunition to flip through when you have no ideas", not a "must-pick-from-here" checklist**. When the user provides content/brand/reference, the design unfolds from there — don't force the library. The skill's job is to help users avoid the worst, not to dictate what a good design must look like — good design grows out of the user's real needs.

## How to use this library

1. **First pick a half based on output type**: making a webpage/landing page/corporate site → the 20 web styles; making PPT/deck/presentations → the 20 PPT styles.
2. **Temperature system**: each style is tagged `Bold / Neutral / Quiet`. **Bold styles intentionally make up the majority** — the model's determinism bias naturally leans toward quiet minimalism, so the library's ratio pushes it toward bold.
   - Direction A (safe foundation) picks from Quiet/Neutral per needs; Direction B takes a different temperature for contrast; **Direction C is force-injected with bold styles by the SKILL's "seconds roulette"**.
   - ❌ Don't let all three directions land on "cream white + whitespace + one accent color" — that's the most common failure mode.
3. **Fidelity**: ≥90% can be done with eyes closed; 70-90% the main body is doable with some detail downgrades; <70% (e.g. Memphis aged textures) must **explicitly flag in the output which parts are downgraded to flat color blocks**, don't pretend you can reproduce the original texture.
4. **Fonts**: each style gives open-source alternatives (Inter/Geist/Manrope/Space Grotesk/Fraunces/Playfair etc.), don't use paid fonts (Söhne/Circular etc.).
5. Companions: the SKILL "Design Direction Advisor" Phase 3-5 uses this library to push 3 directions; `assets/showcases/` has a pre-made screenshot gallery.

---

## Color Derivation Protocol (run these three steps before using any style)

> ⚠️ **The hex values in all style entries below are example anchors, not formulas.** The same style applied to different content should derive different color values through this protocol — directly copying the entry's hex is just producing slop with better taste. Why: hard-coded formulas make 100 users get 100 outputs of the same colors, and the information content of color goes to zero; derivation makes color evidence that is "unique to this content".
>
> **Fonts are the same**: the font names in the entries are also example anchors. After picking a style, the display+body pairing should first pass through the pairing logic and the "overused list" in `references/typography.md` — **when the list conflicts with an entry, typography.md wins** (e.g. if the entry says Fraunces, switch to Newsreader or another equivalent per the list).

### Three-step method: Sample → Converge → Justify

| Step | What to do | Why |
|------|--------|--------|
| **1. Sample** | The primary color comes from three sources, don't invent it from nothing: ①brand assets (directly eyedrop from logo/existing VI) ②real content images (dominant colors in product screenshots/photography) ③cultural context (the color memory the content's theme carries, see table below) | Picking a color out of thin air = drawing lots from the model's priors, and you'll always draw one of those few internet-safe colors; colors sampled from content naturally carry a "why" |
| **2. Converge** | Use oklch to compress the palette to **2-3 chromatic colors + 1 neutral set**. Write neutrals as a lightness sequence (e.g. L 0.15/0.35/0.65/0.92/0.98), and keep chromatic colors far apart in oklch hue angle H ≥60° or lightness L difference ≥0.3 | Too many colors = chaos; oklch's L channel is perceptually uniform, so writing out the lightness sequence is a hierarchy system, far more reason-able than a pile of isolated hexes |
| **3. Justify** | Write one sentence on "why this color", put it in the output comments or delivery notes. E.g.: "Primary color taken from the user's logo ocher, chroma lowered to 0.08 to simulate ink" | **If you can't write that sentence, you're copying a formula.** The justification is a self-check gate against slop, not a ritual |

### Print color texture: why low saturation reads more premium than pure screen colors

Ink on paper can never reach the maximum saturation of a screen's RGB — CMYK's gamut is narrower, paper absorbs ink, and ambient light reflects, all of which "gray" the color. The "premium feel" human eyes have been trained on by print for decades is essentially this layer of physical grayness. So deliberately lowering chroma in screen design borrows the texture memory of print.

| Use | oklch chroma reference | Effect |
|------|------------------|------|
| Large background areas | 0.01–0.04 | Paper feel, not harsh |
| Brand primary/accent | 0.08–0.15 | Ink feel, eye-catching but not plasticky |
| Small-area highlights (buttons/links) | 0.15–0.22 | Keeps the energy, small areas only |
| >0.25 full-bleed | Use with caution | Screen-phosphor look, only suits deliberately "electronically native" styles like Wrapped/candy |

### Cultural context quick reference: same hue, different contexts

Choosing a color isn't just choosing a hue, it's choosing the cultural coordinate behind it. The same "red" lands miles apart:

| Hue | Context A | Context B | What differs |
|------|--------|--------|--------|
| Red | Forbidden City vermilion (orange-leaning, gray-tinged, oklch low L low C, darker and muddier than cola red) → traditional/dignified | Cola red (high-saturation pure red) → consumer/excitement | Drop the chroma and it jumps from a store shelf to a palace wall |
| Blue | Japanese indigo/cerulean (deep, purplish-gray) → handcrafted/calm | Tech blue #0066FF family → SaaS/efficiency | The latter is the model's favorite default blue — before using it, ask yourself if you're drawing lots |
| Green | Matcha/moss green (yellow-leaning, low saturation) → natural/Japanese | Neon green #39FF14 → terminal/hacker | Same green, one drinks tea and the other writes code |
| Yellow | Gamboge/mustard (brown-gray tinged) → vintage print | Warning yellow/Mailchimp yellow → eye-catching/playful | Grayness decides whether it's an old book page or a hard hat |
| White | Cream paper white #F5F0E8 → publication/warm | Pure white #FFF → laboratory/Swiss | A 2% color-temperature difference in the background is a temperament divide |

---

## Web Style Library (20 styles)

#### Bold

**Media-Grade Editorial Brutalism (giant Helvetica pressing down small body text)** `Bold · 98% fidelity`
- Reference: Bloomberg Businessweek (Richard Turley 2010-2014 redesign, by Code and Theory); Neue Haas Grotesk lineage
- Fits: media/content publishing, AI product launches, brand site heroes, research report covers, long-opinion-piece headers
- Visual DNA: pure black #000 + pure white #FFF + hyperlink blue #0000EE, accent signal orange-red #FF433D / terminal green #00A33E. Type Helvetica/Neue Haas Grotesk, 120px+ giant left-aligned headlines with tight tracking pressing directly onto 14px body text, extreme size contrast. Layout modular grid + 1px rule lines dividing columns, high information density with deliberately no whitespace. Signature elements: rule-line column dividers, underlined hyperlink blue, large black/white color blocks.
- HTML implementation: pure CSS can reproduce 1:1. CSS Grid for the modular grid + border for rule-line dividers, clamp() for oversized responsive type + tightened letter-spacing, system Helvetica/Arial stack or Inter fallback, hyperlinks directly #0000EE underlined. Zero asset dependency.
- Fonts: Inter (replacing Helvetica/Neue Haas Grotesk), Geist Mono for code

**Neo-Brutalism Clashing Info Stream (thick black-outline cards + high-saturation clashing colors)** `Bold · 95% fidelity`
- Reference: The Verge 2022 redesign (in-house team, PolySans + Mānuka)
- Fits: media/content sites, AI product aggregation pages, event landing pages, community ranking pages, Xiaohongshu-style info cards
- Visual DNA: electric purple #5200FF ~ magenta #E1306C high-saturation primary + bright yellow #F8E000 accent + pure black #08080D + white, large clashing color blocks deliberately unsoftened. Type geometric sans-serif headlines + serif body contrast. Layout card-based feed, 2-4px thick black outlines, hard color-block zones, nearly no rounded corners. Signature elements: thick-outline cards with clashing hover inversion, unfinished-interface vibe.
- HTML implementation: a pure CSS strength. border:3px solid #000 thick outlines + box-shadow hard offset shadow (4px 4px 0 #000) + grid/flex card streams + :hover background clashing inversion. No 3D/light-effect obstacles.
- Fonts: Space Grotesk (replacing PolySans) + any serif like Fraunces

**Memphis Maximalism (clashing color blocks + offset overlaps + vintage type)** `Bold · 72% fidelity`
- Reference: Gucci Vault concept store (Alessandro Michele); the Memphis design movement / Sagmeister's rebellious DNA
- Fits: e-commerce concept stores, creative event pages, brand experiment campaigns, Y2K retro themes, holiday marketing pages
- Visual DNA: vintage red/mustard yellow/royal blue/purple/olive green large clashing color blocks juxtaposed on an aged cream warm base, intensely and deliberately inharmonious. Type vintage serif mixed with decorative faces, print texture, breaking the grid with offset overlaps. Layout anti-grid collage curation, modules of varying sizes offset and overlaid, like wandering through a digital room. Signature elements: clashing color blocks, offset overlaps, unconventional nav easter eggs.
- HTML implementation: transform:rotate() for offset overlaps + position:absolute stacking + high-saturation background color blocks + vintage Google Fonts. Real aged textures can't be reproduced in CSS, downgraded to flat color blocks + mix-blend-mode/contrast filters to simulate texture; the geometric collage version holds up, the archival-aged version gets downgraded.
- Fonts: DM Serif Display + Bungee (decorative) + Space Mono

**Friendly Geometric Candy (candy-color raised 3D buttons, gamified)** `Bold · 85% fidelity`
- Reference: Duolingo (Johnson Banks + Monotype, Feather Bold typeface); anti-Silicon-Valley minimalism
- Fits: education/language learning, consumer app landings, gamified products, mass-friendly products, event signup pages
- Visual DNA: Duo green #58CC02 + duck yellow #FFC800 + sky blue #1CB0F6 candy high saturation + white base, rounded and friendly. Type extra-bold rounded faces (Feather Bold feel). Layout large rounded cards, raised 3D buttons (hard bottom shadow = pressable feel), mascot slot + progress bubble. Signature elements: 3px solid-shadow raised buttons, press-down motion on click, super-rounded corners.
- HTML implementation: pure CSS. box-shadow:0 4px 0 hard bottom shadow for raised buttons + :active translateY(4px) removing the shadow to simulate pressing, large border-radius, flat color blocks. When no image generation, use CSS geometric shapes or emoji for the mascot placeholder (slight downgrade).
- Fonts: Baloo 2 / Nunito (extra-bold rounded replacing Feather)

**Pure-CSS Geometric Illustration + Responsive Morphing Easter Eggs** `Bold · 80% fidelity`
- Reference: Lynn Fisher (lynnandtonic.com, pure CSS art legend, covered in an Adobe feature article)
- Fits: personal homepages, creative 404/easter-egg pages, playful brand landings, tech blog headers, designer self-promotion
- Visual DNA: 2-4 high-contrast flat colors (palette changes per breakpoint). Type bold geometric sans-serif headlines. Layout centers on "art that morphs with the viewport" — a set of CSS shapes recomposes into different pictures at different breakpoints (e.g. a building whose floors change with screen width). Signature elements: pure-CSS geometric illustrations, breakpoint-driven rearrangement easter eggs, zero images.
- HTML implementation: the playground of pure CSS showmanship, zero assets is an advantage. Stack geometric shapes from div + border-radius/clip-path/transform/box-shadow, use @media breakpoints to change shape size/position for morphing. The difficulty is in design thinking rather than technique, but each shape needs careful hand-crafting.
- Fonts: Rubik / Archivo (bold geometric replacing custom)

**Bold Big-Type Editorial, Giant Type, Black-and-White Fashion Poster** `Bold · 88% fidelity`
- Reference: Jacquemus official site / Rik Oostenbroek / Domestika; fashion magazine big-type posters
- Fits: e-commerce fashion, portfolios, media features, brand manifesto pages, video course covers, large-type research reports
- Visual DNA: minimalist black-and-white + a single restrained accent color (blush pink #E8C4C0 or pure red). Type oversized display sans/serif with high contrast, headlines filling the whole screen. Layout full-bleed grid, giant type wrestling with negative space, 1:1 text/image split. Signature elements: screen-filling giant headlines, luxury-grade whitespace, left-right counterpoint layout.
- HTML implementation: pure CSS reproduces perfectly. clamp() giant type + CSS Grid full-bleed splits + generous padding whitespace + vh units so headlines fill the viewport. When no images, use flat color blocks/text blocks as placeholders for fashion photography (slight downgrade but the layout holds).
- Fonts: Archivo Expanded / Anton (Display) + Playfair Display (high-contrast serif)

**Cosmic Retro-Futurism, Vintage Future Space Catalog** `Bold · 75% fidelity`
- Reference: Perplexity Comet browser launch site (The Brand Identity: Black/Blue/Cream; 2001: A Space Odyssey vibes)
- Fits: AI product launch sites, tech brand manifesto pages, countdown pages, futuristic landings, concept launch events
- Visual DNA: pure black #0A0A0A + cream paper white #F0EAD8 + a touch of cobalt-peacock blue #2B4F91, low saturation like vintage astronomy catalogs. Type high-contrast serif (classical astronomy atlas feel) + whitespace. Layout line-drawn orbital/parabolic SVG, planetary dots, cream base with black text, old-book typography. Signature elements: SVG celestial orbital lines, cream+blue+black tri-color, vintage serif large type, astronomy catalog texture.
- HTML implementation: pure CSS+SVG reproduces about 80% of the static version's character. SVG path for orbital parabolas + CSS radial positioning for planetary dots + tri-color variables + high-contrast serif. The gap: the full-screen video transition of "space falling to Earth" (the soul part) — downgraded to CSS scroll parallax + SVG orbit rotation approximation.
- Fonts: Cormorant Garamond / EB Garamond (high-contrast serif) + Space Mono

**Cinematic Sound-Viz Dark (cinematic sound-wave visualization)** `Bold · 72% fidelity`
- Reference: ElevenLabs; movie title sequences (Saul Bass-style minimalist motion) × audio engineering interfaces
- Fits: audio/voice AI products, music tech sites, podcast platforms, media release pages, cinema-grade brand heroes
- Visual DNA: pure black #000 base + pure white text + blue-purple gradient accent waveforms. Type large sans-serif headlines in Saul Bass-style minimalism. Layout full-bleed dark field, sound-wave/spectrum visualization running through, giant titles pressing onto waveforms, card function zones. Signature elements: colored audio-waveform bands, movie-title-style minimalism, high-contrast black-and-white + single gradient, sound-visualization motif.
- HTML implementation: pure CSS+SVG reproduces 70% of the character (skeleton is perfect, the waveform is the downgrade point). SVG polyline for static waveforms or arrays of unequal-height div bars + CSS animation for a 'fake waveform' bouncing approximation. Gap: Web Audio/Canvas spectrums that react to sound in real time can't be reproduced in pure CSS — the static version looks right, the dynamic soul can't be restored.
- Fonts: Inter / Sora (large sans-serif)

**Pixel-Game Side-Scroller, 8-bit narrative** `Bold · 70% fidelity`
- Reference: Robby Leonardi's interactive resume (8/16-bit platform-action-game narrative, a tribute to Nintendo SNES)
- Fits: creative resumes/portfolios, playful brand campaigns, gamified landings, event easter-egg pages, personal hobby homepages
- Visual DNA: retro-game multi-zone palette — forest green #4CAF50 grass + sky blue #5DADE2, transitioning to space purple #2C2A4A, volcano orange-red #E8743B, seabed cyan #1ABC9C, each 'level' gets its own high-saturation cartoon palette. Type pixel fonts (8-bit feel) + bold sans-serif. Layout horizontal/vertical scrolling level-by-level scenes, parallax layers, scroll-triggered displacement. Signature elements: per-level color changes, pixel aesthetics, parallax scrolling, game HUD-style UI.
- HTML implementation: pure CSS + a little JS reproduces the skeleton (the original itself is HTML+CSS+jQuery with no WebGL). Parallax layers via position + scroll displacement, image-rendering:pixelated, CSS frame-by-frame background-position for sprite animations, segmented background colors. Gap: original hand-drawn character/scene pixel illustrations — without image generation, substitute simple pixel icons assembled from CSS blocks (art downgrade, not technique).
- Fonts: Press Start 2P / VT323 (pixel) + Inter

#### Neutral

**Bauhaus Geometric (geometric logo + flat illustration system)** `Neutral · 90% fidelity`
- Reference: Khan Academy rebrand (hexagon + petal logomark + Wonder Blocks design system); Bauhaus geometric composition
- Fits: education course sites, brand logo systems, infographics, children-friendly products, event KVs
- Visual DNA: primary-color-spectrum palette — Bauhaus red #E63946 / yellow #FFB703 / blue #0077B6 + black and white, flat color block assembly. Type geometric sans-serif (rounded geometric feel). Layout circle/triangle/square basic geometric units building illustrations, aligned to a grid, modular puzzle. Signature elements: pure-geometry logomarks, flat no-gradient illustrations, primary color block composition.
- HTML implementation: pure CSS is all-powerful with geometry. border-radius:50% for circles, clip-path/border triangles, square divs assembling geometric illustrations, CSS Grid for alignment, flat fills need no assets. Hand-craft illustrations from CSS shapes or inline SVG geometric paths.
- Fonts: Poppins / Manrope (rounded geometry replacing Wonder Blocks)

**Dark Editorial, two-color sidebar dev portfolio (deep base + single neon accent + mono type)** `Neutral · 96% fidelity`
- Reference: Brittany Chiang (brittanychiang.com v4, the de-facto dev portfolio standard)
- Fits: portfolio personal sites, developer-facing products, tech brand sites, resume pages, AI tool landings
- Visual DNA: deep ink-green/navy base #0A192F + slate gray text #8892B0 + a single neon cyan accent #64FFDA. Type sans-serif body + mono type (numbers/labels). Layout fixed left sidebar nav + scrolling main right area in two columns, section numbering 01/02, hover underline slide-in on links. Signature elements: single accent color, mono number labels, sidebar anchor highlighting.
- HTML implementation: pure CSS reproduces fully. position:sticky for the fixed sidebar + CSS Grid two columns + single-accent variables + mono labels + :hover underline transform slide-in. Zero assets, pure layout and micro-interactions.
- Fonts: Inter + JetBrains Mono (mono)

**Warm Editorial (cream paper base + terracotta orange + serif/sans mixed)** `Neutral · 97% fidelity`
- Reference: Anthropic / Claude (DBCo + Geist Studio, Styrene×Tiempos); Penguin/Pelican paperback typography
- Fits: AI product sites, brand corporate sites, long-form reading pages, orange-cover ebooks, research reports, training materials
- Visual DNA: cream paper base #F5F0E8 + terracotta orange #CC785C/#D97757 accents + near-black text #191919, warm and low saturation. Type serif headlines (Tiempos feel) × sans-serif body (Styrene feel) mixed. Layout book-like single-column reading flow, comfortable line height, restrained dividers. Signature elements: paper-feel warm base, terracotta orange, publication-grade typographic rhythm.
- HTML implementation: pure CSS 100% reproduction, zero assets. Background color variable + serif/sans font stack mixing + max-width to limit reading width + line-height 1.7 comfortable line height. This is the safe home turf for Anthropic's terracotta warm-color version.
- Fonts: Fraunces / Newsreader (replacing Tiempos serif) + Inter (replacing Styrene)

**Linear dark glow + Bento grid (Glassmorphism Bento)** `Neutral · 85% fidelity`
- Reference: Linear / Cursor (the phenomenon-grade 'The Linear Look' school, Frontend Horse has the code recipe)
- Fits: SaaS/AI product sites, developer tools, tech brand heroes, product feature showcases, dark dashboard demos
- Visual DNA: near-black base #08090A + desaturated blue-purple brand #5E6AD2 + low-saturation cyan-purple glow gradient #4EA7FC→#B59AFF. Type geometric sans-serif with tight negative tracking. Layout bento grid blocks, hairline dividers, glassmorphism cards. Signature elements: dark-base glowing gradient borders, bento blocks, streamers, frosted glass.
- HTML implementation: pure CSS strong reproduction. box-shadow/filter blur + radial-gradient for glow halos, backdrop-filter:blur for glassmorphism, conic/linear-gradient borders, CSS Grid to assemble the bento. Only gap: "real product UI screenshots" — substitute simplified fake UI assembled from color blocks + text (that part downgrades).
- Fonts: Inter / Geist (negative tracking) + Geist Mono

**Angled Fluid Gradient (slanted fluid gradient bands)** `Neutral · 92% fidelity`
- Reference: Stripe (iconic angled gradient banner, Klim's custom Söhne typeface)
- Fits: SaaS/Fintech landing pages, brand site heroes, product launch pages, event banners, AI product marketing pages
- Visual DNA: multi-color fluid gradient (indigo #635BFF→cyan→pink→warm orange) as the hero background + pure white content area + near-black text. Type refined sans-serif (Söhne feel). Layout slanted color-block sections (skew-cut zones), gradient hero pressing over structured grid body. Signature elements: angled cut boundaries, multi-color fluid gradients, rational grid over expressive gradients.
- HTML implementation: pure CSS. transform:skewY() or clip-path:polygon() for slanted sections, linear-gradient multi-color stacking (optional CSS animation for slow flow) for the fluid gradient band, Grid for the structured body below. Zero assets.
- Fonts: Inter / Hanken Grotesk (replacing Söhne)

**Utility-First Colorful Docs (pragmatic rainbow-coded documentation)** `Neutral · 98% fidelity`
- Reference: Tailwind CSS Docs (Sky/Cyan brand color + function-category rainbow hue bars)
- Fits: technical documentation, API references, design system sites, tutorial sites, developer knowledge bases, SaaS help centers
- Visual DNA: Sky blue #38BDF8 brand + teal→cyan→sky cyan gradient + Slate gray scale #0F172A/#64748B/#F8FAFC, docs use rainbow hue bars to distinguish function categories (pink #EC4899 / purple #A855F7 / green #10B981 / orange). Type clean sans-serif + mono code. Layout three columns of left sidebar nav + center content + right TOC, color-highlighted code blocks, category color labels. Signature elements: cyan-blue gradient hero, rainbow category colors, three-column docs skeleton, syntax-highlighted code blocks.
- HTML implementation: pure CSS 98% reproduction (it is itself a CSS framework's documentation). Grid three columns + linear-gradient cyan hero + category color variables + code block syntax colors via span coloring. Inter is open source, only the dark-mode toggle/copy needs lightweight JS. Zero light effects/3D/hand-drawing.
- Fonts: Inter + JetBrains Mono / Fira Code (code)

**Terminal-Core Soft-Futurism (mono type + isometric cubes)** `Neutral · 80% fidelity`
- Reference: Cursor (Anysphere); developer terminal aesthetics × Teenage Engineering industrial minimalism
- Fits: AI coding tool sites, CLI product landings, developer infrastructure, tech brand heroes, terminal-type products
- Visual DNA: charcoal black #0B0D14 base + warm white text #F2F0EF + restrained blue-purple gradient accents on buttons and glows. Type mono as the protagonist (command-line feel) + sans-serif support. Layout command-line/code-block foreground, bento sections, 2.5D isometric cube diagrams. Signature elements: mono command lines, isometric projected cubes, warm white × charcoal, restrained gradient glows, industrial minimalism.
- HTML implementation: pure CSS 80% reproduction. Mono code blocks + dark bento + box-shadow glows; 2.5D isometric cubes hand-built with CSS 3D transforms (rotateX/Y + skew) or SVG isometric projection. Gap: clickable multi-interface demos need JS + fake UI assembly. No WebGL requirement.
- Fonts: Geist Mono / JetBrains Mono (protagonist) + Inter (support)

#### Quiet

**Functional Brutalism (gray-line divides + system fonts + blue links, grid community)** `Quiet · 98% fidelity`
- Reference: Are.na / Lobsters / Quartz; Müller-Brockmann grids landing digitally + Tufte information density
- Fits: community/UGC platforms, content aggregation sites, documentation knowledge bases, mobile-first content feeds, geek-oriented products
- Visual DNA: near-white base #FBFBFB + black text + 1px gray dividers #E0E0E0 + classic link blue #0000EE / visited purple. Type system font stack (-apple-system/undecorated). Layout high-density information lists, thin gray line columns, minimal whitespace, compact line spacing. Signature elements: hairline gray dividers, blue links, system fonts, information-density-first.
- HTML implementation: the easiest to reproduce in pure CSS, this is the native look of Brutalist Web. border-bottom:1px gray line lists + system-ui font stack + compact padding + blue links. Almost no assets or JS needed, pure structure.
- Fonts: system-ui system font stack / IBM Plex Sans (fallback)

**Gallery Dark (deep black negative space + single-column large images + EXIF small type)** `Quiet · 75% fidelity`
- Reference: Glass (glass.photo) / Bottega Veneta; gallery darkroom + Apple Photos content-first
- Fits: photography portfolios, luxury e-commerce, immersive visual content display, personal gallery pages, premium product displays
- Visual DNA: pure black base #0A0A0A + the artwork itself provides the only color + very faint gray EXIF small type #666. Type ultra-thin sans-serif small type. Layout single-column centered large images, huge negative-space framing, metadata small type under images. Signature elements: darkroom black base, content-first UI receding, EXIF-style small-type captions, large images owning the viewport.
- HTML implementation: pure CSS reproduces the layout skeleton. Pure black base + centered max-width single column + generous padding frame whitespace + small metadata type. The gap is "real photography" itself — substituting placeholders/flat color blocks loses the soul, but the darkroom atmosphere and layout are 100% buildable.
- Fonts: Inter (light weight 300) / Cormorant (optional serif luxury feel)

**Swiss Monochrome (Vercel-style pure black-and-white + Geist + razor-sharp corners)** `Quiet · 98% fidelity`
- Reference: Vercel / Next.js Docs (self-made Geist now open source); Massimo Vignelli's less-is-more
- Fits: developer tool documentation, tech brand corporate sites, AI product sites, SaaS landing pages, minimalist research reports
- Visual DNA: pure black #000 + pure white #FFF + gray scale #888, zero color or just one touch of blue links. Type Geist geometric sans-serif + Geist Mono. Layout razor-sharp right angles (no or minimal rounded corners), high contrast, precise grids, restrained whitespace. Signature elements: pure black-and-white, sharp corners, Geist type, triangle/arrow geometric markers.
- HTML implementation: pure CSS 100% reproduction, Geist is open source and directly importable. CSS Grid precise grids + black/white variables + border-radius:0 sharp corners + hairline borders. This is HTML's most comfortable minimalist home turf, zero asset dependency.
- Fonts: Geist + Geist Mono (Vercel's open-source originals)

**Kenya Hara White Gallery (Japanese-style white box gallery)** `Quiet · 80% fidelity`
- Reference: Cosmos (cosmos.so) / Aesop official site; Kenya Hara's 'white' emptiness + Swiss grid hybrid
- Fits: high-end e-commerce, creative galleries, content curation platforms, designer portfolios, brand boutiques, moodboard sites
- Visual DNA: near-all-white #FAFAFA base + pure black text #0A0A0A + very faint gray dividers #EFEFEF, content images supply all the color, UI recedes to the background. Type minimalist system/geometric sans-serif small type with wide tracking. Layout masonry waterfall grid, extreme whitespace, faint gray hairline separators, Eastern emptiness. Signature elements: white-box aesthetics, luxury whitespace, content-first UI receding, waterfall curation.
- HTML implementation: pure CSS reproduces the static layout (distinguished from the dark gallery by the 'white'). CSS columns or Grid for masonry + near-white variables + generous padding whitespace + faint gray dividers. The gap is Lenis/GSAP silky inertial scrolling and image entry easing (60% of the premium feel lives there); CSS only does basic transitions, so the motion layer downgrades.
- Fonts: Inter (light weight) / Cooper Hewitt (Aesop's same open-source typeface)

## PPT Style Library (20 styles)

#### Bold

**Neo-Swiss Billboard Editorial** `Bold · 98% fidelity`
- Reference: the Big-Number Editorial school in AI/SaaS pitch decks like Scribe $75M, Flock Safety $47M; Bloomberg Businessweek infographics; Pentagram
- Fits: fundraising pitches, QBR/business reviews, annual trend retrospectives, key product launch pages
- Visual DNA: pure white (#FFFFFF) or near-black (#0A0A0A) base + a single high-saturation accent (electric blue #2D5BFF / neon green #00E676 / brand orange #FF6B2C) + neutral grid lines #E5E5E5. Type = extra-large bold sans-serif, titles occupy half the screen, numbers in tabular-nums with tightened tracking. Master layouts = ①large color-block section pages with one word ②giant numbers occupying half the screen (3.2x) with small notes ③left-right split comparison ④full-bleed flat line/bar charts. Signature = billboarding giant type, strict baseline grids, large color-block section pages
- HTML implementation: clamp() for giant numbers; CSS Grid for strict grids; background-color for large color-block section pages; line/bar charts as pure div+CSS or inline SVG (sharper than pasted images); font-variant-numeric:tabular-nums for number alignment. Zero illustrations, zero 3D
- Fonts: Inter / Geist / Söhne replacing Neue Haas Grotesk; Geist Mono for numbers

**Black Big-Number Stage (giant numbers on black)** `Bold · 97% fidelity`
- Reference: Steve Jobs 2007 iPhone Keynote, Xiaomi SU7 Ultra Lei Jun launch, Spotify Wrapped, Presentation Zen (Garr Reynolds)
- Fits: product launch keynotes, thought leadership presentations, all-hands town halls, emotional annual reviews
- Visual DNA: pure black #000000 base + pure white #FFFFFF text with high contrast, one brand accent color per page (Xiaomi orange #FF6900 / Spotify green #1ED760 / Apple blue #2997FF). Type = geometric sans-serif bold, one word per screen or one giant number filling the view, tightened tracking. Master layouts = ①title page, black base, one centered line of large type ②data-climax page with giant number + unit + one line of note ③left-right parameter comparison two columns (accent color vs gray) ④single slogan page. Lots of negative space
- HTML implementation: a few lines of CSS for black base white text; clamp() + flex centering for giant numbers; separate span for accent-color highlights; CSS Grid two columns + bar highlights for left-right comparison; tabular-nums. Removing product photos and going pure text is actually closer to Zen's essence
- Fonts: Geist / Inter / Source Han Sans replacing SF Pro

**Mono-Brand Type-as-Hero (high-saturation monochrome brand poster)** `Bold · 96% fidelity`
- Reference: Spotify Wrapped visual system, Mailchimp Brand Book (Collins), Netflix red-black modern revival, COLLINS brand systems
- Fits: brand/marketing strategy, campaign pitches, town hall culture pages, event key visuals
- Visual DNA: a single brand primary color full-bleed base (Spotify green #1ED760 / Mailchimp yellow #FFE01B / Netflix red #E50914) + black or white contrasting text, two clashing layers. Type = giant type as the key visual (type-as-hero), reaching ceiling and floor. Master layouts = ①full color-block base + reverse-white giant type ②two color blocks split top/bottom or left/right ③giant numbers filling the frame. Signature = monochrome full-bleed, type as image, high-contrast clashing
- HTML implementation: full-bleed background-color; clamp() giant type filling the screen; two 100vh color blocks for the split; type-as-image via font-weight 900 + negative letter-spacing. Flat color blocks with zero assets, HTML-native at its most satisfying
- Fonts: Inter / Manrope / Archivo (extra-bold) replacing Circular/Cavendish

**Full-Bleed Gradient Manifesto** `Bold · 82% fidelity`
- Reference: Zuora's 'Tell a Different Story' sales deck (broken down by Andy Raskin), Nike's 'Just Do It' campaign, National Geographic double-page spreads
- Fits: sales proposal vision pages, brand manifestos, keynote pivot pages, mission/vision single pages
- Visual DNA: full-bleed CSS gradients (warm orange→magenta / deep blue→cyan) or flat color bleed + reverse-white manifesto giant type + hashtag slogans (#shifthappens). Type = heavy sans-serif all-caps slogans running across. Master layouts = ①full-width gradient + centered reverse-white manifesto ②promised-land vision page ③customer logo wall. Signature = full-bleed bleeding, reverse-white giant slogans, hashtag slogans
- HTML implementation: linear-gradient/radial-gradient full-bleed (no particles/light effects; pure CSS gradients are allowed); centered positioning for reverse-white type; gray-scale SVG/text placeholders in a grid for the logo wall. The parts that originally relied on documentary photographs downgrade to CSS gradient bases + giant type; the missing photography drops fidelity by ~15%
- Fonts: Archivo / Anton / Manrope (extra-bold)

**Candy-Color Lecture Stage (CS50 single-concept stage)** `Bold · 94% fidelity`
- Reference: Harvard CS50 (David Malan), Lessig Method/Takahashi style, Presentation Zen
- Fits: educational courseware, tech lectures, concept explanations, code teaching
- Visual DNA: deep black base #0A0A0A + high-saturation candy-color rotating giant type (magenta #FF2D95 / cyan #00E5FF / bright yellow #FFD500 / green #39FF14). Type = sans-serif giant type floating centered, one concept per screen, minimal text. Master layouts = ①deep black base with a single candy-color giant word ②mono code blocks with syntax highlighting ③stage-spotlight giant type. Signature = deep-black floating candy-color giant type, mono code highlighting, strong stage spotlight, minimal text
- HTML implementation: deep black background + single-color giant type clamp() centered; pre + mono + span coloring for syntax-highlighted code blocks; a very faint radial-gradient vignette (not particle light effects) for the spotlight feel. High fidelity
- Fonts: Inter extra-bold + JetBrains Mono (code)

**Playful Maximalist Editorial (Collins-style)** `Bold · 75% fidelity`
- Reference: Mailchimp Brand Book (Collins 2018), New Yorker cartoon character, Cooper rounded serif, Cavendish fluorescent yellow
- Fits: decks for brands with attitude, creative agency pitches, culture-oriented town halls, marketing pages against SaaS minimalism
- Visual DNA: Cavendish fluorescent yellow #FFE01B in large areas + black + a little clashing color, anti-SaaS minimalism. Type = Cooper-style rounded serif large titles (playful) + magazine-style whitespace composition. Master layouts = ①fluorescent yellow full base + whimsical titles ②magazine-style irregular whitespace layout ③giant-type meme copy. Signature = fluorescent yellow, rounded serif, playful composition, whimsical hand-drawn character (downgraded to geometric color blocks/emoji replacing real illustration)
- HTML implementation: fluorescent yellow background; rounded serif font-family; asymmetric Grid for magazine whitespace. The hand-drawn gorilla/illustration is the core element and can't be done without AI image generation, downgraded to CSS geometric color blocks + large emoji + irregularly transform-rotated text blocks; missing illustration drops fidelity by ~20%
- Fonts: Fraunces (adjustable roundness) / Bree Serif replacing Cooper; Inter for body

**Irreverent Pop (Reddit-style)** `Bold · 80% fidelity`
- Reference: Reddit Ads sales deck (listed by Dock as the most characterful), David Carson-style irreverent layout, 90s web retro, Memphis playfulness
- Fits: Gen-Z brands, meme marketing decks, community/creator audiences, proposals that dare to be unserious
- Visual DNA: Reddit orange-red #FF4500 + clashing colors, 90s web retro palette. Type = mixed/layout-breaking David Carson-style typography, meme-style colloquial copy. Master layouts = ①fun pages with meme giant type ②facts pages with rhythmic pivot into serious data ③colloquial headlines. Signature = layout-breaking mixed type, orange-red, meme colloquialism, fun→facts rhythm reversal, retro web texture
- HTML implementation: deliberately break the grid with transform rotations/overlapping positioning/mixed font sizes; orange-red + clashing color blocks; retro texture via thick black borders + hard box-shadows (no blur). Custom meme illustrations downgrade to emoji + geometric collage, but the mixed-type layout itself is HTML-reproducible
- Fonts: Archivo / Space Grotesk + mixed Inter for contrast

**Maximalist 3D-Type (Wrapped-style Y2K inflated giant type)** `Bold · 78% fidelity`
- Reference: Spotify Wrapped 2022/2023/2025, Memphis clashing colors, Y2K/Maximalism, duotone portrait gradients
- Fits: annual reviews (emotion-driven virality), personalized data cards, social sharing vertical cards, brand year-end
- Visual DNA: high-saturation clashing full-bleed background (magenta + cyan + orange) + Spotify green as the highlight + duotone two-color gradients. Type = ceiling-to-floor giant numbers, years/numbers with 3D inflation/metallic texture. Master layouts = ①clashing full-bleed + giant inflated numbers ②duotone portrait/color-block base + reverse-white giant type ③vertical shareable cards. Signature = giant inflated 3D numbers, clashing full-bleed, duotone gradients, metallic year texture, vertical story cards
- HTML implementation: clashing full-bleed background; 3D inflated numbers via stacked CSS text-shadow layers + transform:perspective or SVG + stroke for dimensionality (not real 3D rendering); duotone via mix-blend-mode + gradient layered over grayscale placeholder blocks. Metallic texture downgrades to gradient-filled text via background-clip:text, dropping fidelity by ~15%
- Fonts: Archivo Black / Anton extra-bold + Clash Display for numbers

#### Neutral

**Bento Grid** `Neutral · 95% fidelity`
- Reference: the Apple Keynote Bento Grid era, the new-gen MBB Bento/Big-Type decks (2024-2026), Stripe annual report metric card matrices, Pitch.com QBR templates
- Fits: product feature summaries, consulting/QBR data reports, sales result pages, town hall metric pages
- Visual DNA: light gray/cream base (#F5F5F7/cream) or near-black base + brand primary + 1-2 accent colors, cards with light color-block bases + rounded corners + subtle borders/subtle shadows. Type = oversized display titles + regular body, strong weight contrast, KPI numbers in tabular figures. Master layouts = ①title page with giant single sentence + whitespace ②bento pages with 2×2/3-column unequal-height cards, one insight per card (number/line icon/sparkline) ③one-insight giant-number pages. Signature = unequal-height card grids, rounded subtle borders, breathing room
- HTML implementation: CSS Grid's grid-template-areas for unequal-height bento; border-radius + subtle box-shadows + 1px hairlines for cards; inline SVG for sparklines; inline SVG stroke for line icons. Zero pasted images
- Fonts: Inter / Geist + Geist Mono for numbers

**Dark Hairline Terminal (Neo-Swiss dark terminal aesthetics)** `Neutral · 94% fidelity`
- Reference: Linear pitch deck, Vercel design language, CS50 deep-black stage courseware; typeface Inter Tight + JetBrains Mono
- Fits: developer tool/tech product launches, tech roadshows, engineering reports
- Visual DNA: near-black base (#0D0D0F/#111113) + hairline thin-line #262629 grid + a single purple-blue accent (#5B5BD6/#7C7CFF). Type = Inter Tight large titles + JetBrains Mono for labels/data. Master layouts = ①minimalist title page with one sentence + mono small labels ②hairline-divided data grids ③mono-labeled feature lists. Signature = 1px thin-line grids, mono single-width labels, extreme whitespace, near-black rather than pure black
- HTML implementation: near-black background + border:1px solid hairline grids; mono font-family for mono labels; a very faint box-shadow/border highlight for subtle glow rather than real light effects (downgrade to avoid the cyber-neon forbidden zone). Avoid the #0D1117 deep-blue forbidden zone, use neutral near-black
- Fonts: Inter Tight + JetBrains Mono / IBM Plex Mono

**Two-Font Consulting (Bower-style)** `Neutral · 90% fidelity`
- Reference: McKinsey 2019 brand system (designed by Wolff Olins, Bower serif + sans-serif), BCG Executive Perspectives, deep-blue thin-line patterns
- Fits: consulting reports, executive presentations, industry research, authoritative institution proposals
- Visual DNA: deep blue (#051C2C/McKinsey deep blue) × white binary + a single brand color highlight (BCG green #00805A), warm gray base with breathing room. Type = characterful serif large titles (Bower-style) juxtaposed with sans-serif body at high contrast. Master layouts = ①conclusion-style action titles in the top-left corner ②deep-blue thin-line pattern decoration ③magazine-style left/right division of labor (conclusion text + visuals) ④giant-number data-point cards. Signature = serif × sans high contrast, deep-blue thin-line patterns, action titles, warm-gray premium feel
- HTML implementation: two-font font-family juxtaposition (serif titles + sans body); repeating-linear-gradient or SVG lines for thin-line patterns; pure CSS for data-point cards; the grayscale treatment of photos is skippable when there are no photos. The blue-purple edge shimmer downgrades to a flat color edge
- Fonts: Playfair Display / Fraunces serif titles + Inter body (replacing Bower)

**Diagram-Driven Isotype (enterprise diagram arrows)** `Neutral · 88% fidelity`
- Reference: Salesforce sales decks, the Isotype (Otto Neurath) lineage, Gene Zelazny's Say It With Charts, Hans Rosling/Gapminder
- Fits: platform/architecture explanations, customer journeys, process methodologies, ecosystem maps
- Visual DNA: enterprise blue color blocks + product-line color distinctions + iconified capability grids. Type = clean sans-serif. Master layouts = ①horizontal customer journey arrow flows ②layered platform architecture diagrams ③iconified capability grids ④2×2/waterfall/pyramid structure diagrams. Signature = arrow flows, layered architecture boxes, Isotype icon grids, process as narrative
- HTML implementation: Flexbox + CSS clip-path triangles or SVG arrows for arrow flows; nested bordered divs for architecture layers; inline SVG stroke for unified icon outlines; Grid + slanted cuts for waterfall/pyramid; CSS circles + positioning for bubble charts. Pure vector drawing
- Fonts: Inter / IBM Plex Sans (chart-friendly)

**Diagrammatic Minimalism (single master diagram concept)** `Neutral · 95% fidelity`
- Reference: Simon Sinek's Golden Circle TED talk, Bauhaus geometric abstraction, information architecture's "one diagram rules the page"
- Fits: theoretical framework explanations, TED-style thought dissemination, model/methodology visualization, single-concept keynotes
- Visual DNA: minimalist white/light base + black + 1 accent color, flat geometric colors. Type = sans-serif, labels embedded in shapes in uppercase. Master layouts = ①a single geometric master diagram (concentric circles/triangles/matrices) carrying the whole concept ②inside-out arrows ③comparison cases. Signature = single geometric master diagram, nested concentric circles/triangles, uppercase labels, one diagram carrying the concept
- HTML implementation: border-radius:50% nested divs or SVG circles for concentric circles; clip-path/SVG polygons for triangles; SVG markers for arrows; absolute-positioned labels pasted onto the shapes. Pure geometry, HTML reproduces perfectly
- Fonts: Manrope / Futura family (open-source Jost alternative) geometric feel

**Narrative Sparkline (Duarte-style)** `Neutral · 91% fidelity`
- Reference: Nancy Duarte's Resonate sparkline narrative, Al Gore's An Inconvenient Truth, Duarte Inc. data storytelling
- Fits: presentation structure design, change narratives, before/after comparisons, data story arcs
- Visual DNA: dark or white base + brand orange accent at turning points + grayed comparisons. Type = sans-serif, annotation labels at points. Master layouts = ①a wave line running across the screen ②text annotation points on the wave ③vertically juxtaposed comparison waves ④a single data line floating on an all-black base ⑤progressive reveal. Signature = across-screen wave lines, annotation points on waves, orange turning points, comparison waves, curves climbing out of the frame
- HTML implementation: inline SVG paths (smooth Beziers) for wave lines; SVG circles + text positioning for annotation points; two paths for comparison waves; CSS animation stroke-dashoffset for reveals. Pure SVG drawing, zero assets
- Fonts: Inter + Geist Mono for numbers

#### Quiet

**Assertion-Evidence / Tufte Information Design** `Quiet · 93% fidelity`
- Reference: Michael Alley's Assertion-Evidence (Penn State evidence), McKinsey/BCG action titles, Edward Tufte's data-ink ratio, Barbara Minto's Pyramid Principle
- Fits: academic/engineering reports, data-rigorous consulting pages, policy research reports, technical reviews
- Visual DNA: white/very light gray base + black body text + a single restrained accent color (deep blue/brick red). Type = full-sentence titles (not noun phrases), one dedicated chart under the title, text annotations embedded in the chart. Master layouts = ①full-sentence action titles ②single-chart evidence under the title ③zero bullets. Signature = full-sentence titles, single-chart evidence, embedded annotations, zero chartjunk, high data-ink ratio
- HTML implementation: layout hierarchy for full-sentence titles; pure CSS/inline SVG for minimal line/scatter charts (remove gridlines and legends, position annotations as text directly beside data points); zero decoration. Tufte's restraint is exactly HTML's strength
- Fonts: Source Serif / Lora titles + Inter body (dual-font reading grade)

**Institutional Swiss Minimal** `Quiet · 96% fidelity`
- Reference: Sequoia's official 10-page pitch template, Airbnb's 2009 seed-round deck, Müller-Brockmann grids, Massimo Vignelli
- Fits: investment roadshows, standard business proposals, problem-solution narratives, deco-lite brand proposals
- Visual DNA: pure white base + black/gray body text + a single brand accent color (Airbnb coral red #FF5A3C / neutral blue). Type = Helvetica-family sans-serif, medium-size bold one-sentence titles, body as short sentences with wide spacing. Master layouts = ①centered logo + slogan ②top one-sentence title bar + three-column antithesis below (Problem/Solution three points) ③layered TAM giant numbers ④2×2 competitor matrix. Signature = top title bars, three-column antithesis, monochrome accents, 2×2 matrices
- HTML implementation: Flexbox for three-column antithesis; pure CSS Grid + border for 2×2 matrices; nested divs or concentric squares for TAM layering; one message per page. Almost pure typographic grid, HTML's ideal subject
- Fonts: Inter / Helvetica Now replacing Helvetica; Inter for body

**Editorial Longform (magazine long-form flow)** `Quiet · 95% fidelity`
- Reference: Stripe Annual Letter ($1.9T), Amazon six-page narrative memos, Benedict Evans' 'X eats the world', Stripe Press
- Fits: annual letters/retrospective narratives, deep thought long-form essays, internal updates, research-report-style reading
- Visual DNA: cream/off-white base (#FBFAF8) + deep ink text + brand color highlights (Stripe purple #635BFF). Type = serif or high-quality sans-serif, prose paragraphs + inline data cards, oversized display numbers interspersed. Master layouts = ①masthead giant titles ②multi-column prose + inline metric cards ③giant-number paragraph anchors. Signature = publication reading rhythm, inline data cards, restrained whitespace, prose rather than bullets
- HTML implementation: column-count or Grid for multi-column; float/inline-block for inline data cards embedded in text; serif body with max-width line length ~65ch; oversized numbers interspersed. Pure typography, zero assets
- Fonts: Newsreader / Source Serif body + Inter support; tabular numbers

**Humanist Rounded Cards (Khan-style)** `Quiet · 80% fidelity`
- Reference: Khan Academy Wonder Blocks design system, Source Serif Pro serif, forest green brand, friendly humanism
- Fits: education products, approachable courseware, public/nonprofit decks, warm brand proposals
- Visual DNA: forest green #14BF96/#0A5C4B + cream white base + warm support colors, soft and non-harsh. Type = Source Serif serif titles (humanistic) + sans-serif body. Master layouts = ①rounded card component groups ②serif titles + approachable body ③real photography slots (downgraded to green-family geometric/rounded color blocks). Signature = forest green, serif titles, large rounded cards, humanistic warmth, imperfect approachable texture
- HTML implementation: large border-radius cards + soft box-shadows; serif font-family for titles; warm cream white base. Real teacher-student photography can't be done without AI image generation, downgraded to green-family geometric illustration blocks/large-rounded flat placeholders + emoji characters; missing photography drops fidelity by ~18%
- Fonts: Source Serif 4 titles + Nunito Sans / Inter body (Nunito's roundness echoes humanism)

**Dense Research Report (Meeker-style)** `Quiet · 92% fidelity`
- Reference: Mary Meeker's Internet Trends (BOND), CB Insights' State of AI, McKinsey Global Institute's Year in Charts, FT/Bloomberg data journalism
- Fits: trend research reports, industry data retrospectives, dense data reports, market maps
- Visual DNA: white base + brand color (BOND/CB Insights bright blue #0066FF) in a stepped monochrome highlight while everything else grays out, almost zero whitespace. Type = conclusion-style sentence titles, one chart density per page, tiny source footnotes. Master layouts = ①conclusion-sentence titles + full-page single chart ②logo grid market maps ③giant-number KPI cards ④dense multi-chart grids + footnotes. Signature = conclusion-sentence titles, zero-whitespace research-report feel, stepped monochrome highlights, logo market maps, footnote conventions
- HTML implementation: all dense charts drawn in pure CSS/inline SVG (bars/lines/stacks/scatter); Grid + text/SVG placeholder cells for logo market maps; CSS for KPI cards; small type for footnotes. Extreme information density is exactly what HTML excels at, zero assets
- Fonts: Inter + IBM Plex Sans + tabular Geist Mono for numbers

**All-Text Manifesto (Netflix/Amazon-style)** `Quiet · 97% fidelity`
- Reference: Netflix Culture Deck (2009, 125 pages), Amazon six-page narrative memos (Bezos), Tufte's anti-PowerPoint stance, Matthew Carter's reading-grade typography
- Fits: culture manifestos, values presentations, deep memos, anti-PPT pure-document presentations
- Visual DNA: pure white or pure black base + a single accent color (Netflix red #E50914) as the only highlight, extreme restraint. Type = reading-grade typography, one page one viewpoint, golden-quote assertions/pure prose with zero bullets zero images. Master layouts = ①full-bleed base + golden-quote assertions ②colloquial candid paragraphs ③institutional-term highlights (Keeper Test) ④six pages of prose + appendix table. Signature = pure text one-page-one-viewpoint, zero images zero bullets, monochrome highlighted golden quotes, colloquial candor, silent-read document feel
- HTML implementation: pure typography: large clamp() left-aligned hierarchy for golden quotes; max-width for prose line length; the single accent color as a span highlighting key phrases; a minimal table for the appendix. Zero assets zero images, pure text is HTML's most stable reproduction
- Fonts: Newsreader / Source Serif (reading grade) or Inter (manifesto style); Archivo extra-bold optional for titles

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
| Sagmeister & Walsh (color explosion) | Handmade objects + experimental layout | The clashing-color skeleton is doable (already merged into web 'Memphis' and PPT 'mono-brand poster'), but the handmade texture can't be done |

> These aren't "bad", they're "wrong medium" — their native medium is AI-direct images, not the browser DOM.

---

## Default Aesthetic Forbidden Zones (users may override per their own brand)

- ❌ **GitHub-dark lazy fix**: uniform deep-blue base (#0D1117) + generic cyan/purple neon glow — only this one overused combination is banned, not "all dark styles"
- ✅ **Not forbidden**: cinematic dramatic lighting, warm cyberpunk (Ash Thorp orange/cyan), sports-poetry dark-field narratives — dark styles with authorial intent stay (this library's 'Linear dark glow', 'Black Big-Number Stage', and 'CS50 Candy Stage' are all legitimate dark styles)
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

**Version**: v3.0 (2026-06 fully restructured as an HTML-native 40-style library)
**Applies to**: the default HTML path for all visual design — web/PPT/PDF/infographics/covers/Apps etc.
