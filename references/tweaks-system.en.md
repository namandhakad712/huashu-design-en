# Tweaks: Real-Time Design Variation Parameter Tuning

Tweaks is a core capability in this skill — letting users switch variations/adjust parameters in real-time without changing code.

**Cross-agent environment adaptation**: Some design-agent native environments (like Claude.ai Artifacts) rely on host's postMessage to persist tweak values back to source code. This skill uses **pure frontend localStorage solution** — same effect (state persists on refresh), but persistence happens in browser localStorage not source file. This solution works in any agent environment (Claude Code / Codex / Cursor / Trae / etc.).

## When to Add Tweaks

- User explicitly asks "can adjust parameters"/"switch between multiple versions"
- Design has multiple variations to compare
- User didn't say it, but you subjectively judge **adding a few insightful tweaks helps user see possibilities**

Default recommendation: **Add 2-3 tweaks per design** (color theme/font size/layout variant) even if user didn't ask — showing user possibility space is part of design service.

## Implementation (Pure Frontend Version)

### Basic Structure

```jsx
const TWEAK_DEFAULTS = {
  "primaryColor": "#D97757",
  "fontSize": 16,
  "density": "comfortable",
  "dark": false
};

function useTweaks() {
  const [tweaks, setTweaks] = React.useState(() => {
    try {
      const stored = localStorage.getItem('design-tweaks');
      return stored ? { ...TWEAK_DEFAULTS, ...JSON.parse(stored) } : TWEAK_DEFAULTS;
    } catch {
      return TWEAK_DEFAULTS;
    }
  });

  const update = (patch) => {
    const next = { ...tweaks, ...patch };
    setTweaks(next);
    try {
      localStorage.setItem('design-tweaks', JSON.stringify(next));
    } catch {}
  };

  const reset = () => {
    setTweaks(TWEAK_DEFAULTS);
    try {
      localStorage.removeItem('design-tweaks');
    } catch {}
  };

  return { tweaks, update, reset };
}
```

### Tweaks Panel UI

Floating panel in bottom right. Collapsible:

```jsx
function TweaksPanel() {
  const { tweaks, update, reset } = useTweaks();
  const [open, setOpen] = React.useState(false);

  return (
    <div style={{
      position: 'fixed',
      bottom: 20,
      right: 20,
      zIndex: 9999,
    }}>
      {open ? (
        <div style={{
          background: 'white',
          border: '1px solid #e5e5e5',
          borderRadius: 12,
          padding: 20,
          boxShadow: '0 10px 40px rgba(0,0,0,0.12)',
          width: 280,
          fontFamily: 'system-ui',
          fontSize: 13,
        }}>
          <div style={{ 
            display: 'flex', 
            justifyContent: 'space-between', 
            alignItems: 'center',
            marginBottom: 16,
          }}>
            <strong>Tweaks</strong>
            <button onClick={() => setOpen(false)} style={{
              border: 'none', background: 'none', cursor: 'pointer', fontSize: 16,
            }}>×</button>
          </div>

          {/* Color */}
          <label style={{ display: 'block', marginBottom: 12 }}>
            <div style={{ marginBottom: 4, color: '#666' }}>Primary Color</div>
            <input 
              type="color" 
              value={tweaks.primaryColor} 
              onChange={e => update({ primaryColor: e.target.value })}
              style={{ width: '100%', height: 32 }}
            />
          </label>

          {/* Font size slider */}
          <label style={{ display: 'block', marginBottom: 12 }}>
            <div style={{ marginBottom: 4, color: '#666' }}>Font Size ({tweaks.fontSize}px)</div>
            <input 
              type="range" 
              min={12} max={24} step={1}
              value={tweaks.fontSize}
              onChange={e => update({ fontSize: +e.target.value })}
              style={{ width: '100%' }}
            />
          </label>

          {/* Density options */}
          <label style={{ display: 'block', marginBottom: 12 }}>
            <div style={{ marginBottom: 4, color: '#666' }}>Density</div>
            <select 
              value={tweaks.density}
              onChange={e => update({ density: e.target.value })}
              style={{ width: '100%', padding: 6 }}
            >
              <option value="compact">Compact</option>
              <option value="comfortable">Comfortable</option>
              <option value="spacious">Spacious</option>
            </select>
          </label>

          {/* Dark mode toggle */}
          <label style={{ 
            display: 'flex', 
            alignItems: 'center',
            gap: 8,
            marginBottom: 16,
          }}>
            <input 
              type="checkbox" 
              checked={tweaks.dark}
              onChange={e => update({ dark: e.target.checked })}
            />
            <span>Dark Mode</span>
          </label>

          <button onClick={reset} style={{
            width: '100%',
            padding: '8px 12px',
            background: '#f5f5f5',
            border: 'none',
            borderRadius: 6,
            cursor: 'pointer',
            fontSize: 12,
          }}>Reset</button>
        </div>
      ) : (
        <button 
          onClick={() => setOpen(true)}
          style={{
            background: '#1A1A1A',
            color: 'white',
            border: 'none',
            borderRadius: 999,
            padding: '10px 16px',
            fontSize: 12,
            cursor: 'pointer',
            boxShadow: '0 4px 12px rgba(0,0,0,0.15)',
          }}
        >⚙ Tweaks</button>
      )}
    </div>
  );
}
```

