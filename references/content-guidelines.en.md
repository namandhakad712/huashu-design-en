# Content Guidelines: Anti-AI Slop, Content Rules, Scale Standards

The most common traps in AI design. This is a "what not to do" checklist — more important than "what to do" — because AI slop is the default, it happens if you don't actively avoid it.

## Complete AI Slop Blacklist

### Visual Traps

**❌ Aggressive gradient backgrounds**
- Purple → pink → blue fullscreen gradient (typical AI-generated web smell)
- Rainbow gradient in any direction
- Mesh gradient covering entire background
- ✅ If using gradients: subtle, single color family, intentional点缀 (e.g., button hover)

**❌ Rounded cards + left border accent**
```css
/* This is the typical signature of AI-flavored cards */
.card {
  border-radius: 12px;
  border-left: 4px solid #3b82f6;
  padding: 16px;
}
```
This card style is everywhere in AI-generated Dashboards. Want emphasis? Use more designed methods: background color contrast, font weight/size contrast, plain dividers, or no cards at all.

**❌ Emoji decoration**
Unless brand itself uses emoji (e.g., Notion, Slack), don't put emoji on UI. **Especially don't**:
- 🚀 ⚡️ ✨ 🎯 💡 before titles
- ✅ in feature lists
- → inside CTA buttons (arrow alone OK, emoji arrow not)

No icons? Use real icon libraries (Lucide/Heroicons/Phosphor), or use placeholder.

**❌ SVG illustration**
Don't try to draw with SVG: people, scenes, devices, objects, abstract art. AI-drawn SVG illustrations instantly scream AI, childish and cheap. **A gray rectangle with "Illustration placeholder 1200×800" text label is 100× better than a拙劣 SVG hero illustration**.

Only scenarios where SVG is usable:
- Real icons (16×16 to 32×32 level)
- Geometric shapes as decorative elements
- Data viz charts

**❌ Overkill iconography**
Not every title/feature/section needs an icon. Icon abuse makes interface look like a toy. Less is more.

