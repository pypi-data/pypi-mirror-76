#imports
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

class MooseColumnMoldMarginalTransformer(BaseEstimator, TransformerMixin):
    """Function returns figures out the marginal value of closing gaps relative to the Mold marginal framework

    :returns: dataframe with all member level care gaps through marginal mold data frame (both specific and general)
    :rtype: pd.DataFrame
    """

    def __init__(self):
        """constructor method
        """
        pass

    # fit function, leave untouched - sklearn needs this, but we do not
    def fit(self, X, y=None):
        """fit method for collaborating with pipeline

        Parameters
        :param X: moose member level output
        :type X: pd.DataFrame
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


        #return X with modifications
        return X