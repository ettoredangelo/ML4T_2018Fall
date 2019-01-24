# -*- coding: utf-8 -*-
"""
Created on Tue Sep 18 14:38:07 2018

@author: rdangelo
"""

import numpy as np
import DTLearner as dt
import BagLearner as bl
import InsaneLearner as il

dataX = np.array([[ 0.885,  0.33 ,  9.1  ],
       [ 0.725,  0.39 , 10.9  ],
       [ 0.56 ,  0.5  ,  9.4  ],
       [ 0.735,  0.57 ,  9.8  ],
       [ 0.61 ,  0.63 ,  8.4  ],
       [ 0.26 ,  0.63 , 11.8  ],
       [ 0.5  ,  0.68 , 10.5  ],
       [ 0.32 ,  0.78 , 10.   ]])

dataY = np.array([4., 5., 6., 5., 3., 8., 7., 6.])

learner = il.InsaneLearner() # constructor
learner.addEvidence(dataX, dataY) # training step
Y = learner.query(dataX)

