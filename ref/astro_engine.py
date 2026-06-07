"""
Astrology Engine — Deterministic Calculation Backend
Supports: Western Tropical, Vedic (Jyotisha/Sidereal), Chinese BaZi

All planetary positions are calculated via Swiss Ephemeris (PySwissEph)
through the Kerykeion library. This is the trusted math layer — no AI
guessing, no hallucination of chart data.

Usage: python3 astro_engine.py --json <birth_data_json>
"""

from __future__ import annotations
import json
import sys
import argparse
from datetime import datetime, timedelta
from kerykeion import AstrologicalSubject, NatalAspects

# ─────────────────────────────────────────────
# WESTERN ASTROLOGY DATA
# ─────────────────────────────────────────────

SIGN_KEYWORDS = {
    "Ari": {"name":"Aries","element":"Fire","modality":"Cardinal","ruler":"Mars",
            "keywords":"boldness, initiative, raw energy, pioneering spirit"},
    "Tau": {"name":"Taurus","element":"Earth","modality":"Fixed","ruler":"Venus",
            "keywords":"stability, sensuality, patience, material security"},
    "Gem": {"name":"Gemini","element":"Air","modality":"Mutable","ruler":"Mercury",
            "keywords":"duality, curiosity, communication, adaptability"},
    "Can": {"name":"Cancer","element":"Water","modality":"Cardinal","ruler":"Moon",
            "keywords":"nurturing, intuition, emotional memory, home and roots"},
    "Leo": {"name":"Leo","element":"Fire","modality":"Fixed","ruler":"Sun",
            "keywords":"creativity, leadership, pride, warmth, generosity"},
    "Vir": {"name":"Virgo","element":"Earth","modality":"Mutable","ruler":"Mercury",
            "keywords":"precision, service, health, discernment, practical mastery"},
    "Lib": {"name":"Libra","element":"Air","modality":"Cardinal","ruler":"Venus",
            "keywords":"balance, justice, partnership, harmony, aesthetic sensibility"},
    "Sco": {"name":"Scorpio","element":"Water","modality":"Fixed","ruler":"Pluto/Mars",
            "keywords":"depth, transformation, power, hidden truths, regeneration"},
    "Sag": {"name":"Sagittarius","element":"Fire","modality":"Mutable","ruler":"Jupiter",
            "keywords":"expansion, philosophy, freedom, truth-seeking, higher knowledge"},
    "Cap": {"name":"Capricorn","element":"Earth","modality":"Cardinal","ruler":"Saturn",
            "keywords":"ambition, discipline, structure, authority, long-term vision"},
    "Aqu": {"name":"Aquarius","element":"Air","modality":"Fixed","ruler":"Uranus/Saturn",
            "keywords":"innovation, humanitarian ideals, detachment, originality"},
    "Pis": {"name":"Pisces","element":"Water","modality":"Mutable","ruler":"Neptune/Jupiter",
            "keywords":"compassion, spirituality, dissolution, imagination, sacrifice"},
}

PLANET_ARCHETYPES = {
    "Sun":    "identity, ego, life force, the father, vitality",
    "Moon":   "emotion, instinct, the mother, subconscious, habits",
    "Mercury":"mind, communication, intellect, trade, siblings",
    "Venus":  "love, beauty, values, art, money, what we attract",
    "Mars":   "drive, desire, action, conflict, sex, the warrior",
    "Jupiter":"expansion, luck, philosophy, wisdom, abundance",
    "Saturn": "discipline, karma, restriction, time, responsibility",
    "Uranus": "rebellion, innovation, sudden change, awakening",
    "Neptune":"dreams, illusions, spirituality, dissolution, compassion",
    "Pluto":  "transformation, power, death/rebirth, shadow work",
    "Chiron": "the wounded healer, deepest wound and greatest gift",
    "True_North_Lunar_Node": "soul's purpose, karmic direction, future growth",
    "True_South_Lunar_Node": "karmic past, comfort zone, where you've been",
}

HOUSE_MEANINGS = {
    1: "Self, identity, physical body, first impressions, how the world sees you",
    2: "Money, possessions, values, self-worth, material security",
    3: "Communication, siblings, short trips, local environment, early education",
    4: "Home, roots, family, ancestry, inner foundation, the end of life",
    5: "Creativity, romance, children, pleasure, self-expression, games",
    6: "Health, daily routine, service, work environment, small animals",
    7: "Partnership, marriage, open enemies, contracts, one-to-one relationships",
    8: "Death, transformation, shared resources, sex, occult, inheritance",
    9: "Philosophy, higher education, long travel, religion, foreign cultures",
    10: "Career, public reputation, authority, legacy, the father figure",
    11: "Friends, groups, social causes, hopes and wishes, the collective",
    12: "Hidden enemies, isolation, spirituality, karma, self-undoing, institutions",
}

ASPECT_MEANINGS = {
    "conjunction": "fusion of energies — intense, amplified, unified (0°)",
    "opposition":  "tension, awareness through contrast, need for balance (180°)",
    "trine":       "natural flow, ease, talent, harmonious support (120°)",
    "square":      "friction, challenge, growth through struggle (90°)",
    "sextile":     "opportunity, cooperation, supportive energy (60°)",
    "quincunx":    "adjustment, discomfort, unrelated energies needing integration (150°)",
}

SATURN_RETURN_AGES = [28, 58, 88]

