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
class test_OtterCareGapMoniterTransformer2(unittest.TestCase):
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

        #grab the nvl function
        NVL = UtilAPI().NVL

        #get the columns of interest
        colScreen = X.columns[0]
        colGap = X.columns[4]

        #make sure there are no ineligle people
        inel = X[X[colGap]==0].shape[0]
        inelError = f"Error: Monitoring Care Gap {colGap}; {str(inel)} members are considered inelgible (none should be by design)"
        self.TestCase.assertEqual(first=inel,second=0,msg=inelError)

        # make sure that all those without a screening are open (compare the number of people who should have have the gap open to the count that do
        testLine = X[[x for x in list(X.columns) if x not in [colScreen,colGap]]].sum(axis=1).fillna(0).tolist()
        openDataCnt = len([y[1] for y in zip(X[colScreen],X[colGap],testLine) if NVL(y[0],0) == 0 or y[2]==0])
        openDisplayCnt = int(X[X[colGap]==2].shape[0])
        openMessage = f"Error: Mointering Care Gap {colGap}; {np.abs(openDataCnt-openDisplayCnt)} people have gaps open and should not"
        self.TestCase.assertEqual(first=openDataCnt,second=openDisplayCnt,msg=openMessage)

        #make sure all members are accounted for
        memberCnt = X[X[colGap]==2].shape[0]+ X[X[colGap]==1].shape[0]+ X[X[colGap]==0].shape[0]
        mismatchMessage = f"Error: Mointering Care Gap {colGap}; {memberCnt-X.shape[0]} members unaccounted for"
        self.TestCase.assertEqual(first=memberCnt,second=X.shape[0],msg = mismatchMessage)



