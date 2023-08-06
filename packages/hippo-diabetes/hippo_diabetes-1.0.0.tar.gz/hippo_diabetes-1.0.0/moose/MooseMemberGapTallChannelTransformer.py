#imports
import pandas as pd
import numpy as np
import itertools
import operator
import os
from sklearn.base import BaseEstimator, TransformerMixin

#cmenagerie model imports
cwd = os.getcwd()
cwdHead = os.getcwd().split("/hippo/")[0]

#import hpackages and return to this directo
os.chdir(cwdHead+ '/hippo/src2/util')
from util import UtilAPI

#return to original directory
os.chdir(cwd)

class MooseMemberGapTallChannelTransformer(BaseEstimator, TransformerMixin):
    """Adds in the channels indicators if the care gap is attempted to be closed by that channel or not

    :returns: dataframe of all care gaps that are being closed as well as the channels being used to close them
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
        :param X: np.array of features of interest for training
        :type X: np.array
        :param y: np.array of features of interest for testing (none in this case)
        :type Y: np.array

        Returns
        :returns: fited data frame
        :rtype: sklearn.base.BaseEstimator
        """
        return self

    #apply the transformation function
    def transform(self, X, y=None):

        #initiate the dictionary
        modelParam = UtilAPI().modelParam

        #for each care gap build a dictionary of the channels that can be used to close it

        #get the list of care gaps
        cgList = list(set(X['care_gap']))

        #get a list of channels corresponding to those care gaps
        cgChannelDict = {k:modelParam['moose_heterogeneity_gap_to_action_dict'][k] for k in cgList}
        cgChannelDict = {k:list(set(x for l in [modelParam['moose_heterogeneity_action_to_channel_dict'][x] for x in v]for x in l)) for k,v in cgChannelDict.items()}

        #iterate through dictionaryies and create column for each channel
        # 1 if cost <= to the expected value of closing the channel and the channel can be used to close, else 0

        for key in modelParam['moose_heterogeneity_channel_dict'].keys():

            #always fire dgitial
            if key == 'digital' or key =='email':
                X[key] = 1
                continue

            #populate
            X[key] = [1 if key in cgChannelDict[x[0]] and x[1] >= modelParam['moose_heterogeneity_channel_dict'][key][2] else 0 for x in zip(X['care_gap'],X['value'])]

        #return the member gap level information
        return X