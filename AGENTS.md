# Astro — Agent Integration Guide

One-line install for 50+ hosts: `npx skills add aryaminus/astro -g`

## Install

| Host | Command |
|------|---------|
| Claude Code | `/plugin marketplace add aryaminus/astro` then `/plugin install astrology` |
| Codex, Cursor, Copilot, Gemini CLI, 50+ hosts | `npx skills add aryaminus/astro -g` |
| claude.ai (web) | [Download `.skill`](https://github.com/aryaminus/astro/releases/latest) → Settings → Capabilities → Skills → + |
| ChatGPT | Copy [`openapi.yaml`](openapi.yaml) into Custom GPT → Actions → Import |
| Claude Desktop / Zed | `npx @smithery/cli install astrology --client claude` |
| Salesforce Agentforce | Import [`openapi.yaml`](openapi.yaml) as External Service |
| Manual / dev | `git clone https://github.com/aryaminus/astro.git && ln -sfn "$(pwd)/astro/skills/astrology" ~/.agents/skills/astrology` |

## 18 MCP Tools

`get_astrology_chart` · `get_astrology_reference` · `save_profile` · `get_profile` · `geocode_city` · `get_solar_return` · `get_lunar_return` · `get_compatibility` · `get_navamsa` · `get_panchang` · `get_moon_phase` · `get_numerology` · `get_composite_chart` · `get_progressions` · `get_planetary_return` · `get_varga` · `get_planetary_hours` · `get_transit_aspects`

## Dev commands

```bash
# Direct engine invocation
python3 skills/astrology/scripts/astro_engine.py --json '{"year":1990,"month":6,"day":15,"hour":14,"minute":30,"lat":40.7128,"lng":-74.0060,"tz":"America/New_York","time_known":true,"systems":["western","vedic","bazi"]}'

# Sync working-tree edits to installed skill
npx skills add . -g -y

# Live-edit via symlink (dev only)
ln -sfn "$PWD/skills/astrology" ~/.agents/skills/astrology
```

## Cloud config

**Free by default.** Set env vars to monetize:

| Var | Default | Effect |
|-----|---------|--------|
| `PORT` | `8000` | HTTP port |
| `ASTRO_API_KEY` | _unset_ | Gate chart endpoints. **Free if unset.** |
| `ASTRO_RATE_LIMIT` | `0` | Per-IP cap per window. `0` = unlimited. |
| `ASTRO_RATE_WINDOW` | `3600` | Rate-limit window (sec) |
| `ASTRO_PROFILE_DIR` | `~` | Profile persistence. Set `/data/profiles` in containers. |
| `ASTRO_LOG_LEVEL` | `INFO` | `DEBUG` / `INFO` / `WARNING` / `ERROR` |
| `ASTRO_MCP_TRANSPORT` | `stdio` | `stdio` / `sse` / `http` |
| `ASTRO_MCP_HOST` | `0.0.0.0` | MCP bind host |
| `ASTRO_MCP_PORT` | `8765` | MCP bind port (SSE/HTTP) |

### Operational endpoints (no auth, no PII)

`GET /health` · `GET /ready` · `GET /version` · `GET /metrics` · `GET /pricing` · `GET /docs` · `GET /openapi.json`

### One-click deploy

- **Render:** connect repo → New → Blueprint (`render.yaml` committed)
- **Docker:** `docker compose up --build`
- **Raw:** `uvicorn skills.astrology.scripts.api:app --host 0.0.0.0 --port 8000`
- **MCP SSE:** `ASTRO_MCP_TRANSPORT=sse python -m skills.astrology.scripts.mcp_server`
