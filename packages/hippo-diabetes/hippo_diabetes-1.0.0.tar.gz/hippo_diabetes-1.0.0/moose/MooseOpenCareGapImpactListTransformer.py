#imports
import pandas as pd
import numpy as np
import itertools
import operator
import os
from sklearn.base import BaseEstimator, TransformerMixin

#get the impact from the current model
from MooseShapImpactOutput import MooseShapImpactOutput

#cmenagerie model imports
cwd = os.getcwd()
cwdHead = os.getcwd().split("/hippo/")[0]

#import hpackages and return to this directo
os.chdir(cwdHead+ '/hippo/src2/util')
from util import UtilAPI

#return to original directory
os.chdir(cwd)

class MooseOpenCareGapImpactListTransformer(BaseEstimator, TransformerMixin):
    """Function retains only the care gap columns
    :param featureNames: column for name of care gap
    :type featureNames: string

    :returns: dataframe with only the care gaps in it
    :rtype: pd.DataFrame
    """

    def __init__(self,careGapList=None):
        """constructor method
        """
        if careGapList is None:
            self.careGapList = UtilAPI().modelParam['moose_impact_feature_list']
        else:
            self.careGapList = careGapList

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

    def spacerFiller(self,careGapList,maxLen):
        """ insure that we have a standardized and complete operating surface for splitting out the care gaps into multiple columns

        Parameters:
        :param careGapList: list of tuples of open care gaps (each tuple holds (care gap ###, care gap short name, shap impact, lit impact))
        :type careGapList: list
        :param maxLen: the highest count of open care gaps of any individual
        :type maxLen: integer

        Return:
        :return: list of tuples of open care gaps and spacers
        :rtype: list

        """
        # spacer
        spacerTuple = [None,None,None,None,None]

        #figure out how  many to add
        adder = [spacerTuple for y in range(0,maxLen-len(careGapList))]

        #put together with current knowledge where available
        #surface nothing when no care gaps open
        if len(careGapList) == 0:
            return adder

        #surface the open care gaps plus spacers when needed
        else:
            return careGapList + adder

    #helper function for transform
    def lowShapThresholdEnforcer(self,v,threshold):
        if v <= threshold:
            return(threshold)
        else:
            return v


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

        #get columns of interest (care gaps)
        careGap2 =self.careGapList

        ####
        #### get the real value and lit values impacts
        ####

        #specify dictionaries
        modelParam = UtilAPI().modelParam
        realDict = MooseShapImpactOutput(X).ShapImpactDict
        litDict = modelParam['moose_impact_feature_lit_value']
        nameDict = modelParam['moose_impact_feature_name']

        # opened limit down to only the columns of interst (opens and shaps)
        openCloseList = [x+"_2" for x in careGap2]
        shapList = [x+"_2_shap" for x in careGap2]
        XSmall=X[openCloseList+shapList]

        #for each shap value get the lowest nonzero value
        lowShapThresholdDict = {}
        for col in shapList:

            #if none open then impact is zero
            if len([x for x in X[col[:-5]]if x==1])==0:
                minHolder = 0

            #if there is at least one person with the care gap open
            else:
                minHolder = np.min([x[0] for x in zip(X[col],X[col[:-5]]) if x[1]==1])

            #make sure minHolder is at or above zero
            if minHolder < 0:
                minHolder = 0

            #put into dictionary
            lowShapThresholdDict[col] = minHolder

        #rename lowShapThresholdDict to make more streamlined around cg names
        lowShapThresholdDict = {k[:-7]:v for k,v in lowShapThresholdDict.items()}

        #holder for meta information
        metaList = []
        #get only the care gaps that are open for each person
        for row in XSmall.itertuples(index=False):

            #dictionary comprehensio
            rowAll = {k:v for k, v in zip(XSmall.columns,row)}

            #split rowAll into care gaps whose values are none zero
            rowCareGapValues = {k:v for k,v in rowAll.items() if float(v) == 1 and "_shap" not in k}

            #for open care gaps get the values for the accompanying shaps
            rowShapValue = {k:v for k,v in rowAll.items() if k[:-5] in rowCareGapValues.keys()}

            #clean up the keys for both dicts
            rowCareGapValues = {k[:-2]:v for k,v in rowCareGapValues.items()}
            rowShapValue = {k[:-7]:v for k,v in rowShapValue.items()}

            #make sure the rowShapvalues abide by the lowShapThreshold
            rowShapValue = {k:self.lowShapThresholdEnforcer(v,lowShapThresholdDict[k]) for k,v in rowShapValue.items()}

            #iterate through care gaps
            rowOpenHolder = []
            for cg in rowCareGapValues.keys():

                #append iteratively
                rowOpenHolder.append([cg,nameDict[cg],realDict[cg],litDict[cg],rowShapValue[cg]])#rowShapValue[cg]])

            #order properly (3 means order by lit values) (2 orders by general values) (4 orders by member values
            rowOpenHolder = sorted(rowOpenHolder, key=operator.itemgetter(4),reverse=True)

            #put together
            metaList.append(rowOpenHolder)

        #input
        ####
        #### create the compact list of all information (dense)
        ####
        X['care_gap_compact'] = metaList

        ####
        #### create the sparse list of care gaps that are spread out
        ####

        #list of information
        openCareGapCompact = X['care_gap_compact'].tolist()

        #max number of iterations
        maxLenHolder = np.max([len(y) for y in openCareGapCompact])

        #apply the spacing so all lists are the same
        openCareGapCompact = [self.spacerFiller(x,maxLenHolder) for x in openCareGapCompact]

        #for loop of information from the first care gap to the max amount
        for rankr in range(0,maxLenHolder):

            #split out information into multiple columns (with headers to insure proper formatin).  These columns hold the apprioriate information
            careGapHolder = ['care_gap']
            careGapNameHolder = ['care_gap_name']
            careGapShapImpactHolder = [0.0]
            careGapLitImpactHolder = [0.0]
            careGapMemberImpactHolder = [0.0]

            #populate with list comprension multiple times for sake of simplity.  Putting together in one large list seems to create errors.
            [ careGapHolder.append(z[rankr][0]) for z in openCareGapCompact]
            [ careGapNameHolder.append(z[rankr][1]) for z in openCareGapCompact]
            [ careGapShapImpactHolder.append(z[rankr][2]) for z in openCareGapCompact]
            [ careGapLitImpactHolder.append(z[rankr][3]) for z in openCareGapCompact]
            [ careGapMemberImpactHolder.append(z[rankr][4]) for z in openCareGapCompact]

            #push back together as dataframe
            cgSmallCol = ['care_gap_{0}'.format(str(rankr+1)),
                          'care_gap_name_{0}'.format(str(rankr+1)),
                          'care_gap_member_shap_delta_{0}'.format(str(rankr+1)),
                          'care_gap_average_shap_delta_{0}'.format(str(rankr+1)),
                          'care_gap_lit_delta_{0}'.format(str(rankr+1))]
            cgSmall = pd.DataFrame(zip(careGapHolder,
                                       careGapNameHolder,
                                       careGapMemberImpactHolder,
                                       careGapShapImpactHolder,
                                       careGapLitImpactHolder),columns=cgSmallCol)

            #drop the header formating row
            cgSmall = cgSmall.iloc[1:,:].reset_index(drop=True)

            #create larger frame by iteratively adding columns as needed
            if rankr == 0:
                cgLarge = cgSmall
            else:
                cgLarge = pd.merge(cgLarge,cgSmall,how="inner",left_index=True,right_index=True)

        #merge back the columns of interest into the overall dataframe
        X[cgLarge.columns] = cgLarge[cgLarge.columns]

        # return only those that have the columns of interest
        return X