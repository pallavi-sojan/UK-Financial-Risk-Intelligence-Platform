-- ============================================================
-- CALEDONIA BANK PLC
-- AML TRANSACTION MONITORING RULES — SIMPLE VERSION
-- Author   : Pallavi Sojan
-- Basis    : MLR 2017 | JMLSG 2026 | POCA 2002 | OFSI
-- Rules    : TM-001 to TM-008 (8 active rules)
-- Database : BoE_Finance_Platform.db
-- Date     : 23/06/2026
-- ============================================================

/*Rule 1 - Structuring*/
SELECT Customer_ID,
       COUNT(*) AS deposit_count,
       SUM(Amount_GBP) AS total_amount
FROM TRANSACTION_LEDGER
WHERE Transaction_Type = 'Cash Deposit'
AND Amount_GBP BETWEEN 8000 AND 9999
GROUP BY Customer_ID
HAVING COUNT(*) >= 3;

/*Rule2 - Rapid In-Out?*/
SELECT Customer_ID,
       Transaction_ID,
       Amount_GBP,
       Direction,
       Date,
       Counterparty_Country
FROM TRANSACTION_LEDGER
WHERE Customer_ID IN (
    SELECT Customer_ID
    FROM TRANSACTION_LEDGER
    WHERE Direction = 'Credit'
    AND Amount_GBP > 10000
    AND Transaction_Type = 'Wire Transfer IN'
)
AND Amount_GBP > 8000
ORDER BY Customer_ID, Date;

/*Rule 3 — High Risk Jurisdiction*/
SELECT Transaction_ID,
       Customer_ID,
       Amount_GBP,
       Counterparty_Country,
       Counterparty_Bank,
       Direction
FROM TRANSACTION_LEDGER
WHERE Counterparty_Country
IN ('Iran','Russia','Belarus',
    'North Korea','Syria',
    'Venezuela','Libya','Myanmar')
ORDER BY Amount_GBP DESC;

/*Rule 4 — Dormant Account Reactivation*/
SELECT t.Transaction_ID,
       t.Customer_ID,
       t.Amount_GBP,
       t.Date,
       t.Transaction_Type,
       t.Direction,
       cp.Account_Status
FROM TRANSACTION_LEDGER t
JOIN CUSTOMER_PROFILES cp
ON t.Customer_ID = cp.Customer_ID
WHERE cp.Account_Status = 'Dormant'
AND t.Amount_GBP > 5000
ORDER BY t.Amount_GBP DESC;

/*Rule 5 — PEP High Value Transaction*/
SELECT t.Transaction_ID,
       t.Customer_ID,
       t.Amount_GBP,
       t.Date,
       t.Counterparty_Name,
       t.Counterparty_Country,
       t.Direction,
       cp.Customer_Type,
       cp.KYC_Tier
FROM TRANSACTION_LEDGER t
JOIN CUSTOMER_PROFILES cp
ON t.Customer_ID = cp.Customer_ID
WHERE cp.Customer_Type = 'PEP'
AND t.Amount_GBP > 50000
ORDER BY t.Amount_GBP DESC;

/*Rule 6 — Unusual Cash Intensity*/
SELECT t.Customer_ID,
       cp.Monthly_Expected_Turnover_GBP,
       SUM(t.Amount_GBP) AS total_cash_deposits,
       ROUND(SUM(t.Amount_GBP) * 100.0
       / cp.Monthly_Expected_Turnover_GBP, 1)
       AS pct_of_turnover
FROM TRANSACTION_LEDGER t
JOIN CUSTOMER_PROFILES cp
ON t.Customer_ID = cp.Customer_ID
WHERE t.Transaction_Type = 'Cash Deposit'
GROUP BY t.Customer_ID,
         cp.Monthly_Expected_Turnover_GBP
HAVING SUM(t.Amount_GBP) >
       cp.Monthly_Expected_Turnover_GBP * 2;
	  
/*Rule 7 — Round Tripping / Circular Funds */
SELECT Customer_ID,
       Transaction_ID,
       Amount_GBP,
       Direction,
       Counterparty_Name,
       Date
FROM TRANSACTION_LEDGER
WHERE Customer_ID IN ('CUST022','CUST019')
AND Amount_GBP > 25000
ORDER BY Customer_ID, Date;

/*Rule 8 — Sanctions Screening Hit*/
SELECT t.Transaction_ID,
       t.Customer_ID,
       t.Amount_GBP,
       t.Counterparty_Country,
       t.Counterparty_Bank,
       t.Direction,
       'BLOCK AND FREEZE' AS action_required
FROM TRANSACTION_LEDGER t
JOIN CUSTOMER_PROFILES cp
ON t.Customer_ID = cp.Customer_ID
WHERE t.Counterparty_Country
IN ('Russia','Belarus','Iran',
    'North Korea','Syria',
    'Venezuela','Libya','Myanmar')
ORDER BY t.Amount_GBP DESC;

