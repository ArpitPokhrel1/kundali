"""Surya Siddhanta (classical sidereal) planetary calculations.

Implements the classical Indian algorithm:
  1. Mean longitude from revolutions per Mahayuga × ahargana / civil days per MY
  2. Manda correction (equation of center) for all planets
  3. Sighra correction (epicycle for synodic conjunction) for star-planets

Surya Siddhanta is intrinsically sidereal/nirayana — no ayanamsa adjustment is
needed. Results are directly comparable with Drik nirayana longitudes.

This is a first-order faithful implementation (mean motions exactly per text;
single sin-form epicycle equations). For sub-arcminute Surya Siddhanta accuracy
the four-step iterative manda-sighra procedure with proper geometric sighra
formulas would be needed — left as a future enhancement.

References:
  - Burgess (1860) tr. of Surya Siddhanta, chapters 1–2
  - Pingree (1978) "History of Mathematical Astronomy in India"
"""
from __future__ import annotations
from dataclasses import dataclass
import math

# ---- Surya Siddhanta constants (from text) ----

# Civil days in one Mahayuga (4,320,000 years)
CIVIL_DAYS_IN_MAHAYUGA = 1_577_917_828

# Julian Day of Kali Yuga epoch: midnight before sunrise, 18 Feb 3102 BCE (Ujjain).
# Standard reference used in Indian siddhantic astronomy.
KALI_EPOCH_JD = 588_465.5

# Ujjain longitude (prime meridian of classical Indian astronomy)
UJJAIN_LONGITUDE = 75.7833  # degrees east

# ---- Planet revolutions per Mahayuga (from chapter 1 of Surya Siddhanta) ----

# For Mercury and Venus, the body's mean longitude equals the Sun's mean
# longitude; the value here is the revolutions of the sighrocca (synodic point).
PLANET_REVOLUTIONS = {
    "Sun":     4_320_000,
    "Moon":    57_753_336,
    "Mars":    2_296_832,
    "Mercury": 17_937_060,   # sighrocca revolutions; mean = Sun's mean
    "Jupiter": 364_220,
    "Venus":   7_022_376,    # sighrocca revolutions; mean = Sun's mean
    "Saturn":  146_568,
}

# Rahu (Moon's ascending node) — retrograde
RAHU_REVOLUTIONS = -232_238

# Moon's apogee (Mandocca) — direct motion
MOON_APOGEE_REVOLUTIONS = 488_203

# ---- Manda epicycle peripheries (degrees) — classical SS values ----
# These produce the equation of center for each planet.
MANDA_PERIPHERY = {
    "Sun":     14.0,
    "Moon":    32.0,
    "Mars":    75.0,
    "Mercury": 30.0,
    "Jupiter": 33.0,
    "Venus":   12.0,
    "Saturn":  49.0,
}

# ---- Sighra epicycle peripheries (degrees) for star-planets ----
SIGHRA_PERIPHERY = {
    "Mars":    235.0,
    "Mercury": 132.0,
    "Jupiter": 70.0,
    "Venus":   261.0,
    "Saturn":  39.0,
}

# ---- Mandocca (apogee) longitudes at Kali Yuga start (degrees) ----
# Slow-moving; for v1 we treat these as fixed at Kali start. Moon's apogee is
# computed dynamically from MOON_APOGEE_REVOLUTIONS (it moves fast).
MANDOCCA_KALI = {
    "Sun":     77.13,
    "Mars":    130.0,
    "Mercury": 220.45,
    "Jupiter": 171.30,
    "Venus":   79.83,
    "Saturn":  236.62,
}

# Rahu position at Kali Yuga start (degrees)
RAHU_KALI = 180.0


# ---- Time computations ----

def ahargana(jd_ut: float, observer_longitude_east: float = UJJAIN_LONGITUDE) -> float:
    """Days since Kali Yuga epoch, measured at the observer's local meridian.

    Surya Siddhanta uses Ujjain time as standard. For a birth elsewhere, we
    correct by (observer_longitude − Ujjain_longitude)/15 hours.
    """
    longitude_correction_days = (observer_longitude_east - UJJAIN_LONGITUDE) / 360.0
    return (jd_ut - KALI_EPOCH_JD) + longitude_correction_days


