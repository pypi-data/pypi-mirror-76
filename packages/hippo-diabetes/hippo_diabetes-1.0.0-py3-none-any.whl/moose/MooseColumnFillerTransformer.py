#imports
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

class MooseColumnFillerTransformer(BaseEstimator, TransformerMixin):
    """Function returns a column was single response information
    :param colNameOriginal: name of column to mutate
    :type colNameOriginal: string
    :param colNameNew: name of column that is created
    :type colNameNew: string
    :param multliplcation: how much to multiple by
    :type multliplcation: float

    :returns: dataframe with one additional transformed columns
    :rtype: pd.DataFrame
    """

    def __init__(self, colNameNew,input):
        """constructor method
        """
        self.colNameNew = colNameNew
        self.input = input

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
        X[self.colNameNew] = self.input

        #return X
        return X