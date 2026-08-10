"""Topic 4 — Process Control Capabilities: hands-on activities (verified in NovaSPC)."""

DOMAIN4 = [
    dict(
        num=11, topic=4,
        title="Compute Process Capability Ratios Cp and Cpk",
        objective="LO4 — Determine process capabilities and verify process control performance",
        desc="A stable shaft-grinding process runs with mean 10.2 mm and standard deviation 0.1 mm "
             "against a customer specification of 10.0 ± 0.5 mm. Hand-compute Cp and Cpk, then run "
             "a 20-shaft sample of the same process through NovaSPC's Process Capability analysis "
             "and compare the tool's indices with yours.",
        build="Cp and Cpk computed by hand, confirmed by NovaSPC's capability analysis, and the corrective action that would raise Cpk.",
        services="NovaSPC (https://alfredang.github.io/novaspc/), Excel / Google Sheets, labs/data/shaft-diameters.csv",
        minutes=10,
        flow=["Cp = (USL−LSL)/6σ = 1.67", "CPU 1.00 · CPL 2.33 → Cpk 1.00", "NovaSPC → Process Capability", "USL 10.5 / LSL 9.5 → Calculate", "Pp/Ppk ≈ your values; fix: re-centre"],
        data=[
            ["Parameter", "Value"],
            ["Process mean μ", "10.2 mm"],
            ["Process standard deviation σ", "0.1 mm"],
            ["Upper spec limit USL", "10.5 mm"],
            ["Lower spec limit LSL", "9.5 mm"],
        ],
        csv=dict(name="shaft-diameters.csv",
                 rows=[["Shaft", "Diameter"],
                       ["1", "10.19"], ["2", "10.32"], ["3", "10.08"], ["4", "10.25"],
                       ["5", "10.15"], ["6", "10.38"], ["7", "10.12"], ["8", "10.22"],
                       ["9", "10.02"], ["10", "10.28"], ["11", "10.17"], ["12", "10.35"],
                       ["13", "10.10"], ["14", "10.21"], ["15", "10.05"], ["16", "10.30"],
                       ["17", "10.14"], ["18", "10.26"], ["19", "10.18"], ["20", "10.23"]]),
        steps=[
            ("Write down the process voice (μ = 10.2, σ = 0.1) and the customer voice (LSL 9.5, USL 10.5).", ""),
            ("Compute Cp = (USL − LSL) / 6σ — the precision-only ratio.", "(10.5 − 9.5) / (6 × 0.1)   → Cp = 1.67"),
            ("Compute CPU = (USL − μ) / 3σ and CPL = (μ − LSL) / 3σ.", "CPU = 0.3/0.3 = 1.00   ·   CPL = 0.7/0.3 = 2.33"),
            ("Take Cpk = min(CPU, CPL) and compare it with Cp.", "Cpk = 1.00  (vs Cp = 1.67)"),
            ("Upload labs/data/shaft-diameters.csv (a 20-shaft sample of this process: mean 10.20, s ≈ 0.10) to NovaSPC and open Analysis → Process Capability.", ""),
            ("Set Data Column = Diameter, USL = 10.5, LSL = 9.5, and click Calculate — read the Capability Indices (Cp, Cpk from σ̂-within; Pp, Ppk from overall s).", "Expect Pp ≈ 1.68 and Ppk ≈ 1.01 — the sample estimates of your Cp / Cpk"),
            ("Open Analysis → Distribution with USL 10.5 / LSL 9.5 to SEE the problem: the histogram sits off-centre, crowding the upper spec limit.", ""),
            ("Interpret and fix: the Cp–Cpk gap is pure mis-centring — re-centre the mean to 10.0 mm and Cpk rises to Cp with no reduction in variation.", ""),
        ],
        test="Hand values Cp = 1.67 and Cpk = 1.00 agree with NovaSPC's capability indices on the 20-shaft "
             "sample (Pp ≈ 1.68, Ppk ≈ 1.01 from the overall s), the Distribution view shows the histogram "
             "crowding the USL, and you can explain that re-centring to 10.0 mm makes Cpk equal Cp.",
    ),
]
