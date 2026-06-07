---
name: Pull request
about: Submit a change to Astro
title: ""
labels: []
---

## What does this change?

<!-- One paragraph. -->

## Why?

<!-- What problem does it solve? Link an issue if there is one. -->

## Type of change

- [ ] Bug fix (non-breaking)
- [ ] New feature (non-breaking)
- [ ] Breaking change (fix or feature that changes existing behavior)
- [ ] Documentation only

## Checklist

- [ ] Engine has **no new imports** outside Python stdlib
- [ ] All 4 surfaces updated (engine, MCP, REST, OpenAPI) — if user-visible
- [ ] `openapi.yaml` validates as YAML
- [ ] `python3 -m py_compile skills/astrology/scripts/*.py` succeeds
- [ ] I tested the new/changed mode end-to-end (curl above)
- [ ] I added an entry to `CHANGELOG.md` under "Unreleased"
- [ ] I updated `skills/astrology/SKILL.md` if the change is user-visible
- [ ] I did **not** add a "death" / "guaranteed" / "will happen" capability
- [ ] Reference texts are MIT-licensed original synthesis (no copyrighted quotes)

## Test data

```json
{
  "year": 1990, "month": 6, "day": 15, "hour": 14, "minute": 30,
  "lat": 40.7128, "lng": -74.0060, "tz": "America/New_York",
  "time_known": true, "systems": ["western", "vedic", "bazi"]
}
```

## Screenshots / output

<!-- If relevant. Otherwise delete this section. -->
