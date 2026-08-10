"""
SINGLE SOURCE OF TRUTH — course metadata (TEMPLATE).

Copy this to course_data.py in your course's
.claude/skills/courseware-build/build/ folder and fill in the values, then add
data_domain1.py … data_domainN.py (one per exam/skills domain) using
data_domain.example.py as the pattern. Every artifact (PPT, LP, LG, LG.md, labs
index) is generated from these files so they stay 100% aligned.

Guiding principle: the course material must be 100% aligned to the exam/skills
domains so students who take the course can pass the exam.
"""

# ------------------------------------------------------------------ metadata
TITLE        = "Your WSQ Course Title (CODE)"
SHORT_TITLE  = "Your WSQ Course Title (CODE)"   # used in output filenames
COURSE_CODE  = "TGS-XXXXXXXXXX"
VERSION      = "v1.0"
VERSION_DATE = "1 January 2026"
ORG          = "Tertiary Infotech Academy Pte Ltd"
UEN          = "UEN: 201200696W"
TRAINER      = "Trainer Name"
DAYS         = 3

# ------------------------------------------------------------------ outcomes
LEARNING_OUTCOMES = [
    "LO1: …",
    "LO2: …",
]

# ------------------------------------------------------------------ topics (= exam/skills domains)
# num, code, title, subtitle, weighting, concept bullets for the section
TOPICS = [
    dict(num=1, code="01",
         title="Domain 1 Title",
         subtitle="Sub-topics · shown under the section header",
         weighting="20%",
         concepts=[
            "Key concept 1 for this domain.",
            "Key concept 2 for this domain.",
         ]),
]

# ------------------------------------------------------------------ day themes (8 training hours/day)
DAY_THEMES = {
    1: "Day 1 theme",
    2: "Day 2 theme",
    3: "Day 3 theme",
}

# ------------------------------------------------------------------ assessment
ASSESSMENT = dict(
    written="Written Assessment (WA) — Short-Answer Questions (SAQ), 1 hour, open book.",
    practical="Practical Performance (PP) — hands-on tasks, 1 hour, open book.",
    note="A minimum of 75% attendance is required to be eligible for assessment and funding.",
)
