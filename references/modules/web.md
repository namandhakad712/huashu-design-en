# Module · Web Pages / Landing Pages / Official Sites / UI Prototypes

Clickable sites, landing pages, official sites, dashboards, and desktop UI prototypes go here (mobile apps go to `references/app-prototype.md`). Cross SKILL.md's narrow bridge first, then follow this manual.

## The Hero: Lead With the Most Distinctive Thing in the Subject's World

The hero is the first thing the audience sees. Open with the most distinctive thing this subject's world has to offer, in whichever form fits best: one headline, one image, one stretch of animation, one playable demo, one interactive moment.

"Big number + small label + a row of supporting data + gradient garnish" is the hero's default answer — use it only when it truly is the best fit. The same goes for the "big hero + three feature columns + testimonials + CTA" landing-page template.

## Build Order

1. Three directions: 1 full HTML per direction + hero screenshot + full-page long screenshot (`references/directions.md`)
2. After the user picks, first write assumptions + a placeholder structure for them to see, then fill in the components (the standard flow in `references/workflow.md`)
3. Add Tweaks only once structure and rhythm are settled (`references/tweaks-system.md`), letting the user tune colors, font sizes, and copy themselves

## Hard Rules

- Body text ≥14px (16px on mobile), tappable elements ≥44×44px, body-text contrast ≥4.5:1
- Responsive: verify at least the two widths 1440 and 375 (`python3 "$HD/scripts/verify.py" page.html --viewports 1440x900,375x812`)
- Interactions must genuinely work: build the navigation, tabs, expanders, and form states, with zero console errors
- No invented data, testimonials, or logo walls; when something is missing, leave an honest placeholder or ask the user for it
- Motion: one choreographed page load beats fade-up on every block; motion that answers user actions (expand, confirm) is the good kind

## Starter Components

| File | Purpose |
|---|---|
| `assets/browser_window.jsx` | Present the web page inside a browser window (URL bar + tab bar) |
| `assets/macos_window.jsx` | Desktop app window shell |
| `assets/design_canvas.jsx` | Several static variants side by side for comparison |

React + Babel conventions and the three technical red lines (style objects must be uniquely named, share across multiple babel scripts with `Object.assign(window, …)`, no `scrollIntoView`): `references/react-setup.md`.

## Related Files

| Want | Read |
|---|---|
| Style library and specimens (the seconds roulette's web section, plus the cross-medium Chinese & East Asian section) | `references/design-styles.md` |
| Font pairing and Chinese typography | `references/typography.md` |
| User has a codebase / design system | `references/design-context.md` |
| Pre-delivery verification | `references/verification.md` |
