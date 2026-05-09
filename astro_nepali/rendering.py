"""Render charts and panchanga results to the terminal using `rich`."""
from __future__ import annotations

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box

from .labels import (
    rashi_label, nakshatra_label, planet_label, vara_label,
    tithi_label, yoga_label, karana_label, to_nepali_digits,
    NEPALI_MONTHS, RASHIS,
)
from .kundali import PLANET_ABBREV, PLANET_ABBREV_DEV


def _format_deg(deg: float) -> str:
    """Format degrees as deg°min'sec''."""
    d = int(deg)
    m_full = (deg - d) * 60
    m = int(m_full)
    s = int((m_full - m) * 60)
    return f"{d:>2}°{m:02d}'{s:02d}\""


def render_birth_info(console: Console, info: dict) -> None:
    """Render the birth-info header panel."""
    bs = info["bs"]
    ad = info["ad"]
    ne_month_dev, ne_month_en = NEPALI_MONTHS[bs["month"] - 1]
    nepali_date_dev = (
        f"{to_nepali_digits(bs['year'])} {ne_month_dev} {to_nepali_digits(bs['day'])}"
    )

    lines = [
        f"[bold cyan]Name:[/]            {info.get('name', '—')}",
        f"[bold cyan]AD:[/]              {ad['date']} {ad['time']} (TZ {ad['tz']:+.2f})",
        f"[bold cyan]BS / विक्रम संवत्:[/]  "
        f"{nepali_date_dev}  ({bs['year']} {ne_month_en} {bs['day']})",
        f"[bold cyan]Place:[/]           {info['place_name']}  "
        f"(lat {info['latitude']:.4f}°, lon {info['longitude']:.4f}°E)",
        f"[bold cyan]Vara / वार:[/]       {vara_label(info['weekday_sun0'])}",
    ]
    console.print(Panel("\n".join(lines), title="Birth / जन्म विवरण", box=box.ROUNDED))


def render_panchanga(console: Console, p, system_label: str) -> None:
    table = Table(title=f"Panchanga / पञ्चाङ्ग — {system_label}", box=box.SIMPLE_HEAVY)
    table.add_column("Limb / अङ्ग", style="cyan")
    table.add_column("Value")

    table.add_row("Tithi / तिथि", tithi_label(p.tithi_in_paksha, p.paksha))
    table.add_row("Nakshatra / नक्षत्र", f"{nakshatra_label(p.nakshatra)} (pada {p.nakshatra_pada})")
    table.add_row("Yoga / योग", yoga_label(p.yoga))
    table.add_row("Karana / करण", karana_label(p.karana))
    table.add_row("Vara / वार", vara_label(p.vara))
    console.print(table)


def render_planet_table(console: Console, positions: dict, system_label: str) -> None:
    table = Table(title=f"Planets / ग्रह — {system_label}", box=box.SIMPLE_HEAVY)
    table.add_column("Planet / ग्रह", style="cyan", no_wrap=True)
    table.add_column("Sign / राशि", style="magenta")
    table.add_column("Position", justify="right")
    table.add_column("Nakshatra / नक्षत्र")
    table.add_column("Pada", justify="center")
    table.add_column("R", justify="center")

    order = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]
    for name in order:
        if name not in positions:
            continue
        p = positions[name]
        retro = "[red]℞[/]" if getattr(p, "retrograde", False) else ""
        table.add_row(
            planet_label(name),
            rashi_label(p.rashi),
            _format_deg(p.deg_in_rashi),
            nakshatra_label(p.nakshatra),
            str(p.nakshatra_pada),
            retro,
        )
    console.print(table)


def render_lagna(console: Console, asc_long: float, asc_rashi: int, deg_in_rashi: float, system: str) -> None:
    text = Text()
    text.append(f"Lagna / लग्न — {system}\n", style="bold yellow")
    text.append(f"  Sign:     {rashi_label(asc_rashi)}\n")
    text.append(f"  Position: {_format_deg(deg_in_rashi)} of {RASHIS[asc_rashi][2]}\n")
    text.append(f"  Absolute: {asc_long:.4f}°")
    console.print(Panel(text, box=box.ROUNDED))


def render_houses(console: Console, lagna_rashi: int, chart: dict, planets_in_house: dict) -> None:
    table = Table(title="Houses / भाव (Whole-sign)", box=box.SIMPLE_HEAVY)
    table.add_column("House / भाव", justify="center", style="cyan")
    table.add_column("Sign / राशि", style="magenta")
    table.add_column("Planets / ग्रह")

    for h in range(1, 13):
        rashi_idx = (lagna_rashi + h - 1) % 12
        planets = planets_in_house.get(h, [])
        planet_str = ", ".join(planet_label(p) for p in planets) if planets else "—"
        marker = " (Lagna)" if h == 1 else ""
        table.add_row(f"{h}{marker}", rashi_label(rashi_idx), planet_str)
    console.print(table)


