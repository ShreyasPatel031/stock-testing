import pandas as pd
from pandas import DataFrame
from datetime import datetime,timedelta
from functools import reduce
import matplotlib.pyplot as plt 
import numpy as np
import math
from statistics import mean 
from sklearn.metrics import mean_squared_error

inp = pd.read_csv("/Users/shreyaspatel/Desktop/Machine_Learning/Personal/Fama_French/Data/Total_Data.csv")
inp.loc[:,('Publish date')]= pd.to_datetime(inp['Publish date'])

var = [
'Dividends',
'Market Capitalisation','Book to Market',
'Cash & Cash Equivalents','Cash From Financing Activities','Cash From Investing Activities','Cash From Operating Activities',
'Change in Working Capital','Current Assets','Current Liabilities',
'Enterprise Value','EBITDA','EV / Sales','Change in Working Capital',
'Net Profit','Net Profit Margin','Operating Margin',
'Total Assets','Total Liabilities','Total Equity','Short term debt','Long Term Debt',
]

date_format = "%Y-%m-%d"
curr  = datetime.strptime('2015-07-01', date_format)
last = datetime.strptime('2019-07-01', date_format)

split=8
delta = (last - curr)/split

def dat(id):
    test = inp.loc[( inp['SimFinID'] == id)]
    test.set_index( test['Publish date'],inplace=True )
    # print(id,test.loc[ test['Indicator Name'] == 'Share Price' ])
    fin = pd.DataFrame(index = test.loc[ test['Indicator Name'] == 'Share Price' ]['Publish date']) 
    
    fin['curr'] = test.loc[ test['Indicator Name'] == 'Share Price' ]['IndicatorValue']
    mcap = test.loc[ test['Indicator Name'] == 'Market Capitalisation' ]['IndicatorValue'].mean()
    fin['div'] = ( ( test.loc[ test['Indicator Name'] == 'Dividends' ]['IndicatorValue'] ) * ( fin['curr'].mean() / mcap ) )
    fin['div'] = fin['div'].rolling(window='180D').sum()
    fin['prev'] = fin['curr'].rolling(window='180D').apply( lambda X : X[0] if X[0] > 0 else np.nan ,raw=False  ) 
    fin['ret'] = (fin['curr'] - fin['prev'] - fin['div']) / fin['curr']
    
    for i in var:
        fin[i] = test.loc[ test['Indicator Name'] == i ]['IndicatorValue']
        fin[i] = fin[i].rolling(window='180D').mean()
    
    fin = fin.loc[curr+delta:]
    fin = fin.replace([np.inf, -np.inf], np.nan)
    fin.dropna(inplace=True)
    fin = fin.drop( columns = ['curr','div','prev'])
    fin['SimFinID'] = id
    
    return fin


op = pd.DataFrame()

for i in ids['SimFinID'] : 
    print(i)
    df = dat(i)
    op = pd.concat([op,df],axis=0)

op.set_index([op.index,'SimFinID'],inplace=True)
op.to_csv('Stocks.csv')



