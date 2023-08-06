# imports from general
import pandas as pd
import os
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline

#imports from other packages
from OtterFeatureSelector import OtterFeatureSelector
from OtterComMedTransformer import OtterComMedTransformer
from OtterCareGapOnlyTransformer import OtterCareGapOnlyTransformer
from OtterCareGapMedAdherenceTransformer import OtterCareGapMedAdherenceTransformer
from OtterCareGapMedAdherencePipeline import OtterCareGapMedAdherencePipeline
from OtterCareGapMedAdherenceAggregatePipeline import OtterCareGapMedAdherenceAggregatePipeline
from OtterCareGapComorbidityTransformer import OtterCareGapComorbidityTransformer
from OtterCareGapComorbidityPipeline import OtterCareGapComorbidityPipeline
from OtterCareGapComorbidityAggregatePipeline import OtterCareGapComorbidityAggregatePipeline
from OtterCareGapMedOptTransformer import OtterCareGapMedOptTransformer
from OtterCareGapMedOptPipeline import OtterCareGapMedOptPipeline
from OtterCareGapMedOptAggregatePipeline import OtterCareGapMedOptAggregatePipeline
from OtterCareGapDeviceTransformer import OtterCareGapDeviceTransformer
from OtterCareGapDevicePipeline import OtterCareGapDevicePipeline
from OtterCareGapDeviceTransformer2 import OtterCareGapDeviceTransformer2
from OtterCareGapDevicePipeline2 import OtterCareGapDevicePipeline2
from OtterCareGapDeviceAggregatePipeline import OtterCareGapDeviceAggregatePipeline
from OtterCareGapMoniterTransformer import OtterCareGapMoniterTransformer 
from OtterCareGapMoniterPipeline import OtterCareGapMoniterPipeline
from OtterCareGapMoniterTransformer2 import OtterCareGapMoniterTransformer2
from OtterCareGapMoniterPipeline2 import OtterCareGapMoniterPipeline2
from OtterCareGapMoniterAggregatePipeline import OtterCareGapMoniterAggregatePipeline

#import from other modules
cwd = os.getcwd()
cwdHead = os.getcwd().split("/hippo/")[0]
os.chdir(cwdHead+ '/hippo/src2/egret')
from EgretCleanDummyTransformer import EgretCleanDummyTransformer
os.chdir(cwdHead+ '/hippo/src2/egret')
from util import UtilAPI
os.chdir(cwd)

modelParam = UtilAPI().modelParam

class OtterAPI:

    # init
    def __init__(self):
        pass

    # main
    def otter(self,X,medAdh=True, comorb=True, medOpt=True, device=True, moniter=True):
        if medAdh:
            print('Start coding med adherence care gaps')
            X = OtterCareGapMedAdherenceAggregatePipeline(modelParamsDict=modelParam['comMedAdherenceDict']).addPipe(X)
        # else:
        #     return X
        
        if comorb:
            print('Start coding comorbidity care gaps')
            X = OtterCareGapComorbidityAggregatePipeline(modelParamsDict=modelParam['comorbidityDict']).addPipe(X)
        # else:
        #     return X
        if medOpt:
            print('Start coding med optimization care gaps')
            X = OtterCareGapMedOptAggregatePipeline(modelParamsDict=modelParam['comMedOptDict']).addPipe(X)
        # else:
        #     return X
        if device:
            print('Start coding device care gaps')
            X = OtterCareGapDeviceAggregatePipeline(modelParamsDict=modelParam['comDeviceDict']).addPipe(X)
        
        if moniter:
            print('Start coding monitering care gaps')
            X = OtterCareGapMoniterAggregatePipeline(modelParamsDict=modelParam['comMoniterDict']).addPipe(X)

        return X
