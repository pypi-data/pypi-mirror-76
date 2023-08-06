#imports
import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin

#class
class EgretCleanDummyTransformer(BaseEstimator, TransformerMixin):
    """Function selects the column of interest

    Parameters
    :param stringFlag: True if we are going to include all features that are strings in the get dummies, False if not
    #type stringFlag: boolean
    :param colManualList: list of features to include in the dummy regardless if they are string or not
    :type colManualList: list
    :param nullCol: True if we want to include null columns from dummies, else fase
    :type nullCol: boolean
    :param careGapStringMaker: True if you want to turn all columns with 'care_gap' in their name to strings, else False
    :type careGapStringMaker: boolean

    Returns
    :returns: dataframe with the columns of interest (split out dummies for some columns transformed
    :rtype: pd.DataFrame
    """

    # Class Constructor
    def __init__(self,stringFlag=True,colManualList=[],nullCol=False,careGapStringMaker=False):

        """ constructor method
        """
        self.stringFlag = stringFlag
        self.colManualList = colManualList
        self.nullCol = nullCol
        self.careGapStringMaker = careGapStringMaker

        # Return self nothing else to do here

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

    # Method that describes what we need this transformer to do
    def transform(self, X, y=None):
        """Select the columns of interest

        Parameters
        :param X: np.array of features of interest for training
        :type X: np.array
        :param y: np.array of features of interest for testing (none in this case)
        :type Y: np.array

        Returns
        :returns: data frame with the columns of interest
        :rtype: pd.DataFrame
        """
        #if careGapStringMaker is true turn the care gap columns to string
        if self.careGapStringMaker:

            #find columns
            careGapList = [x for x in X.columns if 'care_gap' in x]

            #apply string (so then they are dummied in later steps
            X[careGapList] = X[careGapList].astype(str)

        #convert columns as needed to string for any manually specified columns
        if len(self.colManualList) >= 1:

            #apply conversion to files of interest
            X[self.colManualList] = X[self.colManualList].astype(str)

        #if no manual columns and there is not need to dummy the string columns then exit early with unchaged x
        elif len(self.colManualList) == 0 and self.stringFlag ==False:
            return X

        #identify the columns to apply the result to
        if self.stringFlag == True:

            #grab all additional columns as needed that are strings (some redundant)
            colStringList = [ x[0] for x in zip(X.dtypes.keys(),X.dtypes.values) if x[1] in (np.dtype(np.object).type,np.dtype(np.str).type,type('a'))]

            #non redundantly put together the lists
            completeDummyList =list(set(colStringList + self.colManualList))

        # if we only have manual columns
        elif self.stringFlag == False:
            completeDummyList = self.colManualList

        #apply
        #apply dummys if apprioriate

        if len(completeDummyList) >= 1:

            new_cols = []
            #iterate through the columns and apply splits
            for col in completeDummyList:
                dummies = pd.get_dummies(X[col],
                                         prefix=col,
                                         dummy_na=self.nullCol,
                                         dtype=int)
                new_cols.append(dummies)
                X = X.drop([col], axis = 1)

            new_cols = [X] + new_cols
            X = pd.concat(new_cols, axis = 1)
            # lower case all columns (insuring for dummies)
            X.columns = [str(y).lower() for y in X.columns.tolist()]

        #return the dummified data frame
        return X
