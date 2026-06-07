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

## Installation

**Claude Code (recommended):**
```
/plugin marketplace add aryaminus/astro
/plugin install astrology
```

**Codex, Cursor, Copilot, Gemini CLI, or any of 50+ [Agent Skills](https://agentskills.io) hosts:**
```
npx skills add aryaminus/astro -g
```
(`-g` installs globally for your user. Drop it to scope per-project.)

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
To monetize the skill (e.g. via Stripe, x402, or Coze), you must host it as an API instead of running it locally. 

**1. FastAPI Server (For Coze, Dify, and ChatGPT):**
We include a production-ready REST API gated by an optional API key.
```bash
pip install -r requirements.txt
export ASTRO_API_KEY="your_stripe_issued_key" # Optional
python3 skills/astrology/scripts/api.py
```
This runs a server on `http://localhost:8000/chart` matching the `openapi.yaml`.

**2. Hosted MCP Server (For Cursor, Claude, Zed):**
To charge for MCP tool calls using a proxy like MonetizedMCP, host the MCP server via SSE:
```bash
# Using the FastMCP CLI
fastmcp run skills/astrology/scripts/mcp_server.py:mcp --transport sse
```

## What it does

**Core readings:**
- **Western tropical** natal charts — Big Three, planets, houses, aspects, dignities, transits, Saturn return.
- **Vedic / Jyotisha** (Lahiri sidereal) — lagna, rashi, nakshatra, grahas, yogas, and the **Vimshottari dasha** timeline with dates.
- **Chinese BaZi** (Four Pillars) — Day Master & strength, five-element balance, Useful God, Ten Gods, ten-year luck pillars, Tai Sui.
- **Tibetan / Buddhist** (qualitative) — year animal + Mewa + Parkha + Kalachakra lung-ta, using the BaZi engine for the year pillar.
- **Synastry** (relationship compatibility), **transit forecasting**, **electional** (auspicious dates) and **horary** guidance.

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
├── SKILL.md                       # orchestration + anti-Barnum trust discipline
├── scripts/astro_engine.py        # deterministic ephemeris engine (the math layer)
├── references/                    # grounded classical rulesets (the meaning layer)
│   ├── western.md        # Big Three, planets, houses, aspects, medical
│   ├── vedic.md          # Lagna, dasha, yogas, remedies, Namakaran, Mangal Dosha, Guna Milan
│   ├── bazi.md           # Day Master, useful god, Ten Gods, luck pillars, Tai Sui
│   ├── tibetan.md        # Losar, Mewa, Parkha, Kalachakra, Dharma frame
│   ├── health.md         # medical astrology & surgical timing
│   ├── synastry-and-timing.md  # synastry, transits, electional, muhurta
│   ├── specialty-systems.md    # astrocartography, horary, electional deep,
│   │                          #   rectification, Namakaran, lost objects,
│   │                          #   mundane, forensic, corporate, past lives,
│   │                          #   taboo questions, curse, twin, out of scope
│   └── consultation.md   # the human counseling craft + ethics (read for any real reading)
└── assets/profile-template.md    # how a saved birth profile is remembered
```

## The engine (`scripts/astro_engine.py`)

- **Zero dependencies** — a pure-Python geocentric ephemeris (Schlyter
  algorithms + standard perturbation terms) that runs anywhere with Python
  3.9+. Validated against published J2000 positions to <0.5°; exact to the
  sign / house / nakshatra / dasha level.
- **Auto-upgrades** to arcsecond precision and true nodes if `pyswisseph` is
  installed (`pip install pyswisseph`) — no code change; the output's
  `_meta.engine_backend` says which ran.
- **Whole-sign houses** (Placidus available via swisseph). BaZi uses
  solar-term-correct year and month boundaries and the standard
  `(JDN+49)%60` sexagenary day pillar.

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
