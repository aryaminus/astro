#!/usr/bin/env python3
"""
Astrology Engine — Deterministic Calculation Backend
=====================================================
Systems: Western Tropical · Vedic (Jyotisha / Lahiri sidereal) · Chinese BaZi

DESIGN PRINCIPLE — separate the math from the meaning.
  The LLM must NEVER guess planetary positions. This engine computes them.
  Interpretation (turning these numbers into language) happens in the SKILL,
  grounded against the reference rulesets. This file only does math + lookups.

PRECISION / DEPENDENCIES.
  Primary path is ZERO-DEPENDENCY pure Python (stdlib only): a compact
  geocentric ephemeris (Paul Schlyter's algorithms + standard perturbation
  terms) accurate to ~1-2 arcminutes for the Sun, Moon and classical planets,
  ~tens of arcsec→arcmin for outers, well within the tolerance needed for
  sign / house / nakshatra / dasha determination (the coarsest bucket is the
  13°20' nakshatra; signs are 30°).

  If `swisseph` (pyswisseph) is importable it is used instead for
  arcsecond-grade precision and true nodes. The engine auto-detects; output
  records which backend produced the numbers under "_meta".

Usage:
  python3 astro_engine.py --json '<birth_data_json>'
  python3 astro_engine.py --file birth.json
  python3 astro_engine.py            # demo chart

Input JSON (natal):
  {
    "name": "optional label",
    "year": 1990, "month": 6, "day": 15,
    "hour": 14, "minute": 30,           # local clock time at birth place
    "lat": 40.7128, "lng": -74.0060,    # degrees, E+ / N+
    "tz": "America/New_York",           # IANA name (preferred) OR
    "utc_offset": -4,                   #   numeric hours, OR omit to estimate
    "time_known": true,                 # set false if birth time unknown
    "systems": ["western","vedic","bazi"],
    "gender": "male"                    # affects BaZi luck-pillar direction only
  }

Other modes (set "mode"):
  "natal"           (default) — full chart, per "systems"; includes aspect patterns,
                                Part of Fortune, Vertex, moon phase, equal houses,
                                navamsa, and panchang automatically
  "transit"  + "transit_date" — current sky vs the natal chart
  "synastry" + "partner": {…} — relationship comparison of two charts
  "compatibility" + "partner": {…} — detailed 0-100 compatibility scoring with subscores
  "astrocartography"          — planet lines on the globe (relocation)
  "horary"     + (lat/lng at the moment)  — chart of the moment a question is asked
  "event"                       — chart for any "moment of inception"
  "solar_return" + "target_year" — annual solar return chart
  "lunar_return" + "target_year" + "target_month" — monthly lunar return chart
  "navamsa"                     — Vedic D9 navamsa chart with vargottama detection
  "panchang"                    — complete Vedic panchang (Tithi, Nakshatra, Yoga, Karana)
  "moon_phase"                  — current moon phase + upcoming phases
  "numerology"                  — Life Path, Personal Year, Expression, Soul Urge
                                (pass "full_name" for name-based numbers)
  "composite"  + "partner": {…} — midpoint relationship chart
  "progressions" + "target_age" — secondary progressions (1 day = 1 year)
  "planetary_return" + "planet" + "target_year" — return chart for any planet
  "varga" + "varga"             — Vedic divisional chart (D2-D60)
  "planetary_hours"             — Chaldean planetary hours for the day
  "transit_natal_aspects" + "transit_date" — detailed transit-to-natal aspect listing

Extra natal options:
  "include_numerology": true    — adds numerology block to natal output
  "full_name": "..."            — full name for numerology Expression/Soul Urge

Specialty lookups (callable directly, not via JSON mode):
  namakaran(moon_lon_sidereal)            — name syllables from birth nakshatra
  anatomy_chart(planets_block)            — body regions and afflicted systems
  horary(question_utc, lat, lng, text)    — cast + basic signals of a horary chart
  astrocartography(jd, lat, lng)          — planet lines for relocation
  detect_aspect_patterns(lons, ayan=0)    — Grand Trine, T-Square, Yod, etc.
  solar_return(natal_jd, year, lat, lng)  — annual solar return
  lunar_return(natal_jd, year, month, lat, lng) — monthly lunar return
  compatibility_score(jdA, jdB)           — detailed compatibility scoring
  part_of_fortune(sun, moon, asc, sect)   — Lot of Fortune (day/night)
  vertex(jd, lat, lng)                    — Vertex (fated encounters)
  moon_phase(jd)                          — 8-phase lunar cycle data
  navamsa_chart(jd, lat, lng)             — D9 divisional chart
  panchang_elements(jd)                   — Tithi, Nakshatra, Yoga, Karana
  numerology(year, month, day, name)      — Life Path, Personal Year, etc.
  equal_houses(asc_lon)                   — Equal house cusps
  composite_chart(jdA, jdB, latA, lngA, latB, lngB) — midpoint relationship chart
  black_moon_lilith(jd)                   — Mean BML position
  secondary_progressions(jd, age, lat, lng) — 1 day = 1 year
  planetary_return(jd, planet, year, lat, lng) — any planet's return
  compute_arabic_parts(lons, asc, sect)   — 10 Arabic Parts / Lots
  fixed_star_conjunctions(lons, orb)      — 23 fixed stars
  mangal_dosha(jd, lat, lng)             — Kuja/Mars dosha check
  kaalsarpa_dosha(jd, lat, lng)          — Kaalsarpa dosha check
  varga_chart(jd, varga, lat, lng)       — D2–D60 divisional charts
  transit_to_natal_aspects(natal_jd, transit_jd) — detailed transit aspects
  planetary_hours(jd, lat, lng)          — Chaldean planetary hours
"""

from __future__ import annotations
import json
import sys
import math
import argparse
from datetime import datetime, timedelta, timezone

# ── optional high-precision backend ──────────────────────────────────────────
try:
    import swisseph as swe  # type: ignore
    _HAS_SWE = True
except Exception:
    swe = None  # type: ignore
    _HAS_SWE = False

try:
    from zoneinfo import ZoneInfo
    _HAS_TZDB = True
except Exception:
    _HAS_TZDB = False

TODAY = datetime.now(timezone.utc).replace(tzinfo=None)

# ═════════════════════════════════════════════════════════════════════════════
#  SECTION A — WESTERN INTERPRETIVE DATA
# ═════════════════════════════════════════════════════════════════════════════

SIGNS = ["Aries","Taurus","Gemini","Cancer","Leo","Virgo",
         "Libra","Scorpio","Sagittarius","Capricorn","Aquarius","Pisces"]
SIGN_ABBR = ["Ari","Tau","Gem","Can","Leo","Vir","Lib","Sco","Sag","Cap","Aqu","Pis"]

SIGN_DATA = {
    "Aries":      {"element":"Fire","modality":"Cardinal","ruler":"Mars","polarity":"Yang",
                   "keywords":"boldness, initiative, raw energy, pioneering drive, impatience"},
    "Taurus":     {"element":"Earth","modality":"Fixed","ruler":"Venus","polarity":"Yin",
                   "keywords":"stability, sensuality, patience, material security, stubbornness"},
    "Gemini":     {"element":"Air","modality":"Mutable","ruler":"Mercury","polarity":"Yang",
                   "keywords":"duality, curiosity, communication, adaptability, restlessness"},
    "Cancer":     {"element":"Water","modality":"Cardinal","ruler":"Moon","polarity":"Yin",
                   "keywords":"nurturing, intuition, emotional memory, home, defensiveness"},
    "Leo":        {"element":"Fire","modality":"Fixed","ruler":"Sun","polarity":"Yang",
                   "keywords":"creativity, leadership, pride, warmth, generosity, ego"},
    "Virgo":      {"element":"Earth","modality":"Mutable","ruler":"Mercury","polarity":"Yin",
                   "keywords":"precision, service, health, discernment, self-criticism"},
    "Libra":      {"element":"Air","modality":"Cardinal","ruler":"Venus","polarity":"Yang",
                   "keywords":"balance, justice, partnership, harmony, indecision"},
    "Scorpio":    {"element":"Water","modality":"Fixed","ruler":"Mars/Pluto","polarity":"Yin",
                   "keywords":"depth, transformation, power, hidden truths, control"},
    "Sagittarius":{"element":"Fire","modality":"Mutable","ruler":"Jupiter","polarity":"Yang",
                   "keywords":"expansion, philosophy, freedom, truth-seeking, excess"},
    "Capricorn":  {"element":"Earth","modality":"Cardinal","ruler":"Saturn","polarity":"Yin",
                   "keywords":"ambition, discipline, structure, authority, coldness"},
    "Aquarius":   {"element":"Air","modality":"Fixed","ruler":"Saturn/Uranus","polarity":"Yang",
                   "keywords":"innovation, humanitarian ideals, detachment, originality"},
    "Pisces":     {"element":"Water","modality":"Mutable","ruler":"Jupiter/Neptune","polarity":"Yin",
                   "keywords":"compassion, spirituality, imagination, dissolution, escapism"},
}

PLANET_ARCHETYPES = {
    "Sun":"identity, ego, vitality, the father, conscious will",
    "Moon":"emotion, instinct, the mother, subconscious, needs, habits",
    "Mercury":"mind, communication, intellect, learning, siblings",
    "Venus":"love, beauty, values, art, money, what we attract",
    "Mars":"drive, desire, action, conflict, sex, the warrior",
    "Jupiter":"expansion, luck, philosophy, faith, abundance",
    "Saturn":"discipline, karma, restriction, time, responsibility, fear",
    "Uranus":"rebellion, innovation, sudden change, awakening, freedom",
    "Neptune":"dreams, illusion, spirituality, compassion, dissolution",
    "Pluto":"transformation, power, death/rebirth, shadow, obsession",
    "North Node":"soul's growth edge, karmic direction, the unfamiliar",
    "South Node":"karmic past, innate gifts, comfort zone to release",
    "Chiron":"the wounded healer — deepest wound becomes greatest medicine",
}

HOUSE_MEANINGS = {
    1:"Self, body, identity, vitality, first impressions, how the world sees you",
    2:"Money, possessions, values, self-worth, material security, talents",
    3:"Communication, siblings, short trips, local life, early learning, the mind",
    4:"Home, roots, family, ancestry, the inner foundation, one parent",
    5:"Creativity, romance, children, pleasure, play, self-expression",
    6:"Health, daily work, routine, service, habits, the body's maintenance",
    7:"Partnership, marriage, open enemies, contracts, the significant other",
    8:"Death/rebirth, shared resources, intimacy, the occult, others' money, crisis",
    9:"Philosophy, higher study, long travel, religion, meaning, the foreign",
    10:"Career, public role, reputation, authority, legacy, one parent",
    11:"Friends, groups, networks, hopes, causes, the collective, gains",
    12:"The unconscious, solitude, spirituality, self-undoing, institutions, the hidden",
}

ASPECTS = {  # name: (exact angle, default orb degrees, nature)
    "conjunction":(0,8,"fusion — energies merge, amplified, unified"),
    "opposition":(180,8,"tension & awareness through the other; need for balance"),
    "trine":(120,7,"natural flow, ease, talent, harmony — can be lazy"),
    "square":(90,7,"friction, drive, growth forced through struggle"),
    "sextile":(60,5,"opportunity, cooperation if acted on"),
    "quincunx":(150,3,"awkward adjustment, unrelated energies needing constant tuning"),
}

# Essential dignities (classical) — rulership, exaltation, detriment, fall
DIGNITY = {
    "Sun":     {"rule":["Leo"],"exalt":["Aries"],"detri":["Aquarius"],"fall":["Libra"]},
    "Moon":    {"rule":["Cancer"],"exalt":["Taurus"],"detri":["Capricorn"],"fall":["Scorpio"]},
    "Mercury": {"rule":["Gemini","Virgo"],"exalt":["Virgo"],"detri":["Sagittarius","Pisces"],"fall":["Pisces"]},
    "Venus":   {"rule":["Taurus","Libra"],"exalt":["Pisces"],"detri":["Aries","Scorpio"],"fall":["Virgo"]},
    "Mars":    {"rule":["Aries","Scorpio"],"exalt":["Capricorn"],"detri":["Taurus","Libra"],"fall":["Cancer"]},
    "Jupiter": {"rule":["Sagittarius","Pisces"],"exalt":["Cancer"],"detri":["Gemini","Virgo"],"fall":["Capricorn"]},
    "Saturn":  {"rule":["Capricorn","Aquarius"],"exalt":["Libra"],"detri":["Cancer","Leo"],"fall":["Aries"]},
}

SATURN_RETURN_AGES = [29, 58, 87]   # ~29.5 yr Saturn cycle
JUPITER_RETURN_AGES = [12, 24, 36, 48, 60, 72, 84]
NODE_RETURN_AGES = [18.6, 37.2, 55.8, 74.4]   # ~18.6 yr nodal cycle (incl. ~mid 'nodal reversal')

# Western anatomy — zodiac sign → body part (classical rulerships)
# Used in medical astrology: avoid surgery when Moon transits the sign ruling
# the body part, and to read which body systems a chart emphasises.
ANATOMY = {
    "Aries":      {"region":"head, brain, eyes, face, adrenals",
                   "system":"nervous / muscular, acute inflammation, fevers"},
    "Taurus":     {"region":"neck, throat, vocal cords, thyroid, jaw, ears",
                   "system":"throat, lymphatic, lower jaw"},
    "Gemini":     {"region":"lungs, shoulders, arms, hands, nervous system",
                   "system":"respiratory, peripheral nerves"},
    "Cancer":     {"region":"chest, breasts, stomach, ribs, womb, lymph",
                   "system":"digestion, fluids, the body's emotional barometer"},
    "Leo":        {"region":"heart, upper back, spine, circulation",
                   "system":"cardiovascular, vitality"},
    "Virgo":      {"region":"abdomen, intestines, spleen, solar plexus, hands",
                   "system":"digestive, assimilation, hygiene, daily routine"},
    "Libra":      {"region":"kidneys, lower back, adrenals, skin, buttocks",
                   "system":"filtration, balance, glucose regulation"},
    "Scorpio":    {"region":"reproductive organs, bladder, rectum, pelvis, nose",
                   "system":"eliminative, sexual, transformative"},
    "Sagittarius":{"region":"hips, thighs, liver, sciatic nerve, sacrum",
                   "system":"locomotion, hepatic, the traveller's body"},
    "Capricorn":  {"region":"knees, bones, joints, teeth, skin, hair",
                   "system":"skeletal, structural, chronic"},
    "Aquarius":    {"region":"ankles, calves, circulation, electrical system",
                   "system":"nervous, circulatory, sudden/electrical"},
    "Pisces":     {"region":"feet, toes, lymphatic, immune system, the psyche",
                   "system":"immune, psychosomatic, the body's porous boundary"},
}
# Avoid-surgery rule: when Moon is in the sign ruling the body part
# (or afflicting its ruler), defer non-emergency surgery. Also: never operate
# during a lunar eclipse, and prefer Moon in a fixed sign for stability.

# ═════════════════════════════════════════════════════════════════════════════
#  SECTION B — VEDIC (JYOTISHA) DATA
# ═════════════════════════════════════════════════════════════════════════════

NAKSHATRAS = [
    {"name":"Ashwini","lord":"Ketu","deity":"Ashwini Kumaras","symbol":"Horse's head",
     "quality":"swift healing, fresh starts, vitality, restless pioneering"},
    {"name":"Bharani","lord":"Venus","deity":"Yama","symbol":"Yoni",
     "quality":"bearing burdens, fertility, restraint, transformation through endurance"},
    {"name":"Krittika","lord":"Sun","deity":"Agni","symbol":"Razor / flame",
     "quality":"purifying fire, sharp focus, cutting through illusion, ambition"},
    {"name":"Rohini","lord":"Moon","deity":"Brahma","symbol":"Ox-cart / chariot",
     "quality":"growth, beauty, sensual abundance, magnetism, materiality"},
    {"name":"Mrigashira","lord":"Mars","deity":"Soma","symbol":"Deer's head",
     "quality":"seeking, gentle curiosity, wandering, artistic restlessness"},
    {"name":"Ardra","lord":"Rahu","deity":"Rudra","symbol":"Teardrop / diamond",
     "quality":"storm and renewal, raw emotion, destruction that clears the way"},
    {"name":"Punarvasu","lord":"Jupiter","deity":"Aditi","symbol":"Quiver of arrows",
     "quality":"return of light, resilience, optimism, expansion after loss"},
    {"name":"Pushya","lord":"Saturn","deity":"Brihaspati","symbol":"Cow's udder / lotus",
     "quality":"nourishment, devotion, disciplined growth — most auspicious nakshatra"},
    {"name":"Ashlesha","lord":"Mercury","deity":"Nagas","symbol":"Coiled serpent",
     "quality":"penetrating insight, kundalini, hypnotic power, possible cunning"},
    {"name":"Magha","lord":"Ketu","deity":"Pitris (ancestors)","symbol":"Throne",
     "quality":"ancestral power, lineage, pride, the karma of the forefathers"},
    {"name":"Purva Phalguni","lord":"Venus","deity":"Bhaga","symbol":"Front of a bed",
     "quality":"pleasure, romance, rest, creative enjoyment, generosity"},
    {"name":"Uttara Phalguni","lord":"Sun","deity":"Aryaman","symbol":"Back of a bed",
     "quality":"contracts, partnership, patronage, generous service, stability"},
    {"name":"Hasta","lord":"Moon","deity":"Savitar","symbol":"Hand",
     "quality":"skill, craft, healing hands, cleverness, manifesting by hand"},
    {"name":"Chitra","lord":"Mars","deity":"Tvastar","symbol":"Bright jewel",
     "quality":"artistry, design, dazzling charisma, creating beauty/structure"},
    {"name":"Swati","lord":"Rahu","deity":"Vayu","symbol":"Young shoot in wind",
     "quality":"independence, flexibility, trade, self-made movement"},
    {"name":"Vishakha","lord":"Jupiter","deity":"Indra-Agni","symbol":"Triumphal archway",
     "quality":"goal-driven intensity, ambition, harvest after patient effort"},
    {"name":"Anuradha","lord":"Saturn","deity":"Mitra","symbol":"Lotus / staff",
     "quality":"devoted friendship, organisation, success abroad, occult devotion"},
    {"name":"Jyeshtha","lord":"Mercury","deity":"Indra","symbol":"Circular amulet","quality":
     "seniority, protectiveness, responsibility, hidden power, isolation"},
    {"name":"Mula","lord":"Ketu","deity":"Nirriti","symbol":"Bunch of roots",
     "quality":"getting to the root, dissolution, investigation, tearing down to rebuild"},
    {"name":"Purva Ashadha","lord":"Venus","deity":"Apas","symbol":"Fan / winnowing basket",
     "quality":"invincibility, conviction, purification, early victory"},
    {"name":"Uttara Ashadha","lord":"Sun","deity":"Vishvadevas","symbol":"Elephant tusk",
     "quality":"lasting victory, integrity, leadership grounded in principle"},
    {"name":"Shravana","lord":"Moon","deity":"Vishnu","symbol":"Ear / three footprints",
     "quality":"deep listening, learning, connection, preservation of wisdom"},
    {"name":"Dhanishtha","lord":"Mars","deity":"Eight Vasus","symbol":"Drum",
     "quality":"rhythm, wealth, music, group leadership, abundance, ambition"},
    {"name":"Shatabhisha","lord":"Rahu","deity":"Varuna","symbol":"Empty circle / 100 stars",
     "quality":"healing, mysticism, solitude, secrets, scientific detachment"},
    {"name":"Purva Bhadrapada","lord":"Jupiter","deity":"Aja Ekapada","symbol":"Front of a funeral cot",
     "quality":"spiritual fire, intensity, idealism, eccentric vision"},
    {"name":"Uttara Bhadrapada","lord":"Saturn","deity":"Ahir Budhnya","symbol":"Back of a funeral cot",
     "quality":"deep calm, wisdom from depth, endurance, cosmic compassion"},
    {"name":"Revati","lord":"Mercury","deity":"Pushan","symbol":"Fish / drum",
     "quality":"safe passage, nourishment, completion, gentle guidance, journeys' end"},
]
NAK_ARC = 360.0 / 27.0          # 13°20'
PADA_ARC = NAK_ARC / 4.0        # 3°20'

# Namakaran — nakshatra → pada → starting syllables for the child's name.
# Classical rule (Brihat Parashara Hora Shastra): the baby's name begins with
# the syllable of the Moon's birth-nakshatra pada. The syllable is also used
# for naming a business, art project, etc. (the *vibrational frequency* of
# the natal lunar mansion).
NAKSHATRA_SYLLABLES = {
    "Ashwini":         ["Chu","Che","Cho","La"],
    "Bharani":         ["Li","Lu","Le","Lo"],
    "Krittika":        ["A","E","U","O"],
    "Rohini":          ["O","Va","Vi","Vu"],
    "Mrigashira":      ["Ve","Vo","Ka","Ki"],
    "Ardra":           ["Ku","Gha","An","Chha"],
    "Punarvasu":       ["Ke","Ko","Ha","Hi"],
    "Pushya":          ["Hu","He","Ho","Da"],
    "Ashlesha":        ["Di","Du","De","Do"],
    "Magha":           ["Ma","Mi","Mu","Me"],
    "Purva Phalguni":  ["Mo","Ta","Ti","Tu"],
    "Uttara Phalguni": ["Te","To","Pa","Pi"],
    "Hasta":           ["Pu","Sha","An","Tha"],
    "Chitra":          ["Pe","Po","Ra","Ri"],
    "Swati":           ["Ru","Re","Ro","Ta"],
    "Vishakha":        ["Ti","Tu","Te","To"],
    "Anuradha":        ["Na","Ni","Nu","Ne"],
    "Jyeshtha":        ["No","Ya","Yi","Yu"],
    "Mula":            ["Ye","Yo","Ba","Bi"],
    "Purva Ashadha":   ["Bu","Da","Bha","Dha"],
    "Uttara Ashadha":  ["Be","Bo","Ja","Ji"],
    "Shravana":        ["Ju","Je","Jo","Khi"],
    "Dhanishtha":      ["Ga","Gi","Gu","Ge"],
    "Shatabhisha":     ["Go","Sa","Si","Su"],
    "Purva Bhadrapada":["Se","So","Dha","Dhi"],
    "Uttara Bhadrapada":["Du","Tha","Jha","Na"],
    "Revati":          ["De","Do","Cha","Chi"],
}

