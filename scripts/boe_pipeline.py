# ============================================================
# CALEDONIA BANK PLC
# BANK OF ENGLAND DATA PIPELINE
# Author   : Pallavi Sojan
# Purpose  : Download, clean and load BoE public data into SQLite
# Database : BoE_Finance_Platform.db
# Date     : 2025
# ============================================================

import pandas as pd
import sqlite3
import os
import requests
from datetime import datetime

print("=" * 60)
print("  CALEDONIA BANK PLC — BoE DATA PIPELINE")
print("  Author: Pallavi Sojan | MSc Finance & Risk Management")
print("=" * 60)

# ── FILE PATHS ────────────────────────────────────────────────
DATA_RAW       = "data_raw"
DATA_PROCESSED = "data_processed"
DB_PATH        = os.path.join(DATA_PROCESSED, "BoE_Finance_Platform.db")

# Create directories if they don't exist
os.makedirs(DATA_RAW, exist_ok=True)
os.makedirs(DATA_PROCESSED, exist_ok=True)

print(f"\nData raw folder:       {DATA_RAW}/")
print(f"Data processed folder: {DATA_PROCESSED}/")
print(f"Database path:         {DB_PATH}")

# ── LOAD RAW DATA ─────────────────────────────────────────────
# Download CSVs manually from bankofengland.co.uk/boeapps/database
# and save to data_raw/ folder before running this script
# Series codes:
#   IUMABEDR  — Bank Base Rate
#   IUMTLMV   — Variable Mortgage Rate
#   IUMTLMF   — Fixed Mortgage Rate
#   LPMVWYR   — Consumer Credit
#   LPMB3ZX   — Loan Write-offs

print("\n" + "=" * 60)
print("  STEP 1 — LOAD RAW DATA FILES")
print("=" * 60)

def load_boe_csv(filename, value_col_name):
    """Load a BoE CSV file and standardise column names."""
    filepath = os.path.join(DATA_RAW, filename)
    if not os.path.exists(filepath):
        print(f"  ⚠ File not found: {filepath} — skipping")
        return None
    try:
        df = pd.read_csv(filepath, skiprows=0)
        df.columns = ['date', value_col_name]
        df['date'] = pd.to_datetime(df['date'], dayfirst=True, errors='coerce')
        df = df.dropna(subset=['date'])
        df[value_col_name] = pd.to_numeric(df[value_col_name], errors='coerce')
        print(f"  ✓ Loaded {filename}: {len(df)} rows | {df['date'].min().year} - {df['date'].max().year}")
        return df
    except Exception as e:
        print(f"  ✗ Error loading {filename}: {e}")
        return None

# Load each dataset
df_base_rate    = load_boe_csv("boe_base_rate.csv",         "base_rate_pct")
df_var_mortgage = load_boe_csv("variable_mortgage_rate.csv", "variable_mortgage_rate_pct")
df_fix_mortgage = load_boe_csv("fixed_mortgage_rate.csv",    "fixed_mortgage_rate_pct")
df_consumer     = load_boe_csv("consumer_credit.csv",        "consumer_credit_gbm")
df_writeoffs    = load_boe_csv("loan_writeoffs.csv",         "loan_writeoffs_gbm")

# ── CLEAN AND MERGE ───────────────────────────────────────────
print("\n" + "=" * 60)
print("  STEP 2 — CLEAN AND MERGE DATA")
print("=" * 60)

# Use base rate as the master dataset
dfs = [df for df in [df_base_rate, df_var_mortgage, df_fix_mortgage, df_consumer] if df is not None]

if len(dfs) == 0:
    print("  ⚠ No data files found in data_raw/")
    print("  Please download BoE data files and save to data_raw/ folder")
    print("  Then re-run this script")
else:
    # Merge all datasets on date
    master_df = dfs[0]
    for df in dfs[1:]:
        master_df = pd.merge(master_df, df, on='date', how='outer')

    master_df = master_df.sort_values('date').reset_index(drop=True)

    # Add calculated columns
    if 'variable_mortgage_rate_pct' in master_df.columns and 'base_rate_pct' in master_df.columns:
        master_df['mortgage_spread_pct'] = (
            master_df['variable_mortgage_rate_pct'] - master_df['base_rate_pct']
        )

    # Add time dimensions
    master_df['year']    = master_df['date'].dt.year
    master_df['quarter'] = master_df['date'].dt.quarter
    master_df['month']   = master_df['date'].dt.month

    print(f"  ✓ Master dataset: {len(master_df)} rows")
    print(f"  ✓ Columns: {list(master_df.columns)}")
    print(f"  ✓ Date range: {master_df['date'].min()} to {master_df['date'].max()}")

    # Export to CSV
    master_csv = os.path.join(DATA_PROCESSED, "master_boe_data.csv")
    master_df.to_csv(master_csv, index=False)
    print(f"  ✓ Exported: {master_csv}")

    # ── LOAD INTO SQLITE ──────────────────────────────────────
    print("\n" + "=" * 60)
    print("  STEP 3 — LOAD INTO SQLITE DATABASE")
    print("=" * 60)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Load master data
    master_df.to_sql('master_boe_data', conn, if_exists='replace', index=False)
    count = cursor.execute("SELECT COUNT(*) FROM master_boe_data").fetchone()[0]
    print(f"  ✓ Table: master_boe_data — {count} rows loaded")

    # Load loan write-offs if available
    if df_writeoffs is not None:
        df_writeoffs.to_sql('loan_writeoffs', conn, if_exists='replace', index=False)
        count = cursor.execute("SELECT COUNT(*) FROM loan_writeoffs").fetchone()[0]
        print(f"  ✓ Table: loan_writeoffs — {count} rows loaded")
    else:
        print(f"  ⚠ Table: loan_writeoffs — file not found, skipping")

    # Create MFI income table (placeholder if CSV not available)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS mfi_income (
            date TEXT,
            total_income_gbm REAL,
            net_interest_income_gbm REAL,
            non_interest_income_gbm REAL
        )
    """)
    print(f"  ✓ Table: mfi_income — structure created")

    conn.commit()

    # ── VALIDATE ──────────────────────────────────────────────
    print("\n" + "=" * 60)
    print("  STEP 4 — VALIDATION")
    print("=" * 60)

    tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    print(f"  ✓ Tables in database: {[t[0] for t in tables]}")

    for table_name in [t[0] for t in tables]:
        count = cursor.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
        print(f"  ✓ {table_name}: {count} rows")

    conn.close()
    print(f"\n  ✓ Database saved: {DB_PATH}")

# ── SUMMARY ───────────────────────────────────────────────────
print("\n" + "=" * 60)
print("  PIPELINE COMPLETE")
print("=" * 60)
print("  Data source: Bank of England Statistical Database")
print("  URL: bankofengland.co.uk/boeapps/database")
print("  Series: IUMABEDR | IUMTLMV | IUMTLMF | LPMVWYR | LPMB3ZX")
print("\n  Output files:")
print(f"  - {DATA_PROCESSED}/master_boe_data.csv")
print(f"  - {DB_PATH}")
print("\n  Tables created:")
print("  - master_boe_data")
print("  - loan_writeoffs")
print("  - mfi_income")
print("\n" + "=" * 60)
print("  Caledonia Bank plc | Pallavi Sojan | 2025")
print("=" * 60)