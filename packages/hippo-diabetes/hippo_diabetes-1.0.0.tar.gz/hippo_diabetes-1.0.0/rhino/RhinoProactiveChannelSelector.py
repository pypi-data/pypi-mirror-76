#imports
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin


class RhinoProactiveChannelSelector(BaseEstimator, TransformerMixin):
    """Pick the preferred proactive call channel based on CTA decision tree
    :param proactive_channels: names of direct proactive call channels, configured in util
    :type proactive_channels: list
 

    :returns: dataframe with one additional transformed columns
    :rtype: pd.DataFrame
    """

    def __init__(self, proactive_channels):
        """constructor method
        """
        self.proactive_channels =proactive_channels

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
        """function to select the preferred proactive call based on CTA decision tree

        Parameters
        :param X: np.array of features of interest for training
        :type X: np.array
        :param y: np.array of features of interest for testing (none in this case)
        :type Y: np.array

        :returns: dataframe
        :rtype: pd.DataFrame
        """        
        # version 1: don't use cpco for screen, lifelstyle, device
        X.loc[X['selected_campaign'].isin(['Screen','Lifestyle','Device','MedAdh']) & (X['has_healthhub_access'] ==1), 'proactive_call'] = 'health_hub'
        X.loc[X['selected_campaign'].isin(['Screen','Lifestyle','Device','MedAdh']) & (X['has_healthhub_access'] !=1), 'proactive_call'] = 'care_coordinator'

        X.loc[X['selected_campaign'].isin(['MedOpt']) & (X['is_cvs_filler'] ==1) , 'proactive_call'] = 'pharmacist_cpco'
        X.loc[X['selected_campaign'].isin(['MedOpt']) & (X['is_cvs_filler'] !=1) & (X['has_healthhub_access']==1), 'proactive_call'] = 'health_hub'
        X.loc[X['selected_campaign'].isin(['MedOpt']) & (X['is_cvs_filler'] !=1) & (X['has_healthhub_access']!=1), 'proactive_call'] = 'care_coordinator'
        
        # add a column of the selected proactive call availability
        X['procall_open'] = X.lookup(X.index, "select_"+X['proactive_call'])

        #return X
        return X