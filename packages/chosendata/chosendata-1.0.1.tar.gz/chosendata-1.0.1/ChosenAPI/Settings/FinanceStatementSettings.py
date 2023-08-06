


class StatementName(object):
    def __init__(self):
        pass

    def import_initial_data(self):
        initial_data = {"Import": "baseinformation"}
        return initial_data

    def combine_table_on(self):
        on = ["ID", "report_date", "username"]
        return on

    def import_table_name(self, statement_name):
        if statement_name == "资产负债表":
            import_tables = {
                            "Import": ["BalanceSheet"],
                            "Calculation": ["BalanceSheetInnerRatio", ]}
        elif statement_name == "利润表":
            import_tables = {
                            "Import": ["IncomeStatement"],
                             "Calculation": ["IncomeStatementInnerRatio"]}

        elif statement_name == "现金流量表":
            import_tables = {
                            "Import": ["CashFlow"],
                             "Calculation": ["CashFlowInnerRatio"],
                             }

        elif statement_name in ["偿债能力", "营运能力", "盈利能力", "现金流量"]:  # 与AccountName类finance_ratio_dictionary函数对应
            import_tables = {
                "Calculation": ["FinanceRatio"],
            }

        else:
            import_tables = ""

        return import_tables

    def forecast_finance_statement(self, tablename):
        if tablename == "资产负债表":
            fields = {
                "report_date": "报告期",
                "CashEquivalents": "货币资金",
                "TradingAssetsAndFairValue": "交易性金融资产",
                "AccountReceivableNetValue": "应收账款",
                "BillReceivable": "应收票据",
                "AdvancePayment": "预付账款",
                "OtherReceivableNetValue": "其他应收款",
                "Inventories": "存货",
                "OtherCurrentAssets": "其他流动资产",
                "TotalCurrentAssets": "流动资产合计",
                "LongtermReceivableAccount": "长期应收款",
                "HoldForSaleAssets": "可供出售金融资产",
                "LongtermEquityInvest": "长期股权投资",
                "InvestmentPropertyAndFairValue": "投资性房地产",
                "FixedAssets": "固定资产",
                "ConstruInProcess": "在建工程",
                "IntangibleAssets": "无形资产",
                "DevelopmentExpenditure": "开发支出",
                "GoodWill": "商誉",
                "LongDeferredExpense": "长期待摊费用",
                "OtherNoncurrentAssets": "其他非流动资产",
                "TotalNonCurrentAssets": "非流动资产合计",
                "TotalAssets": "总资产",
                "ShorttermLoan": "短期借款",
                "TradingLiability": "交易性金融负债",
                "AccountsPayable": "应付账款",
                "NotesPayable": "应付票据",
                "AdvancePeceipts": "预收账款",
                "SalariesPayable": "应付职工薪酬",
                "OtherPayable": "其他应付款",
                "OtherCurrentLiabilities": "其他流动负债",
                "TotalCurrentLiabilities": "流动负债合计",
                "LongtermLoan": "长期借款",
                "LongtermAccountPayable": "长期应付款",
                "EstimateLiability": "预计负债",
                "OtherNoncurrentLiabilities": "其他非流动负债",
                "TotalNonCurrentLiabilities": "非流动负债合计",
                "TotalLiabilities": "负债合计",
                "TotalOwnerEquities": "股东权益",
                "TotalLiabilitiesAndOwnerEquities": "负债及所有者权益合计"
            }
        elif tablename == "利润表":
            fields = {
                "report_date": "报告期",
                "OperatingRevenue": "营业收入",
                "OperatingCost": "减：营业成本",
                "OperatingTaxSurcharges": "营业税金及附加",
                "SaleExpense": "销售费用",
                "AdministrationExpense": "管理费用",
                "RdExpenses": "研发费用",
                "FinancialExpense": "财务费用",
                "AssetImpairmentLoss": "资产减值损失",
                "OtherEarnings": "其他收益",
                "ReOperationProfitBeforeTax": "税前经营利润",
                "IncomeTaxFromOperation": "经营利润所得税",
                "NetOperationProfit": "税后经营利润",
                "InvestmentIncome": "投资收益",
                "AssetDealIncome": "资产处置收益",
                "FairValueVariableIncome": "公允价值变动收益",
                "NonOperationProfitBeforeTax": "税前非经营利润",
                "IncomeTax_from_non_operation": "非经营利润所得税",
                "net_non_operation_profit": "税后非经营利润",
                "NetProfit": "净利润",
                "dividend": "普通股股利",
                "RetainEarningAdd": "留存收益增加"
            }

        elif tablename == "现金流量表":
            fields = {
                "report_date": "报告期",
                "NetOperationProfit": "税后经营利润",
                "DepreciationAndAmortization": "加：折旧与摊销",
                "AssetImpairmentLoss": "资产减值损失",
                "FinancialExpense": "利息费用",
                "Inventories_change": "存货的减少(增加以“-”填列)",
                "AR_change": "经营性应收项目的减少(增加以“-”填列)",
                "AP_change": "经营性应付项目的增加(减少以“-”填列)",
                "OtherOperationCashFlow": "其他经营活动有关的现金流量",
                "NetOperateCashFlow": "经营活动产生的现金流量净额",
                "InvestmentIncomeOfCashFlow": "加：投资收益",
                "AssetDealIncomeOfCashFlow": "资产处置收益",
                "FinancialAssetsNetAdd": "减：金融资产投资",
                "AddInvestFromConstruInProcess": "在建工程投资",
                "AddInvestFromFixAsset": "固定资产投资",
                "AddInvestFromIntangibleAssets": "无形资产投资",
                "AddInvestFromDevelopmentExpenditure": "开发支出投资",
                "AddInvestFromInvestmentProperty": "投资性房地产投资",
                "AddInvestFromLongTermEquityInvest": "长期股权投资投资",
                "AddGoodWill": "商誉增加",
                "AddInvestFromLongDeferredExpense": "长期待摊费用投资",
                "OtherInvestmentCashFlow": "加：其他投资活动有关的现金流量",
                "NetInvestCashFlow": "投资活动产生的现金流量净额",
                "finance_add_total_owner_equities_list": "加：股东投入增加",
                "add_short_term_loan_list": "短期带息债务增加",
                "add_long_term_loan_list": "长期带息债务增加",
                "dividend": "支付普通股股利",
                "CashFlowFinancialExpense": "偿付利息",
                "add_longterm_account_payable_list": "加：其他筹资活动有关的现金流量",
                "NetFinanceCashFlow": "筹资活动产生的现金流量净额",
                "CashEquivalentsNetChange": "现金及现金等价物净增加额"

            }
        elif tablename == "偿债能力":
            fields = {
                "report_date": "报告期",
                "CurrentRatio": "流动比率",
                "QuickRatio": "速动比率",
                "DebtAssetsRatio": "资产负债率",
                "InteBearDebtToTotalDebt": "带息债务／总负债(%)",
                "InterestCover": "利息保障倍数",
                "NOCFToInterest": "现金流量利息保障倍数",
                "InteBearDebtToTotalCapital": "长期资本负债率(%)",

            }

        elif tablename == "运营能力":
            fields = {
                "report_date": "报告期",
                "TotalAssetTRate": "总资产周转率",
                "AccountsPayablesTRate": "应收账款周转率",
                "InventoryTRate": "存货周转率"
            }

        elif tablename == "盈利能力":
            fields = {
                "report_date": "报告期",
                "GrossIncomeRatio": "毛利率(%)",
                "OperatingProfitToTOR": "营业净利润率(%)",
                "NetProfitRatio": "净利润率(%)",
                "ROA": "总资产报酬率(%)",
                "ROE": "净资产收益率(%)",
                "PeriodExpenseToRevenue": "期间费用／营业收入(%)",
                "EBITToRevenue": "EBIT／营业收入(%)",
                "EBITDAToRevenue": "EBITDA／营业收入(%)",

            }

        else:
            fields = {}

        return fields

    def forecast_settings(self):
        dic = {
            "货币资金占营业收入的最低资金比例(%)": "CashEquivalents",
            "在建工程总投入及各期投入比例(%)": "ConstructionInProgress",
            "固定资产总投入及各期投入比例(%)": "FixedAssets",
            "投资性房地产总投入及各期投入比例(%)": "InvestmentProperty",
            "无形资产总投入及各期投入比例(%)": "IntangibleAssets",
            "开发支出总投入及各期投入比例(%)": "DevelopmentExpenditure",
            "长期待摊费用总投入及各期投入比例(%)": "LongDeferredExpense",
            "应收账款周转率": "AccountReceivable",
            "坏账准备比例(%)": "BedDebt",
            "应收票据周转率": "BillReceivable",
            "预付账款周转率": "AdvancePayment",
            "其他应收款周转率": "OtherReceivable",
            "存货周转率": "Inventories",
            "应付账款周转率": "AccountsPayable",
            "应付票据周转率": "NotesPayable",
            "预收账款周转率": "AdvancePeceipts",
            "其他应付款周转率": "OtherPayable",
            "应付职工薪酬增量": "SalariesPayable",
            "其他流动资产增量": "OtherCurrentAssets",
            "其他流动负债增量": "OtherCurrentLiabilities",
            "长期应收款增量": "LongtermReceivableAccount",
            "预计负债增量": "EstimateLiability",
            "其他非流动资产增量": "OtherNoncurrentAssets",
            "其他非流动负债增量": "OtherNoncurrentLiabilities",
            "长期应付款增量": "LongtermAccountPayable",
            "交易性金融资产投入": "TradingSssets",
            "可供出售金融资产投入": "HoldForSaleAssets",
            "交易性金融负债投入": "TradingLiability",
            "长期股权投资投入": "LongtermEquityInvest",
            "商誉增加": "GoodWill",
            "销售收入增长率(%)": "OperatingRevenue",
            "毛利率(%)": "OperatingCost",
            "营业税金及附加占收入比率(%)": "OperatingTaxSurcharges",
            "销售费用占收入比率(%)": "SaleExpense",
            "管理费用占收入比率(%)": "AdministrationExpense",
            "研发费用占收入比率(%)": "RdExpense",
            "短期债务利率(%)": "ShortFinancialExpense",
            "长期债务利率(%)": "LongFinancialExpense",
            "短期债务投入比例(%)": "ShortFinancialRatio",
            "长期债务投入比例(%)": "LongFinancialRatio",
            "股东投入比例(%)": "EquityFinancialRatio",
            "金融投资公允价值变动": "FinanceAssetsFairValue",
            "投资性房地产公允价值变动": "InvestmentPropertyFairValue",
            "投资收益": "InvestmentIncome",
            "资产处置收益": "AssetDealIncome",
            "其他收益": "OtherEarnings",
            "营业外收入": "NonOperatingRevenue",
            "营业外支出": "NonOperatingExpense",
            "所得税率(%)": "IncomeTax",
            "普通股分红比例(%)": "Dividend"
        }

        contents = []
        for k in dic.keys():
            contents.append([k])

        return dic, contents


