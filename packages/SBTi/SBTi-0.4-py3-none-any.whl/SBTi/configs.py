"""
This file defines the constants used throughout the different classes. In order to redefine these settings whilst using
the module, extend the respective config class and pass it to the class as the "constants" parameter.
"""
import os


class ColumnsConfig:
    # Define a constant for each column used in the
    COMPANY_ID = "company_id"
    COMPANY_ISIC = "ISIC"
    REGRESSION_PARAM = "param"
    REGRESSION_INTERCEPT = "intercept"
    MARKET_CAP = "market_cap"
    INVESTMENT_VALUE = "investment_value"
    COMPANY_ENTERPRISE_VALUE = "company_enterprise_value"
    COMPANY_EV_PLUS_CASH = "company_ev_plus_cash"
    COMPANY_TOTAL_ASSETS = "company_total_assets"
    TARGET_REFERENCE_NUMBER = "Target type"
    SCOPE = "Scope"
    SCOPE_CATEGORY = "scope_category"
    SR15 = "SR15"
    REDUCTION_FROM_BASE_YEAR = "reduction_from_base_year"
    START_YEAR = "start_year"
    VARIABLE = "variable"
    SLOPE = "slope"
    TIME_FRAME = "time_frame"
    MODEL = "model"
    ANNUAL_REDUCTION_RATE = "annual_reduction_rate"
    EMISSIONS_IN_SCOPE = "emissions_in_scope"
    TEMPERATURE_SCORE = "temperature_score"
    COMPANY_NAME = "company_name"
    OWNED_EMISSIONS = "owned_emissions"
    COUNTRY = 'Country'
    SECTOR = 'sector'
    GHG_SCOPE12 = 'GHG_scope1+2'
    GHG_SCOPE3 = 'GHG_scope3'
    COMPANY_REVENUE = 'Revenue'
    CASH_EQUIVALENTS = 'cash_equivalents'
    TARGET_CLASSIFICATION = 'Target_classification'
    REDUCTION_AMBITION = 'reduction_ambition'
    BASE_YEAR = 'base_year'
    END_YEAR = 'end_year'
    SBTI_STATUS = 'SBTi_status'
    ACHIEVED_EMISSIONS = "achieved_reduction"
    ISIC = 'ISIC'
    INDUSTRY_LVL1 = "Industry_lvl1"
    INDUSTRY_LVL2 = "Industry_lvl2"
    INDUSTRY_LVL3 = "Industry_lvl3"
    INDUSTRY_LVL4 = "Industry_lvl4"
    COVERAGE_S1 = 'Coverage_S1'
    COVERAGE_S2 = 'Coverage_S2'
    COVERAGE_S3 = 'Coverage_S3'
    INTENSITY_METRIC = 'Intensity_metric'
    INTENSITY_METRIC_SR15 = 'Intensity_metric'
    TARGET_TYPE_SR15 = "Target_type"
    SR15_VARIABLE = "SR15_variable"
    REGRESSION_MODEL = 'Regression_model'
    BASEYEAR_GHG_S1 = 'BaseYear_GHG_S1'
    BASEYEAR_GHG_S2 = 'BaseYear_GHG_S2'
    BASEYEAR_GHG_S3 = 'BaseYear_GHG_S3'
    REGION = 'Region'
    ENGAGEMENT_TARGET = 'engagement_target'

    # SR15 mapping columns
    PARAM = "param"
    INTERCEPT = "intercept"

    # Output columns
    WEIGHTED_TEMPERATURE_SCORE = "weighted_temperature_score"
    CONTRIBUTION_RELATIVE = "contribution_relative"
    CONTRIBUTION = "contribution"

    # This defines which columns contain company specific, instead of target specific data
    COMPANY_COLUMNS = [COMPANY_NAME, INDUSTRY_LVL1, INDUSTRY_LVL2, INDUSTRY_LVL3, INDUSTRY_LVL4, INTENSITY_METRIC,
                       REGRESSION_PARAM,
                       REGRESSION_INTERCEPT, GHG_SCOPE12, GHG_SCOPE3, MARKET_CAP, INVESTMENT_VALUE,
                       COMPANY_ENTERPRISE_VALUE, CASH_EQUIVALENTS, COMPANY_TOTAL_ASSETS, REGION, COUNTRY,
                       COMPANY_REVENUE]

    # These columns are not allowed to have null values
    REQUIRED_FIELDS_TARGETS = [REDUCTION_AMBITION, SCOPE, TARGET_REFERENCE_NUMBER]
    REQUIRED_FIELDS_COMPANY = [GHG_SCOPE12, GHG_SCOPE3]

    # These column have to be available in the data set
    REQUIRED_COLUMNS_TARGETS = [COMPANY_ID, TARGET_REFERENCE_NUMBER, INTENSITY_METRIC, SCOPE, COVERAGE_S1, COVERAGE_S2,
                                COVERAGE_S3, REDUCTION_AMBITION, BASE_YEAR, END_YEAR, BASEYEAR_GHG_S1, BASEYEAR_GHG_S2,
                                BASEYEAR_GHG_S3, ACHIEVED_EMISSIONS]
    REQUIRED_COLUMNS_COMPANY = [COMPANY_NAME, COMPANY_ID, GHG_SCOPE12, GHG_SCOPE3]


