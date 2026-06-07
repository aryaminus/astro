# astrology — a trustworthy multi-tradition astrology skill

A Claude skill that gives **mathematically real** astrology readings across three living
traditions, then interprets and counsels like a seasoned astrologer.

The thesis (why this is trustworthy where a raw LLM is not): an LLM cannot reliably
calculate where Mars was on a Tuesday in 1997 — it hallucinates chart data. This skill
**decouples the calculation from the interpretation**. A deterministic engine computes
the sky; the model only does the synthesis and counsel a calculator can't.

## What it does
- **Western tropical** natal charts — Big Three, planets, houses, aspects, dignities, transits, Saturn return.
- **Vedic / Jyotisha** (Lahiri sidereal) — lagna, rashi, nakshatra, grahas, yogas, and the **Vimshottari dasha** timeline with dates.
- **Chinese BaZi** (Four Pillars) — Day Master & strength, five-element balance, Useful God, Ten Gods, ten-year luck pillars, Tai Sui.
- **Synastry** (relationship compatibility), **transit forecasting**, **electional** (auspicious dates) and **horary** guidance.

## Architecture
```
astrology/
├── SKILL.md                       # orchestration + anti-Barnum trust discipline
├── scripts/astro_engine.py        # deterministic ephemeris engine (the math layer)
├── references/                    # grounded classical rulesets (the meaning layer)
│   ├── western.md  vedic.md  bazi.md
│   ├── synastry-and-timing.md
│   └── consultation.md            # the human counseling craft + ethics
└── assets/profile-template.md     # how a saved birth profile is remembered
```

## The engine (`scripts/astro_engine.py`)
- **Zero dependencies** — a pure-Python geocentric ephemeris (Schlyter algorithms +
  standard perturbation terms) that runs anywhere with Python 3.9+. Validated against
  published J2000 positions to <0.5°; exact to the sign / house / nakshatra / dasha level.
- **Auto-upgrades** to arcsecond precision and true nodes if `pyswisseph` is installed
  (`pip install pyswisseph`) — no code change; the output's `_meta.engine_backend` says which ran.
- Whole-sign houses (Placidus available via swisseph). BaZi uses solar-term-correct year
  and month boundaries and the standard `(JDN+49)%60` sexagenary day pillar.

```bash
python3 scripts/astro_engine.py --json '{"year":1990,"month":6,"day":15,
  "hour":14,"minute":30,"lat":40.71,"lng":-74.0,"tz":"America/New_York",
  "systems":["western","vedic","bazi"]}'
```
Modes: `natal` (default), `transit` (+`transit_date`), `synastry` (+`partner`).

## Usage
Invoke with `/astrology`, or just ask Claude anything astrological ("what's my chart",
"am I compatible with…", "what's my luck this year", "pick an auspicious date"). The
skill gathers birth data (or recalls a saved profile), runs the engine, grounds the
reading in the rulesets, and counsels — never inventing a single planetary position.
