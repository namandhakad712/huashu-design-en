# Content Guidelines: Anti-AI Slop, Content Rules, Scale Standards

The most common trap to fall into in AI design. This is a "what not to do" checklist — more important than "what to do" — because AI slop is the default; if you don't actively avoid it, it happens.

## Complete AI Slop Blacklist

### Visual traps

**❌ Aggressive gradient backgrounds**
- Purple → pink → blue full-screen gradients (the typical flavor of AI-generated webpages)
- Rainbow gradients in any direction
- Mesh gradients covering the background
- ✅ If you must use a gradient: subtle, monochromatic, applied with intent (e.g. a button hover)

**❌ Rounded cards + left border accent color**
```css
/* This is the typical signature of an AI-flavored card */
.card {
  border-radius: 12px;
  border-left: 4px solid #3b82f6;
  padding: 16px;
}
```
This kind of card is everywhere in AI-generated dashboards. Want emphasis? Use a more designed approach: background-color contrast, weight/size contrast, a plain divider, or just don't use a card at all.

**❌ Emoji decoration**
Unless the brand itself uses emoji (e.g. Notion, Slack), don't put emoji in the UI. **Especially not**:
- 🚀 ⚡️ ✨ 🎯 💡 in front of headings
- ✅ in feature lists
- → in CTA buttons (a standalone arrow is fine; an emoji arrow is not)

No icon? Use a real icon library (Lucide/Heroicons/Phosphor), or use a placeholder.

**❌ SVG for imagery**
Don't try to draw with SVG: people, scenes, devices, objects, abstract art. AI-drawn SVG imagery screams AI at a glance — childish and cheap. **A gray rectangle with the text label "illustration placeholder 1200×800" is 100 times better than a clumsy SVG hero illustration**.

The only scenarios where SVG is allowed:
- Real icons (16×16 to 32×32 scale)
- Geometric shapes as decorative elements
- Charts for data viz

**❌ Too much iconography**
Not every heading/feature/section needs an icon. Overusing icons makes the interface look like a toy. Less is more.

