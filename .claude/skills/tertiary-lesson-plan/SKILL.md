---
name: tertiary-lesson-plan
description: Generate a Tertiary Infotech Academy WSQ Lesson Plan as a professionally formatted Word document (.docx) with the house cover page (course title + n8n & Tertiary logos + UEN), Document Version Control Record, auto Table of Contents, Arial 11pt body, colour-coded daily schedule tables, and a copyright + page-number footer on every page. Each training day totals exactly 8 instructional hours (9:30am–6:30pm with a 1-hour lunch; tea breaks counted within). Use when creating or updating a lesson plan / training schedule for a WSQ course.
---

# WSQ Lesson Plan (DOCX)

Generate the 3-day lesson plan DOCX. Template: `make_lesson_plan.py` (uses `prodoc.py`).

## How to use
1. Edit `make_lesson_plan.py`: set `REPO_DIR`, course title, `LP_VERSIONS`, and the per-session schedule tables.
2. Run `python3 make_lesson_plan.py` → writes `courseware/Lesson Plan - <course>.docx`.
3. The script asserts **each day = 480 minutes (8 hours)** excluding the 1-hour lunch.

## Schedule rules
- Daily window **9:30am – 6:30pm**, **1-hour lunch** (e.g. 1:00–2:00pm). Each day = **8 instructional hours**; short tea breaks are counted within the day.
- Each session is a table: **Time | Topic / Activity | Duration**. Topic rows are highlighted; lunch/tea-break rows are tinted.
- Include Course Overview, Learning Outcomes, the daily schedule, a Tools/Resources table, and an Assessment section.
- Verify every day sums to 480 minutes before saving.

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
