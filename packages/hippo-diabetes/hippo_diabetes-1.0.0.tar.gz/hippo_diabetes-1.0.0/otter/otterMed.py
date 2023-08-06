# imports from general
import pandas as pd
import os
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline

#imports from other packages
from OtterCareGapOnlyTransformer import OtterCareGapOnlyTransformer
from OtterComMedTransformer import OtterComMedTransformer
from OtterDensePipeline import OtterDensePipeline
from OtterCareGapAllOptionColTransformer import OtterCareGapAllOptionColTransformer
from OtterColUnderpinningCareGapRemovalTransformer import OtterColUnderpinningCareGapRemovalTransformer
from OtterFeatureSelector import OtterFeatureSelector
# imports for med adherence gaps
from OtterCareGapMedMedAdherenceTransformer import OtterCareGapMedMedAdherenceTransformer
from OtterCareGapMedMedAdherencePipeline import OtterCareGapMedMedAdherencePipeline
from OtterCareGapMedMedAdherenceAggregatePipeline import OtterCareGapMedMedAdherenceAggregatePipeline
# imports for comorbidity gaps
from OtterCareGapMedComorbidityTransformer import OtterCareGapMedComorbidityTransformer
from OtterCareGapMedComorbidityPipeline import OtterCareGapMedComorbidityPipeline
from OtterCareGapMedComorbidityAggregatePipeline import OtterCareGapMedComorbidityAggregatePipeline
# imports for med optization gaps
from OtterCareGapMedMedOptTransformer import OtterCareGapMedMedOptTransformer
from OtterCareGapMedMedOptPipeline import OtterCareGapMedMedOptPipeline
from OtterCareGapMedMedOptAggregatePipeline import OtterCareGapMedMedOptAggregatePipeline
from OtterCareGapMedMedOpt4thLineTransformer import OtterCareGapMedMedOpt4thLineTransformer
from OtterCareGapMedMedOpt4thLinePipeline import OtterCareGapMedMedOpt4thLinePipeline
from OtterCareGapMedMedOpt4thLineAggregatePipeline import OtterCareGapMedMedOpt4thLineAggregatePipeline
# imports for device gaps
from OtterCareGapMedDeviceSMBG5Transformer import OtterCareGapMedDeviceSMBG5Transformer
from OtterCareGapMedDeviceSMBG5Pipeline import OtterCareGapMedDeviceSMBG5Pipeline
from OtterCareGapMedDeviceSMBG5AggregatePipeline import OtterCareGapMedDeviceSMBG5AggregatePipeline
from OtterCareGapMedDeviceSMBG7Transformer import OtterCareGapMedDeviceSMBG7Transformer
from OtterCareGapMedDeviceSMBG7Pipeline import OtterCareGapMedDeviceSMBG7Pipeline
from OtterCareGapMedDeviceSMBG7AggregatePipeline import OtterCareGapMedDeviceSMBG7AggregatePipeline 
from OtterCareGapMedMoniterPcpTransformer import OtterCareGapMedMoniterPcpTransformer 
from OtterCareGapMedMoniterPcpPipeline import OtterCareGapMedMoniterPcpPipeline
from OtterCareGapMedMoniterPcpAggregatePipeline import OtterCareGapMedMoniterPcpAggregatePipeline
from OtterCareGapMedMoniterLipidTransformer import OtterCareGapMedMoniterLipidTransformer
from OtterCareGapMedMoniterLipidPipeline import OtterCareGapMedMoniterLipidPipeline
from OtterCareGapMedMoniterLipidAggregatePipeline import OtterCareGapMedMoniterLipidAggregatePipeline

#import from other modules
cwd = os.getcwd()
cwdHead = os.getcwd().split("/hippo/")[0]
os.chdir(cwdHead+ '/hippo/src2/egret')
from EgretCleanDummyTransformer import EgretCleanDummyTransformer
os.chdir(cwdHead+ '/hippo/src2/util')
from util import UtilAPI
os.chdir(cwd)

modelParam = UtilAPI().modelParam

class OtterMedAPI:

    # init
    def __init__(self):
        """constructor class
        """

        modelParam = UtilAPI().modelParam
        print('AHA')


        self.medAdh =  modelParam['otter_care_gap_med_medAdh_bool']
        self.comorb =  modelParam['otter_care_gap_med_comorb_bool']
        self.medOpt =  modelParam['otter_care_gap_med_medOpt_bool']
        self.device =  modelParam['otter_care_gap_med_device_bool']
        self.moniter = modelParam['otter_care_gap_med_moniter_bool']



    # main
    def otter(self,X):

        """package for data imputtation and transformation (care gap creation)
        :param X: sparse data frame from egret
        :type X: pd.DataFrame
        :return: dense data frame for hippo with care gaps, imputted features, and no nulls
        :rtype: pd.DataFrame
        """
        #substatin
        modelParam = UtilAPI().modelParam

        ####
        #### build care gaps
        ####
        if self.medAdh:
            print('Start coding med adherence care gaps')

            X = OtterCareGapMedMedAdherenceAggregatePipeline(modelParamsDict=modelParam['otter_care_gap_med_medAdh']).addPipe(X)

        if self.medOpt:
            print('Start coding med optimization care gaps')
            X = OtterCareGapMedMedOptAggregatePipeline(modelParamsDict=modelParam['otter_care_gap_med_medOpt']).addPipe(X)
            X = OtterCareGapMedMedOpt4thLineAggregatePipeline(modelParamsDict=modelParam['otter_care_gap_med_medOpt_4thline']).addPipe(X)
        if self.comorb:
            print('Start coding Comorbidity gaps')
            X = OtterCareGapMedComorbidityAggregatePipeline(modelParamsDict=modelParam['otter_care_gap_med_comor']).addPipe(X)           

        if self.device:
            print('Start coding device care gaps')
            X = OtterCareGapMedDeviceSMBG5AggregatePipeline(modelParamsDict=modelParam['otter_care_gap_med_deviceSMBG5'] ).addPipe(X)
            X = OtterCareGapMedDeviceSMBG7AggregatePipeline(modelParamsDict=modelParam['otter_care_gap_med_deviceSMBG7'] ).addPipe(X)

        if self.moniter:
            print('Start coding monitering care gaps')
            X = OtterCareGapMedMoniterPcpAggregatePipeline(modelParamsDict=modelParam['otter_care_gap_med_moniter_pcp']).addPipe(X)
            X = OtterCareGapMedMoniterLipidAggregatePipeline(modelParamsDict=modelParam['otter_care_gap_med_moniter_lipid']).addPipe(X)


        #drop 'insure_med'
        X = X.drop(['insure_med'],axis=1)

#         #dummy the care gaps (everything with the word care gap in it will be submitted
        X = EgretCleanDummyTransformer(stringFlag=True,careGapStringMaker=True,colManualList=[x for x in X.columns if 'care_gap' in x]).transform(X)

# #         #insure that all care gaps have all options (0, 1, 2)
#         X = OtterCareGapAllOptionColTransformer().transform(X)

#         # make dense
#         X = OtterDensePipeline().add_pipe().transform(X)

#         #remove columns that are used in the medical adherence pipeline
#         X = OtterColUnderpinningCareGapRemovalTransformer().transform(X)

        #save as memory object

        self.X = X


