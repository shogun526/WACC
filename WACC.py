import yfinance as yf
from curl_cffi import requests
session = requests.Session(impersonate="chrome")


# (E/(E+D)*Ke)+(D/(D+E)*Kd*(1-T))
#Define ticker
tax =  0.21 #Corporate tax rate in the us, only input so far
ticker = "AMZN"
msft = yf.Ticker(ticker, session = session)
#Introduce all 3 statements
income_statement = msft.financials.T
cash_flow_statement = msft.cashflow.T
balance_sheet = msft.balance_sheet.T

#Find total debt
debt = balance_sheet["Total Debt"].iloc[0]
equity = balance_sheet["Total Assets"].iloc[0]-balance_sheet["Total Liabilities Net Minority Interest"].iloc[0]
capital = debt + equity
#Finding Risk free rate (^IRX), ticker is 13 weeks US treasury bonds
irx_data = yf.Ticker("^IRX")
irx_history = irx_data.history(period="5d")

risk_free_rate = irx_history["Close"].iloc[-1] / 100  # Convert percentage to decimal

#Compute cost of debt
#We will do Interest expense/total debt
interest = income_statement["Interest Expense"].iloc[0]
kd = interest/debt

#Compute cost of Equity

#First, find beta
beta = msft.info["beta"]
#find Market rate of return. Compare to S&P 500 ig
mrr = 0.1 #Let us use the classic 10% return atm bcuz I dont feel like it

ke = risk_free_rate + beta*(mrr-risk_free_rate)
#Finally, get to WACC
# (E/(E+D)*Ke)+(D/(D+E)*Kd*(1-T))

WACC = (equity/capital)*ke+((debt/capital)*kd*(1-tax))
print("debt is :",debt)
print("equity is :",equity)
print("risk free rate is :",risk_free_rate)
print("Cost of debt is:",kd)
print("found beta is :",beta)
print("Cost of equity is :",ke)
print("Wacc is :",WACC)