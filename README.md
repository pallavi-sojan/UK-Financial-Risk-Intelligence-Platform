# 🏦 UK Financial Risk Intelligence Platform
### Caledonia Bank plc (Fictional) — Multi-Module Financial Analytics Portfolio

**Built by:** Pallavi Sojan | MSc Finance & Risk Management | Edinburgh, UK  
**Data Source:** Bank of England Statistical Database (Public)  
**Status:** Active Development | 6 Modules

---

## 📊 Live Dashboards

| Dashboard | Tool | Link |
|-----------|------|------|
| FP&A Performance Dashboard | Tableau Public | *[ 🔄 Coming soon ]* |
| Credit Risk Dashboard | Tableau Public | *[ 🔄 Coming soon ]* |
| AML Compliance Dashboard | Tableau Public | [View Live Dashboard](https://public.tableau.com/app/profile/pallavi.sojan/viz/AMLInvestigationLog/Dashboard1) |
| Regulatory Reporting Dashboard | Power BI | *[ 🔄 Coming soon ]* |
| FP&A Report | Power BI | *[ 🔄 Coming soon ]* |

---

## 🎯 Project Overview

This platform simulates the analytical infrastructure of a UK retail bank using real Bank of England public data. It covers six interconnected modules spanning FP&A, credit risk, AML compliance, regulatory reporting, and internal audit — the core functions of a UK financial services firm.

**Fictional entity:** Caledonia Bank plc  
**Data:** Bank of England Statistical Database (IADB)  
**Tools:** Python | SQL | Excel | Tableau | Power BI | Word  
**Regulatory frameworks:** MLR 2017 | IFRS 9 | Basel III | COREP/FinRep | IIA Standards 2025

---

## 📦 Module Summary

### ✅ Module 1 — BoE Data Pipeline (In progress)
**Tools:** Python, SQLite, VS Code  
**Files:** `scripts/boe_pipeline.py` | `sql_queries/01_data_validation.sql`

- Automated data pipeline pulling 7 Bank of England interest rate and lending datasets
- SQLite database with 3 tables: `master_boe_data`, `loan_writeoffs`, `mfi_income`
- Data cleaning, merging, and validation using pandas
- BoE series codes: IUMABEDR, IUMTLMV, IUMTLMF, LPMVWYR, LPMB3ZX

---

### ✅ Module 2 — FP&A Model (In Progress)
**Tools:** Excel, Tableau, Power BI  
**Files:** `excel_models/FPA_PL_Model.xlsx`

- Fully linked 3-statement banking P&L model (2019A-2024A, 2025E-2027E)
- 7 sheets: PL_MODEL, BALANCE_SHEET, CASH_FLOW, BUDGET_VS_ACTUAL, SCENARIO_ANALYSIS, MODEL_VALIDATION, CHARTS
- Budget vs actual variance analysis with auto-flagging (ADVERSE/FAVOURABLE/OK)
- 4-scenario stress test: BASE, BULL, BEAR, SEVERE STRESS
- 15 model validation checks — 100% pass rate
- Key ratios: NIM 3.2%, Cost-to-Income 35%, ROE 19%
- Management Commentary Word document (CFO-quality, 5 pages)

---

### ✅ Module 3 — Credit Risk / IFRS 9
**Tools:** Excel, Python, SQL  
**Files:** `excel_models/Credit_Risk_Scorecard.xlsx` | `scripts/ifrs9_ecl_model.py`

- Quantitative credit risk scorecard using BoE sectoral lending and write-off data
- PD proxy, LGD (45% secured / 65% unsecured per Basel), EAD and ECL by sector
- IFRS 9 impairment staging: Stage 1 (12-month ECL), Stage 2/3 (lifetime ECL)
- 4-scenario stress test calibrated to BoE Annual Cyclical Scenario (+100/200/300bps)
- Under severe stress: portfolio ECL increases 65% from £1,126m to £1,858m
- Python IFRS 9 ECL model with matplotlib output

---

### ✅ Module 4 — AML & Compliance
**Tools:** Excel, SQL, Word  
**Files:** `excel_models/AML_Transaction_Monitoring.xlsx` | `sql_queries/aml_tm_rules_simple.sql` | `audit_documents/SAR_CUST018_ALT001.docx`

- 30-customer synthetic dataset with 8 seeded suspicious transaction patterns
- 8 SQL transaction monitoring rules covering structuring, sanctions, PEP, dormant accounts, round tripping, rapid in-out, cash intensity, high-risk jurisdictions
- KYC/CDD framework: 3-tier model (SDD/CDD/EDD) aligned to MLR 2017 and JMLSG 2026
- Customer risk scoring model (5 dimensions, 100 points) applied to all 30 customers
- Alert Investigation Log: 10 alerts, 4 dispositions (TRUE POSITIVE / FALSE POSITIVE / PENDING / WHITELISTED)
- NCA-format SAR under POCA 2002 Section 330 — ALT001 structuring case
- Regulatory framework: MLR 2017 | JMLSG 2026 | POCA 2002 | FCA FCG | OFSI

---

### ✅ Module 5 — Regulatory Reporting (COREP & FinRep) (In Progress)
**Tools:** Excel, Power BI  
**Files:** `excel_models/Regulatory_Reporting_Model.xlsx`

- COREP capital adequacy returns: C01 Own Funds, C02 Capital Requirements, C47 Leverage Ratio
- Capital ratios: CET1 14% (min 4.5%) ✅ | Tier 1 15% (min 6%) ✅ | Total Capital 18% (min 8%) ✅
- Leverage ratio: 6.85% (min 3.5%) ✅ — all ratios PASS regulatory minimums
- FinRep P&L (F02) and Balance Sheet (F01) in EBA standardised format
- Data quality reconciliation: FinRep vs management accounts — all lines reconcile to zero
- PRA submission calendar: 5 returns, zero missed deadlines FY2024
- Regulatory framework: CRR | EBA ITS | Basel III | UK Leverage Ratio Framework

---

### ✅ Module 6 — Internal Audit & Controls
**Tools:** Excel, Word  
**Files:** `audit_documents/Audit_Planning_Documents.xlsx` | `audit_documents/Risk_Control_Matrix.xlsx` | `audit_documents/Internal_Audit_Report_FINAL.docx`

- Audit Universe: 25 auditable entities across 10 HIGH, 10 MEDIUM, 5 LOW risk categories
- Annual Audit Plan: 4 audits planned across FY2025 quarters
- Risk & Control Matrix: 23 controls across 5 process areas
- Controls Testing Log: 23 tests, 19 PASS (83% pass rate), 4 FAIL
- Internal Audit Report: PARTIALLY SATISFACTORY opinion, 3 HIGH findings, 1 LOW finding
- Standards: IIA Global Internal Audit Standards (January 2025) | UK Internal Audit Code of Practice (January 2025)

---

## 🗄️ Data Sources

All data is publicly available from the Bank of England:

| Dataset | BoE Series Code | Description |
|---------|----------------|-------------|
| Bank Base Rate | IUMABEDR | Official Bank Rate |
| Variable Mortgage Rate | IUMTLMV | Effective interest rates — variable mortgages |
| Fixed Mortgage Rate | IUMTLMF | Effective interest rates — fixed mortgages |
| Consumer Credit | LPMVWYR | Consumer credit lending |
| Loan Write-offs | LPMB3ZX | Sectoral loan write-offs |
| MFI Income (B3.1) | Bankstats Table B3.1 | Monetary financial institutions income |
| FSR Data Annex | FSR Annex | Financial Stability Report data |

---

## 🛠️ Tools & Technologies

| Tool | Version | Use |
|------|---------|-----|
| Python | 3.11 | Data pipeline, IFRS 9 ECL model |
| pandas | Latest | Data cleaning and transformation |
| SQLite | 3.x | Database storage and SQL queries |
| DB Browser for SQLite | 3.12 | SQL query execution |
| Excel | 16.x (Mac) | Financial models, scorecards |
| Tableau Public | Latest | FP&A and AML dashboards |
| Power BI | Browser | Regulatory and executive reporting |
| VS Code | Latest | Python and SQL development |

---

## 📁 Repository Structure

```
UK-Financial-Risk-Intelligence-Platform/
├── README.md
├── scripts/
│   ├── boe_pipeline.py          # BoE data pipeline (Module 1)
│   └── ifrs9_ecl_model.py       # IFRS 9 ECL Python model (Module 3)
├── sql_queries/
│   ├── 01_data_validation.sql   # BoE data validation queries
│   ├── aml_tm_rules_simple.sql  # AML TM rules engine (Module 4)
│   └── outputs/                 # SQL query output CSVs
│       ├── TM001_structuring_results.csv
│       ├── TM002_rapid_inout_results.csv
│       ├── TM003_high_risk_jurisdiction_results.csv
│       ├── TM004_dormant_account_results.csv
│       ├── TM005_pep_high_value_results.csv
│       ├── TM006_cash_intensity_results.csv
│       ├── TM007_round_tripping_results.csv
│       └── TM008_sanctions_results.csv
├── excel_models/
│   ├── FPA_PL_Model.xlsx                  # Module 2 — FP&A
│   ├── Credit_Risk_Scorecard.xlsx         # Module 3 — Credit Risk
│   ├── AML_Transaction_Monitoring.xlsx    # Module 4 — AML
│   └── Regulatory_Reporting_Model.xlsx    # Module 5 — Regulatory
├── audit_documents/
│   ├── Audit_Planning_Documents.xlsx      # Module 6 — Audit Universe & Plan
│   ├── Risk_Control_Matrix.xlsx           # Module 6 — RCM & Testing Log
│   ├── Internal_Audit_Report_FINAL.pdf    # Module 6 — Audit Report
│   └── SAR_CUST018_ALT001.pdf            # Module 4 — SAR Document
├── portfolio/
│   ├── FPA_Dashboard.pdf                  # Tableau export
│   └── screenshots/                       # Power BI screenshots
└── data_processed/
    └── BoE_Finance_Platform.db            # SQLite database
```

---

## 🎓 Regulatory Frameworks Referenced

| Framework | Module | What it covers |
|-----------|--------|---------------|
| MLR 2017 | AML | Money Laundering Regulations — CDD, EDD, SAR obligations |
| JMLSG 2026 | AML | Industry AML guidance — KYC/CDD best practice |
| POCA 2002 | AML | SAR filing (S.330), tipping off offence (S.333A) |
| FCA FCG | AML | FCA Financial Crime Guide — supervisory expectations |
| OFSI | AML | UK sanctions screening — consolidated sanctions list |
| IFRS 9 | Credit Risk | Impairment staging — 12-month and lifetime ECL |
| Basel III | Credit Risk | Risk weights — 35% mortgages, 75% retail, 100% corporate |
| BoE ACS | Credit Risk | Annual Cyclical Scenario — stress test calibration |
| COREP/EBA ITS | Reg Reporting | Capital adequacy returns — C01, C02, C47 |
| FinRep/EBA ITS | Reg Reporting | Financial reporting — F01, F02 |
| IIA Standards 2025 | Internal Audit | IIA Global Internal Audit Standards (January 2025) |
| UK IA Code 2025 | Internal Audit | UK Internal Audit Code of Practice (January 2025) |

---

## 👤 About

**Pallavi Sojan**  
MSc Finance & Risk Management — University of Stirling  
ICA Advanced Certificate in AML (July 2026 cohort)  
Edinburgh, UK | 

**Target roles:** AML/KYC Analyst | FP&A Analyst | Credit Risk Analyst | Regulatory Reporting Analyst 

📧 *pallavisojan92@gmail.com*  
💼 *linkedin.com/in/pallavi-sojan*  

---

*Data source: Bank of England Statistical Database - all data publicly available at bankofengland.co.uk/boeapps/database*  
*Caledonia Bank plc is a fictional entity created for portfolio purposes only*
