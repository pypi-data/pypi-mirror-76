#imports
import pandas as pd
import numpy as np
import itertools
import operator
import unittest
import os
from sklearn.base import BaseEstimator, TransformerMixin

#cmenagerie model imports
cwd = os.getcwd()
cwdHead = os.getcwd().split("/hippo/")[0]

#import hpackages and return to this directo
os.chdir(cwdHead+ '/hippo/src2/util')
from util import UtilAPI

#return to original directory
os.chdir(cwd)

class MooseMemberGapTallTransformer(BaseEstimator, TransformerMixin):
    """To support heterogentiy work, Reorganizes the number of columns specified into one large, tall data frame.  Also converts A1C into dollars.

    :returns: dataframe with only the care gaps in it
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
        :param X: np.array of features of interest for training
        :type X: np.array
        :param y: np.array of features of interest for testing (none in this case)
        :type Y: np.array

        Returns
        :returns: fited data frame
        :rtype: sklearn.base.BaseEstimator
        """
        return self

    #apply the transformation function
    def transform(self, X, y=None):

        #initiate the dictionary
        modelParam = UtilAPI().modelParam

        #build new individual id (repeats for the number of care gaps that are grabbed
        idList = X['individual_id'].tolist()*modelParam['moose_heterogeneity_top_gap_consider']

        #build new output that holds the rank ordering of the care gaps

        #number of ranks considered
        lenHolder = len(X['individual_id'])

        #holds information
        rankList = []

        #iteratively build the rankList
        for i in range(0,modelParam['moose_heterogeneity_top_gap_consider']):

            #ranks (itervely add)
            rankList += [i+1 for x in range(0,lenHolder)]

        #get the care gaps by name and their underpinning shap values
        cgList = []
        shapList = []
        for cg in range(0,modelParam['moose_heterogeneity_top_gap_consider'],1):

            #adjust from zero
            cg1 = str(cg+1)
            cgCol = 'care_gap_name_{0}'.format(cg1)

            #verify that the care gaps of that name are in the member level output, if not break
            if cgCol not in X.columns:

                #break and stop the for loop, no additionsl care gaps can exisist (build up)
                break

            #add in the list of care gap names
            cgList = cgList + X[cgCol].tolist()

            #add in the list of care gap shap values (scaled apprirotiely)
            shapScaler = float(modelParam['moose_heterogeneity_gap_rank_proportional_value'][f'care_gap_{cg1}'])
            shapList = shapList + [x*shapScaler for x in X[f'care_gap_member_shap_delta_{cg1}'].tolist()]

        #shap conversion to usd (scale from month to year)

        #commerical conversion
        if modelParam['otter_care_gap_comm_vs_medi_bool'] == 'comm':
            shapList = [x*(modelParam['moose_a1c_one_point_drop_usd_pppm_commerical']*12) for x in shapList]

        #medicare conversion
        elif modelParam['otter_care_gap_comm_vs_medi_bool'] == 'medi':
            shapList = [x*(modelParam['moose_a1c_one_point_drop_usd_pppm_medicare']*12) for x in shapList]

        #error
        else:
            #assert error
            unittest.TestCase().assertTrue(False,msg='''Error: MooseMemberGapTallTransformer in Moose. Shap to $USD conversion not inputted neither comm or medi''')

        #put it all together
        returnX = pd.DataFrame(zip(idList,cgList,shapList,rankList),columns = ['individual_id','care_gap','value','rank'])

        #drop nulls
        returnX = returnX[[True if pd.notnull(x) else False for x in returnX['care_gap']]].reset_index(drop=True)

        #return the member gap level information
        return returnX