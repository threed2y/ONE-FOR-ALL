# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 08:39:58 2022

@author: HP
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.formula.api import ols
import statsmodels.api as sm
from scipy import stats

df = pd.read_csv("E:\Msc sem 4\Econ lab\Practical-2 (Hetroscedasticity)\Data.csv")
df.rename(columns = {'Over all AIQ':'AIQ'}, inplace = True)

plt.figure()
plt.title('')
plt.scatter(df['AIQ'], df.PM10)
plt.ylabel('Over all AIQ')
plt.show()

df_model = ols('AIQ ~ PM10' , data = df).fit()
df_model.summary()


def test_model(col):
    s=[]
    for i in col:
        a = [1,i]
        s.append(a)
    return(np.array(s))
prof_model = test_model(df['AIQ'])


# H0 : Homoscedasticity is present
# H1 : Hetroscedasticity is present

# Breuschpagan Test
from statsmodels.stats.diagnostic import het_breuschpagan
bp_test = het_breuschpagan(df_model.resid, prof_model)
print('LM - test p-value',round(bp_test[1],7))

# White Test
from statsmodels.stats.diagnostic import het_white
white_test = het_white(df_model.resid,prof_model)
print('white test p value :',round(white_test[1],4))

# If there were Hetro then some transformation to remove

#1) Log trasformation

df['log_AIQ'] = np.log(df['AIQ'])
f = 'log_AIQ ~ PM10'
df_model2 = ols(f,data = df).fit()
df_model2.summary()

plt.figure()
plt.scatter(df.log_AIQ, df_model2.resid)


log_model2 = test_model(df['log_AIQ'])
bp_test2 = het_breuschpagan(df_model2.resid, log_model2)
print('BP test With Log transformation p-value',round(bp_test2[1],4))

#2) box-cox trasformation
x,_ = stats.boxcox(df['AIQ'])
df['trans_AIQ'] = x
f = 'trans_AIQ ~ PM10'
df_model3 = ols(f, data = df).fit()
df_model3.summary()

plt.figure()
plt.scatter(df.trans_AIQ, df_model3.resid)

trans_AIQ_model = test_model(df['AIQ'])
bp_test3 = het_breuschpagan(df_model3.resid, trans_AIQ_model)
print('BP test With Box-cox p-value',round(bp_test3[1],7))




