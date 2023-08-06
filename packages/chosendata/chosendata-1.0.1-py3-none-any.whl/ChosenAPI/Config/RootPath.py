

path_dic = {
    "login": "users/login",
    "check_user": "users/checkUser",
    "industry_data_index_name": "industry/industryNames",
    "industry_data": "industry/industryData",
    "industry_index_name": "industry/industryIndexNames",
    "industry_index_data": "industry/industryIndexData",
    "china_macro_all_index": "chinaMacro/showAllIndex",
    "china_macro_guide": "chinaMacro/showIndexes",
    "china_macro_query": "chinaMacro/showIndexData",
    "foreign_macro_all_index": "vip/foreignMacroAllIndex",
    "foreign_macro_guide": "vip/foreignMacroGuide",
    "foreign_macro_query": "vip/foreignMacroQuery",
    "finance_statement": "finance/financeStatement",
    "finance_ratio": "finance/financeRatio",
    "bussiness_composition": "finance/BussinessComposition",
    "finance_statement_xsb": "vip/financeStatementXSB",
    "finance_statement_hk": "vip/financeStatementHK",
    "finance_statement_us": "vip/financeStatementUS",
    "finance_risk_model_value": "vip/financeRiskValue",
    "real_time_news": "publicOpinion/realTimeNews",
    "real_time_news_by_keywords": "publicOpinion/realTimeNewsByKeywords",
    "company_news": "publicOpinion/companyNews",
    "company_news_by_keywords": "publicOpinion/companyNewsByKeywords",
    "company_opinion_score": "publicOpinion/companyPublicOpinionScore",
    "listcompany_report": "report/companyReport",
    "listcompany_rate": "report/companyProfitForecast",
    "industry_report": "report/industryReport",
    "company_job": "job/companyJob",
    "city_job": "job/cityJob",
    "mb_info": "job/mbInfo",
    "company_main_info": "company/companyMainInfo",
    "company_merge_info": "company/companyMergeInfo",
    "ch_stock_trade_daily": "marketTrade/chStockTradeDaily",
    "ch_option_info": "marketTrade/chOptionInfo",
    "ch_option_trade": "marketTrade/chOptionTrade",
    "money_trade": "marketTrade/moneyTrade",
    "vip_mongo_query": "vip/VipDataFromMongo",
    "hot_search_event": "v1/hotSearch/hotEvent",
    "option_recommendation": "v1/option/IvRecommendation",
    "call_option_value": "v1/option/CallOptionIv",
    "option_letter": "v1/option/OptionLetter",
    "option_iv": "v1/option/OptionIv",
    "delete_client_finance_data": "v1/upload/DeleteClientFinanceData",
    "check_client_all_info": "v1/upload/CheckClientAllInfo",
    "forecast_statement_recommendation": "v1/finance/ForecastFinanceStatementRecommendation",
    "forecast_finance_statement": "v1/finance/ForecastFinanceStatement",
    "finance_risk_calculate": "v1/finance/FinanceRiskCalculate",
    "finance_risk_client_query": "v1/finance/FinanceRiskClientQuery",
    "finance_risk_public_query": "v1/finance/FinanceRiskPublicQuery",
    "update_risk_client_query": "v1/finance/FinanceRiskClientUpdate",
    "absolute_valuation_recommendation": "v1/equity/AbsoluteValuationRecommendation",
    "absolute_valuation": "v1/equity/AbsoluteValuation",
    "relative_valuation_recommendation": "v1/equity/RelativeValuationRecommendation",
    "relative_valuation": "v1/equity/RelativeValuation",
    "var_risk_valuation": "v1/equity/VarRiskValuation",
    "bond_macaulay_duration": "v1/bond/MacaulayDuration",
    "bond_convexity": "v1/bond/Convexity",
    "zero_coupon_bond_value": "v1/bond/ZeroCouponBond",
    "best_equity_portfolio": "v1/portfolio/BestEquityPortfolio",
    "related_coefficient": "v1/portfolio/RelatedCoefficient",
    "CAMP_model_value": "v1/portfolio/CAPMModelValue",

}


class RootDest(object):
    def __init__(self):
        self.root_path = {
            'main': 'http://interface.chosen-data.com/v1/',
            'calculate':  'http://calculate.chosen-data.com/',
                          }

    def set_path(self, func, select='main'):
        """
        :param select:
        :param func:
        :return:
        """
        url = self.root_path[select] + path_dic[func]
        print(url)
        return url
