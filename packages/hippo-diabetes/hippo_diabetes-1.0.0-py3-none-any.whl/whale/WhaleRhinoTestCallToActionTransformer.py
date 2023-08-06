#imports
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
import unittest

class WhaleRhinoTestCallToActionTransformer(BaseEstimator, TransformerMixin):
    """evaluates if call to action was properly applied.  The specific following checks are going to be appled
    1) Care Gap Category limited to only the following options : ['MedAdh', 'Lifestyle', 'Screen', 'Device', 'MedOpt']
    2) Care Gap Category has no nulls
    3) Call to Action is limited to only the following options : ['go_to_provider', 'get_smbg', 'go_to_pharmacist']
    4) Call to Action has no nulls
    5) There are equal row counts for member-gaps that have care gap category as 'MedAdh' and call to action as 'go_to_pharmacist'
    6) There are equal row counts for member-gaps that have care gap category as 'Device' and call to action as 'get_smbg'
    7) There are equal row counts for member-gaps that have care gap category among ['Lifestyle', 'Screen', 'MedOpt'] and call to action as 'go_to_provider'

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

        #1) Care Gap Category limited to only the following options : ['MedAdh', 'Lifestyle', 'Screen', 'Device', 'MedOpt']
        self.TestCase.assertTrue(np.all([True if x in ['MedAdh', 'Lifestyle', 'Screen', 'Device', 'MedOpt'] else False for x in set(X['gap_category'])]),
                                 """Error in Rhino: Care Gap Category column has values other than 'MedAdh', 'Lifestyle', 'Screen', 'Device', 'MedOpt'.""")

        #2) Care Gap Category has no nulls
        self.TestCase.assertTrue(np.any(pd.notnull(X['gap_category'])),
                                 "Error in Rhino: Care Gap Category column has nulls values.")

        #3) Call to Action is limited to only the following options : ['go_to_provider', 'get_smbg', 'go_to_pharmacist']
        self.TestCase.assertTrue(np.all([True if x in ['go_to_provider', 'get_smbg', 'go_to_pharmacist'] else False for x in set(X['CTA'])]),
                                 """Error in Rhino: Call to Action column has values other than 'go_to_provider', 'get_smbg', 'go_to_pharmacist'.""")

        #4) Call to Action has no nulls
        self.TestCase.assertTrue(np.any(pd.notnull(X['CTA'])),
                                 "Error in Rhino: CTA column has nulls values.")
        
        #5) There are equal row counts for member-gaps that have care gap category as 'MedAdh' and call to action as 'go_to_pharmacist'
        self.TestCase.assertEqual(X[X['gap_category']=='MedAdh'].shape[0],
                                  X[X['CTA']=='go_to_pharmacist'].shape[0],
                                  "Error in Rhino: Mismatch between count of rows of 'MedAdh' (gap category) and 'go_to_pharmacist' (CTA).")

        #6) There are equal row counts for member-gaps that have care gap category as 'Device' and call to action as 'get_smbg'
        self.TestCase.assertEqual(X[X['gap_category']=='Device'].shape[0],
                                  X[X['CTA']=='get_smbg'].shape[0],
                                  "Error in Rhino: Mismatch between count of rows of 'Device' (gap category) and 'get_smbg' (CTA).")

        #7) There are equal row counts for member-gaps that have care gap category among ['Lifestyle', 'Screen', 'MedOpt'] and call to action as 'go_to_provider'
        self.TestCase.assertEqual(X[(X['gap_category']=='Lifestyle')|(X['gap_category']=='Screen')|(X['gap_category']=='MedOpt')].shape[0],
                                  X[X['CTA']=='go_to_provider'].shape[0],
                                  "Error in Rhino: Mismatch between count of rows of 'Lifestyle', 'Screen', and 'MedOpt' (gap category) and 'go_to_provider' (CTA).")

        #return X (if there are no errors) for additional tests
        return X