**❌ "Data slop"**
Fabricated stats decoration:
- "10,000+ happy customers" (you don't know if that's true)
- "99.9% uptime" (don't write if no real data)
- Decorative "metric cards" made of icon + number + word
- Fancily dressed-up fake data in mock tables

If no real data, leave placeholder or ask user.

**❌ "Quote slop"**
Fabricated user reviews, famous quotes decorating page. Leave placeholder, ask user for real quote.

### Typography Traps

**❌ Avoid these overused fonts**:
- Inter (AI-generated web default)
- Roboto
- Arial / Helvetica
- Pure system font stack
- Fraunces (AI discovered and overused this)
- Space Grotesk (AI's recent favorite)

**✅ Use distinctive display+body pairing**. Inspiration directions:
- Serif display + sans body (editorial feel)
- Mono display + sans body (technical feel)
- Heavy display + light body (contrast)
- Variable font for hero weight animation

Font resources:
- Underserved good options from Google Fonts (Instrument Serif, Cormorant, Bricolage Grotesque, JetBrains Mono)
- Open source font sites (Fraunces siblings, Adobe Fonts)
- Don't invent font names from nothing

### Color Traps

**❌ Inventing colors from nothing**
Don't design a whole unfamiliar color system from scratch. Usually not harmonious.

**✅ Strategy**:
1. Have brand colors → use brand colors, missing color tokens use oklch interpolation
2. No brand colors but have reference → extract colors from reference product screenshot
3. Start from zero entirely → pick a known color system (Radix Colors / Tailwind default palette / Anthropic brand), don't tune yourself

**Defining colors with oklch** is the most modern approach:
```css
:root {
  --primary: oklch(0.65 0.18 25);      /* warm terracotta */
  --primary-light: oklch(0.85 0.08 25); /* same color family light */
  --primary-dark: oklch(0.45 0.20 25);  /* same color family dark */
}
```
oklch guarantees hue doesn't drift when adjusting lightness, better than hsl.

**❌ Adding dark mode by simple invert**
Not simple color invert. Good dark mode needs resaturated colors, adjusted contrast, changed accent colors. Don't do dark mode if you don't want to do it right.

### Layout Traps

**❌ Overused Bento grid**
Every AI-generated landing page wants bento. Unless your information structure really suits bento, use other layouts.

**❌ Large hero + 3-column features + testimonials + CTA**
This landing page template is exhausted. If innovating, really innovate.

**❌ Every card in card grid looks the same**
Asymmetric, different sizes, some with images some only text, some spanning columns — that's what real designers do.

## Content Rules

### 1. Don't add filler content

Every element must earn its place. White space is a design problem, solved through **composition** (contrast, rhythm, whitespace), **not** by filling with content.

**Judging filler problems**:
- If removing this content, would the design get worse? If answer is "no", remove.
- What real problem does this element solve? If it's "make page not so empty", delete.
- Is this stats/quote/feature backed by real data? If not, don't invent.

"One thousand no's for every yes".

### 2. Ask before adding material

Think adding another paragraph/page/section would be better? Ask user first, don't unilaterally add.

Reason:
- User knows their audience better than you
- Adding content has cost, user may not want it
- Unilaterally adding content violates "junior designer reporting to work" relationship

### 3. Create a system up front

After exploring design context, **first say out loud the system you'll use**, let user confirm:

```markdown
My design system:
- Colors: #1A1A1A main + #F0EEE6 background + #D97757 accent (from your brand)
- Typography: Instrument Serif for display + Geist Sans for body
- Rhythm: section title uses full-bleed colored background + white text; regular sections use white background
- Images: hero uses full-bleed photo, feature section uses placeholder waiting for you
- Use at most 2 background colors to avoid clutter

Confirm this direction and I start.
```

Proceed after user confirms. This check-in avoids "halfway done才发现 direction wrong".

## Scale Standards

### Slides (1920×1080)

- Body minimum **24px**, ideal 28-36px
- Titles 60-120px
- Section titles 80-160px
- Hero headline can use 180-240px large text
- Never use <24px text on slides

### Print Documents

- Body minimum **10pt** (≈13.3px), ideal 11-12pt
- Titles 18-36pt
- Captions 8-9pt

### Web and Mobile

- Body minimum **14px** (use 16px for elderly-friendly)
- Mobile body **16px** (prevents iOS auto-zoom)
- Hit targets (clickable elements) minimum **44×44px**
- Line height 1.5-1.7 (Chinese 1.7-1.8)

### Contrast

- Body vs background **at least 4.5:1** (WCAG AA)
- Large text vs background **at least 3:1**
- Use Chrome DevTools accessibility tool to check

## CSS Superpowers

**Advanced CSS features** are designers' good friends, use boldly:

### Typography

```css
/* More natural title line breaks, last line won't be lonely word */
h1, h2, h3 { text-wrap: balance; }

/* Body text wrapping, avoid widows and orphans */
p { text-wrap: pretty; }

/* Chinese typography essential: punctuation compression, line start/end control */
p { 
  text-spacing-trim: space-all;
  hanging-punctuation: first;
}
```

### Layout

```css
/* CSS Grid + named areas = readability through the roof */
.layout {
  display: grid;
  grid-template-areas:
    "header header"
    "sidebar main"
    "footer footer";
  grid-template-columns: 240px 1fr;
  grid-template-rows: auto 1fr auto;
}

/* Subgrid aligns card content */
.card { display: grid; grid-template-rows: subgrid; }
```

### Visual Effects

```css
/* Stylish scrollbar */
* { scrollbar-width: thin; scrollbar-color: #666 transparent; }

/* Glassmorphism (use sparingly) */
.glass {
  backdrop-filter: blur(20px) saturate(150%);
  background: color-mix(in oklch, white 70%, transparent);
}

/* View transitions API makes page switches silky */
@view-transition { navigation: auto; }
```

### Interaction

```css
/* :has() selector makes conditional styling easier */
.card:has(img) { padding-top: 0; } /* Cards with images no top padding */

/* container queries make components truly responsive */
@container (min-width: 500px) { ... }

/* New color-mix function */
.button:hover {
  background: color-mix(in oklch, var(--primary) 85%, black);
}
```

## Decision Quick Reference: When in Doubt

- Want to add a gradient? → Mostly don't add
- Want to add an emoji? → Don't add
- Want to add rounded corners + border-left accent to card? → Don't, change method
- Want to draw hero illustration with SVG? → Don't, use placeholder
- Want to add decorative quote? → First ask user if they have real quote
- Want to add row of icon features? → First ask if icons needed, may not need
- Using Inter? → Change to more distinctive
- Using purple gradient? → Change to color with basis

**When you feel "adding this will look better" — that's usually a sign of AI slop**. Start with simplest version, only add when user asks.