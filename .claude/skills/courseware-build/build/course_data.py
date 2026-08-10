"""
SINGLE SOURCE OF TRUTH — WSQ Budgeting for Small and Medium Enterprises.

Every artifact (PPT, LP, LG, LG.md, labs index, assessments) is generated from
this file + data_domain1.py … data_domain7.py so they stay 100% aligned.
"""

# ------------------------------------------------------------------ metadata
TITLE        = "WSQ Budgeting for Small and Medium Enterprises"
SHORT_TITLE  = "WSQ Budgeting for Small and Medium Enterprises"   # used in output filenames
COURSE_CODE  = "TGS-2021002336"
VERSION      = "v12"
VERSION_DATE = "10 August 2026"
ORG          = "Tertiary Infotech Academy Pte Ltd"
UEN          = "UEN: 201200696W"
TRAINER      = "Dr Alfred Ang"
DAYS         = 2

# Skills Framework alignment
TSC_TITLE = "Budgeting"
TSC_CODE  = "ICT-FIN-3001-1.1"

TSC_ABILITIES = [
    "A1: Analyse business function strategies, functional objectives and operational plans",
    "A2: Carry out forecasting and budgeting for the financial year",
    "A3: Calculate the business unit's cash flow requirements",
    "A4: Determine the business unit's financing needs for the financial year",
    "A5: Compare budget data with estimations to highlight discrepancies",
    "A6: Report budget calculations and discrepancies to organisation management to facilitate decisions on budget allocation",
    "A7: Ensure adherence to financial controls in accordance with relevant organisational corporate governance and financial policies, legislation and regulations",
]
TSC_KNOWLEDGE = [
    "K1: Objectives, parameters and types of budgets",
    "K2: Key principles of accounting and financial systems",
    "K3: Types of data sources and data required to prepare a budget",
    "K4: Accounting principles and practices related to budget preparation",
    "K5: Key principles of budgetary control and budget plans, budgetary control techniques",
    "K6: Requirements of Singapore's taxation policies",
    "K7: Functional objectives and key requirements",
    "K8: Organisational financial data",
    "K9: Financial analytical techniques and methodology",
    "K10: Stakeholders to consult on budget calculations",
]

# ------------------------------------------------------------------ outcomes
LEARNING_OUTCOMES = [
    "LO1: Analyse business strategies and objectives",
    "LO2: Carry out financial forecasting",
    "LO3: Prepare budget to meet cash flow requirements",
    "LO4: Prepare budget control plan",
    "LO5: Perform financial analysis to highlight discrepancies",
    "LO6: Report budget and seek approval",
    "LO7: Perform financial control to ensure compliance",
]

