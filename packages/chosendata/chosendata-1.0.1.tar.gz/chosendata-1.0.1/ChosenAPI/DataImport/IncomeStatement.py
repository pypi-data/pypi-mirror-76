
import pandas as pd
from ChosenAPI.DataImport.ChangeToNum import ChangeData



class GetIncomeStatement(object):
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
            "TotalOperatingRevenue_this": data.cell_value(6, 3),  # D7 7行4列    营业总收入
            "OperatingRevenue_this": data.cell_value(7, 3),  # D8 8行4列    其中：营业收入
            "InterestIncome_TotalOperatingRevenue_this": data.cell_value(8, 3),  # D9 9行4列          利息收入
            "PremiumsEarned_this": data.cell_value(9, 3),  # D10 10行4列          已赚保费
            "CommissionIncome_this": data.cell_value(10, 3),  # D11 11行4列          手续费及佣金收入
            "TotalOperatingCost_this": data.cell_value(11, 3),  # D12 12行4列    营业总成本
            "OperatingCost_this": data.cell_value(12, 3),  # D13 13行4列    其中：营业成本
            "InterestExpense_this": data.cell_value(13, 3),  # D14 14行4列          利息支出
            "CommissionExpense_this": data.cell_value(14, 3),  # D15 15行4列          手续费及佣金支出
            "RefundedPremiums_this": data.cell_value(15, 3),  # D16 16行4列          退保金
            "NetPayInsuranceClaims_this": data.cell_value(16, 3),  # D17 17行4列          赔付支出净额
            "WithdrawInsuranceContractReserve_this": data.cell_value(17, 3),  # D18 18行4列          提取保险合同准备金净额
            "PolicyDividendPayout_this": data.cell_value(18, 3),  # D19 19行4列          保单红利支出
            "ReinsuranceCost_this": data.cell_value(19, 3),  # D20 20行4列          分保费用
            "OperatingTaxSurcharges_this": data.cell_value(20, 3),  # D21 21行4列          税金及附加
            "SaleExpense_this": data.cell_value(21, 3),  # D22 22行4列          销售费用
            "AdministrationExpense_this": data.cell_value(22, 3),  # D23 23行4列          管理费用
            "RdExpenses_this": data.cell_value(23, 3),  # D24 24行4列          研发费用
            "FinancialExpense_this": data.cell_value(24, 3),  # D25 25行4列          财务费用
            "InterestCharges_this": data.cell_value(25, 3),  # D26 26行4列          其中：利息费用
            "InterestIncome_this": data.cell_value(26, 3),  # D27 27行4列                利息收入
            "AssetImpairmentLoss_this": data.cell_value(27, 3),  # D28 28行4列          资产减值损失
            "OtherEarnings_this": data.cell_value(28, 3),  # D29 29行4列      加：其他收益
            "InvestmentIncome_this": data.cell_value(29, 3),  # D30 30行4列          投资收益
            "InvestIncomeAssociates_this": data.cell_value(30, 3),  # D31 31行4列          其中：对联营企业和合营企业的投资收益
            "FairValueVariableIncome_this": data.cell_value(31, 3),  # D32 32行4列          公允价值变动收益
            "ExchangeIncome_this": data.cell_value(32, 3),  # D33 33行4列          汇兑收益
            "AssetDealIncome_this": data.cell_value(33, 3),  # D34 34行4列          资产处置收益
            "OperatingProfit_this": data.cell_value(34, 3),  # D35 35行4列    营业利润
            "NonOperatingRevenue_this": data.cell_value(35, 3),  # D36 36行4列      加：营业外收入
            "NonOperatingExpense_this": data.cell_value(36, 3),  # D37 37行4列      减：营业外支出
            "TotalProfit_this": data.cell_value(37, 3),  # D38 38行4列    利润总额
            "IncomeTax_this": data.cell_value(38, 3),  # D39 39行4列      减：所得税费用
            "NetProfit_this": data.cell_value(39, 3),  # D40 40行4列    净利润
            "NetProfitFromGoingConcern_this": data.cell_value(40, 3),  # D41 41行4列    持续经营净利润
            "NetProfitAfterOperation_this": data.cell_value(41, 3),  # D42 42行4列    终止经营净利润
            "NpParentCompanyOwners_this": data.cell_value(42, 3),  # D43 43行4列    归属于母公司所有者的净利润
            "MinorityProfit_this": data.cell_value(43, 3),  # D44 44行4列    少数股东损益
            "NetAfterTaxOfOtherComprehensiveIncome_this": data.cell_value(44, 3),  # D45 45行4列    其他综合收益的税后净额
            "TotalCompositeIncome_this": data.cell_value(60, 3),  # D61 61行4列    综合收益总额
            "CiParentCompanyOwners_this": data.cell_value(61, 3),  # D62 62行4列    归属于母公司所有者的综合收益总额
            "CiMinorityOwners_this": data.cell_value(62, 3),  # D63 63行4列    归属于少数股东的综合收益总额
            "TotalOperatingRevenue_last": data.cell_value(6, 4),  # D7 7行5列    营业总收入
            "OperatingRevenue_last": data.cell_value(7, 4),  # D8 8行5列    其中：营业收入
            "InterestIncome_TotalOperatingRevenue_last": data.cell_value(8, 4),  # D9 9行5列          利息收入
            "PremiumsEarned_last": data.cell_value(9, 4),  # D10 10行5列          已赚保费
            "CommissionIncome_last": data.cell_value(10, 4),  # D11 11行5列          手续费及佣金收入
            "TotalOperatingCost_last": data.cell_value(11, 4),  # D12 12行5列    营业总成本
            "OperatingCost_last": data.cell_value(12, 4),  # D13 13行5列    其中：营业成本
            "InterestExpense_last": data.cell_value(13, 4),  # D14 14行5列          利息支出
            "CommissionExpense_last": data.cell_value(14, 4),  # D15 15行5列          手续费及佣金支出
            "RefundedPremiums_last": data.cell_value(15, 4),  # D16 16行5列          退保金
            "NetPayInsuranceClaims_last": data.cell_value(16, 4),  # D17 17行5列          赔付支出净额
            "WithdrawInsuranceContractReserve_last": data.cell_value(17, 4),  # D18 18行5列          提取保险合同准备金净额
            "PolicyDividendPayout_last": data.cell_value(18, 4),  # D19 19行5列          保单红利支出
            "ReinsuranceCost_last": data.cell_value(19, 4),  # D20 20行5列          分保费用
            "OperatingTaxSurcharges_last": data.cell_value(20, 4),  # D21 21行5列          税金及附加
            "SaleExpense_last": data.cell_value(21, 4),  # D22 22行5列          销售费用
            "AdministrationExpense_last": data.cell_value(22, 4),  # D23 23行5列          管理费用
            "RdExpenses_last": data.cell_value(23, 4),  # D24 24行5列          研发费用
            "FinancialExpense_last": data.cell_value(24, 4),  # D25 25行5列          财务费用
            "InterestCharges_last": data.cell_value(25, 4),  # D26 26行5列          其中：利息费用
            "InterestIncome_last": data.cell_value(26, 4),  # D27 27行5列                利息收入
            "AssetImpairmentLoss_last": data.cell_value(27, 4),  # D28 28行5列          资产减值损失
            "OtherEarnings_last": data.cell_value(28, 4),  # D29 29行5列      加：其他收益
            "InvestmentIncome_last": data.cell_value(29, 4),  # D30 30行5列          投资收益
            "InvestIncomeAssociates_last": data.cell_value(30, 4),  # D31 31行5列          其中：对联营企业和合营企业的投资收益
            "FairValueVariableIncome_last": data.cell_value(31, 4),  # D32 32行5列          公允价值变动收益
            "ExchangeIncome_last": data.cell_value(32, 4),  # D33 33行5列          汇兑收益
            "AssetDealIncome_last": data.cell_value(33, 4),  # D34 34行5列          资产处置收益
            "OperatingProfit_last": data.cell_value(34, 4),  # D35 35行5列    营业利润
            "NonOperatingRevenue_last": data.cell_value(35, 4),  # D36 36行5列      加：营业外收入
            "NonOperatingExpense_last": data.cell_value(36, 4),  # D37 37行5列      减：营业外支出
            "TotalProfit_last": data.cell_value(37, 4),  # D38 38行5列    利润总额
            "IncomeTax_last": data.cell_value(38, 4),  # D39 39行5列      减：所得税费用
            "NetProfit_last": data.cell_value(39, 4),  # D40 40行5列    净利润
            "NetProfitFromGoingConcern_last": data.cell_value(40, 4),  # D41 41行5列    持续经营净利润
            "NetProfitAfterOperation_last": data.cell_value(41, 4),  # D42 42行5列    终止经营净利润
            "NpParentCompanyOwners_last": data.cell_value(42, 4),  # D43 43行5列    归属于母公司所有者的净利润
            "MinorityProfit_last": data.cell_value(43, 4),  # D44 44行5列    少数股东损益
            "NetAfterTaxOfOtherComprehensiveIncome_last": data.cell_value(44, 4),  # D45 45行5列    其他综合收益的税后净额
            "TotalCompositeIncome_last": data.cell_value(60, 4),  # D61 61行5列    综合收益总额
            "CiParentCompanyOwners_last": data.cell_value(61, 4),  # D62 62行5列    归属于母公司所有者的综合收益总额
            "CiMinorityOwners_last": data.cell_value(62, 4),  # D63 63行5列    归属于少数股东的综合收益总额

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
        # 营业收入+利息收入+已赚保费+手续费及佣金收入=营业总收入
        if abs(df["OperatingRevenue_this"].fillna(0).values + df["InterestIncome_TotalOperatingRevenue_this"].fillna(0).values + df["PremiumsEarned_this"].fillna(0).values + df["CommissionIncome_this"].fillna(0).values - df["TotalOperatingRevenue_this"].fillna(0).values) > 0.01:
            error = "利润表:本期营业收入+本期利息收入+本期已赚保费+本期手续费及佣金收入<>本期营业总收入"
            errorlist.append(error)
        if abs(df["OperatingRevenue_last"].fillna(0).values + df["InterestIncome_TotalOperatingRevenue_last"].fillna(0).values + df["PremiumsEarned_last"].fillna(0).values + df["CommissionIncome_last"].fillna(0).values - df["TotalOperatingRevenue_last"].fillna(0).values) > 0.01:
            error = "利润表:上期营业收入+上期利息收入+上期已赚保费+上期手续费及佣金收入<>上期营业总收入"
            errorlist.append(error)
        # 营业成本+利息支出+手续费及佣金支出+退保金+赔付支出净额+提取保险合同准备金净额+保单红利支出+分保费用+税金及附加+销售费用+管理费用+研发费用+财务费用+资产减值损失=营业总成本
        if abs(df["OperatingCost_this"].fillna(0).values + df["InterestExpense_this"].fillna(0).values + df["CommissionExpense_this"].fillna(0).values + df["RefundedPremiums_this"].fillna(0).values + df["NetPayInsuranceClaims_this"].fillna(0).values + df["WithdrawInsuranceContractReserve_this"].fillna(0).values + df["PolicyDividendPayout_this"].fillna(0).values + df["ReinsuranceCost_this"].fillna(0).values + df["OperatingTaxSurcharges_this"].fillna(0).values + df["SaleExpense_this"].fillna(0).values + df["AdministrationExpense_this"].fillna(0).values + df["RdExpenses_this"].fillna(0).values + df["FinancialExpense_this"].fillna(0).values + df["AssetImpairmentLoss_this"].fillna(0).values - df["TotalOperatingCost_this"].fillna(0).values) > 0.01:
            error = "利润表:本期营业成本+本期利息支出+本期手续费及佣金支出+本期退保金+本期赔付支出净额+本期提取保险合同准备金净额+本期保单红利支出+本期分保费用+本期税金及附++本期管理费用+本期研发费用+本期财务费用+本期资产减值损失+本期<>本期营业总成本"
            errorlist.append(error)
        if abs(df["OperatingCost_last"].fillna(0).values + df["InterestExpense_last"].fillna(0).values + df["CommissionExpense_last"].fillna(0).values + df["RefundedPremiums_last"].fillna(0).values + df["NetPayInsuranceClaims_last"].fillna(0).values + df["WithdrawInsuranceContractReserve_last"].fillna(0).values + df["PolicyDividendPayout_last"].fillna(0).values + df["ReinsuranceCost_last"].fillna(0).values + df["OperatingTaxSurcharges_last"].fillna(0).values + df["SaleExpense_last"].fillna(0).values + df["AdministrationExpense_last"].fillna(0).values + df["RdExpenses_last"].fillna(0).values + df["FinancialExpense_last"].fillna(0).values + df["AssetImpairmentLoss_last"].fillna(0).values - df["TotalOperatingCost_last"].fillna(0).values) > 0.01:
            error = "利润表:上期营业成本+上期利息支出+上期手续费及佣金支出+上期退保金+上期赔付支出净额+上期提取保险合同准备金净额+上期保单红利支出+上期分保费用+上期税金及附++上期管理费用+上期研发费用+上期财务费用+上期资产减值损失+上期<>上期营业总成本"
            errorlist.append(error)
        # 营业总收入-营业总成本+（其他收益+投资收益+公允价值变动收益+汇兑收益+资产处置收益)=营业利润
        if abs(df["TotalOperatingRevenue_this"].fillna(0).values - df["TotalOperatingCost_this"].fillna(0).values + df["OtherEarnings_this"].fillna(0).values + df["InvestmentIncome_this"].fillna(0).values + df["FairValueVariableIncome_this"].fillna(0).values + df["ExchangeIncome_this"].fillna(0).values + df["AssetDealIncome_this"].fillna(0).values - df["OperatingProfit_this"].fillna(0).values) > 0.01:
            error = "利润表:本期营业总收入-本期总成本+本期其他收益+本期投资收益+公允价值变动收益+本期汇兑收益+本期资产处置收益<>本期营业利润"
            errorlist.append(error)
        if abs(df["TotalOperatingRevenue_last"].fillna(0).values - df["TotalOperatingCost_last"].fillna(0).values + df["OtherEarnings_last"].fillna(0).values + df["InvestmentIncome_last"].fillna(0).values + df["FairValueVariableIncome_last"].fillna(0).values + df["ExchangeIncome_last"].fillna(0).values + df["AssetDealIncome_last"].fillna(0).values - df["OperatingProfit_last"].fillna(0).values) > 0.01:
            error = "利润表:上期营业总收入-上期总成本+本期其他收益+上期投资收益+公允价值变动收益+上期汇兑收益+上期资产处置收益<>上期营业利润"
            errorlist.append(error)
        # 营业利润+营业外收入-营业外支出=利润总额
        if abs(df["OperatingProfit_this"].fillna(0).values + df["NonOperatingRevenue_this"].fillna(0).values - df["NonOperatingExpense_this"].fillna(0).values - df["TotalProfit_this"].fillna(0).values) > 0.01:
            error = "利润表:本期营业利润+本期营业外收入-本期营业外支出<>本期利润总额"
            errorlist.append(error)
        if abs(df["OperatingProfit_last"].fillna(0).values + df["NonOperatingRevenue_last"].fillna(0).values - df["NonOperatingExpense_last"].fillna(0).values - df["TotalProfit_last"].fillna(0).values) > 0.01:
            error = "利润表:上期营业利润+上期营业外收入-上期营业外支出<>上期利润总额"
            errorlist.append(error)
        # 利润总额-所得税费用=净利润
        if abs(df["TotalProfit_this"].fillna(0).values - df["IncomeTax_this"].fillna(0).values - df["NetProfit_this"].fillna(0).values) > 0.01:
            error = "利润表:本期利润总额-本期所得税费用<>本期净利润"
            errorlist.append(error)
        if abs(df["TotalProfit_last"].fillna(0).values - df["IncomeTax_last"].fillna(0).values - df["NetProfit_last"].fillna(0).values) > 0.01:
            error = "利润表:上期利润总额-上期所得税费用<>上期净利润"
            errorlist.append(error)

        return df, errorlist


if __name__ == "__main__":
    d = GetIncomeStatement()