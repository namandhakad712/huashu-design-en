# React + Babel Project Standards

Technical standards that must be followed when building prototypes with HTML + React + Babel. Not following them will blow things up.

## Pinned Script Tags (Must Use These Versions)

Put these three script tags in the HTML `<head>`, using **pinned versions + integrity hashes**:

```html
<script src="https://unpkg.com/react@18.3.1/umd/react.development.js" integrity="sha384-hD6/rw4ppMLGNu3tX5cjIb+uRZ7UkRJ6BPkLpg4hAu/6onKUg4lLsHAs9EBPT82L" crossorigin="anonymous"></script>
<script src="https://unpkg.com/react-dom@18.3.1/umd/react-dom.development.js" integrity="sha384-u6aeetuaXnQ38mYT8rp6sbXaQe3NL9t+IBXmnYxwkUI2Hw4bsp2Wvmx4yRQF1uAm" crossorigin="anonymous"></script>
<script src="https://unpkg.com/@babel/standalone@7.29.0/babel.min.js" integrity="sha384-m08KidiNqLdpJqLq95G/LEi8Qvjl/xUYll3QILypMoQ65QorJ9Lvtp2RXYGBFj1y" crossorigin="anonymous"></script>
```

**Don't** use unpinned versions like `react@18` or `react@latest` — you'll get version drift/caching issues.

**Don't** omit `integrity` — if the CDN is hijacked or tampered with, this is your defense line.

## File Structure

```
Project Name/
├── index.html               # main HTML
├── components.jsx           # component files (loaded via type="text/babel")
├── data.js                  # data file
└── styles.css               # extra CSS (optional)
```

How it's loaded in the HTML:

```html
<!-- React+Babel first -->
<script src="https://unpkg.com/react@18.3.1/..."></script>
<script src="https://unpkg.com/react-dom@18.3.1/..."></script>
<script src="https://unpkg.com/@babel/standalone@7.29.0/..."></script>

<!-- Then your component files -->
<script type="text/babel" src="components.jsx"></script>
<script type="text/babel" src="pages.jsx"></script>

<!-- Finally, the main entry -->
<script type="text/babel">
  const root = ReactDOM.createRoot(document.getElementById('root'));
  root.render(<App />);
</script>
```

**Don't** use `type="module"` — it conflicts with Babel.

## Three Unbreakable Rules

### Rule 1: The `styles` Object Must Use Unique Naming

**Wrong** (guaranteed to break with multiple components):
```jsx
// components.jsx
const styles = { button: {...}, card: {...} };

// pages.jsx  ← same name overwrites!
const styles = { container: {...}, header: {...} };
```

**Correct**: give each component file's styles a unique prefix.

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

This is **non-negotiable**. Every `const styles = {...}` must be renamed to a specific name, otherwise you'll get a full-stack error when multiple components load.

### Rule 2: Scopes Aren't Shared — Export Manually

**Key insight**: each `<script type="text/babel">` is compiled independently by Babel, so their scopes **don't communicate**. The `Terminal` component defined in `components.jsx` is **undefined by default** in `pages.jsx`.

**Solution**: at the end of each component file, export the components/utilities you want to share onto `window`:

```jsx
// end of components.jsx
function Terminal(props) { ... }
function Line(props) { ... }
const colors = { green: '#...', red: '#...' };

Object.assign(window, {
  Terminal, Line, colors,
  // list everything you need elsewhere here
});
```

Then `pages.jsx` can use `<Terminal />` directly, because JSX will look up `window.Terminal`.

### Rule 3: Don't Use scrollIntoView

`scrollIntoView` pushes the entire HTML container up, breaking the web harness layout. **Never use it**.

Alternatives:
```js
// scroll to a position within the container
container.scrollTop = targetElement.offsetTop;

// or use element.scrollTo
container.scrollTo({
  top: targetElement.offsetTop - 100,
  behavior: 'smooth'
});
```

## Calling the Claude API (Inside HTML)

