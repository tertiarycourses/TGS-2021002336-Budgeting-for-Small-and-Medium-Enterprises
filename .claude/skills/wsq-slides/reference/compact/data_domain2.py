"""Topic 2 — Control Charts: hands-on activities (variable + attribute charts).

Every chart activity follows the same pattern: hand-compute the statistics first,
then upload the SAME data (course CSVs in labs/data/) to the NovaSPC ed-tool
(https://alfredang.github.io/novaspc/) and let its chart panel confirm the centre
lines, control limits and out-of-control counts.
"""

# Shared thickness data set used by the Xbar-R and Xbar-S activities.
THICKNESS = [
    ["Subgroup", "X1", "X2", "X3", "X4"],
    ["1", "10.2", "10.4", "10.1", "10.3"],
    ["2", "10.5", "10.3", "10.2", "10.2"],
    ["3", "10.1", "10.0", "10.3", "10.4"],
    ["4", "10.3", "10.6", "10.4", "10.3"],
    ["5", "10.2", "10.1", "10.2", "10.3"],
]
THICKNESS_CSV = dict(name="thickness.csv", rows=THICKNESS)

DOMAIN2 = [
    dict(
        num=3, topic=2,
        title="Xbar-R Chart in NovaSPC",
        objective="LO2 — Identify appropriate process control system and control charts",
        desc="From five subgroups of coating-thickness measurements (n = 4), hand-compute the "
             "subgroup means (Xbar) and ranges (R) and their centre lines, then upload the same "
             "data to NovaSPC and generate the X̄-R chart — the tool's Statistics tiles must "
             "reproduce your numbers.",
        build="A hand-computed Xbar/R worksheet AND the matching NovaSPC X̄-R chart with its statistics tiles.",
        services="NovaSPC (https://alfredang.github.io/novaspc/), Excel / Google Sheets, labs/data/thickness.csv",
        minutes=5,
        flow=["Xbar & R per subgroup by hand", "Grand average → 10.27", "R-bar → 0.30", "Upload thickness.csv to NovaSPC", "X̄-R Chart → Generate → compare"],
        data=THICKNESS,
        csv=THICKNESS_CSV,
        steps=[
            ("Compute each subgroup mean Xbar = (X1 + X2 + X3 + X4) / 4 by hand or in a spreadsheet.", "=AVERAGE(B2:E2)   → 10.25, 10.30, 10.20, 10.40, 10.20"),
            ("Compute each subgroup range R = max − min.", "=MAX(B2:E2)-MIN(B2:E2)   → 0.3, 0.3, 0.4, 0.3, 0.2"),
            ("Compute the grand average X-double-bar and the average range R-bar.", "X̿ = 10.27   ·   R̄ = 0.30"),
            ("Open NovaSPC (https://alfredang.github.io/novaspc/) and drop labs/data/thickness.csv onto the Data Input page — the Data Preview shows 5 rows × 5 cols.", ""),
            ("Open Variable Charts → X̄-R Chart: the tool auto-detects measurement columns X1–X4 (Data Layout: Columns = Subgroup). Click Generate Chart.", ""),
            ("Compare the Statistics tiles with your worksheet: X̄̄ (CL), R̄ (CL), the UCL/LCL for both panels, n = 4, k = 5, and the X̄/R OOC counts (0).", ""),
        ],
        test="NovaSPC's X̄-R statistics show X̄̄ (CL) = 10.2700 and R̄ (CL) = 0.3000 — identical to your hand "
             "values — with X̄ UCL/LCL ≈ 10.49 / 10.05, R UCL ≈ 0.68, and 0 points out of control on both panels.",
    ),
    dict(
        num=4, topic=2,
        title="Xbar-S Chart in NovaSPC",
        objective="LO2 — Identify appropriate process control system and control charts",
        desc="Reuse the same thickness data to hand-compute each subgroup's standard deviation (S) "
             "and the S-bar centre line, then generate the X̄-s chart in NovaSPC and confirm the "
             "tool reports the same dispersion statistics.",
        build="A hand-computed Xbar/S worksheet AND the matching NovaSPC X̄-s chart.",
        services="NovaSPC (https://alfredang.github.io/novaspc/), Excel / Google Sheets, labs/data/thickness.csv",
        minutes=5,
        flow=["S = STDEV.S per subgroup", "S-bar → 0.135", "Xbar CL unchanged 10.27", "NovaSPC → X̄-s Chart → Generate", "Compare tiles; when n > 10 use S"],
        data=THICKNESS,
        csv=THICKNESS_CSV,
        steps=[
            ("Compute each subgroup's sample standard deviation with STDEV.S (divide by n − 1 = 3).", "=STDEV.S(B2:E2)   → 0.129, 0.141, 0.183, 0.141, 0.082"),
            ("Compute S-bar, the average of the five subgroup standard deviations.", "=AVERAGE(H2:H6)   → 0.135"),
            ("Confirm the Xbar centre line is unchanged: X-double-bar is still 10.27 mm.", ""),
            ("In NovaSPC (thickness.csv still loaded), open Variable Charts → X̄-s Chart and click Generate Chart.", ""),
            ("Compare the Statistics tiles with your worksheet: X̄̄ (CL), S̄ (CL) and the control limits for both panels.", ""),
            ("State when you would prefer the S chart: subgroup size n > 10, where the range wastes information.", ""),
        ],
        test="NovaSPC's X̄-s statistics show X̄̄ (CL) = 10.27 and S̄ (CL) ≈ 0.135 — matching your subgroup "
             "standard deviations 0.129 / 0.141 / 0.183 / 0.141 / 0.082 — and you can explain why S replaces R when n > 10.",
    ),
    dict(
        num=5, topic=2,
        title="I-MR (X-mR) Chart in NovaSPC",
        objective="LO2 — Identify appropriate process control system and control charts",
        desc="For a slow batch process measured one unit at a time, hand-compute the individuals' "
             "mean (I-bar) and the moving ranges (MR) between consecutive readings, then generate "
             "the X-mR chart in NovaSPC from the same eight viscosity readings.",
        build="A hand-computed I-MR worksheet AND the matching NovaSPC X-mR chart.",
        services="NovaSPC (https://alfredang.github.io/novaspc/), Excel / Google Sheets, labs/data/viscosity.csv",
        minutes=5,
        flow=["Enter 8 readings in time order", "I-bar → 25.39", "MR = |current − previous| → MR-bar 0.33", "NovaSPC → X-mR Chart → Generate", "Compare CLs and OOC counts"],
        data=[
            ["Batch", "1", "2", "3", "4", "5", "6", "7", "8"],
            ["Viscosity (cP)", "25.1", "25.4", "25.2", "25.8", "25.5", "25.3", "25.6", "25.2"],
        ],
        csv=dict(name="viscosity.csv",
                 rows=[["Batch", "Viscosity"],
                       ["1", "25.1"], ["2", "25.4"], ["3", "25.2"], ["4", "25.8"],
                       ["5", "25.5"], ["6", "25.3"], ["7", "25.6"], ["8", "25.2"]]),
        steps=[
            ("Compute I-bar, the mean of the eight individual readings.", "=AVERAGE(B2:I2)   → 25.39"),
            ("Compute each moving range MR = |current reading − previous reading| (7 values).", "=ABS(C2-B2)   → 0.3, 0.2, 0.6, 0.3, 0.2, 0.3, 0.4"),
            ("Compute MR-bar, the average of the seven moving ranges.", "=AVERAGE(...)   → 0.329"),
            ("Upload labs/data/viscosity.csv to NovaSPC's Data Input page, open Variable Charts → X-mR Chart, choose the Viscosity column and click Generate Chart.", ""),
            ("Compare the Statistics tiles: the individuals centre line ≈ 25.39 and the moving-range centre line ≈ 0.33, plus the ±3σ limits the tool derives from MR-bar.", ""),
            ("List when I-MR is the right chart: slow production, expensive/destructive testing, batch processes.", ""),
        ],
        test="NovaSPC's X-mR statistics confirm I-bar ≈ 25.39 cP and MR-bar ≈ 0.33 cP with all points in "
             "control, and you can name two situations where an I-MR chart beats an Xbar-R chart.",
    ),
    dict(
        num=6, topic=2,
        title="p Chart in NovaSPC",
        objective="LO2 — Identify appropriate process control system and control charts",
        desc="A TV assembly line inspects a sample from each batch and records the number of "
             "defective units. Hand-compute each batch's proportion defective and p-bar, then "
             "generate the p chart in NovaSPC from the same counts (binomial data: pass/fail).",
        build="A hand-computed p worksheet AND the matching NovaSPC p chart with p-bar and limits.",
        services="NovaSPC (https://alfredang.github.io/novaspc/), Excel / Google Sheets, labs/data/tv-defectives.csv",
        minutes=5,
        flow=["p = defective ÷ n per batch", "p-bar = 10/125 = 0.08", "Limits: p̄ ± 3·√(p̄(1−p̄)/n)", "NovaSPC → p Chart → Generate", "All 5 points inside"],
        data=[
            ["Batch", "Sample size n", "Defective", "Proportion p"],
            ["1", "25", "1", "0.04"],
            ["2", "25", "3", "0.12"],
            ["3", "25", "0", "0.00"],
            ["4", "25", "2", "0.08"],
            ["5", "25", "4", "0.16"],
        ],
        csv=dict(name="tv-defectives.csv",
                 rows=[["Batch", "SampleSize", "Defective"],
                       ["1", "25", "1"], ["2", "25", "3"], ["3", "25", "0"],
                       ["4", "25", "2"], ["5", "25", "4"]]),
        steps=[
            ("Compute each batch's proportion defective p = defectives ÷ sample size.", "=C2/B2   → 0.04, 0.12, 0.00, 0.08, 0.16"),
            ("Compute p-bar = total defectives ÷ total inspected.", "=SUM(C2:C6)/SUM(B2:B6)   → 10/125 = 0.08"),
            ("Preview the limits by hand: UCL/LCL = p-bar ± 3·√(p-bar(1−p-bar)/n); a negative LCL is set to 0.", "0.08 ± 3·√(0.08·0.92/25) → UCL 0.243, LCL 0"),
            ("Upload labs/data/tv-defectives.csv to NovaSPC, open Attribute Charts → p Chart, map Defective as the count and SampleSize as the sample size, then Generate Chart.", ""),
            ("Compare the tool's centre line and limits with your hand values, and check the OOC count is 0.", ""),
            ("State why the p chart tolerates varying sample sizes while the np chart does not.", ""),
        ],
        test="NovaSPC's p chart shows p-bar = 0.08 with UCL ≈ 0.243 / LCL = 0 — matching your hand "
             "proportions 0.04 / 0.12 / 0.00 / 0.08 / 0.16 — and all five batches are in control.",
    ),
    dict(
        num=7, topic=2,
        title="np Chart in NovaSPC",
        objective="LO2 — Identify appropriate process control system and control charts",
        desc="A line inspects a CONSTANT 50 units per day and records defective units. Hand-compute "
             "np-bar and the limits, then generate the np chart in NovaSPC — the count-of-defectives "
             "chart that plots numbers instead of proportions.",
        build="A hand-computed np worksheet AND the matching NovaSPC np chart.",
        services="NovaSPC (https://alfredang.github.io/novaspc/), Excel / Google Sheets, labs/data/daily-defectives.csv",
        minutes=5,
        flow=["np-bar → 4.0 (p-bar 0.08)", "UCL = np̄+3·√(np̄(1−p̄)) → 9.75", "LCL floored at 0", "NovaSPC → np Chart → Generate", "State the constant-n rule"],
        data=[
            ["Day", "Sample size n", "Defective (np)"],
            ["1", "50", "3"],
            ["2", "50", "5"],
            ["3", "50", "2"],
            ["4", "50", "6"],
            ["5", "50", "4"],
        ],
        csv=dict(name="daily-defectives.csv",
                 rows=[["Day", "SampleSize", "Defective"],
                       ["1", "50", "3"], ["2", "50", "5"], ["3", "50", "2"],
                       ["4", "50", "6"], ["5", "50", "4"]]),
        steps=[
            ("Compute np-bar, the average number of defectives per day.", "=AVERAGE(C2:C6)   → 20/5 = 4.0"),
            ("Compute p-bar = np-bar ÷ n for the limit formula.", "4/50 = 0.08"),
            ("Preview the limits by hand: np-bar ± 3·√(np-bar·(1−p-bar)).", "4 ± 3·√(4·0.92) → UCL 9.75, LCL 0"),
            ("Upload labs/data/daily-defectives.csv to NovaSPC, open Attribute Charts → np Chart and Generate Chart.", ""),
            ("Compare the tool's np-bar centre line and UCL/LCL with your hand values; confirm 0 points OOC.", ""),
            ("State the np chart's precondition (equal sample sizes) and what to use when it fails (the p chart).", ""),
        ],
        test="NovaSPC's np chart shows the centre line at 4.0 defectives/day with UCL ≈ 9.75 and LCL = 0 — "
             "matching your hand computation — and you can state why np charts require a constant sample size.",
    ),
    dict(
        num=8, topic=2,
        title="u Chart in NovaSPC",
        objective="LO2 — Identify appropriate process control system and control charts",
        desc="A PCB line counts solder DEFECTS across a varying number of boards per shift (one "
             "board can carry several defects). Hand-compute defects-per-unit u and u-bar, then "
             "generate the u chart in NovaSPC and watch its limits step with each shift's n.",
        build="A hand-computed u worksheet AND the matching NovaSPC u chart with stepped limits.",
        services="NovaSPC (https://alfredang.github.io/novaspc/), Excel / Google Sheets, labs/data/pcb-defects.csv",
        minutes=5,
        flow=["u = c ÷ n per shift", "u-bar = 80/120 = 0.667", "Limits step with each n", "NovaSPC → u Chart → Generate", "Defects vs defectives"],
        data=[
            ["Shift", "Boards inspected n", "Defects c", "u = c/n"],
            ["1", "20", "12", "0.60"],
            ["2", "25", "18", "0.72"],
            ["3", "20", "10", "0.50"],
            ["4", "30", "24", "0.80"],
            ["5", "25", "16", "0.64"],
        ],
        csv=dict(name="pcb-defects.csv",
                 rows=[["Shift", "Boards", "Defects"],
                       ["1", "20", "12"], ["2", "25", "18"], ["3", "20", "10"],
                       ["4", "30", "24"], ["5", "25", "16"]]),
        steps=[
            ("Compute each shift's defects per unit u = c ÷ n.", "=C2/B2   → 0.60, 0.72, 0.50, 0.80, 0.64"),
            ("Compute u-bar = total defects ÷ total units inspected.", "=SUM(C2:C6)/SUM(B2:B6)   → 80/120 = 0.667"),
            ("Note by hand that u-chart limits vary with each shift's n: u-bar ± 3·√(u-bar/n).", "n=20 → UCL 1.21; n=30 → UCL 1.11"),
            ("Upload labs/data/pcb-defects.csv to NovaSPC, open Attribute Charts → u Chart, map Defects and Boards, and Generate Chart.", ""),
            ("Observe the STEPPED control limits on the tool's chart — wider for small n, tighter for large n — and confirm u-bar ≈ 0.667.", ""),
            ("Contrast defects (u/c charts, Poisson) with defectives (p/np charts, binomial) in one sentence each.", ""),
        ],
        test="NovaSPC's u chart shows u-bar ≈ 0.667 defects per board with limits that step up and down with "
             "each shift's sample size — matching your hand values 0.60 / 0.72 / 0.50 / 0.80 / 0.64 — all in control.",
    ),
    dict(
        num=9, topic=2,
        title="c Chart in NovaSPC",
        objective="LO2 — Identify appropriate process control system and control charts",
        desc="A TV screen inspection counts defective pixels per TV — a constant inspection unit "
             "where each item can carry multiple defects. Hand-compute c-bar and the ±3σ limits "
             "(σ = √c-bar for Poisson counts), then confirm them on NovaSPC's c chart.",
        build="A hand-computed c worksheet AND the matching NovaSPC c chart.",
        services="NovaSPC (https://alfredang.github.io/novaspc/), Excel / Google Sheets, labs/data/pixel-defects.csv",
        minutes=5,
        flow=["c-bar → 6.5", "UCL = c̄ + 3·√c̄ = 14.15", "LCL = 0 (floored)", "NovaSPC → c Chart → Generate", "State the constant-unit rule"],
        data=[
            ["TV unit", "1", "2", "3", "4", "5", "6"],
            ["Defective pixels c", "7", "5", "9", "4", "6", "8"],
        ],
        csv=dict(name="pixel-defects.csv",
                 rows=[["TV", "Defects"],
                       ["1", "7"], ["2", "5"], ["3", "9"], ["4", "4"], ["5", "6"], ["6", "8"]]),
        steps=[
            ("Compute c-bar, the average defects per unit.", "=AVERAGE(B2:G2)   → 39/6 = 6.5"),
            ("Compute the ±3σ limits by hand with σ = √c-bar: UCL = c-bar + 3·√c-bar.", "6.5 + 3·√6.5 → UCL ≈ 14.15"),
            ("Compute LCL = c-bar − 3·√c-bar; a negative result is set to 0.", "6.5 − 7.65 < 0 → LCL = 0"),
            ("Upload labs/data/pixel-defects.csv to NovaSPC, open Attribute Charts → c Chart, choose the Defects column, and Generate Chart.", ""),
            ("Compare the tool's centre line and limits with your hand values; confirm all six TVs are in control.", ""),
            ("State the c chart's precondition: use it only when the inspection unit (subgroup size) is constant.", ""),
        ],
        test="NovaSPC's c chart shows c-bar = 6.5 defective pixels with UCL ≈ 14.15 and LCL = 0 — matching "
             "your hand computation — all six TVs in control, and you can say when a u chart must replace it.",
    ),
]
