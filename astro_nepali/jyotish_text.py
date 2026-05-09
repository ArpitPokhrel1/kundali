"""Long-form Jyotish content — for the Explanation tab and Dasha era notes.

All entries available in English ('en') and Nepali ('ne'). Goals:
  - Educational, for someone who wants to LEARN classical reading.
  - Plain, non-deterministic language ("tendency", "supports", "tests", not
    "you will" / "must").
  - Nepali version uses correct Nepali (not Hindi-Nepali pidgin) and proper
    devanagari spellings for astrological terms.
"""
from __future__ import annotations

# ============================================================================
#                            MAHADASHA ERA NOTES
# ============================================================================
# For each of the 9 Vimshottari Mahadasha lords, a multi-section reading of
# what classical Jyotish associates with that period. Use these for educational
# purposes; the actual flavor depends on the lord's placement, dignity, and
# aspects in the natal chart.

MAHADASHA_NOTES_EN = {
    "Sun": {
        "headline": "Sun (Surya) Mahadasha — 6 years",
        "overview": (
            "Sun rules soul (atman), authority, the father, vitality, and one's "
            "sense of inner direction. A Sun period emphasizes themes of identity, "
            "leadership, recognition, and self-respect. Where the Sun is well-placed, "
            "it grants visibility, status, and a clearer sense of dharma; where weak "
            "or afflicted, it can bring ego-bruises, conflicts with authority, or "
            "father-related concerns."
        ),
        "career": (
            "Often a period of stepping forward — promotion, public role, taking "
            "responsibility. People may ask you to lead. Recognition for past work "
            "is common. If Sun is debilitated or in dusthanas (6/8/12), be alert to "
            "ego-clashes with seniors and reputation tests."
        ),
        "relationships": (
            "Father and father-figures come into focus, for better or for difficulty. "
            "Authority dynamics in marriage and at work get a stress-test. Social "
            "circle may shrink to fewer, weightier relationships."
        ),
        "health": (
            "Heart, eyes (especially right eye for males / left for females), "
            "circulation, bones, digestion of fats. Tendency to push too hard — "
            "burnout if rest is neglected."
        ),
        "psychology": (
            "Strong inner pull toward 'who am I, what is my purpose'. Self-discipline "
            "rises. Pride and dignity are felt acutely — small slights can sting "
            "more than they would otherwise. A good period for spiritual practices "
            "centered on the inner Self (atman vichara)."
        ),
        "tip": (
            "Watch which house holds the Sun and which sign it occupies — that area "
            "of life will be lit up (or scorched) for these 6 years."
        ),
    },
    "Moon": {
        "headline": "Moon (Chandra) Mahadasha — 10 years",
        "overview": (
            "Moon rules mind (manas), emotions, mother, the public, comfort, and "
            "the body's fluids. A Moon period is fundamentally about emotional "
            "weather and one's relationship to home, women, family, and the "
            "general public. Mood, intuition, and sensitivity are heightened."
        ),
        "career": (
            "Public-facing work flourishes — sales, hospitality, food, real estate, "
            "nursing, teaching, anything 'caring'. Career mood rather than ambition "
            "drives choices; you'll do best in work that emotionally resonates."
        ),
        "relationships": (
            "Mother and mother-figures take center stage. Family bonds intensify. "
            "Marriage and partnership become a primary source of emotional grounding. "
            "Friendships with women often become important."
        ),
        "health": (
            "Lungs, stomach, breast tissue, fluids. Watch for water-imbalance "
            "issues, sinus, cold-related conditions. Sleep quality matters more "
            "than usual; insomnia surfaces if Moon is afflicted."
        ),
        "psychology": (
            "A decade of emotional learning. Mood swings are common — neither "
            "fight them nor be ruled by them. Intuition sharpens; dreams become "
            "informative. Tendency toward nostalgia, attachment to home, and "
            "preoccupation with belonging."
        ),
        "tip": (
            "Moon's strength is judged by its phase (waxing/full = strong; new/waning "
            "= weaker) and house. A waning Moon dasha can feel emotionally depleting "
            "until practices for inner steadiness are in place."
        ),
    },
    "Mars": {
        "headline": "Mars (Mangal) Mahadasha — 7 years",
        "overview": (
            "Mars rules action, courage, energy, brothers, conflict, surgery, "
            "engineering, the military, real estate, and the principle of 'cutting "
            "through obstacles'. A Mars period is short but intense — much can be "
            "accomplished, and much can be ignited, in 7 years."
        ),
        "career": (
            "Drive surges. Suited to entrepreneurial moves, hard physical work, "
            "sports, military, surgery, IT/engineering, real estate dealings. "
            "Risk-taking pays — but only with discipline. Without it, expensive "
            "mistakes."
        ),
        "relationships": (
            "Brothers/cousins are emphasized. Sexual intensity rises. Conflicts "
            "with peers, neighbors, or rivals can flare; learning when to fight "
            "and when to walk away is the period's lesson."
        ),
        "health": (
            "Blood, bone marrow, muscles, the head (Mars rules the forehead). "
            "Accidents, surgeries, fevers, inflammations — all more probable. "
            "Exercise is essential; Mars energy turns inward and burns the body "
            "if not externalized."
        ),
        "psychology": (
            "Quick to act, quick to anger. Patience is the central practice. "
            "Boldness can shade into recklessness. Boundaries — saying no, "
            "protecting your time — improve dramatically if used well."
        ),
        "tip": (
            "Mars's house tells you where the fire burns. In angles (1/4/7/10) "
            "ambition is direct. In trikonas (5/9) it's creative. In 6/8/12 it's "
            "either combative (6) or transformative (8/12)."
        ),
    },
    "Mercury": {
        "headline": "Mercury (Budha) Mahadasha — 17 years",
        "overview": (
            "Mercury rules intellect, speech, learning, business, writing, "
            "calculation, communication, friendships, and skill of the hands. "
            "A Mercury period — second-longest after Venus — is about thinking, "
            "talking, trading, and connecting. It rewards the curious."
        ),
        "career": (
            "Education, writing, teaching, journalism, accounting, software, "
            "trade/commerce, mediation, sales — all favored. People may go back "
            "to school or pivot to a knowledge-based career. Networks expand. "
            "Multiple income streams become normal."
        ),
        "relationships": (
            "Friendships and casual connections matter more than deep romantic "
            "bonds. Communication in marriage gets a workout; clarity matters. "
            "Maternal uncles and cousins (Mercury's significations) come into "
            "play."
        ),
        "health": (
            "Nervous system, skin, lungs, speech organs. Anxiety and 'over-thinking' "
            "are the period's signature health risks. Hands, fingers."
        ),
        "psychology": (
            "Mind in overdrive — many ideas, many words. The discipline of "
            "FINISHING what you start matters. Communication style sets up career "
            "outcomes. Truthfulness in speech becomes a lifelong practice (Mercury "
            "rules speech karma)."
        ),
        "tip": (
            "Mercury takes on the qualities of the planet it sits with — with "
            "Sun it gets royal/authoritative; with Mars it gets sharp/argumentative; "
            "with Saturn it gets serious/researcher-like."
        ),
    },
    "Jupiter": {
        "headline": "Jupiter (Guru/Brihaspati) Mahadasha — 16 years",
        "overview": (
            "Jupiter rules wisdom, teachers, dharma, expansion, prosperity, "
            "children (especially first-born), religion, philosophy, and law. "
            "Considered the most benefic graha. A Jupiter period typically expands "
            "life — career, family, learning, spiritual practice. The risk is "
            "that it can also expand WHAT YOU ARE — including weight, ego, and "
            "bad habits."
        ),
        "career": (
            "Teaching, advisory roles, law, finance, spirituality, education, "
            "publishing, government — all favored. Promotion, recognition by "
            "elders/seniors, and a sense of being mentored or guided are common."
        ),
        "relationships": (
            "Marriage often happens in this period (especially for women — Jupiter "
            "is karaka of husband). Children are born or come into focus. Bond with "
            "father (and father-figures, gurus) deepens."
        ),
        "health": (
            "Liver, pancreas, fat metabolism, hips/thighs. Diabetes risk increases. "
            "Tendency toward over-indulgence — sweet things, comfort foods, "
            "excessive ease."
        ),
        "psychology": (
            "Optimism, philosophical mind, generosity. A growing sense that 'life "
            "has meaning'. Tendency to over-promise. Pride in knowledge can become "
            "intellectual arrogance. Faith in something larger than oneself "
            "deepens — religion, dharma, principles."
        ),
        "tip": (
            "Jupiter's house is where life expands during this dasha. If Jupiter "
            "is in the 7th, expect partnerships; in the 5th, children/creativity; "
            "in the 10th, public dharma/career; in the 11th, large gains."
        ),
    },
    "Venus": {
        "headline": "Venus (Shukra) Mahadasha — 20 years",
        "overview": (
            "Venus rules love, beauty, art, music, comfort, partnerships, vehicles, "
            "luxury, sweet things, and reproductive health. The longest Mahadasha. "
            "A Venus period is about pleasure, partnership, refinement — and the "
            "discipline to enjoy without becoming attached."
        ),
        "career": (
            "Arts, design, fashion, entertainment, beauty, hospitality, food, "
            "diplomacy, real estate, finance — all favored. The work tends to feel "
            "good rather than just feeling productive. Relationships with clients "
            "and partners drive opportunities."
        ),
        "relationships": (
            "Marriage is often initiated, deepened, or tested in Venus dasha "
            "(especially for men — Venus is karaka of wife). Romantic life is "
            "vivid. Friendships, social circles, and aesthetic communities flourish."
        ),
        "health": (
            "Reproductive system, kidneys, urinary tract, throat, eyes. Sweet "
            "tooth and rich-food risks: diabetes, weight gain. Skin glows when "
            "Venus is happy."
        ),
        "psychology": (
            "Sensitivity to beauty, harmony, and pleasure. Tendency to avoid "
            "conflict — which can become an inability to set boundaries. Love "
            "feels like the central question of life. The shadow side: indulgence, "
            "addiction to comfort, and difficulty walking away from the wrong "
            "partnership because it's 'sweet enough'."
        ),
        "tip": (
            "Venus suffers if it's in 6/8/12 (especially 8). With Mars it's passionate "
            "but turbulent; with Saturn it's mature/late-blooming; with Sun it can "
            "feel suppressed or dimmed."
        ),
    },
    "Saturn": {
        "headline": "Saturn (Shani) Mahadasha — 19 years",
        "overview": (
            "Saturn rules discipline, work, longevity, perseverance, restriction, "
            "old age, the masses, servants, justice, and karma. The most demanding "
            "but ultimately the most-rewarding-for-the-patient Mahadasha. Saturn "
            "delays so that the result will last; that's the period's promise."
        ),
        "career": (
            "Slow climb, no shortcuts. Civil service, law, mining, manufacturing, "
            "labor unions, the elderly, real estate (land specifically), engineering. "
            "Recognition is late, but solid. Job changes happen but each one weighs "
            "more than it would in another dasha."
        ),
        "relationships": (
            "Loneliness is a frequent theme — relationships feel heavier, more "
            "responsible, less playful. Older partners or partners far away are "
            "common. Marriage may be delayed or feel duty-bound. Friendships thin "
            "out, with the survivors becoming lifelong."
        ),
        "health": (
            "Bones, joints, knees, teeth, chronic conditions, nervous system "
            "depletion. Saturn brings what's been ignored to the surface. Regular "
            "rest, simple food, and consistent rhythm matter more than supplements."
        ),
        "psychology": (
            "Realism — sometimes pessimism. A sense that effort is the only honest "
            "currency. Patience is forced upon you until it becomes natural. "
            "Boundaries get clearer; people-pleasing diminishes. Late in the dasha, "
            "a quiet authority emerges that no one can take away."
        ),
        "tip": (
            "Saturn becomes much friendlier when one already has discipline going "
            "in. If you cooperate with what Saturn is teaching (slow down, do the "
            "work, don't cheat), the last 5–6 years of the dasha can be remarkable. "
            "Saturn rules reaping; whatever you sow in years 1–13 you harvest in "
            "years 14–19."
        ),
    },
    "Rahu": {
        "headline": "Rahu Mahadasha — 18 years",
        "overview": (
            "Rahu (north node of the Moon) rules ambition, foreign things, "
            "obsession, sudden gains, mass movements, technology, the unconventional, "
            "and shadow-desires we don't admit. Rahu doesn't deliver in a straight "
            "line — it amplifies, distorts, and rewards in ways that surprise. Rahu "
            "dashas are famously turbulent and famously transformative."
        ),
        "career": (
            "Foreign travel/work, technology, media, politics, research into the "
            "occult/hidden, anything cutting-edge. Sudden rises. Sudden falls. "
            "Career often pivots in unexpected directions; old plans go out the "
            "window. Speculation, crypto, viral fame — Rahu's playground. Income "
            "spikes, sometimes through unconventional channels."
        ),
        "relationships": (
            "Unconventional partnerships are common — different culture, age, "
            "background, or social circle than expected. Marriage may happen "
            "suddenly or be delayed strangely. Old friendships drop; entirely new "
            "circles form."
        ),
        "health": (
            "Phantom complaints, allergies, undiagnosable issues, anxiety, "
            "addictions, skin problems. Rahu confuses the diagnostic process. "
            "Mental health needs careful attention — restlessness, racing mind, "
            "FOMO."
        ),
        "psychology": (
            "Hunger that doesn't quite know what it wants. Strong desire for "
            "'more' — more visibility, more wealth, more exotic experiences. The "
            "temptation to cut corners, exaggerate, and chase the next thing is "
            "constant. The lesson: maturing into your hunger so it doesn't run you."
        ),
        "tip": (
            "Rahu in trikonas (5/9) tends to give worldly success; in dusthanas "
            "(6/8/12) it gives spiritual progress through rough karma; in kendras "
            "(1/4/7/10) it gives prominence with instability. The first 3–4 years "
            "and last 2 years are often most volatile."
        ),
    },
    "Ketu": {
        "headline": "Ketu Mahadasha — 7 years",
        "overview": (
            "Ketu (south node) rules detachment, past-life merit, intuition, "
            "moksha (liberation), losses that purify, isolation, and spiritual "
            "depth. Where Rahu hungers, Ketu releases. A Ketu period strips away "
            "what the soul no longer needs — sometimes gently, sometimes painfully — "
            "and reveals what was always there underneath."
        ),
        "career": (
            "Career can feel directionless, or undergo a quiet about-face. Suited "
            "to research, healing, contemplative work, occult/spiritual fields, "
            "emergency medicine, chemistry. Not a period of obvious 'success' — "
            "it's a period of consolidation and release. Sudden departures from "
            "long-held jobs are common."
        ),
        "relationships": (
            "Detachment surfaces. Long relationships may end without obvious cause "
            "— or deepen into a wordless companionship. Time alone increases. "
            "Marriage in Ketu dasha is rare; if it happens, often after a strong "
            "spiritual or fated encounter."
        ),
        "health": (
            "Mysterious ailments, chronic fatigue, skin/scalp problems, the spine. "
            "Ketu rules the lower body. Energy levels can dip. Spiritual practices "
            "(yoga, meditation) provide more relief than medical interventions."
        ),
        "psychology": (
            "A sense that surfaces no longer satisfy. Withdrawal from social noise. "
            "The mind wants depth, silence, and the question 'what am I really?' "
            "Old identities dissolve. People may misread you as 'changed' or "
            "'distant' — you've simply outgrown the old shape."
        ),
        "tip": (
            "Ketu accelerates spiritual evolution but is harsh on material "
            "ambitions. If the natal Ketu is well-placed (in 9/12 especially) the "
            "dasha can deliver remarkable insight; in 6/8 it can bring trying "
            "events that ultimately serve the soul."
        ),
    },
}


