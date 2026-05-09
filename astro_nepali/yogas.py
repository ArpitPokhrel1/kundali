"""Yoga detection — classical combinations from the natal chart.

Each yoga is detected if its rule fires. We return a list of `Yoga`
findings; the renderer turns these into a Yogas tab.

Implemented:
  - Gajakesari Yoga                      (Moon ↔ Jupiter mutual kendras)
  - Buddha-Aditya Yoga                   (Sun + Mercury same rashi)
  - Chandra-Mangala Yoga                 (Moon + Mars same rashi)
  - Pancha Mahapurusha Yogas (5)         (Mars/Mer/Jup/Ven/Sat — own/exalted in kendra)
  - Raja Yoga                            (Kendra-lord + Trikona-lord conjunction)
  - Dhana Yoga                           (2nd-lord + 11th-lord conjunction)
  - Viparita Raja Yoga                   (any two of 6/8/12 lords conjunct)
  - Kemadruma Yoga (cautionary)          (Moon isolated in 2nd & 12th)
  - Adhi Yoga                            (benefic in 6/7/8 from Moon)
  - Neechabhanga Raja Yoga (specific)    (debilitation cancellation)
"""
from __future__ import annotations
from dataclasses import dataclass

from .dignities import (
    EXALTATION, OWN, RASHI_LORDS, BENEFICS_NATURAL,
)


@dataclass
class Yoga:
    name_en: str
    name_ne: str
    quality: str         # 'positive', 'cautionary', or 'mixed'
    explanation_en: str
    explanation_ne: str


KENDRAS = {1, 4, 7, 10}
TRIKONAS = {1, 5, 9}
DUSTHANAS = {6, 8, 12}


def _house_of(planet_rashi: int, lagna_rashi: int) -> int:
    return ((planet_rashi - lagna_rashi) % 12) + 1


def _planet_house(positions: dict, name: str, lagna_rashi: int) -> int:
    return _house_of(positions[name].rashi, lagna_rashi)


