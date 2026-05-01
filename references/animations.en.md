# Animations: Timeline Animation Engine

Read this when making animation/motion design HTML. Principles, usage, typical patterns.

## Core Pattern: Stage + Sprite

Our animation system (`assets/animations.jsx`) provides a timeline-driven engine:

- **`<Stage>`**: Container for entire animation, auto-provides auto-scale (fit viewport) + scrubber + play/pause/loop controls
- **`<Sprite start end>`**: Time segment. A Sprite only displays during `start` to `end` time. Internally can use `useSprite()` hook to read its own local progress `t` (0→1)
- **`useTime()`**: Read current global time (seconds)
- **`Easing.easeInOut` / `Easing.easeOut` / ...**: Easing functions
- **`interpolate(t, from, to, easing?)`**: Interpolate based on t

This pattern借鉴Remotion/After Effects ideas, but lightweight, zero dependencies.

## Getting Started

```html
<script type="text/babel" src="animations.jsx"></script>
<script type="text/babel">
  const { Stage, Sprite, useTime, useSprite, Easing, interpolate } = window.Animations;

  function Title() {
    const { t } = useSprite();  // Local progress 0→1
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

**Note range**: `[0, 0.3]` means complete fade-in in first 30% of sprite time, then keep opacity=1.

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

### 3. Character-by-Character Typewriter

```jsx
function Typewriter({ text }) {
  const { t } = useSprite();
  const charCount = Math.floor(text.length * Math.min(t * 2, 1));
  return <span>{text.slice(0, charCount)}</span>;
}
```

### 4. Number Count Up

```jsx
function CountUp({ from = 0, to = 100, duration = 0.6 }) {
  const { t } = useSprite();
  const progress = interpolate(t, [0, duration], [0, 1], Easing.easeOut);
  const value = Math.floor(from + (to - from) * progress);
  return <span>{value.toLocaleString()}</span>;
}
```

### 5. Segmented Explanation (Typical Tutorial Animation)

```jsx
function Scene() {
  return (
    <Stage duration={20}>
      {/* Phase 1: Show problem */}
      <Sprite start={0} end={4}>
        <Problem />
      </Sprite>

      {/* Phase 2: Show approach */}
      <Sprite start={4} end={10}>
        <Approach />
      </Sprite>

      {/* Phase 3: Show result */}
      <Sprite start={10} end={16}>
        <Result />
      </Sprite>

      {/* Subtitle shown throughout */}
      <Sprite start={0} end={20}>
        <Caption />
      </Sprite>
    </Stage>
  );
}
```

## Easing Functions

Preset easing curves:

| Easing | Characteristic | Use For |
|--------|------|------|
| `linear` | Constant speed | Scrolling subtitles, continuous animations |
| `easeIn` | Slow→fast | Exit/disappear |
| `easeOut` | Fast→slow | Entry/appear |
| `easeInOut` | Slow→fast→slow | Position changes |
| **`expoOut`** ⭐ | **Exponential ease-out** | **Anthropic-level main easing** (physical weight feel) |
| **`overshoot`** ⭐ | **Elastic bounce** | **Toggle/button pop/emphasis interaction** |
| `spring` | Spring | Interaction feedback, geometry return |
| `anticipation` | Reverse then forward first | Emphasize action |

**Default main easing use `expoOut`** (not `easeOut`) — see `animation-best-practices.md` §2.
Entry use `expoOut`, exit use `easeIn`, toggle use `overshoot` — basic rhythm for Anthropic-level animation.

## Rhythm and Duration Guide

### Micro-interactions (0.1-0.3 seconds)
- Button hover
- Card expand
- Tooltip appear

### UI Transitions (0.3-0.8 seconds)
- Page switch
- Modal appear
- List item add

### Narrative Animation (2-10 seconds per segment)
- One phase of concept explanation
- Data chart reveal
- Scene transition

### Single Narrative Segment Max 10 Seconds
Human attention limited. 10 seconds for one thing, then move to next.

## Thinking Order for Designing Animation

### 1. Have Content/Story First, Then Animation

**Wrong**: Want fancy animation first, then stuff content in
**Correct**: First clarify what information to convey, then use animation to serve that information

Animation is **signal**, not **decoration**. A fade-in emphasizes "look here, this is important" — if everything fades in, signal失效.

### 2. Write Timeline by Scene

```
0:00 - 0:03   Problem appears (fade in)
0:03 - 0:06   Problem enlarges/expands (zoom+pan)
0:06 - 0:09   Solution appears (slide in from right)
0:09 - 0:12   Solution explained (typewriter)
0:12 - 0:15   Result demo (counter up + chart reveal)
0:15 - 0:18   Summary one sentence (static, read 3 seconds)
0:18 - 0:20   CTA or fade out
```

Write components after timeline.

### 3. Resources First

Images/icons/fonts for animation **prepare first**. Don't search for materials halfway — breaks rhythm.

## Common Issues

**Animation lag**
→ Mainly layout thrashing. Use `transform` and `opacity`, don't change `top`/`left`/`width`/`height`/`margin`. Browser GPU accelerates `transform`.

**Animation too fast, can't see clearly**
→ Humans need 100-150ms to read one Chinese character, 300-500ms for a word. If telling story with text, leave at least 3 seconds per sentence.

**Animation too slow, audience bored**
→ Interesting visual changes should be dense. Static画面 over 5 seconds gets boring.

**Multiple animations affecting each other**
→ Use CSS `will-change: transform` to tell browser in advance this element will move, reduce reflow.

**Recording to video**
→ Use skill's built-in toolchain (one command outputs three formats): see `video-export.md`
- `scripts/render-video.js` — HTML → 25fps MP4 (Playwright + ffmpeg)
- `scripts/convert-formats.sh` — 25fps MP4 → 60fps MP4 + optimized GIF
- Need more precise frame rendering? Make render(t) pure function, see `animation-pitfalls.md` point 5.

## Coordination with Video Tools

This skill makes **HTML animations** (runs in browser). If final output needed as video asset:

- **Short animation/concept demo**: Make HTML animation here → screen recording
- **Long video/narrative**: This skill specializes in HTML animation, long videos use AI video generation skills or professional video software
- **Motion graphics**: Professional After Effects/Motion Canvas more suitable

## About Popmotion and Other Libraries

If you really need physical animations (spring, decay, keyframes with precise timing), our engine can't handle, can fallback to Popmotion:

```html
<script src="https://unpkg.com/popmotion@11.0.5/dist/popmotion.min.js"></script>
```

But **try our engine first**. 90% of cases sufficient.