# Animations: Timeline Animation Engine

Read this when making animation/motion design HTML. Principles, usage, typical patterns.

## Core Pattern: Stage + Sprite

Our animation system (`assets/animations.jsx`) provides a timeline-driven engine:

- **`<Stage>`**: the container of the whole animation, automatically providing auto-scale (fit viewport) + scrubber + play/pause/loop controls
- **`<Sprite start end>`**: a time segment. A Sprite is only displayed during the `start` to `end` window. Internally you can use the `useSprite()` hook to read its own local progress `t` (0→1)
- **`useTime()`**: read the current global time (seconds)
- **`Easing.easeInOut` / `Easing.easeOut` / ...**: easing functions
- **`interpolate(t, from, to, easing?)`**: interpolate based on t

This pattern borrows from Remotion / After Effects thinking, but lightweight and zero-dependency.

## Getting Started

```html
<script type="text/babel" src="animations.jsx"></script>
<script type="text/babel">
  const { Stage, Sprite, useTime, useSprite, Easing, interpolate } = window.Animations;

  function Title() {
    const { t } = useSprite();  // local progress 0→1
    const opacity = interpolate(t, [0, 1], [0, 1], Easing.easeOut);
    const y = interpolate(t, [0, 1], [40, 0], Easing.easeOut);
    return (
      <h1 style={{ 
        opacity, 
        transform: `translateY(${y}px)`,
        fontSize: 120,
        fontWeight: 900,
      }}>
        Hello.
      </h1>
    );
  }

  function Scene() {
    return (
      <Stage duration={10}>  {/* 10-second animation */}
        <Sprite start={0} end={3}>
          <Title />
        </Sprite>
        <Sprite start={2} end={5}>
          <SubTitle />
        </Sprite>
        {/* ... */}
      </Stage>
    );
  }

  const root = ReactDOM.createRoot(document.getElementById('root'));
  root.render(<Scene />);
</script>
```

## Common Animation Patterns

### 1. Fade In / Fade Out

```jsx
function FadeIn({ children }) {
  const { t } = useSprite();
  const opacity = interpolate(t, [0, 0.3], [0, 1], Easing.easeOut);
  return <div style={{ opacity }}>{children}</div>;
}
```

**Note on the range**: `[0, 0.3]` means the fade-in completes in the first 30% of the sprite's time, then stays at opacity=1.

### 2. Slide In

```jsx
function SlideIn({ children, from = 'left' }) {
  const { t } = useSprite();
  const progress = interpolate(t, [0, 0.4], [0, 1], Easing.easeOut);
  const offset = (1 - progress) * 100;
  const directions = {
    left: `translateX(-${offset}px)`,
    right: `translateX(${offset}px)`,
    top: `translateY(-${offset}px)`,
    bottom: `translateY(${offset}px)`,
  };
  return (
    <div style={{
      transform: directions[from],
      opacity: progress,
    }}>
      {children}
    </div>
  );
}
```

### 3. Typewriter Effect (⚠️ first distinguish the two scenarios; don't use per-character pops)

A constant-speed per-character Typewriter is the official counter-example (in the best-practices "AI slop" list: it looks like old movie subtitles). Pick the right solution by content:

- **AI output** (token streaming emergence) → Chunk Reveal: irregular blocky emergence, see `animation-best-practices.md` §4.5 / `gsap-recipes.md` §3.4
- **User input** (a real person typing in an input box) → 3f/character + cursor steady-on turning to blinking + occasional backspaces, see `ui-demo-animation.md` trick ③

### 4. Number Count-Up

```jsx
function CountUp({ from = 0, to = 100, duration = 0.6 }) {
  const { t } = useSprite();
  const progress = interpolate(t, [0, duration], [0, 1], Easing.easeOut);
  const value = Math.floor(from + (to - from) * progress);
  return <span>{value.toLocaleString()}</span>;
}
```

### 5. Segmented Explanation (typical teaching animation)

```jsx
function Scene() {
  return (
    <Stage duration={20}>
      {/* Phase 1: present the problem */}
      <Sprite start={0} end={4}>
        <Problem />
      </Sprite>

      {/* Phase 2: present the approach */}
      <Sprite start={4} end={10}>
        <Approach />
      </Sprite>

      {/* Phase 3: present the result */}
      <Sprite start={10} end={16}>
        <Result />
      </Sprite>

      {/* caption shown throughout */}
      <Sprite start={0} end={20}>
        <Caption />
      </Sprite>
    </Stage>
  );
}
```

