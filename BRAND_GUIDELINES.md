# Kundali Tarjun Brand Guidelines

## Brand Position

Kundali Tarjun is a calm Vedic Kundali workspace for people who want chart calculation, structured interpretation, and learning without visual noise or fatalistic language.

The brand should feel:

- Clear, grounded, and respectful.
- Hindu-inspired without becoming decorative or crowded.
- Educational first, predictive second.
- Bilingual by default: English and Nepali should feel equally native.
- Age-aware: the same chart should be explained differently for a student, a young adult, a householder, and an elder.

## Minimalist Hindu Design Principle

Minimalist Hindu design strips away the religion's typically vibrant, chaotic palette in favor of clean lines and grounding, intentional colors. It relies on earth, fire, and spirit tones, with negative space used to make symbolic meaning visible.

Use one sacred cue at a time: a saffron mark, a thin line, a temple-flag geometry, a small bindi-like dot, or a restrained bhava-grid motif.

Avoid:

- Festival-like color mixing.
- Decorative deity art as background.
- Heavy gradients, neon glow, or crowded mandala fills.
- More than one dominant accent color in one view.

## Core Palette

| Token | Hex | Use |
|---|---:|---|
| Dharma White | `#FFFCF6` | Primary background and negative space |
| Temple Sand | `#EFE5D4` | Soft panels, dividers, warm depth |
| Terracotta | `#B86A3E` | Earth grounding, secondary accents |
| Agni Saffron | `#D96B1C` | Main accent; use sparingly for active states and key marks |
| Kalava Red | `#B3261E` | Rare auspicious emphasis, warnings, destructive actions |
| Vidya Yellow | `#D8A928` | Learning, wisdom, educational callouts |
| Cosmic Blue | `#173A63` | Depth, charts, serious interpretation, night mode support |
| Ink | `#1B1814` | Primary text |

Rules:

- Use Dharma White or Temple Sand as the default canvas.
- Use Agni Saffron as the single primary accent.
- Do not pair Saffron, Red, Yellow, and Blue together in the same component.
- Use Red only as a small signal, never as a full panel background.
- Use monochromatic shading for most layouts: white, sand, terracotta, ink.

## Typography

Nepali typography must be Unicode-first. Avoid Preeti/AMS fonts for live website UI because they rely on legacy character mapping and can break search, accessibility, copy/paste, and browser rendering.

Font research notes:

- aNepali lists Anek Devanagari as an Ek Type Unicode font with 8 styles.
- aNepali lists Mukta as an Ek Type Unicode font with 7 styles.
- aNepali lists Noto Sans Devanagari as a Google Unicode font with 9 styles.
- aNepali lists Tiro Devanagari Sanskrit as a Unicode font with 2 styles.
- aNepali’s font library includes Unicode, Preeti, and AMS categories; use Unicode for web text.

Recommended stack:

```css
--font-latin: "Plus Jakarta Sans", system-ui, sans-serif;
--font-nepali-ui: "Anek Devanagari", "Mukta", "Noto Sans Devanagari", "Nirmala UI", sans-serif;
--font-nepali-reading: "Mukta", "Anek Devanagari", "Noto Sans Devanagari", sans-serif;
--font-sacred: "Tiro Devanagari Sanskrit", "Noto Sans Devanagari", serif;
--font-mono: "JetBrains Mono", ui-monospace, monospace;
```

Usage:

- Anek Devanagari: Nepali UI labels, headings, tabs, buttons.
- Mukta: dense Nepali explanations and long interpretation text.
- Noto Sans Devanagari: fallback for maximum glyph coverage.
- Tiro Devanagari Sanskrit: rare mantra, shloka, or sacred-label moments only.
- Plus Jakarta Sans: English UI and Latin text.

Sources:

- https://www.anepali.com/font/anek-devanagari/
- https://anepali.com/font/mukta/
- https://anepali.com/font/noto-sans-devanagari/
- https://www.anepali.com/font/tiro-devanagari-sanskrit/
- https://anepali.com/

## Logo And Symbol System

The logo should be built from simple sacred geometry:

- A small orbit, bhava-grid, or circular bindu.
- Thin linework.
- No complex deity illustration.
- No heavy mandala.
- No multiple religious symbols competing together.

Preferred motif:

- A single circular bindu inside a light orbital line.
- A subtle 12-house grid reference in chart surfaces.
- A saffron line used as a directional mark.

## Layout System

The interface should behave like a quiet interpretation desk.

