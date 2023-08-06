#imports
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin


class MooseColumnCareGapOpenCountTransformer(BaseEstimator, TransformerMixin):
    """Gets the count of care gaps quickly
    :param colNameCompact: name of column to mutate; has the care gap compact column
    :type colNameCompact: string
    :param colNameNew: name of new columns
    :type colNameNew: string

    :returns: dataframe with one additional transformed columns
    :rtype: pd.DataFrame
    """

    def __init__(self,colNameCompact,colNameNew):
        """constructor method
        """
        self.colNameCompact = colNameCompact
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
        #create new column that has the columns of interest
        X[self.colNameNew] = [y*self.multliplcation for y in X[self.colNameCompact ]]

        #return X
        return X