# ------------------------------------------------------------------ topics
TOPICS = [
    dict(num=1, code="01",
         title="Introduction to Financial Budgeting",
         subtitle="Business strategies and objectives · Budgeting parameters · Budgeting types  (A1, K1)",
         weighting="A1 · K1",
         concepts=[
            ("What is a budget?", "A quantitative operational plan for acquiring and using resources over a set period — goals plus a detailed plan to achieve them."),
            ("The three statements", "A company budget is expressed through the Profit & Loss, Balance Sheet and Cash Flow Statement."),
            ("An internal function", "Budgeting is management accounting — customised to the company's needs, unlike IFRS/GAAP financial statements."),
            ("Master Budget", "Aggregates operating, financial and investing inputs from every department into one plan."),
            ("Static vs flexible", "Most companies review results monthly or quarterly and re-forecast — a flexible planning model."),
            ("Budget types", "Operating, financial, capital and cash budgets; baseline, incremental, zero-based and hybrid methods."),
         ]),
    dict(num=2, code="02",
         title="Financial Forecasting",
         subtitle="Key principles of accounting · Key principles of corporate finance · Time value of money  (A2, K2)",
         weighting="A2 · K2",
         concepts=[
            ("Accounting principles", "GAAP/IFRS rules — accrual, conservatism, consistency, matching, materiality, revenue recognition and going concern."),
            ("Accrual vs cash method", "Accrual records revenue when earned and expenses when incurred; cash records only when money moves."),
            ("Corporate finance", "Maximising shareholder value through capital investment, capital financing and working-capital decisions."),
            ("Capital financing", "Balancing debt against equity — too much debt raises default risk; too much equity dilutes earnings."),
            ("Time value of money", "A dollar today is worth more than a dollar tomorrow — discount long-horizon budgets accordingly."),
            ("Forecasting techniques", "Qualitative and quantitative methods over short, medium and long horizons; bottom-up and top-down."),
         ]),
    dict(num=3, code="03",
         title="Budget Preparation",
         subtitle="Cash flow calculation · Preparing the budget  (A3, K3, K4)",
         weighting="A3 · K3 K4",
         concepts=[
            ("Budgeting methods", "Baseline, incremental, zero-based and hybrid — choose per account and per business need."),
            ("Key components", "Fixed vs flexible expenses, total income and disposable income (surplus)."),
            ("Cash budget", "Estimates cash inflows and outflows weekly, monthly, quarterly or annually to prove the entity can keep operating."),
            ("Cash inflow / outflow", "Inflows from sales, investments and financing; outflows for wages, rent, suppliers and dividends."),
            ("Working capital", "Current assets minus current liabilities — the measure of liquidity and short-term health."),
            ("The 7-step master budget", "Revenue → cost of sales → SG&A → fixed assets → working capital → financial liabilities → compilation."),
         ]),
    dict(num=4, code="04",
         title="Budget Control Plan",
         subtitle="Preparing the budget control plan · Budgetary control techniques  (A4, K5, K7)",
         weighting="A4 · K5 K7",
         concepts=[
            ("Budgetary control", "Prepare budgets, compare standards with actual performance, find the reasons for differences and take corrective action."),
            ("Operating control", "Covers revenue and operating expenses to protect day-to-day operations and target EBITDA."),
            ("Cash flow control", "Compares forecast inflows/outflows with actuals so obligations are always covered; invests idle cash."),
            ("Capex control", "Plans and manages large capital expenditures so only profitable investments are made, at the right time."),
            ("Road map", "Develop the budget collaboratively, document policies, train users and designate a budget manager."),
            ("Accountability", "Managers are responsible and accountable for their department budgets, on one source of truth."),
         ]),
    dict(num=5, code="05",
         title="Budget Analysis",
         subtitle="Compare budget with estimation · Financial methodologies for budget control  (A5, K8, K9)",
         weighting="A5 · K8 K9",
         concepts=[
            ("Budget vs actual", "Variance = actual − budget, in dollars and as a % — displayed on a Budget-to-Actual report."),
            ("Adverse variance", "Actual income below budget or expenditure above budget — a deficit to investigate."),
            ("Favourable variance", "Actual income above budget or expenditure below budget — a surplus to substantiate."),
            ("Thresholds", "Manage overspends and underspends with clear dollar or percentage variance thresholds."),
            ("Analysis techniques", "Vertical and horizontal analysis, benchmarking, and P&L / Balance-Sheet / ratio KPIs."),
            ("Technology & BI", "Move beyond Excel — ERP budgeting modules and BI dashboards (Power BI on Xero) for insight."),
         ]),
    dict(num=6, code="06",
         title="Budget Approval",
         subtitle="Budget approval process · Stakeholder precautions  (A6, K10)",
         weighting="A6 · K10",
         concepts=[
            ("Stakeholders", "Boards are ambitious, mid-management conservative — the budgeting committee reconciles and 'sells' the final numbers."),
            ("Approval pack", "Review of past year, goals and objectives, rolling forecast, plan details and realistic costs."),
            ("Approval process", "Draft → departmental review → budget committee → board approval → communicated plan."),
            ("Communicate fast", "An approved plan adds no value until business units receive it and start tracking performance."),
            ("Common issues", "Slow approvals, no tracking framework, manual effort and no single source of truth for spend."),
            ("Right tooling", "Robust tracking tools, frameworks and resources make approval meaningful."),
         ]),
    dict(num=7, code="07",
         title="Financial Compliance",
         subtitle="Singapore taxation policies · Financial control and compliance  (A7, K6)",
         weighting="A7 · K6",
         concepts=[
            ("Corporate tax", "All companies pay tax under the Income Tax Act on income derived from or remitted into Singapore — flat 17% on chargeable income."),
            ("Tax residency", "A company is tax-resident where control and management are exercised — usually where board meetings are held."),
            ("Year of Assessment", "The 12-month period in which income is assessed — YA follows the financial year end."),
            ("Start-Up Exemption", "First 3 YAs: 75% exemption on the first S$100k and 50% on the next S$100k of chargeable income."),
            ("ECI & filing", "File Estimated Chargeable Income within 3 months of FY end; e-File corporate tax by 30 Nov."),
            ("Penalties", "Late filing risks prosecution; late payment attracts 5% penalty plus 1% per month up to 12%."),
         ]),
]

# ------------------------------------------------------------------ day themes (8 training hours/day)
DAY_THEMES = {
    1: "Budgeting Foundations, Forecasting & Budget Preparation",
    2: "Budget Control, Analysis, Approval, Compliance & Assessment",
}

# ------------------------------------------------------------------ assessment
ASSESSMENT = dict(
    written="Written Assessment (WA) — Short-Answer Questions (SAQ), 70 minutes, open book.",
    practical="Written Assessment (WA) — Case Study (CS), 80 minutes, open book.",
    note="A minimum of 75% attendance is required to be eligible for assessment and funding.",
)

PRACTICE_EXAM_URL = "https://exams.tertiaryinfotech.com"
LMS_URL = "https://lms-tms.tertiaryinfotech.com"
