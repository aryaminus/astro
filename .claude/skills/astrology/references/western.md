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
| **Chiron** | wounded healer | your deepest wound (the sign/house it's in) that becomes your greatest teacher — the gift emerges *through* the wound, not despite it |

**Chiron in brief** — Chiron transits one sign every 2–8 years (very eccentric orbit; fastest near Virgo/Libra, slowest near Pisces/Aries). Its natal sign describes the *wound-theme* of a generation; its natal **house** personalises which life arena the wound plays out. Chiron in a natal chart is often most powerful when a transit or progressed planet makes a hard aspect to it. The classic Chiron reading: the house it occupies is where the person *cannot help others most powerfully* — because it's where they bled first.

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

## 9. Health in the Western chart
Health questions map to the **6th house** (chronic habits, daily body maintenance), **1st house/Ascendant** (vitality, constitution), and **8th house** (crises, surgery, transformation). Specific indicators:
- **Saturn** in the 6th or afflicting the Ascendant ruler → chronic conditions, structural/skeletal issues, need for discipline in body maintenance.
- **Mars** in the 6th or 8th → inflammation, fever, accidents; read the sign for which body system (Aries=head, Taurus=throat, etc.).
- **Chiron's house** → the arena where chronic wounding lives (often psychosomatic); also the theme the person eventually heals *in others*.
- **12th house** → hidden health undermines; hospitals, immune/sleep issues.
- Always name the **path through** (concrete habits that help) — never predict disease as a fixed outcome.

## Reading recipe
1. State the Big Three as a living negotiation.
2. Name the dominant element/modality and what it makes the person *do*.
3. Pull the 2–3 tightest aspects → the central paradox.
4. Locate it in houses (which life arenas light up).
5. If timing was asked: overlay current transits + the cycle they're in.
6. End with the growth edge (North Node) and one concrete action.
7. **Health reading**: map to 1st/6th/8th/12th, name the Saturn/Mars/Chiron indicators, give the constructive habit — never the diagnosis.
