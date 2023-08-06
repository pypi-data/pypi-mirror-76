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
class test_OtterCareConsiderationTransformer(unittest.TestCase):
    """  tests if OtterCareConsiderationTransformer is properly behaving, otherwise fails.
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
        """ test transformer function of  OtterCareConsiderationTransformer
        Parameters
        :param X: dataframe of data (column 1 is 0/3/1 describing member compliance state on the monitor event, and second col is the care gap (0,1,2))
        :type X: pd.DataFrame
        """
        #get the columns of interext
        MonitorEvent = X.columns[0]
        GapCol = X.columns[1]
        
        meDict = X[MonitorEvent].value_counts()
        gapDict = X[GapCol].value_counts()
       
        # check if # of open cases equates # of non-compliance
        delta_open = meDict[1] - gapDict[2]
        openError = f"Error: Care Consideration {GapCol}; {str(np.abs(delta_open))} members do not have the open gap properly expressed"
        self.TestCase.assertEqual(first=delta_open, second=0,msg=openError)
        
        # check if # of close cases equates # of compliance
        delta_close = meDict[3]-gapDict[1]
        closeError = f"Error: Care Consideration {GapCol}; {str(np.abs(delta_close))} members do not have the close gap properly expressed"
        self.TestCase.assertEqual(first=delta_close, second=0,msg=openError)
        
        # check if sum of 0,1,2 cases equates number of  
        delta_ineligible = meDict.sum() - (gapDict[2]+gapDict[1]+gapDict[0])
        ineliError = f"Error: Care Consideration {GapCol}; {str(np.abs(delta_ineligible))} members do not have the ineligible gap properly expressed"
        self.TestCase.assertEqual(first=delta_ineligible,second=0,msg=ineliError)
        
        
        

        pass