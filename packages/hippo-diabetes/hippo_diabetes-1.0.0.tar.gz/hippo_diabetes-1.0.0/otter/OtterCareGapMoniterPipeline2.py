#imports
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline

from OtterFeatureSelector import OtterFeatureSelector
from OtterCareGapMoniterTransformer2 import OtterCareGapMoniterTransformer2
from OtterComMedTransformer import OtterComMedTransformer
from OtterCareGapOnlyTransformer import OtterCareGapOnlyTransformer

class OtterCareGapMoniterPipeline2:
    """Pipeline for Moniter gaps

    Parameters:
    :param careGapNameValue: column for name of new care gap
    :type careGapNameValue: string
    :param comMedColValue: column for type of insurance indicator
    :type comMedColValue: string
    :param screenCol: column from dataframe that determines if the person has the screening
    :type screenCol: string
    :param testListCol: column from dataframe that determines if the person has the test screening
    :type testListCol: string
    :param comMedOutcomeValue: indication we want commerical, medicare, neither (pass through) or both in the final output
    :type comMedOutcomeValue: string

    Returns:
    :returns: data frame new care gap column for each line of business specified with = int: 0 if ineligible, 1 if closed and eligible, 2 if closed and eligble
    :rtype: pd.DataFrame
    """


    def __init__(self, careGapNameValue, screenCol, testListCol, comMedOutcomeValue,comMedCol=None):
        """constructor method
        """
        if comMedCol == None:
            #unless otherwise specified, use the stantard breakdown of insulreance
            comMedCol=['insure_med_com_full','insure_med_com_self','insure_med_com_split','insure_med_med_group','insure_med_med_indiv']
        self.careGapNameValue = careGapNameValue
        self.comMedCol = comMedCol
        self.screenCol = screenCol
        self.testListCol = testListCol
        self.comMedOutcomeValue = comMedOutcomeValue

    # apply pipe function
    def addPipe(self):
        commericalMetforminAdherencePipeline = Pipeline(steps=[
            ('OtterFeatureSelector', OtterFeatureSelector(featureNames=[self.comMedCol] + [self.screenCol]+self.testListCol)),
            ('OtterCareGapMoniterTransformer2', OtterCareGapMoniterTransformer2(careGapName=self.careGapNameValue,
                                                                                  comMedCol=self.comMedCol,
                                                                                  screen=self.screenCol,
                                                                                  testList = self.testListCol)),
            ('OtterComMedTransformer', OtterComMedTransformer(careGapName=self.careGapNameValue,
                                                               comMedCol=self.comMedCol,
                                                               comMedOutcome=self.comMedOutcomeValue,
                                                               )),
            ('OtterCareGapOnlyTransformer', OtterCareGapOnlyTransformer(careGapName=self.careGapNameValue))
        ])

        # return pipeline
        return commericalMetforminAdherencePipeline
