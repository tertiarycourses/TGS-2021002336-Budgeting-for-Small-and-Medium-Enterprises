# WSQ Budgeting for Small and Medium Enterprises

**Course Code:** TGS-2021002336 · **Skills Framework TSC:** Budgeting (ICT-FIN-3001-1.1)
**Conducted by:** Tertiary Infotech Academy Pte Ltd (UEN 201200696W)
**Course page:** <https://www.tertiarycourses.com.sg/wsq-budgeting-for-small-and-medium-enterprises.html>

A 2-day (16-hour) WSQ course that teaches SME owners, managers and finance executives to
forecast, prepare, control, analyse, report and comply — the full budgeting cycle — with
hands-on activities on Xero, Microsoft Power BI and case-study templates.

## Courseware (current version: v13)

| Artifact | File |
|---|---|
| Trainer slide deck (130 slides) | `courseware/WSQ Budgeting for Small and Medium Enterprises-v13.pptx` (+ PDF) |
| Lesson Plan (LP) | `courseware/LP-WSQ Budgeting for Small and Medium Enterprises.docx` (+ PDF) |
| Learner Guide (LG) | `courseware/LG-WSQ Budgeting for Small and Medium Enterprises.docx` (+ PDF) |
| Learner Guide Markdown mirror | `LG-WSQ Budgeting for Small and Medium Enterprises.md` |
| Hands-on activities (12) | [`activities/`](activities/README.md) — one folder per activity (`activity01` … `activity12`), each with the guide, workflow diagram and mock data (Excel + CSV) |

Superseded versions live in `courseware/archive/`. Assessments are confidential and are
distributed via Google Drive / the LMS only — they are not in this repository.

## Learning outcomes

- LO1: Analyse business strategies and objectives
- LO2: Carry out financial forecasting
- LO3: Prepare budget to meet cash flow requirements
- LO4: Prepare budget control plan
- LO5: Perform financial analysis to highlight discrepancies
- LO6: Report budget and seek approval
- LO7: Perform financial control to ensure compliance

## Topics & activities

| Topic | Activities |
|---|---|
| 1. Introduction to Financial Budgeting | 1 Financial Statements with Xero · 2 Creating a Budget in Xero · 3 Identifying Budget Types |
| 2. Financial Forecasting | 4 Financial Forecasting with Xero |
| 3. Budget Preparation | 5 Master Budget Preparation — 99 Agency Case Study |
| 4. Budget Control Plan | 6 Knowledge Check Quiz — Budget Control |
| 5. Budget Analysis | 7 Budget Variance Analysis in Xero · 8 Budget Analysis Dashboard with Power BI |
| 6. Budget Approval | 9 Knowledge Check Quiz — Budget Approval |
| 7. Financial Compliance | 10 Year of Assessment · 11 ECI & Tax Filing Deadlines · 12 Start-Up Tax Computation |

## Rebuilding the courseware

The deck, LP, LG (+ Markdown mirror), activities and workflow diagrams are all generated from one
single-source content module (`.claude/skills/courseware-build/build/course_data.py` +
`data_domain1..7.py`):

```bash
python3 .claude/skills/courseware-build/build/build_labs.py       # activities/activityNN/README.md guides
python3 .claude/skills/courseware-build/build/build_diagrams.py   # activities/activityNN/ workflow PNGs
python3 .claude/skills/courseware-build/build/build_datasets.py   # activities/activityNN/ mock data (Excel + CSV)
bash    .claude/skills/courseware-build/build/build_courseware.sh # PPT + LP + LG + PDFs
```

## Support

Email <enquiry@tertiaryinfotech.com> · Tel +65 6100 0613 · <https://www.tertiarycourses.com.sg>