# Nepali version — written in proper Nepali, not transliterated Hindi.
MAHADASHA_NOTES_NE = {
    "Sun": {
        "headline": "सूर्य महादशा — ६ वर्ष",
        "overview": (
            "सूर्यले हाम्रो आत्मा (भित्री ‘म’), बुबा, अधिकार जमाउने "
            "क्षमता, र शरीरको ओजलाई बुझाउँछ। सूर्य महादशा सुरु हुँदा "
            "‘मेरो परिचय के हो, मेरो काम के हो’ भन्ने प्रश्न महत्त्वपूर्ण "
            "बन्छ। नेतृत्व लिने अवसर, अरूको सम्मान, र आत्मगौरव — "
            "यी कुरा यी ६ वर्षमा प्रमुख हुन्छन्। कुण्डलीमा सूर्य राम्रो "
            "ठाउँमा छ भने प्रतिष्ठा र देखिने अवसर बढ्छन्; कमजोर वा "
            "पीडित छ भने हाकिमसँग ठक्कर, अहम्‌मा चोट, वा बुबासँगका "
            "चिन्ता आउन सक्छन्।"
        ),
        "career": (
            "अघि सर्ने बेला हो — पदोन्नति, सार्वजनिक भूमिका, ठूलो "
            "जिम्मेवारी। मानिसहरू तपाईंलाई नेता बनाउन खोज्छन्। पुरानो "
            "कामको कदर हुन्छ। तर सूर्य कमजोर भएमा वरिष्ठहरूसँग "
            "टकराव र प्रतिष्ठाको परीक्षा पनि सम्भव।"
        ),
        "relationships": (
            "बुबा र बुबा-तुल्य व्यक्ति मनमा आइरहन्छन् — राम्रो वा "
            "गाह्रो जे होस्। विवाह र काममा ‘को मुख्य’ भन्ने कुराको "
            "परीक्षा हुन्छ। साथी कम तर भारी हुन्छन् — गहन कुरा गर्न "
            "मिल्ने थोरै मानिस।"
        ),
        "health": (
            "मुटु, आँखा (पुरुषमा दायाँ, महिलामा बायाँ बढी), रगत बग्ने "
            "नली, हड्डी, बोसो पाचन। आफूलाई धेरै थकाउने प्रवृत्ति बढ्छ "
            "— पूरै विश्राम नभए ‘बर्नआउट’ हुन सक्छ।"
        ),
        "psychology": (
            "‘म को हुँ, मेरो काम के हो’ भन्ने प्रश्न मनमा गहिरो "
            "बस्छ। आफैँलाई अनुशासनमा राख्ने रुचि बढ्छ। मान-सम्मानप्रति "
            "बढी संवेदनशील — सानो अपमान पनि मनमा गहिरो लाग्छ। ध्यान "
            "र आत्म-चिन्तन यस बेला विशेष फलदायी।"
        ),
        "tip": (
            "कुण्डलीमा सूर्य कुन भाव र राशिमा छ — त्यही जीवन-क्षेत्र "
            "यी ६ वर्षभर ‘उज्यालिने’ वा ‘पोल्ने’ हुन्छ। उदाहरणका लागि: "
            "सूर्य १० मा भए करियर मुख्य; ७ मा भए विवाह/साझेदारी; "
            "४ मा भए घर र आमासँगको सम्बन्ध।"
        ),
    },
    "Moon": {
        "headline": "चन्द्र महादशा — १० वर्ष",
        "overview": (
            "चन्द्रले हाम्रो मन, भावना, आमा, र साधारण मानिसहरूसँगको "
            "सम्बन्ध बुझाउँछ। चन्द्र महादशा भनेको १० वर्षको ‘भावनात्मक "
            "मौसम’ हो — घर, परिवार, महिला, र जनसमुदायसँगको सम्बन्धमा "
            "गहन प्रभाव पर्ने समय। यस बेला तपाईंको मूड, अन्तर्ज्ञान "
            "(भित्री बोध), र संवेदनशीलता बढ्छन्।"
        ),
        "career": (
            "मानिसहरूसँग सीधा जोडिने काम राम्रो फस्टाउँछ — बिक्री, "
            "होटल/रेस्टुरेन्ट, खाद्य, घरजग्गा, नर्सिङ, शिक्षण, हेरचाह। "
            "‘ठूलो हुने इच्छा’ भन्दा ‘मन मिल्ने काम’ ले अघि बढाउँछ; "
            "मनलाई सुहाउने काममा सबभन्दा राम्रो फल।"
        ),
        "relationships": (
            "आमा र आमा-तुल्य व्यक्ति केन्द्रमा। पारिवारिक बन्धन गाढा "
            "हुन्छन्। विवाह र साझेदारी भावनात्मक टेकोको स्रोत बन्छन्। "
            "महिलाहरूसँगको मित्रता विशेष महत्त्वपूर्ण।"
        ),
        "health": (
            "फोक्सो, पेट, छाती, शरीरका तरल पदार्थ। पानी असन्तुलन, "
            "साइनस, चिसो रोग। निद्राको गुणस्तर सामान्यभन्दा बढी "
            "महत्त्वपूर्ण; चन्द्र पीडित भए अनिद्रा देखिन सक्छ।"
        ),
        "psychology": (
            "एक दशक भावनात्मक सिकाइको। मूड परिवर्तन हुनु सामान्य — "
            "लड्न पनि नपर्ने, बहकिनु पनि नपर्ने। अन्तर्ज्ञान तीव्र हुन्छ; "
            "सपनाले पनि सूचना दिन्छ। पुराना कुराको याद, घरप्रति लगाव, "
            "‘कतै पनि मिलेर बस्ने’ इच्छा बारम्बार आउँछ।"
        ),
        "tip": (
            "चन्द्रको शक्ति त्यसको ‘कला’ ले निर्धारण हुन्छ — शुक्ल "
            "पक्ष/पूर्ण = बलियो; कृष्ण/क्षीण = कमजोर। क्षीण चन्द्रको "
            "दशा भावनात्मक रूपमा थकाउने हुन सक्छ — ध्यान, प्रार्थना, "
            "परिवारसँगको समय धेरै सहयोगी।"
        ),
    },
    "Mars": {
        "headline": "मङ्गल महादशा — ७ वर्ष",
        "overview": (
            "मङ्गलले कर्म-शक्ति, साहस, क्रोध, भाइ, र ‘बाधा छेद्ने’ "
            "शक्ति बुझाउँछ। मङ्गल महादशा छोटो (७ वर्ष) तर तीव्र "
            "हुन्छ — यस बेला धेरै कुरा सिद्ध गर्न सकिन्छ; ध्यान नदिए "
            "धेरै कुरा डढ्न पनि सक्छन्।"
        ),
        "career": (
            "आफ्नो व्यवसाय, कडा शारीरिक काम, खेलकुद, सेना, शल्यक्रिया, "
            "इन्जिनियरिङ/आईटी, घरजग्गा कारोबार — यी क्षेत्रमा राम्रो "
            "फल। जोखिम लिने उद्यमलाई पुरस्कार — तर अनुशासनसँग मात्र। "
            "नभए महँगा गल्ती।"
        ),
        "relationships": (
            "भाइ-दिदी-बहिनी केन्द्रमा। यौन ऊर्जा बढ्छ। साथी, छिमेकी, "
            "प्रतिद्वन्द्वीसँग टकराव सम्भव — ‘कहिले लड्ने, कहिले हट्ने’ "
            "भन्ने पाठ यो दशाको मुख्य सिकाइ हो।"
        ),
        "health": (
            "रगत, हाडको मज्जा, मांसपेशी, टाउको। दुर्घटना, शल्यक्रिया, "
            "ज्वरो, सूजन — सम्भावना बढी। नियमित व्यायाम अनिवार्य; "
            "नभए मङ्गलको आगो शरीरभित्रै फर्केर पोल्न थाल्छ।"
        ),
        "psychology": (
            "छिटो काम, छिटो रिस। धैर्य नै सबभन्दा महत्त्वपूर्ण अभ्यास। "
            "साहस लापरबाहीमा फेरिन सक्छ। तर सही ढङ्गले प्रयोग गर्ने "
            "हो भने ‘नाइँ’ भन्न सक्ने, आफ्नो समय जोगाउन सक्ने क्षमता "
            "खुब बढ्छ।"
        ),
        "tip": (
            "मङ्गलको भावले ‘आगो कहाँ बल्छ’ बताउँछ। केन्द्र भाव "
            "(१/४/७/१०) मा भए महत्त्वाकाङ्क्षा सीधा; त्रिकोण (५/९) "
            "मा भए सिर्जनशील; ६ भावमा द्वन्द्वमुखी; ८/१२ मा गहिरो "
            "रूपान्तरण ल्याउने।"
        ),
    },
    "Mercury": {
        "headline": "बुध महादशा — १७ वर्ष",
        "overview": (
            "बुधले बुद्धि, वाणी, अध्ययन, व्यापार, लेखन, हिसाब, "
            "सञ्चार, र मित्रता बुझाउँछ। बुध महादशा (१७ वर्ष) ‘सोच्ने, "
            "बोल्ने, कारोबार गर्ने, मानिसमानिस जोडिने’ अवधि हो। "
            "जिज्ञासुलाई पुरस्कार दिने समय।"
        ),
        "career": (
            "शिक्षण, लेखन, पत्रकारिता, हिसाब-किताब, सफ्टवेयर, व्यापार, "
            "मध्यस्थता, बिक्री — सबै राम्रा। मानिसहरू पुनः अध्ययनमा "
            "फर्किन्छन् वा ज्ञानमूलक करियर रोज्छन्। सम्पर्क-वृत्त बढ्छ। "
            "आम्दानीका धेरै स्रोत हुनु सामान्य।"
        ),
        "relationships": (
            "मित्रता र साधारण सम्पर्क गहिरो प्रेमभन्दा बढी प्रभावशाली। "
            "विवाहमा सञ्चारको परीक्षा — स्पष्ट कुरा भनिएन भने तनाव। "
            "मामा र भाइ-बहिनी (बुधले बुझाउने) ले महत्त्वपूर्ण भूमिका "
            "लिन्छन्।"
        ),
        "health": (
            "स्नायु प्रणाली (मस्तिष्क-तन्तु), छाला, फोक्सो, वाणी। "
            "चिन्ता र ‘धेरै सोच्ने’ ले बुधको दशामा सबभन्दा बढी असर "
            "गर्छ। हात-औंलाका समस्या पनि देखिन सक्छन्।"
        ),
        "psychology": (
            "मन तीव्र, विचार धेरै, शब्द धेरै। ‘सुरु गरेको काम पूरा "
            "गर्ने’ अनुशासनले फरक पार्छ। बोलीचालीको शैलीले करियर "
            "बनाउँछ। सत्य बोल्ने अभ्यास (बुध वाणीको स्वामी) यस बेला "
            "विशेष महत्त्वको हुन्छ।"
        ),
        "tip": (
            "बुधले साथमा बस्ने ग्रहको गुण लिन्छ — सूर्यसँग बस्दा "
            "राजसी, मङ्गलसँग बस्दा तीक्ष्ण/विवादी, शनिसँग बस्दा "
            "गम्भीर/अनुसन्धानमुखी।"
        ),
    },
    "Jupiter": {
        "headline": "बृहस्पति (गुरु) महादशा — १६ वर्ष",
        "overview": (
            "गुरुले ज्ञान, शिक्षक, धर्म, विस्तार, समृद्धि, सन्तान, र "
            "दर्शन बुझाउँछ — सबभन्दा शुभ ग्रह मानिन्छ। गुरु महादशा "
            "(१६ वर्ष) मा जीवन सामान्यतया फैलिन्छ — करियर, परिवार, "
            "अध्ययन, साधना। तर ‘तपाईं जे हुनुहुन्छ’ त्यो पनि फैलिन्छ — "
            "तौल, अहम्, खराब बानी समेत।"
        ),
        "career": (
            "शिक्षण, सल्लाह, कानून, वित्त, अध्यात्म, शिक्षा, प्रकाशन, "
            "सरकारी क्षेत्र — सबै राम्रा। पदोन्नति र वरिष्ठहरूले "
            "मार्गदर्शन गरेको अनुभूति सामान्य।"
        ),
        "relationships": (
            "विवाह यो दशामा प्रायः हुन्छ (विशेषतः महिलाका लागि — "
            "गुरु पतिको प्रतीक)। सन्तानको जन्म वा त्यसको सोच केन्द्रमा। "
            "बुबा र गुरु-तुल्य व्यक्तिसँगको सम्बन्ध गहिरो।"
        ),
        "health": (
            "कलेजो, अग्न्याशय (पाचनको ग्रन्थि), बोसो चयापचय, कमर/"
            "जाँघ। मधुमेहको जोखिम बढ्न सक्छ। मीठो र आराममा बढी "
            "अभ्यस्त हुने सम्भावना।"
        ),
        "psychology": (
            "आशा, दार्शनिक मन, उदारता। ‘जीवनको अर्थ छ’ भन्ने अनुभूति "
            "बढ्छ। बढी प्रतिज्ञा गर्ने प्रवृत्ति। ज्ञानप्रतिको गर्व "
            "विनयको अभावमा बौद्धिक अहंकारमा बदलिन सक्छ। आफूभन्दा "
            "ठूलो कुरामा (धर्म, सिद्धान्त) विश्वास गहिरो हुन्छ।"
        ),
        "tip": (
            "गुरुको भावले ‘जीवन कहाँ फैलिन्छ’ देखाउँछ। ७ मा "
            "साझेदारी; ५ मा सन्तान/सिर्जना; १० मा सार्वजनिक "
            "धर्म/करियर; ११ मा ठूलो लाभ।"
        ),
    },
    "Venus": {
        "headline": "शुक्र महादशा — २० वर्ष",
        "overview": (
            "शुक्रले प्रेम, कला, सौन्दर्य, सुख, साझेदारी, सवारी, र "
            "विलासिता बुझाउँछ। शुक्र महादशा सबभन्दा लामो (२० वर्ष) — "
            "यो भोग, सम्बन्ध, परिष्कार, र ‘अनासक्त भोग’ को अनुशासन "
            "सिकाउने समय।"
        ),
        "career": (
            "कला, डिजाइन, फेसन, मनोरञ्जन, सौन्दर्य, होटल, खाद्य, "
            "कूटनीति, घरजग्गा, वित्त — राम्रा। काम सिर्फ ‘उत्पादक’ "
            "नभई ‘रमाइलो लाग्ने’ हुन्छ। ग्राहक र साझेदारसँगको "
            "सम्बन्धले अवसर ल्याउँछ।"
        ),
        "relationships": (
            "विवाहको प्रारम्भ, गहन हुने, वा परीक्षा — विशेषतः पुरुषका "
            "लागि (शुक्र पत्नीको प्रतीक)। प्रेम-जीवन सजीव। मित्रता, "
            "सामाजिक सम्बन्ध, कलात्मक समूह फस्टाउँछन्।"
        ),
        "health": (
            "प्रजनन प्रणाली, मिर्गौला, मूत्रमार्ग, घाँटी, आँखा। मीठो "
            "खानेकुराको लोभ — मधुमेह र तौल वृद्धिको जोखिम। शुक्र खुसी "
            "हुँदा छाला चम्किन्छ।"
        ),
        "psychology": (
            "सौन्दर्य र सद्भावप्रति संवेदनशीलता बढ्छ। द्वन्द्व छल्ने "
            "प्रवृत्ति — सीमारेखा कोर्न नसक्ने हुन सक्छ। ‘प्रेम जीवनको "
            "केन्द्रीय कुरा हो’ जस्तो लाग्ने। छाया-पक्ष: भोग, आरामको "
            "लत, गलत साझेदारी छोड्न नसक्ने।"
        ),
        "tip": (
            "शुक्र ६/८/१२ भावमा पीडित हुन्छ (विशेष ८ मा)। मङ्गलसँग — "
            "भावुक तर अशान्त; शनिसँग — परिपक्व/ढिलो खुल्ने; सूर्यसँग — "
            "दबिएको।"
        ),
    },
    "Saturn": {
        "headline": "शनि महादशा — १९ वर्ष",
        "overview": (
            "शनिले अनुशासन, श्रम, उमेर, धैर्य, प्रतिबन्ध, र कर्मफल "
            "बुझाउँछ। सबभन्दा कठिन तर धैर्यवानलाई दीर्घकालीन फल दिने "
            "महादशा। शनिले ढिलो गर्छ ताकि फल टिकाउ होस् — यही "
            "दशाको वचन हो।"
        ),
        "career": (
            "बिस्तारै चढाइ, छोटो बाटो छैन। निजामती सेवा, कानून, खानी, "
            "उत्पादन, श्रमिक संगठन, बूढापाकाको सेवा, घरजग्गा (विशेषतः "
            "जग्गा), इन्जिनियरिङ। कदर ढिलो तर पक्का। काम परिवर्तन "
            "हुन्छ तर हरेकको तौल बढी।"
        ),
        "relationships": (
            "एकाकीपन प्रायः हुन्छ — सम्बन्ध भारी, जिम्मेवारीले भरिएका, "
            "कम चञ्चल। वृद्ध वा टाढाका साझेदार सामान्य। विवाह ढिलो "
            "वा कर्तव्य-बद्ध अनुभूति। मित्रता पातलो हुन्छ — तर बाँकी "
            "रहेका आजीवन।"
        ),
        "health": (
            "हाड, जोर्नी, घुँडा, दाँत, दीर्घ रोग, स्नायु थकान। शनिले "
            "पहिले उपेक्षा गरिएका कुरा सतहमा ल्याउँछ। नियमित विश्राम, "
            "सादा खाना, नियमित दिनचर्या — औषधिभन्दा महत्त्वपूर्ण।"
        ),
        "psychology": (
            "यथार्थवादी सोच — कहिले निराशामुखी पनि। ‘प्रयास नै सच्चा "
            "मुद्रा’ भन्ने मान्यता बस्छ। धैर्य बाध्य भएर पनि स्वाभाविक "
            "बन्छ। ‘अरूलाई खुसी पार्ने’ प्रवृत्ति घट्छ। दशाको अन्त्यतिर "
            "एक मौन अधिकार उत्पन्न हुन्छ — कसैले खोस्न नसक्ने।"
        ),
        "tip": (
            "शनि अनुशासन भएकालाई मित्रवत्। ‘बिस्तारै, कर्म गर, "
            "छक्याउँदै नबाट’ भन्ने शनिको शिक्षा मान्नेले अन्तिम ५-६ "
            "वर्षमा असाधारण फल पाउँछ। १-१३ वर्षमा रोपेको १४-१९ मा "
            "कटाइन्छ।"
        ),
    },
    "Rahu": {
        "headline": "राहु महादशा — १८ वर्ष",
        "overview": (
            "राहु (चन्द्रको उत्तर पात) ले महत्त्वाकाङ्क्षा, विदेशी कुरा, "
            "मोह, अकस्मात लाभ, जनसमुदाय, प्रविधि, अपरम्परागत, र "
            "भित्र दबिएका इच्छा बुझाउँछ। राहु सीधै फल दिँदैन — "
            "विस्तार गर्छ, बङ्ग्याउँछ, अनपेक्षित ढङ्गले पुरस्कार "
            "दिन्छ। राहु महादशा प्रसिद्ध रूपमा अशान्त र ‘ठूलो "
            "परिवर्तन ल्याउने’।"
        ),
        "career": (
            "विदेश यात्रा/काम, प्रविधि, सञ्चारमाध्यम, राजनीति, गुप्त "
            "विषयको अनुसन्धान, अत्याधुनिक क्षेत्र। अकस्मात उन्नति। "
            "अकस्मात पतन। पुराना योजना भग्न। सट्टेबाजी, क्रिप्टो, "
            "भाइरल ख्याति — राहुको खेल मैदान। आम्दानी असामान्य "
            "ढङ्गले बढ्न सक्छ।"
        ),
        "relationships": (
            "अपरम्परागत साझेदारी सामान्य — फरक संस्कृति, उमेर, "
            "पृष्ठभूमि। विवाह अकस्मात वा अनौठो ढङ्गले ढिलो हुन सक्छ। "
            "पुरानो मित्रता टुट्छ; पूर्णतः नयाँ वृत्त बन्छ।"
        ),
        "health": (
            "अदृश्य गुनासा, एलर्जी, निदान हुन नसक्ने समस्या, चिन्ता, "
            "लत, छाला रोग। राहुले निदान प्रक्रियालाई अल्मल्याउँछ। "
            "मानसिक स्वास्थ्यमा विशेष ध्यान चाहिन्छ — अस्थिरता, "
            "दौडिने मन, ‘छुट्न डर लाग्ने’ भाव।"
        ),
        "psychology": (
            "‘के चाहिएको हो’ थाहै नभएको भोक। ‘अझ धेरै’ — दृश्यता, "
            "धन, अनौठा अनुभव। छोटो बाटो लिन, अतिशयोक्ति गर्न, अर्को "
            "कुरामा हम्किन मन लाग्छ। पाठ: आफ्नो भोकलाई परिपक्व "
            "बनाउनुहोस्, ताकि त्यसले तपाईंलाई नचलाओस्।"
        ),
        "tip": (
            "राहु त्रिकोण (५/९) मा भए भौतिक सफलता; दुस्थान (६/८/१२) "
            "मा भए कठिन कर्म हुँदै आध्यात्मिक प्रगति; केन्द्र "
            "(१/४/७/१०) मा भए अस्थिर प्रसिद्धि। पहिलो ३-४ र अन्तिम "
            "२ वर्ष सबभन्दा अशान्त।"
        ),
    },
    "Ketu": {
        "headline": "केतु महादशा — ७ वर्ष",
        "overview": (
            "केतु (दक्षिण पात) ले वैराग्य, पूर्व जन्मको पुण्य, "
            "अन्तर्ज्ञान, मोक्ष, शुद्धिकारक हानि, एकान्त, र आध्यात्मिक "
            "गहिराइ बुझाउँछ। जहाँ राहु भोको हुन्छ, केतुले छोड्न "
            "सिकाउँछ। केतु महादशामा अनावश्यक कुराहरू झर्छन् — "
            "कहिले बिस्तारै, कहिले पीडासहित — अनि भित्र जहिल्यै "
            "रहेको कुरा देखिन्छ।"
        ),
        "career": (
            "करियर दिशाहीन लाग्न सक्छ, वा शान्त रूपमा फेरिन्छ। "
            "अनुसन्धान, उपचार, चिन्तनात्मक काम, गुप्त/आध्यात्मिक "
            "क्षेत्र, आपत्कालीन चिकित्सा, रसायन — उपयुक्त। ‘बाहिरी "
            "सफलता’ को बेला होइन — एकीकरण र छोड्ने समय। लामो "
            "जागिर अकस्मात छोड्ने सम्भावना।"
        ),
        "relationships": (
            "वैराग्य उठ्छ। लामो सम्बन्ध बिनाकारण अन्त्य हुन सक्छ — "
            "वा मौन सहचर्यमा गहिरो। एकान्त बढ्छ। केतु महादशामा "
            "विवाह विरलै, भए पनि बलियो आध्यात्मिक/भाग्यपूर्ण भेटपछि।"
        ),
        "health": (
            "रहस्यमय रोग, दीर्घ थकान, छाला/कपाल समस्या, मेरुदण्ड। "
            "केतु तल्लो शरीरको प्रतीक। ऊर्जा घट्न सक्छ। योग र ध्यान "
            "— चिकित्साभन्दा बढी राहत।"
        ),
        "psychology": (
            "सतही कुराले सन्तुष्टि नदिने अनुभूति। सामाजिक हल्लाबाट "
            "टाढिने इच्छा। मनले गहिराइ, मौन, ‘म वास्तवमा को हुँ?’ "
            "खोज्छ। पुराना पहिचानहरू गल्छन्। अरूले ‘बदलियो’ वा "
            "‘टाढियो’ ठान्न सक्छन् — तर तपाईं त पुरानो आकार छाडेर "
            "अघि बढ्नुभएको हो।"
        ),
        "tip": (
            "केतुले आध्यात्मिक उन्नति तीव्र बनाउँछ तर भौतिक "
            "महत्त्वाकाङ्क्षामा कठोर। कुण्डलीमा केतु ९/१२ मा भए यो "
            "दशाले गहिरो ज्ञान दिन्छ; ६/८ मा भए कठिन तर आत्म-शुद्धि "
            "गर्ने घटनाहरू।"
        ),
    },
}


