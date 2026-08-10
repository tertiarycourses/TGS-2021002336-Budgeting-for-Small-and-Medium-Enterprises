#!/usr/bin/env python3
"""PreToolUse hook: gate any push of courseware to the TMS/LMS (or to the Google Drive
courseware folder that the TMS links to) behind a passing /courseware-qa audit.

Nothing goes to the trainers and learners until the deck, the LP/LG and the assessment
set have been rendered, looked at, and verified against the WSQ house standards.
"""
import json, sys

try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)

tool = data.get("tool_name", "")
ti = data.get("tool_input") or {}
cmd = (ti.get("command", "") or "") if tool == "Bash" else ""
# The skills that publish courseware outward.
skill = (ti.get("skill", "") or "") if tool == "Skill" else ""

PUSH_MARKERS = (
    "lms-push", "lms_push", "gdrive-push", "gdrive_push", "gdrive-push-ato",
    "lms-tms.tertiaryinfotech.com", "tms-push", "push_to_lms", "push_to_tms",
)

# Don't fire on commands that merely mention the hooks/skills themselves (installing, editing,
# copying them) — only on an actual push.
SELF_REFS = ("courseware-tms-push-hook", ".claude/hooks", ".claude/commands", ".claude/skills")
is_self_ref = any(s in cmd for s in SELF_REFS)

if not is_self_ref and (any(m in cmd for m in PUSH_MARKERS) or any(m in skill for m in PUSH_MARKERS)):
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "allow",
            "additionalContext": (
                "TMS PUSH PRE-CHECK (mandatory): you are about to publish courseware to the "
                "TMS/LMS or its Drive folder. Courseware must NOT be pushed unless the "
                "/courseware-qa audit has PASSED on the exact files being pushed. If you have not "
                "run it in this session since the last regeneration, run /courseware-qa NOW "
                "(render the pages to images — do not check by text alone) and verify: "
                "PPT — two trainer profile cards (General Trainer template + Dr Alfred Ang); "
                "Download Course Material visual (lms-tms.tertiaryinfotech.com screenshot, not a "
                "text link); Assessment Flow diagram; Practice Exam slide "
                "(exams.tertiaryinfotech.com); exactly ONE version number on the cover, matching "
                "the -vNN filename; Briefing before Assessment; TRAQOM at front and end; "
                "superseded versions in courseware/archive/. "
                "LP/LG — WSQ cover, Document Version Control Record with the version bumped, TOC, "
                "footer on every page. "
                "ASSESSMENT — every paper and answer key carries the WSQ cover page naming the "
                "correct instrument (Written Assessment (SAQ) / Practical Performance (PP) / Case "
                "Study (CS)); page 2 of every question paper carries the Trainee Information + Instructions "
                "+ Grading block, with the scenario/questions starting on page 3; "
                "the NUMBER OF QUESTIONS is unchanged from the original/reference "
                "paper; EVERY K is covered by the WA and EVERY A by the PP/CS, with the codes "
                "printed on each question — a missing K or A is a BLOCKING issue; zero multiple "
                "choice. "
                "If any check fails: STOP, do not push, tell the user, fix it and re-run the audit."
            ),
        }
    }))
sys.exit(0)
