# Security Policy

## Supported versions

| Version | Supported          |
|---------|--------------------|
| 2.1.x   | ✅ Active          |
| 2.0.x   | ✅ Security fixes only |
| < 2.0   | ❌ End of life     |

## Reporting a vulnerability

**Please do not file a public GitHub issue for security vulnerabilities.**

Email **security@aryaminus.dev** (or open a [GitHub Security Advisory](https://github.com/aryaminus/astro/security/advisories/new))
with:

1. A description of the vulnerability
2. Steps to reproduce (proof-of-concept preferred)
3. The impact you believe it has
4. Your handle / affiliation (optional, for credit)

We aim to acknowledge within **48 hours** and patch within **14 days** for
high-severity issues.

## Scope

In scope:

- Anything in `skills/astrology/scripts/api.py` (FastAPI server)
- Anything in `skills/astrology/scripts/mcp_server.py` (MCP server)
- Anything in `skills/astrology/scripts/astro_engine.py` (math core)
- The Docker image built from the root `Dockerfile`
- The dependency surface declared in `requirements.txt` (`mcp`, `fastapi`, `uvicorn`)

Out of scope:

- The reference `.md` text files (no executable code, no risk)
- Documentation-only changes
- Denial-of-service via heavy computation (the engine is pure-Python
  and slower than a compiled lib; we will rate-limit, not patch)

## Privacy

The engine **does not** call home. The only outbound network call is the
optional `geocoding-api.open-meteo.com` lookup from the API/MCP wrapper when
a user passes a city name. If `lat`/`lng` are passed directly, no network
call is made.

The REST API stores **no PII by default**. Profile saves are written to a
local JSON file (`~/.astro_profiles.json` or `ASTRO_PROFILE_DIR`); there is
no central database. `DELETE /profile/{name}` and `DELETE /interact/{session_id}`
are GDPR-friendly.

## Bug bounty

We do not currently run a paid bug bounty. Responsible disclosures are
credited in release notes.

## Past advisories

_None._

## Dependency versions

- **Python**: 3.10+ (3.9 not supported — `mcp` SDK requires ≥ 3.10)
- **Runtime deps**: `mcp`, `fastapi`, `uvicorn` (see `requirements.txt`)
- **Optional**: `pyswisseph` (auto-upgrades engine precision if installed)
