"""Topic 2 — Financial Forecasting (A2, K2) — hands-on activities."""

DOMAIN2 = [
    dict(
        num=4, topic=2,
        title="Financial Forecasting with Xero",
        objective="LO2 — Carry out financial forecasting (A2, K2)",
        desc="Use Xero's Budget Manager to perform a full financial forecast for the coming year from a set of business assumptions, choosing and justifying your budgeting methods.",
        build="A 12-month financial forecast in Xero Budget Manager reflecting all given sales, cost, headcount and capex assumptions.",
        services="Xero Budget Manager",
        steps=[
            ("Open Budget Manager (Accounting menu → Reports → Financial → Budget Manager) and start a new 12-month budget for the coming financial year.", ""),
            ("Forecast Sales to improve by 10% month-on-month from January, in comparison to the same month last year.", ""),
            ("Add Sales Commission at 5% of Sales for every month.", ""),
            ("Add Sales Discount at 2% of Sales for every month.", ""),
            ("Set Direct Costs at 55% of Revenue under normal circumstances.", ""),
            ("From June, add an additional office location at 1.5 times the current office rental.", ""),
            ("From July, increase full-time headcount by 3 from the current 10 — scale salary expense accordingly.", ""),
            ("Add depreciation of $30,000 per month from January for the new capital-expenditure projects.", ""),
            ("Ignore income tax and keep all other expenses unchanged. Save the budget.", ""),
            ("Review the resulting monthly surplus/deficit and be ready to justify which budgeting method (baseline, incremental, zero-based or hybrid) you applied to each line.", ""),
        ],
        test="Your Budget Manager forecast reflects every assumption (10% MoM sales growth, 5% commission, 2% discount, 55% direct costs, new office from June, +3 headcount from July, $30k/month depreciation) and you can justify the method used for each line.",
    ),
]