# ─────────────────────────────────────────────
# VEDIC / JYOTISH DATA
# ─────────────────────────────────────────────

NAKSHATRAS = [
    {"name":"Ashwini",    "lord":"Ketu",    "deity":"Ashwini Kumaras","symbol":"Horse's head",
     "quality":"Swift healing, beginnings, vitality, enthusiasm"},
    {"name":"Bharani",    "lord":"Venus",   "deity":"Yama","symbol":"Yoni (womb/vulva)",
     "quality":"Carrying burdens, creativity, restraint, nurturing transformations"},
    {"name":"Krittika",   "lord":"Sun",     "deity":"Agni","symbol":"Knife/flame",
     "quality":"Purification through fire, sharp focus, cutting away the false"},
    {"name":"Rohini",     "lord":"Moon",    "deity":"Brahma","symbol":"Ox cart/chariot",
     "quality":"Fertility, growth, creativity, beauty, sensuality, abundance"},
    {"name":"Mrigashira", "lord":"Mars",    "deity":"Soma","symbol":"Deer's head",
     "quality":"Searching, gentle sensitivity, wandering, artistic seeking"},
    {"name":"Ardra",      "lord":"Rahu",    "deity":"Rudra","symbol":"Teardrop/diamond",
     "quality":"Storms, destruction leading to renewal, raw power, grief"},
    {"name":"Punarvasu",  "lord":"Jupiter", "deity":"Aditi","symbol":"Quiver of arrows",
     "quality":"Return of light, restoration, optimism, expansion after difficulty"},
    {"name":"Pushya",     "lord":"Saturn",  "deity":"Brihaspati","symbol":"Cow's udder",
     "quality":"Nourishing, disciplined spiritual growth, the most auspicious nakshatra"},
    {"name":"Ashlesha",   "lord":"Mercury", "deity":"Nagas","symbol":"Coiled serpent",
     "quality":"Serpent wisdom, penetrating insight, kundalini, potential deception"},
    {"name":"Magha",      "lord":"Ketu",    "deity":"Pitris (ancestors)","symbol":"Throne",
     "quality":"Royal lineage, ancestral power, pride, karma of the fathers"},
    {"name":"Purva Phalguni","lord":"Venus","deity":"Bhaga","symbol":"Front legs of bed/hammock",
     "quality":"Creative enjoyment, romance, rest, pleasure, sensual expression"},
    {"name":"Uttara Phalguni","lord":"Sun", "deity":"Aryaman","symbol":"Rear legs of bed",
     "quality":"Patronage, contracts, unions, the benefits of generous giving"},
    {"name":"Hasta",      "lord":"Moon",    "deity":"Savitar","symbol":"Hand",
     "quality":"Skill, craftsmanship, healing hands, mental cleverness"},
    {"name":"Chitra",     "lord":"Mars",    "deity":"Tvastar","symbol":"Bright jewel/pearl",
     "quality":"Creating beauty, artistry, architectural genius, dazzling charisma"},
    {"name":"Swati",      "lord":"Rahu",    "deity":"Vayu","symbol":"Coral/sword/seedling",
     "quality":"Independence, flexibility like wind, trade, self-actualization"},
    {"name":"Vishakha",   "lord":"Jupiter", "deity":"Indra-Agni","symbol":"Triumphal arch",
     "quality":"Determined ambition, goal orientation, intensity, harvest after patience"},
    {"name":"Anuradha",   "lord":"Saturn",  "deity":"Mitra","symbol":"Lotus/staff",
     "quality":"Devoted friendship, organizational ability, occult power, spiritual practice"},
    {"name":"Jyeshtha",   "lord":"Mercury", "deity":"Indra","symbol":"Circular talisman",
     "quality":"Eldest/chief energy, protection, responsibility, occult power"},
    {"name":"Mula",       "lord":"Ketu",    "deity":"Nirriti","symbol":"Bundle of roots/lion's tail",
     "quality":"Root investigation, dissolution, examining foundations, destructive to rebuild"},
    {"name":"Purva Ashadha","lord":"Venus", "deity":"Apas (water)","symbol":"Fan/winnowing basket",
     "quality":"Invincibility, purification, declaring war, early victory"},
    {"name":"Uttara Ashadha","lord":"Sun",  "deity":"Vishvadevas","symbol":"Tusk of elephant",
     "quality":"Final victory, universal principles, unchallengeable righteousness"},
    {"name":"Shravana",   "lord":"Moon",    "deity":"Vishnu","symbol":"Ear/three footprints",
     "quality":"Learning by listening, connecting disparate things, Vishnu's preservation"},
    {"name":"Dhanishtha", "lord":"Mars",    "deity":"Eight Vasus","symbol":"Drum/flute",
     "quality":"Wealth, musical talent, marching forward, group harmony, abundance"},
    {"name":"Shatabhisha","lord":"Rahu",    "deity":"Varuna","symbol":"Empty circle/1000 stars",
     "quality":"Healing through solitude, cosmic secrets, reclusive mysticism"},
    {"name":"Purva Bhadrapada","lord":"Jupiter","deity":"Aja Ekapada","symbol":"Front of funeral cot",
     "quality":"Intense spiritual fire, elevated consciousness, eccentric wisdom"},
    {"name":"Uttara Bhadrapada","lord":"Saturn","deity":"Ahir Budhnya","symbol":"Back of funeral cot",
     "quality":"Depths of the cosmic serpent, wisdom accumulated over lifetimes, rain"},
    {"name":"Revati",     "lord":"Mercury", "deity":"Pushan","symbol":"Fish/drum",
     "quality":"Safe passage, journeys end, nourishing others, cosmic completion"},
]
NAKSHATRA_LORDS_SEQ = ["Ketu","Venus","Sun","Moon","Mars","Rahu","Jupiter","Saturn","Mercury"]
NAKSHATRA_DEGREES = 360/27  # 13.333...°

