# React + Babel Project Standards

Technical standards that must be followed when making prototypes with HTML+React+Babel. Not following will break things.

## Pinned Script Tags (Must Use These Versions)

In HTML `<head>`, put these three script tags, with **fixed versions + integrity hashes**:

```html
<script src="https://unpkg.com/react@18.3.1/umd/react.development.js" integrity="sha384-hD6/rw4ppMLGNu3tX5cjIb+uRZ7UkRJ6BPkLpg4hAu/6onKUg4lLsHAs9EBPT82L" crossorigin="anonymous"></script>
<script src="https://unpkg.com/react-dom@18.3.1/umd/react-dom.development.js" integrity="sha384-u6aeetuaXnQ38mYT8rp6sbXaQe3NL9t+IBXmnYxwkUI2Hw4bsp2Wvmx4yRQF1uAm" crossorigin="anonymous"></script>
<script src="https://unpkg.com/@babel/standalone@7.29.0/babel.min.js" integrity="sha384-m08KidiNqLdpJqLq95G/LEi8Qvjl/xUYll3QILypMoQ65QorJ9Lvtp2RXYGBFj1y" crossorigin="anonymous"></script>
```

**Don't** use unpinned versions like `react@18` or `react@latest` — version drift/cache problems will occur.

**Don't** omit `integrity` — this is the defense line if CDN is hijacked or tampered.

## File Structure

```
Project Name/
├── index.html               # Main HTML
├── components.jsx           # Component files (loaded with type="text/babel")
├── data.js                  # Data file
└── styles.css               # Extra CSS (optional)
```

Loading in HTML:

```html
<!-- React+Babel first -->
<script src="https://unpkg.com/react@18.3.1/..."></script>
<script src="https://unpkg.com/react-dom@18.3.1/..."></script>
<script src="https://unpkg.com/@babel/standalone@7.29.0/..."></script>

<!-- Then your component files -->
<script type="text/babel" src="components.jsx"></script>
<script type="text/babel" src="pages.jsx"></script>

<!-- Finally main entry -->
<script type="text/babel">
  const root = ReactDOM.createRoot(document.getElementById('root'));
  root.render(<App />);
</script>
```

**Don't** use `type="module"` — conflicts with Babel.

## Three Unbreakable Rules

### Rule 1: Styles objects must use unique naming

**Wrong** (guaranteed to break with multiple components):
```jsx
// components.jsx
const styles = { button: {...}, card: {...} };

// pages.jsx ← same name overwrites!
const styles = { container: {...}, header: {...} };
```

**Correct**: Each component file's styles use unique prefix.

```jsx
// terminal.jsx
const terminalStyles = { 
  screen: {...}, 
  line: {...} 
};

// sidebar.jsx
const sidebarStyles = { 
  container: {...}, 
  item: {...} 
};
```

**Or use inline styles** (recommended for small components):
```jsx
<div style={{ padding: 16, background: '#111' }}>...</div>
```

This is **non-negotiable**. Every time you write `const styles = {...}` must replace with specific naming, otherwise when multiple components load, entire stack errors.

### Rule 2: Scope not shared, need manual export

**Key understanding**: Each `<script type="text/babel">` is compiled independently by Babel, their scopes **don't communicate**. The `Terminal` component defined in `components.jsx` is **undefined by default** in `pages.jsx`.

**Solution**: At end of each component file, export components/tools to share to `window`:

```jsx
// end of components.jsx
function Terminal(props) { ... }
function Line(props) { ... }
const colors = { green: '#...', red: '#...' };

Object.assign(window, {
  Terminal, Line, colors,
  // list everything you want to use elsewhere
});
```

Then `pages.jsx` can directly use `<Terminal />`, because JSX will look for `window.Terminal`.

### Rule 3: Don't use scrollIntoView

`scrollIntoView` pushes the entire HTML container up, breaking web harness layout. **Never use**.

Alternative solutions:
```js
// Scroll to position within container
container.scrollTop = targetElement.offsetTop;

// Or use element.scrollTo
container.scrollTo({
  top: targetElement.offsetTop - 100,
  behavior: 'smooth'
});
```

## Calling Claude API (Within HTML)

Some native design-agent environments (like Claude.ai Artifacts) have no-config `window.claude.complete`, but most agent environments (Claude Code / Codex / Cursor / Trae / etc.) locally **don't have it**.

If your HTML prototype needs to call LLM for demo (e.g., making a chat interface), two options:

### Option A: Don't really call, use mock

Recommended for demo scenarios. Write a fake helper, returns preset response:
```jsx
window.claude = {
  async complete(prompt) {
    await new Promise(r => setTimeout(r, 800)); // simulate delay
    return "This is a mock response. Replace with real API in actual deployment.";
  }
};
```

### Option B: Really call Anthropic API

Needs API key, user must paste their own key in HTML to run. **Never hardcode key in HTML**.

