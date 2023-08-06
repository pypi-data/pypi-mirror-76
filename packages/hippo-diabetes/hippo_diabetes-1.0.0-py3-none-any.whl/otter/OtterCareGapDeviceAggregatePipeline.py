#imports
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline

from OtterFeatureSelector import OtterFeatureSelector
from OtterComMedTransformer import OtterComMedTransformer
from OtterCareGapOnlyTransformer import OtterCareGapOnlyTransformer
from OtterCareGapDeviceTransformer import OtterCareGapDeviceTransformer
from OtterCareGapDevicePipeline import OtterCareGapDevicePipeline
from OtterCareGapDeviceTransformer2 import OtterCareGapDeviceTransformer2
from OtterCareGapDevicePipeline2 import OtterCareGapDevicePipeline2
class OtterCareGapDeviceAggregatePipeline:
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
        key_1 = [k for k in self.modelParamsDict.keys()][0]
        key_2 = [k for k in self.modelParamsDict.keys()][1]
        #print('Start coding {}'.format(key_1))
        gap_cm121 = OtterCareGapDevicePipeline(careGapNameValue=key_1,
                                                        comMedCol='insure_med',
                                                        drugInsulin12Col=self.modelParamsDict[key_1][0],
                                                        deviceTestCol = self.modelParamsDict[key_1][1],
                                                        comMedOutcomeValue='neither').addPipe().transform(X)
        #print('Start coding {}'.format(key_2))
        gap_cm122 = OtterCareGapDevicePipeline2(careGapNameValue=key_2,
                                                        comMedCol='insure_med',
                                                        hypoglycemicDxCol=self.modelParamsDict[key_2][0],
                                                        drugInsulin12Col=self.modelParamsDict[key_2][1],
                                                        deviceTestCol = self.modelParamsDict[key_2][2],
                                                        SUDx12Col = self.modelParamsDict[key_2][3],
                                                        a1cThreshCol = self.modelParamsDict[key_2][4],
                                                        comMedOutcomeValue='neither').addPipe().transform(X)                     
        X = pd.concat([X,gap_cm121,gap_cm122],axis = 1)
        #return
        return X 