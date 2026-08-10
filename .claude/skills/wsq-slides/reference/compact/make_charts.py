#!/usr/bin/env python3
"""CHART-ASSET reference (companion to build_slides_compact.py) — worked example
from the SPC course. Pattern: matplotlib, Arial, white background, brand palette,
150 dpi, saved to courseware/assets/ and placed via img_points()/img_full().

Generate the SPC chart/diagram assets placed on the course slides.

Every image is drawn from the SAME numbers used in the hands-on activities
(data_domainN.py) so the visuals, labs, LG and assessment stay aligned.
Output: courseware/assets/*.png (150 dpi, white background, Arial).
"""
import os, sys
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch

HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)

def _find_repo(start):
    env = os.environ.get("COURSE_REPO")
    if env and os.path.isdir(env): return env
    d = start
    for _ in range(8):
        d = os.path.dirname(d)
        if os.path.isdir(os.path.join(d, "courseware")) and os.path.isdir(os.path.join(d, "labs")): return d
    return os.path.dirname(os.path.dirname(HERE))

REPO = _find_repo(HERE)
OUT = os.path.join(REPO, "courseware", "assets")
os.makedirs(OUT, exist_ok=True)

BLUE="#1F6FEB"; TEAL="#10B981"; VIOLET="#7C3AED"; AMBER="#F59E0B"; RED="#DC2626"
INK="#161B26"; GREY="#5B6372"; LIGHT="#F5F8FC"; LINE="#E2E8F0"

plt.rcParams.update({
    "font.family": "Arial", "font.size": 11, "axes.edgecolor": GREY,
    "axes.labelcolor": INK, "xtick.color": GREY, "ytick.color": GREY,
    "axes.titlesize": 13, "axes.titleweight": "bold", "figure.facecolor": "white",
    "axes.facecolor": "white", "axes.spines.top": False, "axes.spines.right": False,
})

LBL_BOX = dict(boxstyle="round,pad=0.22", fc="white", ec="none", alpha=0.9)

def save(fig, name, w=7.2, h=4.0):
    fig.set_size_inches(w, h)
    fig.savefig(os.path.join(OUT, name), dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("  asset:", name)

def norm_pdf(x, mu=0.0, s=1.0):
    return np.exp(-0.5*((x-mu)/s)**2)/(s*np.sqrt(2*np.pi))

# ---------------------------------------------------------------- 1. normal distribution 68-95-99.7
fig, ax = plt.subplots()
x = np.linspace(-4, 4, 400); y = norm_pdf(x)
ax.plot(x, y, color=BLUE, lw=2.5)
for k, col, alpha in [(3, AMBER, 0.15), (2, TEAL, 0.22), (1, BLUE, 0.30)]:
    xs = np.linspace(-k, k, 200)
    ax.fill_between(xs, norm_pdf(xs), color=col, alpha=alpha, lw=0)
for k, label, ypos in [(1, "68.3% within ±1σ", 0.150), (2, "95.4% within ±2σ", 0.065), (3, "99.73% within ±3σ", 0.014)]:
    ax.annotate("", xy=(-k, ypos), xytext=(k, ypos), arrowprops=dict(arrowstyle="<->", color=INK, lw=1.2))
    ax.text(0, ypos+0.008, label, ha="center", fontsize=10.5, color=INK, fontweight="bold")
ax.text(3.05, norm_pdf(3.0)+0.02, "only 0.27%\noutside ±3σ", fontsize=9.5, color=RED, fontweight="bold")
ax.set_xticks(range(-4,5)); ax.set_xticklabels(["-4σ","-3σ","-2σ","-1σ","μ","+1σ","+2σ","+3σ","+4σ"])
ax.set_yticks([]); ax.set_title("Normal (Gaussian) Distribution — the bell curve behind SPC")
save(fig, "dist_normal.png")

# ---------------------------------------------------------------- 2. binomial
from math import comb
fig, ax = plt.subplots()
n, p = 25, 0.08
ks = np.arange(0, 11)
pmf = [comb(n,k)*p**k*(1-p)**(n-k) for k in ks]
ax.bar(ks, pmf, color=BLUE, alpha=0.85, label=f"n=25, p=0.08 (TV batch)")
n2, p2 = 25, 0.3
pmf2 = [comb(n2,k)*p2**k*(1-p2)**(n2-k) for k in ks]
ax.bar(ks+0.0, pmf2, color=TEAL, alpha=0.45, label="n=25, p=0.30")
ax.set_xlabel("Number of defectives k in the sample"); ax.set_ylabel("Probability")
ax.legend(frameon=False); ax.set_title("Binomial Distribution — counts of DEFECTIVES (p / np charts)")
ax.text(0.98, 0.55, "mean = np\nvariance = np(1−p)", transform=ax.transAxes, ha="right",
        fontsize=11, color=INK, bbox=dict(boxstyle="round,pad=0.5", fc=LIGHT, ec=LINE))
save(fig, "dist_binomial.png")

# ---------------------------------------------------------------- 3. poisson
from math import exp, factorial
fig, ax = plt.subplots()
ks = np.arange(0, 16)
for lam, col in [(1, BLUE), (4, TEAL), (8, VIOLET)]:
    pmf = [exp(-lam)*lam**k/factorial(k) for k in ks]
    ax.plot(ks, pmf, "o-", color=col, lw=1.8, ms=5, label=f"λ = {lam}")
ax.set_xlabel("Number of defects k per unit / interval"); ax.set_ylabel("Probability")
ax.legend(frameon=False, title="expected defects λ")
ax.set_title("Poisson Distribution — counts of DEFECTS (c / u charts)")
ax.text(0.98, 0.6, "P(k) = λ^k e^(−λ) / k!\nmean = variance = λ", transform=ax.transAxes, ha="right",
        fontsize=11, color=INK, bbox=dict(boxstyle="round,pad=0.5", fc=LIGHT, ec=LINE))
save(fig, "dist_poisson.png")

# ---------------------------------------------------------------- 4. CLT
rng = np.random.default_rng(7)
pop = rng.exponential(1.0, 200000)
fig, axes = plt.subplots(1, 3)
axes[0].hist(pop, bins=60, color=GREY, alpha=0.8, density=True)
axes[0].set_title("Population\n(skewed, NOT normal)", fontsize=11)
for ax_, n, col in [(axes[1], 5, TEAL), (axes[2], 30, BLUE)]:
    means = rng.exponential(1.0, (20000, n)).mean(axis=1)
    ax_.hist(means, bins=60, color=col, alpha=0.85, density=True)
    ax_.set_title(f"Means of samples, n = {n}", fontsize=11)
for ax_ in axes: ax_.set_yticks([])
axes[2].text(0.96, 0.68, "n ≥ 30 →\nbell shape", transform=axes[2].transAxes, ha="right",
             fontsize=10, fontweight="bold", color=INK,
             bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="none", alpha=0.85))
