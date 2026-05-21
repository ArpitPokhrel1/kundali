"""HTML renderers for the GUI's QTextBrowser tabs (theme-aware, educational)."""
from __future__ import annotations
from datetime import date

from .labels import (
    RASHIS, NAKSHATRAS, NEPALI_MONTHS, to_nepali_digits,
    rashi_label, nakshatra_label, planet_label, vara_label,
    tithi_label, yoga_label, karana_label,
)
from .kundali import PLANET_ABBREV
from .i18n import T
from .explain import (
    RASHI_TRAITS, HOUSE_MEANINGS, PLANET_MEANINGS, NAKSHATRA_THEMES,
)
from .jyotish_text import mahadasha_notes, planet_psychology
from .themes import get_theme
from .dignities import DIGNITY_LABEL_EN, DIGNITY_LABEL_NE
from . import calendar_bs, render_chart, dasha as dasha_mod


CSS_TEMPLATE = """
<style>
  body {{ font-family: 'Anek Devanagari', 'Mukta', 'Noto Sans Devanagari', 'Nirmala UI', sans-serif;
         font-size: 13px; color: {text}; line-height: 1.6; background: {bg}; }}
  h2 {{ color: {accent}; border-bottom: 2px solid {accent_pale};
       padding-bottom: 4px; margin-top: 18px; }}
  h3 {{ color: {accent_light}; margin-top: 16px; margin-bottom: 6px; }}
  h4 {{ color: {accent_lighter}; margin-top: 12px; margin-bottom: 4px;
        font-size: 14px; }}
  table {{ border-collapse: collapse; margin: 6px 0 14px 0; width: 100%; }}
  th {{ background: {th_bg}; color: {th_text}; text-align: left;
       padding: 6px 10px; border: 1px solid {border}; font-weight: 600; }}
  td {{ padding: 6px 10px; border: 1px solid {border_light};
       vertical-align: top; }}
  tr:nth-child(even) td {{ background: {alt_row}; }}
  .key {{ color: {accent}; font-weight: 600; }}
  .retro {{ color: {retro}; font-weight: bold; }}
  .delta-pos {{ color: {delta_pos}; }}
  .delta-neg {{ color: {delta_neg}; }}
  .highlight {{ background: {highlight}; }}
  .panel {{ background: {panel_bg}; border-left: 4px solid {panel_border};
           padding: 10px 14px; margin: 10px 0; }}
  .small {{ color: {small}; font-size: 11px; }}
  .bs-date {{ color: {bs_date}; font-size: 11px; display: block; }}
  .footer {{ color: {footer}; font-style: italic; margin-top: 20px;
            border-top: 1px solid {border}; padding-top: 10px; }}
  .era {{ background: {era_bg}; border: 1px solid {era_border};
         border-radius: 6px; padding: 12px 16px; margin: 14px 0; }}
  .era h4 {{ margin-top: 0; }}
  .era p {{ margin: 6px 0; }}
  .planet-block {{ background: {block_bg}; border-left: 3px solid {accent_light};
                  padding: 10px 14px; margin: 10px 0; }}
  .placement-line {{ font-weight: 600; color: {accent}; margin-bottom: 4px; }}
  .edu {{ background: {edu_bg}; border-left: 4px solid {edu_border};
         padding: 10px 14px; margin: 10px 0; border-radius: 4px; }}
  .edu h4 {{ margin-top: 0; color: {accent}; }}
  .edu ul {{ margin: 6px 0; padding-left: 22px; }}
  .edu li {{ margin: 4px 0; }}
</style>
"""


def _css(theme_name: str) -> str:
    theme = get_theme(theme_name)
    return CSS_TEMPLATE.format(**theme["html"])


def _format_deg(deg: float) -> str:
    d = int(deg)
    m_full = (deg - d) * 60
    m = int(m_full)
    s = int((m_full - m) * 60)
    return f"{d:>2}°{m:02d}′{s:02d}″"


def _ad_with_bs(ad_date) -> str:
    ad_str = ad_date.strftime("%Y-%m-%d")
    try:
        y, m, d = calendar_bs.ad_to_bs(ad_date)
    except Exception:
        return ad_str
    bs_str = (f"{to_nepali_digits(y)}-{to_nepali_digits(f'{m:02d}')}-"
              f"{to_nepali_digits(f'{d:02d}')}")
    return f"{ad_str}<span class='bs-date'>वि.सं. {bs_str}</span>"


# ============================================================================
# EDUCATIONAL EXPLANATIONS — bilingual
# ============================================================================

EDU_KUNDALI = {
    "en": """
    <div class='edu'>
      <h4>What is a Janma Kundali?</h4>
      <p>The <b>Janma Kundali</b> ('birth chart') is a snapshot of the sky at
      the moment you were born, drawn as a square divided into 12 sections.
      Each section is a <b>house (bhava)</b> representing one area of life —
      self, money, siblings, home, children, and so on, all the way to losses.
      The North-Indian style chart used here is read like this:</p>
      <ul>
        <li>The cell at <b>top center</b> is always <b>House 1 (Lagna)</b> — the
            sign that was rising on the eastern horizon when you were born.</li>
        <li>From there, houses go <b>counterclockwise</b>: H2 is upper-left, H3
            left-upper, H4 left-center, and so on around to H12 upper-right.</li>
        <li>Each cell shows its <b>house number</b>, the <b>sign (rashi)</b>
            that occupies it, and any <b>planets</b> sitting there
            (Su=Sun, Mo=Moon, Ma=Mars, etc.).</li>
        <li>Planets sitting in a house powerfully shape that area of life.
            Planets <i>aspecting</i> a house from elsewhere also influence it
            (a more advanced reading).</li>
      </ul>
      <p><b>Most powerful houses</b>: 1, 4, 7, 10 (the four <i>kendras</i> /
      angles). <b>Most auspicious</b>: 5 and 9 (the <i>trikonas</i> / trines).
      <b>Most challenging</b>: 6, 8, 12 (the <i>dusthanas</i>).</p>
    </div>
    """,
    "ne": """
    <div class='edu'>
      <h4>जन्म कुण्डली के हो?</h4>
      <p><b>जन्म कुण्डली</b> भनेको तपाईं जन्मेको बेला आकाश कस्तो थियो
      भन्ने तस्बिर हो। यो एउटा वर्ग खाका हो, जसलाई १२ टुक्रामा बाँडिएको
      हुन्छ। हरेक टुक्रालाई <b>भाव</b> भनिन्छ — एउटा भावले जीवनको एउटा
      पाटो जनाउँछ (आफ्नो शरीर, धन, भाइबहिनी, घर, सन्तान, आदि)।
      उत्तर भारतीय शैलीको कुण्डली यसरी पढिन्छ:</p>
      <ul>
        <li>माथिको बीचमा रहेको कोठा सधैँ <b>पहिलो भाव (लग्न)</b> हो —
            तपाईं जन्मँदा पूर्वी क्षितिजमा उदाएको राशि।</li>
        <li>त्यहाँबाट <b>उल्टो (वामावर्त) दिशामा</b> भावहरू बढ्दै
            जान्छन्: २ नम्बर माथि-बायाँ, ३ बायाँ-माथिल्लो, ४ बायाँ बीच,
            र यसरी १२ नम्बरमा माथि-दायाँ पुग्छ।</li>
        <li>हरेक कोठाले देखाउँछ — <b>भाव नम्बर</b>, त्यस भावमा रहेको
            <b>राशि</b>, र त्यहाँ बसेका <b>ग्रहहरू</b>
            (Su=सूर्य, Mo=चन्द्र, Ma=मङ्गल, आदि)।</li>
        <li>एउटा भावमा बसेको ग्रहले त्यस जीवन-क्षेत्रलाई बलियोसँग
            प्रभाव पार्छ। टाढाका ग्रहहरूले पनि <i>दृष्टि</i>द्वारा
            असर गर्न सक्छन् (यो अलि अघिल्लो अध्ययन)।</li>
      </ul>
      <p><b>सबभन्दा बलिया भावहरू</b>: १, ४, ७, १० (केन्द्र भनिन्छ)।
      <b>सबभन्दा शुभ</b>: ५ र ९ (त्रिकोण)। <b>सबभन्दा कठिन</b>: ६, ८,
      १२ (दुस्थान)।</p>
    </div>
    """,
}


