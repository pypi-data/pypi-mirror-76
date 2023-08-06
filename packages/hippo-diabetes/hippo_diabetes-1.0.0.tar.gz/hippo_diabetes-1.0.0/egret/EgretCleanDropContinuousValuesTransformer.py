#imports
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

#class
class EgretCleanDropContinuousValuesTransformer(BaseEstimator, TransformerMixin):
    """For given inputs of a feature and the minimum and maximum acceptable range, drop members outside of that range

    Parameters
    :param col: name of column in fed dataframe that holds the continuous value we are limiting
    #type col: string
    :param lowerBound: lowest possible acceptable value for continuous value
    :type lowerBound: float
    :param upperBound: highest possible acceptable value for continuous value
    :type upperBound: float


    Returns
    :returns: dataframe with the columns of interest
    :rtype: pd.DataFrame
    """

    # Class Constructor
    def __init__(self,col,lowerBound,upperBound):
        """ constructor method
        """
        self.col = col
        self.lowerBound = lowerBound
        self.upperBound = upperBound

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

        #reduce down to the rows with the known genders
        X = X[[True if x >= self.lowerBound and x <= self.upperBound else False for x in X[self.col]]].reset_index(drop=True)
        return X