# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.1.2] - 2026-06-07

### Fixed
- **Silent wrong chart on `lon`/`longitude` input** — `calculate_full_profile` read only
  `lng` and defaulted the missing field to `0.0°`, producing a completely wrong ascendant
  with no error signal. `lon`, `long`, and `longitude` are now accepted as aliases.
- **`KeyError: 'year'` on ISO date input** — LLMs naturally pass `{"date":"1990-06-15","time":"14:30"}`;
  the engine hard-required `year`/`month`/`day` with no fallback. ISO `date`/`time` strings are
  now normalized to canonical fields before processing.
- Added `_normalize_birth()` normalizer (called at the top of `calculate_full_profile`) that
  coerces `lon`/`long`/`longitude` → `lng`, `latitude` → `lat`, and ISO `date`/`time` → integer
  fields. Recurses into `partner` for synastry/compatibility. Canonical fields always win.

### Added
- **CI: input-tolerance regression test** — asserts that `lon`, `longitude`, and ISO `date+time`
  variants all produce the same ascendant as the canonical `lng`/`year/month/day` form.
  Prevents the silent-wrong-chart regression from ever shipping again.

### Changed
- Prompt in README and docs/cloud-setup.md now lists `git clone` first (most reliable in
  sandboxes) and annotates the `curl`/release-CDN path as potentially blocked in restricted
  environments. Explicit engine schema (`year/month/day/lat/lng/tz`) is now inline in the
  prompt so AIs don't guess alias field names.

## [2.1.1] - 2026-06-07

### Fixed
- **MCP server could not start** — `mcp.run()` was called with `host`/`port` kwargs it
  doesn't accept (they belong on the `FastMCP` constructor), raising `TypeError` on every
  transport. Boot is now correct; host/port resolve from `$PORT` (cloud) or `ASTRO_MCP_PORT`.
- **MCP `streamable-http` transport** — alias normalization was inverted (`streamable-http`
  → invalid `http`); `http`/`streamable-http`/`streamable_http` now all map correctly.
- **`render.yaml` MCP service** — removed the invalid self-referencing `fromService` port
  binding; the server now binds to Render's injected `$PORT`.
- **`openapi.yaml`** — removed a duplicate server `description` key and a duplicate
  `/profile/{name}` path that was silently dropping the `GET` operation from the published
  contract; `GET` + `DELETE` are now both documented.
- **Docs accuracy** — corrected the REST endpoint count (27 → 31), replaced a dead
  advertised instance URL (`astro-api.onrender.com`) with placeholders, and restored an
  astrology-qualified README H1 / repo description for discoverability.

### Added
- **Release automation** (`.github/workflows/release.yml`) — tagging `vX.Y.Z` now auto-builds
  and publishes the `astrology.skill` asset, so `releases/latest/download/astrology.skill`
  never goes stale. Verifies the tag matches `plugin.json`/`marketplace.json` versions.
- **CI**: MCP-server SSE boot smoke-test, OpenAPI duplicate-key + api.py-parity checks, and a
  skill-package build + cross-manifest version-agreement check.
- **One-line SKILL.md setup** — point any URL-capable AI at the canonical `SKILL.md` spec.

### Changed
- Aligned all manifest versions (`SKILL.md` was stale at `2.0`) to a single coherent version.

## [2.1.0] - 2026-06-06

### Added
- **Cloud hosting**: `Dockerfile`, `render.yaml`, `docker-compose.yml`, `.dockerignore`
  for one-click Render deploy and Docker self-hosting
- **SSE transport** for MCP server (`ASTRO_MCP_TRANSPORT=sse`) for cloud MCP hosts
- **`/interact` endpoint** — chat-style poke endpoint that detects intent from
  natural-language questions, runs the engine, and returns a structured
  `grounding_packet` for the host LLM to interpret; multi-turn via `session_id`
- **Per-IP rate limiter** (configurable via `ASTRO_RATE_LIMIT` /
  `ASTRO_RATE_WINDOW`); in-process sliding window, thread-safe
