# imports from general
import pandas as pd
import numpy as np
import multiprocessing
import os
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline

# imports from other packages
from OtterCareGapOnlyTransformer import OtterCareGapOnlyTransformer
from OtterComMedTransformer import OtterComMedTransformer
from OtterDensePipeline import OtterDensePipeline
from OtterCareGapAllOptionColTransformer import OtterCareGapAllOptionColTransformer
from OtterColUnderpinningCareGapRemovalTransformer import OtterColUnderpinningCareGapRemovalTransformer
from OtterFeatureSelector import OtterFeatureSelector
from OtterA1cImputation import OtterA1cImputation
# imports for med optimization gaps
from OtterCareGapComMedOptTransformer import OtterCareGapComMedOptTransformer
from OtterCareGapComMedOptPipeline import OtterCareGapComMedOptPipeline
from OtterCareGapComMedOptAggregatePipeline import OtterCareGapComMedOptAggregatePipeline
from OtterCareGapComMedOpt4thLineTransformer import OtterCareGapComMedOpt4thLineTransformer
from OtterCareGapComMedOpt4thLinePipeline import OtterCareGapComMedOpt4thLinePipeline
from OtterCareGapComMedOpt4thLineAggregatePipeline import OtterCareGapComMedOpt4thLineAggregatePipeline

# imports for med adherence gaps
from OtterCareGapComMedAdherenceTransformer import OtterCareGapComMedAdherenceTransformer
from OtterCareGapComMedAdherencePipeline import OtterCareGapComMedAdherencePipeline
from OtterCareGapComMedAdherenceAggregatePipeline import OtterCareGapComMedAdherenceAggregatePipeline

# imports for device care gaps
from OtterCareGapComDeviceSMBG5Transformer import OtterCareGapComDeviceSMBG5Transformer
from OtterCareGapComDeviceSMBG5Pipeline import OtterCareGapComDeviceSMBG5Pipeline
from OtterCareGapComDeviceSMBG5AggregatePipeline import OtterCareGapComDeviceSMBG5AggregatePipeline
from OtterCareGapComDeviceSMBG7Transformer import OtterCareGapComDeviceSMBG7Transformer
from OtterCareGapComDeviceSMBG7Pipeline import OtterCareGapComDeviceSMBG7Pipeline
from OtterCareGapComDeviceSMBG7AggregatePipeline import OtterCareGapComDeviceSMBG7AggregatePipeline

# imports for comorbidities
from OtterCareGapComComorbidityTransformer import OtterCareGapComComorbidityTransformer
from OtterCareGapComComorbidityPipeline import OtterCareGapComComorbidityPipeline
from OtterCareGapComComorbidityAggregatePipeline import OtterCareGapComComorbidityAggregatePipeline

# imports for Moniter gaps
from OtterCareGapComMoniterPcpTransformer import OtterCareGapComMoniterPcpTransformer
from OtterCareGapComMoniterPcpPipeline import OtterCareGapComMoniterPcpPipeline
from OtterCareGapComMoniterPcpAggregatePipeline import OtterCareGapComMoniterPcpAggregatePipeline
from OtterCareGapComMoniterLipidTransformer import OtterCareGapComMoniterLipidTransformer
from OtterCareGapComMoniterLipidPipeline import OtterCareGapComMoniterLipidPipeline
from OtterCareGapComMoniterLipidAggregatePipeline import OtterCareGapComMoniterLipidAggregatePipeline

# imports for Care Consideration gaps
from OtterCareConsiderationTransformer import OtterCareConsiderationTransformer
from OtterCareConsiderationPipeline import OtterCareConsiderationPipeline
from OtterCareConsiderationComAggregatePipeline import OtterCareConsiderationComAggregatePipeline
from OtterCareConsiderationMedAggregatePipeline import OtterCareConsiderationMedAggregatePipeline


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

# misc
from OtterCareGapColumnConsolidater import OtterCareGapColumnConsolidater

# import from other modules
cwd = os.getcwd()
cwdHead = os.getcwd().split("/hippo/")[0]
os.chdir(cwdHead + '/hippo/src2/egret')
from EgretCleanDummyTransformer import EgretCleanDummyTransformer
os.chdir(cwdHead + '/hippo/src2/util')
from util import UtilAPI

os.chdir(cwd)