DASHA_YEARS = {"Ketu":7,"Venus":20,"Sun":6,"Moon":10,"Mars":7,"Rahu":18,"Jupiter":16,"Saturn":19,"Mercury":17}
DASHA_SEQUENCE = ["Ketu","Venus","Sun","Moon","Mars","Rahu","Jupiter","Saturn","Mercury"]

RASHI_LORDS = {
    "Ari":"Mars","Tau":"Venus","Gem":"Mercury","Can":"Moon","Leo":"Sun","Vir":"Mercury",
    "Lib":"Venus","Sco":"Mars","Sag":"Jupiter","Cap":"Saturn","Aqu":"Saturn","Pis":"Jupiter"
}

GRAHA_KARAKAS = {
    "Sun":    "Atma (soul), authority, father, government, health",
    "Moon":   "Mind, emotions, mother, public, liquids, the masses",
    "Mars":   "Energy, siblings, property, courage, accidents",
    "Mercury":"Speech, education, business, friends, mathematics",
    "Jupiter":"Wisdom, children, wealth, dharma, teachers, expansion",
    "Venus":  "Marriage, spouse, luxury, arts, vehicles, pleasures",
    "Saturn": "Longevity, service, suffering, karma, discipline, the masses",
    "Rahu":   "Obsession, foreign lands, illusion, sudden gains, material desire",
    "Ketu":   "Liberation, spirituality, past-life skills, loss, moksha",
}

VEDIC_HOUSE_MEANINGS = {
    1:  "Lagna — Self, body, personality, overall life direction",
    2:  "Dhana — Wealth, family, speech, early childhood",
    3:  "Sahaja — Courage, siblings, short journeys, effort, communication",
    4:  "Sukha — Mother, home, happiness, vehicles, education, heart",
    5:  "Putra — Children, intelligence, creativity, past-life merit, romance",
    6:  "Shatru — Enemies, debts, disease, service, daily work, obstacles overcome",
    7:  "Yuvati — Spouse, business partners, foreign travel, death (maraka)",
    8:  "Ayu — Longevity, hidden knowledge, transformation, inheritance, in-laws",
    9:  "Bhagya — Dharma, luck, father, higher wisdom, long journeys, spirituality",
    10: "Karma — Career, social status, government, fame, authority",
    11: "Labha — Income, gains, elder siblings, ambitions, social networks",
    12: "Vyaya — Loss, isolation, foreign lands, moksha, hidden enemies, sleep",
}

# ─────────────────────────────────────────────
# CHINESE BAZI DATA
# ─────────────────────────────────────────────

HEAVENLY_STEMS = {
    0: {"han":"甲","pinyin":"Jiǎ","element":"Wood","polarity":"Yang","nature":"Like a great tree — expansive leadership, pioneering"},
    1: {"han":"乙","pinyin":"Yǐ","element":"Wood","polarity":"Yin","nature":"Like flexible grass — adaptable, persistent, diplomatic"},
    2: {"han":"丙","pinyin":"Bǐng","element":"Fire","polarity":"Yang","nature":"Like the blazing sun — radiant, generous, extroverted"},
    3: {"han":"丁","pinyin":"Dīng","element":"Fire","polarity":"Yin","nature":"Like candlelight — illuminating subtly, precise, warm"},
    4: {"han":"戊","pinyin":"Wù","element":"Earth","polarity":"Yang","nature":"Like a mountain — solid, reliable, dependable, stoic"},
    5: {"han":"己","pinyin":"Jǐ","element":"Earth","polarity":"Yin","nature":"Like fertile soil — nurturing, receptive, subtle productivity"},
    6: {"han":"庚","pinyin":"Gēng","element":"Metal","polarity":"Yang","nature":"Like a sword — decisive, determined, righteous, cutting"},
    7: {"han":"辛","pinyin":"Xīn","element":"Metal","polarity":"Yin","nature":"Like a jewel — refined, aesthetic, precise, sensitive"},
    8: {"han":"Rén","pinyin":"Rén","element":"Water","polarity":"Yang","nature":"Like a great river — powerful flow, intelligent, strategic"},
    9: {"han":"癸","pinyin":"Guǐ","element":"Water","polarity":"Yin","nature":"Like rain or mist — gentle permeation, wisdom, adaptability"},
}