def mahadasha_notes(lord: str, locale: str = "en") -> dict:
    src = MAHADASHA_NOTES_NE if locale == "ne" else MAHADASHA_NOTES_EN
    return src.get(lord, {})


# ============================================================================
#                  PLANET PSYCHOLOGY (in-house, in-rashi readings)
# ============================================================================

PLANET_PSYCHOLOGY_EN = {
    "Sun": (
        "The Sun is the soul (atman) and the seed of identity. Wherever the "
        "Sun sits in your chart, that area of life becomes the place where you "
        "feel called to BE someone — to claim authority, to be seen, to mean "
        "something. Inner pride and outer recognition both stem from here. "
        "If the Sun is well-placed, you carry quiet authority in this domain; "
        "if afflicted, ego-bruises and authority struggles are likely to show "
        "up here repeatedly until inner steadiness develops."
    ),
    "Moon": (
        "The Moon is the mind (manas) and the emotional waterline. Where the "
        "Moon sits, that area of life is where you FEEL most — for better or "
        "worse. It's where you seek emotional safety and where you're most "
        "vulnerable to mood. The Moon's house tells you what soothes you; its "
        "sign tells you HOW you process emotion (fast/slow, hot/cool, "
        "expressive/internal)."
    ),
    "Mars": (
        "Mars is the warrior — courage, drive, anger, the will to act. Mars's "
        "house shows where you fight, push, or get burned. Mars in a good "
        "position gives focused courage and the ability to defend yourself; "
        "afflicted, it manifests as conflict, accidents, or unprocessed anger "
        "in that domain. Mars rewards those who externalize energy through "
        "physical work, sport, or focused action."
    ),
    "Mercury": (
        "Mercury is the mind's NIMBLE part — speech, learning, calculation, "
        "humor, networks. Mercury's house is where you think, talk, and "
        "exchange most actively. Mercury takes on the qualities of nearby "
        "planets, so it rarely acts alone — read it together with its closest "
        "companion in the chart. Truth in speech and discipline in thinking "
        "are Mercury's central practices."
    ),
    "Jupiter": (
        "Jupiter (Guru) is the great teacher and benefic. Wherever Jupiter "
        "sits, life expands and protection appears. Jupiter's house is where "
        "wisdom, faith, and good fortune come most naturally — and also where "
        "you may take too much for granted. Pride in knowledge can shade into "
        "intellectual arrogance if not balanced by humility."
    ),
    "Venus": (
        "Venus (Shukra) rules love, art, comfort, and reproductive vitality. "
        "Venus's house is where you seek beauty, partnership, and pleasure. "
        "It's where life feels SWEET. Well-placed Venus brings refined "
        "relationships and aesthetic gifts; afflicted, it can manifest as "
        "unfulfilling pleasures, overindulgence, or stuck patterns in love."
    ),
    "Saturn": (
        "Saturn (Shani) is the karmic taskmaster — discipline, time, "
        "perseverance, restriction, and slow rewards. Wherever Saturn sits, "
        "life asks for patience and EARNED progress. Early difficulty in this "
        "house often turns into late, durable mastery. Saturn rewards those "
        "who don't cheat the process."
    ),
    "Rahu": (
        "Rahu (north node) is the appetite of the soul — obsession, exotic "
        "longing, ambition, and the magnetic pull toward what is unfamiliar. "
        "Rahu's house is where you HUNGER, sometimes obsessively. Big rises "
        "and big falls happen here. The growth path is to satisfy this hunger "
        "through real engagement rather than fantasy or cutting corners."
    ),
    "Ketu": (
        "Ketu (south node) is the renouncer — past-life mastery, detachment, "
        "and the urge to let things go. Ketu's house is where you already "
        "carry skill from before, but where you also feel a strange "
        "disinterest. Things in Ketu's house may come and go without holding "
        "your attention. Ketu's gift is INSIGHT in this domain; its risk is "
        "indifference where engagement is needed."
    ),
}

