# Western Tropical — interpretation ruleset

Tropical zodiac (tied to the seasons), psychological/archetypal focus. The engine
returns planets with `sign`, `deg_in_sign`, `house`, `retrograde`, `dignity`, plus
houses, aspects, and element/modality balance. Read it in this order.

## 1. The Big Three (start here, always)
- **Sun** = core identity, conscious will, what you're growing *into*. The sign's element/modality is the engine of the personality.
- **Moon** = emotional nature, instinct, what you need to feel safe, the inner child and the mother.
- **Rising / Ascendant** = the mask, the body, first impressions, the lens you meet life through. Sets the whole house framework.

A person is the **dialogue** between these three. Sun in fiery Aries with Moon in
watery Cancer and Libra rising = a warrior who needs emotional safety and presents as
a diplomat. Name that negotiation.

## 2. Planets = the cast
| Planet | Archetype | Reads as |
| --- | --- | --- |
| Mercury | mind, voice | how you think, learn, speak (check if near Sun = combust/intense) |
| Venus | love, value | what you find beautiful, how you love and attract, money taste |
| Mars | drive, anger | how you act, fight, desire; your raw engine |
| Jupiter | expansion, luck | where you grow, your faith, your excess |
| Saturn | discipline, fear | where you're tested, mature slowly, build mastery through limitation |
| Uranus | disruption | where you're a rebel/genius, sudden change (generational) |
| Neptune | dreams, dissolution | where you idealise, escape, or attune spiritually (generational) |
| Pluto | power, rebirth | where you transform through crisis and confront the shadow (generational) |
| N/S Node | growth axis | North = unfamiliar growth edge; South = innate gift to release |

## 3. Sign qualities
- **Elements**: Fire (spirit/action), Earth (matter/practicality), Air (mind/relation), Water (emotion/intuition). The engine gives the element & modality balance — a chart lacking an element craves it; an over-loaded element runs the show.
- **Modalities**: Cardinal (initiates), Fixed (sustains/resists), Mutable (adapts/scatters).
- Each sign's keywords (incl. the shadow) are in the engine's data and `SIGN_DATA`.

## 4. Houses (life arenas) — engine uses whole-sign
A planet's **house** says *where in life* its energy plays out (1=self, 2=money,
7=partners, 10=career… full list in engine `HOUSE_MEANINGS`). Sign = *how*; house =
*where*. The ruler of each house's sign links arenas together (e.g. 2nd-house ruler in
the 9th = money through travel/teaching/publishing).

## 5. Aspects = the wiring (the chart's drama)
Engine returns aspects sorted by tightness (smaller orb = stronger). Read the tightest
3–5 first; they define the person.
- **Conjunction (0°)** — fusion; the two planets act as one.
- **Trine (120°) / Sextile (60°)** — ease, talent, flow (trine can be lazy; sextile needs effort to cash in).
- **Square (90°)** — friction that *drives*; the chart's growth engine, felt as inner conflict.
- **Opposition (180°)** — a see-saw, usually projected onto other people until owned.
- **Quincunx (150°)** — chronic awkward adjustment between unrelated drives.

Synthesise aspects, don't list them: a Sun–Saturn square is "you had to earn your own
authority the hard way, and you're harder on yourself than anyone."

## 6. Dignity (a planet's strength)
The engine tags `domicile/rulership`, `exalted`, `detriment`, `fall`. A planet in
domicile or exalted acts cleanly and strongly; in detriment/fall it's strained and
needs conscious work. Mention it when it sharpens the read.

## 7. Retrogrades
Natal retrograde (engine `retrograde:true`) = that planet's energy turns *inward* /
reworks itself (Mercury Rx: thinks before speaks, non-linear mind). Not "bad."

## 8. Timing — transits & the great cycles (use `mode:"transit"`)
- **Saturn Return (~age 29, 58)** — the structural reckoning; adulthood demands you build what lasts. The single most-asked-about transit.
- **Jupiter Return (~every 12 yrs)** — a door of growth/opportunity opens.
- **Uranus Opposition (~age 40–42)** — the "mid-life" awakening: authenticity vs. the built life.
- **Nodal Return (~18.6, 37, 56)** — karmic re-orientation of direction & relationships.
- Transiting **Saturn/Jupiter/Pluto** aspects to natal planets time the major chapters; the engine lists the tightest. Always name **when a hard transit eases** — that timeline is the relief people came for.

## Reading recipe
1. State the Big Three as a living negotiation.
2. Name the dominant element/modality and what it makes the person *do*.
3. Pull the 2–3 tightest aspects → the central paradox.
4. Locate it in houses (which life arenas light up).
5. If timing was asked: overlay current transits + the cycle they're in.
6. End with the growth edge (North Node) and one concrete action.
