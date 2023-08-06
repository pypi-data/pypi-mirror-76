#imports
import pandas as pd
import numpy as np
import os
from sklearn.base import BaseEstimator, TransformerMixin
#custome modules
cwd = os.getcwd()
cwdHead = os.getcwd().split("/hippo/")[0]
os.chdir(cwdHead+ '/hippo/src2/util')
from util import UtilAPI
# os.chdir(cwdHead+ '/hippo/src2/whale')
# from test_OtterCareGapMoniterTransformer import test_OtterCareGapMoniterTransformer
os.chdir(cwd)

#custome modules
cwd = os.getcwd()
cwdHead = os.getcwd().split("/hippo/")[0]
os.chdir(cwdHead+ '/hippo/src2/util')
from util import UtilAPI
os.chdir(cwdHead+ '/hippo/src2/whale')
from test_OtterCareGapMoniterTransformer import test_OtterCareGapMoniterTransformer
os.chdir(cwd)

class OtterCareGapMoniterTransformer(BaseEstimator, TransformerMixin):
    """Function develops monitering care gaps

    Parameters:
    :param careGapName: column for name of care gap
    :type careGapName: string
    :param screen: column from dataframe that determines if the person has the screening in the last 12 months
    :type screen: string

    Returns:
    :returns: new care gap column with = int: 0 if ineligible, 1 if closed and eligible, 2 if opened and eligble
    :rtype: pd.DataFrame
    """

    def __init__(self, careGapName, comMedCol, screen):
        """constructor method
        """
        self.careGapName = careGapName
        self.comMedCol = comMedCol
        self.screen = screen

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
    def moniter(self, screen):
        """turns compenent columns into care gap open, closed or ineligible
        Parameters
        :param screen: 0,1 expressing if the person has this screening
        :type drugValue: integer
        Returns
        :returns: 0 if ineligible, 1 if closed and elgible, 2 and opened and elibible
        :rtype: interger
        """

        #pull in NVL function
        NVL = UtilAPI().NVL

        # among those who don't have a screening, then open
        if NVL(screen, 0) == 0:
            return int(2)
        # among those who have a screening, then close
        elif NVL(screen,0) == 1:
            return int(1)
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
        returnX =  pd.DataFrame(zip(X[self.screen],
                                [self.moniter(d) for d in X[self.screen]]),

                            columns=[self.screen, self.careGapName])

        #add on insure med columns
        returnX[self.comMedCol] = X[self.comMedCol]

        #run unit test
#         test_OtterCareGapMoniterTransformer().test_transformer(returnX)

        return returnX
