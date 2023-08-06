import pandas as pd
import numpy as np
import os
import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from operator import add
import unittest
import datetime
from scipy.stats import skew
from IPython.display import display_html

#cmenagerie model imports
cwd = os.getcwd()
cwdHead = os.getcwd().split("/hippo/")[0]

#import hpackages and return to this directo
os.chdir(cwdHead+ '/hippo/src2/rhino')
from rhino import RhinoAPI
os.chdir(cwdHead+ '/hippo/src2/util')
from util import UtilAPI
#os.chdir(cwdHead+ '/hippo/src2/whale')

#return to original directory
os.chdir(cwd)

class UtilPlotAPI:
    """
    :param fontsize: size of font in plots
    :type fontsize: integer
    :param a1cCol: name of column with lab a1c information in data frame X
    :type a1cCol: string
    :param figsize: size of images to create
    :type figsize: tuple
    """

    def __init__(self,
                 fontsize=20,
                 figsize=(10,10),
                 a1cCol='lab_a1c',
                 idCol='individual_id',
                 psuidCol='plan_sponsor_id',
                 psuidCntCol ="ps_unique_id_member_cnt",
                 psuidDiabCntCol = "ps_unique_id_diab_member_cnt"
                 ):
        """
        constructor class
        """
        self.fontsize=fontsize
        self.figsize = figsize
        self.a1cCol = a1cCol
        self.idCol = idCol
        self.psuidCol = psuidCol
        self.psuidCntCol = psuidCntCol
        self.psuidDiabCntCol = psuidDiabCntCol


    ####
    #### raven
    ####

    def ravenHistogramLabA1cPlot(self,X):
        """ plots histogram of a1c.  Every member is considered
        """

        #size plot
        plt.figure(figsize=self.figsize)

        #make histogram
        plt.hist([x for x in X[self.a1cCol] if x >= 2 and x<= 18],bins=50,color='blue')

        #assign lables
        plt.xlabel('Lab A1C',fontsize=self.fontsize)
        plt.xticks(fontsize=self.fontsize*0.75)
        plt.ylabel('Count of Unique Members',fontsize=self.fontsize)
        plt.yticks(fontsize=self.fontsize*0.75)

        #show plot
        plt.show()


    def ravenHistogramPlanSponsorDiabetesPrevelancePlot(self,X,printPercentile=True,saveFig=True):
        """ plot histogram of diabetes preveleance.  Group by plan sponsors.
        Diabetes is considered beyond our cohort.
        """

        ####
        #### organize information
        ####

        #limit down df to just the columns of interest
        X = X[[self.idCol,self.a1cCol,self.psuidCol,self.psuidCntCol,self.psuidDiabCntCol]]

        #drop null a1c
        X['a1c_cnt'] = [1 if pd.notna(x) else False for x in X[self.a1cCol]]

        #aggreagate by psuid
        XGroup = X.groupby([self.psuidCol]).agg({self.psuidCol:np.max,
                                                 'a1c_cnt':np.sum,
                                                 self.psuidCntCol:np.max,
                                                 self.psuidDiabCntCol:np.max}).reset_index(drop=True)

        #get share
        XGroup['diab_prevalence'] = XGroup[self.psuidDiabCntCol]/XGroup[self.psuidCntCol]
        XGroup['a1c_prevalence'] = XGroup['a1c_cnt']/XGroup[self.psuidCntCol]

        #get overall (for plot)
        histCol = 'diab_prevalence'

        #insure a1c shares are resonable, remove PSUIds above 0 and below 1
        XGroup = XGroup[(XGroup[histCol]>= 0)&(XGroup[histCol]<= 1)].reset_index(drop=True)

        ####
        #### print data
        ####
        if printPercentile:
            incr = 5
            print('Percentiles of {0}:'.format(histCol))
            for p in np.arange(0,100+incr,incr):
                print("----",p,":",round(np.percentile(XGroup[histCol],p),4))

        ####
        #### plot
        ####
        #plot prevelances
        plt.figure(figsize=(10,10))
        plt.hist(XGroup[histCol],bins=50)

        #label axisx
        plt.xlabel('For Each Unique Plan Sponsor,\n Prevelance of Diabetes',fontsize=self.fontsize)
        plt.ylabel('Count of Unique Plan Sponsors',fontsize=self.fontsize)
        plt.xticks(np.arange(0,1.1,0.1),[str(int(x*100))+"%" for x in np.arange(0,1.1,0.1)],fontsize=self.fontsize*0.75)
        plt.yticks(fontsize=self.fontsize*0.75)

        #save fig as requested
        if saveFig:
            #save figure at date of interest
            dater = str(datetime.datetime.now().day) +"_"+str(datetime.datetime.now().month) + "_" +str(datetime.datetime.now().year)
            plt.savefig(f'ravenHistogramPlanSponsorDiabetesPrevelancePlot{dater}.jpg',format='jpeg',dpi=500)


        #show plot
        plt.show()

    def ravenHistogramPlanSponsorA1CPrevelancePlot(self,X, printPercentile=True,saveFig=False):
        """ plot histogram of a1c preveleance.  Group by plan sponsors.
        """

        ####
        #### organize information
        ####

        #limit down df to just the columns of interest
        X = X[[self.idCol,self.a1cCol,self.psuidCol,self.psuidCntCol,self.psuidDiabCntCol]]

        #drop null a1c
        X['a1c_cnt'] = [1 if pd.notna(x) else False for x in X[self.a1cCol]]

        #aggreagate by psuid
        XGroup = X.groupby([self.psuidCol]).agg({self.psuidCol:np.max,
                                                 'a1c_cnt':np.sum,
                                                 self.psuidCntCol:np.max,
                                                 self.psuidDiabCntCol:np.max}).reset_index(drop=True)

        #get share
        XGroup['diab_prevalence'] = XGroup[self.psuidDiabCntCol]/XGroup[self.psuidCntCol]
        XGroup['a1c_prevalence'] = XGroup['a1c_cnt']/XGroup[self.psuidCntCol]

        #get overall (for plot)
        histCol = 'a1c_prevalence'

        #insure a1c shares are resonable, remove PSUIds above 0 and below 1
        XGroup = XGroup[(XGroup[histCol]>= 0)&(XGroup[histCol]<= 1)].reset_index(drop=True)

        ####
        #### print data
        ####
        if printPercentile:
            incr = 5
            print('Percentiles of {0}:'.format(histCol))
            for p in np.arange(0,100+incr,incr):
                print("----",p,":",round(np.percentile(XGroup[histCol],p),4))

        ####
        #### plot
        ####
        #plot prevelances
        plt.figure(figsize=self.figsize)
        plt.hist(XGroup[histCol],bins=50)

        #label axisx
        plt.xlabel('For Each Unique Plan Sponsor,\n Prevelance of A1C',fontsize=self.fontsize)
        plt.ylabel('Count of Unique Plan Sponsors',fontsize=self.fontsize)
        plt.xticks(np.arange(0,1.1,0.1),[str(int(x*100))+"%" for x in np.arange(0,1.1,0.1)],fontsize=self.fontsize*0.75)
        plt.yticks(fontsize=self.fontsize*0.75)

        #save fig as requested
        if saveFig:
            #save figure at date of interest
            dater = str(datetime.datetime.now().day) +"_"+str(datetime.datetime.now().month) + "_" +str(datetime.datetime.now().year)
            plt.savefig(f'ravenHistogramPlanSponsorA1CPrevelancePlot{dater}.jpg',format='jpeg',dpi=500)


        #show plot as requested
        plt.show()

    def ravenHistogramPlanSponsorDiabetesMemberCountPlot(self,X,printPercentile=True,saveFig=False):
        """ count of members with diabetes by plan sponsor
        """

        ####
        #### organize information
        ####

        #limit down df to just the columns of interest
        X = X[[self.idCol,self.psuidCol,self.psuidDiabCntCol]]

        #aggreagate by psuid
        XGroup = X.groupby([self.psuidCol]).agg({self.psuidDiabCntCol:np.max}).reset_index(drop=True)

        ####
        #### print data
        ####
        if printPercentile:
            incr = 5
            print('Count of {0} == 0: {1}'.format(self.psuidDiabCntCol,XGroup[XGroup[self.psuidDiabCntCol]==0].shape[0]))
            print('Percentiles of {0}:'.format(self.psuidDiabCntCol))
            for p in np.arange(0,100,incr):
                print("----",p,":",round(np.percentile(XGroup[self.psuidDiabCntCol],p),4))
            for p in np.arange(100-incr,100+1,1):
                print("----",p,":",round(np.percentile(XGroup[self.psuidDiabCntCol],p),4))

        #after prints, insure real values and make zero apear (but only be a tiny bit above zero)
        XGroup =XGroup[XGroup[self.psuidDiabCntCol]>0].reset_index(drop=True)

        ####
        #### plot
        ####
        #plot prevelances
        plt.figure(figsize=(10,10))
        plt.hist(np.log10(XGroup[self.psuidDiabCntCol]),bins=100)

        #label axisx
        plt.xlabel('For Each Unique Plan Sponsor,\n Count of Unique Members with Diabetes \n (Log Base 10 - Zeros Excluded)',fontsize=self.fontsize)
        plt.ylabel('Count of Unique Plan Sponsors',fontsize=self.fontsize)
        plt.xticks(fontsize=self.fontsize*0.75)
        plt.yticks(fontsize=self.fontsize*0.75)

        #save fig as requested
        if saveFig:
            #save figure at date of interest
            dater = str(datetime.datetime.now().day) +"_"+str(datetime.datetime.now().month) + "_" +str(datetime.datetime.now().year)
            plt.savefig(f'ravenHistogramPlanSponsorDiabetesMemberCountPlot{dater}.jpg',format='jpeg',dpi=500)


        #show plot as requested
        plt.show()

    def ravenHistogramPlanSponsorMemberCountPlot(self,X,printPercentile=True,saveFig=False):
        """for each plan sponsor, count of unique members
        """

        ####
        #### organize information
        ####

        #limit down df to just the columns of interest
        X = X[[self.idCol,self.psuidCol,self.psuidCntCol]]

        #aggreagate by psuid
        XGroup = X.groupby([self.psuidCol]).agg({self.psuidCntCol:np.max}).reset_index(drop=True)

        ####
        #### print data
        ####
        if printPercentile:
            incr = 5
            print('Percentiles of {0}:'.format(self.psuidCntCol))
            for p in np.arange(0,100,incr):
                print("----",p,":",round(np.percentile(XGroup[self.psuidCntCol],p),4))
            for p in np.arange(100-incr,100+1,1):
                print("----",p,":",round(np.percentile(XGroup[self.psuidCntCol],p),4))

        ####
        #### plot
        ####
        #plot prevelances
        plt.figure(figsize=(10,10))
        plt.hist(np.log10(XGroup[self.psuidCntCol]),bins=50)

        #label axisx
        plt.xlabel('For Each Unique Plan Sponsor,\n Count of Unique Members (Log Base 10)',fontsize=self.fontsize)
        plt.ylabel('Count of Unique Plan Sponsors',fontsize=self.fontsize)
        plt.xticks(fontsize=self.fontsize*0.75)
        plt.yticks(fontsize=self.fontsize*0.75)

        #save fig as requested
        if saveFig:
            #save figure at date of interest
            dater = str(datetime.datetime.now().day) +"_"+str(datetime.datetime.now().month) + "_" +str(datetime.datetime.now().year)
            plt.savefig(f'ravenHistogramPlanSponsorMemberCountPlot{dater}.jpg',format='jpeg',dpi=500)


        #show plot as requested
        plt.show()

    def ravenHistogramPlanSponsorA1CVsDiabetesPrevelancePlot(self,X,printPercentile=True,saveFig=False):
        """ by plan sponsor, compares A1C prevelance vs diabetes prevelance
        """

        ####
        #### organize information
        ####

        #limit down df to just the columns of interest
        X = X[[self.idCol,self.a1cCol,self.psuidCol,self.psuidCntCol,self.psuidDiabCntCol]]

        #drop null a1c
        X['a1c_cnt'] = [1 if pd.notna(x) else False for x in X[self.a1cCol]]

        #aggreagate by psuid
        XGroup = X.groupby([self.psuidCol]).agg({self.psuidCol:np.max,
                                                 'a1c_cnt':np.sum,
                                                 self.psuidCntCol:np.max,
                                                 self.psuidDiabCntCol:np.max}).reset_index(drop=True)

        #get share
        XGroup['diab_prevalence'] = XGroup[self.psuidDiabCntCol]/XGroup[self.psuidCntCol]
        XGroup['a1c_prevalence'] = XGroup['a1c_cnt']/XGroup[self.psuidCntCol]

        #get overall (for plot)
        histCol = 'a1c_prevalence_over_diab_prevalence'
        XGroup[histCol] =   XGroup['a1c_prevalence']/XGroup['diab_prevalence']

        #insure a1c shares are resonable, remove PSUIds above 0 and below 1
        XGroup = XGroup[(XGroup[histCol]>= 0)&(XGroup[histCol]<= 1)].reset_index(drop=True)

        ####
        #### print data
        ####
        if printPercentile:
            incr = 5
            print('Percentiles of {0}:'.format(histCol))
            for p in np.arange(0,100+incr,incr):
                print("----",p,":",round(np.percentile(XGroup[histCol],p),4))

        ####
        #### plot
        ####
        #plot prevelances
        plt.figure(figsize=(10,10))
        plt.hist(XGroup[histCol],bins=50)

        #label axisx
        plt.xlabel('For Each Unique Plan Sponsor,\n Prevelance of A1C Divided By Prevelance of Diabetes',fontsize=self.fontsize)
        plt.ylabel('Count of Unique Plan Sponsors',fontsize=self.fontsize)
        plt.xticks(np.arange(0,1.1,0.1),[str(int(x*100))+"%" for x in np.arange(0,1.1,0.1)],fontsize=self.fontsize*0.75)
        plt.yticks(fontsize=self.fontsize*0.75)

        #save fig as requested
        if saveFig:
            #save figure at date of interest
            dater = str(datetime.datetime.now().day) +"_"+str(datetime.datetime.now().month) + "_" +str(datetime.datetime.now().year)
            plt.savefig(f'ravenHistogramPlanSponsorA1CVsDiabetesPrevelancePlot{dater}.jpg',format='jpeg',dpi=500)


        #show plot as requested
        plt.show()


    ####
    #### hippo
    ####

    def hippoMeanShapGapTable(self,hippo):
        """ for each gap, get the banded A1c impoact.  Returns for each gap its mean and std of open a1c impact

        :param hippo: hippo.X
        :type hippo: pd.DataFrame
        :return: pd.DataFrame
        """

        ####
        #### get inputs
        ####
        modelParam = UtilAPI().modelParam

        ####
        #### organize data to get columns of interest and masks
        ####
        #get columns of interest
        cg = sorted([x for x in hippo.columns if 'care_gap' in x and 'shap' not in x and x[-2:]=="_2"])
        cgShap = sorted([x for x in hippo.columns if 'care_gap' in x and x[-7:] == '_2_shap'])

        #masks
        #get boolean mask for values to keep (gaps open)
        cgMask = hippo[cg]
        cgMask = np.where(cgMask==1,True,False)

        #get boolean mask for values to exclude due to negative shap values
        #(banding the impact of care gaps based on realism assumptions by Eli)
        cgShapMask = hippo[cgShap]
        cgShapMask = np.where(cgShapMask>=0,True,False)

        ####
        #### apply masks
        ####

        #apply boolean mask to the shap values
        cgShapDF = hippo[cgShap].where(cgMask).where(cgShapMask)

        ####
        #### get outcome
        ####

        #gap level mean
        gapLevelMean = cgShapDF.mean(skipna=True)
        gapLevelMean.index = [x[:-7] for x in gapLevelMean.index]
        gapLevelMean = pd.DataFrame(zip(gapLevelMean.index.values.tolist(),gapLevelMean),columns=['care_gap','mean_shap_a1c'])

        #get the gap level std
        gapLevelStd = cgShapDF.std(skipna=True)
        gapLevelStd.index = [x[:-7] for x in gapLevelStd.index]
        gapLevelStd = pd.DataFrame(zip(gapLevelStd.index.values.tolist(),gapLevelStd),columns=['care_gap','std_shap_a1c'])

        #put together
        gapMean = pd.merge(gapLevelMean,gapLevelStd,how="left",on="care_gap")


        ####
        #### generate outcome
        ####

        #additional information
        gapMean['care_gap_name'] = [modelParam['moose_impact_feature_name'][x] if x != 'overall' else "" for x in gapMean['care_gap'] ]
        gapMean['care_gap_category'] = [modelParam['moose_impact_feature_category'][x] if x != 'overall' else "" for x in gapMean['care_gap'] ]

        # #reorder columns and rows
        gapMean = gapMean[['care_gap','care_gap_name','care_gap_category','mean_shap_a1c','std_shap_a1c']]
        gapMean = gapMean.sort_values(['care_gap_category','care_gap_name'],ascending=True).reset_index(drop=True)

        # #overall added to the outcome
        gapMean = pd.concat([pd.DataFrame([['overall',"","", np.nanmean(cgShapDF.values),np.nanstd(cgShapDF.values)]],columns=gapMean.columns),gapMean]).reset_index(drop=True)

        #final return
        return gapMean


    ####
    #### moose
    ####

    def normalRandom(self,original,mean,std,arrayLen=1,threshold=0):
        """ get a randomly choosen number (randomly distributed

        :param mean: mean of distrbution
        :param std: std of distribtion
        :param arrayLen: number to create
        :param threshold: no output allowed less than the threshold
        :return: returner (half of original and half of the other non zero value)
        """
        #get outcome
        returner = 0

        #resample until above zero
        while returner<=threshold:

            #get the blended (half original, half random value from spread of information)
            returner = (original + np.sum(np.random.normal(loc=mean,scale=std,size=arrayLen)))/2

        #return value above threshold
        return returner

    def moooseHistogramLabA1cProgramImpactPlot(self,X,egret,costCol,saveFig=True,blend=False):
        """ plots histogram of a1c. compares a1c with the program and without the program

        :param X: moose.mooseMemberLevel output
        :type X: pd.DataFrame
        :param egret: egret.X final output
        :type egret: pd.DataFrame
        :param costCol: column for cost to be created (must be in label dict)
        :type costCol: str
        :param saveFig: True if saving the picture, else False (nothing
        :type saveFig: bool
        """
        ####
        #### set up
        ####
        #set titles for the plot
        labelDict = {
            'etg_diab_chf30_ttl_allw_amt_12mo': '''Log of Gross Spending Absent EDS VS.\n Log of Gross Spending With EDS \n (Diabetes + 30% Cardiovascular One Year)''',
            'etg_diab_ttl_allw_amt_12mo' : '''Log of Gross Spending Absent EDS VS.\n Log of Gross Spending With EDS \n (Diabetes Only One Year)''',
            'total_allowed_usd_one_year' : '''Log of Gross Spending Absent EDS VS.\n Log of Gross Spending With EDS \n (Total Allowed Cost One Year)'''
        }

        #set the titles for the plot
        aggLabelDict = {
            'etg_diab_chf30_ttl_allw_amt_12mo': ['''Diabetes + 30% Cardiovascular One Year Cost Absent EDS''','''Diabetes + 30% Cardiovascular One Year Cost With EDS''' ],
            'etg_diab_ttl_allw_amt_12mo' : ['''Diabetes Only One Year Cost Absent EDS''','''Diabetes Only One Year Cost With EDS''' ],
            'total_allowed_usd_one_year' : ['''Total Allowed One Year Cost Absent EDS''','''Total Allowed One Year Cost With EDS''' ]
        }

        #model Pram
        modelParam = UtilAPI().modelParam

        #insure joinable
        X[self.idCol] = X[self.idCol].astype(str)
        egret[self.idCol] = egret[self.idCol].astype(str)

        ####
        #### get episode grouper information from egret
        ####

        #get information related to episode gropuper columns associated with the different members
        #get only the grouper columns of interest
        egret = egret[['individual_id',
                       'etg_diab_ttl_allw_amt_12mo',
                       'etg_chf_ttl_allw_amt_12mo']].fillna(0)

        #add in dfGroup columns for 30% chf
        egret['etg_diab_chf30_ttl_allw_amt_12mo'] = (egret['etg_diab_ttl_allw_amt_12mo'] +
                                                     egret['etg_chf_ttl_allw_amt_12mo']*0.3)

        #merge data (total_allowed_usd_one_year already in X)
        X = pd.merge(X,egret,how="left",on="individual_id")

        #size for later use
        biXN = X.shape[0]

        ####
        #### organize data for eds value of the program
        ####

        #value of the program (assuming that we grab all the care gaps)
        valueColumn = []
        for cg in range(1,modelParam['moose_heterogeneity_top_gap_consider']+1):

            #verify it exisits, if not then remove
            if f'care_gap_member_shap_delta_{str(cg)}' not in X.columns:
                continue

            #for columns that exist
            if len(valueColumn) == 0:
                valueColumn = X[f'care_gap_member_shap_delta_{str(cg)}'].fillna(0)
            else:
                valueColumn = list( map(add, valueColumn, X[f'care_gap_member_shap_delta_{str(cg)}'].fillna(0)) )

        #convert value column from a1c to $USD
        #multiple by 12 because the below is in pmpm and we need pmpy
        if modelParam['otter_care_gap_comm_vs_medi_bool'] == 'comm':
            a1cDollarConversion = 12*modelParam['moose_a1c_one_point_drop_usd_pppm_commerical']
        elif modelParam['otter_care_gap_comm_vs_medi_bool'] =="medi":
            a1cDollarConversion = 12*modelParam['moose_a1c_one_point_drop_usd_pppm_medicare']
        else:
            unittest.TestCase().assertFalse(True,msg='Error in UtilPlotAPI moooseHistogramLabA1cProgramImpactPlot; fed line of business that is neither comm nor medi')

        #value conversion from a1c to dollars
        valueColumn = [x*a1cDollarConversion for x in valueColumn]

        ####
        #### centralize data
        ####
        valueEDS = pd.DataFrame(zip(X[costCol],X[costCol]-valueColumn),columns=['original_cost','original_cost_minus_eds'])

        ####
        #### blending (discontinued)
        ####

        #if blend is turned on
        if blend:

            #blend columns (remove is not blending)
            ocMedian = np.median(valueEDS['original_cost'])
            ocMean = np.mean(valueEDS['original_cost'])
            ocSTD = np.std(valueEDS['original_cost'])

            #apply blending
            valueEDS['original_cost'] = [self.normalRandom(original,ocMean,ocSTD) for original in valueEDS['original_cost']]
            valueEDS['original_cost_minus_eds'] = valueEDS['original_cost']-valueColumn

        #drop people with negative costs (not realistic or representative of our work. Also align with commerical work
        #valueEDS = valueEDS[valueEDS['original_cost']>10]
        valueEDS = valueEDS[valueEDS['original_cost_minus_eds']>0]

        ####
        #### table
        ####

        #hold information
        legendCol = []
        originalCostCol = []
        originalCostMinusEdsCol = []
        differnceCol = []

        #get percentiles
        for p in [0,1,5,25,33,50,66,75,90,95,99,100]:
            legendCol.append(f'Percentile {str(p)}')
            originalCostCol.append("$ " + "{:.2f}".format(np.percentile(valueEDS['original_cost'],p)))
            originalCostMinusEdsCol.append("$ " + "{:.2f}".format(np.percentile(valueEDS['original_cost_minus_eds'],p)))
            differnceCol.append("$ " + "{:.2f}".format(np.percentile(valueEDS['original_cost'],p)-np.percentile(valueEDS['original_cost_minus_eds'],p)))

        #space
        legendCol.append("")
        originalCostCol.append("")
        originalCostMinusEdsCol.append("")
        differnceCol.append("")

        #mean
        legendCol.append('Average')
        originalCostCol.append("$ " + "{:.2f}".format(np.mean(valueEDS['original_cost'])))
        originalCostMinusEdsCol.append("$ " + "{:.2f}".format(np.mean(valueEDS['original_cost_minus_eds'])))
        differnceCol.append("$ " + "{:.2f}".format(np.mean(valueEDS['original_cost'])-np.mean(valueEDS['original_cost_minus_eds'])))

        #std
        legendCol.append('Standard Deviation')
        originalCostCol.append("$ " + "{:.2f}".format(np.std(valueEDS['original_cost'])))
        originalCostMinusEdsCol.append("$ " + "{:.2f}".format(np.std(valueEDS['original_cost_minus_eds'])))
        differnceCol.append("$ " + "{:.2f}".format(np.std(valueEDS['original_cost'])-np.std(valueEDS['original_cost_minus_eds'])))

        #skew
        legendCol.append('Skew')
        originalCostCol.append("$ " + "{:.2f}".format(skew(valueEDS['original_cost'])))
        originalCostMinusEdsCol.append("$ " + "{:.2f}".format(skew(valueEDS['original_cost_minus_eds'])))
        differnceCol.append("$ " + "{:.2f}".format(skew(valueEDS['original_cost'])-skew(valueEDS['original_cost_minus_eds'])))

        #space
        legendCol.append("")
        originalCostCol.append("")
        originalCostMinusEdsCol.append("")
        differnceCol.append("")

        #sample size (included)
        legendCol.append('Sample Size')
        originalCostCol.append("{:,.0f}".format((len(valueEDS['original_cost'])))+ " members")
        originalCostMinusEdsCol.append(("{:,.0f}".format((len(valueEDS['original_cost_minus_eds']))))+ " members")
        differnceCol.append("{:,.0f}".format((len(valueEDS['original_cost'])))+ " members")

        #excluded sample size
        legendCol.append('Excluded From Sample (EDS Pushed Predicted Costs Negative)')
        originalCostCol.append(("{:,.0f}".format((biXN-(len(valueEDS['original_cost']))))+ " members"))
        originalCostMinusEdsCol.append(("{:,.0f}".format((biXN-(len(valueEDS['original_cost_minus_eds'])))))+ " members")
        differnceCol.append(("{:,.0f}".format((biXN-(len(valueEDS['original_cost']))))+ " members"))

        #excluded sample size
        legendCol.append('Total Member Level Output Size')
        originalCostCol.append("{:,.0f}".format((biXN))+ " members")
        originalCostMinusEdsCol.append("{:,.0f}".format((biXN))+ " members")
        differnceCol.append("{:,.0f}".format((biXN))+ " members")

        #get aggreageted plot
        agg = pd.DataFrame(zip(legendCol,originalCostCol,originalCostMinusEdsCol,differnceCol),columns=['Statistic']+aggLabelDict[costCol]+['Difference'])

        ####
        #### plot
        ####

        #apply logs
        valueEDS['original_cost'] = np.log10(valueEDS['original_cost'] )
        valueEDS['original_cost_minus_eds'] = np.log10(valueEDS['original_cost_minus_eds'] )

        #size plot
        plt.figure(figsize=self.figsize)

        #histograms
        #make histogram of basic costs without EDS
        plt.hist(valueEDS['original_cost'],bins=100,color='blue',alpha=0.3,label= 'Gross Spending Absent EDS')

        #make histogram of costs with EDS
        plt.hist(valueEDS['original_cost_minus_eds'],bins=100,color='red',alpha=0.3,label= 'Gross Spending With EDS')

        #mean lines
        #plt.axvline(x=np.mean(valueEDS['original_cost']),color='blue')
        #plt.axvline(x=np.mean(valueEDS['original_cost_minus_eds']),color='red')

        #assign legend
        plt.legend(title='Spend Type', loc='upper left', labels=['Gross Spending Absent EDS',
                                                                 'Gross Spending With EDS'])

        #assign label
        plt.title( labelDict[costCol],fontsize=self.fontsize)
        plt.xlabel('Log, Base 10,of Allowed Costs (Over the Last 12 Months) ',fontsize=self.fontsize)
        plt.xticks(fontsize=self.fontsize*0.75)
        plt.ylabel('Count of Unique Members',fontsize=self.fontsize)
        plt.yticks(fontsize=self.fontsize*0.75)

        #save figure
        if saveFig:

            #date
            dater = str(datetime.datetime.now().day) +"_"+str(datetime.datetime.now().month) + "_" +str(datetime.datetime.now().year)

            #save table
            agg.to_csv(f'moooseHistogramLabA1cProgramImpactPlot_table_{costCol}_{dater}.csv',index=False,index_label=False)

            #save plot figure at date of interest

            plt.savefig(f'moooseHistogramLabA1cProgramImpactPlot_plot_{costCol}_{dater}.jpg',format='jpeg',dpi=500)

        #show plot
        plt.show()

        #show pandas table
        print('')
        display_html(agg.to_html().replace('table','table style="display:inline"'),raw=True)
        print('')

    def moooseHistogramLabA1cProgramImpactDifferencePlot(self,X,egret,costCol,saveFig=True):
        """ plots histogram of a1c. compares a1c with the program and without the program - only the difference between the programs

        :param X: moose.mooseMemberLevel output
        :type X: pd.DataFrame
        :param egret: egret.X final output
        :type egret: pd.DataFrame
        :param costCol: column for cost to be created (must be in label dict)
        :type costCol: str
        :param saveFig: True if saving the picture, else False (nothing
        :type saveFig: bool
        """
        ####
        #### set up
        ####
        #set titles for the plot
        labelDict = {
            'etg_diab_chf30_ttl_allw_amt_12mo': '''Impact of EDS (Diabetes + 30% Cardiovascular One Year)''',
            'etg_diab_ttl_allw_amt_12mo' : '''Impact of EDS (Diabetes Only One Year)''',
            'total_allowed_usd_one_year' : '''Impact of EDS (Total Allowed Cost One Year)'''
        }

        #model Pram
        modelParam = UtilAPI().modelParam

        #insure joinable
        X[self.idCol] = X[self.idCol].astype(str)
        egret[self.idCol] = egret[self.idCol].astype(str)

        ####
        #### get episode grouper information from egret
        ####

        #get information related to episode gropuper columns associated with the different members
        #get only the grouper columns of interest
        egret = egret[['individual_id',
                       'etg_diab_ttl_allw_amt_12mo',
                       'etg_chf_ttl_allw_amt_12mo']].fillna(0)

        #add in dfGroup columns for 30% chf
        egret['etg_diab_chf30_ttl_allw_amt_12mo'] = (egret['etg_diab_ttl_allw_amt_12mo'] +
                                                     egret['etg_chf_ttl_allw_amt_12mo']*0.3)

        #merge data (total_allowed_usd_one_year already in X)
        X = pd.merge(X,egret,how="left",on="individual_id")

        #size for later use
        biXN = X.shape[0]

        ####
        #### organize data for eds value of the program
        ####

        #value of the program (assuming that we grab all the care gaps)
        valueColumn = []
        for cg in range(1,modelParam['moose_heterogeneity_top_gap_consider']+1):

            #verify it exisits, if not then remove
            if f'care_gap_member_shap_delta_{str(cg)}' not in X.columns:
                continue

            #for columns that exist
            if len(valueColumn) == 0:
                valueColumn = X[f'care_gap_member_shap_delta_{str(cg)}'].fillna(0)
            else:
                valueColumn = list( map(add, valueColumn, X[f'care_gap_member_shap_delta_{str(cg)}'].fillna(0)) )

        #convert value column from a1c to $USD
        #multiple by 12 because the below is in pmpm and we need pmpy
        if modelParam['otter_care_gap_comm_vs_medi_bool'] == 'comm':
            a1cDollarConversion = 12*modelParam['moose_a1c_one_point_drop_usd_pppm_commerical']
        elif modelParam['otter_care_gap_comm_vs_medi_bool'] =="medi":
            a1cDollarConversion = 12*modelParam['moose_a1c_one_point_drop_usd_pppm_medicare']
        else:
            unittest.TestCase().assertFalse(True,msg='Error in UtilPlotAPI moooseHistogramLabA1cProgramImpactPlot; fed line of business that is neither comm nor medi')

        #value conversion from a1c to dollars
        valueColumn = [x*a1cDollarConversion for x in valueColumn]

        ####
        #### centralize data
        ####
        valueEDS = pd.DataFrame(zip(valueColumn),columns=['eds'])

        ####
        #### table
        ####

        #hold information
        legendCol = []
        differnceCol = []

        #get percentiles
        for p in [0,1,5,25,33,50,66,75,90,95,99,100]:
            legendCol.append(f'Percentile {str(p)}')
            differnceCol.append("$ " + "{:.2f}".format(np.percentile(valueEDS['eds'],p)))

        #space
        legendCol.append("")
        differnceCol.append("")

        #mean
        legendCol.append('Average')
        differnceCol.append("$ " + "{:.2f}".format(np.mean(valueEDS['eds'])))

        #std
        legendCol.append('Standard Deviation')
        differnceCol.append("$ " + "{:.2f}".format(np.std(valueEDS['eds'])))

        #skew
        legendCol.append('Skew')
        differnceCol.append("$ " + "{:.2f}".format(skew(valueEDS['eds'])))

        #space
        legendCol.append("")
        differnceCol.append("")

        #sample size (included)
        legendCol.append('Sample Size')
        differnceCol.append("{:,.0f}".format((len(valueEDS['eds'])))+ " members")

        #excluded sample size
        legendCol.append('Total Member Level Output Size')
        differnceCol.append("{:,.0f}".format((biXN))+ " members")

        #get aggreageted plot
        agg = pd.DataFrame(zip(legendCol,differnceCol),columns=['Statistic','Impact of EDS'])

        ####
        #### plot
        ####

        #size plot
        plt.figure(figsize=self.figsize)

        #histograms
        #make histogram of impact of EDS
        plt.hist(valueEDS['eds'],bins=100,color='blue',alpha=0.3,label= 'Impact of EDS')

        #mean lines
        #plt.axvline(x=np.mean(valueEDS['original_cost']),color='blue')
        #plt.axvline(x=np.mean(valueEDS['original_cost_minus_eds']),color='red')

        #assign legend
        #plt.legend(title='Spend Type', loc='upper left', labels=['Gross Spending Absent EDS',
        #                                                         'Gross Spending With EDS'])

        #assign label
        plt.title( labelDict[costCol],fontsize=self.fontsize)
        plt.xlabel('Impact of EDS on Allowed Costs (Over the Last 12 Months) ',fontsize=self.fontsize)
        plt.xticks(fontsize=self.fontsize*0.75)
        plt.ylabel('Count of Unique Members',fontsize=self.fontsize)
        plt.yticks(fontsize=self.fontsize*0.75)

        #save figure
        if saveFig:

            #date
            dater = str(datetime.datetime.now().day) +"_"+str(datetime.datetime.now().month) + "_" +str(datetime.datetime.now().year)

            #save table
            agg.to_csv(f'moooseHistogramLabA1cProgramImpactDifferencePlot_table_{costCol}_{dater}.csv',index=False,index_label=False)

            #save plot figure at date of interest

            plt.savefig(f'moooseHistogramLabA1cProgramImpactDifferencePlot_plot_{costCol}_{dater}.eps',format='eps',dpi=500)

        #show plot
        plt.show()

        #show pandas table
        print('')
        display_html(agg.to_html().replace('table','table style="display:inline"'),raw=True)
        print('')
