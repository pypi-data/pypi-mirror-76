#imports
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline

from OtterFeatureSelector import OtterFeatureSelector
from OtterComMedTransformer import OtterComMedTransformer
from OtterCareGapOnlyTransformer import OtterCareGapOnlyTransformer
from OtterCareGapMedMoniterPcpTransformer import OtterCareGapMedMoniterPcpTransformer
from OtterCareGapMedMoniterLipidTransformer import OtterCareGapMedMoniterLipidTransformer
from OtterCareGapMedMoniterPcpPipeline import OtterCareGapMedMoniterPcpPipeline
from OtterCareGapMedMoniterLipidPipeline import OtterCareGapMedMoniterLipidPipeline

class OtterCareGapMedMoniterAggregatePipeline:
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
        key_1 = [k for k in self.modelParamsDict.keys()][0]
        key_2 = [k for k in self.modelParamsDict.keys()][1]
        #print('Start coding {}'.format(key_1))
        gap_1 = OtterCareGapMoniterPipeline(careGapNameValue=key_1,
                                                        comMedCol='insure_med',
                                                        screenCol=self.modelParamsDict[key_1],
                                                        comMedOutcomeValue='neither').addPipe().transform(X)
        #print('Start coding {}'.format(key_2))
        gap_2 = OtterCareGapMoniterPipeline2(careGapNameValue=key_2,
                                                        comMedCol='insure_med',
                                                        screenCol=self.modelParamsDict[key_2][0],
                                                        testListCol=self.modelParamsDict[key_2][1],
                                                        comMedOutcomeValue='med').addPipe().transform(X)
        X = pd.concat([X,gap_1,gap_2],axis = 1)
        #return
        return X 