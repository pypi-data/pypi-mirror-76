from ChosenAPI.DataImport.BaseInformation import GetBaseInformation
from ChosenAPI.DataImport.Business_composition import GetBussinessComposition
from ChosenAPI.DataImport.BalanceSheet import GetBalanceSheet
from ChosenAPI.DataImport.IncomeStatement import GetIncomeStatement
from ChosenAPI.DataImport.CashFlow import GetCashFlow
from ChosenAPI.DataImport.important_matters import GetImportantMatters
from ChosenAPI.DataImport.main_taxes_and_rates import GetMainTaxesAndRates
from ChosenAPI.DataImport.cash_equivalents import GetCashEquivalents
from ChosenAPI.DataImport.trading_assets import GetTradingAssets
from ChosenAPI.DataImport.bill_receivable import GetBillReceivable
from ChosenAPI.DataImport.account_receivable import GetAccountReceivable
from ChosenAPI.DataImport.advance_payment import GetAdvancePayment
from ChosenAPI.DataImport.interest_receivable import GetInterestReceivable
from ChosenAPI.DataImport.dividend_receivable import GetDividendReceivable
from ChosenAPI.DataImport.other_receivable import GetOtherReceivable
from ChosenAPI.DataImport.inventories import GetInventories
from ChosenAPI.DataImport.hold_assets_for_sale import GetHoldAssetsForSale
from ChosenAPI.DataImport.non_current_asset_in_one_year import GetNonCurrentAssetInOneYear
from ChosenAPI.DataImport.other_current_assets import GetOtherCurrentAssets
from ChosenAPI.DataImport.hold_for_sale_assets import GetHoldForSaleAssets
from ChosenAPI.DataImport.hold_to_maturity_investments import GetHoldToMaturityInvestments
from ChosenAPI.DataImport.longterm_receivable_account import GetLongtermReceivableAccount
from ChosenAPI.DataImport.longterm_equity_invest import GetLongtermEquityInvest
from ChosenAPI.DataImport.investment_property import GetInvestmentProperty
from ChosenAPI.DataImport.fixed_assets import GetFixedAssets
from ChosenAPI.DataImport.constru_in_process import GetConstruInProcess
from ChosenAPI.DataImport.biological_assets import GetBiologicalAssets
from ChosenAPI.DataImport.intangible_assets import GetIntangibleAssets
from ChosenAPI.DataImport.development_expenditure import GetDevelopmentExpenditure
from ChosenAPI.DataImport.good_will import GetGoodWill
from ChosenAPI.DataImport.long_deferred_expense import GetLongDeferredExpense
from ChosenAPI.DataImport.deferred_tax_assets_and_deferred_tax_liability import GetDeferredTaxAssetsAndDeferredTaxLiability
from ChosenAPI.DataImport.other_noncurrent_assets import GetOtherNoncurrentAssets
from ChosenAPI.DataImport.shortterm_loan import GetShorttermLoan
from ChosenAPI.DataImport.trading_liability import GetTradingLiability
from ChosenAPI.DataImport.notes_payable import GetNotesPayable
from ChosenAPI.DataImport.accounts_payable import GetAccountsPayable
from ChosenAPI.DataImport.advance_peceipts import GetAdvancePeceipts
from ChosenAPI.DataImport.salaries_payable import GetSalariesPayable
from ChosenAPI.DataImport.taxs_payable import GetTaxsPayable
from ChosenAPI.DataImport.interest_payable import GetInterestPayable
from ChosenAPI.DataImport.dividend_payable import GetDividendPayable
from ChosenAPI.DataImport.other_payable import GetOtherPayable
from ChosenAPI.DataImport.hold_liabilities_for_sale import GetHoldLiabilitiesForSale
from ChosenAPI.DataImport.non_current_liability_in_one_year import GetNonCurrentLiabilityInOneYear
from ChosenAPI.DataImport.other_current_liabilities import GetOtherCurrentLiabilities
from ChosenAPI.DataImport.longterm_loan import GetLongtermLoan
from ChosenAPI.DataImport.bonds_payable import GetBondsPayable
from ChosenAPI.DataImport.longterm_account_payable import GetLongtermAccountPayable
from ChosenAPI.DataImport.estimate_liability import GetEstimateLiability
from ChosenAPI.DataImport.deferred_earning import GetDeferredEarning
from ChosenAPI.DataImport.other_noncurrent_liabilities import GetOtherNoncurrentLiabilities
from ChosenAPI.DataImport.other_comprehesive_income import GetOtherComprehesiveIncome
from ChosenAPI.DataImport.operating_revenue_and_operating_cost import GetOperatingRevenueAndOperatingCost
from ChosenAPI.DataImport.operating_tax_surcharges import GetOperatingTaxSurcharges
from ChosenAPI.DataImport.sale_expense import GetSaleExpense
from ChosenAPI.DataImport.administration_expense import GetAdministrationExpense
from ChosenAPI.DataImport.rd_expenses import GetRdExpenses
from ChosenAPI.DataImport.financial_expense import GetFinancialExpense
from ChosenAPI.DataImport.asset_impairment_loss import GetAssetImpairmentLoss
from ChosenAPI.DataImport.other_earnings import GetOtherEarnings
from ChosenAPI.DataImport.investment_income import GetInvestmentIncome
from ChosenAPI.DataImport.fair_value_variable_income import GetFairValueVariableIncome
from ChosenAPI.DataImport.asset_deal_income import GetAssetDealIncome
from ChosenAPI.DataImport.non_operating_revenue import GetNonOperatingRevenue
from ChosenAPI.DataImport.non_operating_expense import GetNonOperatingExpense
from ChosenAPI.DataImport.income_tax import GetIncomeTax
from ChosenAPI.DataImport.cash_flow_additional_information import GetCashFlowAdditionalInformation
from ChosenAPI.DataImport.foreign_currency_monetary_items import GetFCMonetaryItems
from ChosenAPI.DataImport.government_subsidies import GetGovernmentSubsidies
from ChosenAPI.DataImport.limited_assets import GetLimitedAssets
from ChosenAPI.DataImport.employee_situation import GetEmployeeSituation





