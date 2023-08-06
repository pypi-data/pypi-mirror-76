#imports
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline

from OtterFeatureSelector import OtterFeatureSelector
from OtterComMedTransformer import OtterComMedTransformer
from OtterCareGapOnlyTransformer import OtterCareGapOnlyTransformer
from OtterCareGapComDeviceSMBG7Transformer import OtterCareGapComDeviceSMBG7Transformer
from OtterCareGapComDeviceSMBG7Pipeline import OtterCareGapComDeviceSMBG7Pipeline

class OtterCareGapComDeviceSMBG7AggregatePipeline:
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
            gap = OtterCareGapComDeviceSMBG7Pipeline(careGapNameValue=key,
                                                            comMedCol='insure_med',
                                                            hypoglycemicDxCol=self.modelParamsDict[key][0],
                                                            drugInsulin12Col=self.modelParamsDict[key][1],
                                                            deviceTestCol = self.modelParamsDict[key][2],
                                                            SUDx12Col = self.modelParamsDict[key][3],
                                                            a1cThreshCol = self.modelParamsDict[key][4],
                                                            comMedOutcomeValue='com').addPipe().transform(X)
        X = pd.concat([X,gap],axis = 1)
        #return
        return X 