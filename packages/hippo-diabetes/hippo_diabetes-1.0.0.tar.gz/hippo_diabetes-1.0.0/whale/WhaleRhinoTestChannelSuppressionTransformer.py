#imports
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
import unittest

class WhaleRhinoTestChannelSuppressionTransformer(BaseEstimator, TransformerMixin):
    """make sure program overlap based channel suppression is implemented
    
    1) 'select_ivr' should be 0 any of the program overlap indicator is 1 except Hot Hedis
    2) 'select_care_coordinator' should be 0 if any of the program overlap indicator is 1
    
    :returns: dataframe as inputted no changes (else asserts error)
    :rtype: pd.DataFrame
    """

    def __init__(self, no_IVR_CC_prgms, no_CC_prgms):
        """constructor method
        """
        self.TestCase = unittest.TestCase()
        self.no_IVR_CC_prgms = no_IVR_CC_prgms
        self.no_CC_prgms = no_CC_prgms


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
        """applies checks related call to action

        :returns: dataframe
        :rtype: pd.DataFrame
        """
        #1) For members with IVR available, they should not be overlapped with any programs, except hot hedis.
        self.TestCase.assertEqual(X.loc[X['select_ivr'] == 1, self.no_IVR_CC_prgms].sum(axis =1).max(), 
                                      0,
                                     "Error in Rhino: ivr is used while the member is targeted/engaged by other programs")
        #2) for members with Care Coordinator available, they should be not overlapped with any programs.
        self.TestCase.assertEqual(X.loc[(X['proactive_call'] == "care_coordinator") & (X['procall_open'] == 1), self.no_IVR_CC_prgms + self.no_CC_prgms].sum(axis =1).max(), 
                                      0,
                                     "Error in Rhino: care coordinator is used while the member is targeted/engaged by hot hedis")
        
        #return X (if there are no errors) for additional tests
        return X