def render_north_indian_diamond(console: Console, lagna_rashi: int, planets_in_house: dict) -> None:
    """Render a stylized 4x4-ish North-Indian chart in Unicode box drawing.

    House layout used (standard North Indian):
            +------+------+------+
            |  12  |  1   |  2   |
            +------+------+------+
            |  11  | Lag  |  3   |
            +------+------+------+
            |  10  |  -   |  4   |
            +------+------+------+
            |  9   |8 / 7 |  5   |
            +------+------+------+
    Houses 6 + 8 share the bottom-middle cell to keep it 3x4 = 12.
    """
    def cell(house: int) -> str:
        rashi_idx = (lagna_rashi + house - 1) % 12
        rashi_dev = RASHIS[rashi_idx][0]
        planets = planets_in_house.get(house, [])
        abbrev = " ".join(PLANET_ABBREV[p] for p in planets) if planets else ""
        return f"H{house} {rashi_dev}\n{abbrev}".rstrip()

    table = Table(box=box.HEAVY, show_header=False, show_lines=True,
                  title="Janma Kundali / जन्म कुण्डली (North-Indian, Whole-sign)")
    for _ in range(3):
        table.add_column(justify="center", width=14)

    table.add_row(cell(12), cell(1), cell(2))
    # Middle: row showing Lagna explicitly
    lag_rashi = RASHIS[lagna_rashi][0]
    lagna_cell = f"[bold yellow]LAGNA[/]\n{lag_rashi}"
    table.add_row(cell(11), lagna_cell, cell(3))
    table.add_row(cell(10), cell(4) if False else "", cell(4))
    # We'll combine the bottom row carefully:
    bottom_mid = cell(7) + (("\n— H8: " + " ".join(PLANET_ABBREV[p] for p in planets_in_house.get(8, []))) if planets_in_house.get(8) else "")
    bottom_mid_simple = f"H7 {RASHIS[(lagna_rashi+6)%12][0]} | H8 {RASHIS[(lagna_rashi+7)%12][0]}\n" + (
        " ".join(PLANET_ABBREV[p] for p in planets_in_house.get(7, [])) +
        (" / " + " ".join(PLANET_ABBREV[p] for p in planets_in_house.get(8, [])) if planets_in_house.get(8) else "")
    )
    table.add_row(cell(9), bottom_mid_simple, cell(5))
    # H6 row
    h6 = cell(6)
    table.add_row("", h6, "")
    console.print(table)


def render_dasha(console: Console, dashas: list, current) -> None:
    table = Table(title="Vimshottari Mahadasha / विंशोत्तरी महादशा", box=box.SIMPLE_HEAVY)
    table.add_column("Lord / स्वामी", style="cyan")
    table.add_column("Start")
    table.add_column("End")
    table.add_column("Years", justify="right")

    for d in dashas:
        years = (d.end - d.start).days / 365.25
        is_current = current is not None and d.start == current.start
        style = "bold green" if is_current else None
        marker = " ◀ current" if is_current else ""
        table.add_row(
            f"{planet_label(d.lord)}{marker}",
            d.start.strftime("%Y-%m-%d"),
            d.end.strftime("%Y-%m-%d"),
            f"{years:.2f}",
            style=style,
        )
    console.print(table)


def render_drik_vs_ss(console: Console, drik: dict, ss: dict) -> None:
    """Compare Drik vs Surya Siddhanta longitudes side by side."""
    table = Table(title="Drik vs Surya Siddhanta — Sidereal Longitudes",
                  box=box.SIMPLE_HEAVY,
                  caption="Δ = Drik longitude − SS longitude (positive = SS lags)")
    table.add_column("Planet / ग्रह", style="cyan")
    table.add_column("Drik (Lahiri)", justify="right")
    table.add_column("Surya Siddhanta", justify="right")
    table.add_column("Δ", justify="right")

    order = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]
    for name in order:
        if name not in drik or name not in ss:
            continue
        d_lon = drik[name].longitude
        s_lon = ss[name].longitude
        delta = (d_lon - s_lon + 540) % 360 - 180  # signed difference in (-180, 180]
        delta_str = f"{delta:+.3f}°"
        table.add_row(
            planet_label(name),
            f"{d_lon:.4f}°",
            f"{s_lon:.4f}°",
            delta_str,
        )
    console.print(table)
