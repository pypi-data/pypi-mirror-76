#imports
import pandas as pd
import numpy as np
import os
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline

#import custom packages
cwd = os.getcwd()
cwdHead = os.getcwd().split("/hippo/")[0]
os.chdir(cwdHead+ '/hippo/src2/util')
from util import UtilAPI
os.chdir(cwd)

from OtterFeatureSelector import OtterFeatureSelector
from OtterCareGapMedOptTransformer import OtterCareGapMedOptTransformer
from OtterComMedTransformer import OtterComMedTransformer
from OtterCareGapOnlyTransformer import OtterCareGapOnlyTransformer

class OtterCareGapMedOptPipeline:
    """Pipeline for med optimization gaps

    Parameters:
    :param careGapNameValue: column for name of new care gap
    :type careGapNameValue: string
    :param comMedCol: column for type of insurance indicator
    :type comMedCol: string
    :param a1cValueCol: column from dataframe of lab a1c values
    :type a1cValueCol: string
    :param a1cCriteriaValue: a1c threshold 
    :type a1cCriteriaValue: integer
    :param conditionStatusValue: indicator of any condition comorbidity to exclude/include/None 
    :type conditionStatusValue: string
    :param conditionValueCol: columns of any condition comorbidity to exclude/include/None
    :type conditionValueCol:string
    :param requiredAntiDiabeticDrugCol: columns from dataframe of prerequisite drug with pdc >=80%
    :type requiredAntiDiabeticDrugCol: string
    :param countOfAnyRequiredDrugValue: required count of other antidiabetic drug
    :type countOfAnyRequiredDrugValue: integer
    :param comMedOutcomeValue: indication we want commerical, medicare, neither (pass through) or both in the final output
    :type comMedOutcomeValue: string

    Returns:
    :returns: data frame new care gap column for each line of business specified with = int: 0 if ineligible, 1 if closed and eligible, 2 if closed and eligble
    :rtype: pd.DataFrame
    """

    def __init__(self, careGapNameValue, a1cValueCol, a1cCriteriaValue, conditionStatusValue, conditionValueCol, 
                requiredAntiDiabeticDrugCol,requiredAntiDiabeticDrugPDCCol, countOfAnyRequiredDrugValue, comMedOutcomeValue,extraDrugCol,extraDrugCountCol, drugListCol=None, drugPDCListCol=None,comMedCol=None, selectorList= None):
        """constructor method
        """
        #get model param
        modelParam = UtilAPI().modelParam

        self.careGapNameValue = careGapNameValue
        self.a1cValueCol = a1cValueCol
        if comMedCol == None:
            comMedCol = modelParam['otter_med_insurance_list']
        
        self.a1cCriteriaValue = a1cCriteriaValue
        self.comMedCol = comMedCol
        self.conditionStatusValue = conditionStatusValue
        self.conditionValueCol = conditionValueCol
        self.requiredAntiDiabeticDrugCol = requiredAntiDiabeticDrugCol
        self.requiredAntiDiabeticDrugPDCCol = requiredAntiDiabeticDrugPDCCol
        self.countOfAnyRequiredDrugValue = countOfAnyRequiredDrugValue
        self.extraDrugCol = extraDrugCol
        self.extraDrugCountCol = extraDrugCountCol
        self.comMedOutcomeValue = comMedOutcomeValue


        if drugListCol == None:
            drugListCol = ['rx_biguanides_last_12_month','rx_glp1_agonist_last_12_month', 'rx_alpha_glucosidase_inhibitor_last_12_month','rx_meglitinide_analogues_last_12_month',
                            'rx_dpp_4_inhibitors_last_12_month','rx_thiazolidinediones_last_12_month', 'rx_sulfonylureas_last_12_month','rx_insulin_last_12_month','rx_statins_last_12_month','rx_sglt2_inhibitors_last_12_month']
        self.drugListCol = drugListCol
        if drugPDCListCol ==None:
            drugPDCListCol =  ['rx_biguanides_pdc_last_12_month','rx_glp1_agonist_pdc_last_12_month', 'rx_alpha_glucosidase_inhibitor_pdc_last_12_month','rx_meglitinide_analogues_pdc_last_12_month',
                            'rx_dpp_4_inhibitors_pdc_last_12_month','rx_thiazolidinediones_pdc_last_12_month', 'rx_sulfonylureas_pdc_last_12_month','rx_statins_pdc_last_12_month', 'rx_insulin_pdc_last_12_month','rx_sglt2_inhibitors_pdc_last_12_month']
        if selectorList == None:
            selectorList = ['lab_a1c_12mo','ckd_1','ckd_2','ckd_3','ckd_4','ckd_5','ckd_unspecified','ckd_esrd','como_heart_failure','como_ascvd','como_obesity']
        self.drugPDCListCol = drugPDCListCol
        self.selectorList = selectorList

    # apply pipe function
    def addPipe(self):

        #conduct pipeline
        commericalMedOptPipeline = Pipeline(steps=[
            ('OtterFeatureSelector', OtterFeatureSelector(featureNames=self.comMedCol + self.drugListCol + self.drugPDCListCol+self.selectorList)),
            ('OtterCareGapMedOptTransformer', OtterCareGapMedOptTransformer(careGapName=self.careGapNameValue,
                                                                                  comMedCol=self.comMedCol,
                                                                                  a1cValue = self.a1cValueCol,
                                                                                  a1cCriteria = self.a1cCriteriaValue,
                                                                                  conditionStatus = self.conditionStatusValue,
                                                                                  conditionValue = self.conditionValueCol,
                                                                                  drugList = self.drugListCol,
                                                                                  requiredAntiDiabeticDrug = self.requiredAntiDiabeticDrugCol,
                                                                                  requiredAntiDiabeticDrugPDC = self.requiredAntiDiabeticDrugPDCCol,
                                                                                  countOfAnyRequiredDrug=self.countOfAnyRequiredDrugValue,
                                                                                  extraDrug = self.extraDrugCol,
                                                                                  extraDrugCount = self.extraDrugCountCol)),
            ('OtterComMedTransformer', OtterComMedTransformer(careGapName=self.careGapNameValue,
                                                               comMedCol=self.comMedCol,
                                                               comMedOutcome=self.comMedOutcomeValue,
                                                               )),
            ('OtterCareGapOnlyTransformer', OtterCareGapOnlyTransformer(careGapName=self.careGapNameValue))
        ])

        # return pipeline
        return commericalMedOptPipeline

