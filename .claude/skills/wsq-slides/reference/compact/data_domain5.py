"""Topic 5 — Out of Control and Follow-Up Actions: hands-on activities (detected in NovaSPC)."""

DOMAIN5 = [
    dict(
        num=12, topic=5,
        title="Detect OOC and Find the Root Cause",
        objective="LO5 — Analyze out of control (OOC) scenarios and determine follow-up actions required",
        desc="A coating line drifted after the afternoon material-lot change and operator handover. "
             "First DETECT the out-of-control condition yourself: chart the shift's data in NovaSPC "
             "and watch the tool flag the OOC subgroups. Then, in small groups, build an Ishikawa "
             "fishbone across the 6 Ms to identify the most likely root causes and propose "
             "follow-up actions.",
        build="A NovaSPC X̄-R chart with the OOC points flagged, plus a completed fishbone with the top 2–3 root causes and a follow-up action for each.",
        services="NovaSPC (https://alfredang.github.io/novaspc/), labs/data/coating-ooc.csv, whiteboard / flip chart or draw.io",
        minutes=10,
        flow=["Upload coating-ooc.csv to NovaSPC", "X̄-R Chart → OOC points flagged", "Draw the spine + 6 M bones", "Ask 'why?' down the hot bones", "Top causes → follow-up actions"],
        data=None,
        csv=dict(name="coating-ooc.csv",
                 rows=[["Subgroup", "X1", "X2", "X3", "X4"],
                       ["1", "9.9", "10.1", "10.0", "10.2"],
                       ["2", "10.0", "9.8", "10.1", "10.0"],
                       ["3", "10.1", "10.0", "9.9", "10.2"],
                       ["4", "9.9", "10.0", "10.2", "10.1"],
                       ["5", "10.0", "10.1", "9.8", "10.0"],
                       ["6", "10.1", "9.9", "10.0", "10.1"],
                       ["7", "9.8", "10.0", "10.1", "9.9"],
                       ["8", "10.0", "10.2", "9.9", "10.1"],
                       ["9", "10.1", "10.0", "10.0", "9.9"],
                       ["10", "10.4", "10.5", "10.3", "10.6"],
                       ["11", "10.5", "10.4", "10.6", "10.4"],
                       ["12", "10.6", "10.4", "10.5", "10.3"]]),
        steps=[
            ("Read the scenario: subgroups 1–9 are the morning shift; subgroups 10–12 were collected after a raw-material lot change and an operator handover.", ""),
            ("Upload labs/data/coating-ooc.csv to NovaSPC's Data Input page and open Variable Charts → X̄-R Chart → Generate Chart.", ""),
            ("Read the verdict: the X̄ OOC tile is non-zero — the final subgroups sit ABOVE the upper control limit while the R chart stays in control. A level SHIFT, not extra spread.", ""),
            ("Draw the fishbone spine with the problem head: 'Coating thickness OOC — afternoon subgroups above UCL'.", ""),
            ("Label the six main bones with the 6 Ms and brainstorm causes onto each (e.g. Material: new lot viscosity; Man: handover setup skipped; Machine: nozzle wear).", ""),
            ("Ask 'why?' down each promising bone until you reach an actionable root cause, and circle the top 2–3 the team agrees on.", ""),
            ("Write one follow-up action per root cause (contain → correct → verify on the chart), and state when the control limits may be recalculated.", ""),
        ],
        test="NovaSPC flags the afternoon subgroups out of control on the X̄ panel (R panel stable — a shift in "
             "level, not spread), and your group presents a fishbone with all 6 Ms populated, 2–3 circled root "
             "causes that explain the shift, and a concrete follow-up action for each — including how you would "
             "verify the fix on the chart.",
    ),
]
