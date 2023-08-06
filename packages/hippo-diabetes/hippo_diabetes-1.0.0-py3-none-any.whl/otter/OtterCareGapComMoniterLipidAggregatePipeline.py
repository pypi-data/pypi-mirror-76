#imports
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
import unittest

from OtterFeatureSelector import OtterFeatureSelector
from OtterComMedTransformer import OtterComMedTransformer
from OtterCareGapOnlyTransformer import OtterCareGapOnlyTransformer
from OtterCareGapComMoniterLipidTransformer import OtterCareGapComMoniterLipidTransformer
from OtterCareGapComMoniterLipidPipeline import OtterCareGapComMoniterLipidPipeline

class OtterCareGapComMoniterLipidAggregatePipeline:
    """Aggregate monitering care gaps

    Parameters:
    :param modelParamsDict: dictionary for the care gap model parameters
    :type modelParamsDict: dictionary

    Returns:
    :returns: data frame new care gap column for each line of business specified with = int: 0 if ineligible, 1 if closed and eligible, 2 if closed and eligble
    :rtype: pd.DataFrame
    """

    def __init__(self, modelParamsDict):
        """constructor method
        """
        self.modelParamsDict = modelParamsDict

    
    # Apply aggregate function
    def addPipe(self,X):
        # iterate through care gaps
        for key in self.modelParamsDict.keys():   
            #print('Start coding {}'.format(key))
            gap = OtterCareGapComMoniterLipidPipeline(careGapNameValue=key,
                                                            comMedCol='insure_med',
                                                            screenCol=self.modelParamsDict[key][0],
                                                            testListCol=self.modelParamsDict[key][1],
                                                            comMedOutcomeValue='com').addPipe().transform(X)
            X = pd.concat([X,gap],axis = 1)
        #return
        return X 