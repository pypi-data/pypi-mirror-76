import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.tsa.api as smt
import statsmodels.api as sm
import scipy.stats as scs
from statsmodels.tsa.stattools import adfuller

#%%

#def gen_ar1(phi,n_sample=1000):
#    r = np.zeros(n_sample)
#    a = np.random.normal(0,1,n_sample)
#    r[0] = a[0]
#    for i in range(1,len(r)):
#        r[i] = phi * r[i-1] + a[i]
#    return r
#
#
#def gen_arch1(a0, a1, n_sample=1000):
#    y = np.zeros(n_sample)
#    z = np.random.normal(0,1,n_sample)
#    sigma = np.zeros(n_sample)
#    
#    sigma[0] = np.sqrt(a0)
#    y[0] = sigma[0] * z[0]
#    for i in range(1,len(y)):
#        sigma[i] = np.sqrt(a0 + a1 * y[i-1]**2)
#        y[i] = sigma[i] * z[i]
#    return y
#
#def gen_grach11(a0, a1, b1, n_sample=1000):
#    y = np.zeros(n_sample)
#    z = np.random.normal(0,1,n_sample)
#    sigma = np.zeros(n_sample)
#    
#    sigma[0] = np.sqrt(a0)
#    y[0] = sigma[0] * z[0]
#    for i in range(1,len(y)):
#        sigma[i] = np.sqrt(a0 + a1 * y[i-1]**2 + b1 * sigma[i-1]**2)
#        y[i] = sigma[i] * z[i]
#    return y

def tsplot(y, lags=None, figsize=(10, 8), style='bmh'):
    if not isinstance(y, pd.Series):
        y = pd.Series(y)
    with plt.style.context(style):    
        fig = plt.figure(figsize=figsize)
        #mpl.rcParams['font.family'] = 'Ubuntu Mono'
        layout = (3, 2)
        ts_ax = plt.subplot2grid(layout, (0, 0), colspan=2)
        acf_ax = plt.subplot2grid(layout, (1, 0))
        pacf_ax = plt.subplot2grid(layout, (1, 1))
        qq_ax = plt.subplot2grid(layout, (2, 0))
        pp_ax = plt.subplot2grid(layout, (2, 1))
        
        y.plot(ax=ts_ax)
        ts_ax.set_title('Time Series Analysis Plots')
        smt.graphics.plot_acf(y, lags=lags, ax=acf_ax, alpha=0.5)
        smt.graphics.plot_pacf(y, lags=lags, ax=pacf_ax, alpha=0.5)
        sm.qqplot(y, line='s', ax=qq_ax)
        qq_ax.set_title('QQ Plot')        
        scs.probplot(y, sparams=(y.mean(), y.std()), plot=pp_ax)

        plt.tight_layout()
    return 

def test_stationarity(timeseries):
    
    #Determing rolling statistics
    rolmean = pd.Series(timeseries).rolling(window=12).mean()
    rolstd = pd.Series(timeseries).rolling(window=12).std()

    #Plot rolling statistics:
    orig = plt.plot(timeseries, color='blue',label='Original')
    mean = plt.plot(rolmean, color='red', label='Rolling Mean')
    std = plt.plot(rolstd, color='black', label = 'Rolling Std')
    plt.legend(loc='best')
    plt.title('Rolling Mean & Standard Deviation')
    plt.show(block=False)
    
    #Perform Dickey-Fuller test:
    print( 'Results of Dickey-Fuller Test:')
    dftest = adfuller(timeseries, autolag='AIC')
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic','p-value','#Lags Used','Number of Observations Used'])
    for key,value in dftest[4].items():
        dfoutput['Critical Value (%s)'%key] = value
    print(dfoutput)

def plot_forecast(y, f, ci=np.array([])):
    plt.plot(range(1,len(y)+1), y)
    plt.plot(range(len(y)+1,len(y)+1+len(f)), f, 'r')
    if len(ci)>0:
        plt.fill_between(range(len(y)+1,len(y)+1+len(f)), ci[:,0], ci[:,1], alpha=0.2)