import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
import unittest

class WhaleRhinoTestROIThresholdTransformer(BaseEstimator, TransformerMixin):
    """make sure only channels that meet ROI threshold are open
    
    1) There are no null 'select_channel' value.
    2) For all members with 'channel' open, is the min(CTA bundle value) >= the expected cost of success per channel
    
    :returns: dataframe as inputted no changes (else asserts error)
    :rtype: pd.DataFrame
    """

    def __init__(self, channel_dict, direct_comms, proactive_channels):
        """constructor method
        """
        self.TestCase = unittest.TestCase()
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
        """applies checks related to ROI threshold
        :returns: dataframe
        :rtype: pd.DataFrame
        """
        #Checking 'select_email','select_sms','select_dm','select_ivr','select_pharmacist_cpco','select_health_hub','select_care_coordinator'
        for c in self.direct_comms + self.proactive_channels:
            #1) There are no null value for each channel selection 
            self.TestCase.assertEqual(X['select_'+c].isnull().any(),
                                      False,
                                     "Error in Rhino: select_{} column has null values".format(c))
            #2) For all members with 'channel' open, is the min(CTA bundle value) >= the expected cost of success per channel
            min_bundle_value = X.loc[X['select_'+c] ==1, 'bundle_value'].min()
            channel_threshold = self.channel_dict[c][0]/self.channel_dict[c][1]
            self.TestCase.assertEqual(min_bundle_value >= channel_threshold,
                                      True,
                                      "Error in Rhino: For members with {} open, the minimum CTA bundle value is ${:.1f}, lower than the threshold ${:.1f} ".format(c, min_bundle_value, channel_threshold))
        
      
        #return X (if there are no errors) for additional tests
        return X
