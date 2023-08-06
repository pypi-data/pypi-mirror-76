#imports
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin


class MooseKeepNamedColumnsTransformer(BaseEstimator, TransformerMixin):
    """Function retains only the care gap columns.  If fed in more columns than those that exist will only return the subset that exists
    :param featureNames: column for name of care gap (can be more than exist)
    :type featureNames: string

    :returns: dataframe with only the care gaps in it
    :rtype: pd.DataFrame
    """

    def __init__(self, featureNames):
        """constructor method
        """
        self.featureNames = featureNames

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

        # return only those that have the columns of interest
        existingFeatureNames = [x for x in self.featureNames if x in X.columns]

        #select only the columns that exist and are specifed
        return X[existingFeatureNames]