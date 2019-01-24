"""
Student
Name: Ettore d'Angelo
GT User ID: edangelo3
GT ID: 903248685
"""
import pandas as pd  		   	  			    		  		  		    	 		 		   		 		  
import numpy as np  		   	  			    		  		  		    	 		 		   		 		  
import datetime as dt 
import matplotlib.pyplot as plt		   	  			    		  		  		    	 		 		   		 		  
from util import get_data, plot_data
from marketsimcode import compute_portvals

class TheoreticallyOptimalStrategy:
    
    def testPolicy(self, symbol, sd, ed, sv):
        s = []
        s.append(symbol)
        df_prices = get_data(s, pd.date_range(sd, ed))
        del df_prices['SPY']
        
        df_change = df_prices.values[1:] - df_prices.values[:-1]
        df_change = pd.DataFrame(df_change, columns = [symbol], index = df_prices.index[:-1])
        
        df_position = df_change.copy()
        df_position[df_change > 0] = 1 # hold
        df_position[df_change < 0] = -1 # short
        df_position[df_change == 0] = 0 #do nothing
        
        df_position = df_position.loc[(df_position != 0).any(axis = 1)]
        
        order_list = []
        
        day = df_position.index[0]
        if df_position.loc[day][symbol] > 0:
            order_list.append([day.date(), symbol, 'BUY', 1000])
        elif df_position.loc[day][symbol] < 0:
            order_list.append([day.date(), symbol, 'SELL', 1000])
        
        for i in range(len(df_position.index[1:])):
            day = df_position.index[i+1]
            prev = df_position.index[i]
            if df_position.loc[day][symbol] > df_position.loc[prev][symbol]:
                order_list.append([day.date(), symbol, 'BUY', 2000])
            elif df_position.loc[day][symbol] < df_position.loc[prev][symbol]:
                order_list.append([day.date(), symbol, 'SELL', 2000])
        
        df_orders = pd.DataFrame(data = order_list, columns = ['Date', 'Symbol', 'Order', 'Shares'])
        
        opt = compute_portvals(df_orders, sd, ed, start_val = sv, commission = 0.0, impact = 0.0)
        df_bench = pd.DataFrame(data = [[df_prices.index[0], symbol, 'BUY', 1000]], columns = ['Date', 'Symbol', 'Order', 'Shares'])
        bench = compute_portvals(df_bench, sd, ed, start_val = sv, commission = 0.0, impact = 0.0)
        
        # da salvare in un png e scriverci sotto i valori
        
        # Get daily return
        daily_return_opt = (opt[1:]/ opt[:-1].values) - 1
        daily_return_bench = (bench[1:]/ bench[:-1].values) - 1
        
    
        # Get portfolio statistics (note: std_daily_ret = volatility)
        cr = (opt.iloc[-1] - opt.iloc[0])/ opt.iloc[0]
        print 'Cumulative return opt:', cr.iloc[0]
        cr = (bench.iloc[-1] - bench.iloc[0])/ opt.iloc[0]
        print 'Cumulative return bench:', cr.iloc[0]
        adr = daily_return_opt.mean()
        print 'Mean daily return opt:', adr.iloc[0]
        adr = daily_return_bench.mean()
        print 'Mean daily return bench:', adr.iloc[0]
        sddr = daily_return_opt.std()
        print 'Stdev of daily return opt:', sddr.iloc[0]
        sddr = daily_return_bench.std()
        print 'Stdev of daily return bench:', sddr.iloc[0]
        
        opt /= opt.iloc[0]
        bench /= bench.iloc[0]
        
        plt.plot(opt, c = 'black')
        plt.plot(bench, c = 'blue')
        plt.title('Theoretically optimal strategy')
        plt.savefig('theoretically.png')
        plt.close()

        return df_orders
        
if __name__ == "__main__":
    tos = TheoreticallyOptimalStrategy()
    df_trades = tos.testPolicy("JPM", dt.datetime(2008,1,1), dt.datetime(2009,12,31), 100000) 