EARTHLY_BRANCHES = {
    0:  {"han":"子","pinyin":"Zǐ","animal":"Rat","element":"Water","hidden_stems":["Rén"],"hours":"23:00–01:00"},
    1:  {"han":"丑","pinyin":"Chǒu","animal":"Ox","element":"Earth","hidden_stems":["Jǐ","Xīn","Guǐ"],"hours":"01:00–03:00"},
    2:  {"han":"寅","pinyin":"Yín","animal":"Tiger","element":"Wood","hidden_stems":["Jiǎ","Bǐng","Wù"],"hours":"03:00–05:00"},
    3:  {"han":"卯","pinyin":"Mǎo","animal":"Rabbit","element":"Wood","hidden_stems":["Yǐ"],"hours":"05:00–07:00"},
    4:  {"han":"Chén","pinyin":"Chén","animal":"Dragon","element":"Earth","hidden_stems":["Wù","Yǐ","Guǐ"],"hours":"07:00–09:00"},
    5:  {"han":"巳","pinyin":"Sì","animal":"Snake","element":"Fire","hidden_stems":["Bǐng","Gēng","Wù"],"hours":"09:00–11:00"},
    6:  {"han":"午","pinyin":"Wǔ","animal":"Horse","element":"Fire","hidden_stems":["Bǐng","Dīng"],"hours":"11:00–13:00"},
    7:  {"han":"未","pinyin":"Wèi","animal":"Goat","element":"Earth","hidden_stems":["Jǐ","Dīng","Yǐ"],"hours":"13:00–15:00"},
    8:  {"han":"申","pinyin":"Shēn","animal":"Monkey","element":"Metal","hidden_stems":["Gēng","Rén","Wù"],"hours":"15:00–17:00"},
    9:  {"han":"酉","pinyin":"Yǒu","animal":"Rooster","element":"Metal","hidden_stems":["Xīn"],"hours":"17:00–19:00"},
    10: {"han":"戌","pinyin":"Xū","animal":"Dog","element":"Earth","hidden_stems":["Wù","Xīn","Dīng"],"hours":"19:00–21:00"},
    11: {"han":"亥","pinyin":"Hài","animal":"Pig","element":"Water","hidden_stems":["Rén","Jiǎ"],"hours":"21:00–23:00"},
}

ELEMENT_INTERACTIONS = {
    ("Wood","Fire"):   "generating",   # Wood feeds Fire
    ("Fire","Earth"):  "generating",
    ("Earth","Metal"): "generating",
    ("Metal","Water"): "generating",
    ("Water","Wood"):  "generating",
    ("Fire","Wood"):   "generated_by",
    ("Earth","Fire"):  "generated_by",
    ("Metal","Earth"): "generated_by",
    ("Water","Metal"): "generated_by",
    ("Wood","Water"):  "generated_by",
    ("Metal","Wood"):  "controlling",  # Metal cuts Wood
    ("Wood","Earth"):  "controlling",
    ("Earth","Water"): "controlling",
    ("Water","Fire"):  "controlling",
    ("Fire","Metal"):  "controlling",
    ("Wood","Metal"):  "controlled_by",
    ("Earth","Wood"):  "controlled_by",
    ("Water","Earth"): "controlled_by",
    ("Fire","Water"):  "controlled_by",
    ("Metal","Fire"):  "controlled_by",
}

ELEMENT_IMBALANCE_ADVICE = {
    "Wood":  "Seek creative outlets, spend time in nature, avoid over-planning. Strengthen with green foods and forest environments.",
    "Fire":  "Channel passion constructively, avoid burning out, cultivate joy. Strengthen with sunlight, red foods, social warmth.",
    "Earth": "Ground yourself with routines, avoid overthinking, nurture reliability. Strengthen with yellow/brown foods, mountains, meditation.",
    "Metal": "Pursue precision and refinement, set clear boundaries, let go of clutter. Strengthen with white foods, metal tools, clear structure.",
    "Water": "Trust your intuition, embrace stillness, allow flow. Strengthen with black/dark blue foods, water environments, reflective practice.",
}

CHINESE_ZODIAC_COMPATIBILITY = {
    "Rat":     {"best":["Dragon","Monkey"],"challenging":["Horse","Rabbit"],"neutral":["Ox","Snake","Rooster","Dog"]},
    "Ox":      {"best":["Snake","Rooster"],"challenging":["Goat","Horse","Dog"],"neutral":["Rat","Rabbit","Dragon","Pig"]},
    "Tiger":   {"best":["Horse","Dog"],"challenging":["Monkey","Snake"],"neutral":["Rabbit","Dragon","Goat","Rooster","Pig"]},
    "Rabbit":  {"best":["Goat","Pig"],"challenging":["Rooster","Dragon","Rat"],"neutral":["Ox","Tiger","Snake","Monkey","Dog"]},
    "Dragon":  {"best":["Rat","Monkey"],"challenging":["Dog","Rabbit","Dragon"],"neutral":["Ox","Tiger","Snake","Horse","Goat","Rooster","Pig"]},
    "Snake":   {"best":["Ox","Rooster"],"challenging":["Tiger","Pig"],"neutral":["Rat","Rabbit","Dragon","Horse","Goat","Monkey","Dog"]},
    "Horse":   {"best":["Tiger","Dog"],"challenging":["Rat","Ox"],"neutral":["Rabbit","Dragon","Snake","Goat","Monkey","Rooster","Pig"]},
    "Goat":    {"best":["Rabbit","Pig"],"challenging":["Ox","Dog","Rat"],"neutral":["Tiger","Dragon","Snake","Horse","Monkey","Rooster"]},
    "Monkey":  {"best":["Rat","Dragon"],"challenging":["Tiger","Pig"],"neutral":["Ox","Rabbit","Snake","Horse","Goat","Rooster","Dog"]},
    "Rooster": {"best":["Ox","Snake"],"challenging":["Rabbit","Dog","Rooster"],"neutral":["Rat","Tiger","Dragon","Horse","Goat","Monkey","Pig"]},
    "Dog":     {"best":["Tiger","Horse"],"challenging":["Dragon","Ox","Goat"],"neutral":["Rat","Rabbit","Snake","Monkey","Rooster","Pig"]},
    "Pig":     {"best":["Rabbit","Goat"],"challenging":["Snake","Monkey"],"neutral":["Rat","Ox","Tiger","Dragon","Horse","Rooster","Dog"]},
}

