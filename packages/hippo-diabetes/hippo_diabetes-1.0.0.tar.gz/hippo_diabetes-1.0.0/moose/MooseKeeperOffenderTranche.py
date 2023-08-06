#imports
import pandas as pd
import numpy as np
import os
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline

#import packages from this modula
from MooseKeeperOffenderPipeline import *

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

#class
class MooseKeeperOffenderTranche(BaseEstimator, TransformerMixin):
    """splits data into two data frames; keepers to continue on to be the member level output and the offenders who are going to be excluded

    Parameters

    Returns
    :returns: keepers data frame (hippo X egret to be turned into member level output), offenders data frame of those who are going to be excluded
    :rtype: pd.DataFrame, pd.DataFrame
    """

    def __init__(self):
        """constructor method
        """
        pass

    # apply split function
    def tranche(self,X):

        #init dict
        modelParam = UtilAPI().modelParam

        #add keeper and offender columns
        X = MooseKeeperOffenderPipeline().add_pipe().transform(X)

        #for those who have any of the offenders columns open put to the side
        keepOffColumn = [x for x in X.columns if 'keepoff_' in x]
        boolMaskList = X[[x for x in keepOffColumn]].any(axis=1)

        #find offenders
        offender = X[boolMaskList].reset_index(drop=True)

        #for those who are kept reassign back to X sans the keep drop columns
        X = X[~boolMaskList]

        #get the member level output
        X = X.drop(keepOffColumn,axis=1).reset_index(drop=True)

        #return
        return X, offender
