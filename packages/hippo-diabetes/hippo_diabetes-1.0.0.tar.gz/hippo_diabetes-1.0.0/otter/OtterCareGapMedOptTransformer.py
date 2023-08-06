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
from test_OtterCareGapMedOptTransformer import test_OtterCareGapMedOptTransformer
os.chdir(cwd)

class OtterCareGapMedOptTransformer(BaseEstimator, TransformerMixin):
    """Function develops the med optimization care gaps

    Parameters:
    :param careGapName: column for name of care gap
    :type careGapName: string
    :param comMedCol: column for type of insurance indicator
    :type comMedCol: string
    :param a1cValue: column from dataframe of latest A1c value
    :type a1cValue: string
    :param a1cCriteria: a1c threshold 
    :type a1cCriteria: integer
    :param conditionComor: indicator whether there are any comorbidity condition 
    :type conditionComor: boolean
    :param conditionValue: columns from dataframe of any condition comorbidity to exclude/include/None
    :type conditionValue: string
    :param requiredAntiDiabeticDrug: columns from dataframe of prerequisite drug with pdc >=80%
    :type requiredAntiDiabeticDrug: string
    :param countOfAnyRequiredDrug: required count of other antidiabetic drug
    :type countOfAnyRequiredDrug: integer
    :param extraDrug: required extra anti-diabetic drug that should not have
    :type extraDrug: string
    :param extraDrugCount: required extra anti-diabetic drug count 
    :type extraDrugCount: integer
    

    Returns:
    :returns: new care gap column with = int: 0 if ineligible, 1 if closed and eligible, 2 if opened and eligible
    :rtype: pd.DataFrame
    """

    def __init__(self, careGapName, comMedCol, a1cValue, a1cCriteria, conditionStatus,conditionValue, extraDrug,extraDrugCount, drugList, requiredAntiDiabeticDrug, requiredAntiDiabeticDrugPDC,countOfAnyRequiredDrug):
        """constructor method
        """
        self.careGapName = careGapName
        self.comMedCol = comMedCol
        self.a1cValue = a1cValue
        self.a1cCriteria = a1cCriteria
        self.conditionStatus = conditionStatus
        self.conditionValue = conditionValue
        self.extraDrug = extraDrug
        self.extraDrugCount = extraDrugCount
        self.requiredAntiDiabeticDrug = requiredAntiDiabeticDrug
        self.requiredAntiDiabeticDrugPDC = requiredAntiDiabeticDrugPDC
        self.countOfAnyRequiredDrug = countOfAnyRequiredDrug
        self.drugList = drugList

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
 
    # helper function(replace null values with another value)
    def NVL(self, Value, newValue):
        """replace null values with new value

        Parameters
        :param Value: a scalar indicates whether value is missing 
        :type Value: a scalar (for missing value: NaN in numeric arrays, None or NaN in object arrays, NaT in datetimelike)
        :param newValue: a scalar of the new value
        :type newValue: a scalar 

        Returns
        :returns: a scalar with missing value replaced
        :rtype: a scalar
        """
        # replace missing value with newValue
        if pd.isnull(Value):
            return newValue
        else:
            return Value

    # helper function(filter the columns that meet the a1c Criteria)
    def a1cThresh(self, X, Value, Threshold):
        """filter the values that meet the a1c criteria if any

        Parameters
        :param X: DataFrame of Unify table
        :type X: DataFrame
        :param Value: Column for the lab a1c Value
        :type Value:string
        :param Threshold: A scalar of A1c Threshold
        :type Threshold: a scalar(None if no threshold, integer for the ones with threshold)
        """


        #run unti test
        test_OtterCareGapMedOptTransformer().test_a1cThresh(self.careGapName,X[Value],Threshold)


        # skip the filter if no a1c threshold

        if Threshold is None:
            return True
        else:
            return X[Value] in Threshold

    # helper function(Filter values that meet the include/exclude condition)
    def condition(self, X, Status, Condition):
        """filter the values that meet the commorbidity condition

        Parameters
        :param X: DataFrame of Unify table
        :type X: DataFrame
        :param Status: None, 'exclude', 'include' indicate the commorbidity status
        :type Status: String
        :param Condtion: Commorbidity list that need include or exclude
        :type Condition: list
        """

        #apply unit test (if statement to handle no comos)
        if Condition is not None:
            test_OtterCareGapMedOptTransformer().test_condition(self.careGapName,Status,Condition,X[Condition].tolist())
        else:
            test_OtterCareGapMedOptTransformer().test_condition(self.careGapName,Status,Condition,None)

        # skip the filter if no required commorbidity condition
        if  Status is None:
            return True
        # among those who must have the commorbidity condition
        elif Status == 'include' and sum(X[Condition]) >= 1:
            return True
        # among those who must not have the commorbidity condition
        elif Status == 'exclude' and sum(X[Condition]) == 0:
            return True
        # among those who are ineligible
        else:
            return False

    # helper function(filter values that have the prerequisite antidiabetic drug)
    def preFilter(self, X, requiredDrug, requiredPDC):
        """filter the values that have the prerequisite drug with PDC >= 0.8

        Parameters
        :param X: DataFrame of Unify table
        :type X: DataFrame
        :param requiredDrug: list of the required prerequisite drug
        :type requiredDrug: list
        :param requiredPDC: list of the required prerequisite drug pdc
        :type requiredPDc: list
        """

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

        #unit testing (paused do to emergency request)
        #modelParam = UtilAPI().modelParam
        #test_OtterCareGapMedOptTransformer().test_preFilter(resultHolder,
        #                                                    self.careGapName,
        #                                                requiredDrug,
        #                                                requiredPDC,
        #                                                X[requiredDrug],
        #                                                X[requiredPDC],
        #                                                X[modelParam['otter_list_of_anti_diabetic_drug_cnt']],
        #                                                X[modelParam['otter_list_of_anti_diabetic_drug_pdc']])

        #if passes unit test, return
        return resultHolder

    # update the antidiabetic drug and antidiabetic pdc list via removing the required anti Diabetic drug
    def antiDiabeticListUpdate(self, drugList,requiredDrug):
        """return the updated antidiabetic drug list and updated drug pdc list with required drug removed

        Parameters
        :param drugList: the whole drug list of antidiabtics
        :type drugList: list
        :param requiredDrug: drug list of the prerequisite antidiabetic drug list per this care gap
        :type requiredDrug: list
        """

        drugPDCList = []
        # save a copy
        drugListCopy = drugList.copy()
        for i in drugListCopy:
            # get the drug pdc name based on drug name
            pdc = '_'.join(i.split('_')[:-3]) + '_pdc_' + '_'.join(i.split('_')[-3:])
            drugPDCList.append(pdc)
        # no required antidiabetic drug
        if not requiredDrug:
            return drugListCopy, drugPDCList
        else:
            # update the drug and pdc list with removing requied one
            for i in requiredDrug:
                drugListCopy.remove(i)
                pdc = '_'.join(i.split('_')[:-3]) + '_pdc_' + '_'.join(i.split('_')[-3:])
                drugPDCList.remove(pdc)
            return drugListCopy, drugPDCList

    # helper function(deal with the extra conditions for anti diabetic drugs)

    def extraFilter(self,X, extraDrug,extraDrugCount):

        if extraDrug is None:
            return True
        else:
            return sum(X[extraDrug]) <= extraDrugCount
        

    # helper function(distinguish the value that is open or close)
    def finalFilter(self, X , count, drugList, drugPDCList):
        """filter the values that have the required number of antidiabetic drug and return the open and close care gap

        Parameters
        :param X: DataFrame of Unify table
        :type X: DataFrame
        :param count: required number of antidiabtic drug
        :type count: integer
        :param drugList: updated antidiabetic drug list
        :type list
        :param drugPDCList: updated antidiabetic drug PDC list
        :type list
        """

        # skip the filter if no other antidiabetic drug requirement
        if count is None:
            return sum(X[drugList]) == 0
        # among those who have required antidiabtic drug
        elif (sum(X[drugList]) == count) and (sum([1 if p > 0.8 else 0 for p in X[drugPDCList]]) == count):
            return True
        # among those who are ineligible
        else:
            return False


    # helper function (distinguishes if they have met the condition or not)
    def medOpt(self, X, Value, Threshold, Status, Condition, requiredDrug, requiredPDC,count,drugListUpdate,drugPDCListUpdate,extraDrug,extraDrugCount):
        """turns compenent columns into care gap open, closed or ineligible

        Returns
        :returns: 0 if ineligible, 1 if closed and elgible, 2 and opened and elibible
        :rtype: interger
        """
        holder = []
        # apply to all the members
        for i in range(X.shape[0]):
            x = X.iloc[i]
            # among those who meet the a1c threshold
            if self.a1cThresh(x, Value,Threshold):
                # among those who meet the commorbidity condition
                if self.condition(x,Status,Condition):
                    # among those who meet the extra requirement of antidiabetic drug
                    if self.extraFilter(x,extraDrug,extraDrugCount):
                        # among those who have the required antidiabetic drug and pdc
                        if self.preFilter(x,requiredDrug, requiredPDC):
                            # among those who have other required antidiabetic drug and pdc
                            if self.finalFilter(x,count,drugListUpdate,drugPDCListUpdate):
                                holder.append(int(2))
                            else:
                                # among those who don't have other required antidiabetic drug
                                holder.append(int(1))
                            continue
            # among those who are ineligible
            holder.append(int(0))

