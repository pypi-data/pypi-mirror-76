#imports
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline

from OtterFeatureSelector import OtterFeatureSelector
from OtterComMedTransformer import OtterComMedTransformer
from OtterCareGapOnlyTransformer import OtterCareGapOnlyTransformer
from OtterCareGapMedComorbidityTransformer import OtterCareGapMedComorbidityTransformer
from OtterCareGapMedComorbidityPipeline import OtterCareGapMedComorbidityPipeline

class OtterCareGapMedComorbidityAggregatePipeline:
    """Aggregate comorbidity care gaps

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
        
        #iterate through keys ( keys hold the med adherence gap names)
        for key in self.modelParamsDict.keys():
            #print('Start coding {}'.format(key))
            #create med adherent gaps 
            X = pd.concat([X, OtterCareGapMedComorbidityPipeline(careGapNameValue=key,
                                                                    comMedCol='insure_med',
                                                                    comorbidityCol=self.modelParamsDict[key],
                                                                    comMedOutcomeValue='med').addPipe().transform(X)], axis = 1)
  
        #return
        return X 
