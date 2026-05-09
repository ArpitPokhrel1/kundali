"""Topic-based readings — Education, Health, Career, Marriage, Wealth,
Family, Travel, Spirituality.

Each topic returns a `TopicReading` with relevant houses, karakas, observations,
and a short prose summary. Observations are bilingual.
"""
from __future__ import annotations
from dataclasses import dataclass, field

from .dignities import (
    RASHI_LORDS, EXALTATION, OWN, BENEFICS_NATURAL, MALEFICS_NATURAL,
    dignity_of,
)


@dataclass
class TopicReading:
    key: str             # 'education', 'health', etc.
    name_en: str
    name_ne: str
    icon: str
    houses: list[int]    # relevant houses
    karakas: list[str]   # significator planets
    findings_en: list[str]
    findings_ne: list[str]
    summary_en: str
    summary_ne: str


def _house_of(rashi: int, lagna_rashi: int) -> int:
    return ((rashi - lagna_rashi) % 12) + 1


def _planets_in_house(positions: dict, lagna_rashi: int, house: int) -> list[str]:
    target_rashi = (lagna_rashi + house - 1) % 12
    return [name for name, p in positions.items() if p.rashi == target_rashi]


def _lord_of_house(lagna_rashi: int, house: int) -> str:
    rashi = (lagna_rashi + house - 1) % 12
    return RASHI_LORDS[rashi]


def _describe_lord(positions, lagna_rashi: int, lord: str, lord_of: int) -> tuple[str, str]:
    """Return (en, ne) sentence describing where this lord sits."""
    if lord not in positions:
        return "", ""
    p = positions[lord]
    house = _house_of(p.rashi, lagna_rashi)
    dign = dignity_of(lord, p.longitude)
    en = (f"Lord of the {_ord(lord_of)} ({lord}) sits in the {_ord(house)} "
          f"house ({dign}).")
    ne = (f"{lord_of} औं भावको स्वामी ({lord}) {house} औं भावमा छ ({dign})।")
    return en, ne