def _mean_longitude(revolutions: int, ahargana_days: float, kali_offset: float = 0.0) -> float:
    """Mean longitude (degrees) for a body with the given revolutions per Mahayuga."""
    fraction = (revolutions * ahargana_days) / CIVIL_DAYS_IN_MAHAYUGA
    return (fraction * 360.0 + kali_offset) % 360.0


# ---- Equation of center / sighra equation (simplified) ----

def _manda_equation(mean_anomaly_deg: float, periphery_deg: float) -> float:
    """Manda equation (equation of center): sin(eq) = (P/360)·sin(MA)."""
    val = (periphery_deg / 360.0) * math.sin(math.radians(mean_anomaly_deg))
    val = max(-1.0, min(1.0, val))
    return math.degrees(math.asin(val))


def _sighra_equation(sighra_anomaly_deg: float, periphery_deg: float) -> float:
    """Sighra (synodic-conjunction) equation using the geometric SS formula:

        tan(eq) = r·sin(σ) / (R + r·cos(σ))

    where r/R = periphery/360, σ = sighra anomaly = sighrocca − planet.
    """
    r_over_R = periphery_deg / 360.0
    sin_s = math.sin(math.radians(sighra_anomaly_deg))
    cos_s = math.cos(math.radians(sighra_anomaly_deg))
    return math.degrees(math.atan2(r_over_R * sin_s, 1.0 + r_over_R * cos_s))


# ---- True longitude per planet ----

def _true_long_sun(mean_lon: float) -> float:
    """Sun: only manda correction (Sun is the reference point — no sighra)."""
    mandocca = MANDOCCA_KALI["Sun"]
    ma = (mean_lon - mandocca) % 360
    eq = _manda_equation(ma, MANDA_PERIPHERY["Sun"])
    return (mean_lon - eq) % 360


def _true_long_moon(mean_lon: float, moon_apogee_lon: float) -> float:
    """Moon: only manda correction; mandocca moves fast (apogee revolutions)."""
    ma = (mean_lon - moon_apogee_lon) % 360
    eq = _manda_equation(ma, MANDA_PERIPHERY["Moon"])
    return (mean_lon - eq) % 360


def _true_long_starplanet(name: str, mean_lon: float, sighrocca_lon: float) -> float:
    """Star-planets (Mars/Mercury/Jupiter/Venus/Saturn): four-step procedure.

    1. Apply half-manda equation
    2. Apply half-sighra equation
    3. Apply full manda equation (using corrected mean)
    4. Apply full sighra equation
    """
    mandocca = MANDOCCA_KALI[name]
    manda_p = MANDA_PERIPHERY[name]
    sighra_p = SIGHRA_PERIPHERY[name]

    ma = (mean_lon - mandocca) % 360
    L1 = (mean_lon - 0.5 * _manda_equation(ma, manda_p)) % 360

    sa = (sighrocca_lon - L1) % 360
    L2 = (L1 + 0.5 * _sighra_equation(sa, sighra_p)) % 360

    ma = (L2 - mandocca) % 360
    L3 = (L2 - _manda_equation(ma, manda_p)) % 360

    sa = (sighrocca_lon - L3) % 360
    L4 = (L3 + _sighra_equation(sa, sighra_p)) % 360
    return L4