class PortfolioAggregationConfig:
    COLS = ColumnsConfig
    VALUE_TIME_FRAMES = ["short", "mid", "long"]
    VALUE_SCOPE_S1S2 = "scope 1+2"
    VALUE_SCOPE_S3 = "scope 3"
    VALUE_SCOPE_S1S2S3 = "scope 1+2+3"
    VALUE_BASE_SCOPES = [VALUE_SCOPE_S1S2, VALUE_SCOPE_S3]

    VALUE_SCOPE_CATEGORY_S1S2 = "s1s2"
    VALUE_SCOPE_CATEGORY_S3 = "s3"
    VALUE_SCOPE_CATEGORY_S1S2S3 = "s1s2s3"
    VALUE_SCOPE_CATEGORIES = [VALUE_SCOPE_CATEGORY_S1S2, VALUE_SCOPE_CATEGORY_S3, VALUE_SCOPE_CATEGORY_S1S2S3]

    SCOPE_MAP = {"s1+s2": "s1s2", "s3": "s3", "s1+s2+s3": "s1s2s3", 's2': 's1s2', 's1': 's1s2', 's3_up': 's3',
                 's3_down': 's3',
                 's3_total': 's3'}


class TemperatureScoreConfig(PortfolioAggregationConfig):
    FILE_SR15_MAPPING = os.path.join(os.path.dirname(os.path.realpath(__file__)), "inputs",
                                     "sr15_mapping.xlsx")
    FILE_REGRESSION_MODEL_SUMMARY = os.path.join(os.path.dirname(os.path.realpath(__file__)), "inputs",
                                                 "regression_model_summary.xlsx")
    FILE_RAW_DATA_DUMP = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "app",
                                      "uploads", "test_output.csv")

    DEFAULT_INDUSTRY = "Others"

    VALUE_TARGET_REFERENCE_ABSOLUTE = "Absolute"
    VALUE_TARGET_REFERENCE_INTENSITY = "Intensity"
    VALUE_TARGET_REFERENCE_INTENSITY_BASE = "Int"
    CONTRIBUTION_COLUMNS = [ColumnsConfig.COMPANY_NAME, ColumnsConfig.TEMPERATURE_SCORE,
                            ColumnsConfig.CONTRIBUTION_RELATIVE, ColumnsConfig.CONTRIBUTION]

    SLOPE_MAP = {
        "short": "slope5",
        "mid": "slope15",
        "long": "slope30",
    }

    TEMPERATURE_RESULTS = 'temperature_results'
    INVESTMENT_VALUE = "investment_value"
    TIME_FRAME_SHORT = 'short'
    TIME_FRAME_MID = 'mid'
    TIME_FRAME_LONG = 'long'


class PortfolioCoverageTVPConfig(PortfolioAggregationConfig):
    FILE_TARGETS = os.path.join(os.path.dirname(os.path.realpath(__file__)), "inputs",
                                "current-Companies-Taking-Action-191.xlsx")

    OUTPUT_TARGET_STATUS = "sbti_target_status"
    OUTPUT_WEIGHTED_TARGET_STATUS = "weighted_sbti_target_status"
    VALUE_TARGET_NO = "No target"
    VALUE_TARGET_COMMITTED = "Committed"
    VALUE_TARGET_SET = "Targets Set"

    TARGET_SCORE_MAP = {
        VALUE_TARGET_NO: 0,
        VALUE_TARGET_COMMITTED: 0,
        VALUE_TARGET_SET: 100,
    }

    # SBTi targets overview (TVP coverage)
    COL_COMPANY_NAME = "Company Name"
    COL_COMPANY_ID = "ISIN"
    COL_TARGET_STATUS = "Status"