TAI_SUI_ANNUAL_BRANCHES = {
    # Year branch that conflicts with Tai Sui and what it means
    # Offenses: Direct clash (Chong), Punishment (Xing), Harm (Hai), Obstruction (Fan)
    0:  "Rat year — Tai Sui governs. Rats in direct alignment; others face indirect effects.",
    1:  "Ox year — Tai Sui governs Ox. Dog, Goat, Horse may face Fan Tai Sui or Chong.",
    2:  "Tiger year — Tai Sui governs Tiger. Monkey faces Chong (direct clash).",
    3:  "Rabbit year — Tai Sui governs Rabbit. Rooster faces Chong (direct clash).",
    4:  "Dragon year — Tai Sui governs Dragon. Dog faces Chong.",
    5:  "Snake year — Tai Sui governs Snake. Pig faces Chong.",
    6:  "Horse year — Tai Sui governs Horse. Rat faces Chong.",
    7:  "Goat year — Tai Sui governs Goat. Ox faces Chong.",
    8:  "Monkey year — Tai Sui governs Monkey. Tiger faces Chong.",
    9:  "Rooster year — Tai Sui governs Rooster. Rabbit faces Chong.",
    10: "Dog year — Tai Sui governs Dog. Dragon faces Chong.",
    11: "Pig year — Tai Sui governs Pig. Snake faces Chong.",
}


# ─────────────────────────────────────────────
# CALCULATION FUNCTIONS
# ─────────────────────────────────────────────

def calculate_western_chart(year, month, day, hour, minute, lat, lng, tz_str):
    """Full Western tropical natal chart via Swiss Ephemeris"""
    subject = AstrologicalSubject(
        "NatalChart",
        year=year, month=month, day=day,
        hour=hour, minute=minute,
        lat=lat, lng=lng, tz_str=tz_str,
        online=False
    )

    planets_data = {}
    planet_attrs = ['sun','moon','mercury','venus','mars','jupiter','saturn',
                    'uranus','neptune','pluto','chiron','true_north_lunar_node','true_south_lunar_node']
    for p in planet_attrs:
        try:
            obj = getattr(subject, p)
            if obj:
                sign_info = SIGN_KEYWORDS.get(obj.sign, {})
                house_num = int(obj.house.replace("_House","").replace("First","1")
                                .replace("Second","2").replace("Third","3").replace("Fourth","4")
                                .replace("Fifth","5").replace("Sixth","6").replace("Seventh","7")
                                .replace("Eighth","8").replace("Ninth","9").replace("Tenth","10")
                                .replace("Eleventh","11").replace("Twelfth","12")) if obj.house else 0
                planets_data[p] = {
                    "sign": obj.sign,
                    "sign_name": sign_info.get("name", obj.sign),
                    "sign_element": sign_info.get("element",""),
                    "sign_modality": sign_info.get("modality",""),
                    "sign_ruler": sign_info.get("ruler",""),
                    "degree": round(obj.position, 2),
                    "abs_degree": round(obj.abs_pos, 2),
                    "house": house_num,
                    "retrograde": obj.retrograde,
                    "archetype": PLANET_ARCHETYPES.get(p.replace("_"," ").title(),""),
                }
        except Exception:
            pass

    # Houses
    houses_data = {}
    house_attrs = ['first_house','second_house','third_house','fourth_house','fifth_house','sixth_house',
                   'seventh_house','eighth_house','ninth_house','tenth_house','eleventh_house','twelfth_house']
    for i, h in enumerate(house_attrs, 1):
        try:
            obj = getattr(subject, h)
            if obj:
                sign_info = SIGN_KEYWORDS.get(obj.sign, {})
                houses_data[i] = {
                    "sign": obj.sign,
                    "sign_name": sign_info.get("name", obj.sign),
                    "degree": round(obj.position, 2),
                    "meaning": HOUSE_MEANINGS.get(i, ""),
                    "ruler": sign_info.get("ruler",""),
                }
        except Exception:
            pass

    # Key angles
    asc = subject.first_house
    mc  = subject.tenth_house

    # Aspects
    aspects_data = []
    try:
        natal_aspects = NatalAspects(subject)
        for asp in natal_aspects.relevant_aspects[:30]:
            aspects_data.append({
                "planet1": asp.p1_name,
                "planet2": asp.p2_name,
                "aspect": asp.aspect,
                "orbit": round(asp.orbit, 2),
                "movement": asp.aspect_movement,
                "meaning": ASPECT_MEANINGS.get(asp.aspect, ""),
            })
    except Exception:
        pass

    # Element & modality distribution
    elem_count = {"Fire":0,"Earth":0,"Air":0,"Water":0}
    mod_count  = {"Cardinal":0,"Fixed":0,"Mutable":0}
    for p_data in planets_data.values():
        e = p_data.get("sign_element","")
        m = p_data.get("sign_modality","")
        if e in elem_count: elem_count[e] += 1
        if m in mod_count:  mod_count[m]  += 1

    # Big three
    sun_sign = planets_data.get("sun",{}).get("sign_name","")
    moon_sign = planets_data.get("moon",{}).get("sign_name","")
    asc_sign  = houses_data.get(1,{}).get("sign_name","")

    # Saturn return check
    birth_date = datetime(year, month, day)
    current_date = datetime(2026, 6, 6)
    age = (current_date - birth_date).days / 365.25
    saturn_return_upcoming = None
    for sr_age in SATURN_RETURN_AGES:
        if abs(age - sr_age) < 3:
            saturn_return_upcoming = {"age": sr_age, "approx_year": year + sr_age}

    return {
        "system": "Western Tropical",
        "big_three": {"sun": sun_sign, "moon": moon_sign, "ascendant": asc_sign},
        "planets": planets_data,
        "houses": houses_data,
        "aspects": aspects_data,
        "element_balance": elem_count,
        "modality_balance": mod_count,
        "saturn_return": saturn_return_upcoming,
        "ascendant": {"sign": asc.sign if asc else "", "degree": round(asc.position,2) if asc else 0},
        "midheaven": {"sign": mc.sign if mc else "", "degree": round(mc.position,2) if mc else 0},
    }