- Large negative space.
- One primary workspace per screen.
- Inputs grouped by birth data, place, and calculation settings.
- Result output divided into clear reading fields.
- Tables should be readable and restrained.
- Charts should sit in a clean framed surface, not a decorative shrine.

Glassmorphism can remain, but it must be quiet:

- Use translucent white/sand surfaces.
- Keep blur subtle.
- Use saffron as an edge or active state, not a glow.
- Avoid blue-heavy SaaS visuals unless used as Cosmic Blue for chart depth.

## Age-Aware Personalization

The app should adapt interpretation tone based on the age derived from the entered birth date.

| Age Band | Reading Tone | Priority |
|---|---|---|
| Under 18 | Educational and protective | Study habits, health rhythm, family guidance |
| 18-24 | Direction-setting | Education, skills, early career, emotional maturity |
| 25-34 | Formation | Career, marriage, finance, relocation, identity |
| 35-49 | Consolidation | Leadership, children, property, reputation, health maintenance |
| 50+ | Legacy | Dharma, mentoring, spiritual practice, wealth preservation |

Do not present deterministic outcomes. Use language such as:

- "This pattern tends to..."
- "The chart suggests..."
- "This house becomes active through..."
- "Timing depends on dasha and transits."

Avoid:

- "You will definitely..."
- "This guarantees..."
- "This is bad luck."
- Fear-based health, marriage, or death statements.

## Structured Interpretation Format

Every field of interest should render in the same structure.

1. Reading Method
   - Key houses.
   - Karaka planets.
   - Relevant chart layer, such as D1, D9, Dasha.

2. Age-Aware Focus
   - Explain how the reading changes for the user’s current age.

3. House + Planet Mixture
   - Explain what happens when planets occupy the relevant houses.
   - Explain where the house lord is placed.
   - Explain benefic/malefic balance.
   - Explain whether the house is kendra, trikona, dusthana, upachaya, or maraka.

4. Observed Chart Signals
   - List concrete placements and combinations found in the chart.

5. Interpretation Summary
   - Plain-language synthesis.
   - Practical caution.
   - No fatalistic claim.

## Field Mapping

| Field | Houses | Karakas | Chart Notes |
|---|---|---|---|
| Education | 4, 5, 9 | Mercury, Jupiter | Learning, intelligence, formal education, higher knowledge |
| Health | 1, 6, 8, 12 | Sun, Moon, Mars, Saturn | Vitality, illness, chronic strain, rest |
| Career | 6, 10, 11 | Sun, Saturn, Mercury, Jupiter | Work, duty, profession, gains |
| Wealth | 2, 5, 9, 11 | Jupiter, Venus | Savings, fortune, gains, luxury |
| Marriage | 2, 7, 8, 12 | Venus, Jupiter | Partnership, family integration, intimacy, D9 support |
| Family | 3, 4, 5, 9, 11 | Sun, Moon, Mars, Jupiter | Parents, siblings, children, home |
| Travel | 3, 9, 12 | Moon, Rahu | Short travel, long journeys, foreign settlement |
| Spirituality | 5, 8, 9, 12 | Jupiter, Ketu, Saturn | Devotion, occult depth, dharma, moksha |

## House And Planet Mixture Logic

Use this synthesis model:

- A planet in a house directly colors that life field.
- The house lord shows where the result travels.
- Benefics support, soften, and protect.
- Malefics activate, pressure, delay, or force discipline.
- Kendra houses make themes visible and practical.
- Trikona houses make themes meaningful, talented, or lucky.
- Dusthana houses make themes difficult but transformative.
- Upachaya houses improve with age, repetition, and effort.
- Maraka houses require careful handling of attachment, value, and health pressure.

Prediction must combine:

- Planet nature.
- House meaning.
- Lordship.
- Dignity.
- Dasha timing.
- Age context.

Never judge one factor alone.

## Voice

English voice:

- Calm.
- Precise.
- Direct.
- Educational.
- Avoid mystical exaggeration.

Nepali voice:

- सम्मानजनक।
- सरल।
- शास्त्रीय तर बुझ्न सजिलो।
- डर देखाउने भाषा होइन।
- अन्तिम निर्णय जस्तो भाषा होइन।

## Accessibility And Trust

- Keep contrast high.
- Preserve Unicode Nepali text.
- Avoid text embedded in images.
- Make all results copyable.
- Keep PDF export readable.
- Include practical disclaimers for medical, legal, financial, and marriage decisions.

