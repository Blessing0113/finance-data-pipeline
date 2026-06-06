import yfinance as yf
import pandas as pd
from datetime import datetime

stocks = ['AAPL', 'GOOGL', 'TSLA', 'MSFT', 'AMZN']

start_date = '2024-01-01'
end_date = datetime.today().strftime('%Y-%m-%d')

def extract_stock_data(tickers, start, end):
    print(f"Extracting data for: {tickers}")
    df = yf.download(tickers, start=start, end=end, auto_adjust=True)
    print(f"Data extracted successfully! Shape:{df.shape}")
    return df
    

raw_data = extract_stock_data(stocks, start_date, end_date)

raw_data.to_csv('C:/Users/vhuga/Desktop/SIDE PROJECTS/finance-data-pipeline/data/raw_stock_data.csv')

print("Raw data saved to data/raw_stock_data.csv")

