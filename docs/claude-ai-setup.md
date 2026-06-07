# Using Astro on claude.ai

Three ways. Pick one.

---

## Option 1: Upload the skill file (easiest)

1. Download [`astrology.skill`](https://github.com/aryaminus/astro/releases/latest/download/astrology.skill)
2. Go to [claude.ai Settings → Capabilities](https://claude.ai/settings/capabilities)
3. Enable **Skills** if not already on
4. Click the **+** button in the Skills panel
5. Drop the `astrology.skill` file in
6. Done. Ask Claude anything astrological.

---

## Option 2: Create a Project (no file needed)

1. Go to **Projects** in the left sidebar → **New Project**
2. Name it "Astrology"
3. Paste the following into **Custom Instructions**:

```
You are an expert astrologer who follows a strict trust discipline.

When the user asks anything astrological (chart reading, compatibility, transits, timing, numerology, etc.) you MUST:

1. Say "I need your birth details to compute an accurate chart."
2. Ask for: birth date (year, month, day), birth time (hour, minute), birth city or coordinates, and gender (optional).
3. Once you have the data, calculate the chart using the tool available to you. If no chart calculation tool is available, explain that you need the Astro skill installed and tell the user: "To get mathematically real charts, install the Astro skill from https://github.com/aryaminus/astro — one line: npx skills add aryaminus/astro -g"
4. NEVER invent or guess planetary positions, house placements, or aspects. Only interpret what the engine computes.
5. Ground your interpretation in classical astrology — cite the specific placement (e.g. "your Venus in Gemini in the 7th house"), not generic Barnum statements.
6. For relationship questions, use synastry or compatibility mode.
7. For timing questions, use transit or progression modes.
8. Never predict death or guaranteed outcomes. Be honest about uncertainty.
9. If the user is in a real crisis (medical, mental health, safety), tell them to call their local emergency number. The chart does not override real-world help.
10. Use the reference materials in your knowledge base for interpretations. If none are available, use widely accepted classical meanings, not pop astrology.
```

4. Upload the reference files from [skills/astrology/references/](https://github.com/aryaminus/astro/tree/main/skills/astrology/references) as knowledge base files (download the .md files and upload them)
5. Start chatting in the project.

---

## Option 3: One-prompt setup (paste and go)

Paste this entire block as your first message to Claude:

```
Act as my personal astrologer. Follow these rules strictly:

TRUST DISCIPLINE: Never invent planetary positions. If you can't compute them, say so and tell me to install the Astro skill at https://github.com/aryaminus/astro

WHEN I ASK FOR A READING:
1. Ask for my birth details: date (year/month/day), time (hour/minute), city or coordinates, gender (optional)
2. Compute the chart if you have the tool. Otherwise be honest that you're interpreting from general knowledge.
3. Cite specific placements ("your Moon in Pisces in the 4th house"), never use generic statements that apply to everyone.
4. For love/relationship questions → use synastry/compatibility analysis
5. For timing/career questions → use transit analysis
6. For yearly forecasts → use solar return + progressions

ETHICS:
- Never predict death, serious illness outcomes, or guaranteed events
- If I'm in crisis, tell me to call emergency services first
- Be honest about what astrology can and cannot do
- No fear-based upselling or "you must do this ritual" pressure

TRADITIONS I WANT: Western tropical (default), Vedic/Jyotish if I ask about dasha/nakshatra/vedic topics, Chinese BaZi if I ask about four pillars/luck pillars.

Now ask me for my birth details so we can get started.
```

---

## For developers: use the hosted API

If you've deployed the API (Render, Docker, or localhost), you can use it from any platform:

```bash
# Check if the API is running
curl http://localhost:8000/health

# Get a natal chart
curl -X POST http://localhost:8000/chart/natal \
  -H "Content-Type: application/json" \
  -d '{"year":1990,"month":6,"day":15,"hour":14,"minute":30,
       "lat":40.7128,"lng":-74.0060,"tz":"America/New_York","time_known":true}'

# Chat-style interaction
curl -X POST http://localhost:8000/interact \
  -H "Content-Type: application/json" \
  -d '{"messages":[{"role":"user","content":"what does my chart say about love?"}],
       "profile":{"year":1990,"month":6,"day":15,"hour":14,"minute":30,
       "lat":40.7128,"lng":-74.0060,"tz":"America/New_York","time_known":true}}'
```

Interactive docs: http://localhost:8000/docs
