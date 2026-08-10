---
name: tertiary-course-slides
description: Generate a highly professional, all-white-theme WSQ course slide deck (python-pptx) for Tertiary Infotech Academy. Produces a cover page with course title + n8n & Tertiary logos + UEN, admin slides (digital attendance/TRAQOM, About the Trainer, Ground Rules, Lesson Plan, Learning Outcomes, Assessment), n8n key-concept slides, per-activity overview + workflow screenshot + step-by-step slides, and lunch/tea-break dividers. Use when creating or updating course/training slides for a Tertiary Infotech WSQ course.
---

# WSQ Course Slides

Generate a professional 3-day course deck with `python-pptx`. Template: `make_slides.py`.

## How to use
1. Edit `make_slides.py`: set `REPO` and the activity/concept content.
2. Run `python3 make_slides.py` → writes `courseware/n8n-slides.pptx` (150–200 slides for a 3-day course).
3. Embed real n8n **workflow screenshots** (see the `verify`/Playwright flow) or rendered diagrams from `labs/<activity>/*.png`.

## Design rules (must follow)
- **White theme only — NO dark/black slide backgrounds.** Use white slides with blue/teal accents.
- **16:9** (13.333 × 7.5 in). **Font: Arial** for every run.
- **Cover slide**: course title, the **n8n course logo** (top-right) and **Tertiary Infotech Academy logo** (top-left), `WSQ Course Code: TGS-XXXX`, `Conducted by Tertiary Infotech Academy Pte Ltd`, `UEN 201200696W`.
- **Section dividers**: white background, big faint number, blue kicker + ink title (never a full dark fill).
- **Admin front matter**: Digital Attendance (Mandatory / TRAQOM — SSG QR), About the Trainer, Let's Know Each Other, Ground Rules, LMS/TMS, Lesson Plan, Learning Outcomes, Assessment (Written SAQ 1h + Practical PP 1h, open book), Briefing for Assessment.
- **n8n key concepts**: What is n8n, nodes, triggers & actions, execution modes, data/JSON/expressions, pin data, code/edit-fields, IF/Switch, split out, merge, sub-workflows; AI agents (LLM/memory/tools/system prompt); RAG (embeddings/vector store); API & HTTP request; webhooks & auth; security/guardrails.
- **Per activity**: an overview slide (tag + description + "You'll build" + key nodes), a **workflow screenshot** slide, then **one step per slide** (big numbered badge), then a green "Test it" slide.
- **Breaks**: white slides reading "Lunch Break / 1 hour" and "Tea Break / 15 minutes".
- **Footer on every content slide**: course title · TGS code (left), `© 2026 Tertiary Infotech Academy Pte Ltd` (center), slide number (right).

## House format — Tertiary Infotech Academy Pte Ltd (WSQ)

Every generated document/deck MUST include:

- **Cover page** with: the **Course Title**; the **n8n course logo** and the **Tertiary Infotech Academy Pte Ltd logo**; `WSQ Course Code: TGS-XXXX`; `Conducted by Tertiary Infotech Academy Pte Ltd`; `UEN: 201200696W`; and a **Version** number. (Logos live in `.claude/skills/tertiary-course-slides/assets/`: `tertiary-infotech-logo.png`, `n8n-course-logo.png`.)
- **Document Version Control Record** table — columns: Version Number | Effective Date of Release | Summary of Included Changes | Author.
- **Table of Contents** — a Word TOC field that auto-updates (headings use the built-in Heading 1/2 styles; `updateFields` is enabled so Word refreshes it on open).
- **Footer on every page** — the copyright line `© 2026 Tertiary Infotech Academy Pte Ltd. All rights reserved.` and **Page X of Y** numbering. The footer URL is **www.tertiarycourses.com.sg**.
- **Font: Arial**, **11 pt** body; headings in Arial bold.
- **Brand colours**: blue `#1F6FEB`, teal `#10B981`, ink `#161B26`, grey `#5B6372`.

The reusable helper `prodoc.py` implements the cover page, version-control table, TOC field, page numbering and copyright footer — import it and call `add_cover_page`, `add_version_control`, `add_toc`, `add_page_numbers`, `enable_update_fields`, `style_headings`.

## Versioning rule (MANDATORY — every update)

Every content update to a courseware artifact MUST, in the same change:

1. **Bump the version number** (and the version date) in the generator/template — e.g. `VERSION="vNN"` for slide decks (the version is also part of the output filename), `VERSION = "N.N"` plus a new `VERSIONS` entry for DOCX documents.
2. **Document the change in the Document Version Control Record** — add a row (Version Number | Effective Date of Release | Summary of Included Changes | Author) wherever the document carries one (Learner Guide / Lesson Plan). For slide decks the bumped version must appear on the cover page and in the filename.
3. **Regenerate the outputs**, remove (`git rm`) the superseded versioned files, and update any references to the versioned filename (README, slides that cite the document, etc.).

