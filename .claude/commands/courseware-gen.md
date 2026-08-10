---
description: Generate the WSQ courseware for this course — the slide deck (PPT), Lesson Plan (LP) and Learner Guide (LG) plus their PDFs — to the published Tertiary Infotech standards, then audit with /courseware-qa.
---

# /courseware-gen — generate the PPT, LP and LG (+ PDFs)

Generate this course's **slide deck, Lesson Plan and Learner Guide**, and the **PDF of each**, to the standards at <https://tertiarycourses.github.io/wsqcourseware/>.

Arguments (optional): `$ARGUMENTS` — restrict to one artifact (`ppt`, `lp`, `lg`). With no argument, generate all three.

## Before you generate

1. **Read the course content first** — `labs/`, the existing `courseware/` artifacts, and the **assessment papers in `assessment/`**. The courseware must be **100% aligned to the labs**, and nothing may be assessed that is not taught.
2. **Use the skills, do not hand-roll**: `courseware-build` (single-source pipeline), `wsq-slides` / `tertiary-course-slides` + `tertiary-ppt-design` (deck), `wsq-lesson-plan` / `tertiary-lesson-plan` (LP), `wsq-learner-guide` / `tertiary-learner-guide` (LG). Reuse the reference deck's visual components (tile grids, flow diagrams, profile cards) — never hand-build an admin slide layout.
3. **Bump the version** and add a **Document Version Control Record** row (LP/LG). The deck's version goes on the cover **and** in the filename.

## The deck must satisfy the 7-point PPT checklist

1. **Two trainer profiles** — a general trainer **template** card **and** a named **Dr Alfred Ang** profile.
2. **Download Course Material** — a **visual** (screenshot / step graphic) showing how to download from **lms-tms.tertiaryinfotech.com**. Not a bare text link.
3. **Assessment Flow diagram** — WA → PP/CS and the sign-off path, as a flow graphic.
4. **Practice Exam** — the matching exam from **exams.tertiaryinfotech.com** on a visual slide, with the link.
5. **Version on the cover**, matching the `<<Course Title>>-vNN` filename.
6. **Only ONE version label** on the cover.
7. Every assessment carries the WSQ cover page (see `/assessment-gen`).

Plus: **all admin pages present**; Briefing **before** Assessment; the closing block runs **Assessment → Assessment Flow → Digital Attendance (TRAQOM) → Thank You**, with TRAQOM at the front **and** the end; the cover carries the course title, logos, UEN and TGS code.

> **Golden Rule — more visuals, not just text.** Tile grids, flow diagrams, profile cards and screenshots. **No bullet walls.** Every generated diagram asset in `courseware/assets/` must actually be placed on a slide.
>
> **Never paste a raster slide from another course.** Every slide's footer must carry *this* course's title and TGS code.

## The LP must

- Carry the WSQ cover page, the version-control record, a **real Word TOC field**, Arial 11pt body, and a **Page X of Y** footer on every page.
- **Carry the slide numbers**, and they must **match the current deck exactly**. **Any change to the PPT means the LP must be re-checked** — if slides were added, removed or reordered, update every activity's slide reference.
- State the real assessment instruments and their durations, and have each day total the stated instructional hours.

## The LG must

- Carry the WSQ cover page, the version-control record, a real TOC field, Arial 11pt body, and a footer on every page.
- Contain **step-by-step detailed guides to the labs**.
- Have a **Markdown mirror** (`LG-*.md`) that matches the DOCX — one LG Markdown only, no divergent copies.

## Then

1. **Generate the PDFs** for the PPT, the LP and the LG:
   `soffice --headless --convert-to pdf --outdir courseware "<file>"`
2. **Archive superseded versions** — move the old `-vNN` deck/PDF into `courseware/archive/`, and stage the moves in git so the repo carries **one live version only**.
3. **Run `/courseware-qa`** and fix every failure, regenerate, and re-run until it passes. Do not report completion on a failing audit.
4. **Never push `assessment/` to GitHub** — it is confidential and Drive-only.
