# Core Asset Protocol (full version)

> The full protocol descended from SKILL.md "Core Philosophy #1.a" (2026-06 slim-down). SKILL.md keeps the trigger conditions + 5-step titles + self-check; here are the 5 steps in detailed operation, download commands, the brand-spec template, full-process failure fallbacks, and anti-examples with cost comparisons.
> Trigger: enforced whenever a task involves a specific brand/product. Return to SKILL.md for the condensed version and context.

#### 1.a Core Asset Protocol (enforced when a specific brand is involved)

> **This is v1's most core constraint and the lifeline of stability.** Whether the agent walks this protocol directly determines whether output quality is 40 or 90 points. Don't skip any step.
>
> **v1.1 refactor (2026-04-20)**: upgraded from "Brand Asset Protocol" to "Core Asset Protocol". The previous version over-focused on color values and fonts, missing the most basic things in design — logo / product images / UI screenshots. The original author's words: "Besides the so-called brand color, we should obviously find and use DJI's logo, use Pocket 4's product image. If it's a non-physical product like a website or app, the logo should at least be a must. This might be a more basic logic than the so-called brand design spec. Otherwise, what are we expressing?"

**Trigger condition**: the task involves a specific brand — the user named a product/company/specific client (Stripe, Linear, Anthropic, Notion, Lovart, DJI, their own company, etc.), regardless of whether the user proactively provided brand materials.

**Precondition**: before walking the protocol you must have confirmed via "#0 verify facts before assumptions" that the brand/product exists and its status is known. If you're not sure whether the product is released/specs/version yet, go search first.

##### Core idea: assets > specs

**A brand's essence is "being recognized"**. Recognized by what? Ranked by recognition power:

| Asset type | Recognition contribution | Necessity |
|---|---|---|
| **Logo** | Highest · any brand is recognized at a glance when its logo appears | **Required for every brand** |
| **Product image / product render** | Extremely high · a physical product's "protagonist" is the product itself | **Required for physical products (hardware/packaging/consumer goods)** |
| **UI screenshot / interface assets** | Extremely high · a digital product's "protagonist" is its interface | **Required for digital products (App/website/SaaS)** |
| **Color values** | Medium · auxiliary recognition; often clashes with others when the first three are absent | Auxiliary |
| **Fonts** | Low · needs the above to establish recognition | Auxiliary |
| **Character keywords** | Low · for agent self-check | Auxiliary |

**Translated into execution rules**:
- Only extracting color values + fonts without finding logo / product image / UI → **violates this protocol**
- Using CSS silhouettes / hand-drawn SVG to substitute for real product images → **violates this protocol** (the output is just "generic tech animation," every brand looks the same)
- Not telling the user when assets can't be found, not AI-generating, and forcing it through → **violates this protocol**
- Better to stop and ask the user for assets than to fill with generic content

##### 5-step hard process (each step has a fallback, never silently skipped)

##### Step 1 · Ask (ask the whole asset list at once)

Don't just ask "do you have brand guidelines?" — it's too broad, the user doesn't know what to give. Ask item by item against the list:

```
Regarding <brand/product>, which of the following do you have on hand? Listed by priority:
1. Logo (SVG / high-res PNG) —— required for any brand
2. Product image / official render —— required for physical products (e.g. DJI Pocket 4 product photos)
3. UI screenshot / interface assets —— required for digital products (e.g. screenshots of the app's main pages)
4. Color value list (HEX / RGB / brand color palette)
5. Font list (Display / Body)
6. Brand guidelines PDF / Figma design system / brand website link

If you have any, send them over; if not, I'll search/scrape/generate them.
```

##### Step 2 · Search official channels (by asset type)

| Asset | Search path |
|---|---|
| **Logo** | `<brand>.com/brand` · `<brand>.com/press` · `<brand>.com/press-kit` · `brand.<brand>.com` · inline SVG in the site's header |
| **Product image/render** | `<brand>.com/<product>` product detail page hero image + gallery · official YouTube launch film frames · images attached to official press releases |
| **UI screenshot** | App Store / Google Play product page screenshots · official site screenshots section · frames from the product's official demo video |
| **Color values** | official site inline CSS / Tailwind config / brand guidelines PDF |
| **Fonts** | official site `<link rel="stylesheet">` references · Google Fonts tracking · brand guidelines |

