# Astro — Trustworthy Multi-Tradition Astrology for AI Agents

> A deterministic, multi-tradition astrology engine that **decouples calculation
> from interpretation** so AI agents never have to hallucinate a planetary
> position to answer "what does my chart say?"

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-zero-brightgreen.svg)]())
[![MCP](https://img.shields.io/badge/MCP-compatible-blueviolet)](https://modelcontextprotocol.io)
[![MCP Tools](https://img.shields.io/badge/MCP_tools-18-purple)]())
[![REST Endpoints](https://img.shields.io/badge/REST_endpoints-27-orange)]())
[![Modes](https://img.shields.io/badge/calculation_modes-19-ff69b4)]())
[![Traditions](https://img.shields.io/badge/traditions-3-teal)]())
[![Deploy](https://img.shields.io/badge/Deploy-Render-46a2f1)](render.yaml)

---

## Why this exists

A raw LLM cannot reliably tell you where Mars was on a Tuesday in 1997 — it
hallucinates chart data. **Astro** solves this by splitting the work:

| Layer | What it does | Who does it |
|-------|--------------|-------------|
| **Engine** | Computes mathematically real sky positions, aspects, dashas, doshas, fixed-star conjunctions, Arabic Parts, etc. | Deterministic Python (zero deps) |
| **Skill** | Orchestrates the engine + loads classical interpretation rulesets | The host LLM |
| **Glue** | Lets any AI platform reach the engine: MCP, REST, CLI, ChatGPT Actions, Salesforce Agentforce | MCP / FastAPI / CLI wrappers |

The model never has to guess a position. It interprets structured output the
engine computed, grounded in classical rulesets we ship in
`skills/astrology/references/`.

---

## Features

### 19 calculation modes
`natal` · `transit` · `synastry` · `compatibility` · `composite` · `astrocartography` · `horary` · `event` · `solar_return` · `lunar_return` · `planetary_return` · `navamsa` · `varga (D2–D60)` · `panchang` · `moon_phase` · `numerology` · `progressions` · `planetary_hours` · `transit_natal_aspects`

### 3 traditions, side by side
- **Western tropical** — Big Three, aspects, houses, fixed stars, Arabic Parts
- **Vedic / Jyotisha** — Lahiri sidereal, Lagna, Vimshottari dasha, divisional charts (D2–D60), Nakshatra, Yogas, Mangal/Kaalsarpa Dosha
- **Chinese BaZi** — Four Pillars, Day Master, Ten Gods, luck pillars + qualitative **Tibetan/Buddhist** frame

### Auto-included in every natal chart
Aspect patterns (Grand Trine, Kite, T-Square, Grand Cross, Yod, Mystic Rectangle, Stellium) · Part of Fortune · Vertex · Black Moon Lilith · Moon phase · 10 Arabic Parts · 23 fixed-star conjunctions · Equal houses · Navamsa D9 · Panchang · Mangal Dosha · Kaalsarpa Dosha

### 3 ways to deploy
- **Local skill** — `npx skills add aryaminus/astro -g`
- **MCP server** — stdio (default) or SSE for cloud hosts
- **REST API** — FastAPI with `/docs`, OAuth-style auth, rate limiting, `X-Tool-Price` billing headers

### Zero dependencies
Pure-Python geocentric ephemeris (Schlyter algorithms + JPL perturbation
terms). Runs anywhere with Python 3.9+. Auto-upgrades to Swiss Ephemeris
arcsecond precision if `pyswisseph` is installed — no code change needed.

### Honest
Hard ethics: no death predictions, real crisis overrides the chart,
anti-Barnum discipline (cite the specific placement, no generic fluff).

---

## Quick start

### 1. As a Claude skill (recommended)
```
/plugin marketplace add aryaminus/astro
/plugin install astrology
```

### 2. As an MCP server (Claude Desktop, Cursor, Zed, Devin)
```bash
# Local (stdio)
git clone https://github.com/aryaminus/astro.git
cd astro
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python3 -m skills.astrology.scripts.mcp_server

# Cloud (SSE)
ASTRO_MCP_TRANSPORT=sse ASTRO_MCP_PORT=8765 \
  python3 -m skills.astrology.scripts.mcp_server
```

Or one-shot install via Smithery:
```bash
npx @smithery/cli install astrology --client claude
```

### 3. As a REST API
```bash
# Local
uvicorn skills.astrology.scripts.api:app --host 0.0.0.0 --port 8000

# Docker
docker compose up --build

# One-click to Render (free tier)
# Connect this repo at https://render.com → New + → Blueprint
# render.yaml is committed.
```

Then: `curl http://localhost:8000/health`

### 4. As a CLI
```bash
python3 skills/astrology/scripts/astro_engine.py --json '{
  "year": 1990, "month": 6, "day": 15, "hour": 14, "minute": 30,
  "lat": 40.71, "lng": -74.0, "tz": "America/New_York",
  "time_known": true, "systems": ["western", "vedic", "bazi"]
}'
```

### 5. As a ChatGPT Custom GPT
Copy `openapi.yaml` into the GPT's Action schema. Point the server URL to
your hosted instance.

### 6. As a Salesforce Agentforce External Service
Import `openapi.yaml` directly into Salesforce as an External Service to bind
the astrology API to your CRM agents.

---

## Try it

After installing, ask Claude (or any host agent) any of these — the skill
will compute the chart and ground the reading:

- *"What's my chart?"* — full natal with all 19 modes
- *"What does today have in store for me?"* — current transits + natal aspects
- *"Am I compatible with…?"* — synastry + 0–100 compatibility scoring
- *"What should I name the baby?"* — Namakaran (Vedic name syllables)
- *"When's my next Saturn return?"* — planetary return + timing
- *"Where should I live for career?"* — astrocartography lines
- *"Should I have surgery this month?"* — medical astrology + Moon-in-sign timing
- *"What was the sky like when Apple was founded?"* — event chart
- *"What time should I start the meeting?"* — Chaldean planetary hours

---

## Project layout

```
astro/
├── README.md                       # you are here
├── LICENSE                         # MIT
├── CHANGELOG.md                    # release history
├── CONTRIBUTING.md                 # how to contribute
├── SECURITY.md                     # vulnerability reporting
├── SUPPORT.md                      # where to get help
│
├── skills/astrology/
│   ├── SKILL.md                    # canonical skill spec (loaded by the model)
│   ├── README.md                   # skill-specific docs
│   ├── assets/
│   │   └── profile-template.md     # how saved profiles are remembered
│   ├── references/                 # 8 grounded classical rulesets
│   │   ├── western.md
│   │   ├── vedic.md
│   │   ├── bazi.md
│   │   ├── tibetan.md
│   │   ├── health.md
│   │   ├── synastry-and-timing.md
│   │   ├── specialty-systems.md
│   │   └── consultation.md
│   └── scripts/
│       ├── astro_engine.py         # deterministic ephemeris (~2930 lines, 19 modes)
│       ├── mcp_server.py           # MCP wrapper (18 tools, stdio + SSE)
│       └── api.py                  # FastAPI REST server (27 endpoints)
│
├── openapi.yaml                    # OpenAPI 3.1 spec for ChatGPT, Coze, Agentforce
├── smithery.yaml                   # Smithery registry config
├── gemini-extension.json           # Gemini CLI extension manifest
├── AGENTS.md                       # integration map for 50+ agent hosts
├── llms.txt                        # LLM-friendly project summary
│
├── Dockerfile                      # production image (non-root, /ready healthcheck)
├── docker-compose.yml              # API + optional MCP-over-SSE sidecar
├── render.yaml                     # one-click Render deploy
├── .dockerignore
├── requirements.txt                # mcp + fastapi + uvicorn
│
├── .github/
│   ├── CODEOWNERS
│   ├── dependabot.yml
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug.md
│   │   ├── feature.md
│   │   └── question.md
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── workflows/
│       ├── ci.yml                  # smoke-test all 18 MCP tools + 27 endpoints
│       ├── docker.yml              # publish image to GHCR
│       └── codeql.yml              # security analysis
│
└── .claude-plugin/                 # Claude Code marketplace + plugin manifests
    ├── plugin.json
    └── marketplace.json
```

---

## Architecture

```
                       ┌─────────────────────────────────────────┐
                       │         Host LLM / Agent Runtime        │
                       │  (Claude Code, Cursor, GPT, Coze, ...)  │
                       └─────────────────┬───────────────────────┘
                                         │
              ┌──────────────────────────┼──────────────────────────┐
              │                          │                          │
              ▼                          ▼                          ▼
       ┌──────────────┐           ┌──────────────┐          ┌──────────────┐
       │  MCP server  │           │  REST API    │          │  CLI / SDK   │
       │  18 tools    │           │  27 endpoints│          │  direct call │
       │  stdio / SSE │           │  /docs       │          │  JSON in/out │
       └──────┬───────┘           └──────┬───────┘          └──────┬───────┘
              │                          │                          │
              └──────────────────────────┼──────────────────────────┘
                                         ▼
                       ┌─────────────────────────────────────────┐
                       │  astro_engine.py (zero-dep Python)     │
                       │  Schlyter + JPL perturbation terms      │
                       │  Auto-upgrades to pyswisseph if present │
                       │  19 modes, ~2930 lines, pure stdlib     │
                       └─────────────────┬───────────────────────┘
                                         │
                                         ▼
                       ┌─────────────────────────────────────────┐
                       │  references/*.md (8 rulesets)           │
                       │  The "what does it mean" layer          │
                       │  The host LLM grounds in these.         │
                       └─────────────────────────────────────────┘
```

---

## Configuration

All transport modes honor the same environment variables:

| Var | Default | Effect |
|-----|---------|--------|
| `PORT` | `8000` | HTTP port (REST API) |
| `ASTRO_API_KEY` | _unset_ | If set, requires `Authorization: <key>` on chart endpoints. **Free if unset.** |
| `ASTRO_RATE_LIMIT` | `0` | Max requests per IP per window. `0` = unlimited. |
| `ASTRO_RATE_WINDOW` | `3600` | Rate-limit window in seconds. |
| `ASTRO_PROFILE_DIR` | `~` | Where saved profiles are persisted. **Set to `/data/profiles` in containers.** |
| `ASTRO_LOG_LEVEL` | `INFO` | `DEBUG` / `INFO` / `WARNING` / `ERROR` |
| `ASTRO_MCP_TRANSPORT` | `stdio` | `stdio` (local) / `sse` (cloud) / `http` (streamable) |
| `ASTRO_MCP_HOST` | `0.0.0.0` | MCP bind host |
| `ASTRO_MCP_PORT` | `8765` | MCP bind port (SSE/HTTP) |

---

## Cloud hosting

### Render (free tier, one-click)
1. Go to https://render.com → New + → Blueprint
2. Connect this repo
3. Render reads `render.yaml` and provisions the API + a 1 GB disk for saved profiles
4. Get a public URL like `https://astro-api.onrender.com`
5. Test: `curl https://astro-api.onrender.com/health`

### Self-host
```bash
git clone https://github.com/aryaminus/astro.git
cd astro
docker compose up --build
# API: http://localhost:8000
# Docs: http://localhost:8000/docs
```

Or raw Python:
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn skills.astrology.scripts.api:app --host 0.0.0.0 --port 8000
```

### Other platforms
- **Fly.io** — same Dockerfile works, just `fly launch`
- **Railway** — connect repo, set start command to `uvicorn skills.astrology.scripts.api:app --host 0.0.0.0 --port $PORT`
- **Cloudflare Workers** — use the SSE MCP transport behind a Worker proxy
- **Smithery** — publish via `smithery.yaml`

### Operational endpoints
- `GET /health` — liveness, no auth
- `GET /ready` — readiness (loads engine first), no auth
- `GET /version` — version payload, no auth
- `GET /metrics` — rate-limit counters, no PII, no auth
- `GET /pricing` — per-call pricing, no auth
- `GET /docs` — interactive Swagger UI, no auth
- `GET /openapi.json` — OpenAPI 3.1 spec, no auth

### Response headers (every chart call)
- `X-Request-Id` — request correlation id
- `X-API-Version` — current version
- `X-RateLimit-Limit` / `X-RateLimit-Remaining` / `X-RateLimit-Reset` — per-IP budget
- `X-Tool-Price` / `X-Tool-Name` — billing/analytics headers (always present)

---

## Documentation

- [`AGENTS.md`](AGENTS.md) — integration map for 50+ agent hosts
- [`skills/astrology/SKILL.md`](skills/astrology/SKILL.md) — the canonical skill spec the model reads
- [`skills/astrology/README.md`](skills/astrology/README.md) — engine internals + mode reference
- [`openapi.yaml`](openapi.yaml) — REST API schema
- [`llms.txt`](llms.txt) — LLM-friendly project summary
- [`CHANGELOG.md`](CHANGELOG.md) — release history
- [`CONTRIBUTING.md`](CONTRIBUTING.md) — how to contribute
- [`SECURITY.md`](SECURITY.md) — how to report vulnerabilities

---

## Contributing

We welcome PRs. The hard rules:

1. **The engine stays zero-dep.** No `numpy`, no `pandas`, no `swisseph` as a required dep (it's an optional auto-upgrade).
2. **The engine never imports `mcp`, `fastapi`, or any framework.** Those belong in their wrappers.
3. **If you add a feature, update all 4 surfaces:** engine, MCP server, REST API, OpenAPI spec.
4. **The skill is honest.** No death predictions, no fake precision, anti-Barnum discipline. See `skills/astrology/SKILL.md`.

See [`CONTRIBUTING.md`](CONTRIBUTING.md) for the full workflow.

---

## License

[MIT](LICENSE). The bundled reference texts in `skills/astrology/references/`
are original works by the project authors, also MIT-licensed, synthesizing
classical sources which are public-tradition.

---

## Acknowledgments

Built on the Schlyter algorithm (public domain) and perturbation terms from
NASA JPL (public domain). Auto-upgrades to [Swiss Ephemeris](https://www.astro.com/ftp/swisseph/)
arcsecond precision when `pyswisseph` is installed.

Vedic calculations use the Lahiri ayanamsa (Indian government standard).
Fixed-star coordinates from the [HYG database](https://github.com/astronexus/HYG-Database)
(CC-BY-SA). Arabic Parts use the classical [Lot formulas](https://en.wikipedia.org/wiki/Arabic_parts).
