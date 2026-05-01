# Verification: Output Verification Process

Some design-agent native environments (like Claude.ai Artifacts) have built-in `fork_verifier_agent` to start subagent using iframe screenshot checking. Most agent environments (Claude Code / Codex / Cursor / Trae / etc.) don't have this built-in capability — using Playwright manually covers the same verification scenarios.

## Verification Checklist

After each HTML output, run through this checklist:

### 1. Browser Rendering Check (Mandatory)

Most basic: **Can HTML open?** On macOS:

```bash
open -a "Google Chrome" "/path/to/your/design.html"
```

Or use Playwright to screenshot (next section).

### 2. Console Error Check

Most common issue in HTML files is JS errors causing white screen. Run with Playwright:

```bash
python ~/.claude/skills/claude-design/scripts/verify.py path/to/design.html
```

This script will:
1. Open HTML with headless chromium
2. Screenshot to project directory
3. Capture console errors
4. Report status

See `scripts/verify.py` for details.

### 3. Multi-Viewport Check

If responsive design, capture multiple viewports:

```bash
python verify.py design.html --viewports 1920x1080,1440x900,768x1024,375x667
```

### 4. Interaction Check

Tweaks, animation, button toggles — static screenshots by default don't show. **Recommend letting user open browser and click through themselves**, or use Playwright to record video:

```python
page.video.record('interaction.mp4')
```

### 5. Slide-by-Slide Check

For deck-style HTML, screenshot page by page:

```bash
python verify.py deck.html --slides 10  # Screenshot first 10
```

Generates `deck-slide-01.png`, `deck-slide-02.png`... for quick browsing.

## Playwright Setup

First-time use needs:

```bash
# If not installed yet
npm install -g playwright
npx playwright install chromium

# Or Python version
pip install playwright
playwright install chromium
```

If user already has Playwright installed globally, use directly.

## Screenshot Best Practices

### Screenshot full page

```python
page.screenshot(path='full.png', full_page=True)
```

### Screenshot viewport

```python
page.screenshot(path='viewport.png')  # Only captures visible area by default
```

### Screenshot specific element

```python
element = page.query_selector('.hero-section')
element.screenshot(path='hero.png')
```

### High-DPI screenshot

```python
page = browser.new_page(device_scale_factor=2)  # retina
```

### Wait for animation before screenshot

```python
page.wait_for_timeout(2000)  # Wait 2 seconds for animation to settle
page.screenshot(...)
```

## Sending Screenshots to User

### Open local screenshot directly

```bash
open screenshot.png
```

User will view in their Preview/Figma/VSCode/browser.

### Upload to image hosting to share link

If need to share with remote collaborators (e.g., Slack/Feishu/WeChat), let user use their image hosting tool or MCP to upload:

```bash
python ~/Documents/写作/tools/upload_image.py screenshot.png
```

Returns ImgBB permanent link, can paste anywhere.

## When Verification Errors

### White screen

Console definitely has errors. Check first:

1. React+Babel script tag integrity hash correct? (see `react-setup.md`)
2. Is `const styles = {...}` naming conflict?
3. Cross-file components exported to `window`?
4. JSX syntax error (babel.min.js doesn't report, use non-minified babel.js)

### Animation lag

- Use Chrome DevTools Performance tab to record一段
- Find layout thrashing (frequent reflow)
- Animation prefer `transform` and `opacity` (GPU accelerated)

### Wrong fonts

- Check if `@font-face` URL accessible
- Check fallback fonts
- Chinese fonts load slow: show fallback first, switch after loaded

### Layout misalignment

- Check if `box-sizing: border-box` applied globally
- Check `* { margin: 0; padding: 0 }` reset
- In Chrome DevTools, turn on gridlines to see actual layout

## Verification = Designer's Second Pair of Eyes

**Always run through yourself**. When AI writes code, often:

- Looks right but interaction has bugs
- Static screenshot good but scrolls misaligned
- Wide screen looks good but narrow screen breaks
- Dark mode forgot to test
- Some components don't respond after Tweaks switch

**Last minute of verification saves 1 hour of rework**.

## Common Verification Script Commands

```bash
# Basic: open + screenshot + capture errors
python verify.py design.html

# Multiple viewports
python verify.py design.html --viewports 1920x1080,375x667

# Multiple slides
python verify.py deck.html --slides 10

# Output to specified directory
python verify.py design.html --output ./screenshots/

# headless=false, open real browser for you to see
python verify.py design.html --show
```