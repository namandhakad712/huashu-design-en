# Design Engine API Specification

> API for programmatic design task execution across CLIs.

## Base Endpoint

```
POST /api/design/generate
```

## Request Schema

```json
{
  "prompt": "Create a product launch animation...",
  "output_type": "animation | prototype | deck | infographic",
  "options": {
    "style": "Apple Gallery | Claude Brand | Linear Style",
    "brand_assets": "base64 or file:// URL",
    "duration": 30,
    "language": "en | zh",
    "verify": true
  }
}
```

## Response Schema

```json
{
  "task_id": "uuid",
  "status": "queued | running | completed | failed",
  "output": {
    "path": "/outputs/xxx.html",
    "preview": "base64 thumbnail",
    "format": "html"
  },
  "metadata": {
    "duration_seconds": 45,
    "iterations": 3,
    "cli_used": "claude"
  }
}
```

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| POST | /api/design/generate | Create new design task |
| GET | /api/design/{task_id} | Get task status |
| GET | /api/design/{task_id}/output | Download output |
| POST | /api/design/{task_id}/regenerate | Regenerate with changes |
| GET | /api/styles | List available design vocabularies |
| POST | /api/verify | Verify HTML output |

## CLI Integration

### Claude Code
```bash
claude --print "Using huashu-design, {prompt}"
```

### Cursor
```bash
cursor --prompt "{prompt}" --skill huashu-design
```

### Kimi
```bash
kimi generate --type design --prompt "{prompt}"
```

## Error Codes

| Code | Description |
|------|-------------|
| 400 | Invalid request body |
| 404 | Task not found |
| 500 | CLI execution failed |
| 503 | All CLIs busy |