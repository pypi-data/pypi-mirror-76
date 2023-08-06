#imports
import os
import pandas as pd
import numpy as np
import unittest
import itertools
from sklearn.base import BaseEstimator, TransformerMixin

#get custom packages
cwd = os.getcwd()
cwdHead = os.getcwd().split("/hippo/")[0]
os.chdir(cwdHead+ '/hippo/src2/util')
from util import UtilAPI
os.chdir(cwd)

class MooseKeeperOffenderMutuallyExclusiveTransformer(BaseEstimator, TransformerMixin):
    """ based on gaps that are mutually exclusive, identify members

    :returns: dataframe with all member level and new flag if they are a duplicate
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

        #setup
        #information from model Param needed for tis
        modelParam = UtilAPI().modelParam

        #information holders
        #med opt vs med adh mutually exclusive pairings holder
        mutExMedAdhList = []

        #med opt exclusive pairiings within each specific line
        medOptLineList = []

        #information about med opt gaps firing in multiple lines at the same time
        multiLineFiringList = []

        #get list of care gaps and their names that are in X (exclude care considerations, no deep understand of that logic)
        gapNameDict = {k:v for k,v in modelParam['moose_impact_feature_name'].items() if k+"_2" in X.columns and 'cc' not in v}

        #breakdown by categories
        medOptDict = {k:v for k,v in gapNameDict.items() if modelParam['moose_impact_feature_category'][k] == 'med_opt'}
        medAdhDict = {k:v for k,v in gapNameDict.items() if modelParam['moose_impact_feature_category'][k] == 'med_adh'}

        #med adh mut ex vs med opt
        #get mutually exclusive pairing between med opt and med adh
        for drug in ['alpha_glucose','metformin','dpp4','glp1','meglitinide','sglt2','sulfonylureas','tdz','insulin','statins']:
            for opt in [k for k,v in medOptDict.items() if drug in v]:
                for adh in [k for k,v in medAdhDict.items() if drug in v]:
                    mutExMedAdhList.append([opt,adh])

        #make sure that the care gaps are firing at the proper rank
        #get the number pairings
        numList = ['_one_','_two_','_three_','_four_']
        for num in numList:

            #iterate through eeach dictionare twice
            for opt1 in medOptDict.values():
                for opt2 in medOptDict.values():

                    #skip over identical pairs
                    if opt1 == opt2:
                        continue

                    #skip over general (these gaps are never exclusive)
                    if 'general' in opt1 or 'general' in opt2:
                        continue

                    #for specific lines only
                    #in cases where the number is in both med opt gaps (indicating the line fired) make sure they are mutually exclusive
                    if num in opt1:
                        if num in opt2:

                            #make sure not already in the list
                            if sorted([opt1,opt2]) not in medOptLineList:

                                #otherwise append
                                medOptLineList.append(sorted([opt1,opt2]))

        #crosswalk the names back into the care gaps
        medOptDictReverse = {v:k for k,v in medOptDict.items()}
        medOptLineList = [[medOptDictReverse[x[0]],medOptDictReverse[x[1]]] for x in medOptLineList]


        #multiline firing list
        #get the list of gaps that are mutuually exclusive across different lines of business
        oneHolder = [k for k,v in medOptDict.items() if '_one_' in v]
        twoHolder = [k for k,v in medOptDict.items() if '_two_' in v]
        threeHolder = [k for k,v in medOptDict.items() if '_three_' in v]
        fourHolder = [k for k,v in medOptDict.items() if '_four_' in v]

        #for
        for first in [oneHolder,twoHolder,threeHolder,fourHolder]:
            for second in [oneHolder,twoHolder,threeHolder,fourHolder]:
                if first != second:

                    #create list
                    shortMultiLineFiringList = list(itertools.product(first, second))

                    #iterateively append values that do not exisits
                    for v in shortMultiLineFiringList:
                        if sorted(list(v)) not in multiLineFiringList:
                            multiLineFiringList.append(sorted(list(v)))

        #convert to lists (malable)
        #push all the mutually exclusive list together (insure no duplicates )
        mutExList = []
        for x in (mutExMedAdhList + medOptLineList+multiLineFiringList):
            if sorted(x) not in mutExList:
                mutExList.append(x)

        #create columns for each pair
        for pair in mutExList:

            #create new columns for each pair
            X['keepoff_mut_ex_'+pair[0]+"_x_"+pair[1]] = np.where((X[pair[0]+"_2"]==1) & (X[pair[1]+"_2"]==1),True,False)


        #return X
        return X
