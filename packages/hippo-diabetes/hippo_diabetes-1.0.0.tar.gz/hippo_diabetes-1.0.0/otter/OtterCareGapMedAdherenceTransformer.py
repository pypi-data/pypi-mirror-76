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
os.chdir(cwdHead+ '/hippo/src2/whale')
from test_OtterCareGapMedAdherenceTransformer import test_OtterCareGapMedAdherenceTransformer
os.chdir(cwd)

class OtterCareGapMedAdherenceTransformer(BaseEstimator, TransformerMixin):
    """Function develops the med adherence care gaps

    Parameters:
    :param careGapName: column for name of care gap
    :type careGapName: string
    :param comMed: column for type of insruance indicator
    :type comMed: string
    :param drug: column from dataframe that determines if the person has the drug in the last 12 months
    :type drug: string
    :param drugPDC: column from dataframe that determines the pdc for the drug in drug
    :type drugPDC: string

    Returns:
    :returns: new care gap column with = int: 0 if ineligible, 1 if closed and eligible, 2 if opened and eligble
    :rtype: pd.DataFrame
    """

    def __init__(self, careGapName, comMedCol, drug, drugPDC):
        """constructor method
        """
        self.comMedCol = comMedCol
        self.careGapName = careGapName
        self.drug = drug
        self.drugPDC = drugPDC

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
    def medAdhere(self, drugValue, drugPDCValue):
        """turns compenent columns into care gap open, closed or ineligible.
        Tweaked so we can handle edge cases where members data indicate that they have don't have the drug but they do have a pdc
        Information is not fully reconcilable as of march 13 2020

        Parameters
        :param drugValue: 0,1 expressing if the person is on the drug or not
        :type drugValue: integer
        :parm drugPDCValue: 0-1 expressing the PDC (share of time) a person is on the drug of interest
        :type drugPDCValue: float
        Returns
        :returns: 0 if ineligible, 1 if closed and elgible, 2 and opened and elibible
        :rtype: interger
        """
        #grab nvl
        NVL = UtilAPI().NVL

        # among those who are elgible
        if NVL(drugValue, 0) == 1:

            # if taking it sufficiently, then closed
            if NVL(drugPDCValue, 0) >= 0.80:
                return int(1)

            # if take it insufficiently, then opened
            elif NVL(drugPDCValue,0) < 0.80:
                return int(2)

        # among those who are not eligible
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
        returnX =  pd.DataFrame(zip(X[self.drug],
                                X[self.drugPDC],
                                [self.medAdhere(d[0], d[1]) for d in zip(X[self.drug], X[self.drugPDC])]),
                            columns=[self.drug, self.drugPDC, self.careGapName])

        #add on insure med columns
        returnX[self.comMedCol] = X[self.comMedCol]

        #run unit test
        test_OtterCareGapMedAdherenceTransformer().test_transformer(returnX)

        #if pass unit test, continue

        return returnX

