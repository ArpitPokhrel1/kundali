"""Pure computation engine — used by both CLI, GUI, and the web app.

Returns a structured KundaliResult; rendering is the caller's responsibility.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from . import calendar_bs, ephemeris_drik, surya_siddhanta
from . import panchanga as pan_module
from . import kundali, dasha, d9, yogas, topics, dignities


@dataclass
class KundaliResult:
    # ---- Inputs ----
    name: str
    birth_local: datetime
    tz_offset_hours: float
    latitude: float
    longitude: float
    place_name: str
    bs_date: tuple[int, int, int]
    weekday_sun0: int

    # ---- Drik (rasi chart, D1) ----
    drik_positions: dict
    drik_lagna_long: float
    drik_lagna_rashi: int
    drik_lagna_deg: float
    drik_panchanga: Any
    drik_chart: dict
    drik_planets_in_house: dict
    ayanamsa_lahiri: float

    # ---- Surya Siddhanta (optional) ----
    ss_positions: dict | None = None
    ss_panchanga: Any = None

    # ---- Vimshottari Dasha ----
    dashas: list = field(default_factory=list)
    current_dasha: Any = None
    current_antardasha: Any = None  # AntarPeriod

    # ---- D9 Navamsha ----
    d9: Any = None                  # d9.D9Result
    vargottama: list[str] = field(default_factory=list)

    # ---- Dignities (planet -> 'Exalted' / 'Own' / etc.) ----
    drik_dignities: dict = field(default_factory=dict)

    # ---- Yogas ----
    yogas: list = field(default_factory=list)  # list[Yoga]

    # ---- Topic readings (Education, Health, ... ) ----
    topics: list = field(default_factory=list)  # list[TopicReading]


def compute(
    *,
    name: str,
    birth_local: datetime,
    tz_offset_hours: float,
    latitude: float,
    longitude_east: float,
    place_name: str,
    include_ss: bool = True,
) -> KundaliResult:
    """Compute the full kundali from birth datetime + place."""
    bs_y, bs_m, bs_d = calendar_bs.ad_to_bs(birth_local.date())
    weekday_sun0 = (birth_local.weekday() + 1) % 7  # Sunday=0

    jd_ut = ephemeris_drik.to_julian_day_ut(birth_local, tz_offset_hours)

    # ---- Drik (D1) ----
    drik_pos = ephemeris_drik.planet_positions(jd_ut)
    drik_asc_long, drik_asc_rashi, drik_asc_deg = ephemeris_drik.lagna(
        jd_ut, latitude, longitude_east
    )
    ayan = ephemeris_drik.lahiri_ayanamsa(jd_ut)

    drik_panchanga = pan_module.compute_panchanga(
        drik_pos["Sun"].longitude,
        drik_pos["Moon"].longitude,
        weekday_sun0,
    )
    drik_planet_rashis = {n: p.rashi for n, p in drik_pos.items()}
    drik_chart = kundali.assemble_chart(drik_asc_rashi, drik_planet_rashis)
    drik_planets_in_house = kundali.planets_by_house(drik_chart)

    # ---- D9 Navamsha ----
    d9_result = d9.compute_d9(drik_pos, drik_asc_long)
    vargottama = d9.vargottama_planets(drik_pos, d9_result)

    # ---- Dignities ----
    dign_map = {
        name: dignities.dignity_of(name, p.longitude)
        for name, p in drik_pos.items()
    }

    # ---- Surya Siddhanta ----
    ss_pos = ss_panchanga = None
    if include_ss:
        ss_pos = surya_siddhanta.planet_positions_ss(
            jd_ut, observer_longitude_east=longitude_east
        )
        ss_panchanga = pan_module.compute_panchanga(
            ss_pos["Sun"].longitude,
            ss_pos["Moon"].longitude,
            weekday_sun0,
        )

    # ---- Vimshottari (Maha + Antar) ----
    md_list = dasha.compute_dashas(birth_local, drik_pos["Moon"].longitude)
    now = datetime.now()
    current_md = dasha.current_dasha(md_list, now)
    current_antar = None
    if current_md is not None:
        antars = dasha.antardashas_for(current_md)
        current_antar = dasha.current_antardasha(antars, now)

    # ---- Yogas ----
    detected_yogas = yogas.detect(drik_pos, drik_asc_rashi)

    # ---- Topic readings ----
    topic_readings = topics.analyze_all(drik_pos, drik_asc_rashi)

    return KundaliResult(
        name=name,
        birth_local=birth_local,
        tz_offset_hours=tz_offset_hours,
        latitude=latitude,
        longitude=longitude_east,
        place_name=place_name,
        bs_date=(bs_y, bs_m, bs_d),
        weekday_sun0=weekday_sun0,
        drik_positions=drik_pos,
        drik_lagna_long=drik_asc_long,
        drik_lagna_rashi=drik_asc_rashi,
        drik_lagna_deg=drik_asc_deg,
        drik_panchanga=drik_panchanga,
        drik_chart=drik_chart,
        drik_planets_in_house=drik_planets_in_house,
        ayanamsa_lahiri=ayan,
        ss_positions=ss_pos,
        ss_panchanga=ss_panchanga,
        dashas=md_list,
        current_dasha=current_md,
        current_antardasha=current_antar,
        d9=d9_result,
        vargottama=vargottama,
        drik_dignities=dign_map,
        yogas=detected_yogas,
        topics=topic_readings,
    )
