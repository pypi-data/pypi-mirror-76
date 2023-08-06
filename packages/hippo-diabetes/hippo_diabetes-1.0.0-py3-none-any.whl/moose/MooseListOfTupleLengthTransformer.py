#imports
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

class MooseListOfTupleLengthTransformer(BaseEstimator, TransformerMixin):
    """for a column with list of tuples find the length of each set of tuples and return that information
    :param colNameOld: name of column to mutate
    :type colNameOld: string
    :param colNameNew: name of column that is created
    :type colNameNew: string

    :returns: dataframe with one additional transformed columns
    :rtype: pd.DataFrame
    """

    def __init__(self, colNameOld,colNameNew):
        """constructor method
        """
        self.colNameOld = colNameOld
        self.colNameNew = colNameNew

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
        #create new column of single input
        X[self.colNameNew] = [len(y) for y in X[self.colNameOld]]

        #return X
        return X