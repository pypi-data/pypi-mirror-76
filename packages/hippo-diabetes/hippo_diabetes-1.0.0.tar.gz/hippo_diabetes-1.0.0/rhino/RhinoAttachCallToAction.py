#imports
import pandas as pd
import numpy as np
import itertools
import operator
import unittest
import os
from sklearn.base import BaseEstimator, TransformerMixin


class RhinoAttachCallToAction(BaseEstimator, TransformerMixin):
    """Attach call to action based on the care gap category

    :returns: dataframe with CTA column
    :rtype: pd.DataFrame
    """

    def __init__(self):
        """constructor method
        """
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

    #apply the transformation function
    def transform(self, X, y=None):
        """attach the call to action
        
        Parameters
        :param X: Dataframe of member model output
        :type X: pd.Dataframe
        :param y: np.array 
        :type Y: np.array

        Returns
        :returns: Dataframe with Call to Action column
        :rtype: pd.Dataframe
        """
        # attach call to action
        X['CTA'] = ['go_to_provider' if i in ['MedOpt','Screen','Lifestyle'] else 'get_smbg' if i=='Device' else 'go_to_pharmacist' if i == 'MedAdh' else None for i in X['gap_category']]
        return X
