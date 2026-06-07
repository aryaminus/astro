---
name: Bug report
about: Something is broken in the engine, API, or MCP server
title: "[bug] "
labels: ["bug", "needs-triage"]
assignees: []
---

## What happened

<!-- A clear, one-paragraph description. -->

## Reproduction

<!-- Minimal input that triggers the bug. For chart bugs, paste the JSON
     you sent to the engine. -->

```bash
curl -X POST http://localhost:8000/chart/natal -H "Content-Type: application/json" -d '{
  "year": ..., "month": ..., "day": ..., "hour": ..., "minute": ...,
  "lat": ..., "lng": ..., "tz": "...", "time_known": true
}'
```

## Expected

<!-- What did you expect to happen? -->

## Actual

<!-- What actually happened? Paste response, logs, screenshots. -->

## Environment

- [ ] Version / commit SHA: (run `git rev-parse HEAD`)
- [ ] Python version: (run `python3 --version`)
- [ ] Deployment: local / Docker / Render / `npx skills add`
- [ ] OS:
- [ ] `pyswisseph` installed? (run `pip show pyswisseph`)

## Logs

<!-- Set ASTRO_LOG_LEVEL=DEBUG and paste relevant lines. -->