def calculate_vedic_chart(year, month, day, hour, minute, lat, lng, tz_str):
    """Full Vedic sidereal chart (Lahiri ayanamsha) via Swiss Ephemeris"""
    subject = AstrologicalSubject(
        "VedicChart",
        year=year, month=month, day=day,
        hour=hour, minute=minute,
        lat=lat, lng=lng, tz_str=tz_str,
        zodiac_type="Sidereal",
        sidereal_mode="LAHIRI",
        online=False
    )

    def house_num(house_str):
        mapping = {"First":1,"Second":2,"Third":3,"Fourth":4,"Fifth":5,"Sixth":6,
                   "Seventh":7,"Eighth":8,"Ninth":9,"Tenth":10,"Eleventh":11,"Twelfth":12}
        for k,v in mapping.items():
            if k in house_str: return v
        return 0

    planets_data = {}
    planet_attrs = ['sun','moon','mercury','venus','mars','jupiter','saturn',
                    'true_north_lunar_node','true_south_lunar_node']
    for p in planet_attrs:
        try:
            obj = getattr(subject, p)
            if obj:
                hn = house_num(obj.house) if obj.house else 0
                lord = RASHI_LORDS.get(obj.sign, "")
                planets_data[p] = {
                    "sign": obj.sign,
                    "sign_name": SIGN_KEYWORDS.get(obj.sign,{}).get("name", obj.sign),
                    "degree": round(obj.position, 2),
                    "abs_degree": round(obj.abs_pos, 2),
                    "house": hn,
                    "retrograde": obj.retrograde,
                    "rashi_lord": lord,
                    "karaka": GRAHA_KARAKAS.get(p.replace("true_north_lunar_node","Rahu")
                                                  .replace("true_south_lunar_node","Ketu")
                                                  .title().replace("_"," "), ""),
                    "house_meaning": VEDIC_HOUSE_MEANINGS.get(hn, ""),
                }
        except Exception:
            pass

    # Nakshatra for Moon (Janma Nakshatra)
    moon_abs = subject.moon.abs_pos if subject.moon else 0
    moon_nak_idx = int(moon_abs / NAKSHATRA_DEGREES) % 27
    moon_pada = int((moon_abs % NAKSHATRA_DEGREES) / (NAKSHATRA_DEGREES/4)) + 1
    moon_nak = NAKSHATRAS[moon_nak_idx]

    # Nakshatra for all planets
    planet_nakshatras = {}
    for p in planet_attrs:
        try:
            obj = getattr(subject, p)
            if obj:
                idx = int(obj.abs_pos / NAKSHATRA_DEGREES) % 27
                pada = int((obj.abs_pos % NAKSHATRA_DEGREES) / (NAKSHATRA_DEGREES/4)) + 1
                nak = NAKSHATRAS[idx]
                planet_nakshatras[p] = {
                    "nakshatra": nak["name"],
                    "lord": nak["lord"],
                    "deity": nak["deity"],
                    "pada": pada,
                    "quality": nak["quality"],
                }
        except Exception:
            pass

    # Vimshottari Dasha
    lord = moon_nak["lord"]
    moon_deg_in_nak = moon_abs % NAKSHATRA_DEGREES
    elapsed_fraction = moon_deg_in_nak / NAKSHATRA_DEGREES
    first_lord_idx = DASHA_SEQUENCE.index(lord)
    first_remaining_years = DASHA_YEARS[lord] * (1 - elapsed_fraction)

    birth_date = datetime(year, month, day)
    current_date = datetime(2026, 6, 6)

    dashas = []
    cur_end = birth_date + timedelta(days=first_remaining_years*365.25)
    dashas.append({"lord": lord, "start": birth_date.strftime("%Y-%m"), "end": cur_end.strftime("%Y-%m"),
                   "years": DASHA_YEARS[lord], "is_current": birth_date <= current_date <= cur_end})

    for offset in range(1, 10):
        next_lord = DASHA_SEQUENCE[(first_lord_idx + offset) % 9]
        next_start = cur_end
        next_end = next_start + timedelta(days=DASHA_YEARS[next_lord]*365.25)
        dashas.append({"lord": next_lord, "start": next_start.strftime("%Y-%m"), "end": next_end.strftime("%Y-%m"),
                       "years": DASHA_YEARS[next_lord], "is_current": next_start <= current_date <= next_end})
        cur_end = next_end

    current_dasha = next((d for d in dashas if d["is_current"]), dashas[0])

    # Lagna (Ascendant)
    lagna = subject.first_house
    lagna_sign = lagna.sign if lagna else ""

    return {
        "system": "Vedic (Jyotish) — Lahiri Sidereal",
        "lagna": {"sign": lagna_sign, "sign_name": SIGN_KEYWORDS.get(lagna_sign,{}).get("name",""),
                  "degree": round(lagna.position,2) if lagna else 0},
        "janma_rashi": {"sign": subject.moon.sign if subject.moon else "",
                        "sign_name": SIGN_KEYWORDS.get(subject.moon.sign,{}).get("name","") if subject.moon else ""},
        "janma_nakshatra": {
            "name": moon_nak["name"],
            "lord": moon_nak["lord"],
            "deity": moon_nak["deity"],
            "pada": moon_pada,
            "quality": moon_nak["quality"],
        },
        "planets": planets_data,
        "planet_nakshatras": planet_nakshatras,
        "vimshottari_dasha": {
            "birth_lord": lord,
            "current_mahadasha": current_dasha,
            "timeline": dashas,
        },
    }


