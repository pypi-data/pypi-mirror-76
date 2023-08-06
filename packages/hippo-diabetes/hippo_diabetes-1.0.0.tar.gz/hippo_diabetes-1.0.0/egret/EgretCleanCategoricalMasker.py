#imports
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

#class
class EgretCleanCategoricalMasker(BaseEstimator, TransformerMixin):
    """Function selects the column of interest

    Parameters
    :param genderCol: name of column in fed dataframe that holds the gender information
    #type genderCol: string
    :param genderList: list of genders to include (M,F,U) acceptable options
    :type genderList: list

    Returns
    :returns: dataframe with the columns of interest
    :rtype: pd.DataFrame
    """

    # Class Constructor
    def __init__(self,col,acceptable):
        """ constructor method
        """
        self.genderCol = col
        self.genderList = acceptable

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
        X = X[[True if x in self.genderList else False for x in X[self.genderCol]]].reset_index(drop=True)

        #insure there are no nas in the column of interest (we never can handle nulls, particulary in these vital columns)
        X = X[X[self.genderCol].notna()].reset_index(drop=True)

        #return
        return X