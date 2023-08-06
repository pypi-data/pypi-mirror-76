# imports from general
import pandas as pd
import os
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from collections import Counter

#imports from other packages
from OtterCareGapOnlyTransformer import OtterCareGapOnlyTransformer
from OtterComMedTransformer import OtterComMedTransformer
from OtterDensePipeline import OtterDensePipeline
from OtterCareGapAllOptionColTransformer import OtterCareGapAllOptionColTransformer
from OtterColUnderpinningCareGapRemovalTransformer import OtterColUnderpinningCareGapRemovalTransformer
from OtterFeatureSelector import OtterFeatureSelector
#imports for med optimization gaps
from OtterCareGapComMedOptTransformer import OtterCareGapComMedOptTransformer
from OtterCareGapComMedOptPipeline import OtterCareGapComMedOptPipeline
from OtterCareGapComMedOptAggregatePipeline import OtterCareGapComMedOptAggregatePipeline
from OtterCareGapComMedOpt4thLineTransformer import OtterCareGapComMedOpt4thLineTransformer
from OtterCareGapComMedOpt4thLinePipeline import OtterCareGapComMedOpt4thLinePipeline
from OtterCareGapComMedOpt4thLineAggregatePipeline import OtterCareGapComMedOpt4thLineAggregatePipeline
#imports for med adherence gaps
from OtterCareGapComMedAdherenceTransformer import OtterCareGapComMedAdherenceTransformer
from OtterCareGapComMedAdherencePipeline import OtterCareGapComMedAdherencePipeline
from OtterCareGapComMedAdherenceAggregatePipeline import OtterCareGapComMedAdherenceAggregatePipeline
#imports for device care gaps
from OtterCareGapComDeviceSMBG5Transformer import OtterCareGapComDeviceSMBG5Transformer
from OtterCareGapComDeviceSMBG5Pipeline import OtterCareGapComDeviceSMBG5Pipeline
from OtterCareGapComDeviceSMBG5AggregatePipeline import OtterCareGapComDeviceSMBG5AggregatePipeline
from OtterCareGapComDeviceSMBG7Transformer import OtterCareGapComDeviceSMBG7Transformer
from OtterCareGapComDeviceSMBG7Pipeline import OtterCareGapComDeviceSMBG7Pipeline
from OtterCareGapComDeviceSMBG7AggregatePipeline import OtterCareGapComDeviceSMBG7AggregatePipeline
#imports for comorbidities
from OtterCareGapComComorbidityTransformer import OtterCareGapComComorbidityTransformer
from OtterCareGapComComorbidityPipeline import OtterCareGapComComorbidityPipeline
from OtterCareGapComComorbidityAggregatePipeline import OtterCareGapComComorbidityAggregatePipeline
#imports for Moniter gaps
from OtterCareGapComMoniterPcpTransformer import OtterCareGapComMoniterPcpTransformer
from OtterCareGapComMoniterPcpPipeline import OtterCareGapComMoniterPcpPipeline
from OtterCareGapComMoniterPcpAggregatePipeline import OtterCareGapComMoniterPcpAggregatePipeline
from OtterCareGapComMoniterLipidTransformer import OtterCareGapComMoniterLipidTransformer
from OtterCareGapComMoniterLipidPipeline import OtterCareGapComMoniterLipidPipeline
from OtterCareGapComMoniterLipidAggregatePipeline import OtterCareGapComMoniterLipidAggregatePipeline


#import from other modules
cwd = os.getcwd()
cwdHead = os.getcwd().split("/hippo/")[0]
os.chdir(cwdHead+ '/hippo/src2/egret')
from EgretCleanDummyTransformer import EgretCleanDummyTransformer
os.chdir(cwdHead+ '/hippo/src2/util')
from util import UtilAPI
os.chdir(cwd)

modelParam = UtilAPI().modelParam

class OtterComAPI:

    # init
    def __init__(self):
        """constructor class
        """

        modelParam = UtilAPI().modelParam


        self.medAdh =  modelParam['otter_care_gap_com_medAdh_bool']
        self.comorb =  modelParam['otter_care_gap_com_comorb_bool']
        self.medOpt =  modelParam['otter_care_gap_com_medOpt_bool']
        self.device =  modelParam['otter_care_gap_com_device_bool']
        self.moniter = modelParam['otter_care_gap_com_moniter_bool']



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

            X = OtterCareGapComMedAdherenceAggregatePipeline(modelParamsDict=modelParam['otter_care_gap_com_medAdh']).addPipe(X)

        if self.medOpt:
            print('Start coding med optimization care gaps')
            X = OtterCareGapComMedOptAggregatePipeline(modelParamsDict=modelParam['otter_care_gap_com_medOpt']).addPipe(X)
            X = OtterCareGapComMedOpt4thLineAggregatePipeline(modelParamsDict=modelParam['otter_care_gap_com_medOpt_4thline']).addPipe(X)
        if self.comorb:
            print('Start coding Comorbidity gaps')
            X = OtterCareGapComComorbidityAggregatePipeline(modelParamsDict=modelParam['otter_care_gap_com_comor']).addPipe(X)           

        if self.device:
            print('Start coding device care gaps')
            X = OtterCareGapComDeviceSMBG5AggregatePipeline(modelParamsDict=modelParam['otter_care_gap_com_deviceSMBG5'] ).addPipe(X)
            X = OtterCareGapComDeviceSMBG7AggregatePipeline(modelParamsDict=modelParam['otter_care_gap_com_deviceSMBG7'] ).addPipe(X)

        if self.moniter:
            print('Start coding monitering care gaps')
            X = OtterCareGapComMoniterPcpAggregatePipeline(modelParamsDict=modelParam['otter_care_gap_com_moniter_pcp']).addPipe(X)
            X = OtterCareGapComMoniterLipidAggregatePipeline(modelParamsDict=modelParam['otter_care_gap_com_moniter_lipid']).addPipe(X)


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

