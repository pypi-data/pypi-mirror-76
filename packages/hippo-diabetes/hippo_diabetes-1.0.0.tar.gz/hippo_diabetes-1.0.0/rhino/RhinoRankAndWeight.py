#imports
import pandas as pd
import numpy as np
import itertools
import operator
import unittest
import os
from sklearn.base import BaseEstimator, TransformerMixin


class RhinoRankAndWeight(BaseEstimator, TransformerMixin):
    """added weighted care gap values and rank the gap values within call to actions

    :returns: dataframe 
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
        """create the gap rank within each CTA for each member, and add the weighted gap value using 100-80-60 haircut rule and sum it within each CTA
        Parameters
        :param X: Dataframe of member model output
        :type X: pd.Dataframe
        :param y: np.array 
        :type Y: np.array

        Returns
        :returns: Dataframe with gap rank, weighted gap value and bundle value for each CTA
        :rtype: pd.Dataframe
        """
        # care gap rank within Call to action
        X['gap_rank_within_cta'] = X[['individual_id','CTA','value']].groupby(['individual_id','CTA'], sort=False).rank(ascending=False,method='first')
        
        # care gap weighted value using 100-80-60 cuts
        X['weighted_gap_value'] = [1 if i==1 else 0.8 if i==2 else 0.6 for i in X['gap_rank_within_cta']]*X['value']
        
        # calculate the bundle value of call to actions for each member
        X['bundle_value'] = X[['individual_id','CTA','weighted_gap_value']].groupby(['individual_id','CTA'])['weighted_gap_value'].transform('sum')
        
        return X
