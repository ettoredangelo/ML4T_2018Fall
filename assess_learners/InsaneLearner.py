import numpy as np 
import BagLearner as bl
import LinRegLearner as lrl 		   	  			    		  		  		    	 		 		   		 		  
  		   	  			    		  		  		    	 		 		   		 		  
class InsaneLearner(object): 		   	  			    		  		  		    	 		 		   		 		  
    def __init__(self, verbose = False):
        self.learner = bl.BagLearner(learner= bl.BagLearner, kwargs = {'learner' : lrl.LinRegLearner, 'kwargs' :{}, 'bags': 20, 'boost' : False, 'verbose': False}, bags = 20, boost = False, verbose = False)       
    def author(self):  		   	  			    		  		  		    	 		 		   		 		  
        return 'edangelo3' # replace tb34 with your Georgia Tech username    
    def addEvidence(self, dataX, dataY): 
        self.learner.addEvidence(dataX, dataY)
    def query(self, X):
        self.learner.query(X)

if __name__=="__main__":  		   	  			    		  		  		    	 		 		   		 		  
    print "the secret clue is 'zzyzx'"