`WebSearch` fallback keywords:
- Logo not found → `<brand> logo download SVG`, `<brand> press kit`
- Product image not found → `<brand> <product> official renders`, `<brand> <product> product photography`
- UI not found → `<brand> app screenshots`, `<brand> dashboard UI`

##### Step 3 · Download assets · three fallback paths per type

**3.1 Logo (required for any brand)**

> ⚠️ **Don't give up after only trying `curl <brand>.com/logo.svg`** — most official sites today are SPAs; hitting a static path directly mostly returns empty-shell HTML (2026-06-06 test: all 5 direct paths to the Trae official site were empty shells). **For digital products / SaaS / AI tools, prefer icon aggregation sources first** — highest hit rate, clean SVG right out.

By descending success rate:
0. **Icon aggregation source (first choice for well-known digital products/SaaS/AI tools, highest hit rate)**:
   ```bash
   unset ALL_PROXY HTTP_PROXY HTTPS_PROXY all_proxy http_proxy https_proxy   # clear proxy, otherwise TLS tends to break
   # svgl —— most complete coverage of AI/developer brands (Claude/Cursor/OpenAI/Copilot/Anthropic/Vercel…), includes light/dark + wordmark
   curl -s "https://api.svgl.app?search=<brand>"   # returns JSON, take the svg URL from route(.light/.dark), then download
   # simpleicons —— monochrome glyph, can be colored directly with the brand color
   curl -o logo.svg "https://cdn.simpleicons.org/<slug>/<hexcolor>"
   ```
1. Standalone SVG/PNG file / official brand page (e.g. `<brand>.com/brand`, `/press`):
   ```bash
   curl -A "Mozilla/5.0" -L -o assets/<brand>-brand/logo.svg "<official-logo-url>"
   ```
2. Extract inline SVG from the full official site HTML:
   ```bash
   curl -A "Mozilla/5.0" -L https://<brand>.com -o assets/<brand>-brand/homepage.html
   # then grep <svg>...</svg> to extract the logo node
   ```
3. **Google favicon service (real site mark fallback, almost never fails)**:
   ```bash
   curl -o logo.png "https://www.google.com/s2/favicons?domain=<brand-domain>&sz=256"   # 256px official site icon
   ```
4. Official social media avatar (last resort): GitHub/Twitter/LinkedIn company avatars are usually 400×400 or 800×800 transparent-background PNGs

After downloading, **verify each one**: `file <logo>` confirms it's a real SVG/PNG (not a 106-byte placeholder or HTML empty shell), `head -c 90 <logo.svg>` checks it starts with `<svg`.

**3.2 Product image / render (required for physical products)**

By priority:
1. **Official product page hero image** (highest priority): right-click to view image address / fetch with curl. Usually 2000px+ resolution
2. **Official press kit**: `<brand>.com/press` often has high-res product images for download
3. **Official launch video frames**: use `yt-dlp` to download the YouTube video, extract a few high-res frames with ffmpeg
4. **Wikimedia Commons**: public domain often has them
5. **AI generation fallback** (nano-banana-pro): send the real product image to the AI as reference, let it generate variants that fit the animation scene. **Don't hand-draw with CSS/SVG instead**

```bash
# example: download the DJI official product hero image
curl -A "Mozilla/5.0" -L "<hero-image-url>" -o assets/<brand>-brand/product-hero.png
```

**3.3 UI screenshots (required for digital products)**

- App Store / Google Play product screenshots (note: may be mockups rather than the real UI — compare)
- Official site screenshots section
- Frames from product demo videos
- Product's official Twitter/X launch screenshots (often the latest version)
- When the user has an account, screenshot the real product interface directly

**3.4 · Asset quality gate "5-10-2-8" principle (iron law)**

> **The logo's rules differ from other assets**. If the logo exists you must use it (if it doesn't, stop and ask the user); other assets (product images/UI/reference images/illustrations) follow the "5-10-2-8" quality gate.
>
> 2026-04-20, the original author's words: "Our principle is to search 5 rounds, find 10 assets, pick 2 good ones. Each needs to score 8/10 or above. Better to have fewer than to pad the task with inferior substitutes."

