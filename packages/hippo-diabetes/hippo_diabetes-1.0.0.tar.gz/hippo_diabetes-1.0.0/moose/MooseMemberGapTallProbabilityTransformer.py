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

class MooseMemberGapTallProbabilityTransformer(BaseEstimator, TransformerMixin):
    """Finds the probability of closing the care gaps based on the channels that are open

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

    #helper function to get the probability based on the probabilites
    def multFunc(self,x):
        """function to multiply values in a list together and minus 1 to get toal prob (this exisits somewhere)

        Parameter:
        :param x: list of probabilites of closing the different columns
        :type x: list

        :returns
        :returns: probability of closing the gap 1+ times
        :rtype: float
        """

        #insure list
        x = x.tolist()

        #zero chance if no channels are fired
        if len(x) < 1:
            return 0

        else:

            #get the first probability to start building the outcome
            #get the remaining to multiply in later
            outcome, x = 1-x[0],x[1:]

            #iterate through rest of list, removing each item iterively
            while len(x) != 0:
                outcome , x = outcome*(1-x[0]),x[1:]

            #return inverse outcome - probability of any closure
            return 1.0 - outcome

    #apply the transformation function
    def transform(self, X, y=None):

        #initiate the dictionary
        modelParam = UtilAPI().modelParam

        #get the channel columns used (in boolean true False)
        channelColName = [col for col in X.columns if col not in ['individual_id','care_gap','value','rank']]
        channel = np.array(X[channelColName].replace(0, False).replace(1,True))

        #probability
        #get arrays of the probabilites by channel
        probHolder = np.array([modelParam['moose_heterogeneity_channel_dict'][x][1] for x in channelColName])
        probArray = np.tile(probHolder[np.newaxis,:],(channel.shape[0],1))

        #boolean mask out the values where channel was not used and assign in
        X['total_close_prob'] = [self.multFunc(probArray[i][channel[i]]) for i in range(channel.shape[0])]

        #cost
        #get arrays of the costs by channel
        costHolder = np.array([modelParam['moose_heterogeneity_channel_dict'][x][0]  for x in channelColName])
        costArray = np.tile(costHolder[np.newaxis,:],(channel.shape[0],1))

        #boolean mask out the values where channel was not used and assign in
        X['total_cost'] = [np.sum(costArray[i][channel[i]]) for i in range(channel.shape[0])]

        #expected values
        X['total_estimated_value'] = X['value'] * X['total_close_prob']

        #return the member gap level information
        return X