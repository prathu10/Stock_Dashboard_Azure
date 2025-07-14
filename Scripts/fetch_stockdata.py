from alpha_vantage.timeseries import TimeSeries
import pandas as pd
import os
from datetime import datetime
import time

API_KEY = 'XU9MHHGCDTB000WC'

# Initialize Alpha Vantage TimeSeries object
ts = TimeSeries(key=API_KEY, output_format='pandas')

# Load symbols from CSV
symbols_df = pd.read_csv('symbols.csv')
symbols = symbols_df['Symbol'].tolist()

# Create a folder to save CSVs
os.makedirs('data', exist_ok=True)

for symbol in symbols:
    try:
        print(f"Fetching intraday data for {symbol}...")
        data, meta = ts.get_intraday(symbol=symbol, interval='1min', outputsize='compact')

        # Add symbol column
        data['symbol'] = symbol

        # Create filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M')
        filename = f'data/{symbol}_intraday_{timestamp}.csv'

        # Save data to CSV
        data.to_csv(filename)
        print(f"✅ Saved data for {symbol} to {filename}")

        # Sleep 12 seconds to respect API rate limits (5 calls per minute)
        time.sleep(12)

    except Exception as e:
        print(f"❌ Failed to fetch data for {symbol}: {e}")