DASHA_YEARS = {"Ketu":7,"Venus":20,"Sun":6,"Moon":10,"Mars":7,
               "Rahu":18,"Jupiter":16,"Saturn":19,"Mercury":17}
DASHA_SEQ = ["Ketu","Venus","Sun","Moon","Mars","Rahu","Jupiter","Saturn","Mercury"]
DASHA_TOTAL = 120

RASHI_LORDS = {"Aries":"Mars","Taurus":"Venus","Gemini":"Mercury","Cancer":"Moon",
    "Leo":"Sun","Virgo":"Mercury","Libra":"Venus","Scorpio":"Mars","Sagittarius":"Jupiter",
    "Capricorn":"Saturn","Aquarius":"Saturn","Pisces":"Jupiter"}

GRAHA_KARAKAS = {
    "Sun":"Atma (soul), father, authority, vitality, government",
    "Moon":"mind, mother, emotions, the public, nourishment",
    "Mars":"energy, siblings, courage, land, conflict",
    "Mercury":"speech, intellect, business, education",
    "Jupiter":"wisdom, children, wealth, dharma, the guru",
    "Venus":"spouse, love, luxury, art, vehicles, pleasure",
    "Saturn":"longevity, discipline, suffering, service, karma",
    "Rahu":"obsession, foreign things, illusion, sudden gain, ambition",
    "Ketu":"liberation, spirituality, loss, past-life skill, moksha",
}

VEDIC_HOUSE = {
    1:"Tanu — self, body, personality, life-direction",
    2:"Dhana — wealth, family, speech, food, early life",
    3:"Sahaja — courage, siblings, effort, skills, communication",
    4:"Sukha — mother, home, happiness, vehicles, heart, schooling",
    5:"Putra — children, intelligence, romance, past-life merit (purva punya)",
    6:"Ari — enemies, debt, disease, service, daily work, obstacles overcome",
    7:"Yuvati — spouse, partnership, business, the public, travel",
    8:"Ayur — longevity, transformation, the hidden, inheritance, sudden events",
    9:"Bhagya — fortune, dharma, father, guru, higher learning, pilgrimage",
    10:"Karma — career, status, reputation, action in the world",
    11:"Labha — gains, income, networks, elder siblings, fulfilment of desire",
    12:"Vyaya — loss, expense, foreign lands, solitude, liberation, the bed",
}

EXALT_SIGN = {"Sun":"Aries","Moon":"Taurus","Mars":"Capricorn","Mercury":"Virgo",
    "Jupiter":"Cancer","Venus":"Pisces","Saturn":"Libra","Rahu":"Taurus","Ketu":"Scorpio"}
DEBIL_SIGN = {"Sun":"Libra","Moon":"Scorpio","Mars":"Cancer","Mercury":"Pisces",
    "Jupiter":"Capricorn","Venus":"Virgo","Saturn":"Aries","Rahu":"Scorpio","Ketu":"Taurus"}

# ═════════════════════════════════════════════════════════════════════════════
#  SECTION C — CHINESE BAZI DATA
# ═════════════════════════════════════════════════════════════════════════════

STEMS = [
    {"han":"甲","pinyin":"Jiǎ","element":"Wood","polarity":"Yang","nature":"the great tree — upright leadership, growth, pioneering"},
    {"han":"乙","pinyin":"Yǐ","element":"Wood","polarity":"Yin","nature":"the vine/grass — adaptable, persistent, diplomatic"},
    {"han":"丙","pinyin":"Bǐng","element":"Fire","polarity":"Yang","nature":"the sun — radiant, generous, expressive, warm"},
    {"han":"丁","pinyin":"Dīng","element":"Fire","polarity":"Yin","nature":"the lamp/candle — focused, refined, illuminating"},
    {"han":"戊","pinyin":"Wù","element":"Earth","polarity":"Yang","nature":"the mountain — solid, dependable, steadfast"},
    {"han":"己","pinyin":"Jǐ","element":"Earth","polarity":"Yin","nature":"the field/soil — nurturing, receptive, productive"},
    {"han":"庚","pinyin":"Gēng","element":"Metal","polarity":"Yang","nature":"the axe/sword — decisive, righteous, forceful"},
    {"han":"辛","pinyin":"Xīn","element":"Metal","polarity":"Yin","nature":"the jewel — refined, sensitive, precise, elegant"},
    {"han":"壬","pinyin":"Rén","element":"Water","polarity":"Yang","nature":"the ocean/river — strategic, resourceful, flowing"},
    {"han":"癸","pinyin":"Guǐ","element":"Water","polarity":"Yin","nature":"the rain/mist — gentle, wise, penetrating, intuitive"},
]
BRANCHES = [
    {"han":"子","pinyin":"Zǐ","animal":"Rat","element":"Water","hidden":["Guǐ"],"hours":"23:00–00:59"},
    {"han":"丑","pinyin":"Chǒu","animal":"Ox","element":"Earth","hidden":["Jǐ","Guǐ","Xīn"],"hours":"01:00–02:59"},
    {"han":"寅","pinyin":"Yín","animal":"Tiger","element":"Wood","hidden":["Jiǎ","Bǐng","Wù"],"hours":"03:00–04:59"},
    {"han":"卯","pinyin":"Mǎo","animal":"Rabbit","element":"Wood","hidden":["Yǐ"],"hours":"05:00–06:59"},
    {"han":"辰","pinyin":"Chén","animal":"Dragon","element":"Earth","hidden":["Wù","Yǐ","Guǐ"],"hours":"07:00–08:59"},
    {"han":"巳","pinyin":"Sì","animal":"Snake","element":"Fire","hidden":["Bǐng","Wù","Gēng"],"hours":"09:00–10:59"},
    {"han":"午","pinyin":"Wǔ","animal":"Horse","element":"Fire","hidden":["Dīng","Jǐ"],"hours":"11:00–12:59"},
    {"han":"未","pinyin":"Wèi","animal":"Goat","element":"Earth","hidden":["Jǐ","Dīng","Yǐ"],"hours":"13:00–14:59"},
    {"han":"申","pinyin":"Shēn","animal":"Monkey","element":"Metal","hidden":["Gēng","Rén","Wù"],"hours":"15:00–16:59"},
    {"han":"酉","pinyin":"Yǒu","animal":"Rooster","element":"Metal","hidden":["Xīn"],"hours":"17:00–18:59"},
    {"han":"戌","pinyin":"Xū","animal":"Dog","element":"Earth","hidden":["Wù","Xīn","Dīng"],"hours":"19:00–20:59"},
    {"han":"亥","pinyin":"Hài","animal":"Pig","element":"Water","hidden":["Rén","Jiǎ"],"hours":"21:00–22:59"},
]
PINYIN_ELEM = {s["pinyin"]:s["element"] for s in STEMS}

# Wu Xing cycles
GENERATES = {"Wood":"Fire","Fire":"Earth","Earth":"Metal","Metal":"Water","Water":"Wood"}
GENERATED_BY = {v:k for k,v in GENERATES.items()}
CONTROLS = {"Wood":"Earth","Earth":"Water","Water":"Fire","Fire":"Metal","Metal":"Wood"}
CONTROLLED_BY = {v:k for k,v in CONTROLS.items()}

ELEMENT_ADVICE = {
    "Wood":"Strengthen with growth, learning, nature, green foods, the east, planning; weaken by pruning over-extension.",
    "Fire":"Strengthen with sunlight, joy, social warmth, red, the south, expression; weaken by cooling impulsiveness.",
    "Earth":"Strengthen with routine, grounding, yellow/brown foods, the centre, reliability; weaken by avoiding over-worry.",
    "Metal":"Strengthen with structure, precision, white/metal, the west, decluttering; weaken by softening rigidity.",
    "Water":"Strengthen with stillness, study, black/blue, the north, flow, intuition; weaken by avoiding withdrawal.",
}

ZODIAC_COMPAT = {
    "Rat":{"best":["Dragon","Monkey","Ox"],"clash":"Horse","harm":"Goat"},
    "Ox":{"best":["Snake","Rooster","Rat"],"clash":"Goat","harm":"Horse"},
    "Tiger":{"best":["Horse","Dog","Pig"],"clash":"Monkey","harm":"Snake"},
    "Rabbit":{"best":["Goat","Pig","Dog"],"clash":"Rooster","harm":"Dragon"},
    "Dragon":{"best":["Rat","Monkey","Rooster"],"clash":"Dog","harm":"Rabbit"},
    "Snake":{"best":["Ox","Rooster","Monkey"],"clash":"Pig","harm":"Tiger"},
    "Horse":{"best":["Tiger","Dog","Goat"],"clash":"Rat","harm":"Ox"},
    "Goat":{"best":["Rabbit","Pig","Horse"],"clash":"Ox","harm":"Rat"},
    "Monkey":{"best":["Rat","Dragon","Snake"],"clash":"Tiger","harm":"Pig"},
    "Rooster":{"best":["Ox","Snake","Dragon"],"clash":"Rabbit","harm":"Dog"},
    "Dog":{"best":["Tiger","Horse","Rabbit"],"clash":"Dragon","harm":"Rooster"},
    "Pig":{"best":["Rabbit","Goat","Tiger"],"clash":"Snake","harm":"Monkey"},
}

# Ten Gods (十神) relationship of another stem to the Day Master, by element-relation + polarity
def ten_god(dm_elem, dm_pol, other_elem, other_pol):
    same_pol = (dm_pol == other_pol)
    if other_elem == dm_elem:
        return "Friend (比肩)" if same_pol else "Rob Wealth (劫財)"
    if GENERATED_BY[dm_elem] == other_elem:           # resource (feeds DM)
        return "Direct Resource (正印)" if not same_pol else "Indirect Resource (偏印)"
    if GENERATES[dm_elem] == other_elem:              # output (DM produces)
        return "Hurting Officer (傷官)" if not same_pol else "Eating God (食神)"
    if CONTROLS[dm_elem] == other_elem:               # wealth (DM controls)
        return "Direct Wealth (正財)" if not same_pol else "Indirect Wealth (偏財)"
    if CONTROLLED_BY[dm_elem] == other_elem:          # officer (controls DM)
        return "Direct Officer (正官)" if not same_pol else "Seven Killings (七殺)"
    return ""

# Solar-term month boundaries: month branch starts when Sun reaches these tropical longitudes.
# Tiger month (寅, idx 2) begins at Li Chun, Sun = 315°.
SOLAR_TERM_START_LON = 315.0   # Li Chun → start of Tiger month / BaZi solar year

# ═════════════════════════════════════════════════════════════════════════════
#  SECTION D — ASTRONOMY (pure-Python geocentric ephemeris, Schlyter method)
# ═════════════════════════════════════════════════════════════════════════════

def _sin(d): return math.sin(math.radians(d))
def _cos(d): return math.cos(math.radians(d))
def _tan(d): return math.tan(math.radians(d))
def _asin(x): return math.degrees(math.asin(max(-1.0,min(1.0,x))))
def _atan2(y,x): return math.degrees(math.atan2(y,x))
def norm360(x): return x % 360.0
def norm180(x):
    x = x % 360.0
    return x - 360.0 if x > 180 else x

def julian_day(dt_utc: datetime) -> float:
    """JD (UT) from a naive UTC datetime."""
    y, m = dt_utc.year, dt_utc.month
    d = (dt_utc.day + dt_utc.hour/24 + dt_utc.minute/1440
         + dt_utc.second/86400 + dt_utc.microsecond/86400e6)
    if m <= 2:
        y -= 1; m += 12
    a = y // 100
    b = 2 - a + a // 4
    return (math.floor(365.25*(y+4716)) + math.floor(30.6001*(m+1))
            + d + b - 1524.5)

def obliquity(d):   # d = days since 2000 Jan 0.0
    return 23.4393 - 3.563e-7 * d

def _kepler(M_deg, e):
    """Solve Kepler's equation E - e·sin E = M. M in deg, e dimensionless.
    Solved in radians (correct Newton derivative), returned in degrees."""
    M = math.radians(norm360(M_deg))
    E = M + e*math.sin(M)*(1 + e*math.cos(M))
    for _ in range(12):
        dE = (E - e*math.sin(E) - M) / (1 - e*math.cos(E))
        E -= dE
        if abs(dE) < 1e-11:
            break
    return math.degrees(E)

def _orbit_xyz(N,i,w,a,e,M):
    """Heliocentric ecliptic rectangular coords from orbital elements (deg)."""
    E = _kepler(M, e)
    xv = a*(_cos(E) - e)
    yv = a*(math.sqrt(1-e*e)*_sin(E))
    v = _atan2(yv, xv)
    r = math.hypot(xv, yv)
    xh = r*(_cos(N)*_cos(v+w) - _sin(N)*_sin(v+w)*_cos(i))
    yh = r*(_sin(N)*_cos(v+w) + _cos(N)*_sin(v+w)*_cos(i))
    zh = r*(_sin(v+w)*_sin(i))
    return xh, yh, zh, r, v

def _sun(d):
    w = 282.9404 + 4.70935e-5*d
    e = 0.016709 - 1.151e-9*d
    M = norm360(356.0470 + 0.9856002585*d)
    E = _kepler(M, e)
    xv = _cos(E) - e
    yv = math.sqrt(1-e*e)*_sin(E)
    v = _atan2(yv, xv)
    r = math.hypot(xv, yv)
    lon = norm360(v + w)
    # geocentric Sun rectangular (ecliptic)
    xs = r*_cos(lon); ys = r*_sin(lon)
    return {"lon":lon, "r":r, "xs":xs, "ys":ys, "M":M, "L":norm360(w+M)}

# Planetary orbital elements as functions of d ────────────────────────────────
def _elems(body, d):
    E = {
    "Mercury":(48.3313+3.24587e-5*d, 7.0047+5.00e-8*d, 29.1241+1.01444e-5*d,
               0.387098, 0.205635+5.59e-10*d, 168.6562+4.0923344368*d),
    "Venus":(76.6799+2.46590e-5*d, 3.3946+2.75e-8*d, 54.8910+1.38374e-5*d,
             0.723330, 0.006773-1.302e-9*d, 48.0052+1.6021302244*d),
    "Mars":(49.5574+2.11081e-5*d, 1.8497-1.78e-8*d, 286.5016+2.92961e-5*d,
            1.523688, 0.093405+2.516e-9*d, 18.6021+0.5240207766*d),
    "Jupiter":(100.4542+2.76854e-5*d, 1.3030-1.557e-7*d, 273.8777+1.64505e-5*d,
               5.20256, 0.048498+4.469e-9*d, 19.8950+0.0830853001*d),
    "Saturn":(113.6634+2.38980e-5*d, 2.4886-1.081e-7*d, 339.3939+2.97661e-5*d,
              9.55475, 0.055546-9.499e-9*d, 316.9670+0.0334442282*d),
    "Uranus":(74.0005+1.3978e-5*d, 0.7733+1.9e-8*d, 96.6612+3.0565e-5*d,
              19.18171-1.55e-8*d, 0.047318+7.45e-9*d, 142.5905+0.011725806*d),
    "Neptune":(131.7806+3.0173e-5*d, 1.7700-2.55e-7*d, 272.8461-6.027e-6*d,
               30.05826+3.313e-8*d, 0.008606+2.15e-9*d, 260.2471+0.005995147*d),
    }[body]
    return E

def _planet_geo_lon(body, d, sun):
    N,i,w,a,e,M = _elems(body, d)
    M = norm360(M)
    xh,yh,zh,r,v = _orbit_xyz(N,i,w,a,e,M)
    # geocentric
    xg = xh + sun["xs"]; yg = yh + sun["ys"]; zg = zh
    lon = norm360(_atan2(yg, xg))
    # perturbations (Schlyter) for the big bodies
    Mj = norm360(19.8950+0.0830853001*d)
    Msa = norm360(316.9670+0.0334442282*d)
    Mu = norm360(142.5905+0.011725806*d)
    pert = 0.0
    if body == "Jupiter":
        pert = (-0.332*_sin(2*Mj-5*Msa-67.6) -0.056*_sin(2*Mj-2*Msa+21)
                +0.042*_sin(3*Mj-5*Msa+21) -0.036*_sin(Mj-2*Msa)
                +0.022*_cos(Mj-Msa) +0.023*_sin(2*Mj-3*Msa+52)
                -0.016*_sin(Mj-5*Msa-69))
    elif body == "Saturn":
        pert = (+0.812*_sin(2*Mj-5*Msa-67.6) -0.229*_cos(2*Mj-4*Msa-2)
                +0.119*_sin(Mj-2*Msa-3) +0.046*_sin(2*Mj-6*Msa-69)
                +0.014*_sin(Mj-3*Msa+32))
    elif body == "Uranus":
        pert = (+0.040*_sin(Msa-2*Mu+6) +0.035*_sin(Msa-3*Mu+33)
                -0.015*_sin(Mj-Mu+20))
    return norm360(lon + pert)

def _moon_geo_lon(d, sun):
    N = 125.1228 - 0.0529538083*d
    i = 5.1454
    w = 318.0634 + 0.1643573223*d
    a = 60.2666
    e = 0.054900
    M = norm360(115.3654 + 13.0649929509*d)
    xh,yh,zh,r,v = _orbit_xyz(N,i,w,a,e,M)
    lon = norm360(_atan2(yh, xh))
    lat = _atan2(zh, math.hypot(xh,yh))
    # perturbation arguments
    Ls = sun["L"]; Lm = norm360(N+w+M); Ms = sun["M"]; Mm = M
    D = norm360(Lm - Ls); F = norm360(Lm - N)
    dlon = (-1.274*_sin(Mm-2*D) +0.658*_sin(2*D) -0.186*_sin(Ms)
            -0.059*_sin(2*Mm-2*D) -0.057*_sin(Mm-2*D+Ms) +0.053*_sin(Mm+2*D)
            +0.046*_sin(2*D-Ms) +0.041*_sin(Mm-Ms) -0.035*_sin(D)
            -0.031*_sin(Mm+Ms) -0.015*_sin(2*F-2*D) +0.011*_sin(Mm-4*D))
    return norm360(lon + dlon)

def _node_lon(d):
    """Mean ascending lunar node (Rahu)."""
    return norm360(125.1228 - 0.0529538083*d)

def _chiron_geo_lon(d, sun):
    """Chiron geocentric longitude via Keplerian orbit. ~3° accuracy, sign-level reliable.
    Elements calibrated to JPL J2000 position (~267° Sagittarius). Perihelion ~mid-1994."""
    N = 208.70               # longitude of ascending node (degrees)
    i = 6.93                 # inclination
    w = 339.62               # argument of perihelion
    a = 13.648               # semi-major axis AU
    e = 0.3786               # eccentricity
    M = norm360(39.2 + 0.01955178*d)   # mean anomaly; 39.2° at J2000
    xh, yh, zh, r, v = _orbit_xyz(N, i, w, a, e, M)
    xg = xh + sun["xs"]
    yg = yh + sun["ys"]
    return norm360(_atan2(yg, xg))

def _pluto_geo_lon(d):
    """Schlyter's approximation, valid roughly 1800–2050."""
    S = 50.03 + 0.033459652*d
    P = 238.95 + 0.003968789*d
    lon = (238.9508 + 0.00400703*d
        - 19.799*_sin(P) + 19.848*_cos(P)
        + 0.897*_sin(2*P) - 4.956*_cos(2*P)
        + 0.610*_sin(3*P) + 1.211*_cos(3*P)
        - 0.341*_sin(4*P) - 0.190*_cos(4*P)
        + 0.128*_sin(5*P) - 0.034*_cos(5*P)
        - 0.038*_sin(6*P) + 0.031*_cos(6*P)
        + 0.020*_sin(S-P) - 0.010*_cos(S-P))
    return norm360(lon)

# Tropical geocentric longitudes for all bodies at JD ──────────────────────────
PLANET_ORDER = ["Sun","Moon","Mercury","Venus","Mars","Jupiter","Saturn",
                "Uranus","Neptune","Pluto","North Node","South Node","Chiron"]

def tropical_longitudes(jd):
    """Return {body: longitude_deg} (tropical/geocentric) via builtin ephemeris."""
    d = jd - 2451543.5
    sun = _sun(d)
    out = {"Sun":sun["lon"], "Moon":_moon_geo_lon(d,sun)}
    for p in ["Mercury","Venus","Mars","Jupiter","Saturn","Uranus","Neptune"]:
        out[p] = _planet_geo_lon(p, d, sun)
    out["Pluto"] = _pluto_geo_lon(d)
    node = _node_lon(d)
    out["North Node"] = node
    out["South Node"] = norm360(node+180)
    out["Chiron"] = _chiron_geo_lon(d, sun)
    return out

