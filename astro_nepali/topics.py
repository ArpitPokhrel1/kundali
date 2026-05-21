"""Topic-based readings — Education, Health, Career, Marriage, Wealth,
Family, Travel, Spirituality.

Each topic returns a `TopicReading` with relevant houses, karakas, observations,
and a short prose summary. Findings are bilingual and now include an inline
interpretation alongside each bare fact.
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
    mixture_en: list[str] = field(default_factory=list)
    mixture_ne: list[str] = field(default_factory=list)


# House themes — used to add "what it means" interpretation to each finding.
HOUSE_THEMES = {
    1:  ("self / body / vitality / overall direction",
         "आफू / शरीर / ओज / जीवनको दिशा"),
    2:  ("wealth / family / speech / food",
         "धन / परिवार / वाणी / खाना"),
    3:  ("courage / younger siblings / short trips / communication",
         "साहस / कान्छा भाइबहिनी / छोटो यात्रा / सञ्चार"),
    4:  ("home / mother / comfort / formal education / vehicles",
         "घर / आमा / सुख / औपचारिक शिक्षा / सवारी"),
    5:  ("intellect / children / creativity / romance / past-life merit",
         "बुद्धि / सन्तान / सिर्जना / प्रेम / पुण्य"),
    6:  ("daily work / service / illness / debts / enemies / obstacles",
         "दैनिक काम / सेवा / रोग / ऋण / शत्रु / बाधा"),
    7:  ("spouse / partnership / business / public dealings",
         "जीवनसाथी / साझेदारी / व्यापार / जनसम्बन्ध"),
    8:  ("hidden things / longevity / transformation / inheritance / research",
         "गुप्त / दीर्घायु / रूपान्तरण / उत्तराधिकार / अनुसन्धान"),
    9:  ("fortune / father / dharma / higher learning / long journeys",
         "भाग्य / बुबा / धर्म / उच्च शिक्षा / लामो यात्रा"),
    10: ("career / public role / status / reputation",
         "करियर / सार्वजनिक भूमिका / प्रतिष्ठा"),
    11: ("gains / friends / hopes / elder siblings / networks",
         "लाभ / मित्र / आशा / दाजुदिदी / सम्पर्क"),
    12: ("losses / expenses / foreign / sleep / liberation",
         "हानि / खर्च / विदेश / निद्रा / मोक्ष"),
}

# What each karaka represents in plain language.
KARAKA_ROLES = {
    "Sun":     ("vitality, authority, fatherly influence",
                "ओज, अधिकार, पिताको प्रभाव"),
    "Moon":    ("mind, emotions, motherly influence",
                "मन, भावना, आमाको प्रभाव"),
    "Mars":    ("courage, energy, blood and muscle",
                "साहस, ऊर्जा, रगत र मांसपेशी"),
    "Mercury": ("intellect, speech, communication",
                "बुद्धि, वाणी, सञ्चार"),
    "Jupiter": ("wisdom, prosperity, dharma, children",
                "ज्ञान, समृद्धि, धर्म, सन्तान"),
    "Venus":   ("love, beauty, harmony, partnership",
                "प्रेम, सौन्दर्य, सद्भाव, साझेदारी"),
    "Saturn":  ("discipline, longevity, slow-built results",
                "अनुशासन, दीर्घायु, ढिलो बनेको फल"),
    "Rahu":    ("ambition, foreign things, the unconventional",
                "महत्त्वाकाङ्क्षा, विदेशी कुरा, अपरम्परा"),
    "Ketu":    ("detachment, depth, spiritual insight",
                "वैराग्य, गहिराइ, आध्यात्मिक अन्तर्दृष्टि"),
}

PLANET_BEHAVIOR = {
    "Sun":     ("identity, authority, visibility", "पहिचान, अधिकार, देखिने भूमिका"),
    "Moon":    ("emotional rhythm, care, adaptation", "भावनात्मक लय, हेरचाह, अनुकूलन"),
    "Mars":    ("drive, conflict, decisive action", "जोश, संघर्ष, निर्णायक कर्म"),
    "Mercury": ("analysis, speech, trade, learning", "विश्लेषण, वाणी, व्यापार, सिकाइ"),
    "Jupiter": ("growth, ethics, protection, counsel", "विकास, नीति, संरक्षण, सल्लाह"),
    "Venus":   ("relationship, comfort, aesthetics", "सम्बन्ध, सुख, सौन्दर्य"),
    "Saturn":  ("delay, discipline, endurance", "ढिलाइ, अनुशासन, धैर्य"),
    "Rahu":    ("ambition, foreignness, disruption", "महत्त्वाकाङ्क्षा, विदेशीपन, असामान्यता"),
    "Ketu":    ("detachment, depth, inward focus", "वैराग्य, गहिराइ, भित्री ध्यान"),
}

HOUSE_GROUPS = {
    "kendra": ((1, 4, 7, 10), "kendra/angular house: visible, strong, practical", "केन्द्र भाव: देखिने, बलियो, व्यवहारिक"),
    "trikona": ((1, 5, 9), "trikona/trine: dharma, ease, talent", "त्रिकोण भाव: धर्म, सहजता, प्रतिभा"),
    "dusthana": ((6, 8, 12), "dusthana: pressure, repair, transformation", "दुस्थान: दबाब, सुधार, रूपान्तरण"),
    "upachaya": ((3, 6, 10, 11), "upachaya: improves through effort and age", "उपचय: प्रयास र उमेरसँग सुध्रिने"),
    "maraka": ((2, 7), "maraka/material house: attachment, value, pressure", "मारक/भौतिक भाव: लगाव, मूल्य, दबाब"),
}

# Dignity flavor — appended to a finding to flag how well the placement supports.
DIGNITY_FLAVOR = {
    "Exalted":     (" Strongly placed (exalted) — supports outcomes powerfully.",
                    " स्थिति बलियो (उच्च) — फल जोडदार।"),
    "Mooltrikona": (" Strongly placed (mooltrikona) — supports outcomes powerfully.",
                    " स्थिति बलियो (मूलत्रिकोण) — फल जोडदार।"),
    "Own":         (" Comfortably placed (own sign) — natural and supportive.",
                    " आफ्नै राशिमा — स्वाभाविक र सहयोगी।"),
    "Friend":      (" Friendly sign — moderately supportive.",
                    " मित्र-राशिमा — मध्यम सहयोगी।"),
    "Neutral":     ("", ""),
    "Enemy":       (" Enemy sign — under stress; results take more effort.",
                    " शत्रु-राशिमा — तनावमा; फलका लागि बढी मेहनत।"),
    "Debilitated": (" Weakly placed (debilitated) — results come slowly or need cancellation rules.",
                    " स्थिति कमजोर (नीच) — ढिलो फल वा नीचभङ्ग नियम आवश्यक।"),
}


def _house_of(rashi: int, lagna_rashi: int) -> int:
    return ((rashi - lagna_rashi) % 12) + 1


def _planets_in_house(positions: dict, lagna_rashi: int, house: int) -> list[str]:
    target_rashi = (lagna_rashi + house - 1) % 12
    return [name for name, p in positions.items() if p.rashi == target_rashi]


def _lord_of_house(lagna_rashi: int, house: int) -> str:
    rashi = (lagna_rashi + house - 1) % 12
    return RASHI_LORDS[rashi]


def _ord(n: int) -> str:
    s = str(n)
    if 11 <= n % 100 <= 13:
        return f"{n}th"
    return s + {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")


def _house_group_note(house: int) -> tuple[str, str]:
    notes_en = []
    notes_ne = []
    for houses, en, ne in HOUSE_GROUPS.values():
        if house in houses:
            notes_en.append(en)
            notes_ne.append(ne)
    return "; ".join(notes_en), "; ".join(notes_ne)


def _placement_pressure(planets: list[str]) -> tuple[str, str]:
    if not planets:
        return (
            "No planet occupies the house directly, so the house lord becomes the main judge.",
            "यो भावमा ग्रह प्रत्यक्ष बसेको छैन, त्यसैले भाव-स्वामी मुख्य निर्णायक हुन्छ।",
        )
    benefics = [p for p in planets if p in BENEFICS_NATURAL]
    malefics = [p for p in planets if p in MALEFICS_NATURAL]
    if benefics and malefics:
        return (
            "Benefic and malefic forces mix here: support exists, but results require discipline and timing.",
            "यहाँ शुभ र पाप दुवै शक्ति मिसिएका छन्: सहयोग छ, तर फलका लागि अनुशासन र समय चाहिन्छ।",
        )
    if benefics:
        return (
            "Mostly benefic influence: the house tends to produce smoother, more supportive results.",
            "मुख्यतः शुभ प्रभाव: यो भावले तुलनात्मक रूपमा सहज र सहयोगी फल दिन्छ।",
        )
    if malefics:
        return (
            "Mostly malefic influence: the house becomes active, demanding, and result-oriented after effort.",
            "मुख्यतः पाप प्रभाव: यो भाव सक्रिय, माग गर्ने, र प्रयासपछि फलदायी हुन्छ।",
        )
    return (
        "The planet mix is neutral or technical; judge dignity and lordship carefully.",
        "ग्रह-मिश्रण तटस्थ वा प्राविधिक छ; दशा र स्वामित्व ध्यानपूर्वक हेर्नुपर्छ।",
    )


def _build_mixture_findings(positions, lagna_rashi: int, trd: TopicReading) -> tuple[list[str], list[str]]:
    """Summarize how house contents, lords, and karakas combine for a topic."""
    en, ne = [], []
    for house in trd.houses:
        planets = _planets_in_house(positions, lagna_rashi, house)
        theme_en, theme_ne = HOUSE_THEMES[house]
        group_en, group_ne = _house_group_note(house)
        pressure_en, pressure_ne = _placement_pressure(planets)
        if planets:
            planet_mix_en = ", ".join(
                f"{p} ({PLANET_BEHAVIOR.get(p, KARAKA_ROLES.get(p, (p, p)))[0]})"
                for p in planets
            )
            planet_mix_ne = ", ".join(
                f"{p} ({PLANET_BEHAVIOR.get(p, KARAKA_ROLES.get(p, (p, p)))[1]})"
                for p in planets
            )
            en.append(
                f"<b>House {house}</b> carries {planet_mix_en}. This directly colors "
                f"<i>{theme_en}</i>. {pressure_en} <span class='small'>{group_en}</span>"
            )
            ne.append(
                f"<b>भाव {house}</b> मा {planet_mix_ne} छ। यसले <i>{theme_ne}</i>लाई "
                f"सीधै रङ्गाउँछ। {pressure_ne} <span class='small'>{group_ne}</span>"
            )
        else:
            en.append(
                f"<b>House {house}</b> is empty; read its lord and aspects for prediction. "
                f"It still represents <i>{theme_en}</i>. <span class='small'>{group_en}</span>"
            )
            ne.append(
                f"<b>भाव {house}</b> खाली छ; भविष्यवाणीका लागि यसको स्वामी र दृष्टि हेर्नुपर्छ। "
                f"यसले अझै <i>{theme_ne}</i> जनाउँछ। <span class='small'>{group_ne}</span>"
            )

        lord = _lord_of_house(lagna_rashi, house)
        if lord in positions:
            lord_house = _house_of(positions[lord].rashi, lagna_rashi)
            lord_theme_en, lord_theme_ne = HOUSE_THEMES[lord_house]
            dignity = dignity_of(lord, positions[lord].longitude)
            flavor_en, flavor_ne = DIGNITY_FLAVOR.get(dignity, ("", ""))
            en.append(
                f"<b>{_ord(house)} lord {lord}</b> sits in house {lord_house}; "
                f"therefore <i>{theme_en}</i> is delivered through <i>{lord_theme_en}</i>.{flavor_en}"
            )
            ne.append(
                f"<b>भाव {house} को स्वामी {lord}</b> भाव {lord_house} मा छ; "
                f"त्यसैले <i>{theme_ne}</i>का फल <i>{lord_theme_ne}</i>मार्फत आउँछन्।{flavor_ne}"
            )

    karaka_bits_en = []
    karaka_bits_ne = []
    for planet in trd.karakas:
        if planet not in positions:
            continue
        house = _house_of(positions[planet].rashi, lagna_rashi)
        theme_en, theme_ne = HOUSE_THEMES[house]
        role_en, role_ne = KARAKA_ROLES.get(planet, (planet, planet))
        karaka_bits_en.append(f"{planet} ({role_en}) in house {house} links the topic to {theme_en}")
        karaka_bits_ne.append(f"{planet} ({role_ne}) भाव {house} मा भएर विषयलाई {theme_ne}सँग जोड्छ")
    if karaka_bits_en:
        en.append("<b>Karaka blend:</b> " + "; ".join(karaka_bits_en) + ".")
        ne.append("<b>कारक मिश्रण:</b> " + "; ".join(karaka_bits_ne) + "।")

    return en, ne


def _describe_lord(positions, lagna_rashi: int, lord: str, lord_of: int) -> tuple[str, str]:
    """Fact + inline interpretation: lord-of-house X is in house Y."""
    if lord not in positions:
        return "", ""
    p = positions[lord]
    house = _house_of(p.rashi, lagna_rashi)
    dign = dignity_of(lord, p.longitude)
    src_en, src_ne = HOUSE_THEMES[lord_of]
    dst_en, dst_ne = HOUSE_THEMES[house]
    flavor_en, flavor_ne = DIGNITY_FLAVOR.get(dign, ("", ""))

    en = (f"<b>Lord of the {_ord(lord_of)} ({lord}) is in house {house}</b> "
          f"({dign}) — matters of <i>{src_en}</i> express through "
          f"<i>{dst_en}</i>.{flavor_en}")
    ne = (f"<b>{lord_of} औं भावको स्वामी ({lord}) भाव {house} मा</b> "
          f"({dign}) — <i>{src_ne}</i>का कुरा <i>{dst_ne}</i>मार्फत "
          f"प्रकट हुन्छन्।{flavor_ne}")
    return en, ne


def _karaka_status(positions, lagna_rashi: int, planet: str) -> tuple[str, str]:
    """Fact + inline interpretation: this karaka sits in house X."""
    if planet not in positions:
        return "", ""
    p = positions[planet]
    house = _house_of(p.rashi, lagna_rashi)
    dign = dignity_of(planet, p.longitude)
    role_en, role_ne = KARAKA_ROLES.get(planet, (planet, planet))
    dst_en, dst_ne = HOUSE_THEMES[house]
    flavor_en, flavor_ne = DIGNITY_FLAVOR.get(dign, ("", ""))

    en = (f"<b>{planet} (significator of {role_en}) sits in house {house}</b> "
          f"({dign}) — focuses {planet}'s energy on <i>{dst_en}</i>.{flavor_en}")
    ne = (f"<b>{planet} ({role_ne}को कारक) भाव {house} मा</b> "
          f"({dign}) — {planet}को ऊर्जा <i>{dst_ne}</i>मा "
          f"केन्द्रित।{flavor_ne}")
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
    """Fact + inline interpretation: which planets sit in this house."""
    planets = _planets_in_house(positions, lagna_rashi, house)
    if not planets:
        return
    dst_en, dst_ne = HOUSE_THEMES[house]
    # Briefly note what each planet brings to the house
    bits_en = []
    bits_ne = []
    for p in planets:
        role_en, role_ne = KARAKA_ROLES.get(p, (p, p))
        bits_en.append(f"{p} ({role_en})")
        bits_ne.append(f"{p} ({role_ne})")
    findings_en.append(
        f"<b>House {house} contains:</b> {', '.join(bits_en)} — "
        f"these forces directly shape <i>{dst_en}</i>."
    )
    findings_ne.append(
        f"<b>भाव {house} मा:</b> {', '.join(bits_ne)} — "
        f"यिनै शक्तिहरूले <i>{dst_ne}</i>लाई सीधै आकार दिन्छन्।"
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
        "education", "Education", "शिक्षा", "ED",
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
        "health", "Health", "स्वास्थ्य", "HE",
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
        "career", "Career & Employment", "करियर र रोजगार", "CR",
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
        "wealth", "Wealth & Finance", "धन र वित्त", "FI",
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
        "marriage", "Marriage & Partnership", "विवाह र साझेदारी", "MR",
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
        "family", "Family & Children", "परिवार र सन्तान", "FA",
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
        "travel", "Travel & Foreign", "यात्रा र विदेश", "TR",
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
        "spirituality", "Spirituality & Dharma", "अध्यात्म र धर्म", "SP",
        [5, 8, 9, 12], ["Jupiter", "Ketu", "Saturn"],
        fe, fn, summary_en, summary_ne,
    )


def analyze_all(positions, lagna_rashi: int) -> list[TopicReading]:
    """Run every topic analyzer in display order."""
    readings = [
        analyze_education(positions, lagna_rashi),
        analyze_health(positions, lagna_rashi),
        analyze_career(positions, lagna_rashi),
        analyze_wealth(positions, lagna_rashi),
        analyze_marriage(positions, lagna_rashi),
        analyze_family(positions, lagna_rashi),
        analyze_travel(positions, lagna_rashi),
        analyze_spirituality(positions, lagna_rashi),
    ]
    for reading in readings:
        reading.mixture_en, reading.mixture_ne = _build_mixture_findings(
            positions, lagna_rashi, reading,
        )
    return readings
