import os
import json
import pyodbc
from dotenv import load_dotenv

# Load credentials from .env
load_dotenv()

# SQL Azure connection
conn = pyodbc.connect(
    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
    f"SERVER={os.getenv('SQL_SERVER')};"
    f"DATABASE={os.getenv('SQL_DATABASE')};"
    f"UID={os.getenv('SQL_USERNAME')};"
    f"PWD={os.getenv('SQL_PASSWORD')};"
    "TrustServerCertificate=yes"
)
cursor = conn.cursor()

# Columns in the StockFundamentals table
allowed_columns = [
    "symbol", "address1", "city", "state", "zip", "country", "phone", "website",
    "industry", "sector", "longBusinessSummary", "fullTimeEmployees", "marketCap",
    "volume", "open", "dayLow", "dayHigh", "trailingPE", "forwardPE", "dividendRate",
    "dividendYield", "beta", "bookValue", "priceToBook", "revenuePerShare",
    "returnOnAssets", "returnOnEquity", "grossMargins", "operatingMargins",
    "profitMargins", "totalCash", "totalDebt", "totalRevenue", "currency"
]

# Path to folder with *_info.json files
json_folder = r"F:\PROJECTS\Stock Market Dashboard with Real-Time Data and Azure Data Stack\PROJECT\Scripts\data\fundamentals"

# Loop through all *_info.json files
for filename in os.listdir(json_folder):
    if filename.endswith('_info.json'):
        filepath = os.path.join(json_folder, filename)

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                json_data = json.load(f)

            # Filter fields to match table columns
            data = {k: json_data.get(k) for k in allowed_columns if k in json_data}

            # If symbol is missing in file, infer from filename
            if "symbol" not in data:
                data["symbol"] = filename.replace('_info.json', '')

            # Skip empty rows
            if not data:
                print(f" Skipping empty data: {filename}")
                continue

            # Build SQL insert with bracketed column names
            cols = ", ".join(f"[{col}]" for col in data.keys())
            placeholders = ", ".join(["?"] * len(data))
            values = list(data.values())

            query = f"INSERT INTO StockFundamentals ({cols}) VALUES ({placeholders})"
            cursor.execute(query, values)
            conn.commit()

            print(f" Uploaded: {filename}")

        except Exception as e:
            print(f" Error processing {filename}: {e}")

# Close resources
cursor.close()
conn.close()