**❌ "Data slop"**
Fabricated stats as decoration:
- "10,000+ happy customers" (you don't even know if that's true)
- "99.9% uptime" (don't write it without real data)
- Decorative "metric cards" made of icon + number + word
- Mock tables dressed up with fake data

If there's no real data, leave a placeholder or ask the user.

**❌ "Quote slop"**
Fabricated user testimonials or famous quotes decorating the page. Leave a placeholder and ask the user for a real quote.

### Typography traps

**❌ Avoid these overused typefaces**:
- Inter (the default for AI-generated webpages)
- Roboto
- Arial / Helvetica
- Bare system font stacks
- Fraunces (AI discovered it and ran it into the ground)
- Space Grotesk (recent AI favorite)

**✅ Use a distinctive display+body pairing**. Direction inspiration:
- Serif display + sans body (editorial feel)
- Mono display + sans body (technical feel)
- Heavy display + light body (contrast)
- A variable font for hero weight animation

Typeface resources:
- Underrated gems on Google Fonts (Instrument Serif, Cormorant, Bricolage Grotesque, JetBrains Mono)
- Open-source typeface sites (Fraunces' sibling faces, Adobe Fonts)
- Don't invent typeface names out of thin air

### Color traps

**❌ Inventing colors out of thin air**
Don't design an entire unfamiliar color system from scratch. It's usually inharmonious.

**✅ Strategy**:
1. Have brand colors → use them, interpolate the missing color tokens with oklch
2. No brand colors but have a reference → eyedrop colors from the reference product screenshots
3. Starting completely from zero → pick a known color system (Radix Colors / Tailwind default palette / Anthropic brand), don't tune it yourself

**Defining colors in oklch** is the most modern approach:
```css
:root {
  --primary: oklch(0.65 0.18 25);      /* warm terracotta */
  --primary-light: oklch(0.85 0.08 25); /* lighter, same hue */
  --primary-dark: oklch(0.45 0.20 25);  /* darker, same hue */
}
```
oklch guarantees the hue doesn't drift when you adjust lightness — easier to use than hsl.

**❌ Slapping inverted colors on dark mode**
It's not simply inverting colors. Good dark mode requires re-adjusting saturation, contrast, and accent colors. If you don't want to do dark mode, don't.

### Layout traps

**❌ Bento grid overuse**
Every AI-generated landing page wants to be a bento. Unless your information structure genuinely suits a bento, use another layout.

**❌ Big hero + 3-column features + testimonials + CTA**
This landing page template is played out. If you want to innovate, actually innovate.

**❌ Every card in the grid looks the same**
Asymmetric cards, different sizes, some with images and some text-only, some spanning columns — that's what a real designer does.

## Content Rules

### 1. Don't add filler content

Every element must earn its place. Empty space is a design problem, solved with **composition** (contrast, rhythm, whitespace), **not** by filling it with content.

**Questions to judge filler**:
- If you remove this content, does the design get worse? If the answer is "no", remove it.
- What real problem does this element solve? If it's "to make the page less empty", delete it.
- Is this stat/quote/feature backed by real data? If not, don't write it from nothing.

「One thousand no's for every yes」.

### 2. Ask before adding material

You think adding another paragraph/page/section would be better? Ask the user first — don't add unilaterally.

Why:
- The user knows their audience better than you do
- Adding content has a cost; the user may not want it
- Adding content unilaterally violates the "junior designer reporting to the lead" relationship

### 3. Create a system up front

After exploring the design context, **state the system you plan to use verbally first**, and get the user to confirm:

```markdown
My design system:
- Color: #1A1A1A primary + #F0EEE6 background + #D97757 accent (from your brand)
- Typography: Instrument Serif for display + Geist Sans for body
- Rhythm: section titles get full-bleed colored backgrounds + white text; regular sections use white backgrounds
- Imagery: full-bleed photos for the hero, placeholders for feature sections until you provide them
- At most 2 background colors, to avoid clutter

Once you confirm this direction I'll start.
```

Get the user's confirmation before starting. This check-in avoids "finishing halfway and finding the direction was wrong".

## Scale Standards

### Slides (1920×1080)

- Body text minimum **24px**, ideal 28-36px
- Titles 60-120px
- Section titles 80-160px
- Hero headlines can use large type at 180-240px
- Never put text smaller than 24px on a slide

### Print documents

- Body text minimum **10pt** (≈13.3px), ideal 11-12pt
- Titles 18-36pt
- Captions 8-9pt

### Web and mobile

- Body text minimum **14px** (use 16px for elderly-friendly)
- Mobile body text **16px** (to avoid iOS auto-zoom)
- Hit targets (clickable elements) minimum **44×44px**
- Line height 1.5-1.7 (1.7-1.8 for Chinese)

### Contrast

- Body vs background **at least 4.5:1** (WCAG AA)
- Large text vs background **at least 3:1**
- Check with Chrome DevTools' accessibility tools

## CSS Power Tools

**Advanced CSS features** are a designer's best friend — use them boldly:

### Typography

```css
/* Make headings wrap more naturally, no lone orphan word on the last line */
h1, h2, h3 { text-wrap: balance; }

/* Body text wrapping, avoiding widows and orphans */
p { text-wrap: pretty; }

/* Chinese typography power-ups: punctuation squeezing, start/end line control */
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

### Visual effects

```css
/* Designed scrollbars */
* { scrollbar-width: thin; scrollbar-color: #666 transparent; }

/* Glassmorphism (use with restraint) */
.glass {
  backdrop-filter: blur(20px) saturate(150%);
  background: color-mix(in oklch, white 70%, transparent);
}

/* View transitions API for silky page transitions */
@view-transition { navigation: auto; }
```

### Interaction

```css
/* :has() selector makes conditional styling easy */
.card:has(img) { padding-top: 0; } /* cards with images get no top padding */

/* Container queries make components truly responsive */
@container (min-width: 500px) { ... }

/* The new color-mix function */
.button:hover {
  background: color-mix(in oklch, var(--primary) 85%, black);
}
```

## Decision Quick Reference: when you're hesitating

- Want to add a gradient? → Most likely don't
- Want to add an emoji? → Don't
- Want to give cards rounded corners + border-left accent? → Don't, use another approach
- Want to draw a hero illustration in SVG? → Don't, use a placeholder
- Want to add a decorative quote? → First ask the user if they have a real quote
- Want to add a row of icon features? → First ask whether icons are wanted; maybe not
- Using Inter? → Swap for something more distinctive
- Using a purple gradient? → Swap for a color scheme with a basis

**When you think "adding this would look nicer" — that's usually a sign of AI slop**. Do the most minimal version first; only add when the user asks.
