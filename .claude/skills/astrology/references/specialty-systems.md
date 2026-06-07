# Specialty & Niche Branches — the secondary layer

Beyond the core reading of a natal chart, every tradition has a long tail of
specialised branches — the questions a long-time client brings once the basics
have been covered. This file is the playbook for those questions. It pairs
with the engine's extra modes (`astrocartography`, `horary`, `event`) and
its specialty lookups (`namakaran`, `anatomy_chart`).

Rule that governs every section here: **always cite the computed placement**.
The specialty branches are the most tempting to free-associate on. Resist.

---

## 1. Astrocartography & relocation (engine `mode:"astrocartography"`)

**The question it answers:** *"Where in the world should I live for love / career
/ health / to find my 'Venus line' / to escape a hard Saturn placement?"*

### How it works
At the exact moment of your birth, the planets were in specific positions
relative to the **celestial sphere**. If you project that sphere onto the
Earth's surface (by drawing lines through where each planet was rising,
culminating, setting, or on the nadir), you get four "lines" per planet:

- **MC line** (planet on the Midheaven / highest point) → career, public role, what the world sees
- **IC line** (planet on the Imum Coeli / deepest point) → home, roots, ancestry, private foundation
- **ASC line** (planet on the Ascendant / eastern horizon) → body, identity, vitality, how you meet life
- **DSC line** (planet on the Descendant / western horizon) → partnerships, the "other," the mirror

Living on or near a planet line tends to **activate that planet's themes**.
The engine returns the **longitude of each line**; reference cities on each
line come from the built-in `CITIES` table.

### How to read it
- **Jupiter / Venus / Sun lines** → generally beneficial (growth, love, visibility)
- **Saturn / Pluto / Chiron / South Node lines** → demanding, karmic, transformative
- **Mars lines** → energy, drive, friction, accidents — useful for athletes, hazardous for sensitive souls
- **Uranus / Neptune lines** → awakening, artistic, unstable, "I came here and my life changed"
- **North Node line** → the soul's growth direction; moving there often feels like "I can finally breathe"
- **ASC + IC** for the place of birth → you feel "native"; **MC + ASC** for career cities

### The honest frame
Astrocartography is a *tendency*, not a verdict. The engine reports the math;
the agent interprets. The classic mistake: "Saturn line bad → avoid" — many
people thrive on Saturn lines (they need structure to do their best work).
Frame each line as **what it asks of you**, not a binary good/bad.

### The Twin Problem (a note)
Astrologers note that many people flourish in cities *opposite* their birth
longitude. The DS line of the Sun, the IC line of the Moon, the ASC line of
Jupiter — these are often "where I become who I was always meant to be." Use
the engine's output to surface non-obvious lines for the client.

---

## 2. Horary / Prasna — chart of the moment (engine `mode:"horary"`)

**The questions it answers:** *"Will my ex come back? Where did I lose my ring?
Is the rumor about my boss true? Should I sign this contract today?"*

### The classical method
Cast a chart for the **exact moment a question is asked**, at the place where
it's asked. The chart is interpreted with a tight set of rules:

- **Ascendant** = the querent (the person asking)
- **Ascendant ruler** = the querent's proxy through events
- **Moon** = the flow of the matter, common people, daily events
- **House ruling the matter** = the question's domain:
  - 1 self · 2 money/possessions · 3 messages, siblings, short travel
  - 4 home, land, property, the end of a matter
  - 5 children, romance, creativity, speculation
  - 6 illness, small animals, servants, debt
  - 7 spouse, partner, open enemies, the querent in any 1:1 contest
  - 8 death, transformation, others' money, sex
  - 9 foreign travel, law, higher learning, the guru
  - 10 career, status, the boss, the mother (in some traditions)
  - 11 friends, groups, hopes, gains
  - 12 hidden enemies, secrets, hospitals, the unconscious
- **Ruler of that house** = the answer's actor
- **Aspects to Moon and the Ascendant ruler** = timing

### Critical signals the engine returns
- **Void-of-course Moon** (Moon makes no further major aspect before leaving
  its sign) → classical: *"Nothing will come of the matter."* Don't act on
  a question with VoC Moon — wait and re-ask later.
