import pandas as pd
from pandas import DataFrame
from datetime import datetime,timedelta
from functools import reduce
import matplotlib.pyplot as plt 
import numpy as np
import math
from statistics import mean 
from sklearn.metrics import mean_squared_error

stocks = pd.read_csv("/Users/shreyaspatel/Desktop/Machine_Learning/Personal/Fama_French/Data/Stocks.csv")


stocks = stocks.groupby('SimFinID').mean()
temp = stocks

stocks = temp
values = {
 'ret' : 11,
 'Dividends': 30,
 'Market Capitalisation': 20,
 'Book to Market': 30,
 'Cash & Cash Equivalents': 3,
 'Cash From Financing Activities': 5,
 'Cash From Investing Activities': 5,
 'Cash From Operating Activities': 0,
 'Change in Working Capital': 12,
 'Current Assets': 11,
 'Current Liabilities': 5,
 'Enterprise Value': 0,
 'EBITDA': 2,
 'EV / Sales': 30,
 'Net Profit': 0,
 'Net Profit Margin': 20,
 'Operating Margin': 20,
 'Total Assets': 0,
 'Total Liabilities': 5,
 'Total Equity': 5,
 'Short term debt': 10,
 'Long Term Debt': 5}

for i in stocks:
    stocks = stocks.drop(stocks[i].abs().nlargest(values[i]).index.values)
    # plt.title(i)
    # plt.plot(stocks[i])
    # plt.show()

pd.DataFrame(list(stocks.index),columns=['SimFinID']).to_csv('ID.csv',index=False)