| Dimension | Standard | Anti-pattern |
|---|---|---|
| **5 search rounds** | Cross-channel searches (official site / press kit / official social media / YouTube frames / Wikimedia / user-account screenshots), not stopping after grabbing the top 2 in one round | Using first-page results directly |
| **10 candidates** | Gather at least 10 candidates before starting to filter | Only grabbing 2, no choice at all |
| **Pick 2 good ones** | Select 2 from the 10 as the final assets | Using everything = visual overload + diluted taste |
| **Each 8/10 or above** | Under 8 points, **rather not use** — use an honest placeholder (gray block + text label) or AI generation (nano-banana-pro based on the official reference) | Padding 7-point assets into brand-spec.md |

**The 8/10 scoring dimensions** (record scores in `brand-spec.md` when scoring):

1. **Resolution** · ≥2000px (≥3000px for print / large-screen scenarios)
2. **Copyright clarity** · official source > public domain > free stock > suspected stolen (stolen = straight 0)
3. **Fit with brand character** · consistent with the "character keywords" in brand-spec.md
4. **Light / composition / style consistency** · the 2 assets don't clash when placed together
5. **Standalone narrative ability** · can express a narrative role on its own (not decoration)

**Why this gate is an iron law**:
- The original author's philosophy: **rather go without than go bad**. Inferior filler is worse than none — it pollutes visual taste and signals "unprofessional"
- **The quantified version of "do one detail at 120%, everything else at 80%"**: 8 is the floor of "the other 80%"; real hero assets need 9-10
- When viewers evaluate work, every visual element is **adding or subtracting points**. A 7-point asset is a deduction — better to leave it empty

**The logo exception** (restated): if it exists you must use it; "5-10-2-8" doesn't apply. Because the logo isn't a "pick one of many" problem but a "foundation of recognition" problem — even a logo scoring only 6 is 10 times better than having no logo at all.

##### Step 4 · Verify + extract (not just grepping color values)

| Asset | Verification action |
|---|---|
| **Logo** | file exists + SVG/PNG opens + at least two versions (for dark/light backgrounds) + transparent background |
| **Product image** | at least one 2000px+ resolution + cutout or clean background + multiple angles (main view, detail, scene) |
| **UI screenshot** | real resolution (1x / 2x) + latest version (not an old one) + no user-data contamination |
| **Color values** | `grep -hoE '#[0-9A-Fa-f]{6}' assets/<brand>-brand/*.{svg,html,css} \| sort \| uniq -c \| sort -rn \| head -20`, filter out black/white/gray |

**Beware demo-brand contamination**: product screenshots often contain the brand colors of a demo (e.g. a tool's screenshot demoing Heytea red) — that's not the tool's color. **When two strong colors appear at once, you must distinguish them.**

**Brand facets**: the same brand's marketing color on the official site often differs from its product UI color (Lovart's site is warm beige + orange, its product UI is Charcoal + Lime). **Both sets are real** — pick the appropriate facet based on the delivery scenario.

##### Step 5 · Solidify into a `brand-spec.md` file (the template must cover all assets)

```markdown
# <Brand> · Brand Spec
> Collection date: YYYY-MM-DD
> Asset sources: <list download sources>
> Asset completeness: <complete / partial / inferred>

## 🎯 Core assets (first-class citizens)

### Logo
- Main version: `assets/<brand>-brand/logo.svg`
- Reverse-color version for light backgrounds: `assets/<brand>-brand/logo-white.svg`
- Use cases: <opening/closing/corner watermark/global>
- Forbidden distortions: <no stretching/recoloring/adding outlines>

### Product image (required for physical products)
- Main view: `assets/<brand>-brand/product-hero.png` (2000×1500)
- Detail shots: `assets/<brand>-brand/product-detail-1.png` / `product-detail-2.png`
- Scene shot: `assets/<brand>-brand/product-scene.png`
- Use cases: <close-up/rotation/comparison>

### UI screenshots (required for digital products)
- Home page: `assets/<brand>-brand/ui-home.png`
- Core feature: `assets/<brand>-brand/ui-feature-<name>.png`
- Use cases: <product showcase/Dashboard fade-in/comparison demo>

## 🎨 Auxiliary assets

### Color palette
- Primary: #XXXXXX  <source annotation>
- Background: #XXXXXX
- Ink: #XXXXXX
- Accent: #XXXXXX
- Forbidden colors: <color families the brand explicitly doesn't use>

### Typography
- Display: <font stack>
- Body: <font stack>
- Mono (for data HUDs): <font stack>

### Signature details
- <which details are the "done at 120%">

### Restricted zones
- <explicitly forbidden: e.g. Lovart doesn't use blue, Stripe doesn't use low-saturation warm colors>

### Character keywords
- <3-5 adjectives>
```

