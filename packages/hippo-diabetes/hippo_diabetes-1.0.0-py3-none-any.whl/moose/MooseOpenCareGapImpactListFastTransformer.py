#imports
import pandas as pd
import numpy as np
import itertools
import operator
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

class MooseOpenCareGapImpactListFastTransformer(BaseEstimator, TransformerMixin):
    """Function that creates and organizes the infomration about care gaps

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
        """function to select only the columns of interest about the care gaps and their formal names, shap, lit, and average values

        Parameters
        :param X: np.array of features of interest for training
        :type X: np.array
        :param y: np.array of features of interest for testing (none in this case)
        :type Y: np.array

        :returns: dataframe
        :rtype: pd.DataFrame
        """

        ####
        #### set up
        ####

        #setup model Param
        modelParam = UtilAPI().modelParam

        ####
        #### open and close columns
        ####
        #open and close columns locations
        colLoc = [X.columns.get_loc(c) for c in X.columns if 'care_gap' in c and c[-2:]=='_2']

        #names of the open couls
        colName = np.array([c for c in X.columns if 'care_gap' in c and c[-2:]=='_2'])

        ####
        #### shap columns
        ####

        #shap values (sometimes of the open and close columns)
        #locations of columns of interest
        colShapLoc = [X.columns.get_loc(c) for c in X.columns if 'care_gap' in c and c[-7:]=='_2_shap']

        #open names
        colShapName = np.array([c for c in X.columns if 'care_gap' in c and c[-7:]=='_2_shap'])

        ####
        #### care gaps that are open and shut
        ####

        #boolean mask
        XOpenMask = X.values[:,colLoc] == 1
        
        #which gaps are opne
        # create matrix of column names of length = # rows
        c = np.tile(colName[np.newaxis,:], (X.shape[0],1))

        # do mask on row basis
        member_gaps = [c[i][XOpenMask[i]] for i in range(XOpenMask.shape[0])]

        ####
        #### member level shap values
        ####

        #get array of all shap values (based on the column names )
        #values of the open gaps
        member_shaps_all = X.values[:,colShapLoc]
        
        #insure that the members shap values are in acceptable range, starting with taking the min
        min_shaps_by_col = member_shaps_all.min(axis=0)
      
        #band
        members_shaps_all_up = np.array([np.subtract(member_shaps_all[:,i],min_shaps_by_col[i]) for i in range(min_shaps_by_col.shape[0])])

        #transpose for ease of use
        members_shaps_all_up = members_shaps_all_up.transpose()

        #means of shap values (later used in the dictionary)
        members_shaps_all_up_mean = members_shaps_all_up.mean(axis=0)

        #upodate shaoe vakyes apprruateky
      
        member_shaps = [members_shaps_all_up[i][XOpenMask[i]] for i in range(XOpenMask.shape[0])]

        ####
        #### literature a1c values
        ####

        #pull in dictionary of values
        litDict = modelParam['moose_impact_feature_lit_value']

        #relative to col name, pull in the names in order
        litName = np.array([litDict[x[:-2]] for x in colName])

        #create large array of all the lit values
        
        lit_values_all = np.tile(litName[np.newaxis,:], (X.shape[0],1))

        #boolean mask the proper values
        lit_values = [lit_values_all[i][XOpenMask[i]] for i in range(XOpenMask.shape[0])]

        ####
        #### average shape values
        ####

        #create a dictionary of the average shap values (assumes that the shap values have already been banded )
        #banded means come from members_shaps_all_up_mean when shap values are banded
        generalShapDict = {k[:-5]:v for k,v in zip(colShapName,members_shaps_all_up_mean)}

        #based on col name, create and array of the all the shap dict values
        generalName = np.array([generalShapDict[x] for x in colName])

        #create large array of average care gap values
        general_values_all = np.tile(generalName[np.newaxis,:], (X.shape[0],1))

        #boolen mask to get the proper values
        general_values = [general_values_all[i][XOpenMask[i]] for i in range(XOpenMask.shape[0])]

        ####
        #### long names
        ####

        #pull in the banes of the care gaps
        longNameDict = {k+"_2":v for k,v in modelParam['moose_impact_feature_name'].items()}

        #relative to col name, pull in the names in order
        longName = np.array([longNameDict[x] for x in colName])

        #create large array only of the formal namnes
        long_name_all = np.tile(longName[np.newaxis,:], (X.shape[0],1))

        #get the data frame of the names
        long_name = [long_name_all[i][XOpenMask[i]] for i in range(XOpenMask.shape[0])]

        ####
        #### sort and organize columns by member level shap values
        ####

        #function to sort gaps
        def argSorter(sorter,sortee):
            return sortee[sorter.argsort()[::-1]]

        #organize each and every array by shap values
        member_gaps = [argSorter(member_shaps[i],member_gaps[i]) for i in range(XOpenMask.shape[0])]
        lit_values = [argSorter(member_shaps[i],lit_values[i]) for i in range(XOpenMask.shape[0])]
        general_values = [argSorter(member_shaps[i],general_values[i]) for i in range(XOpenMask.shape[0])]
        long_name = [argSorter(member_shaps[i],long_name[i]) for i in range(XOpenMask.shape[0])]

        #finally order the member shapes as well
        member_shaps = [argSorter(member_shaps[i],member_shaps[i]) for i in range(XOpenMask.shape[0])]

        ####
        #### get the count of open care gaps
        ####

        cg_care_gap_cnt = [len(x) for x in member_gaps]

        ####
        #### top 3 gap value
        ####

        #average value of shaps
        index_s = []
        cg_names = []
        cg_sum_3 = []

        #iterate through member shaps
        for row in member_shaps:
            top_3_index = row.argsort()[-3:][::-1]
            index_s.append(top_3_index)
            top_3_cg_names = np.array(colName)[top_3_index]
            cg_names.append(top_3_cg_names)

            if len(row[top_3_index]) == 3:
                top_3_sum = np.multiply(row[top_3_index], [1,0.8,0.6]).sum()
            elif len(row[top_3_index]) == 2:
                top_3_sum = np.multiply(row[top_3_index], [1,0.8]).sum()
            elif len(row[top_3_index]) == 1:
                top_3_sum = np.multiply(row[top_3_index], [1]).sum()
            else:
                top_3_sum = 0

            cg_sum_3.append(top_3_sum)

        ####
        #### output section
        ####

        #data frame the care gap name columns
        member_gaps_df = pd.DataFrame(member_gaps)
        member_gaps_df.columns = [f'care_gap_{str(x+1)}' for x in range(member_gaps_df.shape[1])]

        #data frame of the care gaps formal names
        long_name_df = pd.DataFrame(long_name)
        long_name_df.columns = [f'care_gap_name_{str(x+1)}' for x in range(long_name_df.shape[1])]

        #data farme the care gap shap columns
        member_shaps_df = pd.DataFrame(member_shaps)
        member_shaps_df.columns = [f'care_gap_member_shap_delta_{str(x+1)}' for x in range(member_shaps_df.shape[1])]

        #data frane the average values of the care gaps
        general_values_df = pd.DataFrame(general_values)
        general_values_df.columns = [f'care_gap_average_shap_delta_{str(x+1)}' for x in range(general_values_df.shape[1])]

        #data frane the lit values of the columns
        lit_values_df = pd.DataFrame(lit_values)
        lit_values_df.columns = [f'care_gap_lit_delta_{str(x+1)}' for x in range(lit_values_df.shape[1])]

        #put into massive dataframe
        outputDF = pd.concat([member_gaps_df,long_name_df,member_shaps_df,general_values_df,lit_values_df],axis=1)

        #reorder columns as needed
        outputDF = outputDF[[x for x in modelParam['moose_output_included_care_gap_name'] if x in outputDF.columns]]

        #at the front insert the additional columns needed (care gap count and top three care gap value)
        outputDF.insert(0, 'top_3_care_gap_100_80_60', cg_sum_3)
        outputDF.insert(0, 'care_gap_count', cg_care_gap_cnt)

        #### return (along with orginal output)
        return pd.concat([X,outputDF],axis=1).reset_index(drop=True)