EDU_PANCHANGA = {
    "en": """
    <div class='edu'>
      <h4>What is the Panchanga?</h4>
      <p><b>Panchanga</b> means 'five limbs'. It is the Vedic way of
      describing the QUALITY of a moment in time, using five components:</p>
      <ul>
        <li><b>Tithi (lunar day)</b> — based on the angle between Moon and
            Sun. There are 30 tithis in a lunar month. Tithi 1 to 15 is the
            <i>Shukla paksha</i> (waxing); 16 to 30 is the <i>Krishna paksha</i>
            (waning). Tithi colors the day's emotional tone.</li>
        <li><b>Nakshatra</b> — which of the 27 lunar mansions the Moon is in
            right now. Each nakshatra has its own deity and theme.</li>
        <li><b>Yoga</b> — a sky-quality calculated from the combined
            longitude of Sun and Moon, divided into 27 named yogas (e.g.
            Brahma, Indra, Vishti). Affects auspiciousness for activities.</li>
        <li><b>Karana</b> — half a tithi (so 60 in a month, mapped to 11
            names). Used in fine-grained <i>muhurta</i> (timing) decisions.</li>
        <li><b>Vara</b> — the weekday, ruled by one of the 7 visible planets
            (Sun for Sunday, Moon for Monday, etc.).</li>
      </ul>
      <p>For a birth chart, panchanga tells us about the energetic flavor of
      the moment — used in choosing names, planning ceremonies, and reading
      personality nuances beyond just the planets.</p>
    </div>
    """,
    "ne": """
    <div class='edu'>
      <h4>पञ्चाङ्ग के हो?</h4>
      <p><b>पञ्चाङ्ग</b> को अर्थ हो ‘पाँच अङ्ग’। एउटा क्षणको
      ‘गुण’ कस्तो छ भनेर वैदिक परम्पराले पाँच कुराबाट हेर्छ:</p>
      <ul>
        <li><b>तिथि</b> — चन्द्र र सूर्यबीचको कोणबाट निस्किने चान्द्र
            दिन। एक चान्द्र महिनामा ३० तिथि हुन्छन्। तिथि १ देखि १५ सम्म
            <i>शुक्ल पक्ष</i> (बढ्दै जाने), १६ देखि ३० सम्म
            <i>कृष्ण पक्ष</i> (घट्दै जाने)। तिथिले दिनको भावनात्मक
            रङ्ग देखाउँछ।</li>
        <li><b>नक्षत्र</b> — चन्द्र अहिले कुन नक्षत्र (आकाशको २७
            तारापुञ्जमध्ये एक) मा छ। हरेक नक्षत्रको आफ्नै देवता र विषय
            छ।</li>
        <li><b>योग</b> — सूर्य र चन्द्रको देशान्तर जोडेर निकालिने
            आकाशीय गुण। २७ नाम छन् (जस्तै ब्रह्म, इन्द्र, विष्टि)।
            कुनै काम सुरु गर्न शुभ वा अशुभ बेला छुट्याउँछ।</li>
        <li><b>करण</b> — आधा तिथि (महिनाभरि ६० करण, ११ नामहरूमा बाँडिने)।
            <i>मुहूर्त</i> (शुभ बेला छान्ने काम)मा प्रयोग।</li>
        <li><b>वार</b> — हप्ताको दिन। हरेक वार एउटा ग्रहले चलाउँछ
            (आइतबार सूर्य, सोमबार चन्द्र, आदि)।</li>
      </ul>
      <p>जन्म कुण्डलीमा पञ्चाङ्गले त्यस क्षणको ऊर्जा-स्वाद बताउँछ —
      नामकरण, पूजा-अर्चना, मुहूर्त, र व्यक्तित्वको सूक्ष्म पाटो
      बुझ्न उपयोगी।</p>
    </div>
    """,
}


EDU_HOUSES = {
    "en": """
    <div class='edu'>
      <h4>The 12 Houses (Bhavas) — what they cover</h4>
      <p>Every house is a department of life. Whichever planets sit in a
      house — and whichever sign occupies it — color what happens in that
      department. Quick map:</p>
      <ul>
        <li><b>1 — Tanu</b>: body, personality, vitality, overall direction.</li>
        <li><b>2 — Dhana</b>: wealth, family, speech, food, the close family.</li>
        <li><b>3 — Sahaja</b>: siblings, courage, short trips, communication.</li>
        <li><b>4 — Sukha</b>: mother, home, comfort, education, vehicles.</li>
        <li><b>5 — Putra</b>: children, intellect, creativity, romance, past-life merit.</li>
        <li><b>6 — Ari</b>: enemies, illness, debts, daily work, obstacles, service.</li>
        <li><b>7 — Yuvati</b>: spouse, partnerships, business, public dealings.</li>
        <li><b>8 — Ayu</b>: longevity, hidden things, transformations, inheritance.</li>
        <li><b>9 — Dharma</b>: father, fortune, higher learning, religion, long journeys.</li>
        <li><b>10 — Karma</b>: career, public role, status, reputation.</li>
        <li><b>11 — Labha</b>: gains, friendships, hopes, elder siblings, networks.</li>
        <li><b>12 — Vyaya</b>: losses, expenses, foreign lands, sleep, liberation.</li>
      </ul>
      <p><b>How to read a house</b>: look at (1) the sign in it, (2) the
      planets sitting in it, (3) the planet that <i>rules</i> the sign in it
      and where THAT planet sits. A strong house lord placed in another
      strong house brings good results to both.</p>
    </div>
    """,
    "ne": """
    <div class='edu'>
      <h4>१२ भाव — कुन भावले के बुझाउँछ</h4>
      <p>हरेक भाव जीवनको एउटा क्षेत्र हो। त्यस भावमा बसेको ग्रह र
      त्यहाँको राशिले त्यस क्षेत्रलाई रङ्गिन्छ। द्रुत नक्शा:</p>
      <ul>
        <li><b>१ — तनु</b>: शरीर, स्वभाव, ओज, जीवनको समग्र दिशा।</li>
        <li><b>२ — धन</b>: सम्पत्ति, परिवार (नजिकको), वाणी, खानेकुरा।</li>
        <li><b>३ — सहज</b>: भाइबहिनी, साहस, छोटा यात्रा, सञ्चार।</li>
        <li><b>४ — सुख</b>: आमा, घर, सुख-सुविधा, शिक्षा, सवारी।</li>
        <li><b>५ — पुत्र</b>: सन्तान, बुद्धि, सिर्जना, प्रेम, पूर्व
            जन्मको पुण्य।</li>
        <li><b>६ — अरि</b>: शत्रु, रोग, ऋण, दैनिक काम, बाधा, सेवा।</li>
        <li><b>७ — युवती</b>: जीवनसाथी, साझेदारी, व्यापार, सार्वजनिक
            सम्बन्ध।</li>
        <li><b>८ — आयु</b>: उमेर, गुप्त कुरा, ठूलो परिवर्तन, उत्तराधिकार।</li>
        <li><b>९ — धर्म</b>: बुबा, भाग्य, उच्च शिक्षा, धर्म, लामो यात्रा।</li>
        <li><b>१० — कर्म</b>: करियर, सार्वजनिक भूमिका, प्रतिष्ठा।</li>
        <li><b>११ — लाभ</b>: फाइदा, मित्र, आशा, दाजुदिदी, सम्पर्क-वृत्त।</li>
        <li><b>१२ — व्यय</b>: हानि, खर्च, विदेश, निद्रा, मोक्ष।</li>
      </ul>
      <p><b>कसरी पढ्ने</b>: भाव हेर्दा (१) त्यसमा रहेको राशि, (२) त्यहाँ
      बसेका ग्रह, (३) त्यस राशिको <i>स्वामी</i> ग्रह कहाँ बसेको छ —
      यी तीन कुरा हेरिन्छ। बलियो भाव-स्वामी अर्को बलियो भावमा बसेमा
      दुवै भावमा शुभ फल।</p>
    </div>
    """,
}


