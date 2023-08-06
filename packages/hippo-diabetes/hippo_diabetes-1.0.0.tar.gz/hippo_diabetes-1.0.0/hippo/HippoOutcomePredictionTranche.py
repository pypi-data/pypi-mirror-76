#imports
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

#class
class HippoOutcomePredictionTranche(BaseEstimator, TransformerMixin):
    """Function selects the column of interest

    Parameters
    :param outcomeColName: string of outcome column of interest
    :type outcomeColName: string
    :param memberShare: percentage of members to use in the modeling process.  Between 0 and 1
    :type memberShare: float

    Returns
    :returns: dataframe with the columns of interest
    :rtype: pd.DataFrame
    """

    # Class Constructor
    def __init__(self, outcomeColName,memberShare,careGapNotOpenRemove=True):
        """ constructor method
        """
        self.outcomeColname = outcomeColName
        self.memberShare = memberShare
        self.careGapNotOpenRemove = careGapNotOpenRemove

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
        :returns Xmain: data frame for training (data)
        :rtype: pd.DataFrame
        :returns Ymain: datafarme column for training (target)
        :rtype: pd.Series
        ;returns Xmisc: dataframe of features excluded from analysis (care gaps of 0 and 1)
        :rtype: pd.DataFrame
        """

        #as needed, work with only a parition of the data
        #for running the dataset, for running part of the dataset lower memberShare
        if self.memberShare != 1.0:
            booleanMasker = [True if np.random.uniform(0.0,1.0) >= self.memberShare else False for x in range(0,X.shape[0])]
            X = X[booleanMasker]

        #identify and split out the columns of interest
        YMain = X[self.outcomeColname]
        XMain = X.drop(self.outcomeColname,axis=1)

        #remove the overall dataframe to prevent confusion
        del X

        #if we are removing care gaps that are inelgible or closed and elgible from the modeling process (obfuscate results
        if self.careGapNotOpenRemove:

            #columns of interest
            careGapNotOpenList = [y for y in [x for x in XMain.columns if 'care_gap' in x] if y[-1:]!='2']

            #retain
            XMisc = XMain[careGapNotOpenList]

            #drop
            XMain = XMain.drop(careGapNotOpenList,axis=1)

        return XMain, YMain, XMisc