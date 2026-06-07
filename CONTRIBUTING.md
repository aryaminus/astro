# Contributing to Astro

Thanks for your interest in making AI-driven astrology more trustworthy.
This project has a few hard rules — they keep the engine correct and the
skill honest.

## Code of conduct

Be kind. Be specific. Disagree with ideas, not people. The maintainers
reserve the right to close unproductive threads.

## Hard rules

### 1. The engine stays zero-dependency

The heart of the project is `skills/astrology/scripts/astro_engine.py`.

- **No** `numpy`, `pandas`, `sweph`, `flatlib`, `pyephem`, or any other lib.
- All math uses the Python stdlib (`math`, `datetime`, `calendar`).
- The minimum Python version is **3.10** (required by the `mcp` SDK).
- The engine **must not import** `mcp`, `fastapi`, `requests`, `urllib`, or
  any framework. It is pure math; wrappers handle I/O.

If your change needs a dependency, it belongs in a wrapper, not the engine.

### 2. Touch all four surfaces

If you add a calculation mode, parameter, or response field, update all of:

1. `skills/astrology/scripts/astro_engine.py` — the calculation
2. `skills/astrology/scripts/mcp_server.py` — expose as MCP tool
3. `skills/astrology/scripts/api.py` — expose as REST endpoint
4. `openapi.yaml` — update the OpenAPI spec

Forgetting one means the change is invisible to half the platform.

### 3. The skill is honest

- No death predictions, no health-outcome guarantees.
- When precision is unknown, say so. The engine reports `~1-2 arcmin`
  for the builtin backend; don't claim sub-arcsecond.
- Anti-Barnum discipline: cite the specific placement, no generic fluff.
- If you add a new mode, document its uncertainty in `SKILL.md`.

### 4. Reference texts are MIT-licensed original works

The `.md` files in `skills/astrology/references/` are **original syntheses**
of classical sources, not copies of copyrighted books. Keep it that way —
paraphrase classical ideas, don't quote at length from copyrighted modern
authors.

## Development workflow

```bash
# 1. Fork + clone
git clone https://github.com/yourname/astro.git
cd astro

# 2. Create a venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 3. Make a branch
git checkout -b feature/my-new-mode

# 4. Edit code

# 5. Run the smoke test
PORT=8765 ASTRO_RATE_LIMIT=0 .venv/bin/python -m uvicorn \
  skills.astrology.scripts.api:app --host 127.0.0.1 --port 8765 &
curl http://127.0.0.1:8765/health

# 6. Test the engine directly
.venv/bin/python skills/astrology/scripts/astro_engine.py --json '{
  "year": 1990, "month": 6, "day": 15, "hour": 14, "minute": 30,
  "lat": 40.71, "lng": -74.0, "tz": "America/New_York",
  "time_known": true, "systems": ["western", "vedic", "bazi"]
}' | python3 -m json.tool

# 7. Add a CLI smoke check (if you added a new mode)
#    See skills/astrology/SKILL.md for the canonical test data.

# 8. Run the full OpenAPI validation
.venv/bin/python -c "import yaml; yaml.safe_load(open('openapi.yaml')); print('OK')"

# 9. Commit + push + open PR
git add -A
git commit -m "feat: <concise description>"
git push origin feature/my-new-mode
```

## Pull request checklist

A maintainer will check the following — please self-check first:

- [ ] Engine change has **no new imports** outside stdlib
- [ ] All 4 surfaces updated (engine, MCP, REST, OpenAPI)
- [ ] `openapi.yaml` validates as YAML
- [ ] `python3 -m py_compile skills/astrology/scripts/*.py` succeeds
- [ ] I tested the new mode end-to-end with the smoke curl above
- [ ] I updated `CHANGELOG.md` under "Unreleased"
- [ ] I updated `skills/astrology/SKILL.md` if the change is user-visible
- [ ] I added a new reference file in `references/` if I added a new tradition
- [ ] I did **not** add a "death" / "guaranteed" / "will happen" capability

## Adding a new tradition

If you're adding a fourth tradition (e.g. Burmese, Burmese-influenced, Hellenistic):

1. Add a `_compute_<tradition>_chart(data)` function in `astro_engine.py`
2. Add it to the `systems` enum
3. Create `skills/astrology/references/<tradition>.md` (1-5 KB, MIT-licensed original)
4. Add the `get_<tradition>_chart` tool to `mcp_server.py`
5. Add a new section to `SKILL.md` explaining when the model should reach for it

## Reporting issues

- **Bug** → use the bug template
- **Feature** → use the feature template
- **Question** → use the question template (or open a discussion)
- **Security** → see [SECURITY.md](SECURITY.md); **do not file a public issue**

## Release process

Maintainers cut a release by:

1. Bumping `VERSION` in `api.py` and the `version` field in `openapi.yaml`
2. Moving the "Unreleased" section of `CHANGELOG.md` into a dated version
3. Tagging: `git tag -s vX.Y.Z -m "vX.Y.Z"` and `git push --tags`
4. The CI workflow publishes the Docker image to GHCR automatically
