import pandas as pd
import unittest
import os

#get classes from moose
from MooseKeeperOffenderTranche import *
from MooseShapImpactOutput import *
from MooseMemberLevelPipeline import *
from MooseROIReportOutput  import *
from MooseMemberGapLevelPipeline import *
from MooseGapOAReportOutput import *

#get custom packages
cwd = os.getcwd()
cwdHead = os.getcwd().split("/hippo/")[0]
os.chdir(cwdHead+ '/hippo/src2/util')
from util import UtilAPI
os.chdir(cwd)

# package for ROI and financial modeling
class MooseAPI:

    # init
    def __init__(self,pdc):

        #holder
        self.realImpact = None

        #egertPDC
        self.pdc = pdc
        pass

    # main
    def moose(self,X):
        #initiate modelParam
        modelParam = UtilAPI().modelParam

        #gather basic data
        #merge on the pdc information (per business request)
        X = pd.merge(X,self.pdc,how="left",on="individual_id")

        #select only specified LOB
        #select only commerical
        if modelParam['otter_care_gap_comm_vs_medi_bool'] =='comm':
            X = X[np.where((X['insure_med_com_full']+X['insure_med_com_self']+X['insure_med_com_split'])==1,True,False)]

        #select only medicare
        elif modelParam['otter_care_gap_comm_vs_medi_bool'] == 'medi':
            X = X[np.where((X['insure_med_med_group']+X['insure_med_med_indiv'])==1,True,False)]

        else:
            unittest.TestCase().assertTrue(False,msg=f"Error in Moose. Neither comm nor medi read in as LOB.")

        #develope outputs

        #keepers and offenders
        X, self.Offender = MooseKeeperOffenderTranche().tranche(X)

        # member level output
        self.MemberLevel  = MooseMemberLevelPipeline().add_pipe().transform(X)

        # heterogenity output
        self.MemberGapLevel = MooseMemberGapLevelPipeline().add_pipe().transform(self.MemberLevel)

        # heterogentiy report output
        self.ROIReport = MooseROIReportOutput(self.MemberGapLevel,X.shape[0]).report()

        # gap level OA output
        self.GapOAReport = MooseGapOAReportOutput(hippo=X,member=self.MemberLevel,memberGap=self.MemberGapLevel).report()
