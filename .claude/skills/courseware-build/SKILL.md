---
name: courseware-build
description: Single-source build pipeline for a WSQ course — one content module (course_data.py + data_domainN.py) drives ALL artifacts (the all-white slide deck PPT, the Lesson Plan LP, the Learner Guide LG + its Markdown mirror, and the labs/ index) so they stay 100% aligned. Generic and course-agnostic: it locates the course repo and derives every filename from course_data, so the same engine works for any WSQ course. Use to regenerate courseware after editing course content.
---

# courseware-build — single-source WSQ courseware pipeline

**Key principle:** the course material must be **100% aligned to the exam/skills domains so
students who take the course can pass the exam.** One content module drives every artifact, so
titles, lab numbering, learning outcomes, the schedule and the assessment can never drift apart.

## Layout

```
.claude/skills/courseware-build/
  SKILL.md
  assets/            brand assets (tertiary-infotech-logo.png + any course badge)
  build/
    course_data.example.py   TEMPLATE → copy to course_data.py and fill in (metadata, outcomes, topics, schedule)
    data_domain.example.py   TEMPLATE → copy to data_domain1.py … data_domainN.py (per-domain activities/labs)
    build_slides.py       generic engine → courseware/<TITLE>-<VER>.pptx  (all-white house style)
    build_lesson_plan.py  generic engine → courseware/LP-<TITLE>.docx
    build_learner_guide.py generic engine → LG-<TITLE>.md (repo root) + courseware/LG-<TITLE>.docx
    prodoc.py             shared DOCX helpers (cover page, version-control record, TOC, page numbers)
    inject_toc.py         page-numbered TOC injector (LibreOffice can't update TOC fields headless)
    build_courseware.sh   orchestrator: generate → render PDF → inject TOC → re-render
```

## How the pipeline stays generic (won't break when moved / installed elsewhere)

- Each builder finds the **course repo** by walking up from its own location for a directory that
  contains both `courseware/` and `labs/`. Override with the `COURSE_REPO` env var.
- `assets/` is resolved **relative to the skill** (co-located), never a hard-coded path.
- Output filenames are derived from `course_data.SHORT_TITLE` / `VERSION` — nothing is hard-coded to
  a specific course, so the same engine builds any WSQ course.

## Build

```bash
# one command: PPT + LP + LG as DOCX + PDF, with page-numbered TOCs
bash .claude/skills/courseware-build/build/build_courseware.sh

# or individually
python3 .claude/skills/courseware-build/build/build_slides.py
python3 .claude/skills/courseware-build/build/build_lesson_plan.py
python3 .claude/skills/courseware-build/build/build_learner_guide.py
```

Assessments (WA SAQ + PP) are built by the sibling **wsq-assessment** skill from the same course
content, so the assessment stays aligned with the slides/LG/LP.

## After a build (mandatory)

Bump `VERSION` in `course_data.py`, add a Document Version Control Record entry in the LG/LP builders,
delete superseded versioned files, then run the **courseware-qa** agent to visually audit the deck
against the WSQ hard rules before reporting completion.

## Reusing for a new course

Copy this skill into the new course's `.claude/skills/courseware-build/`, replace `course_data.py` and
`data_domainN.py` with the new course's content, drop the course badge into `assets/`, and run the
orchestrator. The engine files (build_*.py, prodoc.py, inject_toc.py, build_courseware.sh) are reused
unchanged.


## Course ed-tool (NovaSPC pattern)

If the course has a companion ed-tool (e.g. NovaSPC, https://alfredang.github.io/novaspc/, for the
SPC course), it is part of the single source: each activity dict carries the tool in `services`, a
tool step inside `steps`/`flow`, and a `csv=dict(name=..., rows=[[header],[...]])` data set. The LG
builder writes every `csv` to **labs/data/<name>.csv** and the lab files link it; the slide builder
renders an ed-tool intro slide in the admin block. Expected tool outputs (centre lines, limits,
OOC counts, Cp/Cpk/Pp/Ppk) belong in each activity's `test` so learners can self-verify.
