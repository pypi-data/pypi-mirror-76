#imports
import pandas as pd
import numpy as np
import os
import unittest
import xlsxwriter
import datetime
from sklearn.base import BaseEstimator, TransformerMixin
import string

#get custom packages
cwd = os.getcwd()
cwdHead = os.getcwd().split("/hippo/")[0]
os.chdir(cwdHead+ '/hippo/src2/util')
from util import UtilAPI
os.chdir(cwd)

#class
class MooseGapOAReportOutput(BaseEstimator, TransformerMixin):
    """Create DataFrame and Dictionary and table of average impact of shap for each gap

    Parameters
    :param hippo: output from hippo (combinded with columns from self.egret)
    :type hippo: pd.DataFrame
    :param member: Member level rollup of the gaps
    :type member: pd.DataFrame
    :param memberGap: For open gaps, a gap level output (from the heterogenity work)
    :type memberGap: pd.DataFrame

    Returns
    :returns: gap level oa output
    :rtype: gap level oa output
    """

    # Class Constructor
    def __init__(self,hippo,member,memberGap):

        #initialize
        self.hippo = hippo
        self.member = member
        self.memberGap =memberGap

    #get all the future column positions
    def excelColList(self):
        """
        Generates list of the columns at the head of the excel for each column

        :return: all the excel columns
        :rtype: list
        """

        #result list
        resultList = []

        #charList Based 1
        oneChar = [x for x in string.ascii_uppercase]

        #get the one char elements
        oneCharResultList = [x+":"+x for x in oneChar]

        #itearte
        for first in oneChar:
            for second in oneChar:
                resultList.append(first+second+":"+first+second)

        #add on the
        resultList = oneCharResultList+resultList

        #return
        return resultList

    #build excel
    def excel(self,X,considerRank):

        #get modelParam
        modelParam = UtilAPI().modelParam

        #initialize xlsx
        #label at the time
        now = str(datetime.datetime.now().year)+"-"+str(datetime.datetime.now().month)+"-"+str(datetime.datetime.now().day)
        nowFile = modelParam['otter_care_gap_comm_vs_medi_bool'] + '_oa_{}.xlsx'.format(now)

        # develop workbook
        writer = pd.ExcelWriter(nowFile, engine='xlsxwriter')
        workbook = writer.book

        #standard width
        standHeight = 25
        standWidth = 12

        #set formats in workbook to use
        #text size
        formatHeader = workbook.add_format({'valign':'center','text_wrap': True,'bottom':2})
        formatText = workbook.add_format({'valign':'right','text_wrap': True,'text_wrap': True,})
        formatTextLeft = workbook.add_format({'valign':'left','text_wrap': True,'text_wrap': True,})
        formatNumber = workbook.add_format({'num_format': '###,###,###,##0','valign':'right','text_wrap': True,})
        formatPercent = workbook.add_format({'num_format': '0.00%','valign':'right','text_wrap': True,})
        formatDollar = workbook.add_format({'num_format': '$###,###,###,##0','valign':'right','text_wrap': True,})
        formatCent   = workbook.add_format({'num_format':'$###,###,###,###0.00','text_wrap': True,})
        formatDecimal = workbook.add_format({'num_format': '#.##','valign':'right','text_wrap': True,})

        #specify dictionary that has all the details needed for making the spreadsheet
        #values
        #0 = format
        #1 = width given
        #2 = name of column in excel

        # get the positions
        rankPosList = self.excelColList()

        #populate
        columnDict = {}
        columnDict['care_gap'] = [formatText,standWidth*2, rankPosList.pop(0)]
        columnDict['care_gap_name'] = [formatText,standWidth*4, rankPosList.pop(0)]
        columnDict['care_gap_category'] = [formatText,standWidth, rankPosList.pop(0)]
        columnDict['care_gap_category_med_opt'] = [formatText,standWidth*2, rankPosList.pop(0)]
        columnDict['open_count'] = [formatNumber,standWidth, rankPosList.pop(0)]
        columnDict['close_count'] = [formatNumber,standWidth, rankPosList.pop(0)]
        columnDict['eligible_count'] = [formatNumber,standWidth, rankPosList.pop(0)]
        columnDict['ineligible_count'] = [formatNumber,standWidth, rankPosList.pop(0)]
        columnDict['total_count'] = [formatNumber,standWidth, rankPosList.pop(0)]
        columnDict['open_share'] = [formatPercent,standWidth, rankPosList.pop(0)]
        columnDict['close_share'] = [formatPercent,standWidth, rankPosList.pop(0)]
        columnDict['eligible_share'] = [formatPercent,standWidth, rankPosList.pop(0)]
        columnDict['ineligible_share'] = [formatPercent,standWidth, rankPosList.pop(0)]
        columnDict['total_share'] = [formatPercent,standWidth, rankPosList.pop(0)]
        columnDict['total_mean_shap_a1c'] = [formatDecimal,standWidth, rankPosList.pop(0)]
        columnDict['total_std_shap_a1c'] = [formatDecimal,standWidth, rankPosList.pop(0)]
        columnDict['total_expected_value'] = [formatDollar,standWidth, rankPosList.pop(0)]
        columnDict['top_3_rank_expected_value'] = [formatDollar,standWidth, rankPosList.pop(0)]
        columnDict['total_weighted_mean_expected_value'] = [formatDollar,standWidth, rankPosList.pop(0)]

        #for the ranks add in iteratively
        for r in range(1,considerRank+1):

            #string of rank
            rs = str(r)

            #populate dictionary of information related to ranks
            columnDict[f'rank_{rs}_care_gap_open_total_count_potential']=[formatNumber,standWidth, rankPosList.pop(0)]
            columnDict[f'rank_{rs}_care_gap_open_total_share_potential']=[formatPercent,standWidth,  rankPosList.pop(0)]
            columnDict[f'rank_{rs}_care_gap_open_mean_value_potential']=[formatDollar,standWidth,  rankPosList.pop(0)]
            columnDict[f'rank_{rs}_care_gap_open_total_count_expected']=[formatNumber,standWidth,  rankPosList.pop(0)]
            columnDict[f'rank_{rs}_care_gap_open_total_share_expected']=[formatPercent,standWidth, rankPosList.pop(0)]
            columnDict[f'rank_{rs}_care_gap_open_mean_value_expected']=[formatDollar,standWidth,  rankPosList.pop(0)]
            columnDict[f'rank_{rs}_care_gap_open_mean_success_probability']=[formatPercent,standWidth, rankPosList.pop(0)]
            columnDict[f'rank_{rs}_care_gap_open_mean_communication_cost']=[formatCent,standWidth, rankPosList.pop(0)]

        #develope new copy of X for presentation
        XPres = pd.DataFrame(X.values,columns=X.columns)
        XPres.columns = [x.replace("_"," ") for x in XPres.columns]

        #create the execlel doument and point to it
        sheetName = modelParam['otter_care_gap_comm_vs_medi_bool']+"_gap_level"
        XPres.to_excel(writer,sheetName,index=False,index_label=False)
        worksheet = writer.sheets[sheetName]

        #populate care gaps from the columnDict dictionary
        for col in X.columns:

            #set worksheet columns
            worksheet.set_column(columnDict[col][2],columnDict[col][1],columnDict[col][0])

        #freeze first column and first two rows
        worksheet.freeze_panes(1, 2)

        #close workbook
        workbook.close()

    #build csv
    def report(self,save=False):
        ####
        #### setup
        ####

        #get modelParam
        modelParam = UtilAPI().modelParam

        #get the report
        XReport = pd.DataFrame()

        ####
        #### basic information - gap and name (based on LOB
        ####
        #get the care gaps and the care gap names

        #get the information to filter the dictionary
        lobIndictator = modelParam['otter_care_gap_comm_vs_medi_bool']

        #commerical
        if lobIndictator == 'comm':

            #build reverse indicator to eliminate care gaps from other LOB
            inverseLobIndictator ='_medi'

        #medicare
        elif lobIndictator == 'medi':

            #build reverse indicator to eliminate care gaps from other LOB
            inverseLobIndictator ='_comm'

        else:
            #else send out an error
            unittest.TestCase().assertTrue(False,msg="Error in MooseGapOAReportOutput of Moose.  LOB not medi or comm")

        #filter the dictionary, include both (niether medi nor comm) and do not have excluding lob
        gapDict = {k:v for k,v in modelParam['moose_impact_feature_name'].items() if inverseLobIndictator not in v}

        #filter out care gaps that were not fired in the util setup
        #commerical
        if lobIndictator == 'comm':

            #if the indicator is false, remove those gaps - otherwise keept
            if modelParam['otter_care_gap_com_medAdh_bool'] == False:
                gapDict = {k:v for k,v in gapDict.items() if modelParam['moose_impact_feature_category'][k] != 'med_adh'}
            if modelParam['otter_care_gap_com_comorb_bool'] == False:
                gapDict = {k:v for k,v in gapDict.items() if modelParam['moose_impact_feature_category'][k] != 'como'}
            if modelParam['otter_care_gap_com_medOpt_bool'] == False:
                gapDict = {k:v for k,v in gapDict.items() if modelParam['moose_impact_feature_category'][k] != 'med_opt'}
            if modelParam['otter_care_gap_com_device_bool'] == False:
                gapDict = {k:v for k,v in gapDict.items() if modelParam['moose_impact_feature_category'][k] != 'smbg'}
            if modelParam['otter_care_gap_com_moniter_bool'] == False:
                gapDict = {k:v for k,v in gapDict.items() if modelParam['moose_impact_feature_category'][k] != 'screen'}
            if modelParam['otter_care_gap_com_carecon_bool'] == False:
                gapDict = {k:v for k,v in gapDict.items() if modelParam['moose_impact_feature_category'][k] != 'cc'}
            #build reverse indicator to eliminate care gaps from other LOB
            inverseLobIndictator ='_medi'

        #medicare
        elif lobIndictator == 'medi':
            if modelParam['otter_care_gap_med_medAdh_bool'] == False:
                gapDict = {k:v for k,v in gapDict.items() if modelParam['moose_impact_feature_category'][k] != 'med_adh'}
            if modelParam['otter_care_gap_med_comorb_bool'] == False:
                gapDict = {k:v for k,v in gapDict.items() if modelParam['moose_impact_feature_category'][k] != 'como'}
            if modelParam['otter_care_gap_med_medOpt_bool'] == False:
                gapDict = {k:v for k,v in gapDict.items() if modelParam['moose_impact_feature_category'][k] != 'med_opt'}
            if modelParam['otter_care_gap_med_device_bool'] == False:
                gapDict = {k:v for k,v in gapDict.items() if modelParam['moose_impact_feature_category'][k] != 'smbg'}
            if modelParam['otter_care_gap_med_moniter_bool'] == False:
                gapDict = {k:v for k,v in gapDict.items() if modelParam['moose_impact_feature_category'][k] != 'screen'}
            if modelParam['otter_care_gap_med_carecon_bool'] == False:
                gapDict = {k:v for k,v in gapDict.items() if modelParam['moose_impact_feature_category'][k] != 'cc'}
            #build reverse indicator to eliminate care gaps from other LOB
            inverseLobIndictator ='_comm'

        else:
            #else send out an error
            unittest.TestCase().assertTrue(False,msg="Error in MooseGapOAReportOutput of Moose.  LOB not medi or comm")

        #populate the care gap name and care gap and all information that only corresponds to the care gap
        XReport['care_gap'] = gapDict.keys()
        XReport['care_gap_name'] = gapDict.values()
        XReport['care_gap_category'] = [modelParam['moose_impact_feature_category'][x] for x in XReport['care_gap']]
        XReport['care_gap_category_med_opt']= [modelParam['moose_impact_feature_category_med_opt'][x] for x in XReport['care_gap']]

        ####
        #### care gap overall , open , closed, ineligible from
        ####

        #populate overall counts
        XReport['open_count'] = [self.hippo[x+"_2"].sum() if x+"_2" in self.hippo.columns else 0 for x in XReport['care_gap']]
        XReport['close_count'] = [self.hippo[x+"_1"].sum() if x+"_1" in self.hippo.columns else 0 for x in XReport['care_gap']]
        XReport['eligible_count'] = XReport['open_count'] + XReport['close_count']
        XReport['ineligible_count'] = [self.hippo[x+"_0"].sum() if x+"_0" in self.hippo.columns else 0 for x in XReport['care_gap']]
        XReport['total_count'] = XReport['eligible_count'] + XReport['ineligible_count']

        #populat overall shares
        XReport['open_share'] = XReport['open_count']/XReport['total_count']
        XReport['close_share'] =  XReport['close_count']/ XReport['total_count']
        XReport['eligible_share'] = XReport['eligible_count']/XReport['total_count']
        XReport['ineligible_share'] = XReport['ineligible_count']/XReport['total_count']
        XReport['total_share'] = XReport['total_count']/XReport['total_count']

        ####
        #### means and std
        ####
        #get columns of interest
        cg = sorted([x for x in self.hippo.columns if 'care_gap' in x and 'shap' not in x and x[-2:]=="_2"])
        cgShap = sorted([x for x in self.hippo.columns if 'care_gap' in x and x[-7:] == '_2_shap'])

        #masks
        #get boolean mask for values to keep (gaps open)
        cgMask = self.hippo[cg]
        cgMask = np.where(cgMask==1,True,False)

        #get boolean mask for values to exclude due to negative shap values
        #(banding the impact of care gaps based on realism assumptions by Eli)
        cgShapMask = self.hippo[cgShap]
        cgShapMask = np.where(cgShapMask>=0,True,False)

        #apply boolean mask to the shap values
        cgShapDF = self.hippo[cgShap].where(cgMask).where(cgShapMask)

        #gap level mean
        gapLevelMean = cgShapDF.mean(skipna=True)
        gapLevelMean.index = [x[:-7] for x in gapLevelMean.index]
        gapLevelMean = pd.DataFrame(zip(gapLevelMean.index.values.tolist(),gapLevelMean),columns=['care_gap','total_mean_shap_a1c'])

        #get the gap level std
        gapLevelStd = cgShapDF.std(skipna=True)
        gapLevelStd.index = [x[:-7] for x in gapLevelStd.index]
        gapLevelStd = pd.DataFrame(zip(gapLevelStd.index.values.tolist(),gapLevelStd),columns=['care_gap','total_std_shap_a1c'])

        #put together
        gapMean = pd.merge(gapLevelMean,gapLevelStd,how="left",on="care_gap")

        #append
        XReport = pd.merge(XReport,gapMean,how="left",on="care_gap")

        ####
        #### misc
        ####

        #make sure that care gap is string
        XReport['care_gap'] = XReport['care_gap'].astype(str)

        #get holder for the total number of gaps to consider in the excel
        considerRank = 0

        ####
        #### rank ordered gaps
        ####

        #get the total number of people
        bigN = np.max(XReport['total_count'])
        #iterate through the rank order gaps as needed
        for rank in range(1,modelParam['moose_heterogeneity_top_gap_consider']+1):

            #verify that there members with that many care gaps, if not cance
            if 'care_gap_{0}'.format(str(rank)) not in self.member.columns:
                break
            else:
                considerRank += 1

            #filter down to the open care gaps of interest, itervley
            cgList = []
            openList = []
            shareList = []
            anticipatedOpenList = []
            anticipatedShareList = []
            valueList = []
            probList = []
            commList = []
            estimatedValueList = []

            #iterate through care gaps
            for cg in XReport['care_gap']:

                #get the cg name to align with the Member Gap Level Report
                cgName = modelParam['moose_impact_feature_name'][cg]

                #filter down to care gap of interest and rank of interest
                memberGapSmall = self.memberGap[(self.memberGap['care_gap']==cgName)&(self.memberGap['rank']==rank)].reset_index(drop=True)

                #populate lists if values are present
                if memberGapSmall.shape[0]>0:
                    cgList += [cg]
                    openList += [int(memberGapSmall.shape[0])]
                    shareList += [memberGapSmall.shape[0]/bigN]

                    #anticpiated
                    anticpatedSum = np.sum(memberGapSmall['total_close_prob'])
                    anticipatedOpenList += [anticpatedSum]
                    anticipatedShareList += [anticpatedSum/bigN]

                    #probability and value
                    valueList += [np.mean(memberGapSmall['value'])]
                    probList += [np.mean(memberGapSmall['total_close_prob'])]
                    commList += [np.mean(memberGapSmall['total_cost'])]
                    estimatedValueList += [np.mean(memberGapSmall['total_estimated_value'])]

                # if no members have the gap open for that rank, zero it out
                elif memberGapSmall.shape[0] == 0:
                    cgList += [0]
                    openList += [0]
                    shareList += [0]
                    anticipatedOpenList += [0]
                    anticipatedShareList += [0]
                    valueList += [0]
                    probList += [0]
                    commList += [0]
                    estimatedValueList += [0]

                #otherwise assert error
                else:
                    unittest.TestCase().assertTrue(False,msg=f"Error in MooseGapOAReportOutput of Moose. For care gap {cg} and rank{rank} error occured")

            #create dataframe of all the values of a given rank
            rankHolder = pd.DataFrame(zip(cgList,
                                     openList,
                                     shareList,
                                     valueList,
                                     anticipatedOpenList,
                                     anticipatedShareList,
                                     estimatedValueList,
                                     probList,
                                     commList,
                                     ),
                                 columns=['care_gap',
                                          f'rank_{rank}_care_gap_open_total_count_potential',
                                          f'rank_{rank}_care_gap_open_total_share_potential',
                                          f'rank_{rank}_care_gap_open_mean_value_potential',
                                          f'rank_{rank}_care_gap_open_total_count_expected',
                                          f'rank_{rank}_care_gap_open_total_share_expected',
                                          f'rank_{rank}_care_gap_open_mean_value_expected',
                                          f'rank_{rank}_care_gap_open_mean_success_probability',
                                          f'rank_{rank}_care_gap_open_mean_communication_cost',
                                          ])


            #merge onto overall data frame
            XReport = pd.merge(XReport,rankHolder,how="left",on="care_gap")

        #fill nas as zeros (useful for the rank columns where there are no gaps of the given rank
        XReport = XReport.fillna(0)
        
        #sum the gap $value for closing all ranks and top3
        gap_values_sum_all = []
        gap_values_sum_top3 = []

        #iterate through ranks
        for rank in range(1,considerRank+1):

            #get the open counts and the expected counts
            open_count = XReport[ f'rank_{rank}_care_gap_open_total_count_potential']
            expected_value = XReport[ f'rank_{rank}_care_gap_open_mean_value_expected']

            #iterate through the ranks
            if rank == 1:

                #top
                gap_values_sum_all = open_count * expected_value
                gap_values_sum_top3 = open_count * expected_value

                #mean
                gapValueSum = open_count * expected_value
                gapValueCount = open_count

            elif rank <=3:

                #top
                gap_values_sum_all += open_count * expected_value
                gap_values_sum_top3 += open_count * expected_value

                #mean
                gapValueSum += open_count * expected_value
                gapValueCount += open_count

            else:

                #top
                gap_values_sum_all += open_count * expected_value

                #mean
                gapValueSum += open_count * expected_value
                gapValueCount += open_count


        #put columns into the outcome report
        XReport['total_expected_value'] = gap_values_sum_all
        XReport['top_3_rank_expected_value'] = gap_values_sum_top3

        #get the weighted mean from all expected gap columns
        XReport['total_weighted_mean_expected_value'] = gapValueSum/gapValueCount

        #reorder columns and enter into the report (16 initial, 3 added, remainder are rank columns)
        reordered_colnames = XReport.columns[:16].tolist()+['total_expected_value', 'top_3_rank_expected_value','total_weighted_mean_expected_value']+ XReport.columns[16:-3].tolist()
        XReport = XReport.reindex(columns=reordered_colnames)

        ####
        #### create excel report
        ####
        self.excel(XReport,considerRank)

        ####
        #### return final
        ####
        return XReport
