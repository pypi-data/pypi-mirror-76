#imports
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin


class RhinoHighMediumLowClassfier(BaseEstimator, TransformerMixin):
    """ Classify member journey into High/ Medium/ Low
    :param direct_comms: name of direct communication channels
    :type direct_comms: list of strings
    :param proactive_channels: name of proactive call channels
    :type proactive_channels: list of string

    :returns: dataframe with one additional transformed columns
    :rtype: pd.DataFrame
    """

    def __init__(self,direct_comms, proactive_channels):
        """constructor method
        """
        self.direct_comms = direct_comms
        self.proactive_channels = proactive_channels

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
        """function to select only the columns of interest

        Parameters
        :param X: np.array of features of interest for training
        :type X: np.array
        :param y: np.array of features of interest for testing (none in this case)
        :type Y: np.array

        :returns: dataframe
        :rtype: pd.DataFrame
        """
        # classify member journey into High/ Medium/ Low      
        # if the member' preferred proactive call is available, then High journey
        X.loc[X['procall_open']==1, 'JourneyLevel'] = 'High'      
        # if the member does not have any proactive channel, but has both ivr and letter open, then Medium journey        
        X.loc[(X['procall_open']!=1) & (X[['select_ivr','select_dm']].sum(axis=1) >= 1), 'JourneyLevel'] = 'Medium'
        # if the member does not meet either High nor Medium standard, then Low journey
        X.loc[(X['procall_open']!=1) & (X[['select_ivr','select_dm']].sum(axis=1) < 1), 'JourneyLevel'] = 'Low'
        #return X
        return X