fig.suptitle("Central Limit Theorem — sample means become normal, whatever the population", fontweight="bold", fontsize=12.5)
fig.set_size_inches(9.0, 3.2)
fig.tight_layout(rect=[0, 0, 1, 0.86])
save(fig, "clt.png", w=9.0, h=3.2)

# ---------------------------------------------------------------- 5. control chart anatomy (+ rotated normal origin)
fig = plt.figure()
gs = fig.add_gridspec(1, 2, width_ratios=[1, 4], wspace=0.02)
axn = fig.add_subplot(gs[0]); axc = fig.add_subplot(gs[1])
rng2 = np.random.default_rng(3)
data = 10.27 + rng2.normal(0, 0.07, 24)
CL, UCL, LCL = 10.27, 10.48, 10.06
yy = np.linspace(LCL-0.08, UCL+0.08, 200)
axn.plot(norm_pdf(yy, CL, 0.07), yy, color=BLUE, lw=2)
axn.fill_betweenx(yy, 0, norm_pdf(yy, CL, 0.07), color=BLUE, alpha=0.15)
axn.invert_xaxis(); axn.set_xticks([]); axn.set_yticks([])
axn.set_title("normal curve\nrotated 90°", fontsize=9.5, color=GREY, fontweight="normal")
axc.plot(range(1, 25), data, "o-", color=INK, lw=1.4, ms=5, mfc=BLUE, mec=BLUE)
for yv, lab, col in [(CL, "CL — centre line (process location)", TEAL),
                     (UCL, "UCL = CL + 3σ", RED), (LCL, "LCL = CL − 3σ", RED)]:
    axc.axhline(yv, color=col, lw=1.6, ls="-" if yv==CL else "--")
    axc.text(24.4, yv, lab, va="center", fontsize=10.5, color=col, fontweight="bold")
axc.set_xlim(0, 33); axc.set_ylim(LCL-0.08, UCL+0.08)
axc.set_xticks([1,6,12,18,24]); axc.set_yticks([])
axc.set_xlabel("Subgroups in time order  →")
axc.set_title("Shewhart's insight: rotate the bell curve, add ±3σ lines, plot in time order", fontsize=12)
save(fig, "control_chart_anatomy.png", w=8.6, h=3.8)

# ---------------------------------------------------------------- 6. Xbar-R chart (lab data)
XBARS = [10.25, 10.30, 10.20, 10.40, 10.20]; RS = [0.3, 0.3, 0.4, 0.3, 0.2]
XBB, RBAR = 10.27, 0.30
fig, (a1, a2) = plt.subplots(2, 1, sharex=True)
a1.plot(range(1,6), XBARS, "o-", color=BLUE, lw=1.8, ms=7)
for yv,c,ls,lab in [(XBB,TEAL,"-","CL 10.27"),(10.49,RED,"--","UCL 10.49"),(10.05,RED,"--","LCL 10.05")]:
    a1.axhline(yv,color=c,lw=1.5,ls=ls); a1.text(5.25,yv,lab,va="center",fontsize=9.5,color=c,fontweight="bold", bbox=LBL_BOX)
