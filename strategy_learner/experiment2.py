# -*- coding: utf-8 -*-
"""
Created on Sat Dec  1 20:25:56 2018

@author: rdangelo

Student Name: Ettore d'Angelo
GT User ID: edangelo3
GT ID: 903248685
"""
from ManualStrategy import ManualStrategy
from StrategyLearner import StrategyLearner
from marketsimcode import compute_portvals
import matplotlib.pyplot as plt
import datetime as dt
import numpy as np

def author():
    return 'edangelo3'

if __name__=="__main__":
    symbol = 'JPM'
    sd = dt.datetime(2008,1,1)
    ed = dt.datetime(2009,12,31)
    sv = 100000
    impact = 0.001
    
    for i in range(6):
        impact = 0.001 * i
        s = StrategyLearner(verbose = False, impact = impact)
        s.addEvidence(symbol, sd, ed, sv)
        s.testPolicy(symbol, sd, ed, sv)
        df_trades = s.trades
        
        strat_1 = compute_portvals(df_trades, sd, ed, start_val = sv, commission = 0, impact = impact)
        
        df_trades[df_trades == 0] = np.nan
        df_trades.dropna(inplace = True)
        print 'Number of trades = ' + str(df_trades.shape[0])

        daily_return_strat_1 = (strat_1[1:]/ strat_1[:-1].values) - 1
        
    
        # Get portfolio statistics
        print 'Impact = ' + str(impact)
        cr = (strat_1.iloc[-1] - strat_1.iloc[0])/ strat_1.iloc[0]
        print 'Cumulative return strategy:', cr.iloc[0]
        adr = daily_return_strat_1.mean()
        print 'Mean daily return strategy:', adr.iloc[0]
        sddr = daily_return_strat_1.std()
        print 'Stdev of daily return strategy:', sddr.iloc[0]
        print ''
        
        strat_1 /= strat_1.iloc[0]
        
        plt.plot(strat_1, label = 'Impact = '+ str(impact))
        
    plt.title('Experiment 2')
    plt.legend()
    plt.savefig('Experiment2.png')
    plt.close()
        