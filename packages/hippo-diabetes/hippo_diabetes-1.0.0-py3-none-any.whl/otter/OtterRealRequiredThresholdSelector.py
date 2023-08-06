#imports
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

#class
class OtterRealRequiredThresholdSelector(BaseEstimator, TransformerMixin):
    """Function selects the column of interest

    Parameters
    :param realRequiredThreshold: for a column to be retained, this number (expressing a percentage between 0 and 100) most have none null values
    :type realRequiredThreshold: float

    Returns
    :returns: dataframe with the columns of interest
    :rtype: pd.DataFrame
    """

    # Class Constructor
    def __init__(self, realRequiredThreshold):
        """ constructor method
        """
        self.realRequiredThreshold = realRequiredThreshold

        # Return self nothing else to do here

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

    # Method that describes what we need this transformer to do
    def transform(self, X, y=None):
        """Select the columns of interest

        Parameters
        :param X: np.array of features of interest for training
        :type X: np.array
        :param y: np.array of features of interest for testing (none in this case)
        :type Y: np.array

        Returns
        :returns: data frame with the columns of interest
        :rtype: pd.DataFrame
        """

        #retain the columns with greater than or equal to the realRequiredThreshold share
        return X[[col for col in X.columns if 1-(X[col].isnull().sum()/len(X[col])) >= self.realRequiredThreshold/100.0]]