---
description: Audit the WSQ courseware (PPT, LP, LG, labs) and the assessment set (WA + PP/CS) against the published Tertiary Infotech standards at https://tertiarycourses.github.io/wsqcourseware/ — renders every checked page to an image and reports pass/fail.
---

# /courseware-qa — WSQ courseware quality audit

Audit this course against the **published house standards**: <https://tertiarycourses.github.io/wsqcourseware/>. That page is the source of truth — the two mandatory checklists below (PPT 7-point, Assessment 5-point) are reproduced from it. If it has changed since this command was written, **fetch it and follow the page**, then tell the user what differs.

**Render every page you check to an image and LOOK at it.** A text-only check misses overlapping, clipped and missing visuals — exactly the defects this command exists to catch.

Arguments (optional): `$ARGUMENTS` — restrict the audit to one artifact (`ppt`, `lp`, `lg`, `labs`, `assessment`). With no argument, audit **everything**.

## How to run it

1. Locate the artifacts: deck + documents in `courseware/` (ignore `courseware/archive/`), the assessment DOCX in `assessment/`, the labs in `labs/`, and the original/reference papers in `reference/` if present.
2. Convert and render:
   - `soffice --headless --convert-to pdf --outdir <scratchpad> <file>`
   - render pages to PNG with PyMuPDF; **always** look at the cover, the admin slides (front and end), the assessment pages, and every page that changed.
3. Work the checklists. Report **PASS**, or **FAIL — file · page · defect · fix**.
4. **Fix every failure, regenerate, and re-run this audit** until it passes. Never report completion on a failing audit.
5. Delegate the page-by-page visual pass to the **courseware-qa agent** when the audit is large — it holds the same standards.

---

## A. PPT Quality Audit — 7-point mandatory checklist

1. **Two Trainer Profiles** — a **general trainer template** card **and** a named **Dr Alfred Ang** profile (two separate visual profile pages, never a bullet list).
2. **Download Course Material** — a **visual** showing learners how to download from **lms-tms.tertiaryinfotech.com** (screenshot / step graphic, not a bare text link).
3. **Assessment Flow Visual** — an **Assessment Flow diagram** mapping **WA → PP** (or WA → CS) and the **sign-off path**. A diagram, not a bulleted list.
4. **Practice Exam** — the matching **Practice Exam from exams.tertiaryinfotech.com** surfaced on a **visual slide** with the exam link.
5. **Version on Cover** — the version number is printed on the **cover page** and **matches the `<<Course Title>>-version` filename**.
6. **Single Version Number** — **only one** version label appears on the cover page (no duplicate or conflicting versions).
7. **Assessment Cover Pages** — **every** assessment (WA, PP, Case Study) carries the **WSQ cover page**.

> **Golden Rule — more visuals, not just text.** Replace bullet walls with tile grids, flow diagrams, profile cards and screenshots. Flag any bullet-wall slide.

Also check: **all admin pages are present**; no overlapping, clipped or off-slide text; the copyright line, course title and UEN appear.

---

## B. Assessment Quality Audit — 5-point mandatory checklist

1. **Same Question Count** — the assessment carries the **exact same number of questions as the original**. A changed count is a **FAIL**; compare against `reference/` (or the previous version).
2. **PP/CS Aligns to Labs** — the **Practical Performance (PP) or Case Study (CS) tasks align to the actual labs and activities**. Each task cites the lab it comes from, and the model answer is the lab procedure. Nothing assessed that was not done in class.
3. **Full K & A Coverage** — **every K and A criterion is assessed**: the **WA covers the K codes**, the **PP or CS covers the A codes**. Every question/task **prints its own codes** on the paper and the answer key repeats the identical codes. Report the coverage as a table (code → question(s) → lab/slide). **A missing K or A is a FAIL, not a caveat — flag it.**
4. **Cover Page Required** — the **Assessment, the Learner Guide and the Lesson Plan each carry the WSQ cover page**. On the assessment the cover must **name the correct instrument** — Written Assessment (SAQ) / Practical Performance (PP) / Case Study (CS) — with answer keys marked as the Answer Key. Check the section headings too, not just the cover. Assessments carry the **cover page only — no version-control record**.
5. **Preserve Instrument Type** — **if the original assessment is a Case Study, it stays a Case Study** (and a PP stays a PP). Never convert one to the other.

> **Golden Rule — mirror the original.** Same question count, same instrument, same K/A mapping and timings; **rewrite only the content**.

House additions (also FAIL if broken):

- **All questions OPEN-ENDED** — zero multiple choice anywhere.
- **Page layout is fixed** — page 1 the cover; **page 2 the Trainee Information + Instructions to Candidate (with the clickable LMS link https://lms-tms.tertiaryinfotech.com/) + the Grading / For Official Use Only block, and nothing else**; the **scenario and questions start on page 3**. (Answer keys are trainer copies: cover, then model answers.)
- **Timings match the original papers.**
- **Model-answer tables render as real tables** — no wrapped ASCII columns, no row split across a page break, nothing past the right margin.

---

## C. Lesson Plan (LP)

1. **WSQ cover page** (see B4) and the Document Version Control Record, with the **version bumped and a new row** for this change.
2. **The LP must have the slide numbers**, and the **LP slide numbers must always match the current deck**.
3. **Any change to the PPT means the LP must be re-checked** — if slides were added, removed or reordered, every activity must reference the **correct slide number**. Verify against the current deck, slide by slide.
4. Auto Table of Contents; Arial 11pt body; copyright + page-number footer on every page. Day totals match the stated instructional hours.

## D. Learner Guide (LG)

1. **WSQ cover page** + Document Version Control Record (version bumped).
2. **The LG must have step-by-step detailed guides to the labs.**
3. **A Learner Guide MD exists and mirrors the LG** — the Markdown and the DOCX/PDF must not have diverged.
4. TOC, Arial 11pt body, footer on every page; no clipped text or broken images.

## E. Labs and alignment

1. **The courseware must be 100% aligned to the labs** — deck, LG and assessment all trace to the same labs; nothing assessed or taught that the labs do not cover.

## F. Files, versions and distribution

1. **File naming convention** — e.g. the PPT is `<<Course Title>>-version`.
2. **Generate PDF for the PPT, the LG and the LP.** Confirm each PDF exists and matches the current DOCX/PPTX.
3. **One version only** in `courseware/` — superseded versions moved to `courseware/archive/`.
4. **DO NOT push the assessment to GitHub** — confidential assessment material is excluded. If `assessment/` is tracked by git or not ignored, that is a **FAIL**: report it.
5. **Assessments go to Google Drive only**; Drive sharing is **anyone-with-link (viewer)**.
6. **Learner Slide (PDF)** is taken from the **Learner Guide folder, not the trainer folder**.

---

## Report format

- A **PASS / FAIL** line per section (A–F), leading with the two mandatory checklists.
- Every failure as: `file · page · defect · fix`.
- The **K/A coverage table**.
- Overall verdict. If anything failed: fix it, regenerate, and re-run this command.
