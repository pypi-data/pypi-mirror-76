import os
import pandas as pd
import numpy as np
import unittest

cwd = os.getcwd()
cwdHead = os.getcwd().split("/hippo/")[0]
os.chdir(cwdHead+ '/hippo/src2/util')
from util import UtilAPI
os.chdir(cwd)

#class
class test_OtterCareGapComorbidityTransformer(unittest.TestCase):
    """  tests if test_OtterCareGapComorbidityTransformer is properly behaving, otherwise fails.
    Return, but if it fails it gives a detailed message
    No Parameters or Returns
    """
    pass

    def __init__(self):
        """constructor
        """
        self.TestCase = unittest.TestCase()
        pass

    def test_transformer(self,X):
        """ test transformer function of  OtterCareGapMedAdherenceTransformer
        Parameters
        :param X: dataframe of data (column 1 is 1/0 if the person is on the drug of interest, and second col is drug pdc for that drug, 3 is the care gap (0,1,2))
        :type X: pd.DataFrame
        """
        # #get the columns of interext
        # XComoCal = X.columns[0]
        # XGapCol = X.columns[1]
        #
        # #checks if the number of people with the care gap open meet expectations (walk back out the +1)
        # delta = sum([x[1]-x[0]-1 for x in zip(X[XComoCal],X[XGapCol])])
        # comoError = f"Error: Comorbidity Care Gap {XGapCol}; {str(np.abs(delta))} members do not have the gap properly expressed"
        # self.TestCase.assertEqual(first=delta,second=0,msg=comoError)
        #
        # #make sure there are no ineligle people
        # inel = X[X[XGapCol]==0].shape[0]
        # inelError = f"Error: Comorbidity Care Gap {XGapCol}; {str(inel)} members are considered inelgible (none should be by design)"
        # self.TestCase.assertEqual(first=inel,second=0,msg=inelError)

        pass