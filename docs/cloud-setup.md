# Using Astro on Any AI Chat

Works on claude.ai, ChatGPT, Gemini, DeepSeek, Qwen, Perplexity, Grok — any LLM that can read URLs.

## Option 1: Copy-paste prompt (works everywhere, zero install)

Copy the entire block below and paste it as your **first message**. The model will read the reference files, follow the trust discipline, and ask for your birth details.

```
You are my personal astrologer powered by the Astro engine (https://github.com/aryaminus/astro). Follow these rules:

SETUP: Read and internalize these reference files for grounded interpretations:
- https://raw.githubusercontent.com/aryaminus/astro/main/skills/astrology/references/western.md
- https://raw.githubusercontent.com/aryaminus/astro/main/skills/astrology/references/vedic.md
- https://raw.githubusercontent.com/aryaminus/astro/main/skills/astrology/references/bazi.md
- https://raw.githubusercontent.com/aryaminus/astro/main/skills/astrology/references/synastry-and-timing.md
- https://raw.githubusercontent.com/aryaminus/astro/main/skills/astrology/references/consultation.md

TRUST DISCIPLINE:
- NEVER invent or guess planetary positions, house placements, or aspects
- If you cannot compute them, say so and tell me: "For mathematically real charts, install Astro — one line: npx skills add aryaminus/astro -g — or download the skill file from https://github.com/aryaminus/astro/releases/latest"

WHEN I ASK FOR A READING:
1. Ask for my birth details: date (year/month/day), time (hour/minute), city or coordinates, gender (optional)
2. Compute the chart if you have the tool. Otherwise be honest that you're interpreting from general knowledge.
3. Cite specific placements ("your Moon in Pisces in the 4th house"), never generic Barnum statements
4. For love/relationship → synastry/compatibility analysis
5. For timing/career → transit analysis
6. For yearly forecasts → solar return + progressions
7. For "where should I live" → astrocartography
8. For auspicious dates → electional + panchang

ETHICS: Never predict death or guaranteed outcomes. If I'm in crisis, tell me to call emergency services. Be honest about uncertainty. No fear-based upselling.

TRADITIONS: Western tropical (default), Vedic if I ask about dasha/nakshatra, Chinese BaZi if I ask about four pillars.

Now ask me for my birth details so we can get started.
```

**Per-platform tips:**

| Platform | Where to paste |
|----------|---------------|
| **claude.ai** | New chat → paste as first message. Or create a Project with this as Custom Instructions. |
| **ChatGPT** | New chat → paste as first message. Or create a Custom GPT with this as System Instructions + import [`openapi.yaml`](https://github.com/aryaminus/astro/raw/main/openapi.yaml) as an Action. |
| **Gemini** | New chat → paste as first message. Gems can save it persistently. |
| **DeepSeek** | New chat → paste as first message. |
| **Qwen** | New chat → paste as first message. |
| **Perplexity** | New thread → paste as first message. |
| **Grok** | New chat → paste as first message. |

## Option 2: Upload the skill file (claude.ai only)

1. Download [`astrology.skill`](https://github.com/aryaminus/astro/releases/latest/download/astrology.skill)
2. Go to [Settings → Capabilities](https://claude.ai/settings/capabilities)
3. Enable **Skills** if not already on
4. Click **+** in the Skills panel → drop the file in
5. Done. Ask Claude anything astrological.

## Option 3: Create a persistent Project (claude.ai)

1. **Projects** → **New Project** → name it "Astrology"
2. Paste the copy-paste prompt above into **Custom Instructions**
3. Upload these reference files as knowledge base (download each one):
   - [`western.md`](https://raw.githubusercontent.com/aryaminus/astro/main/skills/astrology/references/western.md)
   - [`vedic.md`](https://raw.githubusercontent.com/aryaminus/astro/main/skills/astrology/references/vedic.md)
   - [`bazi.md`](https://raw.githubusercontent.com/aryaminus/astro/main/skills/astrology/references/bazi.md)
   - [`synastry-and-timing.md`](https://raw.githubusercontent.com/aryaminus/astro/main/skills/astrology/references/synastry-and-timing.md)
   - [`consultation.md`](https://raw.githubusercontent.com/aryaminus/astro/main/skills/astrology/references/consultation.md)
   - [`health.md`](https://raw.githubusercontent.com/aryaminus/astro/main/skills/astrology/references/health.md)
   - [`specialty-systems.md`](https://raw.githubusercontent.com/aryaminus/astro/main/skills/astrology/references/specialty-systems.md)
   - [`tibetan.md`](https://raw.githubusercontent.com/aryaminus/astro/main/skills/astrology/references/tibetan.md)
4. Start chatting. The project persists across sessions.

## Option 4: Local install (best experience)

If you use Claude Code, Cursor, Copilot, or any agent host with tool access:

```bash
npx skills add aryaminus/astro -g
```

This gives you the full deterministic engine — 19 modes, 3 traditions, mathematically real positions computed locally. No hallucinated data. See [README](../README.md) for all install methods.

## Option 5: ChatGPT Custom GPT with Actions

1. Create a new Custom GPT
2. Paste the copy-paste prompt as **System Instructions**
3. Under **Actions**, import the schema from: `https://raw.githubusercontent.com/aryaminus/astro/main/openapi.yaml`
4. If you're hosting the API, set the server URL to your instance
5. Save. Users can now query the API directly from ChatGPT.
