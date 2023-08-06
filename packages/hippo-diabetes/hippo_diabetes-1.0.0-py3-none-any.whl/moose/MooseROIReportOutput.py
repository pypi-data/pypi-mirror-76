#imports
import pandas as pd
import numpy as np
import os
from sklearn.base import BaseEstimator, TransformerMixin

#get custom packages
cwd = os.getcwd()
cwdHead = os.getcwd().split("/hippo/")[0]
os.chdir(cwdHead+ '/hippo/src2/util')
from util import UtilAPI
os.chdir(cwd)

class MooseROIReportOutput(BaseEstimator, TransformerMixin):
    """ creates ROI report about the member gap information

    Paramters
    :param X: dataframe of member gap information
    :type X: pd.DataFrame
    :param memberCount: number of unique members in the overall populution
    :type memberCount: int

    :return: ROI Report of the member gap information
    :rtype: string
    """

    def __init__(self,X,memberCount):
        """constructor class
        """
        self.X = X
        self.memberCount = memberCount

    #build out the spacer rows
    def spacerRow(self,title,charWidth=100):

        #add spaces
        title = " " + title + " "

        #return the input row centered and with spacers
        return "-"*int(np.floor((charWidth-len(title))/2)) + title + "-"*int(np.ceil((charWidth-len(title))/2)) +"\n"

    #build and print the report
    def report(self):

        #get modelParam
        modelParam = UtilAPI().modelParam

        #initate string
        report = str()

        ####
        #### input section
        ####
        report += self.spacerRow('INPUTS')

        #go no go
        report += 'Minimum Value/Cost Go-No Go ROI Threshold:'+ str(modelParam['moose_heterogeneity_channel_go_roi_threshold']) +"\n"

        #information about the population

        #commerical inputs
        if modelParam['otter_care_gap_comm_vs_medi_bool'] == 'comm':
            report += 'Estimated PMPM Costs (To the External Client): $'+ str(modelParam['moose_heterogeneity_commerical_cost_pmpm']) +"\n"
            report += 'People with Diabetes In Studied Commercial Population:'+'{:,.0f}'.format(self.memberCount) +"\n"
            report += 'People in total estimated population given {0} share with diabetes:'.format(str( modelParam['moose_heterogeneity_commerical_rate_of_diabetes']))+'{:,.0f}'.format(self.memberCount/modelParam['moose_heterogeneity_commerical_rate_of_diabetes']) +"\n"

        #medicare inputs
        elif modelParam['otter_care_gap_comm_vs_medi_bool'] =='medi':
            report += 'Estimated PMPM Costs : $'+str(modelParam['moose_heterogeneity_medicare_cost_pmpm'])+"\n"
            report += 'People with Diabetes In Studied Medicare Population:'+'{:,.0f}'.format(self.memberCount) +"\n"
            report += 'People in total estimated population given {0} share with diabetes: '.format(str(modelParam['moose_heterogeneity_medicare_rate_of_diabetes']))+'{:,.0f}'.format(self.memberCount/modelParam['moose_heterogeneity_medicare_rate_of_diabetes']) +"\n"

        ####
        ####gap section
        ####
        report += self.spacerRow('GAPS')

        report +='Total Gaps That Could Be Attempted:'+'{:,.0f}'.format(self.X.shape[0] )+"\n"
        report +='Cap on Gaps That Could Be Attempted Per Person:' + str(modelParam['moose_heterogeneity_top_gap_consider'])+"\n"
        report +='Mean Care Gaps Per Person That Could Be Attempted:'+ str(round(len(self.X['care_gap']) /len(list(set(self.X['individual_id']))),2))+"\n"
        report +='Count of Gaps that were attempted at least once:'+'{:,.0f}'.format(self.X['digital'].sum())+"\n"
        report +='Share of Gaps that were attempted at least once:'+'{:,.2f}'.format(100*self.X['digital'].sum()/len(self.X['care_gap']))+"%\n"
        report +='Estimated Count of Gaps Closed:'+'{:,.0f}'.format(self.X['total_close_prob'].sum())+"\n"
        report +='Estimated Share of Gaps Closed:'+'{:,.4f}'.format(self.X['total_close_prob'].sum()/self.X.shape[0] )+"\n"

        ####
        ####value and roi section
        ####
        report += self.spacerRow('VALUE & ROI')

        report += 'Total Estimated Value Generated: $'+'{:,.2f}'.format(round(self.X['total_estimated_value'].sum(),2))+"\n"
        report += 'Total Cost of Attempting to Close Gaps: $'+ '{:,.2f}'.format(round(self.X['total_cost'].sum(),2))+"\n"
        report += 'Internal ROI (Total Estimated Value Generated/Total Cost of Attempting to Close Gaps): '+str(round(self.X['total_estimated_value'].sum()/self.X['total_cost'].sum(),2))+"\n"

        #costs to external clients determined if medicare or commerical
        if modelParam['otter_care_gap_comm_vs_medi_bool'] == 'comm':
            reportCostHolder = 12*modelParam['moose_heterogeneity_commerical_cost_pmpm']*(self.memberCount/modelParam['moose_heterogeneity_commerical_rate_of_diabetes'])
            report += 'Total Cost to External Client: $'+ '{:,.2f}'.format(reportCostHolder)+"\n"

        elif modelParam['otter_care_gap_comm_vs_medi_bool'] =='medi':
            reportCostHolder = 12*modelParam['moose_heterogeneity_medicare_cost_pmpm']*(self.memberCount/modelParam['moose_heterogeneity_medicare_rate_of_diabetes'])
            report += 'Total Cost to External Client: $'+ '{:,.2f}'.format(reportCostHolder)+"\n"

        report += 'External ROI (Total Estimated Value Generated/Total Cost to External Clients): '+'{:,.2f}'.format((self.X['total_estimated_value'].sum()/(reportCostHolder)))+"\n"

        ####
        ####attempts section
        ####
        report += self.spacerRow('ATTEMPTS')

        #iterate through dictioanry values
        for key in modelParam['moose_heterogeneity_channel_dict'].keys():

            #get printable key
            spacerKey = key + "-"*(14-len(key))

            #get the number of care gaps attempted by this channel
            summer = self.X[key].sum()

            #add to the report
            report += spacerKey+ " | attempts made ="+'{:,.0f}'.format(summer) +" | total cost =$ "'{:,.0f}'.format(summer * modelParam['moose_heterogeneity_channel_dict'][key][0]) +"\n"

        ####
        ####channels section
        ####
        report += self.spacerRow('CHANNELS')

        #iterate through channles
        for key in modelParam['moose_heterogeneity_channel_dict'].keys():

            #key with information
            spacerKey = key + "-"*(14-len(key))

            #report
            report += spacerKey + "| Cost Per Attempt |$"+ str(modelParam['moose_heterogeneity_channel_dict'][key][0]) + " | Probability of Closing Gap | "+str(round(100*modelParam['moose_heterogeneity_channel_dict'][key][1],2))+"%\n"

        #print report
        print(report)

        #return report
        return report