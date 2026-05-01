# Orchestrator Integration

Multi-CLI workflow integration for huashu-design. Route design tasks to appropriate CLIs based on task type.

## Contents

| File | Description |
|------|-------------|
| `routing-rules.md` | Design task routing decision matrix |
| `design-rules.md` | 10 core rules for system prompt injection |
| `router.py` | Python CLI router implementation |
| `design-engine-api.md` | REST API specification |

## Quick Start

```bash
# Route a task
python router.py task.json

# Or start API server
python -m http.server 8080
```

## CLI Routing

| Task Type | Primary CLI |
|-----------|-------------|
| Animation/Cinematic | Claude Code |
| UI Prototype | Cursor |
| Content-heavy (Chinese) | Kimi |
| Brand identity | Kimi |

## System Prompt Injection

Add to your agent's system prompt:
```
You follow huashu-design principles:
- Anti-AI Slop, brand-first
- Output-driven design
- Three-attempt minimum
- Verify with Playwright
```

Full rules: `design-rules.md`