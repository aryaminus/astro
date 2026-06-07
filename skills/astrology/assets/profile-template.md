# Saved astrology profile — memory template

When a user wants their chart remembered, write ONE memory file per person to the
project memory dir using this shape, then add a one-line pointer to `MEMORY.md`.
This makes every future reading instant and consistent (same chart, read the same way).

Only save when the user asks. Never store a third party's birth data unprompted.

## Memory file format

```markdown
---
name: astro-profile-<person-kebab>
description: Astrology birth profile for <name> — used to recall the chart for any future reading
metadata:
  type: project
---

# Astrology profile — <name>

**Birth data** (the only thing needed to recompute everything):
- Date: <YYYY-MM-DD>  Time: <HH:MM> (time_known: <true|false>)
- Place: <city, country> — lat <±dd.dddd>, lng <±dd.dddd>, tz <IANA name>
- Gender (BaZi only): <m|f|unknown>

**Computed anchors** (cached for quick reference — recompute with the engine for any real reading):
- Western Big Three: Sun <sign>, Moon <sign>, Rising <sign>
- Vedic: Lagna <sign>, Janma Rashi <sign>, Nakshatra <name> pada <n>; current mahadasha <lord> (<start>–<end>)
- BaZi: Day Master <pinyin> (<element>, <strength>); year animal <animal>; useful elements <…>

**Notes from past readings:** <the central paradox, the question they keep asking, what landed>

To recompute: run `scripts/astro_engine.py` with the birth data above.
```

## MEMORY.md pointer line
```
- [Astrology profile — <name>](astro-profile-<person-kebab>.md) — <Sun>/<Moon>/<Rising>, DM <pinyin>; recompute via astrology skill
```

## Why cache the anchors
The birth data alone regenerates the full chart deterministically, so the cached
anchors are just for fast recall and continuity ("last time we talked, you were entering
your Saturn return"). Always recompute with the engine before giving a real reading —
never read from the cache alone, and never from memory of "what the chart probably says."
```
