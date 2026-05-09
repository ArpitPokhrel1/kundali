"""D9 Navamsha — divisional chart for marriage, dharma, and inner-strength reading.

Each rashi (30°) is divided into 9 navamshas of 3°20'. The navamsha rashi is:

    navamsha_rashi = floor(longitude * 9 / 30) % 12

Equivalently, for a planet at longitude L:
  - rashi R = L // 30
  - pada P = floor((L - R*30) * 9 / 30)  ∈ [0, 8]
  - navamsha = (R*9 + P) % 12

Verification by movable / fixed / dual rule:
  - Movable signs (R % 3 == 0): start from same sign       → matches R*9 % 12
  - Fixed signs   (R % 3 == 1): start from 9th from itself → matches R*9 % 12
  - Dual signs    (R % 3 == 2): start from 5th from itself → matches R*9 % 12
"""
from __future__ import annotations
from dataclasses import dataclass

from .kundali import HousePlacement, planet_house, planets_by_house


@dataclass
class D9Result:
    lagna_rashi: int
    planet_rashis: dict[str, int]    # planet name -> rashi index
    chart: dict[str, HousePlacement] # planet -> house placement (whole-sign)
    planets_in_house: dict[int, list[str]]


def navamsha_rashi(longitude: float) -> int:
    """Return the navamsha rashi index (0-11) for a given longitude (degrees)."""
    return int(longitude * 9.0 / 30.0) % 12


def compute_d9(positions: dict, lagna_long: float) -> D9Result:
    """Build the D9 navamsha chart from rasi-chart longitudes."""
    d9_lagna = navamsha_rashi(lagna_long)
    planet_rashis = {
        name: navamsha_rashi(p.longitude) for name, p in positions.items()
    }
    chart = {
        name: HousePlacement(planet_house(rashi, d9_lagna), rashi)
        for name, rashi in planet_rashis.items()
    }
    by_house = planets_by_house(chart)
    return D9Result(
        lagna_rashi=d9_lagna,
        planet_rashis=planet_rashis,
        chart=chart,
        planets_in_house=by_house,
    )


# Notes:
# - "Vargottama": when a planet sits in the same rashi in both D1 and D9.
#   This significantly strengthens the planet.
# - The Lagna's navamsha is itself an important "Navamsha Lagna" — read for
#   marriage and dharmic direction.

def vargottama_planets(d1_positions: dict, d9: D9Result) -> list[str]:
    """Return planets that are vargottama (same rashi in D1 and D9)."""
    out = []
    for name, p1 in d1_positions.items():
        if d9.planet_rashis.get(name) == p1.rashi:
            out.append(name)
    return out
