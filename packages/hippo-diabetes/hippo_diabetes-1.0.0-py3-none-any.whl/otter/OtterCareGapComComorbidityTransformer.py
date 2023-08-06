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
os.chdir(cwd)

class OtterCareGapComComorbidityTransformer(BaseEstimator, TransformerMixin):
    """Function develops the comorbidity care gaps
    Biguindates = GPI Codes: 231*, 232*

    Parameters:
    :param careGapName: column for name of care gap
    :type careGapName: string
    :param comMedCol: column for type of insurance indicator
    :type comMedCol: string
    :param comorbidity: column from dataframe that determines if the person has the comorbidity
    :type comorbidity: string

    Returns:
    :returns: new care gap column with = int: 0 if ineligible, 1 if closed and eligible, 2 if opened and eligble
    :rtype: pd.DataFrame
    """

    def __init__(self, careGapName, comMedCol, comorbidity):
        """constructor method
        """
        self.careGapName = careGapName
        self.comMedCol = comMedCol
        self.comorbidity = comorbidity

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
    def comorbi(self, comorbidity):
        """turns compenent columns into care gap open, closed or ineligible

        Parameters
        :param comorbidityValue: 0,1 expressing if the person have this comorbidity or not
        :type comorbidityValue: integer

        Returns
        :returns: 0 if ineligible, 1 if closed and elgible, 2 and opened and elibible
        :rtype: interger
        """
        # grab NVL
        NVL = UtilAPI().NVL

        # among those who don't have the comorbidity
        if NVL(comorbidity, 0) == 0:
            return int(1)
        # among those who have the comorbidity
        elif NVL(comorbidity, 0) == 1:
            return int(2)
        # among those who are ineligible
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
        :returns: dataframe of care gaps opened or closed based on med adhere
        :rtype: dataframe
        """
        # build return dataframe with the addition
        returnX =  pd.DataFrame(zip(X[self.comorbidity],
                                    X[self.comMedCol],
                                [self.comorbi(d) for d in X[self.comorbidity]]),
                            columns=[self.comorbidity,self.comMedCol, self.careGapName])

        return returnX


