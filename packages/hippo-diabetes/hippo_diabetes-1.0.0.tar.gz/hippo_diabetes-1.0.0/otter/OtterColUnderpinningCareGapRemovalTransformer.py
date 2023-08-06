#imports
import pandas as pd
import numpy as np
import os
from sklearn.base import BaseEstimator, TransformerMixin

#import custom modules
#cmenagerie model imports
cwd = os.getcwd()
cwdHead = os.getcwd().split("/hippo/")[0]

#import hpackages and return to this directo
os.chdir(cwdHead+ '/hippo/src2/util')
from util import UtilAPI

#return to original directory
os.chdir(cwd)

#class
class OtterColUnderpinningCareGapRemovalTransformer(BaseEstimator, TransformerMixin):
    """Remove columns related to care gaps that undermine independence between features


    Parameters
    :param featureNames: list of columns to exclude because they underpin caregaps and undermine independence
    :type featureNames: list


    Returns
    :returns: dataframe with the columns of interest
    :rtype: pd.DataFrame
    """

    # Class Constructor
    def __init__(self, featureNames=None):
        """ constructor method
        """
        modelParam = UtilAPI().modelParam
        if featureNames is None:
            self.featureNames = modelParam['otter_col_underpinning_care_gaps']
        else:
            self.featureNames = featureNames

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

        #list of features in X
        XCol = X.columns

        #remove those that are specified
        XCol = [x for x in XCol if x not in self.featureNames]

        #return columns of interest
        return X[XCol]