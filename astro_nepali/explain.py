"""Plain-language explanation of the Kundali for a non-astrologer reader.

Style: friendly, descriptive, avoids fortune-telling claims. Explains what each
piece of the chart MEANS in classical Vedic terms — not what will happen.
"""
from __future__ import annotations

from .labels import RASHIS, NAKSHATRAS, PLANETS, PLANET_BY_ENGLISH


# Concise traits associated with each rashi (sign).
RASHI_TRAITS = {
    "Aries":       "energetic, pioneering, direct — ruled by Mars",
    "Taurus":      "steady, sensual, patient — ruled by Venus",
    "Gemini":      "curious, communicative, quick-thinking — ruled by Mercury",
    "Cancer":      "emotional, nurturing, home-loving — ruled by the Moon",
    "Leo":         "confident, generous, leader-like — ruled by the Sun",
    "Virgo":       "analytical, careful, service-oriented — ruled by Mercury",
    "Libra":       "diplomatic, fair-minded, social — ruled by Venus",
    "Scorpio":     "intense, deep, transformative — ruled by Mars",
    "Sagittarius": "philosophical, optimistic, freedom-loving — ruled by Jupiter",
    "Capricorn":   "disciplined, ambitious, practical — ruled by Saturn",
    "Aquarius":    "innovative, humanitarian, independent — ruled by Saturn",
    "Pisces":      "imaginative, compassionate, dreamy — ruled by Jupiter",
}

# What the 12 houses (bhavas) classically signify.
HOUSE_MEANINGS = {
    1:  ("Tanu / तनु",      "self, body, personality, overall vitality"),
    2:  ("Dhana / धन",      "wealth, family, speech, food"),
    3:  ("Sahaja / सहज",    "siblings, courage, short journeys, communication"),
    4:  ("Sukha / सुख",     "mother, home, comfort, education, vehicles"),
    5:  ("Putra / पुत्र",    "children, intellect, creativity, past-life merit"),
    6:  ("Ari / अरि",       "enemies, illness, debts, daily work, obstacles"),
    7:  ("Yuvati / युवती",  "spouse, partnerships, business, public dealings"),
    8:  ("Ayu / आयु",       "longevity, hidden things, transformation, inheritance"),
    9:  ("Dharma / धर्म",   "father, fortune, higher learning, religion, long journeys"),
    10: ("Karma / कर्म",    "career, status, public reputation, action in the world"),
    11: ("Labha / लाभ",     "gains, friendships, hopes, elder siblings"),
    12: ("Vyaya / व्यय",    "losses, expenses, foreign lands, liberation, sleep"),
}

PLANET_MEANINGS = {
    "Sun":     "soul, ego, father, authority, vitality",
    "Moon":    "mind, emotions, mother, comfort, public",
    "Mars":    "energy, courage, brothers, action, conflict",
    "Mercury": "intellect, speech, learning, business, wit",
    "Jupiter": "wisdom, teachers, dharma, prosperity, expansion",
    "Venus":   "love, beauty, partners, art, comfort",
    "Saturn":  "discipline, work, longevity, restriction, perseverance",
    "Rahu":    "ambition, foreign things, obsession, sudden gains",
    "Ketu":    "spirituality, detachment, past lives, intuition, loss",
}

# Generic nakshatra theme — kept brief and non-deterministic.
NAKSHATRA_THEMES = {
    "Ashwini":          "swift, healing, fresh starts",
    "Bharani":          "transformation, intensity, creative power",
    "Krittika":         "sharpness, leadership, cutting through illusion",
    "Rohini":           "beauty, fertility, sensual abundance",
    "Mrigashira":       "searching, curiosity, gentle pursuit",
    "Ardra":            "storms and renewal — strong emotions, breakthroughs",
    "Punarvasu":        "return to home, wholesome generosity",
    "Pushya":           "nourishment, care, the most auspicious nakshatra",
    "Ashlesha":         "depth, mystery, serpentine wisdom",
    "Magha":            "ancestral pride, royal legacy",
    "Purva Phalguni":   "joy, romance, creative play",
    "Uttara Phalguni":  "kindness, partnership, organized service",
    "Hasta":            "skill of the hands, craft, cleverness",
    "Chitra":           "design, glamour, brilliant artistry",
    "Swati":            "independence, balance, learning to bend without breaking",
    "Vishakha":         "focused goals, two-pointed determination",
    "Anuradha":         "loyal friendship, devotion, success through community",
    "Jyeshtha":         "elder authority, courage in adversity",
    "Mula":             "deep roots, getting to the bottom of things",
    "Purva Ashadha":    "invincibility, pride in conviction",
    "Uttara Ashadha":   "lasting victory, righteous achievement",
    "Shravana":         "deep listening, learning, connection across distances",
    "Dhanishtha":       "rhythm, music, prosperity through skill",
    "Shatabhisha":      "healing, mystery, the lone researcher",
    "Purva Bhadrapada": "intensity, transformation through fire",
    "Uttara Bhadrapada":"wisdom of the depths, calm under pressure",
    "Revati":           "completion, gentle protection, safe journeys",
}


