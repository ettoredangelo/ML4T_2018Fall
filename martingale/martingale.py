"""
The goal of this code is to assess a betting strategy.

Martingale's betting strategy is a set of betting strategies that were popular 
in France in the 18th century in France.
Originally the system was devised to work in the following scenario.
The gambler wins its bet if in a coin toss it comes up heads and loses if it 
comes up tails.
Hence the probability of winning is 50%. The strategy expects the gambler to 
double its bet after every loss and then go back to the initial bet after a 
win. The result is that after a win the gambler will make a profit equal to 
his initial bet.
The Martingale strategy has been used in other different scenarios where the
probability of winning is near to 50%. An exemple of this is the roulette game.
Betting on black/red or even/odd gives you a winning probability that is 
slightly less then 50%.
There are actually two kinds of roulettes. 
The European one has the numbers from zero to 36. The zero is not considered 
neither an even nor an odd number and neither a red nor a black. 
This fact gives the casino the edge. In particular you have a probability of 
winning of 18/37 = 0.4864  in a simple bet.
The American roulette is the same as the European one plus the double zero 
number. This lowers the winning probability to 18/38 = 0.4736.

In this simulation I will simulate the Martingale strategy with an American 
roulette both when you have an infinite amount of money to bet and when you 
instead have a limited amount of money. The gambler initial bet will be 2$ and 
the gambler will stop betting when his total profit is 80$. Moreover the 
gambler can't bet in more then 1000 spins

This file contains the following functions:
    - get_spin_result: Simulates a roulette spin
    - test_code: Runs all the other functions
    - one_run_limited: Performs 1000 throws with limited bank account
    - one_run: Performs 1000 throws with unlimited bank account
    - experiment1: Performs the 1000 throws with unlimited balance account and 
                   then plots the results
    - experiment2: Performs the 1000 throws with limited balance account and 
                   then plots the results

When this file is run the test _code function will be called
"""

import matplotlib
matplotlib.use('Agg')
import numpy as np
import matplotlib.pyplot as plt
  		   	  			    		  		  		    	 		 		   		 		  
def get_spin_result(win_prob):
    '''
    Simulates a roulette spin 
    
    params:
        win_prob: probability for the gambler to win
    return:
        True if the gambler won, False if the gambler lost
    '''
	result = False  		   	  			    		  		  		    	 		 		   		 		  
	if np.random.random() <= win_prob:  		   	  			    		  		  		    	 		 		   		 		  
		result = True  		   	  			    		  		  		    	 		 		   		 		  
	return result  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
def test_code():
    '''
    Runs all the other functions
    '''	   	  			    		  		  		    	 		 		   		 		  
    win_prob = 18.0/38.0 # winning probbility in an American roulette
    np.random.seed(10) # setting the seed so that the experiment is replicable
    experiment1(win_prob)
    experiment2(win_prob)
    
def one_run_limited(win_prob):
    '''
    Performs 1000 throws with limited bank account
    
    params:
        win_prob: probability for the gambler to win
    return:
        list of the balance account after each spin
    '''
    winnings = np.zeros(1001)
    count = 0
    while count < 1000:
        bet_amount = 1
        won = False
        while not won and count < 1000:
            count += 1
            won = get_spin_result(win_prob)
            if won == True:
                winnings[count] = winnings[count-1] + bet_amount
            else:
                winnings[count] = winnings[count-1] - bet_amount
                account = winnings[count] + 256
                if bet_amount * 2 > account:
                    bet_amount = account
                else:
                    bet_amount *= 2
            
            if winnings[count] >= 80 or winnings[count] <= -256:
                winnings[count+1:] = winnings[count]
                return winnings
    
    return winnings
    
def one_run(win_prob):
    '''
    Performs 1000 throws with unlimited bank account
    
    params:
        win_prob: probability for the gambler to win
    return:
        list of the balance account after each spin
    '''
    winnings = np.zeros(1001)
    count = 0
    while count < 1000:
        bet_amount = 1
        won = False
        while not won and count < 1000:
            count += 1
            won = get_spin_result(win_prob)
            if won == True:
                winnings[count] = winnings[count-1] + bet_amount
            else:
                winnings[count] = winnings[count-1] - bet_amount
                bet_amount *= 2
            
            if winnings[count] >= 80:
                winnings[count+1:] = winnings[count]
                return winnings
    
    return winnings

def experiment1(win_prob):
    '''
    Performs the 1000 throws with unlimited balance account and then plots the 
    results
    
    params:
        win_prob: probability for the gambler to win
    '''
    # create plot 10 simulations of the unlimited balance account situation 
    plt.axis([0, 300, -256, 100])
    plt.title('10 simulations')
    for i in range(10):
        winnings = one_run(win_prob)
        plt.plot(winnings)
    plt.savefig('figure1.png')
    plt.close()
    
    # create a plot with the mean and the standard deviation
    plt.axis([0, 300, -256, 100])
    plt.title('Experiment 1 - mean and standard deviation')
    runs = one_run(win_prob)
    for i in range(999):
        winnings = one_run(win_prob)
        runs = np.vstack((runs, winnings))
    mean = np.mean(runs, axis = 0)
    std = np.std(runs, axis = 0)
    plt.plot(mean)
    plt.plot(mean - std, c = 'yellow')
    plt.plot(mean + std, c = 'yellow')
    plt.savefig('figure2.png')
    plt.close()
    
    # create a plot with the median and the standard deviation
    plt.title('Experiment 1 - median and standard deviation')
    plt.axis([0, 300, -256, 100])
    median = np.median(runs, axis = 0)
    plt.plot(median)
    plt.plot(median - std, c = 'yellow')
    plt.plot(median + std, c = 'yellow')
    plt.savefig('figure3.png')
    plt.close()
    
def experiment2(win_prob):
    '''
    Performs the 1000 throws with limited balance account and then plots the 
    results
    
    params:
        win_prob: probability for the gambler to win
    '''
    # figure 4
    plt.axis([0, 300, -256, 100])
    runs = one_run_limited(win_prob)
    for i in range(999):
        winnings = one_run_limited(win_prob)
        runs = np.vstack((runs, winnings))
    
    mean = np.mean(runs, axis = 0)
    std = np.std(runs, axis = 0)
    
    plt.plot(mean)
    plt.title('Experiment 2 - mean and standard deviation')
    plt.plot(mean - std, c = 'yellow')
    plt.plot(mean + std, c = 'yellow')
    plt.savefig('figure4.png')
    plt.close()
    
    # figure 5
    plt.axis([0, 300, -256, 300])
    plt.title('Experiment 2 - median and standard deviation')
    median = np.median(runs, axis = 0)
    plt.plot(median)
    plt.plot(median - std, c = 'yellow')
    plt.plot(median + std, c = 'yellow')
    plt.savefig('figure5.png')
    plt.close() 

if __name__ == "__main__": 	 		 		   		 		  
    test_code()  		   	  			    		  		  		    	 		 		   		 		  