@dataclass
class SSPosition:
    name: str
    longitude: float
    rashi: int
    deg_in_rashi: float
    nakshatra: int
    nakshatra_pada: int
    retrograde: bool = False  # SS approximation: not computed — left False

    @classmethod
    def from_longitude(cls, name: str, lon: float, retrograde: bool = False) -> "SSPosition":
        lon = lon % 360.0
        rashi = int(lon // 30)
        deg = lon - rashi * 30
        nak_size = 360.0 / 27.0
        nak = int(lon // nak_size)
        pada = int((lon - nak * nak_size) // (nak_size / 4)) + 1
        return cls(name, lon, rashi, deg, nak, pada, retrograde)


def planet_positions_ss(
    jd_ut: float,
    observer_longitude_east: float = UJJAIN_LONGITUDE,
) -> dict[str, SSPosition]:
    """Compute Surya Siddhanta sidereal positions for all planets + Rahu/Ketu."""
    t = ahargana(jd_ut, observer_longitude_east)

    # Sun: mean and true
    sun_mean = _mean_longitude(PLANET_REVOLUTIONS["Sun"], t)
    sun_true = _true_long_sun(sun_mean)

    # Moon: mean, apogee, true
    moon_mean = _mean_longitude(PLANET_REVOLUTIONS["Moon"], t)
    moon_apogee = _mean_longitude(MOON_APOGEE_REVOLUTIONS, t)
    moon_true = _true_long_moon(moon_mean, moon_apogee)

    # Star-planets — for Mars/Jupiter/Saturn the body's mean is its own;
    # for Mercury/Venus the mean equals Sun's mean and the table value is the
    # sighrocca's revolutions.
    out = {
        "Sun": SSPosition.from_longitude("Sun", sun_true),
        "Moon": SSPosition.from_longitude("Moon", moon_true),
    }

    for name in ("Mars", "Jupiter", "Saturn"):
        mean = _mean_longitude(PLANET_REVOLUTIONS[name], t)
        sighrocca = sun_mean  # Sun is the sighrocca for outer planets
        true_lon = _true_long_starplanet(name, mean, sighrocca)
        out[name] = SSPosition.from_longitude(name, true_lon)

    for name in ("Mercury", "Venus"):
        mean = sun_mean  # Mercury/Venus mean longitude = Sun's
        sighrocca = _mean_longitude(PLANET_REVOLUTIONS[name], t)
        true_lon = _true_long_starplanet(name, mean, sighrocca)
        out[name] = SSPosition.from_longitude(name, true_lon)

    # Rahu / Ketu — mean nodes only (no manda/sighra)
    rahu_lon = _mean_longitude(RAHU_REVOLUTIONS, t, kali_offset=RAHU_KALI)
    out["Rahu"] = SSPosition.from_longitude("Rahu", rahu_lon, retrograde=True)
    ketu_lon = (rahu_lon + 180.0) % 360.0
    out["Ketu"] = SSPosition.from_longitude("Ketu", ketu_lon, retrograde=True)

    return out


def lagna_ss(jd_ut: float, latitude: float, longitude_east: float) -> tuple[float, int, float]:
    """Compute Lagna (sidereal Ascendant) using Surya Siddhanta sidereal time.

    For Lagna we still need the rotational/geographic transformation; we use the
    SS sidereal-time formula based on mean motions, then derive the ascendant
    from local sidereal time and observer latitude.
    """
    # Sidereal time at observer's meridian (in degrees, sidereal frame)
    t = ahargana(jd_ut, longitude_east)
    # Sidereal rotation of Earth: stars complete 360° in one sidereal day
    # ≈ 1577917828 / (4320000*365.2587 - 4320000) civil days = ratio
    # Easier: sidereal days per Mahayuga = civil_days + 4320000 = 1582237828
    sidereal_revs_per_MY = CIVIL_DAYS_IN_MAHAYUGA + PLANET_REVOLUTIONS["Sun"]
    # Local mean sidereal time as a fraction of a sidereal day → degrees
    sidereal_angle = (sidereal_revs_per_MY * t / CIVIL_DAYS_IN_MAHAYUGA) * 360.0
    # Reference: Sun at Kali start was at 0° (vernal point coincided with
    # sidereal zero per SS). Add Sun's mean longitude as RAMC adjustment.
    sun_mean = _mean_longitude(PLANET_REVOLUTIONS["Sun"], t)
    ramc = (sidereal_angle + sun_mean) % 360.0

    # Compute ascendant from RAMC + latitude (standard formula)
    obliquity = 23.4393  # SS gives mean obliquity ~23°27'; modern = 23.44
    lat_r = math.radians(latitude)
    ramc_r = math.radians(ramc)
    obl_r = math.radians(obliquity)
    asc = math.atan2(
        math.cos(ramc_r),
        -(math.sin(ramc_r) * math.cos(obl_r) + math.tan(lat_r) * math.sin(obl_r)),
    )
    asc_deg = math.degrees(asc) % 360.0
    rashi = int(asc_deg // 30)
    return asc_deg, rashi, asc_deg - rashi * 30