def longitudes_swe(jd):
    """High-precision longitudes if swisseph present (tropical)."""
    swe.set_ephe_path(None)
    ids = {"Sun":swe.SUN,"Moon":swe.MOON,"Mercury":swe.MERCURY,"Venus":swe.VENUS,
           "Mars":swe.MARS,"Jupiter":swe.JUPITER,"Saturn":swe.SATURN,"Uranus":swe.URANUS,
           "Neptune":swe.NEPTUNE,"Pluto":swe.PLUTO,"North Node":swe.TRUE_NODE,
           "Chiron":swe.CHIRON}
    out = {}
    speed = {}
    for name, pid in ids.items():
        res = swe.calc_ut(jd, pid, swe.FLG_SWIEPH | swe.FLG_SPEED)[0]
        out[name] = res[0] % 360.0
        speed[name] = res[3]
    out["South Node"] = (out["North Node"]+180) % 360.0
    speed["South Node"] = speed["North Node"]
    return out, speed

def body_longitudes(jd):
    """Unified accessor: (longitudes, retro_speed, backend)."""
    if _HAS_SWE:
        try:
            lons, speed = longitudes_swe(jd)
            return lons, speed, "swisseph"
        except Exception:
            pass
    lons = tropical_longitudes(jd)
    # finite-difference speed for retrograde detection
    lons2 = tropical_longitudes(jd + 1.0)
    speed = {b: norm180(lons2[b]-lons[b]) for b in lons}
    return lons, speed, "builtin"

def ayanamsha_lahiri(jd):
    """Lahiri ayanamsha in degrees (Chitrapaksha). Accurate to ~1-2 arcmin."""
    if _HAS_SWE:
        try:
            swe.set_sid_mode(swe.SIDM_LAHIRI)
            return swe.get_ayanamsa_ut(jd)
        except Exception:
            pass
    # polynomial fit: 23.853° at J2000, precessing 50.2388"/yr
    t = (jd - 2451545.0) / 365.25
    return 23.85304 + t * (50.2388/3600.0)

# ── Houses & angles ──────────────────────────────────────────────────────────
def gmst_deg(jd):
    T = (jd - 2451545.0)/36525.0
    g = (280.46061837 + 360.98564736629*(jd-2451545.0)
         + 0.000387933*T*T - (T*T*T)/38710000.0)
    return norm360(g)

def ascendant_mc(jd, lat, lng, ayan=0.0):
    """Return (asc_lon, mc_lon) tropical-minus-ayan (sidereal if ayan>0)."""
    d = jd - 2451543.5
    eps = obliquity(d)
    ramc = norm360(gmst_deg(jd) + lng)             # right ascension of MC
    mc = norm360(_atan2(_sin(ramc), _cos(ramc)*_cos(eps)))
    # Ascendant
    asc = _atan2(_cos(ramc), -(_sin(ramc)*_cos(eps) + _tan(lat)*_sin(eps)))
    asc = norm360(asc)
    # ensure ascendant is the eastern point (≈ ramc+90 region)
    if not (norm360(asc - ramc) < 180):
        asc = norm360(asc + 180)
    return norm360(asc - ayan), norm360(mc - ayan)