def _edu(key_dict: dict, locale: str) -> str:
    return key_dict.get(locale, key_dict["en"])


# ============================================================================
# SUMMARY TAB
# ============================================================================

def render_summary(result, t: T, theme: str = "light") -> str:
    bs_y, bs_m, bs_d = result.bs_date
    ne_dev, ne_en = NEPALI_MONTHS[bs_m - 1]
    bs_str_dev = (
        f"{to_nepali_digits(bs_y)} {ne_dev} {to_nepali_digits(bs_d)}"
    )
    bs_str_en = f"{bs_y} {ne_en} {bs_d}"

    ad_str = result.birth_local.strftime("%Y-%m-%d %H:%M")
    moon = result.drik_positions["Moon"]
    sun = result.drik_positions["Sun"]
    nak_dev, nak_en = NAKSHATRAS[moon.nakshatra]

    cur = ""
    if result.current_dasha:
        cur = (
            f"<tr><td class='key'>{t['label_current_dasha']}</td>"
            f"<td>{planet_label(result.current_dasha.lord)} "
            f"({result.current_dasha.start.strftime('%Y-%m-%d')} → "
            f"{result.current_dasha.end.strftime('%Y-%m-%d')})</td></tr>"
        )

    return _css(theme) + f"""
    <h2>{t['section_birth']}</h2>
    <table>
      <tr><td class='key'>{t['label_name']}</td>
          <td>{result.name or '—'}</td></tr>
      <tr><td class='key'>{t['label_ad_date']}</td>
          <td>{ad_str} (UTC{result.tz_offset_hours:+.2f})</td></tr>
      <tr><td class='key'>{t['label_bs_date']}</td>
          <td>{bs_str_dev} &nbsp; ({bs_str_en})</td></tr>
      <tr><td class='key'>{t['label_place']}</td>
          <td>{result.place_name} ({result.latitude:.4f}°,
          {result.longitude:.4f}°E)</td></tr>
      <tr><td class='key'>{t['label_vara']}</td>
          <td>{vara_label(result.weekday_sun0)}</td></tr>
      <tr><td class='key'>{t['label_ayanamsa']}</td>
          <td>{result.ayanamsa_lahiri:.4f}°</td></tr>
    </table>

    <h2>{t['section_lagna']}</h2>
    <div class='panel'>
      <b>{t['label_lagna']}:</b> {rashi_label(result.drik_lagna_rashi)} —
      {_format_deg(result.drik_lagna_deg)}
    </div>

    <h3>{t['label_moon_sign']}</h3>
    <div class='panel'>{rashi_label(moon.rashi)} —
        {RASHI_TRAITS[RASHIS[moon.rashi][2]]}</div>

    <h3>{t['label_sun_sign']}</h3>
    <div class='panel'>{rashi_label(sun.rashi)} —
        {RASHI_TRAITS[RASHIS[sun.rashi][2]]}</div>

    <h3>{t['label_nakshatra']}</h3>
    <div class='panel'>{nak_dev} / {nak_en} — pada {moon.nakshatra_pada}<br>
       <span class='small'>{NAKSHATRA_THEMES.get(nak_en, '')}</span></div>

    <table>{cur}</table>
    """


# ============================================================================
# DRIK TAB — chart + panchanga + houses, each with educational explainer
# ============================================================================

def _planet_table(positions: dict, t: T, dignities: dict | None = None) -> str:
    rows = []
    order = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus",
             "Saturn", "Rahu", "Ketu"]
    show_dign = dignities is not None
    dign_labels = DIGNITY_LABEL_NE if t.locale == "ne" else DIGNITY_LABEL_EN
    for name in order:
        if name not in positions:
            continue
        p = positions[name]
        retro = ("<span class='retro'>℞</span>"
                 if getattr(p, "retrograde", False) else "")
        dign_cell = ""
        if show_dign:
            d = dignities.get(name, "Neutral")
            label = dign_labels.get(d, d)
            cls = ""
            if d == "Exalted":     cls = " style='color:#2e7d32;font-weight:600'"
            elif d == "Debilitated": cls = " style='color:#c62828;font-weight:600'"
            elif d in ("Own", "Mooltrikona"): cls = " style='color:#1565c0;font-weight:600'"
            dign_cell = f"<td{cls}>{label}</td>"
        rows.append(
            f"<tr><td>{planet_label(name)}</td>"
            f"<td>{rashi_label(p.rashi)}</td>"
            f"<td>{_format_deg(p.deg_in_rashi)}</td>"
            f"<td>{nakshatra_label(p.nakshatra)}</td>"
            f"<td>{p.nakshatra_pada}</td>"
            f"<td>{retro}</td>"
            f"{dign_cell}</tr>"
        )
    body = "".join(rows)
    dign_header = f"<th>{('दशा' if t.locale == 'ne' else 'Dignity')}</th>" if show_dign else ""
    return f"""
    <table>
      <tr><th>{t['col_planet']}</th><th>{t['col_sign']}</th>
          <th>{t['col_position']}</th><th>{t['col_nakshatra']}</th>
          <th>{t['col_pada']}</th><th>{t['col_retro']}</th>
          {dign_header}</tr>
      {body}
    </table>
    """


def _panchanga_block(p, t: T) -> str:
    return f"""
    <table>
      <tr><th>{t['col_planet']}</th><th>{t['col_sign']}</th></tr>
      <tr><td class='key'>Tithi / तिथि</td>
          <td>{tithi_label(p.tithi_in_paksha, p.paksha)}</td></tr>
      <tr><td class='key'>{t['col_nakshatra']}</td>
          <td>{nakshatra_label(p.nakshatra)} (pada {p.nakshatra_pada})</td></tr>
      <tr><td class='key'>Yoga / योग</td><td>{yoga_label(p.yoga)}</td></tr>
      <tr><td class='key'>Karana / करण</td><td>{karana_label(p.karana)}</td></tr>
      <tr><td class='key'>{t['label_vara']}</td><td>{vara_label(p.vara)}</td></tr>
    </table>
    """


def _houses_table(lagna_rashi: int, planets_in_house: dict, t: T) -> str:
    rows = []
    for h in range(1, 13):
        rashi = (lagna_rashi + h - 1) % 12
        planets = planets_in_house.get(h, [])
        plist = ", ".join(planet_label(p) for p in planets) if planets else "—"
        marker = " (Lagna)" if h == 1 else ""
        cls = " class='highlight'" if h == 1 else ""
        rows.append(
            f"<tr{cls}><td>{h}{marker}</td>"
            f"<td>{rashi_label(rashi)}</td><td>{plist}</td></tr>"
        )
    return f"""
    <table>
      <tr><th>{t['col_house']}</th><th>{t['col_sign']}</th>
          <th>{t['col_planets']}</th></tr>
      {''.join(rows)}
    </table>
    """


