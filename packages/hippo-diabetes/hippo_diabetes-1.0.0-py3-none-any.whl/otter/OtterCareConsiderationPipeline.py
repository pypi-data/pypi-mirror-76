#imports
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline

from OtterFeatureSelector import OtterFeatureSelector
from OtterCareConsiderationTransformer import OtterCareConsiderationTransformer
from OtterComMedTransformer import OtterComMedTransformer
from OtterCareGapOnlyTransformer import OtterCareGapOnlyTransformer

class OtterCareConsiderationPipeline:
    """Pipeline for comorbidity gaps

    Parameters:
    :param careGapNameValue: column for name of new care gap
    :type careGapNameValue: string
    :param comMedColValue: column for type of insurance indicator
    :type comMedColValue: string
    :param monitorEventCol: column from dataframe that determines member's state of a monitor event
    :type drug: string
    :param comMedOutcomeValue: indication we want commerical, medicare, neither (pass through) or both in the final output
    :type comMedOutcomeValue: string

    Returns:
    :returns: data frame new care gap column for each line of business specified with = int: 0 if ineligible, 1 if closed and eligible, 2 if closed and eligble
    :rtype: pd.DataFrame
    """

    def __init__(self, careGapNameValue, monitorEventCol, comMedOutcomeValue,comMedCol=None):
        """constructor method
        """
        if comMedCol == None:
            #unless otherwise specified, use the stantard breakdown of insulreance
            comMedCol=['insure_med_com_full','insure_med_com_self','insure_med_com_split','insure_med_med_group','insure_med_med_indiv']
        self.careGapNameValue = careGapNameValue
        self.comMedCol = comMedCol
        self.monitorEventCol = monitorEventCol
        self.comMedOutcomeValue = comMedOutcomeValue

    # apply pipe function
    def addPipe(self):
        careConsiderationPipeline = Pipeline(steps=[
            ('OtterFeatureSelector', OtterFeatureSelector(featureNames=[self.comMedCol] + [self.monitorEventCol])),
            ('OtterCareConsiderationTransformer', OtterCareConsiderationTransformer(careGapName=self.careGapNameValue,
                                                                                  comMedCol=self.comMedCol,
                                                                                  monitorEvent=self.monitorEventCol)),
            ('OtterComMedTransformer', OtterComMedTransformer(careGapName=self.careGapNameValue,
                                                               comMedCol=self.comMedCol,
                                                               comMedOutcome=self.comMedOutcomeValue,
                                                               )),
            ('OtterCareGapOnlyTransformer', OtterCareGapOnlyTransformer(careGapName=self.careGapNameValue))
        ])

        # return pipeline
        return careConsiderationPipeline