# astrology — engine internals

The deterministic ephemeris engine and its interpretation rulesets. For install
instructions, cloud hosting, and env vars, see the [root README](../../README.md)
and [AGENTS.md](../../AGENTS.md).

## Architecture

```
astrology/
├── SKILL.md                       # orchestration + anti-Barnum trust discipline (v2.0)
├── scripts/astro_engine.py        # deterministic ephemeris engine (~2930 lines, 19 modes)
├── scripts/mcp_server.py          # MCP server (18 tools, stdio + SSE)
├── scripts/api.py                 # FastAPI REST server (27 endpoints, auth + billing headers)
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

- **Zero dependencies** — pure-Python geocentric ephemeris (Schlyter algorithms + perturbation terms). Python 3.10+.
- **Auto-upgrades** to Swiss Ephemeris arcsecond precision if `pyswisseph` is installed — no code change needed.
- **19 modes** — see [SKILL.md](SKILL.md) for the full list with parameters.
- **Auto-enriched natal** — aspect patterns, 10 Arabic Parts, 23 fixed stars, Black Moon Lilith, dignities, chart ruler, Descendant, IC, equal houses, navamsa D9, panchang, Mangal Dosha, Kaalsarpa Dosha.

### API surface

| Layer | File | Endpoints/Tools | Transport |
|-------|------|-----------------|-----------|
| CLI | `astro_engine.py --json` | 19 modes | stdin |
| MCP | `mcp_server.py` | 18 tools | stdio / SSE |
| REST | `api.py` | 27 endpoints | HTTP |
| Skill | `SKILL.md` | Agent integration | Claude/Cursor/Copilot |

### Mode examples

```bash
# Natal chart
python3 scripts/astro_engine.py --json '{"year":1990,"month":6,"day":15,
  "hour":14,"minute":30,"lat":40.71,"lng":-74.0,"tz":"America/New_York",
  "systems":["western","vedic","bazi"]}'

# Transit (current sky vs natal)
python3 scripts/astro_engine.py --json '{...natal data...,
  "mode":"transit","transit_date":"2026-12-01"}'

# Synastry (relationship)
python3 scripts/astro_engine.py --json '{...personA...,
  "mode":"synastry","partner":{...personB...}}'

# Vedic divisional chart
python3 scripts/astro_engine.py --json '{...natal data...,
  "mode":"varga","varga":"D10","systems":["vedic"]}'

# Horary (chart of the moment)
python3 scripts/astro_engine.py --json '{...location data...,
  "mode":"horary","question_time":"2026-06-07 12:30",
  "question":"Will my ex come back?"}'
```

### Specialty lookups

```python
from astro_engine import (
    namakaran,         # name syllables from birth nakshatra
    anatomy_chart,     # body regions + afflicted systems
    horary,            # cast + basic signals of a horary chart
    astrocartography,  # planet lines for relocation
)
```

## What it reads

The reference rulesets cover the global astrologer catalog:
love/marriage/heartbreak, career/wealth, timing/crisis/health, soul
purpose/karma, family/children, astrocartography, horary, electional,
medical, corporate, pet, Namakaran, past lives, twin problem, curse, taboo,
lost objects — with a hard ethical frame (no death predictions, real crisis
overrides the chart, no fear-based upsell) and anti-Barnum discipline
(cite the specific placement, no generic fluff).

Full trust discipline in [SKILL.md](SKILL.md).
