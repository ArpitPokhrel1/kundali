"""Panchanga: the five limbs (Tithi, Nakshatra, Yoga, Karana, Vara) at birth.

All computations work from sidereal Sun and Moon longitudes. Pass the longitudes
from either Drik or SS — same arithmetic, just different inputs.
"""
from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Panchanga:
    tithi_index: int          # 1..30 (1..15 Shukla, 16..30 Krishna)
    tithi_in_paksha: int      # 1..15
    paksha: str               # "Shukla" or "Krishna"
    nakshatra: int            # 0..26 (Moon's nakshatra)
    nakshatra_pada: int       # 1..4
    yoga: int                 # 0..26
    karana: int               # 0..10  (one of 11 karana names)
    vara: int                 # 0..6 (Sunday=0)


def compute_panchanga(
    sun_longitude: float,
    moon_longitude: float,
    weekday_sun0: int,
) -> Panchanga:
    """Compute panchanga from sidereal Sun + Moon longitudes and weekday."""
    # Tithi: lunar elongation from Sun, in 12° steps (1..30)
    elongation = (moon_longitude - sun_longitude) % 360.0
    tithi_index = int(elongation // 12) + 1   # 1..30
    if tithi_index <= 15:
        paksha = "Shukla"
        tithi_in_paksha = tithi_index
    else:
        paksha = "Krishna"
        tithi_in_paksha = tithi_index - 15

    # Nakshatra (Moon-based): each is 360/27 = 13.333° wide
    nak_size = 360.0 / 27.0
    nakshatra = int(moon_longitude // nak_size)
    pos_in_nak = moon_longitude - nakshatra * nak_size
    pada = int(pos_in_nak // (nak_size / 4)) + 1

    # Yoga: (Sun + Moon) sum mapped to 27 divisions of 360°
    yoga_sum = (sun_longitude + moon_longitude) % 360.0
    yoga = int(yoga_sum // nak_size)

    # Karana: half-tithi, mapped to 11 names. There are 60 half-tithis in a month.
    # First half-tithi (Shukla Pratipada first half) → "Kimstughna" (last name).
    # Then: 8 cycles of (Bava..Vishti) covering tithis 1.5..28.0,
    # followed by Shakuni, Chatushpada, Naga at tithis 28.5..30.
    # We'll use the standard mapping:
    half_tithi = int(elongation // 6)  # 0..59
    karana = _karana_index_for_half_tithi(half_tithi)

    return Panchanga(
        tithi_index=tithi_index,
        tithi_in_paksha=tithi_in_paksha,
        paksha=paksha,
        nakshatra=nakshatra,
        nakshatra_pada=pada,
        yoga=yoga,
        karana=karana,
        vara=weekday_sun0,
    )


def _karana_index_for_half_tithi(half: int) -> int:
    """Map a half-tithi (0..59 since lunar new moon) to one of 11 karana names.

    Karana name order (matches astro_nepali.labels.KARANA_NAMES):
        0:Bava 1:Balava 2:Kaulava 3:Taitila 4:Garaja 5:Vanija 6:Vishti
        7:Shakuni 8:Chatushpada 9:Naga 10:Kimstughna

    Layout:
      half_tithi 0           → Kimstughna (10)
      half_tithi 1..56       → 8 cycles of Bava..Vishti (0..6 repeating)
      half_tithi 57          → Shakuni (7)
      half_tithi 58          → Chatushpada (8)
      half_tithi 59          → Naga (9)
    """
    if half == 0:
        return 10  # Kimstughna
    if half <= 56:
        return (half - 1) % 7  # Bava..Vishti
    return 7 + (half - 57)     # Shakuni, Chatushpada, Naga
