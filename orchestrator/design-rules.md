# Core Design Rules for System Prompt Injection

> 10 core rules from huashu-design to auto-inject into agent system prompts.

## The Rules

### 1. Anti-AI Slop Principle
```
Never produce "AI-generic" outputs. Reject: 
- Default gradients (blue/purple/pink)
- Generic illustrations (unsplash-style)
- Corporate memphis / blob shapes
- Stolen Apple/Figma aesthetics
Always add human touch: local cultural references, 
specific brand DNA, intentional "imperfections".
```

### 2. Brand First, Default Second
```
If brand assets provided: extract logo, color palette, 
typography, voice - integrate into every output.

If no brand assets: use huashu-design's 20 built-in 
design vocabularies (Apple Gallery, Claude Brand, 
Linear Style, etc.) - never generic.
```

### 3. Output-Driven, Not Feature-Driven
```
Never build "features" for the sake of features.
Every design must serve a clear output purpose:
- Product launch animation → cinematic, high-impact
- App prototype → clickable, flows work
- PPT deck → editable, presenter-friendly
- Infographic → print-grade, shareable
```

### 4. Temporal Design Language
```
Animation is not decoration - it's narrative.
- Entrance: 0-15% of timeline (hook)
- Development: 15-70% (show detail)
- Climax: 70-90% (key message)
- Outro: 90-100% (CTA)
Each scene needs clear start/end triggers.
```

### 5. Three-Attempt Minimum
```
Never accept first output. Iterate:
- Attempt 1: Functional but rough
- Attempt 2: Refine typography, spacing
- Attempt 3: Polish micro-interactions
If still not right at 3 → escalate with specific feedback.
```

### 6. Verification Before Delivery
```
Every output must pass:
- Browser render test (no broken layout)
- Font fallbacks work
- Animations don't jitter
- File sizes reasonable
- All links/buttons functional
```

### 7. Context Budget Awareness
```
Start with full context, but know when to trim.
- First 3 messages: max detail
- Messages 4-10: essential only
- Messages 10+: summarize, reference previous
AI attention degrades after ~8K tokens in single thread.
```

### 8. Two-Track Audio
```
Always include both:
- SFX: Sound effects for interactions (UI sounds, transitions)
- BGM: Background music for atmosphere

Never use copyrighted music. Prefer:
- Huashu SFX library (37 presets)
- Production music (Artlist, Epidemic Sound)
```

### 9. Playwright Verification
```
After any HTML output:
- Open in Playwright
- Check console for errors
- Screenshot at key breakpoints
- Verify animations trigger correctly
```

### 10. File Communication Protocol
```
When passing between CLIs/tools:
- Use file paths, not inline content
- Include preview thumbnails where possible
- Note: "This is v2, changed X from v1"
- Keep master assets in /assets folder
```

## Injection Template

Add to your agent's system prompt:

```
You follow huashu-design principles. Key rules:
1. Anti-AI Slop - reject generic outputs
2. Brand-first or use built-in design vocabularies  
3. Output-driven (animation/prototype/deck/infographic)
4. Temporal animation (entrance → development → climax → outro)
5. Three-attempt minimum, verify before delivery
6. Include both SFX + BGM for any animation
7. Verify HTML with Playwright before presenting
```

## Reference

- Full rules: `../SKILL.md`
- Design vocabularies: `../references/design-styles.md`
- Audio library: `../references/sfx-library.md`
- Verification: `../references/verification.md`