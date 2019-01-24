"""Optimize a portfolio.                                                                                                               
                                                                                                     
"""                                                                                                               
                                                                                                               
                                                                                                               
import pandas as pd                                                                                                               
import matplotlib.pyplot as plt                                                                                                               
import numpy as np                                                                                                               
import datetime as dt                                                                                                               
from util import get_data, plot_data     
import scipy.optimize as spo                                                                                             
                                                                                                               
# This is the function that will be tested by the autograder                                                                                                               
# The student must update this code to properly implement the functionality                                                                                                               
def optimize_portfolio(sd=dt.datetime(2008,1,1), ed=dt.datetime(2009,1,1), \
    syms=['GOOG','AAPL','GLD','XOM'], gen_plot=False):                                                                                                               
                                                                                                               
    # Read in adjusted closing prices for given symbols, date range                                                                                                               
    dates = pd.date_range(sd, ed)                                                                                                               
    prices_all = get_data(syms, dates)  # automatically adds SPY                                                                                                               
    prices = prices_all[syms]  # only portfolio symbols 
    prices = prices.fillna(method = 'ffill')
    prices = prices.fillna(method = 'bfill')
    normed = prices / prices.iloc[0]                                                                                                       
    prices_SPY = prices_all['SPY']  # only SPY, for comparison later 
    allocs = np.asarray([1.0/len(syms) for i in range(len(syms))])
    bounds = [(0.0, 1.0) for i in range(len(syms))]
    cons = {'type':'eq', 'fun': lambda allocs : 1.0 - np.sum(allocs)}                                                                                        
    # find the allocations for the optimal portfolio                                                                                                              
    allocs = spo.minimize(compute_portfolio_stats, allocs, args = (normed, 0.0, 252.0), 
                          bounds = bounds, constraints = cons, method = 'SLSQP').x                                                                                  
    cr, adr, sddr, sr = support(prices, allocs) # add code here to compute stats                                                                                                               
                                                                                                               
    # Get daily portfolio value                                                                                                             
    port_val = prices*allocs
    port_val= port_val.sum(axis = 1)                                                                                                  
                                                                                                               
    # Compare daily portfolio value with SPY using a normalized plot                                                                                                               
    if gen_plot:                                                                                                               
        # add code to plot here                                                                                                               
        p = port_val /port_val[0]
        spy = prices_SPY / prices_SPY[0]
        df_temp = pd.concat([p, spy], keys=['Portfolio', 'SPY'], axis=1)
        ax = df_temp.plot(title='Optimal portfolio', fontsize=12)
        ax.set_xlabel('Date')  		   	  			    		  		  		    	 		 		   		 		  
        ax.set_ylabel('Value')
        plt.savefig('plot.png')
        plt.close()                                                                                               
                                                                                                               
    return allocs, cr, adr, sddr, sr

def support(allocs, normed, rfr = 0.0, sf = 252.0):
    alloced = normed * allocs
    port_val = alloced.sum(axis = 1)
    # Get daily portfolio return
    daily_return = (port_val[1:]/ port_val[:-1].values) - 1

    # Get portfolio statistics
    cr = (port_val[-1] - port_val[0])/ port_val[0]
    adr = daily_return.mean()
    sddr = daily_return.std()
    sr = sf**0.5 * (daily_return - rfr).mean() / sddr
    return cr, adr, sddr, sr    

def compute_portfolio_stats(allocs, normed, rfr = 0.0, sf = 252):
    alloced = normed * allocs
    port_val = alloced.sum(axis = 1)
    # Get daily portfolio return
    daily_return = (port_val[1:]/ port_val[:-1].values) - 1

    # Get portfolio statistics (note: std_daily_ret = volatility)
    sddr = daily_return.std()
    sr = sf**0.5 * (daily_return - rfr).mean() / sddr
    
    return  - sr                                                                                                         

def create_png():
    start_date = dt.datetime(2008,6,1)                                                                                                               
    end_date = dt.datetime(2009,6,1)                                                                                                               
    symbols = ['IBM', 'X', 'GLD', 'JPM']                                                                                                             
                                                                                                               
    # Assess the portfolio                                                                                                               
    allocations, cr, adr, sddr, sr = optimize_portfolio(sd = start_date, ed = end_date,\
        syms = symbols, \
        gen_plot = True)                                                                                                               
                                                                                                               
    # Print statistics                                                                                                               
    print "Start Date:", start_date                                                                                                               
    print "End Date:", end_date                                                                                                               
    print "Symbols:", symbols                                                                                                               
    print "Allocations:", allocations                                                                                                               
    print "Sharpe Ratio:", sr                                                                                                               
    print "Volatility (stdev of daily returns):", sddr                                                                                                               
    print "Average Daily Return:", adr                                                                                                               
    print "Cumulative Return:", cr 
                                                                                                               
def test_code():                                                                                                               
    # This function WILL NOT be called by the auto grader                                                                                                               
    # Do not assume that any variables defined here are available to your function/code                                                                                                               
    # It is only here to help you set up and test your code                                                                                                               
                                                                                                               
    # Define input parameters                                                                                                               
    # Note that ALL of these values will be set to different values by                                                                                                               
    # the autograder!                                                                                                               
                                                                                                               
    start_date = dt.datetime(2008,6,1)                                                                                                               
    end_date = dt.datetime(2009,6,1)                                                                                                               
    symbols = ['IBM', 'X', 'GLD', 'JPM']                                                                                                             
                                                                                                               
    # Assess the portfolio                                                                                                               
    allocations, cr, adr, sddr, sr = optimize_portfolio(sd = start_date, ed = end_date,\
        syms = symbols, \
        gen_plot = True)                                                                                                               
                                                                                                               
    # Print statistics                                                                                                               
    print "Start Date:", start_date                                                                                                               
    print "End Date:", end_date                                                                                                               
    print "Symbols:", symbols                                                                                                               
    print "Allocations:", allocations                                                                                                               
    print "Sharpe Ratio:", sr                                                                                                               
    print "Volatility (stdev of daily returns):", sddr                                                                                                               
    print "Average Daily Return:", adr                                                                                                               
    print "Cumulative Return:", cr                                                                                                               
                                                                                                               
if __name__ == "__main__":                                                                                                               
    # This code WILL NOT be called by the auto grader                                                                                                               
    # Do not assume that it will be called                                                                                                               
    test_code()                                                                                                               