**Execution discipline after writing the spec (hard requirement)**:
- All HTML must **reference** the asset file paths in `brand-spec.md`; substituting with CSS silhouettes / hand-drawn SVG is not allowed
- The logo is referenced as an `<img>` pointing at the real file, never redrawn
- Product images are referenced as `<img>` pointing at real files, never replaced by CSS silhouettes
- CSS variables are injected from the spec: `:root { --brand-primary: ...; }`, and HTML only uses `var(--brand-*)`
- This turns brand consistency from "relies on willpower" into "relies on structure" — adding an ad-hoc color requires changing the spec first

##### Fallbacks for total process failure

Handle separately by asset type:

| Missing | Handling |
|---|---|
| **Logo completely unfindable** | **Stop and ask the user**, don't force it (the logo is the foundation of brand recognition) |
| **Product image (physical product) unfindable** | Prefer nano-banana-pro AI generation (based on the official reference image) → next, ask the user → last, an honest placeholder (gray block + text label, clearly marked "product image pending") |
| **UI screenshot (digital product) unfindable** | Ask the user for screenshots from their own account → official demo video frames. Don't pad with a mockup generator |
| **Color values completely unfindable** | Follow the "design direction consultant mode": recommend 3 directions to the user and annotate the assumptions |

**Forbidden**: silently forcing it through with CSS silhouettes / generic gradients when assets can't be found — this is the protocol's biggest anti-pattern. **Rather stop and ask than pad.**

##### Anti-examples (real pits stepped in)

- **Kimi animation**: guessed "should be orange" from memory; Kimi is actually `#1783FF` blue — one full rework
- **Lovart design**: mistook the demo brand's Heytea red in the product screenshot for Lovart's own color — nearly ruined the whole design
- **DJI Pocket 4 launch animation (2026-04-20, the real case that triggered this protocol's upgrade)**: ran the old color-extraction-only protocol, didn't download the DJI logo, didn't find Pocket 4 product images, substituted CSS silhouettes for the product — the result was "a generic black-background + orange-accent tech animation" with zero DJI recognition. The original author's words: "Otherwise, what are we expressing?" → protocol upgraded.
- Extracted colors but never wrote them into brand-spec.md; by the third page the primary color value was forgotten and an ad-hoc "close but not exact" hex was added — brand consistency collapsed
- **Five Coding Agent comparison PPT (2026-06-06, the real case that triggered the trigger-condition expansion)**: the agent judged the task as "PPT + no style reference," went down the Fallback design-direction-consultant path, and after extracting only the five brands' colors spawned three design logics — **not one of the five product logos (Claude Code / Cursor / Codex / Copilot / Trae) was fetched**. Called out on the spot by the original author: "Why didn't we go fetch these products' logos." Root cause: misjudged a "comparison / leaderboard deck" as not triggering §1.a (thought §1.a only governs "producing materials for a single client"), and the Fallback path had no logo checkpoint at all. → Fixes: ①trigger condition expanded to two categories (including "design names/ranks real products side by side") ②Fallback doesn't exempt logo fetching ③Phase 3.5 adds a "named-product logo sub-gate" that must pass before spawn ④Step 3.1 adds the reliable svgl/simpleicons/Google-favicon image-fetch chain.

##### Cost of the protocol vs cost of not doing it

| Scenario | Time |
|---|---|
| Walking the protocol correctly | download logo 5 min + download 3-5 product images/UI 10 min + grep color values 5 min + write spec 10 min = **30 minutes** |
| Cost of not doing the protocol | producing a generic animation with no recognition → 1-2 hours of user rework, or even starting over |

**This is the cheapest investment in stability.** Especially for commercial orders / launches / key-client projects, the 30-minute asset protocol is money that saves your life.
