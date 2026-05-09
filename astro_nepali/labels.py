"""Bilingual labels: Devanagari (Nepali/Sanskrit) + English."""

RASHIS = [
    ("मेष", "Mesha", "Aries"),
    ("वृष", "Vrisha", "Taurus"),
    ("मिथुन", "Mithuna", "Gemini"),
    ("कर्क", "Karka", "Cancer"),
    ("सिंह", "Simha", "Leo"),
    ("कन्या", "Kanya", "Virgo"),
    ("तुला", "Tula", "Libra"),
    ("वृश्चिक", "Vrishchika", "Scorpio"),
    ("धनु", "Dhanu", "Sagittarius"),
    ("मकर", "Makara", "Capricorn"),
    ("कुम्भ", "Kumbha", "Aquarius"),
    ("मीन", "Meena", "Pisces"),
]

NAKSHATRAS = [
    ("अश्विनी", "Ashwini"),
    ("भरणी", "Bharani"),
    ("कृत्तिका", "Krittika"),
    ("रोहिणी", "Rohini"),
    ("मृगशिरा", "Mrigashira"),
    ("आर्द्रा", "Ardra"),
    ("पुनर्वसु", "Punarvasu"),
    ("पुष्य", "Pushya"),
    ("आश्लेषा", "Ashlesha"),
    ("मघा", "Magha"),
    ("पूर्व फाल्गुनी", "Purva Phalguni"),
    ("उत्तर फाल्गुनी", "Uttara Phalguni"),
    ("हस्त", "Hasta"),
    ("चित्रा", "Chitra"),
    ("स्वाती", "Swati"),
    ("विशाखा", "Vishakha"),
    ("अनुराधा", "Anuradha"),
    ("ज्येष्ठा", "Jyeshtha"),
    ("मूल", "Mula"),
    ("पूर्वाषाढा", "Purva Ashadha"),
    ("उत्तराषाढा", "Uttara Ashadha"),
    ("श्रवण", "Shravana"),
    ("धनिष्ठा", "Dhanishtha"),
    ("शतभिषा", "Shatabhisha"),
    ("पूर्व भाद्रपद", "Purva Bhadrapada"),
    ("उत्तर भाद्रपद", "Uttara Bhadrapada"),
    ("रेवती", "Revati"),
]

# Nakshatra lord (for Vimshottari Dasha) and planet ruling that nakshatra
NAKSHATRA_LORDS = [
    "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury",
    "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury",
    "Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury",
]

PLANETS = [
    ("सूर्य", "Surya", "Sun"),
    ("चन्द्र", "Chandra", "Moon"),
    ("मङ्गल", "Mangala", "Mars"),
    ("बुध", "Budha", "Mercury"),
    ("बृहस्पति", "Guru", "Jupiter"),
    ("शुक्र", "Shukra", "Venus"),
    ("शनि", "Shani", "Saturn"),
    ("राहु", "Rahu", "Rahu"),
    ("केतु", "Ketu", "Ketu"),
]

PLANET_BY_ENGLISH = {p[2]: p for p in PLANETS}

VARA = [  # Weekday — index 0 = Sunday
    ("आइतबार", "Ravivara", "Sunday"),
    ("सोमबार", "Somavara", "Monday"),
    ("मङ्गलबार", "Mangalavara", "Tuesday"),
    ("बुधबार", "Budhavara", "Wednesday"),
    ("बिहीबार", "Guruvara", "Thursday"),
    ("शुक्रबार", "Shukravara", "Friday"),
    ("शनिबार", "Shanivara", "Saturday"),
]

TITHI_NAMES = [
    "Pratipada", "Dwitiya", "Tritiya", "Chaturthi", "Panchami",
    "Shashthi", "Saptami", "Ashtami", "Navami", "Dashami",
    "Ekadashi", "Dwadashi", "Trayodashi", "Chaturdashi", "Purnima/Amavasya",
]

