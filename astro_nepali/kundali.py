"""Kundali (birth chart) assembly: Lagna, planet → house mapping."""
from __future__ import annotations
from dataclasses import dataclass


@dataclass
class HousePlacement:
    house: int      # 1..12
    rashi: int      # 0..11


def planet_house(planet_rashi: int, lagna_rashi: int) -> int:
    """Whole-sign house number (1..12) for a planet given the Lagna's rashi."""
    return ((planet_rashi - lagna_rashi) % 12) + 1


def assemble_chart(
    lagna_rashi: int,
    planet_rashis: dict[str, int],
) -> dict[str, HousePlacement]:
    """For each planet, compute its house and rashi (whole-sign system)."""
    return {
        name: HousePlacement(planet_house(rashi, lagna_rashi), rashi)
        for name, rashi in planet_rashis.items()
    }


def planets_by_house(
    chart: dict[str, HousePlacement],
) -> dict[int, list[str]]:
    """Group planet names by their house number (1..12)."""
    out: dict[int, list[str]] = {h: [] for h in range(1, 13)}
    for name, hp in chart.items():
        out[hp.house].append(name)
    return out


# Planet abbreviations for the chart diagram (English)
PLANET_ABBREV = {
    "Sun": "Su", "Moon": "Mo", "Mars": "Ma", "Mercury": "Me",
    "Jupiter": "Ju", "Venus": "Ve", "Saturn": "Sa",
    "Rahu": "Ra", "Ketu": "Ke",
}

# Devanagari abbreviations
PLANET_ABBREV_DEV = {
    "Sun": "सू", "Moon": "च", "Mars": "मं", "Mercury": "बु",
    "Jupiter": "गु", "Venus": "शु", "Saturn": "श",
    "Rahu": "रा", "Ketu": "के",
}
