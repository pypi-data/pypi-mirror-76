#imports
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

class OtterCareGapLivognoTransformer(BaseEstimator, TransformerMixin):
    """Function develops the livongo

    Parameters:
    :param careGapName: column for name of care gap
    :type careGapName: string
    :param comMed: column for type of insruance indicator
    :type comMed: string
    :param drug: column from dataframe that determines if the person has the drug in the last 12 months
    :type drug: string
    :param drug_pdc: column from dataframe that determines the pdc for the drug in drug
    :type drug_pdc: string

    Returns:
    :returns: same data frame with new care gap column with = int: 0 if ineligible, 1 if closed and eligible, 2 if opened and eligble
    :rtype: pd.DataFrame
    """

    def __init__(self, careGapName, comMedCol, drug, drugPDC):
        """constructor method
        """
        self.careGapName = careGapName
        self.comMedCol = comMedCol
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

    def ineligble(self):
        pass
        #idenift the people who are zeros

    def start_a1c_(selfs):
        pass

    def model(selfs):
        pass
        #idnefitys if 1 or 2

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

        #X start
        #self.name of thing


        #XReturn the exact same as X, plus the livongo care gap column (0,1,2 notation)
        #0 these are people who have not a type 1 diagnosis, do not have insulin, and have not had a hypogylcemic episode
        #1 these are people in your model you think do not have a start a1c less that 9 or will not engage for 6 months
        #2 these are people in your model you think have a start a1c less that 9 AND will engage for 6 months

        #return
        return XReturn


OtterCareGapLivognoTransformer(careGapName=self.careGapNameValue,
                                    comMedCol=self.comMedCol,
                                    drug=self.drugCol,
                                    drugPDC=self.drugPDCCol).transform(X)