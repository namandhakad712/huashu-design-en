# Materials First: The Frame's Protagonist Shouldn't Be Just Type and Cards

If what pure HTML/CSS can put on the page shrinks to "type + cards + tables + hairlines", no style will keep the result from looking monotonous — the second root cause of the old version's monotonous output. This file settles two things: every direction picks its lead material first; and materials are tiered by the capabilities the user actually has in hand — recommend installing what's missing, but never block on it.

## Principles

1. **Every direction picks its lead material first**, written into the direction card (`references/directions.md`). Don't let all three directions be "pure typography"; when typography is the material, it has to be deliberate typography — the type itself becoming the image (giant type, vertical setting, cropping), not the default headline-plus-body arrangement.
2. **Fetch every image the content requires before designing.** In designs that introduce animals, places, people, products, or history, images are content, not decoration; a parrot site with no parrot = failure. When in doubt, treat it as content-required.
3. **The real-image honesty test**: remove the image — does the information lose anything? No loss = decoration, don't add it. No stock "inspiration images".
4. **People, animals, physical objects, and scenes are never hand-drawn in SVG** — the faces come out misaligned and the proportions eerie. Use real photos, generated images, or an honest placeholder. Geometry, icons, data graphics, and map linework are exempt; silhouette masks are for composition only (cropping photos, building shapes), never a stand-in for a product shot.

**When it involves the user themselves or their own product, real assets come first**: check `personal-asset-index.json` under the user's private memory / config directory first (on first use, copy `assets/personal-asset-index.example.json` over there and fill in the real data; real data never lives in the skill directory, so it can't leak out with distribution). If it isn't there, ask the user for it — never fabricate.

## Probe capabilities first

```bash
# $HD = this skill's root directory (the directory containing SKILL.md), not the user's project directory
python3 "$HD/scripts/capabilities.py"
```

It checks which related skills are installed on this machine, whether there's an image-generation key, and whether ffmpeg / playwright are present, then reports the tier plus an install suggestion for whatever's missing. A capability it fails to detect isn't necessarily absent (Codex, for one, bundles image_gen); if the user says they have it, the user's word wins.

## The three tiers

### T0 · Every user has these (the default; no extra capability required)

- **Real photos**: `python3 "$HD/scripts/fetch_images.py" --query "English keywords" --out <project>/assets/img --count 2 --width 1600` (Wikimedia Commons, Met / Art Institute open collections, Biodiversity Heritage Library, Unsplash, Pexels — with license info in the output and failure fallbacks). The user's own products go through the Core Asset Protocol for official shots.
- **Named products' logos**: however many recognizable products appear in the design, that many logos get fetched (svgl → simpleicons → favicon, see `references/brand-asset-protocol.md`). If a single one on the list doesn't land, keep filling the gap; only when it truly can't be fetched do you fall back to an honest placeholder and say so plainly.
- **Procedural materials** (work in a single file, no fetch needed):
  - SVG filters: `feTurbulence` + `feDisplacementMap` for paper grain, noise, ink bleed, misregistered print
  - CSS: layered `radial-gradient` for light and volume, `mask-image` / `clip-path` for silhouettes and crops, `mix-blend-mode` for overprint
  - Canvas-generated images: contour lines, dot grids, flow fields, star charts, fabric textures (fixed random seed, reproducible in screenshots)
  - Three.js (loaded from cdnjs via `<script src>`, works under `file://`) for procedural geometry, materials, and lighting
- **Data as image**: turn the numbers in the content into the main visual — a scale spanning the whole page, a physical object scaled to proportion, a route drawn on a map — not three big number cards
- **Physical replicas**: tickets, labels, ID cards, instruction sheets, postcards, newspaper spreads built in HTML, with paper stock, punch holes, stamps, and creases
- **Type as image**: oversized glyphs sliced out of the frame, vertical setting, glyphs interlocking with images

### T1 · AI image generation available

How to tell: an image-gen skill such as `huashu-gpt-image` or `nano-banana-pro` is installed on this machine, or the runtime you're in ships an image-generation tool (Codex's image_gen, say — you know whether you have one), or the user says so outright. An API key alone doesn't count: this skill has no script that calls an image-gen API directly.

- **Probe images at the direction-board stage**: generate one atmosphere or hero image per direction (material, light, subject) and lay it in front of the user alongside the HTML draft. The visual layer exists before any code is written — what the user picks is "something they can see".
- **After the pick, generate hero images, illustration, textures, people, and scenes**. Prompts spell out concrete visual features and real reference names, not adjectives like "premium feel" or "minimalist" — method in `huashu-gpt-image`.
- Generated images must pass the real-image honesty test, and brand product images are generated with official reference images as the base — never draw a product out of thin air.

### T2 · Sibling skills installed

| skill | What it adds | Public address |
|---|---|---|
| huashu-gpt-image | Image-gen prompt methodology — illustrations, posters, infographics, UI mockups | `npx skills add alchaincyf/huashu-gpt-image` |
| huashu-art-motion | 36 art and narration-animation styles, voiceover-driven full films | `npx skills add alchaincyf/huashu-art-motion` |
| huashu-md-html | md into publication-grade html / PDF / EPUB | `npx skills add alchaincyf/huashu-md-html` |
| huashu-3djs, huashu-flow-diagram | Procedural 3D scenes, architecture diagrams that flow | Not public yet — if installed locally, use them |

## What to say when a capability is missing

No blocking: drop down to T0 and keep going, then tell the user in one line at delivery what more they could get:

> This version's hero visual uses a procedural paper texture + public-domain illustration. With huashu-gpt-image installed (`npx skills add alchaincyf/huashu-gpt-image`), the next run can generate hero visuals and probe images directly.

Recommend the one that's relevant to this task — no catalog pitching.

## The three-level fallback for failed fetches

1. Nothing in the public-domain libraries → switch to Unsplash / Pexels
2. Nothing suitable anywhere on the web → if T1 is available, generate from a reference image as the base
3. Still nothing → continue with an honest "image to be added" placeholder and say so at delivery. A failed fetch means degrade and continue, not stop
