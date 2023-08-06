import os
import pandas as pd
import unittest

#custome modules
cwd = os.getcwd()
cwdHead = os.getcwd().split("/hippo/")[0]
os.chdir(cwdHead+ '/hippo/src2/util')
from util import UtilAPI
os.chdir(cwd)

#class
class test_OtterCareGapMedAdherenceTransformer(unittest.TestCase):
    """  tests if OtterCareGapMedAdherenceTransformer is properly behaving, otherwise fails.
    No Return, but if it fails it gives a detailed message

    No Parameters or Returns
    """
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
        pass

        #grab nvl function
        NVL = UtilAPI().NVL

        #care gap column
        XDrugColumn = X.columns[0]
        XPDCColumn = X.columns[1]
        XCGColumn = X.columns[2]

        #groups of people to conduct checks upon
        XInel = X[X[XCGColumn]==0]
        XClose = X[X[XCGColumn]==1]
        XOpen = X[X[XCGColumn]==2]

        ####
        #### open
        ####
        #count of members with too low PDC
        openPDCMsgCount = sum([1 if x >= 0.8 else 0 for x in XOpen[XPDCColumn].tolist()])
        openPDCMsgError = f"Error: Med Adherence for {XCGColumn}; {str(openPDCMsgCount)} opem members with greater than 80% PDC"
        self.TestCase.assertEqual(first=openPDCMsgCount,second=0,msg=openPDCMsgError)

        #count of members not on the drug when they should be
        #also include members nominally not on the drug, but they have pdc indicating they are
        openDrugMsgCount = sum([0 if x[0] == 1 or (x[1] >= 0) else 1 for x in zip(XOpen[XDrugColumn],XOpen[XCGColumn])])
        openDrugMsgError = f"Error: Med Adherence for {XCGColumn}; {str(openDrugMsgCount)} members not on drug and PDC gap open"
        self.TestCase.assertEqual(first=openDrugMsgCount,second=0,msg=openDrugMsgError)

        ####
        #### closed
        ####
        #count of members with too low PDC
        closePDCMsgCount = sum([1 if x < 0.8 else 0 for x in XClose[XPDCColumn].tolist()])
        closePDCMsgError = f"Error: Med Adherence for {XCGColumn}; {str(closePDCMsgCount)} closed members with less than 80% PDC"
        self.TestCase.assertEqual(first=closePDCMsgCount,second=0,msg=closePDCMsgError)

        #count of members not on the drug when they should be
        closeDrugMsgCount = sum([0 if x[0] == 1 or (x[1] >= 0) else 1 for x in zip(XClose[XDrugColumn],XClose[XCGColumn])])
        closeDrugMsgError = f"Error: Med Adherence for {XCGColumn}; {str(closeDrugMsgCount)} members not on drug and PDC gap closed"
        self.TestCase.assertEqual(first=closeDrugMsgCount,second=0,msg=closeDrugMsgError)

        ####
        #### ineligible
        ####
        #count of members with existant pdc
        inelPDCMsgCount = sum([1 if NVL(x,-1) != -1 else 0 for x in XInel[XPDCColumn].tolist()])
        inelPDCMsgError = f"Error: Med Adherence for {XCGColumn}; {str(inelPDCMsgCount)} inelgible members with non-null pdc"
        self.TestCase.assertEqual(first=inelPDCMsgCount,second=0,msg=inelPDCMsgError)

        #count of members not on drug when they should not be
        inelDrugMsgCount = sum([1 if x[0] == 1 or (NVL(x[1],-1) < 0) else 0 for x in zip(XInel[XDrugColumn],XInel[XCGColumn])])
        inelDrugMsgError = f"Error: Med Adherence for {XCGColumn}; {str(inelDrugMsgCount)} members on drug and PDC gap inelgible"
        self.TestCase.assertEqual(first=inelDrugMsgCount,second=0,msg=inelDrugMsgError)

        #end