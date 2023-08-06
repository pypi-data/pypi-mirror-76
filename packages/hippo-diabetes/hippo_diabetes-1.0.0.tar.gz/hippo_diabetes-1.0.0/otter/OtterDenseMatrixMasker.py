#imports
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

#class
class OtterDenseMatrixMasker(BaseEstimator, TransformerMixin):
    """Function selects the column of interest

    Parameters

    Returns
    :returns: dataframe with with no nulls
    :rtype: pd.DataFrame
    """

    # Class Constructor
    def __init__(self):
        """ constructor method
        """
        pass

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
        :returns: data frame with dense matrix
        :rtype: pd.DataFrame
        """

        #drop nulls
        return X.dropna().reset_index(drop=True)