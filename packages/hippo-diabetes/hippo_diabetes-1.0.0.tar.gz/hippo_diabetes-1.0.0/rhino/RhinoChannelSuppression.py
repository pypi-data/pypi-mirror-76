#imports
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin


class RhinoChannelSuppression(BaseEstimator, TransformerMixin):
    """Suppress IVR and Care Coordinators if engaged/targed in specific programs
    :param no_IVR_CC_prgms: indicator column names of all programs to avoid overlap usage of both IVR and Care Coordinator
    :type no_IVR_CC_prgms: list of strings
    :param no_CC_prgms: indicator column names of all programs to avoid overlap usage of only Care Coordinator
    :type no_CC_prgms: list of strings


    :returns: dataframe with one additional transformed columns
    :rtype: pd.DataFrame
    """

    def __init__(self,no_IVR_CC_prgms, no_CC_prgms):
        """constructor method
        """
        self.no_IVR_CC_prgms = no_IVR_CC_prgms
        self.no_CC_prgms = no_CC_prgms
       

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
        # suppress ivr and care coordinator
        X.loc[X[self.no_IVR_CC_prgms].sum(axis=1)>=1,['select_ivr', 'select_care_coordinator']] = 0
        # suppress care coordinator
        X.loc[X[self.no_CC_prgms].sum(axis=1)>=1,'select_care_coordinator'] = 0
        #return X
        return X