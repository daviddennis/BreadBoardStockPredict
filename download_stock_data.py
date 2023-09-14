import yfinance as yf
import pandas as pd

# Define a few stock symbols
ticker_symbols = ["AAPL", "MSFT", "GOOGL", "AMZN"]

all_data = []

# Pull opening price data from Yahoo Finance
for ticker in ticker_symbols:
    stock = yf.Ticker(ticker)
    data = stock.history(period="5y", interval="1d")
    
    # Extract relevant data and store in the list
    for date, open_price in data['Open'].items():
        all_data.append([ticker, date, open_price])

# Save the DataFrame to CSV
df = pd.DataFrame(all_data, columns=["Symbol", "Date", "Opening Price"])
df.to_csv('data/stock_opening_prices.csv', index=False)
