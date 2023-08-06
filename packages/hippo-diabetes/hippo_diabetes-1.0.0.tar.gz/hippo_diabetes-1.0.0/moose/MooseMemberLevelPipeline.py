#imports
import pandas as pd
import numpy as np
import os
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline

#import packages from this modula
from MooseLineOfBusinessOneColumnTransformer import *
from MooseKeepNamedColumnsTransformer import *
from MooseOpenCareGapImpactListTransformer import *
from MooseShapCostColumnTransformer import *
from MooseColumnMultiplicationTransformer import *
from MooseColumnFillerTransformer import *
from MooseColumnCareGapOpenCountTransformer import *
from MooseListOfTupleLengthTransformer import *
from MooseOpenCareGapImpactListFastTransformer import *
from MooseColumnTypeSetTransformer import *
from MooseColumnMoldMarginalTransformer import *

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

#class
class MooseMemberLevelPipeline(BaseEstimator, TransformerMixin):
    """Get the member level output

    Parameters

    Returns
    :returns: dataframe reorganized to get information reqested for the above specifications
    :rtype: pd.DataFrame
    """

    def __init__(self):
        """constructor method
        """
        pass

    # apply pipe function
    def add_pipe(self):

        #init dict
        modelParam = UtilAPI().modelParam

        #get only the columns of interest including the indicators if any care gap is open or not open
        keepList = (['individual_id','line_of_business','age','total_allowed_usd_one_year']
                    + ['etg_diab_ttl_allw_amt_12mo','etg_chf_ttl_allw_amt_12mo']
                    + [modelParam['hippo_model_outcomeColName']]
                    + [modelParam['hippo_model_outcomeColName']+'_prediction']
                    + ['a1c_type_indicator','a1c_test_ordered']
                    + ['hh_geo_access_april1_2020', 'store_number_april1_2020',
                    'hh_geo_access_sept1_2020', 'store_number_sept1_2020',
                    'hh_geo_access_jan1_2021', 'store_number_jan1_2021']
                    + ['ivr_permissions','dm_permissions',
                    'email_permissions','sms_permissions']
                    + ['rx_count_last6m','maint_rx_at_cvs_last6m',
                    'latest_fill_date_last6m', 'max_supply_days_last6m',
                    'rx_count_last12m','maint_rx_at_cvs_last12m',
                    'latest_fill_date_last12m','max_supply_days_last12m']
                    + ['care_gap_count','top_3_care_gap_100_80_60']
                    + modelParam['egret_anti_diabetic_pdc_drug_columns']
                    + ['care_gap_compact']
                      + modelParam['moose_output_included_care_gap_name'])

        #create all the features of interest
        MemberLevelPipeline = Pipeline(steps=[
            ('MooseLineOfBusinessOneColumnTransformer',MooseLineOfBusinessOneColumnTransformer()),
            ('MooseOpenCareGapImpactListFastTransformer',MooseOpenCareGapImpactListFastTransformer()),
            #('MooseColumnMoldMarginalTransformer',MooseColumnMoldMarginalTransformer()),
            ('MooseShapCostColumnTransformer',MooseShapCostColumnTransformer()),
            ('MooseColumnMultiplication_cost',MooseColumnMultiplicationTransformer('cost_past_total_allowed_amt_pmpm','total_allowed_usd_one_year',12)),
            ('MooseColumnFillerTransformer_a1c_type',MooseColumnFillerTransformer('a1c_type_indicator','actual')),
            ('MooseColumnFillerTransformer_a1c_test_ordered',MooseColumnFillerTransformer('a1c_test_ordered','yes')),
            ('MooseColumnFillerTransformer_accp',MooseColumnFillerTransformer('accp','')),
            ('MooseColumnTypeSetTransformer_individidual_id',MooseColumnTypeSetTransformer('individual_id','str')),
            ('MooseKeepNamedColumnsTransformer',MooseKeepNamedColumnsTransformer(featureNames=keepList))
        ])

        # return pipeline
        return MemberLevelPipeline