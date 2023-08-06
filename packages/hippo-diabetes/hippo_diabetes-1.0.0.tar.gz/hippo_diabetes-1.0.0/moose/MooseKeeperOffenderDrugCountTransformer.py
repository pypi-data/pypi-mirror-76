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
os.chdir(cwdHead+ '/hippo/src2/otter')
from otter import OtterAPI
from OtterFeatureSelector import OtterFeatureSelector
os.chdir(cwdHead+ '/hippo/src2/util')
from util import UtilAPI
#return to original directory
os.chdir(cwd)

class MooseKeeperOffenderDrugCountTransformer(BaseEstimator, TransformerMixin):
    """verify that people are firing for the correct level (one, two, three, four) of med opts

    :returns: dataframe with all member level and new flags if they are firing for the wrong count of drugs
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

    def drugCounter(self,x):
        """find the level of the drug

        :param x: med opt drug column for analysis
        :type x: st

        :return: level of drug (1,2,3,4)
        :rtype: int
        """
        if '_one_' in x:
            return 0
        elif '_two_' in x:
            return 1
        elif '_three_' in x:
            return 2
        elif '_four_' in x:
            return 3

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

        #get list of col drugs (statins excluded, not an anti-diabetic drug)
        drugColList = [col for col in X.columns if 'pdc' in col and 'statins' not in col and 'shap' not in col]

        #build indicator of the number of drugs per person
        memberDrugCount = np.where((pd.notna(X[drugColList])) &(X[drugColList]>0),1,0).sum(axis=1)

        #build dictionary for the number of care gaps of med opt that are being called
        #get list of care gaps and their names that are in X (exclude care considerations, no deep understand of that logic)
        gapNameDict = {k:v for k,v in modelParam['moose_impact_feature_name'].items() if k+"_2" in X.columns and 'cc' not in v}

        #breakdown by categories and count
        medOptDict = {k:self.drugCounter(v) for k,v in gapNameDict.items() if modelParam['moose_impact_feature_category'][k] == 'med_opt'}

        #iterate and create the columns of interest
        for cg,count in medOptDict.items():

            #apply boolean fitler
            X['keepoff_drug_count_mismatch_'+cg] = np.where((X[cg+"_2"]==1)&(memberDrugCount!=count),True,False)

        #return X with new column
        return X