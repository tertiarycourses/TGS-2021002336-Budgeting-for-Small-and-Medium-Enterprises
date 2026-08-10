"""Topic 1 — Introduction to Statistical Process Control: hands-on activities.

Every computation activity is verified in the course ed-tool NovaSPC
(https://alfredang.github.io/novaspc/) — learners hand-compute first, then upload
the same data as CSV and let the tool confirm every statistic.
"""

NOVASPC = "https://alfredang.github.io/novaspc/"

DOMAIN1 = [
    dict(
        num=1, topic=1,
        title="Central Limit Theorem Demo",
        objective="LO1 — Determine process control with statistical functions",
        desc="See the Central Limit Theorem in action twice: first in an interactive online "
             "simulator (any population shape → bell-shaped sample means), then on real subgroup "
             "data in NovaSPC's Distribution view, where a histogram of measurements is overlaid "
             "with the fitted normal curve.",
        build="A screenshot of a sampling distribution turned bell-shaped, plus NovaSPC's histogram + normal overlay of real subgroup data.",
        services="NovaSPC (https://alfredang.github.io/novaspc/), LTCC Online CLT simulation, web browser",
        minutes=5,
        flow=["Open the LTCC CLT simulator", "Skewed population, n = 2 → 30", "Open NovaSPC → example data", "Distribution → Generate Chart", "Bell curve over the histogram"],
        data=None,
        csv=None,
        steps=[
            ("Open the LTCC Online CLT simulation at http://www.ltcconline.net/greenl/java/Statistics/clt/cltsimulation.html and choose a clearly NON-normal (skewed) population.", ""),
            ("Run it with sample size n = 2, then n = 10, then n = 30 — watch the distribution of sample MEANS tighten into a bell shape as n grows.", ""),
            ("Open NovaSPC at https://alfredang.github.io/novaspc/ and on the Data Input page click the example dataset 'Subgroup Data (X̄-R / X̄-s)' — 20 subgroups of 5 measurements load into the Data Preview.", ""),
            ("Go to Analysis → Distribution, keep Data Column X1, and click Generate Chart.", ""),
            ("Read the histogram with the normal-curve overlay, and the Statistics tiles: Mean 25.02, Std Dev 0.16, Skewness ≈ 0 — real measurement data following the bell curve.", ""),
            ("Note the sample size at which the simulator's sampling distribution looked convincingly normal, and compare with your neighbour.", ""),
        ],
        test="For n ≥ 30 the simulator's distribution of sample means is visibly bell-shaped even for a skewed "
             "population, and NovaSPC's Distribution view shows the example measurement data hugging its normal "
             "overlay (skewness ≈ 0) — this is why control charts of subgroup AVERAGES can assume normality.",
    ),
    dict(
        num=2, topic=1,
        title="Sample Mean and Standard Deviation",
        objective="LO1 — Determine process control with statistical functions",
        desc="Compute the sample mean, range and standard deviation of a set of shaft-diameter "
             "measurements by hand, then upload the same readings to NovaSPC and let its "
             "Distribution statistics confirm every number.",
        build="The mean, range and standard deviation of a 5-reading sample, hand-computed and confirmed by NovaSPC.",
        services="NovaSPC (https://alfredang.github.io/novaspc/), Excel / Google Sheets or calculator",
        minutes=5,
        flow=["Enter the 5 readings", "Mean =AVERAGE → 12.30", "Range =MAX−MIN → 0.40", "SD =SQRT(0.10/4) → 0.158", "Verify in NovaSPC → Distribution"],
        data=[
            ["Reading", "1", "2", "3", "4", "5"],
            ["Diameter (mm)", "12.1", "12.5", "12.3", "12.2", "12.4"],
        ],
        csv=dict(name="diameter.csv",
                 rows=[["Reading", "Diameter"],
                       ["1", "12.1"], ["2", "12.5"], ["3", "12.3"], ["4", "12.2"], ["5", "12.4"]]),
        steps=[
            ("Compute the sample mean: add the five readings and divide by 5.", "=AVERAGE(12.1, 12.5, 12.3, 12.2, 12.4)   → 12.30 mm"),
            ("Compute the range: maximum reading minus minimum reading.", "=MAX(...) - MIN(...)   → 12.5 − 12.1 = 0.40 mm"),
            ("Compute each deviation from the mean, square it, and sum the squares.", "(−0.2)² + (0.2)² + 0² + (−0.1)² + (0.1)² = 0.10"),
            ("Divide the sum of squares by (n − 1) = 4 to get the sample variance, then square-root it.", "=SQRT(0.10 / 4)   → s = 0.158 mm"),
            ("Open NovaSPC (https://alfredang.github.io/novaspc/) and drag the course file labs/data/diameter.csv onto the Data Input page (or Browse files).", ""),
            ("Go to Analysis → Distribution, set Data Column to Diameter, and click Generate Chart — read the Statistics tiles.", ""),
        ],
        test="Your hand computation gives mean = 12.30 mm, range = 0.40 mm and s ≈ 0.158 mm, and NovaSPC's "
             "Distribution statistics show the identical Mean 12.30, Min 12.10 / Max 12.50 and Std Dev 0.158.",
    ),
]
