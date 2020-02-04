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

def testing(op,h):
    rmse = math.sqrt(mean_squared_error(op,h))
    final['Avg RMSE'].append(rmse)
    tot = np.sum(np.absolute(h))
    weight = h/tot
    profit = np.multiply(op,weight)
    tot_prof = np.sum(profit)*100
    final['Avg profit'].append(tot_prof)



date_format = "%Y-%m-%d"
curr  = datetime.strptime('2015-07-01', date_format)
last = datetime.strptime('2019-07-01', date_format)

split=8
delta = (last - curr)/split


h = pd.read_csv('/Users/shreyaspatel/Desktop/Machine_Learning/Personal/Fama_French/Testing/Hypothesis.csv')
op = pd.read_csv('/Users/shreyaspatel/Desktop/Machine_Learning/Personal/Fama_French/Testing/Test.csv')

final = {'Avg RMSE':[],'Avg profit':[]}
for i in range( 2, split ):
    testing(op[str(i)].dropna(),h[str(i)].dropna())


scores = pd.DataFrame(columns=[ (curr + j*delta).strftime("%d %b, %Y") for j in list(range( 2, split )) ],index=['rmse','profit'] )
# scores.append
scores.loc['rmse'] = final['Avg RMSE']
scores.loc['profit'] = [ "{:.2f}%".format(i) for i in final['Avg profit'] ]
scores['Average'] = [ mean(final['Avg RMSE']),"{:.2f}%".format(mean(final['Avg profit']) ) ]
scores.to_csv('Scores.csv')
 