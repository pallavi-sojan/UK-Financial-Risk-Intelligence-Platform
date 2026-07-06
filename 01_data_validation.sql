-- ============================================================
-- CALEDONIA BANK PLC
-- BOE DATA VALIDATION QUERIES
-- File     : 01_data_validation.sql
-- Author   : Pallavi Sojan
-- Database : BoE_Finance_Platform.db
-- Purpose  : Validate data quality after pipeline run
-- Date     : 2025
-- ============================================================


-- ── QUERY 1 — ROW COUNTS AND DATE RANGES ─────────────────────
-- Confirm all 3 tables loaded with expected row counts
-- and date ranges covering 2010 to present

SELECT
    'master_boe_data'       AS table_name,
    COUNT(*)                AS row_count,
    MIN(date)               AS earliest_date,
    MAX(date)               AS latest_date
FROM master_boe_data

UNION ALL

SELECT
    'loan_writeoffs'        AS table_name,
    COUNT(*)                AS row_count,
    MIN(date)               AS earliest_date,
    MAX(date)               AS latest_date
FROM loan_writeoffs

UNION ALL

SELECT
    'mfi_income'            AS table_name,
    COUNT(*)                AS row_count,
    MIN(date)               AS earliest_date,
    MAX(date)               AS latest_date
FROM mfi_income;


-- ── QUERY 2 — NULL CHECK ──────────────────────────────────────
-- Flag any rows with missing values in key columns
-- Expected result: 0 rows returned (no nulls)

SELECT
    date,
    base_rate_pct,
    variable_mortgage_rate_pct,
    consumer_credit_gbm
FROM master_boe_data
WHERE
    base_rate_pct               IS NULL
    OR variable_mortgage_rate_pct IS NULL
    OR consumer_credit_gbm        IS NULL;


-- ── QUERY 3 — MORTGAGE SPREAD CALCULATION ─────────────────────
-- Calculate spread between variable mortgage rate and base rate
-- Spread should be positive (mortgages priced above base rate)
-- Shows most recent 10 observations

SELECT
    date,
    ROUND(base_rate_pct, 3)                 AS base_rate_pct,
    ROUND(variable_mortgage_rate_pct, 3)    AS variable_mortgage_rate_pct,
    ROUND(variable_mortgage_rate_pct
          - base_rate_pct, 3)               AS mortgage_spread_pct
FROM master_boe_data
WHERE base_rate_pct IS NOT NULL
  AND variable_mortgage_rate_pct IS NOT NULL
ORDER BY date DESC
LIMIT 10;


-- ── QUERY 4 — YEAR ON YEAR RATE CHANGES ──────────────────────
-- Show annual average base rate by year
-- Useful for identifying rate cycles in the data

SELECT
    year,
    ROUND(AVG(base_rate_pct), 3)            AS avg_base_rate_pct,
    ROUND(MIN(base_rate_pct), 3)            AS min_base_rate_pct,
    ROUND(MAX(base_rate_pct), 3)            AS max_base_rate_pct,
    COUNT(*)                                AS observations
FROM master_boe_data
WHERE base_rate_pct IS NOT NULL
GROUP BY year
ORDER BY year DESC;


-- ── QUERY 5 — LOAN WRITE-OFF TREND ───────────────────────────
-- Show loan write-offs by year
-- Useful for identifying credit stress periods (e.g. Covid 2020-21)

SELECT
    SUBSTR(date, 1, 4)                      AS year,
    ROUND(SUM(loan_writeoffs_gbm), 0)       AS total_writeoffs_gbm,
    ROUND(AVG(loan_writeoffs_gbm), 0)       AS avg_quarterly_writeoffs_gbm,
    COUNT(*)                                AS quarters
FROM loan_writeoffs
WHERE loan_writeoffs_gbm IS NOT NULL
GROUP BY SUBSTR(date, 1, 4)
ORDER BY year DESC;


-- ── QUERY 6 — DATA QUALITY SUMMARY ───────────────────────────
-- Overall data quality score for the master dataset
-- Expected: null_count = 0, completeness_pct = 100%

SELECT
    COUNT(*)                                AS total_rows,
    SUM(CASE WHEN base_rate_pct IS NULL
             THEN 1 ELSE 0 END)             AS null_base_rate,
    SUM(CASE WHEN variable_mortgage_rate_pct IS NULL
             THEN 1 ELSE 0 END)             AS null_variable_rate,
    ROUND(
        100.0 * SUM(CASE WHEN base_rate_pct IS NOT NULL
                         THEN 1 ELSE 0 END)
        / COUNT(*), 1
    )                                       AS base_rate_completeness_pct
FROM master_boe_data;


-- ── QUERY 7 — RECENT DATA CHECK ───────────────────────────────
-- Show the 5 most recent records to confirm data is current

SELECT
    date,
    ROUND(base_rate_pct, 3)                 AS base_rate_pct,
    ROUND(variable_mortgage_rate_pct, 3)    AS variable_mortgage_pct,
    ROUND(fixed_mortgage_rate_pct, 3)       AS fixed_mortgage_pct,
    ROUND(consumer_credit_gbm, 0)           AS consumer_credit_gbm,
    ROUND(mortgage_spread_pct, 3)           AS mortgage_spread_pct
FROM master_boe_data
ORDER BY date DESC
LIMIT 5;

-- ============================================================
-- END OF FILE
-- 01_data_validation.sql | Caledonia Bank plc | Pallavi Sojan
-- ============================================================