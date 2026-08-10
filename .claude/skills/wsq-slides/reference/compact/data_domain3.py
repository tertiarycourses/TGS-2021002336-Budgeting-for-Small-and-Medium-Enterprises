"""Topic 3 — Setup SPC: hands-on activities (verified in the NovaSPC ed-tool)."""

from data_domain2 import THICKNESS, THICKNESS_CSV

DOMAIN3 = [
    dict(
        num=10, topic=3,
        title="Compute Control Limits for an Xbar-R Chart",
        objective="LO3 — Set up process control system and control charts",
        desc="Turn the Xbar-R statistics from Topic 2 into a working control chart: look up the "
             "chart constants for subgroup size n = 4 (A2, D3, D4), hand-compute the UCL and LCL "
             "for both panels, then prove your limits against NovaSPC's X̄-R chart and export the "
             "finished chart as evidence.",
        build="A fully set-up Xbar-R control chart — hand-computed limits confirmed by NovaSPC, exported as PNG.",
        services="NovaSPC (https://alfredang.github.io/novaspc/), chart constants table, labs/data/thickness.csv",
        minutes=5,
        flow=["Look up A2, D3, D4 for n = 4", "UCL(R) = D4·R̄ = 0.68", "X̿ ± A2·R̄ → 10.05 / 10.49", "NovaSPC X̄-R tiles must match", "Export the chart as PNG"],
        data=[
            ["Statistic", "Value", "Constant (n = 4)", "Value"],
            ["Grand average X-double-bar", "10.27 mm", "A2", "0.729"],
            ["Average range R-bar", "0.30 mm", "D3", "0 (none for n ≤ 6)"],
            ["Subgroup size n", "4", "D4", "2.282"],
        ],
        csv=THICKNESS_CSV,
        steps=[
            ("Start from the Topic 2 results: X-double-bar = 10.27 mm and R-bar = 0.30 mm with subgroup size n = 4.", ""),
            ("Look up the constants for n = 4 in the chart-constants table: A2 = 0.729, D3 = 0, D4 = 2.282.", ""),
            ("Compute the R-chart upper limit first: UCL(R) = D4 × R-bar; LCL(R) = 0 for n ≤ 6.", "2.282 × 0.30   → UCL(R) ≈ 0.68"),
            ("Compute the Xbar-chart limits: UCL/LCL(Xbar) = X-double-bar ± A2 × R-bar.", "10.27 ± 0.729×0.30   → UCL 10.49, LCL 10.05"),
            ("In NovaSPC (labs/data/thickness.csv loaded), open Variable Charts → X̄-R Chart → Generate Chart, and check the Statistics tiles show the SAME limits — the tool applies the same constants you just looked up.", ""),
            ("Verify the R chart is in control first (max R = 0.4 < 0.68), THEN read the Xbar panel against 10.05–10.49; both OOC tiles must read 0.", ""),
            ("Click Export (top right) to save the finished chart as a PNG — the set-up evidence a quality engineer files.", ""),
        ],
        test="Your hand limits — UCL(R) ≈ 0.68 / LCL(R) = 0 and UCL(Xbar) ≈ 10.49 / LCL(Xbar) ≈ 10.05 — match "
             "NovaSPC's X̄-R statistics tiles exactly, both OOC counts read 0, and you exported the chart as PNG.",
    ),
]
