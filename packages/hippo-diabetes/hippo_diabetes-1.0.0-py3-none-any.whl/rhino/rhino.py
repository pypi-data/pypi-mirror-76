# import packages
import os
import pandas as pd
import unittest
import numpy as np

#import used modules
from RhinoPreCPLPipeline import RhinoPreCPLPipeline

# import from other modules
cwd = os.getcwd()
cwdHead = os.getcwd().split("/hippo/")[0]

#util
os.chdir(cwdHead + '/hippo/src2/util')
from util import UtilAPI

#whal quality controls
os.chdir(cwdHead + '/hippo/src2/whale')
from WhaleRhinoPipeline import WhaleRhinoPipeline

#return to directory
os.chdir(cwd)


#API and JSON builder for the CPL
class RhinoAPI:
    """ for each member, attach the call to action and corresponding bundle values, select the right campaign

    Parameters
    :param X: hippo output - holds all information about care gaps and their values (from hippo.X)
    :type X: pd.DataFrame

    Returns
    :returns: Dataframe with call to action and selected campaign
    :rtype: pd.DataFrame
    """
    
    #init
    def __init__(self):
        """constructor class
        """
        self.modelParam = UtilAPI().modelParam
        self.TestCase = unittest.TestCase()
    #main
    def rhino(self,X):
        
        #initiate modelParam(for lingli)
        modelParam = UtilAPI().modelParam
        
        #preCPL pipeline
        self.X = RhinoPreCPLPipeline().add_pipe().transform(X)
        
        #test preCPL pipeline
        WhaleRhinoPipeline().add_pipe().transform(self.X)
        
        #overall validation
        self.TestCase.assertEqual(X.shape[0],
                                  self.X.shape[0],
                                  "Error in Rhino: Mismatch row counts of raw model output and pre-CPL output.")
        self.TestCase.assertEqual(X['individual_id'].nunique(),
                                  self.X['individual_id'].nunique(),
                                  "Error in Rhino: Mismatch member counts of raw model output and pre-CPL output.")
        np.testing.assert_array_equal(X['care_gap'].value_counts(),
                                      self.X['care_gap'].value_counts(),
                                  "Error in Rhino: Mismatch caregap counts of raw model output and pre-CPL output.")
        
        