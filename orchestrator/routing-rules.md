# Design Task Routing Rules

> Guidelines for routing design tasks to appropriate CLIs in multi-CLI workflows.

## Overview

When orchestrating between multiple CLIs (Claude Code, Cursor, Kimi, etc.), design tasks should be routed to the CLI that best matches the requirements.

## Routing Decision Matrix

| Task Type | Primary CLI | Fallback | Reason |
|-----------|-------------|----------|--------|
| UI/UX Design with code | Cursor | Claude Code | IDE integration for rapid iteration |
| Content-heavy design | Kimi | Claude Code | Strong Chinese language + long context |
| Animation + video | Claude Code | Kimi | Tool use for video export |
| Brand identity | Kimi | Claude Code | Cultural nuance understanding |
| Rapid prototyping | Cursor | Claude Code | Fast preview cycles |
| High-fidelity presentation | Claude Code | Kimi | Attention to detail |

## Task Classification

### Type A: Visual Design (→ Cursor/Claude Code)
- Component-level UI design
- Interactive prototypes
- Design system creation

### Type B: Content Design (→ Kimi)
- Presentation decks
- Marketing materials
- Copy-heavy layouts

### Type C: Motion Design (→ Claude Code)
- Product launch animations
- Cinematic sequences
- Complex timeline编排

### Type D: Brand Design (→ Kimi)
- Logo concepts
- Visual identity
- Brand guidelines

## Routing Examples

```python
def route_design_task(task):
    if task.type in ['animation', 'cinematic', 'video']:
        return 'claude-code'
    elif task.type in ['prototype', 'component', 'ui']:
        return 'cursor'
    elif task.content_heavy or task.language == 'zh':
        return 'kimi'
    else:
        return 'claude-code'
```

## Multi-CLI Handoff

When a task spans multiple types:
1. Split into subtasks by type
2. Route each to appropriate CLI
3. Consolidate outputs in final step
4. Use huashu-design skill on primary CLI