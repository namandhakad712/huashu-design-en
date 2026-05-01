# Design Context: Start from Existing Context

**This is the most important one thing for this skill.**

Good hi-fi design always grows from existing design context. **Creating hi-fi from nothing is a last resort and will always produce generic work.** So at the start of every design task, first ask: is there anything to reference?

## What is Design Context

Priority from high to low:

### 1. User's Design System/UI Kit
User's existing component library, color tokens, typography specs, icon system. **Most perfect scenario**.

### 2. User's Codebase
If user gave codebase, there are living component implementations. Read those component files:
- `theme.ts` / `colors.ts` / `tokens.css` / `_variables.scss`
- Specific components (Button.tsx, Card.tsx)
- Layout scaffold (App.tsx, MainLayout.tsx)
- Global stylesheets

**Read code to copy exact values**: hex codes, spacing scale, font stack, border radius. Don't redraw from memory.

### 3. User's Released Product
If user has released product but didn't give code, use Playwright or have user provide screenshots.

```bash
# Screenshot a public URL using Playwright
npx playwright screenshot https://example.com screenshot.png --viewport-size=1920,1080
```

Lets you see real visual vocabulary.

### 4. Brand Guidelines/Logo/Existing Assets
User may have: Logo files, brand color specs, marketing materials, slide templates. All are context.

### 5. Competitor Reference
User says "like XX website" — get URL or screenshot from them. **Don't** do based on your training data's vague impression.

### 6. Known Design Systems (fallback)
If none of above, use recognized design systems as base:
- Apple HIG
- Material Design 3
- Radix Colors (colors)
- shadcn/ui (components)
- Tailwind default palette

Explicitly tell user what you used, let them know it's starting point not final.

## Getting Context Process

### Step 1: Ask User

Must-ask checklist at task start (from `workflow.md`):

```markdown
1. Do you have existing design system/UI kit/component library? Where?
2. Have brand guidelines, color/typography specs?
3. Can you give me screenshots or URL of existing product?
4. Is there a codebase I can read?
```

### Step 2: User Says "None" — Help Find

Don't give up directly. Try:

```markdown
Let me see if there's any线索:
- Do you have related designs from previous projects?
- What colors/typography does your company's marketing website use?
- What's the style of your product's logo? Can you send me one?
- Any products you admire as reference?
```

### Step 3: Read All Context Found

If user gave codebase path, you read:
1. **First list file structure**: find style/theme/component related files
2. **Read theme/token files**: lift specific hex/px values
3. **Read 2-3 representative components**: see visual vocabulary (hover state, shadow, border, padding node pattern)
4. **Read global stylesheet**: base resets, font loading
5. **If Figma link/screenshots**: look at images, but **trust code more**

**Important**: **Don't** glance and do from impression. Only truly lifted when you have 30+ specific values.

### Step 4: Vocalize System You're Using

After reviewing context, tell user system you'll use:

```markdown
Based on your codebase and product screenshots, the design system I extracted:

**Colors**
- Primary: #C27558 (from tokens.css)
- Background: #FDF9F0
- Text: #1A1A1A
- Muted: #6B6B6B

**Typography**
- Display: Instrument Serif (from global.css @font-face)
- Body: Geist Sans
- Mono: JetBrains Mono

**Spacing** (from your scale system)
- 4, 8, 12, 16, 24, 32, 48, 64

**Shadow pattern**
- `0 1px 2px rgba(0,0,0,0.04)` (subtle card)
- `0 10px 40px rgba(0,0,0,0.1)` (elevated modal)

**Border-radius**
- Small components 4px, cards 12px, buttons 8px

**Component vocabulary**
- Button: filled primary, outlined secondary, ghost tertiary, all 8px rounded
- Card: white background, subtle shadow, no border

I'll start working with this system. Confirm okay?
```

Proceed after user confirms.

## Designing from Nothing (Fallback When No Context)

**Strong warning**: Output quality significantly degrades in this situation. Explicitly tell user.

```markdown
You have no design context, so I can only work from generic intuition.
Output will be "looks okay but lacks uniqueness".
Do you want to continue, or first add some reference materials?
```

If user insists you proceed, make decisions in this order:

### 1. Choose an aesthetic direction
Don't give generic result. Pick a clear direction:
- brutally minimal
- editorial/magazine
- brutalist/raw
- organic/natural
- luxury/refined
- playful/toy
- retro-futuristic
- soft/pastel

Tell user which you chose.

### 2. Choose known design system as skeleton
- Use Radix Colors for palette (https://www.radix-ui.com/colors)
- Use shadcn/ui for component vocabulary (https://ui.shadcn.com)
- Use Tailwind spacing scale (multiples of 4)

### 3. Choose distinctive font pairing

Don't use Inter/Roboto. Recommended combos (free from Google Fonts):
- Instrument Serif + Geist Sans
- Cormorant Garamond + Inter Tight
- Bricolage Grotesque + Söhne (paid)
- Fraunces + Work Sans (note: Fraunces already overused by AI)
- JetBrains Mono + Geist Sans (technical feel)

### 4. Every key decision has reasoning

Don't choose silently. Write in HTML comments:

```html
<!--
Design decisions:
- Primary color: warm terracotta (oklch 0.65 0.18 25) — fits the "editorial" direction  
- Display: Instrument Serif for humanist, literary feel
- Body: Geist Sans for cleanness contrast
- No gradients — committed to minimal, no AI slop
- Spacing: 8px base, golden ratio friendly (8/13/21/34)
-->
```

## Import Strategy (User Gives Codebase)

If user says "import this codebase for reference":

### Small (<50 files)
Read all, internalize context.

### Medium (50-500 files)
Focus on:
- `src/components/` or `components/`
- All styles/tokens/theme related files
- 2-3 representative full-page components (Home.tsx, Dashboard.tsx)

### Large (>500 files)
Let user specify focus:
- "I need to make settings page" → read existing settings related
- "I need to make a new feature" → read overall shell + closest reference
- Don't seek completeness, seek accuracy.

## Working with Figma/Design Files

If user gave Figma link:

- **Don't** expect you can directly "convert Figma to HTML" — that needs extra tools
- Figma links usually not publicly accessible
- Let user: export as **screenshot** send to you + tell you specific color/spacing values

If only got Figma screenshot, tell user:
- I can see visuals, but can't extract precise values
- Key numbers (hex, px) tell me, or export as code (Figma supports)

## Final Reminder

**A project's design quality ceiling is determined by the quality of context you receive.**

Spending 10 minutes collecting context is more valuable than 1 hour creating hi-fi from nothing.

**When encountering no context situation, prioritize asking user rather than forcing through.**