def render_drik(result, t: T, theme: str = "light", chart_mode: str = "auto") -> str:
    asc_long = result.drik_lagna_long
    asc_rashi = result.drik_lagna_rashi
    asc_deg = result.drik_lagna_deg
    chart_html = render_chart.chart_html(
        asc_rashi, result.drik_planets_in_house, mode=chart_mode,
    )

    abbr_legend = (
        "Su=Sun, Mo=Moon, Ma=Mars, Me=Mercury, Ju=Jupiter, "
        "Ve=Venus, Sa=Saturn, Ra=Rahu, Ke=Ketu"
        if t.locale == "en" else
        "Su=सूर्य, Mo=चन्द्र, Ma=मङ्गल, Me=बुध, Ju=बृहस्पति, "
        "Ve=शुक्र, Sa=शनि, Ra=राहु, Ke=केतु"
    )

    return _css(theme) + f"""
    <h2>{t['section_chart']}</h2>
    {_edu(EDU_KUNDALI, t.locale)}
    {chart_html}
    <p class='small' style='text-align:center;'>{abbr_legend}</p>

    <h2>{t['section_planets']} — Drik (Lahiri)</h2>
    {_planet_table(result.drik_positions, t, result.drik_dignities)}

    <h2>{t['section_lagna']}</h2>
    <div class='panel'>{rashi_label(asc_rashi)} — {_format_deg(asc_deg)}
        &nbsp; <span class='small'>(absolute {asc_long:.4f}°)</span></div>

    <h2>{t['section_panchanga']}</h2>
    {_edu(EDU_PANCHANGA, t.locale)}
    {_panchanga_block(result.drik_panchanga, t)}

    <h2>{t['section_houses']}</h2>
    {_edu(EDU_HOUSES, t.locale)}
    {_houses_table(asc_rashi, result.drik_planets_in_house, t)}
    """


# ============================================================================
# SS TAB / COMPARE TAB
# ============================================================================

def render_ss(result, t: T, theme: str = "light") -> str:
    if result.ss_positions is None:
        return _css(theme) + "<p>Surya Siddhanta not computed.</p>"
    return _css(theme) + f"""
    <h2>{t['section_planets']} — Surya Siddhanta</h2>
    {_planet_table(result.ss_positions, t)}
    <h2>{t['section_panchanga']} — Surya Siddhanta</h2>
    {_panchanga_block(result.ss_panchanga, t)}
    <p class='small'>Surya Siddhanta is intrinsically sidereal (nirayana) —
       no ayanamsa applied.</p>
    """


def render_compare(result, t: T, theme: str = "light") -> str:
    if result.ss_positions is None:
        return _css(theme) + "<p>Run with Surya Siddhanta enabled to compare.</p>"
    rows = []
    order = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus",
             "Saturn", "Rahu", "Ketu"]
    for name in order:
        if name not in result.drik_positions or name not in result.ss_positions:
            continue
        d = result.drik_positions[name].longitude
        s = result.ss_positions[name].longitude
        delta = (d - s + 540) % 360 - 180
        cls = "delta-pos" if delta >= 0 else "delta-neg"
        rows.append(
            f"<tr><td>{planet_label(name)}</td>"
            f"<td>{d:.4f}°</td><td>{s:.4f}°</td>"
            f"<td class='{cls}'>{delta:+.3f}°</td></tr>"
        )
    return _css(theme) + f"""
    <h2>Drik vs Surya Siddhanta — Sidereal Longitudes</h2>
    <table>
      <tr><th>{t['col_planet']}</th><th>{t['col_drik']}</th>
          <th>{t['col_ss']}</th><th>{t['col_delta']}</th></tr>
      {''.join(rows)}
    </table>
    <p class='small'>Δ = Drik longitude − SS longitude. Positive means SS lags
       behind Drik. Mars and Mercury typically show the largest divergence
       (~10–20°), reflecting the limits of the classical model.</p>
    """


# ============================================================================
# DASHA TAB
# ============================================================================

EDU_DASHA = {
    "en": """
    <div class='edu'>
      <h4>What is the Vimshottari Dasha?</h4>
      <p>Vimshottari is a 120-year cycle of <b>nine planetary periods</b>
      called <i>Mahadashas</i>. The fixed order is: Ketu → Venus → Sun →
      Moon → Mars → Rahu → Jupiter → Saturn → Mercury, with periods of 7,
      20, 6, 10, 7, 18, 16, 19, and 17 years respectively (= 120 total).</p>
      <p>Which Mahadasha you are born INTO depends on the Moon's nakshatra at
      birth. The first Mahadasha is partial — only the unspent fraction of
      the nakshatra's lord. After that, the cycle proceeds in fixed order.</p>
      <p>Each Mahadasha colors that stretch of life with its lord's themes.
      Below the table you will find a detailed reading of every Mahadasha you
      will pass through — a full 120 years of guidance to learn from.</p>
    </div>
    """,
    "ne": """
    <div class='edu'>
      <h4>विंशोत्तरी दशा के हो?</h4>
      <p>विंशोत्तरी १२० वर्षको चक्र हो — नौ ग्रहीय अवधि (<i>महादशा</i>)
      हरूको। यिनको क्रम तय छ: केतु → शुक्र → सूर्य → चन्द्र → मङ्गल → राहु
      → बृहस्पति → शनि → बुध। अवधि क्रमशः ७, २०, ६, १०, ७, १८, १६, १९, र
      १७ वर्ष — जोड्दा १२० वर्ष।</p>
      <p>जन्ममा कुन महादशा सुरु हुन्छ — त्यो जन्म नक्षत्रले तय गर्छ।
      पहिलो महादशा अधुरो हुन्छ — त्यस नक्षत्रको स्वामीको समय जति बाँकी छ
      त्यतिकै। त्यसपछि क्रम तय छ।</p>
      <p>हरेक महादशाले त्यस अवधिको जीवनलाई आफ्नो स्वामीको गुणले रङ्ग्याउँछ।
      तालिकाको तल — तपाईंको जीवनभर आउने हरेक महादशाको विस्तृत व्याख्या —
      सिक्न सजिलो हुने गरी राखिएको छ।</p>
    </div>
    """,
}


def render_dasha(result, t: T, theme: str = "light") -> str:
    rows = []
    for d in result.dashas:
        years = (d.end - d.start).days / 365.25
        is_cur = (result.current_dasha is not None
                  and d.start == result.current_dasha.start)
        cls = " class='highlight'" if is_cur else ""
        marker = (" ◀ " + ("current" if t.locale == "en" else "हाल")
                  if is_cur else "")
        rows.append(
            f"<tr{cls}><td>{planet_label(d.lord)}{marker}</td>"
            f"<td>{_ad_with_bs(d.start.date())}</td>"
            f"<td>{_ad_with_bs(d.end.date())}</td>"
            f"<td>{years:.2f}</td></tr>"
        )

    education_header = (
        "What each Mahadasha typically brings"
        if t.locale == "en"
        else "हरेक महादशामा प्रायः के–के हुन्छ"
    )

    education_blocks = []
    for d in result.dashas:
        notes = mahadasha_notes(d.lord, t.locale)
        if not notes:
            continue
        years = (d.end - d.start).days / 365.25
        period_str = (
            f"{d.start.strftime('%Y-%m-%d')} → {d.end.strftime('%Y-%m-%d')} "
            f"(~{years:.1f} {'years' if t.locale == 'en' else 'वर्ष'})"
        )
        labels = (
            ("Overview", "Career & finance", "Relationships", "Health",
             "Mind & psychology", "Tip for reading")
            if t.locale == "en"
            else ("समग्र दृष्टि", "करियर र पैसा", "सम्बन्ध", "स्वास्थ्य",
                  "मन र मनोविज्ञान", "पढ्ने टिप्स")
        )
        keys = ("overview", "career", "relationships", "health",
                "psychology", "tip")

        sections_html = []
        for label, key in zip(labels, keys):
            sections_html.append(
                f"<h4>{label}</h4><p>{notes.get(key, '')}</p>"
            )

        education_blocks.append(
            f"<div class='era'>"
            f"<h3>{notes['headline']}</h3>"
            f"<p class='small'>{period_str}</p>"
            + "".join(sections_html)
            + "</div>"
        )

    return _css(theme) + f"""
    <h2>{t['section_dasha']}</h2>
    {_edu(EDU_DASHA, t.locale)}
    <table>
      <tr><th>{t['col_lord']}</th><th>{t['col_start']}</th>
          <th>{t['col_end']}</th><th>{t['col_years']}</th></tr>
      {''.join(rows)}
    </table>

    <h2>{education_header}</h2>
    {''.join(education_blocks)}
    """


