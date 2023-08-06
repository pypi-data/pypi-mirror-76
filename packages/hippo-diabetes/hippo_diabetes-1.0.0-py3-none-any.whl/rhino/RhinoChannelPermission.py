#imports
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin


class RhinoChannelPermission(BaseEstimator, TransformerMixin):
    """apply channel permissions to member journey selection
    :param direct_comms: names of direct communication channels, configured in util
    :type direct_comms: list
    :param proactive_channels: names of direct proactive call channels, configured in util
    :type proactive_channels: list

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
        #apply channel permissions to disable channels without perimissions
        for channel in (self.direct_comms): 
            # ivr_permission is indeed phone permission, it's applicable to all proactive call channels and ivr
            if channel == 'ivr':
                X.loc[X[channel+'_permissions']!='Y', ['select_'+call for call in ['ivr']+self.proactive_channels]] = 0
            else:
                X.loc[X[channel+'_permissions']!='Y', 'select_'+channel] = 0
       #apply cvs filler and nearby health hub as access constraints
        X.loc[X['has_healthhub_access']!= 1, ['select_health_hub']] = 0
        X.loc[X['is_cvs_filler']!= 1, ['select_pharmacist_cpco']] = 0
       
        #return X
        return X