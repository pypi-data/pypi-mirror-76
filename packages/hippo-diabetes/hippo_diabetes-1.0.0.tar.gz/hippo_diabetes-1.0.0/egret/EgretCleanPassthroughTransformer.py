#imports
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

#class
class EgretCleanPassthroughTransformer(BaseEstimator, TransformerMixin):
    """Function transformer that does not alter the outcome(head of pipe)

    Parameters

    Returns
    :returns: dataframe with the columns of interest
    :rtype: pd.DataFrame
    """

    def __init__(self):
        ''' constructor class
        '''
        pass

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
        return X