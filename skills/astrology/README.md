# astrology — a trustworthy multi-tradition astrology skill

A Claude skill that gives **mathematically real** astrology readings across
three living traditions (Western tropical, Vedic/Jyotisha, Chinese BaZi) and
Tibetan/Buddhist (qualitative), then interprets and counsels like a seasoned
astrologer.

The thesis (why this is trustworthy where a raw LLM is not): an LLM cannot
reliably calculate where Mars was on a Tuesday in 1997 — it hallucinates
chart data. This skill **decouples the calculation from the interpretation**.
A deterministic engine computes the sky; the model only does the synthesis
and counsel a calculator can't.

## Capabilities (v2.0)

### 19 Calculation Modes
`natal` · `transit` · `synastry` · `compatibility` · `composite` · `astrocartography` · `horary` · `event` · `solar_return` · `lunar_return` · `planetary_return` · `navamsa` · `varga` (D2–D60) · `panchang` · `moon_phase` · `numerology` · `progressions` · `planetary_hours` · `transit_natal_aspects`

### Auto-included in Natal
Aspect patterns (Grand Trine, Kite, T-Square, Grand Cross, Yod, Mystic Rectangle, Stellium) · Part of Fortune · Vertex · Black Moon Lilith · Moon phase · 10 Arabic Parts · Fixed star conjunctions (23 stars) · Equal houses · Navamsa D9 · Panchang · Mangal Dosha · Kaalsarpa Dosha · Dignities · Chart ruler · Descendant · IC

### 3 Traditions
Western tropical · Vedic/Jyotisha (Lahiri sidereal) · Chinese BaZi (Four Pillars) + Tibetan/Buddhist qualitative

### 25 REST Endpoints · 18 MCP Tools · Zero Dependencies

## Installation

**Claude Code (recommended):**
```
/plugin marketplace add aryaminus/astro
/plugin install astrology
```

