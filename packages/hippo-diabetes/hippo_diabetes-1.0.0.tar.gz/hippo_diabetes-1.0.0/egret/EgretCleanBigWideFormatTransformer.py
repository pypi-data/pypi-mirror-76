#imports
import pandas as pd
import numpy as np
import os
from sklearn.base import BaseEstimator, TransformerMixin

#import custom modules
#cmenagerie model imports
cwd = os.getcwd()
cwdHead = os.getcwd().split("/hippo/")[0]

#import hpackages and return to this directo
os.chdir(cwdHead+ '/hippo/src2/util')
from util import UtilAPI

#return to original directory
os.chdir(cwd)

#class
class EgretCleanBigWideFormatTransformer(BaseEstimator, TransformerMixin):
    """For all drug pdc fill nulls with zeros so they can be used in mooose

    Parameters
    :param genderCol: name of column in fed dataframe that holds the gender information
    #type genderCol: string
    :param genderList: list of genders to include (M,F,U) acceptable options
    :type genderList: list

    Returns
    :returns: dataframe with the columns of interest
    :rtype: pd.DataFrame
    """

    # Class Constructor
    def __init__(self):
        """ constructor method
        """
        pass

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

    def crosswalk(self,input):
        """ crosswalks the 3,1,None to 2,1,0

        :param input:
        :type input: interger/none
        :return: new clean name of the care conisderations
        :rtype: integer
        """

        #it not null
        if pd.notnull(input):
            if input == 3:
                #adjust opened
                return 2
            elif input == 1:
                #return closed as is
                return 1
            else:
                #indicates problem
                return -1

        else:
            #if null return zero
            return 0

    # Method that describes what we need this transformer to do
    def transform(self, X, y=None):
        """crosswalk all the columns of interest in place

        Parameters
        :param X: np.array of features of interest for training
        :type X: np.array
        :param y: np.array of features of interest for testing (none in this case)
        :type Y: np.array

        Returns
        :returns: data frame with the columns of interest
        :rtype: pd.DataFrame
        """

        #get the columns of interest
        modelParam = UtilAPI().modelParam

        #grab columns of interest
        colList = modelParam['egret_big_wide_columns']

        #convert each column one at atime
        for col in colList:

            #crosswalk codes
            X[col] = [self.crosswalk(x) for x in X[col]]

            #code as string so treated as categorical in later step
            X[col] = X[col].astype(str)

        #fill the columns with zeros
        return X