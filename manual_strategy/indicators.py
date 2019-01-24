"""
Student
Name: Ettore d'Angelo
GT User ID: edangelo3
GT ID: 903248685
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dt
from util import get_data, plot_data
from marketsimcode import compute_portvals

def build_orders(symbols, start_date, end_date, lookback, period = 5):
    price = get_data(symbols, pd.date_range(start_date, end_date))
    
    sma = smacalc(price, lookback)
    bbp = bollinger(price, lookback, sma)
    sma = smaoverprice(sma, price)
    rsi = Rsi(lookback, price)
    mom = momentum_calc(price, period)
    macd = MACD(price)
    
    orders = price.copy()
    orders.ix[:,:] = np.nan
    
    spy_mom = mom.copy()
    spy_mom.values[:,:] = spy_mom.ix[:,['SPY']]
    
    sma_cross = pd.DataFrame(0, index = sma.index, columns = sma.columns)
    sma_cross[sma >= 1] = 1
    
    sma_cross[1:] = sma_cross.diff()
    sma_cross.ix[0] = 0
    
    orders[(sma < 0.95) & (bbp < 0) & (mom < -1) & (spy_mom > .5)] = 1000
#    orders[(sma > 1.05) & (bbp > 1) & (mom > 0) & (spy_mom < -.5)] = - 1000

#    orders[(sma < 0.95) & (bbp < 0)] = 1000
    orders[(sma > 1.05) & (bbp > 1)] = - 1000    
    
    orders[sma_cross != 0] = 0
    orders.ffill(inplace = True)
    orders.fillna(0, inplace = True)
    
    orders[1:] = orders.diff()
    orders.ix[0] = 0

    del orders['SPY']
    
    symbols = list(orders.columns)
    orders = orders.loc[(orders != 0).any(axis = 1)]
    
    order_list = []
    
    for day in orders.index:
        for sym in symbols:
            if orders.ix[day, sym] > 0:
                order_list.append([day.date(), sym, 'BUY', 1000])
            elif orders.ix[day, sym] < 0:
                order_list.append([day.date(), sym, 'SELL', 1000])
    
    df_orders = pd.DataFrame(data = order_list, columns = ['Date', 'Symbol', 'Order', 'Shares'])
    
    return df_orders

def smacalc(price, lookback):    
    sma = price.rolling(window = lookback, min_periods = lookback).mean()
    
    return sma

def bollinger(price, lookback, sma):
    rolling_std = price.rolling(window = lookback, min_periods = lookback).std()
    top_band = sma + (2 * rolling_std)
    bottom_band = sma - (2 * rolling_std)
    
    bbp = (price - bottom_band) / (top_band - bottom_band)
            
    return bbp

def plot_bollinger(price, lookback):
    price = price/price.iloc[0]
    sma = smacalc(price, lookback)
    rolling_std = price.rolling(window = lookback, min_periods = lookback).std()
    top_band = sma + (2 * rolling_std)
    bottom_band = sma - (2 * rolling_std)
    
    bbp = (price - bottom_band) / (top_band - bottom_band)
    
    f, (ax1,ax2) = plt.subplots(2,1,sharex= True,gridspec_kw={'height_ratios':[4,1]})
    ax1.plot(price['JPM'], c = 'black', label = 'Price')
    ax1.plot(top_band['JPM'], c = 'blue', label = 'Top band')
    ax1.plot(bottom_band['JPM'], c = 'red', label = 'Bottom band')
    ax1.set_title('Bollinger bands')
    ax2.plot(bbp['JPM'], label = 'Bollinger band percentage')
    ax2.set_title('Bollinger bands percentage')
    ax1.legend()
    plt.savefig('Bollinger.png')
    plt.close()

    
def smaoverprice(sma, price):
    sma = price / sma
    return sma

def plot_priceoversma(price, lookback):
    price = price / price.iloc[0]
    sma = smacalc(price, lookback)
    sma_price = smaoverprice(sma, price)
    one = pd.DataFrame(data = np.ones(sma.shape[0]), index = sma.index)
    
    plt.plot(sma_price['JPM'], c ='red', label = 'Price / SMA')
    plt.plot(price['JPM'], c = 'black', label = 'Price')
    plt.plot(sma['JPM'], c = 'blue', label = 'SMA')
    plt.plot(one, c = 'green')
    plt.title('Price / SMA')
    plt.legend()
    plt.savefig('SMA.png')
    plt.close()
    
def Rsi(lookback, price):
    rsi = price.copy()
    rsi.ix[:,:] = 0
            
    daily_rets = price.copy()
    daily_rets.values[1:, :] = price.values[1:, :] - price.values[:-1, :]
    daily_rets.values[0, :] = np.nan
            
    up_rets = daily_rets[daily_rets >= 0].fillna(0).cumsum()
    down_rets = -1 * daily_rets[daily_rets < 0].fillna(0).cumsum()
    
    up_gain = price.copy()
    up_gain.ix[:,:] = 0
    up_gain.values[lookback:,:] = up_rets.values[lookback:,:] - up_rets.values[:-lookback,:]
    
    down_loss = price.copy()
    down_loss.ix[:,:] = 0
    down_loss.values[lookback:,:] = down_rets.values[lookback:,:] - down_rets.values[:-lookback,:]
        
    rs = (up_gain / lookback) / (down_loss / lookback)
    rsi =  100 - (100/(1 + rs))
    rsi.ix[:lookback,:] = np.nan
        
    rsi[rsi == np.inf] = 100
    
    return rsi

def plot_rsi(lookback, price):
    price = price / price.iloc[0]
    rsi = Rsi(lookback, price)
    
    plt.plot(rsi['JPM'], label = 'RSI')
    plt.title('RSI')
    plt.legend()
    plt.savefig('RSI.png')
    plt.close()

def momentum_calc(price, period):
    momentum = price.copy()
    momentum.values[period:, :] = price.iloc[period:].values - price.iloc[:price.shape[0]-period].values
    momentum.ix[:period,:] = np.nan
    return momentum

def plot_momentum(price, period = 5):
    mom = momentum_calc(price, period)
    
    plt.plot(mom['JPM'], label = 'Momentum')
    plt.title('Momentum')
    plt.legend()
    plt.savefig('momentum.png')
    plt.close()

def MACD(price):
    ema_26 = price.ewm(span = 26).mean()
    ema_12 = price.ewm(span = 12).mean()
    macd = ema_12 - ema_26
    
    return macd

def plot_macd(price):
    macd = MACD(price)
    zero = pd.DataFrame(data = np.zeros(macd.shape[0]), index = macd.index)
    
    plt.plot(macd['JPM'], label = 'MACD')
    plt.plot(zero)
    plt.title('macd')
    plt.legend()
    plt.savefig('macd.png')
    plt.close()
    

if __name__ == "__main__":
    start_date = dt.datetime(2008,01,01)
    end_date = dt.datetime(2009,12,31)
    symbols = ['JPM']
    lookback = 14
    price = get_data(symbols, pd.date_range(start_date, end_date))
    plot_bollinger(price, lookback)
    plot_priceoversma(price, lookback)
    plot_rsi(lookback, price)
    plot_momentum(price)
    plot_macd(price)