def detect(positions: dict, lagna_rashi: int) -> list[Yoga]:
    """Run every detection rule and return the firing yogas."""
    found: list[Yoga] = []
    P = positions

    # ---- 1. Gajakesari ----
    moon_r = P["Moon"].rashi
    jup_r = P["Jupiter"].rashi
    sep = (jup_r - moon_r) % 12
    if sep in (0, 3, 6, 9):
        found.append(Yoga(
            "Gajakesari Yoga",
            "गजकेसरी योग",
            "positive",
            "Moon and Jupiter are in mutual kendras (1st/4th/7th/10th from each "
            "other). Classical: gives wisdom, social respect, eloquent speech, "
            "and a benevolent disposition. Strongest when both are in their "
            "own / exalted signs.",
            "चन्द्र र बृहस्पति एक–अर्काबाट केन्द्र (१/४/७/१०) मा छन्। "
            "शास्त्र: ज्ञान, समाजमा प्रतिष्ठा, राम्रो वाणी, र उदार स्वभाव दिन्छ। "
            "दुवै ग्रह आफ्नै/उच्च राशिमा छन् भने सबभन्दा बलियो हुन्छ।",
        ))

    # ---- 2. Buddha-Aditya ----
    if P["Sun"].rashi == P["Mercury"].rashi:
        # Combust caveat: Mercury within 14° of Sun is technically combust
        sep_deg = abs((P["Sun"].longitude - P["Mercury"].longitude + 180) % 360 - 180)
        combust_note = (
            " Note: Mercury is also combust (within 14° of Sun) — pure-form "
            "yoga effect is weakened; Mercury's qualities act through Sun's "
            "ego/identity instead."
            if sep_deg < 14 else ""
        )
        combust_note_ne = (
            " नोट: बुध सूर्यबाट १४° भित्र छ — अस्त (combust)। शुद्ध फल कमजोर; "
            "बुधको गुण सूर्यको अहम्/पहिचानमार्फत प्रकट हुन्छ।"
            if sep_deg < 14 else ""
        )
        found.append(Yoga(
            "Buddha-Aditya Yoga",
            "बुधादित्य योग",
            "positive",
            "Sun and Mercury share a rashi. Sharp intellect, eloquence, "
            "scholarship, and recognized intelligence." + combust_note,
            "सूर्य र बुध एउटै राशिमा छन्। तीव्र बुद्धि, राम्रो वाणी, "
            "विद्वत्ता, र मान्यता प्राप्त बुद्धिमत्ता।" + combust_note_ne,
        ))

    # ---- 3. Chandra-Mangala ----
    if P["Moon"].rashi == P["Mars"].rashi:
        found.append(Yoga(
            "Chandra-Mangala Yoga",
            "चन्द्र-मङ्गल योग",
            "mixed",
            "Moon and Mars share a rashi. Strong business sense, decisive "
            "action, ability to earn through enterprise. Can also bring "
            "emotional intensity and short temper.",
            "चन्द्र र मङ्गल एउटै राशिमा छन्। व्यापारिक बुद्धि, निर्णायक "
            "कर्म, उद्यमबाट कमाउने सामर्थ्य। साथै, भावनात्मक तीव्रता र "
            "छोटो रिस आउन सक्छ।",
        ))

    # ---- 4. Pancha Mahapurusha (5 yogas) ----
    MAHAPURUSHA = [
        ("Mars",    "Ruchaka",  "रुचक",   "courageous, powerful, leader-like",
                    "साहसी, बलवान्, नेतृत्वमुखी"),
        ("Mercury", "Bhadra",   "भद्र",   "intelligent, wealthy, persuasive",
                    "बुद्धिमान्, धनी, प्रभावी वक्ता"),
        ("Jupiter", "Hamsa",    "हंस",    "learned, righteous, respected",
                    "विद्वान्, धार्मिक, सम्मानित"),
        ("Venus",   "Malavya",  "मालव्य", "beautiful, artistic, prosperous",
                    "सुन्दर, कलाप्रेमी, समृद्ध"),
        ("Saturn",  "Shasha",   "शश",     "authoritative, hard-working, long-lived",
                    "अधिकारी, श्रमी, दीर्घजीवी"),
    ]
    for planet, name_en, name_ne, traits_en, traits_ne in MAHAPURUSHA:
        ex_rashi = EXALTATION[planet][0]
        own_rashis = OWN[planet]
        p_rashi = P[planet].rashi
        if p_rashi == ex_rashi or p_rashi in own_rashis:
            house = _house_of(p_rashi, lagna_rashi)
            if house in KENDRAS:
                kind = "exalted" if p_rashi == ex_rashi else "in own sign"
                kind_ne = "उच्च" if p_rashi == ex_rashi else "स्व-राशिमा"
                found.append(Yoga(
                    f"{name_en} Yoga (Pancha Mahapurusha)",
                    f"{name_ne} योग (पञ्च-महापुरुष)",
                    "positive",
                    f"{planet} is {kind} and in kendra (house {house}). "
                    f"This is one of the five Mahapurusha (great-soul) yogas — "
                    f"the native tends to be {traits_en}.",
                    f"{planet} {kind_ne} छ र केन्द्र (भाव {house}) मा छ। "
                    f"पाँच महापुरुष योग मध्ये एक — व्यक्ति प्रायः {traits_ne} हुन्छ।",
                ))

    # ---- 5. Raja Yoga (kendra lord + trikona lord conjunct) ----
    kendra_lords = {RASHI_LORDS[(lagna_rashi + h - 1) % 12] for h in KENDRAS}
    trikona_lords = {RASHI_LORDS[(lagna_rashi + h - 1) % 12] for h in TRIKONAS}
    raja_pairs = set()
    for kl in kendra_lords:
        for tl in trikona_lords:
            if kl != tl and kl in P and tl in P:
                if P[kl].rashi == P[tl].rashi:
                    raja_pairs.add(tuple(sorted([kl, tl])))
    for kl, tl in raja_pairs:
        found.append(Yoga(
            f"Raja Yoga ({kl} + {tl})",
            f"राज योग ({kl} + {tl})",
            "positive",
            f"A kendra-lord ({kl}) and a trikona-lord ({tl}) sit in the same "
            f"rashi. Classical: rise in life, authority, recognition. "
            f"The strength depends on the dignity of both lords.",
            f"केन्द्र-स्वामी ({kl}) र त्रिकोण-स्वामी ({tl}) एउटै राशिमा। "
            f"शास्त्र: जीवनमा उन्नति, अधिकार, र मान्यता। दुवै ग्रहको बलले "
            f"फल निर्धारण गर्छ।",
        ))

    # ---- 6. Dhana Yoga (2nd lord + 11th lord conjunct) ----
    rashi_2 = (lagna_rashi + 1) % 12
    rashi_11 = (lagna_rashi + 10) % 12
    lord_2 = RASHI_LORDS[rashi_2]
    lord_11 = RASHI_LORDS[rashi_11]
    if lord_2 != lord_11 and P[lord_2].rashi == P[lord_11].rashi:
        found.append(Yoga(
            f"Dhana Yoga ({lord_2} + {lord_11})",
            f"धन योग ({lord_2} + {lord_11})",
            "positive",
            f"Lord of 2nd ({lord_2}) and lord of 11th ({lord_11}) join — "
            f"a classical wealth combination. Suggests money-flow through "
            f"both savings and active gains.",
            f"दोस्रो भावको स्वामी ({lord_2}) र एघारौँको स्वामी ({lord_11}) "
            f"मिलेको — शास्त्रीय धन-योग। बचत र आय दुवैबाट सम्पत्ति।",
        ))

    # ---- 7. Viparita Raja Yoga (any two dusthana lords conjunct) ----
    dusthana_lords_map = {
        h: RASHI_LORDS[(lagna_rashi + h - 1) % 12] for h in DUSTHANAS
    }
    seen = set()
    for h1 in DUSTHANAS:
        for h2 in DUSTHANAS:
            if h1 >= h2:
                continue
            l1, l2 = dusthana_lords_map[h1], dusthana_lords_map[h2]
            if l1 == l2 or l1 not in P or l2 not in P:
                continue
            if P[l1].rashi == P[l2].rashi:
                key = tuple(sorted([l1, l2]))
                if key in seen:
                    continue
                seen.add(key)
                found.append(Yoga(
                    f"Viparita Raja Yoga ({l1} + {l2})",
                    f"विपरीत राज योग ({l1} + {l2})",
                    "mixed",
                    f"Two dusthana lords ({l1} from {h1}, {l2} from {h2}) "
                    f"join. Classical: the difficult houses cancel each "
                    f"other's negativity, giving rise from adversity.",
                    f"दुस्थान भावका दुई स्वामी ({l1}–भाव {h1}, {l2}–भाव {h2}) "
                    f"मिलेका। दुस्थानहरूले एक-अर्काको नकारात्मकता रद्द गर्छन् — "
                    f"कठिनाइबाट उठ्ने अनपेक्षित सफलता।",
                ))

    # ---- 8. Kemadruma (Moon isolated) ----
    moon_house = _house_of(moon_r, lagna_rashi)
    second_from_moon = (moon_r + 1) % 12
    twelfth_from_moon = (moon_r - 1) % 12
    others = [name for name in P
              if name not in ("Moon", "Sun", "Rahu", "Ketu")]
    has_neighbor = any(P[n].rashi in (second_from_moon, twelfth_from_moon)
                       for n in others)
    moon_with_other = any(P[n].rashi == moon_r for n in others)
    # Classical Kemadruma: no planet (other than luminaries/nodes) in the 2nd
    # AND 12th from Moon AND no planet conjunct Moon.
    if not has_neighbor and not moon_with_other:
        found.append(Yoga(
            "Kemadruma Yoga (cautionary)",
            "केमद्रुम योग (सावधान)",
            "cautionary",
            "Moon stands alone — no planet in the 2nd or 12th from Moon, and "
            "no planet conjunct Moon (excluding luminaries/nodes). Classical: "
            "challenges to mental peace and material flow. Often cancelled by "
            "Adhi yoga, strong Moon, or planets in kendras from Moon.",
            "चन्द्र एक्लो छ — चन्द्रबाट २ र १२ भावमा कुनै ग्रह छैन; चन्द्रसँग "
            "पनि कोही छैन। शास्त्र: मानसिक शान्ति र भौतिक फलमा बाधा। "
            "अधि योग, बलियो चन्द्र, वा चन्द्रबाट केन्द्रमा रहेका ग्रहले "
            "रद्द गर्न सक्छन्।",
        ))

    # ---- 9. Adhi Yoga (benefics in 6/7/8 from Moon) ----
    benefic_houses_from_moon = []
    for benefic in ("Mercury", "Jupiter", "Venus"):
        b_rashi = P[benefic].rashi
        h_from_moon = ((b_rashi - moon_r) % 12) + 1
        if h_from_moon in (6, 7, 8):
            benefic_houses_from_moon.append((benefic, h_from_moon))
    if len(benefic_houses_from_moon) >= 2:
        names = ", ".join(b for b, _ in benefic_houses_from_moon)
        found.append(Yoga(
            "Adhi Yoga",
            "अधि योग",
            "positive",
            f"Two or more benefics ({names}) sit in the 6th/7th/8th from "
            f"Moon. Classical: leadership, dignity, success through helpers. "
            f"Cancels Kemadruma if both are present.",
            f"दुई वा बढी शुभ ग्रह ({names}) चन्द्रबाट ६/७/८ भावमा छन्। "
            f"शास्त्र: नेतृत्व, मर्यादा, सहयोगीहरूबाट सफलता। केमद्रुम योग "
            f"रद्द गर्न सक्छ।",
        ))

    # ---- 10. Neechabhanga Raja Yoga (debilitation cancellation, simplified) ----
    DEBILITATION = {p: ((r + 6) % 12, d) for p, (r, d) in EXALTATION.items()}
    for planet in ("Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn"):
        if planet not in P:
            continue
        debil_rashi, _ = DEBILITATION[planet]
        if P[planet].rashi != debil_rashi:
            continue
        # Cancellation (one common rule): the lord of the debilitation sign,
        # OR the planet that would be EXALTED in this sign, sits in a kendra
        # from Lagna or Moon.
        debil_sign_lord = RASHI_LORDS[debil_rashi]
        # Find planet exalted in this sign
        exalted_here = None
        for p2, (rashi2, _) in EXALTATION.items():
            if rashi2 == debil_rashi:
                exalted_here = p2
                break
        cancellers = []
        for cand in (debil_sign_lord, exalted_here):
            if cand and cand in P:
                h_lagna = _house_of(P[cand].rashi, lagna_rashi)
                h_moon = ((P[cand].rashi - moon_r) % 12) + 1
                if h_lagna in KENDRAS or h_moon in KENDRAS:
                    cancellers.append(cand)
        if cancellers:
            found.append(Yoga(
                f"Neechabhanga Raja Yoga ({planet})",
                f"नीचभङ्ग राज योग ({planet})",
                "positive",
                f"{planet} is debilitated, BUT the cancellation rule fires — "
                f"{', '.join(cancellers)} sits in a kendra from Lagna or Moon. "
                f"Classical: the apparent weakness of {planet} converts into "
                f"unexpected rise.",
                f"{planet} नीच छ, तर नीचभङ्ग नियम सक्रिय छ — {', '.join(cancellers)} "
                f"लग्न वा चन्द्रबाट केन्द्रमा बसेको छ। शास्त्र: {planet} को "
                f"देखिने कमजोरी अप्रत्याशित उन्नतिमा बदलिन्छ।",
            ))

    return found
