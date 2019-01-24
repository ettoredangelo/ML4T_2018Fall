"""  		   	  			    		  		  		    	 		 		   		 		  
Test a learner.  (c) 2015 Tucker Balch  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
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
import math  		   	  			    		  		  		    	 		 		   		 		  
import LinRegLearner as lrl 
import DTLearner as dt
import RTLearner as rt
import BagLearner as bl
import sys
import matplotlib.pyplot as plt
import pandas as pd
import time		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
if __name__=="__main__":  		   	  			    		  		  		    	 		 		   		 		  
    if len(sys.argv) != 2:  		   	  			    		  		  		    	 		 		   		 		  
        print "Usage: python testlearner.py <filename>"  		   	  			    		  		  		    	 		 		   		 		  
        sys.exit(1)  		   	  			    		  		  		    	 		 		   		 		  
    
    if sys.argv[1].lower() == 'data/istanbul.csv':
        data = pd.read_csv(sys.argv[1])
        del data['date']
        data = data.values
    else:
        inf = open(sys.argv[1])
        data = np.array([map(float,s.strip().split(',')) for s in inf.readlines()])  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
    # compute how much of the data is training and testing  		   	  			    		  		  		    	 		 		   		 		  
    train_rows = int(0.6 * data.shape[0])  		   	  			    		  		  		    	 		 		   		 		  
    test_rows = data.shape[0] - train_rows  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
    # separate out training and testing data  		   	  			    		  		  		    	 		 		   		 		  
    trainX = data[:train_rows,0:-1]  		   	  			    		  		  		    	 		 		   		 		  
    trainY = data[:train_rows,-1]  		   	  			    		  		  		    	 		 		   		 		  
    testX = data[train_rows:,0:-1]  		   	  			    		  		  		    	 		 		   		 		  
    testY = data[train_rows:,-1]  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		   		   	  			    		  		  		    	 		 		   		 		  

    s = [] # in sample result
    o = [] #out of sample result
    for i in range(1,51):
        learner = dt.DTLearner(leaf_size = i, verbose = False) # create a LinRegLearner
        learner.addEvidence(trainX, trainY)
        predY = learner.query(trainX) # get the predictions  		   	  			    		  		  		    	 		 		   		 		  
        rmse = math.sqrt(((trainY - predY) ** 2).sum()/trainY.shape[0])
        s.append(rmse)
        
        predY = learner.query(testX) # get the predictions  		   	  			    		  		  		    	 		 		   		 		  
        rmse = math.sqrt(((testY - predY) ** 2).sum()/testY.shape[0])
        o.append(rmse)
    plt.clf()
    plt.plot([i for i in range(1,51)], s, label = 'in sample')
    plt.plot([i for i in range(1,51)], o, label = 'out of sample')
    plt.title('Question 1')
    plt.xlabel('leaf size')
    plt.ylabel('RMSE')
    plt.legend()
    plt.savefig('Question1.png')
    
    s = [] # in sample result
    o = [] #out of sample result
    for i in range(1,51):
        learner = bl.BagLearner(dt.DTLearner, kwargs = {'leaf_size': i}, bags = 10, boost = False, verbose = False) # create a LinRegLearner
        learner.addEvidence(trainX, trainY)
        predY = learner.query(trainX) # get the predictions  		   	  			    		  		  		    	 		 		   		 		  
        rmse = math.sqrt(((trainY - predY) ** 2).sum()/trainY.shape[0])
        s.append(rmse)
        
        predY = learner.query(testX) # get the predictions  		   	  			    		  		  		    	 		 		   		 		  
        rmse = math.sqrt(((testY - predY) ** 2).sum()/testY.shape[0])
        o.append(rmse)
    
    plt.clf()
    plt.plot([i for i in range(1,51)], s, label = 'in sample')
    plt.plot([i for i in range(1,51)], o, label = 'out of sample')
    plt.title('Question 2')
    plt.xlabel('leaf size')
    plt.ylabel('RMSE')
    plt.legend()
    plt.savefig('Question2.png')
    
    plt.close()
    
    ld = [] # decision trees
    lr = [] # random trees
    qd = [] # decision trees
    qr = [] # random trees
    dl = []
    rl = []
    for i in range(1,51):
        start = time.time()
        learner = dt.DTLearner(leaf_size =  i, verbose = False)
        learner.addEvidence(trainX, trainY)
        end = time.time()
        ld.append(end-start)
        dl.append(learner.matrix.shape[0])
        
        start = time.time()
        learner.query(testX)
        end = time.time()
        qd.append(end-start)
        
        start = time.time()
        learner = rt.RTLearner(leaf_size =  i, verbose = False)
        learner.addEvidence(trainX, trainY)
        end = time.time()
        lr.append(end-start)
        rl.append(learner.matrix.shape[0])
        
        start = time.time()
        learner.query(testX)
        end = time.time()
        qr.append(end-start)
    
    plt.clf()
    plt.plot([i for i in range(1,51)], ld, label = 'Decision tree')
    plt.plot([i for i in range(1,51)], lr, label = 'Random tree')
    plt.title('Learning Time')
    plt.xlabel('leaf size')
    plt.ylabel('seconds')
    plt.legend()
    plt.savefig('Learning_time.png')
    
    plt.clf()
    plt.plot([i for i in range(1,51)], qd, label = 'Decision tree')
    plt.plot([i for i in range(1,51)], qr, label = 'Random tree')
    plt.title('Quering Time')
    plt.xlabel('leaf size')
    plt.ylabel('seconds')
    plt.legend()
    plt.savefig('Quering_time.png')
    
    plt.clf()
    plt.plot([i for i in range(1,51)], dl, label = 'Decision tree')
    plt.plot([i for i in range(1,51)], rl, label = 'Random tree')
    plt.title('Complexity')
    plt.xlabel('leaf size')
    plt.ylabel('nodes')
    plt.legend()
    plt.savefig('complexity.png')
    
    
    ds = []
    do = []
    rs = []
    ro = []
    for i in range (1, 51):
       
        learner = dt.DTLearner(leaf_size = i, verbose = False) # create a LinRegLearner
        learner.addEvidence(trainX, trainY)
        predY = learner.query(trainX) # get the predictions  		   	  			    		  		  		    	 		 		   		 		  
        rmse = math.sqrt(((trainY - predY) ** 2).sum()/trainY.shape[0])
        ds.append(rmse)
        
        predY = learner.query(testX) # get the predictions  		   	  			    		  		  		    	 		 		   		 		  
        rmse = math.sqrt(((testY - predY) ** 2).sum()/testY.shape[0])
        do.append(rmse)
        
        learner = rt.RTLearner(leaf_size = i, verbose = False) # create a LinRegLearner
        learner.addEvidence(trainX, trainY)
        predY = learner.query(trainX) # get the predictions  		   	  			    		  		  		    	 		 		   		 		  
        rmse = math.sqrt(((trainY - predY) ** 2).sum()/trainY.shape[0])
        rs.append(rmse)
        
        predY = learner.query(testX) # get the predictions  		   	  			    		  		  		    	 		 		   		 		  
        rmse = math.sqrt(((testY - predY) ** 2).sum()/testY.shape[0])
        ro.append(rmse)
        
    plt.clf()
    plt.plot([i for i in range(1, 51)], ds, label = 'Decision tree')
    plt.plot([i for i in range(1, 51)], rs, label = 'Random tree')
    plt.title('In sample accuracy')
    plt.xlabel('leaf size')
    plt.ylabel('RMSE')
    plt.legend()
    plt.savefig('comparison_sample.png')
    
    plt.clf()
    plt.plot([i for i in range(1, 51)], do, label = 'Decision tree')
    plt.plot([i for i in range(1, 51)], ro, label = 'Random tree')
    plt.title('Out of sample accuracy')
    plt.xlabel('leaf size')
    plt.ylabel('RMSE')
    plt.legend()
    plt.savefig('comparison_out.png')
    
    plt.clf()
    plt.plot([i for i in range(1, 51)], rs, label = 'In sample')
    plt.plot([i for i in range(1, 51)], ro, label = 'out of sample')
    plt.title('Random tree accuracy')
    plt.xlabel('leaf size')
    plt.ylabel('RMSE')
    plt.legend()
    plt.savefig('random.png')