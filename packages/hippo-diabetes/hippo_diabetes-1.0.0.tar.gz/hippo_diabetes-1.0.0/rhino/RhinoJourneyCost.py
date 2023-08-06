#imports
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin


class RhinoJourneyCost(BaseEstimator, TransformerMixin):
    """sum the cost of all the available channels for the member
    :param channel_dict: the cost per usage of the channel and the conversion rate
    :type channel_dict: float
    :param direct_comms: name of direct communication channels
    :type direct_comms: list of strings

    :returns: dataframe with one additional transformed columns
    :rtype: pd.DataFrame
    """

    def __init__(self, channel_dict, direct_comms):
        """constructor method
        """
        self.channel_dict = channel_dict
        self.direct_comms = direct_comms
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

    def calculateJourneyCost(self, *select_channels):
        """calculating cost of journey assuming 1 outreach per channel
        param select_channels: first several elements indicates the availability(1/0) of direct comms and the chosen proactive channel, the last element is the chosen proactive channel name
        type select_channels: list
        """
        
        # cost of each channel x open or not indicator
        return sum([self.channel_dict[a][0]*b for a, b in zip(self.direct_comms + [select_channels[-1]], select_channels[:-1])])
        
        
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
        # calculate cost per journey of each member's CTA 
        X['JourneyCost'] = X[['select_'+d for d in self.direct_comms] + ['procall_open','proactive_call']].apply(lambda x : self.calculateJourneyCost(*x), axis = 1)
       
        #return X
        return X