import pandas as pd
from pandas import DataFrame
from datetime import datetime,timedelta
from functools import reduce
import matplotlib.pyplot as plt 
import numpy as np
import math
from statistics import mean 
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
from statsmodels.tsa.vector_ar.var_model import VAR

stocks = pd.read_csv("/Users/shreyaspatel/Desktop/Machine_Learning/Personal/Fama_French/Data/Stocks.csv")
ids = pd.read_csv("/Users/shreyaspatel/Desktop/Machine_Learning/Personal/Fama_French/Preprocessing/ID.csv")

stocks.loc[:,('Publish date')]= pd.to_datetime(stocks['Publish date'])
stocks.set_index(stocks['Publish date'],inplace=True)
stocks.sort_index(inplace=True)
stocks = stocks.drop(columns=['Publish date'])


date_format = "%Y-%m-%d"
curr  = datetime.strptime('2015-07-01', date_format)
last = datetime.strptime('2019-07-01', date_format)

split=8
delta = (last - curr)/split

h = pd.DataFrame(index = ids['SimFinID'] , columns = range( 2, split ) )
op = pd.DataFrame(index = ids['SimFinID'] , columns = range( 2, split ) )

for id in ids['SimFinID']:
    sub = stocks[ stocks['SimFinID'] == id ]
    del sub['SimFinID']
    sub.index = pd.DatetimeIndex(sub.index).to_period('D')

    for j in list(range( 2, split )) :
        train = sub.loc[ slice(curr + delta, curr + j*delta ) ]
        test = sub.loc[ slice(curr + j*delta, curr + (j+1)*delta ) ]

        model = VAR(train,freq=None)
        res = model.fit(trend='nc',maxlags=2)
        forecast = res.forecast(res.endog, steps=len(test))
        forecast = pd.DataFrame(forecast,index=test.index,columns=test.columns)

        # plt.plot(train['ret'],label='train')
        # plt.plot(test['ret'],label='test')
        # plt.plot(forecast['ret'],label='forecast')
        # plt.legend()
        # plt.show()

        h.loc[id,j] = forecast['ret'][-1] 
        op.loc[id,j] = test['ret'][-1]
    print(id,math.sqrt(mean_squared_error(op.loc[id],h.loc[id])))
    if( math.sqrt(mean_squared_error(op.loc[id],h.loc[id])) >= 2 ): # assuming failure of convergence ( 37 companies )
        h.drop([id],inplace=True)
        op.drop([id],inplace=True)

h.to_csv('Hypothesis.csv')
op.to_csv('Test.csv')


