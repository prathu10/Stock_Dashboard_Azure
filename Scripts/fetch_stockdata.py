import yfinance as yf
import pandas as pd
import os
from datetime import datetime
import time
import json

symbols_df = pd.read_csv('../symbols.csv')
symbols = symbols_df['Symbol'].tolist()

# Base data folder
base_dir = 'data'
os.makedirs(base_dir, exist_ok=True)

# Define category folders
categories = ['intraday', 'daily', 'weekly', 'monthly', 'dividends', 'splits', 'fundamentals']

# Create category folders if they don't exist
for category in categories:
    os.makedirs(os.path.join(base_dir, category), exist_ok=True)

for symbol in symbols:
    try:
        print(f"Fetching data for {symbol}...")

        ticker = yf.Ticker(symbol)

        # 1. Intraday data (last 5 days, 1 min interval)
        intraday = ticker.history(period="5d", interval="1m")
        if not intraday.empty:
            intraday['symbol'] = symbol
            intraday.reset_index(inplace=True)
            intraday.to_csv(os.path.join(base_dir, 'intraday', f"{symbol}_intraday.csv"), index=False)

        # 2. Daily historical data (last 5 years)
        daily = ticker.history(period="5y", interval="1d")
        if not daily.empty:
            daily['symbol'] = symbol
            daily.reset_index(inplace=True)
            daily.to_csv(os.path.join(base_dir, 'daily', f"{symbol}_daily.csv"), index=False)

        # 3. Weekly historical data (max available)
        weekly = ticker.history(period="max", interval="1wk")
        if not weekly.empty:
            weekly['symbol'] = symbol
            weekly.reset_index(inplace=True)
            weekly.to_csv(os.path.join(base_dir, 'weekly', f"{symbol}_weekly.csv"), index=False)

        # 4. Monthly historical data (max available)
        monthly = ticker.history(period="max", interval="1mo")
        if not monthly.empty:
            monthly['symbol'] = symbol
            monthly.reset_index(inplace=True)
            monthly.to_csv(os.path.join(base_dir, 'monthly', f"{symbol}_monthly.csv"), index=False)

        # 5. Dividends
        dividends = ticker.dividends.reset_index()
        if not dividends.empty:
            dividends['symbol'] = symbol
            dividends.to_csv(os.path.join(base_dir, 'dividends', f"{symbol}_dividends.csv"), index=False)

        # 6. Splits
        splits = ticker.splits.reset_index()
        if not splits.empty:
            splits['symbol'] = symbol
            splits.to_csv(os.path.join(base_dir, 'splits', f"{symbol}_splits.csv"), index=False)

        # 7. Fundamentals & Info
        info = ticker.info
        if info:
            with open(os.path.join(base_dir, 'fundamentals', f"{symbol}_info.json"), "w") as f:
                json.dump(info, f)

        print(f" Saved all data for {symbol}")

        time.sleep(1)  # polite pause

    except Exception as e:
        print(f" Failed for {symbol}: {e}")
