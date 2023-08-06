#imports
import pandas as pd
import numpy as np
import os
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline

#import custom modules
from MooseMemberGapTallTransformer import MooseMemberGapTallTransformer
from MooseMemberGapTallChannelTransformer import MooseMemberGapTallChannelTransformer
from MooseMemberGapTallProbabilityTransformer import MooseMemberGapTallProbabilityTransformer

#cmenagerie model imports
cwd = os.getcwd()
cwdHead = os.getcwd().split("/hippo/")[0]

#import hpackages and return to this directo
os.chdir(cwdHead+ '/hippo/src2/util')
from util import UtilAPI

#return to original directory
os.chdir(cwd)

#class
class MooseMemberGapLevelPipeline(BaseEstimator, TransformerMixin):
    """Get the output organized to build the heterogenity report

    Parameters

    Returns
    :returns: dataframe reorganized to get information reqested for the above specifications
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
        MemberGapLevelPipeline = Pipeline(steps=[
            ('MooseMemberGapTallTransformer',MooseMemberGapTallTransformer()),
            ('MooseMemberGapTallChannelTransformer',MooseMemberGapTallChannelTransformer()),
            ('MooseMemberGapTallProbabilityTransformer',MooseMemberGapTallProbabilityTransformer())

        ])

        # return pipeline
        return MemberGapLevelPipeline