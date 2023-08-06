#imports
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

#class
class HippoRowRandomizerMasker(BaseEstimator, TransformerMixin):
    """Randomize Rows

    Parameters

    Returns
    :returns: dataframe randomly reordered
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
        :returns: data frame with randomly reorganizing rows
        :rtype: pd.DataFrame
        """
        return X.sample(frac=1).reset_index(drop=True)