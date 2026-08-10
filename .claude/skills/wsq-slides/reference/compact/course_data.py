"""
SINGLE SOURCE OF TRUTH — Statistical Process Control (SPC) in Manufacturing.

Every artifact (PPT, LP, LG + LG.md, labs index) is generated from this module
plus data_domain1.py … data_domain5.py so they stay 100% aligned with the
approved course proposal (CA-WSQ-2020-001500) and Assessment Plan
(CRS-Q-0040896-ELE): 1 training day = 6.5 h classroom facilitation +
1.5 h assessment (WA(Q&A) 80 min + OQ 10 min).
"""

# ------------------------------------------------------------------ metadata
TITLE        = "Statistical Process Control (SPC) in Manufacturing"
SHORT_TITLE  = "Statistical Process Control (SPC) in Manufacturing"
COURSE_CODE  = "TGS-2026064862"
VERSION      = "v14"
VERSION_DATE = "8 August 2026"

# Course ed-tool: every hands-on activity is verified in NovaSPC
TOOL_NAME = "NovaSPC"
TOOL_URL  = "https://alfredang.github.io/novaspc/"
ORG          = "Tertiary Infotech Academy Pte Ltd"
UEN          = "UEN: 201200696W"
TRAINER      = "Dr. Alfred Ang"
DAYS         = 1

# Skills Framework alignment
TSC_TITLE = "Quality Process Control"
TSC_CODE  = "ELE-QUA-4006-1.1"
TSC_ABILITIES = [
    ("A1", "Determine process control function"),
    ("A2", "Identify appropriate process control system"),
    ("A3", "Set up process control system"),
    ("A4", "Verify process control performance"),
    ("A5", "Determine follow-up action required"),
]
TSC_KNOWLEDGE = [
    ("K1", "Process control setup procedures"),
    ("K2", "Process control performance metrics"),
]

# ------------------------------------------------------------------ outcomes
LEARNING_OUTCOMES = [
    "LO1: Determine process control with statistical functions",
    "LO2: Identify appropriate process control system and control charts",
    "LO3: Set up process control system and control charts",
    "LO4: Determine process capabilities and verify process control performance",
    "LO5: Analyze out of control (OOC) scenarios and determine follow-up actions required",
]

