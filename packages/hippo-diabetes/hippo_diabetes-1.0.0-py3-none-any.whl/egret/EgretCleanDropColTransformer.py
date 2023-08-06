#imports
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

#class
class EgretCleanDropColTransformer(BaseEstimator, TransformerMixin):
    """drop column of interest

    Parameters
    :param dropCol: column to drop
    :type dropCol: string

    Returns
    :returns: dataframe without the drop col
    :rtype: pd.DataFrame
    """

    # Class Constructor
    def __init__(self, dropCol):
        """ constructor method
        """
        self.dropCol = dropCol

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
        :param X: np.array of features of interest
        :type X: np.array
        :param y: np.array of features of interest for testing (none in this case)
        :type Y: np.array

        Returns
        :returns: data frame without the dropped column
        :rtype: pd.DataFrame
        """

        #drop the column if possible
        if self.dropCol in X.columns:
            X = X.drop([self.dropCol],axis=1)
            return X
        else:
            return X