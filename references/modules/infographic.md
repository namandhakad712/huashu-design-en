# Module · Infographics / Data Visualization / Long-Form Images

One image, or a set, with data or knowledge as the protagonist and still readable on its own once interaction is stripped away — that goes here: infographics, data-report illustrations, a single tall vertical image, poster-style explainers. The Xiaohongshu kind of image-text post — 3:4, several images, swiped through — goes to `xiaohongshu.md`. Cross SKILL.md's narrow bridge first, then follow this manual.

## Set the Viewer Distance and Container First

- Scrolled past in a mobile feed (Xiaohongshu, WeChat Moments): 1080 wide, and the first screen (about 1080×1350) must stand on its own — title, hero visual, and the single strongest number
- Print or a large screen: fix the physical size and viewing distance first, then the type sizes
- Embedded in an article: follow the body text's width; text inside the image no smaller than the body

## Data Is the Protagonist, Not the Decoration

- **Use only numbers the user gave you or that you can verify**, and label illustrative figures as such on the image. Inventing a number that looks like data is ten times worse than leaving the space empty
- Ask what relationship the numbers are telling first, then pick the form: proportion → real objects or areas scaled to the ratio; change → one curve or a timeline; routes and space → a map; composition → a whole taken apart; scale → one oversized object plus a familiar reference object
- One color carries one meaning only, and the legend is written on the image
- For lead material, prefer real images, public-domain scientific illustrations, and maps (`references/materials.md`), not a platter of icons

## Build Order

1. Three directions: 1 complete HTML per direction, full-page long screenshot at the target width (`references/directions.md`). The three skeletons must differ (a map, a timeline, a field guide, a single giant object, a narrative sequence are all eligible structures), but don't force-fit a metaphor just to be different.
2. After the pick, fill in the full content and proofread every number and unit
3. Export: `npx playwright screenshot --full-page --viewport-size=1080,1350 file:///… out.png`; when it's headed to a platform, slice again to the platform's specs

## Design Check

```bash
# $HD = this skill's root directory (the one containing SKILL.md), not the user's project directory
python3 "$HD/scripts/design_lint.py" check info.html --viewport 1080x1350 --min-body 36 --min-label 28
```

The minimum type size inside the image is computed against the final display size: a 1080-wide long image shrinks to about 390pt wide on a phone (about 2.8×), so body text ≥36px and labels ≥28px on the canvas is what it takes to land at 13–14pt on the phone screen. Print or large screens are computed separately from the actual viewing distance.

## Related Files

| Want | Read |
|---|---|
| Style library and specimens (the seconds roulette's infographic section, plus the cross-medium Chinese & East Asian section) | `references/design-styles.md` |
| Specs quick reference for covers, in-article illustrations, and long-form images | `references/scene-templates.md` |
| Fonts and Chinese typography | `references/typography.md` |
