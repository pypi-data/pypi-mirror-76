#imports
import pandas as pd
import numpy as np
import os
import unittest
from sklearn.base import BaseEstimator, TransformerMixin

#import custom modules
#cmenagerie model imports
cwd = os.getcwd()
cwdHead = os.getcwd().split("/hippo/")[0]

#import hpackages and return to this directo
os.chdir(cwdHead+ '/hippo/src2/otter')
from otter import OtterAPI
from OtterFeatureSelector import OtterFeatureSelector
os.chdir(cwdHead+ '/hippo/src2/util')
from util import UtilAPI
#return to original directory
os.chdir(cwd)

class MooseKeeperOffenderDrugTypeTransformer(BaseEstimator, TransformerMixin):
    """verify that people are not firing for the wrong type of drug, drugs that they are already on

    :returns: dataframe with all member level and new flags if they are firing for the wrong type of drugs
    :rtype: pd.DataFrame
    """

    def __init__(self):
        """constructor method
        """
        pass

    # fit function, leave untouched - sklearn needs this, but we do not
    def fit(self, X, y=None):
        """fit method for collaborating with pipeline

        Parameters
        :param X: moose member level output
        :type X: pd.DataFrame
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

        :returns: dataframe
        :rtype: pd.DataFrame
        """

        #information from model Param needed for tis
        modelParam = UtilAPI().modelParam

        #drugList
        drugList = ['alpha_glucose','metformin','dpp4','glp1','meglitinide','sglt2','sulfonylureas','tdz','insulin','statins']

        #get list of care gaps and their names that are in X (exclude care considerations, no deep understand of that logic)
        gapNameDict = {k:v for k,v in modelParam['moose_impact_feature_name'].items() if k+"_2" in X.columns and 'cc' not in v}

        #breakdown by categories and count
        medOptDict = {k:[x for x in drugList if x in v] for k,v in gapNameDict.items() if modelParam['moose_impact_feature_category'][k] == 'med_opt'}

        #iterate through keys of med opt gaps
        for key in medOptDict.keys():

            #iterate through med given
            for value in medOptDict[key]:

                #get drug col
                drugColIter = [x for x in X.columns if 'pdc' in x and value in x]

                #patch for metformin
                if value == 'metformin':
                    drugColIter = ['rx_biguanides_pdc_last_12_month']

                #eliminate cases where no drug listed ( ex. general)
                if len(drugColIter) == 0:
                    continue

                #create column of interest
                X["keepoff_drug_already_on_"+ value+"_x_"+key] = np.where((X[key+"_2"]==1)&(X[drugColIter[0]]>0),True,False)

        #return X with new columns
        return X