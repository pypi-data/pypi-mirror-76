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


class MooseShapCostColumnTransformer(BaseEstimator, TransformerMixin):
    """Function to convert a1c impact into cash columns

    :returns: dataframe with additional colulmns of the a1c value
    :rtype: pd.DataFrame
    """

    def __init__(self):
        """constructor method
        """
        modelParam = UtilAPI().modelParam

        #columns of interest to create
        self.usdImpactColumns =[ x for x in modelParam['moose_output_included_care_gap_name'] if '_usd_' in x]

        #columns of interest that they are based on
        self.bioMarkerImpactColumns =[ x for x in modelParam['moose_output_included_care_gap_name'] if '_a1c_' in x]

        #cost  conversion from a1c
        self.a1cUSDCommericalRate = modelParam['moose_a1c_one_point_drop_usd_pppm_commerical']
        self.a1cUSDMedicareRate   = modelParam['moose_a1c_one_point_drop_usd_pppm_medicare']


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
        #reimport dictionary (?)
        modelParam = UtilAPI().modelParam

        #slim down number of columns to the ones that exisist
        costCol = [x for x in zip(self.bioMarkerImpactColumns,self.usdImpactColumns) if x[0] in X.columns]

        #create the columns of interest
        comList = [x for x in modelParam['moose_lob_column_dict'].values() if 'commercial' in x]
        for colPair in costCol:

        #create the new column of wealth the is determined by the line of business
            X[colPair[1]] = [x[0]*modelParam['moose_a1c_one_point_drop_usd_pppm_commerical'] if x[1] in comList else x[0]*modelParam['moose_a1c_one_point_drop_usd_pppm_medicare'] for x in zip(X[colPair[0]],X['line_of_business'])]

        #return X
        return X