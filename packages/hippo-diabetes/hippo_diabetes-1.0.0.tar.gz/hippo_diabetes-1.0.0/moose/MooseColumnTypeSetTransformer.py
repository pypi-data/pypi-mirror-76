#imports
import pandas as pd
import numpy as np
import unittest
from sklearn.base import BaseEstimator, TransformerMixin

#class
class MooseColumnTypeSetTransformer(BaseEstimator, TransformerMixin):
    """ convert column from one format to another

    Parameters
    :param col: column to transform
    :type col: string
    :param typeHolder: format to transform to, in string format
    :type typeHolder: string

    Returns
    :returns: dataframe without the drop col
    :rtype: pd.DataFrame
    """

    # Class Constructor
    def __init__(self, col,typeHolder):
        """ constructor method
        """
        self.col = col
        self.typeHolder= typeHolder

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

        #transform column of interest based on the typeHolder

        #string conversion
        if self.typeHolder == 'str':
            X[self.col] = X[self.col].astype(str)

        #float conversion
        elif self.typeHolder == 'float':
            X[self.col] = X[self.col].astype(float)

        #int conversion
        elif self.typeHolder == 'int':
            X[self.col] = X[self.col].astype(int)

        #else
        else:
            unittest.TestCase().assertTrue(False,msg="""Error. Parameters read into MooseColumnTypeSetTransformer not 'str','float',or 'int'.  {0} was entered.""".format(self.typeHolder))


        #return X
        return X