def _ord(n: int) -> str:
    s = str(n)
    if 11 <= n % 100 <= 13:
        return f"{n}th"
    return s + {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")


def _karaka_status(positions, lagna_rashi: int, planet: str) -> tuple[str, str]:
    if planet not in positions:
        return "", ""
    p = positions[planet]
    house = _house_of(p.rashi, lagna_rashi)
    dign = dignity_of(planet, p.longitude)
    en = f"{planet} (significator) is in house {house}, {dign}."
    ne = f"{planet} (कारक) भाव {house} मा, स्थिति: {dign}।"
    return en, ne


def _scan_houses(positions, lagna_rashi: int, houses: list[int]):
    """Yield (house_number, planets_in_it) for each requested house."""
    for h in houses:
        yield h, _planets_in_house(positions, lagna_rashi, h)


# ---------------------------------------------------------------------------
# Topic-specific analyzers
# ---------------------------------------------------------------------------

def _add_lord_finding(findings_en, findings_ne, positions, lagna_rashi, house):
    en, ne = _describe_lord(positions, lagna_rashi, _lord_of_house(lagna_rashi, house), house)
    if en:
        findings_en.append(en)
        findings_ne.append(ne)


def _add_karaka_finding(findings_en, findings_ne, positions, lagna_rashi, planet):
    en, ne = _karaka_status(positions, lagna_rashi, planet)
    if en:
        findings_en.append(en)
        findings_ne.append(ne)


def _scan_house_finding(findings_en, findings_ne, positions, lagna_rashi, house):
    planets = _planets_in_house(positions, lagna_rashi, house)
    if planets:
        findings_en.append(
            f"House {house} contains: {', '.join(planets)}."
        )
        findings_ne.append(
            f"भाव {house} मा: {', '.join(planets)}।"
        )


def analyze_education(positions, lagna_rashi: int) -> TopicReading:
    fe, fn = [], []
    for h in (4, 5, 9):
        _scan_house_finding(fe, fn, positions, lagna_rashi, h)
        _add_lord_finding(fe, fn, positions, lagna_rashi, h)
    for k in ("Mercury", "Jupiter"):
        _add_karaka_finding(fe, fn, positions, lagna_rashi, k)

    # Buddha-Aditya (scholar combination)
    if positions["Sun"].rashi == positions["Mercury"].rashi:
        fe.append("Sun and Mercury share a sign — Buddha-Aditya (sharp intellect).")
        fn.append("सूर्य र बुध एउटै राशिमा — बुधादित्य योग (तीव्र बुद्धि)।")

    # Mercury+Jupiter together = pure scholar
    if positions["Mercury"].rashi == positions["Jupiter"].rashi:
        fe.append("Mercury and Jupiter share a sign — wisdom + intellect together (scholar).")
        fn.append("बुध र बृहस्पति एउटै राशिमा — बुद्धि र ज्ञानको संयोग (विद्वान्)।")

    summary_en = (
        "Education is read primarily from house 4 (formal schooling, mother's "
        "support), house 5 (intellect, creativity, past-life merit), and house 9 "
        "(higher learning, gurus, dharma). The intellect-karaka is Mercury; the "
        "wisdom-karaka is Jupiter. Strong placements of these — and clear lords "
        "of 4, 5, 9 — typically support a smooth educational path."
    )
    summary_ne = (
        "शिक्षा हेर्न मुख्यतया भाव ४ (विद्यालय, आमाको सहयोग), भाव ५ "
        "(बुद्धि, सिर्जना, पूर्व-जन्म पुण्य), र भाव ९ (उच्च शिक्षा, गुरु, "
        "धर्म) हेरिन्छन्। बुद्धिको कारक बुध; ज्ञानको कारक गुरु। यिनको बलियो "
        "स्थान, र भाव ४/५/९ का स्वामीहरू स्पष्ट हुनु — शिक्षाको बाटो "
        "सहज बनाउँछ।"
    )
    return TopicReading(
        "education", "Education", "शिक्षा", "🎓",
        [4, 5, 9], ["Mercury", "Jupiter"],
        fe, fn, summary_en, summary_ne,
    )


def analyze_health(positions, lagna_rashi: int) -> TopicReading:
    fe, fn = [], []
    for h in (1, 6, 8, 12):
        _scan_house_finding(fe, fn, positions, lagna_rashi, h)
        _add_lord_finding(fe, fn, positions, lagna_rashi, h)
    for k in ("Sun", "Moon", "Mars", "Saturn"):
        _add_karaka_finding(fe, fn, positions, lagna_rashi, k)

    # Lagna lord placement
    lagna_lord = _lord_of_house(lagna_rashi, 1)
    if lagna_lord in positions:
        h = _house_of(positions[lagna_lord].rashi, lagna_rashi)
        if h in (6, 8, 12):
            fe.append(
                f"Lagna lord ({lagna_lord}) sits in {_ord(h)} (a dusthana) — "
                f"classical caution about constitutional vitality; needs "
                f"supportive routine."
            )
            fn.append(
                f"लग्न-स्वामी ({lagna_lord}) भाव {h} (दुस्थान) मा — "
                f"शारीरिक ऊर्जामा सतर्कताको शास्त्रीय सङ्केत; "
                f"नियमित दिनचर्या आवश्यक।"
            )

    summary_en = (
        "Health is read from house 1 (the body, vitality), house 6 (illness, "
        "daily strain), house 8 (longevity, chronic conditions), and house 12 "
        "(rest, hospitalization). The Sun governs vitality; Moon governs the "
        "mind and fluids; Mars rules blood and inflammation; Saturn rules "
        "chronic patterns and the bones. A strong Lagna lord and benefic "
        "support to the 1st are the foundation of robust health."
    )
    summary_ne = (
        "स्वास्थ्य हेर्न भाव १ (शरीर, ओज), भाव ६ (रोग, दैनिक श्रम), भाव ८ "
        "(दीर्घायु, दीर्घ रोग), र भाव १२ (विश्राम, अस्पताल) हेरिन्छन्। "
        "सूर्य ओजको कारक; चन्द्र मन र तरलको; मङ्गल रगत र सूजनको; शनि दीर्घ "
        "रोग र हाडको। बलियो लग्न-स्वामी र भाव १ मा शुभ ग्रहको सहयोग — "
        "स्वस्थ जीवनको आधार।"
    )
    return TopicReading(
        "health", "Health", "स्वास्थ्य", "❤️",
        [1, 6, 8, 12], ["Sun", "Moon", "Mars", "Saturn"],
        fe, fn, summary_en, summary_ne,
    )


def analyze_career(positions, lagna_rashi: int) -> TopicReading:
    fe, fn = [], []
    for h in (6, 10, 11):
        _scan_house_finding(fe, fn, positions, lagna_rashi, h)
        _add_lord_finding(fe, fn, positions, lagna_rashi, h)
    for k in ("Sun", "Saturn", "Mercury", "Jupiter"):
        _add_karaka_finding(fe, fn, positions, lagna_rashi, k)

    # Career field hint based on what's strongest in 10th
    h10_planets = _planets_in_house(positions, lagna_rashi, 10)
    if h10_planets:
        FIELD = {
            "Sun":     ("government, leadership, authority",
                        "सरकार, नेतृत्व, अधिकार"),
            "Moon":    ("public-facing work, hospitality, food, healthcare",
                        "जनसम्पर्क, आतिथ्य, खाद्य, स्वास्थ्य"),
            "Mars":    ("technical, military, sports, engineering, surgery",
                        "प्राविधिक, सेना, खेलकुद, इन्जिनियरिङ, शल्यक्रिया"),
            "Mercury": ("commerce, writing, communication, software",
                        "व्यापार, लेखन, सञ्चार, सफ्टवेयर"),
            "Jupiter": ("teaching, advisory, law, finance, religion",
                        "शिक्षण, सल्लाह, कानून, वित्त, धर्म"),
            "Venus":   ("arts, design, fashion, hospitality, diplomacy",
                        "कला, डिजाइन, फेसन, आतिथ्य, कूटनीति"),
            "Saturn":  ("manufacturing, mining, civil service, slow-built work",
                        "उत्पादन, खानी, निजामती सेवा, ढिलो तर पक्का काम"),
            "Rahu":    ("foreign work, technology, unconventional fields",
                        "विदेशी काम, प्रविधि, अपरम्परागत क्षेत्र"),
            "Ketu":    ("research, healing, investigation, occult studies",
                        "अनुसन्धान, उपचार, गुप्त विषयको अध्ययन"),
        }
        for p in h10_planets:
            if p in FIELD:
                fe.append(f"{p} in 10th suggests {FIELD[p][0]}.")
                fn.append(f"१० भावमा {p} → {FIELD[p][1]} क्षेत्र अनुकूल।")

    summary_en = (
        "Career is read from house 10 (profession, public role), house 6 "
        "(service, daily work), and house 11 (gains, networks). The four "
        "career karakas are Sun (govt/authority), Saturn (effort/labor), "
        "Mercury (business/communication), and Jupiter (advisory/wisdom). "
        "The planet(s) in or aspecting the 10th give the strongest hint "
        "about the natural field."
    )
    summary_ne = (
        "करियर हेर्न भाव १० (पेशा, सार्वजनिक भूमिका), भाव ६ (सेवा, दैनिक "
        "काम), र भाव ११ (लाभ, सम्पर्क) हेरिन्छन्। चार कारक: सूर्य "
        "(सरकार/अधिकार), शनि (श्रम), बुध (व्यापार/सञ्चार), र गुरु "
        "(सल्लाह/ज्ञान)। १० औं भावमा वा त्यसलाई हेर्ने ग्रहले प्राकृतिक "
        "करियर क्षेत्रको सबभन्दा बलियो सङ्केत दिन्छ।"
    )
    return TopicReading(
        "career", "Career & Employment", "करियर र रोजगार", "💼",
        [6, 10, 11], ["Sun", "Saturn", "Mercury", "Jupiter"],
        fe, fn, summary_en, summary_ne,
    )


def analyze_wealth(positions, lagna_rashi: int) -> TopicReading:
    fe, fn = [], []
    for h in (2, 5, 9, 11):
        _scan_house_finding(fe, fn, positions, lagna_rashi, h)
        _add_lord_finding(fe, fn, positions, lagna_rashi, h)
    for k in ("Jupiter", "Venus"):
        _add_karaka_finding(fe, fn, positions, lagna_rashi, k)

    # Dhana yoga: 2nd & 11th lords conjunct
    l2 = _lord_of_house(lagna_rashi, 2)
    l11 = _lord_of_house(lagna_rashi, 11)
    if l2 != l11 and l2 in positions and l11 in positions:
        if positions[l2].rashi == positions[l11].rashi:
            fe.append(
                f"Lords of 2nd ({l2}) and 11th ({l11}) join — classical Dhana yoga."
            )
            fn.append(
                f"भाव २ ({l2}) र भाव ११ ({l11}) का स्वामी मिलेका — शास्त्रीय धन योग।"
            )

    summary_en = (
        "Wealth is read from house 2 (savings, family wealth), house 11 "
        "(active gains, networks), house 5 (lucky speculative gains, "
        "past-life merit), and house 9 (fortune, paternal wealth). Jupiter is "
        "the wealth karaka; Venus governs luxury. Connections between the "
        "lords of 2/5/9/11 form the various Dhana yogas."
    )
    summary_ne = (
        "धन हेर्न भाव २ (बचत, पारिवारिक सम्पत्ति), भाव ११ (आम्दानी, सम्पर्क), "
        "भाव ५ (अनपेक्षित लाभ, पुण्य), र भाव ९ (भाग्य, बुबाको सम्पत्ति) "
        "हेरिन्छन्। गुरु धनको कारक; शुक्र विलासिताको। भाव २/५/९/११ का "
        "स्वामीहरूको सम्बन्धले विभिन्न धन योग बनाउँछन्।"
    )
    return TopicReading(
        "wealth", "Wealth & Finance", "धन र वित्त", "💰",
        [2, 5, 9, 11], ["Jupiter", "Venus"],
        fe, fn, summary_en, summary_ne,
    )


def analyze_marriage(positions, lagna_rashi: int) -> TopicReading:
    fe, fn = [], []
    for h in (2, 7, 8, 12):
        _scan_house_finding(fe, fn, positions, lagna_rashi, h)
        _add_lord_finding(fe, fn, positions, lagna_rashi, h)
    for k in ("Venus", "Jupiter"):
        _add_karaka_finding(fe, fn, positions, lagna_rashi, k)

    # Mangal Dosha (Mars in 1, 4, 7, 8, 12 from Lagna)
    mars_house = _house_of(positions["Mars"].rashi, lagna_rashi)
    if mars_house in (1, 4, 7, 8, 12):
        fe.append(
            f"Mars sits in house {mars_house} from Lagna — known as Mangal "
            f"(Kuja) Dosha in classical tradition. Caveats apply: many "
            f"cancellations exist (Mars in own/exalted, similar dosha in "
            f"partner's chart, etc.). Treat as a flag, not a verdict."
        )
        fn.append(
            f"मङ्गल लग्नबाट भाव {mars_house} मा — शास्त्रीय 'मङ्गल दोष'। "
            f"धेरै अपवाद छन् (मङ्गल आफ्नै/उच्च राशि, साथीको कुण्डलीमा पनि "
            f"त्यस्तै दोष, इत्यादि)। यो एक सङ्केत हो — अन्तिम निर्णय होइन।"
        )

    # Saturn in 7th = late marriage tendency
    sat_house = _house_of(positions["Saturn"].rashi, lagna_rashi)
    if sat_house == 7:
        fe.append("Saturn in 7th — classical: marriage tends to be late or to a serious / older partner.")
        fn.append("शनि भाव ७ मा — शास्त्र: विवाह ढिलो वा गम्भीर/वृद्ध साथी।")

    summary_en = (
        "Marriage is read from house 7 (spouse, partnership) — primary; house "
        "2 (extended family); house 8 (intimacy, in-laws); house 12 (bedroom). "
        "Venus is the karaka of marriage for men; Jupiter is the karaka for "
        "women (and indicates the husband). For deeper marriage analysis, "
        "the D9 navamsha chart is examined alongside the rasi chart."
    )
    summary_ne = (
        "विवाह हेर्न भाव ७ (जीवनसाथी, साझेदारी) — मुख्य; भाव २ (विस्तारित "
        "परिवार); भाव ८ (अन्तरङ्गता, ससुराली); भाव १२ (शयनकक्ष)। पुरुषका "
        "लागि शुक्र विवाहको कारक; महिलाका लागि गुरु (पतिको प्रतीक)। "
        "विवाहको गहन अध्ययनमा D9 नवांश पनि हेरिन्छ।"
    )
    return TopicReading(
        "marriage", "Marriage & Partnership", "विवाह र साझेदारी", "💍",
        [2, 7, 8, 12], ["Venus", "Jupiter"],
        fe, fn, summary_en, summary_ne,
    )


def analyze_family(positions, lagna_rashi: int) -> TopicReading:
    fe, fn = [], []
    for h in (3, 4, 5, 9, 11):
        _add_lord_finding(fe, fn, positions, lagna_rashi, h)
    for k in ("Sun", "Moon", "Mars", "Jupiter"):
        _add_karaka_finding(fe, fn, positions, lagna_rashi, k)

    summary_en = (
        "Family is read across multiple houses: 4th (mother, home), 9th "
        "(father, ancestral wisdom), 5th (children, creativity), 3rd "
        "(younger siblings), 11th (elder siblings). The karakas are Moon "
        "(mother), Sun (father), Jupiter (children — for men), Mars "
        "(siblings)."
    )
    summary_ne = (
        "परिवार धेरै भावबाट हेरिन्छ: ४ (आमा, घर), ९ (बुबा, पुर्ख्यौली ज्ञान), "
        "५ (सन्तान, सिर्जना), ३ (भाइ-बहिनी कान्छो), ११ (दाजुदिदी)। कारक: "
        "चन्द्र (आमा), सूर्य (बुबा), गुरु (सन्तान — पुरुषका लागि), मङ्गल "
        "(भाइ)।"
    )
    return TopicReading(
        "family", "Family & Children", "परिवार र सन्तान", "👪",
        [3, 4, 5, 9, 11], ["Sun", "Moon", "Mars", "Jupiter"],
        fe, fn, summary_en, summary_ne,
    )


def analyze_travel(positions, lagna_rashi: int) -> TopicReading:
    fe, fn = [], []
    for h in (3, 9, 12):
        _scan_house_finding(fe, fn, positions, lagna_rashi, h)
        _add_lord_finding(fe, fn, positions, lagna_rashi, h)
    for k in ("Moon", "Rahu"):
        _add_karaka_finding(fe, fn, positions, lagna_rashi, k)

    # Strong Rahu in 9 or 12 → foreign settlement
    rahu_house = _house_of(positions["Rahu"].rashi, lagna_rashi)
    if rahu_house in (9, 12):
        fe.append(f"Rahu in house {rahu_house} — strong indicator of foreign travel or settlement.")
        fn.append(f"राहु भाव {rahu_house} मा — विदेश यात्रा/बसाइँको बलियो सङ्केत।")

    summary_en = (
        "Travel is read from house 3 (short trips, neighborhood), house 9 "
        "(long journeys, foreign visits), and house 12 (foreign settlement, "
        "leaving the homeland). Moon governs movement; Rahu rules everything "
        "foreign and unconventional."
    )
    summary_ne = (
        "यात्रा हेर्न भाव ३ (छोटो यात्रा, छिमेक), भाव ९ (लामो यात्रा, विदेश "
        "भ्रमण), र भाव १२ (विदेश बसाइँ, मातृभूमि छोड्ने) हेरिन्छन्। चन्द्र "
        "गति-कारक; राहु विदेशी र अपरम्परागत कुराको कारक।"
    )
    return TopicReading(
        "travel", "Travel & Foreign", "यात्रा र विदेश", "✈️",
        [3, 9, 12], ["Moon", "Rahu"],
        fe, fn, summary_en, summary_ne,
    )


def analyze_spirituality(positions, lagna_rashi: int) -> TopicReading:
    fe, fn = [], []
    for h in (5, 8, 9, 12):
        _scan_house_finding(fe, fn, positions, lagna_rashi, h)
        _add_lord_finding(fe, fn, positions, lagna_rashi, h)
    for k in ("Jupiter", "Ketu", "Saturn"):
        _add_karaka_finding(fe, fn, positions, lagna_rashi, k)

    # Ketu in 9/12 = strong moksha indicator
    ketu_house = _house_of(positions["Ketu"].rashi, lagna_rashi)
    if ketu_house in (9, 12):
        fe.append(f"Ketu in house {ketu_house} — strong moksha-tendency, deep spiritual leanings.")
        fn.append(f"केतु भाव {ketu_house} मा — गहिरो आध्यात्मिक प्रवृत्ति, मोक्ष-मार्ग।")

    summary_en = (
        "Spirituality and dharma are read from house 5 (devotion, mantra), "
        "house 8 (occult, hidden knowledge), house 9 (dharma, religion, gurus), "
        "and house 12 (moksha, meditation, withdrawal). Jupiter is the dharma "
        "karaka; Ketu is the moksha karaka; Saturn governs ascetic discipline."
    )
    summary_ne = (
        "अध्यात्म र धर्म हेर्न भाव ५ (भक्ति, मन्त्र), भाव ८ (गुप्त ज्ञान), "
        "भाव ९ (धर्म, गुरु), र भाव १२ (मोक्ष, ध्यान, एकान्त) हेरिन्छन्। "
        "गुरु धर्मको कारक; केतु मोक्षको; शनि तपस्याको।"
    )
    return TopicReading(
        "spirituality", "Spirituality & Dharma", "अध्यात्म र धर्म", "🕉️",
        [5, 8, 9, 12], ["Jupiter", "Ketu", "Saturn"],
        fe, fn, summary_en, summary_ne,
    )


def analyze_all(positions, lagna_rashi: int) -> list[TopicReading]:
    """Run every topic analyzer in display order."""
    return [
        analyze_education(positions, lagna_rashi),
        analyze_health(positions, lagna_rashi),
        analyze_career(positions, lagna_rashi),
        analyze_wealth(positions, lagna_rashi),
        analyze_marriage(positions, lagna_rashi),
        analyze_family(positions, lagna_rashi),
        analyze_travel(positions, lagna_rashi),
        analyze_spirituality(positions, lagna_rashi),
    ]
