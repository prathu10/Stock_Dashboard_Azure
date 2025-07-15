import os
import pyodbc
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

server = os.getenv('SQL_SERVER')
database = os.getenv('SQL_DATABASE')
username = os.getenv('SQL_USERNAME')
password = os.getenv('SQL_PASSWORD')

conn_str = (
    f'DRIVER={{ODBC Driver 18 for SQL Server}};'
    f'SERVER={server};'
    f'DATABASE={database};'
    f'UID={username};'
    f'PWD={password};'
    'Encrypt=yes;'
    'TrustServerCertificate=no;'
    'Connection Timeout=30;'
)

conn = pyodbc.connect(conn_str)
cursor = conn.cursor()
cursor.fast_executemany = True  

# Path to intraday CSVs
csv_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'intraday'))

for filename in os.listdir(csv_folder):
    if filename.endswith('.csv'):
        filepath = os.path.join(csv_folder, filename)
        print(f"Uploading: {filename}")
        try:
            df = pd.read_csv(filepath)



            # --- Data Cleaning and Preparation ---
            # Trim and truncate 'symbol' to 50 characters max
            df['symbol'] = df['symbol'].astype(str).str.strip().str.slice(0, 50)

            # Convert datetime to pandas datetime type, then format as string in ISO format if needed
            # Adjust this if your DB expects specific datetime format
            df['Datetime'] = pd.to_datetime(df['Datetime'], errors='coerce')
            if df['Datetime'].isnull().any():
                raise ValueError(f"Invalid datetime values found in {filename}")

            # Convert numeric columns safely, replace invalid values with NaN then drop rows with NaN in critical columns
            numeric_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
            df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')

            # Drop rows missing required fields
            df.dropna(subset=['symbol', 'Datetime', 'Open', 'High', 'Low', 'Close', 'Volume'], inplace=True)

            # Prepare list of tuples for executemany
            data_to_insert = list(zip(
                df['symbol'],
                df['Datetime'].dt.strftime('%Y-%m-%d %H:%M:%S'),  # format datetime as string
                df['Open'],
                df['High'],
                df['Low'],
                df['Close'],
                df['Volume']
            ))

            cursor.executemany('''
                INSERT INTO dbo.StockIntraday (symbol, [Datetime], [Open], [High], [Low], [Close], [Volume])
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', data_to_insert)

            conn.commit()
            print(f"  Uploaded: {filename}")

        except Exception as e:
            print(f" Error uploading {filename}: {e}")

cursor.close()
conn.close()
