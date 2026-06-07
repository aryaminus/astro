# Health & Medical Astrology — interpretation ruleset

People ask health questions constantly (ref/6.txt Q27–30, Q33). This file grounds those
readings in classical medical astrology across all three traditions. **Ethics first:**
never diagnose, never terrify, never predict death. Map the chart; point to a doctor.

---

## A. Western Medical Astrology

### Body parts ruled by each sign
| Sign | Body region |
| --- | --- |
| Aries | Head, face, brain, eyes |
| Taurus | Throat, neck, thyroid, vocal cords |
| Gemini | Lungs, arms, hands, nervous system |
| Cancer | Stomach, breasts, lymphatic system |
| Leo | Heart, spine, upper back |
| Virgo | Digestive system, intestines, pancreas |
| Libra | Kidneys, lower back, adrenal glands |
| Scorpio | Reproductive organs, colon, bladder |
| Sagittarius | Hips, thighs, liver, sciatic nerve |
| Capricorn | Knees, bones, skin, teeth, joints |
| Aquarius | Ankles, calves, circulatory system |
| Pisces | Feet, lymph, immune system, sensitivity to drugs/alcohol |

**How to use**: If a person says "I constantly suffer from [X]," look at whether the ruling
sign of that body part is stressed (malefic in that sign, or that sign's house ruler afflicted).
Example: chronic throat issues → check Taurus planets + 2nd house + Venus.

### Planetary health rulerships
- **Sun** → vitality, heart, eyes, spine. Afflicted Sun = low vitality, heart stress, poor immunity.
- **Moon** → fluids, stomach, lymph, hormonal cycles. Afflicted Moon = digestion, mood, cycles.
- **Mercury** → nervous system, lungs, hands. Afflicted Mercury = anxiety, respiratory issues.
- **Venus** → kidneys, skin, reproductive system, sugar metabolism.
- **Mars** → inflammation, fever, accidents, surgery, adrenals, iron. Afflicted Mars = infections, injuries.
- **Jupiter** → liver, fat metabolism, expansion (physical and literal — weight, tumours, excess).
- **Saturn** → bones, teeth, joints, chronic conditions, deficiency, hardening. Saturn = the long-term chronic.
- **Uranus** → nervous system disruptions, sudden conditions, erratic signals.
- **Neptune** → immune confusion, allergies, mystery illnesses, sensitivity to medications, addiction.
- **Pluto** → deep cellular transformation, cancer (in the sense of radical change), toxins, regeneration.
- **Chiron** → chronic wounds that never quite heal but become the teacher; the body's story.

### The key health houses
- **1st house** — the body and vitality overall; its sign and ruler reveal constitution.
- **6th house** — daily health, illness, service. Planets here and its ruler's placement = health weaknesses.
- **8th house** — chronic and hidden conditions, surgery, transformation through illness.
- **12th house** — hospitalisation, hidden enemies of the body, immune conditions, confinement.

**Reading recipe for health**: (1) Check the Ascendant sign and 1st-house planets for constitution.
(2) Find planets in the 6th, and the 6th-house ruler — where is it, how is it aspected?
(3) Any planet in fall/detriment + in a health house = a system under strain.
(4) Current transits to the 1st/6th/8th (especially Saturn and Mars) time health challenges.
(5) Mention the body part ruled by the stressed sign → a maintenance focus, not a diagnosis.

### Surgical timing (Electional Medical Astrology)
Classical rule: **avoid surgery on the body part ruled by the Moon's current sign.**
(Moon in Taurus → avoid throat surgery; Moon in Scorpio → avoid reproductive surgery.)
Best windows: Moon in a fixed sign, waxing phase for building up, waning for reduction.
Avoid Mercury retrograde for anything requiring clear communication with the surgical team.
Saturn transiting the 6th or 1st = a period to take preventive health steps seriously.

---

## B. Vedic Health (Ayurvedic layer)

### The three doshas from the chart
| Dosha | Elements | Governing planets | Constitution traits |
| --- | --- | --- | --- |
| **Vata** (air + ether) | Air, Ether | Saturn, Rahu, Mercury | Thin, dry, anxious, creative, variable digestion |
| **Pitta** (fire + water) | Fire, Water | Sun, Mars, Ketu | Medium build, intense, ambitious, inflammatory tendency |
| **Kapha** (earth + water) | Earth, Water | Moon, Jupiter, Venus | Solid build, calm, loyal, prone to congestion and weight |

**Dosha from chart**: Look at the lagna (rising sign) element + Moon sign element + dominant planetary stellium. Fire/Mars dominant = Pitta. Air/Saturn dominant = Vata. Earth or Water + Moon/Jupiter = Kapha.

### Vedic health houses
- **1st (Lagna)** — body, vitality, the physical self.
- **6th (Shatru bhava)** — disease (roga), enemies of the body. 6th lord in bad dignity = prone to illness.
- **8th (Ayu bhava)** — longevity, hidden/chronic illness, transformation.
- **12th (Vyaya)** — hospitalisation, loss of health, bed confinement.
- **Dusthana rule**: 6th lord in 8th or 8th lord in 6th can form **Viparita Raja Yoga** (weakness that secretly becomes strength — illness that catalyses transformation) — note the nuance before calling it simply bad.

### Sade Sati and health
The engine detects **Sade Sati** (`sade_sati` field). The **peak phase** (Saturn over natal Moon
sign) is the most physically demanding — digestion, sleep, and immunity often suffer. This is
*not illness; it is the body's seven-year renovation*. Advise: rest, reduce excess, eat well,
exercise consistently. The rising and setting phases are lighter but still watchful periods.

### Health-graha combinations to note (cite from engine data, don't invent)
- Sun in 6th or 8th, afflicted → vitality dips, paternal health parallels
- Moon afflicted by Mars or Rahu → hormonal/menstrual/emotional health cycles
- Saturn in 1st or 6th → chronic conditions, slow metabolism, bone/joint care needed
- Mars in 8th → accident-prone; surgery a likelihood at some point; channel Mars (exercise)
- Rahu in 6th → mystery illnesses, allergies, unusual diagnoses

### Remedial approach (grounded, not fear-mongering)
- Strengthen weak health planets with their day/mantra/colour (Sun: Sunday, Gayatri mantra, copper)
- Align diet with dosha; if Pitta dominant, cooling foods (avoid excess spice/heat)
- **Gemstones**: only mention specific gemstones if the user asks, and always say "consult a qualified
  Jyotish astrologer before wearing" — stones are potent and contraindicated for some charts
- For Saturn-related chronic conditions: Shani mantra on Saturdays, service, dark-coloured foods

---

## C. BaZi Health (Five Elements balance)

Element imbalance = health pattern. The engine returns `element_balance` and `dominant_element`:

| Missing / Weak element | Health tendency |
| --- | --- |
| Wood (missing) | Liver, gallbladder, eyes, tendons; depression, lack of creative drive |
| Fire (missing) | Heart, small intestine, circulation; anxiety, cold extremities |
| Earth (missing) | Spleen, stomach, digestion; worry loops, overthinking |
| Metal (missing) | Lungs, large intestine, skin; grief, immune weakness, respiratory |
| Water (missing) | Kidneys, bladder, bones, adrenals; fear, chronic fatigue, low back |

**Flooding element** (excess): same organ system but in a different direction — overactivity,
inflammation, or burnout in that system's domain.

**Day Master and health**: A Weak Day Master is already depleted — the person tires easily,
must guard energy. A Strong Day Master may have excess that manifests as inflammation or
aggression if not channelled. The Useful God element is also the health-restorative element:
surround yourself with it (food, environment, activity).

**Annual health outlook**: If the current annual pillar or luck pillar's elements control or
exhaust the Day Master element badly, take extra care. If they support the Useful God, a year
of improved vitality.

---

## Ethics & framing

- **Never** state "your chart shows you will have [disease X]." Say "this placement suggests
  a tendency to watch [area Y] — practical self-care in this direction is wise."
- **Longevity questions** (Q28): avoid specific age predictions entirely. Say: "classical texts
  examine the 8th house and lagna lord's strength for long life indicators; your chart shows
  [strong/weak] vitality indications — but longevity is medicine and lifestyle as much as karma."
- **Chronic illness timing**: when does it ease? Use Saturn transit + dasha exit dates. Frame
  as "a season of particular demand on [system]" with a specific end date from the engine.
- **Real medical crisis overrides the chart**: always recommend a doctor first. The chart
  contextualises; it doesn't replace diagnosis.
