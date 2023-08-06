from RavenTableCheckOutput import *


# ingestion and organization of raw data from database
class RavenAPI:

    # init
    def __init__(self):
        pass

    # main
    def raven(self, df):
        # def table check
        self.ravenTableCheck = RavenTableCheckOutput()

        # develope output
        self.X = df

        # get list of tables of interest

        tableList = {'hippo_cohort': 'cohort',
                     'hippo_demographics': 'demo',
                     'hippo_insurance': 'insure',
                     'hippo_plan_sponsor': 'ps',
                     'hippo_comorbidities': 'como',
                     'hippo_ckd_tier': 'ckdtr',
                     'hippo_feature_ascvd': 'cvd',
                     'hippo_feature_procedure_codes': 'prcdr',
                     'hippo_specialty_all': 'specialty',
                     'hippo_feature_lab_a1c_all': 'lab_a1c',
                     'hippo_feature_lab_a1c_12mo': 'lab_a1c_12mo',
                     'hippo_feature_lab_cholesterol': 'lab_cholesterol',
                     'hippo_feature_lab_creatinine': 'lab_creatinine',
                     'hippo_feature_lab_cholesterol_hdl': 'lab_cholesterol_hdl',
                     'hippo_feature_lab_bilirubin': 'lab_bilirubin',
                     'hippo_feature_lab_cholesterol_ldl': 'lab_cholesterol_ldl',
                     'hippo_feature_lab_cholesterol_12mo': 'lab_cholesterol_12mo',
                     'hippo_feature_lab_cholesterol_hdl_12mo': 'lab_cholesterol_hdl_12mo',
                     'hippo_feature_lab_cholesterol_ldl_12mo': 'lab_cholesterol_ldl_12mo',
                     'hippo_feature_total_cholesterol_cpt': 'total_cholesterol_cpt',
                     'hippo_feature_cholesterol_hdl_cpt': 'cholesterol_hdl_cpt',
                     'hippo_feature_cholesterol_ldl_cpt': 'cholesterol_ldl_cpt',
                     'hippo_feature_lab_triglyceride_12mo': 'lab_triglyceride_12mo',
                     'hippo_feature_lab_glucose': 'lab_glucose',
                     'hippo_feature_lab_gfr_non_black': 'lab_gfr_non_black',
                     'hippo_feature_lab_gfr': 'lab_gfr',
                     'hippo_feature_lab_creatinine_oth': 'lab_creatinine_oth',
                     'hippo_feature_lab_albumin': 'lab_albumin',
                     'hippo_feature_lab_systolic_blood_pressure': 'lab_systolic_blood_pressure',
                     'hippo_feature_lab_diastolic_blood_pressure': 'lab_diastolic_blood_pressure',
                     'hippo_feature_lab_height': 'lab_height',
                     'hippo_feature_lab_cholesterol_hdl_total': 'lab_cholesterol_hdl_total',
                     'hippo_feature_lab_weight': 'lab_weight',
                     'hippo_feature_lab_waist': 'lab_waist',
                     'hippo_feature_lab_triglyceride': 'lab_triglyceride',
                     'hippo_feature_triglyceride_cpt': 'triglyceride_cpt',
                     'hippo_feature_lab_magnesium': 'lab_magnesium',
                     'hippo_feature_lab_lipoprotein': 'lab_lipoprotein',
                     'hippo_feature_lab_bmi': 'lab_bmi',
                     'hippo_feature_lab_urea_nitro': 'lab_urea_nitro',
                     'hippo_feature_lab_mean_arterial_pressure': 'lab_mean_arterial_pressure',
                     'hippo_feature_lab_a1c_count': 'lab_a1c_count',
                     'hippo_feature_visit_medical_practitioner': 'visit_medical_practitioner',
                     'hippo_feature_visit_endocrinologist': 'visit_endocrinologist',
                     'hippo_feature_visit_ophthalmologist': 'visit_ophthalmologist',
                     'hippo_feature_visit_cardiologist': 'visit_cardiologist',
                     'hippo_feature_visit_registered_dietician': 'visit_registered_dietician',
                     'hippo_feature_visit_physical_therapist': 'visit_physical_therapist',
                     'hippo_feature_visit_nephrologist': 'visit_nephrologist',
                     'hippo_feature_office_visit_cpt': 'office_visit_cpt',
                     'hippo_feature_drug_diabetes': 'drug_diabetes',
                     'hippo_feature_drug_diabetes_pdc': 'drug_diabetes_pdc',
                     'hippo_feature_diagnosis': 'diagnosis',
                     'hippo_hypoglycemia_diagnosis': 'hypoglycemia_dx',
                     'hippo_feature_survey_response': 'survey_response',
                     'hippo_feature_cost_past': 'cost_past',
                     'hippo_feature_final_race': 'race',
                     'hippo_feature_drug_diabetes_device': 'ddd',
                     'hippo_geographic_region': 'geo',
                     'hippo_feature_anti_diabetic_drug': 'anti_diabetic_drug',
                     'hippo_feature_member_permissions_small': 'permission',
                     'hippo_big_wide': 'bw',
                     'hippo_feature_care_considerations_final': 'engine',
                     'hippo_feature_care_gap_088': 'care_gap_088',
                     'hippo_feature_episode_grouper_diab': 'epi_group_diab',
                     'hippo_feature_episode_grouper_chf': 'epi_group_chf',
                     'member_hh_dist': 'hh_geo_small',
                     'member_hh_dist_eoy2020': 'hh_geo_eoy2020',
                     'hippo_fills_at_cvs_pharmacy_aetna_only': 'rx_aetna'}