**OpenClaw, Codex, Cursor, Copilot, Gemini CLI, or any of 50+ [Agent Skills](https://agentskills.io) hosts:**
```
npx skills add aryaminus/astro -g
```
(`-g` installs globally for your user. Drop it to scope per-project.)

**Enterprise Frameworks (CrewAI, LangGraph, Manus AI, Salesforce Agentforce):**
- *CrewAI / LangGraph / Manus AI:* Load the server natively into your multi-agent codebases using `langchain-mcp-adapters`.
- *Salesforce Agentforce:* Import the `openapi.yaml` directly as an External Service to bind it to your CRM agents.

**Claude Desktop, Cursor, Zed, Devin (MCP Protocol):**
Requires `pip install mcp`. You can install automatically via Smithery:
```bash
npx @smithery/cli install astrology --client claude
```
Or configure your MCP host manually:
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

**ChatGPT Custom Actions (OpenAPI):**
Paste the contents of `openapi.yaml` into your Custom GPT's Action schema, and update the URL to point to your hosted instance.

## Monetization & API Deployment

**Currently FREE — all endpoints open, no key needed.** Payment infrastructure is pre-wired. Flip a single env var to start charging.

### Quick Start (Free)

```bash
pip install -r requirements.txt
python3 skills/astrology/scripts/api.py
# → http://localhost:8000 — all 25 endpoints, no auth, unlimited
```

### Turn On Payments (One Env Var)

| Env Var | What It Does | Default |
|---------|-------------|---------|
| `ASTRO_API_KEY` | Gate all endpoints behind this key | unset (free) |
| `ASTRO_RATE_LIMIT` | Max requests per IP per hour | 0 (unlimited) |

```bash
# Railway / Render / Fly.io
export ASTRO_API_KEY="sk_live_xxx"    # → 403 without valid key
uvicorn skills.astrology.scripts.api:app --host 0.0.0.0 --port $PORT
```

Every response includes `X-Tool-Price` and `X-Tool-Name` headers — ready for Moesif, x402, or MonetizedMCP billing proxies. `GET /pricing` lists all prices. `GET /health` shows current auth/billing state.

## What it does

**Core readings:**
- **Western tropical** natal charts — Big Three, planets, houses, aspects, dignities, transits, Saturn return. Auto-includes chart ruler, Descendant, IC, Black Moon Lilith, 10 Arabic Parts, 23 fixed star conjunctions, aspect patterns (Grand Trine, T-Square, Yod, Mystic Rectangle, Stellium).
- **Vedic / Jyotisha** (Lahiri sidereal) — lagna, rashi, nakshatra, grahas, yogas, Vimshottari dasha timeline. Auto-includes Panchang (Tithi, Nakshatra, Yoga, Karana), Navamsa D9, Mangal Dosha, Kaalsarpa Dosha.
- **Chinese BaZi** (Four Pillars) — Day Master & strength, five-element balance, Useful God, Ten Gods, ten-year luck pillars, Tai Sui.
- **Tibetan / Buddhist** (qualitative) — year animal + Mewa + Parkha + Kalachakra lung-ta.
- **Relationships** — synastry, 0-100 compatibility scoring (5 subscores), composite (midpoint) charts.
- **Timing** — transits, solar/lunar returns, planetary returns (any planet), secondary progressions, transit-to-natal aspect listing, planetary hours, Panchang.
- **Numerology** — Life Path, Personal Year, Expression, Soul Urge (master numbers 11/22/33 preserved).

**Specialty branches** (see `references/specialty-systems.md`):
- **Astrocartography** — where to live / relocate (`mode:"astrocartography"`)
- **Horary / Prasna** — chart of the moment for a specific question (`mode:"horary"`)
- **Event charts** — any "moment of inception": corporate, pet, wedding, app launch (`mode:"event"`)
- **Namakaran** — name syllables from birth nakshatra
- **Anatomy & surgery timing** — body regions + "avoid Moon in the sign of the body part" rule (`health.md`)
- **Mundane astrology** — political / market / eclipse forecasting
- **Forensic / lost-object** — symbol-based, with honesty about its limits
- **Past lives / evolutionary** — Pluto, Rahu-Ketu, the soul's curriculum
- **Twin problem** — D-9 Navamsha + progressions as the answer

## Architecture

```
astrology/
├── SKILL.md                       # orchestration + anti-Barnum trust discipline (v2.0)
├── scripts/astro_engine.py        # deterministic ephemeris engine (~2930 lines, 19 modes)
├── scripts/mcp_server.py          # MCP server (18 tools, stdio + SSE)
├── scripts/api.py                 # FastAPI REST server (25 endpoints, auth + billing headers)
├── references/                    # grounded classical rulesets (the meaning layer)
│   ├── western.md                 # Big Three, planets, houses, aspects, medical
│   ├── vedic.md                   # Lagna, dasha, yogas, remedies, Namakaran, Guna Milan
│   ├── bazi.md                    # Day Master, useful god, Ten Gods, luck pillars, Tai Sui
│   ├── tibetan.md                 # Losar, Mewa, Parkha, Kalachakra, Dharma frame
│   ├── health.md                  # medical astrology & surgical timing
│   ├── synastry-and-timing.md     # synastry, transits, electional, muhurta
│   ├── specialty-systems.md       # astrocartography, horary, electional, rectification, etc.
│   └── consultation.md            # the human counseling craft + ethics
└── assets/profile-template.md     # how a saved birth profile is remembered
```

## The engine (`scripts/astro_engine.py`)

- **Zero dependencies** — pure-Python geocentric ephemeris (Schlyter algorithms
  + perturbation terms). Runs anywhere with Python 3.9+. Exact to sign/house/nakshatra/dasha.
- **Auto-upgrades** to Swiss Ephemeris arcsecond precision if `pyswisseph` is installed — no code change needed.
- **19 modes** — natal, transit, synastry, compatibility, composite, astrocartography, horary, event, solar_return, lunar_return, planetary_return, navamsa, varga (D2–D60), panchang, moon_phase, numerology, progressions, planetary_hours, transit_natal_aspects.
- **Auto-enriched natal** — aspect patterns, 10 Arabic Parts, 23 fixed stars, Black Moon Lilith, dignities, chart ruler, Descendant, IC, equal houses, navamsa D9, panchang, Mangal Dosha, Kaalsarpa Dosha.

### API surface

| Layer | File | Endpoints/Tools | Transport |
|-------|------|-----------------|-----------|
| CLI | `astro_engine.py --json` | 19 modes | stdin |
| MCP | `mcp_server.py` | 18 tools | stdio / SSE |
| REST | `api.py` | 25 endpoints | HTTP |
| Skill | `SKILL.md` | Agent integration | Claude/Cursor/Copilot |

### Modes

```bash
# Natal chart (default)
python3 scripts/astro_engine.py --json '{"year":1990,"month":6,"day":15,
  "hour":14,"minute":30,"lat":40.71,"lng":-74.0,"tz":"America/New_York",
  "systems":["western","vedic","bazi"]}'

# Transit (current sky vs natal)
python3 scripts/astro_engine.py --json '{...natal data...,
  "mode":"transit","transit_date":"2026-12-01"}'

# Synastry (relationship)
python3 scripts/astro_engine.py --json '{...personA...,
  "mode":"synastry","partner":{...personB...}}'

# Astrocartography (relocation)
python3 scripts/astro_engine.py --json '{...natal data...,
  "mode":"astrocartography"}'

# Horary (chart of the moment)
python3 scripts/astro_engine.py --json '{...location data...,
  "mode":"horary","question_time":"2026-06-07 12:30",
  "question":"Will my ex come back?"}'

# Event (corporate / pet / wedding / app launch / etc.)
python3 scripts/astro_engine.py --json '{"subject":"Acme Corp",
  "kind":"corporate","mode":"event",...moment data...}'
```

### Specialty lookups (callable from a Python session)

```python
from astro_engine import (
    namakaran,         # name syllables from birth nakshatra
    anatomy_chart,     # body regions + afflicted systems
    horary,            # cast + basic signals of a horary chart
    astrocartography,  # planet lines for relocation
)
```

## Usage

Invoke with `/astrology`, or just ask Claude anything astrological ("what's
my chart", "am I compatible with…", "what's my luck this year", "pick an
auspicious wedding date", "where should I live", "is my partner cheating",
"will I have children", "what should I name the baby", "should I have
surgery this month", "what is ChatGPT's chart"). The skill gathers birth
data (or recalls a saved profile), runs the engine, grounds the reading in
the rulesets, and counsels — never inventing a single planetary position.

## Coverage

The reference rulesets cover the questions from the global astrologer
catalog (love/marriage/heartbreak, career/wealth, timing/crisis/health, soul
purpose/karma, family/children, astrocartography, horary, electional,
medical, corporate, pet, Namakaran, past lives, twin problem, curse, taboo,
lost objects) — with a hard ethical frame (no death predictions, real crisis
overrides the chart, no fear-based upsell) and the anti-Barnum discipline
(cite the specific placement, no generic fluff).

## Cloud Hosting & Self-Hosting (v2.1)

The skill works **three ways**:

| Mode | Transport | Use case |
|------|-----------|----------|
| Local skill | `python3` CLI | Claude Code, Cursor, local dev |
| MCP server | stdio (default) / SSE | Claude Desktop, Cursor, Zed, Cloudflare Agents, Smithery |
| REST API | HTTP | ChatGPT Custom GPTs, Coze, Dify, webhooks, server-to-server |

**All three are FREE by default. No auth required, no rate limits.** Set
`ASTRO_API_KEY` env var to gate access when you're ready to monetize.

### One-click deploy to Render (free tier)

The repo ships a `render.yaml` for one-click deploy:

1. Click "New +" → "Blueprint" in [Render](https://render.com)
2. Connect this repo
3. Render reads `render.yaml` and provisions the API + a 1 GB disk for saved profiles
4. Get a public URL like `https://astro-api.onrender.com`
5. Test: `curl https://astro-api.onrender.com/health`

### Self-host with Docker

```bash
git clone https://github.com/aryaminus/astro.git
cd astro
docker compose up --build
# API: http://localhost:8000
# Docs: http://localhost:8000/docs
```

### Self-host with raw Python

```bash
git clone https://github.com/aryaminus/astro.git
cd astro
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn skills.astrology.scripts.api:app --host 0.0.0.0 --port 8000
```

### Run the MCP server (stdio or SSE)

```bash
# stdio (Claude Desktop, Cursor, Zed — local)
python3 -m skills.astrology.scripts.mcp_server

# SSE (Smithery, Cloudflare, Render — cloud)
ASTRO_MCP_TRANSPORT=sse ASTRO_MCP_PORT=8765 \
  python3 -m skills.astrology.scripts.mcp_server
```

### Environment variables

| Var | Default | Effect |
|-----|---------|--------|
| `PORT` | `8000` | HTTP port |
| `ASTRO_API_KEY` | _unset_ | If set, requires `Authorization: <key>` on chart endpoints. **Free if unset.** |
| `ASTRO_RATE_LIMIT` | `0` | Max requests per IP per window. `0` = unlimited. |
| `ASTRO_RATE_WINDOW` | `3600` | Rate-limit window in seconds. |
| `ASTRO_PROFILE_DIR` | `~` | Where saved profiles are persisted. **Set to `/data/profiles` in containers.** |
| `ASTRO_LOG_LEVEL` | `INFO` | `DEBUG` / `INFO` / `WARNING` / `ERROR` |
| `ASTRO_MCP_TRANSPORT` | `stdio` | `stdio` (local) / `sse` (cloud) / `http` (streamable) |
| `ASTRO_MCP_HOST` | `0.0.0.0` | MCP bind host |
| `ASTRO_MCP_PORT` | `8765` | MCP bind port (SSE/HTTP) |

### Chat-style poke endpoint

For agents that want to "poke" the engine with a natural-language question
without deciding which mode to call, hit `POST /interact`:

```bash
curl -X POST $API/interact -H "Content-Type: application/json" -d '{
  "messages": [{"role":"user","content":"what does my birth chart say about love?"}],
  "profile": {"year":1990,"month":6,"day":15,"hour":14,"minute":30,
              "lat":40.71,"lng":-74.0,"tz":"America/New_York","time_known":true}
}'
```

The endpoint detects intent, runs the engine, and returns a
`grounding_packet` the host LLM interprets. Multi-turn is supported via
`session_id` (the profile is cached for follow-up calls).

### Operational endpoints

- `GET /health` — liveness, returns version + feature flags
- `GET /ready` — readiness, loads engine before returning 200
- `GET /version` — version payload
- `GET /metrics` — rate-limit counters, active IPs, uptime, session count (no PII)
- `GET /pricing` — per-call pricing table
- `GET /docs` — interactive Swagger UI
- `GET /openapi.json` — OpenAPI 3.1 spec

### Response headers

Every chart response carries:

- `X-Request-Id` — request correlation id (also accepted from caller)
- `X-API-Version` — `2.1.0`
- `X-RateLimit-Limit` / `X-RateLimit-Remaining` / `X-RateLimit-Reset` — per-IP budget
- `X-Tool-Price` / `X-Tool-Name` — billing/analytics headers (always present)
