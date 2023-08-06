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
class test_OtterCareGapMedOptTransformer(unittest.TestCase):
    """ testing the test_OtterCareGapMedOptTransformer
     No Return, but if it fails it gives a detailed message

    No Parameters or Returns
    """

    def __init__(self):
        """constructor
        """
        self.TestCase = unittest.TestCase()
        pass

    def test_a1cThresh(self,careGapName,a1cValue,a1cThrehold):
        """

        :param careGapName: name of care gap of interest
        :type careGapName: string
        :param a1cValue: value of the given member
        :type a1cValue: float
        :param a1cThrehold: threshold that the care gap is designed to hit
        :type a1cThrehold: float
        """

        #make sure that a1c value is in accetable range for user a1c value (where a1c value exists)
        if isinstance(a1cValue,int) or isinstance(a1cValue,float):
            a1CValueMsg = f'Error: Med Optimization Gap {careGapName}: A1C Value of Member Out of Reasonable Range'
            self.TestCase.assertIn(a1cValue,pd.Interval(2,18,closed='both'),a1CValueMsg)

        #make sure that a1c is in an accetable range for threshold
        if isinstance(a1cThrehold,int) or isinstance(a1cThrehold,float):
            a1CThresholdValueMsg = f'Error: Med Optimization Gap {careGapName}: A1C Value of Threshold Out of Reasonable Range'
            self.TestCase.assertIn(a1cThrehold,pd.Interval(2,18,closed='both'),a1CThresholdValueMsg)




    def test_inclusion(self,careGapName,excludeComorb,member):
        """ tests for comorobidities
        :param careGapName: name of care gap
        :type careGapName: string
        :param excludeComorb: columns from dataframe of comorbidity that need to exclude
        :type excludeComorb: string
        :param member: information from the como list if the member has the comos or not
        :type member: list
        :return:
        """
        #grab information from modelParam related to this care gap
        careGapCondition = UtilAPI().modelParam['otter_care_gap_med_medOpt'][careGapName]
        comoExcludeList = careGapCondition[2]

        #verify that the como (or nones themselves are indentical as wll;
        comoMatchMsg = f"Error: Med Optimization Care Gap {careGapName}: Exclusion List of Comorobidties Does not Match Expectations"
        self.TestCase.assertEqual(comoExcludeList,excludeComorb,comoMatchMsg)

        #verify that it is firing properly
        #get results
        excludeResult = sum(member) == 0

        #verify sum of member is indeed greater than one
        excludeTest = None
        if sum(member) == 0:
            excludeTest = True
        else:
            excludeTest = False

        #print message if there is an error
        excludeMsg = f"Error: Med optimization care gap {careGapName}: For exclusion of comorobidites, exclusion comorbidites not meeting expectations"
        self.TestCase.assertEqual(excludeResult,excludeTest,excludeMsg)

        pass

    def test_preFilter(self,resultHolder,careGapName,requiredDrug, requiredPDC,memberDrug,memberPDC,allDrug,allPDC):
        """tests firing for the correct count of drugs

        :param resultHolder: final result from care gap (member level)
        :type resultHolder: boolean
        :param careGapName: name of care gap
        :type careGapName: string
        :param requiredDrug: list of drugs the member must be on to fire (can be None)
        :type requiredDrug: list
        :param requiredPDC: list of pdc of drugs the member must be on to fire (can be None)
        :type requiredPDC: list
        :param memberDrug: list of drugs the member is on among the requiredDrug list.  1s and zeros
        :type memberDrug: list
        :param memberPDC: list of all pdcs of drugs the member is on among the required pdc list, numbers between 0 ans 1
        :type memberPDC: list
        :param allDrug: listof all antibeitic drug counts
        :type allPDC: list
        :param allDrug: list of all antibetic drug pdcs
        :type allPDC: list
        :return:
        """

        #get the drug of interest
        modelParam = UtilAPI().modelParam

        # skip the filter if no required anti diabetic drugs
        resultHolder = None
        if requiredDrug is None:
            resultHolder = True
        # among those who have the required drug and pdc
        elif sum(X[requiredDrug]) == len(requiredDrug) and sum([1 if p > 0.8 else 0 for p in X[requiredPDC]])==len(requiredDrug):
            resultHolder = True
        # among those who are ineligible
        else:
            resultHolder = False

        #unit testing
        modelParam = UtilAPI().modelParam
        test_OtterCareGapMedOptTransformer().test_preFilter(resultHolder,
                                                            self.careGapName,
                                                            requiredDrug,
                                                            requiredPDC,
                                                            X[requiredDrug],
                                                            X[requiredPDC],
                                                            X[modelParam['otter_list_of_anti_diabetic_drug_cnt']],
                                                            X[modelParam['otter_list_of_anti_diabetic_drug_pdc']])


        pass

    def test_antiDiabeticListUpdate(self):
        pass

    def test_extraFilter(self):
        pass

    def test_finalFilter(self):
        pass

    def test_medOpt(self,X):
        pass

    def test_transformer(self,X,XUnify):
        """ test transformer function of test_OtterCareGapMedOptTransformer
        Parameters
        :param X: dataframe of data (column 1 is 1/0 if the person is on the drug of interest, and second col is drug pdc for that drug, 3 is the care gap (0,1,2))
        :type X: pd.DataFrame
        """
        pass
        # #make sure that everyone is accounted for
        # gapCol = X.columns[0]
        # a1cCol = X.columns[1]
        # #grab information from modelParam related to this care gap
        # careGapCondition = UtilAPI().modelParam['otter_care_gap_med_medOpt'][gapCol]
        # a1cThrehold = careGapCondition[0]
        # comoIncludeList = careGapCondition[1]
        # comoExcludeList = careGapCondition[2]
        # #count values
        # total = X.shape[0]
        # open = X[X[gapCol]==2].shape[0]
        # close = X[X[gapCol]==1].shape[0]
        # inel = X[X[gapCol]==0].shape[0]
        # # group people to conduct checks upon
        # XInel = X[X[gapCol]==0]
        # XElig = X[X[gapCol]>0]
        # XClose = X[X[gapCol]==1]
        # XOpen = X[X[gapCol]==2]
        #
        # #design the message
        # misMatchMessage = 'Error: Med Optimization care gap {gapCol}: {total-open-close-inel} members are not open/close/inelgible'
        # self.TestCase.assertEqual(first=total,second=(open+close+inel),msg=misMatchMessage)
        #
        # # A1C check
        # #make sure the ELIGIBLE members are in the right a1c threshold
        # eligA1cMsgCount = sum([0 if x in a1cThrehold else 1 for x in XElig[a1cCol]])
        # eligA1cMsgError = f"Error: Med Optimization care gap for {gapCol}; {str(eligA1cMsgCount)} eligible members with A1c not in the threshold"
        # self.TestCase.assertEqual(first=eligA1cMsgCount,second=0,msg=eligA1cMsgError)