a1.set_ylabel("Xbar (mm)"); a1.set_title("Xbar chart — subgroup MEANS (between-subgroup variation)", fontsize=11)
a1.set_xlim(0.6, 6.4); a1.set_ylim(9.98, 10.56)
a2.plot(range(1,6), RS, "s-", color=VIOLET, lw=1.8, ms=7)
for yv,c,ls,lab in [(RBAR,TEAL,"-","CL 0.30"),(0.68,RED,"--","UCL 0.68"),(0.0,RED,"--","LCL 0")]:
    a2.axhline(yv,color=c,lw=1.5,ls=ls); a2.text(5.25,yv,lab,va="center",fontsize=9.5,color=c,fontweight="bold", bbox=LBL_BOX)
a2.set_ylabel("Range R (mm)"); a2.set_xlabel("Subgroup (n = 4)")
a2.set_title("R chart — subgroup RANGES (within-subgroup variation) — read this one FIRST", fontsize=11)
a2.set_xlim(0.6, 6.4); a2.set_ylim(-0.06, 0.8); a2.set_xticks(range(1,6))
save(fig, "xbar_r_chart.png", w=7.4, h=4.6)

# ---------------------------------------------------------------- 7. Xbar-S chart (lab data)
SS = [0.129, 0.141, 0.183, 0.141, 0.082]; SBAR = 0.135
fig, (a1, a2) = plt.subplots(2, 1, sharex=True)
a1.plot(range(1,6), XBARS, "o-", color=BLUE, lw=1.8, ms=7)
a1.axhline(XBB, color=TEAL, lw=1.5); a1.text(5.25, XBB, "CL 10.27", va="center", fontsize=9.5, color=TEAL, fontweight="bold", bbox=LBL_BOX)
a1.set_ylabel("Xbar (mm)"); a1.set_title("Xbar chart — subgroup means", fontsize=11); a1.set_xlim(0.6, 6.4)
a2.plot(range(1,6), SS, "s-", color=AMBER, lw=1.8, ms=7)
a2.axhline(SBAR, color=TEAL, lw=1.5); a2.text(5.25, SBAR, "CL S̄ 0.135", va="center", fontsize=9.5, color=TEAL, fontweight="bold", bbox=LBL_BOX)
a2.set_ylabel("Std dev S (mm)"); a2.set_xlabel("Subgroup")
a2.set_title("S chart — subgroup standard deviations (use when n > 10)", fontsize=11)
a2.set_xlim(0.6, 6.4); a2.set_xticks(range(1,6))
save(fig, "xbar_s_chart.png", w=7.4, h=4.6)

# ---------------------------------------------------------------- 8. I-MR chart (lab data)
IND = [25.1, 25.4, 25.2, 25.8, 25.5, 25.3, 25.6, 25.2]
MRS = [abs(IND[i]-IND[i-1]) for i in range(1, len(IND))]
IBAR = float(np.mean(IND)); MRBAR = float(np.mean(MRS))
fig, (a1, a2) = plt.subplots(2, 1)
a1.plot(range(1,9), IND, "o-", color=BLUE, lw=1.8, ms=7)
a1.axhline(IBAR, color=TEAL, lw=1.5); a1.text(8.3, IBAR, f"CL {IBAR:.2f}", va="center", fontsize=9.5, color=TEAL, fontweight="bold", bbox=LBL_BOX)
a1.set_ylabel("Individual (cP)"); a1.set_title("I chart — every single reading (subgroup size = 1)", fontsize=11)
a1.set_xlim(0.5, 9.6); a1.set_xticks(range(1,9))
a2.plot(range(2,9), MRS, "s-", color=VIOLET, lw=1.8, ms=7)
a2.axhline(MRBAR, color=TEAL, lw=1.5); a2.text(8.3, MRBAR, f"CL {MRBAR:.2f}", va="center", fontsize=9.5, color=TEAL, fontweight="bold", bbox=LBL_BOX)
a2.set_ylabel("Moving range"); a2.set_xlabel("Batch")
a2.set_title("MR chart — |current − previous| tracks short-term variation", fontsize=11)
a2.set_xlim(0.5, 9.6); a2.set_xticks(range(1,9))
fig.set_size_inches(7.4, 4.6)
fig.tight_layout(h_pad=2.0)
save(fig, "imr_chart.png", w=7.4, h=4.6)

