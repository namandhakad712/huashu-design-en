# App / iOS Prototype-Specific Guidelines · Complete Operations Manual

> The full version spun down from SKILL.md. SKILL.md keeps a quick reference of the 7 hard rules; this file expands each rule: architecture selection, image sources and code, the AppPhone JSX skeleton, the three-step ios_frame usage, and the full taste-anchor table.


When building iOS/Android/mobile app prototypes (triggers: "app prototype", "iOS mockup", "mobile app", "make an app"), the four rules below **override** the generic placeholder principles — an app prototype is a live demo; static staged mockups and beige placeholder cards aren't convincing.

### 0. Architecture selection (decide this first)

**Single-file inline React by default** — all JSX/data/styles go directly inside the main HTML's `<script type="text/babel">...</script>` tag; **don't** load them externally via `<script src="components.jsx">`. Reason: under the `file://` protocol, browsers block external JS as cross-origin, and forcing the user to start an HTTP server violates the "double-click and it opens" prototype instinct. Local images must be embedded as base64 data URLs — don't assume a server exists.

**Split into external files only in two cases**:
- (a) a single file over 1000 lines is hard to maintain → split into `components.jsx` + `data.js`, and clearly state the delivery instructions (`python3 -m http.server` command + access URL)
- (b) multiple subagents need to write different screens in parallel → `index.html` + a standalone HTML per screen (`today.html`/`graph.html`...), aggregated via iframe, each screen still a self-contained single file

**Selection quick reference**:

| Scenario | Architecture | Delivery |
|------|------|----------|
| Solo building a 4-6 screen prototype (mainstream) | Single-file inline | One `.html`, double-click to open |
| Solo building a large app (>10 screens) | Multiple jsx + server | Include a startup command |
| Multiple agents in parallel | Multiple HTML + iframe | Aggregated in `index.html`, each screen opens standalone |

### 1. Find real images first, not placeholders sitting around

By default, actively fetch real images to fill the screens; don't draw SVGs, don't leave beige cards sitting there, don't wait for the user to ask. Common channels:

| Scenario | Preferred channel |
|------|---------|
| Art / museum / history content | Wikimedia Commons (public domain), Met Museum Open Access, Art Institute of Chicago API |
| General lifestyle / photography | Unsplash, Pexels (royalty-free) |
| Assets the user already has locally | `~/Downloads`, the project's `_archive/`, or the user-configured asset library |

Wikimedia download pitfalls (on this machine, curl over the proxy breaks TLS; Python urllib works directly):

```python
# A compliant User-Agent is mandatory, otherwise 429
UA = 'ProjectName/0.1 (https://github.com/you; you@example.com)'
# Use the MediaWiki API to look up the real URL
api = 'https://commons.wikimedia.org/w/api.php'
# action=query&list=categorymembers to batch-fetch series / prop=imageinfo+iiurlwidth to get a thumburl at a given width
```