# ============================================================================
# EXPLANATION TAB
# ============================================================================

def render_explanation(result, t: T, theme: str = "light") -> str:
    if t.locale == "ne":
        return _explanation_ne(result, theme)
    return _explanation_en(result, theme)


def _explanation_en(result, theme: str) -> str:
    moon = result.drik_positions["Moon"]
    sun = result.drik_positions["Sun"]
    lagna_en = RASHIS[result.drik_lagna_rashi][2]
    moon_en = RASHIS[moon.rashi][2]
    sun_en = RASHIS[sun.rashi][2]
    nak_en = NAKSHATRAS[moon.nakshatra][1]

    placements = []
    for planet in ("Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus",
                   "Saturn", "Rahu", "Ketu"):
        hp = result.drik_chart.get(planet)
        if hp is None:
            continue
        h_label, h_meaning = HOUSE_MEANINGS[hp.house]
        rashi_en_p = RASHIS[hp.rashi][2]
        placements.append(f"""
        <div class='planet-block'>
          <div class='placement-line'>
            {planet} in House {hp.house} ({h_label}) — sign {rashi_en_p}
          </div>
          <p>{planet_psychology(planet, 'en')}</p>
          <p><b>For this birth:</b> {planet}'s placement in House {hp.house}
          ({h_meaning}) shapes those areas of life through {planet}'s nature
          ({PLANET_MEANINGS[planet]}). The sign {rashi_en_p}
          ({RASHI_TRAITS[rashi_en_p]}) colors HOW {planet} expresses itself
          here.</p>
        </div>
        """)

    cur_block = ""
    if result.current_dasha:
        cd = result.current_dasha
        cd_notes = mahadasha_notes(cd.lord, "en")
        years_left = (cd.end - cd.start).days / 365.25
        cur_block = f"""
        <h3>Current Dasha — {cd.lord}</h3>
        <p>You are currently in the <b>{cd.lord} Mahadasha</b>, running until
        <b>{cd.end.strftime('%Y-%m-%d')}</b> (~{years_left:.1f} years total).
        See the <i>Dasha</i> tab for the full era reading. In short:
        {cd_notes.get('overview', '')}</p>
        """

    return _css(theme) + f"""
    <h2>Kundali in Plain Language — for {result.name or 'this person'}</h2>

    <h3>What is a Kundali?</h3>
    <p>A <b>Kundali</b> (कुण्डली) is a snapshot of the sky at the moment you
    were born. Vedic astrology divides the sky into 12 <i>rashis</i>
    (zodiac signs) and 27 <i>nakshatras</i> (lunar mansions), and tracks the
    Sun, Moon, the five visible planets, and the two lunar nodes Rahu &amp;
    Ketu. From your date / time / place of birth, we calculate where each one
    was and place them into 12 <i>bhavas</i> (houses), each representing a
    different area of life.</p>

    <h3>Three Anchors of the Chart</h3>
    <p>Most readings start by understanding three things:</p>
    <ul>
      <li><b>Lagna (Ascendant) — {lagna_en}</b>: how you APPEAR; how you meet
          new situations. Yours is {lagna_en} — {RASHI_TRAITS[lagna_en]}.</li>
      <li><b>Janma Rashi / Moon sign — {moon_en}</b>: your INNER emotional
          world. Yours is {moon_en} — {RASHI_TRAITS[moon_en]}.</li>
      <li><b>Surya Rashi / Sun sign — {sun_en}</b>: your CORE identity / soul
          purpose. Yours is {sun_en} — {RASHI_TRAITS[sun_en]}.
          <span class='small'>(This is the sidereal Sun sign — typically one
          sign earlier than the tropical sign in Western horoscopes.)</span></li>
    </ul>

    <h3>Janma Nakshatra — {nak_en}</h3>
    <p>The 27 nakshatras are a finer classification of the sky than the 12
    rashis. Yours is <b>{nak_en}</b>: {NAKSHATRA_THEMES.get(nak_en, '')}.
    The nakshatra also fixes the starting Mahadasha — see the Dasha tab.</p>

    <h3>What Each Planet Says — and Where It Lands in Your Life</h3>
    <p>For each planet, the first paragraph below gives the GENERAL
    psychological signature; the second is specific to its placement in your
    chart.</p>
    {''.join(placements)}

    {cur_block}

    <p class='footer'>A Kundali is a map, not a verdict. Classical texts treat
    it as a guide to tendencies and timings — the choices within those
    tendencies are still yours.</p>
    """


def _explanation_ne(result, theme: str) -> str:
    moon = result.drik_positions["Moon"]
    sun = result.drik_positions["Sun"]
    lagna_dev = RASHIS[result.drik_lagna_rashi][0]
    moon_dev = RASHIS[moon.rashi][0]
    sun_dev = RASHIS[sun.rashi][0]
    nak_dev = NAKSHATRAS[moon.nakshatra][0]
    lagna_en = RASHIS[result.drik_lagna_rashi][2]
    moon_en = RASHIS[moon.rashi][2]
    sun_en = RASHIS[sun.rashi][2]

    placements = []
    for planet in ("Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus",
                   "Saturn", "Rahu", "Ketu"):
        hp = result.drik_chart.get(planet)
        if hp is None:
            continue
        rashi_dev_p = RASHIS[hp.rashi][0]
        h_label_full = HOUSE_MEANINGS[hp.house][0]
        placements.append(f"""
        <div class='planet-block'>
          <div class='placement-line'>
            {planet_label(planet)} — भाव {hp.house} ({h_label_full}),
            राशि {rashi_dev_p}
          </div>
          <p>{planet_psychology(planet, 'ne')}</p>
        </div>
        """)

    cur_block = ""
    if result.current_dasha:
        cd = result.current_dasha
        cd_notes = mahadasha_notes(cd.lord, "ne")
        cur_block = f"""
        <h3>हालको दशा — {planet_label(cd.lord)}</h3>
        <p>तपाईं अहिले <b>{planet_label(cd.lord)} महादशा</b>मा हुनुहुन्छ —
        <b>{cd.end.strftime('%Y-%m-%d')}</b> सम्म चल्ने।
        विस्तृत व्याख्याका लागि <i>दशा</i> ट्याबमा हेर्नुहोस्। संक्षेपमा:
        {cd_notes.get('overview', '')}</p>
        """

    return _css(theme) + f"""
    <h2>{result.name or 'यो व्यक्ति'}को कुण्डली — सरल भाषामा</h2>

    <h3>कुण्डली के हो?</h3>
    <p><b>कुण्डली</b> भनेको तपाईं जन्मेको बेला आकाश कस्तो थियो भन्ने
    तस्बिर हो। वैदिक ज्योतिषले आकाशलाई १२ <i>राशि</i> र २७ <i>नक्षत्र</i>मा
    बाँडेर हेर्छ — र सूर्य, चन्द्र, पाँच आँखाले देखिने ग्रह, अनि चन्द्रको
    दुई पात (राहु–केतु) कहाँ छन् भनेर पत्ता लगाउँछ। तपाईंको जन्म मिति,
    समय, र ठाउँबाट यी सबैको स्थान निकालिन्छ — अनि १२ <i>भाव</i>मा राख्दा
    जीवनका १२ क्षेत्र देखिन्छन्।</p>

    <h3>कुण्डली पढ्ने तीन मुख्य आधार</h3>
    <p>कुण्डली अध्ययन सुरु गर्दा प्रायः यी तीन कुरा पहिले हेरिन्छ:</p>
    <ul>
      <li><b>लग्न — {lagna_dev} ({lagna_en})</b>: तपाईं बाहिर कस्तो
          देखिनुहुन्छ; नयाँ ठाउँमा कस्तो प्रतिक्रिया दिनुहुन्छ। तपाईंको
          लग्न {lagna_dev} — {RASHI_TRAITS[lagna_en]}।</li>
      <li><b>जन्म राशि / चन्द्र राशि — {moon_dev} ({moon_en})</b>:
          तपाईंको भित्री मन र भावनात्मक संसार। तपाईंको चन्द्र राशि
          {moon_dev} — {RASHI_TRAITS[moon_en]}।</li>
      <li><b>सूर्य राशि — {sun_dev} ({sun_en})</b>: तपाईंको आत्मा र
          जीवनको मूल उद्देश्य। तपाईंको सूर्य राशि {sun_dev} —
          {RASHI_TRAITS[sun_en]}।
          <span class='small'>(यो निरयन सूर्य राशि हो — पाश्चात्य
          ज्योतिषमा देखिने सायन राशिभन्दा प्रायः एक राशि अघिको।)</span></li>
    </ul>

    <h3>जन्म नक्षत्र — {nak_dev}</h3>
    <p>नक्षत्र भनेको आकाशको २७ टुक्रा हुन् — राशिभन्दा सानो र सूक्ष्म।
    तपाईंको जन्म नक्षत्र <b>{nak_dev}</b> हो। नक्षत्रले तपाईंको
    विंशोत्तरी महादशाको सुरु पनि तय गर्छ — विस्तार लागि
    <i>दशा</i> ट्याबमा हेर्नुहोस्।</p>

    <h3>हरेक ग्रहको कुरा — र तपाईंको जीवनमा कहाँ छ</h3>
    <p>तलका हरेक ग्रहको खण्डमा त्यस ग्रहको <b>सामान्य स्वभाव</b> (सबैका
    लागि लागू) र तपाईंको कुण्डलीमा त्यो <b>कुन भाव र राशिमा छ</b> भन्ने
    दुवै कुरा छ।</p>
    {''.join(placements)}

    {cur_block}

    <p class='footer'>कुण्डली जीवनको नक्शा हो, अन्तिम निर्णय होइन।
    शास्त्रहरूले यसलाई प्रवृत्ति र समयको मार्गदर्शक मान्छन् —
    निर्णयचाहिँ तपाईंकै हुन्छ।</p>
    """


