# Astro — Multi-Tradition Astrology Engine for AI Agents

> Trustworthy birth charts, transits, and synastry across Western, Vedic/Jyotish, and Chinese BaZi. The engine computes; the model interprets.

[![MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![MCP](https://img.shields.io/badge/MCP-18_tools-blueviolet)](https://modelcontextprotocol.io)
[![REST](https://img.shields.io/badge/REST-31_endpoints-orange)](openapi.yaml)
[![Deploy](https://img.shields.io/badge/Deploy-Render-46a2f1)](render.yaml)

---

**Paste this into any AI chat or agent (Claude, ChatGPT, Gemini, Claude Code, Cursor, Codex, DeepSeek, Perplexity…). It installs Astro itself — you don't set anything up first:**

```
You are my personal astrologer powered by Astro, an open-source multi-tradition astrology engine that computes mathematically real charts instead of guessing: https://github.com/aryaminus/astro

SET YOURSELF UP now using whatever you're capable of — try in this order, don't ask me first:
1. If you can run shell/terminal commands, get the pure-Python engine (zero dependencies — no pip install) by ANY of these, then call `python3 <path>/astro_engine.py --json '{...}'`:
   - `npx skills add aryaminus/astro -g` — installs the skill on Claude Code, Cursor, Codex, Gemini CLI + 50+ hosts (engine at skills/astrology/scripts/astro_engine.py)
   - latest packaged release, needs only curl + tar (no npm/git): `curl -L -o astrology.skill https://github.com/aryaminus/astro/releases/latest/download/astrology.skill && tar xzf astrology.skill` — engine then at scripts/astro_engine.py
   - `git clone https://github.com/aryaminus/astro` — engine at skills/astrology/scripts/astro_engine.py
2. If you already have an Astro MCP server or REST API connected, use those tools to compute charts.
3. If you can only browse the web: read the canonical spec and follow it as your operating instructions — https://raw.githubusercontent.com/aryaminus/astro/main/skills/astrology/SKILL.md — and fetch the classical reference rulesets it links (western, vedic, bazi, synastry-and-timing, consultation) from https://github.com/aryaminus/astro/tree/main/skills/astrology/references
4. If you can't do any of the above: tell me in one line how to install it (`npx skills add aryaminus/astro -g`, or download the skill from https://github.com/aryaminus/astro/releases/latest for claude.ai), then proceed by interpreting from classical reference and state clearly that you are NOT computing real positions.

THEN behave exactly as Astro's SKILL.md defines:
- COMPUTE the real chart before interpreting — NEVER invent a planetary position, house, or aspect. If no compute path worked, say so honestly.
- CITE specific placements ("your Moon in Pisces in the 4th house"); never generic statements true of everyone.
- ROUTE by question: love → synastry/compatibility; timing/career → transits; year ahead → solar return + progressions; where to live → astrocartography; auspicious dates → electional + panchang.
- TRADITIONS: Western tropical by default; Vedic (dasha/nakshatra) when I ask; Chinese BaZi (four pillars) when I ask.
- ETHICS: never predict death or guaranteed doom; give me agency; if I'm in crisis, point me to real emergency help first.

Now ask me for my birth details (date — and ideally exact time + city) and let's begin.
```

**Local install — works on Claude Code, Cursor, Codex, Copilot, Gemini CLI, and 50+ [Agent Skills](https://agentskills.io) hosts:**

```
npx skills add aryaminus/astro -g
```

| Host | Install | Update |
|------|---------|--------|
| **Claude Code** | `/plugin marketplace add aryaminus/astro` then `/plugin install astrology` | Auto via marketplace |
| **Codex, Cursor, Copilot, Gemini CLI, 50+ hosts** | `npx skills add aryaminus/astro -g` | `npx skills update astrology -g` |
| **claude.ai** | [Download `.skill`](https://github.com/aryaminus/astro/releases/latest/download/astrology.skill) → [Customize → Skills](https://claude.ai/customize/skills) → + | Re-download |
| **ChatGPT** | Copy [`openapi.yaml`](openapi.yaml) into Custom GPT → Actions → Import | Manual |
| **Poke** (Messages/WhatsApp/Telegram) | [Add as MCP integration](https://poke.com/integrations/new) → URL: `https://your-render-url.onrender.com/sse` | — |
| **Claude Desktop / Zed** | `npx @smithery/cli install astrology --client claude` | Re-run |
| **Manual / dev** | `git clone https://github.com/aryaminus/astro.git && ln -sfn "$(pwd)/astro/skills/astrology" ~/.agents/skills/astrology` | `git pull` |

---

## Why this exists

A raw LLM cannot tell you where Mars was on a Tuesday in 1997 — it hallucinates chart data. Astro splits the work:

1. **Engine** — deterministic Python math computes real sky positions (zero deps, pure stdlib)
2. **Skill** — orchestrates the engine + loads classical interpretation rulesets
3. **Glue** — MCP, REST, CLI, ChatGPT Actions reach the engine from any platform

The model never guesses a position. It interprets structured output grounded in 8 classical rulesets.

## 19 modes · 3 traditions · zero dependencies

**Modes:** natal, transit, synastry, compatibility, composite, astrocartography, horary, event, solar/lunar/planetary return, navamsa, varga (D2–D60), panchang, moon phase, numerology, progressions, planetary hours, transit-to-natal aspects. Full list and parameters in [`skills/astrology/SKILL.md`](skills/astrology/SKILL.md).

**Traditions:** Western tropical, Vedic/Jyotisha (Lahiri sidereal), Chinese BaZi + Tibetan/Buddhist.

**Auto-included in every natal chart:** Aspect patterns (Grand Trine, Kite, T-Square, Grand Cross, Yod, Mystic Rectangle, Stellium) · Part of Fortune · Vertex · Black Moon Lilith · Moon phase · 10 Arabic Parts · 23 fixed-star conjunctions · Navamsa D9 · Panchang · Mangal Dosha · Kaalsarpa Dosha.

## Try it

After installing, ask any of these:

- *"What's my chart?"* → full natal
- *"Am I compatible with…?"* → synastry + 0–100 scoring
- *"When's my Saturn return?"* → planetary return + timing
- *"Where should I live for career?"* → astrocartography
- *"What time should I start the meeting?"* → Chaldean planetary hours
- *"Pick an auspicious wedding date"* → electional + panchang
- *"Should I have surgery this month?"* → medical timing
- *"What does today have in store?"* → transits + natal aspects

## Project layout

```
astro/
├── skills/astrology/
│   ├── SKILL.md                    # runtime spec the model reads
│   ├── scripts/astro_engine.py     # deterministic engine (~2930 lines)
│   ├── scripts/mcp_server.py       # MCP wrapper (18 tools, stdio + SSE)
│   ├── scripts/api.py              # REST API (31 endpoints)
│   └── references/                 # 8 classical rulesets
│       ├── western.md · vedic.md · bazi.md · tibetan.md
│       ├── health.md · synastry-and-timing.md
│       ├── specialty-systems.md · consultation.md
├── openapi.yaml                    # OpenAPI 3.1 (ChatGPT, Agentforce, Coze)
├── smithery.yaml                   # Smithery registry
├── Dockerfile · docker-compose.yml · render.yaml   # cloud deploy
└── AGENTS.md · CONTRIBUTING.md · SECURITY.md · CHANGELOG.md
```

## Cloud hosting

**Free by default.** No auth, no rate limits. Set `ASTRO_API_KEY` to gate, `ASTRO_RATE_LIMIT` to throttle.

**Render (one-click, free tier):** Connect this repo → New → Blueprint. `render.yaml` provisions everything and gives you a public URL like `https://<your-app>.onrender.com`. Verify with `curl https://<your-app>.onrender.com/health`.

**Docker:**
```bash
docker compose up --build    # API on :8000, docs at /docs
```

**Raw Python:**
```bash
pip install -r requirements.txt
uvicorn skills.astrology.scripts.api:app --host 0.0.0.0 --port 8000
```

**MCP over SSE (Smithery, Cloudflare):**
```bash
ASTRO_MCP_TRANSPORT=sse python -m skills.astrology.scripts.mcp_server
```

Env vars and operational endpoints documented in [`AGENTS.md`](AGENTS.md).

## Documentation

| File | What it covers |
|------|---------------|
| [`AGENTS.md`](AGENTS.md) | Install methods, env vars, cloud config, MCP tools list |
| [`docs/cloud-setup.md`](docs/cloud-setup.md) | Using Astro on any AI chat (Claude, ChatGPT, Gemini, DeepSeek, Qwen) |
| [`skills/astrology/SKILL.md`](skills/astrology/SKILL.md) | Runtime spec, mode parameters, trust discipline |
| [`skills/astrology/README.md`](skills/astrology/README.md) | Engine internals, API surface, specialty branches |
| [`openapi.yaml`](openapi.yaml) | REST API schema (ChatGPT, Agentforce, Coze) |
| [`CHANGELOG.md`](CHANGELOG.md) | Release history |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | Hard rules, dev workflow, PR checklist |
| [`SECURITY.md`](SECURITY.md) | Vulnerability reporting |

## Contributing

PRs welcome. Hard rules: engine stays zero-dep, engine never imports frameworks, touch all 4 surfaces (engine + MCP + REST + OpenAPI), the skill is honest. See [`CONTRIBUTING.md`](CONTRIBUTING.md).

## License

[MIT](LICENSE). Reference texts in `skills/astrology/references/` are original MIT-licensed syntheses of classical sources.