### Applying Tweaks

Use Tweaks in main component:

```jsx
function App() {
  const { tweaks } = useTweaks();

  return (
    <div style={{
      '--primary': tweaks.primaryColor,
      '--font-size': `${tweaks.fontSize}px`,
      background: tweaks.dark ? '#0A0A0A' : '#FAFAFA',
      color: tweaks.dark ? '#FAFAFA' : '#1A1A1A',
    }}>
      {/* Your content */}
      <TweaksPanel />
    </div>
  );
}
```

Use variables in CSS:

```css
button.cta {
  background: var(--primary);
  color: white;
  font-size: var(--font-size);
}
```

## Typical Tweak Options

What tweaks to add for different design types:

### General
- Primary color (color picker)
- Font size (slider 12-24px)
- Typography (select: display font vs body font)
- Dark mode (toggle)

### Slide deck
- Theme (light/dark/brand)
- Background style (solid/gradient/image)
- Font contrast (more decorative vs more restrained)
- Information density (minimal/standard/dense)

### Product prototype
- Layout variants (layout A / B / C)
- Interaction speed (animation speed 0.5x-2x)
- Data amount (mock data rows 5/20/100)
- States (empty/loading/success/error)

### Animation
- Speed (0.5x-2x)
- Loop (once/loop/ping-pong)
- Easing (linear/easeOut/spring)

### Landing page
- Hero style (image/gradient/pattern/solid)
- CTA copy (several variants)
- Structure (single column / two column / sidebar)

## Tweaks Design Principles

### 1. Meaningful options, not折腾人的

Each tweak must show **real design options**. Don't add tweaks nobody will actually switch (e.g., border-radius 0-50px slider — user adjusts and finds all intermediate values ugly).

Good tweaks expose **discrete, thoughtful variations**:
- "Corner style": no corners / subtle corners / big corners (three options)
- Not: "Corner radius": 0-50px slider

### 2. Less is more

Tweaks panel for a design **max 5-6 options**. More becomes "configuration page", loses meaning of quick variation exploration.

### 3. Default value is finished design

Tweaks are **the icing on the cake**. Default must be a complete, shippable design. When user closes Tweaks panel, what they see is the deliverable.

### 4. Reasonable grouping

Group when many options:

```
---- Visual ----
Primary | Font Size | Dark Mode

---- Layout ----
Density | Sidebar Position

---- Content ----
Show Data Amount | State
```

## Forward Compatibility with Source-Level Persistence Host

If later want to upload design to environment supporting source-level tweaks (like Claude.ai Artifacts), preserve **EDITMODE marker block**:

```jsx
const TWEAK_DEFAULTS = /*EDITMODE-BEGIN*/{
  "primaryColor": "#D97757",
  "fontSize": 16,
  "density": "comfortable",
  "dark": false
}/*EDITMODE-END*/;
```

Marker block **does nothing** in localStorage solution (just a regular comment), but will be read in host supporting source writeback, achieving source-level persistence. Adding this does no harm to current environment while maintaining forward compatibility.

## Common Issues

**Tweaks panel covers design content**
→ Make it closable. Default closed, show small button, expand when clicked.

**User needs to repeat settings after switching tweaks**
→ Already using localStorage. If doesn't persist after refresh, check if localStorage available (incognito mode fails, catch it).

**Multiple HTML pages want to share tweaks**
→ Add project name to localStorage key: `design-tweaks-[projectName]`.

**I want tweaks to have linked relationships**
→ Add logic in `update`:

```jsx
const update = (patch) => {
  let next = { ...tweaks, ...patch };
  // Linked: when dark mode selected, auto switch font color
  if (patch.dark === true && !patch.textColor) {
    next.textColor = '#F0EEE6';
  }
  setTweaks(next);
  localStorage.setItem(...);
};
```