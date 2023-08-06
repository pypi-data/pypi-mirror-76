#imports
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline

class OtterCareGapOnlyTransformer(BaseEstimator, TransformerMixin):
    """Function retains only the care gap columns
    :param careGapName: column for name of care gap
    :type careGapName: string

    :returns: dataframe with only the care gaps in it
    :rtype: pd.DataFrame
    """

    def __init__(self, careGapName):
        """constructor method
        """
        self.careGapName = careGapName

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

        :returns: dataframe with only the care gaps in it
        :rtype: pd.DataFrame
        """
        returnX = X[[a for a in X.columns if self.careGapName in a]]
        
        # return only those that have the care gap columns
        return returnX
        