**Only** when all channels fail / copyright is unclear / the user explicitly asks do you fall back to an honest placeholder (still, don't draw crummy SVGs).

**Real-image honesty test** (critical): before picking an image, ask yourself — "if this image were removed, would the information suffer?"

| Scenario | Verdict | Action |
|------|------|------|
| Covers for article/Essay lists, scenic headers on profile pages, decorative banners on settings pages | Decorative, no inherent relation to the content | **Don't add**. Adding one is AI slop, equivalent to a purple gradient |
| Portraits for museum/person content, product photos for product details, places on map cards | The content itself, inherently related | **Must add** |
| Faint texture behind diagrams / visualizations | Atmosphere, defers to the content without stealing the show | Add, but opacity ≤ 0.08 |

**Counterexamples**: pairing a text Essay with an Unsplash "inspiration image", putting a stock photo model in a notes app — both are AI slop. Permission to use real images is not a license to abuse them.

### 2. Delivery format: default to "tiled + interactive", don't ask the user

The iOS app prototype has **exactly one default delivery format — stop asking the user "tiled or interactive"**: **tile 4-6 main screens, and make every phone interactive**. You see the whole picture at a glance (multiple iPhones side by side), and each phone supports tab switching and basic in-screen actions (expand, switch, select, open a modal). Both benefits delivered in one go; don't make the user choose one.

| Dimension | Default approach |
|------|---------|
| **Screen count** | Tile **4-6 main screens** (covering the app's core feature surface, not just any screens). If there are more than 6, take the 4-6 most important; the rest are reachable via tabs/navigation within a single phone |
| **Layout** | Multiple standalone iPhones side by side with `flexWrap`, each with a small italic label line above it indicating which screen it is |
| **Interaction per phone** | Each phone is an independent mini state machine: the tab bar switches, buttons/cards/toggles inside the screen are clickable, modals can pop up — not a static staged mockup |

**Only two exceptions deviate from the default** (only when the user explicitly says so; otherwise always the default):
- User explicitly says "static screenshots only / doesn't need to be clickable / just checking the layout" → fall back to a purely static overview (each phone only renders `ScreenComponent`, no state machine attached)
- User explicitly says "demonstrate a single flow / walk through onboarding / single-phone demo" → a single `AppPhone` runs the full flow

**Default skeleton** (tiled phones, each with its own stateful AppPhone):

```jsx
// each phone = one independent state machine, initially landing on the main screen it owns
function AppPhone({ initial }) {
  const [screen, setScreen] = React.useState(initial);
  const [modal, setModal] = React.useState(null);
  // render the ScreenComponent matching screen, passing callbacks like onTabChange/onOpen/onClose/onToggle
  return (
    <IosFrame>
      <ScreenComponent
        screen={screen}
        onTabChange={setScreen}
        onOpen={setModal}
        onClose={() => setModal(null)}
      />
    </IosFrame>
  );
}

// tiled: 4-6 phones side by side, each initial landing on a different main screen
<div style={{display: 'flex', gap: 32, flexWrap: 'wrap', padding: 48, alignItems: 'flex-start'}}>
  {mainScreens.map(s => (
    <div key={s.id}>
      <div style={{fontSize: 13, color: '#666', marginBottom: 8, fontStyle: 'italic'}}>{s.label}</div>
      <AppPhone initial={s.id} />
    </div>
  ))}
</div>
```

Screen components take callback props (`onTabChange`, `onOpen`, `onClose`, `onToggle`, `onAnnotation`) instead of hardcoding state. TabBar, buttons, work cards, and toggles get `cursor: pointer` + hover feedback. Each phone lands on a different main screen, but they can reach each other after tab switching — tiling gives the overview, clicking gives the depth.

### 3. Run a real click-through test before delivery

Static screenshots only show the layout; interaction bugs are only found by clicking through. Use Playwright to run 3 minimal click tests: enter details / key annotation points / tab switching. Confirm `pageerror` is 0 before delivering. Playwright can be invoked via `npx playwright`, or via the machine's global install path (`npm root -g` + `/playwright`).

### 4. Taste anchors (pursue list, first-choice fallback)

Without a design system, default to these directions to avoid hitting AI slop:

| Dimension | Preferred | Avoid |
|------|------|------|
| **Typography** | Serif display (Newsreader/Source Serif/EB Garamond) + `-apple-system` body | SF Pro or Inter everywhere — too close to the system default, no personality |
| **Color** | One warm background tone + a **single** accent throughout (rust orange / dark green / deep red) | Multi-color clustering (unless the data genuinely has ≥3 categorical dimensions) |
| **Information density · restrained** (default) | One fewer container layer, one fewer border, one fewer **decorative** icon — give the content room to breathe | Every card paired with a meaningless icon + tag + status dot |
| **Information density · high-density** (exception) | When the product's core selling point is "intelligence / data / context-awareness" (AI tools, dashboards, trackers, Copilot, Pomodoro timers, health monitoring, expense trackers), every screen needs **at least 3 visible product-differentiating pieces of information**: non-decorative data, conversation/reasoning snippets, state inference, contextual relations | Just a button and a clock — the AI's intelligence isn't expressed, no different from an ordinary app |
| **Detail signature** | Keep one "screenshot-worthy" texture: a very faint oil-painting texture / a serif italic quote / a full-screen black recording waveform | Spreading effort evenly everywhere, ending up bland in every spot |

**Both principles apply at once**:
1. Taste = one detail done to 120%, the rest to 80% — not refined everywhere, but refined enough in the right places
2. Subtraction is a fallback, not a universal law — when the product's core selling point needs information density (AI / data / context-aware categories), addition outranks restraint. See "information density types" below.

### 5. iOS device frames must use `assets/ios_frame.jsx` — hand-writing Dynamic Island / status bar is forbidden

When making an iPhone mockup, **mandatorily use** `assets/ios_frame.jsx`. It's a standard shell already aligned to the exact iPhone 15 Pro specs: the bezel, Dynamic Island (124×36, top:12, centered), status bar (time/signal/battery, keeping clear of the island on both sides, vertically centered on the island's midline), Home Indicator, and content-area top padding are all handled.

**Never hand-write any of the following in your HTML**:
- `.dynamic-island` / `.island` / `position: absolute; top: 11/12px; width: ~120; centered black rounded rectangle`
- `.status-bar` with hand-written time/signal/battery icons
- `.home-indicator` / the bottom home bar
- iPhone bezel's rounded outer frame + black stroke + shadow

Hand-writing it hits a position bug 99% of the time — the status bar's time/battery get squeezed by the island, or a miscalculated content top padding puts the first line underneath the island. The iPhone 15 Pro's notch is a **fixed 124×36 pixels**, leaving very little usable width for the status bar on both sides — not something you estimate out of thin air.

**Usage (strict three steps)**:

```jsx
// Step 1: Read this skill's assets/ios_frame.jsx (path relative to this SKILL.md)
// Step 2: Paste the entire iosFrameStyles constant + IosFrame component into your <script type="text/babel">
// Step 3: Wrap your own screen component in <IosFrame>...</IosFrame>; don't touch the island/status bar/home indicator
<IosFrame time="9:41" battery={85}>
  <YourScreen />  {/* content renders from top 54, bottom left for the home indicator — you don't need to worry */}
</IosFrame>
```

**Exceptions**: only bypass it when the user explicitly asks to "fake an iPhone 14 non-Pro notch", "make an Android instead of iOS", or "custom device form factor" — then read the corresponding `android_frame.jsx` or modify `ios_frame.jsx`'s constants; **don't** build a separate island/status bar setup in the project HTML.