- **Day vs. night chart** (Sun above/below horizon) → Sun is stronger in a
  day chart; Moon is stronger at night. Affects which planets are reliable.
- **Planetary hour ruler** (the planet ruling the Chaldean hour the question
  is asked) → the *flavour* of the moment and the timing of the answer.
- **Retrograde planets in the chart** → the matter may go backwards, return,
  or need to be re-done.

### The honest frame
Horary is the **most interpretive** branch. The engine returns the chart and
the classical signals; the agent reads them through the specific question.
The agent must (a) identify the house the question belongs to, (b) check VoC
Moon first (it overrides everything), (c) read the planetary hour ruler for
flavour, (d) read the Ascendant ruler and the relevant house ruler for the
answer. Never assert certainty — frame as "the chart suggests…"

### Lost objects (a horary speciality)
"Where did I lose it?" → 4th house rules the matter's end (where the object
rests). The **sign on the 4th** gives the **element** of the location:

- **Fire (Aries/Leo/Sagittarius)** → near heat (kitchen, fireplace), high places, east-facing rooms
- **Earth (Taurus/Virgo/Capricorn)** → on the ground, in storage, in soil or wood; low shelves
- **Air (Gemini/Libra/Aquarius)** → where air moves (windows, vents), on paper, in books
- **Water (Cancer/Scorpio/Pisces)** → near water (sink, bathroom), in containers, dark damp places

The **Moon's last aspect** before changing sign → which direction relative
to where you are now. This is the level of specificity the engine + agent
can offer; for the actual "it's in the upstairs bedroom closet" the querent
needs to walk through the space.

---

## 3. Electional astrology — picking the right day (also `synastry-and-timing.md`)

**The questions it answers:** *"When should I get married? Launch the business?
Sign the contract? Have the surgery? Send the email? Move house?"*

### Core rules (cross-tradition)
1. **Identify the house that rules the matter** (7=marriage, 10=career, 2/8=finance, 5=children/creativity).
2. **Find a day when the relevant planet is strong and unafflicted:**
   - Marriage → Venus, Jupiter, 7th house lord well-aspected
   - Business launch → Jupiter (expansion), Mercury (commerce), 10th house lord
   - Surgery → Moon NOT in the sign ruling the body part (see Medical below); avoid lunar eclipse
   - Contract signing → Mercury direct (not retrograde), no major malefic aspecting Mercury
   - Moving house → Moon in a fixed sign (Taurus, Leo, Scorpio, Aquarius) for stability
3. **Avoid Mercury retrograde** for any signing, launching, or starting-from-scratch.
4. **Avoid lunar eclipses** for almost all beginnings.
5. **Favour benefics on the relevant point:** Moon in a friendly sign, Jupiter trine or sextile the Ascendant, Venus well-placed.