```html
<input id="api-key" placeholder="Paste your Anthropic API key" />
<script>
window.claude = {
  async complete(prompt) {
    const key = document.getElementById('api-key').value;
    const res = await fetch('https://api.anthropic.com/v1/messages', {
      method: 'POST',
      headers: {
        'x-api-key': key,
        'anthropic-version': '2023-06-01',
        'content-type': 'application/json',
      },
      body: JSON.stringify({
        model: 'claude-haiku-4-5',
        max_tokens: 1024,
        messages: [{ role: 'user', content: prompt }]
      })
    });
    const data = await res.json();
    return data.content[0].text;
  }
};
</script>
```

**Note**: Browser directly calling Anthropic API will encounter CORS issues. If user's preview environment doesn't support CORS bypass, this path won't work. Use Option A mock, or tell user a proxy backend is needed.

### Option C: Use agent's LLM capability to generate mock data

If just for local demo, you can within current agent session temporarily call that agent's LLM capability (or user's installed multi-model skill) to first generate mock response data, then hardcode into HTML. This way HTML at runtime doesn't depend on any API.

## Typical HTML Starting Template

Copy this template as React prototype skeleton:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Your Prototype Name</title>

  <!-- React + Babel pinned -->
  <script src="https://unpkg.com/react@18.3.1/umd/react.development.js" integrity="sha384-hD6/rw4ppMLGNu3tX5cjIb+uRZ7UkRJ6BPkLpg4hAu/6onKUg4lLsHAs9EBPT82L" crossorigin="anonymous"></script>
  <script src="https://unpkg.com/react-dom@18.3.1/umd/react-dom.development.js" integrity="sha384-u6aeetuaXnQ38mYT8rp6sbXaQe3NL9t+IBXmnYxwkUI2Hw4bsp2Wvmx4yRQF1uAm" crossorigin="anonymous"></script>
  <script src="https://unpkg.com/@babel/standalone@7.29.0/babel.min.js" integrity="sha384-m08KidiNqLdpJqLq95G/LEi8Qvjl/xUYll3QILypMoQ65QorJ9Lvtp2RXYGBFj1y" crossorigin="anonymous"></script>

  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    html, body { height: 100%; width: 100%; }
    body { 
      font-family: -apple-system, 'SF Pro Text', sans-serif;
      background: #FAFAFA;
      color: #1A1A1A;
    }
    #root { min-height: 100vh; }
  </style>
</head>
<body>
  <div id="root"></div>

  <!-- Your component files -->
  <script type="text/babel" src="components.jsx"></script>

  <!-- Main entry -->
  <script type="text/babel">
    const { useState, useEffect } = React;

    function App() {
      return (
        <div style={{padding: 40}}>
          <h1>Hello</h1>
        </div>
      );
    }

    const root = ReactDOM.createRoot(document.getElementById('root'));
    root.render(<App />);
  </script>
</body>
</html>
```

## Common Errors and Solutions

**`styles is not defined` or `Cannot read property 'button' of undefined`**
→ You defined `const styles` in one file, another file overwrote it. Change each to specific naming.

**`Terminal is not defined`**
→ Cross-file reference scope doesn't communicate. At end of file defining Terminal, add `Object.assign(window, {Terminal})`.

**Entire page white screen, no console errors**
→ Most likely JSX syntax error but Babel didn't report in console. Temporarily swap `babel.min.js` for non-minified `babel.js`, error messages clearer.

**ReactDOM.createRoot is not a function**
→ Wrong version. Confirm using react-dom@18.3.1 (not 17 or other).

**`Objects are not valid as a React child`**
→ You rendered an object instead of JSX/string. Usually wrote `{someObj}` should be `{someObj.name}`.

## How to Split Files for Large Projects

**>1000 lines single file** hard to maintain. Splitting approach:

```
Project/
├── index.html
├── src/
│   ├── primitives.jsx      # Basic elements: Button, Card, Badge...
│   ├── components.jsx      # Business components: UserCard, PostList...
│   ├── pages/
│   │   ├── home.jsx        # Home page
│   │   ├── detail.jsx      # Detail page
│   │   └── settings.jsx    # Settings page
│   ├── router.jsx          # Simple routing (React state switching)
│   └── app.jsx             # Entry component
└── data.js                 # Mock data
```

Load in HTML in order:
```html
<script type="text/babel" src="src/primitives.jsx"></script>
<script type="text/babel" src="src/components.jsx"></script>
<script type="text/babel" src="src/pages/home.jsx"></script>
<script type="text/babel" src="src/pages/detail.jsx"></script>
<script type="text/babel" src="src/pages/settings.jsx"></script>
<script type="text/babel" src="src/router.jsx"></script>
<script type="text/babel" src="src/app.jsx"></script>
```

**At end of each file** must `Object.assign(window, {...})` export what to share.