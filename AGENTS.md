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

### Agent Skills hosts (Codex, Cursor, Gemini, etc.)
```
npx skills add aryaminus/astro -g
```
(`-g` installs globally for your user, available across all projects. Drop it to scope per-project.)

### Claude Desktop, Cursor, Zed, Devin (MCP Protocol)
Configure your MCP client to spawn the server:
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