### Vedic muhurta (the deepest electional system)
- **Pushya nakshatra** is the most auspicious for nearly all beginnings (nourishment, growth, support from Saturn's disciplined quality).
- **Rohini** (Moon) — beauty, abundance, creativity, marriage.
- **Hasta** (Moon) — skill, craftsmanship, healing.
- **Mrigashira** (Mars) — searching, gentle beginnings, journeys.
- **Avoid:** Ashlesha (serpent, deceit), Jyeshtha (seniority, isolation), Mula (uprooting).
- **Avoid 8th-house or 6th-house days** (Rahu Kalam, Yama Ghantaka, Gulika Kalam in South-Indian panchang).
- **Best weekday + hora combination** for the matter: e.g. Thursday + Jupiter's hora for financial beginnings, Friday + Venus's hora for romance/arts.

### Chinese day selection
- **Day branch** favourable to the querent's year animal (not clashing).
- **Day element** should feed the querent's Day Master (useful-god alignment).
- **No Tai Sui clash with the year** (see `bazi.md`).
- **Avoid "Bai Ji" days** (十恶大败日) — the ten days traditionally considered unfit for important beginnings.

### Giving the answer
Don't issue a single decree. Give **2–3 ranked candidate windows** with the
specific reason each one works, and one or two specific "avoid" windows. The
agent should explain *why*, not just *when*.

---

## 4. Rectification — when the birth time is unknown

**The question it answers:** *"Can you tell me exactly when I was born, given
that I know when my major life events happened?"*

### The method
1. **Collect 5–10 major life events with exact dates**: parent's death, marriage(s), first job, moves, accidents, childbirth, near-death experiences.
2. **For each candidate birth time** (typically 30-minute windows across the plausible range from the family), cast a chart and check whether **secondary progressions** or **solar arc directions** trigger each life event at its known date.
3. The candidate time that **simultaneously** triggers the most events at the right dates is the rectified time.

### What the engine can do
The current engine doesn't run automatic rectification — it doesn't compute
progressions or solar arcs. The honest move for the agent:
- **If the user only has a rough time** (e.g. "around breakfast"), run with
  `time_known:true` at the approximate time and flag that Rising, houses,
  and Moon degree carry an uncertainty of ~30 minutes. **Proceed.**
- **If the user has no time at all**, set `time_known:false` and read at
  Sun-sign level (Big Three replaced by Big One: the Sun). The Vedic lagna
  and BaZi hour pillar drop, but Moon, nakshatra, and dasha all still
  compute. Be honest about the missing layers.
- **If the user wants true rectification**, explain the method above, ask
  for the major events, and note that this is a multi-hour manual process
  (some professional astrologers charge $200–$500 specifically for it). The
  skill does not run automatic rectification in this version.

### The ethics of missing time
A common client fear: "If my chart is wrong, my whole reading is wrong." The
honest response: Sun sign + Moon sign + nakshatra are **unchanged by birth
time**. The dasha, the rashi, the element balance, the major yogas — all
robust to ±2 hours. Only the **Rising sign, the houses, and the BaZi hour
pillar** are time-sensitive. A reading without a birth time is still a
substantive reading; just say what's missing.

---

## 5. Namakaran — naming a child (or a business, or a project)

**The question it answers:** *"What should my baby be named? What syllable
vibrates with my chart / my business's inception chart?"*

### The classical rule (Vedic)
The **starting syllable of the name** is taken from the **Janma Nakshatra
pada** of the Moon (or for a business, of the inception chart's Moon).
The engine's `namakaran(moon_lon_sidereal)` returns the four syllables of
the relevant nakshatra, one per pada. Traditional rules:

- **Boy**: odd padas (1, 3) favoured; even padas (2, 4) sometimes preferred by region
- **Girl**: even padas (2, 4) favoured; odd padas (1, 3) sometimes preferred by region
- **Avoid** syllables that rhyme with the family surname (sound clash) and syllables of grahas to be pacified (e.g. Shani's syllable "Sa" not used if Saturn is the worst planet in the chart)
- **Combine** with the family letter tradition (e.g. South Indian: family letter from the father's name)

### The Western equivalent
Western baby-naming fads come and go; the most astro-aligned modern trend is
matching the child's chart to the **name's numerology** (Pythagorean, Chaldean,
or Vedic) and the **initial letter's zodiacal sign ruler** (Aries = "A" names
ruled by Mars). Less codified; the agent should be honest this is folk rather
than classical.

### Business naming
For a business: cast the **inception chart** (engine `mode:"event"`), find
its Moon, and run `namakaran` on it. The syllable that resonates with the
business's birth Moon becomes the suggested starting sound for the brand.
Pair with the **founder's own Janma Nakshatra** if compatibility with the
founder is the priority.

---

## 6. Medical astrology (deeper than the core reading)

**The questions it answers:** *"What body systems does my chart say to watch?
Why do I always get sick at the same time of year? When is the best time for
surgery? What herbs/medicines suit me?"*

### The zodiac-anatomy map
Each sign rules a body region (engine `ANATOMY`):
- **Aries** — head, brain, eyes, face, adrenals
- **Taurus** — neck, throat, vocal cords, thyroid, jaw
- **Gemini** — lungs, shoulders, arms, hands, peripheral nerves
- **Cancer** — chest, breasts, stomach, womb, lymph
- **Leo** — heart, upper back, spine, circulation
- **Virgo** — abdomen, intestines, spleen, assimilation
- **Libra** — kidneys, lower back, adrenals, skin
- **Scorpio** — reproductive organs, bladder, rectum, pelvis
- **Sagittarius** — hips, thighs, liver, sciatic nerve
- **Capricorn** — knees, bones, joints, teeth, skin
- **Aquarius** — ankles, calves, circulation, the electrical system
- **Pisces** — feet, immune system, the psyche

### The chart tells you which body systems to watch
- The **6th house** (Western) and **Shatru bhava** (Vedic) = chronic, daily-body patterns; its sign tells the system.
- **Saturn in or afflicting the 6th** = chronic, structural, long-lasting issues
- **Mars in the 6th or 8th** = inflammation, accidents, surgery themes
- **Chiron's house** = the arena of psychosomatic wounding and the gift of healing others through that wound
- **The Ascendant and its ruler** = the constitutional baseline

### Surgery timing — the most actionable rule
**Avoid elective surgery when the Moon transits the sign ruling the body part.**
- Throat surgery → avoid Moon in Taurus
- Heart surgery → avoid Moon in Leo
- Abdominal surgery → avoid Moon in Virgo
- Hips/thighs surgery → avoid Moon in Sagittarius
- Knee surgery → avoid Moon in Capricorn
- Etc.

**Additional rules** (classical):
- Avoid the **lunar eclipse** windows (2 weeks before/after) for elective procedures
- Prefer **Moon in a fixed sign** (Taurus, Leo, Scorpio, Aquarius) for stable outcomes
- **Mars afflicting the Moon** or the Ascendant ruler → higher risk of complications; defer
- The **waning Moon** is traditionally preferred for surgery (less vital force bleeding out)
- The **waxing Moon** is preferred for treatments that need to "build" (long-term therapies, organ-supportive procedures)

### The honest frame
**Astrology complements but never replaces medicine.** Use the engine to read
the *timing* and the *vulnerability map*. A real diagnosis comes from a real
doctor. The agent must be unequivocal about this: "your chart suggests
watching X; please see a qualified practitioner for any actual symptoms."

### Diet & lifestyle by chart
- **Aries-rising / Mars-prominent** → favours a cooling diet (less red meat, more greens); rhythmic exercise
- **Taurus / Venus-prominent** → favours slow, sensual eating; watch the throat (salt, sugar, voice use)
- **Gemini / Mercury-prominent** → favours light, varied meals; the breath and the lungs are the barometer
- **Cancer / Moon-prominent** → favours warm, cooked food; the gut is the emotional barometer
- **Leo / Sun-prominent** → favours the heart; aerobic exercise and warming spices
- **Virgo / Mercury-prominent** → favours simple, whole foods; routine is the medicine
- **Libra / Venus-prominent** → favours balance; the kidneys and skin
- **Scorpio / Mars-Pluto-prominent** → favours cleansing; the reproductive and eliminative systems
- **Sagittarius / Jupiter-prominent** → favours variety and the outdoors; the liver thrives on movement
- **Capricorn / Saturn-prominent** → favours discipline; bones and joints need weight-bearing and minerals
- **Aquarius / Uranus-Saturn-prominent** → favours the circulatory and nervous systems; rhythm and rest
- **Pisces / Neptune-Jupiter-prominent** → favours the immune and the psyche; the body is porous to environment

---

## 7. Mundane astrology — collective events, markets, politics

**The questions it answers:** *"Who will win the election? Is a recession
coming? When will the market crash?"*

### The methods
- **Ingress charts**: cast a chart for the **exact moment the Sun enters
  Aries** (Spring Equinox), Cancer (Summer Solstice), Libra (Autumn
  Equinox), Capricorn (Winter Solstice) at the capital. The Aries ingress
  is the year's primary mundane chart for that nation.
- **Eclipses**: solar and lunar eclipses mark **major collective
  inflection points** for 6 months before/after. Where the eclipse falls
  (which sign, which house of the nation's chart) describes the area of life
  most activated.
- **Outer-planet cycles**: Uranus, Neptune, Pluto sign changes mark
  generational shifts. **Pluto entering Aquarius** (2023–2044) is the
  current macro-signature: power, technology, AI, collective
  restructuring, and the dissolution/rebirth of old institutions.
- **Jupiter-Saturn conjunctions** ("Great Conjunctions") every ~20 years
  mark societal themes. The 2020 conjunction at 0° Aquarius began a
  ~200-year Aquarius era; 2020s will be defined by the early Aquarius
  archetype (technology, networks, collective governance).
- **Corporate charts**: cast a chart for the **moment of incorporation**;
  transits to that chart time the company's chapters (launches, crises,
  growth, mergers).

### What the engine can do
The engine computes ingress charts via the standard `mode:"event"` with the
event moment (e.g. the moment of Aries ingress for a given year, computed
astronomically as the equinox). For corporate / mundane work, the agent
should ask for the exact moment of the event (incorporation filing time,
election poll closing, etc.) and treat it as a regular chart.

### The honest frame
Mundane astrology is **the most contested branch** — even professional
astrologers disagree on whether it works at the collective level. The agent
should always offer it as **a possible lens, not a forecast**. Pair with
real-world data (e.g. "transiting Pluto in the 2nd house of the US Sibly
chart suggests financial restructuring, which lines up with the actual
2023 banking stress").

---

## 8. Forensic & lost-object astrology

**The questions it answers:** *"Where is the missing body? Is the rumor
true? Who committed the crime? Where is my lost ring?"*

### Lost objects (horary)
- **2nd house** = the lost item (your possessions); **4th house** = where it rests
- The **sign on the 4th house cusp** = the **element** of the location
  (see Horary above for Fire/Earth/Air/Water correspondences)
- The **Moon's last separating aspect** = the direction relative to the querent

### Forensic event charts
- Cast a chart for the **exact moment of the crime** (or "moment last seen")
- **Ascendant** = the victim; **Descendant** = the perpetrator
- **Mars** = violence, anger, the actor; **Saturn** = death, restriction
- **4th house** = the end of the matter (the grave, the hiding place)
- **Sign on the 4th** = element/direction of the location
- The **7th house ruler's sign and aspects** = the perpetrator's profile

### The honest frame
Forensic astrology is a **pseudoscience for most practical purposes** and
should be presented as a narrative, not a police report. The agent should
say so explicitly: "this is a reading of the *symbolic geometry* of the
moment, not an investigation tool. Real forensic work is for the police and
qualified investigators." Even so, the symbolic reading can sometimes
**suggest a direction or characteristic** that the querent already half-knows.

---

## 9. Corporate, pet, and event charts (engine `mode:"event"`)

**The questions it answers:** *"What is the destiny of my startup? Will the
new kitten get along with my cat? Should I move in on this date? Is this
moment right to launch?"*

### The method
Any "moment of inception" can be charted — the math is identical to a natal
chart. The agent and querent choose the moment together:

- **Company / startup** → exact moment of incorporation, or the moment a
  partnership agreement is signed, or the moment the product ships
- **Pet** → birth date/time (if known); if not, the moment the pet came
  home / was adopted
- **Wedding** → the moment the vows are exchanged (or the legal signing time)
- **House purchase** → moment the contract is signed
- **Project / creative work** → moment of public launch or first public showing
- **App / product** → moment of public release (this is the literal "ChatGPT
  moment" — the day OpenAI pushed the public release)

### The interpretation
Once you have the chart, **read it as a person**: Big Three = the
"personality" of the entity; 7th house = the customers/audience; 10th house
= market position/reputation; 2nd house = revenue model; 8th house =
investment/capital; 6th house = operations/employees. Transits to the
inception chart = the entity's life chapters. This is the same framework
as a human chart, just with the agent remapping "person" to "entity."

### Pet compatibility (synastry)
Two pet charts → `mode:"synastry"` with the two birth data sets. Read Sun-Moon
(bond), Venus-Mars (play), Mars-Mars (the fights). The fact that the
compatibility is computed the same way as a couple is itself the answer.

---

## 10. Out of scope (acknowledge honestly)

Some branches the skill does **not** support, and the agent should say so:

- **Nadi astrology** (Tamil palm-leaf reading) — requires physical access to
  the Nadi libraries in Tamil Nadu; not computable from a birth chart. If a
  user asks, explain the tradition and direct them to a practitioner.
- **Astrometeorology** (weather/earthquake prediction from eclipses) — a
  real historical branch but not a personal reading tool; the engine does
  not model it.
- **True automatic rectification** (no candidate-time scan against life
  events) — the engine does not run progressions or solar arcs; the agent
  can guide a manual rectification but does not automate it.

For these, the agent's job is to **acknowledge the tradition, explain the
method, and refer** to a qualified practitioner.
