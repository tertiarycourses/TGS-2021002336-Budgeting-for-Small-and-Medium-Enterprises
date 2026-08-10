# WSQ courseware reference pipeline (PPT + LP + LG, single source)

This is the **canonical reference implementation** for Tertiary Infotech Academy WSQ
courseware. One content module drives **all three** artifacts so the slide deck, Lesson
Plan and Learner Guide can never drift apart. It is the reference the `wsq-slides`,
`wsq-lesson-plan` and `wsq-learner-guide` skills point to.

Origin: the AZ-104 course (`TGS-2023039182`). Treat the AZ-104 content as an **example** —
copy this folder into a new course repo and swap in that course's content.

## Files

| File | Role |
|------|------|
| `course_data.py` | **Single source of truth** — metadata, learning outcomes, topics/exam areas + concept bullets, day themes, assessment strings. Edit this first. |
| `data_domain1.py … data_domain5.py` | Per-topic activity/lab data (title, desc, build, services, step-by-step + test). One module per topic; rename/renumber to match the course. |
| `prodoc.py` | Shared DOCX helpers: WSQ cover page, Document Version Control Record, TOC field, "Page X of Y" footer. Used by the LP and LG builders. |
| `build_slides.py` | **The slide deck** (python-pptx, all-white house style). Contains the full **visual component library**: `cover`, `section`, `content`, `two_col`, `cards3`, `tile_grid`, `flow_h`, `trainer_slide`, `big_statement`, `activity_overview`, `step_slide`, `test_slide`, `brk`. |
| `build_lesson_plan.py` | **The Lesson Plan** DOCX (cover, version control, TOC, colour-coded day schedule tables). |
| `build_learner_guide.py` | **The Learner Guide** as a Markdown mirror + DOCX from one source. |
| `inject_toc.py` | Post-processes the DOCX TOC field. |
| `build_courseware.sh` | Builds all artifacts in order. |

## The visual + structural rules this pipeline encodes

`build_slides.py` is the reference for the `wsq-slides` **hard rules**:

- **Always visual** — concept / outcome / process / trainer slides use `tile_grid`,
  `flow_h`, `cards3`, `two_col` or `trainer_slide`, never plain bullet walls.
- **About the Trainer ×2** — `trainer_slide(...)` profile cards: a blank *General Trainer*
  template and the *named trainer*.
- **Assessment Flow** — `flow_h(...)` horizontal numbered flow diagram.
- **TRAQOM · SSG Digital Attendance** page present at the front and again at the end.
- **Assessment admin pages repeated at the END** before *Thank You*:
  Assessment → Assessment Flow → Digital Attendance (Mandatory).
- Palette cycles blue → teal → violet → amber; footer carries course · code · © · page.

## How to build a new course

1. Copy this `reference/` folder into the new course repo (e.g. `courseware/build/`).
2. Put the Tertiary logo (and any course logo) in `courseware/assets/`.
3. Edit `course_data.py` (title, TGS code, outcomes, topics, concepts, day themes) and the
   `data_domainN.py` modules (activities/labs). Add/remove domain modules to match the
   number of topics — update the `import`s at the top of each builder accordingly.
4. Build:
   ```bash
   python3 build_slides.py          # -> courseware/<Short Title>-<ver>.pptx
   python3 build_lesson_plan.py     # -> courseware/LP-<Short Title>.docx
   python3 build_learner_guide.py   # -> LG mirror (.md) + courseware/LG-<Short Title>.docx
   # or: ./build_courseware.sh
   ```
5. Run visual QA on the deck (render slides to images, inspect) before delivering.

> Assessments (WA + PP) are produced by the separate **wsq-assessment** skill, not this
> pipeline.
