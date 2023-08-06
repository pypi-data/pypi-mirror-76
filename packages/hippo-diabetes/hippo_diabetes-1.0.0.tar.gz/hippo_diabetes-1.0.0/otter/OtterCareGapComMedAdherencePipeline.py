#imports
import pandas as pd
import os
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
from OtterCareGapComMedAdherenceTransformer import OtterCareGapComMedAdherenceTransformer
from OtterComMedTransformer import OtterComMedTransformer
from OtterCareGapOnlyTransformer import OtterCareGapOnlyTransformer

class OtterCareGapComMedAdherencePipeline:
    """Pipeline for med adherence gaps

    Parameters:
    :param careGapNameValue: column for name of new care gap
    :type careGapNameValue: string
    :param comMedCol: column for type of insurance indicator
    :type comMedCol: string
    :param drugCol: column from dataframe that determines if the person has the drug in the last 12 months
    :type drugCol: string
    :param drugPDCCol: column from dataframe that determines the pdc for the drug in drug
    :type drugPDCCol: string
    :param comMedOutcomeValue: indication we want commerical, medicare, neither (pass through) or both in the final output
    :type comMedOutcomeValue: string

    Returns:
    :returns: data frame new care gap column for each line of business specified with = int: 0 if ineligible, 1 if closed and eligible, 2 if closed and eligble
    :rtype: pd.DataFrame
    """

    def __init__(self, careGapNameValue, drugCol, drugPDCCol, comMedOutcomeValue,comMedCol=None):
        """constructor method
        """
        #get model param
        modelParam = UtilAPI().modelParam

        self.comMedCol = 'insure_med'
        self.careGapNameValue = careGapNameValue
        self.drugCol = drugCol
        self.drugPDCCol = drugPDCCol
        self.comMedOutcomeValue = comMedOutcomeValue

    # apply pipe function

    def addPipe(self):
        commercialMedAdherencePipeline = Pipeline(steps=[
            ('OtterFeatureSelector', OtterFeatureSelector(featureNames=[self.comMedCol] + [self.drugCol, self.drugPDCCol])),
            ('OtterCareGapMedAdherenceTransformer', OtterCareGapComMedAdherenceTransformer(careGapName=self.careGapNameValue,
                                                                                  comMedCol=self.comMedCol,
                                                                                  drug=self.drugCol,
                                                                                  drugPDC=self.drugPDCCol)),
            ('OtterComMedTransformer', OtterComMedTransformer(careGapName=self.careGapNameValue,
                                                               comMedCol=self.comMedCol,
                                                               comMedOutcome=self.comMedOutcomeValue,
                                                               )),
            ('OtterCareGapOnlyTransformer', OtterCareGapOnlyTransformer(careGapName=self.careGapNameValue))
        ])

        # return pipeline
        return commercialMedAdherencePipeline

