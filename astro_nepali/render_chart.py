"""North-Indian Janma Kundali chart — proper diamond geometry.

Builds an SVG (12 polygons + diagonals + outer diamond), renders it to PNG
using Qt's QSvgRenderer so it can be embedded in QTextBrowser via a base64
data URI.

House polygon mapping (counterclockwise from H1 at top):
  H1  = inner-top diamond region        H7  = inner-bottom diamond region
  H2  = upper-left corner, top side     H8  = lower-right corner, bottom side
  H3  = upper-left corner, left side    H9  = lower-right corner, right side
  H4  = inner-left diamond region       H10 = inner-right diamond region
  H5  = lower-left corner, left side    H11 = upper-right corner, right side
  H6  = lower-left corner, bottom side  H12 = upper-right corner, top side
"""
from __future__ import annotations
import base64

from .labels import RASHIS
from .kundali import PLANET_ABBREV


# Canvas size
SIZE = 600

# Vertices
TL, TM, TR = (0, 0), (SIZE // 2, 0), (SIZE, 0)
ML, C, MR = (0, SIZE // 2), (SIZE // 2, SIZE // 2), (SIZE, SIZE // 2)
BL, BM, BR = (0, SIZE), (SIZE // 2, SIZE), (SIZE, SIZE)
# Diagonal-diamond intersections
P1 = (SIZE // 4, SIZE // 4)         # upper-left
P2 = (3 * SIZE // 4, SIZE // 4)     # upper-right
P3 = (3 * SIZE // 4, 3 * SIZE // 4) # lower-right
P4 = (SIZE // 4, 3 * SIZE // 4)     # lower-left

# House polygons and centroid positions for labels
HOUSE_POLYGONS = {
    1:  [TM, P2, C, P1],
    2:  [TL, TM, P1],
    3:  [TL, ML, P1],
    4:  [P1, C, P4, ML],
    5:  [BL, ML, P4],
    6:  [BL, BM, P4],
    7:  [C, P3, BM, P4],
    8:  [BR, BM, P3],
    9:  [BR, MR, P3],
    10: [P2, MR, P3, C],
    11: [TR, MR, P2],
    12: [TR, TM, P2],
}

# Roughly visually-balanced label centers (centroid is OK but slight nudges
# avoid overlap with diagonals)
LABEL_CENTERS = {
    1:  (300, 130),
    2:  (160, 60),
    3:  (60, 160),
    4:  (130, 300),
    5:  (60, 440),
    6:  (160, 540),
    7:  (300, 470),
    8:  (440, 540),
    9:  (540, 440),
    10: (470, 300),
    11: (540, 160),
    12: (440, 60),
}


def _polygon_str(points: list[tuple[int, int]]) -> str:
    return " ".join(f"{x},{y}" for x, y in points)


def make_svg(lagna_rashi: int, planets_in_house: dict[int, list[str]]) -> str:
    """Build the SVG markup for the North-Indian chart."""
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{SIZE}" height="{SIZE}" '
        f'viewBox="0 0 {SIZE} {SIZE}">',
        # Background
        f'<rect width="{SIZE}" height="{SIZE}" fill="#fefcff" />',
        # Highlight Lagna (H1) polygon
        f'<polygon points="{_polygon_str(HOUSE_POLYGONS[1])}" '
        f'fill="#fff3e0" stroke="none" />',
        # Outer square
        f'<rect x="2" y="2" width="{SIZE-4}" height="{SIZE-4}" '
        f'fill="none" stroke="#4a148c" stroke-width="3" />',
        # Diagonals
        f'<line x1="0" y1="0" x2="{SIZE}" y2="{SIZE}" '
        f'stroke="#6a1b9a" stroke-width="2" />',
        f'<line x1="{SIZE}" y1="0" x2="0" y2="{SIZE}" '
        f'stroke="#6a1b9a" stroke-width="2" />',
        # Midpoint diamond
        f'<polygon points="{TM[0]},{TM[1]} {MR[0]},{MR[1]} '
        f'{BM[0]},{BM[1]} {ML[0]},{ML[1]}" '
        f'fill="none" stroke="#6a1b9a" stroke-width="2" />',
    ]

    # Per-house labels: house number, sign, planets
    for h in range(1, 13):
        rashi_idx = (lagna_rashi + h - 1) % 12
        rashi_dev = RASHIS[rashi_idx][0]
        rashi_en = RASHIS[rashi_idx][2][:3]  # short form
        planets = planets_in_house.get(h, [])
        cx, cy = LABEL_CENTERS[h]
        is_lagna = (h == 1)

        # House number — small, top-corner-style
        parts.append(
            f'<text x="{cx}" y="{cy - 22}" font-family="Anek Devanagari, Mukta, sans-serif" '
            f'font-size="11" fill="#7b6b5b" text-anchor="middle">'
            f'{"Lagna" if is_lagna else f"H{h}"}</text>'
        )
        # Sign (Devanagari + English short)
        parts.append(
            f'<text x="{cx}" y="{cy - 5}" font-family="Anek Devanagari, Mukta, '
            f'Nirmala UI, sans-serif" font-size="14" fill="#173a63" '
            f'font-weight="bold" text-anchor="middle">'
            f'{rashi_dev} ({rashi_en})</text>'
        )
        # Planets
        if planets:
            txt = "  ".join(PLANET_ABBREV[p] for p in planets)
            parts.append(
                f'<text x="{cx}" y="{cy + 18}" font-family="Anek Devanagari, Mukta, sans-serif" '
                f'font-size="15" fill="#b85f24" font-weight="bold" '
                f'text-anchor="middle">{txt}</text>'
            )

    parts.append("</svg>")
    return "\n".join(parts)


def svg_to_png_data_uri(svg: str) -> str:
    """Render the SVG to PNG using Qt's QSvgRenderer; return as data URI.

    Falls back to embedding the raw SVG (as a data URI) when no QGuiApplication
    is alive — needed so non-GUI contexts (smoke tests, CLI, PDF export setup)
    can still produce HTML without crashing on QImage instantiation.
    """
    from PySide6.QtCore import QByteArray, QBuffer, QIODevice
    from PySide6.QtGui import QImage, QPainter, QColor, QGuiApplication
    from PySide6.QtSvg import QSvgRenderer

    if QGuiApplication.instance() is None:
        b64 = base64.b64encode(svg.encode("utf-8")).decode("ascii")
        return f"data:image/svg+xml;base64,{b64}"

    renderer = QSvgRenderer(QByteArray(svg.encode("utf-8")))
    image = QImage(SIZE, SIZE, QImage.Format_ARGB32)
    image.fill(QColor("white"))
    painter = QPainter(image)
    renderer.render(painter)
    painter.end()

    buf = QByteArray()
    qbuf = QBuffer(buf)
    qbuf.open(QIODevice.WriteOnly)
    image.save(qbuf, "PNG")
    qbuf.close()

    b64 = base64.b64encode(bytes(buf)).decode("ascii")
    return f"data:image/png;base64,{b64}"


def chart_html(lagna_rashi: int, planets_in_house: dict[int, list[str]],
               mode: str = "auto") -> str:
    """Return chart markup for embedding.

    mode='auto'   — PNG if QApplication exists (GUI), else inline SVG (web).
    mode='png'    — force the Qt PNG path.
    mode='svg'    — force inline SVG (browsers render it natively).
    """
    svg = make_svg(lagna_rashi, planets_in_house)

    if mode == "svg":
        return f'<div class="kundali-chart-shell" style="text-align:center;margin:14px auto;">{svg}</div>'

    if mode == "png":
        uri = svg_to_png_data_uri(svg)
        return (
            f'<div class="kundali-chart-shell" style="text-align:center;margin:14px auto;">'
            f'<img src="{uri}" width="{SIZE}" height="{SIZE}" '
            f'alt="Janma Kundali chart"/></div>'
        )

    # auto: detect Qt
    try:
        from PySide6.QtGui import QGuiApplication
        if QGuiApplication.instance() is not None:
            uri = svg_to_png_data_uri(svg)
            return (
                f'<div class="kundali-chart-shell" style="text-align:center;margin:14px auto;">'
                f'<img src="{uri}" width="{SIZE}" height="{SIZE}" '
                f'alt="Janma Kundali chart"/></div>'
            )
    except Exception:
        pass
    return f'<div class="kundali-chart-shell" style="text-align:center;margin:14px auto;">{svg}</div>'