#         #unit testing
#         test_OtterCareGapMedOptTransformer().test_medOpt(holder)

        # return the result
        return holder
    
    ## The Pandas Built-In Function: iterrows()(distinguishes if they have met the condition or not)
    def medOptIterrows(self, X, Value, Threshold, Status, Condition, requiredDrug, requiredPDC,count,drugListUpdate,drugPDCListUpdate,extraDrug,extraDrugCount):
        """turns compenent columns into care gap open, closed or ineligible

        Returns
        :returns: 0 if ineligible, 1 if closed and elgible, 2 and opened and elibible
        :rtype: interger
        """
        holder = []
        # apply to all the members
        for index, x in X.iterrows():
            # among those who meet the a1c threshold
            if self.a1cThresh(x, Value,Threshold):
                # among those who meet the commorbidity condition
                if self.condition(x,Status,Condition):
                    # among those who meet the extra requirement of antidiabetic drug
                    if self.extraFilter(x,extraDrug,extraDrugCount):
                        # among those who have the required antidiabetic drug and pdc
                        if self.preFilter(x,requiredDrug, requiredPDC):
                            # among those who have other required antidiabetic drug and pdc
                            if self.finalFilter(x,count,drugListUpdate,drugPDCListUpdate):
                                holder.append(int(2))
                            else:
                                # among those who don't have other required antidiabetic drug
                                holder.append(int(1))
                            continue
            # among those who are ineligible
            holder.append(int(0))

        # return the result
        return holder


    ## The apply(distinguishes if they have met the condition or not)
    def medOptApply(self, X, Value, Threshold, Status, Condition, requiredDrug, requiredPDC,count,drugListUpdate,drugPDCListUpdate,extraDrug,extraDrugCount):
        """turns compenent columns into care gap open, closed or ineligible

        Returns
        :returns: 0 if ineligible, 1 if closed and elgible, 2 and opened and elibible
        :rtype: interger
        """
        # among those who meet the a1c threshold
        a1cIndicator = X.apply(lambda x:self.a1cThresh(x, Value,Threshold),axis = 1)
        conditionIndicator = X.apply(lambda x:self.condition(x,Status,Condition), axis = 1)
        extraIndicator = X.apply(lambda x:self.extraFilter(x,extraDrug,extraDrugCount), axis = 1)
        preIndicator = X.apply(lambda x:self.preFilter(x,requiredDrug, requiredPDC),axis = 1)
        finalIndicator = X.apply(lambda x:self.finalFilter(x,count,drugListUpdate,drugPDCListUpdate),axis = 1)
        
        return [2 if i[0]&i[1]&i[2]&i[3]&i[4] else 1 if i[0]&i[1]&i[2]&i[3] else 0 for i in                                                                                                                                  zip(a1cIndicator,conditionIndicator,extraIndicator,preIndicator,finalIndicator)]

    
    # main function
    def transform(self, X, y=None):
        """fit method for collaborating with pipeline. 

        Parameters
        :param y: np.array of features of interest for testing (none in this case)
        :type Y: np.array

        Returns
        :returns: dataframe of care gaps opened or closed based on med adhere
        :rtype: dataframe
        """
        #drugs to use
        drugListUpdate,drugPDCListUpdate = self.antiDiabeticListUpdate(self.drugList, self.requiredAntiDiabeticDrug)
        # build return dataframe with the addition
        returnX =  pd.DataFrame(self.medOptIterrows(X, self.a1cValue, self.a1cCriteria, self.conditionStatus, self.conditionValue, 
                                self.requiredAntiDiabeticDrug, self.requiredAntiDiabeticDrugPDC,self.countOfAnyRequiredDrug,
                                drugListUpdate,drugPDCListUpdate, self.extraDrug,self.extraDrugCount),
                            columns=[self.careGapName])
        #unittest
#         test_OtterCareGapMedOptTransformer().test_transformer(returnX)

        #add on insure med columns
        returnX[self.comMedCol] = X[self.comMedCol]

        #return results
        return returnX


