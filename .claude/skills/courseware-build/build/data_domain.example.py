"""
Per-domain hands-on activities (TEMPLATE / single source of the labs).

Copy to data_domain1.py, data_domain2.py, … (one file per domain). Each file
defines DOMAINn = [ dict(...), ... ]. The lab `num` is the GLOBAL, contiguous
lab number across all domains (1, 2, 3, …); `topic` is the domain number. The
build engine renders one PPT activity + step slides, one Learner-Guide section,
and one Lesson-Plan schedule entry per activity, and the labs/lab-NN-*.md files
carry the full commands. Keep the numbering contiguous so every artifact aligns.
"""

DOMAIN1 = [
    dict(
        num=1,                       # global contiguous lab number
        topic=1,                     # domain number (matches course_data TOPICS num)
        title="Example Lab Title",
        objective="Exam objective(s) this lab maps to.",
        desc="One-paragraph description of what the learner does in this lab.",
        build="What the learner ends up with (artifact/output).",
        services="Tool1, Tool2, Tool3",
        steps=[
            ("Step instruction shown on the slide / guide", "the command to run"),
            ("Another step (leave command empty for a discussion step)", ""),
        ],
        test="How the learner verifies success ('Test it').",
    ),
]