def calculate_bazi(year, month, day, hour):
    """Chinese BaZi Four Pillars of Destiny"""

    def year_pillar(y):
        stem_idx  = (y - 4) % 10
        branch_idx = (y - 4) % 12
        return stem_idx, branch_idx

    def month_pillar(y, m):
        # Solar month based — month 1 = Feb in Chinese calendar
        # Using simplified approximation for Gregorian
        year_stem_idx = (y - 4) % 10
        # Month stems cycle: Jiǎ/Jǐ year → Bǐng starts month 1
        stem_bases = {0:2, 1:4, 2:6, 3:8, 4:0, 5:2, 6:4, 7:6, 8:8, 9:0}
        stem_idx = (stem_bases[year_stem_idx] + (m - 1)) % 10
        # Month branches: Feb=Tiger(2), Mar=Rabbit(3)... Jan=Ox(1)
        month_branch = {1:1, 2:2, 3:3, 4:4, 5:5, 6:6, 7:7, 8:8, 9:9, 10:10, 11:11, 12:0}
        branch_idx = month_branch[m]
        return stem_idx, branch_idx

    def day_pillar(y, m, d):
        # Day Jiazi cycle using Julian Day Number offset
        from datetime import datetime
        ref = datetime(1900, 1, 1)  # This was a Jiazi day (stem 0, branch 0)
        dt = datetime(y, m, d)
        delta = (dt - ref).days
        stem_idx = delta % 10
        branch_idx = delta % 12
        return stem_idx, branch_idx

    def hour_pillar(day_stem_idx, h):
        hour_branch_map = {23:0, 0:0, 1:1, 2:1, 3:2, 4:2, 5:3, 6:3,
                           7:4, 8:4, 9:5, 10:5, 11:6, 12:6, 13:7, 14:7,
                           15:8, 16:8, 17:9, 18:9, 19:10, 20:10, 21:11, 22:11}
        branch_idx = hour_branch_map.get(h, 0)
        stem_bases = {0:0, 1:2, 2:4, 3:6, 4:8, 5:0, 6:2, 7:4, 8:6, 9:8}
        stem_idx = (stem_bases[day_stem_idx % 10] + branch_idx) % 10
        return stem_idx, branch_idx

    ys, yb = year_pillar(year)
    ms, mb = month_pillar(year, month)
    ds, db = day_pillar(year, month, day)
    hs, hb = hour_pillar(ds, hour)

    def pillar_info(si, bi):
        stem = HEAVENLY_STEMS[si]
        branch = EARTHLY_BRANCHES[bi]
        return {
            "stem": {"han": stem["han"], "pinyin": stem["pinyin"],
                     "element": stem["element"], "polarity": stem["polarity"],
                     "nature": stem["nature"]},
            "branch": {"han": branch["han"], "pinyin": branch["pinyin"],
                       "animal": branch["animal"], "element": branch["element"],
                       "hours": branch.get("hours","")},
        }

    year_p  = pillar_info(ys, yb)
    month_p = pillar_info(ms, mb)
    day_p   = pillar_info(ds, db)
    hour_p  = pillar_info(hs, hb)

    # Day Master = Day Stem
    day_master = HEAVENLY_STEMS[ds]

    # Element count (stems + branches of all 4 pillars)
    elements = []
    for si, bi in [(ys,yb),(ms,mb),(ds,db),(hs,hb)]:
        elements.append(HEAVENLY_STEMS[si]["element"])
        elements.append(EARTHLY_BRANCHES[bi]["element"])

    from collections import Counter
    elem_count = dict(Counter(elements))

    # Determine missing/excess elements
    all_elements = ["Wood","Fire","Earth","Metal","Water"]
    for e in all_elements:
        if e not in elem_count:
            elem_count[e] = 0

    max_elem = max(elem_count, key=elem_count.get)
    min_elem = min(elem_count, key=elem_count.get)

    # Day master strength analysis (simplified)
    # Day master is strong if supported by month branch and many same-element pillars
    dm_element = day_master["element"]
    dm_count = sum(1 for e in elements if e == dm_element)
    # Supporting elements (elements that generate day master)
    generating = {"Wood":"Water","Fire":"Wood","Earth":"Fire","Metal":"Earth","Water":"Metal"}
    support_element = generating[dm_element]
    support_count = sum(1 for e in elements if e == support_element)
    dm_strength = "Strong" if (dm_count + support_count) >= 4 else ("Moderate" if (dm_count + support_count) >= 2 else "Weak")

    # Chinese zodiac animal
    year_animal = EARTHLY_BRANCHES[yb]["animal"]
    day_animal  = EARTHLY_BRANCHES[db]["animal"]
    compat = CHINESE_ZODIAC_COMPATIBILITY.get(year_animal, {})

    # Current year Tai Sui (2026 = Year of Horse, branch 6)
    current_year_branch = (2026 - 4) % 12  # = 6 = Horse
    tai_sui_info = TAI_SUI_ANNUAL_BRANCHES.get(current_year_branch, "")

    # Ten Year Luck Pillars (大运 Dà Yùn)
    # Direction depends on polarity of year stem
    year_stem_polarity = HEAVENLY_STEMS[ys]["polarity"]
    gender_is_male = True  # Will be overridden by actual gender if provided
    # Forward if: Yang year + Male OR Yin year + Female
    # Backward if: Yin year + Male OR Yang year + Female
    # We'll include both and let the interpreter decide
    luck_pillars = []
    # Simplified: start from month pillar, advance one stem/branch per 10 years
    lp_start_age = 8  # approximation (more precisely based on solar terms)
    for i in range(8):
        lp_stem = (ms + (i+1)) % 10
        lp_branch = (mb + (i+1)) % 12
        lp_age_start = lp_start_age + i*10
        lp_age_end = lp_age_start + 9
        birth_date = datetime(year, month, day)
        lp_year_start = year + lp_age_start
        lp_stem_data = HEAVENLY_STEMS[lp_stem]
        lp_branch_data = EARTHLY_BRANCHES[lp_branch]
        luck_pillars.append({
            "age": f"{lp_age_start}–{lp_age_end}",
            "approximate_years": f"{lp_year_start}–{lp_year_start+9}",
            "stem": lp_stem_data["pinyin"],
            "branch": lp_branch_data["animal"],
            "stem_element": lp_stem_data["element"],
            "branch_element": lp_branch_data["element"],
        })

    return {
        "system": "Chinese BaZi (Four Pillars of Destiny)",
        "four_pillars": {
            "year":  year_p,
            "month": month_p,
            "day":   day_p,
            "hour":  hour_p,
        },
        "day_master": {
            "han":     day_master["han"],
            "pinyin":  day_master["pinyin"],
            "element": day_master["element"],
            "polarity":day_master["polarity"],
            "nature":  day_master["nature"],
            "strength": dm_strength,
        },
        "element_balance": elem_count,
        "dominant_element": max_elem,
        "missing_element": min_elem,
        "missing_element_advice": ELEMENT_IMBALANCE_ADVICE.get(min_elem,""),
        "year_animal": year_animal,
        "day_animal":  day_animal,
        "zodiac_compatibility": compat,
        "ten_year_luck_pillars": luck_pillars,
        "tai_sui_2026": tai_sui_info,
    }


