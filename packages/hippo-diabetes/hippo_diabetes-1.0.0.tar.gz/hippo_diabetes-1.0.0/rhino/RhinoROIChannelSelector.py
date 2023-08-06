#imports
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin


class RhinoROIChannelSelector(BaseEstimator, TransformerMixin):
    """ Turn on the channel if CTA bundle value is >= (the cost per usage/ probability of success)
    
    :param channel_dict: the cost per usage of the channel and the conversion rate
    :type channel_dict: float

    :returns: dataframe with one additional transformed columns
    :rtype: pd.DataFrame
    """

    def __init__(self,channel_dict, direct_comms, proactive_channels):
        """constructor method
        """
        self.channel_dict = channel_dict
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
        # calculate ROI threshold per channel
        channel_cost_dict = {channel: cost/conversion_rate for channel, [cost,conversion_rate] in self.channel_dict.items()}
        # mark 1 (open) for ROI>=1, mark 0 (closed) for ROI <1
        for channel in self.direct_comms + self.proactive_channels:
            X["select_"+channel] = [1 if a>=channel_cost_dict[channel] else 0 for a in X['bundle_value']]

        return X