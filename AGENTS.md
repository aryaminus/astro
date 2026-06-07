# Astrology Skill

Agent Skills package for trustworthy multi-tradition astrology. Installable across Claude Code, Codex, Cursor, GitHub Copilot, Gemini CLI, and 50+ other [Agent Skills](https://agentskills.io) hosts.

## Structure
- `skills/astrology/SKILL.md` — canonical skill definition / runtime spec the model reads when the slash command fires.
- `skills/astrology/scripts/astro_engine.py` — deterministic ephemeris and chart calculation engine.
- `skills/astrology/references/` — grounding texts and reference frameworks for various astrological systems.

## Installation

### Claude Code (recommended)
```
/plugin marketplace add aryaminus/astro
/plugin install astrology
```

### OpenClaw, Codex, Cursor, Gemini & 50+ Agent Skills Hosts
```
npx skills add aryaminus/astro -g
```
(`-g` installs globally for your user, available across all projects. Drop it to scope per-project.)

### Frameworks (CrewAI, LangGraph, Manus AI, Salesforce Agentforce)
* **CrewAI / LangGraph / Manus AI:** Use the `langchain-mcp-adapters` package to load the MCP server natively into your multi-agent teams.
* **Salesforce Agentforce:** Import the `openapi.yaml` specification directly into Salesforce as an External Service to bind the astrology API to your CRM agents.

### Claude Desktop, Cursor, Zed, Devin (MCP Protocol)
You can install via Smithery (the official MCP registry):
```bash
npx @smithery/cli install astrology --client claude
```
Or configure your MCP client manually to spawn the server:
```json
{
  "mcpServers": {
    "astrology": {
      "command": "python3",
      "args": ["/absolute/path/to/skills/astrology/scripts/mcp_server.py"]
    }
  }
}
```

### ChatGPT Custom Actions (OpenAPI)
Copy the contents of `openapi.yaml` into your Custom GPT's Action schema. Point the server URL to your hosted instance.

## Commands
```bash
# Dev/fallback: direct engine invocation
python3 skills/astrology/scripts/astro_engine.py --json '{"year": 1990, "month": 6, "day": 15, "hour": 14, "minute": 30, "lat": 40.7128, "lng": -74.0060, "tz": "America/New_York", "time_known": true, "systems": ["western", "vedic", "bazi"], "gender": "female"}'

# Update the installed global skill
npx skills add . -g -y
```

## Rules
- One-time setup: `npx skills add . -g -y` copies the skill into `~/.agents/skills/<name>/`. **Working-tree edits do NOT propagate automatically**. To sync after edits, re-run `npx skills add . -g -y`.
- For live-edit on a dev machine, replace the install copy with a symlink to the working tree: `ln -sfn "$PWD/skills/astrology" ~/.agents/skills/astrology` (run from the repo root).

## Capabilities (v2.0)

### 19 Modes
`natal` · `transit` · `synastry` · `compatibility` · `composite` · `astrocartography` · `horary` · `event` · `solar_return` · `lunar_return` · `planetary_return` · `navamsa` · `varga` (D2–D60) · `panchang` · `moon_phase` · `numerology` · `progressions` · `planetary_hours` · `transit_natal_aspects`

### Auto-included in Natal
Aspect patterns (Grand Trine, Kite, T-Square, Grand Cross, Yod, Mystic Rectangle, Stellium) · Part of Fortune · Vertex · Black Moon Lilith · Moon phase · 10 Arabic Parts · Fixed star conjunctions (23 stars) · Equal houses · Navamsa D9 · Panchang · Mangal Dosha · Kaalsarpa Dosha

### 3 Traditions
Western tropical · Vedic/Jyotisha (Lahiri sidereal) · Chinese BaZi (Four Pillars) + Tibetan/Buddhist qualitative

### 18 MCP Tools
`get_astrology_chart` · `get_astrology_reference` · `save_profile` · `get_profile` · `geocode_city` · `get_solar_return` · `get_lunar_return` · `get_compatibility` · `get_navamsa` · `get_panchang` · `get_moon_phase` · `get_numerology` · `get_composite_chart` · `get_progressions` · `get_planetary_return` · `get_varga` · `get_planetary_hours` · `get_transit_aspects`

### Zero Dependencies
Pure-Python ephemeris (stdlib only). Auto-upgrades to Swiss Ephemeris if `pyswisseph` is installed. No paid APIs.

## Cloud Hosting (v2.1)

The skill is deploy-ready out of the box. All three transport modes work:
- **Local skill** — `python3` CLI
- **MCP server** — stdio (default) or SSE for cloud hosts (set `ASTRO_MCP_TRANSPORT=sse`)
- **REST API** — FastAPI, 27 endpoints including `/interact` for chat-style poke

**One-click deploy to Render:** connect this repo via `render.yaml` (already committed). Public URL on Render free tier.

**Self-host:** `docker compose up` or `uvicorn skills.astrology.scripts.api:app --host 0.0.0.0 --port 8000`.

**FREE by default.** Set `ASTRO_API_KEY` to gate, `ASTRO_RATE_LIMIT` to throttle. Response headers `X-Tool-Price` / `X-Tool-Name` are always included for billing/analytics.

### Operational endpoints (no auth)
- `GET /health` — liveness
- `GET /ready` — readiness (loads engine first)
- `GET /version` — version payload
- `GET /metrics` — rate-limit counters, no PII
- `GET /pricing` — per-call pricing
- `GET /docs` — interactive Swagger UI

### Environment variables
| Var | Default | Effect |
|-----|---------|--------|
| `PORT` | `8000` | HTTP port |
| `ASTRO_API_KEY` | _unset_ | Gate chart endpoints. **Free if unset.** |
| `ASTRO_RATE_LIMIT` | `0` | Per-IP cap per window. `0` = unlimited. |
| `ASTRO_RATE_WINDOW` | `3600` | Rate-limit window (sec) |
| `ASTRO_PROFILE_DIR` | `~` | Profile persistence dir. Set `/data/profiles` in containers. |
| `ASTRO_MCP_TRANSPORT` | `stdio` | `stdio` / `sse` / `http` |
| `ASTRO_MCP_PORT` | `8765` | MCP SSE/HTTP port |