def get_timezone_for_coords(lat, lng):
    """Simple timezone estimation from longitude (fallback if tz_str not provided)"""
    offset_hours = round(lng / 15)
    if offset_hours >= 0:
        return f"Etc/GMT-{offset_hours}"
    else:
        return f"Etc/GMT+{abs(offset_hours)}"


def calculate_full_profile(data):
    """Master function: calculate all requested chart systems"""
    year    = data.get("year")
    month   = data.get("month")
    day     = data.get("day")
    hour    = data.get("hour", 12)
    minute  = data.get("minute", 0)
    lat     = data.get("lat", 0.0)
    lng     = data.get("lng", 0.0)
    tz_str  = data.get("tz_str") or get_timezone_for_coords(lat, lng)
    systems = data.get("systems", ["western","vedic","bazi"])

    result = {"input": data, "charts": {}}

    if "western" in systems:
        try:
            result["charts"]["western"] = calculate_western_chart(year, month, day, hour, minute, lat, lng, tz_str)
        except Exception as e:
            result["charts"]["western"] = {"error": str(e)}

    if "vedic" in systems:
        try:
            result["charts"]["vedic"] = calculate_vedic_chart(year, month, day, hour, minute, lat, lng, tz_str)
        except Exception as e:
            result["charts"]["vedic"] = {"error": str(e)}

    if "bazi" in systems:
        try:
            result["charts"]["bazi"] = calculate_bazi(year, month, day, hour)
        except Exception as e:
            result["charts"]["bazi"] = {"error": str(e)}

    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Astrology calculation engine")
    parser.add_argument("--json", help="JSON birth data string")
    parser.add_argument("--file", help="Path to JSON birth data file")
    args = parser.parse_args()

    if args.json:
        data = json.loads(args.json)
    elif args.file:
        with open(args.file) as f:
            data = json.load(f)
    else:
        # Demo run
        data = {
            "year": 1990, "month": 6, "day": 15,
            "hour": 14, "minute": 30,
            "lat": 40.7128, "lng": -74.0060,
            "tz_str": "America/New_York",
            "systems": ["western","vedic","bazi"]
        }

    result = calculate_full_profile(data)
    print(json.dumps(result, indent=2, default=str))