# Specialty & Niche Branches — the secondary layer

Beyond the core reading of a natal chart, every tradition has a long tail of
specialised branches — the questions a long-time client brings once the basics
have been covered. This file is the playbook for those questions, organised
by branch. It pairs with the engine's extra modes (`astrocartography`,
`horary`, `event`) and its specialty lookups (`namakaran`, `anatomy_chart`).

Rule that governs every section here: **always cite the computed placement**.
The specialty branches are the most tempting to free-associate on. Resist.

---

## §1 — Astrocartography & relocation (engine `mode:"astrocartography"`)

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

### The Twin Cities note
Astrologers note that many people flourish in cities *opposite* their birth
longitude. The DS line of the Sun, the IC line of the Moon, the ASC line of
Jupiter — these are often "where I become who I was always meant to be." Use
the engine's output to surface non-obvious lines for the client.

### Property buying & home timing

4th house lord's strength + current 4th-house transits time home purchases.
Jupiter or Venus transiting the 4th = auspicious time to buy home/land.
In BaZi: choose a year whose element supports the Day Master, and a house
facing a direction aligned with the Useful God element. Avoid purchasing
when malefics (Saturn, Rahu, Mars) heavily afflict the 4th house lord.

### Travel safety

Check the Moon and 9th-house ruler for the travel period. Avoid major malefic
transits to the Ascendant or Moon during the travel window. In BaZi, avoid
travelling in years that clash with your year-branch animal (e.g. Dragon year
person avoids Dog year travel). See also the **local space chart**: the natal
chart's angular planets (1st/4th/7th/10th) point in specific compass directions
from the birthplace — living or travelling in those directions activates the
planet's themes.

---

## §2 — Horary / Prasna — chart of the moment (engine `mode:"horary"`)

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

For lost-object guidance, see **§6** below.

---

## §3 — Electional astrology — picking the right day (also `synastry-and-timing.md`)

**The questions it answers:** *"When should I get married? Launch the business?
Sign the contract? Have the surgery? Send the email? Move house?"*

### Core rules (cross-tradition)
1. **Identify the house that rules the matter** (7=marriage, 10=career, 2/8=finance, 5=children/creativity).
2. **Find a day when the relevant planet is strong and unafflicted.**
3. **Avoid Mercury retrograde** for any signing, launching, or starting-from-scratch.
4. **Avoid lunar eclipses** for almost all beginnings.
5. **Favour benefics on the relevant point:** Moon in a friendly sign, Jupiter trine or sextile the Ascendant, Venus well-placed.
6. **Check Void-of-course Moon** → if VoC on the candidate day, do not initiate.

### Vedic muhurta (the deepest electional system)
- **Pushya nakshatra** is the most auspicious for nearly all beginnings.
- **Rohini** (Moon) — beauty, abundance, creativity, marriage.
- **Hasta** (Moon) — skill, craftsmanship, healing.
- **Mrigashira** (Mars) — searching, gentle beginnings, journeys.
- **Avoid:** Ashlesha (serpent, deceit), Jyeshtha (seniority, isolation), Mula (uprooting).
- **Avoid 8th-house or 6th-house days** (Rahu Kalam, Yama Ghantaka, Gulika Kalam in South-Indian panchang).
- **Best weekday + hora combination** for the matter: e.g. Thursday + Jupiter's hora for financial beginnings, Friday + Venus's hora for romance/arts.

### Specific event rules (also see `synastry-and-timing.md §C.1–C.5`)
- **Wedding muhurtham**: fixed (Sthira) Lagna; Moon in Rohini / Mrigashira / Magha / Uttara Phalguni / Hasta / Swati / Anuradha / Uttara Ashadha / Uttara Bhadrapada / Revati; Venus and Jupiter unafflicted; Tarabala favourable for both bride and groom.
- **Business launch**: movable (Chara) Lagna; 10th house strong; Mercury and Jupiter unafflicted; Pushya / Hasta / Rohini nakshatra.
- **Surgery**: avoid Moon in the sign ruling the body part; avoid lunar eclipse; prefer fixed-sign Moon; waning Moon; Mars not afflicting the Lagna.
- **Contract signing**: Mercury direct; Moon not in 6/8/12 from Lagna; Mercury unafflicted.
- **House purchase / renovation**: 4th house strong, unafflicted; fixed-sign Moon; Venus well-aspected; Mars not in the 4th.

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