# ============================================================================
# D9 NAVAMSHA TAB
# ============================================================================

EDU_D9 = {
    "en": """
    <div class='edu'>
      <h4>What is the D9 Navamsha?</h4>
      <p>Each rashi (30°) is divided into 9 equal parts of 3°20'. The
      <b>Navamsha</b> chart (D9) shows where each planet sits in this finer
      classification. Classical use: marriage and partnership analysis;
      a planet's <i>inner strength</i> (D9 dignity often matters more than
      D1 dignity in some readings); the trajectory of dharma/destiny.</p>
      <p><b>Vargottama</b>: when a planet sits in the SAME rashi in both D1
      and D9, it is "Vargottama" — strong, focused, consistent in its results.</p>
      <p><b>Navamsha Lagna</b>: the rashi rising in the D9 chart; it gives
      a complementary reading to the natal Lagna, especially around marriage
      and dharmic direction.</p>
    </div>
    """,
    "ne": """
    <div class='edu'>
      <h4>D9 नवांश के हो?</h4>
      <p>हरेक राशि (३०°) लाई ९ बराबर भागमा (३°२०′ प्रत्येक) बाँडिन्छ।
      <b>नवांश</b> कुण्डली (D9) ले हरेक ग्रह यस सूक्ष्म वर्गीकरणमा कहाँ
      छ देखाउँछ। शास्त्रीय प्रयोग: विवाह र साझेदारीको अध्ययन; ग्रहको
      <i>भित्री बल</i> (D9 दशा कतिपय पठनमा D1 भन्दा बढी महत्त्वपूर्ण);
      धर्म/भाग्यको यात्रा।</p>
      <p><b>वर्गोत्तम</b>: ग्रह D1 र D9 दुवैमा एउटै राशिमा छ भने त्यो
      ‘वर्गोत्तम’ हो — बलियो, एकाग्र, सुसंगत फल।</p>
      <p><b>नवांश लग्न</b>: D9 कुण्डलीमा उदाएको राशि — विवाह र धार्मिक
      दिशाको पूरक पठन दिन्छ।</p>
    </div>
    """,
}


def _d9_planet_table(d9_result, vargottama: list[str], t: T) -> str:
    rows = []
    order = ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus",
             "Saturn", "Rahu", "Ketu"]
    for name in order:
        if name not in d9_result.planet_rashis:
            continue
        rashi = d9_result.planet_rashis[name]
        house = ((rashi - d9_result.lagna_rashi) % 12) + 1
        var_marker = ""
        if name in vargottama:
            tag = "वर्गोत्तम" if t.locale == "ne" else "Vargottama"
            var_marker = f" <span style='color:#2e7d32;font-weight:600'>★ {tag}</span>"
        rows.append(
            f"<tr><td>{planet_label(name)}{var_marker}</td>"
            f"<td>{rashi_label(rashi)}</td>"
            f"<td>{house}</td></tr>"
        )
    head_h = "भाव" if t.locale == "ne" else "House"
    return f"""
    <table>
      <tr><th>{t['col_planet']}</th><th>{t['col_sign']}</th>
          <th>{head_h}</th></tr>
      {''.join(rows)}
    </table>
    """


def render_d9(result, t: T, theme: str = "light", chart_mode: str = "auto") -> str:
    if result.d9 is None:
        return _css(theme) + "<p>D9 not computed.</p>"
    chart_html = render_chart.chart_html(
        result.d9.lagna_rashi, result.d9.planets_in_house, mode=chart_mode,
    )
    abbr_legend = (
        "Su=Sun, Mo=Moon, Ma=Mars, Me=Mercury, Ju=Jupiter, Ve=Venus, "
        "Sa=Saturn, Ra=Rahu, Ke=Ketu"
        if t.locale == "en" else
        "Su=सूर्य, Mo=चन्द्र, Ma=मङ्गल, Me=बुध, Ju=बृहस्पति, Ve=शुक्र, "
        "Sa=शनि, Ra=राहु, Ke=केतु"
    )
    title = "नवांश कुण्डली (D9)" if t.locale == "ne" else "Navamsha Chart (D9)"
    nlagna_label = "नवांश लग्न" if t.locale == "ne" else "Navamsha Lagna"
    plan_title = "नवांश ग्रह स्थिति" if t.locale == "ne" else "Planet positions in D9"
    return _css(theme) + f"""
    <h2>{title}</h2>
    {_edu(EDU_D9, t.locale)}
    <div class='panel'>
      <b>{nlagna_label}:</b> {rashi_label(result.d9.lagna_rashi)}
    </div>
    {chart_html}
    <p class='small' style='text-align:center;'>{abbr_legend}</p>
    <h3>{plan_title}</h3>
    {_d9_planet_table(result.d9, result.vargottama, t)}
    """


# ============================================================================
# ANTARDASHA TAB
# ============================================================================

