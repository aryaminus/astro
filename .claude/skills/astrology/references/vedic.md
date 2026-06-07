# Vedic / Jyotisha — interpretation ruleset

Sidereal zodiac (Lahiri ayanamsha — the engine subtracts ~24° from tropical), Parashari
tradition. Focus: **karma, destiny, and the timing of life-events** via planetary
periods. This is the system for *"when"* and *"why is this my fate"* questions. Keep
its logic pure — do **not** import Western psychology mid-reading.

## 1. The three anchors
- **Lagna (Ascendant / rising sign)** = the body, self, and the frame for all 12 houses (bhavas). Its lord ("Lagnesha") and that lord's placement set the life's direction.
- **Janma Rashi (Moon sign)** = the mind and emotional life; in Vedic, the Moon often matters *more* than the Sun. Predictions are frequently read from the Moon as well as the Lagna.
- **Janma Nakshatra (the Moon's lunar mansion)** = the deepest signature of character and the seed of the dasha clock. The engine gives the nakshatra, its lord, deity, pada (quarter), and quality.

## 2. The Grahas (planets) and their karakas
Each graha *signifies* (is the karaka of) life-domains — engine `GRAHA_KARAKAS`:
Sun=soul/father/authority · Moon=mind/mother · Mars=energy/siblings/courage ·
Mercury=intellect/speech/business · Jupiter (Guru)=wisdom/children/wealth/dharma — the
great benefic · Venus (Shukra)=spouse/luxury/art · Saturn (Shani)=discipline/suffering/
longevity/karma — the great teacher through hardship · **Rahu** (north node)=obsession,
foreign, worldly amplification, illusion · **Ketu** (south node)=spirituality, loss,
past-life mastery, moksha.

**Dignity** (engine tags `exalted` / `debilitated` / `own sign`): an exalted graha
delivers its significations richly; debilitated, it struggles (but can form a
cancellation/Neecha-Bhanga that turns weakness to strength — note the possibility).

## 3. Bhavas (houses) — engine `VEDIC_HOUSE`
Same 1–12 frame, Vedic shading: 1 self/body · 2 wealth/family/speech · 3 courage/siblings
· 4 mother/home/heart · 5 children/intelligence/*purva punya* (past-life merit) · 6
enemies/debt/disease · 7 spouse/partnership · 8 longevity/transformation/the hidden · 9
fortune/dharma/father/guru (the luckiest house) · 10 career/status/action · 11
gains/income/desires-fulfilled · 12 loss/expense/foreign/moksha.
**Trikona** (1,5,9 = dharma/fortune) and **Kendra** (1,4,7,10 = pillars of action) are
the strong, auspicious houses; **Dusthana** (6,8,12) are the houses of struggle.

## 4. Yogas (special combinations) — engine `yogas`
The engine mechanically detects a few classical, checkable yogas:
- **Gajakesari** (Jupiter in kendra from Moon) — intelligence, reputation, lasting prosperity.
- **Budha-Aditya** (Sun+Mercury together) — sharp intellect, administrative skill.
- **Chandra-Mangala** (Moon+Mars) — drive for wealth, entrepreneurial intensity.
- **Exalted grahas** — that planet's gifts powerfully expressed.
Treat yogas as *amplifiers*, read in context of dignity and house. (Thousands more
exist in the classics; only report the ones the engine confirms — never invent yogas.)

## 5. Vimshottari Dasha — the timing engine (this is Jyotish's superpower)
A 120-year cycle of planetary periods (mahadashas) seeded by the birth nakshatra. The
engine returns the **current mahadasha**, the **current antardasha (sub-period / bhukti)**,
and the full timeline with dates. This is what lets you say:

> *"You entered your Mercury mahadasha in 2019; it runs to 2036. Mercury rules your 2nd
> and 7th — so this ~17-year chapter pushes communication, business, and partnership to
> the centre of your life. Right now you're in the Mercury–Venus sub-period, which
> favours relationships, contracts, and creative income through 2027."*

Read a dasha by: (a) the period-lord's natural significations, (b) the houses it rules
from the Lagna, (c) the house it *sits in*, (d) its dignity. The mahadasha sets the
decade's theme; the antardasha times the year. **Always give the dates** — concrete
timing is the relief people seek.

## 6. Karma framing
Vedic charts are read as the soul's karmic ledger: the 5th house (purva punya) shows
the merit you brought in; Saturn shows where the debt is paid through discipline; Rahu/
Ketu show the axis between past-life mastery (Ketu) and this-life hunger (Rahu).
Frame difficulty as *karma being worked through*, with agency — never as a fixed sentence.

## 7. Remedies (upayas) — offer gently, never as fear-sales
Classical remedies for a troubled graha: mantra (e.g. for Saturn on Saturdays), charity
aligned to the planet, gemstones (only on a competent astrologer's advice — they're
strong), strengthening the dasha lord's significations through right action. Present
these as supportive practices, not as "pay to avoid doom." (See `consultation.md` ethics.)

## 7. Health in the Vedic chart
Jyotish gives a detailed health map. The primary indicators:
- **1st bhava (Lagna)** — constitution, overall vitality; afflicted Lagna or Lagna lord = weaker body.
- **6th bhava (Shatru/Roga)** — diseases, debt, enemies; planets here or its lord's condition show chronic ailment tendencies. The *sign* of the 6th narrows the body system.
- **8th bhava (Ayu)** — longevity, hidden/chronic conditions, surgeries; Rahu in 8th or an afflicted 8th lord can bring sudden health disruptions.
- **12th bhava (Vyaya)** — hospitalisation, hidden enemies to the body, sleep quality.

**Graha health signatures**:
- **Surya (Sun)**: vitality, heart, spine, right eye; afflicted Sun → authority/ego injuries.
- **Chandra (Moon)**: mind, lungs, chest, left eye, hormonal tides; afflicted Moon → emotional/mental instability.
- **Mangal (Mars)**: blood, inflammation, fever, accidents, muscles; a strong Mars protects; afflicted → operations.
- **Shani (Saturn)**: bones, joints, nervous system, chronic ailments, teeth; its mahadasha often tests health through depletion.
- **Rahu**: mysterious/unusual conditions, foreign substances, poisons; Ketu → past-life ailments, separative surgeries.

**Timing health events**: The 6th/8th/12th lord dashas, or a transit of a malefic over the Lagna/Moon, can activate latent patterns. Always pair with "when does the dasha ease" — that's the recovery window.

**Remedies for health**: Strengthening the Lagna lord (mantra, right lifestyle for that planet); Saturn afflictions → discipline, service, cold water routines; Mars → non-violence, cooling diet.

## 8. Sade Sati — Saturn's 7.5-year Moon transit (most-asked Vedic question)

**Sade Sati** = Saturn transiting the sign before the natal Moon, the Moon sign itself, and
the sign after — three signs × 2.5 years = 7.5 years. The engine detects this in `sade_sati`.

- **Rising phase** (sign before Moon): external pressures begin, responsibilities mount.
- **Peak phase** (Saturn over Moon sign): the most demanding — emotional weight, health care
  needed, relationships tested, career restructuring. *Not a curse — Saturn's audit.*
- **Setting phase** (sign after Moon): pressure lifts; rebuilding; harvest of what was genuine.

Always name the **end date** of the current phase. *"Your Sade Sati peak runs through [date].
After that, this weight lifts."* That certainty is the relief people need. Frame it as a
seven-year renovation — people emerge with their most durable life structure.

**Remedies**: Shani mantra on Saturdays, black sesame charity, service to the elderly,
consistent discipline and routine (Saturn rewards what Sade Sati tests).

## 9. Atmakaraka — the soul significator (Jaimini)

The engine returns `atmakaraka`: the planet with the highest degree in its sign, excluding
Rahu/Ketu. It represents the soul's primary lesson and deepest essential quality.

| Atmakaraka | Soul theme |
| --- | --- |
| Sun | Leadership, self-authorship, authority — father/self are the karmic arena |
| Moon | Nourishment, belonging, emotional wholeness — mother and inner life |
| Mars | Courage, right action, standing firm — conflict is the soul's classroom |
| Mercury | Communication, discernment — the mind and speech are the soul's instrument |
| Jupiter | Wisdom, dharma, the guru — student relationships and expansion |
| Venus | Love, beauty, relationship — partnership and desire are the curriculum |
| Saturn | Discipline, humility, service — the soul agreed to learn through limitation |

The Atmakaraka's natal house shows *where* the soul's deepest work plays out this life.

## 10. Love marriage vs. arranged marriage (Q8 — common in South Asian contexts)

- **5th house/lord** = romantic desire, love affairs, the heart's choice.
- **7th house/lord** = formal partnership, the socially/family-sanctioned spouse.
- **Rahu in 5th or 7th** = unconventional relationships, cross-boundary love marriages.
- Venus aspecting the 5th = romantic path more natural; Venus in 7th = partnership through formal channels.
- Timing: 5th-lord or Venus dasha + Jupiter transiting 5th or 7th → marriage (love or arranged) is classically indicated.

## 11. Putra Bhava — children and fertility (Q45)

- **5th house** = children, creativity, past-life merit (purva punya).
- **Jupiter** = natural significator for children; his dignity is crucial.
- Delays (not denial): Saturn in 5th, 5th lord in 6/8/12, Jupiter debilitated.
  Neecha-Bhanga can reverse this; always check before saying "no children."
- **Timing**: Jupiter mahadasha/antardasha, or Jupiter transiting 1st/5th/9th = classic windows.
- Child's nature from 5th sign: Fire = energetic/assertive; Earth = steady/practical; Air = communicative; Water = sensitive.

## 12. Namakaran — naming a child or business (Q in §3 of ref/6.txt)

The classical rule: the **starting syllable of the name** is taken from the
**Janma Nakshatra pada** of the Moon (for a child) or the inception chart's
Moon (for a business). The engine's `namakaran(moon_lon_sidereal)` returns
the four pada-syllables for the relevant nakshatra. Common application rules:

- **Boys**: odd padas (1, 3) traditionally preferred; **girls**: even padas (2, 4).
- **Combine** with the family's traditional naming letter (varies by region).
- **Avoid** syllables of grahas to be pacified (e.g. don't start a name with "Sa" if Saturn is the worst planet in the chart).
- For **businesses**: cast the inception chart (`mode:"event"`), then `namakaran` on its Moon.

## 13. Mangal Dosha (Kuja Dosha) — the marriage flag

**Mars in the 1st, 2nd, 4th, 7th, 8th, or 12th house from the Lagna** is
traditionally flagged as Mangal Dosha (also called "Manglik") — said to bring
friction to marriage. **Important**:
- Mars in its **own sign** (Aries, Scorpio) or **exalted** (Capricorn) in these houses often **cancels** the dosha.
- The dosha is also **cancelled** if both partners are Manglik, or if Mars is in a kendra/trikona of the Navamsha.
- Modern practitioners are split on the strength of the flag; the agent should mention it when present and contextualise, not as a verdict.

## 14. Ashtakoota / Guna Milan — the 36-point marriage match (Q2)

The classical 8-Koota score (out of 36) for marriage compatibility. The engine
returns the two Janma Nakshatras; the agent can describe each Koota
qualitatively; for the full point scoring, the user can use a dedicated tool
or see a Jyotish practitioner.

| Koota | Max | What it measures |
| --- | --- | --- |
| **Varna** | 1 | spiritual / dharmic compatibility |
| **Vashya** | 2 | control / attraction |
| **Tara** | 3 | luck / birth-star harmony (9-count from each nakshatra) |
| **Yoni** | 4 | physical / sexual compatibility (animal-symbol) |
| **Graha Maitri** | 5 | mental compatibility (lordship friendship) |
| **Gana** | 6 | temperament (Deva / Manushya / Rakshasa) |
| **Bhakoot** | 7 | Moon-sign relationship (some combos = dosha) |
| **Nadi** | 8 | physiological / karmic (highest weight; **same Nadi = Nadi Dosha**) |

- Score **≥ 18**: workable. **≥ 25**: strong. **< 18**: friction; traditional.
- **Nadi Dosha** (same nadi) is the classical deal-breaker; many modern astrologers consider it overstated. Mention it; let the user decide.

## 15. Deeper remedies (upayas) — the classical toolkit

For a troubled graha, the classical remedies form a hierarchy. **Always offer as supportive practices, never as "pay to avoid doom."**

- **Mantra (beej) — repeat on the graha's day:**
  - Surya (Sun): "Om Hraam Hreem Hraum Sah Suryaya Namah" (Sunday)
  - Chandra (Moon): "Om Shraam Shreem Shraum Sah Chandraya Namah" (Monday)
  - Mangal (Mars): "Om Kraam Kreem Kraum Sah Bhaumaya Namah" (Tuesday)
  - Budha (Mercury): "Om Braam Breem Braum Sah Budhaya Namah" (Wednesday)
  - Guru (Jupiter): "Om Graam Greem Graum Sah Gurave Namah" (Thursday)
  - Shukra (Venus): "Om Draam Dreem Draum Sah Shukraya Namah" (Friday)
  - Shani (Saturn): "Om Praam Preem Praum Sah Shanaischaraya Namah" (Saturday)
  - Rahu: "Om Bhram Bhrim Bhraum Sah Rahave Namah" (Saturday)
  - Ketu: "Om Stram Strim Straum Sah Ketave Namah" (Tuesday/Thursday)
- **Charity (daan)** — to the graha's signifier: Saturn → the poor, elderly, disabled, dark sesame, iron; Mars → soldiers, blood donation, red lentils; etc.
- **Fasting (vrat)** — the graha's day, or the 11th tithi from birth.
- **Gemstones (ratna)** — the strongest remedy; **only on the recommendation of a competent Jyotish practitioner**, and only when the graha is functional and well-placed (wearing the gem of a weak/malefic graha can amplify problems).
- **Right action** — strengthen the dasha lord's significations through aligned conduct (Saturn mahadasha = disciplined service; Jupiter = teaching/learning; Venus = art/relationship care).

**Remedies never to give**: terminal-illness predictions, expensive rituals to "lift a curse," or a gem to "fix" a relationship.

## 16. Litigation, business & money outcomes (Q22)

For "will I win this lawsuit?" / "will the business turn a profit?" / "will I recover what was stolen?":
- **6th house (Shatru)** = the contest, the opponent; a strong 6th lord = strong position
- **10th house (Karma)** = the public outcome
- **11th house (Labha)** = gains from the verdict
- **2nd (Dhana) / 8th (others' money)** = the contested resource
- **Jupiter** (judge, dharma) well-placed in kendra/trikona = favourable judgment
- **Mercury** (the brief) well-placed = case well-presented
- **Active mahadasha of 6th or 10th lord** = resolution window

Frame honestly: charts show *tendency*, not verdicts. A good lawyer, evidence, and timing all matter; the chart is one input.

## 17. Inheritance & others' money (Q in §6 of ref/6.txt)

For "which parent will leave the larger inheritance?" / "will I receive the expected sum?" / "will the siblings fight me for it?":
- **8th house** = others' money (including inheritance), the partner's assets, sudden transformation
- **4th house** = one parent (often the mother), the home you inherit
- **10th house** = the other parent (often the father), status inheritance
- **2nd from 8th (= 9th)** = the luck of the inheritance reaching you
- **Benefics on 8th / 8th lord in a good house** = the inheritance is likely
- **Malefics on 8th / 8th lord in 6/8/12** = delay, dispute, or litigation over it
- **3rd house** = siblings; a hard aspect between 3rd and 8th lords = sibling friction over the estate

Frame as a *family-pattern* issue (often karmic, often with a hard emotional truth); don't fuel family conflict. For sensitive family-wealth questions, suggest the querent discuss the patterns calmly with a mediator or estate planner, not at the dinner table.

## 18. Foreign travel & relocation (Q19)

For "should I move abroad?" / "will I be more successful overseas?":
- **12th house** = foreign lands, life away from birth, the bed
- **9th house** = long travel, fortune, the foreign
- **Lagna lord in 7th, 9th, or 12th** = life-direction is *away* from birth
- **Moon in a movable (cardinal) sign** or strong cardinal emphasis = a life of movement
- **Rahu in 9th** = the soul's pull toward the uncharted
- **Saturn in 12th** = the cost of foreign life (loneliness, slow start, but eventual depth)
- For the *where*, use the **astrocartography** mode of the engine — see `specialty-systems.md §1`

## Reading recipe
1. Lagna + its lord's placement → the life's frame and direction.
2. Moon sign + nakshatra → mind, emotion, character seed.
3. Scan dignities & the engine's yogas → the chart's strengths and strains.
4. **Current mahadasha + antardasha with dates** + Sade Sati status → the chapter they're living now.
5. Tie the question's house(s) to the active dasha lord → the specific, timed answer.
6. Check Atmakaraka for soul-purpose questions.
7. Frame as karma-with-agency; offer a constructive remedy if apt.
8. **Health reading**: check 1st/6th/8th/12th + Saturn/Mars/Rahu; give the dasha timing and a practical remedy — never a diagnosis.
