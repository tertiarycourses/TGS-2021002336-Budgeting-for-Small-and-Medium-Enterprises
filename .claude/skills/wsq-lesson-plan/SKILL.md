---
name: wsq-lesson-plan
description: >
  Create a WSQ Lesson Plan document (.docx) for Tertiary Infotech Academy Pte Ltd in
  the house template format. Use when building, revamping or standardising a WSQ lesson
  plan. Enforces the cover page, Document Version Control Record, Word Table of Contents
  field, the day schedule table, and the assessment scheduling rules.
---

> **Key principle:** The course material must be **100% aligned to the exam/skills domains** so that students who take the course can pass the exam.

# WSQ Lesson Plan Skill

> **Scope:** This skill (with `wsq-slides` and `wsq-learner-guide`) applies to **all**
> Tertiary Infotech Academy WSQ courseware design — not just one course. Swap in the relevant
> course title, TGS code and content; keep the house format below.

House format for Tertiary Infotech Academy WSQ **Lesson Plan** documents. The deliverables
are a Microsoft Word `.docx` **and** a `.pdf` rendered from it — **no Markdown mirror** (HARD
RULE 4). Build the body in Markdown as a throwaway intermediate, then wrap it with the cover,
version-control record and a live Word TOC field (see [Build method](#build-method)).

## HARD RULES (non-negotiable)

1. **The Lesson Plan MUST cite the slide (page) numbers of the course deck.** The trainer
   uses the LP to run the class from the slides, so every teaching session must point to the
   matching deck pages:
   - The **Daily Schedule table** carries a **`Slides`** column giving the deck page range for
     each teaching row (e.g. `Slides 21–23`); use `—` for admin/break/assessment rows.
   - The **Topic-by-topic breakdown** shows the deck slide number on each activity/lab heading
     (e.g. `### Lab 6 — Containerization with Docker · Slide 26`) and the divider + range on
     each topic/domain heading.
   - Slide numbers must be **read from the actual built deck, not hand-typed** — the deck build
     writes a `slide_map.json` (lab/topic → page number) that the LP builder consumes, so the
     two never drift. Always build the slide deck **before** the Lesson Plan.
2. **Cover page, Document Version Control Record and a live Word TOC field** must all be present
   (see [Document structure](#document-structure-in-order)).
3. **Assessment scheduling** must match the deck / `wsq-slides` skill (see below).
4. **Deliverables are the DOCX and a PDF ONLY — never a Markdown mirror.** The only Lesson Plan
   artifacts kept in the repo are `LP-<course>.docx` and `LP-<course>.pdf` (rendered from the
   DOCX). Markdown may be used **only** as a throwaway build intermediate for pandoc and MUST be
   deleted once the DOCX is built — do **not** save or commit a `Lesson-Plan.md` / `LP-*.md`
   alongside the document.

## Reference implementation (shared, single-source)

The canonical **single-source build pipeline** for WSQ courseware (slide deck + **Lesson
Plan** + Learner Guide from one content module) ships with the `wsq-slides` skill at
`../wsq-slides/reference/` (installed at both `~/.claude/skills/wsq-slides/reference/` and
`.claude/skills/wsq-slides/reference/`). The Lesson Plan builder is
`reference/build_lesson_plan.py`; it reads `course_data.py` + `data_domainN.py` (the same
content that drives the deck and guide, so all three stay aligned) and uses `prodoc.py`
for the WSQ cover page, version-control record, TOC and footer. Copy `reference/` into the
course repo, edit the data modules, and run `python3 build_lesson_plan.py`. See
`reference/README.md`.

## Organisation constants

- Organisation name: **Tertiary Infotech Academy Pte Ltd**
- UEN: **201200696W**
- Contact: enquiry@tertiaryinfotech.com · +65 6100 0613 · www.tertiarycourses.com.sg
- LMS (courseware + assessment): **https://lms-tms.tertiaryinfotech.com/**

## Document structure (in order)

1. **Cover page** (all centred, single page, then a page break):
   - Organisation name — 13 pt bold
   - `UEN: 201200696W` — 10 pt
   - **LESSON PLAN** — 26 pt bold
   - `For` — 12 pt
   - Course title — 20 pt bold
   - `TGS Ref No: <code>` — 12 pt
   - `Conducted by` — 12 pt
   - Organisation name — 13 pt bold
   - `UEN: 201200696W` — 10 pt
   - `Version <x.y>` — 12 pt bold
2. **DOCUMENT VERSION CONTROL RECORD** (bold heading + bordered table, then page break).
   Columns: **Version Number | Effective Date of Release | Summary of Included Changes | Author**.
   One row per revision; convert relative dates to absolute (e.g. "27 Jun 2026").
3. **TABLE OF CONTENTS** (bold heading + a Word TOC field `TOC \o "1-3" \h \z \u`, then a
   page break). Set `w:updateFields val="true"` so Word offers to build it on open.
4. **Body** (uses Heading 1/2/3 styles so the TOC builds):
   - **Course Overview** — 1–2 sentences on the course.
   - **Learning Outcomes** — bulleted, "By the end of this course, participants will be able to…".
   - **Daily Schedule** — a table: **Time | Duration | Topic / Activity | Method | Slides**.
     The **Slides** column is mandatory (HARD RULE 1) — the deck page range per teaching row.
     Show breaks and the assessment block explicitly. For a one-day class use 9:00 AM – 6:00 PM.
   - **Topic-by-topic breakdown** — Heading 1 per topic, with sub-points and activities; put
     the **deck slide number on every activity/lab heading** (HARD RULE 1).
   - **Resources Required** — bulleted.
   - **Assessment** — WA + PP timings, start time, open-book, funding criteria, and the LMS link.

## Assessment scheduling (must match the deck / wsq-slides skill)

- Every class ends at **6:00 PM**. Schedule content to finish before the assessment.
- **One-day class:** 1-hour assessment at **5:00 PM** = **30 min WA + 30 min PP**.
- **Two-day class:** 2-hour assessment at **4:00 PM** on the final day = **1 hr WA + 1 hr PP**.
- To make room, breaks may be **10 min** and lunch **45 min**.
- Show the assessment block on the schedule table with its start and end time.
- Courseware and the assessment are on the LMS (https://lms-tms.tertiaryinfotech.com/).

See the **wsq-slides** skill for the slide-deck equivalents and the assessment flow
(TRAQOM → Attendance → Assessment → Submit answers → Sign the record).

## Build method

1. Write the body in Markdown as a **temporary intermediate** (e.g. a scratch `body.md`)
   starting at `## Learning Outcomes` (no cover/title in the body — the cover is generated
   separately).
2. `pandoc body.md -o body.docx` to get Heading-styled body content.
3. With `python-docx`, build a front-matter doc: cover page, version-control table, and a
   TOC field (raw OOXML `w:fldChar`/`w:instrText`).
4. Merge with **docxcompose** (`Composer(front).append(body)`), set `updateFields`, save.
5. Render the DOCX to PDF and QA the cover, version table and page breaks.
6. **Delete the intermediate Markdown** (HARD RULE 4) — keep only `LP-<course>.docx` and
   `LP-<course>.pdf`. Never leave a `Lesson-Plan.md` / `LP-*.md` in the repo.

Keep prose clean: no decorative formatting; mirror the wording style of the existing
`template/` documents in the project.

## Versioning rule (MANDATORY — every update)

Every content update to a courseware artifact MUST, in the same change:

1. **Bump the version number** (and the version date) in the generator/template — e.g. `VERSION="vNN"` for slide decks (the version is also part of the output filename), `VERSION = "N.N"` plus a new `VERSIONS` entry for DOCX documents.
2. **Document the change in the Document Version Control Record** — add a row (Version Number | Effective Date of Release | Summary of Included Changes | Author) wherever the document carries one (Learner Guide / Lesson Plan). For slide decks the bumped version must appear on the cover page and in the filename.
3. **Regenerate the outputs**, remove (`git rm`) the superseded versioned files, and update any references to the versioned filename (README, slides that cite the document, etc.).

Never regenerate an artifact with content changes while keeping the old version number.
