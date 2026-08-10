---
name: wsq-learner-guide
description: >
  Create a WSQ Learner Guide document (.docx) for Tertiary Infotech Academy Pte Ltd in
  the house template format. Use when building, revamping or standardising a WSQ learner
  guide. Enforces the cover page, Document Version Control Record, Word Table of Contents
  field, and a body of topics with detailed step-by-step activities.
---

> **Key principle:** The course material must be **100% aligned to the exam/skills domains** so that students who take the course can pass the exam.

# WSQ Learner Guide Skill

> **Scope:** This skill (with `wsq-slides` and `wsq-lesson-plan`) applies to **all** Tertiary
> Infotech Academy WSQ courseware design — not just one course. Swap in the relevant course
> title, TGS code and content; keep the house format below.

House format for Tertiary Infotech Academy WSQ **Learner Guide** documents. The deliverables
are a Microsoft Word `.docx` **and** a `.pdf` rendered from it — **no Markdown mirror** (HARD
RULE 1). Build the body in Markdown as a throwaway intermediate, then wrap it with the cover,
version-control record and a live Word TOC field (see [Build method](#build-method)).

## HARD RULES (non-negotiable)

1. **Deliverables are the DOCX and a PDF ONLY — never a Markdown mirror.** The only Learner
   Guide artifacts kept in the repo are `LG-<course>.docx` and `LG-<course>.pdf` (rendered from
   the DOCX). Markdown may be used **only** as a throwaway build intermediate for pandoc and MUST
   be deleted once the DOCX is built — do **not** save or commit a `Learner-Guide.md` / `LG-*.md`
   alongside the document.
2. **Cover page, Document Version Control Record and a live Word TOC field** must all be present
   (see [Document structure](#document-structure-in-order)).

## Reference implementation (shared, single-source)

The canonical **single-source build pipeline** for WSQ courseware (slide deck + Lesson
Plan + **Learner Guide** from one content module) ships with the `wsq-slides` skill at
`../wsq-slides/reference/` (installed at both `~/.claude/skills/wsq-slides/reference/` and
`.claude/skills/wsq-slides/reference/`). The Learner Guide builder is
`reference/build_learner_guide.py`; it builds the DOCX from a single source (any Markdown it
emits is a throwaway intermediate — delete it, keep only the DOCX + PDF, HARD RULE 1),
reading `course_data.py` + `data_domainN.py` (the same content that drives the deck
and Lesson Plan, so all three stay aligned) and using `prodoc.py` for the WSQ cover page,
version-control record, TOC and footer. Copy `reference/` into the course repo, edit the
data modules, and run `python3 build_learner_guide.py`. See `reference/README.md`.

## Organisation constants

- Organisation name: **Tertiary Infotech Academy Pte Ltd**
- UEN: **201200696W**
- Contact: enquiry@tertiaryinfotech.com · +65 6100 0613 · www.tertiarycourses.com.sg
- LMS (courseware + assessment): **https://lms-tms.tertiaryinfotech.com/**

## Document structure (in order)

1. **Cover page** (all centred, single page, then a page break):
   - Organisation name — 13 pt bold
   - `UEN: 201200696W` — 10 pt
   - **LEARNER GUIDE** — 26 pt bold
   - `For` — 12 pt
   - Course title — 20 pt bold
   - `TGS Ref No: <code>` — 12 pt
   - `Conducted by` — 12 pt
   - Organisation name — 13 pt bold
   - `UEN: 201200696W` — 10 pt
   - `Version <x.y>` — 12 pt bold
2. **DOCUMENT VERSION CONTROL RECORD** (bold heading + bordered table, then page break).
   Columns: **Version Number | Effective Date of Release | Summary of Included Changes | Author**.
   One row per revision; use absolute dates.
3. **TABLE OF CONTENTS** (bold heading + a Word TOC field `TOC \o "1-3" \h \z \u`, then a
   page break). Set `w:updateFields val="true"` so Word builds it on open.
4. **Body** (uses Heading 1/2/3 styles so the TOC builds, ideally two levels: Topics and
   Activities):
   - **How to Use This Guide** — short intro + what learners need before starting.
   - **Topic sections** (Heading 1 per topic) with numbered sub-sections (Heading 2/3) for
     concepts.
   - **Step-by-step Activities** (Heading 2) — each activity has a one-line **Goal**, then a
     numbered **Step-by-step** list. Include exact commands, file paths and code blocks the
     learner runs. Where a long prompt or file is needed (e.g. a build prompt or a command
     file), include it verbatim in a block quote or fenced code block.
   - **Quick Command Reference** — a two-column table of commands and what they do.
   - **Support** — contact details, LMS link, and the **assessment flow**.

## Assessment flow (include near the end)

Show the order learners follow at the assessment step:

1. **TRAQOM** — scan the TRAQOM QR code on the LMS and complete the survey.
2. **Assessment Digital Attendance**.
3. **Assessment** (Written Assessment + Practical Performance).
4. **Submit the assessment answers** on the LMS.
5. **Sign the Assessment Summary Record**.

Courseware and the assessment are on the LMS (https://lms-tms.tertiaryinfotech.com/).
For assessment timings (one-day vs two-day) see the **wsq-lesson-plan** / **wsq-slides** skills.

## Formatting rules

- **Prose prompts are NOT code.** When a step says "ask Claude …", write the prompt as a
  **block quote** (`> …`) or plain text on a single line — never inside a fenced code block.
  Fenced code blocks render in a monospace font that does not word-wrap, so in Word long
  prompts break mid-word (e.g. "val\nid"). Block quotes wrap cleanly.
- **Use fenced code blocks ONLY for real code** — shell commands, JSON/YAML, file contents
  (e.g. `CLAUDE.md`, a `.claude/commands/*.md` file, a settings snippet). Keep these lines
  short so they don't wrap awkwardly.
- Keep one consistent style across every activity in the document.

## Build method

1. Write the body in Markdown as a **temporary intermediate** (e.g. a scratch `body.md`)
   starting at `## How to Use This Guide` (no cover/title block in the body).
2. `pandoc body.md -o body.docx` for Heading-styled body content.
3. With `python-docx`, build a front-matter doc: cover page, version-control table, and a
   TOC field (raw OOXML `w:fldChar`/`w:instrText`).
4. Merge with **docxcompose** (`Composer(front).append(body)`), set `updateFields`, save.
5. Render the DOCX to PDF and QA the cover, version table, TOC page and activity formatting.
6. **Delete the intermediate Markdown** (HARD RULE 1) — keep only `LG-<course>.docx` and
   `LG-<course>.pdf`. Never leave a `Learner-Guide.md` / `LG-*.md` in the repo.

Write activities so a learner can follow them click-by-click; prefer concrete commands and
expected results over prose. Keep formatting clean and consistent with the project `template/`.

## Versioning rule (MANDATORY — every update)

Every content update to a courseware artifact MUST, in the same change:

1. **Bump the version number** (and the version date) in the generator/template — e.g. `VERSION="vNN"` for slide decks (the version is also part of the output filename), `VERSION = "N.N"` plus a new `VERSIONS` entry for DOCX documents.
2. **Document the change in the Document Version Control Record** — add a row (Version Number | Effective Date of Release | Summary of Included Changes | Author) wherever the document carries one (Learner Guide / Lesson Plan). For slide decks the bumped version must appear on the cover page and in the filename.
3. **Regenerate the outputs**, remove (`git rm`) the superseded versioned files, and update any references to the versioned filename (README, slides that cite the document, etc.).

Never regenerate an artifact with content changes while keeping the old version number.


## Course ed-tool (NovaSPC pattern)

When the course uses a companion ed-tool (e.g. NovaSPC, https://alfredang.github.io/novaspc/), the
Learner Guide must include: (1) the tool in **Before You Start — What You Need**; (2) a
**"how every activity uses it"** subsection walking the tool's actual UI (Data Input → chart panel
→ Generate Chart → Statistics tiles → Analysis → Export); (3) per-activity steps that upload the
activity's labs/data/*.csv and compare the tool's statistics with the hand computation, with the
expected numbers stated so learners can self-verify.
