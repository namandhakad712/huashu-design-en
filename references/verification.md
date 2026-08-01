# Verification: Output verification process

Some design-agent native environments (like Claude.ai Artifacts) have a built-in `fork_verifier_agent` that spawns a subagent to screenshot-check with iframes. Most agent environments (Claude Code / Codex / Cursor / Trae / etc.) don't have this built-in capability — doing it manually with Playwright covers the same verification scenarios.

## Verification checklist

After every HTML output, run through this checklist:

### 1. Browser rendering check (required)

The most basic: **can the HTML open?** On macOS:

```bash
open -a "Google Chrome" "/path/to/your/design.html"
```

Or screenshot with Playwright (next section).

### 2. Console error check

The most common problem in HTML files is a JS error causing a white screen. Run it through Playwright:

```bash
python ~/.claude/skills/huashu-design/scripts/verify.py path/to/design.html
```

This script will:
1. Open the HTML with headless chromium
2. Save a screenshot to the project directory
3. Capture console errors
4. Report the status

See `scripts/verify.py` for details.

### 3. Multi-viewport check

If it's a responsive design, capture multiple viewports:

```bash
python verify.py design.html --viewports 1920x1080,1440x900,768x1024,375x667
```

### 4. Interaction check

Tweaks, animations, button toggles — the default static screenshots can't show them. **Recommend letting the user open the browser and click through it themselves**, or record with Playwright:

```python
page.video.record('interaction.mp4')
```

### 5. Slide-by-slide check

For deck-type HTML, screenshot page by page:

```bash
python verify.py deck.html --slides 10  # screenshot the first 10 slides
```

Generates `deck-slide-01.png`, `deck-slide-02.png`... for quick browsing.

## Playwright setup

First-time use requires:

```bash
# If not installed yet
npm install -g playwright
npx playwright install chromium

# Or the Python version
pip install playwright
playwright install chromium
```

If the user already has Playwright installed globally, use it directly.

## Screenshot best practices

### Capture the full page

```python
page.screenshot(path='full.png', full_page=True)
```

### Capture the viewport

```python
page.screenshot(path='viewport.png')  # default only captures the visible area
```

### Capture a specific element

```python
element = page.query_selector('.hero-section')
element.screenshot(path='hero.png')
```

### High-DPI screenshots

```python
page = browser.new_page(device_scale_factor=2)  # retina
```

### Wait for animations to finish before capturing

```python
page.wait_for_timeout(2000)  # wait 2 seconds for the animation to settle
page.screenshot(...)
```

## Sending screenshots to the user

### Open a local screenshot directly

```bash
open screenshot.png
```

The user will view it in their Preview/Figma/VSCode/browser.

### Upload to an image host to share a link

If you need to show remote collaborators (e.g., Slack/Feishu/WeChat), have the user upload the screenshot with their own image-hosting tool or MCP to get a permanent link that can be pasted anywhere.

## When verification fails

### White screen

The console definitely has errors. Check first:

1. Whether the integrity hash on the React+Babel script tag is correct (see `react-setup.md`)
2. Whether there's a `const styles = {...}` naming conflict
3. Whether cross-file components are exported to `window`
4. JSX syntax errors (babel.min.js doesn't report them; switch to the non-minified babel.js)

### Animation lag

- Record a section with the Chrome DevTools Performance tab
- Look for layout thrashing (frequent reflow)
- Prefer `transform` and `opacity` for animations (GPU accelerated)

### Wrong fonts

- Check whether the `@font-face` URL is accessible
- Check the fallback fonts
- Chinese fonts load slowly: show the fallback first, switch after it finishes loading

### Layout misalignment

- Check whether `box-sizing: border-box` is applied globally
- Check the `* { margin: 0; padding: 0 }` reset
- Turn on gridlines in Chrome DevTools to see the actual layout

## Verification = the designer's second pair of eyes

**Always review it yourself.** When AI writes code, it often:

- Looks right but has interaction bugs
- Screenshots fine statically but misaligns on scroll
- Looks good wide but breaks narrow
- Forgets to test dark mode
- Has some components that don't respond after a Tweaks toggle

**1 minute of verification at the end saves 1 hour of rework.**

## Common verification script commands

```bash
# Basic: open + screenshot + capture errors
python verify.py design.html

# Multiple viewports
python verify.py design.html --viewports 1920x1080,375x667

# Multiple slides
python verify.py deck.html --slides 10

# Output to a specified directory
python verify.py design.html --output ./screenshots/

# headless=false, opens a real browser for you to see
python verify.py design.html --show
```

## Hard validation of video artifacts (verify-video.sh)

Don't rely on eyeballing the rendered MP4/final film — hard-validate it with a script (the HTML composition side is audited by the `hyperframes check` five-gate audit; this script only handles the artifact side):

```bash
# Final film (an audio track is required by default)
bash scripts/verify-video.sh final.mp4 --duration=22 --fps=60 --width=1920 --height=1080

# Silent intermediate artifact
bash scripts/verify-video.sh raw.mp4 --duration=10 --fps=60 --no-audio

# Deliberately cinematic black-open
bash scripts/verify-video.sh film.mp4 --duration=30 --fps=60 --allow-black-open
```

Checks: resolution/frame rate, duration tolerance (±2%), audio stream existence (the machine-executed rule that no audio track = unfinished film), black frames at head/tail (blackdetect, a typical symptom of recording offset/loop bounce-back), LUFS loudness (final film target −14±4). A non-zero exit code means it must not be delivered.
