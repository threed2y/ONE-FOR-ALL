import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.formula.api import ols
from scipy import stats

df = pd.read_excel("E:\Msc sem 4\Econ lab\Practical-2 (Hetroscedasticity)\Practical-2.xlsx", sheet_name="Sheet2")
df = df.iloc[:,0:3]

plt.figure()
plt.title('sales VS profit')
plt.scatter(df.Sales,df.Profits)
plt.ylabel('PROFITS')
plt.show

plt.figure()
plt.title('R&D VS profit')
plt.scatter(df['R&D'],df.Profits)
plt.ylabel('PROFITS')
plt.show

df_model = ols('Profits ~ Sales' , data = df).fit()
df_model.summary()

'''
import statsmodels.api as sm
df_model1 = sm.OLS(df.Profits,df.Sales)
model1 = df_model1.fit()
model1
model1.summary()
'''

def test_model(col):
    s=[]
    for i in col:
        a = [1,i]
        s.append(a)
    return(np.array(s))
prof_model = test_model(df['Profits'])


# H0 : Homoscedasticity is present
# H1 : Hetroscedasticity is present


from statsmodels.stats.diagnostic import het_breuschpagan
bp_test = het_breuschpagan(df_model.resid, prof_model)
print('LM - test p-value',round(bp_test[1],7))


# If there were Hetro then some transformation to remove

#1) Log trasformation

df['log_profits'] = np.log(df['Profits'])
f = 'log_profits ~ Sales'
df_model2 = ols(f,data = df).fit()

log_model2 = test_model(df['log_profits'])
bp_test2 = het_breuschpagan(df_model.resid, log_model2)
print('With Log trans p-value',round(bp_test2[1],7))

#2) box-cox trasformation
x,_ = stats.boxcox(df['Profits'])
df['trans_Profits'] = x
f = 'trans_Profits~Sales'
df_model3 = ols(f, data = df).fit()

trans_Profits_model = test_model(df['trans_Profits'])
bp_test3 = het_breuschpagan(df_model3.resid, trans_Profits_model)
print('With Box-cox p-value',round(bp_test3[1],7))





