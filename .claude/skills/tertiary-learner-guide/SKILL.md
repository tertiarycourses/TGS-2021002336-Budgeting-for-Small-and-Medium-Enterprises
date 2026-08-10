---
name: tertiary-learner-guide
description: Generate a Tertiary Infotech Academy WSQ Learner Guide as BOTH an aligned Markdown file (LEARNER-GUIDE.md) and a professionally formatted Word document (.docx) from a single source so the two never diverge. The DOCX has the WSQ cover page (course title + n8n & Tertiary logos + UEN), Document Version Control Record, auto Table of Contents, Arial 11pt body, embedded workflow screenshots, and a copyright + page-number footer on every page. Use when writing or updating a detailed step-by-step learner guide for a WSQ course.
---

# WSQ Learner Guide (Markdown + DOCX, aligned)

Single-source generator: author content once in the block DSL; it emits **both**
`LEARNER-GUIDE.md` (repo root) and `courseware/<course> Learner Guide.docx`.
Template: `make_learner_guide.py` (uses `prodoc.py`).

## How to use
1. Edit `make_learner_guide.py`: set `REPO`, `TITLE`, `VERSION`, `VERSIONS`, and the content blocks `B`.
2. Use the helpers: `h1/h2/h3`, `p`, `steps`, `bullets`, `code`, `table`, `note`, `rule`, plus `("img", path, caption)` for workflow screenshots.
3. Run `python3 make_learner_guide.py`. The MD and DOCX are generated from the same `B`, so they stay aligned.
4. Each activity should embed its **workflow screenshot** right after the "Goal" section (the generator does this via `insert_images`).

## Content rules
- Detailed **step-by-step** for every activity (numbered `steps`), a **Goal**, a **What you'll build** node flow, and a **Test it** box.
- A `0. Before You Start` setup section: accounts/API keys table, run-n8n (cloud + local Docker), credentials, and a **GitHub download link** for the workflows.
- A Troubleshooting cheat-sheet and a Glossary table.
- Keep the MD and DOCX content identical (single source).

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


## Course ed-tool (NovaSPC pattern)

When the course uses a companion ed-tool (e.g. NovaSPC, https://alfredang.github.io/novaspc/), the
Learner Guide must include: (1) the tool in **Before You Start — What You Need**; (2) a
**"how every activity uses it"** subsection walking the tool's actual UI (Data Input → chart panel
→ Generate Chart → Statistics tiles → Analysis → Export); (3) per-activity steps that upload the
activity's labs/data/*.csv and compare the tool's statistics with the hand computation, with the
expected numbers stated so learners can self-verify.
