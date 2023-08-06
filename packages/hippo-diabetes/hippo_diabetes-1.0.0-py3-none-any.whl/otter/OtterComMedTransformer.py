#imports
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

class OtterComMedTransformer(BaseEstimator, TransformerMixin):
    """Custom Transformer that extracts columns passed as argument to its constructor
    Parameters:
    :param careGapName: name of general column with care gap information in 0,1,2 notation
    :type comMcareGapNameedCol: string
    :param comMedOutcome: indicator of what type of information we are seeking (both=both,commericla only=c,medicare only =m)
    :type comMedOutcome:string
    :param comMedCol: name of column with the commerical, medicare, or other insurance
    :type comMedCol: string
    Retruns:
    :returns: dataframe, care gap column is split into the categories of interest by the comMedIndicator
    :rtype: dataframe
    """

    def __init__(self, careGapName, comMedOutcome, comMedCol):
        """constructor method
        """
        self.careGapName = careGapName
        self.comMedOutcome = comMedOutcome
        self.comMedCol = comMedCol

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
        """apply the breakout
        Parameters
        :param X: np.array of features of interest for training
        :type X: np.array
        :param y: np.array of features of interest for testing (none in this case)
        :type Y: np.array
        Returns
        :returns: fited data frame
        :rtype: sklearn.base.BaseEstimator
        """
        # if response is neither, just leave it as the current gap
        if self.comMedOutcome == 'neither':
            return X

        # split into the columns of interest
        #develope commerical as neeed
        if self.comMedOutcome in ['com']:
            # make ineligibile if the information if in medicare
            X['com_' + self.careGapName] = [a[0] if a[1] in ['com_self','com_full','com_split'] else 0 for a in zip(X[self.careGapName], X[self.comMedCol])]

        #develope medicare as needed
        if self.comMedOutcome in ['med']:
            # make ineligibile if the information if in commerical
            X["med_" + self.careGapName] = [a[0] if a[1] in ['med_indiv','med_group'] else 0 for a in zip(X[self.careGapName], X[self.comMedCol])]

        #develop a both column as needed
        if self.comMedOutcome in ['both']:
            # make ineligibile if the information if in medicare
            X["both_"+ self.careGapName ] = X[self.careGapName]

        # drop original column
        X = X.drop([self.careGapName], axis=1)

        # return everything
        return X