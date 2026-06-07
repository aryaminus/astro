# Using Astro on Any AI Chat or Assistant

Works everywhere. Pick your platform.

## Option 1: One paste sets everything up (any chat, zero manual install)

Paste this as your **first message** on claude.ai, ChatGPT, Gemini, Claude Code, Cursor, Codex, DeepSeek, Qwen, Perplexity, Grok, or any LLM. It tells the AI to install Astro itself by whatever means it has (shell, MCP/API, or just the web) and degrades gracefully if it can't — so you never have to set anything up by hand:

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

| Platform | Where to paste |
|----------|---------------|
| **claude.ai** | New chat → paste. Or create a Project with this as Custom Instructions. |
| **ChatGPT** | New chat → paste. Or create a Custom GPT with this as System Instructions + [`openapi.yaml`](https://github.com/aryaminus/astro/raw/main/openapi.yaml) as an Action. |
| **Gemini** | New chat → paste. Gems save it persistently. |
| **DeepSeek / Qwen / Perplexity / Grok** | New chat → paste. |

## Option 2: Poke (Apple Messages, WhatsApp, Telegram, RCS)

Astro runs as an MCP server that Poke connects to. You need a deployed instance first.

### Deploy the MCP server

One-click to Render (free tier): connect [aryaminus/astro](https://github.com/aryaminus/astro) → New → Blueprint. This gives you a public URL like `https://astro-api-xxxx.onrender.com`.

Or self-host:
```bash
docker compose up --build
# MCP over SSE on port 8765:
ASTRO_MCP_TRANSPORT=sse python -m skills.astrology.scripts.mcp_server
```

### Add to Poke

**Via web app:**
1. Go to [poke.com/integrations/new](https://poke.com/integrations/new)
2. Name: `Astro`
3. MCP Server URL: `https://your-render-url.onrender.com/sse`
4. Click **Create Integration**

**Via CLI:**
```bash
npx poke@latest mcp add https://your-render-url.onrender.com/sse -n "Astro"
```

### Create a Poke Recipe (shareable)

```bash
npx poke@latest tunnel http://localhost:8765/sse -n "Astro" --recipe
```

Or in [Kitchen](https://poke.com/kitchen):
1. Create recipe → name it "Astrology"
2. Onboarding context: `Your birth date (year/month/day), birth time, and birth city`
3. Prefilled first message: `I'd like an astrology reading. Ask me for my birth details.`
4. Add the Astro MCP integration
5. Publish → share the link

### Use it

Once connected, message Poke:
- *"What's my birth chart?"*
- *"Am I compatible with someone born March 22, 1985?"*
- *"When's my next Saturn return?"*
- *"What does today have in store for me?"*

Poke calls the Astro MCP server's 18 tools to compute real positions, then interprets the results.

## Option 3: Upload the skill file (claude.ai)

1. Download [`astrology.skill`](https://github.com/aryaminus/astro/releases/latest/download/astrology.skill)
2. Go to [Customize → Skills](https://claude.ai/customize/skills)
3. Click **+** → drop the file in
4. Done.

## Option 4: Create a persistent Project (claude.ai)

1. **Projects** → **New Project** → "Astrology"
2. Paste the copy-paste prompt from Option 1 as **Custom Instructions**
3. Upload reference files as knowledge base:
   - [`western.md`](https://raw.githubusercontent.com/aryaminus/astro/main/skills/astrology/references/western.md) · [`vedic.md`](https://raw.githubusercontent.com/aryaminus/astro/main/skills/astrology/references/vedic.md) · [`bazi.md`](https://raw.githubusercontent.com/aryaminus/astro/main/skills/astrology/references/bazi.md) · [`synastry-and-timing.md`](https://raw.githubusercontent.com/aryaminus/astro/main/skills/astrology/references/synastry-and-timing.md) · [`consultation.md`](https://raw.githubusercontent.com/aryaminus/astro/main/skills/astrology/references/consultation.md) · [`health.md`](https://raw.githubusercontent.com/aryaminus/astro/main/skills/astrology/references/health.md) · [`specialty-systems.md`](https://raw.githubusercontent.com/aryaminus/astro/main/skills/astrology/references/specialty-systems.md) · [`tibetan.md`](https://raw.githubusercontent.com/aryaminus/astro/main/skills/astrology/references/tibetan.md)

## Option 5: Local install (best experience)

```bash
npx skills add aryaminus/astro -g
```

Full deterministic engine — 19 modes, 3 traditions, real positions computed locally. Works on Claude Code, Cursor, Codex, Copilot, Gemini CLI, and 50+ agent hosts. See [README](../README.md) for all install methods.

## Option 6: ChatGPT Custom GPT with Actions

1. Create a Custom GPT
2. Paste the copy-paste prompt as **System Instructions**
3. Under **Actions**, import: `https://raw.githubusercontent.com/aryaminus/astro/main/openapi.yaml`
4. Set server URL to your hosted instance
5. Save.
