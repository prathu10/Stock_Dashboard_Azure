import os
import pyodbc
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# SQL connection string
conn_str = (
    f'DRIVER={{ODBC Driver 18 for SQL Server}};'
    f'SERVER={os.getenv("SQL_SERVER")};'
    f'DATABASE={os.getenv("SQL_DATABASE")};'
    f'UID={os.getenv("SQL_USERNAME")};'
    f'PWD={os.getenv("SQL_PASSWORD")};'
    'Encrypt=yes;'
    'TrustServerCertificate=no;'
    'Connection Timeout=30;'
)
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()
cursor.fast_executemany = True

# Base folder of this script's data
base_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))

category_mapping = {
    'daily': {
        'folder': os.path.join(base_folder, 'daily'),
        'table': 'StockDaily',
        'columns': ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock_Splits', 'symbol'],
        'date_col': 'Date',
        'numeric_cols': ['Open', 'High', 'Low', 'Close', 'Volume', 'Dividends'],
        'text_cols': ['Stock_Splits', 'symbol']
    },
    'weekly': {
        'folder': os.path.join(base_folder, 'weekly'),
        'table': 'StockWeekly',
        'columns': ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock_Splits', 'symbol'],
        'date_col': 'Date',
        'numeric_cols': ['Open', 'High', 'Low', 'Close', 'Volume', 'Dividends'],
        'text_cols': ['Stock_Splits', 'symbol']
    },
    'monthly': {
        'folder': os.path.join(base_folder, 'monthly'),
        'table': 'StockMonthly',
        'columns': ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock_Splits', 'symbol'],
        'date_col': 'Date',
        'numeric_cols': ['Open', 'High', 'Low', 'Close', 'Volume', 'Dividends'],
        'text_cols': ['Stock_Splits', 'symbol']
    },
    'dividends': {
        'folder': os.path.join(base_folder, 'dividends'),
        'table': 'StockDividends',
        'columns': ['Date', 'Dividends', 'symbol'],
        'date_col': 'Date',
        'numeric_cols': ['Dividends'],
        'text_cols': []
    },
    'splits': {
        'folder': os.path.join(base_folder, 'splits'),
        'table': 'StockSplits',
        'columns': ['Date', 'Stock_Splits', 'symbol'],
        'date_col': 'Date',
        'numeric_cols': [],
        'text_cols': ['Stock_Splits', 'symbol']
    },
    
}

def clean_and_prepare_df(df, info):
    df['symbol'] = df['symbol'].astype(str).str.strip().str[:50]

    if 'date_col' in info:
        df[info['date_col']] = pd.to_datetime(df[info['date_col']], errors='coerce', utc=True)
        df[info['date_col']] = df[info['date_col']].dt.tz_convert(None).dt.normalize()  


        # Debug: log rows with invalid dates
        invalid_dates = df[df[info['date_col']].isna()]
        if not invalid_dates.empty:
            print(f"Warning: {len(invalid_dates)} rows with invalid dates in {info['table']}")
            print(invalid_dates[['symbol', info['date_col']]])

        # Drop invalid dates
        df = df[df[info['date_col']].notna()]

        # Filter out dates before SQL Server datetime min (1753-01-01)
        min_sql_date = pd.Timestamp('1753-01-01')
        df = df[df[info['date_col']] >= min_sql_date]
        out_of_range = df[df[info['date_col']] < min_sql_date]
        if not out_of_range.empty:
            print(f"Warning: {len(out_of_range)} rows with dates before 1753-01-01 in {info['table']}")
            print(out_of_range[['symbol', info['date_col']]])
        df = df[df[info['date_col']] >= min_sql_date]

    for col in info.get('numeric_cols', []):
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    for col in info.get('text_cols', []):
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    subset_cols = ['symbol']
    if 'date_col' in info:
        subset_cols.append(info['date_col'])
    df.dropna(subset=subset_cols, inplace=True)

    return df

for category, info in category_mapping.items():
    print(f"\n==== Uploading {category.upper()} data ====")
    folder_path = info['folder']

    if not os.path.exists(folder_path):
        print(f"  Folder does not exist: {folder_path}")
        continue

    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            filepath = os.path.join(folder_path, filename)
            print(f"Uploading: {filename}")
            try:
                df = pd.read_csv(filepath)
                df = clean_and_prepare_df(df, info)

                print(f"Preview of cleaned data ({filename}):")
                print(df.head())

                insert_cols = info['columns']
                data_to_insert = []
                for _, row in df.iterrows():
                    values = []
                    for col in insert_cols:
                        if col in df.columns:
                            val = row[col]
                            if pd.isna(val):
                                val = None
                            values.append(val)
                        else:
                            values.append(None)
                    data_to_insert.append(tuple(values))

                placeholders = ', '.join(['?'] * len(insert_cols))
                columns_str = ', '.join([f'[{c}]' for c in insert_cols])

                cursor.executemany(f'''
                    INSERT INTO dbo.{info['table']} ({columns_str})
                    VALUES ({placeholders})
                ''', data_to_insert)

                conn.commit()
                print(f"  Uploaded: {filename}")

            except Exception as e:
                print(f" Error uploading {filename}: {e}")

cursor.close()
conn.close()
