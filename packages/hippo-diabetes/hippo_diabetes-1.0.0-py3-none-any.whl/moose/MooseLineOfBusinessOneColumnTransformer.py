#imports
import pandas as pd
import numpy as np
import os
from sklearn.base import BaseEstimator, TransformerMixin

#custom functions from other modules
#import from other modules
cwd = os.getcwd()
cwdHead = os.getcwd().split("/hippo/")[0]
os.chdir(cwdHead+ '/hippo/src2/util')
from util import UtilAPI
os.chdir(cwd)

class MooseLineOfBusinessOneColumnTransformer(BaseEstimator, TransformerMixin):
    """Function retains only the care gap columns
    :param featureNames: column for name of care gap
    :type featureNames: string

    :returns: dataframe with only the care gaps in it
    :rtype: pd.DataFrame
    """

    def __init__(self,lobDict=None):
        """constructor method
        """
        if lobDict is None:
            self.lobDict = UtilAPI().modelParam['moose_lob_column_dict']
        else:
            self.lobDict = lobDict

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

        # main function

    def transform(self, X, y=None):
        """function to select only the columns of interest

        Parameters
        :param X: np.array of features of interest for training
        :type X: np.array
        :param y: np.array of features of interest for testing (none in this case)
        :type Y: np.array

        :returns: dataframe with only the care gaps in it
        :rtype: pd.DataFrame
        """

        #create dictionaryies that will allow us to first flatten without loosing differences and then give correct names
        #isolate columsn of interest and drop from main
        keyList = [x for x in self.lobDict.keys()]

        #get dict to crosswalk values
        self.lobDictCrosswalk =dict(zip(keyList,[x for x in range(1,len(keyList)+1)]))

        #get crosswalk values to outcome printouts
        self.lobDictPrintCat =dict(zip([x for x in range(1,len(keyList)+1)],[x for x in self.lobDict.values()]))

        #get data of interest
        lob = X[keyList]
        X = X.drop(keyList,axis=1)

        #transform columns so each is unique
        for key in keyList:
            lob[key] = [self.lobDictCrosswalk[key] if x == 1 else 0 for x in lob[key]]

        #flatten columns
        lob['line_of_business'] = lob.max(axis=1)

        #rename columns with the proper names
        lob['line_of_business'] = [self.lobDictPrintCat[x] for x in lob['line_of_business']]

        #return
        return pd.concat([X,lob['line_of_business']],axis=1).reset_index(drop=True)