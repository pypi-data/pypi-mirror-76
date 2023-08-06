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
os.chdir(cwdHead+ '/hippo/src2/whale')
from test_OtterCareGapMoniterTransformer2 import test_OtterCareGapMoniterTransformer2
os.chdir(cwd)

class OtterCareGapMedMoniterLipidTransformer(BaseEstimator, TransformerMixin):
    """Function develops monitering care gaps

    Parameters:
    :param careGapName: column for name of care gap
    :type careGapName: string
    :param comMedCol: column for type of insruance indicator
    :type comMedCol: string
    :param screen: column from dataframe that determines if the person has the screening in the last 12 months
    :type screen: string
    :param testList: columns from dataframe of cholesterol test in the last 12 month
    :type testList: string

    Returns:
    :returns: new care gap column with = int: 0 if ineligible, 1 if closed and eligible, 2 if opened and eligble
    :rtype: pd.DataFrame
    """

    def __init__(self, careGapName, comMedCol, screen,testList):
        """constructor method
        """
        self.careGapName = careGapName
        self.comMedCol = comMedCol
        self.screen = screen
        self.testList = testList

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
    def moniter(self, screen,testList):
        """turns compenent columns into care gap open, closed or ineligible

        Parameters
        :param screen: 0,1 expressing if the person has this screen or not
        :type screen: integer
        :param testList: 0,1 expressing if the person has the test or not
        :type testList: integer

        Returns
        :returns: 0 if ineligible, 1 if closed and elgible, 2 and opened and elibible
        :rtype: interger
        """
        # grab NVL
        NVL = UtilAPI().NVL
        # among those who don't have a screening, then open
        if np.nansum(testList) == 0:
            return int(2)
        else:
            if NVL(screen,0) == 0:
                return int(2)
            else:
                return int(1)
        

    # main function
    def transform(self, X, y=None):
        """fit method for collaborating with pipeline.  

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
        returnX =  pd.DataFrame(zip(X[self.screen],X[self.testList[0]],X[self.testList[1]],X[self.testList[2]],
                                [self.moniter(d[0],d[1]) for d in zip(X[self.screen],X[self.testList].values)]),
                            columns=[self.screen]+ self.testList+ [self.careGapName])

        #add on insure med columns
        returnX[self.comMedCol] = X[self.comMedCol]
        
        #run unit test, see if there are any problems
        #test_OtterCareGapMoniterTransformer2().test_transformer(returnX)

        return returnX
