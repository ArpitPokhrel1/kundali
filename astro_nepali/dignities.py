"""Planetary dignity — exalted, debilitated, own sign, mooltrikona, friend/enemy.

Standard classical (Parashara) tables.
"""
from __future__ import annotations

# Rashi indices: 0=Aries, 1=Taurus, ... 11=Pisces

# Exaltation: (rashi, exact-degree)
EXALTATION = {
    "Sun":     (0, 10),    # Aries 10°
    "Moon":    (1, 3),     # Taurus 3°
    "Mars":    (9, 28),    # Capricorn 28°
    "Mercury": (5, 15),    # Virgo 15°
    "Jupiter": (3, 5),     # Cancer 5°
    "Venus":   (11, 27),   # Pisces 27°
    "Saturn":  (6, 20),    # Libra 20°
    "Rahu":    (1, 0),     # Taurus (some say Gemini)
    "Ketu":    (7, 0),     # Scorpio
}

# Debilitation = 180° from exaltation
DEBILITATION = {p: ((r + 6) % 12, d) for p, (r, d) in EXALTATION.items()}

# Own (Sva-rashi)
OWN = {
    "Sun":     {4},          # Leo
    "Moon":    {3},          # Cancer
    "Mars":    {0, 7},       # Aries, Scorpio
    "Mercury": {2, 5},       # Gemini, Virgo
    "Jupiter": {8, 11},      # Sagittarius, Pisces
    "Venus":   {1, 6},       # Taurus, Libra
    "Saturn":  {9, 10},      # Capricorn, Aquarius
}

# Mooltrikona: (rashi, start_deg, end_deg)
MOOLATRIKONA = {
    "Sun":     (4, 0, 20),   # Leo 0–20°
    "Moon":    (1, 4, 20),   # Taurus 4–20°
    "Mars":    (0, 0, 12),   # Aries 0–12°
    "Mercury": (5, 16, 20),  # Virgo 16–20°
    "Jupiter": (8, 0, 10),   # Sagittarius 0–10°
    "Venus":   (6, 0, 15),   # Libra 0–15°
    "Saturn":  (10, 0, 20),  # Aquarius 0–20°
}

# Rashi lords (traditional)
RASHI_LORDS = {
    0: "Mars",     1: "Venus",   2: "Mercury", 3: "Moon",
    4: "Sun",      5: "Mercury", 6: "Venus",   7: "Mars",
    8: "Jupiter",  9: "Saturn", 10: "Saturn", 11: "Jupiter",
}

# Friendship table (Parashara permanent friendships)
FRIENDS = {
    "Sun":     {"Moon", "Mars", "Jupiter"},
    "Moon":    {"Sun", "Mercury"},
    "Mars":    {"Sun", "Moon", "Jupiter"},
    "Mercury": {"Sun", "Venus"},
    "Jupiter": {"Sun", "Moon", "Mars"},
    "Venus":   {"Mercury", "Saturn"},
    "Saturn":  {"Mercury", "Venus"},
}
ENEMIES = {
    "Sun":     {"Venus", "Saturn"},
    "Moon":    set(),  # Moon has no enemies in Parashara's table
    "Mars":    {"Mercury"},
    "Mercury": {"Moon"},
    "Jupiter": {"Mercury", "Venus"},
    "Venus":   {"Sun", "Moon"},
    "Saturn":  {"Sun", "Moon", "Mars"},
}
# Anyone not friend or enemy is neutral. Rahu/Ketu use various conventions; we
# treat them as neutral for dignity-by-friendship.

BENEFICS_NATURAL = {"Jupiter", "Venus", "Moon", "Mercury"}  # Mercury contextual
MALEFICS_NATURAL = {"Sun", "Mars", "Saturn", "Rahu", "Ketu"}


def dignity_of(planet: str, longitude: float) -> str:
    """Return one of: 'Exalted', 'Debilitated', 'Mooltrikona',
    'Own', 'Friend', 'Enemy', 'Neutral'."""
    rashi = int(longitude // 30)
    deg = longitude - rashi * 30

    if planet in EXALTATION:
        ex_rashi, _ = EXALTATION[planet]
        if rashi == ex_rashi:
            return "Exalted"
    if planet in DEBILITATION:
        de_rashi, _ = DEBILITATION[planet]
        if rashi == de_rashi:
            return "Debilitated"
    if planet in MOOLATRIKONA:
        m_rashi, m_start, m_end = MOOLATRIKONA[planet]
        if rashi == m_rashi and m_start <= deg < m_end:
            return "Mooltrikona"
    if planet in OWN and rashi in OWN[planet]:
        return "Own"
    if planet in RASHI_LORDS.values() or planet in FRIENDS:
        sign_lord = RASHI_LORDS.get(rashi)
        if sign_lord:
            if sign_lord == planet:
                return "Own"
            if sign_lord in FRIENDS.get(planet, set()):
                return "Friend"
            if sign_lord in ENEMIES.get(planet, set()):
                return "Enemy"
    return "Neutral"


def is_combust(planet: str, planet_lon: float, sun_lon: float,
               retrograde: bool = False) -> bool:
    """Standard combustion thresholds."""
    if planet in ("Sun", "Rahu", "Ketu"):
        return False
    sep = abs((planet_lon - sun_lon + 180) % 360 - 180)
    thresholds = {
        "Moon": 12,
        "Mars": 17,
        "Mercury": 12 if retrograde else 14,
        "Jupiter": 11,
        "Venus": 8 if retrograde else 10,
        "Saturn": 15,
    }
    return sep < thresholds.get(planet, 360)


# Devanagari labels for dignity, used by render_html
DIGNITY_LABEL_EN = {
    "Exalted": "Exalted (Uchcha)",
    "Debilitated": "Debilitated (Neecha)",
    "Mooltrikona": "Mooltrikona",
    "Own": "Own sign",
    "Friend": "Friend's sign",
    "Enemy": "Enemy's sign",
    "Neutral": "Neutral",
}
DIGNITY_LABEL_NE = {
    "Exalted": "उच्च",
    "Debilitated": "नीच",
    "Mooltrikona": "मूलत्रिकोण",
    "Own": "स्व-राशि",
    "Friend": "मित्र-राशि",
    "Enemy": "शत्रु-राशि",
    "Neutral": "सम-राशि",
}
