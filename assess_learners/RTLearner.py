# -*- coding: utf-8 -*-
"""
Created on Tue Sep 18 13:18:51 2018

@author: ettoredangelo

A simpe Decision Tree Learner
"""

import numpy as np  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
class RTLearner(object):  		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
    def __init__(self, leaf_size = 1, verbose = False):
        self.leaf_size = leaf_size
        self.verbose = verbose

  		   	  			    		  		  		    	 		 		   		 		  
    def author(self):  		   	  			    		  		  		    	 		 		   		 		  
        return 'edangelo3' # replace tb34 with your Georgia Tech username 

    def build_tree(self, dataX, dataY):
        
        # Handle only few data remaining
        if dataX.shape[0] <= self.leaf_size:
            return np.array([[-1, np.mean(dataY), np.NaN, np.NaN]])
        
        # Handle all remaining data equal
        if len(set(dataY)) == 1:
            return np.array([[-1, np.mean(dataY), np.NaN, np.NaN]])
        
        else:
            # Choose feature based on correlation
            if self.verbose:
                print dataX.shape
                print dataY.shape
            
            feat = np.random.randint(dataX.shape[1])
            SplitVal = np.median(dataX[:,feat])
            
            if np.max(dataX[:,feat]) == np.median(dataX[:,feat]):
                return np.array([[-1, np.mean(dataY), np.NaN, np.NaN]])
            
            if self.verbose:
                print feat
                print SplitVal
            
            # Build tree
            
            lefttree = self.build_tree(dataX[dataX[:,feat]<=SplitVal], dataY[dataX[:,feat]<=SplitVal])
            righttree = self.build_tree(dataX[dataX[:,feat]>SplitVal], dataY[dataX[:,feat]>SplitVal])
            root = np.array([feat, SplitVal, 1,	 lefttree.shape[0] +	1])
            return np.vstack((root, lefttree, righttree)) 		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
    def addEvidence(self, dataX, dataY):  		   	  			    		  		  		    	 		 		   		 		  
        """  		   	  			    		  		  		    	 		 		   		 		  
        @summary: Add training data to learner  		   	  			    		  		  		    	 		 		   		 		  
        @param dataX: X values of data to add  		   	  			    		  		  		    	 		 		   		 		  
        @param dataY: the Y training values  		   	  			    		  		  		    	 		 		   		 		  
        """ 		   	  			    		  		  		    	 		 		   		 		  
        self.matrix = self.build_tree(dataX, dataY)

    def single_query(self, X):
        """
        @summary: Estimate a single test point given the model we built.  		   	  			    		  		  		    	 		 		   		 		  
        @param X: a test point.  		   	  			    		  		  		    	 		 		   		 		  
        @returns the estimated value according to the saved model.
        """
        matrix = self.matrix
        i = 0
        l = matrix[i]
        while l[0] != -1:
            if X[int(l[0])] <= l[1]:
                i += int(l[2])
                l = matrix[i]
            else:
                i += int(l[3])
                l = matrix[i]
        return l[1]
  		   	  			    		  		  		    	 		 		   		 		  
    def query(self, X):  		   	  			    		  		  		    	 		 		   		 		  
        """  		   	  			    		  		  		    	 		 		   		 		  
        @summary: Estimate a set of test points given the model we built.  		   	  			    		  		  		    	 		 		   		 		  
        @param X: should be a numpy array with each row corresponding to a specific query.  		   	  			    		  		  		    	 		 		   		 		  
        @returns the estimated values according to the saved model.  		   	  			    		  		  		    	 		 		   		 		  
        """
        result = []
        for it in range(X.shape[0]):
            result.append(self.single_query(X[it]))
        return result		   	  			    		  		  		    	 		 		   		 		  

	   	  			    		  		  		    	 		 		   		 		  
if __name__=="__main__":  		   	  			    		  		  		    	 		 		   		 		  
    print "the secret clue is 'zzyzx'"