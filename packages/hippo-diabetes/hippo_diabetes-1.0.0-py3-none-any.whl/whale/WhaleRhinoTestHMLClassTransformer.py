import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
import unittest

class WhaleRhinoTestHMLClassTransformer(BaseEstimator, TransformerMixin):
    """make sure member journey are classified as High, Medium, Low correctly
    
    1) There are no null value in 'JourneyLevel' column
    2) There are no 'High' journey without available proactive call
    3) There are no 'Medium' journey with available proactive call
    4) There are no 'Medium' journey without neither ivr nor direct mail
    5) There are no 'Low' journey with ivr or direct mail or proactive channel open
    
    :returns: dataframe as inputted no changes (else asserts error)
    :rtype: pd.DataFrame
    """

    def __init__(self):
        """constructor method
        """
        self.TestCase = unittest.TestCase()
        
    # fit function, leave untouched - sklearn needs this, but we do not
    def fit(self, X, y=None):
        """fit method for collaborating with pipeline
        Parameters
        :param X: np.array of features of interest for training
        :type X: np.array
        :param y: np.array of features of interest for testing (none in this case)
        :type Y: np.array
        Returns
        :returns: fited data frame
        :rtype: sklearn.base.BaseEstimator
        """
        return self

        # main function

    def transform(self, X, y=None):
        """apply checks to JourneyLevel column
        :returns: dataframe
        :rtype: pd.DataFrame
        """
      
        #1) There are no null value for each channel selection 
        self.TestCase.assertEqual(X['JourneyLevel'].isnull().any(),
                                    False,
                                    "Error in Rhino: JourneyLevel column has null values")
        
        #2) There are no 'High' journey without available proactive call
        self.TestCase.assertEqual(X[(X['JourneyLevel'] == 'High') & (X['procall_open']==0)].shape[0],
                                    0,
                                    "Error in Rhino: High journeys are assigned without open proactive channel")
        #3) There are no 'Medium' journey with available proactive call
        self.TestCase.assertEqual(X[(X['JourneyLevel'] == 'Medium') & (X['procall_open']==1)].shape[0],
                                    0,
                                    "Error in Rhino: Medium journeys are assigned with open proactive channel")
        #4) There are no 'Medium' journey without neither ivr nor direct mail
        self.TestCase.assertEqual(X[(X['JourneyLevel'] == 'Medium') & (X['select_ivr']==0) & (X['select_dm']==0)].shape[0],
                                    0,
                                    "Error in Rhino: Medium journeys are assigned without IVR nor Diret Mail")
        #5) There are no 'Low' journey with ivr or direct mail or proactive channel open
        self.TestCase.assertEqual(X[(X['JourneyLevel'] == 'Low') & ((X['select_ivr']==1) | (X['select_dm']==1) | (X['procall_open']==1))].shape[0],
                                    0,
                                    "Error in Rhino: Low journeys are assigned with IVR or Diret Mail or Proactive channel available")
        
        #return X (if there are no errors) for additional tests
        return X
