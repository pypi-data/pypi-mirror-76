#imports
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline

from OtterFeatureSelector import OtterFeatureSelector
from OtterComMedTransformer import OtterComMedTransformer
from OtterCareGapOnlyTransformer import OtterCareGapOnlyTransformer
from OtterCareGapComDeviceSMBG5Transformer import OtterCareGapComDeviceSMBG5Transformer
from OtterCareGapComDeviceSMBG5Pipeline import OtterCareGapComDeviceSMBG5Pipeline

class OtterCareGapComDeviceSMBG5AggregatePipeline:
    """Aggregate device care gaps

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
        for key in self.modelParamsDict.keys():
            #print('Start coding {}'.format(key))
            gap = OtterCareGapComDeviceSMBG5Pipeline(careGapNameValue=key,
                                                            comMedCol='insure_med',
                                                            drugInsulin12Col=self.modelParamsDict[key][0],
                                                            deviceTestCol = self.modelParamsDict[key][1],
                                                            comMedOutcomeValue='com').addPipe().transform(X)
        X = pd.concat([X,gap],axis = 1)
        #return
        return X 