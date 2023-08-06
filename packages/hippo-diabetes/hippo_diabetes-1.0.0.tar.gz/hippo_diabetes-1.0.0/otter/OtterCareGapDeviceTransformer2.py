#imports
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

class OtterCareGapDeviceTransformer2(BaseEstimator, TransformerMixin):
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
    :param SUDx12: columns from the dataframe of SU based on GPIs
    :type SUDx12: string
    :param a1cThresh: columns from the dataframe of lab a1c Values
    :type a1cThresh: string

    Returns:
    :returns: new care gap column with = int: 0 if ineligible, 1 if closed and eligible, 2 if opened and eligble
    :rtype: pd.DataFrame
    """

    def __init__(self, careGapName, comMedCol, hypoglycemicDx, drugInsulin12,deviceTest,SUDx12, a1cThresh):
        """constructor method
        """
        self.careGapName = careGapName
        self.comMedCol = comMedCol
        self.hypoglycemicDx = hypoglycemicDx
        self.drugInsulin12 = drugInsulin12
        self.deviceTest = deviceTest
        self.SUDx12 = SUDx12
        self.a1cThresh = a1cThresh

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
    def deviceFilter1(self, hypoglycemicDx, drugInsulin12,deviceTest):
        """turns compenent columns into care gap open, closed or ineligible

        Parameters
        :param hypoglycemicDx: 0,1 expressing if the person has hypoglycemia or not
        :type hypoglycemicDx: integer
        :param drugInsulin12: 0,1 expressing if the person is on insulin or not
        :type drugInsulin12: integer
        :param deviceTest: 0,1 expressing if the person have the claims of test
        :type deviceTest: integer

        Returns
        :returns: 0 if ineligible, 1 if closed and elgible, 2 and opened and elibible
        :rtype: interger
        """

        # among those who are eligible
        if hypoglycemicDx == 1 and drugInsulin12 == 0:
            # if having 1+ claims of testing, then closed
            if np.sum(deviceTest) >= 1:
                return int(1)

            # if having 0 claims of testing, then opened
            elif np.sum(deviceTest) == 0:
                return int(2)

        # among those who are not eligible
        else:
            return int(0)

    # helper function (distinguishes if they have met the condition or not)
    def deviceFilter2(self, hypoglycemicDx, drugInsulin12,deviceTest,SUDx12, a1cThresh):
        """turns compenent columns into care gap open, closed or ineligible

        Parameters
        :param hypoglycemicDx: 0,1 expressing if the person has hypoglycemia or not
        :type hypoglycemicDx: integer
        :param drugInsulin12: 0,1 expressing if the person is on insulin or not
        :type drugInsulin12: integer
        :param deviceTest: 0,1 expressing if the person have the claims of test
        :type deviceTest: integer
        :param SUDx12: 0, 1 expressing if the member on SU
        :type SUDx12: integer
        :param a1cThresh: a1c Value  
        :type a1cThresh: float

        Returns
        :returns: 0 if ineligible, 1 if closed and elgible, 2 and opened and elibible
        :rtype: interger
        """

        # among those who are eligible
        if hypoglycemicDx == 0 and drugInsulin12 == 0 and SUDx12 == 1 and a1cThresh < 6.5:
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
        """fit method for collaborating with pipeline. Uses the drug and drug pdc information

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
        returnX =  pd.DataFrame(zip(X[self.hypoglycemicDx],X[self.drugInsulin12],
                                X[self.deviceTest[0]],X[self.deviceTest[1]],X[self.deviceTest[2]],
                                X[self.SUDx12],X[self.a1cThresh],
                                [a[0]+a[1] for a in zip(
                                [self.deviceFilter1(d[0], d[1], d[2]) for d in zip(X[self.hypoglycemicDx],X[self.drugInsulin12],X[self.deviceTest].values)],
                                [self.deviceFilter2(d[0], d[1], d[2],d[3],d[4]) for d in zip(X[self.hypoglycemicDx],X[self.drugInsulin12],X[self.deviceTest].values,
                                                                                    X[self.SUDx12],X[self.a1cThresh])])]
                                ),
                        columns= [self.hypoglycemicDx, self.drugInsulin12]+ self.deviceTest + [self.SUDx12,self.a1cThresh]+[self.careGapName])

        #add on insure med columns
        returnX[self.comMedCol] = X[self.comMedCol]

        return returnX
