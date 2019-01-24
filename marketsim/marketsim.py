"""MC2-P1: Market simulator.  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
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
  		   	  			    		  		  		    	 		 		   		 		  
import pandas as pd  		   	  			    		  		  		    	 		 		   		 		  
import numpy as np  		   	  			    		  		  		    	 		 		   		 		  
import datetime as dt  		   	  			    		  		  		    	 		 		   		 		  
import os  		   	  			    		  		  		    	 		 		   		 		  
from util import get_data, plot_data  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
def compute_portvals(orders_file = "./orders/orders-12.csv", start_val = 1000000, commission=9.95, impact=0.005):  		   	  			    		  		  		    	 		 		   		 		  
    # this is the function the autograder will call to test your code  		   	  			    		  		  		    	 		 		   		 		  
    # NOTE: orders_file may be a string, or it may be a file object. Your  		   	  			    		  		  		    	 		 		   		 		  
    # code should work correctly with either input  		   	  			    		  		  		    	 		 		   		 		  
    # TODO: Your code here
    df_orders = pd.read_csv(orders_file)
    df_orders = df_orders.sort_values('Date') # sort by date
    
    # date wanted
    start_date = dt.datetime(int(df_orders['Date'][0].split('-')[0]),int(df_orders['Date'][0].split('-')[1]),int(df_orders['Date'][0].split('-')[2]))
    e = df_orders['Date'][df_orders.shape[0]-1]
    end_date = dt.datetime(int(e.split('-')[0]),int(e.split('-')[1]),int(e.split('-')[2]))
    
    companies = list(set(df_orders['Symbol'])) # companies we are interested in
    
    df_prices = get_data(companies, pd.date_range(start_date, end_date))
    df_prices = df_prices.fillna(method = 'ffill')
    df_prices = df_prices.fillna(method = 'bfill')

    df_prices['Cash'] = df_prices['SPY']
    del df_prices['SPY']
    df_prices['Cash'] = 1.0
    
    df_trades = pd.DataFrame(data=np.zeros(df_prices.shape), columns = df_prices.columns, index = df_prices.index)
    
    for i in range(df_orders.shape[0]):
        order = df_orders.loc[i]
        date = order['Date']
        symbol = order['Symbol']
        price = df_prices[symbol][date]
        
        if order['Order'] == 'BUY':
            df_trades[symbol][date] += order['Shares']
            df_trades['Cash'][date] -= order['Shares'] * price + commission + order['Shares'] * price * impact
        elif order['Order'] == 'SELL':
            df_trades[symbol][date] -= order['Shares']
            df_trades['Cash'][date] += order['Shares'] * price - commission - order['Shares'] * price * impact
    
    df_holdings = pd.DataFrame(data=np.zeros(df_prices.shape), columns = df_prices.columns, index = df_prices.index)
    df_holdings['Cash'][0] = start_val
    df_holdings += df_trades
    df_holdings = df_holdings.cumsum()
    
#    df_holdings.iloc[0] += df_trades.iloc[0]
#    for i in range(1,df_holdings.shape[0]):
#        df_holdings.iloc[i] = df_holdings.iloc[i-1] + df_trades.iloc[i]
    
    df_value = df_prices*df_holdings
    
    portvals = df_value.sum(axis = 1).to_frame()
    
    return portvals  		   	  			    		  		  		    	 		 		   		 		  

def author():
    return 'edangelo3'
  		   	  			    		  		  		    	 		 		   		 		  
def test_code():  		   	  			    		  		  		    	 		 		   		 		  
    # this is a helper function you can use to test your code  		   	  			    		  		  		    	 		 		   		 		  
    # note that during autograding this function will not be called.  		   	  			    		  		  		    	 		 		   		 		  
    # Define input parameters  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
    of = "./orders/orders-02.csv"  		   	  			    		  		  		    	 		 		   		 		  
    sv = 1000000  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
    # Process orders  		   	  			    		  		  		    	 		 		   		 		  
    portvals = compute_portvals(orders_file = of, start_val = sv)  		   	  			    		  		  		    	 		 		   		 		  
    if isinstance(portvals, pd.DataFrame):  		   	  			    		  		  		    	 		 		   		 		  
        portvals = portvals[portvals.columns[0]] # just get the first column  		   	  			    		  		  		    	 		 		   		 		  
    else:  		   	  			    		  		  		    	 		 		   		 		  
        "warning, code did not return a DataFrame"  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
    # Get portfolio stats  		   	  			    		  		  		    	 		 		   		 		  
    # Here we just fake the data. you should use your code from previous assignments.  		   	  			    		  		  		    	 		 		   		 		  
    start_date = dt.datetime(2008,1,1)  		   	  			    		  		  		    	 		 		   		 		  
    end_date = dt.datetime(2008,6,1)  		   	  			    		  		  		    	 		 		   		 		  
    cum_ret, avg_daily_ret, std_daily_ret, sharpe_ratio = [0.2,0.01,0.02,1.5]  		   	  			    		  		  		    	 		 		   		 		  
    cum_ret_SPY, avg_daily_ret_SPY, std_daily_ret_SPY, sharpe_ratio_SPY = [0.2,0.01,0.02,1.5]  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
    # Compare portfolio against $SPX  		   	  			    		  		  		    	 		 		   		 		  
    print "Date Range: {} to {}".format(start_date, end_date)  		   	  			    		  		  		    	 		 		   		 		  
    print  		   	  			    		  		  		    	 		 		   		 		  
    print "Sharpe Ratio of Fund: {}".format(sharpe_ratio)  		   	  			    		  		  		    	 		 		   		 		  
    print "Sharpe Ratio of SPY : {}".format(sharpe_ratio_SPY)  		   	  			    		  		  		    	 		 		   		 		  
    print  		   	  			    		  		  		    	 		 		   		 		  
    print "Cumulative Return of Fund: {}".format(cum_ret)  		   	  			    		  		  		    	 		 		   		 		  
    print "Cumulative Return of SPY : {}".format(cum_ret_SPY)  		   	  			    		  		  		    	 		 		   		 		  
    print  		   	  			    		  		  		    	 		 		   		 		  
    print "Standard Deviation of Fund: {}".format(std_daily_ret)  		   	  			    		  		  		    	 		 		   		 		  
    print "Standard Deviation of SPY : {}".format(std_daily_ret_SPY)  		   	  			    		  		  		    	 		 		   		 		  
    print  		   	  			    		  		  		    	 		 		   		 		  
    print "Average Daily Return of Fund: {}".format(avg_daily_ret)  		   	  			    		  		  		    	 		 		   		 		  
    print "Average Daily Return of SPY : {}".format(avg_daily_ret_SPY)  		   	  			    		  		  		    	 		 		   		 		  
    print  		   	  			    		  		  		    	 		 		   		 		  
    print "Final Portfolio Value: {}".format(portvals[-1])  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
if __name__ == "__main__":  		   	  			    		  		  		    	 		 		   		 		  
    pass
    #test_code()  		   	  			    		  		  		    	 		 		   		 		  