# ---------------------------------------------------------------- 9. attribute charts 2x2 (lab data)
fig, axes = plt.subplots(2, 2)
# p chart
ax = axes[0][0]; ps=[0.04,0.12,0.00,0.08,0.16]; pbar=0.08; ucl=pbar+3*np.sqrt(pbar*0.92/25)
ax.plot(range(1,6), ps, "o-", color=BLUE, ms=6); ax.axhline(pbar, color=TEAL, lw=1.4)
ax.axhline(ucl, color=RED, lw=1.4, ls="--"); ax.axhline(0, color=RED, lw=1.4, ls="--")
ax.set_title("p chart — PROPORTION defective\n(binomial; n may vary)", fontsize=10.5)
ax.text(5.15, pbar, "p̄ 0.08", fontsize=9, color=TEAL, va="center", fontweight="bold")
ax.text(5.15, ucl, f"UCL {ucl:.2f}", fontsize=9, color=RED, va="center"); ax.set_xticks(range(1,6)); ax.set_xlim(0.6,6.3)
# np chart
ax = axes[0][1]; nps=[3,5,2,6,4]; npbar=4.0; ucl=npbar+3*np.sqrt(npbar*0.92)
ax.plot(range(1,6), nps, "o-", color=TEAL, ms=6); ax.axhline(npbar, color=TEAL, lw=1.4)
ax.axhline(ucl, color=RED, lw=1.4, ls="--"); ax.axhline(0, color=RED, lw=1.4, ls="--")
ax.set_title("np chart — NUMBER defective\n(binomial; constant n only)", fontsize=10.5)
ax.text(5.15, npbar, "np̄ 4.0", fontsize=9, color=TEAL, va="center", fontweight="bold")
ax.text(5.15, ucl, f"UCL {ucl:.1f}", fontsize=9, color=RED, va="center"); ax.set_xticks(range(1,6)); ax.set_xlim(0.6,6.3)
# u chart
ax = axes[1][0]; ns=[20,25,20,30,25]; cs=[12,18,10,24,16]; us=[c/n for c,n in zip(cs,ns)]; ubar=sum(cs)/sum(ns)
ax.plot(range(1,6), us, "o-", color=VIOLET, ms=6); ax.axhline(ubar, color=TEAL, lw=1.4)
ucls=[ubar+3*np.sqrt(ubar/n) for n in ns]
ax.step(np.arange(0.5,6.0), ucls+[ucls[-1]], where="post", color=RED, lw=1.4, ls="--")
ax.set_title("u chart — defects PER UNIT\n(Poisson; limits step with n)", fontsize=10.5)
ax.text(5.15, ubar, "ū 0.67", fontsize=9, color=TEAL, va="center", fontweight="bold")
ax.set_xticks(range(1,6)); ax.set_xlim(0.4,6.3); ax.set_xlabel("Sample")
# c chart
ax = axes[1][1]; cs2=[7,5,9,4,6,8]; cbar=6.5; ucl=cbar+3*np.sqrt(cbar)
ax.plot(range(1,7), cs2, "o-", color=AMBER, ms=6); ax.axhline(cbar, color=TEAL, lw=1.4)
ax.axhline(ucl, color=RED, lw=1.4, ls="--"); ax.axhline(0, color=RED, lw=1.4, ls="--")
ax.set_title("c chart — defects COUNT\n(Poisson; constant unit only)", fontsize=10.5)
ax.text(6.2, cbar, "c̄ 6.5", fontsize=9, color=TEAL, va="center", fontweight="bold")
ax.text(6.2, ucl, f"UCL {ucl:.1f}", fontsize=9, color=RED, va="center")
ax.set_xticks(range(1,7)); ax.set_xlim(0.5,7.5); ax.set_xlabel("Unit")
fig.suptitle("The four attribute control charts — all built from the hands-on lab data", fontweight="bold", fontsize=12.5)
fig.tight_layout(rect=[0,0,1,0.94])
save(fig, "attribute_charts.png", w=9.4, h=5.6)

# ---------------------------------------------------------------- 10. why 3 sigma (cost trade-off)
fig, ax = plt.subplots()
k = np.linspace(0.5, 5, 300)
alpha_cost = 3.2*np.exp(-((k-0.)**2)/2.6)         # false alarms — falls as limits widen
beta_cost = 0.12*np.exp(0.78*k)                   # missed shifts — rises as limits widen
total = alpha_cost + beta_cost
ax.plot(k, alpha_cost, color=BLUE, lw=2, label="Cost of FALSE ALARMS (α) — investigating a stable process")
ax.plot(k, beta_cost, color=AMBER, lw=2, label="Cost of MISSED SHIFTS (β) — defects reach the customer")
ax.plot(k, total, color=RED, lw=2.6, label="TOTAL quality cost")
kmin = k[np.argmin(total)]
ax.axvline(3.0, color=TEAL, lw=1.8, ls="--")
ax.annotate("±3σ ≈ the economic minimum\n(Shewhart, 1924)", xy=(3.0, total[np.argmin(np.abs(k-3))]),
            xytext=(3.35, 2.6), fontsize=11, fontweight="bold", color=TEAL,
            arrowprops=dict(arrowstyle="->", color=TEAL))
ax.set_xlabel("Control limit width (± kσ)"); ax.set_ylabel("Cost (relative)")
ax.set_xticks([1,2,3,4,5]); ax.set_xticklabels(["1σ","2σ","3σ","4σ","5σ"]); ax.set_yticks([])
ax.legend(frameon=False, fontsize=9.5, loc="upper center")
ax.set_title("Why 3 Sigma? — the most economical control limit")
save(fig, "three_sigma_cost.png")