TITHI_NAMES_DEV = [
    "प्रतिपदा", "द्वितीया", "तृतीया", "चतुर्थी", "पञ्चमी",
    "षष्ठी", "सप्तमी", "अष्टमी", "नवमी", "दशमी",
    "एकादशी", "द्वादशी", "त्रयोदशी", "चतुर्दशी", "पूर्णिमा/अमावस्या",
]

YOGA_NAMES = [
    ("विष्कम्भ", "Vishkambha"), ("प्रीति", "Priti"), ("आयुष्मान्", "Ayushman"),
    ("सौभाग्य", "Saubhagya"), ("शोभन", "Shobhana"), ("अतिगण्ड", "Atiganda"),
    ("सुकर्मा", "Sukarma"), ("धृति", "Dhriti"), ("शूल", "Shula"),
    ("गण्ड", "Ganda"), ("वृद्धि", "Vriddhi"), ("ध्रुव", "Dhruva"),
    ("व्याघात", "Vyaghata"), ("हर्षण", "Harshana"), ("वज्र", "Vajra"),
    ("सिद्धि", "Siddhi"), ("व्यतीपात", "Vyatipata"), ("वरीयान्", "Variyan"),
    ("परिघ", "Parigha"), ("शिव", "Shiva"), ("सिद्ध", "Siddha"),
    ("साध्य", "Sadhya"), ("शुभ", "Shubha"), ("शुक्ल", "Shukla"),
    ("ब्रह्म", "Brahma"), ("इन्द्र", "Indra"), ("वैधृति", "Vaidhriti"),
]

KARANA_NAMES = [
    "Bava", "Balava", "Kaulava", "Taitila", "Garaja", "Vanija", "Vishti",
    "Shakuni", "Chatushpada", "Naga", "Kimstughna",
]

NEPALI_MONTHS = [
    ("बैशाख", "Baisakh"),
    ("जेठ", "Jestha"),
    ("असार", "Ashadh"),
    ("साउन", "Shrawan"),
    ("भदौ", "Bhadra"),
    ("असोज", "Ashwin"),
    ("कार्तिक", "Kartik"),
    ("मंसिर", "Mangsir"),
    ("पुष", "Poush"),
    ("माघ", "Magh"),
    ("फागुन", "Falgun"),
    ("चैत", "Chaitra"),
]

NEPALI_DIGITS = "०१२३४५६७८९"


def to_nepali_digits(s: str) -> str:
    return "".join(NEPALI_DIGITS[int(c)] if c.isdigit() else c for c in str(s))


def rashi_label(idx: int) -> str:
    """Return 'देवनागरी / English' for a rashi index (0..11)."""
    dev, _, en = RASHIS[idx % 12]
    return f"{dev} / {en}"


def nakshatra_label(idx: int) -> str:
    dev, en = NAKSHATRAS[idx % 27]
    return f"{dev} / {en}"


def planet_label(english_name: str) -> str:
    p = PLANET_BY_ENGLISH.get(english_name)
    if not p:
        return english_name
    dev, _, en = p
    return f"{dev} / {en}"


def vara_label(weekday_sun0: int) -> str:
    dev, _, en = VARA[weekday_sun0 % 7]
    return f"{dev} / {en}"


def tithi_label(idx_1based: int, paksha: str) -> str:
    """idx_1based is 1..15; paksha is 'Shukla' or 'Krishna'."""
    idx = (idx_1based - 1) % 15
    en = TITHI_NAMES[idx]
    dev = TITHI_NAMES_DEV[idx]
    paksha_dev = "शुक्ल" if paksha == "Shukla" else "कृष्ण"
    return f"{paksha_dev} {dev} / {paksha} {en}"


def yoga_label(idx: int) -> str:
    dev, en = YOGA_NAMES[idx % 27]
    return f"{dev} / {en}"


def karana_label(idx: int) -> str:
    return KARANA_NAMES[idx % 11]