# initiate modelParam
modelParam = UtilAPI().modelParam

class OtterAPI:

    # init
    def __init__(self):
        """constructor class
        """

        modelParam = UtilAPI().modelParam

        # commercial/medicare indicator
        self.com_med = modelParam['otter_care_gap_comm_vs_medi_bool']

        # commerical
        self.com_medAdh = modelParam['otter_care_gap_com_medAdh_bool']
        self.com_comorb = modelParam['otter_care_gap_com_comorb_bool']
        self.com_medOpt = modelParam['otter_care_gap_com_medOpt_bool']
        self.com_device = modelParam['otter_care_gap_com_device_bool']
        self.com_moniter = modelParam['otter_care_gap_com_moniter_bool']
        self.com_carecon = modelParam['otter_care_gap_com_carecon_bool']

        # medicare
        self.med_medAdh = modelParam['otter_care_gap_med_medAdh_bool']
        self.med_comorb = modelParam['otter_care_gap_med_comorb_bool']
        self.med_medOpt = modelParam['otter_care_gap_med_medOpt_bool']
        self.med_device = modelParam['otter_care_gap_med_device_bool']
        self.med_moniter = modelParam['otter_care_gap_med_moniter_bool']
        self.med_carecon = modelParam['otter_care_gap_med_carecon_bool']

    # main
    def otterCareGap(self, X):
        """care gap creation

        :param X: input from egret, to create the care gaps
        :type X: pd.DataFrame

        :return: dense data frame for hippo with care gaps, imputted features, and no nulls
        :rtype: pd.DataFrame
        """
        # substatin
        modelParam = UtilAPI().modelParam

        # if not starting at the midpoint then pull all gaps
        ####
        #### build care gaps
        ####
        # substatin
        modelParam = UtilAPI().modelParam

        ####
        #### build commerical care gaps
        ####
        if self.com_med == 'comm':
            #print('Start coding commercial care gaps')
            if self.com_medAdh:
                #print('Start coding med adherence care gaps')
                X = OtterCareGapComMedAdherenceAggregatePipeline(
                    modelParamsDict=modelParam['otter_care_gap_com_medAdh']).addPipe(X)

            if self.com_medOpt:
                #print('Start coding med optimization care gaps')
                X = OtterCareGapComMedOptAggregatePipeline(
                    modelParamsDict=modelParam['otter_care_gap_com_medOpt']).addPipe(X)
                X = OtterCareGapComMedOpt4thLineAggregatePipeline(
                    modelParamsDict=modelParam['otter_care_gap_com_medOpt_4thline']).addPipe(X)

            if self.com_comorb:
                #print('Start coding Comorbidity gaps')
                X = OtterCareGapComComorbidityAggregatePipeline(
                    modelParamsDict=modelParam['otter_care_gap_com_comor']).addPipe(X)

            if self.com_device:
                #print('Start coding device care gaps')
                X = OtterCareGapComDeviceSMBG5AggregatePipeline(
                    modelParamsDict=modelParam['otter_care_gap_com_deviceSMBG5']).addPipe(X)
                X = OtterCareGapComDeviceSMBG7AggregatePipeline(
                    modelParamsDict=modelParam['otter_care_gap_com_deviceSMBG7']).addPipe(X)
           
            if self.com_moniter:
#                 print('Start coding monitering care gaps')
                X = OtterCareGapComMoniterPcpAggregatePipeline(
                    modelParamsDict=modelParam['otter_care_gap_com_moniter_pcp']).addPipe(X)
                X = OtterCareGapComMoniterLipidAggregatePipeline(
                    modelParamsDict=modelParam['otter_care_gap_com_moniter_lipid']).addPipe(X)
            
            if self.com_carecon:
