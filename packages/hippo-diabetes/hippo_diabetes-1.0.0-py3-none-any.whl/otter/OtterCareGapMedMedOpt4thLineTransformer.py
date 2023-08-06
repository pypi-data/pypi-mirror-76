# imports
import pandas as pd
import numpy as np
import os
from sklearn.base import BaseEstimator, TransformerMixin


class OtterCareGapMedMedOpt4thLineTransformer(BaseEstimator, TransformerMixin):
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
    :param includeComor: columns from dataframe of comorbidity that need to include
    :type includeComor: string
    :param excludeComorb: columns from dataframe of comorbidity that need to exclude
    :type excludeComorb: string
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

    def __init__(self, careGapName, comMedCol, a1cValue, a1cCriteria, includeComorb, excludeComorb, extraDrug,
                 extraDrugCount, drugList, requiredAntiDiabeticDrug, requiredAntiDiabeticDrugPDC,
                 countOfAnyRequiredDrug):
        """constructor method
        """
        self.careGapName = careGapName
        self.comMedCol = comMedCol
        self.a1cValue = a1cValue
        self.a1cCriteria = a1cCriteria
        self.includeComorb = includeComorb
        self.excludeComorb = excludeComorb
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

        # run unti test
        #         test_OtterCareGapMedOptTransformer().test_a1cThresh(self.careGapName,X[Value],Threshold)

        # skip the filter if no a1c threshold
        if Threshold is None:
            return True
        else:
            # for those who meet the a1c threshold criteria
            return X[Value] in Threshold

    # helper function(Filter values that meet the include condition)
    def inclusion(self, X, Condition):
        """filter the values that meet the commorbidity condition

        Parameters
        :param X: DataFrame of Unify table
        :type X: DataFrame
        :param Condtion: Commorbidity list that need include
        :type Condition: list
        """
        # skip the filter if no required commorbidity condition
        if Condition is None:
            return True
        # among those who must have the commorbidity condition
        else:
            return np.nansum(X[Condition]) >= 1

    # helper function(Filter values that meet the exclude condition)
    def exclusion(self, X, Condition):
        """filter the values that meet the commorbidity condition

        Parameters
        :param X: DataFrame of Unify table
        :type X: DataFrame
        :param Condtion: Commorbidity list that need exclude
        :type Condition: list
        """
        # skip the filter if no required commorbidity condition
        if Condition is None:
            return True
        # among those who must have the commorbidity condition
        else:
            return np.nansum(X[Condition]) == 0

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
        if requiredDrug is None:
            return True
        # among those who have the required drug and pdc
        elif np.nansum(X[requiredDrug]) == len(requiredDrug) and np.nansum(
                [1 if p >= 0.8 else 0 for p in X[requiredPDC]]) == len(requiredDrug):
            return True
        # among those who are ineligible
        else:
            return False

    # update the antidiabetic drug and antidiabetic pdc list via removing the required anti Diabetic drug
    def antiDiabeticListUpdate(self, drugList, requiredDrug):
        """return the updated antidiabetic drug list and updated drug pdc list with required drug removed

        Parameters
        :param drugList: the whole drug list of antidiabtics
        :type drugList: list
        :param requiredDrug: drug list of the prerequisite antidiabetic drug list per this care gap
        :type requiredDrug: list
        """
        drugPDCList = []
        drugLongerThan12moList = []
        # save a copy
        drugListCopy = drugList.copy()
        for i in drugListCopy:
            # get the drug indicator of whether or not it lasts for 12 months
            drugFeature = '_'.join(i.split('_')[:-3]) + '_longer_' + '_'.join(i.split('_')[-2:])
            drugLongerThan12moList.append(drugFeature)
            # get the drug pdc name based on drug name
            pdc = '_'.join(i.split('_')[:-3]) + '_pdc_' + '_'.join(i.split('_')[-3:])
            drugPDCList.append(pdc)
        # no required antidiabetic drug
        if not requiredDrug:
            return drugListCopy, drugPDCList, drugLongerThan12moList
        else:
            # update the drug and pdc list with removing requied one
            for i in requiredDrug:
                drugListCopy.remove(i)
                pdc = '_'.join(i.split('_')[:-3]) + '_pdc_' + '_'.join(i.split('_')[-3:])
                drugFeature = '_'.join(i.split('_')[:-3]) + '_longer_' + '_'.join(i.split('_')[-2:])
                drugPDCList.remove(pdc)
                drugLongerThan12moList.remove(drugFeature)
            return drugListCopy, drugPDCList, drugLongerThan12moList

    # helper function(deal with the extra conditions for anti diabetic drugs)
    def extraFilter(self, X, extraDrug, extraDrugCount):
        if extraDrug is None:
            return True
        else:
            return np.nansum(X[extraDrug]) <= extraDrugCount

    # helper function(distinguish the value that is open or close)
    def finalFilter(self, X, count, drugList, drugPDCList, drugLongerThan12moList):
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
            return np.nansum(X[drugList]) == 0
        # among those who have required antidiabtic drug
        elif (np.nansum(X[drugList]) == count) and (np.nansum(X[drugLongerThan12moList]) >= 1) and (
                np.nansum([1 if p >= 0.8 else 0 for p in X[drugPDCList]]) == count):
            return True
        # among those who are ineligible
        else:
            return False

    # helper function (distinguishes if they have met the condition or not)
    def medOpt(self, X, Value, Threshold, inclusionValue, exclusionValue, requiredDrug, requiredPDC, count,
               drugListUpdate, drugPDCListUpdate, drugLongerThan12moListUpdate, extraDrug, extraDrugCount):
        """turns compenent columns into care gap open, closed or ineligible

        Returns
        :returns: 0 if ineligible, 1 if closed and elgible, 2 and opened and elibible
        :rtype: interger
        """
        holder = []
        # apply to all the members
        for index, x in X.iterrows():
            # among those who meet the a1c threshold
            if self.a1cThresh(x, Value, Threshold):
                # among those who meet the include commorbidity condition
                if self.inclusion(x, inclusionValue):
                    # among those who meet the exclude comorbidity condition
                    if self.exclusion(x, exclusionValue):
                        # among those who meet the extra requirement of antidiabetic drug
                        if self.extraFilter(x, extraDrug, extraDrugCount):
                            # among those who have the required antidiabetic drug and pdc
                            if self.preFilter(x, requiredDrug, requiredPDC):
                                # among those who have other required antidiabetic drug and pdc
                                if self.finalFilter(x, count, drugListUpdate, drugPDCListUpdate,
                                                    drugLongerThan12moListUpdate):
                                    holder.append(int(2))
                                else:
                                    # among those who don't have other required antidiabetic drug
                                    holder.append(int(1))
                                continue
            # among those who are ineligible
            holder.append(int(0))

        # #test results
        # pd.DataFrame(holder,columns=[self.careGapName]).to_csv('temp.csv',index=False,index_label=False)

        # #unit testing
        # test_OtterCareGapMedOptTransformer().test_medOpt(holder)

        # return the result
        return holder

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
        # drugs to use
        drugListUpdate, drugPDCListUpdate, drugLongerThan12moListUpdate = self.antiDiabeticListUpdate(self.drugList,
                                                                                                      self.requiredAntiDiabeticDrug)
        # build return dataframe with the addition
        returnX = pd.DataFrame(self.medOpt(X, self.a1cValue, self.a1cCriteria, self.includeComorb, self.excludeComorb,
                                           self.requiredAntiDiabeticDrug, self.requiredAntiDiabeticDrugPDC,
                                           self.countOfAnyRequiredDrug,
                                           drugListUpdate, drugPDCListUpdate, drugLongerThan12moListUpdate,
                                           self.extraDrug, self.extraDrugCount),
                               columns=[self.careGapName])
        # unittest
        # test_OtterCareGapMedOptTransformer().test_transformer(returnX)

        # add on insure med columns
        returnX[self.comMedCol] = X[self.comMedCol]

        # return results
        return returnX
