"""Vimshottari Dasha — 120-year planetary period system.

Birth Mahadasha is determined by the Moon's nakshatra at birth. The remaining
fraction of the Mahadasha is computed from how far the Moon has traveled within
the nakshatra at the moment of birth.
"""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timedelta

# Mahadasha order (each row: lord, years)
DASHA_SEQUENCE = [
    ("Ketu", 7),
    ("Venus", 20),
    ("Sun", 6),
    ("Moon", 10),
    ("Mars", 7),
    ("Rahu", 18),
    ("Jupiter", 16),
    ("Saturn", 19),
    ("Mercury", 17),
]
DASHA_TOTAL_YEARS = 120

# Map nakshatra index (0..26) → starting Mahadasha lord
# Order: Ashwini=Ketu, Bharani=Venus, Krittika=Sun, ... cycles every 9
def nakshatra_lord(nakshatra_index: int) -> str:
    return DASHA_SEQUENCE[nakshatra_index % 9][0]


def years_for_lord(lord: str) -> int:
    return next(y for l, y in DASHA_SEQUENCE if l == lord)


@dataclass
class DashaPeriod:
    lord: str
    start: datetime
    end: datetime


def compute_dashas(
    birth: datetime,
    moon_longitude_sidereal: float,
    levels: int = 1,
) -> list[DashaPeriod]:
    """Compute Mahadasha sequence from birth.

    levels=1 → just Mahadashas. (Antardashas/Bhuktis are an easy extension.)
    Returns the 9 Mahadashas covering ~120 years from birth, with the FIRST
    Mahadasha being the partial remainder of the nakshatra at birth.
    """
    nak_size = 360.0 / 27.0
    nak_index = int(moon_longitude_sidereal // nak_size)
    pos_in_nak = moon_longitude_sidereal - nak_index * nak_size
    fraction_traversed = pos_in_nak / nak_size  # 0..1

    starting_lord = nakshatra_lord(nak_index)
    starting_lord_idx = next(i for i, (l, _) in enumerate(DASHA_SEQUENCE) if l == starting_lord)

    out: list[DashaPeriod] = []
    cursor = birth

    # First (partial) Mahadasha
    full_years = years_for_lord(starting_lord)
    remaining_years = full_years * (1.0 - fraction_traversed)
    end = cursor + timedelta(days=remaining_years * 365.25)
    out.append(DashaPeriod(starting_lord, cursor, end))
    cursor = end

    # Subsequent full Mahadashas
    for offset in range(1, 9):
        idx = (starting_lord_idx + offset) % 9
        lord, years = DASHA_SEQUENCE[idx]
        end = cursor + timedelta(days=years * 365.25)
        out.append(DashaPeriod(lord, cursor, end))
        cursor = end

    return out


def current_dasha(dashas: list[DashaPeriod], at: datetime) -> DashaPeriod | None:
    for d in dashas:
        if d.start <= at < d.end:
            return d
    return None


# ---- Antardasha (sub-period inside a Mahadasha) ----

@dataclass
class AntarPeriod:
    maha_lord: str       # the Mahadasha's lord
    antar_lord: str      # the Antardasha's lord
    start: datetime
    end: datetime

    @property
    def label(self) -> str:
        return f"{self.maha_lord}–{self.antar_lord}"


def antardashas_for(mahadasha: DashaPeriod) -> list[AntarPeriod]:
    """Return the 9 antardashas inside the given Mahadasha.

    Order: starts with the Mahadasha's own lord, then proceeds in the
    standard Vimshottari sequence. Duration of each antardasha is
    proportional: (mahadasha_years * antar_lord_years) / 120.
    """
    md_lord = mahadasha.lord
    md_years = years_for_lord(md_lord)
    md_idx = next(i for i, (l, _) in enumerate(DASHA_SEQUENCE) if l == md_lord)

    out: list[AntarPeriod] = []
    cursor = mahadasha.start
    for offset in range(9):
        idx = (md_idx + offset) % 9
        lord, lord_years = DASHA_SEQUENCE[idx]
        duration_days = (md_years * lord_years / 120.0) * 365.25
        end = cursor + timedelta(days=duration_days)
        # Snap last antardasha to mahadasha end (avoid floating-point drift)
        if offset == 8:
            end = mahadasha.end
        out.append(AntarPeriod(md_lord, lord, cursor, end))
        cursor = end
    return out


def all_antardashas(dashas: list[DashaPeriod]) -> list[AntarPeriod]:
    """Flatten all Mahadashas into their antardashas — 9 × 9 = 81 sub-periods."""
    out: list[AntarPeriod] = []
    for md in dashas:
        out.extend(antardashas_for(md))
    return out


def current_antardasha(antars: list[AntarPeriod], at: datetime) -> AntarPeriod | None:
    for a in antars:
        if a.start <= at < a.end:
            return a
    return None