EDU_ANTAR = {
    "en": """
    <div class='edu'>
      <h4>Antardasha — sub-periods inside a Mahadasha</h4>
      <p>Each Mahadasha is divided into 9 <b>Antardashas</b> (also called
      Bhuktis). The order starts with the Mahadasha's own lord, then proceeds
      through the standard Vimshottari sequence. Duration of each antardasha:
      (mahadasha_years × antar_lord_years) ÷ 120.</p>
      <p>Antardashas explain the FLAVOR of months/years inside a long
      planetary period. Example: in a Jupiter Mahadasha (16 yrs), the
      Jupiter–Saturn antardasha (≈ 2.5 yrs) brings serious, consolidating
      themes within Jupiter's expansive period.</p>
    </div>
    """,
    "ne": """
    <div class='edu'>
      <h4>अन्तरदशा — महादशाभित्रको उप-अवधि</h4>
      <p>हरेक महादशालाई ९ <b>अन्तरदशा</b> (भुक्ति पनि भनिन्छ) मा बाँडिन्छ।
      क्रम महादशाकै स्वामीबाट सुरु हुन्छ, अनि विंशोत्तरीको मानक क्रममा।
      हरेकको अवधि: (महादशा_वर्ष × अन्तर_स्वामी_वर्ष) ÷ १२०।</p>
      <p>अन्तरदशाले लामो ग्रहीय अवधिभित्रका महिना/वर्षको स्वाद बुझाउँछ।
      उदाहरण: १६ वर्षको गुरु महादशामा, गुरु–शनि अन्तरदशा (≈ २.५ वर्ष) ले
      गुरुको विस्तारशील समयभित्र पनि गम्भीर र दृढीकरणका विषय ल्याउँछ।</p>
    </div>
    """,
}


def _antardasha_table(antars, current_antar, t: T) -> str:
    rows = []
    for a in antars:
        years = (a.end - a.start).days / 365.25
        is_cur = (current_antar is not None
                  and a.start == current_antar.start
                  and a.antar_lord == current_antar.antar_lord)
        cls = " class='highlight'" if is_cur else ""
        marker = (" ◀ " + ("current" if t.locale == "en" else "हाल")
                  if is_cur else "")
        rows.append(
            f"<tr{cls}><td>{planet_label(a.antar_lord)}{marker}</td>"
            f"<td>{_ad_with_bs(a.start.date())}</td>"
            f"<td>{_ad_with_bs(a.end.date())}</td>"
            f"<td>{years:.2f}</td></tr>"
        )
    return f"""
    <table>
      <tr><th>{t['col_lord']}</th><th>{t['col_start']}</th>
          <th>{t['col_end']}</th><th>{t['col_years']}</th></tr>
      {''.join(rows)}
    </table>
    """


def render_antardasha(result, t: T, theme: str = "light") -> str:
    title = "अन्तरदशा" if t.locale == "ne" else "Antardasha (Sub-periods)"
    cur_md = result.current_dasha
    if not result.dashas or cur_md is None:
        return _css(theme) + (
            f"<h2>{title}</h2>"
            f"<p>{'चालू महादशा फेला परेन।' if t.locale=='ne' else 'No active Mahadasha found.'}</p>"
        )

    cur_md_title = "हालको महादशा भित्र" if t.locale == "ne" else "Inside the current Mahadasha"
    next_md_title = "अर्को महादशा भित्र" if t.locale == "ne" else "Inside the next Mahadasha"

    blocks = []
    cur_antars = dasha_mod.antardashas_for(cur_md)
    blocks.append(
        f"<h3>{cur_md_title} — {planet_label(cur_md.lord)} "
        f"({cur_md.start.strftime('%Y-%m-%d')} → "
        f"{cur_md.end.strftime('%Y-%m-%d')})</h3>"
    )
    blocks.append(_antardasha_table(cur_antars, result.current_antardasha, t))

    idx_cur = next((i for i, d in enumerate(result.dashas)
                    if d.start == cur_md.start), -1)
    if idx_cur != -1 and idx_cur + 1 < len(result.dashas):
        next_md = result.dashas[idx_cur + 1]
        next_antars = dasha_mod.antardashas_for(next_md)
        blocks.append(
            f"<h3>{next_md_title} — {planet_label(next_md.lord)} "
            f"({next_md.start.strftime('%Y-%m-%d')} → "
            f"{next_md.end.strftime('%Y-%m-%d')})</h3>"
        )
        blocks.append(_antardasha_table(next_antars, None, t))

    return _css(theme) + f"<h2>{title}</h2>{_edu(EDU_ANTAR, t.locale)}" + "".join(blocks)


# ============================================================================
# YOGAS TAB
# ============================================================================

EDU_YOGAS = {
    "en": """
    <div class='edu'>
      <h4>Yogas — special planet combinations in your chart</h4>
      <p>A <b>yoga</b> is a specific arrangement of planets that classical
      texts say produces a particular result. Below is every yoga we could
      detect from your placements. Yogas don't act in isolation — they
      strengthen, weaken, or even cancel one another. Read them as
      <i>tendencies</i>, not verdicts.</p>
      <p>Quality marker: <b style="color:#2e7d32">●</b> positive,
         <b style="color:#f9a825">●</b> mixed,
         <b style="color:#c62828">●</b> cautionary.</p>
    </div>
    """,
    "ne": """
    <div class='edu'>
      <h4>योग — तपाईंको कुण्डलीमा देखिने विशेष ग्रह-संयोजन</h4>
      <p><b>योग</b> भनेको ग्रहहरूको त्यस्तो संयोजन हो जसले शास्त्र अनुसार
      खास फल दिन्छ। तल तपाईंको ग्रह-स्थानबाट देखिएका सबै योग छन्। योगहरू
      एक्लै काम गर्दैनन् — एक–अर्कोलाई बल/कमजोर पार्न वा रद्द पनि गर्न
      सक्छन्। यिनलाई <i>प्रवृत्ति</i> मान्नुहोस्, अन्तिम निर्णय होइन।</p>
      <p>रङ सङ्केत: <b style="color:#2e7d32">●</b> शुभ,
         <b style="color:#f9a825">●</b> मिश्रित,
         <b style="color:#c62828">●</b> सावधानी।</p>
    </div>
    """,
}


def render_yogas(result, t: T, theme: str = "light") -> str:
    title = "तपाईंको कुण्डलीमा योगहरू" if t.locale == "ne" else "Yogas in Your Chart"
    none_msg = ("कुनै शास्त्रीय योग प्रकट भएन — यो दुर्लभ होइन, धेरै "
                "जन्म-कुण्डलीमा शुभ योग देखिँदैनन्।"
                if t.locale == "ne" else
                "No classical yogas detected. This is not uncommon — "
                "many charts simply do not feature the textbook combinations.")
    if not result.yogas:
        return _css(theme) + f"<h2>{title}</h2>{_edu(EDU_YOGAS, t.locale)}<p>{none_msg}</p>"

    color_for = {"positive": "#2e7d32", "mixed": "#f9a825", "cautionary": "#c62828"}
    blocks = []
    for y in result.yogas:
        name = y.name_ne if t.locale == "ne" else y.name_en
        text = y.explanation_ne if t.locale == "ne" else y.explanation_en
        c = color_for.get(y.quality, "#888")
        blocks.append(f"""
        <div class='era'>
          <h3 style='color:{c};margin-top:0;'>● {name}</h3>
          <p>{text}</p>
        </div>
        """)
    return _css(theme) + f"<h2>{title}</h2>{_edu(EDU_YOGAS, t.locale)}" + "".join(blocks)


# ============================================================================
# TOPICS TAB — Education / Health / Career / etc.
# ============================================================================

def _age_years(birth_local) -> int | None:
    try:
        born = birth_local.date()
        today = date.today()
        return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
    except Exception:
        return None


AGE_STAGE_EN = [
    (17, "Foundation stage: keep readings educational, non-fatalistic, and focused on study habits, health rhythm, and family guidance."),
    (24, "Emerging adult stage: emphasize skill-building, career direction, relationship maturity, and financial basics."),
    (34, "Formation stage: decisions around work, partnership, wealth-building, and relocation carry more practical weight."),
    (49, "Consolidation stage: read for leadership, family responsibility, health maintenance, and durable reputation."),
    (200, "Legacy stage: emphasize health rhythm, dharma, mentoring, spiritual practice, and wealth preservation."),
]

