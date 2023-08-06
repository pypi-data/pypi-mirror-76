#imports
import pandas as pd
import numpy as np
import os
from sklearn.base import BaseEstimator, TransformerMixin

#get custom packages
cwd = os.getcwd()
cwdHead = os.getcwd().split("/hippo/")[0]

os.chdir(cwdHead+ '/hippo/src2/otter')
from OtterFeatureSelector import OtterFeatureSelector
os.chdir(cwdHead+ '/hippo/src2/util')
from util import UtilAPI
os.chdir(cwd)

#class
class MooseShapImpactOutput(BaseEstimator, TransformerMixin):
    """Create DataFrame and Dictionary and table of average impact of shap for each gap

    Parameters

    Returns
    :returns: dictionary with the average impact for each care gap
    :rtype: dictionary
    """

    # Class Constructor
    def __init__(self,X):
        """
        Parameters
        :param X: np.array of features of interest for training
            :type X: np.array

        :returns

        """
        ####
        #### read in data frame
        ####
        self.X = X

        ####
        #### find the impacts and build data frame
        ####

        #find the impacts
        #retrieve model params
        modelParam = UtilAPI().modelParam

        #columns with indicators if they have the care gap or not
        careGapCol = modelParam['moose_impact_feature_list']

        #get the names of the relevant columns
        careGapColOpen = [x+"_2" for x in careGapCol]
        careGapColClose = [x+"_1" for x in careGapCol]

        #get the shaps for the impact
        careGapColOpenShap = [x+"_2"+modelParam['hippo_model_impact_label'] for x in careGapCol]

        #select down to the columns of interest
        self.X = OtterFeatureSelector(careGapColOpen+careGapColClose+careGapColOpenShap).transform(self.X)

        #impact holder
        impactHolderOpen = []
        impactHolderClose = []

        #get the means for each feature that is open
        #gets the care gap, care gap shap, count, and the mean
        for col in zip(careGapColOpen,careGapColOpenShap):

            #get all the shap values where the cg is open
            openShap = [x[1] for x in zip(self.X[col[0]],self.X[col[1]]) if x[0] == 1]

            #zero out if none exisits
            if len(openShap) == 0:
                openShap = [0]

            #find the min (and boost to zero if below zero
            openShapMin = np.min(openShap)
            if openShapMin > 0:
                openShapMin = 0

            #replace all openShap values that are below the min with the min
            openShap = [x if x >= openShapMin else openShapMin for x in openShap]

            #get the mean impact for each opened gap where the gap is open
            impactHolderOpen.append([col[0],np.mean(openShap)])

        #get into pandas data frame so we can merge
        impactHolderOpen = pd.DataFrame(impactHolderOpen,columns =['care_gap','mean_open_a1c_shap'])
        impactHolderOpen['care_gap'] = [x[:-2] for x in impactHolderOpen['care_gap']]

        #get the means for each features that is closed
        for col in zip(careGapColClose,careGapColOpenShap):

            #get the mean impact for each opened gap where the gap is open
            impactHolderClose.append([col[0],np.mean([x[1] for x in zip(self.X[col[0]],self.X[col[1]]) if x[0] == 1])])

        #get into pandas dataframe so we can merge
        impactHolderClose = pd.DataFrame(impactHolderClose,columns =['care_gap','mean_close_a1c_shap'])
        impactHolderClose['care_gap'] = [x[:-2] for x in impactHolderClose['care_gap']]

        #merge and flatten down
        impactHolder = pd.merge(impactHolderOpen,impactHolderClose,how="left",on="care_gap").fillna(0)

        #get the impact of closing each gap
        impactHolder['mean_delta_a1c_shap'] = impactHolder['mean_open_a1c_shap'] - impactHolder['mean_close_a1c_shap']

        #set attribute
        self.ShapImpact = impactHolder

        ####
        #### build dictionary of just the impacts
        ####
        self.ShapImpactDict = dict(zip(impactHolder['care_gap'],impactHolder['mean_delta_a1c_shap']))

        ####
        ####
        ####

        ####
        #### clear out data to minimize memory size
        ####
        self.X = None

        ####
        #### return
        ####

