
import pandas as pd
from ChosenAPI.DataImport.ChangeToNum import ChangeData



class GetCashFlow(object):
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
            "GoodsSaleAndServiceRenderCash_this": data.cell_value(7, 4),  # E8 8行5列    销售商品、提供劳务收到的现金
            "NetDepositIncrease_this": data.cell_value(8, 4),  # E9 9行5列    客户存款和同业存放款项净增加额
            "NetBorrowingFromCentralBank_this": data.cell_value(9, 4),  # E10 10行5列    向中央银行借款净增加额
            "NetBorrowingFromFinanceCo_this": data.cell_value(10, 4),  # E11 11行5列    向其他金融机构拆入资金净增加额
            "NetOriginalInsuranceCash_this": data.cell_value(11, 4),  # E12 12行5列    收到原保险合同保费取得的现金
            "NetCashReceivedFromReinsuranceBusiness_this": data.cell_value(12, 4),  # E13 13行5列    收到再保险业务现金净额
            "NetInsurerDepositInvestment_this": data.cell_value(13, 4),  # E14 14行5列    保户储金及投资款净增加额
            "NetDealTradingAssets_this": data.cell_value(14, 4),  # E15 15行5列    处置以公允价值计量且其变动计入当期损益的金融资产净增加额
            "InterestAndCommissionCashin_this": data.cell_value(15, 4),  # E16 16行5列    收取利息、手续费及佣金的现金
            "NetIncreaseInPlacements_this": data.cell_value(16, 4),  # E17 17行5列    拆入资金净增加额
            "NetBuyback_this": data.cell_value(17, 4),  # E18 18行5列    回购业务资金净增加额
            "TaxLevyRefund_this": data.cell_value(18, 4),  # E19 19行5列    收到的税费返还
            "OtherCashInRelatedOperate_this": data.cell_value(19, 4),  # E20 20行5列    收到其他与经营活动有关的现金
            "SubtotalOperateCashInflow_this": data.cell_value(20, 4),  # E21 21行5列    经营活动现金流入小计
            "GoodsAndServicesCashPaid_this": data.cell_value(21, 4),  # E22 22行5列    购买商品、接受劳务支付的现金
            "NetLoanAndAdvanceIncrease_this": data.cell_value(22, 4),  # E23 23行5列    客户贷款及垫款净增加额
            "NetDepositInCbAndIb_this": data.cell_value(23, 4),  # E24 24行5列    存放中央银行和同业款项净增加额
            "OriginalCompensationPaid_this": data.cell_value(24, 4),  # E25 25行5列    支付原保险合同赔付款项的现金
            "HandlingChargesAndCommission_this": data.cell_value(25, 4),  # E26 26行5列    支付利息、手续费及佣金的现金
            "PolicyDividendCashPaid_this": data.cell_value(26, 4),  # E27 27行5列    支付保单红利的现金
            "StaffBehalfPaid_this": data.cell_value(27, 4),  # E28 28行5列    支付给职工以及为职工支付的现金
            "TaxPayments_this": data.cell_value(28, 4),  # E29 29行5列    支付的各项税费
            "OtherOperateCashPaid_this": data.cell_value(29, 4),  # E30 30行5列    支付的其他与经营活动有关的现金
            "SubtotalOperateCashOutflow_this": data.cell_value(30, 4),  # E31 31行5列    经营活动现金流出小计
            "NetOperateCashFlow_this": data.cell_value(31, 4),  # E32 32行5列    经营活动产生的现金流量净额
            "InvestWithdrawalCash_this": data.cell_value(33, 4),  # E34 34行5列    收回投资收到的现金
            "InvestProceeds_this": data.cell_value(34, 4),  # E35 35行5列    取得投资收益收到的现金
            "FixIntanOtherAssetDispoCash_this": data.cell_value(35, 4),  # E36 36行5列    处置固定资产、无形资产和其他长期资产收回的现金净额
            "NetCashDealSubcompany_this": data.cell_value(36, 4),  # E37 37行5列    处置子公司及其他营业单位收到的现金净额
            "OtherCashInRelatedInvest_this": data.cell_value(37, 4),  # E38 38行5列    收到的其他与投资活动有关的现金
            "SubtotalInvestCashInflow_this": data.cell_value(38, 4),  # E39 39行5列    投资活动现金流入小计
            "FixIntanOtherAssetAcquiCash_this": data.cell_value(39, 4),  # E40 40行5列    购建固定资产、无形资产和其他长期资产支付的现金
            "InvestCashPaid_this": data.cell_value(40, 4),  # E41 41行5列    投资支付的现金
            "ImpawnedLoanNetIncrease_this": data.cell_value(41, 4),  # E42 42行5列    质押贷款净增加额
            "NetCashFromSubCompany_this": data.cell_value(42, 4),  # E43 43行5列    取得子公司及其他营业单位支付的现金净额
            "OtherInvestCashPaid_this": data.cell_value(43, 4),  # E44 44行5列    支付的其他与投资活动有关的现金
            "SubtotalInvestCashOutflow_this": data.cell_value(44, 4),  # E45 45行5列    投资活动现金流出小计
            "NetInvestCashFlow_this": data.cell_value(45, 4),  # E46 46行5列    投资活动产生的现金流量净额
            "CashFromInvest_this": data.cell_value(47, 4),  # E48 48行5列    吸收投资收到的现金
            "CashFromMinoSInvestSub_this": data.cell_value(48, 4),  # E49 49行5列    其中：子公司吸收少数股东投资收到的现金
            "CashFromBorrowing_this": data.cell_value(49, 4),  # E50 50行5列    取得借款收到的现金
            "CashFromBondsIssue_this": data.cell_value(50, 4),  # E51 51行5列    发行债券收到的现金
            "OtherCashInRelatedFinance_this": data.cell_value(51, 4),  # E52 52行5列    收到其他与筹资活动有关的现金
            "SubtotalFinanceCashInflow_this": data.cell_value(52, 4),  # E53 53行5列      筹资活动现金流入小计
            "BorrowingRepayment_this": data.cell_value(53, 4),  # E54 54行5列    偿还债务支付的现金
            "DividendInterestPayment_this": data.cell_value(54, 4),  # E55 55行5列    分配股利、利润或偿付利息支付的现金
            "ProceedsFromSubToMinoS_this": data.cell_value(55, 4),  # E56 56行5列    其中：子公司支付给少数股东的股利、利润
            "OtherFinanceCashPaid_this": data.cell_value(56, 4),  # E57 57行5列    支付的其他与筹资活动有关的现金
            "SubtotalFinanceCashOutflow_this": data.cell_value(57, 4),  # E58 58行5列      筹资活动现金流出小计
            "NetFinanceCashFlow_this": data.cell_value(58, 4),  # E59 59行5列    筹资活动产生的现金流量净额
            "ExchangeRateChangeEffect_this": data.cell_value(59, 4),  # E60 60行5列  汇率变动对现金及现金等价物的影响
            "CashEquivalentIncrease_this": data.cell_value(60, 4),  # E61 61行5列    现金及现金等价物净增加额
            "CashEquivalentsAtBeginning_this": data.cell_value(61, 4),  # E62 62行5列    加：年初现金及现金等价物余额
            "CashAndEquivalentsAtEnd_this": data.cell_value(62, 4),  # E63 63行5列    期末现金及现金等价物余额
            "GoodsSaleAndServiceRenderCash_last": data.cell_value(7, 5),  # E8 8行6列    销售商品、提供劳务收到的现金
            "NetDepositIncrease_last": data.cell_value(8, 5),  # E9 9行6列    客户存款和同业存放款项净增加额
            "NetBorrowingFromCentralBank_last": data.cell_value(9, 5),  # E10 10行6列    向中央银行借款净增加额
            "NetBorrowingFromFinanceCo_last": data.cell_value(10, 5),  # E11 11行6列    向其他金融机构拆入资金净增加额
            "NetOriginalInsuranceCash_last": data.cell_value(11, 5),  # E12 12行6列    收到原保险合同保费取得的现金
            "NetCashReceivedFromReinsuranceBusiness_last": data.cell_value(12, 5),  # E13 13行6列    收到再保险业务现金净额
            "NetInsurerDepositInvestment_last": data.cell_value(13, 5),  # E14 14行6列    保户储金及投资款净增加额
            "NetDealTradingAssets_last": data.cell_value(14, 5),  # E15 15行6列    处置以公允价值计量且其变动计入当期损益的金融资产净增加额
            "InterestAndCommissionCashin_last": data.cell_value(15, 5),  # E16 16行6列    收取利息、手续费及佣金的现金
            "NetIncreaseInPlacements_last": data.cell_value(16, 5),  # E17 17行6列    拆入资金净增加额
            "NetBuyback_last": data.cell_value(17, 5),  # E18 18行6列    回购业务资金净增加额
            "TaxLevyRefund_last": data.cell_value(18, 5),  # E19 19行6列    收到的税费返还
            "OtherCashInRelatedOperate_last": data.cell_value(19, 5),  # E20 20行6列    收到其他与经营活动有关的现金
            "SubtotalOperateCashInflow_last": data.cell_value(20, 5),  # E21 21行6列    经营活动现金流入小计
            "GoodsAndServicesCashPaid_last": data.cell_value(21, 5),  # E22 22行6列    购买商品、接受劳务支付的现金
            "NetLoanAndAdvanceIncrease_last": data.cell_value(22, 5),  # E23 23行6列    客户贷款及垫款净增加额
            "NetDepositInCbAndIb_last": data.cell_value(23, 5),  # E24 24行6列    存放中央银行和同业款项净增加额
            "OriginalCompensationPaid_last": data.cell_value(24, 5),  # E25 25行6列    支付原保险合同赔付款项的现金
            "HandlingChargesAndCommission_last": data.cell_value(25, 5),  # E26 26行6列    支付利息、手续费及佣金的现金
            "PolicyDividendCashPaid_last": data.cell_value(26, 5),  # E27 27行6列    支付保单红利的现金
            "StaffBehalfPaid_last": data.cell_value(27, 5),  # E28 28行6列    支付给职工以及为职工支付的现金
            "TaxPayments_last": data.cell_value(28, 5),  # E29 29行6列    支付的各项税费
            "OtherOperateCashPaid_last": data.cell_value(29, 5),  # E30 30行6列    支付的其他与经营活动有关的现金
            "SubtotalOperateCashOutflow_last": data.cell_value(30, 5),  # E31 31行6列    经营活动现金流出小计
            "NetOperateCashFlow_last": data.cell_value(31, 5),  # E32 32行6列    经营活动产生的现金流量净额
            "InvestWithdrawalCash_last": data.cell_value(33, 5),  # E34 34行6列    收回投资收到的现金
            "InvestProceeds_last": data.cell_value(34, 5),  # E35 35行6列    取得投资收益收到的现金
            "FixIntanOtherAssetDispoCash_last": data.cell_value(35, 5),  # E36 36行6列    处置固定资产、无形资产和其他长期资产收回的现金净额
            "NetCashDealSubcompany_last": data.cell_value(36, 5),  # E37 37行6列    处置子公司及其他营业单位收到的现金净额
            "OtherCashInRelatedInvest_last": data.cell_value(37, 5),  # E38 38行6列    收到的其他与投资活动有关的现金
            "SubtotalInvestCashInflow_last": data.cell_value(38, 5),  # E39 39行6列    投资活动现金流入小计
            "FixIntanOtherAssetAcquiCash_last": data.cell_value(39, 5),  # E40 40行6列    购建固定资产、无形资产和其他长期资产支付的现金
            "InvestCashPaid_last": data.cell_value(40, 5),  # E41 41行6列    投资支付的现金
            "ImpawnedLoanNetIncrease_last": data.cell_value(41, 5),  # E42 42行6列    质押贷款净增加额
            "NetCashFromSubCompany_last": data.cell_value(42, 5),  # E43 43行6列    取得子公司及其他营业单位支付的现金净额
            "OtherInvestCashPaid_last": data.cell_value(43, 5),  # E44 44行6列    支付的其他与投资活动有关的现金
            "SubtotalInvestCashOutflow_last": data.cell_value(44, 5),  # E45 45行6列    投资活动现金流出小计
            "NetInvestCashFlow_last": data.cell_value(45, 5),  # E46 46行6列    投资活动产生的现金流量净额
            "CashFromInvest_last": data.cell_value(47, 5),  # E48 48行6列    吸收投资收到的现金
            "CashFromMinoSInvestSub_last": data.cell_value(48, 5),  # E49 49行6列    其中：子公司吸收少数股东投资收到的现金
            "CashFromBorrowing_last": data.cell_value(49, 5),  # E50 50行6列    取得借款收到的现金
            "CashFromBondsIssue_last": data.cell_value(50, 5),  # E51 51行6列    发行债券收到的现金
            "OtherCashInRelatedFinance_last": data.cell_value(51, 5),  # E52 52行6列    收到其他与筹资活动有关的现金
            "SubtotalFinanceCashInflow_last": data.cell_value(52, 5),  # E53 53行6列      筹资活动现金流入小计
            "BorrowingRepayment_last": data.cell_value(53, 5),  # E54 54行6列    偿还债务支付的现金
            "DividendInterestPayment_last": data.cell_value(54, 5),  # E55 55行6列    分配股利、利润或偿付利息支付的现金
            "ProceedsFromSubToMinoS_last": data.cell_value(55, 5),  # E56 56行6列    其中：子公司支付给少数股东的股利、利润
            "OtherFinanceCashPaid_last": data.cell_value(56, 5),  # E57 57行6列    支付的其他与筹资活动有关的现金
            "SubtotalFinanceCashOutflow_last": data.cell_value(57, 5),  # E58 58行6列      筹资活动现金流出小计
            "NetFinanceCashFlow_last": data.cell_value(58, 5),  # E59 59行6列    筹资活动产生的现金流量净额
            "ExchangeRateChangeEffect_last": data.cell_value(59, 5),  # E60 60行6列  汇率变动对现金及现金等价物的影响
            "CashEquivalentIncrease_last": data.cell_value(60, 5),  # E61 61行6列    现金及现金等价物净增加额
            "CashEquivalentsAtBeginning_last": data.cell_value(61, 5),  # E62 62行6列    加：年初现金及现金等价物余额
            "CashAndEquivalentsAtEnd_last": data.cell_value(62, 5),  # E63 63行6列    期末现金及现金等价物余额

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
        dic["username"] = username,  # 用户名
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
        # 经营活动现金流入小计-经营活动现金流出小计=经营活动产生的现金流量净额
        if abs(df["SubtotalOperateCashInflow_this"].fillna(0).values - df["SubtotalOperateCashOutflow_this"].fillna(0).values - df["NetOperateCashFlow_this"].fillna(0).values) > 0.01:
            error = "现金流量表:本期经营活动现金流入小计-本期经营活动现金流出小计<>本期经营活动产生的现金流量净额"
            errorlist.append(error)
        if abs(df["SubtotalOperateCashInflow_last"].fillna(0).values - df["SubtotalOperateCashOutflow_last"].fillna(0).values - df["NetOperateCashFlow_last"].fillna(0).values) > 0.01:
            error = "现金流量表:上期经营活动现金流入小计-上期经营活动现金流出小计<>上期经营活动产生的现金流量净额"
            errorlist.append(error)
        # 投资活动现金流入小计-投资活动现金流出小计=投资活动产生的现金流量净额
        if abs(df["SubtotalInvestCashInflow_this"].fillna(0).values - df["SubtotalInvestCashOutflow_this"].fillna(0).values - df["NetInvestCashFlow_this"].fillna(0).values) > 0.01:
            error = "现金流量表:本期投资活动现金流入小计-本期投资活动现金流出小计<>本期投资活动产生的现金流量净额"
            errorlist.append(error)
        if abs(df["SubtotalInvestCashInflow_last"].fillna(0).values - df["SubtotalInvestCashOutflow_last"].fillna(0).values - df["NetInvestCashFlow_last"].fillna(0).values) > 0.01:
            error = "现金流量表:上期投资活动现金流入小计-上期投资活动现金流出小计<>上期投资活动产生的现金流量净额"
            errorlist.append(error)
        # 筹资活动现金流入小计-筹资活动现金流出小计=筹资活动产生的现金流量净额
        if abs(df["SubtotalFinanceCashInflow_this"].fillna(0).values - df["SubtotalFinanceCashOutflow_this"].fillna(0).values - df["NetFinanceCashFlow_this"].fillna(0).values) > 0.01:
            error = "现金流量表:本期筹资活动现金流入小计-本期筹资活动现金流出小计<>本期筹资活动产生的现金流量净额"
            errorlist.append(error)
        if abs(df["SubtotalFinanceCashInflow_last"].fillna(0).values - df["SubtotalFinanceCashOutflow_last"].fillna(0).values - df["NetFinanceCashFlow_last"].fillna(0).values) > 0.01:
            error = "现金流量表:上期筹资活动现金流入小计-上期筹资活动现金流出小计<>上期筹资活动产生的现金流量净额"
            errorlist.append(error)
        # 经营活动产生的现金流量净额+投资活动产生的现金流量净额+筹资活动产生的现金流量净额+汇率变动对现金及现金等价物的影响=现金及现金等价物净增加额
        if abs(df["NetOperateCashFlow_this"].fillna(0).values + df["NetInvestCashFlow_this"].fillna(0).values + df["NetFinanceCashFlow_this"].fillna(0).values + df["ExchangeRateChangeEffect_this"].fillna(0).values - df["CashEquivalentIncrease_this"].fillna(0).values) > 0.01:
            error = "现金流量表:本期经营活动产生的现金流量净额+本期投资活动产生的现金流量净额+本期筹资活动产生的现金流量净额+本期汇率变动对现金及现金等价物的影响<>本期现金及现金等价物净增加额"
            errorlist.append(error)
        if abs(df["NetOperateCashFlow_last"].fillna(0).values + df["NetInvestCashFlow_last"].fillna(0).values + df["NetFinanceCashFlow_last"].fillna(0).values + df["ExchangeRateChangeEffect_last"].fillna(0).values - df["CashEquivalentIncrease_last"].fillna(0).values) > 0.01:
            error = "现金流量表:上期经营活动产生的现金流量净额+上期投资活动产生的现金流量净额+上期筹资活动产生的现金流量净额+上期汇率变动对现金及现金等价物的影响<>上期现金及现金等价物净增加额"
            errorlist.append(error)
        # 现金及现金等价物净增加额+年初现金及现金等价物余额=期末现金及现金等价物余额
        if abs(df["CashEquivalentIncrease_this"].fillna(0).values + df["CashEquivalentsAtBeginning_this"].fillna(0).values - df["CashAndEquivalentsAtEnd_this"].fillna(0).values) > 0.01:
            error = "现金流量表:本期现金及现金等价物净增加额+本期年初现金及现金等价物余额<>本期期末现金及现金等价物余额"
            errorlist.append(error)
        if abs(df["CashEquivalentIncrease_last"].fillna(0).values + df["CashEquivalentsAtBeginning_last"].fillna(0).values - df["CashAndEquivalentsAtEnd_last"].fillna(0).values) > 0.01:
            error = "现金流量表:上期现金及现金等价物净增加额+上期年初现金及现金等价物余额<>上期期末现金及现金等价物余额"
            errorlist.append(error)

        return df, errorlist




if __name__ == "__main__":
    d = GetCashFlow()