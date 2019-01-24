# -*- coding: utf-8 -*-
"""
Created on Sat Dec  1 20:24:42 2018

@author: rdangelo

Student Name: Ettore d'Angelo
GT User ID: edangelo3
GT ID: 90324868
"""
from ManualStrategy import ManualStrategy
from StrategyLearner import StrategyLearner
from marketsimcode import compute_portvals, compute_portvals_orders
import matplotlib.pyplot as plt
import datetime as dt
import pandas as pd
import numpy as np


def author():
    return 'edangelo3'

if __name__=="__main__":
    
    symbol = 'JPM'
    sd = dt.datetime(2008,1,1)
    ed = dt.datetime(2009,12,31)
    sv = 100000
    impact = 0.0
    
    ms = ManualStrategy()
    df_orders = ms.testPolicy(symbol, sd, ed, sv)
    s = StrategyLearner(verbose = False)
    s.addEvidence(symbol, sd, ed, sv)
    s.testPolicy(symbol, sd, ed, sv)
    df_trades = s.trades
    
    man = compute_portvals_orders(df_orders, sd, ed, start_val = sv, commission = 0, impact = impact)
    strat = compute_portvals(df_trades, sd, ed, start_val = sv, commission = 0, impact = impact)
    
    # Get daily return
    daily_return_man = (man[1:]/ man[:-1].values) - 1
    daily_return_strat = (strat[1:]/ strat[:-1].values) - 1
    

    # Get portfolio statistics (note: std_daily_ret = volatility)
    cr = (strat.iloc[-1] - strat.iloc[0])/ strat.iloc[0]
    print 'Cumulative return strat:', cr.iloc[0]
    cr = (man.iloc[-1] - man.iloc[0])/ man.iloc[0]
    print 'Cumulative return man:', cr.iloc[0]
    adr = daily_return_strat.mean()
    print 'Mean daily return strat:', adr.iloc[0]
    adr = daily_return_man.mean()
    print 'Mean daily return man:', adr.iloc[0]
    sddr = daily_return_strat.std()
    print 'Stdev of daily return strat:', sddr.iloc[0]
    sddr = daily_return_man.std()
    print 'Stdev of daily return man:', sddr.iloc[0]
    
    strat /= strat.iloc[0]
    man /= man.iloc[0]
    
    plt.plot(strat, c = 'black', label = 'Strategy Learner')
    plt.plot(man, c = 'blue', label = 'Manual strategy')
    plt.legend()
    plt.savefig('Experiment1.png')
    plt.close()