# ---------------------------------------------------------------- 11. zones A/B/C
fig, ax = plt.subplots()
rng3 = np.random.default_rng(11)
pts = np.clip(rng3.normal(0, 1.0, 22), -2.9, 2.9); pts[15]=2.55; pts[16]=2.4
bands = [(2,3,AMBER,0.28,"Zone A  (2σ–3σ)"), (1,2,TEAL,0.22,"Zone B  (1σ–2σ)"), (0,1,BLUE,0.15,"Zone C  (0–1σ)"),
         (-1,0,BLUE,0.15,"Zone C"), (-2,-1,TEAL,0.22,"Zone B"), (-3,-2,AMBER,0.28,"Zone A")]
for lo,hi,col,al,lab in bands:
    ax.axhspan(lo,hi,color=col,alpha=al)
    ax.text(22.6,(lo+hi)/2,lab,va="center",fontsize=10.5,color=INK,fontweight="bold")
ax.axhline(0,color=INK,lw=1.6); ax.axhline(3,color=RED,lw=1.8); ax.axhline(-3,color=RED,lw=1.8)
ax.text(22.6, 3, "UCL (+3σ)", va="center", fontsize=10.5, color=RED, fontweight="bold")
ax.text(22.6, -3, "LCL (−3σ)", va="center", fontsize=10.5, color=RED, fontweight="bold")
ax.text(22.6, 0.0, "CL", va="center", fontsize=10.5, color=INK, fontweight="bold")
ax.plot(range(1,23), pts, "o-", color=INK, lw=1.3, ms=5, mfc="white")
ax.set_xlim(0, 30); ax.set_ylim(-3.6, 3.6); ax.set_yticks([]); ax.set_xticks([])
ax.set_xlabel("Time  →"); ax.set_title("Control Chart Zones — three equal 1σ bands each side of the centre line")
save(fig, "zones.png", w=8.2, h=4.0)

# ---------------------------------------------------------------- 12. SPC rules (Western Electric, 4 panels)
fig, axes = plt.subplots(2, 2)
def zone_bg(ax):
    for lo,hi,col,al in [(2,3,AMBER,0.22),(1,2,TEAL,0.16),(0,1,BLUE,0.10),(-1,0,BLUE,0.10),(-2,-1,TEAL,0.16),(-3,-2,AMBER,0.22)]:
        ax.axhspan(lo,hi,color=col,alpha=al)
    ax.axhline(0,color=INK,lw=1.2); ax.axhline(3,color=RED,lw=1.5); ax.axhline(-3,color=RED,lw=1.5)
    ax.set_xticks([]); ax.set_yticks([]); ax.set_ylim(-3.7,3.7)
r = np.random.default_rng(5)
# Rule 1
ax=axes[0][0]; zone_bg(ax); y=r.normal(0,0.9,12); y[8]=3.4
ax.plot(range(12), y, "o-", color=INK, lw=1.2, ms=5, mfc="white")
ax.plot(8, y[8], "o", ms=9, color=RED)
ax.set_title("Rule 1 — one point beyond ±3σ", fontsize=11)
# Rule 2: 2 of 3 in zone A
ax=axes[0][1]; zone_bg(ax); y=r.normal(0,0.8,12); y[7],y[8],y[9]=2.5,1.6,2.7
ax.plot(range(12), y, "o-", color=INK, lw=1.2, ms=5, mfc="white")
for i in (7,9): ax.plot(i, y[i], "o", ms=9, color=RED)
ax.set_title("Rule 2 — 2 of 3 consecutive in Zone A (same side)", fontsize=11)
# Rule 3: run of 8 same side (shift)
ax=axes[1][0]; zone_bg(ax); y=np.concatenate([r.normal(0,0.8,4), np.abs(r.normal(1.0,0.5,8))])
ax.plot(range(12), y, "o-", color=INK, lw=1.2, ms=5, mfc="white")
for i in range(4,12): ax.plot(i, y[i], "o", ms=7, color=RED)
ax.set_title("Rule 3 — run of 8 on one side of CL (SHIFT)", fontsize=11)
# Rule 4: trend of 6
ax=axes[1][1]; zone_bg(ax); y=np.linspace(-2.2,2.4,8)+r.normal(0,0.12,8); y=np.concatenate([r.normal(-1,0.5,3),y])
ax.plot(range(11), y, "o-", color=INK, lw=1.2, ms=5, mfc="white")
for i in range(3,11): ax.plot(i, y[i], "o", ms=7, color=RED)
ax.set_title("Rule 4 — 6+ points steadily rising/falling (TREND)", fontsize=11)
fig.suptitle("SPC Rules (Western Electric) — non-random patterns that signal a special cause", fontweight="bold", fontsize=12.5)
fig.tight_layout(rect=[0,0,1,0.94])
save(fig, "spc_rules.png", w=9.4, h=5.4)

