#imports
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

#class
class OtterCareGapAllOptionColTransformer(BaseEstimator, TransformerMixin):
    """For all care gaps insure that there are 0, 1, and 2 columns present.  Add zerod out columns as needed

    Parameters
    :param careGapStrIndicator: string if present in a care gap we can determine it to be a care gap
    :type careGapStrIndicator: string

    Returns
    :returns: dataframe with the columns of interest
    :rtype: pd.DataFrame
    """

    # Class Constructor
    def __init__(self, careGapStrIndicator='care_gap'):
        """ constructor method
        """
        self.careGapStrIndicator = careGapStrIndicator

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
        #identify cols of interest
        careGapCol = sorted(list(set([x[:-2] for x in X.columns if self.careGapStrIndicator in x])))

        # make sure we iterate through all known care gaps
        for col in careGapCol:

            #iterate through all known permutations
            for suffix in ["_0","_1","_2"]:

                #check if the columns
                if col+suffix not in X.columns:

                    #if not in the columns create an empty columns
                    X[col+suffix] = 0

        #return data frame with new columns
        return X