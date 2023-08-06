#imports
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline

from OtterFeatureSelector import OtterFeatureSelector
from OtterCareGapMedDeviceSMBG5Transformer import OtterCareGapMedDeviceSMBG5Transformer
from OtterComMedTransformer import OtterComMedTransformer
from OtterCareGapOnlyTransformer import OtterCareGapOnlyTransformer


class OtterCareGapMedDeviceSMBG5Pipeline:
    """Pipeline for device care gaps

    Parameters:
    :param careGapNameValue: column for name of new care gap
    :type careGapNameValue: string
    :param comMedCol: column for type of insurance indicator
    :type comMedCol: string
    :param drugInsulin12Col: column from dataframe that determines if the person is on insulin in last 12 month
    :type drugInsulin12Col: string
    :param deviceTestCol: column from dataframe that determines if the person is testing in last 6 month
    :type deviceTestCol: string
    :param comMedOutcomeValue: indication we want commerical, medicare, neither (pass through) or both in the final output
    :type comMedOutcomeValue: string

    Returns:
    :returns: data frame new care gap column for each line of business specified with = int: 0 if ineligible, 1 if closed and eligible, 2 if closed and eligble
    :rtype: pd.DataFrame
    """

    def __init__(self, careGapNameValue, drugInsulin12Col, deviceTestCol, comMedOutcomeValue,comMedCol=None):
        """constructor method
        """
        if comMedCol == None:
            #unless otherwise specified, use the stantard breakdown of insulreance
            comMedCol=['insure_med_com_full','insure_med_com_self','insure_med_com_split','insure_med_med_group','insure_med_med_indiv']
        self.careGapNameValue = careGapNameValue
        self.comMedCol = comMedCol
        self.drugInsulin12Col = drugInsulin12Col
        self.deviceTestCol = deviceTestCol
        self.comMedOutcomeValue = comMedOutcomeValue

    # apply pipe function

    def addPipe(self):
        commercialDevicePipeline = Pipeline(steps=[
            ('OtterFeatureSelector', OtterFeatureSelector(featureNames=[self.comMedCol] +
                                                          [self.drugInsulin12Col] +
                                                          self.deviceTestCol)),
            ('OtterCareGapMedDeviceSMBG5Transformer', OtterCareGapMedDeviceSMBG5Transformer(careGapName=self.careGapNameValue,
                                                                                  comMedCol=self.comMedCol,
                                                                                  drugInsulin12 = self.drugInsulin12Col,
                                                                                  deviceTest = self.deviceTestCol)),
            ('OtterComMedTransformer', OtterComMedTransformer(careGapName=self.careGapNameValue,
                                                               comMedCol=self.comMedCol,
                                                               comMedOutcome=self.comMedOutcomeValue,
                                                               )),
            ('OtterCareGapOnlyTransformer', OtterCareGapOnlyTransformer(careGapName=self.careGapNameValue))
        ])

        # return pipeline
        return commercialDevicePipeline

 