# ---------------------------------------------------------------- 13. capability = defects
fig, (a1, a2) = plt.subplots(1, 2, sharey=True)
xx = np.linspace(6, 14, 400)
for ax, s, title in [(a1, 0.55, "CAPABLE — spread fits the spec"), (a2, 1.35, "NOT capable — tails spill over")]:
    ax.plot(xx, norm_pdf(xx, 10, s), color=BLUE, lw=2.2)
    ax.fill_between(xx, norm_pdf(xx, 10, s), color=BLUE, alpha=0.12)
    bad_lo = xx[xx < 8.5]; bad_hi = xx[xx > 11.5]
    ax.fill_between(bad_lo, norm_pdf(bad_lo, 10, s), color=RED, alpha=0.55)
    ax.fill_between(bad_hi, norm_pdf(bad_hi, 10, s), color=RED, alpha=0.55)
    for sv, lab in [(8.5, "LSL"), (11.5, "USL")]:
        ax.axvline(sv, color=INK, lw=1.6, ls="--"); ax.text(sv, 0.66, lab, ha="center", fontsize=11, fontweight="bold", color=INK)
    ax.set_yticks([]); ax.set_xticks([]); ax.set_ylim(0, 0.78); ax.set_title(title, fontsize=11.5, pad=10)
a2.annotate("DEFECTS", xy=(12.15, 0.06), xytext=(12.4, 0.3), fontsize=11, color=RED, fontweight="bold",
            arrowprops=dict(arrowstyle="->", color=RED))
fig.suptitle("Process capability = how much of the output falls inside the customer's specification", fontweight="bold", fontsize=12.5)
fig.set_size_inches(9.0, 3.4)
fig.tight_layout(rect=[0, 0, 1, 0.86])
save(fig, "capability_defects.png", w=9.0, h=3.4)

# ---------------------------------------------------------------- 14. accuracy vs precision targets
fig, axes = plt.subplots(1, 4)
cases = [("Accurate + precise", 0, 0, 0.16, TEAL), ("Precise, NOT accurate", 0.5, 0.45, 0.16, AMBER),
         ("Accurate, NOT precise", 0, 0, 0.52, BLUE), ("Neither", 0.5, -0.45, 0.5, RED)]
rt = np.random.default_rng(2)
for ax, (title, dx, dy, spread, col) in zip(axes, cases):
    for radius in [1.0, 0.66, 0.33]:
        ax.add_patch(plt.Circle((0,0), radius, fill=(radius==0.33), color=LINE if radius>0.34 else "#FDECEC", ec=GREY, lw=1.2))
    ax.add_patch(plt.Circle((0,0), 0.08, color=RED))
    px, py = rt.normal(dx, spread, 9), rt.normal(dy, spread, 9)
    ax.plot(px, py, "o", ms=6, color=col, mec=INK, mew=0.4)
    ax.set_xlim(-1.25,1.25); ax.set_ylim(-1.25,1.25); ax.set_aspect("equal")
    ax.axis("off"); ax.set_title(title, fontsize=10.5)
fig.suptitle("Process capability needs BOTH — accuracy (on target) and precision (small spread)", fontweight="bold", fontsize=12.5)
save(fig, "accuracy_precision.png", w=10.0, h=3.0)

# ---------------------------------------------------------------- 15. Cp/Cpk lab scenario
fig, ax = plt.subplots()
xx = np.linspace(9.3, 10.8, 400)
ax.plot(xx, norm_pdf(xx, 10.2, 0.1), color=BLUE, lw=2.4)
ax.fill_between(xx, norm_pdf(xx, 10.2, 0.1), color=BLUE, alpha=0.14)
for sv, lab in [(9.5, "LSL 9.5"), (10.5, "USL 10.5")]:
    ax.axvline(sv, color=INK, lw=1.8, ls="--"); ax.text(sv, 4.35, lab, ha="center", fontsize=11.5, fontweight="bold")
ax.axvline(10.0, color=GREY, lw=1.2, ls=":"); ax.text(10.0, 4.35, "spec centre 10.0", ha="center", fontsize=10, color=GREY)
ax.axvline(10.2, color=RED, lw=1.8); ax.text(10.2, 4.7, "μ = 10.2 (off-centre)", ha="center", fontsize=11, color=RED, fontweight="bold")
ax.annotate("", xy=(10.5, 2.0), xytext=(10.2, 2.0), arrowprops=dict(arrowstyle="<->", color=AMBER, lw=1.8))
ax.text(10.35, 2.15, "USL−μ = 0.3\nCPU = 1.00", ha="center", fontsize=10, color=AMBER, fontweight="bold")
ax.annotate("", xy=(10.2, 0.55), xytext=(9.5, 0.55), arrowprops=dict(arrowstyle="<->", color=TEAL, lw=1.8))
ax.text(9.8, 0.68, "μ−LSL = 0.7   CPL = 2.33", ha="center", fontsize=10, color=TEAL, fontweight="bold")
ax.text(9.42, 3.3, "Cp  = (USL−LSL)/6σ = 1.67\nCpk = min(CPU, CPL) = 1.00", fontsize=12, fontweight="bold",
        color=INK, bbox=dict(boxstyle="round,pad=0.6", fc=LIGHT, ec=LINE))