class AccountName(object):

    def __init__(self):
        pass

    def account_dictionary(self, statement_name):
        if statement_name == "资产负债表":

            dic = {
                "CashEquivalents": "货币资金",
                "SettlementProvi": "结算备付金",
                "LendCapital": "拆出资金",
                "TradingAssets": "以公允价值计量且其变动计入当期损益的金融资产",
                "DerivativeFinancialAsset": "衍生金融资产",
                "BillReceivable": "应收票据",
                "AccountReceivable": "应收账款",
                "AdvancePayment": "预付款项",
                "InsuranceReceivables": "应收保费",
                "ReinsuranceReceivables": "应收分保账款",
                "ReinsuranceContractReservesReceivable": "应收分保合同准备金",
                "InterestReceivable": "应收利息",
                "DividendReceivable": "应收股利",
                "OtherReceivable": "其他应收款",
                "BoughtSellbackAssets": "买入返售金融资产",
                "Inventories": "存货",
                "ContractAssets": "合同资产",
                "HoldAssetsForSale": "持有待售资产",
                "NonCurrentAssetInOneYear": "一年内到期的非流动资产",
                "OtherCurrentAssets": "其他流动资产",
                "TotalCurrentAssets": "流动资产合计",
                "LoanAndAdvance": "发放贷款和垫款",
                "HoldForSaleAssets": "可供出售金融资产",
                "HoldToMaturityInvestments": "持有至到期投资",
                "LongtermReceivableAccount": "长期应收款",
                "LongtermEquityInvest": "长期股权投资",
                "InvestmentProperty": "投资性房地产",
                "FixedAssets": "固定资产",
                "ConstruInProcess": "在建工程",
                "BiologicalAssets": "生产性生物资产",
                "OilGasAssets": "油气资产",
                "IntangibleAssets": "无形资产",
                "DevelopmentExpenditure": "开发支出",
                "GoodWill": "商誉",
                "LongDeferredExpense": "长期待摊费用",
                "DeferredTaxAssets": "递延所得税资产",
                "OtherNoncurrentAssets": "其他非流动资产",
                "TotalNonCurrentAssets": "非流动资产合计",
                "TotalAssets": "资产总计",
                "ShorttermLoan": "短期借款",
                "BorrowingFromCentralbank": "向中央银行借款",
                "DepositInInterbank": "吸收存款及同业存放",
                "BorrowingCapital": "拆入资金",
                "TradingLiability": "以公允价值计量且其变动计入当期损益的金融负债",
                "DerivativeFinancialLiability": "衍生金融负债",
                "NotesPayable": "应付票据",
                "AccountsPayable": "应付账款",
                "AdvancePeceipts": "预收款项",
                "ContractLiabilities": "合同负债",
                "SoldBuybackSecuProceeds": "卖出回购金融资产款",
                "CommissionPayable": "应付手续费及佣金",
                "SalariesPayable": "应付职工薪酬",
                "TaxsPayable": "应交税费",
                "InterestPayable": "应付利息",
                "DividendPayable": "应付股利",
                "OtherPayable": "其他应付款",
                "ReinsurancePayables": "应付分保账款",
                "InsuranceContractReserves": "保险合同准备金",
                "ProxySecuProceeds": "代理买卖证券款",
                "ReceivingsFromVicariouslySoldSecurities": "代理承销证券款",
                "HoldLiabilitiesForSale": "持有待售负债",
                "NonCurrentLiabilityInOneYear": "一年内到期的非流动负债",
                "OtherCurrentLiabilities": "其他流动负债",
                "TotalCurrentLiability": "流动负债合计",
                "LongtermLoan": "长期借款",
                "BondsPayable": "应付债券",
                "PreferredSharesNoncurrent": "其中：优先股",
                "PepertualLiabilityNoncurrent": "永续债",
                "LongtermAccountPayable": "长期应付款",
                "LongtermSalariesPayable": "长期应付职工薪酬",
                "EstimateLiability": "预计负债",
                "DeferredEarning": "递延收益",
                "DeferredTaxLiability": "递延所得税负债",
                "OtherNoncurrentLiabilities": "其他非流动负债",
                "TotalNonCurrentLiability": "非流动负债合计",
                "TotalLiability": "负债合计",
                "TotalOwnerEquities": "股东权益合计",
                "OtherComprehesiveIncome": "其他综合收益",
                "TotalSheetOwnerEquities": "负债和股东权益合计",

            }

        elif statement_name == "利润表":

            dic = {
                "TotalOperatingRevenue": "营业总收入",
                "OperatingRevenue": "其中：营业收入",
                "InterestIncome_TotalOperatingRevenue": "利息收入",
                "PremiumsEarned": "已赚保费",
                "CommissionIncome": "手续费及佣金收入",
                "TotalOperatingCost": "营业总成本",
                "OperatingCost": "其中：营业成本",
                "InterestExpense": "利息支出",
                "CommissionExpense": "手续费及佣金支出",
                "RefundedPremiums": "退保金",
                "NetPayInsuranceClaims": "赔付支出净额",
                "WithdrawInsuranceContractReserve": "提取保险合同准备金净额",
                "PolicyDividendPayout": "保单红利支出",
                "ReinsuranceCost": "分保费用",
                "OperatingTaxSurcharges": "税金及附加",
                "SaleExpense": "销售费用",
                "AdministrationExpense": "管理费用",
                "RdExpenses": "研发费用",
                "FinancialExpense": "财务费用",
                "InterestCharges": "其中：利息费用",
                "InterestIncome": "利息收入",
                "AssetImpairmentLoss": "资产减值损失",
                "OtherEarnings": "加：其他收益",
                "InvestmentIncome": "投资收益",
                "InvestIncomeAssociates": "其中：对联营企业和合营企业的投资收益",
                "FairValueVariableIncome": "公允价值变动收益",
                "ExchangeIncome": "汇兑收益",
                "AssetDealIncome": "资产处置收益",
                "OperatingProfit": "营业利润",
                "NonOperatingRevenue": "加：营业外收入",
                "NonOperatingExpense": "减：营业外支出",
                "TotalProfit": "利润总额",
                "IncomeTax": "减：所得税费用",
                "NetProfit": "净利润",
                "NetProfitFromGoingConcern": "持续经营净利润",
                "NetProfitAfterOperation": "终止经营净利润",
                "NpParentCompanyOwners": "归属于母公司所有者的净利润",
                "MinorityProfit": "少数股东损益",
                "NetAfterTaxOfOtherComprehensiveIncome": "其他综合收益的税后净额",
                "TotalCompositeIncome": "综合收益总额",
                "CiParentCompanyOwners": "归属于母公司所有者的综合收益总额",
                "CiMinorityOwners": "归属于少数股东的综合收益总额",

            }

        elif statement_name == "现金流量表":
            dic = {
                "GoodsSaleAndServiceRenderCash": "销售商品、提供劳务收到的现金",
                "NetDepositIncrease": "客户存款和同业存放款项净增加额",
                "NetBorrowingFromCentralBank": "向中央银行借款净增加额",
                "NetBorrowingFromFinanceCo": "向其他金融机构拆入资金净增加额",
                "NetOriginalInsuranceCash": "收到原保险合同保费取得的现金",
                "NetCashReceivedFromReinsuranceBusiness": "收到再保险业务现金净额",
                "NetInsurerDepositInvestment": "保户储金及投资款净增加额",
                "NetDealTradingAssets": "处置以公允价值计量且其变动计入当期损益的金融资产净增加额",
                "InterestAndCommissionCashin": "收取利息、手续费及佣金的现金",
                "NetIncreaseInPlacements": "拆入资金净增加额",
                "NetBuyback": "回购业务资金净增加额",
                "TaxLevyRefund": "收到的税费返还",
                "OtherCashInRelatedOperate": "收到其他与经营活动有关的现金",
                "SubtotalOperateCashInflow": "经营活动现金流入小计",

                # "NetOperateCashFlow": "经营活动产生的现金流量净额",
                "InvestWithdrawalCash": "收回投资收到的现金",
                "InvestProceeds": "取得投资收益收到的现金",
                "FixIntanOtherAssetDispoCash": "处置固定资产、无形资产和其他长期资产收回的现金净额",
                "NetCashDealSubcompany": "处置子公司及其他营业单位收到的现金净额",
                "OtherCashInRelatedInvest": "收到的其他与投资活动有关的现金",
                "SubtotalInvestCashInflow": "投资活动现金流入小计",

                # "NetInvestCashFlow": "投资活动产生的现金流量净额",
                "CashFromInvest": "吸收投资收到的现金",
                "CashFromMinoSInvestSub": "其中：子公司吸收少数股东投资收到的现金",
                "CashFromBorrowing": "取得借款收到的现金",
                "CashFromBondsIssue": "发行债券收到的现金",
                "OtherCashInRelatedFinance": "收到其他与筹资活动有关的现金",
                "SubtotalFinanceCashInflow": "筹资活动现金流入小计",

                "GoodsAndServicesCashPaid": "购买商品、接受劳务支付的现金",
                "NetLoanAndAdvanceIncrease": "客户贷款及垫款净增加额",
                "NetDepositInCbAndIb": "存放中央银行和同业款项净增加额",
                "OriginalCompensationPaid": "支付原保险合同赔付款项的现金",
                "HandlingChargesAndCommission": "支付利息、手续费及佣金的现金",
                "PolicyDividendCashPaid": "支付保单红利的现金",
                "StaffBehalfPaid": "支付给职工以及为职工支付的现金",
                "TaxPayments": "支付的各项税费",
                "OtherOperateCashPaid": "支付的其他与经营活动有关的现金",
                "SubtotalOperateCashOutflow": "经营活动现金流出小计",

                "FixIntanOtherAssetAcquiCash": "购建固定资产、无形资产和其他长期资产支付的现金",
                "InvestCashPaid": "投资支付的现金",
                "ImpawnedLoanNetIncrease": "质押贷款净增加额",
                "NetCashFromSubCompany": "取得子公司及其他营业单位支付的现金净额",
                "OtherInvestCashPaid": "支付的其他与投资活动有关的现金",
                "SubtotalInvestCashOutflow": "投资活动现金流出小计",

                "BorrowingRepayment": "偿还债务支付的现金",
                "DividendInterestPayment": "分配股利、利润或偿付利息支付的现金",
                "ProceedsFromSubToMinoS": "其中：子公司支付给少数股东的股利、利润",
                "OtherFinanceCashPaid": "支付的其他与筹资活动有关的现金",
                "SubtotalFinanceCashOutflow": "筹资活动现金流出小计",

                # "NetFinanceCashFlow": "筹资活动产生的现金流量净额",
                # "ExchangeRateChangeEffect": "汇率变动对现金及现金等价物的影响",
                # "CashEquivalentIncrease": "现金及现金等价物净增加额",
                # "CashEquivalentsAtBeginning": "加：年初现金及现金等价物余额",
                # "CashAndEquivalentsAtEnd": "期末现金及现金等价物余额",
            }

        else:
            dic = {}

        return dic

    def finance_ratio_dictionary(self, classify_name):
        if classify_name == "偿债能力":
            dic = {
                "CurrentRatio": "流动比率",
                "QuickRatio": "速动比率",
                "SuperQuickRatio": "超速动比率",
                "DebtAssetsRatio": "资产负债率(%)",
                "DebtEquityRatio": "产权比率",
                "SEWithoutMIToTL": "归属母公司股东产权比率",
                "SEWMIToInterestBearDebt": "归属母公司股东的权益带息债务率",
                "DebtTangibleEquityRatio": "有形净值债务率",
                "InterestCover": "利息保障倍数",
                "LongDebtToWorkingCapital": "长期负债与营运资金比率",
                "OperCashInToCurrentDebt": "现金流动负债比",
                "CurrentAssetsToTA": "流动资产／总资产(%)",
                "NonCurrentAssetsToTA": "非流动资产／总资产(%)",
                "FixAssetRatio": "固定资产比率(%)",
                "IntangibleAssetRatio": "无形资产比率(%)",
                "LongDebtToAsset": "长期借款/总资产(%)",
                "BondsPayableToAsset": "应付债券/总资产(%)",
                "CurrentLiabilityToTL": "流动负债／负债合计(%)",
                "NonCurrentLiabilityToTL":"非流动负债／负债合计(%)",
                "EquityToAsset": "股东权益比率(%)",
                "EquityMultipler": "权益乘数",
                "LongDebtToEquity": "长期负债/股东权益合计",
                "NetAssetGrowRate": "净资产增长率",
                "TotalAssetGrowRate": "总资产增长率",
                "SEWithoutMIGrowRateYTD": "归属母公司股东的权益增长率"

            }

        elif classify_name == "营运能力":
            dic = {
                "TotalAssetTRate": "总资产周转率",
                "ARTRate": "应收账款周转率",
                "InventoryTRate": "存货周转率",
                "AccountsPayablesTRate": "应付账款周转率",
                "ARTDays": "应收账款周转天数",
                "InventoryTDays": "存货周转天数",
                "AccountsPayablesTDays": "应付账款周转天数",
                "OperCycle": "营业周期",
                "CurrentAssetsTRate": "流动资产周转率",
                "FixedAssetTRate": "固定资产周转率",
                "EquityTRate": "股东权益周转率",

            }

        elif classify_name == "盈利能力":
            dic = {
                "NPToTOR": "净利润率",
                "NPToTORTTM": "净利润率(TTM)",
                "NetProfitRatio": "销售净利率",
                "NetProfitRatioTTM": "销售净利率TTM",
                "GrossIncomeRatio": "销售毛利率",
                "GrossIncomeRatioTTM": "销售毛利率(TTM)",
                "OperatingProfitToTOR": "营业利润率",
                "OperatingProfitToTORTTM": "营业利润率TTM",
                "EBITToTOR": "息税前利润率",
                "EBITToTORTTM": "息税前利润率TTM",
                "ROEAvg": "净资产收益率_平均",
                "ROE": "净资产收益率_摊薄",
                "ROETTM": "净资产收益率(TTM)",
                "NAORYOY": "净资产收益率(摊薄)同比增长",
                "ROA_EBIT": "总资产报酬率(EBIT)",
                "ROA_EBITTTM": "总资产报酬率(EBIT_TTM)",
                "OperatingRevenueGrowRate": "营业收入同比增长(%)",
                "NPParentCompanyYOY": "归属母公司股东的净利润同比增长",
                "ROA": "总资产净利率",
                "SalesCostRatio": "销售成本率",
                "PeriodCostsRate": "销售期间费用率",
                "TOperatingCostToTOR": "营业总成本率",
                "TOperatingCostToTORTTM": "营业总成本率TTM",
                "OperatingExpenseRate": "销售费用率",
                "OperatingExpenseRateTTM": "销售费用率TTM",
                "AdminiExpenseRate": "管理费用率",
                "AdminiExpenseRateTTM": "管理费用率TTM",
                "FinancialExpenseRate": "财务费用率",
                "FinancialExpenseRateTTM": "财务费用率TTM",
                "AssetImpaLossToTOR": "资产减值损失率",
                "AssetImpaLossToTORTTM": "资产减值损失率TTM",
                "OperatingProfitRatio": "营业利润率",
                "TotalProfitCostRatio": "成本费用利润率",

            }

        elif classify_name == "现金流量":
            dic = {
                "NetOperateCashFlowYOY": "经营活动产生的现金流量净额同比增长",
                "SaleServiceCashToOR": "销售商品提供劳务收到的现金/营业收入",
                "SaleServiceCashToORTTM": "销售商品提供劳务收到的现金/营业收入(TTM)",
                "CashRateOfSalesTTM": "经营活动产生的现金流量净额/营业收入(TTM)",
                "NOCFToOperatingNI": "经营活动产生的现金流量净额/经营活动净收益",
                "NOCFToOperatingNITTM": "经营活动产生的现金流量净额/经营活动净收益(TTM)",
                "NetProfitCashCover": "净利润现金含量",
                "OperatingRevenueCashCover": "营业收入现金含量",
                "OperCashInToAsset": "总资产现金回收率",

            }

        else:
            dic = {}

        return dic







