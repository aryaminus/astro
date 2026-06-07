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

## Reading recipe
1. Lagna + its lord's placement → the life's frame and direction.
2. Moon sign + nakshatra → mind, emotion, character seed.
3. Scan dignities & the engine's yogas → the chart's strengths and strains.
4. **Current mahadasha + antardasha with dates** → the chapter they're living now and what it asks.
5. Tie the question's house(s) to the active dasha lord → the specific, timed answer.
6. Frame as karma-with-agency; offer a constructive remedy if apt.
7. **Health reading**: check 1st/6th/8th/12th + Saturn/Mars/Rahu; give the dasha timing and a practical remedy — never a diagnosis.
