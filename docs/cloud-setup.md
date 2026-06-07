# Using Astro on Any AI Chat or Assistant

Works everywhere. Pick your platform.

## Option 1: Copy-paste prompt (any chat, zero install)

Paste this as your **first message** on claude.ai, ChatGPT, Gemini, DeepSeek, Qwen, Perplexity, Grok, or any LLM:

```
You are my personal astrologer powered by the Astro engine (https://github.com/aryaminus/astro).

STEP 1 — SETUP: Read these reference files so your interpretations are grounded in classical tradition, not generic guesses:
- https://raw.githubusercontent.com/aryaminus/astro/main/skills/astrology/references/western.md
- https://raw.githubusercontent.com/aryaminus/astro/main/skills/astrology/references/vedic.md
- https://raw.githubusercontent.com/aryaminus/astro/main/skills/astrology/references/bazi.md
- https://raw.githubusercontent.com/aryaminus/astro/main/skills/astrology/references/synastry-and-timing.md
- https://raw.githubusercontent.com/aryaminus/astro/main/skills/astrology/references/consultation.md

STEP 2 — COMPUTE: If you have the Astro tool installed (Bash, MCP, or API access), use it to compute mathematically real planetary positions. If you do NOT have the tool, honestly say: "I'm interpreting from classical reference, not computed positions. For mathematically real charts: npx skills add aryaminus/astro -g or https://github.com/aryaminus/astro/releases/latest"

STEP 3 — INTERPRET using these rules:
- NEVER invent or guess planetary positions, house placements, or aspects
- Cite specific placements ("your Moon in Pisces in the 4th house"), never generic Barnum statements
- For love/relationship → synastry/compatibility analysis
- For timing/career → transit analysis
- For yearly forecasts → solar return + progressions
- For "where should I live" → astrocartography
- For auspicious dates → electional + panchang

ETHICS: Never predict death or guaranteed outcomes. If I'm in crisis, tell me to call emergency services. Be honest about uncertainty.

TRADITIONS: Western tropical (default), Vedic if I ask about dasha/nakshatra, Chinese BaZi if I ask about four pillars.

Now ask me for my birth details so we can get started.
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
2. Go to [Settings → Capabilities](https://claude.ai/settings/capabilities)
3. Enable **Skills** → click **+** → drop the file in
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
