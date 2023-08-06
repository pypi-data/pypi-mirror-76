#imports
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
import unittest

class WhaleRhinoTestRankAndWeightTransformer(BaseEstimator, TransformerMixin):
    """evaluates if care gaps are properly bundled and ordered by call to action bundle.  The specific following checks are going to be applied
    Column: 'gap_rank_within_cta'
    1) There are no null rank per member per CTA 
    2) The Rank 1 care gap within CTA has the highest value
    3) There is no duplicate gap rank within cta
    
    Column: 'weighted_gap_value'
    4) There no null weighted gap value.
    5) 100/80/60, 60 forever weights are added to care gap values by rank within CTA
    
    #Column: 'bundle_value','CTA_rank'
    6) Call to action's weighted value sum column has no null
    7) There are no null rank per member per CTA
    8) There are no more than 3 call to action bundles per member
    9) There are no duplicate ranks within a member's call to actions
    10) The Rank 1 CTA has the highest weighted sum
    
   
    

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
        """applies checks related call to action

        :returns: dataframe
        :rtype: pd.DataFrame
        """
        #Checking 'gap_rank_within_cta'
        #1) There are no null rank per member per CTA 
        self.TestCase.assertEqual(X['gap_rank_within_cta'].isnull().any(), False,
                                 "Error in Rhino: gap_rank_within_cta column has null values.")
        
        #2) The Rank 1 care gap within CTA has the highest value
        X['highest_gap_value_in_CTA'] = X[['individual_id','CTA','value']].groupby(['individual_id','CTA'])['value'].transform('max')
        self.TestCase.assertTrue(np.all([rank1Value == maxValue for (rank1Value, maxValue) 
                                          in X.loc[X['gap_rank_within_cta'] == 1, ['value','highest_gap_value_in_CTA']].values]),
                                "Error in Rhino: rank 1 care gaps don't have the highest values.")
        #3) There is no duplicate gap rank within cta
        np.testing.assert_array_equal(X[['individual_id','CTA','gap_rank_within_cta']].groupby(['individual_id','CTA'])['gap_rank_within_cta'].nunique(),
                                  X[['individual_id','CTA','gap_rank_within_cta']].groupby(['individual_id','CTA'])['gap_rank_within_cta'].count(),
                                 "Error in Rhino: some member have duplicate gap_rank_within_cta.")
    
        #Column: 'weighted_gap_value'
        #4) There no null weighted gap value.
        self.TestCase.assertEqual(X['weighted_gap_value'].isnull().any(), False,
                                 "Error in Rhino: weighted_gap_value column has null values.")
        #5) 100/80/60, 60 forever weights are added to care gap values by rank within CTA, zero value care gaps are ignored
        np.testing.assert_array_equal([round(w,2) for w in X.loc[X['value'] != 0,'weighted_gap_value'] / 
                                                           X.loc[X['value'] != 0,'value']], 
                                      [1 if i==1 else 0.8 if i==2 else 0.6 for i in X.loc[X['value'] != 0,'gap_rank_within_cta'] ],
                                      "Error in Rhino: weights are not correctly applied column has null values.")
        
        #Column: 'bundle_value','CTA_rank'
        #6) Call to action's weighted value sum column has no null
        self.TestCase.assertEqual(X['bundle_value'].isnull().any(), False,
                                 "Error in Rhino: bundle_value column has null values.")
        
        #7) There are no null rank per member per CTA
        self.TestCase.assertEqual(X['CTA_rank'].isnull().any(), False,
                                 "Error in Rhino: CTA_rank column has null values.")
        
        #8) There are no more than 3 call to action bundles per member
        self.TestCase.assertTrue(np.all([True if count <=3 else False 
                                         for count in X[['individual_id','CTA']].groupby(['individual_id'])['CTA'].nunique().values]),
                                 "Error in Rhino: some members have more than 3 CTA assigned")
        
        #9) The Rank 1 CTA has the highest weighted sum
        X['highest_bundle_value'] = X[['individual_id','CTA','bundle_value']].groupby(['individual_id','CTA'])['bundle_value'].transform('max')
        self.TestCase.assertTrue(np.all([rank1Value == maxValue for (rank1Value, maxValue) 
                                          in X.loc[X['CTA_rank'] == 1, ['bundle_value','highest_bundle_value']].values]),
                                 "Error in Rhino: rank 1 CTA bundle don't have the highest bundle value.")
        
        X.drop(columns = ['highest_gap_value_in_CTA', 'highest_bundle_value'], inplace = True)
      
        #return X (if there are no errors) for additional tests
        return X