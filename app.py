"""Flask web app for Kundali Tarjun.

Run dev:    python app.py            (from inside web/)
Run prod:   gunicorn app:app
"""
from __future__ import annotations
import os
import sys
from datetime import datetime
from io import BytesIO

from flask import (
    Flask, render_template, request, jsonify, send_file, abort,
)

# astro_nepali lives next to this file (web/ is the project root)
HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

from astro_nepali import engine, calendar_bs, geocoding, render_html
from astro_nepali.i18n import T
from astro_nepali.labels import (
    RASHIS, NAKSHATRAS, NEPALI_MONTHS, PLANETS, NAKSHATRA_LORDS,
)
from astro_nepali.explain import (
    RASHI_TRAITS, HOUSE_MEANINGS, PLANET_MEANINGS, NAKSHATRA_THEMES,
)
from astro_nepali.jyotish_text import (
    MAHADASHA_NOTES_EN, MAHADASHA_NOTES_NE,
    PLANET_PSYCHOLOGY_EN, PLANET_PSYCHOLOGY_NE,
)


app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static",
)

BACKLINK_URL = "https://kundali.tarjun.com"
BACKLINK_TEXT = "Kundali Tarjun"
SITE_DOMAIN = "kundali.tarjun.com"
ASSET_VERSION = "hindu-minimal-20260521-01"


@app.context_processor
def inject_globals():
    """Make backlink + locale available to every template."""
    locale = request.cookies.get("locale", "en") if request else "en"
    if locale not in ("en", "ne"):
        locale = "en"
    theme = request.cookies.get("theme", "light") if request else "light"
    if theme not in ("light", "dark", "sepia"):
        theme = "light"
    t = T(locale)
    return {
        "BACKLINK_URL": BACKLINK_URL,
        "BACKLINK_TEXT": BACKLINK_TEXT,
        "SITE_DOMAIN": SITE_DOMAIN,
        "ASSET_VERSION": ASSET_VERSION,
        "locale": locale,
        "theme": theme,
        "t": t,
        "year": datetime.now().year,
    }


# ---------- Routes ----------

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/learn/")
def learn_index():
    return render_template("learn/index.html")


LEARN_TOPICS = {
    "rashis":     "rashis.html",
    "nakshatras": "nakshatras.html",
    "planets":    "planets.html",
    "houses":     "houses.html",
    "panchanga":  "panchanga.html",
    "dashas":     "dashas.html",
    "yogas":      "yogas.html",
    "aspects":    "aspects.html",
    "concepts":   "concepts.html",
    "how-to-read": "how_to_read.html",
}


@app.route("/learn/<topic>")
def learn_topic(topic):
    template = LEARN_TOPICS.get(topic)
    if not template:
        abort(404)
    ctx = {
        "topic": topic,
        "rashis": RASHIS,
        "rashi_traits": RASHI_TRAITS,
        "nakshatras": NAKSHATRAS,
        "nakshatra_themes": NAKSHATRA_THEMES,
        "nakshatra_lords": NAKSHATRA_LORDS,
        "planets": PLANETS,
        "planet_meanings": PLANET_MEANINGS,
        "house_meanings": HOUSE_MEANINGS,
        "mahadasha_en": MAHADASHA_NOTES_EN,
        "mahadasha_ne": MAHADASHA_NOTES_NE,
        "psy_en": PLANET_PSYCHOLOGY_EN,
        "psy_ne": PLANET_PSYCHOLOGY_NE,
    }
    return render_template(f"learn/{template}", **ctx)


@app.route("/about/")
def about():
    return render_template("about.html")


# ---------- API ----------

@app.route("/api/search-place")
def api_search_place():
    q = request.args.get("q", "").strip()
    if not q:
        return jsonify({"results": []})
    results = geocoding.search_places(q, limit=6)
    return jsonify({
        "results": [
            {"display": r.display_name, "lat": r.latitude, "lon": r.longitude}
            for r in results
        ]
    })


@app.route("/api/timezone")
def api_timezone():
    try:
        lat = float(request.args.get("lat", ""))
        lon = float(request.args.get("lon", ""))
        date_str = request.args.get("date", "")
        dt = datetime.strptime(date_str, "%Y-%m-%d")
    except (ValueError, TypeError):
        return jsonify({"error": "bad params"}), 400
    offset = geocoding.timezone_offset_hours(lat, lon, dt)
    return jsonify({"offset": offset})


@app.route("/api/bs-to-ad")
def api_bs_to_ad():
    try:
        y = int(request.args.get("y"))
        m = int(request.args.get("m"))
        d = int(request.args.get("d"))
        ad = calendar_bs.bs_to_ad(y, m, d)
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    return jsonify({"ad": ad.strftime("%Y-%m-%d")})


@app.route("/api/ad-to-bs")
def api_ad_to_bs():
    try:
        ad = datetime.strptime(request.args.get("d", ""), "%Y-%m-%d").date()
        y, m, d = calendar_bs.ad_to_bs(ad)
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    return jsonify({"y": y, "m": m, "d": d, "month_en": NEPALI_MONTHS[m - 1][1]})


@app.route("/api/compute", methods=["POST"])
def api_compute():
    """Compute the kundali. Returns rendered HTML for each tab."""
    data = request.get_json(silent=True) or {}
    try:
        date_mode = data.get("date_mode", "ad")
        if date_mode == "bs":
            ad_date = calendar_bs.bs_to_ad(
                int(data["bs_year"]), int(data["bs_month"]), int(data["bs_day"]),
            )
        else:
            ad_date = datetime.strptime(data["ad_date"], "%Y-%m-%d").date()
        h, m = (int(x) for x in data["time"].split(":"))
        birth_local = datetime(ad_date.year, ad_date.month, ad_date.day, h, m)

        result = engine.compute(
            name=data.get("name", "").strip(),
            birth_local=birth_local,
            tz_offset_hours=float(data.get("tz", 5.75)),
            latitude=float(data.get("lat", 27.7172)),
            longitude_east=float(data.get("lon", 85.3240)),
            place_name=data.get("place", "—") or "—",
            include_ss=True,
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    locale = data.get("locale", "en")
    theme = data.get("theme", "light")
    t = T(locale)
    return jsonify({
        "summary":     render_html.render_summary(result, t, theme),
        "topics":      render_html.render_topics(result, t, theme),
        "drik":        render_html.render_drik(result, t, theme, chart_mode="svg"),
        "d9":          render_html.render_d9(result, t, theme, chart_mode="svg"),
        "yogas":       render_html.render_yogas(result, t, theme),
        "dasha":       render_html.render_dasha(result, t, theme),
        "antardasha":  render_html.render_antardasha(result, t, theme),
        "ss":          render_html.render_ss(result, t, theme),
        "compare":     render_html.render_compare(result, t, theme),
        "explanation": render_html.render_explanation(result, t, theme),
    })


# ---------- Settings cookies ----------

@app.route("/api/set-pref", methods=["POST"])
def api_set_pref():
    """Persist locale and theme choice in cookies."""
    payload = request.get_json(silent=True) or request.form
    locale = payload.get("locale")
    theme = payload.get("theme")
    resp = jsonify({"ok": True})
    if locale in ("en", "ne"):
        resp.set_cookie("locale", locale, max_age=60 * 60 * 24 * 365)
    if theme in ("light", "dark", "sepia"):
        resp.set_cookie("theme", theme, max_age=60 * 60 * 24 * 365)
    return resp


@app.errorhandler(404)
def not_found(_):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
