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
from indicators import smacalc, bollinger, smaoverprice, Rsi, momentum_calc

class ManualStrategy:
    
    def testPolicy(self, symbol, sd, ed, sv):
        lookback = 18
        period = 10
        
        symbols = []
        symbols.append(symbol)
        
        price = get_data(symbols, pd.date_range(sd, ed))
    
        sma = smacalc(price, lookback)
        bbp = bollinger(price, lookback, sma)
        sma = smaoverprice(sma, price)
        rsi = Rsi(lookback, price)
        mom = momentum_calc(price, period)
        
        orders = price.copy()
        orders.ix[:,:] = np.nan
        
        spy_mom = mom.copy()
        spy_mom.values[:,:] = spy_mom.ix[:,['SPY']]
        
        sma_cross = pd.DataFrame(0, index = sma.index, columns = sma.columns)
        sma_cross[sma >= 1] = 1
        
        sma_cross[1:] = sma_cross.diff()
        sma_cross.ix[0] = 0
        
        orders[(sma < 0.95) & (bbp < 0) & (mom < 0) & (spy_mom > 0)] = 1000
        orders[(sma > 1.05) & (bbp > 1) & (mom > 0) & (spy_mom < 0)] = - 1000

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
    
    def author(self):
        return 'edangelo3'
        
        
    
if __name__ == "__main__":
    
    sd = dt.datetime(2008,1,1)
    ed = dt.datetime(2009,12,31)
    sv = 100000
    
    ms = ManualStrategy()
    df_trades = ms.testPolicy("JPM", sd, ed, sv)   
    
    price = get_data(['JPM'], pd.date_range(sd, ed))
    
    opt = compute_portvals(df_trades, sd, ed, start_val = sv, commission = 9.95, impact = 0.005)
    df_bench = pd.DataFrame(data = [[price.index[0], 'JPM', 'BUY', 1000]], columns = ['Date', 'Symbol', 'Order', 'Shares'])
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
#        spy = price['SPY'].copy()
#        spy /= spy.iloc[0]
    
    plt.plot(opt, c = 'black')
    plt.plot(bench, c = 'blue')
    book = df_trades.iloc[::2, :]
    for row in range(book.shape[0]):
        if book['Order'].iloc[row] == 'BUY':
            color = 'green'
        else:
            color = 'red'
        plt.axvline(x = book['Date'].iloc[row], c = color)
#        plt.plot(spy, c = 'red')
    plt.savefig('figure1.png')
    plt.close()
    
    
    # out of sample
    print 'OUT OF SAMPLE'
    sd = dt.datetime(2010,1,1)
    ed = dt.datetime(2011,12,31)
    df_trades = ms.testPolicy("JPM", sd, ed, sv)
    
    price = get_data(['JPM'], pd.date_range(sd, ed))
    
    opt = compute_portvals(df_trades, sd, ed, start_val = sv, commission = 9.95, impact = 0.005)
    df_bench = pd.DataFrame(data = [[price.index[0], 'JPM', 'BUY', 1000]], columns = ['Date', 'Symbol', 'Order', 'Shares'])
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
#        spy = price['SPY'].copy()
#        spy /= spy.iloc[0]
    
    plt.plot(opt, c = 'black')
    plt.plot(bench, c = 'blue')
    book = df_trades.iloc[::2, :]
    for row in range(book.shape[0]):
        if book['Order'].iloc[row] == 'BUY':
            color = 'green'
        else:
            color = 'red'
        plt.axvline(x = book['Date'].iloc[row], c = color)
#        plt.plot(spy, c = 'red')
    plt.savefig('figure2.png')
    plt.close()
    