def sign_of(lon):
    idx = int(norm360(lon)//30)
    return SIGNS[idx], idx, round(norm360(lon) % 30, 3)

def whole_sign_house(planet_lon, asc_lon):
    asc_sign = int(norm360(asc_lon)//30)
    p_sign = int(norm360(planet_lon)//30)
    return ((p_sign - asc_sign) % 12) + 1

# ═════════════════════════════════════════════════════════════════════════════
#  SECTION E — TIME / INPUT NORMALISATION
# ═════════════════════════════════════════════════════════════════════════════

def to_utc(data):
    """Return (naive UTC datetime, info dict). Handles tz name / offset / estimate."""
    y=data["year"]; mo=data["month"]; d=data["day"]
    h=int(data.get("hour",12)); mi=int(data.get("minute",0))
    info = {"time_known": data.get("time_known", True)}
    if not info["time_known"]:
        h, mi = 12, 0
        info["note"] = "birth time unknown — defaulted to local noon; houses/Asc/Moon-degree are approximate"
    tz = data.get("tz")
    off = data.get("utc_offset")
    naive_local = datetime(y,mo,d,h,mi)
    if tz and _HAS_TZDB:
        try:
            local = naive_local.replace(tzinfo=ZoneInfo(tz))
            utc = local.astimezone(timezone.utc).replace(tzinfo=None)
            info["tz_used"] = tz
            info["utc_offset_applied"] = local.utcoffset().total_seconds()/3600
            return utc, info
        except Exception:
            pass
    if off is None:
        off = round(data.get("lng",0.0)/15.0)
        info["tz_note"] = f"no timezone given — estimated UTC offset {off:+d}h from longitude (may be off; ask user for tz)"
    utc = naive_local - timedelta(hours=off)
    info["utc_offset_applied"] = off
    return utc, info

# ═════════════════════════════════════════════════════════════════════════════
#  SECTION F — CHART BUILDERS
# ═════════════════════════════════════════════════════════════════════════════

def _planet_block(lons, speed, asc_lon, names, ayan=0.0, vedic=False):
    out = {}
    for nm in names:
        lon = norm360(lons[nm] - ayan)
        sign, idx, deg = sign_of(lon)
        retro = speed.get(nm, 0) < 0 if nm not in ("South Node",) else (speed.get("North Node",0) < 0)
        if nm in ("North Node","South Node"):
            retro = True  # nodes are always retrograde by mean motion
        block = {
            "sign": sign, "deg_in_sign": deg, "abs_lon": round(lon,3),
            "house": whole_sign_house(lon, asc_lon),
            "retrograde": retro,
        }
        if vedic:
            nak_i = int(lon // NAK_ARC) % 27
            pada = int((lon % NAK_ARC)//PADA_ARC)+1
            nk = NAKSHATRAS[nak_i]
            block.update({
                "rashi_lord": RASHI_LORDS[sign],
                "nakshatra": nk["name"], "nakshatra_lord": nk["lord"], "pada": pada,
                "karaka": GRAHA_KARAKAS.get(_vedic_name(nm),""),
            })
            vn = _vedic_name(nm)
            if EXALT_SIGN.get(vn)==sign: block["dignity"]="exalted"
            elif DEBIL_SIGN.get(vn)==sign: block["dignity"]="debilitated"
            elif RASHI_LORDS[sign]==vn: block["dignity"]="own sign"
        else:
            block["archetype"] = PLANET_ARCHETYPES.get(nm,"")
            block["dignity"] = dignity_western(nm, sign)
        out[nm] = block
    return out

def _vedic_name(nm):
    return {"North Node":"Rahu","South Node":"Ketu"}.get(nm, nm)

def dignity_western(planet, sign):
    dg = DIGNITY.get(planet)
    if not dg: return ""
    if sign in dg["rule"]: return "domicile (rulership)"
    if sign in dg["exalt"]: return "exalted"
    if sign in dg["detri"]: return "detriment"
    if sign in dg["fall"]: return "fall"
    return ""

def compute_aspects(lons, ayan=0.0, bodies=None):
    bodies = bodies or ["Sun","Moon","Mercury","Venus","Mars","Jupiter","Saturn",
                        "Uranus","Neptune","Pluto","North Node"]
    L = {b: norm360(lons[b]-ayan) for b in bodies if b in lons}
    res = []
    keys = list(L.keys())
    for i in range(len(keys)):
        for j in range(i+1,len(keys)):
            a,b = keys[i],keys[j]
            sep = abs(norm180(L[a]-L[b]))
            for asp,(ang,orb,desc) in ASPECTS.items():
                d = abs(sep-ang)
                if d <= orb:
                    res.append({"a":a,"b":b,"aspect":asp,"orb":round(d,2),
                                "exact_sep":round(sep,2),"meaning":desc,
                                "applying": None})
    res.sort(key=lambda x:x["orb"])
    return res

def western_chart(jd, lat, lng, time_known=True):
    lons, speed, backend = body_longitudes(jd)
    asc_lon, mc_lon = ascendant_mc(jd, lat, lng) if time_known else (lons["Sun"], norm360(lons["Sun"]+270))
    names = ["Sun","Moon","Mercury","Venus","Mars","Jupiter","Saturn",
             "Uranus","Neptune","Pluto","North Node","South Node","Chiron"]
    planets = _planet_block(lons, speed, asc_lon, names, vedic=False)
    asc_sign,_,asc_deg = sign_of(asc_lon)
    mc_sign,_,mc_deg = sign_of(mc_lon)
    # element / modality balance over the 10 planets + Asc
    elem={"Fire":0,"Earth":0,"Air":0,"Water":0}; mod={"Cardinal":0,"Fixed":0,"Mutable":0}
    for nm in ["Sun","Moon","Mercury","Venus","Mars","Jupiter","Saturn","Uranus","Neptune","Pluto"]:
        sd=SIGN_DATA[planets[nm]["sign"]]; elem[sd["element"]]+=1; mod[sd["modality"]]+=1
    sd=SIGN_DATA[asc_sign]; elem[sd["element"]]+=1; mod[sd["modality"]]+=1
    # whole-sign house cusps
    houses={}
    asc_idx=int(asc_lon//30)
    for hnum in range(1,13):
        s=SIGNS[(asc_idx+hnum-1)%12]
        houses[hnum]={"sign":s,"ruler":SIGN_DATA[s]["ruler"],"meaning":HOUSE_MEANINGS[hnum]}
    return {
        "system":"Western Tropical (whole-sign houses)",
        "big_three":{"sun":planets["Sun"]["sign"],"moon":planets["Moon"]["sign"],"rising":asc_sign},
        "ascendant":{"sign":asc_sign,"deg_in_sign":asc_deg,"abs_lon":round(asc_lon,3)},
        "midheaven":{"sign":mc_sign,"deg_in_sign":mc_deg,"abs_lon":round(mc_lon,3)},
        "descendant":{"sign":SIGNS[(asc_idx+6)%12],"deg_in_sign":round(asc_deg,2),
                      "abs_lon":round(norm360(asc_lon+180),3)},
        "imum_coeli":{"sign":SIGNS[(int(mc_lon//30)+6)%12],"deg_in_sign":round(mc_deg,2),
                      "abs_lon":round(norm360(mc_lon+180),3)},
        "chart_ruler": SIGN_DATA[asc_sign]["ruler"],
        "planets":planets,
        "houses":houses,
        "aspects":compute_aspects(lons)[:24],
        "element_balance":elem,"modality_balance":mod,
        "dominant_element":max(elem,key=elem.get),"lacking_element":min(elem,key=elem.get),
    }

def vedic_chart(jd, lat, lng, birth_dt, time_known=True):
    lons, speed, backend = body_longitudes(jd)
    ayan = ayanamsha_lahiri(jd)
    asc_lon, mc_lon = ascendant_mc(jd, lat, lng, ayan) if time_known else (norm360(lons["Sun"]-ayan), 0)
    names=["Sun","Moon","Mercury","Venus","Mars","Jupiter","Saturn","North Node","South Node"]
    planets=_planet_block(lons, speed, asc_lon, names, ayan=ayan, vedic=True)
    # remap node names to Rahu/Ketu in output
    planets["Rahu"]=planets.pop("North Node"); planets["Ketu"]=planets.pop("South Node")
    lagna_sign,_,lagna_deg = sign_of(asc_lon)
    moon_lon = norm360(lons["Moon"]-ayan)
    nak_i=int(moon_lon//NAK_ARC)%27
    pada=int((moon_lon%NAK_ARC)//PADA_ARC)+1
    nk=NAKSHATRAS[nak_i]
    dasha=vimshottari(moon_lon, birth_dt)
    yogas=detect_yogas(planets, lagna_sign)
    # Atmakaraka: planet with highest degree in its sign (excludes Rahu/Ketu)
    atma_candidates = {p: planets[p]["deg_in_sign"] for p in
                       ["Sun","Moon","Mars","Mercury","Jupiter","Venus","Saturn"] if p in planets}
    atmakaraka = max(atma_candidates, key=atma_candidates.get) if atma_candidates else None
    # Sade Sati: Saturn transiting Moon sign ±1 (7.5-yr period)
    moon_sign_idx = SIGNS.index(sign_of(moon_lon)[0])
    current_sat_lon = norm360(body_longitudes(julian_day(TODAY))[0]["Saturn"] - ayanamsha_lahiri(julian_day(TODAY)))
    sat_sign_idx = SIGNS.index(sign_of(current_sat_lon)[0])
    sade_sati_phase = None
    delta = (sat_sign_idx - moon_sign_idx) % 12
    if delta == 11:   sade_sati_phase = "rising (Saturn in the sign before your Moon sign)"
    elif delta == 0:  sade_sati_phase = "peak (Saturn transiting your natal Moon sign directly)"
    elif delta == 1:  sade_sati_phase = "setting (Saturn in the sign after your Moon sign)"
    
    # Tithi Calculation (Hindu Lunar Day)
    tithi_val = (lons["Moon"] - lons["Sun"]) % 360
    tithi_index = int(tithi_val / 12) + 1
    paksha = "Shukla" if tithi_index <= 15 else "Krishna"
    tithi_num = tithi_index if tithi_index <= 15 else tithi_index - 15
    
    return {
        "tithi": f"{paksha} Paksha, Tithi {tithi_num}",
        "system":"Vedic / Jyotisha — Lahiri sidereal, whole-sign (rashi) houses",
        "ayanamsha_deg":round(ayan,4),
        "lagna":{"sign":lagna_sign,"deg_in_sign":lagna_deg,"lord":RASHI_LORDS[lagna_sign]},
        "janma_rashi":{"sign":sign_of(moon_lon)[0]},
        "janma_nakshatra":{"name":nk["name"],"lord":nk["lord"],"deity":nk["deity"],
                           "pada":pada,"quality":nk["quality"]},
        "atmakaraka":{"planet":atmakaraka,
                      "deg":round(atma_candidates.get(atmakaraka,0),3) if atmakaraka else None,
                      "note":"Jaimini soul-significator — the planet that has travelled farthest in its sign"},
        "sade_sati":{"active": sade_sati_phase is not None,
                     "phase": sade_sati_phase,
                     "note":"Saturn's 7.5-yr transit over natal Moon ±1 sign; challenging but transformative"},
        "planets":planets,
        "vimshottari_dasha":dasha,
        "yogas":yogas,
        "house_meanings":VEDIC_HOUSE,
    }

def vimshottari(moon_lon, birth_dt):
    """Full Vimshottari maha-dasha timeline + current antardasha (bhukti)."""
    nak_i=int(moon_lon//NAK_ARC)%27
    lord=NAKSHATRAS[nak_i]["lord"]
    frac_elapsed=(moon_lon % NAK_ARC)/NAK_ARC
    start_idx=DASHA_SEQ.index(lord)
    timeline=[]
    cur=birth_dt - timedelta(days=DASHA_YEARS[lord]*frac_elapsed*365.25)
    for k in range(10):
        L=DASHA_SEQ[(start_idx+k)%9]
        yrs=DASHA_YEARS[L]
        end=cur+timedelta(days=yrs*365.25)
        timeline.append({"lord":L,"start":cur.strftime("%Y-%m-%d"),
                         "end":end.strftime("%Y-%m-%d"),"years":yrs,
                         "is_current": cur<=TODAY<=end})
        cur=end
    current=next((d for d in timeline if d["is_current"]), None)
    bhukti=[]
    if current:
        antardasha=_antardasha(current["lord"],
                               datetime.strptime(current["start"],"%Y-%m-%d"))
        bhukti=antardasha
    return {"birth_dasha_lord":lord,
            "current_mahadasha":current,
            "current_antardasha":next((b for b in bhukti if b["is_current"]),None),
            "maha_timeline":timeline,
            "antardasha_in_current_maha":bhukti}

def _antardasha(maha_lord, maha_start):
    """Sub-periods within a maha-dasha."""
    start_idx=DASHA_SEQ.index(maha_lord)
    maha_years=DASHA_YEARS[maha_lord]
    out=[]; cur=maha_start
    for k in range(9):
        L=DASHA_SEQ[(start_idx+k)%9]
        sub_years=maha_years*DASHA_YEARS[L]/DASHA_TOTAL
        end=cur+timedelta(days=sub_years*365.25)
        out.append({"lord":L,"start":cur.strftime("%Y-%m-%d"),"end":end.strftime("%Y-%m-%d"),
                    "is_current":cur<=TODAY<=end})
        cur=end
    return out

def detect_yogas(planets, lagna_sign):
    """A few classical, mechanically-checkable yogas (grounded, not exhaustive)."""
    yogas=[]
    def house(p): return planets[p]["house"] if p in planets else None
    # Gajakesari: Jupiter in kendra (1/4/7/10) from Moon
    if "Jupiter" in planets and "Moon" in planets:
        diff=(planets["Jupiter"]["house"]-planets["Moon"]["house"])%12
        if planets["Jupiter"]["house"] in (1,4,7,10) and \
           ((SIGNS.index(planets["Jupiter"]["sign"])-SIGNS.index(planets["Moon"]["sign"]))%12) in (0,3,6,9):
            yogas.append({"name":"Gajakesari Yoga",
                "rule":"Jupiter in a kendra (1/4/7/10) from the Moon",
                "effect":"intelligence, reputation, lasting prosperity, respected influence"})
    # Budha-Aditya: Sun & Mercury same sign
    if planets.get("Sun",{}).get("sign")==planets.get("Mercury",{}).get("sign"):
        yogas.append({"name":"Budha-Aditya Yoga",
            "rule":"Sun and Mercury conjoined in the same sign",
            "effect":"sharp intellect, communication skill, administrative talent (weakened if Mercury combust)"})
    # Chandra-Mangala: Moon & Mars conjoined
    if planets.get("Moon",{}).get("sign")==planets.get("Mars",{}).get("sign"):
        yogas.append({"name":"Chandra-Mangala Yoga",
            "rule":"Moon and Mars in the same sign",
            "effect":"drive for wealth, emotional intensity, entrepreneurial energy"})
    # Exalted planets
    for p in ["Sun","Moon","Mars","Mercury","Jupiter","Venus","Saturn"]:
        if planets.get(p,{}).get("dignity")=="exalted":
            yogas.append({"name":f"{p} exalted",
                "rule":f"{p} in its sign of exaltation ({EXALT_SIGN[p]})",
                "effect":f"the significations of {p} ({GRAHA_KARAKAS[p]}) are powerfully expressed"})
    return yogas

# ── BaZi ─────────────────────────────────────────────────────────────────────
def bazi_chart(jd, birth_dt_local, gender="unknown", lat=0.0):
    """Four Pillars using solar-term-correct year & month, JDN day pillar."""
    lons, speed, backend = body_longitudes(jd)
    sun_lon = lons["Sun"]
    y=birth_dt_local.year; mo=birth_dt_local.month; d=birth_dt_local.day; h=birth_dt_local.hour
    # Solar year: switches at Li Chun (Sun = 315°). In Jan/early Feb before Li Chun → previous year.
    bazi_year=y
    if mo in (1,2) and sun_lon < SOLAR_TERM_START_LON:
        bazi_year=y-1
    ys=(bazi_year-4)%10; yb=(bazi_year-4)%12
    # Month branch from Sun's tropical longitude: Tiger(2) starts at 315°, each branch +30°
    month_order=int(((sun_lon-SOLAR_TERM_START_LON)%360)//30)   # 0=Tiger
    mb=(2+month_order)%12
    stem_base={0:2,1:4,2:6,3:8,4:0,5:2,6:4,7:6,8:8,9:0}[ys]      # 五虎遁
    ms=(stem_base+month_order)%10
    # Day pillar: continuous sexagenary cycle via the standard (JDN+49)%60 formula,
    # keyed to the LOCAL civil date (the day boundary is local midnight, not UT).
    jdn=int(math.floor(julian_day(datetime(y,mo,d,12))+0.5))
    sexa=(jdn+49)%60
    ds=sexa%10
    db=sexa%12
    # Hour branch (Zi=23:00). Late 23:00–23:59 belongs to next day's Zi in some schools;
    # we use same-day Zi (common simplification).
    hour_branch_map={23:0,0:0,1:1,2:1,3:2,4:2,5:3,6:3,7:4,8:4,9:5,10:5,
                     11:6,12:6,13:7,14:7,15:8,16:8,17:9,18:9,19:10,20:10,21:11,22:11}
    hb=hour_branch_map.get(h,0)
    hour_base={0:0,1:2,2:4,3:6,4:8,5:0,6:2,7:4,8:6,9:8}[ds]      # 五鼠遁
    hs=(hour_base+hb)%10

    def pillar(si,bi):
        s=STEMS[si]; b=BRANCHES[bi]
        return {"stem":{"han":s["han"],"pinyin":s["pinyin"],"element":s["element"],
                        "polarity":s["polarity"],"nature":s["nature"]},
                "branch":{"han":b["han"],"pinyin":b["pinyin"],"animal":b["animal"],
                          "element":b["element"],"hidden_stems":b["hidden"],"hours":b["hours"]}}
    pillars={"year":pillar(ys,yb),"month":pillar(ms,mb),"day":pillar(ds,db),"hour":pillar(hs,hb)}

    dm=STEMS[ds]
    # element tally (stems weight 1, main branch weight 1, hidden stems weight 0.5)
    tally={e:0.0 for e in ["Wood","Fire","Earth","Metal","Water"]}
    for si,bi in [(ys,yb),(ms,mb),(ds,db),(hs,hb)]:
        tally[STEMS[si]["element"]]+=1.0
        tally[BRANCHES[bi]["element"]]+=1.0
        for hidden in BRANCHES[bi]["hidden"]:
            tally[PINYIN_ELEM[hidden]]+=0.5
    tally={k:round(v,1) for k,v in tally.items()}
    # Day-master strength: support = same element + element that generates DM
    dm_e=dm["element"]; res_e=GENERATED_BY[dm_e]
    support=tally[dm_e]+tally[res_e]
    total=sum(tally.values())
    ratio=support/total if total else 0
    strength="Strong" if ratio>=0.5 else ("Balanced" if ratio>=0.35 else "Weak")
    # Favourable elements: weak DM → strengthen with resource & friend; strong DM → drain with output/wealth/officer
    if strength=="Weak":
        favourable=[res_e, dm_e]
        unfavourable=[CONTROLLED_BY[dm_e], CONTROLS[dm_e]]
        useful_note="Day Master is weak — it benefits from Resource and Friend elements that support it."
    elif strength=="Strong":
        favourable=[GENERATES[dm_e], CONTROLS[dm_e], CONTROLLED_BY[dm_e]]
        unfavourable=[res_e, dm_e]
        useful_note="Day Master is strong — it benefits from Output, Wealth and Officer elements that channel and balance it."
    else:
        favourable=[GENERATES[dm_e], CONTROLS[dm_e]]
        unfavourable=[]
        useful_note="Day Master is balanced — favour elements that keep flow without tipping the balance."

    # Ten Gods of the other three stems toward Day Master
    ten_gods={}
    for label,si in [("year",ys),("month",ms),("hour",hs)]:
        s=STEMS[si]
        ten_gods[label]=ten_god(dm_e,dm["polarity"],s["element"],s["polarity"])

    # Luck pillars (大運): direction from year-stem polarity + gender
    yang_year=STEMS[ys]["polarity"]=="Yang"
    male=str(gender).lower().startswith("m")
    forward=(yang_year and male) or ((not yang_year) and (not male))
    if str(gender).lower() not in ("m","male","f","female","man","woman"):
        forward=True  # default if unknown
    luck=[]
    start_age=8  # approximation; precise start needs distance to next/prev solar term
    for i in range(1,9):
        step=i if forward else -i
        lsi=(ms+step)%10; lbi=(mb+step)%12
        a0=start_age+(i-1)*10
        luck.append({"age":f"{a0}–{a0+9}","approx_years":f"{birth_dt_local.year+a0}–{birth_dt_local.year+a0+9}",
                     "stem":STEMS[lsi]["pinyin"],"stem_element":STEMS[lsi]["element"],
                     "branch":BRANCHES[lbi]["animal"],"branch_element":BRANCHES[lbi]["element"],
                     "direction":"forward" if forward else "reverse",
                     "is_current": a0 <= _age(birth_dt_local) <= a0+9})
    year_animal=BRANCHES[yb]["animal"]
    cur_year_branch=(TODAY.year-4)%12
    cur_animal=BRANCHES[cur_year_branch]["animal"]
    compat=ZODIAC_COMPAT.get(year_animal,{})
    tai_sui=_tai_sui(year_animal, cur_animal)

    return {
        "system":"Chinese BaZi — Four Pillars of Destiny (solar-term corrected)",
        "solar_year_used":bazi_year,
        "four_pillars":pillars,
        "day_master":{"han":dm["han"],"pinyin":dm["pinyin"],"element":dm_e,
                      "polarity":dm["polarity"],"nature":dm["nature"],"strength":strength,
                      "strength_ratio":round(ratio,2)},
        "element_balance":tally,
        "dominant_element":max(tally,key=tally.get),
        "weakest_element":min(tally,key=tally.get),
        "favourable_elements":favourable,"unfavourable_elements":unfavourable,
        "useful_god_note":useful_note,
        "element_advice":{e:ELEMENT_ADVICE[e] for e in favourable},
        "ten_gods":ten_gods,
        "luck_pillars":luck,
        "year_animal":year_animal,
        "zodiac_compatibility":compat,
        "current_year":{"year":TODAY.year,"animal":cur_animal,"tai_sui":tai_sui},
    }

def _age(birth_dt):
    return (TODAY - birth_dt).days/365.25

def _tai_sui(natal_animal, year_animal):
    order=[b["animal"] for b in BRANCHES]
    if natal_animal==year_animal:
        return f"{natal_animal} offends Tai Sui this year (本命年 / Ben Ming Nian) — a year to be cautious, steady, and avoid major risky changes."
    clash=ZODIAC_COMPAT.get(natal_animal,{}).get("clash")
    harm=ZODIAC_COMPAT.get(natal_animal,{}).get("harm")
    if year_animal==clash:
        return f"{natal_animal} clashes (沖) with the {year_animal} year — expect movement, change, friction; channel it into deliberate transitions."
    if year_animal==harm:
        return f"{natal_animal} is harmed (害) by the {year_animal} year — guard relationships and health; avoid hidden conflicts."
    return f"No direct Tai Sui conflict between {natal_animal} and the {year_animal} year — a relatively neutral-to-supportive year."

# ═════════════════════════════════════════════════════════════════════════════
#  SECTION G — TRANSITS & SYNASTRY
# ═════════════════════════════════════════════════════════════════════════════

def transits(natal_jd, natal_lat, natal_lng, transit_dt_utc):
    """Current-sky planets and the aspects they make to the natal chart."""
    natal_lons,_,_ = body_longitudes(natal_jd)
    t_jd=julian_day(transit_dt_utc)
    t_lons, t_speed, _ = body_longitudes(t_jd)
    transiting=["Jupiter","Saturn","Uranus","Neptune","Pluto","North Node","Mars"]
    natal_pts=["Sun","Moon","Mercury","Venus","Mars","Jupiter","Saturn",
               "Uranus","Neptune","Pluto","North Node"]
    hits=[]
    for tp in transiting:
        for npn in natal_pts:
            sep=abs(norm180(t_lons[tp]-natal_lons[npn]))
            for asp,(ang,orb,desc) in ASPECTS.items():
                tight = orb if tp in ("Jupiter","Saturn") else min(orb,4)
                if abs(sep-ang)<=tight:
                    hits.append({"transiting":tp,"to_natal":npn,"aspect":asp,
                                 "orb":round(abs(sep-ang),2),
                                 "transiting_sign":sign_of(t_lons[tp])[0],
                                 "retrograde":t_speed.get(tp,0)<0,
                                 "meaning":desc})
    hits.sort(key=lambda x:x["orb"])
    # Sade Sati check against transit Saturn
    natal_moon_sign = sign_of(natal_lons["Moon"])[0]
    natal_moon_idx = SIGNS.index(natal_moon_sign)
    sat_sign_idx = SIGNS.index(sign_of(t_lons["Saturn"])[0])
    delta = (sat_sign_idx - natal_moon_idx) % 12
    sade_sati = None
    if delta == 11:   sade_sati = {"active":True,"phase":"rising","saturn_sign":SIGNS[sat_sign_idx],"moon_sign":natal_moon_sign}
    elif delta == 0:  sade_sati = {"active":True,"phase":"peak","saturn_sign":SIGNS[sat_sign_idx],"moon_sign":natal_moon_sign}
    elif delta == 1:  sade_sati = {"active":True,"phase":"setting","saturn_sign":SIGNS[sat_sign_idx],"moon_sign":natal_moon_sign}
    else:             sade_sati = {"active":False,"saturn_sign":SIGNS[sat_sign_idx],"moon_sign":natal_moon_sign}
    return {"transit_date":transit_dt_utc.strftime("%Y-%m-%d"),
            "current_positions":{p:{"sign":sign_of(t_lons[p])[0],
                                    "deg":round(t_lons[p]%30,2),
                                    "retrograde":t_speed.get(p,0)<0}
                                 for p in ["Sun","Mercury","Venus","Mars","Jupiter","Saturn",
                                           "Uranus","Neptune","Pluto"]},
            "aspects_to_natal":hits[:20],
            "sade_sati":sade_sati}

def synastry(jdA, jdB):
    """Inter-chart aspects (A's planets to B's planets) — relationship synastry."""
    lonsA,_,_=body_longitudes(jdA)
    lonsB,_,_=body_longitudes(jdB)
    pts=["Sun","Moon","Mercury","Venus","Mars","Jupiter","Saturn","North Node"]
    inter=[]
    for a in pts:
        for b in pts:
            sep=abs(norm180(lonsA[a]-lonsB[b]))
            for asp,(ang,orb,desc) in ASPECTS.items():
                if abs(sep-ang)<=orb:
                    weight="major" if {a,b}&{"Sun","Moon","Venus","Mars"} else "minor"
                    inter.append({"personA_planet":a,"personB_planet":b,"aspect":asp,
                                  "orb":round(abs(sep-ang),2),"weight":weight,"meaning":desc})
    inter.sort(key=lambda x:(0 if x["weight"]=="major" else 1, x["orb"]))
    # quick harmony score: trine/sextile/conjunction(benefic) = +, square/opposition = −
    score=0
    for it in inter[:25]:
        if it["aspect"] in ("trine","sextile"): score+=2
        elif it["aspect"]=="conjunction": score+=1
        elif it["aspect"] in ("square","opposition"): score-=1
    return {"inter_aspects":inter[:25],
            "harmony_index":score,
            "note":"Harmony index is a coarse heuristic, not a verdict; read the actual aspects — Sun/Moon/Venus/Mars contacts matter most."}

# ═════════════════════════════════════════════════════════════════════════════
#  SECTION H — ASPECT PATTERNS (Grand Trine, T-Square, Yod, Stellium, etc.)
# ═════════════════════════════════════════════════════════════════════════════

def detect_aspect_patterns(lons, ayan=0.0):
    """Detect classical Western multi-planet configurations in the chart.
    Returns list of patterns with type, involved planets, tightness score (0-100),
    and interpretation key. Inspired by RoxyAPI's pattern detection."""
    bodies = ["Sun","Moon","Mercury","Venus","Mars","Jupiter","Saturn",
              "Uranus","Neptune","Pluto"]
    L = {b: norm360(lons[b] - ayan) for b in bodies if b in lons}
    aspects_list = compute_aspects(lons, ayan, bodies)
    patterns = []

    def has_aspect(a, b, asp_type=None):
        for asp in aspects_list:
            if (asp["a"]==a and asp["b"]==b) or (asp["a"]==b and asp["b"]==a):
                if asp_type is None or asp["aspect"]==asp_type:
                    return asp
        return None

    def orb_sum(planets_in_pattern):
        total = 0; count = 0
        for i in range(len(planets_in_pattern)):
            for j in range(i+1, len(planets_in_pattern)):
                a = has_aspect(planets_in_pattern[i], planets_in_pattern[j])
                if a:
                    total += a["orb"]; count += 1
        return total / count if count else 99

    def tightness(avg_orb, max_orb=8.0):
        return max(0, min(100, round(100 * (1 - avg_orb / max_orb))))

    signs_of = {b: sign_of(L[b])[0] for b in L}
    elements_of = {b: SIGN_DATA.get(signs_of.get(b,""),{}).get("element","") for b in L}
    modalities_of = {b: SIGN_DATA.get(signs_of.get(b,""),{}).get("modality","") for b in L}

    found_trines = []
    for i in range(len(bodies)):
        for j in range(i+1, len(bodies)):
            for k in range(j+1, len(bodies)):
                a, b, c = bodies[i], bodies[j], bodies[k]
                ab = has_aspect(a, b, "trine")
                bc = has_aspect(b, c, "trine")
                ac = has_aspect(a, c, "trine")
                if ab and bc and ac:
                    elems = {elements_of.get(p,"") for p in [a,b,c]}
                    is_dissociate = len(elems) > 1
                    avg = (ab["orb"]+bc["orb"]+ac["orb"])/3
                    found_trines.append({"planets":[a,b,c],"avg_orb":avg,
                                         "element":elems.pop() if len(elems)==1 else "mixed",
                                         "dissociate":is_dissociate})

    for tr in found_trines:
        a, b, c = tr["planets"]
        for d in bodies:
            if d in (a,b,c): continue
            opp_to = None
            for p in (a,b,c):
                opp = has_aspect(d, p, "opposition")
                if opp:
                    opp_to = p; break
            if opp_to:
                sext1 = has_aspect(d, [x for x in (a,b,c) if x!=opp_to][0], "sextile")
                sext2 = has_aspect(d, [x for x in (a,b,c) if x!=opp_to][1], "sextile")
                if sext1 and sext2:
                    avg = (tr["avg_orb"] + has_aspect(d, opp_to, "opposition")["orb"] +
                           sext1["orb"] + sext2["orb"]) / 4
                    patterns.append({"kind":"KITE","name":"Kite",
                        "planets":[a,b,c,d],"apex":d,"base_trine":[a,b,c],
                        "tightness":tightness(avg, 6),
                        "interpretation":f"Kite pattern with apex {d}: the Grand Trine talent finds directed expression through {d}'s focus."})
                    break

    grand_trine_planets = set()
    for p in patterns:
        if p["kind"]=="KITE":
            grand_trine_planets.update(p.get("base_trine",[]))
    for tr in found_trines:
        tp = set(tr["planets"])
        if tp & grand_trine_planets == tp:
            continue
        avg = tr["avg_orb"]
        patterns.append({"kind":"GRAND_TRINE","name":"Grand Trine",
            "planets":tr["planets"],"element":tr["element"],
            "dissociate":tr["dissociate"],"tightness":tightness(avg),
            "interpretation":f"Grand Trine in {tr['element']}: natural talent and ease among {', '.join(tr['planets'])}, but may lack motivation."})

    for i in range(len(bodies)):
        for j in range(i+1, len(bodies)):
            opp = has_aspect(bodies[i], bodies[j], "opposition")
            if not opp: continue
            for k in range(len(bodies)):
                if k in (i,j): continue
                sq1 = has_aspect(bodies[k], bodies[i], "square")
                sq2 = has_aspect(bodies[k], bodies[j], "square")
                if sq1 and sq2:
                    mods = {modalities_of.get(bodies[k],""), modalities_of.get(bodies[i],""),
                            modalities_of.get(bodies[j],"")}
                    avg = (opp["orb"]+sq1["orb"]+sq2["orb"])/3
                    is_gc = has_aspect(bodies[i], bodies[j], "opposition") is not None
                    for extra in bodies:
                        if extra in (bodies[i],bodies[j],bodies[k]): continue
                        ex_sq1 = has_aspect(extra, bodies[i], "square")
                        ex_sq2 = has_aspect(extra, bodies[j], "square")
                        if ex_sq1 and ex_sq2:
                            avg2 = (opp["orb"]+sq1["orb"]+sq2["orb"]+ex_sq1["orb"]+ex_sq2["orb"])/5
                            patterns.append({"kind":"GRAND_CROSS","name":"Grand Cross",
                                "planets":[bodies[i],bodies[j],bodies[k],extra],
                                "modality":mods.pop() if len(mods)==1 else "mixed",
                                "tightness":tightness(avg2, 7),
                                "interpretation":f"Grand Cross: intense tension demanding constant action and integration among {', '.join([bodies[i],bodies[j],bodies[k],extra])}."})
                            break
                    patterns.append({"kind":"T_SQUARE","name":"T-Square",
                        "planets":[bodies[i],bodies[j],bodies[k]],"apex":bodies[k],
                        "modality":mods.pop() if len(mods)==1 else "mixed",
                        "dissociate":False,"tightness":tightness(avg, 7),
                        "interpretation":f"T-Square focused on {bodies[k]} in {signs_of.get(bodies[k],'')}, tension between {bodies[i]} and {bodies[j]} demands resolution at the apex."})

    for i in range(len(bodies)):
        for j in range(i+1, len(bodies)):
            q1 = has_aspect(bodies[i], bodies[j], "quincunx")
            if not q1: continue
            for k in range(len(bodies)):
                if k in (i,j): continue
                q2 = has_aspect(bodies[k], bodies[i], "quincunx")
                sext = has_aspect(bodies[k], bodies[j], "sextile")
                if q2 and sext:
                    avg = (q1["orb"]+q2["orb"]+sext["orb"])/3
                    patterns.append({"kind":"YOD","name":"Yod (Finger of Fate)",
                        "planets":[bodies[i],bodies[j],bodies[k]],"apex":bodies[i],
                        "tightness":tightness(avg, 4),
                        "interpretation":f"Yod with apex {bodies[i]} in {signs_of.get(bodies[i],'')}: a fated sense of purpose that requires constant adjustment between {bodies[j]} and {bodies[k]}."})
                    break

    for s_idx in range(12):
        sign_start = s_idx * 30
        sign_end = sign_start + 30
        in_sign = [b for b in bodies if b in L and sign_start <= L[b] < sign_end]
        if len(in_sign) >= 3:
            orbs = [L[b] % 30 for b in in_sign]
            spread = max(orbs) - min(orbs)
            patterns.append({"kind":"STELLIUM","name":"Stellium",
                "planets":in_sign,"sign":SIGNS[s_idx],
                "planet_count":len(in_sign),"spread_deg":round(spread, 1),
                "tightness":max(0, min(100, round(100 * (1 - spread / 30)))),
                "interpretation":f"Stellium of {len(in_sign)} planets in {SIGNS[s_idx]} ({', '.join(in_sign)}): concentrated energy in {SIGN_DATA[SIGNS[s_idx]]['element']}/{SIGN_DATA[SIGNS[s_idx]]['modality']} affairs."})

    for i in range(len(bodies)):
        for j in range(i+1, len(bodies)):
            opp1 = has_aspect(bodies[i], bodies[j], "opposition")
            if not opp1:
                continue
            for k in range(len(bodies)):
                if k in (i, j):
                    continue
                for m_idx in range(k+1, len(bodies)):
                    if m_idx in (i, j):
                        continue
                    opp2 = has_aspect(bodies[k], bodies[m_idx], "opposition")
                    if not opp2:
                        continue
                    sext1a = has_aspect(bodies[i], bodies[k], "sextile")
                    sext1b = has_aspect(bodies[j], bodies[m_idx], "sextile")
                    sext2a = has_aspect(bodies[i], bodies[m_idx], "sextile")
                    sext2b = has_aspect(bodies[j], bodies[k], "sextile")
                    tr1a = has_aspect(bodies[i], bodies[k], "trine")
                    tr1b = has_aspect(bodies[j], bodies[m_idx], "trine")
                    tr2a = has_aspect(bodies[i], bodies[m_idx], "trine")
                    tr2b = has_aspect(bodies[j], bodies[k], "trine")
                    if ((sext1a and tr1b and sext2b and tr2a) or
                        (sext2a and tr2b and sext1b and tr1a)):
                        avg = (opp1["orb"] + opp2["orb"]) / 2
                        if sext1a: avg = (avg + sext1a["orb"]) / 2
                        if tr1b: avg = (avg + tr1b["orb"]) / 2
                        patterns.append({"kind": "MYSTIC_RECTANGLE", "name": "Mystic Rectangle",
                            "planets": [bodies[i], bodies[j], bodies[k], bodies[m_idx]],
                            "tightness": tightness(avg, 7),
                            "interpretation": f"Mystic Rectangle: two oppositions linked by harmonious aspects, creating tension that finds productive expression through {', '.join([bodies[i], bodies[j], bodies[k], bodies[m_idx]])}."})

    deduped = []
    seen = set()
    for p in patterns:
        key = (p["kind"], tuple(sorted(p["planets"])))
        if key not in seen:
            seen.add(key); deduped.append(p)

    gc_planets = {frozenset(p["planets"]) for p in deduped if p["kind"]=="GRAND_CROSS"}
    ts_to_remove = []
    for idx, p in enumerate(deduped):
        if p["kind"] == "T_SQUARE":
            ts_set = frozenset(p["planets"])
            if gc_planets and any(ts_set.issubset(gc) for gc in gc_planets):
                ts_to_remove.append(idx)
    kite_trines = {frozenset(p.get("base_trine",[])) for p in deduped if p["kind"]=="KITE"}
    gt_to_remove = []
    for idx, p in enumerate(deduped):
        if p["kind"] == "GRAND_TRINE":
            gt_set = frozenset(p["planets"])
            if any(gt_set == kt for kt in kite_trines):
                gt_to_remove.append(idx)
    for idx in sorted(ts_to_remove + gt_to_remove, reverse=True):
        if idx < len(deduped):
            deduped.pop(idx)

    return sorted(deduped, key=lambda x: -x["tightness"])

# ═════════════════════════════════════════════════════════════════════════════
#  SECTION H2 — SOLAR & LUNAR RETURNS
# ═════════════════════════════════════════════════════════════════════════════

def solar_return(natal_jd, target_year, lat, lng):
    """Find the exact moment in target_year when the transiting Sun returns
    to its natal ecliptic longitude, then cast a chart for that moment.
    This is the foundational technique for annual forecasting in Western astrology."""
    natal_lons, _, backend = body_longitudes(natal_jd)
    natal_sun_lon = natal_lons["Sun"]

    approx_jan = julian_day(datetime(target_year, 1, 1, 0, 0))
    low = approx_jan - 2
    high = approx_jan + 367

    for _ in range(60):
        mid = (low + high) / 2
        t_lons = tropical_longitudes(mid)
        if _HAS_SWE:
            try:
                t_lons_s, _, _ = body_longitudes(mid)
                t_lons = t_lons_s
            except Exception:
                pass
        t_sun = t_lons["Sun"]
        diff = norm180(t_sun - natal_sun_lon)
        if abs(diff) < 0.001:
            break
        if diff > 0:
            high = mid
        else:
            low = mid

    sr_jd = (low + high) / 2
    sr_dt_utc = datetime(2000, 1, 1) + timedelta(days=sr_jd - 2451544.5)

    sr_chart = western_chart(sr_jd, lat, lng, True)
    sr_lons, sr_speed, _ = body_longitudes(sr_jd)

    return {
        "system": "Solar Return (Western Tropical)",
        "target_year": target_year,
        "return_moment_utc": sr_dt_utc.strftime("%Y-%m-%d %H:%M"),
        "julian_day": round(sr_jd, 5),
        "natal_sun_lon": round(natal_sun_lon, 3),
        "return_sun_lon": round(sr_lons["Sun"], 3),
        "precision": "arcsecond" if _HAS_SWE else "~1 arcmin",
        "chart": sr_chart,
        "note": "Solar Return chart: cast for the moment the Sun returns to its exact natal longitude. Read for annual themes — house placement of the SR Sun shows the year's focus area."
    }

def lunar_return(natal_jd, target_year, target_month, lat, lng):
    """Find the moment in the target month when the transiting Moon returns
    to its natal ecliptic longitude. Monthly forecasting technique."""
    natal_lons, _, backend = body_longitudes(natal_jd)
    natal_moon_lon = natal_lons["Moon"]

    approx_start = julian_day(datetime(target_year, target_month, 1, 0, 0))
    low = approx_start - 2
    high = approx_start + 32

    for _ in range(80):
        mid = (low + high) / 2
        t_lons = tropical_longitudes(mid)
        if _HAS_SWE:
            try:
                t_lons_s, _, _ = body_longitudes(mid)
                t_lons = t_lons_s
            except Exception:
                pass
        t_moon = t_lons["Moon"]
        diff = norm180(t_moon - natal_moon_lon)
        if abs(diff) < 0.005:
            break
        if diff > 0:
            high = mid
        else:
            low = mid

    lr_jd = (low + high) / 2
    lr_dt_utc = datetime(2000, 1, 1) + timedelta(days=lr_jd - 2451544.5)

    lr_chart = western_chart(lr_jd, lat, lng, True)

    return {
        "system": "Lunar Return (Western Tropical)",
        "target_year": target_year,
        "target_month": target_month,
        "return_moment_utc": lr_dt_utc.strftime("%Y-%m-%d %H:%M"),
        "natal_moon_lon": round(natal_moon_lon, 3),
        "chart": lr_chart,
        "note": "Lunar Return chart: cast for the moment the Moon returns to its natal position (~every 27.3 days). Read for monthly emotional themes and domestic focus."
    }

# ═════════════════════════════════════════════════════════════════════════════
#  SECTION H3 — COMPATIBILITY SCORING (weighted synastry breakdown)
# ═════════════════════════════════════════════════════════════════════════════

def compatibility_score(jdA, jdB):
    """Detailed compatibility scoring with category breakdown.
    Returns 0-100 overall score plus romantic/emotional/intellectual/physical/spiritual subscores."""
    lonsA, _, _ = body_longitudes(jdA)
    lonsB, _, _ = body_longitudes(jdB)

    def score_pair(pA, pB, weight=1.0):
        sep = abs(norm180(lonsA[pA] - lonsB[pB]))
        pts = 0; best_asp = "none"; orb = 0
        for asp, (ang, max_orb, _) in ASPECTS.items():
            d = abs(sep - ang)
            if d <= max_orb:
                quality = 1.0 if asp in ("conjunction","trine","sextile") else -0.7
                if asp == "conjunction" and pA in ("Mars","Saturn") and pB in ("Mars","Saturn"):
                    quality = -0.3
                pts = quality * weight * (1 - d/max_orb)
                best_asp = asp; orb = d
                break
        return pts, best_asp, round(orb, 2)

    romantic, _, _ = score_pair("Venus", "Mars", 2.0)
    romantic += score_pair("Venus", "Venus", 1.0)[0]
    romantic += score_pair("Mars", "Venus", 1.5)[0] if score_pair("Venus", "Mars", 0)[1] == "none" else 0

    emotional, _, _ = score_pair("Moon", "Moon", 2.0)
    emotional += score_pair("Moon", "Venus", 1.5)[0]
    emotional += score_pair("Sun", "Moon", 1.5)[0]
    emotional += score_pair("Moon", "Sun", 1.5)[0]

    intellectual, _, _ = score_pair("Mercury", "Mercury", 2.0)
    intellectual += score_pair("Mercury", "Sun", 1.0)[0]
    intellectual += score_pair("Mercury", "Jupiter", 1.0)[0]

    physical, _, _ = score_pair("Mars", "Mars", 1.5)
    physical += score_pair("Sun", "Sun", 1.0)[0]
    physical += score_pair("Venus", "Mars", 1.5)[0]

    spiritual, _, _ = score_pair("North Node", "North Node", 1.0)
    spiritual += score_pair("North Node", "Sun", 1.0)[0]
    spiritual += score_pair("North Node", "Moon", 1.0)[0]
    spiritual += score_pair("Neptune", "Venus", 0.5)[0]

    def normalize(raw, max_possible=5.0):
        return max(0, min(100, round(50 + (raw / max_possible) * 50)))

    sub = {
        "romantic": normalize(romantic, 5.0),
        "emotional": normalize(emotional, 7.0),
        "intellectual": normalize(intellectual, 4.0),
        "physical": normalize(physical, 4.0),
        "spiritual": normalize(spiritual, 3.5),
    }
    overall = round(sum(sub.values()) / len(sub))
    if overall >= 80: desc = "Exceptional"
    elif overall >= 65: desc = "Strong"
    elif overall >= 50: desc = "Moderate"
    elif overall >= 35: desc = "Challenging"
    else: desc = "Difficult"

    signA = {p: sign_of(lonsA[p])[0] for p in ["Sun","Moon","Venus","Mars"]}
    signB = {p: sign_of(lonsB[p])[0] for p in ["Sun","Moon","Venus","Mars"]}
    elemA = [SIGN_DATA[signA[p]]["element"] for p in ["Sun","Moon","Venus","Mars"]]
    elemB = [SIGN_DATA[signB[p]]["element"] for p in ["Sun","Moon","Venus","Mars"]]
    shared = len(set(elemA) & set(elemB))

    return {
        "overall_score": overall,
        "description": desc,
        "breakdown": sub,
        "element_harmony": {"shared_elements": shared, "personA": elemA, "personB": elemB},
        "key_contacts": [
            {"pair": "Sun-Moon", "aspect": score_pair("Sun", "Moon")[1],
             "note": "Core identity meets emotional needs"},
            {"pair": "Venus-Mars", "aspect": score_pair("Venus", "Mars")[1],
             "note": "Love language meets desire style"},
            {"pair": "Moon-Moon", "aspect": score_pair("Moon", "Moon")[1],
             "note": "Emotional compatibility at the gut level"},
        ],
        "note": "Score is a heuristic from planetary geometry, not a verdict. Two 'difficult' charts can build something extraordinary; two 'exceptional' charts still need work."
    }

# ═════════════════════════════════════════════════════════════════════════════
#  SECTION H4 — PART OF FORTUNE, VERTEX, MOON PHASE, CALCULATED POINTS
# ═════════════════════════════════════════════════════════════════════════════

def part_of_fortune(sun_lon, moon_lon, asc_lon, is_day_chart=True):
    """Calculate the Part of Fortune (Lot of Fortune).
    Day chart: Asc + Moon - Sun. Night chart: Asc + Sun - Moon."""
    if is_day_chart:
        pof = asc_lon + moon_lon - sun_lon
    else:
        pof = asc_lon + sun_lon - moon_lon
    pof = norm360(pof)
    sign, idx, deg = sign_of(pof)
    return {"longitude": round(pof, 3), "sign": sign, "degree": round(deg, 2),
            "sect": "day" if is_day_chart else "night",
            "meaning": "The Part of Fortune represents the intersection of spirit (Sun), soul (Moon), and body (Ascendant) — a point of natural prosperity, joy, and physical well-being in the chart."}

def vertex(jd, lat, lng):
    """Calculate the Vertex — the 'point of fated encounters' in the chart.
    It's the intersection of the prime vertical with the ecliptic in the western hemisphere."""
    d = jd - 2451543.5
    eps = obliquity(d)
    gmst_val = gmst_deg(jd)
    ramc = norm360(gmst_val + lng)
    # Vertex formula: arctan(-cos(RAMC) / (sin(eps)*tan(lat) + cos(eps)*sin(RAMC)))
    num = -_cos(ramc)
    den = _sin(eps) * _tan(lat) + _cos(eps) * _sin(ramc)
    v_lon = norm360(_atan2(num, den))
    sign, idx, deg = sign_of(v_lon)
    return {"longitude": round(v_lon, 3), "sign": sign, "degree": round(deg, 2),
            "meaning": "The Vertex is the 'electric ascendant' — a point of fated encounters, significant relationships, and destined events, especially in synastry."}

def moon_phase(jd):
    """Calculate the Moon's phase: name, illumination fraction, age in days since New Moon,
    and the lunation cycle position."""
    lons, _, _ = body_longitudes(jd)
    sun_lon = lons["Sun"]
    moon_lon = lons["Moon"]

    elongation = norm360(moon_lon - sun_lon)
    synodic_period = 29.53059
    age = (elongation / 360.0) * synodic_period
    illumination = (1 - _cos(elongation)) / 2.0

    if elongation < 45: phase_name = "New Moon"
    elif elongation < 90: phase_name = "Waxing Crescent"
    elif elongation < 135: phase_name = "First Quarter"
    elif elongation < 180: phase_name = "Waxing Gibbous"
    elif elongation < 225: phase_name = "Full Moon"
    elif elongation < 270: phase_name = "Waning Gibbous"
    elif elongation < 315: phase_name = "Last Quarter"
    else: phase_name = "Waning Crescent"

    cycle_positions = {
        "New Moon": "initiation, new beginnings, planting seeds",
        "Waxing Crescent": "setting intentions, building momentum, taking first steps",
        "First Quarter": "crisis in action, commitment, overcoming obstacles",
        "Waxing Gibbous": "refinement, adjustment, perfecting the approach",
        "Full Moon": "culmination, revelation, harvest, illumination",
        "Waning Gibbous": "dissemination, sharing wisdom, gratitude",
        "Last Quarter": "release, letting go, restructuring, forgiveness",
        "Waning Crescent": "surrender, rest, reflection, preparation for renewal",
    }
    moon_sign, _, moon_deg = sign_of(moon_lon)

    return {
        "phase": phase_name,
        "illumination": round(illumination * 100, 1),
        "age_days": round(age, 2),
        "elongation_deg": round(elongation, 2),
        "moon_sign": moon_sign,
        "moon_degree": moon_deg,
        "cycle_meaning": cycle_positions.get(phase_name, ""),
        "note": f"The Moon is in {phase_name} phase at {round(illumination*100,1)}% illumination in {moon_sign}. {cycle_positions.get(phase_name,'')}."
    }

def upcoming_moon_phases(jd, count=4):
    """Find the next N major lunar phase transitions (New Moon, First Quarter, Full Moon, Last Quarter)."""
    phases_target = [0.0, 90.0, 180.0, 270.0]
    phase_names = {0.0: "New Moon", 90.0: "First Quarter", 180.0: "Full Moon", 270.0: "Last Quarter"}
    results = []
    current_jd = jd

    for _ in range(count * 3):
        if len(results) >= count:
            break
        lons = tropical_longitudes(current_jd)
        if _HAS_SWE:
            try:
                lons, _, _ = body_longitudes(current_jd)
            except Exception:
                pass
        elong = norm360(lons["Moon"] - lons["Sun"])

        for target in phases_target:
            diff = norm360(target - elong)
            if diff < 0.5 or diff > 359.5:
                dt_utc = datetime(2000, 1, 1) + timedelta(days=current_jd - 2451544.5)
                name = phase_names[target]
                already = any(r["phase"] == name for r in results)
                if not already:
                    results.append({"phase": name, "date_utc": dt_utc.strftime("%Y-%m-%d %H:%M"),
                                    "julian_day": round(current_jd, 4)})
                    break

        current_jd += 7.0

    results.sort(key=lambda x: x["julian_day"])
    return results[:count]

# ═════════════════════════════════════════════════════════════════════════════
#  SECTION H5 — NAVAMSA (D9) DIVISIONAL CHART
# ═════════════════════════════════════════════════════════════════════════════

def navamsa_chart(jd, lat, lng, time_known=True):
    """Calculate the Navamsa (D9) — the most important Vedic divisional chart.
    Each 30° sign is divided into 9 equal parts of 3°20' (one pada).
    The Navamsa reveals the soul's potential and strengths in relationships,
    marriage, and dharma. Essential for assessing planetary strength (vargottama)."""
    lons, speed, backend = body_longitudes(jd)
    ayan = ayanamsha_lahiri(jd)
    asc_lon, mc_lon = ascendant_mc(jd, lat, lng, ayan) if time_known else (norm360(lons["Sun"]-ayan), 0)

    navamsa_lons = {}
    names = ["Sun","Moon","Mercury","Venus","Mars","Jupiter","Saturn","North Node","South Node"]
    for nm in names:
        sid_lon = norm360(lons[nm] - ayan)
        sign_idx = int(sid_lon // 30)
        deg_in_sign = sid_lon % 30
        pada = int(deg_in_sign // (30.0/9.0))  # 0-8
        sign_element = SIGN_DATA[SIGNS[sign_idx]]["element"]

        element_navamsa_start = {
            "Fire": 0,    # Aries (0°) starts fire navamsas
            "Earth": 3,   # Capricorn starts earth navamsas
            "Air": 6,     # Libra starts air navamsas
            "Water": 9,   # Cancer starts water navamsas
        }
        navamsa_sign_idx = (element_navamsa_start.get(sign_element, 0) + pada) % 12
        navamsa_deg = (deg_in_sign % (30.0/9.0)) * 9.0
        navamsa_lon = navamsa_sign_idx * 30 + navamsa_deg
        navamsa_lons[nm] = navamsa_lon

    v_name = {"North Node": "Rahu", "South Node": "Ketu"}
    planets = {}
    for nm in names:
        vnm = v_name.get(nm, nm)
        n_lon = navamsa_lons[nm]
        n_sign, n_idx, n_deg = sign_of(n_lon)
        is_vargottama = (sign_of(norm360(lons[nm] - ayan))[0] == n_sign)
        planets[vnm] = {
            "sign": n_sign, "deg_in_sign": round(n_deg, 2),
            "abs_lon": round(n_lon, 3),
            "rashi_lord": RASHI_LORDS[n_sign],
            "vargottama": is_vargottama,
            "vargottama_note": f"{vnm} is vargottama (same sign in D1 and D9) — its strength is amplified." if is_vargottama else ""
        }

    asc_sign, _, asc_deg = sign_of(asc_lon)
    d9_asc_sign, _, d9_asc_deg = sign_of(navamsa_lons.get("Sun", asc_lon))

    return {
        "system": "Navamsa (D9) — Vedic Divisional Chart",
        "note": "The Navamsa is the 'soul chart' — it reveals the inner strength of each planet and the dharmic path. Vargottama planets (same sign in D1 and D9) are powerfully strengthened.",
        "navamsa_lagna": {"sign": d9_asc_sign, "note": "Navamsa Ascendant sign (approximate from D1 Ascendant)"},
        "planets": planets,
        "vargottama_count": sum(1 for p in planets.values() if p["vargottama"]),
    }

# ═════════════════════════════════════════════════════════════════════════════
#  SECTION H6 — KARANA & YOGA (complete Panchang elements)
# ═════════════════════════════════════════════════════════════════════════════

KARANAS = [
    "Bava","Balava","Kaulava","Taitila","Gara","Vanija","Vishti",
    "Shakuni","Chatushpada","Naga","Kinstughna"
]
KARANA_NATURE = {
    "Bava":"auspicious — good for beginnings, travel, financial matters",
    "Balava":"auspicious — good for religious activities, learning, ceremonies",
    "Kaulava":"auspicious — good for relationships, family, agreements",
    "Taitila":"mixed — acceptable for routine work, avoid major beginnings",
    "Gara":"mixed — good for hard work, discipline, avoid leisure",
    "Vanija":"auspicious for commerce — good for trade, business deals",
    "Vishti":"inauspicious (Bhadra) — avoid all auspicious activities",
    "Shakuni":"mixed — good for healing, legal matters, resolving disputes",
    "Chatushpada":"auspicious — good for stability, completion, endings",
    "Naga":"inauspicious — associated with hidden matters, avoid beginnings",
    "Kinstughna":"auspicious — the 'pinch of goodness', brief but positive window",
}

SOLAR_YOGAS = [
    "Vishkambha","Priti","Ayushman","Saubhagya","Shobhana","Atiganda",
    "Sukarma","Dhriti","Shula","Ganda","Vriddhi","Dhruva","Vyaghata",
    "Harshana","Vajra","Siddhi","Vyatipata","Variyana","Parigha","Shiva",
    "Siddha","Sadhya","Shubha","Shukla","Brahma","Indra","Vaidhriti"
]
YOGA_NATURE = {
    "Vishkambha":"mixed — supports endurance and overcoming obstacles",
    "Priti":"auspicious — love, harmony, pleasant interactions",
    "Ayushman":"auspicious — longevity, health, vitality",
    "Saubhagya":"auspicious — good fortune, success, marriage",
    "Shobhana":"auspicious — beauty, refinement, auspicious ceremonies",
    "Atiganda":"inauspicious — obstacles, complications, avoid new ventures",
    "Sukarma":"auspicious — good actions, charity, virtuous deeds",
    "Dhriti":"auspicious — patience, steadfastness, perseverance",
    "Shula":"inauspicious — pain, sharp conflict, surgical procedures only",
    "Ganda":"inauspicious — moral challenges, avoid major decisions",
    "Vriddhi":"auspicious — growth, increase, expansion",
    "Dhruva":"auspicious — stability, permanence, firm decisions",
    "Vyaghata":"inauspicious — obstacles, aggression, accidents",
    "Harshana":"auspicious — joy, happiness, celebrations",
    "Vajra":"mixed — powerful but rigid, good for decisive action",
    "Siddhi":"auspicious — accomplishment, perfection, success",
    "Vyatipata":"inauspicious — disasters, avoid all activities",
    "Variyana":"auspicious — comfort, wealth, increase",
    "Parigha":"mixed — obstacles that can be overcome with effort",
    "Shiva":"highly auspicious — spiritual activities, meditation, worship",
    "Siddha":"auspicious — accomplishment, perfection, spiritual merit",
    "Sadhya":"auspicious — attainable goals, achievable ambitions",
    "Shubha":"highly auspicious — purity, auspicious for all activities",
    "Shukla":"auspicious — brightness, clarity, intellectual pursuits",
    "Brahma":"highly auspicious — creation, knowledge, spiritual growth",
    "Indra":"auspicious — power, authority, leadership activities",
    "Vaidhriti":"mixed — restrictive, good for introspection only",
}

def panchang_elements(jd):
    """Complete Vedic Panchang elements: Tithi, Nakshatra, Yoga, Karana."""
    lons, _, _ = body_longitudes(jd)
    ayan = ayanamsha_lahiri(jd)
    sun_lon = lons["Sun"]
    moon_lon = lons["Moon"]

    tithi_val = norm360(moon_lon - sun_lon)
    tithi_index = int(tithi_val / 12)  # 0-29
    paksha = "Shukla" if tithi_index < 15 else "Krishna"
    tithi_num = tithi_index + 1 if tithi_index < 15 else tithi_index - 14
    tithi_names = [
        "Pratipada","Dwitiya","Tritiya","Chaturthi","Panchami","Shashti",
        "Saptami","Ashtami","Navami","Dashami","Ekadashi","Dwadashi",
        "Trayodashi","Chaturdashi","Purnima/Amavasya"
    ]
    tithi_name = tithi_names[min(tithi_num - 1, 14)]

    karana_index = int(tithi_val / 6)  # 0-59 karanas in full cycle
    if karana_index == 0:
        karana_name = KARANAS[10]  # Kinstughna
    elif karana_index <= 7:
        karana_name = KARANAS[(karana_index - 1) % 7]
    elif karana_index >= 52:
        karana_name = KARANAS[7 + (karana_index - 52)]
    else:
        karana_name = KARANAS[(karana_index - 1) % 7]

    moon_lon_sid = norm360(moon_lon - ayan)
    sun_lon_sid = norm360(sun_lon - ayan)
    yoga_lon = norm360(moon_lon_sid + sun_lon_sid)
    yoga_index = int(yoga_lon / (360.0 / 27)) % 27
    yoga_name = SOLAR_YOGAS[yoga_index]

    nak_i = int(moon_lon_sid // NAK_ARC) % 27
    nk = NAKSHATRAS[nak_i]

    return {
        "tithi": {"num": tithi_num, "name": tithi_name, "paksha": paksha,
                  "note": f"{paksha} Paksha, Tithi {tithi_num} ({tithi_name})"},
        "nakshatra": {"name": nk["name"], "lord": nk["lord"], "pada": int((moon_lon_sid % NAK_ARC)//(NAK_ARC/4))+1},
        "yoga": {"name": yoga_name, "nature": YOGA_NATURE.get(yoga_name, ""),
                 "note": f"Sun-Moon combined longitude determines the Yoga"},
        "karana": {"name": karana_name, "nature": KARANA_NATURE.get(karana_name, ""),
                   "note": f"Half-tithi Karana: {karana_name}"},
    }

# ═════════════════════════════════════════════════════════════════════════════
#  SECTION H7 — NUMEROLOGY (Life Path, Expression, Soul Urge)
# ═════════════════════════════════════════════════════════════════════════════

NUMEROLOGY_MEANINGS = {
    1: {"keyword": "Leadership", "nature": "independent, pioneering, self-determined, original",
        "challenge": "avoid stubbornness, excessive self-reliance, dismissing others' input",
        "careers": "entrepreneur, CEO, inventor, freelancer, any pioneering role"},
    2: {"keyword": "Cooperation", "nature": "diplomatic, sensitive, harmonious, supportive",
        "challenge": "avoid indecision, over-sensitivity, dependency on others' approval",
        "careers": "mediator, counselor, diplomat, healer, team-building roles"},
    3: {"keyword": "Expression", "nature": "creative, joyful, communicative, artistic",
        "challenge": "avoid scattering energy, superficiality, emotional dramatization",
        "careers": "writer, performer, artist, teacher, communicator, entertainer"},
    4: {"keyword": "Foundation", "nature": "practical, disciplined, organized, reliable",
        "challenge": "avoid rigidity, overwork, stubbornness, excessive routine",
        "careers": "engineer, architect, accountant, project manager, builder"},
    5: {"keyword": "Freedom", "nature": "versatile, adventurous, curious, dynamic",
        "challenge": "avoid restlessness, overindulgence, inconsistency, escapism",
        "careers": "travel, sales, marketing, journalism, any role requiring adaptability"},
    6: {"keyword": "Responsibility", "nature": "nurturing, harmonious, compassionate, artistic",
        "challenge": "avoid self-sacrifice to the point of martyrdom, controlling behavior",
        "careers": "teacher, healer, counselor, hospitality, design, community service"},
    7: {"keyword": "Wisdom", "nature": "analytical, spiritual, introspective, perceptive",
        "challenge": "avoid isolation, overthinking, skepticism, emotional detachment",
        "careers": "researcher, philosopher, scientist, spiritual teacher, analyst"},
    8: {"keyword": "Power", "nature": "ambitious, authoritative, business-minded, strategic",
        "challenge": "avoid workaholism, materialism, power struggles, neglecting personal life",
        "careers": "executive, finance, real estate, law, management, entrepreneurship"},
    9: {"keyword": "Humanitarian", "nature": "compassionate, generous, idealistic, wise",
        "challenge": "avoid emotional detachment, self-righteousness, over-giving without boundaries",
        "careers": "nonprofit, healing, teaching, arts, philanthropy, global causes"},
    11: {"keyword": "Master Intuitive", "nature": "visionary, inspired, spiritually gifted, idealistic",
         "challenge": "avoid nervous tension, self-doubt, living too much in the abstract",
         "careers": "spiritual teacher, artist, healer, innovator, inspirational leader"},
    22: {"keyword": "Master Builder", "nature": "visionary architect, practical idealist, transformative leader",
         "challenge": "avoid being overwhelmed by the scope of your visions",
         "careers": "large-scale projects, architecture, global business, system design"},
    33: {"keyword": "Master Teacher", "nature": "compassionate healer, selfless service, spiritual upliftment",
         "challenge": "avoid self-sacrifice without boundaries, carrying others' burdens",
         "careers": "healing, teaching, spiritual leadership, humanitarian work"},
}

def _reduce(n):
    while n > 9 and n not in (11, 22, 33):
        n = sum(int(d) for d in str(n))
    return n

def numerology(year, month, day, full_name=""):
    """Calculate core numerology: Life Path, Personal Year, and (if name provided) Expression & Soul Urge."""
    life_path = _reduce(_reduce(day) + _reduce(month) + _reduce(year))
    personal_year = _reduce(day + month + sum(int(d) for d in str(year)))
    lp_meaning = NUMEROLOGY_MEANINGS.get(life_path, {"keyword": str(life_path), "nature": "", "challenge": "", "careers": ""})

    result = {
        "life_path": {"number": life_path,
                      "meaning": lp_meaning.get("keyword",""),
                      "nature": lp_meaning.get("nature",""),
                      "challenge": lp_meaning.get("challenge",""),
                      "vocations": lp_meaning.get("careers","")},
        "personal_year": {"number": personal_year,
                          "note": f"Personal Year {personal_year} themes: {NUMEROLOGY_MEANINGS.get(personal_year,{}).get('keyword','cycle')}"},
        "birth_date_numbers": {"day": _reduce(day), "month": _reduce(month), "year": _reduce(year)},
    }

    if full_name:
        letter_values = {c: v for c in "abcdefghijklmnopqrstuvwxyz"
                        for v in [1,2,3,4,5,6,7,8,9]
                        if (ord(c) - ord('a')) % 9 + 1 == v}
        letter_map = {}
        for c in "abcdefghijklmnopqrstuvwxyz":
            letter_map[c] = (ord(c) - ord('a')) % 9 + 1
        vowels = set("aeiou")
        name_clean = full_name.lower().replace(" ", "")
        expression = _reduce(sum(letter_map.get(c, 0) for c in name_clean))
        soul_urge = _reduce(sum(letter_map.get(c, 0) for c in name_clean if c in vowels))
        result["expression"] = {"number": expression,
                                "note": f"Full name reveals talents and abilities: {NUMEROLOGY_MEANINGS.get(expression,{}).get('keyword','')}"}
        result["soul_urge"] = {"number": soul_urge,
                               "note": f"Vowels reveal inner motivation: {NUMEROLOGY_MEANINGS.get(soul_urge,{}).get('keyword','')}"}

    return result

# ═════════════════════════════════════════════════════════════════════════════
#  SECTION H8 — EQUAL HOUSE SYSTEM OPTION
# ═════════════════════════════════════════════════════════════════════════════

def equal_houses(asc_lon):
    """Equal house system: each house = 30° starting from the Ascendant degree.
    Simpler than Placidus, commonly used alongside whole-sign."""
    houses = {}
    for hnum in range(1, 13):
        cusp_lon = norm360(asc_lon + (hnum - 1) * 30)
        sign, idx, deg = sign_of(cusp_lon)
        houses[hnum] = {"sign": sign, "cusp_degree": round(deg, 2),
                        "abs_lon": round(cusp_lon, 3),
                        "ruler": SIGN_DATA[sign]["ruler"],
                        "meaning": HOUSE_MEANINGS[hnum]}
    return houses

# ═════════════════════════════════════════════════════════════════════════════
#  SECTION H9 — COMPOSITE CHART (midpoint of two natal charts)
# ═════════════════════════════════════════════════════════════════════════════

def composite_chart(jdA, jdB, latA, lngA, latB, lngB):
    """Midpoint composite chart — the relationship as a third entity.
    Each planet is the midpoint of its positions in both charts."""
    lonsA, speedA, backend = body_longitudes(jdA)
    lonsB, speedB, _ = body_longitudes(jdB)
    names = ["Sun","Moon","Mercury","Venus","Mars","Jupiter","Saturn",
             "Uranus","Neptune","Pluto","North Node","South Node","Chiron"]
    mid_lat = (latA + latB) / 2
    mid_lng = (lngA + lngB) / 2
    ascA, mcA = ascendant_mc(jdA, latA, lngA)
    ascB, mcB = ascendant_mc(jdB, latB, lngB)
    comp_asc = midpoint_lon(ascA, ascB)
    comp_mc = midpoint_lon(mcA, mcB)
    planets = {}
    for nm in names:
        if nm in lonsA and nm in lonsB:
            mid = midpoint_lon(lonsA[nm], lonsB[nm])
            sign, idx, deg = sign_of(mid)
            retro = speedA.get(nm, 0) < 0 or speedB.get(nm, 0) < 0
            house = whole_sign_house(mid, comp_asc)
            planets[nm] = {"longitude": round(mid, 3), "sign": sign,
                           "degree_in_sign": round(deg, 2), "house": house,
                           "retrograde": retro,
                           "dignity": dignity_western(nm, sign)}
    asc_sign, _, asc_deg = sign_of(comp_asc)
    mc_sign, _, mc_deg = sign_of(comp_mc)
    houses = {}
    asc_idx = int(comp_asc // 30)
    for hnum in range(1, 13):
        s = SIGNS[(asc_idx + hnum - 1) % 12]
        houses[hnum] = {"sign": s, "ruler": SIGN_DATA[s]["ruler"],
                        "meaning": HOUSE_MEANINGS[hnum]}
    aspects = compute_aspects({nm: planets[nm]["longitude"] for nm in planets})[:20]
    return {
        "system": "Composite Chart (midpoint method)",
        "note": "The composite chart represents the relationship itself as a third entity. Each planet is the midpoint of its positions in both natal charts.",
        "ascendant": {"sign": asc_sign, "degree": round(asc_deg, 2)},
        "midheaven": {"sign": mc_sign, "degree": round(mc_deg, 2)},
        "chart_ruler": SIGN_DATA[asc_sign]["ruler"],
        "descendant": {"sign": SIGNS[(asc_idx + 6) % 12],
                       "degree": round(asc_deg, 2)},
        "imum_coeli": {"sign": SIGNS[(int(comp_mc // 30) + 6) % 12],
                       "degree": round(mc_deg, 2)},
        "planets": planets, "houses": houses, "aspects": aspects}

def midpoint_lon(a, b):
    mid = (a + b) / 2
    diff = abs(a - b)
    if diff > 180:
        mid = norm360(mid + 180)
    return norm360(mid)

# ═════════════════════════════════════════════════════════════════════════════
#  SECTION H10 — BLACK MOON LILITH (Mean)
# ═════════════════════════════════════════════════════════════════════════════

def black_moon_lilith(jd):
    """Mean Black Moon Lilith — the empty focus of the Moon's orbit.
    Represents the shadow self, repressed desires, and primal wildness.
    Approximation using lunar apogee cycle (~8.85 year period)."""
    T = (jd - 2451545.0) / 36525.0
    lilith_lon = norm360(119.0524 + 406.6057 * T + 0.0107 * T * T)
    sign, idx, deg = sign_of(lilith_lon)
    return {"longitude": round(lilith_lon, 3), "sign": sign,
            "degree_in_sign": round(deg, 2),
            "meaning": "Black Moon Lilith represents the shadow self — repressed desires, primal instincts, and where one rejects conformity. It reveals where raw authenticity meets social conditioning."}

# ═════════════════════════════════════════════════════════════════════════════
#  SECTION H11 — SECONDARY PROGRESSIONS (1 day = 1 year)
# ═════════════════════════════════════════════════════════════════════════════

def secondary_progressions(natal_jd, target_age, lat, lng):
    """Secondary progressions: 1 day after birth = 1 year of life.
    Casts a chart for (natal_jd + target_age) days after birth."""
    prog_jd = natal_jd + target_age
    prog_chart = western_chart(prog_jd, lat, lng, True)
    prog_chart["system"] = "Secondary Progressions"
    prog_chart["target_age"] = target_age
    prog_chart["note"] = f"Progressed chart for age {target_age}. Each day after birth equals one year of life. The progressed Sun, Moon, and Ascendant reveal evolving identity, emotional needs, and outer persona."
    return prog_chart

# ═════════════════════════════════════════════════════════════════════════════
#  SECTION H12 — GENERIC PLANETARY RETURN (Mercury–Saturn)
# ═════════════════════════════════════════════════════════════════════════════

def planetary_return(natal_jd, planet, target_year, lat, lng):
    """Generic planetary return: find when transiting planet returns to natal position.
    Works for any planet. Solar/lunar returns are special cases."""
    natal_lons, _, backend = body_longitudes(natal_jd)
    if planet not in natal_lons:
        return {"error": f"Planet '{planet}' not available"}
    natal_lon = natal_lons[planet]
    approx_jan = julian_day(datetime(target_year, 1, 1, 0, 0))
    periods = {"Sun": 1.0, "Moon": 0.0748, "Mercury": 0.2408,
               "Venus": 0.6152, "Mars": 1.881, "Jupiter": 11.86,
               "Saturn": 29.46, "Uranus": 84.01, "Neptune": 164.8, "Pluto": 248.0}
    window = periods.get(planet, 1.0) * 367
    low = approx_jan - 2
    high = approx_jan + window + 2
    for _ in range(80):
        mid = (low + high) / 2
        t_lons = tropical_longitudes(mid)
        t_lon = t_lons.get(planet)
        if t_lon is None:
            break
        diff = norm180(t_lon - natal_lon)
        if abs(diff) < 0.001:
            break
        if diff > 0:
            high = mid
        else:
            low = mid
    ret_jd = (low + high) / 2
    ret_utc = datetime(2000, 1, 1) + timedelta(days=ret_jd - 2451544.5)
    ret_chart = western_chart(ret_jd, lat, lng, True)
    return {
        "system": f"Planetary Return ({planet})",
        "planet": planet, "target_year": target_year,
        "return_moment_utc": ret_utc.strftime("%Y-%m-%d %H:%M"),
        "natal_longitude": round(natal_lon, 3),
        "orbital_period_years": periods.get(planet, "?"),
        "chart": ret_chart,
        "note": f"{planet} return: the moment {planet} returns to its natal position, beginning a new {planet} cycle."}

# ═════════════════════════════════════════════════════════════════════════════
#  SECTION H13 — MORE ARABIC PARTS (Pars Spiritus, Amoris, etc.)
# ═════════════════════════════════════════════════════════════════════════════

ARABIC_PARTS = {
    "Pars Fortuna":     {"day": ("Asc","Moon","Sun"),  "night": ("Asc","Sun","Moon"),
                         "meaning": "Natural prosperity, joy, physical well-being"},
    "Pars Spiritus":    {"day": ("Asc","Sun","Moon"),  "night": ("Asc","Moon","Sun"),
                         "meaning": "The soul's purpose, spiritual calling, inner vision"},
    "Pars Amoris":      {"day": ("Asc","Venus","Sun"), "night": ("Asc","Sun","Venus"),
                         "meaning": "Love nature, romantic destiny, capacity for intimacy"},
    "Pars Fidei":       {"day": ("Asc","Moon","Saturn"),"night": ("Asc","Saturn","Moon"),
                         "meaning": "Faith, religion, philosophical convictions, trust"},
    "Pars Valetudinis": {"day": ("Asc","Moon","Mars"), "night": ("Asc","Mars","Moon"),
                         "meaning": "Health vulnerabilities, physical constitution"},
    "Pars Magistrix":   {"day": ("Asc","Jupiter","Sun"),"night": ("Asc","Sun","Jupiter"),
                         "meaning": "Career authority, professional recognition, vocation"},
    "Pars Victus":      {"day": ("Asc","Moon","Mercury"),"night": ("Asc","Mercury","Moon"),
                         "meaning": "Daily life, livelihood, routine patterns"},
    "Pars Sororis":     {"day": ("Asc","Venus","Moon"), "night": ("Asc","Moon","Venus"),
                         "meaning": "Sisters, close female friends, feminine bonds"},
    "Pars Fratris":     {"day": ("Asc","Jupiter","Saturn"),"night": ("Asc","Saturn","Jupiter"),
                         "meaning": "Brothers, close male friends, masculine bonds"},
    "Pars Nuptiae":     {"day": ("Asc","Venus","Saturn"),"night": ("Asc","Saturn","Venus"),
                         "meaning": "Marriage, committed partnerships, vows"},
}

def compute_arabic_parts(lons, asc_lon, is_day_chart=True):
    """Compute configured Arabic Parts / Hermetic Lots."""
    sect = "day" if is_day_chart else "night"
    results = {}
    for name, cfg in ARABIC_PARTS.items():
        formula = cfg[sect]
        vals = []
        for key in formula:
            if key == "Asc":
                vals.append(asc_lon)
            elif key in lons:
                vals.append(lons[key])
            else:
                break
        if len(vals) == 3:
            part_lon = norm360(vals[0] + vals[1] - vals[2])
            sign, idx, deg = sign_of(part_lon)
            results[name] = {"longitude": round(part_lon, 3), "sign": sign,
                             "degree_in_sign": round(deg, 2),
                             "sect_used": sect, "meaning": cfg["meaning"]}
    return results

# ═════════════════════════════════════════════════════════════════════════════
#  SECTION H14 — FIXED STARS (23 brightest with magnitude)
# ═════════════════════════════════════════════════════════════════════════════

FIXED_STARS = {
    "Regulus":     {"lon": 150.0,  "mag": 1.4, "nature": "Mars/Jupiter", "meaning": "Royalty, success, then downfall if revenge-seeking"},
    "Spica":       {"lon": 204.0,  "mag": 1.0, "nature": "Venus/Mars", "meaning": "Gifts, talent, wealth, potential for brilliance"},
    "Sirius":      {"lon": 104.0,  "mag": -1.5,"nature": "Jupiter/Mars", "meaning": "Fame, honor, wealth, loyalty, devotion to duty"},
    "Canopus":     {"lon": 55.0,   "mag": -0.7,"nature": "Saturn/Jupiter", "meaning": "Travel, voyages, positions of authority"},
    "Arcturus":    {"lon": 197.0,  "mag": -0.05,"nature": "Jupiter/Venus", "meaning": "Prosperity through travel, honors, self-determination"},
    "Vega":        {"lon": 285.0,  "mag": 0.03,"nature": "Venus/Mercury", "meaning": "Artistic talent, charisma, idealism"},
    "Capella":     {"lon": 80.0,   "mag": 0.08,"nature": "Mars/Mercury", "meaning": "Honor, wealth, public position, independence"},
    "Rigel":       {"lon": 283.0,  "mag": 0.13,"nature": "Jupiter/Saturn", "meaning": "Benevolence, honor, lasting fame through inventive mind"},
    "Procyon":     {"lon": 116.0,  "mag": 0.34,"nature": "Mercury/Mars", "meaning": "Quick rise followed by potential sudden fall"},
    "Betelgeuse":  {"lon": 89.0,   "mag": 0.5, "nature": "Mars/Mercury", "meaning": "Military honor, ambition, but potential for rashness"},
    "Altair":      {"lon": 303.0,  "mag": 0.77,"nature": "Mars/Jupiter", "meaning": "Boldness, ambition, courage, sudden fortune"},
    "Aldebaran":   {"lon": 70.0,   "mag": 0.85,"nature": "Mars", "meaning": "Honor, integrity, public prominence, but potential for failure"},
    "Antares":     {"lon": 250.0,  "mag": 1.1, "nature": "Mars/Jupiter", "meaning": "Obsessive focus, extremes, military honor or downfall"},
    "Pollux":      {"lon": 116.5,  "mag": 1.1, "nature": "Mars", "meaning": "Shrewdness, courage, boxing/martial skill, but cunning"},
    "Fomalhaut":   {"lon": 354.0,  "mag": 1.2, "nature": "Venus/Mercury", "meaning": "Spiritual gifts, fame, idealism, but vulnerability to deceit"},
    "Deneb":       {"lon": 325.0,  "mag": 1.25,"nature": "Venus/Mercury", "meaning": "Intelligence, artistic talent, changeable fortune"},
    "Algol":       {"lon": 46.0,   "mag": 2.1, "nature": "Saturn/Jupiter", "meaning": "Intense passion, confronting the shadow, potential for violence or transformation"},
    "Achernar":    {"lon": 15.0,   "mag": 0.5, "nature": "Jupiter", "meaning": "Success in public office, religious authority"},
    "Alcyone":     {"lon": 60.0,   "mag": 3.0, "nature": "Moon/Mars", "meaning": "Emotional depth, vision, but potential for blindness or obsession"},
    "Alphecca":    {"lon": 232.0,  "mag": 2.2, "nature": "Venus/Mercury", "meaning": "Artistic talent, honor, fame, but shame if dishonorable"},
    "Algorab":     {"lon": 186.0,  "mag": 3.1, "nature": "Saturn/Mars", "meaning": "Destruction, cunning, deceit, but also forensic intelligence"},
    "Deneb Algedi":{"lon": 336.0,  "mag": 2.9, "nature": "Saturn/Jupiter", "meaning": "Legal authority, business acumen, but potential for hardship"},
    "Alkaid":      {"lon": 200.0,  "mag": 1.9, "nature": "Mars/Moon", "meaning": "Mourning, loss, but also intellectual achievement through sorrow"},
}

def fixed_star_conjunctions(lons, max_orb=2.0):
    """Check which planets conjunct fixed stars (within orb degrees)."""
    results = []
    for star, data in FIXED_STARS.items():
        star_lon = data["lon"]
        for planet, p_lon in lons.items():
            if planet in ("North Node","South Node","Chiron"):
                continue
            diff = abs(norm180(star_lon - p_lon))
            if diff <= max_orb:
                results.append({"star": star, "planet": planet,
                                "orb": round(diff, 2),
                                "magnitude": data["mag"],
                                "nature": data["nature"],
                                "meaning": data["meaning"]})
    results.sort(key=lambda x: x["orb"])
    return results

# ═════════════════════════════════════════════════════════════════════════════
#  SECTION H15 — VEDIC DOSHAS (Mangal Dosha, Kaalsarpa Dosha)
# ═════════════════════════════════════════════════════════════════════════════

def mangal_dosha(jd, lat, lng, time_known=True):
    """Check for Mangal (Kuja/Mars) Dosha — Mars in 1st, 2nd, 4th, 7th, 8th, or 12th house."""
    lons, _, _ = body_longitudes(jd)
    ayan = ayanamsha_lahiri(jd)
    mars_sid = norm360(lons["Mars"] - ayan)
    if time_known:
        asc_lon, _ = ascendant_mc(jd, lat, lng, ayan)
    else:
        asc_lon = norm360(lons["Sun"] - ayan)
    asc_idx = int(asc_lon // 30)
    mars_idx = int(mars_sid // 30)
    mars_house = ((mars_idx - asc_idx) % 12) + 1
    dosha_houses = [1, 2, 4, 7, 8, 12]
    has_dosha = mars_house in dosha_houses
    cancellations = []
    mars_sign = SIGNS[mars_idx]
    if mars_sign in ("Aries", "Scorpio"):
        cancellations.append("Mars in own sign (Aries/Scorpio)")
    if mars_sign == "Capricorn":
        cancellations.append("Mars in exaltation (Capricorn)")
    if mars_house in (2, 4) and mars_sign in ("Cancer", "Leo"):
        cancellations.append("Mars in Cancer/Leo in 2nd/4th — partial cancellation")
    return {"has_mangal_dosha": has_dosha,
            "mars_house": mars_house,
            "mars_sign": mars_sign,
            "severity": "high" if mars_house in (1, 7, 8) else "moderate" if has_dosha else "none",
            "cancellations": cancellations,
            "note": "Mangal Dosha occurs when Mars occupies houses 1, 2, 4, 7, 8, or 12 from the ascendant. It affects marriage compatibility and can be cancelled by sign placements." if has_dosha else "No Mangal Dosha detected."}

def kaalsarpa_dosha(jd, lat, lng, time_known=True):
    """Check for Kaalsarpa Dosha — all planets hemmed between Rahu and Ketu."""
    lons, _, _ = body_longitudes(jd)
    ayan = ayanamsha_lahiri(jd)
    rahu_sid = norm360(lons["North Node"] - ayan)
    ketu_sid = norm360(rahu_sid + 180)
    check_bodies = ["Sun","Moon","Mercury","Venus","Mars","Jupiter","Saturn"]
    between_count = 0
    outside_count = 0
    for b in check_bodies:
        b_lon = norm360(lons[b] - ayan)
        if rahu_sid < ketu_sid:
            in_arc = rahu_sid < b_lon < ketu_sid
        else:
            in_arc = b_lon > rahu_sid or b_lon < ketu_sid
        if in_arc:
            between_count += 1
        else:
            outside_count += 1
    has_kaalsarpa = outside_count == 0 and between_count == 7
    partial = outside_count <= 1 and between_count >= 6
    rahu_sign = SIGNS[int(rahu_sid // 30)]
    direction = "rightward (Anulikta)" if rahu_sid < ketu_sid else "leftward (Viloma)"
    return {"has_kaalsarpa": has_kaalsarpa,
            "partial_kaalsarpa": partial and not has_kaalsarpa,
            "rahu_sign": rahu_sign,
            "direction": direction,
            "severity": "full" if has_kaalsarpa else "partial" if partial else "none",
            "note": "Kaalsarpa Dosha: all planets hemmed between Rahu and Ketu, indicating karmic intensity and life obstacles." if has_kaalsarpa else "No Kaalsarpa Dosha detected." if not partial else "Partial Kaalsarpa — most planets between Rahu and Ketu."}

# ═════════════════════════════════════════════════════════════════════════════
#  SECTION H16 — ADDITIONAL VEDIC VARGAS (D2, D3, D10, D12)
# ═════════════════════════════════════════════════════════════════════════════

def varga_chart(jd, varga, lat=0, lng=0, time_known=True):
    """Compute a Vedic divisional chart (Varga).
    D2=Hora (wealth), D3=Drekkana (siblings), D10=Dasamsa (career), D12=Dwadashamsa (parents)."""
    lons, _, backend = body_longitudes(jd)
    ayan = ayanamsha_lahiri(jd)
    if time_known:
        asc_lon, _ = ascendant_mc(jd, lat, lng, ayan)
    else:
        asc_lon = norm360(lons["Sun"] - ayan)

    varga_info = {
        "D2":  {"divisions": 2,  "name": "Hora", "meaning": "Wealth, resources, financial patterns"},
        "D3":  {"divisions": 3,  "name": "Drekkana", "meaning": "Siblings, courage, self-effort"},
        "D4":  {"divisions": 4,  "name": "Chaturthamsa", "meaning": "Property, fixed assets, fortune"},
        "D7":  {"divisions": 7,  "name": "Saptamsa", "meaning": "Children, progeny, creativity"},
        "D10": {"divisions": 10, "name": "Dasamsa", "meaning": "Career, profession, public status"},
        "D12": {"divisions": 12, "name": "Dwadashamsa", "meaning": "Parents, ancestry, lineage"},
        "D16": {"divisions": 16, "name": "Shodasamsa", "meaning": "Vehicles, comforts, luxuries"},
        "D20": {"divisions": 20, "name": "Vimsamsa", "meaning": "Spiritual pursuits, devotion"},
        "D24": {"divisions": 24, "name": "Chaturvimsamsa", "meaning": "Education, learning, knowledge"},
        "D30": {"divisions": 30, "name": "Trimsamsa", "meaning": "Misfortunes, health challenges"},
        "D40": {"divisions": 40, "name": "Khavedamsa", "meaning": "Auspicious/inauspicious events"},
        "D45": {"divisions": 45, "name": "Akshavedamsa", "meaning": "Overall character, conduct"},
        "D60": {"divisions": 60, "name": "Shashtiamsa", "meaning": "Karmic legacy, past life influences"},
    }
    v = varga.upper()
    if v not in varga_info:
        return {"error": f"Varga {v} not supported. Available: {list(varga_info.keys())}"}
    info = varga_info[v]
    d = info["divisions"]
    pada_arc = 30.0 / d
    elements = ["Fire", "Earth", "Air", "Water"]
    element_starts = {"Fire": "Aries", "Earth": "Capricorn", "Air": "Libra", "Water": "Cancer"}
    sign_idx_map = {s: i for i, s in enumerate(SIGNS)}

    varga_lons = {}
    names = ["Sun","Moon","Mercury","Venus","Mars","Jupiter","Saturn","North Node","South Node"]
    for nm in names:
        sid_lon = norm360(lons[nm] - ayan)
        sign_idx = int(sid_lon // 30)
        deg_in_sign = sid_lon % 30
        pada = int(deg_in_sign / pada_arc)
        elem_idx = sign_idx % 4
        elem = elements[elem_idx]
        base_sign_idx = sign_idx_map[element_starts[elem]]
        varga_sign_idx = (base_sign_idx + pada) % 12
        varga_lon = varga_sign_idx * 30 + (deg_in_sign % pada_arc)
        sign = SIGNS[varga_sign_idx]
        varga_lons[nm] = {"longitude": round(varga_lon, 3), "sign": sign,
                          "degree_in_sign": round(deg_in_sign % pada_arc, 2)}

    asc_pada = int((asc_lon % 30) / pada_arc)
    asc_elem_idx = int(asc_lon // 30) % 4
    asc_elem = elements[asc_elem_idx]
    asc_base = sign_idx_map[element_starts[asc_elem]]
    varga_asc_idx = (asc_base + asc_pada) % 12
    varga_asc_sign = SIGNS[varga_asc_idx]

    return {"system": f"Varga {v} ({info['name']})",
            "note": info["meaning"],
            "varga": v, "divisions": d,
            "varga_lagna": varga_asc_sign,
            "planets": varga_lons,
            "backend": backend}

# ═════════════════════════════════════════════════════════════════════════════
#  SECTION H17 — TRANSIT-TO-NATAL ASPECTS (detailed)
# ═════════════════════════════════════════════════════════════════════════════

def transit_to_natal_aspects(natal_jd, transit_jd):
    """Detailed listing of transit-to-natal aspects with impact rating.
    Used for 'what's happening to me right now' readings."""
    natal_lons, _, _ = body_longitudes(natal_jd)
    trans_lons, trans_speed, _ = body_longitudes(transit_jd)
    bodies = ["Sun","Moon","Mercury","Venus","Mars","Jupiter","Saturn",
              "Uranus","Neptune","Pluto","North Node"]
    results = []
    for t_p in bodies:
        if t_p not in trans_lons:
            continue
        for n_p in bodies:
            if n_p not in natal_lons:
                continue
            sep = abs(norm180(trans_lons[t_p] - natal_lons[n_p]))
            for asp, (ang, orb, desc) in ASPECTS.items():
                d = abs(sep - ang)
                if d <= orb:
                    applying = (trans_speed.get(t_p, 0) < 0) if asp in ("conjunction","opposition") else None
                    speed_val = trans_speed.get(t_p, 0)
                    if speed_val != 0:
                        future_sep = abs(norm180(norm360(trans_lons[t_p] + speed_val * 0.1) - natal_lons[n_p]))
                        applying = future_sep < sep
                    impact = "high" if asp in ("conjunction","opposition","square") and d < 2 else \
                             "moderate" if asp in ("conjunction","opposition","square","trine") else "low"
                    results.append({
                        "transit_planet": t_p, "natal_planet": n_p,
                        "aspect": asp, "orb": round(d, 2),
                        "applying": applying,
                        "impact": impact,
                        "retrograde": trans_speed.get(t_p, 0) < 0,
                        "meaning": desc})
    results.sort(key=lambda x: (0 if x["impact"]=="high" else 1 if x["impact"]=="moderate" else 2, x["orb"]))
    return {"transit_aspects": results[:30],
            "high_impact_count": sum(1 for r in results if r["impact"]=="high"),
            "note": "Transit-to-natal aspects show current planetary weather affecting the natal chart. High-impact aspects with tight orbs are most significant."}

# ═════════════════════════════════════════════════════════════════════════════
#  SECTION H18 — PLANETARY HOURS (standalone, not just horary)
# ═════════════════════════════════════════════════════════════════════════════

def planetary_hours(jd, lat, lng):
    """Calculate the planetary hours for a given day and location.
    Each day and night is divided into 12 hours, each ruled by a planet
    following the Chaldean order: Saturn→Jupiter→Mars→Sun→Venus→Mercury→Moon."""
    dt_utc = datetime(2000,1,1) + timedelta(days=jd - 2451544.5)
    chaldean = ["Saturn","Jupiter","Mars","Sun","Venus","Mercury","Moon"]
    weekday_ruler = chaldean[dt_utc.weekday()]
    obliquity_rad = math.radians(23.4393 - 0.0130 * ((jd - 2451545.0) / 36525.0))
    lat_rad = math.radians(lat)
    sun_lon = tropical_longitudes(jd).get("Sun", 0)
    sun_dec = math.asin(math.sin(obliquity_rad) * math.sin(math.radians(sun_lon)))
    cos_ha_rise = -math.tan(lat_rad) * math.tan(sun_dec)
    cos_ha_rise = max(-1, min(1, cos_ha_rise))
    ha_rise = math.degrees(math.acos(cos_ha_rise))
    day_length_hours = 2 * ha_rise / 15.0
    night_length_hours = 24.0 - day_length_hours
    day_hour_len = day_length_hours / 12.0
    night_hour_len = night_length_hours / 12.0
    sunrise_offset = 12.0 - ha_rise / 15.0
    sunrise_h = int(sunrise_offset)
    sunrise_m = int((sunrise_offset - sunrise_h) * 60)
    hour_idx_start = dt_utc.weekday()
    hours = []
    for h in range(24):
        is_day = h < 12
        ruler_idx = (hour_idx_start + h) % 7
        hour_len = day_hour_len if is_day else night_hour_len
        hours.append({"hour": h + 1, "ruler": chaldean[ruler_idx],
                       "is_daytime": is_day,
                       "approx_duration_min": round(hour_len * 60)})
    return {"date_utc": dt_utc.strftime("%Y-%m-%d"),
            "weekday_ruler": weekday_ruler,
            "sunrise_approx_utc": f"{sunrise_h:02d}:{sunrise_m:02d}",
            "day_length": f"{int(day_length_hours)}h {int((day_length_hours % 1) * 60)}m",
            "night_length": f"{int(night_length_hours)}h {int((night_length_hours % 1) * 60)}m",
            "hours": hours,
            "note": "Planetary hours follow the Chaldean sequence. Day hours run sunrise-to-sunset, night hours sunset-to-sunrise. The hour ruler colors the energy of actions taken in that hour."}
# ═════════════════════════════════════════════════════════════════════════════

def _ra_from_lon(lon_deg, eps_deg):
    """Right ascension (deg) from ecliptic longitude at given obliquity."""
    lam = math.radians(lon_deg)
    eps = math.radians(eps_deg)
    return math.degrees(math.atan2(math.sin(lam)*math.cos(eps),
                                   math.cos(lam))) % 360.0

def astrocartography(jd, lat, lng):
    """For each planet, the world-longitudes where it sits on the MC, IC, ASC, DSC
    at the moment of birth. These 'planet lines' are the basis of relocation
    astrology — living where a planet is angular emphasises its themes.

    Output: {planet: {mc: lng, ic: lng, asc: lat_belt, dsc: lat_belt,
                       themes: …}} plus a few reference cities per line.

    The ASC/DSC lines run along specific latitudes (not a single longitude);
    we report the latitude belt where the planet is rising/setting.
    """
    lons,_,backend = body_longitudes(jd)
    eps = obliquity(jd - 2451543.5)
    gmst = gmst_deg(jd)
    out = {"_meta": {"backend": backend, "interpretation_note":
        "Planet lines: where a planet is angular (MC=career, IC=home/roots, "
        "ASC=identity, DSC=relationships) at the moment of birth. Living under "
        "a line tends to activate that planet's themes; difficult planets "
        "(Saturn, Pluto, Chiron, South Node) are felt as tests, benefics "
        "(Jupiter, Venus, Sun) as gifts. Latitude matters as well as longitude."}}
    themes = {
        "Sun":    "identity, vitality, leadership, visibility, the father",
        "Moon":   "emotions, home, mother, the public, nurture, fluctuations",
        "Mercury":"communication, learning, commerce, travel, writing",
        "Venus":  "love, art, beauty, money, attraction, partnership",
        "Mars":   "drive, conflict, action, athletic, accidents, sex",
        "Jupiter":"expansion, luck, faith, higher learning, travel, opportunity",
        "Saturn": "discipline, restriction, hard work, karma, time, loneliness",
        "Uranus": "sudden change, awakening, freedom, disruption, innovation",
        "Neptune":"dreams, dissolution, spirituality, escapism, confusion",
        "Pluto":  "transformation, power, death/rebirth, obsession, shadow",
        "North Node":"destiny, growth edge, the unfamiliar, karmic pull",
        "South Node":"past life, comfort zone, release, innate skill",
        "Chiron": "wound, healing, the wounded-healer vocation, teaching through pain",
    }
    for p, lon in lons.items():
        ra = _ra_from_lon(lon, eps)
        mc_lng = norm360(ra - gmst)
        ic_lng = norm360(mc_lng + 180)
        # ASC line: approximate the latitude where the planet would be rising
        # (its declination). For Earth latitudes, the planet rises when the
        # local sidereal time equals its RA. ASC line lies where the planet's
        # altitude crosses 0°; with whole-sign simplicity, the ASC line is the
        # same longitude band as the MC/IC, but offset in latitude by the
        # planet's declination. We report the declination for the user/agent
        # to interpret, plus the longitude band.
        dec_deg = math.degrees(math.asin(math.sin(math.radians(eps)) *
                                         math.sin(math.radians(lon))))
        out[p] = {
            "mc_longitude": round(mc_lng, 2),
            "ic_longitude": round(ic_lng, 2),
            "ascendant_band": {"longitude": round(mc_lng, 2),
                               "latitude_hint_deg": round(dec_deg, 2),
                               "note": "ASC line is a curve; latitude shown is the planet's declination"},
            "descendant_band": {"longitude": round(ic_lng, 2),
                                "latitude_hint_deg": -round(dec_deg, 2)},
            "themes": themes.get(p, ""),
        }
    return out

# Reference city coordinates (subset — major global cities for planet-line
# interpretation). Latitude/longitude in degrees, E+ / N+. Used to suggest
# "is city X on/near your Jupiter line?" without doing a full GIS lookup.
CITIES = {
    "London":      (51.5, -0.1),    "New York":   (40.7, -74.0),
    "Los Angeles": (34.0, -118.2),  "Chicago":    (41.9, -87.6),
    "Toronto":     (43.7, -79.4),   "Mexico City":(19.4, -99.1),
    "São Paulo":   (-23.5, -46.6),  "Buenos Aires":(-34.6, -58.4),
    "Paris":       (48.9, 2.4),     "Berlin":     (52.5, 13.4),
    "Amsterdam":   (52.4, 4.9),     "Rome":       (41.9, 12.5),
    "Madrid":      (40.4, -3.7),    "Barcelona":  (41.4, 2.2),
    "Istanbul":    (41.0, 29.0),    "Athens":     (38.0, 23.7),
    "Cairo":       (30.0, 31.2),    "Lagos":      (6.5, 3.4),
    "Nairobi":     (-1.3, 36.8),    "Cape Town":  (-33.9, 18.4),
    "Dubai":       (25.2, 55.3),    "Mumbai":     (19.1, 72.9),
    "Delhi":       (28.6, 77.2),    "Bangalore":  (12.9, 77.6),
    "Kolkata":     (22.6, 88.4),    "Bangkok":    (13.7, 100.5),
    "Singapore":   (1.4, 103.8),    "Jakarta":    (-6.2, 106.8),
    "Hong Kong":   (22.3, 114.2),   "Shanghai":   (31.2, 121.5),
    "Beijing":     (39.9, 116.4),   "Seoul":      (37.6, 127.0),
    "Tokyo":       (35.7, 139.7),   "Osaka":      (34.7, 135.5),
    "Sydney":      (-33.9, 151.2),  "Melbourne":  (-37.8, 144.9),
    "Auckland":    (-36.8, 174.8),  "Honolulu":   (21.3, -157.9),
    "Vancouver":   (49.3, -123.1),  "San Francisco":(37.8, -122.4),
    "Miami":       (25.8, -80.2),   "Las Vegas":  (36.2, -115.2),
    "Seattle":     (47.6, -122.3),  "Boston":     (42.4, -71.1),
    "Moscow":      (55.8, 37.6),    "St Petersburg":(59.9, 30.3),
    "Kathmandu":   (27.7, 85.3),    "Colombo":    (6.9, 79.9),
    "Karachi":     (24.9, 67.0),    "Tehran":     (35.7, 51.4),
    "Tel Aviv":    (32.1, 34.8),    "Jerusalem":  (31.8, 35.2),
    "Reykjavik":   (64.1, -21.9),   "Stockholm":  (59.3, 18.1),
    "Helsinki":    (60.2, 24.9),    "Oslo":       (59.9, 10.8),
    "Copenhagen":  (55.7, 12.6),    "Vienna":     (48.2, 16.4),
    "Zurich":      (47.4, 8.5),     "Geneva":     (46.2, 6.1),
    "Lisbon":      (38.7, -9.1),    "Edinburgh":  (55.9, -3.2),
    "Dublin":      (53.3, -6.3),    "Wellington":  (-41.3, 174.8),
    "Anchorage":  (61.2, -149.9),
}

def _cities_on_line(target_lng, target_lat, tol_lng=10.0, tol_lat=8.0):
    """Return cities within tol degrees of a planet-line crossing."""
    hits = []
    for name, (lat, lng) in CITIES.items():
        d_lng = abs(norm180(lng - target_lng))
        d_lat = abs(lat - target_lat)
        if d_lng <= tol_lng and d_lat <= tol_lat:
            hits.append({"city": name, "lat": lat, "lng": lng,
                         "dist_lng": round(d_lng, 1), "dist_lat": round(d_lat, 1)})
    hits.sort(key=lambda x: x["dist_lng"] + x["dist_lat"])
    return hits[:6]

# ═════════════════════════════════════════════════════════════════════════════
#  SECTION J — HORARY (PRASNA) — chart of the moment a question is asked
# ═════════════════════════════════════════════════════════════════════════════

def horary(question_utc, lat, lng, question_text=""):
    """Cast a chart for the exact moment a question is asked. Classical horary
    rules (Prasna in Vedic): the Ascendant and its ruler = the querent; the
    Moon = the flow of events; the house ruling the matter = where to look;
    the planet ruling the house's cusp lord = the answer; aspects to the
    Moon and the Asc ruler show timing.

    Returns the chart plus a small set of classical signals the agent can
    interpret. We do NOT auto-interpret the question — the agent does, with
    full awareness that horary is the most interpretive branch and only a
    hint, not a guarantee.
    """
    jd = julian_day(question_utc)
    lons, speed, backend = body_longitudes(jd)
    ayan = ayanamsha_lahiri(jd)
    asc_lon, mc_lon = ascendant_mc(jd, lat, lng)   # tropical; treat as the moment
    sun_sign_idx = int(lons["Sun"] // 30)
    # Day / night chart (Sun above/below horizon) — used to choose which planets
    # are stronger; this requires computing the Sun's altitude, simplified.
    is_day_chart = (lons["Sun"] > asc_lon - 180) and (lons["Sun"] < asc_lon)
    # Void-of-course Moon: if the Moon makes no major aspect before leaving
    # its current sign, classical horary says "nothing will come of the matter."
    moon_lon = lons["Moon"]
    moon_sign_idx = int(moon_lon // 30)
    next_sign_lon = (moon_sign_idx + 1) * 30.0
    moon_to_next = next_sign_lon - moon_lon
    voc = True
    # check aspects Moon will make within remaining sign
    for p, plon in lons.items():
        if p in ("Moon","South Node"):
            continue
        # if Moon will reach an exact aspect within remaining degrees
        for ang, (exact, orb, _) in ASPECTS.items():
            target = norm360(plon + exact) if p in ("Sun","Mercury","Venus","Mars",
                                                     "Jupiter","Saturn","Uranus",
                                                     "Neptune","Pluto") else None
            if target is None:
                continue
            # distance Moon needs to travel to reach that target
            dist = norm360(target - moon_lon)
            if 0 < dist < moon_to_next + 6:  # 6° applying orb
                voc = False
                break
        if not voc:
            break
    moon_sign = SIGNS[moon_sign_idx]
    moon_p_house = whole_sign_house(moon_lon, asc_lon)
    # Ascendant ruler
    asc_sign = SIGNS[int(asc_lon // 30)]
    asc_ruler = SIGN_DATA[asc_sign]["ruler"]
    # Hour ruler (the planet ruling the weekday + the day-quadrant hour)
    weekday = question_utc.weekday()   # 0=Mon…6=Sun (Mon=Moon, Tue=Mars,…)
    # Classical Chaldean order: Saturn(0), Jupiter(1), Mars(2), Sun(3), Venus(4), Mercury(5), Moon(6)
    chaldean = ["Saturn","Jupiter","Mars","Sun","Venus","Mercury","Moon"]
    weekday_ruler = chaldean[(weekday + 5) % 7]   # adjust to Chaldean: Mon=Moon
    # Planetary hour of the day: divide daylight into 12 equal hours
    sun_alt = math.sin(math.radians(lons["Sun"]))   # crude proxy
    hour_ruler_idx = (weekday * 12 + question_utc.hour) % 7
    hour_ruler = chaldean[hour_ruler_idx]
    # "Hour planet" classical interpretation: the planet ruling the hour
    # describes the *flavour* of the moment, useful in horary timing.
    return {
        "system": "Horary / Prasna (chart of the moment)",
        "question_text": question_text,
        "question_utc": question_utc.strftime("%Y-%m-%d %H:%M:%S"),
        "ascendant": asc_sign,
        "ascendant_ruler": asc_ruler,
        "moon": {"sign": moon_sign,
                 "house_in_horary": moon_p_house,
                 "void_of_course": voc,
                 "interpretation": ("Nothing will come of the matter." if voc
                                    else "Moon is applying to an aspect — the matter proceeds.")},
        "day_chart": is_day_chart,
        "weekday_ruler": weekday_ruler,
        "planetary_hour_ruler": hour_ruler,
        "big_six": {p: {"sign": sign_of(lons[p])[0],
                        "house": whole_sign_house(lons[p], asc_lon),
                        "retrograde": (speed.get(p, 0) < 0)}
                    for p in ["Sun","Moon","Mercury","Venus","Mars","Jupiter","Saturn"]},
        "_meta": {"backend": backend,
                  "note": ("Horary is the most interpretive branch. Use this as "
                           "guidance, not a guarantee. The agent should map the "
                           "querent's question to a house (1=self, 2=money, "
                           "3=communication, 4=home/land, 5=children/creativity, "
                           "7=partnership, 8=others' money/death, 9=travel/law, "
                           "10=career, 11=gains, 12=hidden/loss) and read the "
                           "ruler of that house, plus Moon's applying aspect, for "
                           "the answer.")}
    }

# ═════════════════════════════════════════════════════════════════════════════
#  SECTION K — NAMAKARAN, ANATOMY, MISC SPECIALTY LOOKUPS
# ═════════════════════════════════════════════════════════════════════════════

def namakaran(moon_lon_sidereal):
    """Return the classical starting syllable(s) for a name aligned to the
    birth nakshatra pada. Works in sidereal (Vedic) longitude, since the
    classical rule uses the Janma Nakshatra. From a Moon's tropical longitude,
    pass through ayanamsha_lahiri(jd) first to convert.
    """
    nak_i = int(moon_lon_sidereal // NAK_ARC) % 27
    pada = int((moon_lon_sidereal % NAK_ARC) // PADA_ARC) + 1
    name = NAKSHATRAS[nak_i]["name"]
    syllables = NAKSHATRA_SYLLABLES.get(name, ["?"])
    chosen = syllables[pada - 1]
    return {
        "nakshatra": name,
        "pada": pada,
        "primary_syllable": chosen,
        "all_pada_syllables": syllables,
        "lord": NAKSHATRAS[nak_i]["lord"],
        "interpretation": (
            f"The Moon in {name} pada {pada} (lord {NAKSHATRAS[nak_i]['lord']}) "
            f"vibrates to the syllable '{chosen}'. Classical Namakaran: begin "
            f"the child's name (or a business/project name) with this sound "
            f"for the strongest resonance with the natal lunar mansion.")
    }

def anatomy_chart(planets_block):
    """For a Western planet block (each planet with sign/house), identify the
    body regions and systems emphasised, and flag any afflicted regions.
    Affliction = Saturn or Mars in or aspecting the sign (or its ruler).
    """
    body_map = {}
    afflicted_regions = []
    for planet, data in planets_block.items():
        sign = data.get("sign")
        if not sign:
            continue
        info = ANATOMY.get(sign, {})
        if not info:
            continue
        body_map[planet] = {"sign": sign, "region": info["region"],
                            "system": info["system"], "house": data.get("house")}
        if planet in ("Saturn", "Mars") and data.get("dignity") in ("fall", "detriment"):
            afflicted_regions.append({"planet": planet, "sign": sign,
                                      "region": info["region"]})
    return {"body_regions": body_map, "afflicted_regions": afflicted_regions,
            "surgery_avoidance_note":
                "Medical astrology rule: avoid elective surgery when the Moon "
                "transits the sign ruling the body part (e.g. don't operate on "
                "the throat when Moon is in Taurus). Also avoid during lunar "
                "eclipses, and prefer Moon in a fixed sign for stable outcomes."}

# ═════════════════════════════════════════════════════════════════════════════
#  SECTION L — EVENT / NON-HUMAN CHARTS (corporate, pet, event, moment)
# ═════════════════════════════════════════════════════════════════════════════

def event_chart(data):
    """Cast a chart for any 'moment of inception': a company incorporation, an
    app launch, a pet's adoption/birth, a wedding, a question time, etc.
    The math is identical to a natal chart — only the *subject* differs.
    Returns western + vedic + bazi for the given data.

    Convention: pass `subject` to label the chart; the data fields are the
    same as natal input (year/month/day/hour/minute/lat/lng/tz).
    """
    utc, tinfo = to_utc(data)
    jd = julian_day(utc)
    lat = data.get("lat", 0.0); lng = data.get("lng", 0.0)
    time_known = tinfo.get("time_known", True)
    birth_local = datetime(data["year"], data["month"], data["day"],
                           int(data.get("hour", 12)), int(data.get("minute", 0)))
    systems = data.get("systems", ["western", "vedic", "bazi"])
    _, _, backend = body_longitudes(jd)
    out = {
        "_meta": {"engine_backend": backend, "swisseph_available": _HAS_SWE,
                  "subject": data.get("subject", "(unnamed event)"),
                  "kind": data.get("kind", "event"),
                  "moment_utc": utc.strftime("%Y-%m-%d %H:%M"),
                  "precision_note": ("arcsecond (Swiss Ephemeris)" if backend == "swisseph"
                                     else "~1-2 arcmin (builtin) — exact to sign/house/nakshatra/dasha")},
        "subject": data.get("subject", "(unnamed event)"),
        "moment": {"local": birth_local.strftime("%Y-%m-%d %H:%M"),
                   "utc": utc.strftime("%Y-%m-%d %H:%M"),
                   "place": data.get("place", "")},
        "time_info": tinfo,
    }
    if "western" in systems:
        try: out["western"] = western_chart(jd, lat, lng, time_known)
        except Exception as e: out["western"] = {"error": repr(e)}
    if "vedic" in systems:
        try: out["vedic"] = vedic_chart(jd, lat, lng, birth_local, time_known)
        except Exception as e: out["vedic"] = {"error": repr(e)}
    if "bazi" in systems:
        try: out["bazi"] = bazi_chart(jd, birth_local, data.get("gender", "unknown"), lat)
        except Exception as e: out["bazi"] = {"error": repr(e)}
    return out

# ═════════════════════════════════════════════════════════════════════════════
#  SECTION H — ORCHESTRATION
# ═════════════════════════════════════════════════════════════════════════════

def life_phase(birth_dt):
    """Age-based transit milestones everyone hits — grounded, not chart-specific."""
    age=_age(birth_dt)
    notes=[]
    for sr in SATURN_RETURN_AGES:
        if abs(age-sr)<=2.5:
            notes.append(f"Saturn Return (~age {sr}): a structural reckoning — career, commitment, adulthood; "
                         f"life asks what is built to last.")
    for nr in NODE_RETURN_AGES:
        if abs(age-nr)<=1:
            notes.append(f"Nodal Return/Reversal (~age {nr:.0f}): a karmic re-orientation of direction and relationships.")
    if abs(age-42)<=2:
        notes.append("Uranus Opposition (~age 40-42): the 'mid-life' awakening — authenticity vs. the life you built.")
    if abs(age-12)<=1 or abs(age-24)<=1 or abs(age-36)<=1:
        notes.append("Jupiter Return (~every 12 yrs): a cycle of growth, opportunity and expansion opens.")
    return {"current_age":round(age,1),"active_milestones":notes}

def _normalize_birth(d):
    """Make input forgiving without changing the canonical schema.

    LLMs frequently emit `lon`/`longitude` instead of `lng`, or an ISO
    `date`/`time` string instead of numeric year/month/day/hour/minute.
    Previously `lon` was silently ignored (lng defaulted to 0.0 → a wrong
    ascendant), and `date`/`time` raised KeyError. We coerce these aliases to
    the canonical fields so a guessed shape still produces a correct chart.
    Recurses into a `partner` dict (synastry/compatibility/composite). Pure
    stdlib; canonical fields always win when both are present.
    """
    if not isinstance(d, dict):
        return d
    if "lng" not in d:
        for alias in ("lon", "long", "longitude"):
            if alias in d:
                d["lng"] = d[alias]; break
    if "lat" not in d and "latitude" in d:
        d["lat"] = d["latitude"]
    if "year" not in d and isinstance(d.get("date"), str):
        try:
            y, mo, dy = d["date"].strip().split("T")[0].split("-")[:3]
            d["year"], d["month"], d["day"] = int(y), int(mo), int(dy)
        except Exception:
            pass
    if "hour" not in d and isinstance(d.get("time"), str):
        try:
            hh, mm = (d["time"].strip().split(":") + ["0"])[:2]
            d["hour"], d["minute"] = int(hh), int(mm)
        except Exception:
            pass
    if isinstance(d.get("partner"), dict):
        _normalize_birth(d["partner"])
    return d

def calculate_full_profile(data):
    data = _normalize_birth(data)
    mode=data.get("mode","natal")
    birth_utc, tinfo = to_utc(data)
    jd=julian_day(birth_utc)
    lat=data.get("lat",0.0); lng=data.get("lng",0.0)
    time_known=tinfo.get("time_known",True)
    birth_local=datetime(data["year"],data["month"],data["day"],
                         int(data.get("hour",12)),int(data.get("minute",0)))
    systems=data.get("systems",["western","vedic","bazi"])
    _,_,backend=body_longitudes(jd)

    result={"_meta":{"engine_backend":backend,"swisseph_available":_HAS_SWE,
                     "birth_utc":birth_utc.strftime("%Y-%m-%d %H:%M"),"julian_day":round(jd,5),
                     "computed_on":TODAY.strftime("%Y-%m-%d"),
                     "house_system":"whole-sign (Placidus requires swisseph)",
                     "node_type":"true" if _HAS_SWE else "mean",
                     "precision_note":("arcsecond (Swiss Ephemeris)" if backend=="swisseph"
                                       else "~1-2 arcmin (builtin) — exact to sign/house/nakshatra/dasha")},
            "input":{k:data.get(k) for k in
                     ("name","year","month","day","hour","minute","lat","lng","tz","gender")},
            "time_info":tinfo,
            "summary": {
                "big_three": {
                    "sun": sign_of(body_longitudes(jd)[0]["Sun"])[0],
                    "moon": sign_of(body_longitudes(jd)[0]["Moon"])[0],
                    "ascendant": sign_of(ascendant_mc(jd, lat, lng)[0])[0]
                }
            },
            "mode":mode}

    if mode=="transit":
        result["natal_brief"]=western_chart(jd,lat,lng,time_known)["big_three"]
        tdate=data.get("transit_date")
        tdt=datetime.strptime(tdate,"%Y-%m-%d") if tdate else TODAY
        result["transits"]=transits(jd,lat,lng,tdt)
        result["life_phase"]=life_phase(birth_local)
        return result

    if mode=="synastry":
        p=data["partner"]
        p_utc,_=to_utc(p); jdB=julian_day(p_utc)
        result["synastry"]=synastry(jd,jdB)
        result["personA"]={"big_three":western_chart(jd,lat,lng,time_known)["big_three"]}
        result["personB"]={"big_three":western_chart(jdB,p.get("lat",0),p.get("lng",0),
                                                      p.get("time_known",True))["big_three"]}
        if "bazi" in systems:
            result["personA"]["bazi_animal"]=bazi_chart(jd,birth_local,data.get("gender","unknown")).get("year_animal")
            pb_local=datetime(p["year"],p["month"],p["day"],int(p.get("hour",12)),int(p.get("minute",0)))
            result["personB"]["bazi_animal"]=bazi_chart(jdB,pb_local,p.get("gender","unknown")).get("year_animal")
        return result

    if mode=="astrocartography":
        result["astrocartography"]=astrocartography(jd, lat, lng)
        result["big_three"]=western_chart(jd,lat,lng,time_known)["big_three"]
        return result

    if mode=="horary":
        qtext = data.get("question","")
        qdt = datetime.strptime(data["question_time"], "%Y-%m-%d %H:%M") if data.get("question_time") else datetime.utcnow()
        # Convert to UTC using provided tz if any
        if data.get("tz") and _HAS_TZDB:
            try:
                local = qdt.replace(tzinfo=ZoneInfo(data["tz"]))
                qdt_utc = local.astimezone(timezone.utc).replace(tzinfo=None)
            except Exception:
                qdt_utc = qdt
        else:
            qdt_utc = qdt
        result["horary"]=horary(qdt_utc, lat, lng, qtext)
        return result

    if mode=="event":
        result["event_chart"]=event_chart(data)
        return result

    if mode=="solar_return":
        target_year=data.get("target_year", birth_local.year + 1)
        result["solar_return"]=solar_return(jd, target_year, lat, lng)
        result["natal_sun_sign"]=sign_of(body_longitudes(jd)[0]["Sun"])[0]
        return result

    if mode=="lunar_return":
        target_year=data.get("target_year", birth_local.year)
        target_month=data.get("target_month", birth_local.month)
        result["lunar_return"]=lunar_return(jd, target_year, target_month, lat, lng)
        return result

    if mode=="compatibility":
        p=data["partner"]
        p_utc,_=to_utc(p); jdB=julian_day(p_utc)
        result["compatibility"]=compatibility_score(jd, jdB)
        result["personA"]={"big_three":western_chart(jd,lat,lng,time_known)["big_three"]}
        result["personB"]={"big_three":western_chart(jdB,p.get("lat",0),p.get("lng",0),
                                                      p.get("time_known",True))["big_three"]}
        result["synastry"]=synastry(jd,jdB)
        return result

    if mode=="navamsa":
        result["navamsa"]=navamsa_chart(jd, lat, lng, time_known)
        result["vedic_brief"]=vedic_chart(jd,lat,lng,birth_local,time_known)
        return result

    if mode=="numerology":
        result["numerology"]=numerology(data["year"],data["month"],data["day"],
                                        data.get("full_name",""))
        return result

    if mode=="moon_phase":
        result["moon_phase"]=moon_phase(jd)
        result["upcoming_moon_phases"]=upcoming_moon_phases(jd, count=4)
        return result

    if mode=="panchang":
        result["panchang"]=panchang_elements(jd)
        result["vedic_brief"]=vedic_chart(jd,lat,lng,birth_local,time_known)
        return result

    if mode=="composite":
        p=data["partner"]
        p_utc,_=to_utc(p); jdB=julian_day(p_utc)
        result["composite"]=composite_chart(jd, jdB, lat, lng, p.get("lat",0), p.get("lng",0))
        result["personA"]={"big_three":western_chart(jd,lat,lng,time_known)["big_three"]}
        result["personB"]={"big_three":western_chart(jdB,p.get("lat",0),p.get("lng",0),
                                                      p.get("time_known",True))["big_three"]}
        return result

    if mode=="progressions":
        target_age=data.get("target_age", 30)
        result["progressions"]=secondary_progressions(jd, target_age, lat, lng)
        return result

    if mode=="planetary_return":
        planet=data.get("planet","Jupiter")
        target_year=data.get("target_year", birth_local.year + 1)
        result["planetary_return"]=planetary_return(jd, planet, target_year, lat, lng)
        return result

    if mode=="varga":
        varga=data.get("varga","D10")
        result["varga"]=varga_chart(jd, varga, lat, lng, time_known)
        return result

    if mode=="planetary_hours":
        result["planetary_hours"]=planetary_hours(jd, lat, lng)
        return result

    if mode=="transit_natal_aspects":
        tdate=data.get("transit_date")
        tdt=datetime.strptime(tdate,"%Y-%m-%d") if tdate else TODAY
        tjd=julian_day(tdt)
        result["transit_natal_aspects"]=transit_to_natal_aspects(jd, tjd)
        return result

    # natal (default)
    result["charts"]={}
    if "western" in systems:
        try: result["charts"]["western"]=western_chart(jd,lat,lng,time_known)
        except Exception as e: result["charts"]["western"]={"error":repr(e)}
    if "vedic" in systems:
        try: result["charts"]["vedic"]=vedic_chart(jd,lat,lng,birth_local,time_known)
        except Exception as e: result["charts"]["vedic"]={"error":repr(e)}
    if "bazi" in systems:
        try: result["charts"]["bazi"]=bazi_chart(jd,birth_local,data.get("gender","unknown"),lat)
        except Exception as e: result["charts"]["bazi"]={"error":repr(e)}
    result["life_phase"]=life_phase(birth_local)

    if "western" in systems and time_known:
        try:
            lons, _, _ = body_longitudes(jd)
            asc_lon, _ = ascendant_mc(jd, lat, lng)
            sun_lon = lons["Sun"]
            is_day = 90 <= norm360(asc_lon - sun_lon) <= 270
            result["special_points"]={
                "part_of_fortune": part_of_fortune(sun_lon, lons["Moon"], asc_lon, is_day),
                "vertex": vertex(jd, lat, lng),
                "moon_phase_at_birth": moon_phase(jd),
                "black_moon_lilith": black_moon_lilith(jd),
            }
            result["arabic_parts"]=compute_arabic_parts(lons, asc_lon, is_day)
            result["aspect_patterns"]=detect_aspect_patterns(lons)
            result["fixed_star_conjunctions"]=fixed_star_conjunctions(lons)
            result["equal_houses"]=equal_houses(asc_lon)
        except Exception:
            pass

    if "vedic" in systems:
        try:
            result["panchang"]=panchang_elements(jd)
            result["navamsa"]=navamsa_chart(jd, lat, lng, time_known)
            result["mangal_dosha"]=mangal_dosha(jd, lat, lng, time_known)
            result["kaalsarpa_dosha"]=kaalsarpa_dosha(jd, lat, lng, time_known)
        except Exception:
            pass

    if data.get("include_numerology"):
        try: result["numerology"]=numerology(data["year"],data["month"],data["day"],
                                              data.get("full_name",""))
        except Exception:
            pass

    return result


def _demo():
    return {"name":"Demo","year":1990,"month":6,"day":15,"hour":14,"minute":30,
            "lat":40.7128,"lng":-74.0060,"tz":"America/New_York",
            "systems":["western","vedic","bazi"],"gender":"male"}

if __name__=="__main__":
    ap=argparse.ArgumentParser(description="Deterministic astrology engine")
    ap.add_argument("--json",help="birth data JSON string")
    ap.add_argument("--file",help="path to birth data JSON file")
    a=ap.parse_args()
    if a.json: data=json.loads(a.json)
    elif a.file:
        with open(a.file) as f: data=json.load(f)
    else: data=_demo()
    print(json.dumps(calculate_full_profile(data),indent=2,default=str))
