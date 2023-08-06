#imports
import pandas as pd
import numpy as np
import os
from sklearn.base import BaseEstimator, TransformerMixin

class OtterCareGapColumnConsolidater(BaseEstimator, TransformerMixin):
    """Consolidate same numbered commerical and medicare gaps into

    :param X: dataframe of all features and care gaps.  care gaps are still split into commerical and com
    :type X: pd.DataFrame
    :param prefix_com: True if you want to consolidate care gaps that are commercial (start with com_) else False
    :type prefix_com: boolean
    :param prefix_med: True if you want to consolidate care gaps that are medicare (start with med_) else False
    :type prefix_med: boolean
    """


    def __init__(self, prefix_com = True, prefix_med=True):
        """constructor method
        """
        self.prefix_com = prefix_com
        self.prefix_med = prefix_med

    def transform(self, X):

        #holders for column information
        comCol = []
        medCol = []
        shareCol = []

        #isolate all the com cols
        if self.prefix_com:
            comCol = [x for x in X.columns if 'com_' in x and 'care_gap' in x]

        #isolate the med cols
        if self.prefix_med:
            medCol = [x for x in X.columns if 'med_' in x and 'care_gap' in x]

        #isolate the columns that are shared
        if self.prefix_com & self.prefix_med:

            #get columns to colide
            shareCol = sorted([x[4:] for x in comCol if x[4:] in [y[4:] for y in medCol]])

            #get the columns to keep seperate
            comCol = sorted([x for x in comCol if x[4:] not in shareCol])
            medCol = sorted([x for x in medCol if x[4:] not in shareCol])

        #get the other features
        returnX = X[[col for col in X.columns if 'care_gap' not in col]+comCol+medCol]

        #rename the columns in comCol and com Med
        comMedCol = comCol + medCol
        for col in comMedCol:
            returnX.columns = [x[4:] if x == col else x for x in returnX.columns]

        #input the other columns that are shared
        if self.prefix_com & self.prefix_med:

            #itearte and append all share columns
            for col in shareCol:

                #take the max - none insured gap should be zero, regardless open > close > ineligle
                returnX[col] = [np.max(x) for x in zip(X['com_'+col],X['med_'+col])]

        #return consolidated
        return returnX