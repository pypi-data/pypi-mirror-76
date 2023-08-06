import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
import unittest

class WhaleRhinoTestProactiveChannelSelectorTransformer(BaseEstimator, TransformerMixin):
    """evaluate if proactive channels are selected correctly 
    
    1) There are no null value in 'proactive_call' column
    2) proactive channel is limited to only the following options : ['health_hub', 'care_coordinator', 'pharmacist_cpco']
    3) There are no 'health_hub' selected if no healthhub access
    4) There are no 'pharmacist_cpco' selected if no cvs filler
    5) There are no 'pharmacist_cpco' selected for campaign of Screen,Lifestyle,Device

    
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
        """apply checks to 'proactive_call' column
        :returns: dataframe
        :rtype: pd.DataFrame
        """
      
        #1) There are no null value for each channel selection 
        self.TestCase.assertEqual(X['proactive_call'].isnull().any(),
                                    False,
                                    "Error in Rhino: proactive_call column has null values")
        # 2) proactive channel is limited to only the following options : ['health_hub', 'care_coordinator', 'pharmacist_cpco']
        self.TestCase.assertTrue(np.all([True if x in ['health_hub', 'care_coordinator', 'pharmacist_cpco'] else False for x in set(X['proactive_call'])]),
                                 "Error in Rhino: proactive_call column has values other than 'health_hub', 'care_coordinator', 'pharmacist_cpco'.")
        
        # 3) There are no 'health_hub' selected if no healthhub access
        self.TestCase.assertEqual(X[(X['proactive_call'] == 'health_hub') & (X['has_healthhub_access']!=1)].shape[0],
                                    0,
                                    "Error in Rhino: Health_hub are selected without healthhub access")
        
        
        # 4) There are no 'pharmacist_cpco' selected if no cvs filler
        self.TestCase.assertEqual(X[(X['proactive_call'] == 'pharmacist_cpco') & (X['is_cvs_filler']!=1)].shape[0],
                                    0,
                                    "Error in Rhino: pharmacist_cpco are selected with no cvs filler")
        
        #5) There are no 'pharmacist_cpco' selected for campaign of Screen,Lifestyle,Device
        self.TestCase.assertEqual(X[(X['proactive_call'] == 'pharmacist_cpco') & (X['selected_campaign'].isin(['Screen','Lifestyle','Device']))].shape[0],
                                    0,
                                    "Error in Rhino: pharmacist_cpco are selected for Screen,Lifestyle,Device Campaign")
        
        

        
        #return X (if there are no errors) for additional tests
        return X