Some native design-agent environments (such as Claude.ai Artifacts) have a no-config `window.claude.complete`, but most agent environments (Claude Code / Codex / Cursor / Trae / etc.) **don't have it** locally.

If your HTML prototype needs to call an LLM for a demo (e.g., building a chat interface), there are two options:

### Option A: Don't Really Call — Use a Mock

Recommended for demo scenarios. Write a fake helper that returns a preset response:
```jsx
window.claude = {
  async complete(prompt) {
    await new Promise(r => setTimeout(r, 800)); // simulate delay
    return "This is a mock response. Replace it with the real API in actual deployment.";
  }
};
```

### Option B: Actually Call the Anthropic API (Not Recommended, Local Demos Only)

It requires an API key; the user must paste their own key into the HTML to run it. **Never hardcode a key in the HTML**.

⚠️ Security boundary: this approach is only suitable for local `file://` demos that you close as soon as you're done. The key will remain in the DOM/memory —
**don't deploy this page, and don't distribute screenshots/recordings of the page with a filled-in key**. For production scenarios, always forward through a local proxy backend,
so the browser never touches the key. By default, prefer Option A/C (no key needed at all).

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

**Note**: calling the Anthropic API directly from the browser will run into CORS issues. If the preview environment the user gives you doesn't support CORS bypass, this path won't work. In that case use Option A's mock, or tell the user a proxy backend is needed.

### Option C: Use the Agent-Side LLM Capability to Generate Mock Data

If it's only for local demo use, you can temporarily call the current agent's LLM capability within this agent session (or a user-installed multi-model skill) to generate mock response data first, then hardcode it into the HTML. This way the HTML doesn't depend on any API at runtime.

## Typical HTML Starter Template

Copy this template as the skeleton for your React prototype:

```html
<!DOCTYPE html>
<html lang="zh-CN">
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

  <!-- your component files -->
  <script type="text/babel" src="components.jsx"></script>

  <!-- main entry -->
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

## Common Errors and How to Fix Them

**`styles is not defined` or `Cannot read property 'button' of undefined`**
→ You defined `const styles` in one file, and another file overwrote it. Give each one a specific name.

**`Terminal is not defined`**
→ Scopes don't communicate across files. At the end of the file where `Terminal` is defined, add `Object.assign(window, {Terminal})`.

**The entire page is a white screen, no console errors**
→ Most likely a JSX syntax error that Babel didn't report in the console. Temporarily swap `babel.min.js` for the non-minified `babel.js`; the error messages will be clearer.

**ReactDOM.createRoot is not a function**
→ Wrong version. Make sure you're using react-dom@18.3.1 (not 17 or another version).

**`Objects are not valid as a React child`**
→ You rendered an object instead of JSX/a string. Usually `{someObj}` was written where it should be `{someObj.name}`.

## How to Split Files in Large Projects

**A single file of >1000 lines** is hard to maintain. How to split it up:

```
Project/
├── index.html
├── src/
│   ├── primitives.jsx      # basic elements: Button, Card, Badge...
│   ├── components.jsx      # business components: UserCard, PostList...
│   ├── pages/
│   │   ├── home.jsx        # home page
│   │   ├── detail.jsx      # detail page
│   │   └── settings.jsx    # settings page
│   ├── router.jsx          # simple routing (React state switching)
│   └── app.jsx             # entry component
└── data.js                 # mock data
```

Load them in the HTML in order:
```html
<script type="text/babel" src="src/primitives.jsx"></script>
<script type="text/babel" src="src/components.jsx"></script>
<script type="text/babel" src="src/pages/home.jsx"></script>
<script type="text/babel" src="src/pages/detail.jsx"></script>
<script type="text/babel" src="src/pages/settings.jsx"></script>
<script type="text/babel" src="src/router.jsx"></script>
<script type="text/babel" src="src/app.jsx"></script>
```

**Every file must end** with `Object.assign(window, {...})` exporting whatever needs to be shared.
