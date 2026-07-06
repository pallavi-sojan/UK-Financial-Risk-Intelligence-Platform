import pandas as pd
import sqlite3

db_path = 'data_processed/BoE_Finance_Platform.db'
conn = sqlite3.connect(db_path)

files = {
    'master_boe_data': 'data_processed/Master_BoE_Dataset.csv',
    'loan_writeoffs': 'data_processed/boe_loan_writeoffs.csv',
    'mfi_income': 'data_processed/mfi_income_annually.csv',
}

for table_name, file_path in files.items():
    df = pd.read_csv(file_path, encoding='utf-8-sig')
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    count = pd.read_sql(f'SELECT COUNT(*) as rows FROM {table_name}', conn)
    print(f'{table_name}: {count.iloc[0,0]} rows loaded')

conn.close()
print('\nDatabase saved to:', db_path)
