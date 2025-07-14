from alpha_vantage.timeseries import TimeSeries
import pandas as pd
import os
from datetime import datetime

# Replace with your Alpha Vantage API key
API_KEY = 'XU9MHHGCDTB000WC'
STOCK_SYMBOL = 'AAPL'  # You can change this to any stock

# Initialize connection
ts = TimeSeries(key=API_KEY, output_format='pandas')

# Fetch 1-minute interval intraday data
data, meta = ts.get_intraday(symbol=STOCK_SYMBOL, interval='1min', outputsize='compact')

# Create output folder
os.makedirs('../data', exist_ok=True)

# Save to CSV with timestamp
timestamp = datetime.now().strftime('%Y%m%d_%H%M')
filename = f'../data/{STOCK_SYMBOL}_intraday_{timestamp}.csv'
data.to_csv(filename)

print(f"✅ Data saved to {filename}")
