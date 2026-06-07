# Chinese BaZi (Four Pillars of Destiny) — interpretation ruleset

BaZi (八字, "eight characters") maps birth to four **pillars** (year, month, day, hour),
each a **Heavenly Stem** + **Earthly Branch**, each carrying one of the **Five Elements**
(Wu Xing). It's a system of *elemental balance and life-cycle timing*, not zodiac
personality. The engine computes pillars with solar-term-correct year and month.

## 1. The Day Master (日主) — the self
The **Day Stem** is *you*. The engine gives its element, polarity (Yin/Yang), poetic
nature, and a **strength** rating (Strong / Balanced / Weak) with a ratio. Everything is
read relative to the Day Master. The ten Day Masters:
Jiǎ (Yang Wood, great tree) · Yǐ (Yin Wood, vine) · Bǐng (Yang Fire, sun) · Dīng (Yin
Fire, lamp) · Wù (Yang Earth, mountain) · Jǐ (Yin Earth, field) · Gēng (Yang Metal,
axe) · Xīn (Yin Metal, jewel) · Rén (Yang Water, ocean) · Guǐ (Yin Water, rain).

## 2. The Five Elements & their cycles
Wood→Fire→Earth→Metal→Water→Wood (**generating**, sheng). Wood→Earth→Water→Fire→Metal→
Wood (**controlling**, ke). The engine returns the **element balance** (weighted tally
over stems, branches, and hidden stems), the **dominant** and **weakest** element.

A life runs smoothly when the elements **flow**; suffering shows up as **imbalance** — a
missing element (a capacity you lack and must cultivate) or a flooding one (a force that
overwhelms). Engine `element_advice` gives the practical correction per element
(colours, directions, activities, foods).

## 3. The Useful God (用神) — the key to the whole chart
The single most important judgement: which element the Day Master **needs**.
- **Weak Day Master** → needs **Resource** (the element that generates it) and **Friend**
  (its own element) to gain strength. Engine `favourable_elements`.
- **Strong Day Master** → needs **Output** (what it generates), **Wealth** (what it
  controls), and **Officer** (what controls it) to drain and channel its excess.
- **Balanced** → favour gentle flow without tipping it.

The favourable elements are the person's **luck levers**: the colours to wear, careers,
environments, and the luck-pillar/annual years (matching those elements) that go well.
The unfavourable elements flag the hard years and the forces to manage.

## 4. The Ten Gods (十神) — roles around the self
The engine labels each other stem's relationship to the Day Master. They translate to
life themes:
- **Friend / Rob Wealth** (same element) — peers, competition, allies, ego.
- **Resource — Direct/Indirect Print** (feeds DM) — support, mother, learning, security.
- **Output — Eating God / Hurting Officer** (DM produces) — talent, expression, children, performance, rebellion.
- **Wealth — Direct/Indirect** (DM controls) — money, the body, (for men) wife, control of resources.
- **Officer — Direct Officer / Seven Killings** (controls DM) — authority, career, discipline, pressure, (for women) husband.
Read the dominant Ten God as the chart's life-driver (e.g. heavy Output = a creative/
performer; heavy Officer = drawn to status/structure or feeling pressured by it).

## 5. The Pillars as life-stages & relationships
Year = ancestry, early life, society, the public self (its branch = your **zodiac
animal**). Month = parents, career foundation, your 20s–40s engine (the most weighted
pillar for strength). Day branch = the self's inner life and the **spouse palace**.
Hour = children, late life, ambitions, legacy. The **hidden stems** inside each branch
add subtle elemental influences (engine lists them).

## 6. Luck Pillars (大運) — the ten-year fortune cycles
The engine returns 8 luck pillars (each a 10-year era) with their elements, direction
(forward/reverse by year-stem polarity + gender), and which is **current**. Read a luck
pillar by whether its element is **favourable** (a supported, flowing decade) or
**unfavourable** (a decade demanding effort and care). This is BaZi's long-range
forecasting — say which decade-era the person is in and what it brings.

## 7. The annual year & Tai Sui (太歲)
The engine gives the current year's animal and the person's **Tai Sui** standing:
- **本命年 (Ben Ming Nian)** — your own animal's year: be steady, avoid big risky leaps.
- **沖 (clash)** — the opposite animal's year: movement, change, friction → channel into deliberate transitions.
- **害 (harm)** — guard relationships and health.
Traditionally one "pays respects to Tai Sui" in such years (caution, charity, red items).
Frame as a season to navigate wisely, not a curse.

## 8. The zodiac animal (the popular layer)
The **year branch animal** is the familiar "Chinese sign." Engine `zodiac_compatibility`
gives best matches, clash, and harm animal. Useful for light compatibility, but the real
BaZi compatibility is **element matching** between two charts' Day Masters and useful gods.

## Reading recipe
1. Name the Day Master (element + nature) and its **strength**.
2. State the **Useful God** — the element they need — and the practical levers (colour/
   direction/career) and good vs. hard years from it.
3. Read the element balance: what floods, what's missing, what to cultivate.
4. Identify the dominant Ten God → the life-driver.
5. Locate them in the **current luck pillar** (favourable or testing decade) and the
   **annual / Tai Sui** standing → the now and the year ahead.
6. End with one concrete elemental practice from `element_advice`.
