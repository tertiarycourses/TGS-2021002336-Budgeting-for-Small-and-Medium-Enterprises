"""Topic 5 — Budget Analysis (A5, K8, K9) — hands-on activities."""

DOMAIN5 = [
    dict(
        num=7, topic=5,
        title="Budget Variance Analysis in Xero",
        objective="LO5 — Perform financial analysis to highlight discrepancies (A5, K8, K9)",
        desc="Compare your Xero budget against actual performance, identify favourable and adverse variances, substantiate them as a budget manager and present the analysis.",
        build="A budget-to-actual variance analysis report identifying and substantiating favourable and adverse variances, presented to the class.",
        services="Xero Budget Manager",
        steps=[
            ("Open Budget Manager and display the budget you built in the earlier activity alongside actuals (set the actuals comparison to 3, 6 or 12 months).", ""),
            ("For each key line, compute the variance: actual minus budget, in dollars and as a percentage of budget.", ""),
            ("Classify each variance as favourable (income above budget / expense below budget) or adverse (income below budget / expense above budget).", ""),
            ("As the budget manager, substantiate each material variance — both favourable and adverse: what business events explain it?", ""),
            ("Apply a variance threshold (e.g. ±10% or ±$5,000) to decide which variances need management action.", ""),
            ("Present your variance analysis report to the class.", ""),
        ],
        test="Your report shows dollar and percentage variances for each key account, labels each as favourable or adverse, substantiates the material ones, and was presented to the class.",
    ),
    dict(
        num=8, topic=5,
        title="Budget Analysis Dashboard with Power BI",
        objective="LO5 — Perform financial analysis to highlight discrepancies (A5, K8, K9)",
        desc="Connect Microsoft Power BI to your Xero organisation and build a dashboard that analyses cash flow, overdue invoices and bills, and profitability.",
        build="A Power BI dashboard fed daily from Xero contacts, invoices, bills and trial balance.",
        services="Microsoft Power BI, Xero",
        steps=[
            ("Sign up for a free Microsoft Power BI account at https://powerbi.microsoft.com/en-us/landing/signin/ (a Pro trial is sufficient).", ""),
            ("Follow the Xero guide at https://central.xero.com/s/article/Microsoft-Power-Bi#Connectyourorganisation.", ""),
            ("In the Power BI left navigation pane, click Apps.", ""),
            ("Find Xero, then click Get it now.", ""),
            ("Create a workspace in Power BI.", ""),
            ("Click Xero in Power BI and under Connect your data, click Connect.", ""),
            ("Enter the organisation name exactly as it appears in Xero, then click Next.", ""),
            ("Click Sign In and log in to Xero if you haven't already.", ""),
            ("Select the Xero organisation and click Continue.", ""),
            ("Open the generated dashboard and explore the cash flow, overdue invoices/bills and profitability visuals.", ""),
        ],
        test="Power BI displays the Xero dashboard for your organisation and you can read off cash-flow, receivables and profitability insights that support budget analysis.",
    ),
]