ax.set_yticks([]); ax.set_xlabel("Shaft diameter (mm) — the Activity 11 scenario")
ax.set_ylim(0, 5.1); ax.set_title("Cp vs Cpk — an off-centre mean wastes capability")
save(fig, "cp_cpk.png", w=8.4, h=4.2)

# ---------------------------------------------------------------- 16. pareto
fig, ax = plt.subplots()
causes = ["Nozzle\nclog", "Material\nlot", "Operator\nsetup", "Temp\ndrift", "Fixture\nwear", "Other"]
counts = [42, 27, 14, 8, 5, 4]
cum = np.cumsum(counts)/sum(counts)*100
bars = ax.bar(causes, counts, color=[BLUE, BLUE, TEAL, TEAL, GREY, GREY], alpha=0.9)
ax2 = ax.twinx()
ax2.plot(range(len(causes)), cum, "o-", color=AMBER, lw=2.2, ms=6)
ax2.axhline(80, color=RED, lw=1.3, ls="--"); ax2.text(4.55, 82, "80% line", color=RED, fontsize=10)
for i, c in enumerate(cum): ax2.text(i, c+3.5, f"{c:.0f}%", ha="center", fontsize=9.5, color=AMBER, fontweight="bold")
ax2.set_ylim(0, 112); ax2.set_ylabel("Cumulative % of defects", color=AMBER)
ax2.spines["right"].set_visible(True); ax2.spines["right"].set_color(GREY)
ax.set_ylabel("Defect count"); ax.set_title("Pareto Analysis — the vital few causes explain most of the defects")
ax.text(0.6, 38, "the VITAL FEW\n(~80% of defects)", fontsize=10.5, fontweight="bold", color=INK, ha="center")
save(fig, "pareto.png", w=7.8, h=4.2)

# ---------------------------------------------------------------- 17. fishbone
fig, ax = plt.subplots()
ax.axis("off"); ax.set_xlim(0, 14); ax.set_ylim(0, 8)
ax.annotate("", xy=(11.6, 4), xytext=(0.6, 4), arrowprops=dict(arrowstyle="-|>", color=INK, lw=2.6))
ax.add_patch(plt.Rectangle((11.7, 3.2), 2.25, 1.6, fc="#FDECEC", ec=RED, lw=1.6))
ax.text(12.82, 4.0, "Coating\nthickness\nOOC", ha="center", va="center", fontsize=11, fontweight="bold", color=RED)
bones = [("MAN", 2.6, True, ["handover setup skipped", "new operator untrained"]),
         ("MACHINE", 5.6, True, ["nozzle wear", "pressure drift"]),
         ("MATERIAL", 8.6, True, ["new lot viscosity", "supplier change"]),
         ("METHOD", 2.6, False, ["wrong recipe rev", "no setup checklist"]),
         ("MEASUREMENT", 5.6, False, ["gauge not calibrated", "operator reading error"]),
         ("ENVIRONMENT", 8.6, False, ["afternoon temperature", "humidity spike"])]
for name, bx, top, subs in bones:
    y2 = 7.0 if top else 1.0
    ax.plot([bx, bx+1.7], [y2, 4], color=INK, lw=1.8)
    ax.text(bx-0.05, y2+(0.22 if top else -0.42), name, fontsize=11, fontweight="bold",
            color=BLUE if top else TEAL)
    for i, sub in enumerate(subs):
        frac = 0.30+0.32*i
        sx, sy = bx+1.7*frac, y2+(4-y2)*frac
        ax.plot([sx, sx-1.15], [sy, sy], color=GREY, lw=1.1)
        ax.text(sx-1.22, sy, sub, ha="right", va="center", fontsize=8.8, color=GREY)
ax.set_title("Ishikawa Fishbone — causes organised into the 6 Ms (the Activity 12 scenario)")
save(fig, "fishbone.png", w=9.6, h=4.6)

# ---------------------------------------------------------------- 18. PDSA + DMAIC
fig, (a1, a2) = plt.subplots(1, 2)
a1.axis("off"); a1.set_xlim(-1.6, 1.6); a1.set_ylim(-1.7, 1.7); a1.set_aspect("equal")
quads = [("PLAN", 90, BLUE, "identify the change,\npredict the result"), ("DO", 0, TEAL, "trial it,\nsmall scale"),
         ("STUDY", 270, AMBER, "compare results\nwith prediction"), ("ACT", 180, VIOLET, "adopt, adapt\nor abandon")]
