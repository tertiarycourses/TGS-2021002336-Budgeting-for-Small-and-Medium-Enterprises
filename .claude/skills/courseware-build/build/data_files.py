"""Single source for the per-lab mock data sets (one folder per lab: activities/activity01 … activities/activity12) and the FULL
step-by-step instructions for analyzing them — the Excel workbook AND the CSV
mirrors. Rendered into the Learner Guide and each labs/lab-NN-*.md."""

# DATA[lab_num] = dict(
#   files=[(filename, one-line description), ...],
#   excel_steps=[step, ...],   # detailed walkthrough of the .xlsx
#   csv_steps=[step, ...],     # detailed walkthrough of the .csv mirrors
# )

DATA = {
 1: dict(
  files=[
   ("activity-01-financial-statements.xlsx", "GreenLeaf Trading Pte Ltd — Income Statement, Balance Sheet and Cash Flow sheets with live formulas."),
   ("activity-01-income-statement.csv", "The Income Statement as plain data (Line Item, Amount)."),
   ("activity-01-balance-sheet.csv", "The Balance Sheet as plain data."),
   ("activity-01-cash-flow.csv", "The Cash Flow Statement as plain data."),
  ],
  excel_steps=[
   "Open activities/activity01/activity-01-financial-statements.xlsx in Excel (or Google Sheets / LibreOffice). It has three sheets — Income Statement, Balance Sheet and Cash Flow — mirroring the three statements you generated in Xero.",
   "On the Income Statement sheet, click cell B6 (Total Revenue) and read the formula bar: =SUM(B4:B5). Blue numbers are inputs; black numbers are formulas — never overtype a black cell.",
   "Trace the P&L structure downwards: Total Revenue − Total COGS = Gross Profit (B10); Gross Profit − Total SG&A = Operating Profit; then Interest, Tax (17%) and Net Profit. Click each bold cell and confirm its formula matches the story.",
   "Read the two ratio cells at the bottom: Gross Profit Margin = Gross Profit ÷ Total Revenue (62.1%) and Net Profit Margin (21.4%). Change Marketing to 88,000 and watch Operating Profit, Tax, Net Profit and both margins recalculate; press Ctrl+Z to undo.",
   "On the Balance Sheet sheet, verify TOTAL ASSETS (770,000) = Total Current Assets + Net PP&E, and that the Balance Check cell at the bottom shows 0 — Assets − Liabilities − Equity must always be zero. If you ever edit an input and the check is non-zero, the statement no longer balances.",
   "On the Cash Flow sheet, follow the three sections: Operating (Net Profit + Depreciation ± working-capital movements = 254,470), Investing (−80,000 CAPEX) and Financing (−70,000). Confirm Closing Cash (185,000) equals the Cash and Bank line on the Balance Sheet — the statements tie.",
   "Compare each sheet with the same statement you generated from the Xero demo company: identify where Revenue, COGS, Assets, Liabilities, Equity and the operating/investing/financing sections appear in both.",
  ],
  csv_steps=[
   "Open activities/activity01/activity-01-income-statement.csv in a text editor first — see that a CSV is just comma-separated rows with a header line (Line Item, Amount). This is the format accounting systems export.",
   "Import it into a blank spreadsheet (Excel: Data → Get Data → From Text/CSV; Google Sheets: File → Import → Upload). Confirm the Amount column imported as numbers, not text.",
   "The CSV carries values only — no formulas. Rebuild the checks yourself: in a spare cell compute Gross Profit = Total Revenue − Total COGS with a SUM/lookup, and confirm you get 745,000, matching the Excel workbook.",
   "Import activity-01-balance-sheet.csv the same way and verify TOTAL ASSETS (770,000) = TOTAL LIABILITIES (348,000) + TOTAL EQUITY (422,000) with a formula.",
   "Import activity-01-cash-flow.csv and verify Opening Cash + Net Change in Cash = Closing Cash (80,530 + 104,470 = 185,000).",
  ]),
 2: dict(
  files=[
   ("activity-02-budget-plan.xlsx", "FY2026 12-month budget plan — Sales grows 2%/month; commission, discount and direct costs are live %-of-sales formulas."),
   ("activity-02-budget-plan.csv", "The same budget as plain data, one row per account, Jan–Dec + Total."),
  ],
  excel_steps=[
   "Open activities/activity02/activity-02-budget-plan.xlsx. Row 2 holds the three driver rates in blue — Commission 5%, Discount 2%, Direct Costs 55%. Rows 5–14 are the account lines across Jan–Dec with a Total column.",
   "Click any Sales Commission cell (row 6) and read its formula, e.g. =B5*$C$2 — commission is derived from Sales via an absolute reference to the rate cell. This is why you budget drivers, not hardcoded numbers.",
   "Click the Total column (column N): every account totals with =SUM(B..M). Confirm Sales totals 1,207,085 for the year.",
   "Read the Net Surplus row: each month = Sales − all expense rows. Check which months are surplus and which are deficit.",
   "Test the model: change the Direct Costs rate (G2) from 55% to 60% and watch every month's Direct Costs and Net Surplus recalculate. Undo (Ctrl+Z).",
   "Now enter this budget into Xero Budget Manager (Accounting → Reports → Budget Manager): create a 12-month budget and key the monthly figures for each account — use the green-arrow fill with a 2% monthly increase for Sales instead of typing all 12 cells.",
   "Save in Xero, then cross-check: the Xero budget's annual total for Sales must equal the workbook's Total cell.",
  ],
  csv_steps=[
   "Open activities/activity02/activity-02-budget-plan.csv in a text editor — one row per account, columns Jan–Dec plus Total, values only.",
   "Import it into a blank spreadsheet. Add a check column: =SUM(B2:M2) beside the imported Total and confirm they agree for every account — this is how you validate someone else's exported budget.",
   "Compute the commission rate implied by the data: Sales Commission Total ÷ Sales Total ≈ 5%. Because a CSV has no formulas, recomputing the driver rates is how you reverse-engineer the assumptions.",
   "Use this CSV as your data-entry source when keying the budget into Xero Budget Manager if you prefer working from a printed sheet.",
  ]),
 3: dict(
  files=[
   ("activity-03-budget-classification.xlsx", "12 spending items to classify — yellow Budget Type and Preparation Method columns to fill; a Reference sheet defines every term."),
   ("activity-03-budget-classification.csv", "The same worksheet as plain data with empty classification columns."),
  ],
  excel_steps=[
   "Open activities/activity03/activity-03-budget-classification.xlsx on the Worksheet sheet — 12 real spending items with their annual amounts. The yellow cells are yours to fill.",
   "Open the Reference sheet and read the definitions: Operating / Cash / Capital / Financial budget types, and Baseline / Incremental / Zero-based / Hybrid preparation methods.",
   "For each item, fill Budget Type: e.g. 'Monthly office rental' → Operating; 'New delivery van purchase' → Capital; 'Cash float for retail outlets' → Cash; 'Bank loan repayment' and 'Dividend payout' → Financial.",
   "Fill Preparation Method for each: rent is a Baseline carry-forward; salaries are typically Incremental; a brand-new POS system is Zero-based; raw materials may be Hybrid (baseline volume × new prices). Be ready to justify each choice.",
   "Add a summary: in a spare cell use =COUNTIF(C5:C16,\"Operating\") (and repeat for the other types) to count how many items fall in each budget type.",
   "Compare your classification with a neighbour and defend any differences using the Reference definitions — several items have more than one defensible method.",
  ],
  csv_steps=[
   "Open activities/activity03/activity-03-budget-classification.csv in a text editor to see the raw worksheet — the two classification columns are empty strings.",
   "Import into a spreadsheet, fill the two columns as above, then File → Save As / Download as CSV to practise round-tripping data: open your saved CSV again and confirm your classifications survived.",
   "Sort the imported data by your Budget Type column to group items and check each group's total annual amount with SUMIF.",
  ]),
 4: dict(
  files=[
   ("activity-04-fy2025-actuals.xlsx", "FY2025 monthly actuals (the forecast baseline) plus a yellow Forecast Assumptions sheet holding every FY2026 assumption."),
   ("activity-04-fy2025-actuals.csv", "The FY2025 actuals as plain data, Jan–Dec + Total per account."),
  ],
  excel_steps=[
   "Open activities/activity04/activity-04-fy2025-actuals.xlsx. The FY2025 Actuals sheet is your baseline: Sales grew about 1.5%/month from 75,000; commission 5%, discount 2%, direct costs 55%; rent 7,500; salaries 45,000 (10 staff); depreciation 12,000; other 5,000.",
   "Open the Forecast Assumptions sheet — the yellow cells hold every FY2026 assumption from the activity: +10% sales vs the same month last year, 5% commission, 2% discount, 55% direct costs, an extra office at 1.5× rent from June, +3 headcount at 4,500/month from July, and 30,000/month depreciation from January. Income tax is ignored.",
   "Build the FY2026 forecast: add a new sheet (or columns) and for January compute Sales = Jan FY2025 × (1+10%); copy across all 12 months.",
   "Derive the dependent lines with formulas referencing the assumption cells: Commission = Sales × 5%, Discount = Sales × 2%, Direct Costs = Sales × 55%.",
   "Handle the step changes with IF or by splitting the year: Rent = 7,500 until May, then 7,500 × (1 + 1.5) from June (current office plus the new one at 1.5×); Salaries = 45,000 until June, then (10+3) × 4,500 = 58,500 from July; Depreciation = 12,000 + 30,000 = 42,000 every month.",
   "Add a Net Surplus row = Sales − all expense lines and total the year. Identify which months turn negative after the June/July step-ups and what that means for cash planning.",
   "Now reproduce the same forecast in Xero Budget Manager, using the workbook as your working: the Xero monthly figures must match your sheet. Be ready to justify which budgeting method (baseline / incremental / zero-based / hybrid) you applied to each line.",
  ],
  csv_steps=[
   "Import activities/activity04/activity-04-fy2025-actuals.csv into a blank spreadsheet — this is the same baseline without any formulas, as a finance system would export it.",
   "Verify the baseline before forecasting from it: recompute one derived line (e.g. Jan Commission ÷ Jan Sales = 5%) to confirm the data is internally consistent.",
   "Build the FY2026 forecast columns beside the imported data using the same assumption formulas as the Excel walkthrough — starting from a values-only CSV is the realistic case, since exports never carry formulas.",
  ]),
 5: dict(
  files=[
   ("activity-05-99-agency-template.xlsx", "The 99 Agency master-budget working template — Assumptions, Revenue and Cost of Sales schedules pre-wired; SG&A, Fixed Assets, Working Capital, Liabilities and Master Budget sheets to build."),
   ("activity-05-client-baseline.csv", "Per-client FY2025 revenue and expected FY2026 growth (the bottom-up input)."),
   ("activity-05-assumptions.csv", "Every case assumption as plain data."),
  ],
  excel_steps=[
   "Open activities/activity05/activity-05-99-agency-template.xlsx. The Assumptions sheet holds every case parameter in blue — market size 12m × 12% share, cost-of-sales rates, fixed and variable SG&A, quarterly CAPEX (40k/60k/25k/80k), 10% depreciation on beginning fixed assets of 400k, liabilities falling from 3.2m to 2.8m at 5% interest, and AR/AP days.",
   "STEP 1 — open the '1 Revenue' sheet. The bottom-up plan is pre-wired: each client's FY2026 revenue = FY2025 × (1 + growth) — click D4 and read =B4*(1+C4). The top-down target pulls from the Assumptions sheet (=Assumptions!B4*Assumptions!B5 = 1,440,000), and the yellow committee cell takes the AVERAGE of bottom-up and top-down. Confirm the bottom-up total is 1,534,800 and the committee target 1,487,400.",
   "STEP 2 — open '2 Cost of Sales': revenue is split 60% Ad / 40% SEO, and each stream is costed at its Assumptions rate (30% / 25%). Trace each formula back to the sheets it references — this is the baseline + averaging method from the slides.",
   "STEP 3 — build the '3 SGA' sheet: list the six fixed fees from Assumptions (rent 60k, accounting 12k, legal 8k, training 10k, management salaries 180k, admin 24k), then add the two variable lines = committee revenue × 4% (external services) and × 3% (selling commissions). Total the SG&A.",
   "STEP 4 — build '4 Fixed Assets': beginning fixed assets 400,000 + the four quarterly CAPEX amounts = closing gross assets 605,000; depreciation = 10% × beginning fixed assets = 40,000; closing net assets = closing gross − accumulated depreciation.",
   "STEP 5 — build '5 Working Capital': Accounts Receivable = committee revenue × 45/365; Accounts Payable = total cost of sales × 30/365. Working capital = AR − AP.",
   "STEP 6 — build '6 Liabilities': beginning 3,200,000, ending 2,800,000 (repayment 400,000); interest expense = 5% × average balance ( (3.2m+2.8m)/2 × 5% = 150,000 ).",
   "STEP 7 — build '7 Master Budget': compile the Income Statement (committee revenue − cost of sales − SG&A − depreciation − interest = net profit), then the Balance Sheet (net fixed assets, AR, cash; liabilities and equity with retained earnings up by net profit) and the Cash Flow. Check: the Balance Sheet balances and closing cash ties to the Cash Flow.",
   "Present your consolidated Master Budget: show the committee revenue decision, the schedule totals and the final three statements.",
  ],
  csv_steps=[
   "Open activities/activity05/activity-05-client-baseline.csv — the raw bottom-up input: five client rows with FY2025 revenue and expected growth. Import it into a blank sheet and recompute the bottom-up total (Σ revenue × (1+growth)) = 1,534,800 to verify it matches the template.",
   "Open activities/activity05/activity-05-assumptions.csv — every assumption as data. Use it as your checklist while building STEP 3–7: tick each assumption off as your schedules consume it; an unused assumption means a schedule is incomplete.",
   "If you prefer building from scratch, import both CSVs into one workbook and construct the whole 7-schedule model from the raw data instead of the pre-wired template — the totals must come out identical.",
  ]),
 6: dict(
  files=[
   ("activity-06-budget-control-monitor.xlsx", "Six departments' mid-year budget vs actual with live variance, variance-% and a REVIEW/OK status driven by a 10% threshold cell."),
   ("activity-06-budget-control-monitor.csv", "The same monitor as plain data (no formulas) for you to rebuild."),
  ],
  excel_steps=[
   "Open activities/activity06/activity-06-budget-control-monitor.xlsx before attempting the quiz — it makes the control-loop concepts concrete.",
   "Read row by row: each department has an Annual Budget, YTD Budget and YTD Actual. Variance = Actual − Budget (=D5-C5) and Var % = Variance ÷ YTD Budget.",
   "Click a Status cell and read the control formula: =IF(ABS(F5)>$B$2,\"REVIEW\",\"OK\") — any department whose absolute variance % exceeds the yellow threshold cell (10%) is flagged for corrective action. This IS budgetary control: compare, investigate, correct.",
   "Identify the flagged departments (Marketing overspend ≈ +19%, Operations ≈ +9%) and, for each, say which control applies — operating, cash flow or capital-expenditure control — and what corrective action you would take.",
   "Change the threshold from 10% to 5% and watch more departments flip to REVIEW — thresholds decide how much management attention the process demands. Undo when done.",
   "Now take the Google Form quiz; use the workbook to reason about the control-process questions.",
  ],
  csv_steps=[
   "Import activities/activity06/activity-06-budget-control-monitor.csv into a blank spreadsheet — it has only the three data columns per department.",
   "Rebuild the monitor yourself: add Variance, Var % and Status columns with the formulas from the Excel walkthrough. Getting the IF/ABS threshold formula right is the point of the exercise.",
   "Check your rebuilt monitor flags exactly the same departments as the workbook.",
  ]),
 7: dict(
  files=[
   ("activity-07-budget-vs-actual.xlsx", "Budget and Actual sheets (8 accounts × 12 months) plus a Variance sheet that classifies every line Favourable/Adverse against a threshold."),
   ("activity-07-budget.csv", "The budget as plain data."),
   ("activity-07-actual.csv", "The actuals as plain data."),
  ],
  excel_steps=[
   "Open activities/activity07/activity-07-budget-vs-actual.xlsx. The Budget and Actual sheets hold the same 8 accounts across Jan–Dec; actuals deviate from budget (Sales ran ~3% under, Marketing ~28% over, Direct Costs ~4% over…).",
   "Open the Variance sheet: Budget and Actual totals are pulled cross-sheet (=Budget!N4, =Actual!N4 — green-style links), Variance = Actual − Budget, Var % = Variance ÷ Budget.",
   "Study the Classification formula: for an income account a positive variance is Favourable; for an expense account a NEGATIVE variance is Favourable — click G5 and read the nested IF that encodes this. This distinction is the heart of variance analysis.",
   "Identify every Adverse line above the 10% threshold (Marketing +28%) and every Favourable one (Other Expenses −8%). Substantiate each as the budget manager: what business events explain it?",
   "Sales is under budget by ~3% — express the variance in dollars AND as a % (the Budget-to-Actual report style from the slides: e.g. budget 500,000, actual 400,000 → (100,000) and (20%)).",
   "Reproduce the same analysis in Xero: display your Budget Manager budget alongside actuals, and compare Xero's variance columns with the workbook's.",
   "Write your variance analysis report: each material variance, its classification, substantiation, and the corrective action — then present it to the class.",
  ],
  csv_steps=[
   "Import both activities/activity07/activity-07-budget.csv and activities/activity07/activity-07-actual.csv into ONE spreadsheet on two sheets — this simulates receiving separate system exports.",
   "Build your own Variance sheet from scratch: reference the two imported sheets, compute Variance and Var %, and add the income-vs-expense Favourable/Adverse IF formula.",
   "Cross-check your computed variances against the workbook's Variance sheet — every figure must match. If one differs, find whether your cross-sheet reference points at the wrong row (the classic variance-report bug).",
  ]),
 8: dict(
  files=[
   ("activity-08-xero-export.xlsx", "A Xero-style export: 60 sales invoices, 48 supplier bills and a balanced trial balance."),
   ("activity-08-invoices.csv", "The invoices as CSV — ready to load into Power BI."),
   ("activity-08-bills.csv", "The bills as CSV."),
   ("activity-08-trial-balance.csv", "The trial balance as CSV."),
  ],
  excel_steps=[
   "Open activities/activity08/activity-08-xero-export.xlsx. The Invoices sheet lists six months of sales invoices (number, date, due date, contact, amount, amount paid, status); Bills is the supplier side; Trial Balance is the account-level position.",
   "On Invoices, read the Total and Outstanding cells below the table: Outstanding = total invoiced − total paid — this is the receivables exposure a cash-flow dashboard must show.",
   "Analyse receivables: insert a PivotTable (Insert → PivotTable) with Contact on rows and Amount − Amount Paid as values to rank customers by outstanding balance; filter Status = Authorised to isolate unpaid invoices.",
   "Repeat on Bills for payables: which suppliers are owed the most, and in which months do payments cluster?",
   "On Trial Balance, confirm the Balance check cell equals 0 (total debits = total credits, 1,442,000 each side) — an unbalanced TB means the export is corrupt. Identify which accounts are P&L (Sales, COGS, expenses) and which are Balance Sheet.",
   "From the TB compute profitability in spare cells: Sales − COGS − expenses = operating result; compare gross margin with Activity 1.",
   "In Power BI Desktop (or the Power BI service), use Get Data → Excel workbook to load all three sheets and build three visuals: outstanding receivables by contact (bar), monthly invoiced vs paid (line), and expenses breakdown from the TB (donut). This mirrors what the Xero connector builds automatically.",
  ],
  csv_steps=[
   "The three CSVs are the same tables as system exports. In Power BI: Get Data → Text/CSV, load activity-08-invoices.csv, activity-08-bills.csv and activity-08-trial-balance.csv — use this route whenever the live Xero connector is unavailable in class.",
   "In Power Query, check each column's data type (dates as Date, amounts as Decimal Number) before loading — CSV imports default to text when a type is ambiguous, and a text amount cannot be summed.",
   "Add a computed column Outstanding = Amount − [Amount Paid] on invoices, then build the same three visuals as the Excel walkthrough.",
   "Cross-check one number between the two routes: total outstanding receivables from your CSV-based dashboard must equal the workbook's Outstanding cell.",
  ]),
 9: dict(
  files=[
   ("activity-09-approval-pack.xlsx", "Six departmental FY2027 budget submissions with growth-% formulas and an HQ growth-cap check."),
   ("activity-09-approval-pack.csv", "The submissions as plain data."),
  ],
  excel_steps=[
   "Open activities/activity09/activity-09-approval-pack.xlsx before the quiz — it walks the approval process with real numbers.",
   "Each department row shows FY2026 Actual, FY2027 Requested and a Growth % formula. The yellow cell holds the HQ cap: the total ask may grow at most 8% over prior year.",
   "Read the bottom check: total requested vs total actual → the 'Within HQ cap?' cell. The total ask (1,308,000 vs 1,124,000 ≈ +16%) exceeds the cap, so the committee must trim — exactly the 'numbers are opened up and re-sold' stage from the slides.",
   "Play the budgeting-committee role: decide where to trim to bring the total within 8%, using each department's justification column (protect statutory HR increments; challenge the largest discretionary asks like Marketing +31% and IT +43%).",
   "For your trimmed plan, state how you would present it for approval: past-year review, goals, forecast, plan details, realistic costs — the five-part approval pack.",
   "Then take the Google Form quiz on budget approval.",
  ],
  csv_steps=[
   "Import activities/activity09/activity-09-approval-pack.csv into a spreadsheet and rebuild the pack: add the Growth % column, the totals row and the cap check formula yourself.",
   "Sort by your Growth % column descending to produce the committee's challenge list — the order in which requests get questioned.",
  ]),
 10: dict(
  files=[
   ("activity-10-ya-worksheet.xlsx", "Five financial years with an empty (yellow) Year of Assessment column."),
   ("activity-10-ya-worksheet.csv", "The same worksheet as plain data."),
  ],
  excel_steps=[
   "Open activities/activity10/activity-10-ya-worksheet.xlsx — five financial years, including the three from the slides plus two current ones.",
   "Recall the rule: income earned in a financial year is assessed in the YA that follows the financial year END.",
   "Fill the yellow YA column for each row: a FY ending 31 Dec 2020 → YA 2021; ending 31 Mar 2020 → YA 2021; ending 30 Jun 2020 → YA 2021; ending 31 Dec 2025 → YA 2026; ending 30 Sep 2025 → YA 2026.",
   "For the first row (1 Jan 2019 – 31 Dec 2020, a 24-month first period), note that IRAS attributes the income across two YAs in practice — state the YA for the year end and flag the long-first-period point for discussion.",
   "Compare answers with the class and resolve differences against the IRAS definition.",
  ],
  csv_steps=[
   "Import activities/activity10/activity-10-ya-worksheet.csv, fill the YA column, and save your completed copy as CSV — submit or compare this file in class.",
   "Bonus: derive YA with a formula instead of typing — extract the FY-end year with RIGHT(B2,4) and add 1.",
  ]),
 11: dict(
  files=[
   ("activity-11-filing-deadlines.xlsx", "The same five financial years with empty ECI-deadline and corporate-tax e-Filing deadline columns."),
   ("activity-11-filing-deadlines.csv", "The same worksheet as plain data."),
  ],
  excel_steps=[
   "Open activities/activity11/activity-11-filing-deadlines.xlsx. Two rules drive everything: ECI is due within 3 months of the financial year end; corporate tax is e-Filed by 30 November (of the YA).",
   "Fill the ECI column: FY ending 31 Dec 2020 → ECI by 31 Mar 2021; 31 Mar 2020 → 30 Jun 2020; 30 Jun 2020 → 30 Sep 2020; 31 Dec 2025 → 31 Mar 2026; 30 Sep 2025 → 31 Dec 2025.",
   "Fill the e-Filing column: 30 November of each row's YA (from Activity 10) — e.g. YA 2021 → 30 Nov 2021.",
   "Optional formula: compute the ECI deadline with EDATE(end_date, 3) on a real date value to see how finance teams automate the compliance calendar.",
   "Discuss: what can IRAS do on late filing (prosecution of officers) and late payment (5% penalty + 1%/month up to 12%)?",
  ],
  csv_steps=[
   "Import activities/activity11/activity-11-filing-deadlines.csv, complete both deadline columns, and save your answers back to CSV.",
   "Sort by ECI deadline to produce the compliance calendar in date order — the view a finance manager pins on the wall.",
  ]),
 12: dict(
  files=[
   ("activity-12-startup-tax.xlsx", "Five years of profits with empty exemption / chargeable / tax columns, plus a Rates sheet holding the exemption rules."),
   ("activity-12-startup-tax.csv", "The same computation table as plain data."),
  ],
  excel_steps=[
   "Open activities/activity12/activity-12-startup-tax.xlsx. The Rates sheet holds the rules: 17% flat rate; Start-Up Exemption (first 3 YAs) 75% of the first S$100,000 + 50% of the next S$100,000; from Year 4 the Partial Exemption of 75% of the first S$10,000 + 50% of the next S$190,000.",
   "Year 1 (profits 200,000): exempt = 75%×100,000 + 50%×100,000 = 125,000; chargeable = 75,000; tax = 75,000 × 17% = 12,750. Enter these in the yellow cells — with formulas referencing the Rates sheet, not typed numbers.",
   "Year 2 (300,000): the exemption only ever covers the first 200,000 of income, so exempt = 125,000; chargeable = 175,000; tax = 29,750.",
   "Year 3 (400,000): exempt = 125,000; chargeable = 275,000; tax = 46,750 — the last start-up-exemption year.",
   "Year 4 (500,000): switch to the Partial Exemption — exempt = 75%×10,000 + 50%×190,000 = 102,500; chargeable = 397,500; tax = 67,575.",
   "Year 5 (600,000): exempt = 102,500; chargeable = 497,500; tax = 84,575.",
   "Add a Total row (=SUM of the tax column = 241,400) and a check: effective tax rate per year = tax ÷ profits — watch it climb from 6.4% to 14.1% as the start-up relief expires.",
  ],
  csv_steps=[
   "Import activities/activity12/activity-12-startup-tax.csv, rebuild the same computation with formulas, and compare your five tax figures with the class.",
   "Save your completed computation as CSV — a values-only copy is what you would attach to a tax working-paper file.",
  ]),
}
