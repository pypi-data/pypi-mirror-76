#imports
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline

from OtterFeatureSelector import OtterFeatureSelector
from OtterComMedTransformer import OtterComMedTransformer
from OtterCareGapOnlyTransformer import OtterCareGapOnlyTransformer
from OtterCareGapComMedOptTransformer import OtterCareGapComMedOptTransformer
from OtterCareGapComMedOptPipeline import OtterCareGapComMedOptPipeline

class OtterCareGapComMedOptAggregatePipeline:
    """Aggregate med Opt care gaps

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
        
        #iterate through keys ( keys hold the med Opt gap names)
        for key in self.modelParamsDict.keys():
            #print('Start coding {}'.format(key))
            #create med adherent gaps 
            X = pd.concat([X, OtterCareGapComMedOptPipeline(careGapNameValue=key,
                                                                    comMedCol='insure_med',
                                                                    a1cValueCol = 'lab_a1c_12mo',
                                                                    a1cCriteriaValue = self.modelParamsDict[key][0],
                                                                    includeComorbCol=self.modelParamsDict[key][1],
                                                                    excludeComorbCol = self.modelParamsDict[key][2],
                                                                    requiredAntiDiabeticDrugCol = self.modelParamsDict[key][3],
                                                                    requiredAntiDiabeticDrugPDCCol = self.modelParamsDict[key][4],
                                                                    countOfAnyRequiredDrugValue=self.modelParamsDict[key][5],
                                                                    extraDrugCol = self.modelParamsDict[key][6],
                                                                    extraDrugCountCol = self.modelParamsDict[key][7],
                                                                    comMedOutcomeValue='com').addPipe().transform(X)], axis = 1)

        #return
        return X 