## §4 — Rectification — when the birth time is unknown

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

## §5 — Namakaran — naming a child or business

**The question it answers:** *"What should my baby be named? What syllable
vibrates with my chart / my business's inception chart?"*

### The classical rule (Vedic)
The **starting syllable of the name** is taken from the **Janma Nakshatra
pada** of the Moon (or for a business, of the inception chart's Moon).
The engine returns `janma_nakshatra`. Traditional rules:

- **Boy**: odd padas (1, 3) favoured; even padas (2, 4) sometimes preferred by region
- **Girl**: even padas (2, 4) favoured; odd padas (1, 3) sometimes preferred by region
- **Avoid** syllables that rhyme with the family surname (sound clash) and syllables of grahas to be pacified (e.g. Shani's "Sa" if Saturn is the chart's worst graha)
- **Combine** with the family letter tradition (e.g. South Indian: family letter from the father's name)

### Nakshatra syllable table (all 27)

| Nakshatra | Starting syllables | | Nakshatra | Starting syllables |
| --- | --- | --- | --- | --- |
| Ashwini | Chu, Che, Cho, La | | Vishakha | Ti, Tu, Te, To |
| Bharani | Li, Lu, Le, Lo | | Anuradha | Na, Ni, Nu, Ne |
| Krittika | A, I, U, E | | Jyeshtha | No, Ya, Yi, Yu |
| Rohini | O, Va, Vi, Vu | | Mula | Ye, Yo, Ba, Bi |
| Mrigashira | Ve, Vo, Ka, Ki | | Purva Ashadha | Bu, Dha, Bha, Da |
| Ardra | Ku, Kha, Ng, J | | Uttara Ashadha | Be, Bo, Ja, Ji |
| Punarvasu | Ke, Ko, Ha, Hi | | Shravana | Ju, Je, Jo, Sha |
| Pushya | Hu, He, Ho, Da | | Dhanishtha | Ga, Gi, Gu, Ge |
| Ashlesha | Di, Du, De, Do | | Shatabhisha | Go, Sa, Si, Su |
| Magha | Ma, Mi, Mu, Me | | Purva Bhadrapada | Se, So, Da, Di |
| Purva Phalguni | Mo, Ta, Ti, Tu | | Uttara Bhadrapada | Du, Th, Jha, Na |
| Uttara Phalguni | Te, To, Pa, Pi | | Revati | De, Do, Cha, Chi |
| Hasta | Pu, Sh, Na, Th | | | |
| Chitra | Pe, Po, Ra, Ri | | | |
| Swati | Ru, Re, Ro, Ta | | | |

### Children's charts

Read a child's chart **for the parent's understanding**, not as the child's fate.
Never label a child as "difficult" or use their chart to compare them with siblings.

- **Moon sign** = the child's emotional needs and how they receive love
- **Mercury sign/house** = how they learn best (earth = hands-on; air = verbal/conceptual; fire = enthusiastic; water = intuitive)
- **Sun sign** = the identity they're growing *into* — not there yet, so give patience not projection
- **Saturn's placement** = where they'll face the most structured challenge; give support, not pressure

### Fertility timing

In Vedic: **5th house (Putra bhava)** + Jupiter's condition. Check the 5th lord's dignity and placement — strong = good fertility potential. Delays (not denial) from Saturn/Rahu in the 5th or afflicting the 5th lord. Timing: children classically arrive in **Jupiter dasha/antardasha**, or when Jupiter transits the 5th or 9th, or when the 5th-lord dasha activates. Check for Neecha-Bhanga before calling any delay permanent.

In Western: 5th house planets + Venus/Moon condition. Jupiter transiting the 5th or making a good aspect to natal Moon = fertility window. New Moons near the 5th house cusp align symbolically.

In BaZi: the **Output element** (what the Day Master produces) = children. Strong Output element in the chart or luck pillar = natural window for children.

**Fertility window** = parent in a Jupiter-active period (Jupiter dasha or
antardasha; Jupiter transiting 1/5/9); see `vedic.md §11` for the full Putra
Bhava ruleset.

### Western baby-naming
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

Element vibration for the brand name style: Fire-sign Moon = bold, leading names; Earth = solid, trustworthy names; Air = communicative, clever names; Water = intuitive, caring names.

### Changing one's own name
A common modern question: "If I legally change my first name, will it change
my destiny / fix my bad luck?" Classical Jyotish says: a name *can* shift the
vibrational pattern, but only if (a) the new name's syllable matches the
natal nakshatra pada, (b) the change is done on a favourable muhurta
(see §3), and (c) the person lives into the new name (the chart doesn't
change retroactively, but the *vibration* of the lived name can support a
new chapter). The agent should be honest this is less codified than
parent-to-child naming.

---

## §6 — Lost objects & quick decisions (using the horary engine)

For simple lost-object questions and immediate "should I" decisions, the
agent runs a quick horary chart and reads the **4th house** (where the
object rests / where the matter ends) and the **Moon's last separating
aspect** (direction relative to the querent).

### "Where did I lose my ___?"
- **2nd house** = the lost item (your possessions); **4th house** = where it rests
- The **sign on the 4th house cusp** = the **element** of the location:
  - **Fire (Aries/Leo/Sagittarius)** → near heat (kitchen, fireplace), high places, east-facing rooms
  - **Earth (Taurus/Virgo/Capricorn)** → on the ground, in storage, in soil or wood; low shelves
  - **Air (Gemini/Libra/Aquarius)** → where air moves (windows, vents), on paper, in books
  - **Water (Cancer/Scorpio/Pisces)** → near water (sink, bathroom), in containers, dark damp places
- The **Moon's last separating aspect** = the direction relative to where you are now

### "Should I do X right now?"
- Run a horary chart for the moment of deliberation
- **VoC Moon** → "nothing will come of it" — wait
- **Mercury retrograde** in the chart → "you'll be redoing this — wait"
- **The 1st house ruler applying to a benefic** → "yes, go"
- **The 1st house ruler in 6/8/12 or with a malefic** → "the matter has a cost — proceed with eyes open"

### The honest frame
The chart gives the *element and direction*, not the exact GPS. Be honest
about this limit; the level of specificity a real "where is it?" question
needs is beyond any chart. The querent still has to walk through the space.

---

## §7 — Mundane astrology — collective events, markets, politics

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

## §8 — Forensic & criminal astrology

**The questions it answers:** *"Where is the missing body? Is the rumor
true? Who committed the crime? Where is my lost ring?"*

### Lost objects (use §6 above; the same rules apply)

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

For sensitive forensic questions (missing persons, crime), always
recommend the user also contact law enforcement and licensed investigators.

---

## §9 — Corporate, pet, event, and family-conflict charts (engine `mode:"event"`)

**The questions it answers:** *"What is the destiny of my startup? Will the
new kitten get along with my cat? Should I move in on this date? Is this
moment right to launch? How can I mend my relationship with my parent?"*

### The "moment of inception" method
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
- **Divorce finalisation** → moment the decree is signed
- **Recovery milestone** → first day of sobriety, day out of hospital, etc.

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

### Family conflict & home
For "why is there so much arguing at home?" / "how do I mend things with my parent?":
- **4th house** (Western) / **Sukha bhava** (Vedic) = the home, the parents, the heart of the family
- The 4th house's current **transits** describe the *current* family atmosphere
- The 4th **lord's** placement and condition describe the *texture* of the family
- Saturn in / afflicting the 4th = long-running family weight, often from ancestral patterns
- For parent-specific: 4th = one parent (often mother), 10th = the other (often father); compare to the **natal Moon** and **natal Sun** for the parents as people
- For active mend: a Jupiter transit through the 4th (or the parent's 4th) often opens a window of forgiveness; an eclipsed Moon transit can also crack the family open
- **Read the parent's chart too** if you have it — most family conflict is bidirectional

---

## §10 — Past lives, karma, evolutionary astrology

**The questions it answers:** *"How did I die in a past life? What phobias
am I carrying from before? What is my karmic debt? Why do I keep repeating
the same painful lesson?"*

### Vedic (Jyotish) — Rahu and Ketu
- **Ketu** (south node) = past-life mastery, what the soul has already
  learned, the gift to *use* not *pursue*; in the chart, the Ketu sign/house
  describes an area of innate skill and equally a danger of over-identifying
  with the past
- **Rahu** (north node) = the soul's hunger this lifetime, the unfamiliar
  direction, the area of growth-by-stretching; the Rahu sign/house is where
  obsession, ambition, and unconventional success come
- The **Rahu-Ketu axis** is the karmic spine of the chart; the houses they
  occupy describe the axis of past-life comfort (Ketu) vs. this-life
  stretching (Rahu)

### Western — Pluto and the South Node
- **Pluto** at birth = the soul's evolutionary starting point; the sign and
  house describe the depth of transformation the soul agreed to
- **South Node** = past-life comfort and gifts to release
- **North Node** = this-life growth edge (Rahu's equivalent)
- **Chiron's house** = the area of psychosomatic wounding carried over from
  earlier, which becomes the gift of healing others
- The **12th house** = the unconscious, the past, what's behind the curtain;
  its transits and progressions describe the karmic re-patterning

### Pluto transits
The transits that *most reliably* mark the moments when past-life material
surfaces:
- **Pluto conjunct the Ascendant** → a death-and-rebirth of identity
- **Pluto conjunct the Sun or Moon** → the soul's core question comes up
- **Pluto conjunct the South Node** → the past-life pattern demands resolution
- **Pluto square the Nodal axis** → the karmic balance shifts, often through crisis

### Evolutionary astrology (Jeffrey Wolf Green school)
- Focus is on the *evolutionary intention*: what the soul wanted to do this
  time that it didn't manage last time
- The **South Node** is not just past comfort; it's the *strategy the soul
  developed* to survive, and Pluto shows how the soul will be asked to
  transform it
- The **North Node** is the *evolutionary intention*: the direction the soul
  wants to grow

### Reading recipe
1. Identify the Rahu-Ketu axis (Vedic) and the Pluto placement (Western)
2. Describe the past-life pattern (the gift, the comfort, the over-use)
3. Describe the this-life hunger / evolutionary intention
4. Note the current Pluto transit if active → "the soul is being asked to transform ___ right now"
5. Frame as work the soul *can* do, not a fixed sentence

---

## §11 — Taboo & highly intimate questions

People bring the questions they would never ask a therapist or priest. Because
astrologers are read as neutral observers of a mathematical chart, the
confessional posture is common. The questions span:

- **"I'm having an affair — will my spouse find out?"** — Read the 7th house (the spouse's proxy) and the 12th (the hidden). A 7th-12th hard aspect or 12th-house malefics → concealment has a cost. A 7th-house transit opening → the truth surfaces. **Don't** moralise; reflect the geometry of secrecy and offer the choice.
- **"I hate my career but I make too much money to leave — will the universe force me out?"** — Read the 2nd (security), 10th (career), 6th (daily work), and the transits to the Midheaven. A Saturn return or 10th-house Pluto transit often does exactly this — *forces the exit the person won't choose*.
- **"Which parent will leave the larger inheritance?"** — See `vedic.md §17`. Read 4th and 10th houses, 8th for the inheritance itself. Frame as a family-pattern issue; suggest estate mediation rather than a family fight.
- **"Will I have an affair, ever?"** — Read 5th (romance, pleasure), 8th (intimacy, the hidden), 12th (the unconscious, what's concealed), and Venus/Mars. The honest read: a high-libido signature (Mars-Venus in passionate signs, Pluto aspecting the 5th, Rahu in 7th) describes the *capacity*, not a *fate*. Agency is the agent's gift back to the client.
- **"Will my ex come back?"** — Read the 7th house and its current transits, plus the relationship's dasha timing (Vedic) and the 7th-house activation in the partner's chart if you have it. The honest answer is almost never a binary; it's "the relationship has a future *if both of you do this work*."

**The frame**: these are normal human questions. The agent's job is to hold
them with compassion, never judgement, and to translate the geometry into
honest language. The chart shows the shape of the energy; the person still
chooses the action.

For fertility, conception, and "will I be a parent?" see **§5** above (with
the Putra Bhava rules in `vedic.md §11`).

For inheritance and family-money disputes see `vedic.md §17`.

---

## §12 — Curse / evil eye / blocked energy

**The question it answers:** *"Is there a curse on me? Is someone sending
me negative energy? Why is everything blocked?"*

This question is common in Mediterranean, Middle Eastern, Latin American, and
some South Asian contexts. The agent should:

- **Listen first** — for the person, "curse" is a real felt experience. The
  chart's job is to translate it, not to dismiss it.
- **Reframe through the chart**: classical Jyotish and Hellenistic astrology
  *do* have vocabulary for what the modern mind calls a "curse":
  - **Saturn in the 8th / 12th** with no benefic aspect = chronic, long, hidden suffering
  - **Rahu in the 12th** + 1st-lord in 6/8/12 = the body's energy is "stuck"
  - **Affliction of the 5th house (purva punya)** = the soul came in with unfinished business; the patterns repeat
  - **A "functional malefic" without cancellation** = a planet that can't deliver its gifts; an area of life that feels blocked
- **Offer the classical remedies** (see `vedic.md §15`): the Saturn
  mantra + Saturday service, charity to the graha's signifier, the right
  action. The "lift the curse" framing is a fear-based upsell the agent
  must avoid. The "work the pattern" framing is honest and empowering.
- **Validate the felt experience without endorsing magical thinking**:
  *"What you're describing has a real felt weight. The chart shows it as
  [Saturn in the 8th]. The classical remedy is [Saturn mantra + service
  to the elderly + disciplined daily structure]. That's the work. The
  chart is a map; you're the one walking the path."*
- **If a paid "curse removal" ritual is being suggested** by another
  practitioner, gently flag: classical Jyotish does not support
  paid-ritual "curse lifts" by competent astrologers. This is a known
  exploitation pattern; protect the client.

---

## §13 — The Twin Problem (why a 3-minute difference can change everything)

**The question it answers:** *"My twin and I were born 3 minutes apart. We
have the same chart. Why do we live such different lives?"*

The answer in practice: **they don't have the same chart**. The Ascendant
moves roughly 1° every 4 minutes, so a 3-minute difference can shift the
Ascendant by up to 1° (sometimes the whole Rising sign), and a 2-hour
difference (the longest plausible "twin" interval) can shift the Moon by
1°. The natal chart at finer resolution tells the story:

- **D-9 (Navamsha)** — the marriage and dharma chart; changes every 3°20'
  (≈ 8 minutes of birth time); the most classical resolution to the twin
  problem
- **D-60 (Shashtiamsha)** — the karma chart; changes every 1° (≈ 2 minutes
  of birth time); the most granular
- **D-1, D-2, D-3, D-4…** (the varga charts of Vedic astrology) — each
  layers a different life-domain onto the same planetary positions at
  increasing resolution
- **Progressed chart** (Western) — moves ~1° per year; after the birth,
  the progressed Ascendant can be in a *completely different sign* from
  the natal Ascendant
- **Solar arc directions** — move ~1° per year; trigger life events with
  extraordinary accuracy when calculated correctly

### What the agent should do
- Validate the question (it's a real puzzle and a great one)
- Run the engine and show the difference in the *2nd-3rd minute* of the
  birth time — even a small time shift changes the Moon's exact degree,
  the dasha balance, the planetary aspects
- Note that **the varga charts and progressions are where the real
  difference shows up**; the current engine computes the Rasi (D-1) chart;
  for full twin-differentiation work, see a Jyotish practitioner who
  computes the D-9 and D-60
- The deeper truth: the chart is the *map of possibility*, not the
  *blueprint of fate*; even identical twins make different choices, and
  the chart describes the energy available to those choices, not the
  choices themselves

---

## §14 — Planetary Magic & Talismans (Hermetic / Occult)

**The questions it answers:** *"When should I forge a ring to capture Jupiter's wealth? What planetary spirit is causing my bad luck?"*

This branch uses astrology not to *read* the stars, but to *capture* their power (based on medieval texts like the Picatrix).
- **The method**: Finding the exact minute a planet is perfectly dignified (e.g. in its own sign, rising on the Ascendant, free from hard aspects) to create an object or perform a ritual.
- **The honest frame**: The engine can compute the perfectly dignified moments (using the `event` mode or scanning transits), but the agent must state clearly that the skill maps the *astronomical geometry*, while the ritual/magical practice is beyond the scope of a structural reading.

---

## §15 — Galactic Origins & Starseeds (New Age)

**The questions it answers:** *"Am I a Starseed from the Pleiades? Does my chart connect to the Galactic Center?"*

A modern subculture focused on deep space, Black Holes, and Fixed Stars (Sirius, Arcturus, Pleiades, the Galactic Center at ~27° Sagittarius).
- **The method**: Looking for exact conjunctions (within 1-2 degrees) between personal planets and specific fixed stars.
- **The honest frame**: The base engine currently focuses on the solar system (classical and modern planets + Chiron). The agent should acknowledge the Starseed paradigm as a modern archetypal lens. If the user asks about the Galactic Center, the agent can check if they have planets at late Sagittarius. 

---

## §16 — Sports Betting & The Lottery (Speculative)

**The questions it answers:** *"Who will win the Super Bowl? Will I win the lottery?"*

Astrologers are often asked to beat the house. 
- **Sports**: Horary/event charts cast for the starting whistle (Ascendant = favorite, Descendant = underdog).
- **Lottery**: Examining the 8th house (others' money) and 11th house (sudden windfalls). Saturn in these houses usually means "stop buying tickets."
- **The honest frame**: The agent must **strictly refuse** to provide gambling or financial betting advice. The geometry can be analyzed post-game for educational purposes, but predicting speculative outcomes for money violates the ethical core of the skill.

---

## §17 — Asteroids & Dark Points (Lilith, Chiron, Pallas)

**The questions it answers:** *"Where is my Black Moon Lilith? What is my Chiron wound?"*

When the main 10 planets don't explain a person's pain, astrology looks to asteroids and calculated points.
- **Chiron**: The "Wounded Healer" — where we experience a chronic psychosomatic wound that eventually becomes our greatest medicine for others. (Computed by the engine).
- **Black Moon Lilith**: The lunar apogee, representing repressed rage, raw feminine power, and parts of the psyche rejected by society.
- **Pallas Athena**: Strategy, pattern recognition, and survival in male-dominated systems.
- **The honest frame**: The engine computes Chiron. For Lilith, Pallas, Juno, Vesta, or Ceres, the agent must honestly state they are not currently calculated by the deterministic engine, but if the user provides their placements, the agent can interpret them based on the sign/house archetypes.

---

## §18 — Dream Interpretation (Oneiromancy via Astrology)

**The questions it answers:** *"Why am I having apocalyptic nightmares? Was that dream a real visitation?"*

People experience profound dreams during specific planetary alignments.
- **The method**: Checking transits to the natal Moon (nightmares often correlate with Mars/Pluto/Neptune transits to the Moon) and the 12th House (the subconscious, the veil between worlds).
- **The honest frame**: The agent validates the dream's emotional weight by linking it to the current transiting geometry, particularly emphasizing 12th house activations or hard aspects to the natal Moon.

---

## §19 — Out of scope (acknowledge honestly)

Some branches the skill does **not** support, and the agent should say so:

- **Nadi astrology** (Tamil palm-leaf reading) — requires physical access to the Nadi libraries in Tamil Nadu; not computable from a birth chart. If a user asks, explain the tradition and direct them to a practitioner.
- **Astrometeorology** (weather/earthquake prediction from eclipses) — a real historical branch but not a personal reading tool; the engine does not model it.
- **True automatic rectification** (no candidate-time scan against life events) — the engine does not run progressions or solar arcs; the agent can guide a manual rectification but does not automate it (see §4).
- **Calculated Asteroids/Dark Points** (Lilith, Pallas, etc. besides Chiron) — the engine calculates Chiron, but not Lilith or the thousands of minor asteroids.

For these, the agent's job is to **acknowledge the tradition, explain the method, and refer** to a qualified practitioner or invite the user to provide the data themselves.
