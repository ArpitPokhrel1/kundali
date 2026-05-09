"""Place lookup: type a place name → get lat/lon/timezone offset.

Uses OpenStreetMap Nominatim (free, no API key) for geocoding, and
`timezonefinder` for offline timezone resolution from coordinates.
"""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timezone as dt_timezone
from zoneinfo import ZoneInfo

from geopy.geocoders import Nominatim
from geopy.exc import GeopyError
from timezonefinder import TimezoneFinder


_geocoder = Nominatim(user_agent="astro-nepali/0.1")
_tf = TimezoneFinder()


@dataclass
class PlaceMatch:
    display_name: str
    latitude: float
    longitude: float


def search_places(query: str, limit: int = 6, timeout: int = 8) -> list[PlaceMatch]:
    """Look up a place by name. Returns up to `limit` matches."""
    if not query.strip():
        return []
    try:
        results = _geocoder.geocode(query, exactly_one=False, limit=limit, timeout=timeout)
    except GeopyError:
        return []
    if not results:
        return []
    return [
        PlaceMatch(r.address, r.latitude, r.longitude)
        for r in results
    ]


def timezone_offset_hours(lat: float, lon: float, at: datetime) -> float | None:
    """Return UTC offset in hours for the timezone at (lat, lon) on date `at`.

    Accounts for DST at the given moment. Returns None if no timezone resolved.
    """
    tz_name = _tf.timezone_at(lat=lat, lng=lon)
    if not tz_name:
        return None
    aware = at.replace(tzinfo=ZoneInfo(tz_name))
    return aware.utcoffset().total_seconds() / 3600.0


def osm_url(lat: float, lon: float, zoom: int = 12) -> str:
    """OpenStreetMap link for visual verification."""
    return f"https://www.openstreetmap.org/?mlat={lat}&mlon={lon}#map={zoom}/{lat}/{lon}"
