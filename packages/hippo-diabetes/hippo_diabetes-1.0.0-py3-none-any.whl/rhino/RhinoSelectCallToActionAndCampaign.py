#imports
import pandas as pd
import numpy as np
import itertools
import operator
import unittest
import os
from sklearn.base import BaseEstimator, TransformerMixin


class RhinoSelectCallToActionAndCampaign(BaseEstimator, TransformerMixin):
    """for each member, rank the call to action based on the bundle value and select the campagin 
    
    :returns: dataframe with rank of call to action and selected campaign
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
        """add columns for CTA rank and selected campaign
        
        Parameters
        :param X: Dataframe of member model output
        :type X: pd.Dataframe
        :param y: np.array 
        :type Y: np.array

        Returns
        :returns: Dataframe with Call to Action column
        :rtype: pd.Dataframe
        """
        # for each member, rank the call to action based on bundle values
        X['CTA_rank'] = X[['individual_id','bundle_value']].groupby('individual_id', sort=False).rank(ascending=False, method='dense')
        
        # per each CTA, select the top care gap category(campaign)
        xCate = X[X['gap_rank_within_cta'] == 1][['individual_id','CTA','gap_category']]
        xCate.columns = ['individual_id','CTA','selected_campaign']
        
        # for each member, select the campaign(same campaign for same call to action for each member)
        X = X.merge(xCate,how='left',on=['individual_id','CTA'])
              
        return X