## Easing Functions

The preset easing curves:

| Easing | Characteristics | Used for |
|--------|------|------|
| `linear` | constant speed | scrolling captions, continuous animation |
| `easeIn` | slow→fast | exiting/disappearing |
| `easeOut` | fast→slow | entering/appearing |
| `easeInOut` | slow→fast→slow | position changes |
| **`expoOut`** ⭐ | **exponential ease-out** | **Anthropic-grade primary easing** (physical weight) |
| **`overshoot`** ⭐ | **elastic bounce-back** | **Toggles / button pops / emphasis interactions** |
| `spring` | spring | interaction feedback, geometry settling |
| `anticipation` | reverse first, then forward | emphasis motions |

**The default primary easing is `expoOut`** (not `easeOut`) — see `animation-best-practices.md` §2.
Entries use `expoOut`, exits use `easeIn`, toggles use `overshoot` — the basic rules of Anthropic-grade animation.

## Rhythm and Duration Guidelines

### Micro-interactions (0.1-0.3s)
- button hover
- card expand
- tooltip appearance

### UI transitions (0.3-0.8s)
- page switching
- modal appearance
- list item joining

### Narrative animation (2-10s per segment)
- one phase of a concept explanation
- data chart reveal
- scene transitions

### A single narrative segment must not exceed 10 seconds
Human attention is limited. Say one thing in 10 seconds, then move on to the next.

## The Thinking Order for Designing Animation

### 1. Content/story first, animation second

**Wrong**: first want to do fancy animation, then stuff content into it
**Right**: first figure out what information you want to convey, then use animation to serve that information

Animation is **signal**, not **decoration**. A fade-in emphasizes "this is important, please look" — if everything fade-ins, the signal loses its meaning.

### 2. Write the timeline by Scene

```
0:00 - 0:03   problem appears (fade in)
0:03 - 0:06   problem enlarges/expands (zoom+pan)
0:06 - 0:09   solution appears (slide in from right)
0:09 - 0:12   solution expanded explanation (typewriter)
0:12 - 0:15   result demo (counter up + chart reveal)
0:15 - 0:18   one-sentence summary (static, read for 3 seconds)
0:18 - 0:20   CTA or fade out
```

Write the timeline first, then the components.

### 3. Assets first

Prepare the images/icons/fonts the animation needs **up front**. Don't go hunting for assets halfway through drawing — it breaks the rhythm.

## Common Issues

**Animation stutters**
→ Mainly layout thrashing. Use `transform` and `opacity`; don't touch `top`/`left`/`width`/`height`/`margin`. The browser GPU-accelerates `transform`.

**Animation too fast, hard to read**
→ A human takes 100-150ms to read one Chinese character, 300-500ms for a word. If you're telling the story with text, give each sentence at least 3 seconds.

**Animation too slow, the audience is bored**
→ Interesting visual changes should be dense. A static frame for more than 5 seconds gets dull.

**Multiple animations affecting each other**
→ Use CSS `will-change: transform` to tell the browser early that this element will move, reducing reflow.

**Recording to video**
→ Use the skill's built-in toolchain (one command, three formats out): see `video-export.md`
- `scripts/render-video.js` — HTML → 25fps MP4 (Playwright + ffmpeg)
- `scripts/convert-formats.sh` — 25fps MP4 → 60fps MP4 + optimized GIF
- Want more precise frame rendering? Make render(t) a pure function, see item 5 in `animation-pitfalls.md`

## Coordination with Video Tools

This skill does **HTML animation** (running in the browser). If the final output is to be used as video material:

- **Short animations / concept demos**: make HTML animation with these methods → screen record
- **Long videos / narratives** (5-20 minutes with voiceover): go through SKILL.md Step 9.5's voiceover-driven pipeline (`voiceover-pipeline.md`); don't outsource to other tools
- **Motion graphics**: professional After Effects / Motion Canvas is more suitable

## When You Need Physics Animation (spring / decay)

Don't pull in Popmotion (the CDN is guaranteed to fail on restricted networks, violating the self-containment principle, see `animation-pitfalls.md` #17). For spring needs go with GSAP: `elastic.out` / `back.out` and custom springEase mappings see `gsap-recipes.md` §1.2; for landing settle, use the dampedSettle closed-form solution (`camera-language.md` §9).
