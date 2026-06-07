# Synastry, Forecasting & Auspicious Timing

Covers the three most-monetised, most-asked request types: **compatibility**,
**"what's happening to me now / this year"**, and **"when should I do X"**.

## A. Synastry (relationship compatibility) — `mode:"synastry"`
The engine compares two charts and returns `inter_aspects` (A's planets to B's planets),
weighted, plus a coarse `harmony_index`. **Read the aspects, not the index.**

What the contacts mean (the ones that matter most first):
- **Sun–Moon** (either direction) — the classic marriage aspect; deep mutual recognition, one shines, one nurtures.
- **Venus–Mars** — physical chemistry and attraction.
- **Moon–Moon / Moon–Venus** — emotional comfort, feeling "at home."
- **Sun–Sun, Sun–Ascendant** — sense of self meshes (or clashes).
- **Mercury–Mercury** — how you talk and think together.
- **Saturn–personal planet** — commitment and duty, but can feel heavy/restrictive; the glue *and* the friction.
- **Mars–Mars / Mars–Saturn squares** — where you fight.

Aspect quality: trine/sextile = ease; conjunction = intensity (great on benefics);
**square/opposition = friction that is not necessarily bad** — long relationships need
some square for charge and growth. A frictionless chart can be flat. Never deliver a
verdict of "incompatible"; describe the *texture* — where it flows, where it works, what
each person needs to understand about the other.

**Vedic compatibility (Ashtakoota / Guna Milan)** is the traditional Indian marriage
match (out of 36 points, via the two Moon-nakshatras); if asked for a kundli match,
note the engine gives nakshatras for both — you can describe the nakshatra
compatibility qualitatively and flag that a full 36-point Guna Milan is the formal
method. **BaZi compatibility** = match the two **Day Master elements** and useful gods
(does each supply what the other needs?), plus the zodiac-animal best/clash/harm.

Synthesise across systems: if Western synastry, Vedic nakshatra, and BaZi elements all
say "easy warmth but low friction," that convergence is your honest headline.

## B. Forecasting — transits & periods — `mode:"transit"`
For "why is my life like this right now?", yearly forecasts, "is this a good year":
- The engine returns the current sky's **aspects to the natal chart** (tightest first),
  the **life_phase** milestones (Saturn return, etc.), and current positions.
- **Slow-planet transits carry the story**: Saturn (~2.5 yr/sign) = where life gets
  serious/tested; Jupiter (~1 yr/sign) = where it expands/opens; Pluto/Uranus/Neptune =
  deep, years-long transformations. Mars transits = short, hot triggers.
- Cross-reference **Vedic dasha** (the active mahadasha/antardasha with dates) and the
  **BaZi current luck pillar + annual Tai Sui** for a three-system timeline. When they
  agree on a theme or a turning date, that's the trustworthy forecast.
- **Always name the end date.** "This pressure eases when Saturn leaves the square around
  March 2027" is the certainty people came for. Knowing *when it stops* is the relief.
- "Mercury retrograde" questions: check the engine's `retrograde` flags on current
  positions; frame as a review/redo/reconnect season, not catastrophe.

## C. Electional astrology — picking an auspicious date
For "when should I marry / launch / sign / move?":
1. Identify what the event needs (marriage → Venus/7th; business → Jupiter/2nd/10th & Mercury; surgery → avoid Moon on the body part).
2. Run `mode:"transit"` across candidate dates; favour days when benefics (Jupiter,
   Venus) support the relevant points and malefics (Saturn, Mars) don't afflict them,
   and avoid Mercury-retrograde windows for contracts/launches.
3. **Vedic muhurta**: traditionally avoid an afflicted Moon, prefer auspicious
   nakshatras (e.g. Pushya — the most auspicious — for most beginnings; Rohini, Hasta).
4. **BaZi date selection**: choose a day whose elements are **favourable** to the
   person's Day Master / useful god and that doesn't clash with their year animal.
Give 2–3 ranked options with the reason for each — not one mystical decree.

## D. Horary / Prasna (answering a specific question)
Classical horary casts a chart for the *moment a question is asked*. Lightweight version:
run `mode:"transit"` for now, read the Moon (the querent's flow) and the planet ruling
the matter, and answer the specific yes/when/how — while being honest that horary is the
most interpretive branch and you're giving guidance, not a guarantee.

Classic uses: "Will my missing item be found?" (Moon + 2nd house), "Will I get this job?"
(10th house lord's applying aspects to benefics), "Is my partner faithful?" (7th house lord
+ Venus aspects), "Should I buy this house?" (4th house lord's strength and Moon's phase).

**Prasna (Vedic horary)**: the querent's rising sign at the moment of asking is read exactly
like a natal chart. The Moon's nakshatra and the lagna lord's condition answer the question.

## E. Mundane & Event Charts (Q115 — nations, companies, elections)

Any moment of inception has a chart: a country's independence (e.g., India: Aug 15, 1947,
00:00 IST, New Delhi), a company's incorporation, a marriage ceremony, a product launch.
Cast it like a natal chart. The 1st = the entity's identity; 10th = its public standing;
7th = partners/adversaries; 2nd/8th = finances; 6th = employees and operational challenges.

**Elections**: compare both candidates' transits and dashas against the nation's natal chart.
Jupiter or Venus transiting the candidate's 10th/1st = public favour; Saturn to 10th = obstacle.
Frame as indicators, not predictions — mundane astrology has wide orbs of uncertainty.

**Market / financial**: Eclipse seasons + outer-planet ingresses (Jupiter entering a sign, Saturn
changing sign) mark economic turning points. Uranus in Gemini (2025–2033): communication/tech
disruption cycle. Track slow-planet sign changes for sector themes.

## The honest forecasting frame
Forecasts describe **weather and seasons**, giving the person time to prepare and agency
to act — never a fixed fate. The value is preparation and meaning, not prophecy.