PLANET_PSYCHOLOGY_NE = {
    "Sun": (
        "सूर्यले हाम्रो आत्मा (भित्री ‘म’) र पहिचानको बीज बुझाउँछ। "
        "कुण्डलीमा सूर्य रहेको भाव त्यो जीवन-क्षेत्र हो जहाँ तपाईंलाई "
        "‘कोही हुनुपर्छ’ भन्ने भित्री बोलावा हुन्छ — अधिकार जमाउने, "
        "देखिने, अर्थ राख्ने ठाउँ। आन्तरिक गर्व र बाहिरी सम्मान दुवै "
        "यहीँबाट उत्पन्न। सूर्य राम्रो स्थानमा छ भने त्यस क्षेत्रमा "
        "शान्त अधिकार आउँछ; पीडित छ भने त्यहीँ अहम्‌को चोट र "
        "अधिकार सम्बन्धी द्वन्द्व बारम्बार देखिन्छ — आन्तरिक "
        "स्थिरताले मात्र शमन गर्छ।"
    ),
    "Moon": (
        "चन्द्रले हाम्रो मन र भावनालाई बुझाउँछ। चन्द्रको भाव त्यो "
        "ठाउँ हो जहाँ तपाईं सबभन्दा बढी ‘अनुभूति’ गर्नुहुन्छ — "
        "राम्रो वा नराम्रो। यो भावनात्मक सुरक्षा खोज्ने र मूडप्रति "
        "सबभन्दा कमजोर हुने ठाउँ हो। चन्द्रको भावले तपाईंलाई के "
        "कुराले सान्त्वना दिन्छ बताउँछ; राशिले तपाईं भावनालाई "
        "कसरी सम्हाल्नुहुन्छ बताउँछ।"
    ),
    "Mars": (
        "मङ्गल योद्धा हो — साहस, गति, क्रोध, र कर्म-इच्छा। मङ्गलको "
        "भावले तपाईं कहाँ लड्नुहुन्छ, धकेल्नुहुन्छ, वा डढ्नुहुन्छ "
        "देखाउँछ। राम्रो स्थानमा मङ्गल — एकाग्र साहस र आत्मरक्षा "
        "क्षमता; पीडित हुँदा त्यही क्षेत्रमा द्वन्द्व, दुर्घटना, र "
        "अप्रशोधित क्रोध। मङ्गलले शारीरिक श्रम, खेलकुद, र एकाग्र "
        "कर्ममा ऊर्जा बाहिर निकाल्नेलाई पुरस्कृत गर्छ।"
    ),
    "Mercury": (
        "बुध मनको चपल पाटो हो — वाणी, अध्ययन, हिसाब, हास्य, र "
        "सम्पर्क। बुधको भाव त्यो ठाउँ हो जहाँ तपाईं सबभन्दा बढी "
        "सोच्नुहुन्छ, बोल्नुहुन्छ, र आदानप्रदान गर्नुहुन्छ। बुध "
        "छेउछाउका ग्रहहरूको गुण लिन्छ, त्यसैले एक्लै कमै काम "
        "गर्छ। वाणीमा सत्यता र सोचमा अनुशासन — बुधको केन्द्रीय "
        "अभ्यास।"
    ),
    "Jupiter": (
        "गुरु महान् शिक्षक र शुभ ग्रह हो। गुरु जहाँ रहन्छ, त्यहाँ "
        "जीवन फैलिन्छ र संरक्षण प्रकट हुन्छ। गुरुको भावमा ज्ञान, "
        "श्रद्धा, र सौभाग्य प्राकृतिक रूपमा आउँछन् — साथै यहाँ "
        "तपाईंले धेरै कुरा ‘स्वतःसिद्ध’ ठान्ने जोखिम पनि हुन्छ। "
        "ज्ञानप्रतिको गर्व विनयको अभावमा बौद्धिक अहंकारमा बदलिन "
        "सक्छ।"
    ),
    "Venus": (
        "शुक्र प्रेम, कला, सुख, र प्रजनन-शक्तिको प्रतीक। शुक्रको "
        "भावमा सौन्दर्य, साझेदारी, र आनन्द खोजिन्छ। यो जीवनको "
        "‘मीठो’ अनुभूति हुने ठाउँ। राम्रो शुक्र — परिष्कृत सम्बन्ध "
        "र कलात्मक उपहार; पीडित हुँदा अधूरो सुख, अति-भोग, र प्रेममा "
        "अड्किने ढाँचा।"
    ),
    "Saturn": (
        "शनि कर्मको कठोर शिक्षक — अनुशासन, समय, धैर्य, बन्धन, र "
        "ढिलो फल। शनि जहाँ रहन्छ त्यहाँ जीवनले धैर्य र ‘कमाएको’ "
        "प्रगति माग्छ। त्यस भावमा सुरुको कठिनाइ ढिलो तर टिकाउ "
        "निपुणतामा बदलिन्छ। शनिले प्रक्रिया छक्याउँदै नबाट्नेलाई "
        "पुरस्कृत गर्छ।"
    ),
    "Rahu": (
        "राहु आत्माको भोक हो — मोह, विदेशी कुराको लालसा, "
        "महत्त्वाकाङ्क्षा, र अपरिचितप्रति आकर्षण। राहुको भावमा "
        "तपाईं भोको हुनुहुन्छ — कहिलेकाहीँ अति। ठूलो उन्नति र ठूलो "
        "पतन यहीँ। बढ्ने बाटो: यथार्थ संलग्नताबाट भोक तृप्त "
        "गर्नु — कल्पना वा छोटो बाटोबाट होइन।"
    ),
    "Ketu": (
        "केतु त्यागी हो — पूर्व जन्मको दक्षता, वैराग्य, र छोड्ने "
        "प्रवृत्ति। केतुको भावमा तपाईं पहिल्यै सीप ल्याउनुभएको छ, "
        "तर त्यहीँ अनौठो उदासीनता पनि अनुभव गर्नुहुन्छ। केतुको "
        "भावमा कुराहरू ध्यान नै नतानी आउँछन्-जान्छन्। केतुको "
        "उपहार त्यस क्षेत्रमा अन्तर्दृष्टि; जोखिम — संलग्नता खाँचो "
        "हुँदा उदासीनता।"
    ),
}


def planet_psychology(planet: str, locale: str = "en") -> str:
    src = PLANET_PSYCHOLOGY_NE if locale == "ne" else PLANET_PSYCHOLOGY_EN
    return src.get(planet, "")
