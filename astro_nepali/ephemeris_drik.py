"""Drik Siddhanta (modern observational) calculations via Swiss Ephemeris.

Uses Lahiri ayanamsa (the standard Indian government-endorsed sidereal reference)
to convert Swiss Ephemeris's tropical longitudes into sidereal (nirayana)
longitudes used in Vedic astrology.
"""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta

import swisseph as swe

# Use Lahiri (Chitrapaksha) — the official Indian sidereal ayanamsa.
swe.set_sid_mode(swe.SIDM_LAHIRI, 0, 0)

PLANET_CODES = {
    "Sun": swe.SUN,
    "Moon": swe.MOON,
    "Mars": swe.MARS,
    "Mercury": swe.MERCURY,
    "Jupiter": swe.JUPITER,
    "Venus": swe.VENUS,
    "Saturn": swe.SATURN,
    "Rahu": swe.MEAN_NODE,  # Mean Rahu — the most common Vedic convention
}

# Sidereal computation flag
FLAGS = swe.FLG_SWIEPH | swe.FLG_SIDEREAL | swe.FLG_SPEED


@dataclass
class PlanetPosition:
    name: str
    longitude: float       # sidereal longitude in degrees [0, 360)
    speed: float           # degrees/day (negative = retrograde)
    rashi: int             # 0..11
    deg_in_rashi: float    # 0..30
    nakshatra: int         # 0..26
    nakshatra_pada: int    # 1..4

    @property
    def retrograde(self) -> bool:
        return self.speed < 0


def to_julian_day_ut(dt_local: datetime, tz_offset_hours: float) -> float:
    """Convert local civil datetime + timezone offset to Julian Day (UT)."""
    # Convert to UT
    ut = dt_local - timedelta(hours=tz_offset_hours)
    return swe.julday(
        ut.year, ut.month, ut.day,
        ut.hour + ut.minute / 60.0 + ut.second / 3600.0,
    )


def lahiri_ayanamsa(jd_ut: float) -> float:
    """Lahiri ayanamsa value (degrees) at the given Julian Day (UT)."""
    return swe.get_ayanamsa_ut(jd_ut)


def _decompose(longitude: float) -> tuple[int, float, int, int]:
    longitude = longitude % 360.0
    rashi = int(longitude // 30)
    deg_in_rashi = longitude - rashi * 30
    # Each nakshatra is 360/27 = 13°20' = 13.333... deg
    nak_size = 360.0 / 27.0
    nakshatra = int(longitude // nak_size)
    pos_in_nak = longitude - nakshatra * nak_size
    pada = int(pos_in_nak // (nak_size / 4)) + 1
    return rashi, deg_in_rashi, nakshatra, pada


def planet_positions(jd_ut: float) -> dict[str, PlanetPosition]:
    """Compute sidereal positions of all planets + Rahu/Ketu at the given JD."""
    out: dict[str, PlanetPosition] = {}
    for name, code in PLANET_CODES.items():
        result, _ = swe.calc_ut(jd_ut, code, FLAGS)
        lon = result[0] % 360.0
        speed = result[3]
        rashi, deg, nak, pada = _decompose(lon)
        out[name] = PlanetPosition(name, lon, speed, rashi, deg, nak, pada)
    # Ketu is exactly 180° opposite Rahu
    rahu = out["Rahu"]
    ketu_lon = (rahu.longitude + 180.0) % 360.0
    rashi, deg, nak, pada = _decompose(ketu_lon)
    out["Ketu"] = PlanetPosition(
        "Ketu", ketu_lon, -rahu.speed, rashi, deg, nak, pada
    )
    return out


def lagna(jd_ut: float, latitude: float, longitude: float) -> tuple[float, int, float]:
    """Compute the Lagna (sidereal Ascendant).

    Returns (longitude_deg, rashi_index, deg_within_rashi).
    """
    cusps, ascmc = swe.houses_ex(jd_ut, latitude, longitude, b'P', swe.FLG_SIDEREAL)
    asc = ascmc[0] % 360.0  # ASC is index 0
    rashi = int(asc // 30)
    return asc, rashi, asc - rashi * 30


def house_cusps(jd_ut: float, latitude: float, longitude: float) -> list[float]:
    """Return 12 sidereal house cusps using Placidus."""
    cusps, _ = swe.houses_ex(jd_ut, latitude, longitude, b'P', swe.FLG_SIDEREAL)
    return [c % 360.0 for c in cusps[:12]]


def whole_sign_houses(asc_rashi: int) -> list[int]:
    """Return list of 12 rashi indices for whole-sign houses (1st = Lagna's rashi).

    Whole-sign is the most common Vedic house system in North-Indian style charts.
    """
    return [(asc_rashi + i) % 12 for i in range(12)]
