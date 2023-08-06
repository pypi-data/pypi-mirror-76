#imports
import pandas as pd
import numpy as np
import os
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline

#import packages from this modula
from MooseKeeperOffenderDuplicateTransformer import *
from MooseKeeperOffenderMutuallyExclusiveTransformer import *
from MooseKeeperOffenderDrugTypeTransformer import *
from MooseKeeperOffenderDrugCountTransformer import *

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
class MooseKeeperOffenderPipeline(BaseEstimator, TransformerMixin):
    """Identify keepers (who we are conduction analysis on, offenders (who have something wrong with them), and offender reasons (why we are excludeing membesr

    Parameters

    Returns
    :returns: pd.DataFrame with keepers and offenders included (along with reasons in the keepoff columns)
    :rtype: pd.DataFrame
    """

    def __init__(self):
        """constructor method
        """
        pass

    # apply pipe function
    def add_pipe(self):

        #init dict
        modelParam = UtilAPI().modelParam

        #create all the features of interest
        KeeperOffenderPipeline = Pipeline(steps=[
            ('MooseKeeperOffenderDuplicateTransformer',MooseKeeperOffenderDuplicateTransformer()),
            ('MooseKeeperOffenderMutuallyExclusiveTransformer',MooseKeeperOffenderMutuallyExclusiveTransformer()),
            ('MooseKeeperOffenderDrugTypeTransformer',MooseKeeperOffenderDrugTypeTransformer()),
            ('MooseKeeperOffenderDrugCountTransformer',MooseKeeperOffenderDrugCountTransformer())
        ])

        # return pipeline
        return KeeperOffenderPipeline