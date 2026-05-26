import yfinance as yf
import pandas as pd

sofi = yf.Ticker("SOFI")

# Pull the three financial statements
income_statement = sofi.financials
balance_sheet = sofi.balance_sheet
cash_flow = sofi.cashflow

# Print them so we can see what we're working with
print("=== INCOME STATEMENT ===")
print(income_statement)

print("\n=== CASH FLOW ===")
print(cash_flow)
