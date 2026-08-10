# COMPACT v2 deck reference — information-dense visual format

The canonical reference for the Tertiary Infotech **compact** slide format: every slide is an
information-loaded visual (chart + takeaway tiles, decision tables, formula panels, browser
mockups, one-slide activity workflows) in the style of the Business Process Automation
reference deck. Origin: the SPC in Manufacturing course (TGS-2026064862, v14) — kept here as
the worked example, exactly as the AZ-104 pipeline one level up is kept for the classic format.

## Files

| File | Role |
|---|---|
| `build_slides.py` | The deck engine + FULL v2 component library (see its docstring for the component list, data-contract additions and the hard-learned layout rules). |
| `make_charts.py` | Chart-asset generation reference: matplotlib → `courseware/assets/*.png`, drawn FROM THE SAME NUMBERS the activities use. |
| `course_data.py`, `data_domain1..5.py` | The SPC course's single-source content — the worked example of the v2 data contract (`concepts` as tuples, activities with `minutes`/`flow`/`csv`). |

## How to use for a NEW course

1. Copy this folder's `build_slides.py` + `make_charts.py` into the new course's build dir
   (usually `.claude/skills/courseware-build/build/`).
2. Replace `course_data.py` / `data_domainN.py` with the new course's content, keeping the v2
   contract: topic `concepts` = `(title, caption)` tuples; each activity carries `minutes`,
   `flow` (5 short chip labels) and optionally `csv` (written to `labs/data/`).
3. Rewrite `make_charts.py`'s figures for the new subject — keep the conventions (Arial, white
   background, brand palette, 150 dpi, `LBL_BOX` white bboxes for on-line labels, tight_layout
   with a suptitle rect) and keep every number identical to the activity data.
4. Adapt the EXAMPLE CONTENT section of `build_slides.py` (cover badge, admin text, topic
   slides) — the component functions themselves need no changes.
5. The build exports `slide_map.json` — feed it to the Lesson Plan builder so schedule rows cite
   exact slide ranges that can never drift.

## Non-negotiables carried over from the house rules

Two trainer profile cards · Download Course Material as a VISUAL (browser mockup) · ed-tool
intro slide when the course has one · ONE workflow slide per activity (never step-per-slide) ·
Briefing before Assessment · closing block Assessment → Assessment Flow → Digital Attendance →
Thank You · one version label on the cover matching the `-vNN` filename · titles ≤ ~48 chars.
