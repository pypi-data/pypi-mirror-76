
import pandas as pd
from ChosenAPI.DataImport.ChangeToNum import ChangeData



class GetBalanceSheet(object):
    def __init__(self):
        pass

    def get_data(self, data, username, identify): # 定义数据位置
        """
        获取基本数据表格的数据，
        :param data: 传入数据表格
        :param username: 用户名
        :param identify: 实例识别号
        :return:
        """
        dic = {
            "CashEquivalents_this": data.cell_value(7, 4),  # E8,8行5列货币资金
            "SettlementProvi_this": data.cell_value(8, 4),  # E9,9行5列结算备付金
            "LendCapital_this": data.cell_value(9, 4),  # E10,10行5列拆出资金
            "TradingAssets_this": data.cell_value(10, 4),  # E11,11行5列以公允价值计量且其变动计入当期损益的金融资产
            "DerivativeFinancialAsset_this": data.cell_value(11, 4),  # E12,12行5列衍生金融资产
            "BillReceivable_this": data.cell_value(12, 4),  # E13,13行5列应收票据
            "AccountReceivable_this": data.cell_value(13, 4),  # E14,14行5列应收账款
            "AdvancePayment_this": data.cell_value(14, 4),  # E15,15行5列预付款项
            "InsuranceReceivables_this": data.cell_value(15, 4),  # E16,16行5列应收保费
            "ReinsuranceReceivables_this": data.cell_value(16, 4),  # E17,17行5列应收分保账款
            "ReinsuranceContractReservesReceivable_this": data.cell_value(17, 4),  # E18,18行5列应收分保合同准备金
            "InterestReceivable_this": data.cell_value(18, 4),  # E19,19行5列应收利息
            "DividendReceivable_this": data.cell_value(19, 4),  # E20,20行5列应收股利
            "OtherReceivable_this": data.cell_value(20, 4),  # E21,21行5列其他应收款
            "BoughtSellbackAssets_this": data.cell_value(21, 4),  # E22,22行5列买入返售金融资产
            "Inventories_this": data.cell_value(22, 4),  # E23,23行5列存货
            "ContractAssets_this": data.cell_value(23, 4),  # E24,24行5列合同资产
            "HoldAssetsForSale_this": data.cell_value(24, 4),  # E25,25行5列持有待售资产
            "NonCurrentAssetInOneYear_this": data.cell_value(25, 4),  # E26,26行5列一年内到期的非流动资产
            "OtherCurrentAssets_this": data.cell_value(26, 4),  # E27,27行5列其他流动资产
            "TotalCurrentAssets_this": data.cell_value(27, 4),  # E28,28行5列流动资产合计
            "LoanAndAdvance_this": data.cell_value(29, 4),  # E30,30行5列发放贷款和垫款
            "HoldForSaleAssets_this": data.cell_value(30, 4),  # E31,31行5列可供出售金融资产
            "HoldToMaturityInvestments_this": data.cell_value(31, 4),  # E32,32行5列持有至到期投资
            "LongtermReceivableAccount_this": data.cell_value(32, 4),  # E33,33行5列长期应收款
            "LongtermEquityInvest_this": data.cell_value(33, 4),  # E34,34行5列长期股权投资
            "InvestmentProperty_this": data.cell_value(34, 4),  # E35,35行5列投资性房地产
            "FixedAssets_this": data.cell_value(35, 4),  # E36,36行5列固定资产
            "ConstruInProcess_this": data.cell_value(36, 4),  # E37,37行5列在建工程
            "BiologicalAssets_this": data.cell_value(37, 4),  # E38,38行5列生产性生物资产
            "OilGasAssets_this": data.cell_value(38, 4),  # E39,39行5列油气资产
            "IntangibleAssets_this": data.cell_value(39, 4),  # E40,40行5列无形资产
            "DevelopmentExpenditure_this": data.cell_value(40, 4),  # E41,41行5列开发支出
            "GoodWill_this": data.cell_value(41, 4),  # E42,42行5列商誉
            "LongDeferredExpense_this": data.cell_value(42, 4),  # E43,43行5列长期待摊费用
            "DeferredTaxAssets_this": data.cell_value(43, 4),  # E44,44行5列递延所得税资产
            "OtherNoncurrentAssets_this": data.cell_value(44, 4),  # E45,45行5列其他非流动资产
            "TotalNonCurrentAssets_this": data.cell_value(47, 4),  # E48,48行5列非流动资产合计
            "TotalAssets_this": data.cell_value(48, 4),  # E49,49行5列资产总计
            "CashEquivalents_last": data.cell_value(7, 5),  # F8,8行6列货币资金
            "SettlementProvi_last": data.cell_value(8, 5),  # F9,9行6列结算备付金
            "LendCapital_last": data.cell_value(9, 5),  # F10,10行6列拆出资金
            "TradingAssets_last": data.cell_value(10, 5),  # F11,11行6列以公允价值计量且其变动计入当期损益的金融资产
            "DerivativeFinancialAsset_last": data.cell_value(11, 5),  # F12,12行6列衍生金融资产
            "BillReceivable_last": data.cell_value(12, 5),  # F13,13行6列应收票据
            "AccountReceivable_last": data.cell_value(13, 5),  # F14,14行6列应收账款
            "AdvancePayment_last": data.cell_value(14, 5),  # F15,15行6列预付款项
            "InsuranceReceivables_last": data.cell_value(15, 5),  # F16,16行6列应收保费
            "ReinsuranceReceivables_last": data.cell_value(16, 5),  # F17,17行6列应收分保账款
            "ReinsuranceContractReservesReceivable_last": data.cell_value(17, 5),  # F18,18行6列应收分保合同准备金
            "InterestReceivable_last": data.cell_value(18, 5),  # F19,19行6列应收利息
            "DividendReceivable_last": data.cell_value(19, 5),  # F20,20行6列应收股利
            "OtherReceivable_last": data.cell_value(20, 5),  # F21,21行6列其他应收款
            "BoughtSellbackAssets_last": data.cell_value(21, 5),  # F22,22行6列买入返售金融资产
            "Inventories_last": data.cell_value(22, 5),  # F23,23行6列存货
            "ContractAssets_last": data.cell_value(23, 5),  # F24,24行6列合同资产
            "HoldAssetsForSale_last": data.cell_value(24, 5),  # F25,25行6列持有待售资产
            "NonCurrentAssetInOneYear_last": data.cell_value(25, 5),  # F26,26行6列一年内到期的非流动资产
            "OtherCurrentAssets_last": data.cell_value(26, 5),  # F27,27行6列其他流动资产
            "TotalCurrentAssets_last": data.cell_value(27, 5),  # F28,28行6列流动资产合计
            "LoanAndAdvance_last": data.cell_value(29, 5),  # F30,30行6列发放贷款和垫款
            "HoldForSaleAssets_last": data.cell_value(30, 5),  # F31,31行6列可供出售金融资产
            "HoldToMaturityInvestments_last": data.cell_value(31, 5),  # F32,32行6列持有至到期投资
            "LongtermReceivableAccount_last": data.cell_value(32, 5),  # F33,33行6列长期应收款
            "LongtermEquityInvest_last": data.cell_value(33, 5),  # F34,34行6列长期股权投资
            "InvestmentProperty_last": data.cell_value(34, 5),  # F35,35行6列投资性房地产
            "FixedAssets_last": data.cell_value(35, 5),  # F36,36行6列固定资产
            "ConstruInProcess_last": data.cell_value(36, 5),  # F37,37行6列在建工程
            "BiologicalAssets_last": data.cell_value(37, 5),  # F38,38行6列生产性生物资产
            "OilGasAssets_last": data.cell_value(38, 5),  # F39,39行6列油气资产
            "IntangibleAssets_last": data.cell_value(39, 5),  # F40,40行6列无形资产
            "DevelopmentExpenditure_last": data.cell_value(40, 5),  # F41,41行6列开发支出
            "GoodWill_last": data.cell_value(41, 5),  # F42,42行6列商誉
            "LongDeferredExpense_last": data.cell_value(42, 5),  # F43,43行6列长期待摊费用
            "DeferredTaxAssets_last": data.cell_value(43, 5),  # F44,44行6列递延所得税资产
            "OtherNoncurrentAssets_last": data.cell_value(44, 5),  # F45,45行6列其他非流动资产
            "TotalNonCurrentAssets_last": data.cell_value(47, 5),  # F48,48行6列非流动资产合计
            "TotalAssets_last": data.cell_value(48, 5),  # F49,49行6列资产总计
            "ShorttermLoan_this": data.cell_value(7, 9),  # J8,8行10列短期借款
            "BorrowingFromCentralbank_this": data.cell_value(8, 9),  # J9,9行10列向中央银行借款
            "DepositInInterbank_this": data.cell_value(9, 9),  # J10,10行10列吸收存款及同业存放
            "BorrowingCapital_this": data.cell_value(10, 9),  # J11,11行10列拆入资金
            "TradingLiability_this": data.cell_value(11, 9),  # J12,12行10列以公允价值计量且其变动计入当期损益的金融负债
            "DerivativeFinancialLiability_this": data.cell_value(12, 9),  # J13,13行10列衍生金融负债
            "NotesPayable_this": data.cell_value(13, 9),  # J14,14行10列应付票据
            "AccountsPayable_this": data.cell_value(14, 9),  # J15,15行10列应付账款
            "AdvancePeceipts_this": data.cell_value(15, 9),  # J16,16行10列预收款项
            "ContractLiabilities_this": data.cell_value(16, 9),  # J17,17行10列合同负债
            "SoldBuybackSecuProceeds_this": data.cell_value(17, 9),  # J18,18行10列卖出回购金融资产款
            "CommissionPayable_this": data.cell_value(18, 9),  # J19,19行10列应付手续费及佣金
            "SalariesPayable_this": data.cell_value(19, 9),  # J20,20行10列应付职工薪酬
            "TaxsPayable_this": data.cell_value(20, 9),  # J21,21行10列应交税费
            "InterestPayable_this": data.cell_value(21, 9),  # J22,22行10列应付利息
            "DividendPayable_this": data.cell_value(22, 9),  # J23,23行10列应付股利
            "OtherPayable_this": data.cell_value(23, 9),  # J24,24行10列其他应付款
            "ReinsurancePayables_this": data.cell_value(24, 9),  # J25,25行10列应付分保账款
            "InsuranceContractReserves_this": data.cell_value(25, 9),  # J26,26行10列保险合同准备金
            "ProxySecuProceeds_this": data.cell_value(26, 9),  # J27,27行10列代理买卖证券款
            "ReceivingsFromVicariouslySoldSecurities_this": data.cell_value(27, 9),  # J28,28行10列代理承销证券款
            "HoldLiabilitiesForSale_this": data.cell_value(28, 9),  # J29,29行10列持有待售负债
            "NonCurrentLiabilityInOneYear_this": data.cell_value(29, 9),  # J30,30行10列一年内到期的非流动负债
            "OtherCurrentLiabilities_this": data.cell_value(30, 9),  # J31,31行10列其他流动负债
            "TotalCurrentLiability_this": data.cell_value(31, 9),  # J32,32行10列流动负债合计
            "LongtermLoan_this": data.cell_value(33, 9),  # J34,34行10列长期借款
            "BondsPayable_this": data.cell_value(34, 9),  # J35,35行10列应付债券
            "PreferredSharesNoncurrent_this": data.cell_value(35, 9),  # J36,36行10列其中：优先股
            "PepertualLiabilityNoncurrent_this": data.cell_value(36, 9),  # J37,37行10列永续债
            "LongtermAccountPayable_this": data.cell_value(37, 9),  # J38,38行10列长期应付款
            "LongtermSalariesPayable_this": data.cell_value(38, 9),  # J39,39行10列长期应付职工薪酬
            "EstimateLiability_this": data.cell_value(39, 9),  # J40,40行10列预计负债
            "DeferredEarning_this": data.cell_value(40, 9),  # J41,41行10列递延收益
            "DeferredTaxLiability_this": data.cell_value(41, 9),  # J42,42行10列递延所得税负债
            "OtherNoncurrentLiabilities_this": data.cell_value(42, 9),  # J43,43行10列其他非流动负债
            "TotalNonCurrentLiability_this": data.cell_value(43, 9),  # J44,44行10列非流动负债合计
            "TotalLiability_this": data.cell_value(44, 9),  # J45,45行10列负债合计
            "TotalOwnerEquities_this": data.cell_value(46, 9),  # J47,47行10列股东权益合计
            "OtherComprehesiveIncome_this": data.cell_value(47, 9),  # J48,48行10列其他综合收益
            "TotalSheetOwnerEquities_this": data.cell_value(48, 9),  # J49,49行10列负债和股东权益合计
            "ShorttermLoan_last": data.cell_value(7, 10),  # K8,8行11列短期借款
            "BorrowingFromCentralbank_last": data.cell_value(8, 10),  # K9,9行11列向中央银行借款
            "DepositInInterbank_last": data.cell_value(9, 10),  # K10,10行11列吸收存款及同业存放
            "BorrowingCapital_last": data.cell_value(10, 10),  # K11,11行11列拆入资金
            "TradingLiability_last": data.cell_value(11, 10),  # K12,12行11列以公允价值计量且其变动计入当期损益的金融负债
            "DerivativeFinancialLiability_last": data.cell_value(12, 10),  # K13,13行11列衍生金融负债
            "NotesPayable_last": data.cell_value(13, 10),  # K14,14行11列应付票据
            "AccountsPayable_last": data.cell_value(14, 10),  # K15,15行11列应付账款
            "AdvancePeceipts_last": data.cell_value(15, 10),  # K16,16行11列预收款项
            "ContractLiabilities_last": data.cell_value(16, 10),  # K17,17行11列合同负债
            "SoldBuybackSecuProceeds_last": data.cell_value(17, 10),  # K18,18行11列卖出回购金融资产款
            "CommissionPayable_last": data.cell_value(18, 10),  # K19,19行11列应付手续费及佣金
            "SalariesPayable_last": data.cell_value(19, 10),  # K20,20行11列应付职工薪酬
            "TaxsPayable_last": data.cell_value(20, 10),  # K21,21行11列应交税费
            "InterestPayable_last": data.cell_value(21, 10),  # K22,22行11列应付利息
            "DividendPayable_last": data.cell_value(22, 10),  # K23,23行11列应付股利
            "OtherPayable_last": data.cell_value(23, 10),  # K24,24行11列其他应付款
            "ReinsurancePayables_last": data.cell_value(24, 10),  # K25,25行11列应付分保账款
            "InsuranceContractReserves_last": data.cell_value(25, 10),  # K26,26行11列保险合同准备金
            "ProxySecuProceeds_last": data.cell_value(26, 10),  # K27,27行11列代理买卖证券款
            "ReceivingsFromVicariouslySoldSecurities_last": data.cell_value(27, 10),  # K28,28行11列代理承销证券款
            "HoldLiabilitiesForSale_last": data.cell_value(28, 10),  # K29,29行11列持有待售负债
            "NonCurrentLiabilityInOneYear_last": data.cell_value(29, 10),  # K30,30行11列一年内到期的非流动负债
            "OtherCurrentLiabilities_last": data.cell_value(30, 10),  # K31,31行11列其他流动负债
            "TotalCurrentLiability_last": data.cell_value(31, 10),  # K32,32行11列流动负债合计
            "LongtermLoan_last": data.cell_value(33, 10),  # K34,34行11列长期借款
            "BondsPayable_last": data.cell_value(34, 10),  # K35,35行11列应付债券
            "PreferredSharesNoncurrent_last": data.cell_value(35, 10),  # K36,36行11列其中：优先股
            "PepertualLiabilityNoncurrent_last": data.cell_value(36, 10),  # K37,37行11列永续债
            "LongtermAccountPayable_last": data.cell_value(37, 10),  # K38,38行11列长期应付款
            "LongtermSalariesPayable_last": data.cell_value(38, 10),  # K39,39行11列长期应付职工薪酬
            "EstimateLiability_last": data.cell_value(39, 10),  # K40,40行11列预计负债
            "DeferredEarning_last": data.cell_value(40, 10),  # K41,41行11列递延收益
            "DeferredTaxLiability_last": data.cell_value(41, 10),  # K42,42行11列递延所得税负债
            "OtherNoncurrentLiabilities_last": data.cell_value(42, 10),  # K43,43行11列其他非流动负债
            "TotalNonCurrentLiability_last": data.cell_value(43, 10),  # K44,44行11列非流动负债合计
            "TotalLiability_last": data.cell_value(44, 10),  # K45,45行11列负债合计
            "TotalOwnerEquities_last": data.cell_value(46, 10),  # K47,47行11列股东权益合计
            "OtherComprehesiveIncome_last": data.cell_value(47, 10),  # K48,48行11列其他综合收益
            "TotalSheetOwnerEquities_last": data.cell_value(48, 10),  # K49,49行11列负债和股东权益合计


        }

        keyli = []
        valueli = []
        change = ChangeData()
        for key, value in dic.items():
            keys = key
            values = change.Changing(value)
            keyli.append(keys)
            valueli.append(values)
        dic = dict(zip(keyli, valueli))
        dic["ID"] = identify,  # 实例ID号
        dic["username"] = username, # 用户名
        df = pd.DataFrame(dic, index=[0])  # 打包成DataFram

        return df


    def CheckError(self, df):
        """
        资产负债表数据逻辑关系核对
        :param df:
        :return:
        """
        # 建立错误空列表：
        errorlist = []
        # 流动资产+非流动资产=总资产
        if abs(df["TotalCurrentAssets_this"].fillna(0).values + df["TotalNonCurrentAssets_this"].fillna(0).values - df["TotalAssets_this"].fillna(0).values) > 0.01:
            error = "资产负债表:本期流动资产+本期非流动资产<>本期总资产"
            errorlist.append(error)
        if abs(df["TotalCurrentAssets_last"].fillna(0).values + df["TotalNonCurrentAssets_last"].fillna(0).values - df["TotalAssets_last"].fillna(0).values) > 0.01:
            error = "资产负债表:上期流动资产+上期非流动资产<>上期总资产"
            errorlist.append(error)
        # 流动负债+非流动负债=总负债
        if abs(df["TotalCurrentLiability_this"].fillna(0).values + df["TotalNonCurrentLiability_this"].fillna(0).values - df["TotalLiability_this"].fillna(0).values) > 0.01:
            error = "资产负债表:本期流动负债+本期非流动负债<>本期总负债"
            errorlist.append(error)
        if abs(df["TotalCurrentLiability_last"].fillna(0).values + df["TotalNonCurrentLiability_last"].fillna(0).values - df["TotalLiability_last"].fillna(0).values) > 0.01:
            error = "资产负债表:上期流动负债+上期非流动负债<>上期总负债"
            errorlist.append(error)
        # 负债+所有者权益=总资产
        if abs(df["TotalLiability_this"].fillna(0).values + df["TotalOwnerEquities_this"].fillna(0).values - df["TotalAssets_this"].fillna(0).values) > 0.01:
            error = "资产负债表:本期负债总额+本期所有者权益<>本期总资产"
            errorlist.append(error)
        if abs(df["TotalLiability_last"].fillna(0).values + df["TotalOwnerEquities_last"].fillna(0).values - df["TotalAssets_last"].fillna(0).values) > 0.01:
            error = "资产负债表:上期负债总额+上期所有者权益<>上期总资产"
            errorlist.append(error)

        # if ...继续添加核对逻辑

        return df, errorlist







if __name__ == "__main__":
    d = GetBalanceSheet()
