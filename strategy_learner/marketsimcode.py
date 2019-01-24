"""
Student
Name: Ettore d'Angelo
GT User ID: edangelo3
GT ID: 903248685
"""

import pandas as pd
import numpy as np
import datetime as dt
from util import get_data, plot_data
  		   	  			    		  		  		    	 		 		   		 		  
def compute_portvals(df_trades, start_date, end_date, start_val = 1000000, commission=9.95, impact=0.005):
    
    companies = list(df_trades.columns)[:-1]
    
    df_prices = get_data(companies, pd.date_range(start_date, end_date))
    df_prices = df_prices.fillna(method = 'ffill')
    df_prices = df_prices.fillna(method = 'bfill')

    df_prices['Cash'] = df_prices['SPY']
    del df_prices['SPY']
    df_prices['Cash'] = 1.0
    
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

def compute_portvals_orders(df_orders, start_date, end_date, start_val = 1000000, commission=9.95, impact=0.005):
    
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