class ImportTable(object):
    def __init__(self):
        pass

    def db_table(self):
        db_table = {"基本情况": "baseinformation", "资产负债表": "BalanceSheet", "利润表": "IncomeStatement", "现金流量表": "CashFlow",
                    "业务构成": "BussinessComposition", "员工情况": "EmployeeSituation", "重大事项": "ImportantMatters", "主要税种和税率": "MainTaxesAndRates",
                    "货币资金": "CashEquivalents", "以公允价值计量且其变动计入当期损益的金融资产": "TradingAssets",
                    "应收票据": "BillReceivable", "应收账款": "AccountReceivable", "预付款项": "AdvancePayment",
                    "应收利息": "InterestReceivable", "应收股利": "DividendReceivable", "其他应收款": "OtherReceivable",
                    "存货": "Inventories", "持有待售资产": "HoldAssetsForSale",
                    "一年内到期的非流动资产": "NonCurrentAssetInOneYear", "其他流动资产": "OtherCurrentAssets",
                    "可供出售金融资产": "HoldForSaleAssets", "持有至到期投资": "HoldToMaturityInvestments",
                    "长期应收款": "LongtermReceivableAccount", "长期股权投资": "LongtermEquityInvest",
                    "投资性房地产": "InvestmentProperty", "固定资产": "FixedAssets", "在建工程": "ConstruInProcess",
                    "生产性生物资产": "BiologicalAssets", "无形资产": "IntangibleAssets",
                    "开发支出": "DevelopmentExpenditure", "商誉": "GoodWill", "长期待摊费用": "LongDeferredExpense",
                    "递延所得税资产和递延所得税负债": "DeferredTaxAssetsAndDeferredTaxLiability",
                    "其他非流动资产": "OtherNoncurrentAssets", "短期借款": "ShorttermLoan",
                    "以公允价值计量且其变动计入当期损益的金融负债": "TradingLiability", "应付票据": "NotesPayable",
                    "应付账款": "AccountsPayable", "预收款项": "AdvancePeceipts", "应付职工薪酬": "SalariesPayable",
                    "应交税费": "TaxsPayable", "应付利息": "InterestPayable", "应付股利": "DividendPayable",
                    "其他应付款": "OtherPayable", "持有待售负债": "HoldLiabilitiesForSale",
                    "一年内到期的非流动负债": "NonCurrentLiabilityInOneYear", "其他流动负债": "OtherCurrentLiabilities",
                    "长期借款": "LongtermLoan", "应付债券": "BondsPayable", "长期应付款": "LongtermAccountPayable",
                    "预计负债": "EstimateLiability", "递延收益": "DeferredEarning",
                    "其他非流动负债": "OtherNoncurrentLiabilities", "其他综合收益": "OtherComprehesiveIncome",
                    "营业收入和营业成本": "OperatingRevenueAndOperatingCost", "税金及附加": "OperatingTaxSurcharges",
                    "销售费用": "SaleExpense", "管理费用": "AdministrationExpense", "研发费用": "RdExpenses",
                    "财务费用": "FinancialExpense", "资产减值损失": "AssetImpairmentLoss", "其他收益": "OtherEarnings",
                    "投资收益": "InvestmentIncome", "公允价值变动收益": "FairValueVariableIncome",
                    "资产处置收益": "AssetDealIncome", "营业外收入": "NonOperatingRevenue",
                    "营业外支出": "NonOperatingExpense", "所得税费用": "IncomeTax",
                    "现金流量表补充资料": "CashFlowAdditionalInformation", "外币货币性项目": "ForeignCurrencyMonetaryItems",
                    "政府补助": "GovernmentSubsidies", "受限资产": "LimitedAssets", }
        return db_table

    def object_table(self):
        object_table = {"基本情况": GetBaseInformation(), "资产负债表": GetBalanceSheet(), "利润表": GetIncomeStatement(), "现金流量表": GetCashFlow(),
                        "业务构成": GetBussinessComposition(), "员工情况": GetEmployeeSituation(), "重大事项": GetImportantMatters(),
                        "主要税种和税率": GetMainTaxesAndRates(), "货币资金": GetCashEquivalents(),
                        "以公允价值计量且其变动计入当期损益的金融资产": GetTradingAssets(), "应收票据": GetBillReceivable(),
                        "应收账款": GetAccountReceivable(), "预付款项": GetAdvancePayment(), "应收利息": GetInterestReceivable(),
                        "应收股利": GetDividendReceivable(), "其他应收款": GetOtherReceivable(), "存货": GetInventories(),
                        "持有待售资产": GetHoldAssetsForSale(), "一年内到期的非流动资产": GetNonCurrentAssetInOneYear(),
                        "其他流动资产": GetOtherCurrentAssets(), "可供出售金融资产": GetHoldForSaleAssets(),
                        "持有至到期投资": GetHoldToMaturityInvestments(), "长期应收款": GetLongtermReceivableAccount(),
                        "长期股权投资": GetLongtermEquityInvest(), "投资性房地产": GetInvestmentProperty(),
                        "固定资产": GetFixedAssets(), "在建工程": GetConstruInProcess(), "生产性生物资产": GetBiologicalAssets(),
                        "无形资产": GetIntangibleAssets(), "开发支出": GetDevelopmentExpenditure(), "商誉": GetGoodWill(),
                        "长期待摊费用": GetLongDeferredExpense(),
                        "递延所得税资产和递延所得税负债": GetDeferredTaxAssetsAndDeferredTaxLiability(),
                        "其他非流动资产": GetOtherNoncurrentAssets(), "短期借款": GetShorttermLoan(),
                        "以公允价值计量且其变动计入当期损益的金融负债": GetTradingLiability(), "应付票据": GetNotesPayable(),
                        "应付账款": GetAccountsPayable(), "预收款项": GetAdvancePeceipts(), "应付职工薪酬": GetSalariesPayable(),
                        "应交税费": GetTaxsPayable(), "应付利息": GetInterestPayable(), "应付股利": GetDividendPayable(),
                        "其他应付款": GetOtherPayable(), "持有待售负债": GetHoldLiabilitiesForSale(),
                        "一年内到期的非流动负债": GetNonCurrentLiabilityInOneYear(), "其他流动负债": GetOtherCurrentLiabilities(),
                        "长期借款": GetLongtermLoan(), "应付债券": GetBondsPayable(), "长期应付款": GetLongtermAccountPayable(),
                        "预计负债": GetEstimateLiability(), "递延收益": GetDeferredEarning(),
                        "其他非流动负债": GetOtherNoncurrentLiabilities(), "其他综合收益": GetOtherComprehesiveIncome(),
                        "营业收入和营业成本": GetOperatingRevenueAndOperatingCost(), "税金及附加": GetOperatingTaxSurcharges(),
                        "销售费用": GetSaleExpense(), "管理费用": GetAdministrationExpense(), "研发费用": GetRdExpenses(),
                        "财务费用": GetFinancialExpense(), "资产减值损失": GetAssetImpairmentLoss(), "其他收益": GetOtherEarnings(),
                        "投资收益": GetInvestmentIncome(), "公允价值变动收益": GetFairValueVariableIncome(),
                        "资产处置收益": GetAssetDealIncome(), "营业外收入": GetNonOperatingRevenue(),
                        "营业外支出": GetNonOperatingExpense(), "所得税费用": GetIncomeTax(),
                        "现金流量表补充资料": GetCashFlowAdditionalInformation(), "外币货币性项目": GetFCMonetaryItems(),
                        "政府补助": GetGovernmentSubsidies(), "受限资产": GetLimitedAssets()}
        return object_table