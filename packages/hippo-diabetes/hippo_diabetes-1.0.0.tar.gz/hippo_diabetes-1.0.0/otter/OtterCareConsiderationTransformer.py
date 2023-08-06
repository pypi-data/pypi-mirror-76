#imports
import pandas as pd
import numpy as np
import os
from sklearn.base import BaseEstimator, TransformerMixin

#get custom modulates
cwd = os.getcwd()
cwdHead = os.getcwd().split("/hippo/")[0]
os.chdir(cwdHead+ '/hippo/src2/util')
from util import UtilAPI
# os.chdir(cwdHead+ '/hippo/src2/whale')
# from test_OtterCareConsiderationTransformer import test_OtterCareConsiderationTransformer
os.chdir(cwd)


class OtterCareConsiderationTransformer(BaseEstimator, TransformerMixin):
    """Function develops the med adherence care gaps

    Parameters:
    :param careGapName: column for name of care gap
    :type careGapName: string
    :param comMed: column for type of insruance indicator
    :type comMed: string
    :param monitorEvent: column from dataframe that determines the member's compliance state of the monitor event
    :type monitorEvent: int

    Returns:
    :returns: new care gap column with = int: 0 if ineligible, 1 if closed and eligible, 2 if opened and eligble
    :rtype: pd.DataFrame
    """

    def __init__(self, careGapName, comMedCol, monitorEvent):
        """constructor method
        """
        self.comMedCol = comMedCol
        self.careGapName = careGapName
        self.monitorEvent = monitorEvent
       

    # fit function, leave untouched - sklearn needs this, but we do not
    def fit(self, X, y=None):
        """fit method for collaborating with pipeline

        Parameters
        :param X: np.array of features of interest for training
        :type X: np.array
        :param y: np.array of features of interest for testing (none in this case)
        :type Y: np.array

        Returns
        :returns: fited data frame
        :rtype: sklearn.base.BaseEstimator
        """
        return self
    # helper function (distinguishes if they have met the condition or not)
    def compliance(self, meState):
        """turns compenent columns into care gap open, closed or ineligible

        Parameters
        :param drugValue: 1,3,0 expressing if the person is on the non-compliant, compliant, inappropriate to track
        :type drugValue: integer

        Returns
        :returns: 0 if ineligible, 1 if closed and elgible, 2 and opened and elibible
        :rtype: interger
        """
        # import NVL
        NVL = UtilAPI().NVL
        
        # care engine generated state = 1 means non-compliant, gap open
        if NVL(meState, 0) == 1:
            return int(2)
        
        # care engine generated state = 3 means compliant, gap closed
        elif NVL(meState, 0) == 3:
            return int(1)
        
        # care engine generated state is Null or other value means inappropriate to track, gap ineligible
        else:
            return int(0)

    # main function
    def transform(self, X, y=None):
        """fit method for collaborating with pipeline.  Uses the drug and drug pdc information

        Parameters
        :param X: np.array of features of interest for training
        :type X: np.array
        :param y: np.array of features of interest for testing (none in this case)
        :type Y: np.array

        Returns
        :returns: dataframe of care gaps opened or closed based on compliance()
        :rtype: dataframe
        """

        # build return dataframe with the addition
        returnX =  pd.DataFrame(zip(X[self.monitorEvent],
                                    [self.compliance(s) for s in X[self.monitorEvent]]),
                            columns=[self.monitorEvent, self.careGapName])


        #add on insure med columns
        returnX[self.comMedCol] = X[self.comMedCol]
        #run unit test
#         test_OtterCareConsiderationTransformer().test_transformer(returnX)
#         open/close/ineligible collectively exhaustive
#         no missing value, only 0,1,2

        return returnX