AGE_STAGE_NE = [
    (17, "आधार चरण: पठनलाई शिक्षामूलक, गैर-भाग्यवादि, अध्ययन बानी, स्वास्थ्य लय, र परिवारिक मार्गदर्शनमा केन्द्रित राख्नुहोस्।"),
    (24, "युवा-वयस्क चरण: सीप, करियर दिशा, सम्बन्ध परिपक्वता, र वित्तीय आधारमा जोड दिनुहोस्।"),
    (34, "निर्माण चरण: काम, साझेदारी, धन-सञ्चय, र स्थान परिवर्तनका निर्णयहरू व्यवहारिक रूपमा महत्त्वपूर्ण हुन्छन्।"),
    (49, "स्थिरीकरण चरण: नेतृत्व, परिवारिक जिम्मेवारी, स्वास्थ्य हेरचाह, र दीर्घ प्रतिष्ठालाई प्राथमिकता दिनुहोस्।"),
    (200, "विरासत चरण: स्वास्थ्य लय, धर्म, मार्गदर्शन, आध्यात्मिक अभ्यास, र सम्पत्ति संरक्षणमा जोड दिनुहोस्।"),
]

TOPIC_AGE_FOCUS_EN = {
    "education": "For this age, education means both formal learning and the skill pattern that keeps improving the chart.",
    "health": "For this age, read health as a practical rhythm: sleep, food, recovery, stress, and prevention.",
    "career": "For this age, career prediction should be judged through readiness, daily discipline, and the active dasha period.",
    "wealth": "For this age, wealth means earning capacity, savings behavior, risk appetite, and family obligations.",
    "marriage": "For this age, relationship readings should separate attraction, commitment, family pressure, and timing.",
    "family": "For this age, family impact includes parents, siblings, children, household stability, and emotional duty.",
    "travel": "For this age, travel indicators show movement for study, career, marriage, retreat, or foreign settlement.",
    "spirituality": "For this age, spirituality is read as discipline, meaning, study, service, and inner steadiness.",
}

TOPIC_AGE_FOCUS_NE = {
    "education": "यो उमेरमा शिक्षा भनेको औपचारिक पढाइसँगै निरन्तर सुध्रिने सीप-ढाँचा पनि हो।",
    "health": "यो उमेरमा स्वास्थ्यलाई निद्रा, खाना, पुनर्स्थापना, तनाव, र रोकथामको व्यवहारिक लयका रूपमा पढ्नुहोस्।",
    "career": "यो उमेरमा करियर भविष्यवाणी तयारी, दैनिक अनुशासन, र चालू दशा-अवधिबाट जाँच्नुपर्छ।",
    "wealth": "यो उमेरमा धन भनेको कमाउने क्षमता, बचत बानी, जोखिम लिने शैली, र परिवारिक दायित्व हो।",
    "marriage": "यो उमेरमा सम्बन्ध पठनले आकर्षण, प्रतिबद्धता, परिवारिक दबाब, र समयलाई छुट्याउनुपर्छ।",
    "family": "यो उमेरमा परिवार प्रभावमा आमाबुबा, भाइबहिनी, सन्तान, घरको स्थिरता, र भावनात्मक दायित्व पर्छ।",
    "travel": "यो उमेरमा यात्रा सङ्केतले पढाइ, करियर, विवाह, विश्राम, वा विदेश बसाइँको गति देखाउँछ।",
    "spirituality": "यो उमेरमा अध्यात्म अनुशासन, अर्थ, अध्ययन, सेवा, र भित्री स्थिरताका रूपमा पढिन्छ।",
}


def _age_context(result, key: str, locale: str) -> str:
    age = _age_years(result.birth_local)
    if age is None:
        return ""
    stages = AGE_STAGE_NE if locale == "ne" else AGE_STAGE_EN
    stage_note = next(note for limit, note in stages if age <= limit)
    topic_focus = (TOPIC_AGE_FOCUS_NE if locale == "ne" else TOPIC_AGE_FOCUS_EN).get(key, "")
    age_label = f"{to_nepali_digits(age)} वर्ष" if locale == "ne" else f"{age} years old"
    prefix = "उमेर सन्दर्भ" if locale == "ne" else "Age context"
    return f"<b>{prefix}: {age_label}.</b> {stage_note} {topic_focus}"


def render_topics(result, t: T, theme: str = "light") -> str:
    title = ("जीवनका विषयहरू (विशेष विश्लेषण)"
             if t.locale == "ne" else "Life Topics (Personalized)")
    intro_en = ("Each card below applies your chart to one specific area of "
                "life — Education, Health, Career, Marriage, Wealth, Family, "
                "Travel, Spirituality. Click a card or scroll through.")
    intro_ne = ("तलका हरेक कार्डले तपाईंको कुण्डलीलाई जीवनको विशिष्ट "
                "क्षेत्रसँग जोडेर हेर्छ — शिक्षा, स्वास्थ्य, करियर, विवाह, धन, "
                "परिवार, यात्रा, अध्यात्म। कुनै कार्ड क्लिक गर्नुहोस् वा "
                "तल स्क्रोल गर्नुहोस्।")

    nav_links = []
    for trd in result.topics:
        name = trd.name_ne if t.locale == "ne" else trd.name_en
        nav_links.append(
            f"<a class='topic-nav-link' href='#topic-{trd.key}'>"
            f"<span class='topic-code'>{trd.icon}</span>{name}</a>"
        )

    blocks = []
    for trd in result.topics:
        name = trd.name_ne if t.locale == "ne" else trd.name_en
        findings = trd.findings_ne if t.locale == "ne" else trd.findings_en
        summary = trd.summary_ne if t.locale == "ne" else trd.summary_en

        houses_label = "मुख्य भाव" if t.locale == "ne" else "Key houses"
        karaka_label = "कारक" if t.locale == "ne" else "Karakas"
        age_label = "उमेर अनुसार" if t.locale == "ne" else "Age-aware focus"
        method_label = "पठन विधि" if t.locale == "ne" else "Reading method"
        mixture_label = "भाव + ग्रह मिश्रण" if t.locale == "ne" else "House + planet mixture"
        signals_label = ("यो कुण्डलीमा देखिएका सङ्केतहरू"
                         if t.locale == "ne" else "Observed chart signals")
        summary_label = "निष्कर्ष" if t.locale == "ne" else "Interpretation summary"
        age_context = _age_context(result, trd.key, t.locale)
        mixtures = trd.mixture_ne if t.locale == "ne" else trd.mixture_en

        if findings:
            findings_html = "".join(f"<li>{f}</li>" for f in findings)
        else:
            no_msg = ("कुनै विशेष सङ्केत भेटिएन।"
                      if t.locale == "ne" else "No special indicators found.")
            findings_html = f"<li class='small'>{no_msg}</li>"

        mixture_html = "".join(f"<li>{m}</li>" for m in mixtures)

        blocks.append(f"""
        <section class='era topic-card' id='topic-{trd.key}'>
          <h3><span class='topic-code'>{trd.icon}</span>{name}</h3>
          <div class='topic-structure'>
            <div>
              <h4>{method_label}</h4>
              <p class='small'>
                <b>{houses_label}:</b> {', '.join(str(h) for h in trd.houses)}<br>
                <b>{karaka_label}:</b> {', '.join(planet_label(k) for k in trd.karakas)}
              </p>
            </div>
            <div>
              <h4>{age_label}</h4>
              <p class='small'>{age_context}</p>
            </div>
          </div>
          <h4>{mixture_label}</h4>
          <ul class='mixture-list'>{mixture_html}</ul>
          <h4>{signals_label}</h4>
          <ul>{findings_html}</ul>
          <h4>{summary_label}</h4>
          <p>{summary}</p>
        </section>
        """)

    return _css(theme) + f"""
    <h2>{title}</h2>
    <p>{intro_ne if t.locale == 'ne' else intro_en}</p>
    <div style='margin:12px 0;'>{''.join(nav_links)}</div>
    {''.join(blocks)}
    """

