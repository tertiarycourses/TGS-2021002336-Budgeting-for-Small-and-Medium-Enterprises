#!/usr/bin/env python3
"""PostToolUse hook: after any courseware/assessment generator runs, require the
/courseware-qa audit of what was just produced before completion is reported."""
import json, sys

try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)

cmd = (data.get("tool_input") or {}).get("command", "") or ""

SLIDE_LP_LG = ("make_slides.py", "build_slides.py", "make_lesson_plan.py",
               "build_lesson_plan.py", "make_learner_guide.py", "build_learner_guide.py",
               "build_courseware.sh")
ASSESSMENT = ("build_assessment.py", "build_wsq_assessment.py")

hit_courseware = any(g in cmd for g in SLIDE_LP_LG)
hit_assessment = any(g in cmd for g in ASSESSMENT)

if hit_courseware or hit_assessment:
    what = []
    if hit_courseware:
        what.append(
            "the regenerated PPT/LP/LG (cover, admin slides front AND end, and every changed page): "
            "two trainer profile cards (General Trainer template + Dr Alfred Ang); Download Course "
            "Material visual (lms-tms.tertiaryinfotech.com screenshot, not a text link); Assessment "
            "Flow diagram; Practice Exam slide (exams.tertiaryinfotech.com); ONE version number on "
            "the cover matching the -vNN filename; Briefing before Assessment; TRAQOM digital "
            "attendance at front and end; version bumped with a Document Version Control Record row; "
            "superseded versions moved to courseware/archive/; no overlapping or clipped text"
        )
    if hit_assessment:
        what.append(
            "the regenerated assessment set: every paper AND answer key carries the WSQ cover page "
            "naming the correct instrument (Written Assessment (SAQ) / Practical Performance (PP) / "
            "Case Study (CS)) with no version-control record; page 2 of every question paper carries the "
            "Trainee Information + Instructions + Grading block and the scenario/questions start on "
            "page 3; the NUMBER OF QUESTIONS is unchanged "
            "from the original/reference paper; the instrument type is unchanged (CS stays CS, PP "
            "stays PP); EVERY K is covered by the WA and EVERY A is covered by the PP/CS, with the "
            "codes printed on each question and repeated in the key — FLAG any missing K or A as an "
            "issue; zero multiple choice; each task cites its lab; model-answer tables render as real "
            "tables with no wrapped columns"
        )
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": (
                "COURSEWARE POST-CHECK (mandatory): courseware was just (re)generated. Before "
                "reporting completion, run the /courseware-qa audit (or launch the courseware-qa "
                "agent with the same standards) and RENDER THE PAGES TO IMAGES to verify "
                + "; ALSO verify ".join(what) +
                ". Fix any failure, regenerate, and re-run the check until it passes."
            ),
        }
    }))
sys.exit(0)