#                 print('Start coding care considerations')
                X = OtterCareConsiderationComAggregatePipeline(
                    modelParamsDict=modelParam['otter_care_gap_com_carecon']).addPipe(X)
                

        ####
        #### build medicare care gaps
        ####

        elif self.com_med == 'medi':
            #print('Start coding medicare care gaps')
            if self.med_medAdh:
                #print('Start coding med adherence care gaps')
                X = OtterCareGapMedMedAdherenceAggregatePipeline(
                    modelParamsDict=modelParam['otter_care_gap_med_medAdh']).addPipe(X)

            if self.med_medOpt:
                #print('Start coding med optimization care gaps')
                X = OtterCareGapMedMedOptAggregatePipeline(
                    modelParamsDict=modelParam['otter_care_gap_med_medOpt']).addPipe(X)
                X = OtterCareGapMedMedOpt4thLineAggregatePipeline(
                    modelParamsDict=modelParam['otter_care_gap_med_medOpt_4thline']).addPipe(X)

            if self.med_comorb:
                #print('Start coding Comorbidity gaps')
                X = OtterCareGapMedComorbidityAggregatePipeline(
                    modelParamsDict=modelParam['otter_care_gap_med_comor']).addPipe(X)

            if self.med_device:
                #print('Start coding device care gaps')
                X = OtterCareGapMedDeviceSMBG5AggregatePipeline(
                    modelParamsDict=modelParam['otter_care_gap_med_deviceSMBG5']).addPipe(X)
                X = OtterCareGapMedDeviceSMBG7AggregatePipeline(
                    modelParamsDict=modelParam['otter_care_gap_med_deviceSMBG7']).addPipe(X)

            if self.med_moniter:
                #print('Start coding monitering care gaps')
                X = OtterCareGapMedMoniterPcpAggregatePipeline(
                    modelParamsDict=modelParam['otter_care_gap_med_moniter_pcp']).addPipe(X)
                X = OtterCareGapMedMoniterLipidAggregatePipeline(
                    modelParamsDict=modelParam['otter_care_gap_med_moniter_lipid']).addPipe(X)
           
            if self.med_carecon:
                #print('Start coding care considerations')
                X = OtterCareConsiderationMedAggregatePipeline(
                    modelParamsDict=modelParam['otter_care_gap_med_carecon']).addPipe(X)
            
        else:
            print('Turning off medicare/commercial')

        # consolidate
        X = OtterCareGapColumnConsolidater().transform(X)
        #save as memory object
        return X

    def otterFinalClean(self,X):
        """ cleans and organizes the data for final ingestion into hippo
        :param X: data frame with care gaps
        :type X: pd.DataFrame

        :return:
        """
        # impute the missing a1c values(using stratified imputation)
        X = OtterA1cImputation(mappingCol = ['gender','insure_med','diag_e11_ever'],imputeCol = 'lab_a1c',newImputeCol='lab_a1c_imputed').transform(X)
        # dummy the care gaps (everything with the word care gap in it will be submited
        X = EgretCleanDummyTransformer(stringFlag=True, careGapStringMaker=True,
                                       colManualList=[x for x in X.columns if 'care_gap' in x]).transform(X)

        # insure that all care gaps have all options (0, 1, 2)
        X = OtterCareGapAllOptionColTransformer().transform(X)

        # make dense
        X = OtterDensePipeline().add_pipe().transform(X)

        # remove columns that are used in the medical adherence pipeline
        X = OtterColUnderpinningCareGapRemovalTransformer().transform(X)

        #return
        return X


    def otter(self,X, columns_to_remove = ['care_gap_125', 'care_gap_122']):
        """ master function to build out care gaps and organize code for cleaning

        :param X: data frame with care gaps
        :type X: pd.DataFrame
        :return:
        """

        #parameters of cores and data
        coreN = int(np.floor(multiprocessing.cpu_count()/2))
        dfN = X.shape[0]
        splitN = int(np.floor(dfN/coreN))

        #institute pooling
        pool = multiprocessing.Pool(coreN)

        #partition functionbreak into a list of data frames for parrel processing
        XSplit = [X.iloc[i:i+splitN,:].reset_index(drop=True) for i in range(0,dfN,splitN)]

        # map with care gap multiprocessing and reduce with concat all the groups together could reduce
        X = pd.concat(pool.map(self.otterCareGap,XSplit))
        
        #do remaining preparation for ingestion into hippo (single processing)
        X = self.otterFinalClean(X)

        #close out pool
        pool.close()
        pool.join()

        ####
        #### manual edits
        ####

        #remove columns requested
        print("Removing columns matching any of the following: {}".format(columns_to_remove))
        for col in columns_to_remove:
            matches = [c for c in X.columns if col in c]
            print("Removing {} from columns".format(matches))
            X = X.drop(matches, axis=1)

        ####
        #### outputs
        ####

        #craete output as object
        self.X = X
