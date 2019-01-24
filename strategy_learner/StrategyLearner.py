"""
Template for implementing StrategyLearner  (c) 2016 Tucker Balch

Copyright 2018, Georgia Institute of Technology (Georgia Tech)
Atlanta, Georgia 30332
All Rights Reserved

Template code for CS 4646/7646

Georgia Tech asserts copyright ownership of this template and all derivative
works, including solutions to the projects assigned in this course. Students
and other users of this template code are advised not to share it with others
or to make it available on publicly viewable websites including repositories
such as github and gitlab.  This copyright statement should not be removed
or edited.

We do grant permission to share solutions privately with non-students such
as potential employers. However, sharing with other current or future
students of CS 7646 is prohibited and subject to being investigated as a
GT honor code violation.

-----do not edit anything above this line---

Student Name: Ettore d'Angelo
GT User ID: edangelo3
GT ID: 903248685
"""

import numpy as np
import datetime as dt
import pandas as pd
import util as ut
import random
import QLearner as ql
from indicators import smacalc, bollinger, smaoverprice, momentum_calc
from marketsimcode import compute_portvals

class StrategyLearner(object):

    # constructor
    def __init__(self, verbose = False, impact=0.0):
        self.verbose = verbose
        self.impact = impact
        self.mom = False
        self.sma = False
        self.bbp = False
        self.trades = None

    # this method should create a QLearner, and train it for trading
    def addEvidence(self, symbol = "ML4T-220", \
        sd=dt.datetime(2008,1,1), \
        ed=dt.datetime(2009,12,31), \
        sv = 100000):
        
        
        # example usage of the old backward compatible util function
        syms=[symbol]
        dates = pd.date_range(sd, ed)
        prices_all = ut.get_data(syms, dates)  # automatically adds SPY
        prices = prices_all[syms]  # only portfolio symbols
        prices_SPY = prices_all['SPY']  # only SPY, for comparison later
        
        it = 0
        max_iter = 50
        min_iter = 25
        convergence = False
        lookback = 14
        period = 5
        cr_prev = None
        
        
        # calculate the indicators
        sma = smacalc(prices, lookback)
        bbp = bollinger(prices, lookback, sma)
        sma = smaoverprice(sma, prices)
        mom = momentum_calc(prices, period)
        
        # create the discrtizer lists
        self.bbp = create_discretize(bbp.iloc[lookback:], syms = syms)
        self.sma = create_discretize(sma.iloc[lookback:], syms = syms)
        self.mom = create_discretize(mom.iloc[lookback:], syms = syms)
                
        self.q = ql.QLearner(num_states=10**4, num_actions = 3, alpha = 0.2,
                             gamma = 0.9, rar = 0.5, radr = 0.99, dyna = 0, verbose = False)
        
        # position can be {0: 'short', 1: 'nothing', 2:'long'}
        
        while it < max_iter and not convergence or it < min_iter:
            df_trades = pd.DataFrame(data=np.zeros((prices.shape[0], 2)), columns = [symbol, 'Cash'], index = prices.index)

            position = 1
            action = 1
            state = int(str(position) + str(discretize(self.mom, float(mom.iloc[lookback]))) + 
                        str(discretize(self.sma, float(sma.iloc[lookback]))) + 
                        str(discretize(self.bbp, float(bbp.iloc[lookback]))))
            
            self.q.querysetstate(state)
            
            for day in range(lookback+1, prices.shape[0]):
                if action == 0 and action != position:
                    r = -(prices.iloc[day]/prices.iloc[day-1] - 1) - penalty
                elif action == 0:
                    r = -(prices.iloc[day]/prices.iloc[day-1] - 1)
                elif action == 1:
                    r = 0
                elif action == 2 and action != position:
                    r = (prices.iloc[day]/prices.iloc[day-1] - 1) - penalty
                else:
                    r = (prices.iloc[day]/prices.iloc[day-1] - 1)
                
                position = action
                action = self.q.query(state, r)
                
                if position != action:
                    if 1000 * (action - position) > 0:
                        df_trades[symbol][prices.index[day]] += abs(1000 * (action - position))
                        df_trades['Cash'][prices.index[day]] -= abs(1000 * (action - position)) * prices[symbol][day] + abs(1000 * (action - position)) * prices[symbol][day] * self.impact
                    else:
                        df_trades[symbol][prices.index[day]] -= abs(1000 * (action - position))
                        df_trades['Cash'][prices.index[day]] += abs(1000 * (action - position)) * prices[symbol][day] + abs(1000 * (action - position)) * prices[symbol][day] * self.impact
                    penalty = self.impact * prices.iloc[day]
                
                else:
                    penalty = 0
                    
                    
                state = int(str(action) + str(discretize(self.mom, float(mom.iloc[day]))) + 
                        str(discretize(self.sma, float(sma.iloc[day]))) + 
                        str(discretize(self.bbp, float(bbp.iloc[day]))))
            
            opt = compute_portvals(df_trades, sd, ed, start_val = sv, commission = 0.0, impact = self.impact)
            cr = float((opt.iloc[-1] - opt.iloc[0])/ opt.iloc[0])
            if self.verbose: print str(it) + ': cr = ' + str(cr)
            
            if cr == cr_prev:
                convergence = True
            else:
                cr_prev = cr
                
            it += 1
            
        return df_trades

    # this method should use the existing policy and test it against new data
    def testPolicy(self, symbol = "ML4T-220", \
        sd=dt.datetime(2010,1,1), \
        ed=dt.datetime(2011,12,31), \
        sv = 10000):
        
        # example usage of the old backward compatible util function
        syms=[symbol]
        dates = pd.date_range(sd, ed)
        prices_all = ut.get_data(syms, dates)  # automatically adds SPY
        prices = prices_all[syms]  # only portfolio symbols
        prices_SPY = prices_all['SPY'] 
        
        lookback = 14
        period = 5
        
        # calculate the indicators
        sma = smacalc(prices, lookback)
        bbp = bollinger(prices, lookback, sma)
        sma = smaoverprice(sma, prices)
        mom = momentum_calc(prices, period)
        
        
        position = 1
        state = int(str(position) + str(discretize(self.mom, float(mom.iloc[lookback]))) + 
                    str(discretize(self.sma, float(sma.iloc[lookback]))) + 
                    str(discretize(self.bbp, float(bbp.iloc[lookback]))))
        
        df_trades = pd.DataFrame(data=np.zeros((prices.shape[0], 2)), columns = [symbol, 'Cash'], index = prices.index)
        
        for day in range(lookback+1, prices.shape[0]):
            action = self.q.querysetstate(state)
            
            if position != action:
                if 1000 * (action - position) > 0:
                    df_trades[symbol][prices.index[day]] += abs(1000 * (action - position))
                    df_trades['Cash'][prices.index[day]] -= abs(1000 * (action - position)) * prices[symbol][day] + abs(1000 * (action - position)) * prices[symbol][day] * self.impact
                else:
                    df_trades[symbol][prices.index[day]] -= abs(1000 * (action - position))
                    df_trades['Cash'][prices.index[day]] += abs(1000 * (action - position)) * prices[symbol][day] + abs(1000 * (action - position)) * prices[symbol][day] * self.impact
                position = action
            
            state = int(str(action) + str(discretize(self.mom, float(mom.iloc[day]))) + 
                    str(discretize(self.sma, float(sma.iloc[day]))) + 
                    str(discretize(self.bbp, float(bbp.iloc[day]))))
        
        if self.verbose: print type(df_trades) # it better be a DataFrame!
        if self.verbose: print df_trades
        
        self.trades = df_trades
#        if self.verbose: print prices_all
        return df_trades[symbol].to_frame()
    
    def author(self):
        return 'edangelo3'
    
def create_discretize(ind, syms, steps = 10):
    threshold = []
    ind = ind.sort_values(by = syms, ascending = True).values
    stepsize = int(ind.shape[0]/steps)
    for i in range(steps):
        threshold.append(float(ind[(i+1) * stepsize]))
    
    return threshold

def discretize(discr, val):
    for i in range(len(discr)):
        if val < discr[i]:
            return i
    
    return 9
    
        
if __name__=="__main__":
    s = StrategyLearner(verbose = False, impact = 0.005)
    s.addEvidence()
    s.testPolicy()
    #print "One does not simply think up a strategy"
