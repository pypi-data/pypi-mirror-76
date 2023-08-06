import numpy as np
from scipy.stats import norm
from scipy import optimize
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.ticker as mtick

def sim_path(S, N, sigma, rf=0, dt=1/360, M=1):
    X = rf * dt + sigma * np.sqrt(dt) * np.random.normal(0,1,(N+1,M))
    X[0] = 0  
    return np.cumprod(1+X, axis=0) * S 
    
def calc_delta(pths, K, sigma, rf=0, dt=1/360):
    t = np.arange(len(pths)-1,-1,-1).reshape(-1,1) * dt
    t[-1] = .0000001
    d1 = (np.log(pths/K) + (rf+sigma**2/2)*t)/sigma/np.sqrt(t)
    delta = norm.cdf(d1)
    delta[-1] = 0
    return delta

def calc_cumcost(pths, delta, fee = 1/1000):
    vol_trd = np.vstack((delta[0],np.diff(delta,axis=0)))
    pnl_trd = - pths * vol_trd
    pnl_fee = abs(pnl_trd) * fee
    pnl = pnl_trd - pnl_fee
    return np.cumsum(pnl, axis=0)

def bs(S,K,sigma,T,rf = 0, iscall=True):
    d1 = (np.log(S/K) + (rf+sigma**2/2)*T)/sigma/np.sqrt(T)
    d2 = d1 - sigma * np.sqrt(T)
    if iscall:
        return S * norm.cdf(d1) - K * np.exp(-rf*T) * norm.cdf(d2)
    else:
        return - S * norm.cdf(-d1) + K * np.exp(-rf*T) * norm.cdf(-d2)

def iv(v, S ,K ,T ,rf = 0, iscall=True):
    f = lambda sigma: bs(S, K, sigma, T, rf, iscall) - v
    result = optimize.newton(f, .5)  
    return result

def Leland(sigma, fee, dt = 1/220):
    factor = np.sqrt(8/(np.pi * dt)) * fee / sigma
    sigma_buy = sigma * (1-factor) ** (1/2)
    sigma_sell = sigma * (1+factor) ** (1/2)
    return sigma_buy, sigma_sell

def Leland2(sigma, fee, dt = 1/200):
    factor = 2 * fee * sigma * np.sqrt(2/(np.pi * dt))
    sigma_buy = np.sqrt(sigma**2 - factor)
    sigma_sell = np.sqrt(sigma**2 + factor)
    return sigma_buy, sigma_sell

def show_pnl(price, cumcost):
    def show(a, name = ''):
        stats = {'mean':a.mean(),
                 'median':np.median(a),
                 'prob_win':(a>0).sum()/len(a),
                 'ESF':a[a<0].mean()}
        _, ax = plt.subplots()
        ax.hist(a, density=True, bins=50)
        ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.1f%%'))
        ax.set_title(name + ' distribution')
        ax.grid()
        print('\n' + name + ' stats:')
        print(stats)
    
    cumpnl = price + cumcost
    
    pnl = cumpnl[-1]
    show(pnl,'pnl')

    avg_capital_req = cumpnl.mean(axis = 0)
    show(avg_capital_req, 'avg_capital_req')

    ret = - pnl/avg_capital_req
    show(ret, 'ret')



def sim_short_call(S, K, N, sigma_deal, sigma_expected, fee, rf = 0, M = 10000, dt = 1/220):
    pth = sim_path(S, N, sigma_expected, M = M)
    delta = calc_delta(pth, K, sigma_deal, dt = dt)
    cumcost = calc_cumcost(pth, delta, fee = fee)
    cumcost[-1] -=  np.maximum(pth[-1] - K, 0)
    
    price_deal = bs(S, K, sigma_deal, N*dt, iscall=True)
    price_theo = bs(S, K, sigma_expected, N*dt, iscall=True)
    prem = price_deal / price_theo - 1
    
    print('S = {}\nK = {}\nN = {}\nsigma_deal = {:.2%}\nsigma_expected = {:.2%}\nfee = {:.2%}'.\
          format(S, K, N, sigma_deal, sigma_expected, fee))
    
    print('\nprice_deal = {:.2f}\nprice_theo = {:.2f}\nprem = {:.2%}'.format(price_deal, price_theo, prem))
    show_pnl(price_deal, cumcost)

#%%
if __name__ == '__main__':
    S = 100
    K = 110
    sigma = .2
    N = 30
    dt = 1/365
    fee = 1/1000
#    fee = 0/1000

    pth = sim_path(S,N,sigma,M=500000,dt=dt)
    delta = calc_delta(pth,K,sigma,dt=dt)
    cumcost = calc_cumcost(pth,delta,fee=0/10000)
    payoff = np.maximum(pth[-1] - K, 0)


    cumcost[-1] -= payoff
    rep_cost = cumcost[-1].copy()
    print('rep_cost =', rep_cost.mean())
    print('payoff = ', payoff.mean())
    
    import mibian as mb
    
    op = mb.BS([S, K, 0, N], volatility = sigma * 100)
    price_theo = op.callPrice
    print('price_theo =', price_theo)
    
    import seaborn as sns
    sns.distplot(-rep_cost)
    sns.distplot(payoff)
    
    pd.Series(-rep_cost).describe()
    
#    cumcost[-1] -= np.maximum(pth[-1] - K, 0)
#    cost = cumcost[-1]
#    capital_req = cumcost.min(axis = 0)
#    c = bs(S,K,sigma,N * dt)
#    print(c)
#    print(cost.mean())
#    sim_short_call(S,S,N, .26, .2, fee)
    