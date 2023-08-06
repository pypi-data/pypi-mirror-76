#imports
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline

from OtterFeatureSelector import OtterFeatureSelector
from OtterCareGapDeviceTransformer2 import OtterCareGapDeviceTransformer2
from OtterComMedTransformer import OtterComMedTransformer
from OtterCareGapOnlyTransformer import OtterCareGapOnlyTransformer

class OtterCareGapDevicePipeline2:
    """Pipeline for device care gaps

    Parameters:
    :param careGapNameValue: column for name of new care gap
    :type careGapNameValue: string
    :param comMedCol: column for type of insurance indicator
    :type comMedCol: string
    :param hypoglycemicDxCol: column from dataframe that determines if the person is on hypoglycemic event
    :type hypoglycemicDxCol: string
    :param drugInsulin12Col: column from dataframe that determines if the person is on insulin in last 12 month
    :type drugInsulin12Col: string
    :param deviceTestCol: column from dataframe that determines if the person is testing in last 6 month
    :type deviceTestCol: string
    :param SUDx12Col: columns from the dataframe of SU based on GPIs
    :type SUDx12Col: string
    :param a1cThreshCol: columns from the dataframe of lab a1c value
    :type a1cThreshCol: string
    :param comMedOutcomeValue: indication we want commerical, medicare, neither (pass through) or both in the final output
    :type comMedOutcomeValue: string

    Returns:
    :returns: data frame new care gap column for each line of business specified with = int: 0 if ineligible, 1 if closed and eligible, 2 if closed and eligble
    :rtype: pd.DataFrame
    """

    def __init__(self, careGapNameValue, hypoglycemicDxCol, drugInsulin12Col, deviceTestCol,SUDx12Col,a1cThreshCol, comMedOutcomeValue,comMedCol=None):
        """constructor method
        """
        if comMedCol == None:
            #unless otherwise specified, use the stantard breakdown of insulreance
            comMedCol=['insure_med_com_full','insure_med_com_self','insure_med_com_split','insure_med_med_group','insure_med_med_indiv']
        self.careGapNameValue = careGapNameValue
        self.comMedCol = comMedCol
        self.hypoglycemicDxCol = hypoglycemicDxCol
        self.drugInsulin12Col = drugInsulin12Col
        self.deviceTestCol = deviceTestCol
        self.SUDx12Col = SUDx12Col
        self.a1cThreshCol = a1cThreshCol
        self.comMedOutcomeValue = comMedOutcomeValue

    # apply pipe function

    def addPipe(self):
        commercialDevicePipeline = Pipeline(steps=[
            ('OtterFeatureSelector', OtterFeatureSelector(featureNames=[self.comMedCol] +
                                                          [self.hypoglycemicDxCol, self.drugInsulin12Col] +
                                                          self.deviceTestCol + [self.SUDx12Col,self.a1cThreshCol])),
            ('OtterCareGapDeviceTransformer', OtterCareGapDeviceTransformer2(careGapName=self.careGapNameValue,
                                                                            comMedCol=self.comMedCol,
                                                                            hypoglycemicDx=self.hypoglycemicDxCol,
                                                                            drugInsulin12 = self.drugInsulin12Col,
                                                                            deviceTest = self.deviceTestCol,
                                                                            SUDx12 = self.SUDx12Col,
                                                                            a1cThresh = self.a1cThreshCol)),
            ('OtterComMedTransformer', OtterComMedTransformer(careGapName=self.careGapNameValue,
                                                               comMedCol=self.comMedCol,
                                                               comMedOutcome=self.comMedOutcomeValue,
                                                               )),
            ('OtterCareGapOnlyTransformer', OtterCareGapOnlyTransformer(careGapName=self.careGapNameValue))
        ])

        # return pipeline
        return commercialDevicePipeline

 