#imports
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline

from OtterFeatureSelector import OtterFeatureSelector
from OtterComMedTransformer import OtterComMedTransformer
from OtterCareGapOnlyTransformer import OtterCareGapOnlyTransformer
from OtterCareGapMedDeviceSMBG7Transformer import OtterCareGapMedDeviceSMBG7Transformer
from OtterCareGapMedDeviceSMBG7Pipeline import OtterCareGapMedDeviceSMBG7Pipeline

class OtterCareGapMedDeviceSMBG7AggregatePipeline:
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
            gap = OtterCareGapMedDeviceSMBG7Pipeline(careGapNameValue=key,
                                                            comMedCol='insure_med',
                                                            hypoglycemicDxCol=self.modelParamsDict[key][0],
                                                            drugInsulin12Col=self.modelParamsDict[key][1],
                                                            deviceTestCol = self.modelParamsDict[key][2],
                                                            SUDx12Col = self.modelParamsDict[key][3],
                                                            a1cThreshCol = self.modelParamsDict[key][4],
                                                            comMedOutcomeValue='med').addPipe().transform(X)
            X = pd.concat([X,gap],axis = 1)
        #return
        return X 