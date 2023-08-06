import pandas as pd
import numpy as np
import os

from hyperopt import hp, fmin, tpe, space_eval, STATUS_OK, Trials

# basic utility functions used across the other packages
class UtilAPI:

    # init
    def __init__(self):

        # initiate dict
        modelParam = {}

        # enter keys and values  information

        ####
        #### egret
        ####

        # list of anti_diabetic__drug_ (and statins) that we want the pdc information for
        modelParam['egret_anti_diabetic_pdc_drug_columns'] = ['rx_alpha_glucosidase_inhibitor_pdc_last_12_month',
                                                              'rx_biguanides_pdc_last_12_month',
                                                              'rx_dpp_4_inhibitors_pdc_last_12_month',
                                                              'rx_glp1_agonist_pdc_last_12_month',
                                                              'rx_insulin_pdc_last_12_month',
                                                              'rx_meglitinide_analogues_pdc_last_12_month',
                                                              'rx_sglt2_inhibitors_pdc_last_12_month',
                                                              'rx_statins_pdc_last_12_month',
                                                              'rx_sulfonylureas_pdc_last_12_month',
                                                              'rx_thiazolidinediones_pdc_last_12_month'] \
                                                            + ['hh_geo_access_april1_2020', 'store_number_1_april1_2020',
                                                                'hh_geo_access_sept1_2020', 'store_number_1_sept1_2020',
                                                                'hh_geo_access_jan1_2021', 'store_number_1_jan1_2021'] \
                                                            + ['ivr_permissions','dm_permissions',
                                                                'email_permissions','sms_permissions']

        # columns with bigwide format that need to be changed
        modelParam['egret_big_wide_columns'] = ['big_wide_me913',
                                                'big_wide_me98971',
                                                'big_wide_me99055',
                                                'big_wide_me1008',
                                                'big_wide_me754',
                                                'big_wide_me849',
                                                'big_wide_me519',
                                                'big_wide_me573',
                                                'big_wide_me355',
                                                'big_wide_me369',
                                                'big_wide_me44364',
                                                'big_wide_me44107',
                                                'big_wide_me44096',
                                                'big_wide_me575',
                                                'big_wide_me578',
                                                'big_wide_me397',
                                                'big_wide_me404',
                                                'big_wide_me119',
                                                'big_wide_me742',
                                                'big_wide_me571',
                                                'big_wide_me74',
                                                'big_wide_me55103',
                                                'big_wide_me855',
                                                'big_wide_me987',
                                                'big_wide_me992',
                                                'big_wide_me896',
                                                'big_wide_me98968',
                                                'big_wide_me98980',
                                                'big_wide_me98982',
                                                'big_wide_me99054',
                                                'big_wide_me99020',
                                                'big_wide_me877',
                                                'big_wide_me932',
                                                'big_wide_me965',
                                                'big_wide_me971',
                                                'big_wide_me44184',
                                                'big_wide_me44190',
                                                'big_wide_me44205',
                                                'big_wide_me44061',
                                                'big_wide_me44269',
                                                'big_wide_me833015',
                                                'big_wide_me833016',
                                                'big_wide_me833017',
                                                'big_wide_me833018',
                                                'big_wide_me833019',
                                                'big_wide_me44206',
                                                'big_wide_me323',
                                                'big_wide_me829',
                                                'big_wide_me576',
                                                'big_wide_me120',
                                                'big_wide_me77039',
                                                'big_wide_me77027',
                                                'big_wide_me77009',
                                                'big_wide_me77034',
                                                'big_wide_me77029',
                                                'big_wide_me77038',
                                                'big_wide_me77033',
                                                'big_wide_me77024',
                                                'big_wide_me77035',
                                                'big_wide_me77028',
                                                'big_wide_me77025',
                                                'big_wide_me77030',
                                                'big_wide_me77032',
                                                'big_wide_me1132',
                                                'big_wide_me44220',
                                                'big_wide_me44155',
                                                'big_wide_me44041',
                                                'big_wide_me44240',
                                                'big_wide_me77036',
                                                'big_wide_me77031',
                                                'big_wide_me44275',
                                                'big_wide_me98956',
                                                'big_wide_me1214',
                                                'big_wide_me44089',
                                                'big_wide_me44287',
                                                'big_wide_me356',
                                                'big_wide_me44142',
                                                'big_wide_me1183',
                                                'big_wide_me1176',
                                                'big_wide_me44296',
                                                'big_wide_me833119',
                                                'big_wide_me928',
                                                'big_wide_me44306',
                                                'big_wide_me44298',
                                                'big_wide_me75',
                                                'big_wide_me44309',
                                                'big_wide_me77019',
                                                'big_wide_me966',
                                                'big_wide_me33004',
                                                'big_wide_me1312',
                                                'big_wide_me44088',
                                                'big_wide_me2026',
                                                'big_wide_me2055',
                                                'big_wide_me812',
                                                'big_wide_me44310',
                                                'big_wide_me569',
                                                'big_wide_me99035',
                                                'big_wide_me743',
                                                'big_wide_me44303',
                                                'big_wide_me44090',
                                                'big_wide_me895',
                                                'big_wide_me820',
                                                'big_wide_me856',
                                                'big_wide_me44307',
                                                'big_wide_me1395',
                                                'big_wide_me44136',
                                                'big_wide_me98922',
                                                'big_wide_me686',
                                                'big_wide_me1415',
                                                'big_wide_me1418',
                                                'big_wide_me1428',
                                                'big_wide_me572',
                                                'big_wide_me44067',
                                                'big_wide_me854',
                                                'big_wide_me77041',
                                                'big_wide_me73',
                                                'big_wide_me981',
                                                'big_wide_me77002',
                                                'big_wide_me77012',
                                                'big_wide_me99002',
                                                'big_wide_me99543',
                                                'big_wide_me99743',
                                                'big_wide_me55104',
                                                'big_wide_me55105',
                                                'big_wide_me55106',
                                                'big_wide_me55107',
                                                'big_wide_me55108',
                                                'big_wide_me55109',
                                                'big_wide_me44308',
                                                'big_wide_me44070',
                                                'big_wide_me44239',
                                                'big_wide_me55110',
                                                'big_wide_me55111',
                                                'big_wide_me44137',
                                                'big_wide_me691',
                                                'big_wide_me44242',
                                                'big_wide_me543',
                                                'big_wide_me44138',
                                                'big_wide_me1011',
                                                'big_wide_me44068',
                                                'big_wide_me1299',
                                                'big_wide_me489',
                                                'big_wide_me857',
                                                'big_wide_me98958',
                                                'big_wide_me98967',
                                                'big_wide_me574',
                                                'big_wide_me98981',
                                                'big_wide_me98942',
                                                'big_wide_me99005',
                                                'big_wide_me1168',
                                                'big_wide_me44072',
                                                'big_wide_me77043',
                                                'big_wide_me77042',
                                                'big_wide_me577',
                                                'big_wide_me77040',
                                                'big_wide_me44342',
                                                'big_wide_me44286',
                                                'big_wide_me44139',
                                                'big_wide_me44285',
                                                'big_wide_me77026',
                                                'big_wide_me77037',
                                                'big_wide_me79',
                                                'big_wide_me289']

        ####
        #### otter
        ####

        # list of columns that conflict
        modelParam['otter_col_underpinning_care_gaps'] = ['lab_a1c_12mo',
                                                          'ckd_unspecified',
                                                          'lab_cholesterol',
                                                          'lab_cholesterol_hdl',
                                                          'lab_cholesterol_ldl',
                                                          'lab_cholesterol_hdl_total',
                                                          'visit_pcp_last_6_month_any',
                                                          'visit_pcp_last_6_month_count',
                                                          'visit_pcp_last_12_month_any',
                                                          'visit_pcp_last_12_month_count',
                                                          'visit_pcp_last_18_month_any',
                                                          'visit_pcp_last_18_month_count',
                                                          'ckd_1',
                                                          'ckd_2',
                                                          'ckd_3',
                                                          'ckd_4',
                                                          'ckd_5',
                                                          'ckd_esrd',
                                                          'rx_sulfonylureas_ever',
                                                          'rx_sulfonylureas_last_3_month',
                                                          'rx_sulfonylureas_last_6_month',
                                                          'rx_sulfonylureas_last_9_month',
                                                          'rx_sulfonylureas_last_12_month',
                                                          'rx_biguanides_ever',
                                                          'rx_biguanides_last_3_month',
                                                          'rx_biguanides_last_6_month',
                                                          'rx_biguanides_last_9_month',
                                                          'rx_biguanides_last_12_month',
                                                          'rx_thiazolidinediones_ever',
                                                          'rx_thiazolidinediones_last_3_month',
                                                          'rx_thiazolidinediones_last_6_month',
                                                          'rx_thiazolidinediones_last_9_month',
                                                          'rx_thiazolidinediones_last_12_month',
                                                          'rx_dpp_4_inhibitors_ever',
                                                          'rx_dpp_4_inhibitors_last_3_month',
                                                          'rx_dpp_4_inhibitors_last_6_month',
                                                          'rx_dpp_4_inhibitors_last_9_month',
                                                          'rx_dpp_4_inhibitors_last_12_month',
                                                          'rx_meglitinide_analogues_ever',
                                                          'rx_meglitinide_analogues_last_3_month',
                                                          'rx_meglitinide_analogues_last_6_month',
                                                          'rx_meglitinide_analogues_last_9_month',
                                                          'rx_meglitinide_analogues_last_12_month',
                                                          'rx_sglt2_inhibitors_ever',
                                                          'rx_sglt2_inhibitors_last_3_month',
                                                          'rx_sglt2_inhibitors_last_6_month',
                                                          'rx_sglt2_inhibitors_last_9_month',
                                                          'rx_sglt2_inhibitors_last_12_month',
                                                          'rx_glp1_agonist_ever',
                                                          'rx_glp1_agonist_last_3_month',
                                                          'rx_glp1_agonist_last_6_month',
                                                          'rx_glp1_agonist_last_9_month',
                                                          'rx_glp1_agonist_last_12_month',
                                                          'rx_alpha_glucosidase_inhibitor_ever',
                                                          'rx_alpha_glucosidase_inhibitor_last_3_month',
                                                          'rx_alpha_glucosidase_inhibitor_last_6_month',
                                                          'rx_alpha_glucosidase_inhibitor_last_9_month',
                                                          'rx_alpha_glucosidase_inhibitor_last_12_month',
                                                          'rx_insulin_ever',
                                                          'rx_insulin_last_3_month',
                                                          'rx_insulin_last_6_month',
                                                          'rx_insulin_last_9_month',
                                                          'rx_insulin_last_12_month',
                                                          'rx_sulfonylureas_pdc_last_12_month',
                                                          'rx_biguanides_pdc_last_12_month',
                                                          'rx_thiazolidinediones_pdc_last_12_month',
                                                          'rx_dpp_4_inhibitors_pdc_last_12_month',
                                                          'rx_meglitinide_analogues_pdc_last_12_month',
                                                          'rx_sglt2_inhibitors_pdc_last_12_month',
                                                          'rx_glp1_agonist_pdc_last_12_month',
                                                          'rx_alpha_glucosidase_inhibitor_pdc_last_12_month',
                                                          'rx_insulin_pdc_last_12_month',
                                                          'rx_statins_pdc_last_12_month',
                                                          'rx_test_test_strip_ever',
                                                          'rx_test_test_strip_last_3_month',
                                                          'rx_test_test_strip_last_6_month',
                                                          'rx_test_test_strip_last_9_month',
                                                          'rx_test_test_strip_last_12_month',
                                                          'rx_test_test_strip_last_18_month',
                                                          'rx_test_glucose_meter_ever',
                                                          'rx_test_glucose_meter_last_3_month',
                                                          'rx_test_glucose_meter_last_6_month',
                                                          'rx_test_glucose_meter_last_9_month',
                                                          'rx_test_glucose_meter_last_12_month',
                                                          'rx_test_glucose_meter_last_18_month',
                                                          'rx_test_glucose_monitor_ever',
                                                          'rx_test_glucose_monitor_last_3_month',
                                                          'rx_test_glucose_monitor_last_6_month',
                                                          'rx_test_glucose_monitor_last_9_month',
                                                          'rx_test_glucose_monitor_last_12_month',
                                                          'rx_test_glucose_monitor_last_18_month',
                                                          'como_chronic_renal_failure',
                                                          'como_hyperlipidemia',
                                                          'como_hypertension',
                                                          'como_metabolic_syndrome',
                                                          'como_obesity',
                                                          'como_depression',
                                                          'como_alcoholism',
                                                          'como_iron_deficiency_anemia',
                                                          'como_asthma',
                                                          'como_low_vision_and_blindness',
                                                          'como_heart_failure',
                                                          'lab_glucose',
                                                          'rx_insulin_longer_12_month',
                                                          'rx_sulfonylureas_longer_12_month',
                                                          'como_diabetes',
                                                          'diag_e11_ever',
                                                          'me152',
                                                          'rx_dpp_4_inhibitors_longer_12_month',
                                                          'visit_specialist_last_12_month_count',
                                                          'rx_glipizide_ever',
                                                          'prcdr_lipid_profile_screen_cnt',
                                                          'plan_sponsor_id',
                                                          'me397',
                                                          'me1008',
                                                          'rx_statins_longer_12_month',
                                                          'rx_biguanides_longer_12_month',
                                                          'rx_sglt2_inhibitors_longer_12_month',
                                                          'rx_glipizide_last_12_month',
                                                          'prcdr_diabetes_screening_test_cnt',
                                                          'me1395',
                                                          'cost_past_place_of_service_er_12_month_ever',
                                                          'me120',
                                                          'rx_thiazolidinediones_longer_12_month',
                                                          'hypoglycemia_diagnosis_6_month',
                                                          'me75',
                                                          'me374',
                                                          'rx_statins_last_9_month',
                                                          'rx_glipizide_longer_12_month',
                                                          'rx_statins_last_12_month',
                                                          'prcdr_lipid_profile_screen',
                                                          'diag_e03_ever',
                                                          'rx_test_device_diabetes_supply_ever',
                                                          'rx_test_device_diabetes_supply_last_3_month',
                                                          'rx_test_device_diabetes_supply_last_6_month',
                                                          'rx_test_device_diabetes_supply_last_9_month',
                                                          'rx_test_device_diabetes_supply_last_12_month',
                                                          'rx_test_device_diabetes_supply_last_18_month']

        ####
        #### otter - care gap information
        ####

        ##
        ## misc
        ##
        modelParam['otter_med_insurance_list'] = 'insure_med'

        # modelParam['otter_med_insurance_list'] = ['insure_med_com_full',
        #                                           'insure_med_com_self',
        #                                           'insure_med_com_split',
        #                                           'insure_med_med_group',
        #                                           'insure_med_med_indiv']

        ####
        #### indicate if we generate commercial('comm')/medicare('medi')
        #### other options beyond comm and medi will break the pipeline, by design
        ####

        modelParam['otter_care_gap_comm_vs_medi_bool'] = 'medi'

        ####
        #### indicate if we should use the care gaps or not
        ####
        modelParam['otter_care_gap_com_medAdh_bool']  = True
        modelParam['otter_care_gap_com_comorb_bool']  = False
        modelParam['otter_care_gap_com_medOpt_bool']  = True
        modelParam['otter_care_gap_com_device_bool']  = True
        modelParam['otter_care_gap_com_moniter_bool'] = True
        modelParam['otter_care_gap_com_carecon_bool'] = True

        modelParam['otter_care_gap_med_medAdh_bool']  = True
        modelParam['otter_care_gap_med_comorb_bool']  = False
        modelParam['otter_care_gap_med_medOpt_bool']  = True
        modelParam['otter_care_gap_med_device_bool']  = True
        modelParam['otter_care_gap_med_moniter_bool'] = True
        modelParam['otter_care_gap_med_carecon_bool'] = True
        
        ##
        ## Commercial 28 care considerations
        ##
        com_careConsiderationDict = {}
        com_careConsiderationDict['care_gap_600'] = 'me74'
        com_careConsiderationDict['care_gap_601'] = 'me75'
        com_careConsiderationDict['care_gap_602'] = 'me105'
        com_careConsiderationDict['care_gap_603'] = 'me120'
        com_careConsiderationDict['care_gap_604'] = 'me323'
        com_careConsiderationDict['care_gap_605'] = 'me369'
        com_careConsiderationDict['care_gap_606'] = 'me397'
        com_careConsiderationDict['care_gap_607'] = 'me402'
        com_careConsiderationDict['care_gap_608'] = 'me468'
        com_careConsiderationDict['care_gap_609'] = 'me721'
        
        com_careConsiderationDict['care_gap_610'] = 'me779'
        com_careConsiderationDict['care_gap_611'] = 'me780'
        com_careConsiderationDict['care_gap_612'] = 'me829'
        com_careConsiderationDict['care_gap_613'] = 'me842'
        com_careConsiderationDict['care_gap_614'] = 'me1008'
        com_careConsiderationDict['care_gap_615'] = 'me1168'

        com_careConsiderationDict['care_gap_616'] = 'me1183'
        com_careConsiderationDict['care_gap_617'] = 'me1250'
        com_careConsiderationDict['care_gap_618'] = 'me1312'
        
        com_careConsiderationDict['care_gap_619'] = 'me1317'
        com_careConsiderationDict['care_gap_620'] = 'me1364'
        com_careConsiderationDict['care_gap_621'] = 'me1367'
        com_careConsiderationDict['care_gap_622'] = 'me1387'
        com_careConsiderationDict['care_gap_623'] = 'me1388'
        com_careConsiderationDict['care_gap_624'] = 'me1395'
        com_careConsiderationDict['care_gap_625'] = 'me1422'
        com_careConsiderationDict['care_gap_626'] = 'me1440'
        com_careConsiderationDict['care_gap_627'] = 'me99035'
       
      
        modelParam['otter_care_gap_com_carecon'] = com_careConsiderationDict

        ##
        ## comorbidity
        ##

        comorbidityDict = {}
        comorbidityDict['care_gap_400'] = 'como_alcoholism'
        comorbidityDict['care_gap_402'] = 'como_asthma'
        comorbidityDict['care_gap_407'] = 'como_chronic_renal_failure'
        comorbidityDict['care_gap_408'] = 'como_depression'
        comorbidityDict['care_gap_410'] = 'como_heart_failure'
        comorbidityDict['care_gap_412'] = 'como_hyperlipidemia'
        comorbidityDict['care_gap_413'] = 'como_hypertension'
        comorbidityDict['care_gap_414'] = 'como_iron_deficiency_anemia'
        comorbidityDict['care_gap_416'] = 'como_low_vision_and_blindness'
        comorbidityDict['care_gap_417'] = 'como_metabolic_syndrome'
        comorbidityDict['care_gap_418'] = 'como_obesity'
        modelParam['otter_care_gap_com_comor'] = comorbidityDict

        ##
        ## commercial care gaps for medical adherence
        ##

        comMedAdherenceDict = {}
        comMedAdherenceDict['care_gap_038'] = ['rx_alpha_glucosidase_inhibitor_last_12_month',
                                               'rx_alpha_glucosidase_inhibitor_pdc_last_12_month']
        comMedAdherenceDict['care_gap_039'] = ['rx_biguanides_last_12_month', 'rx_biguanides_pdc_last_12_month']
        comMedAdherenceDict['care_gap_040'] = ['rx_dpp_4_inhibitors_last_12_month',
                                               'rx_dpp_4_inhibitors_pdc_last_12_month']
        comMedAdherenceDict['care_gap_041'] = ['rx_glp1_agonist_last_12_month', 'rx_glp1_agonist_pdc_last_12_month']
        comMedAdherenceDict['care_gap_043'] = ['rx_meglitinide_analogues_last_12_month',
                                               'rx_meglitinide_analogues_pdc_last_12_month']
        comMedAdherenceDict['care_gap_044'] = ['rx_sglt2_inhibitors_last_12_month',
                                               'rx_sglt2_inhibitors_pdc_last_12_month']
        comMedAdherenceDict['care_gap_045'] = ['rx_sulfonylureas_last_12_month', 'rx_sulfonylureas_pdc_last_12_month']
        comMedAdherenceDict['care_gap_046'] = ['rx_thiazolidinediones_last_12_month',
                                               'rx_thiazolidinediones_pdc_last_12_month']
        comMedAdherenceDict['care_gap_047'] = ['rx_statins_last_12_month', 'rx_statins_pdc_last_12_month']

        # input into model Param
        modelParam['otter_care_gap_com_medAdh'] = comMedAdherenceDict

        ##
        ## commercial care gaps for Monitering Gaps
        ##
        comMoniterPcpDict = {}
        comMoniterPcpDict['care_gap_053'] = 'office_visit_cpt_12mo'
        comMoniterLipidDict = {}
        comMoniterLipidDict['care_gap_072'] = ['triglyceride_cpt_12mo',
                                               ['total_cholesterol_cpt_12mo', 'cholesterol_hdl_cpt_12mo',
                                                'cholesterol_ldl_cpt_12mo']]
        modelParam['otter_care_gap_com_moniter_pcp'] = comMoniterPcpDict
        modelParam['otter_care_gap_com_moniter_lipid'] = comMoniterLipidDict

        ##
        ## commercial care gaps for medical optimization
        ##

        # a1c threshold
        modelParam['otter_care_gap_comm_med_opt_a1c_uncontrolled_threshold'] = 7.0

        # build dictionary
        comMedOptDict = {}
        comMedOptDict['care_gap_001XX'] = [pd.Interval( modelParam['otter_care_gap_comm_med_opt_a1c_uncontrolled_threshold'] ,11,closed='neither'),
                                            None,
                                            ['ckd_4', 'ckd_5', 'ckd_esrd'],
                                            None, None, None,None,None]
        comMedOptDict['care_gap_002'] = [pd.Interval(11,18,closed='both'),
                                            None, None, None, None, None,None,None]
        comMedOptDict['care_gap_002XX'] = [pd.Interval(2,11, closed='left'),
                                            ['ckd_4', 'ckd_5', 'ckd_esrd'],
                                           None,None, None, None,None,None]
        comMedOptDict['care_gap_003'] = [pd.Interval( modelParam['otter_care_gap_comm_med_opt_a1c_uncontrolled_threshold'] ,18,closed='right'),
                                         None,
                                         None,
                                         ['rx_biguanides_last_12_month'],
                                         ['rx_biguanides_pdc_last_12_month'],
                                         None,None,None]
        comMedOptDict['care_gap_004'] = [pd.Interval( modelParam['otter_care_gap_comm_med_opt_a1c_uncontrolled_threshold'] ,18,closed='right'),
                                         None,
                                         None,
                                         ['rx_biguanides_last_12_month'],
                                         ['rx_biguanides_pdc_last_12_month'],
                                         1,
                                         None,None]
        #
        comMedOptDict['care_gap_006'] = [pd.Interval( modelParam['otter_care_gap_comm_med_opt_a1c_uncontrolled_threshold'] ,18,closed='right'),
                                         None,
                                         ['ckd_1','ckd_2','ckd_3','ckd_4','ckd_5','ckd_unspecified','ckd_esrd','como_heart_failure','como_ascvd','como_obesity'],
                                         ['rx_biguanides_last_12_month'],
                                         ['rx_biguanides_pdc_last_12_month'],
                                         None,None,None]
        comMedOptDict['care_gap_007'] =[ pd.Interval( modelParam['otter_care_gap_comm_med_opt_a1c_uncontrolled_threshold'] ,18,closed='right'),
                                         None,
                                         ['ckd_1','ckd_2','ckd_3','ckd_4','ckd_5','ckd_unspecified','ckd_esrd','como_heart_failure','como_ascvd','como_obesity'],
                                         ['rx_biguanides_last_12_month'],
                                         ['rx_biguanides_pdc_last_12_month'],
                                         1,
                                         ['rx_glp1_agonist_last_12_month'],
                                         0]

        comMedOptDict['care_gap_010'] = [pd.Interval( modelParam['otter_care_gap_comm_med_opt_a1c_uncontrolled_threshold'] ,18,closed='right'),
                                         ['como_obesity'],
                                         ['ckd_1','ckd_2','ckd_3','ckd_4','ckd_5','ckd_unspecified','ckd_esrd','como_heart_failure','como_ascvd'],
                                         ['rx_biguanides_last_12_month'],
                                         ['rx_biguanides_pdc_last_12_month'],
                                         None,
                                         ['rx_glp1_agonist_last_12_month','rx_sglt2_inhibitors_last_12_month'],
                                         0]
        comMedOptDict['care_gap_011'] = [pd.Interval( modelParam['otter_care_gap_comm_med_opt_a1c_uncontrolled_threshold'] ,18,closed='right'),
                                         ['como_obesity'],
                                         ['ckd_1','ckd_2','ckd_3','ckd_4','ckd_5','ckd_unspecified','ckd_esrd','como_heart_failure','como_ascvd'],
                                         ['rx_biguanides_last_12_month'],
                                         ['rx_biguanides_pdc_last_12_month'],
                                         1,
                                         ['rx_glp1_agonist_last_12_month','rx_sglt2_inhibitors_last_12_month'],
                                         1]

        comMedOptDict['care_gap_014'] = [pd.Interval( modelParam['otter_care_gap_comm_med_opt_a1c_uncontrolled_threshold'] ,18,closed='right'),
                                         ['como_ascvd'], #'como_obesity'], ### RW Review
                                         ['ckd_1','ckd_2','ckd_3','ckd_4','ckd_5','ckd_unspecified','ckd_esrd','como_heart_failure','como_obesity'],
                                         ['rx_biguanides_last_12_month'],
                                         ['rx_biguanides_pdc_last_12_month'],
                                         None,
                                         ['rx_glp1_agonist_last_12_month','rx_sglt2_inhibitors_last_12_month'],
                                        0]
        comMedOptDict['care_gap_015XX'] = [pd.Interval( modelParam['otter_care_gap_comm_med_opt_a1c_uncontrolled_threshold'] ,18,closed='right'),
                                         ['como_ascvd'],
                                         ['ckd_1','ckd_2','ckd_3','ckd_4','ckd_5','ckd_unspecified','ckd_esrd','como_heart_failure'],
                                         ['rx_biguanides_last_12_month'],
                                         ['rx_biguanides_pdc_last_12_month'],
                                         1,
                                         ['rx_sglt2_inhibitors_last_12_month','rx_glp1_agonist_last_12_month'],
                                         1]
        comMedOptDict['care_gap_018'] = [pd.Interval( modelParam['otter_care_gap_comm_med_opt_a1c_uncontrolled_threshold'] ,18,closed='right'),
                                         ['como_heart_failure', 'ckd_1', 'ckd_2', 'ckd_3', 'ckd_unspecified'],
                                         ['ckd_4','ckd_5','ckd_esrd'],
                                         ['rx_biguanides_last_12_month'],
                                         ['rx_biguanides_pdc_last_12_month'],
                                         None,
                                         None,
                                         None]
        comMedOptDict['care_gap_019'] = [pd.Interval( modelParam['otter_care_gap_comm_med_opt_a1c_uncontrolled_threshold'] ,18,closed='right'),
                                         ['como_heart_failure', 'ckd_1', 'ckd_2', 'ckd_3', 'ckd_unspecified'],
                                         ['ckd_4','ckd_5','ckd_esrd'],
                                         ['rx_biguanides_last_12_month'],
                                         ['rx_biguanides_pdc_last_12_month'],
                                         1,
                                         ['rx_sglt2_inhibitors_last_12_month'],
                                         0]
        ##
        ## commercial care gaps for 4th line medical optimization
        ##
        comMedOpt4thLineDict = {}
        comMedOpt4thLineDict['care_gap_005'] = [pd.Interval(2, 18, closed='both'),
                                                None,
                                                None,
                                                ['rx_biguanides_last_12_month'],
                                                ['rx_biguanides_pdc_last_12_month'],
                                                2,
                                                None,
                                                None]
        comMedOpt4thLineDict['care_gap_013'] = [pd.Interval(2, 18, closed='both'),
                                                ['ckd_1', 'ckd_2', 'ckd_3', 'ckd_4', 'ckd_5', 'ckd_unspecified',
                                                 'ckd_esrd', 'como_heart_failure', 'como_ascvd', 'como_obesity'],
                                                None,
                                                ['rx_biguanides_last_12_month'],
                                                ['rx_biguanides_pdc_last_12_month'],
                                                2,
                                                ['rx_insulin_last_12_month'],
                                                0]
        # upload for general consumption
        modelParam['otter_care_gap_com_medOpt'] = comMedOptDict
        modelParam['otter_care_gap_com_medOpt_4thline'] = comMedOpt4thLineDict

        ##
        ## commercial care gaps for device
        ## 
        comDeviceSMBG5Dict = {}
        comDeviceSMBG5Dict['care_gap_121'] = ['rx_insulin_last_12_month',
                                              ['rx_test_test_strip_last_6_month', 'rx_test_glucose_meter_last_6_month',
                                               'rx_test_glucose_monitor_last_6_month']]

        comDeviceSMBG7Dict = {}
        comDeviceSMBG7Dict['care_gap_122'] = ['hypoglycemia_diagnosis_12_month',
                                              'rx_insulin_last_12_month',
                                              ['rx_test_test_strip_last_6_month', 'rx_test_glucose_meter_last_6_month',
                                               'rx_test_glucose_monitor_last_6_month'],
                                              'rx_sulfonylureas_last_12_month',
                                              'lab_a1c_12mo']
        modelParam['otter_care_gap_com_deviceSMBG5'] = comDeviceSMBG5Dict
        modelParam['otter_care_gap_com_deviceSMBG7'] = comDeviceSMBG7Dict

        ##
        ## medicare care considerations 
        ##
        
        
        med_careConsiderationDict = {}
        med_careConsiderationDict['care_gap_628'] = 'me74'
        med_careConsiderationDict['care_gap_629'] = 'me75'
        med_careConsiderationDict['care_gap_630'] = 'me105'
        med_careConsiderationDict['care_gap_631'] = 'me120'
        med_careConsiderationDict['care_gap_632'] = 'me160'
        med_careConsiderationDict['care_gap_633'] = 'me323'
        med_careConsiderationDict['care_gap_634'] = 'me374'
        med_careConsiderationDict['care_gap_635'] = 'me397'
        med_careConsiderationDict['care_gap_636'] = 'me402'
        med_careConsiderationDict['care_gap_637'] = 'me468'
        med_careConsiderationDict['care_gap_638'] = 'me721'
        med_careConsiderationDict['care_gap_639'] = 'me779'
        med_careConsiderationDict['care_gap_640'] = 'me780'
        med_careConsiderationDict['care_gap_641'] = 'me842'
        med_careConsiderationDict['care_gap_642'] = 'me1008'
        med_careConsiderationDict['care_gap_643'] = 'me1183'
        med_careConsiderationDict['care_gap_644'] = 'me1250'
        med_careConsiderationDict['care_gap_645'] = 'me1312'
        med_careConsiderationDict['care_gap_646'] = 'me1317'
        med_careConsiderationDict['care_gap_647'] = 'me1364'
        med_careConsiderationDict['care_gap_648'] = 'me1367'
        med_careConsiderationDict['care_gap_649'] = 'me1387'
        med_careConsiderationDict['care_gap_650'] = 'me1388'
        med_careConsiderationDict['care_gap_651'] = 'me1395'
        med_careConsiderationDict['care_gap_652'] = 'me1422'
        med_careConsiderationDict['care_gap_653'] = 'me1440'
        med_careConsiderationDict['care_gap_654'] = 'me99035'
       
      
        modelParam['otter_care_gap_med_carecon'] = med_careConsiderationDict
        
        ##
        ## medicare care gaps for medical adherence
        ##
        medMedAdherenceDict = {}
        medMedAdherenceDict['care_gap_233'] = ['rx_alpha_glucosidase_inhibitor_last_12_month',
                                               'rx_alpha_glucosidase_inhibitor_pdc_last_12_month']
        medMedAdherenceDict['care_gap_234'] = ['rx_biguanides_last_12_month', 'rx_biguanides_pdc_last_12_month']
        medMedAdherenceDict['care_gap_235'] = ['rx_dpp_4_inhibitors_last_12_month',
                                               'rx_dpp_4_inhibitors_pdc_last_12_month']
        medMedAdherenceDict['care_gap_236'] = ['rx_glp1_agonist_last_12_month', 'rx_glp1_agonist_pdc_last_12_month']
        medMedAdherenceDict['care_gap_238'] = ['rx_meglitinide_analogues_last_12_month',
                                               'rx_meglitinide_analogues_pdc_last_12_month']
        medMedAdherenceDict['care_gap_239'] = ['rx_sglt2_inhibitors_last_12_month',
                                               'rx_sglt2_inhibitors_pdc_last_12_month']
        medMedAdherenceDict['care_gap_240'] = ['rx_glipizide_last_12_month', 'rx_glipizide_pdc_last_12_month']
        medMedAdherenceDict['care_gap_241'] = ['rx_thiazolidinediones_last_12_month',
                                               'rx_thiazolidinediones_pdc_last_12_month']
        medMedAdherenceDict['care_gap_242'] = ['rx_statins_last_12_month', 'rx_statins_pdc_last_12_month']
        # input into model Param
        modelParam['otter_care_gap_med_medAdh'] = comMedAdherenceDict

        ##
        ## medicare care gaps for medical optimization
        ##

        # threshold for controlled vs uncontrolled
        modelParam['otter_care_gap_comm_medi_opt_a1c_uncontrolled_threshold'] = 7.5  # updated to 7.5 by product 27apr2020

        # dictionary of values
        medMedOptDict = {}
        medMedOptDict['care_gap_200XX'] = [
            pd.Interval(modelParam['otter_care_gap_comm_medi_opt_a1c_uncontrolled_threshold'], 11, closed='neither'),
            None,
            ['ckd_4', 'ckd_5', 'ckd_esrd'],
            None, None, None, None, None]
        medMedOptDict['care_gap_201'] = [pd.Interval(11, 18, closed='both'),
                                         None, None, None, None, None, None, None]
        medMedOptDict['care_gap_202'] = [pd.Interval(2, 11, closed='left'),
                                         ['ckd_4', 'ckd_5', 'ckd_esrd'],
                                         None, None, None, None, None, None]
        medMedOptDict['care_gap_549'] = [
            pd.Interval(modelParam['otter_care_gap_comm_medi_opt_a1c_uncontrolled_threshold'], 18, closed='right'),
            None,
            None,
            ['rx_biguanides_last_12_month'],
            ['rx_biguanides_pdc_last_12_month'],
            None, None, None]
        medMedOptDict['care_gap_550'] = [
            pd.Interval(modelParam['otter_care_gap_comm_medi_opt_a1c_uncontrolled_threshold'], 18, closed='right'),
            None,
            None,
            ['rx_biguanides_last_12_month'],
            ['rx_biguanides_pdc_last_12_month'],
            1,
            None, None]
        # medMedOptDict['care_gap_552'] = [
        #     pd.Interval(modelParam['otter_care_gap_comm_medi_opt_a1c_uncontrolled_threshold'], 18, closed='right'),
        #     None,
        #     ['ckd_1', 'ckd_2', 'ckd_3', 'ckd_4', 'ckd_5', 'ckd_unspecified', 'ckd_esrd', 'como_heart_failure',
        #      'como_ascvd', 'como_obesity'],
        #     ['rx_biguanides_last_12_month'],
        #     ['rx_biguanides_pdc_last_12_month'],
        #     0,
        #     None, None]
        # medMedOptDict['care_gap_553'] = [
        #     pd.Interval(modelParam['otter_care_gap_comm_medi_opt_a1c_uncontrolled_threshold'], 18, closed='right'),
        #     ['como_obesity'],
        #     ['ckd_1', 'ckd_2', 'ckd_3', 'ckd_4', 'ckd_5', 'ckd_unspecified', 'ckd_esrd', 'como_heart_failure',
        #      'como_ascvd'],
        #     ['rx_biguanides_last_12_month'],
        #     ['rx_biguanides_pdc_last_12_month'],
        #     None,
        #     ['rx_glp1_agonist_last_12_month', 'rx_sglt2_inhibitors_last_12_month'],
        #     0]
        # medMedOptDict['care_gap_554'] = [
        #     pd.Interval(modelParam['otter_care_gap_comm_medi_opt_a1c_uncontrolled_threshold'], 18, closed='right'),
        #     ['como_ascvd'],
        #     ['ckd_1', 'ckd_2', 'ckd_3', 'ckd_4', 'ckd_5', 'ckd_unspecified', 'ckd_esrd', 'como_heart_failure'],
        #     ['rx_biguanides_last_12_month'],
        #     ['rx_biguanides_pdc_last_12_month'],
        #     None,
        #     ['rx_glp1_agonist_last_12_month', 'rx_sglt2_inhibitors_last_12_month'],
        #     0]
        # medMedOptDict['care_gap_555'] = [
        #     pd.Interval(modelParam['otter_care_gap_comm_medi_opt_a1c_uncontrolled_threshold'], 18, closed='right'),
        #     ['como_heart_failure', 'ckd_1', 'ckd_2', 'ckd_3', 'ckd_unspecified'],
        #     ['ckd_4', 'ckd_5', 'ckd_esrd'],
        #     ['rx_biguanides_last_12_month'],
        #     ['rx_biguanides_pdc_last_12_month'],
        #     None,
        #     None,
        #     None]
        # medMedOptDict['care_gap_556'] = [
        #     pd.Interval(modelParam['otter_care_gap_comm_medi_opt_a1c_uncontrolled_threshold'], 18, closed='right'),
        #     None,
        #     ['ckd_1', 'ckd_2', 'ckd_3', 'ckd_4', 'ckd_5', 'ckd_unspecified', 'ckd_esrd', 'como_heart_failure',
        #      'como_ascvd', 'como_obesity'],
        #     ['rx_biguanides_last_12_month'],
        #     ['rx_biguanides_pdc_last_12_month'],
        #     1,
        #     ['rx_glp1_agonist_last_12_month'],
        #     0]
        # medMedOptDict['care_gap_557'] = [
        #     pd.Interval(modelParam['otter_care_gap_comm_medi_opt_a1c_uncontrolled_threshold'], 18, closed='right'),
        #     ['como_obesity'],
        #     ['ckd_1', 'ckd_2', 'ckd_3', 'ckd_4', 'ckd_5', 'ckd_unspecified', 'ckd_esrd', 'como_heart_failure',
        #      'como_ascvd'],
        #     ['rx_biguanides_last_12_month'],
        #     ['rx_biguanides_pdc_last_12_month'],
        #     1,
        #     ['rx_glp1_agonist_last_12_month', 'rx_sglt2_inhibitors_last_12_month'],
        #     1]
        # medMedOptDict['care_gap_560'] = [
        #     pd.Interval(modelParam['otter_care_gap_comm_medi_opt_a1c_uncontrolled_threshold'], 18, closed='right'),
        #     ['como_ascvd'],
        #     ['ckd_1', 'ckd_2', 'ckd_3', 'ckd_4', 'ckd_5', 'ckd_unspecified', 'ckd_esrd', 'como_heart_failure'],
        #     ['rx_biguanides_last_12_month'],
        #     ['rx_biguanides_pdc_last_12_month'],
        #     1,
        #     ['rx_glp1_agonist_last_12_month', 'rx_sglt2_inhibitors_last_12_month'],
        #     1]

        # medMedOptDict['care_gap_562'] = [
        #     pd.Interval(modelParam['otter_care_gap_comm_medi_opt_a1c_uncontrolled_threshold'], 18, closed='right'),
        #     ['como_heart_failure', 'ckd_1', 'ckd_2', 'ckd_3', 'ckd_unspecified'],
        #     ['ckd_4', 'ckd_5', 'ckd_esrd'],
        #     ['rx_biguanides_last_12_month'],
        #     ['rx_biguanides_pdc_last_12_month'],
        #     1,
        #     ['rx_sglt2_inhibitors_last_12_month'],
        #     0]
        # input into model Param
        modelParam['otter_care_gap_med_medOpt'] = medMedOptDict

        medMedOpt4thlineDict = {}
        medMedOpt4thlineDict['care_gap_565'] = [pd.Interval(2, 18, closed='both'),
                                                ['ckd_1', 'ckd_2', 'ckd_3', 'ckd_4', 'ckd_5', 'ckd_unspecified',
                                                 'ckd_esrd', 'como_heart_failure', 'como_ascvd', 'como_obesity'],
                                                None,
                                                ['rx_biguanides_last_12_month'],
                                                ['rx_biguanides_pdc_last_12_month'],
                                                2,
                                                ['rx_insulin_last_12_month'],
                                                0]
        # input into model Param
        modelParam['otter_care_gap_med_medOpt_4thline'] = medMedOpt4thlineDict

        ##
        ## comorbidity
        ##
        comorbidityDict = {}
        comorbidityDict['care_gap_400'] = 'como_alcoholism'
        comorbidityDict['care_gap_402'] = 'como_asthma'
        comorbidityDict['care_gap_407'] = 'como_chronic_renal_failure'
        comorbidityDict['care_gap_408'] = 'como_depression'
        comorbidityDict['care_gap_410'] = 'como_heart_failure'
        comorbidityDict['care_gap_412'] = 'como_hyperlipidemia'
        comorbidityDict['care_gap_413'] = 'como_hypertension'
        comorbidityDict['care_gap_414'] = 'como_iron_deficiency_anemia'
        comorbidityDict['care_gap_416'] = 'como_low_vision_and_blindness'
        comorbidityDict['care_gap_417'] = 'como_metabolic_syndrome'
        comorbidityDict['care_gap_418'] = 'como_obesity'
        # input into model Param
        modelParam['otter_care_gap_med_comor'] = comorbidityDict

        ##
        ## medicare care gaps for monitering gaps
        ##              
        medMoniterPcpDict = {}
        medMoniterPcpDict['care_gap_247'] = 'office_visit_cpt_12mo'
        medMoniterLipidDict = {}
        medMoniterLipidDict['care_gap_260'] = ['triglyceride_cpt_12mo',
                                               ['total_cholesterol_cpt_12mo', 'cholesterol_hdl_cpt_12mo',
                                                'cholesterol_ldl_cpt_12mo']]
        modelParam['otter_care_gap_med_moniter_pcp'] = medMoniterPcpDict
        modelParam['otter_care_gap_med_moniter_lipid'] = medMoniterLipidDict
        ##
        ## medicare care gaps for device
        ## 
        medDeviceSMBG5Dict = {}
        medDeviceSMBG5Dict['care_gap_124'] = ['rx_insulin_last_12_month',
                                              ['rx_test_test_strip_last_6_month', 'rx_test_glucose_meter_last_6_month',
                                               'rx_test_glucose_monitor_last_6_month']]
        medDeviceSMBG7Dict = {}
        medDeviceSMBG7Dict['care_gap_125'] = ['hypoglycemia_diagnosis_12_month', 'rx_insulin_last_12_month',
                                              ['rx_test_test_strip_last_6_month', 'rx_test_glucose_meter_last_6_month',
                                               'rx_test_glucose_monitor_last_6_month'],
                                              'rx_sulfonylureas_last_12_month', 'lab_a1c_12mo']
        modelParam['otter_care_gap_med_deviceSMBG5'] = medDeviceSMBG5Dict
        modelParam['otter_care_gap_med_deviceSMBG7'] = medDeviceSMBG7Dict

        ####
        #### hippo
        ####

        # outcome column of interest
        modelParam['hippo_model_outcomeColName'] = 'lab_a1c'  # lab_a1c_12mo

        # share of members to run the model on (0.0 = 0% of members, 1.0 = 100% of members)
        modelParam['hippo_model_memberShare'] = 1.0

        # kfold number
        modelParam['hippo_model_kfold'] = 3

        # name of the pickled saved model object
        modelParam['hippo_model_pickleName'] = None  # 'a1cModel_xgboost.dat'

        # true if saving the pickle object, else False
        modelParam['hippo_model_pickleSave'] = False

        # true if we are going to optimize the model, else False
        modelParam['hippo_model_hyperoptGo'] = False

        # in hyperopt, how many times we are to evaluate
        modelParam['hippo_model_maxEval'] = 3

        # unseen if you want the prediction recalculated on unseen people, seen if you want it calculated on seen people (artifically high)
        modelParam['hippo_model_seenUnseen'] = 'unseen'

        # name of new model
        modelParam['hippo_model_newPickleName'] = 'a1cModel_catBoost.dat'

        # model spacers
        modelParam['hippo_model_space'] = {
            'n_estimators': 500,
            'eta': hp.quniform('eta', 0.025, 0.5, 0.025),
            'max_depth': hp.choice('max_depth', np.arange(2, 10, dtype=int)),
            'min_child_weight': hp.quniform('min_child_weight', 1, 6, 1),
            'subsample': hp.quniform('subsample', 0.5, 1, 0.05),
            'gamma': hp.quniform('gamma', 0.05, 0.1, 0.05),
            'colsample_bytree': hp.quniform('colsample_bytree', 0.5, 1, 0.05),
            'eval_metric': 'mae',
            'objective': 'reg:squarederror',
            'nthread': 8,
            'booster': 'gbtree',
            'tree_method': 'exact',
            'silent': 1,
            'error_score': 'raise',
            'seed': 42
        }

        # suffix of impact features
        modelParam['hippo_model_impact_label'] = "_shap"

        ####
        #### moose inputs
        ####

        # names of columns with the lob indications
        modelParam['moose_lob_column_dict'] = dict(zip(['insure_med_com_full',
                                                        'insure_med_com_self',
                                                        'insure_med_com_split',
                                                        'insure_med_med_group',
                                                        'insure_med_med_indiv'],
                                                       ['commercial_full',
                                                        'commercial_self',
                                                        'commercial_split',
                                                        'medicare_group',
                                                        'medicare_indiv']))

        # dictionary with the names of each care gap
        mooseImpactFeatureNameDict = {}
        mooseImpactFeatureNameDict['care_gap_001xx'] = 'med_opt_one_metformin_comm'
        mooseImpactFeatureNameDict['care_gap_200xx'] = 'med_opt_one_metformin_medi'
        mooseImpactFeatureNameDict['care_gap_002'] = 'med_opt_one_insulin_comm'
        mooseImpactFeatureNameDict['care_gap_201'] = 'med_opt_one_insulin_medi'
        mooseImpactFeatureNameDict['care_gap_002xx'] = 'med_opt_one_glp1_dpp4_comm'
        mooseImpactFeatureNameDict['care_gap_202'] = 'med_opt_one_glp1_dpp4_medi'
        mooseImpactFeatureNameDict['care_gap_003'] = 'med_opt_two_general_comm'
        mooseImpactFeatureNameDict['care_gap_549'] = 'med_opt_two_general_medi'
        mooseImpactFeatureNameDict['care_gap_004'] = 'med_opt_three_general_comm'
        mooseImpactFeatureNameDict['care_gap_550'] = 'med_opt_three_general_medi'
        mooseImpactFeatureNameDict['care_gap_005'] = 'med_opt_four_general_comm'
        mooseImpactFeatureNameDict['care_gap_006'] = 'med_opt_two_ex_all_como_comm'
        #mooseImpactFeatureNameDict['care_gap_552'] = 'med_opt_two_ex_all_como_medi'
        mooseImpactFeatureNameDict['care_gap_007'] = 'med_opt_three_ex_all_como_comm'
        #mooseImpactFeatureNameDict['care_gap_556'] = 'med_opt_three_ex_all_como_medi'
        mooseImpactFeatureNameDict['care_gap_010'] = 'med_opt_two_obese_glp1_comm'
        #mooseImpactFeatureNameDict['care_gap_553'] = 'med_opt_two_obese_glp1_medi'
        mooseImpactFeatureNameDict['care_gap_011'] = 'med_opt_three_obese_sglt2_comm'
        #mooseImpactFeatureNameDict['care_gap_557'] = 'med_opt_three_obese_sglt2_medi'
        mooseImpactFeatureNameDict['care_gap_013'] = 'med_opt_four_insulin_comm'
        mooseImpactFeatureNameDict['care_gap_565'] = 'med_opt_four_insulin_medi'
        mooseImpactFeatureNameDict['care_gap_014'] = 'med_opt_two_cvd_glp1_sglt2_comm'
        #mooseImpactFeatureNameDict['care_gap_554'] = 'med_opt_two_cvd_glp1_sglt2_medi'
        mooseImpactFeatureNameDict['care_gap_015xx'] = 'med_opt_three_cvd_sglt2_glp1_comm'
        #mooseImpactFeatureNameDict['care_gap_560'] = 'med_opt_three_cvd_sglt2_glp1_medi'
        mooseImpactFeatureNameDict['care_gap_018'] = 'med_opt_two_chf_ckd123_sglt2_comm'
        #mooseImpactFeatureNameDict['care_gap_555'] = 'med_opt_two_chf_ckd123_sglt2_medi'
        mooseImpactFeatureNameDict['care_gap_019'] = 'med_opt_three_chf_ckd123_glp1_comm'
        #mooseImpactFeatureNameDict['care_gap_562'] = 'med_opt_three_chf_ckd123_glp1_medi'
        mooseImpactFeatureNameDict['care_gap_038'] = 'med_adh_alpha_glucose'
        mooseImpactFeatureNameDict['care_gap_039'] = 'med_adh_metformin'
        mooseImpactFeatureNameDict['care_gap_040'] = 'med_adh_dpp4'
        mooseImpactFeatureNameDict['care_gap_041'] = 'med_adh_glp1'
        mooseImpactFeatureNameDict['care_gap_043'] = 'med_adh_meglitinide'
        mooseImpactFeatureNameDict['care_gap_044'] = 'med_adh_sglt2'
        mooseImpactFeatureNameDict['care_gap_045'] = 'med_adh_sulfonylureas'
        mooseImpactFeatureNameDict['care_gap_046'] = 'med_adh_tdz'
        mooseImpactFeatureNameDict['care_gap_047'] = 'med_adh_statins'
        mooseImpactFeatureNameDict['care_gap_053'] = 'screen_pcp_comm'
        mooseImpactFeatureNameDict['care_gap_247'] = 'screen_pcp_medi'
        mooseImpactFeatureNameDict['care_gap_072'] = 'screen_lipid_comm'
        mooseImpactFeatureNameDict['care_gap_260'] = 'screen_lipid_medi'
        mooseImpactFeatureNameDict['care_gap_121'] = 'smbg5_comm'
        mooseImpactFeatureNameDict['care_gap_122'] = 'smbg7_comm'
        mooseImpactFeatureNameDict['care_gap_124'] = 'smbg14_medi'
        mooseImpactFeatureNameDict['care_gap_125'] = 'smbg16_medi'
        mooseImpactFeatureNameDict['care_gap_400'] = 'como_alcoholism'
        mooseImpactFeatureNameDict['care_gap_402'] = 'como_asthma'
        mooseImpactFeatureNameDict['care_gap_407'] = 'como_chronic_renal_failure'
        mooseImpactFeatureNameDict['care_gap_408'] = 'como_depression'
        mooseImpactFeatureNameDict['care_gap_410'] = 'como_heart_failure'
        mooseImpactFeatureNameDict['care_gap_412'] = 'como_hyperlipidemia'
        mooseImpactFeatureNameDict['care_gap_413'] = 'como_hypertension'
        mooseImpactFeatureNameDict['care_gap_414'] = 'como_iron_deficiency_anemia'
        mooseImpactFeatureNameDict['care_gap_416'] = 'como_low_vision_and_blindness'
        mooseImpactFeatureNameDict['care_gap_417'] = 'como_metabolic_syndrome'
        mooseImpactFeatureNameDict['care_gap_418'] = 'como_obesity'
        
        mooseImpactFeatureNameDict['care_gap_600'] = 'cc_screen_eye_exam_comm'
        mooseImpactFeatureNameDict['care_gap_601'] = 'cc_screen_a1c_comm'
        mooseImpactFeatureNameDict['care_gap_602'] = 'cc_screen_liver_comm'
        mooseImpactFeatureNameDict['care_gap_603'] = 'cc_screen_albuminuria_comm'
        mooseImpactFeatureNameDict['care_gap_604'] = 'cc_med_opt_flu_vacc_comm'
        mooseImpactFeatureNameDict['care_gap_605'] = 'cc_med_opt_pneumoco23_vacc_comm'
        mooseImpactFeatureNameDict['care_gap_606'] = 'cc_med_opt_add_ace_or_arb_comm'
        mooseImpactFeatureNameDict['care_gap_607'] = 'cc_med_opt_metformin_contra_ckd_comm'
        mooseImpactFeatureNameDict['care_gap_608'] = 'cc_med_opt_glitazones_transaminases_elevation_comm'
        mooseImpactFeatureNameDict['care_gap_609'] = 'cc_med_opt_repaglinide_contra_gemfibrozil_comm'
        mooseImpactFeatureNameDict['care_gap_610'] = 'cc_med_opt_pramlintide_contra_gastroparesis_comm'
        mooseImpactFeatureNameDict['care_gap_611'] = 'cc_med_opt_pramlintide_avoid_anticholinergic_comm'
        mooseImpactFeatureNameDict['care_gap_612'] = 'cc_med_opt_estrogen_contain_contraceptives_comm'
        mooseImpactFeatureNameDict['care_gap_613'] = 'cc_med_opt_thiazolidinediones_comm'
        mooseImpactFeatureNameDict['care_gap_614'] = 'cc_como_pancreatitis_comm'
        mooseImpactFeatureNameDict['care_gap_615'] = 'cc_med_opt_hepatitis_b_vacc_comm'
        mooseImpactFeatureNameDict['care_gap_616'] = 'cc_med_opt_ckd_avoid_dm_drug_comm'
        mooseImpactFeatureNameDict['care_gap_617'] = 'cc_med_opt_sglt2_contra_renal_impair_comm'
        mooseImpactFeatureNameDict['care_gap_618'] = 'cc_med_opt_statin_comm'
        mooseImpactFeatureNameDict['care_gap_619'] = 'cc_med_opt_glp1_contra_MTC_comm'
        mooseImpactFeatureNameDict['care_gap_620'] = 'cc_med_opt_alphaglucose_avoid_renal_impair_comm'
        mooseImpactFeatureNameDict['care_gap_621'] = 'cc_med_opt_exenatide_avoid_renal_impair_comm'
        mooseImpactFeatureNameDict['care_gap_622'] = 'cc_med_opt_inhaled_insulin_contra_cld_comm'
        mooseImpactFeatureNameDict['care_gap_623'] = 'cc_screen_inhaled_insulin_spirometry_comm'
        mooseImpactFeatureNameDict['care_gap_624'] = 'cc_med_opt_DM_drug_acute_kidney_injury_comm'
        mooseImpactFeatureNameDict['care_gap_625'] = 'cc_screen_metformin_vb12_comm'
        mooseImpactFeatureNameDict['care_gap_626'] = 'cc_med_opt_canaliflozin_leg_foot_amputation_comm'
        mooseImpactFeatureNameDict['care_gap_627'] = 'cc_lifestyle_smoke_cessation_comm'
        
        mooseImpactFeatureNameDict['care_gap_628'] = 'cc_screen_eye_exam_medi'
        mooseImpactFeatureNameDict['care_gap_629'] = 'cc_screen_a1c_medi'
        mooseImpactFeatureNameDict['care_gap_630'] = 'cc_screen_liver_medi'
        mooseImpactFeatureNameDict['care_gap_631'] = 'cc_screen_albuminuria_medi'
        mooseImpactFeatureNameDict['care_gap_632'] = 'cc_med_opt_avoid_su_in_old_medi'
        mooseImpactFeatureNameDict['care_gap_633'] = 'cc_med_opt_flu_vacc_medi'
        mooseImpactFeatureNameDict['care_gap_634'] = 'cc_med_opt_pneumoco23_vacc_medi'
        mooseImpactFeatureNameDict['care_gap_635'] = 'cc_med_opt_add_ace_or_arb_medi'
        mooseImpactFeatureNameDict['care_gap_636'] = 'cc_med_opt_metformin_contra_ckd_medi'
        mooseImpactFeatureNameDict['care_gap_637'] = 'cc_med_opt_glitazones_transaminases_elevation_medi'
        mooseImpactFeatureNameDict['care_gap_638'] = 'cc_med_opt_repaglinide_contra_gemfibrozil_medi'
        mooseImpactFeatureNameDict['care_gap_639'] = 'cc_med_opt_pramlintide_contra_gastroparesis_medi'
        mooseImpactFeatureNameDict['care_gap_640'] = 'cc_med_opt_pramlintide_avoid_anticholinergic_medi'
        mooseImpactFeatureNameDict['care_gap_641'] = 'cc_med_opt_thiazolidinediones_medi'
        mooseImpactFeatureNameDict['care_gap_642'] = 'cc_como_pancreatitis_medi'
        mooseImpactFeatureNameDict['care_gap_643'] = 'cc_med_opt_ckd_avoid_dm_drug_medi'
        mooseImpactFeatureNameDict['care_gap_644'] = 'cc_med_opt_sglt2_contra_renal_impair_medi'
        mooseImpactFeatureNameDict['care_gap_645'] = 'cc_med_opt_statin_medi'
        mooseImpactFeatureNameDict['care_gap_646'] = 'cc_med_opt_glp1_contra_MTC_medi'
        mooseImpactFeatureNameDict['care_gap_647'] = 'cc_med_opt_alphaglucose_avoid_renal_impair_medi'
        mooseImpactFeatureNameDict['care_gap_648'] = 'cc_med_opt_exenatide_avoid_renal_impair_medi'
        mooseImpactFeatureNameDict['care_gap_649'] = 'cc_med_opt_inhaled_insulin_contra_cld_medi'
        mooseImpactFeatureNameDict['care_gap_650'] = 'cc_screen_inhaled_insulin_spirometry_medi'
        mooseImpactFeatureNameDict['care_gap_651'] = 'cc_med_opt_DM_drug_acute_kidney_injury_medi'
        mooseImpactFeatureNameDict['care_gap_652'] = 'cc_screen_metformin_vb12_medi'
        mooseImpactFeatureNameDict['care_gap_653'] = 'cc_med_opt_canaliflozin_leg_foot_amputation_medi'
        mooseImpactFeatureNameDict['care_gap_654'] = 'cc_lifestyle_smoke_cessation_medi'

        modelParam['moose_impact_feature_name'] = mooseImpactFeatureNameDict

        # list of features (care gaps) that we want to understand the impact of
        modelParam['moose_impact_feature_list'] = [x for x in mooseImpactFeatureNameDict.keys()]

        # get the lit impact of each feature
        # names of each of the care gaps

        mooseImpactFeatureLitDict = {}
        mooseImpactFeatureLitDict['care_gap_001xx'] = 1.25
        mooseImpactFeatureLitDict['care_gap_200xx'] = 1.25
        mooseImpactFeatureLitDict['care_gap_002'] = 1.96
        mooseImpactFeatureLitDict['care_gap_201'] = 1.96
        mooseImpactFeatureLitDict['care_gap_002xx'] = 1.125
        mooseImpactFeatureLitDict['care_gap_202'] = 1.125
        mooseImpactFeatureLitDict['care_gap_003'] = 1.125
        mooseImpactFeatureLitDict['care_gap_549'] = 1.125
        mooseImpactFeatureLitDict['care_gap_004'] = 1.125
        mooseImpactFeatureLitDict['care_gap_550'] = 1.125
        mooseImpactFeatureLitDict['care_gap_005'] = 1.0
        mooseImpactFeatureLitDict['care_gap_551']= 1.0
        mooseImpactFeatureLitDict['care_gap_006'] = 1.125
        mooseImpactFeatureLitDict['care_gap_552'] = 1.125
        mooseImpactFeatureLitDict['care_gap_007'] = 1.125
        mooseImpactFeatureLitDict['care_gap_556'] = 1.125
        mooseImpactFeatureLitDict['care_gap_010'] = 1.125
        mooseImpactFeatureLitDict['care_gap_553'] = 1.125
        mooseImpactFeatureLitDict['care_gap_011'] = 1.125
        mooseImpactFeatureLitDict['care_gap_557'] = 1.125
        mooseImpactFeatureLitDict['care_gap_013'] = 1.125
        mooseImpactFeatureLitDict['care_gap_565'] = 1.125
        mooseImpactFeatureLitDict['care_gap_014'] = 1.125
        mooseImpactFeatureLitDict['care_gap_554'] = 1.125
        mooseImpactFeatureLitDict['care_gap_015xx'] = 1.125
        mooseImpactFeatureLitDict['care_gap_560'] = 1.125
        mooseImpactFeatureLitDict['care_gap_018'] = 1.125
        mooseImpactFeatureLitDict['care_gap_555'] = 1.125
        mooseImpactFeatureLitDict['care_gap_019'] = 1.125
        mooseImpactFeatureLitDict['care_gap_562'] = 1.125
        mooseImpactFeatureLitDict['care_gap_038'] = 1.0
        mooseImpactFeatureLitDict['care_gap_039'] = 1.0
        mooseImpactFeatureLitDict['care_gap_040'] = 1.0
        mooseImpactFeatureLitDict['care_gap_041'] = 1.0
        mooseImpactFeatureLitDict['care_gap_043'] = 1.0
        mooseImpactFeatureLitDict['care_gap_044'] = 1.0
        mooseImpactFeatureLitDict['care_gap_045'] = 1.0
        mooseImpactFeatureLitDict['care_gap_046'] = 1.0
        mooseImpactFeatureLitDict['care_gap_047'] = 1.0
        mooseImpactFeatureLitDict['care_gap_053'] = 0.3
        mooseImpactFeatureLitDict['care_gap_247'] = 0.3
        mooseImpactFeatureLitDict['care_gap_072'] = 0.3
        mooseImpactFeatureLitDict['care_gap_260'] = 0.3
        mooseImpactFeatureLitDict['care_gap_121'] = 0.3
        mooseImpactFeatureLitDict['care_gap_122'] = 0.3
        mooseImpactFeatureLitDict['care_gap_124'] = 0.3
        mooseImpactFeatureLitDict['care_gap_125'] = 0.3
        mooseImpactFeatureLitDict['care_gap_400'] = 0.3
        mooseImpactFeatureLitDict['care_gap_402'] = 0.3
        mooseImpactFeatureLitDict['care_gap_407'] = 0.3
        mooseImpactFeatureLitDict['care_gap_408'] = 0.3
        mooseImpactFeatureLitDict['care_gap_410'] = 0.3
        mooseImpactFeatureLitDict['care_gap_412'] = 0.3
        mooseImpactFeatureLitDict['care_gap_413'] = 0.3
        mooseImpactFeatureLitDict['care_gap_414'] = 0.3
        mooseImpactFeatureLitDict['care_gap_416'] = 0.3
        mooseImpactFeatureLitDict['care_gap_417'] = 0.3
        mooseImpactFeatureLitDict['care_gap_418'] = 0.3
        
        mooseImpactFeatureLitDict['care_gap_600'] = 0.3
        mooseImpactFeatureLitDict['care_gap_601'] = 0.3
        mooseImpactFeatureLitDict['care_gap_602'] = 0.3
        mooseImpactFeatureLitDict['care_gap_603'] = 0.3
        mooseImpactFeatureLitDict['care_gap_604'] = 0.3
        mooseImpactFeatureLitDict['care_gap_605'] = 0.3
        mooseImpactFeatureLitDict['care_gap_606'] = 0.3
        mooseImpactFeatureLitDict['care_gap_607'] = 0.3
        mooseImpactFeatureLitDict['care_gap_608'] = 0.3
        mooseImpactFeatureLitDict['care_gap_609'] = 0.3
        mooseImpactFeatureLitDict['care_gap_610'] = 0.3
        mooseImpactFeatureLitDict['care_gap_611'] = 0.3
        mooseImpactFeatureLitDict['care_gap_612'] = 0.3
        mooseImpactFeatureLitDict['care_gap_613'] = 0.3
        mooseImpactFeatureLitDict['care_gap_614'] = 0.3
        mooseImpactFeatureLitDict['care_gap_615'] = 0.3
        mooseImpactFeatureLitDict['care_gap_616'] = 0.3
        mooseImpactFeatureLitDict['care_gap_617'] = 0.3
        mooseImpactFeatureLitDict['care_gap_618'] = 0.3
        mooseImpactFeatureLitDict['care_gap_619'] = 0.3
        mooseImpactFeatureLitDict['care_gap_620'] = 0.3
        mooseImpactFeatureLitDict['care_gap_621'] = 0.3
        mooseImpactFeatureLitDict['care_gap_622'] = 0.3
        mooseImpactFeatureLitDict['care_gap_623'] = 0.3
        mooseImpactFeatureLitDict['care_gap_624'] = 0.3
        mooseImpactFeatureLitDict['care_gap_625'] = 0.3
        mooseImpactFeatureLitDict['care_gap_626'] = 0.3
        mooseImpactFeatureLitDict['care_gap_627'] = 0.3
        mooseImpactFeatureLitDict['care_gap_628'] = 0.3
        mooseImpactFeatureLitDict['care_gap_629'] = 0.3
        mooseImpactFeatureLitDict['care_gap_630'] = 0.3
        mooseImpactFeatureLitDict['care_gap_631'] = 0.3
        mooseImpactFeatureLitDict['care_gap_632'] = 0.3
        mooseImpactFeatureLitDict['care_gap_633'] = 0.3
        mooseImpactFeatureLitDict['care_gap_634'] = 0.3
        mooseImpactFeatureLitDict['care_gap_635'] = 0.3
        mooseImpactFeatureLitDict['care_gap_636'] = 0.3
        mooseImpactFeatureLitDict['care_gap_637'] = 0.3
        mooseImpactFeatureLitDict['care_gap_638'] = 0.3
        mooseImpactFeatureLitDict['care_gap_639'] = 0.3
        mooseImpactFeatureLitDict['care_gap_640'] = 0.3
        mooseImpactFeatureLitDict['care_gap_641'] = 0.3
        mooseImpactFeatureLitDict['care_gap_642'] = 0.3
        mooseImpactFeatureLitDict['care_gap_643'] = 0.3
        mooseImpactFeatureLitDict['care_gap_644'] = 0.3
        mooseImpactFeatureLitDict['care_gap_645'] = 0.3
        mooseImpactFeatureLitDict['care_gap_646'] = 0.3
        mooseImpactFeatureLitDict['care_gap_647'] = 0.3
        mooseImpactFeatureLitDict['care_gap_648'] = 0.3
        mooseImpactFeatureLitDict['care_gap_649'] = 0.3
        mooseImpactFeatureLitDict['care_gap_650'] = 0.3
        mooseImpactFeatureLitDict['care_gap_651'] = 0.3
        mooseImpactFeatureLitDict['care_gap_652'] = 0.3
        mooseImpactFeatureLitDict['care_gap_653'] = 0.3
        mooseImpactFeatureLitDict['care_gap_654'] = 0.3
        
        
        modelParam['moose_impact_feature_lit_value'] = mooseImpactFeatureLitDict

        # how to rank outputs in care_gap_compact in MooseOpenCareGapImpactListTransformer.py
        # 0=reverse alphabetical of care gap number
        # 1=reverse alphabetical of care gap short name
        # 2=largest to smallest impact by shap
        # 3=largest to smallest impact by literature

        modelParam['moose_impact_feature_rank_choice'] = 3

        # list of possible care gap columns
        colList = []
        for x in range(0, 20):
            colList.append('care_gap_{0}'.format(str(x + 1)))
            colList.append('care_gap_name_{0}'.format(str(x + 1)))
            colList.append('care_gap_member_shap_delta_{0}'.format(str(x + 1)))
            colList.append('care_gap_average_shap_delta_{0}'.format(str(x + 1)))
            colList.append('care_gap_lit_delta_{0}'.format(str(x + 1)))

        modelParam['moose_output_included_care_gap_name'] = colList

        # value of one point a1c drop in the commerical population, from fitch scenario 1
        modelParam['moose_a1c_one_point_drop_usd_pppm_commerical'] = 1400.0 / 12.0

        # value of one point a1c drop in the medicare population, from fitch scenario 1
        modelParam['moose_a1c_one_point_drop_usd_pppm_medicare'] = 1400.0 / 12.0 * 74.55 / 99.44

        # care gap categories
        catDict = {'care_gap_001xx': 'med_opt',
         'care_gap_200xx': 'med_opt',
         'care_gap_002': 'med_opt',
         'care_gap_201': 'med_opt',
         'care_gap_002xx': 'med_opt',
         'care_gap_202': 'med_opt',
         'care_gap_003': 'med_opt',
         'care_gap_549': 'med_opt',
         'care_gap_004': 'med_opt',
         'care_gap_550': 'med_opt',
         'care_gap_005': 'med_opt',
         'care_gap_006': 'med_opt',
         'care_gap_552': 'med_opt',
         'care_gap_007': 'med_opt',
         'care_gap_556': 'med_opt',
         'care_gap_010': 'med_opt',
         'care_gap_553': 'med_opt',
         'care_gap_011': 'med_opt',
         'care_gap_557': 'med_opt',
         'care_gap_013': 'med_opt',
         'care_gap_565': 'med_opt',
         'care_gap_014': 'med_opt',
         'care_gap_554': 'med_opt',
         'care_gap_015xx': 'med_opt',
         'care_gap_560': 'med_opt',
         'care_gap_018': 'med_opt',
         'care_gap_555': 'med_opt',
         'care_gap_019': 'med_opt',
         'care_gap_562': 'med_opt',
         'care_gap_038': 'med_adh',
         'care_gap_039': 'med_adh',
         'care_gap_040': 'med_adh',
         'care_gap_041': 'med_adh',
         'care_gap_043': 'med_adh',
         'care_gap_044': 'med_adh',
         'care_gap_045': 'med_adh',
         'care_gap_046': 'med_adh',
         'care_gap_047': 'med_adh',
         'care_gap_053': 'screen',
         'care_gap_247': 'screen',
         'care_gap_072': 'screen',
         'care_gap_260': 'screen',
         'care_gap_121': 'smbg',
         'care_gap_122': 'smbg',
         'care_gap_124': 'smbg',
         'care_gap_125': 'smbg',
         'care_gap_400': 'como',
         'care_gap_402': 'como',
         'care_gap_407': 'como',
         'care_gap_408': 'como',
         'care_gap_410': 'como',
         'care_gap_412': 'como',
         'care_gap_413': 'como',
         'care_gap_414': 'como',
         'care_gap_416': 'como',
         'care_gap_417': 'como',
         'care_gap_418': 'como',
         'care_gap_600': 'screen',
         'care_gap_601': 'screen',
         'care_gap_602': 'screen',
         'care_gap_603': 'screen',
         'care_gap_604': 'med_opt',
         'care_gap_605': 'med_opt',
         'care_gap_606': 'med_opt',
         'care_gap_607': 'med_opt',
         'care_gap_608': 'med_opt',
         'care_gap_609': 'med_opt',
         'care_gap_610': 'med_opt',
         'care_gap_611': 'med_opt',
         'care_gap_612': 'med_opt',
         'care_gap_613': 'med_opt',
         'care_gap_614': 'como',
         'care_gap_615': 'med_opt',
         'care_gap_616': 'med_opt',
         'care_gap_617': 'med_opt',
         'care_gap_618': 'med_opt',
         'care_gap_619': 'med_opt',
         'care_gap_620': 'med_opt',
         'care_gap_621': 'med_opt',
         'care_gap_622': 'med_opt',
         'care_gap_623': 'screen',
         'care_gap_624': 'med_opt',
         'care_gap_625': 'screen',
         'care_gap_626': 'med_opt',
         'care_gap_627': 'screen',
         'care_gap_628': 'screen',
         'care_gap_629': 'screen',
         'care_gap_630': 'screen',
         'care_gap_631': 'screen',
         'care_gap_632': 'med_opt',
         'care_gap_633': 'med_opt',
         'care_gap_634': 'med_opt',
         'care_gap_635': 'med_opt',
         'care_gap_636': 'med_opt',
         'care_gap_637': 'med_opt',
         'care_gap_638': 'med_opt',
         'care_gap_639': 'med_opt',
         'care_gap_640': 'med_opt',
         'care_gap_641': 'med_opt',
         'care_gap_642': 'como',
         'care_gap_643': 'med_opt',
         'care_gap_644': 'med_opt',
         'care_gap_645': 'med_opt',
         'care_gap_646': 'med_opt',
         'care_gap_647': 'med_opt',
         'care_gap_648': 'med_opt',
         'care_gap_649': 'med_opt',
         'care_gap_650': 'screen',
         'care_gap_651': 'med_opt',
         'care_gap_652': 'screen',
         'care_gap_653': 'med_opt',
         'care_gap_654': 'screen'}

        modelParam['moose_impact_feature_category'] = catDict

        # care gap med opt general, med opt specific, med opt other
        medOptCatDict = {}
        medOptCatDict['care_gap_001xx'] = 'med_opt_specific'
        medOptCatDict['care_gap_200xx'] = 'med_opt_specific'
        medOptCatDict['care_gap_002'] = 'med_opt_specific'
        medOptCatDict['care_gap_201'] = 'med_opt_specific'
        medOptCatDict['care_gap_002xx'] = 'med_opt_specific'
        medOptCatDict['care_gap_202'] = 'med_opt_specific'
        medOptCatDict['care_gap_003'] = 'med_opt_general'
        medOptCatDict['care_gap_549'] = 'med_opt_general'
        medOptCatDict['care_gap_004'] = 'med_opt_general'
        medOptCatDict['care_gap_550'] = 'med_opt_general'
        medOptCatDict['care_gap_005'] = 'med_opt_general'
        medOptCatDict['care_gap_006'] = 'med_opt_specific'
        medOptCatDict['care_gap_552'] = 'med_opt_specific'
        medOptCatDict['care_gap_007'] = 'med_opt_specific'
        medOptCatDict['care_gap_556'] = 'med_opt_specific'
        medOptCatDict['care_gap_010'] = 'med_opt_specific'
        medOptCatDict['care_gap_553'] = 'med_opt_specific'
        medOptCatDict['care_gap_011'] = 'med_opt_specific'
        medOptCatDict['care_gap_557'] = 'med_opt_specific'
        medOptCatDict['care_gap_013'] = 'med_opt_specific'
        medOptCatDict['care_gap_565'] = 'med_opt_specific'
        medOptCatDict['care_gap_014'] = 'med_opt_specific'
        medOptCatDict['care_gap_554'] = 'med_opt_specific'
        medOptCatDict['care_gap_015xx'] = 'med_opt_specific'
        medOptCatDict['care_gap_560'] = 'med_opt_specific'
        medOptCatDict['care_gap_018'] = 'med_opt_specific'
        medOptCatDict['care_gap_555'] = 'med_opt_specific'
        medOptCatDict['care_gap_019'] = 'med_opt_specific'
        medOptCatDict['care_gap_562'] = 'med_opt_specific'
        medOptCatDict['care_gap_038'] = 'non_med_opt'
        medOptCatDict['care_gap_039'] = 'non_med_opt'
        medOptCatDict['care_gap_040'] = 'non_med_opt'
        medOptCatDict['care_gap_041'] = 'non_med_opt'
        medOptCatDict['care_gap_043'] = 'non_med_opt'
        medOptCatDict['care_gap_044'] = 'non_med_opt'
        medOptCatDict['care_gap_045'] = 'non_med_opt'
        medOptCatDict['care_gap_046'] = 'non_med_opt'
        medOptCatDict['care_gap_047'] = 'non_med_opt'
        medOptCatDict['care_gap_053'] = 'non_med_opt'
        medOptCatDict['care_gap_247'] = 'non_med_opt'
        medOptCatDict['care_gap_072'] = 'non_med_opt'
        medOptCatDict['care_gap_260'] = 'non_med_opt'
        medOptCatDict['care_gap_121'] = 'non_med_opt'
        medOptCatDict['care_gap_122'] = 'non_med_opt'
        medOptCatDict['care_gap_124'] = 'non_med_opt'
        medOptCatDict['care_gap_125'] = 'non_med_opt'
        medOptCatDict['care_gap_400'] = 'non_med_opt'
        medOptCatDict['care_gap_402'] = 'non_med_opt'
        medOptCatDict['care_gap_407'] = 'non_med_opt'
        medOptCatDict['care_gap_408'] = 'non_med_opt'
        medOptCatDict['care_gap_410'] = 'non_med_opt'
        medOptCatDict['care_gap_412'] = 'non_med_opt'
        medOptCatDict['care_gap_413'] = 'non_med_opt'
        medOptCatDict['care_gap_414'] = 'non_med_opt'
        medOptCatDict['care_gap_416'] = 'non_med_opt'
        medOptCatDict['care_gap_417'] = 'non_med_opt'
        medOptCatDict['care_gap_418'] = 'non_med_opt'
        
        medOptCatDict['care_gap_600'] = 'non_medopt'
        medOptCatDict['care_gap_601'] = 'non_medopt'
        medOptCatDict['care_gap_602'] = 'non_medopt'
        medOptCatDict['care_gap_603'] = 'non_medopt'
        medOptCatDict['care_gap_604'] = 'non_medopt'
        medOptCatDict['care_gap_605'] = 'non_medopt'
        medOptCatDict['care_gap_606'] = 'non_medopt'
        medOptCatDict['care_gap_607'] = 'non_medopt'
        medOptCatDict['care_gap_608'] = 'non_medopt'
        medOptCatDict['care_gap_609'] = 'non_medopt'
        medOptCatDict['care_gap_610'] = 'non_medopt'
        medOptCatDict['care_gap_611'] = 'non_medopt'
        medOptCatDict['care_gap_612'] = 'non_medopt'
        medOptCatDict['care_gap_613'] = 'non_medopt'
        medOptCatDict['care_gap_614'] = 'non_medopt'
        medOptCatDict['care_gap_615'] = 'non_medopt'
        medOptCatDict['care_gap_616'] = 'non_medopt'
        medOptCatDict['care_gap_617'] = 'non_medopt'
        medOptCatDict['care_gap_618'] = 'non_medopt'
        medOptCatDict['care_gap_619'] = 'non_medopt'
        medOptCatDict['care_gap_620'] = 'non_medopt'
        medOptCatDict['care_gap_621'] = 'non_medopt'
        medOptCatDict['care_gap_622'] = 'non_medopt'
        medOptCatDict['care_gap_623'] = 'non_medopt'
        medOptCatDict['care_gap_624'] = 'non_medopt'
        medOptCatDict['care_gap_625'] = 'non_medopt'
        medOptCatDict['care_gap_626'] = 'non_medopt'
        medOptCatDict['care_gap_627'] = 'non_medopt'
        medOptCatDict['care_gap_628'] = 'non_medopt'
        medOptCatDict['care_gap_629'] = 'non_medopt'
        medOptCatDict['care_gap_630'] = 'non_medopt'
        medOptCatDict['care_gap_631'] = 'non_medopt'
        medOptCatDict['care_gap_632'] = 'non_medopt'
        medOptCatDict['care_gap_633'] = 'non_medopt'
        medOptCatDict['care_gap_634'] = 'non_medopt'
        medOptCatDict['care_gap_635'] = 'non_medopt'
        medOptCatDict['care_gap_636'] = 'non_medopt'
        medOptCatDict['care_gap_637'] = 'non_medopt'
        medOptCatDict['care_gap_638'] = 'non_medopt'
        medOptCatDict['care_gap_639'] = 'non_medopt'
        medOptCatDict['care_gap_640'] = 'non_medopt'
        medOptCatDict['care_gap_641'] = 'non_medopt'
        medOptCatDict['care_gap_642'] = 'non_medopt'
        medOptCatDict['care_gap_643'] = 'non_medopt'
        medOptCatDict['care_gap_644'] = 'non_medopt'
        medOptCatDict['care_gap_645'] = 'non_medopt'
        medOptCatDict['care_gap_646'] = 'non_medopt'
        medOptCatDict['care_gap_647'] = 'non_medopt'
        medOptCatDict['care_gap_648'] = 'non_medopt'
        medOptCatDict['care_gap_649'] = 'non_medopt'
        medOptCatDict['care_gap_650'] = 'non_medopt'
        medOptCatDict['care_gap_651'] = 'non_medopt'
        medOptCatDict['care_gap_652'] = 'non_medopt'
        medOptCatDict['care_gap_653'] = 'non_medopt'
        medOptCatDict['care_gap_654'] = 'non_medopt'

        modelParam['moose_impact_feature_category_med_opt'] = medOptCatDict

        ####
        #### heterogeneity
        ####

        # heterogenity parameters

        # number of gaps to consider in the analysis
        modelParam['moose_heterogeneity_top_gap_consider'] = 20

        # go nno go threshold for firing off a channel
        modelParam['moose_heterogeneity_channel_go_roi_threshold'] = 1.0

        # per member (not just those in the cohort) that we charge the end consuming plan sponsor, commerical
        modelParam['moose_heterogeneity_commerical_cost_pmpm'] = 0.63

        # per member (not just those in the cohort) that we charge the end consuming plan sponsor, medicare
        modelParam['moose_heterogeneity_medicare_cost_pmpm'] = 0.58

        # share of members with diabetes, commerical
        modelParam['moose_heterogeneity_commerical_rate_of_diabetes'] = 0.07

        # share of members with diabetes, medicare
        modelParam['moose_heterogeneity_medicare_rate_of_diabetes'] = 0.288

        # care gap value scaling (typically up to three, in the future this can be replaced by either Mold percentage scaling or refined numbers
        # hard coded to 1.0 for now as we implement Mold to convert changes to % changes rather than absolute changes
        rankValueDict = {'care_gap_1': 1.0,
                         'care_gap_2': 0.8,
                         'care_gap_3': 0.6,
                         'care_gap_4': 0.6,
                         'care_gap_5': 0.6,
                         'care_gap_6': 0.6,
                         'care_gap_7': 0.6,
                         'care_gap_8': 0.6,
                         'care_gap_9': 0.6,
                         'care_gap_10': 0.6,
                         'care_gap_11': 0.6,
                         'care_gap_12': 0.6,
                         'care_gap_13': 0.6,
                         'care_gap_14': 0.6,
                         'care_gap_15': 0.6,
                         'care_gap_16': 0.6,
                         'care_gap_17': 0.6,
                         'care_gap_18': 0.6,
                         'care_gap_19': 0.6,
                         'care_gap_20': 0.6}

        modelParam['moose_heterogeneity_gap_rank_proportional_value'] = rankValueDict

        # channels that people can use in heterogenity analysis
        # value 1 = cost, value 2 = probability of closuse, value 3= value for it to make sense to activate for given the ROI
        # original
        channel_dict = {'digital':          [0.01, 0.0032],
                        'sms':              [0.01, 0.0032],
                        'email':            [0.01, 0.0035],
                        'letter':           [1.00, 0.0158],
                        'dm':               [1.00, 0.0158],
                        'ivr':              [0.34, 0.0045],
                        'callpod':          [8.00, 0.0945],
                        'pharmacist':       [4.35, 0.0211],
                        'pharmacist_cpco':  [4.35, 0.0211],
                        'health_hub':       [4.30, 0.0445],
                        'care_coordinator': [8.00, 0.0930]}

        #channel cost & conversion rate
        modelParam['rhino_channel_dict'] = channel_dict

        # add on overall - go no go criteria threshold
        channel_dict = {
            k: [v[0], v[1], round(modelParam['moose_heterogeneity_channel_go_roi_threshold'] * (v[0] / v[1]), 2)] for
            k, v in channel_dict.items()}

        # assing
        modelParam['moose_heterogeneity_channel_dict'] = channel_dict

        # actions assoicated with channels
        # link between call to action and outreach method
        # action is short for call to action
        action_to_chanel_dict = {'pcp/specialist': ['digital', 'email', 'letter', 'callpod','health_hub'],
                                 'cvs_rx': ['digital', 'email', 'letter', 'callpod', 'pharmacist','health_hub'],
                                 'cvs_mc': ['digital', 'email', 'letter', 'callpod', 'health_hub'],
                                 'cvs_hh': ['digital', 'email', 'letter', 'callpod', 'pharmacist', 'health_hub'],
                                 'device': ['digital','email',  'letter', 'callpod', 'health_hub']}

        modelParam['moose_heterogeneity_action_to_channel_dict'] = action_to_chanel_dict

        # care gaps associated with actions
        # link between gap and call to action
        medOptList = ['pcp/specialist', 'cvs_hh', 'cvs_mc']
        medAdhList = ['cvs_rx']
        comoList = ['pcp/specialist', 'cvs_hh', 'cvs_mc']
        deviceList = ['pcp/specialist', 'cvs_hh', 'cvs_mc', 'device']
        screenList = ['pcp/specialist', 'cvs_hh', 'cvs_mc']
        ccList = ['pcp/specialist', 'cvs_hh', 'cvs_mc']
        # build dict
        gap_to_action_dict = {
            'como_alcoholism': comoList,
            'como_asthma': comoList,
            'como_chronic_renal_failure': comoList,
            'como_depression': comoList,
            'como_heart_failure': comoList,
            'como_hyperlipidemia': comoList,
            'como_hypertension': comoList,
            'como_iron_deficiency_anemia': comoList,
            'como_low_vision_and_blindness': comoList,
            'como_metabolic_syndrome': comoList,
            'como_obesity': comoList,
            'med_adh_alpha_glucose': medAdhList,
            'med_adh_metformin': medAdhList,
            'med_adh_dpp4': medAdhList,
            'med_adh_glp1': medAdhList,
            'med_adh_insulin': medAdhList,
            'med_adh_meglitinide': medAdhList,
            'med_adh_sglt2': medAdhList,
            'med_adh_sulfonylureas': medAdhList,
            'med_adh_tdz': medAdhList,
            'med_adh_statins': medAdhList,
            'med_opt_one_metformin_comm': medOptList,
            'med_opt_four_general_comm': medOptList,
            'med_opt_four_insulin_comm': medOptList,
            'med_opt_one_glp1_dpp4_comm': medOptList,
            'med_opt_one_insulin_comm': medOptList,
            'med_opt_two_general_comm': medOptList,
            'med_opt_three_chf_ckd123_glp1_comm': medOptList,
            'med_opt_three_cvd_sglt2_glp1_comm': medOptList,
            'med_opt_three_ex_all_como_comm': medOptList,
            'med_opt_three_general_comm': medOptList,
            'med_opt_three_obese_sglt2_comm': medOptList,
            'med_opt_two_chf_ckd123_sglt2_comm': medOptList,
            'med_opt_two_cvd_glp1_sglt2_comm': medOptList,
            'med_opt_two_ex_all_como_comm': medOptList,
            'med_opt_two_obese_glp1_comm': medOptList,
            'med_opt_one_metformin_medi': medOptList,
            'med_opt_one_insulin_medi': medOptList,
            'med_opt_one_glp1_dpp4_medi': medOptList,
            'med_opt_two_general_medi': medOptList,
            'med_opt_three_general_medi': medOptList,
            'med_opt_two_ex_all_como_medi': medOptList,
            'med_opt_three_ex_all_como_medi': medOptList,
            'med_opt_two_obese_glp1_medi': medOptList,
            'med_opt_three_obese_sglt2_medi': medOptList,
            'med_opt_four_insulin_medi': medOptList,
            'med_opt_two_cvd_glp1_sglt2_medi': medOptList,
            'med_opt_three_cvd_sglt2_glp1_medi': medOptList,
            'med_opt_two_chf_ckd123_sglt2_medi': medOptList,
            'med_opt_three_chf_ckd123_glp1_medi': medOptList,
            'screen_pcp_comm': screenList,
            'screen_pcp_medi': screenList,
            'screen_lipid_comm': screenList,
            'screen_lipid_medi': screenList,
            'smbg5_comm': deviceList,
            'smbg7_comm': deviceList,
            'smbg14_medi': deviceList,
            'smbg16_medi': deviceList,
            'cc_screen_eye_exam_comm':ccList,
            'cc_screen_a1c_comm':ccList,
            'cc_screen_liver_comm':ccList,
            'cc_screen_albuminuria_comm':ccList,
            'cc_med_opt_flu_vacc_comm':ccList,
            'cc_med_opt_pneumoco23_vacc_comm':ccList,
            'cc_med_opt_add_ace_or_arb_comm':ccList,
            'cc_med_opt_metformin_contra_ckd_comm':ccList,
            'cc_med_opt_glitazones_transaminases_elevation_comm':ccList,
            'cc_med_opt_repaglinide_contra_gemfibrozil_comm':ccList,
            'cc_med_opt_pramlintide_contra_gastroparesis_comm':ccList,
            'cc_med_opt_pramlintide_avoid_anticholinergic_comm':ccList,
            'cc_med_opt_estrogen_contain_contraceptives_comm':ccList,
            'cc_med_opt_thiazolidinediones_comm':ccList,
            'cc_como_pancreatitis_comm':ccList,
            'cc_med_opt_hepatitis_b_vacc_comm':ccList,
            'cc_med_opt_ckd_avoid_dm_drug_comm':ccList,
            'cc_med_opt_sglt2_contra_renal_impair_comm':ccList,
            'cc_med_opt_statin_comm':ccList,
            'cc_med_opt_glp1_contra_MTC_comm':ccList,
            'cc_med_opt_alphaglucose_avoid_renal_impair_comm':ccList,
            'cc_med_opt_exenatide_avoid_renal_impair_comm':ccList,
            'cc_med_opt_inhaled_insulin_contra_cld_comm':ccList,
            'cc_screen_inhaled_insulin_spirometry_comm':ccList,
            'cc_med_opt_DM_drug_acute_kidney_injury_comm':ccList,
            'cc_screen_metformin_vb12_comm':ccList,
            'cc_med_opt_canaliflozin_leg_foot_amputation_comm':ccList,
            'cc_lifestyle_smoke_cessation_comm':ccList,
            'cc_screen_eye_exam_medi':ccList,
            'cc_screen_a1c_medi':ccList,
            'cc_screen_liver_medi':ccList,
            'cc_screen_albuminuria_medi':ccList,
            'cc_med_opt_avoid_su_in_old_medi':ccList,
            'cc_med_opt_flu_vacc_medi':ccList,
            'cc_med_opt_pneumoco23_vacc_medi':ccList,
            'cc_med_opt_add_ace_or_arb_medi':ccList,
            'cc_med_opt_metformin_contra_ckd_medi':ccList,
            'cc_med_opt_glitazones_transaminases_elevation_medi':ccList,
            'cc_med_opt_repaglinide_contra_gemfibrozil_medi':ccList,
            'cc_med_opt_pramlintide_contra_gastroparesis_medi':ccList,
            'cc_med_opt_pramlintide_avoid_anticholinergic_medi':ccList,
            'cc_med_opt_thiazolidinediones_medi':ccList,
            'cc_como_pancreatitis_medi':ccList,
            'cc_med_opt_ckd_avoid_dm_drug_medi':ccList,
            'cc_med_opt_sglt2_contra_renal_impair_medi':ccList,
            'cc_med_opt_statin_medi':ccList,
            'cc_med_opt_glp1_contra_MTC_medi':ccList,
            'cc_med_opt_alphaglucose_avoid_renal_impair_medi':ccList,
            'cc_med_opt_exenatide_avoid_renal_impair_medi':ccList,
            'cc_med_opt_inhaled_insulin_contra_cld_medi':ccList,
            'cc_screen_inhaled_insulin_spirometry_medi':ccList,
            'cc_med_opt_DM_drug_acute_kidney_injury_medi':ccList,
            'cc_screen_metformin_vb12_medi':ccList,
            'cc_med_opt_canaliflozin_leg_foot_amputation_medi':ccList,
            'cc_lifestyle_smoke_cessation_medi':ccList
            }

        modelParam['moose_heterogeneity_gap_to_action_dict'] = gap_to_action_dict

        #### RHINO Params
        modelParam['rhino_direct_comms'] = ['email', 'sms','dm','ivr']
        modelParam['rhino_proactive_channels'] = ['pharmacist_cpco', 'health_hub','care_coordinator']
        
        # overlapped programs that used ivr and care coordinators
        modelParam['rhino_no_IVR_CC_prgms'] = ['ccc_engaged', 'ccc_targeted', 
                                                 'rap_engaged','rap_targeted',
                                                 'in_bh',
                                                 'in_chf', 
                                                 'in_oncology', 
                                                 'in_disease_management', 
                                                 'in_manual_cm',
                                                 'in_nme']
        
        # overlapped programs that used care coordinators
        modelParam['rhino_no_CC_prgms'] = ['in_hot_hedis']
        
        
        #####
        ##### return
        #####
        self.modelParam = modelParam

    # helper function(replace null values with another value)
    def NVL(self, Value, newValue):
        """replace null values with new value when the value is null
        Parameters
        :param Value: a scalar indicates whether value is missing
        :type Value: a scalar (for missing value: NaN in numeric arrays, None or NaN in object arrays, NaT in datetimelike)
        :param newValue: a scalar of the new value
        :type newValue: a scalar
        Returns
        :returns: a scalar with missing value replaced
        :rtype: a scalar
        """
        # replace missing value with newValue
        if pd.isnull(Value):
            return newValue

        # otherwise returns value
        return Value

    """ Determines what the cost is of a particular journey, given input from Finance
        Parameters
        :param journey_type:     The type of the journey
        :type  journey_type:     string
        :param journey_strength: The strength, either "High", "Medium", or "Low"
        :type  journey_strength: string
        :param proactive_call: identifier of which call is being used
        :type  proactive_call: string
        :param procall_open: 0/1 indicator as to whether or not the campaign is open to a proactive call
        :type  procall_open: int
        Returns
        :returns: The cost of the journey
        :rtype:   float
        """
    def GetJourneyCosts(journey_type, journey_strength, proactive_call, procall_open):
        journey_strength_costs = {"Low": 0, "Medium": 2, "High": 5}
        cost = journey_strength_costs[journey_strength]
        if (procall_open == 1 and proactive_call == "care_coordinator"):
            cost = cost + 11
        return(cost)

    # end
