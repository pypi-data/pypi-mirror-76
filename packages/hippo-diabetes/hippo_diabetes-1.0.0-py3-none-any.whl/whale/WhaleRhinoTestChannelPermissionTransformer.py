#imports
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
import unittest

class WhaleRhinoTestChannelPermissionTransformer(BaseEstimator, TransformerMixin):
    """permission checks of every channel
    
    1) 'select_sms' should be 0 if sms permission is off.
    2) 'select_email' should be 0 if email permission is off.
    3) 'select_ivr' should be 0 if ivr permission is off.
    4) 'select_dm' should be 0 if dm permission is off.
    5) 'select_pharmacist_cpco' should be 0 either ivr permission is off or non-cvs filler
    6) 'select_health_hub' should be 0 either ivr permission is off or not nearby Health hub
    7) 'select_care_coordinator' should be 0 if ivr permission is off
    
    :returns: dataframe as inputted no changes (else asserts error)
    :rtype: pd.DataFrame
    """

    def __init__(self, direct_comms, proactive_channels):
        """constructor method
        """
        self.TestCase = unittest.TestCase()
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
        """apply checks related to channel permissions

        :returns: dataframe
        :rtype: pd.DataFrame
        """
        #1) Every open direct comm channels should have corresponding permissions.
        for c in self.direct_comms:
            self.TestCase.assertEqual(X[(X['select_'+c]==1) & (X[c+'_permissions'] != 'Y')].shape[0], 
                                      0,
                                     "Error in Rhino: select_{} column is open without {} permission.".format(c, c))
        #2) Every open proactive channels should have phone permissions.
        for c in self.proactive_channels:
            self.TestCase.assertEqual(X[(X['select_'+c]==1) & (X['ivr_permissions'] != 'Y')].shape[0], 
                                      0,
                                     "Error in Rhino: select_{} column is open without phone(ivr) permission.".format(c))
        #3) All members with health hub available must live near health hub
        self.TestCase.assertEqual(X[(X['select_health_hub']==1) & (X['has_healthhub_access'] !=1)].shape[0], 
                                  0,
                                     "Error in Rhino: select_health_hub column is open without health hub access.")
        #4) All members with pharmacist cpco available must be CVS filler
        self.TestCase.assertEqual(X[(X['select_pharmacist_cpco']==1) & (X['is_cvs_filler'] !=1)].shape[0], 
                                  0,
                                     "Error in Rhino: select_pharmacist_cpco column is open while the member is non-cvs filler.")
        
        #return X (if there are no errors) for additional tests
        return X