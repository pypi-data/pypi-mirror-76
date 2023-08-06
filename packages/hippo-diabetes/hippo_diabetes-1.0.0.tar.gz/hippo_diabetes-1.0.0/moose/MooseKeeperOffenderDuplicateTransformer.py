#imports
import pandas as pd
import numpy as np
import os
import unittest
from collections import Counter
from sklearn.base import BaseEstimator, TransformerMixin

#import custom modules
#cmenagerie model imports
cwd = os.getcwd()
cwdHead = os.getcwd().split("/hippo/")[0]

#import hpackages and return to this directo
os.chdir(cwdHead+ '/hippo/src2/otter')
from otter import OtterAPI
from OtterFeatureSelector import OtterFeatureSelector
os.chdir(cwdHead+ '/hippo/src2/util')
from util import UtilAPI
#return to original directory
os.chdir(cwd)

class MooseKeeperOffenderDuplicateTransformer(BaseEstimator, TransformerMixin):
    """ adds flag for duplicate members ( all except the first occurance of each member )

    :returns: dataframe with all member level and new flag if they are a duplicate
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

        #assert error if any individual ids are nulls (should never be)
        unittest.TestCase().assertFalse(X['individual_id'].isnull().values.any(), "Error in Moose, MooseKeeperOffenderDuplicateTransformer.  1+ members have null individual ids")

        #try flag duplicates and their indexes (keep the first one by eliminating it with the [1:], that will continue to represent eac person)
        indexListList = [X.index[X['individual_id']==k].values[1:] for k,v in Counter(X['individual_id']).items() if v >= 2]

        #if there are a list of lists (meaning there are members that are duplicates) then run
        if len(indexListList) > 0:
            indexList = np.concatenate(indexListList)

            #enter in the boolean mask of those that are duplicates or not
            X['keepoff_duplicate'] = np.isin(X.index,indexList)

            #return X with new column
            return X

        #otherwise there are no duplicates, return as such
        else:
            X['keepoff_duplicate'] =False
            return X