# ------------------------------------------------------------------ topics (= learning units)
TOPICS = [
    dict(num=1, code="01",
         title="Introduction to Statistical Process Control",
         subtitle="Variation · what SPC is and why manufacturing uses it · data types · distributions · Central Limit Theorem",
         weighting="ELO1 · WA 10 min",
         concepts=[
            ("Variation is everywhere", "No two units are identical — material, machine, manpower, method, measurement and environment all vary."),
            ("Common vs special causes", "Random (common) causes are inherent; assignable (special) causes are removable events SPC exists to catch."),
            ("SPC is preventive", "Monitor the process and act before defects are produced — prevention beats inspect-and-sort."),
            ("Data drives the chart", "Continuous (variable) data → Xbar-R/S charts; discrete (attribute) data → p, np, c, u charts."),
            ("Distributions model the data", "Binomial for defectives, Poisson for defects, Normal for measurements."),
            ("Central Limit Theorem", "Sample means are normally distributed for n large enough — the licence to use ±3σ limits on averages."),
         ]),
    dict(num=2, code="02",
         title="Control Charts",
         subtitle="Controlling a process · Shewhart charts · rational subgrouping · variable charts (Xbar-R, Xbar-S, I-MR) · attribute charts (p, np, c, u)",
         weighting="ELO2 · WA 20 min",
         concepts=[
            ("A control chart is a time series", "Centre line + UCL/LCL at ±3σ, plotted in time order — Shewhart's rotated normal curve."),
            ("3σ is the economic choice", "±3σ balances the cost of false alarms (α) against missed shifts (β); only 0.27% of a stable process falls outside."),
            ("Rational subgroups", "Small frequent samples (4–5 per hour) chosen so within-subgroup variation is only common cause."),
            ("Variable charts come in pairs", "Xbar-R (n ≤ 10), Xbar-S (n > 10), I-MR (n = 1) — location chart on top, dispersion chart below."),
            ("Attribute charts count", "p/np chart defectives (binomial); c/u chart defects (Poisson); np and c need constant sample size."),
            ("Read dispersion first", "Interpret the R/S chart before the Xbar chart — its limits are derived from R-bar/S-bar."),
         ]),
    dict(num=3, code="03",
         title="Setup SPC",
         subtitle="Steps to construct control charts · calculating control limits with chart constants · interpreting SPC charts",
         weighting="ELO3 · WA 20 min + OQ 5 min",
         concepts=[
            ("Implementation is a pipeline", "Select the characteristic → plan subgroups → collect ≥ 20 subgroups → compute limits → plot → interpret → act."),
            ("Limits come from the data", "CL = grand average; UCL/LCL = CL ± 3σ estimated via chart constants (A2, D3, D4, A3, B3, B4)."),
            ("Control ≠ specification", "Control limits are the voice of the process; spec limits are the voice of the customer — never draw specs on an Xbar chart."),
            ("Revise limits deliberately", "Recalculate only after a permanent, desired process change — about 20+ points of new evidence."),
            ("Special causes get removed", "Identify, annotate and exclude assignable-cause subgroups, then recompute the trial limits."),
            ("Charting alone changes nothing", "A signal is only useful if someone investigates and acts on it."),
         ]),
    dict(num=4, code="04",
         title="Process Control Capabilities",
         subtitle="Capability vs control · Cp and Cpk indices · control limits vs spec limits · Gage capability and GR&R",
         weighting="ELO4 · WA 20 min + OQ 5 min",
         concepts=[
            ("Control and capability differ", "In control = stable over time; capable = output fits the customer specification. You need both."),
            ("Cp measures precision", "Cp = (USL − LSL) / 6σ — the spec width over the process width, blind to centring."),
            ("Cpk adds accuracy", "Cpk = min(USL − μ, μ − LSL) / 3σ — penalises an off-centre mean; Cpk ≥ 1.33 is the common target."),
            ("Capability needs stability first", "Capability analysis on an out-of-control process is meaningless — stabilise, then measure."),
            ("Trust the gauge first", "GR&R quantifies how much observed variation is the measurement system itself."),
            ("Repeatability vs reproducibility", "Repeatability = same operator, same gauge; reproducibility = different operators, same gauge, same part."),
         ]),
    dict(num=5, code="05",
         title="Out of Control and Follow-Up Actions",
         subtitle="SPC rules and zones · out-of-control signals · root cause analysis (Pareto, fishbone) · follow-up and improvement (PDSA, DMAIC)",
         weighting="ELO5 · WA 10 min",
         concepts=[
            ("One primary signal", "Any point outside a control limit is the primary indicator of an assignable cause."),
            ("Patterns are signals too", "Shifts, trends, stratification, mixture and periodicity inside the limits are secondary indicators."),
            ("Zones make rules testable", "Divide the chart into zones A/B/C (1σ bands) — the Western Electric rules read runs against zones."),
            ("OOC has a procedure", "Mark the signal → hold/contain → investigate → correct the cause → document → resume charting."),
            ("Find the root cause", "Pareto separates the vital few problems; the fishbone (Ishikawa) organises causes into the 6 Ms."),
            ("Improve, then re-baseline", "Drive improvement with PDSA or DMAIC, then recalculate limits after the verified change."),
         ]),
]

# ------------------------------------------------------------------ day themes
DAY_THEMES = {
    1: "SPC fundamentals, control charts, setup, capability and OOC response",
}

# ------------------------------------------------------------------ assessment (per approved Assessment Plan)
ASSESSMENT = dict(
    written="Written Assessment WA(Q&A) — short-answer questions, 80 minutes, open book, assessor:candidate ratio 1:10.",
    practical="Oral Questioning (OQ) — 10 minutes per candidate, assessor:candidate ratio 1:1.",
    note="A minimum of 75% attendance is required and candidates must be assessed as 'Competent' to be eligible for WSQ funding.",
)

# ------------------------------------------------------------------ recommended follow-on courses
RECOMMENDED = [
    "WSQ - Certified Lean Six Sigma White Belt (CLSSWB) Training",
    "WSQ - Certified Lean Six Sigma Yellow Belt (CLSSYB) Training",
    "WSQ - Certified Lean Six Sigma Green Belt (CLSSGB) Training",
    "WSQ - Certified Lean Six Sigma Black Belt (CLSSBB) Training",
    "WSQ - Process and Design FMEA",
]
