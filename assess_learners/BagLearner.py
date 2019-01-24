# -*- coding: utf-8 -*-
"""
Created on Tue Sep 18 17:45:15 2018

@author: rdangelo
"""

import numpy as np  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
class BagLearner(object):  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
    def __init__(self, learner, kwargs, bags, boost = False, verbose = False):
        self.learners = [learner(**kwargs) for i in range(bags)]
        self.bags = bags
        self.boost = boost
        self.verbose = verbose

  		   	  			    		  		  		    	 		 		   		 		  
    def author(self):  		   	  			    		  		  		    	 		 		   		 		  
        return 'edangelo3' # replace tb34 with your Georgia Tech username
    
    def addEvidence(self, dataX, dataY): 
        for i in range(self.bags):
            perm = np.random.randint(dataX.shape[0], size = dataX.shape[0])
            X = dataX[perm]
            y = dataY[perm]
            self.learners[i].addEvidence(X, y)
    
    def query(self, X):
        result = []
        for i in range(self.bags):
            result.append(self.learners[i].query(X))

        return np.mean(result, axis = 0)	
            
	   	  			    		  		  		    	 		 		   		 		  
if __name__=="__main__":  		   	  			    		  		  		    	 		 		   		 		  
    print "the secret clue is 'zzyzx'"