- **API key gate** (optional, via `ASTRO_API_KEY`); **free by default**
- **Operational endpoints**: `/`, `/health`, `/ready`, `/version`, `/metrics`
- **Request-id middleware** — every response carries `X-Request-Id` (also accepted from caller)
- **Rate-limit response headers** — `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`
- **`DELETE /profile/{name}`** — GDPR-friendly profile removal
- **`DELETE /interact/{session_id}`** — clear chat-style sessions
- **Container-safe profile directory** — `ASTRO_PROFILE_DIR` (defaults to `/data/profiles` in Docker)
- **OpenAPI 3.1** spec at v2.1.0, 31 paths, reusable 429/403 responses, Render server
- **CI workflow** — smoke-tests all 18 MCP tools + 27 REST endpoints
- **Dependabot** config for `pip` and `docker`
- **CodeQL** security analysis workflow
- **Issue templates** for bugs, features, and questions
- **PR template** with checklist
- **CODEOWNERS**
- **Top-level README, LICENSE (MIT), CONTRIBUTING, SECURITY, SUPPORT** for the GitHub repo
- `MIT` license with explicit astrology-content disclaimer

### Changed
- `mcp_server.py`: transport is now env-driven (`ASTRO_MCP_TRANSPORT`),
  host/port env vars, import path fix so the module works whether invoked as
  a module or as a script
- `api.py`: structured logging, exception handler, request lifecycle logging
- `openapi.yaml`: bumped to 2.1.0, added Render server, added reusable
  `TooManyRequests` + `Unauthorized` response components
- `README.md` (skill): added cloud hosting section with env var table
- `AGENTS.md`: added Cloud Hosting section

## [2.0.0] - 2026-06-06

### Added
- **14 new calculation features** from a 16-competitor audit:
  - Aspect patterns: Grand Trine, Kite, T-Square, Grand Cross, Yod, Stellium, **Mystic Rectangle**
  - Solar return, lunar return
  - Compatibility scoring (0-100) with 5 subscores
  - Part of Fortune (sect-aware), Vertex, Moon phase, Upcoming moon phases
  - Navamsa chart (D9) with vargottama detection
  - Panchang: Tithi, Nakshatra, Yoga, Karana
  - Numerology: Life Path, Personal Year, Expression, Soul Urge (master numbers preserved)
  - Equal houses
  - Composite chart (midpoint)
  - Black Moon Lilith (mean)
  - Secondary progressions (1 day = 1 year)
  - Generic planetary returns
  - 10 Arabic Parts (Pars Spiritus, Amoris, Fidei, ...)
  - 23 fixed-star conjunctions with magnitude + nature
  - Mangal Dosha + Kaalsarpa Dosha
  - Varga charts D2–D60
  - Transit-to-natal aspects with applying/separating
  - Chaldean planetary hours
- **6 new dispatchers** wired into the engine entry point
- **Western chart enrichment**: chart ruler, descendant, imum coeli
- **Auto-included in natal**: aspect patterns, special points (with BML),
  arabic_parts, fixed_star_conjunctions, equal_houses, panchang, navamsa,
  mangal_dosha, kaalsarpa_dosha
- **18 MCP tools** (was 16)
- **25 REST endpoints** (was 9)
- **OpenAPI 3.1** spec with 25 paths
- **Billing/analytics headers** (`X-Tool-Price`, `X-Tool-Name`) on every chart call
- **8 reference rulesets** (was 5): added tibetan.md, specialty-systems.md, consultation.md

### Changed
- `astro_engine.py` grew from ~1558 → ~2930 lines while remaining pure-stdlib
- Bumped version to 2.0.0 across `api.py`, `openapi.yaml`, `SKILL.md`

### Fixed
- `compatibility_score` tuple unpacking
- `detect_aspect_patterns` set `.values()` call

## [1.0.0] - 2024

### Added
- Initial release: 5 calculation modes (natal, transit, synastry, progressions, solar return)
- Single tradition (Western tropical)
- Pure-Python ephemeris engine, zero dependencies
- 1 REST endpoint, no MCP server
- 2 reference rulesets (western, vedic basics)

[2.1.0]: https://github.com/aryaminus/astro/compare/v2.0.0...v2.1.0
[2.0.0]: https://github.com/aryaminus/astro/compare/v1.0.0...v2.0.0
[1.0.0]: https://github.com/aryaminus/astro/releases/tag/v1.0.0