Never regenerate an artifact with content changes while keeping the old version number.

## HARD RULES — WSQ deck admin slides (non-negotiable)

Every WSQ slide deck built with this skill MUST satisfy all of the following:

1. **About the Trainer — always TWO slides, as visual profile cards** (avatar badge + name/role panel + labelled info tiles — never plain bullets): first a blank **General Trainer** template (grey theme, "?" avatar, fill-in lines: Name, Title/Designation, Qualifications, Areas of expertise, Training & industry experience, Contact) for the trainer to complete, then the **named trainer** (accent theme, initials avatar, filled tiles).
2. **Assessment Flow — a horizontal numbered flow diagram** (numbered chips joined by chevrons): TRAQOM → Assessment digital attendance → Sit WA then PP → Submit on the LMS → Sign the Assessment Summary Record.
3. **TRAQOM · SSG Digital Attendance slide** at the FRONT of the deck and repeated at the END.
4. **Assessment admin pages repeated at the END**, immediately before Thank You, in this order: Assessment (reminder) → Assessment Flow (flow diagram) → Digital Attendance (Mandatory).
5. **Briefing for Assessment comes BEFORE the Assessment slide** in the front admin section.
6. **Use the wsq-slides visual components everywhere** (tile_grid, flow_h, trainer_slide, cards, flows — port them from the wsq-slides skill's reference/build_slides.py); never hand-roll plain bullet walls for admin slides (Ground Rules, Learning Outcomes, etc.).

## GitHub Pages — NOT used for WSQ courseware repos

WSQ courseware repositories (TGS-coded course repos with `courseware/` + `labs/`) do
**not** deploy to GitHub Pages. Do not create a `deploy-pages.yml` workflow, do not
enable the Pages site, and skip any "deploy static site" phase for these repos. The
repo homepage should point to the course page on www.tertiarycourses.com.sg instead.
Lab web apps are run locally by learners (or demoed via localhost) — they don't need
a hosted deployment.


## Course ed-tool integration (NovaSPC pattern)

When the course has a companion **ed-tool** (e.g. the SPC course uses **NovaSPC**,
https://alfredang.github.io/novaspc/ — CSV upload, c/u/np/p and X-mR/X̄-R/X̄-s chart panels,
Distribution and Process Capability analysis, PNG/CSV export), the deck must:

1. Carry ONE **ed-tool introduction slide** in the admin block (after Download Course Material):
   a browser-mockup card of the tool (URL bar + left navigation + statistics tiles) beside a
   numbered "how every activity uses it" tile column — same visual grammar as the LMS slide.
   Never a bare text link.
2. Name the ed-tool (with URL) and the activity's data file (labs/data/*.csv) in every
   **activity workflow slide's Tools line**, and put the tool step inside the workflow strip
   (e.g. "Upload thickness.csv to NovaSPC" → "X̄-R Chart → Generate → compare").
3. Keep the pedagogy **hand-compute first, tool confirms second** — the workflow strip shows the
   hand computation before the tool verification, so the tool never replaces the taught method.

## COMPACT v2 format — preferred for new decks

For new or revamped decks, prefer the **compact information-dense format** in
`reference/compact/` (worked example: the SPC course, TGS-2026064862 v14; visual grammar of the
Business Process Automation reference deck). It extends the classic component set with:

- `img_points` (chart image + colour-coded takeaway tiles — the workhorse concept slide) and
  `img_full` (full-width visual + caption band), fed by matplotlib assets from
  `reference/compact/make_charts.py` drawn from the SAME numbers the activities use
- `table_slide` (styled decision/comparison tables) and `formula_slide` (dark formula panels)
- `activity_slide` — ONE workflow slide per hands-on activity (badge + scenario + 5-chip
  numbered strip + "YOU'LL PRODUCE" band + Tools line); never step-per-slide runs
- browser-mockup slides for the LMS portal and any course ed-tool (never a bare text link)
- `slide_map.json` export so the Lesson Plan cites exact slide ranges

Layout rules that keep QA green: titles ≤ ~48 chars (or they wrap into the divider);
`tight_layout(rect=[0,0,1,0.86])` under matplotlib suptitles; `h_pad ≥ 2` for stacked subplots;
white bbox behind any label sitting ON a chart line; Arial-only glyphs; every generated asset
must be placed on a slide; aspect-fit images with PIL — never stretch.
