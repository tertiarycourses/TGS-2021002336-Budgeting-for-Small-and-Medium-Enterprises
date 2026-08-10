#!/usr/bin/env python3
"""PreToolUse hook: before any courseware generator runs, remind Claude to gather
context from the reference deck and the course assessments first."""
import json, sys

try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)

cmd = (data.get("tool_input") or {}).get("command", "") or ""
GENERATORS = ("make_slides.py", "build_slides.py", "make_lesson_plan.py",
              "build_lesson_plan.py", "make_learner_guide.py", "build_learner_guide.py",
              "build_assessment.py", "build_wsq_assessment.py", "build_courseware.sh")
if any(g in cmd for g in GENERATORS):
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "allow",
            "additionalContext": (
                "COURSEWARE PRE-CHECK (mandatory before generating): "
                "(1) Read the wsq-slides reference deck components "
                "(.claude/skills/wsq-slides/reference/build_slides.py or "
                "~/.claude/skills/wsq-slides/reference/) and reuse its visual components "
                "(tile_grid, flow_h, trainer_slide) — never hand-roll admin slide layouts. "
                "(2) Read the course assessment papers (assessment/ folder — WA SAQ + PP) so "
                "slide/LG/LP content stays aligned with what is assessed. "
                "(3) Bump the artifact version number AND add a Document Version Control "
                "Record entry (LG/LP); show Version vNN + date on the PPT cover; delete "
                "superseded versioned files. "
                "(4) Hard rules: About the Trainer x2 profile cards; Briefing before "
                "Assessment; Assessment Flow chevron diagram; TRAQOM digital attendance at "
                "front AND end (Assessment -> Assessment Flow -> Digital Attendance -> Thank You)."
            ),
        }
    }))
sys.exit(0)
