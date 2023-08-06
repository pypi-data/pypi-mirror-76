#imports
import pandas as pd
import numpy as np
import os
from sklearn.base import BaseEstimator, TransformerMixin

class OtterCareGapDeviceTransformer(BaseEstimator, TransformerMixin):
    """Function develops the device care gaps

    Parameters:
    :param careGapName: column for name of care gap
    :type careGapName: string
    :param comMedCol: column for type of insruance indicator
    :type comMedCol: string
    :param hypoglycemicDx: column from dataframe that determines if the member has hypoglycemic 
    :type hypoglycemicDx: string
    :param drugInsulin12: column from dataframe that determines if the member has insulin in last 12 month
    :type drugInsulin12: string
    :param deviceTest: columns from the dataframe of diabetic device test
    :type deviceTest:List of strings

    Returns:
    :returns: new care gap column with = int: 0 if ineligible, 1 if closed and eligible, 2 if opened and eligble
    :rtype: pd.DataFrame
    """

    def __init__(self, careGapName, comMedCol, drugInsulin12,deviceTest):
        """constructor method
        """
        self.careGapName = careGapName
        self.comMedCol = comMedCol
        self.drugInsulin12 = drugInsulin12
        self.deviceTest = deviceTest

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
        return Value


    # helper function (distinguishes if they have met the condition or not)
    def deviceFilter(self, drugInsulin12,deviceTest):
        """turns compenent columns into care gap open, closed or ineligible

        Parameters
        :param drugInsulin12: 0,1 expressing if the person is on insulin or not
        :type drugInsulin12: integer
        :param deviceTest: 0,1 expressing if the person have the claims of test
        :type deviceTest: integer

        Returns
        :returns: 0 if ineligible, 1 if closed and elgible, 2 and opened and elibible
        :rtype: interger
        """

        # among those who are eligible
        if drugInsulin12 == 1:
            # if having 1+ claims of testing, then closed
            if np.sum(deviceTest) >= 1:
                return int(1)

            # if having 0 claims of testing, then opened
            elif np.sum(deviceTest) == 0:
                return int(2)

        # among those who are not eligible
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
        returnX =  pd.DataFrame(zip(X[self.drugInsulin12],
                                X[self.deviceTest[0]],X[self.deviceTest[1]],X[self.deviceTest[2]],
                                [self.deviceFilter(d[0], d[1]) for d in zip(X[self.drugInsulin12],X[self.deviceTest].values)]),
                        columns= [self.drugInsulin12]+ self.deviceTest + [self.careGapName])

        #add on insure med columns
        returnX[self.comMedCol] = X[self.comMedCol]
        
        return returnX
