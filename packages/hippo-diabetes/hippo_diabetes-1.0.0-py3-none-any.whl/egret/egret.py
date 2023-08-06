# imports from general
import pandas as pd
import os
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline

#class based imports
from EgretCleanPassthroughTransformer import EgretCleanPassthroughTransformer
from EgretCleanDummyTransformer import EgretCleanDummyTransformer
from EgretCleanCategoricalMasker import EgretCleanCategoricalMasker
from EgretCleanDropColTransformer import EgretCleanDropColTransformer
from EgretCleanPDCNullFillerTransformer import EgretCleanPDCNullFillerTransformer
from EgretCleanBigWideFormatTransformer import EgretCleanBigWideFormatTransformer
from EgretCleanDropContinuousValuesTransformer import EgretCleanDropContinuousValuesTransformer

#cmenagerie model imports
cwd = os.getcwd()
cwdHead = os.getcwd().split("/hippo/")[0]

#import hpackages and return to this directo
os.chdir(cwdHead+ '/hippo/src2/util')
from util import UtilAPI

#return to original directory
os.chdir(cwd)


# package for cleaning and organizes data frames ( )
class EgretAPI:

    # init
    def __init__(self):
        pass

    #main
    def egret(self,X,unamedTransformer=True,genderMask=True,insureMedMask=True,dummyTransformer=True,pdcNullTransformer=True,bwTransformer=True):

        #initiate the dictionary
        modelParam = UtilAPI().modelParam

        #initiate pipeline to with passthrough (need something to inititate)
        egretPipeline = Pipeline(steps =[('passthrough',EgretCleanPassthroughTransformer())])

        #build pipeline
        #apply transformer to remove specific col
        if unamedTransformer:
            egretPipeline.steps.append(['EgretCleanDropColTransformer',EgretCleanDropColTransformer(dropCol='Unnamed: 0')])

        #apply apply insurance mask (must have an approved insurance
        if insureMedMask:
            insureMedAcceptable = ['med_indiv','med_group', 'com_self', 'com_full',  'com_split']
            egretPipeline.steps.append(['EgretCleanCategoricalMasker_insure',EgretCleanCategoricalMasker(col='insure_med',acceptable=insureMedAcceptable)])

        #apply gender (must have a gender)
        if genderMask:
            egretPipeline.steps.append(['EgretCleanCategoricalMasker_gender',EgretCleanCategoricalMasker(col='gender',acceptable=['M','F'])])

        #apply age mask
        egretPipeline.steps.append(['EgretCleanDropContinuousValuesTransformer_age',
                                         EgretCleanDropContinuousValuesTransformer(col='age',lowerBound=18,upperBound=120)])

        #convert the big wide columns to the care gap nomeclature
        if bwTransformer:
            egretPipeline.steps.append(['EgretCleanBigWideFormatTransformer',EgretCleanBigWideFormatTransformer()])

        #apply pipeline once complete
        X = egretPipeline.transform(X)

        ####
        #### data manual corrections
        ####

        #overwrite lab a1c 12 mo values with lab a1c values (Eli executive decision 4/16, in future can make better process)
        #both are now the same
        X['lab_a1c_12mo'] = X['lab_a1c']

        #extend testing to consider all diabetic supplies used to be testing
        X['rx_test_glucose_meter_ever'] = [1 if sum(x) >=2 else sum(x) for x in zip(X['rx_test_glucose_meter_ever'],X['rx_test_device_diabetes_supply_ever'])]
        X['rx_test_glucose_meter_last_3_month'] = [1 if sum(x) >=2 else sum(x) for x in zip(X['rx_test_glucose_meter_last_3_month'],X['rx_test_device_diabetes_supply_last_3_month'])]
        X['rx_test_glucose_meter_last_6_month'] = [1 if sum(x) >=2 else sum(x) for x in zip(X['rx_test_glucose_meter_last_6_month'],X['rx_test_device_diabetes_supply_last_6_month'])]
        X['rx_test_glucose_meter_last_9_month'] = [1 if sum(x) >=2 else sum(x) for x in zip(X['rx_test_glucose_meter_last_9_month'],X['rx_test_device_diabetes_supply_last_9_month'])]
        X['rx_test_glucose_meter_last_12_month'] = [1 if sum(x) >=2 else sum(x) for x in zip(X['rx_test_glucose_meter_last_12_month'],X['rx_test_device_diabetes_supply_last_12_month'])]
        X['rx_test_glucose_meter_last_18_month'] = [1 if sum(x) >=2 else sum(x) for x in zip(X['rx_test_glucose_meter_last_18_month'],X['rx_test_device_diabetes_supply_last_18_month'])]

        #isolate the PDC columns for latter usage in moose
        pdcCol = EgretCleanPDCNullFillerTransformer().transform(X[modelParam['egret_anti_diabetic_pdc_drug_columns']])
        pdcCol['individual_id'] = X['individual_id']
        self.pdc= pdcCol

        #make memory object
        self.X = X

