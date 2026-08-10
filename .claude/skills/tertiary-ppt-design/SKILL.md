---
name: tertiary-ppt-design
description: Best-practice design system and rules for building highly professional, visual training/course slide decks with python-pptx (Tertiary Infotech house style). Use whenever creating or polishing a .pptx deck so the result is clean, white-theme, visual, and consistent — large readable fonts, brand colours, icon/card layouts, screenshots and diagrams instead of walls of text. Pair with the tertiary-course-slides skill.
---

# PPT Design & Presentation — Best Practices

Apply these when generating or refining a course/training deck (python-pptx).

## Theme & format
- **16:9** (13.333 × 7.5 in). **All-white slides — never dark/black backgrounds.**
- **Font: Arial** for every run. Brand colours: blue `#1F6FEB`, teal `#10B981`, ink `#161B26`, grey `#5B6372`, violet `#7C3AED`, light `#F5F8FC`.
- Cover with the **course title + n8n & Tertiary Infotech Academy logos + UEN**; footer on every content slide = course/code (left), `© 2026 Tertiary Infotech Academy Pte Ltd` (center), slide number (right).

## Typography (make it presentable — large fonts)
- Slide **title ≈ 28–30 pt**, kicker label ≈ 14 pt (brand colour, uppercase).
- **Body bullets ≈ 18–20 pt** (never below 16 pt). Two-column body ≈ 17 pt. Card body ≈ 14 pt.
- Section dividers: title ≈ 40 pt, big faint topic number ≈ 72 pt.
- Step slides: one step, big numbered circle + step text ≈ 24 pt.

## Be visual, not wordy
- **≤ 5 bullets per slide**, one idea per bullet. Split dense slides.
- Prefer **layouts over paragraphs**:
  - **3 colour cards** for "features / why / pillars" (heading + 3 short lines each).
  - **Two-column** for comparisons (GET vs POST, model vs memory, in-memory vs Pinecone).
  - **Big-statement** slides (one large sentence) to punctuate sections.
  - **Screenshot slides**: real product screenshots (websites, the n8n canvas) beside short steps.
  - **Diagrams**: redraw concepts in the brand theme (e.g. a RAG flow) — never paste watermarked images.
- Add a **workflow screenshot** for every hands-on activity; a **gallery** for sample student work.

## Structure of a course deck
1. Cover → admin (digital attendance/TRAQOM, trainer, ground rules, lesson plan, learning outcomes, assessment).
2. Per topic: a **section divider**, concept slides (what / why / how, with cards & comparisons), then per activity: **overview → workflow screenshot → one-step-per-slide → green "Test it"**.
3. **Lunch/tea-break** divider slides; recap slides at the end of each day; a Thank-You close.

## Consistency & alignment
- Activity titles and topic numbering must **match the Learner Guide and Lesson Plan exactly**.
- Reuse helper functions (`content`, `two_col`, `cards3`, `website_slide`, `gallery_slide`, `img_slide`, `big_statement`, `section`, `step_slide`) so spacing/fonts stay uniform.

Implementation lives in the **tertiary-course-slides** skill (`make_slides.py`).

## COMPACT v2 component specs (proven on the SPC deck, TGS-2026064862)

Full runnable reference: `wsq-slides/reference/compact/` (build_slides.py + make_charts.py +
worked-example content). Key measurements (16:9, 13.333×7.5 in, content area x 0.85–12.48 in,
y 1.95–6.65 in, footer at y 7.05):

- **img_points**: image aspect-fit to ~7.0 in wide × 4.75 in tall on the left; 3–4 takeaway
  tiles on the right, each `LIGHT` panel + 0.09 in colour bar, title 14 pt bold in the palette
  colour, caption 12 pt ink. THE default concept slide — beats any bullet wall.
- **img_full**: image aspect-fit to 11.6 in, centred; optional caption band (LIGHT, 14 pt) at
  y 6.3. For family portraits (all four attribute charts) and big comparisons.
- **table_slide**: header row in BLUE with white 13 pt bold; body rows alternate LIGHT/WHITE
  with LINE borders; first column bold; per-column width fractions; ≤ 8 rows.
- **formula_slide**: 2–3 panels; each LIGHT with 0.1 in top colour bar, heading 16 pt, formula
  in a NAVY box (15 pt bold, light-blue #9CDCFE), caption 12.5 pt grey.
- **activity_slide**: teal kicker `TOPIC 0X · HANDS-ON ACTIVITY`; top-right badge
  `ACTIVITY N · M MIN`; scenario ≤ 3 lines at 15 pt; 5 chips (0.56 in numbered circles, labels
  11.5 pt, ▶ connectors); green `YOU'LL PRODUCE` band; grey Tools line naming the ed-tool +
  data file + "Full step-by-step guide: Learner Guide, Activity N".
- **browser-mock slides** (LMS / ed-tool): white card with traffic-light dots, URL pill, nav or
  content mock inside; numbered how-to tiles on the right; one summary line under both.
- **Chart assets** (make_charts.py): matplotlib, Arial, white bg, palette #1F6FEB/#10B981/
  #7C3AED/#F59E0B (+#DC2626 for limits/defects), 150 dpi, bbox_inches="tight". Draw from the
  SAME numbers the labs use. Pitfalls that cost QA rounds: suptitle needs
  `tight_layout(rect=[0,0,1,0.86])`; stacked subplots need `h_pad ≥ 2`; labels on lines need a
  white bbox; avoid non-Arial glyphs (e.g. superscript minus U+207B).
- **Titles ≤ ~48 chars** at 28 pt or they wrap into the divider rule.
- **slide_map.json**: `mark(key)` before each section/activity; the LP builder reads it so
  schedule slide references never drift from the deck.