import matplotlib.patches as mpatches
for name, start, col, sub in quads:
    a1.add_patch(mpatches.Wedge((0,0), 1.25, start+4, start+86, width=0.62, fc=col, alpha=0.85))
    ang = np.deg2rad(start+45); r0 = 0.95
    a1.text(r0*np.cos(ang), r0*np.sin(ang), name, ha="center", va="center", fontsize=12, fontweight="bold", color="white")
a1.text(0, 0, "Deming\nPDSA", ha="center", va="center", fontsize=11.5, fontweight="bold", color=INK)
a1.annotate("", xy=(0.30, 1.42), xytext=(-0.30, 1.42), arrowprops=dict(arrowstyle="->", color=GREY, lw=1.6))
a1.set_title("PDSA — continuous improvement cycle", fontsize=11.5)
a2.axis("off"); a2.set_xlim(0, 10); a2.set_ylim(0, 8)
steps = [("D", "Define", BLUE, "the problem & the goal"), ("M", "Measure", TEAL, "baseline performance"),
         ("A", "Analyze", VIOLET, "root causes of variation"), ("I", "Improve", AMBER, "implement & verify the fix"),
         ("C", "Control", RED, "hold the gains — with SPC")]
for i, (ltr, name, col, sub) in enumerate(steps):
    y = 7.0 - i*1.45
    a2.add_patch(plt.Circle((1.0, y), 0.48, color=col))
    a2.text(1.0, y, ltr, ha="center", va="center", fontsize=13, fontweight="bold", color="white")
    a2.text(1.85, y+0.13, name, fontsize=12, fontweight="bold", color=INK, va="center")
    a2.text(1.85, y-0.38, sub, fontsize=9.5, color=GREY, va="center")
    if i < 4: a2.annotate("", xy=(1.0, y-0.98), xytext=(1.0, y-0.52), arrowprops=dict(arrowstyle="->", color=GREY, lw=1.5))
a2.set_title("Six Sigma DMAIC — SPC lives in the C", fontsize=11.5)
save(fig, "pdsa_dmaic.png", w=9.4, h=4.4)

# ---------------------------------------------------------------- 19. with/without SPC comparison flow
fig, ax = plt.subplots(); ax.axis("off"); ax.set_xlim(0, 14); ax.set_ylim(0, 8)
def box(ax, x, y, w, h, text, fc, ec, tc=INK, fs=10.5, bold=False):
    ax.add_patch(plt.Rectangle((x, y), w, h, fc=fc, ec=ec, lw=1.4))
    ax.text(x+w/2, y+h/2, text, ha="center", va="center", fontsize=fs, color=tc, fontweight="bold" if bold else "normal")
def arrow(ax, x1, y1, x2, y2, col=GREY):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle="->", color=col, lw=1.8))
ax.text(0.4, 7.35, "WITHOUT SPC — detect & react", fontsize=12, fontweight="bold", color=RED)
box(ax, 0.4, 5.6, 2.6, 1.1, "Process runs\n(blind)", "#FDECEC", RED)
box(ax, 3.9, 5.6, 2.6, 1.1, "Inspect & sort\n100% at the end", "#FDECEC", RED)
box(ax, 7.4, 5.6, 2.6, 1.1, "Scrap or rework\n$$$", "#FDECEC", RED, tc=RED, bold=True)
box(ax, 10.9, 5.6, 2.6, 1.1, "Ship survivors", "#FDECEC", RED)
arrow(ax, 3.0, 6.15, 3.9, 6.15, RED); arrow(ax, 6.5, 6.15, 7.4, 6.15, RED); arrow(ax, 10.0, 6.15, 10.9, 6.15, RED)
ax.text(0.4, 3.85, "WITH SPC — predict & prevent", fontsize=12, fontweight="bold", color=TEAL)
box(ax, 0.4, 2.1, 2.6, 1.1, "Process runs\n+ control chart", "#E8F7EE", TEAL)
box(ax, 3.9, 2.1, 2.6, 1.1, "Signal detected\nBEFORE defects", "#E8F7EE", TEAL)
box(ax, 7.4, 2.1, 2.6, 1.1, "Correct the cause\n(small cost)", "#E8F7EE", TEAL)
box(ax, 10.9, 2.1, 2.6, 1.1, "Ship good product", "#E8F7EE", TEAL, tc=TEAL, bold=True)
arrow(ax, 3.0, 2.65, 3.9, 2.65, TEAL); arrow(ax, 6.5, 2.65, 7.4, 2.65, TEAL); arrow(ax, 10.0, 2.65, 10.9, 2.65, TEAL)
ax.annotate("feedback loop — the chart tells the process how it is doing", xy=(1.7, 2.1), xytext=(5.2, 0.7),
            fontsize=10, color=TEAL, arrowprops=dict(arrowstyle="->", color=TEAL, lw=1.4,
            connectionstyle="arc3,rad=0.25"))
ax.set_title("Manufacturing with vs without SPC — prevention beats inspection", fontweight="bold")
save(fig, "spc_vs_no_spc.png", w=9.6, h=4.4)

print("All chart assets generated in", OUT)