def _planet_in_house_line(planet: str, house: int, rashi_idx: int) -> str:
    rashi_en = RASHIS[rashi_idx][2]
    house_label, house_meaning = HOUSE_MEANINGS[house]
    pm = PLANET_MEANINGS[planet]
    return (
        f"  • [bold]{planet}[/] in House {house} ({house_label}) — sign {rashi_en}.\n"
        f"      → {planet} ({pm}) shapes themes of {house_meaning}."
    )


def explain_kundali(
    *,
    name: str,
    lagna_rashi: int,
    moon_rashi: int,
    sun_rashi: int,
    moon_nakshatra: int,
    chart: dict,        # planet name -> HousePlacement
    current_dasha,      # DashaPeriod
) -> str:
    """Build a multi-paragraph plain-language explanation of the kundali."""

    lagna_name = RASHIS[lagna_rashi][2]
    moon_name = RASHIS[moon_rashi][2]
    sun_name = RASHIS[sun_rashi][2]
    nak_dev, nak_en = NAKSHATRAS[moon_nakshatra]

    parts: list[str] = []

    parts.append(
        f"[bold underline]Kundali in Plain Language — for {name or 'this person'}[/]\n"
    )

    parts.append(
        "[bold]What is a Kundali?[/]\n"
        "A Kundali (कुण्डली) is a snapshot of the sky at the moment you were born.\n"
        "Vedic astrology divides the sky into 12 [italic]rashis[/] (zodiac signs) and 27\n"
        "[italic]nakshatras[/] (lunar mansions). It also tracks the position of the Sun, Moon,\n"
        "the five visible planets (Mars, Mercury, Jupiter, Venus, Saturn), and the\n"
        "two lunar nodes called Rahu and Ketu. From your birth date, time, and place,\n"
        "we calculate where each of those was in the sky and place them into 12 [italic]bhavas[/]\n"
        "(houses) — each house representing a different area of life.\n"
    )

    # Lagna paragraph
    parts.append(
        f"[bold]Your Lagna (Ascendant) — {lagna_name}[/]\n"
        f"The Lagna is the sign that was rising on the eastern horizon when you were born.\n"
        f"It's often called the 'mask you wear' — how you appear to the world and how you\n"
        f"meet new situations. Yours is [bold]{lagna_name}[/]: {RASHI_TRAITS[lagna_name]}.\n"
        f"This sign and its lord become the anchor of the whole chart — every other house\n"
        f"is counted starting from this point.\n"
    )

    # Moon sign paragraph (Rashi)
    parts.append(
        f"[bold]Your Moon Sign / Janma Rashi — {moon_name}[/]\n"
        f"In Vedic tradition the Moon is more important than the Sun for personality and\n"
        f"emotional life. Your 'Rashi' usually refers to where the Moon was: [bold]{moon_name}[/].\n"
        f"This colors your inner world: {RASHI_TRAITS[moon_name]}.\n"
    )

    # Nakshatra
    theme = NAKSHATRA_THEMES.get(nak_en, "")
    parts.append(
        f"[bold]Your Janma Nakshatra (Birth Star) — {nak_dev} / {nak_en}[/]\n"
        f"The nakshatra is a finer division of the sky than the rashi — there are 27 of them.\n"
        f"Yours is [bold]{nak_en}[/]: {theme}.\n"
        f"The nakshatra is also the starting point for your Vimshottari Dasha\n"
        f"(your life's planetary timeline).\n"
    )

    # Sun sign paragraph
    parts.append(
        f"[bold]Your Sun Sign / Surya Rashi — {sun_name}[/]\n"
        f"The Sun represents your core identity, your father, and your sense of authority.\n"
        f"Yours is [bold]{sun_name}[/]: {RASHI_TRAITS[sun_name]}.\n"
        f"(Note: this is the sidereal Sun sign, which usually differs by ~one sign from\n"
        f"the tropical Sun sign you may have seen in Western horoscopes.)\n"
    )

    # Planet placements
    parts.append("[bold]Where Each Planet Sits — and What It Touches[/]")
    for planet in ("Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"):
        if planet in chart:
            hp = chart[planet]
            parts.append(_planet_in_house_line(planet, hp.house, hp.rashi))
    parts.append("")

    # Dasha
    if current_dasha is not None:
        end_str = current_dasha.end.strftime("%Y-%m-%d")
        years_left = (current_dasha.end - current_dasha.start).days / 365.25
        parts.append(
            f"[bold]Current Dasha (Life Period) — {current_dasha.lord}[/]\n"
            f"Vedic astrology divides life into long planetary periods called Mahadashas.\n"
            f"You are currently in the [bold]{current_dasha.lord} Mahadasha[/], "
            f"running until [bold]{end_str}[/].\n"
            f"Themes during this {years_left:.1f}-year period are colored by\n"
            f"{current_dasha.lord} — {PLANET_MEANINGS[current_dasha.lord]}.\n"
        )

    # Closing
    parts.append(
        "[italic dim]A Kundali is a map, not a verdict. Classical texts treat it as a guide\n"
        "to tendencies and timings — the choices you make within those tendencies are\n"
        "still yours.[/]"
    )

    return "\n".join(parts)
