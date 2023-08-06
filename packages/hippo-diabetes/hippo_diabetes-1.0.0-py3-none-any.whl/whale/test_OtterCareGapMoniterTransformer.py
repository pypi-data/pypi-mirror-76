import os
import pandas as pd
import numpy as np
import unittest

#custome modules
cwd = os.getcwd()
cwdHead = os.getcwd().split("/hippo/")[0]
os.chdir(cwdHead+ '/hippo/src2/util')
from util import UtilAPI
os.chdir(cwd)

#class
class test_OtterCareGapMoniterTransformer(unittest.TestCase):
    """ testing the OtterCareGapMedAdhernceTransformer
     No Return, but if it fails it gives a detailed message

    No Parameters or Returns
    """
    pass

    def __init__(self):
        """constructor
        """
        self.TestCase = unittest.TestCase()
        pass

    def test_transformer(self,X):
        """ test transformer function of OtterCareGapMoniterTransformer
        Parameters
        :param X: dataframe of data (column 1 is 1/0 if the person is on the drug of interest, and second col is drug pdc for that drug, 3 is the care gap (0,1,2))
        :type X: pd.DataFrame
        """
        pass

        #get the columns of interest
        colScreen = X.columns[0]
        colGap = X.columns[1]

        #make sure there are no ineligle people
        inel = X[X[colGap]==0].shape[0]
        inelError = f"Error: Monitoring Care Gap {colGap}; {str(inel)} members are considered inelgible (none should be by design)"
        self.TestCase.assertEqual(first=inel,second=0,msg=inelError)

        #there should be the sme number of people with the care gap open as those who have not gotten checked
        screenZero = X[X[colScreen]==0].shape[0]
        gapZero = X[X[colGap]==2].shape[0]
        difZero = np.abs(screenZero-gapZero)
        zeroMessage = f"Error: Monitoring Care Gap {colGap}; {str(difZero)} members who had gap open but had screenings"
        self.TestCase.assertEqual(first=inel,second=0,msg=zeroMessage)

        #there should be the same number of people with the care gap open as those who have not gotten checked
        screenNonZero = X[X[colScreen]==1].shape[0]
        gapNonZero = X[X[colGap]==1].shape[0]
        difNonZero = np.abs(screenNonZero-gapNonZero)
        nonZeroMessage = f"Error: Monitoring Care Gap {colGap}; {str(difNonZero)} members who had gap closed but did not have screenings"
        self.TestCase.assertEqual(first=difNonZero,second=0,msg=nonZeroMessage)

        #all members should be accounted for
        totalGapCount = screenZero+screenNonZero
        completeMessage = f"Error: Monitoring Care Gap {colGap}; {str(totalGapCount-X.shape[0])} members unaccounted for"
        self.TestCase.assertEqual(first=totalGapCount,second=X.shape[0],msg=completeMessage)


