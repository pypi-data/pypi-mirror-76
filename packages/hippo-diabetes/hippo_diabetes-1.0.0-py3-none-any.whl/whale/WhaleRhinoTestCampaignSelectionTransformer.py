#imports
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
import unittest

class WhaleRhinoTestCampaignSelectionTransformer(BaseEstimator, TransformerMixin):
    """evaluates if the campaign assignment matches the care gap category of the most valuable care gap
    
    Column: 'selected_campaign'
    1) There no null selected campaign value.
    2) If the selected campaign values are the same for same member same CTA
    3) The value should be the same as the caregap category of most valuable in the CTA bundle
    
    :returns: dataframe as inputted no changes (else asserts error)
    :rtype: pd.DataFrame
    """

    def __init__(self):
        """constructor method
        """
        self.TestCase = unittest.TestCase()
        pass


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
        #Checking 'gap_rank_within_cta'
        #1) There are no null assigned campaign per member per CTA 
        self.TestCase.assertEqual(X['selected_campaign'].isnull().any(), False,
                                 "Error in Rhino: selected_campaign column has null values.")
        
        #2) The assigned campaigns should be the same if the care gap belongs to the same CTA per member
        self.TestCase.assertTrue(np.all([1==a for a in X[['individual_id', 'CTA', 'selected_campaign']].groupby(['individual_id', 'CTA'])['selected_campaign'].nunique()]),
                                "Error in Rhino: different campaign assigned to care gaps within one CTA per member.")
       
        #3) The assigned campaigns should match the most valuable care gap in each CTA bundle for each member
        self.TestCase.assertTrue(np.all([a==b for (a,b) in X.loc[X['gap_rank_within_cta'] == 1,['gap_category','selected_campaign']].values]),
                                 "Erro in Rhino: the selected campaign does not match the most valuable care gap")
        #return X (if there are no errors) for additional tests
        return X