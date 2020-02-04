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
ids = pd.read_csv("/Users/shreyaspatel/Desktop/Machine_Learning/Personal/Fama_French/Preprocessing/ID.csv")
stocks = pd.merge(stocks,ids,how='inner')
stocks.loc[:,('Publish date')]= pd.to_datetime(stocks['Publish date'])
stocks.set_index(stocks['Publish date'],inplace=True)
stocks.sort_index(inplace=True)
stocks = stocks.drop(columns=['Publish date'])


date_format = "%Y-%m-%d"
curr  = datetime.strptime('2015-07-01', date_format)
last = datetime.strptime('2019-07-01', date_format)

split=8
delta = (last - curr)/split

emp = pd.DataFrame(index = ids['SimFinID'] , columns = range( 2, split ) )
for i in ids['SimFinID']: 
    sub = stocks[ stocks['SimFinID'] == i ]
    for j in range( 2, split ) :
        train = sub.loc[ slice(curr + delta, curr + j*delta ) ]
        test = sub.loc[ slice(curr + j*delta, curr + (j+1)*delta ) ]
#         display(train,test)
        if( (not train.empty) and (not test.empty) ):
            emp.loc[i,j] = 1


pd.DataFrame(emp.dropna().index,columns=['SimFinID']).to_csv('ID.csv',index=False)
print(len(ids))