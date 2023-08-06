
import pandas as pd
from ChosenAPI.DataImport.ChangeToNum import ChangeData



class GetHoldAssetsForSale(object):#持有待售资产
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
            "HoldAssetsForSale_Project1_EndingBookValue": data.cell_value(3, 1),  # B4 4行2列项目1期末账面价值
            "HoldAssetsForSale_Project2_EndingBookValue": data.cell_value(4, 1),  # B5 5行2列项目2期末账面价值
            "HoldAssetsForSale_Project3_EndingBookValue": data.cell_value(5, 1),  # B6 6行2列项目3期末账面价值
            "HoldAssetsForSale_Project4_EndingBookValue": data.cell_value(6, 1),  # B7 7行2列项目4期末账面价值
            "HoldAssetsForSale_Project5_EndingBookValue": data.cell_value(7, 1),  # B8 8行2列项目5期末账面价值
            "HoldAssetsForSale_Project6_EndingBookValue": data.cell_value(8, 1),  # B9 9行2列项目6期末账面价值
            "HoldAssetsForSale_Project7_EndingBookValue": data.cell_value(9, 1),  # B10 10行2列项目7期末账面价值
            "HoldAssetsForSale_Project8_EndingBookValue": data.cell_value(10, 1),  # B11 11行2列项目8期末账面价值
            "HoldAssetsForSale_Project9_EndingBookValue": data.cell_value(11, 1),  # B12 12行2列项目9期末账面价值
            "HoldAssetsForSale_Project10_EndingBookValue": data.cell_value(12, 1),  # B13 13行2列项目10期末账面价值
            "HoldAssetsForSale_Total_EndingBookValue": data.cell_value(13, 1),  # B14 14行2列合计期末账面价值
            "HoldAssetsForSale_Project1_FairValue": data.cell_value(3, 2),  # C4 4行3列项目1公允价值
            "HoldAssetsForSale_Project2_FairValue": data.cell_value(4, 2),  # C5 5行3列项目2公允价值
            "HoldAssetsForSale_Project3_FairValue": data.cell_value(5, 2),  # C6 6行3列项目3公允价值
            "HoldAssetsForSale_Project4_FairValue": data.cell_value(6, 2),  # C7 7行3列项目4公允价值
            "HoldAssetsForSale_Project5_FairValue": data.cell_value(7, 2),  # C8 8行3列项目5公允价值
            "HoldAssetsForSale_Project6_FairValue": data.cell_value(8, 2),  # C9 9行3列项目6公允价值
            "HoldAssetsForSale_Project7_FairValue": data.cell_value(9, 2),  # C10 10行3列项目7公允价值
            "HoldAssetsForSale_Project8_FairValue": data.cell_value(10, 2),  # C11 11行3列项目8公允价值
            "HoldAssetsForSale_Project9_FairValue": data.cell_value(11, 2),  # C12 12行3列项目9公允价值
            "HoldAssetsForSale_Project10_FairValue": data.cell_value(12, 2),  # C13 13行3列项目10公允价值
            "HoldAssetsForSale_Total_FairValue": data.cell_value(13, 2),  # C14 14行3列合计公允价值
            "HoldAssetsForSale_Project1_EstimatedDisposalCost": data.cell_value(3, 3),  # D4 4行4列项目1预计处置费用
            "HoldAssetsForSale_Project2_EstimatedDisposalCost": data.cell_value(4, 3),  # D5 5行4列项目2预计处置费用
            "HoldAssetsForSale_Project3_EstimatedDisposalCost": data.cell_value(5, 3),  # D6 6行4列项目3预计处置费用
            "HoldAssetsForSale_Project4_EstimatedDisposalCost": data.cell_value(6, 3),  # D7 7行4列项目4预计处置费用
            "HoldAssetsForSale_Project5_EstimatedDisposalCost": data.cell_value(7, 3),  # D8 8行4列项目5预计处置费用
            "HoldAssetsForSale_Project6_EstimatedDisposalCost": data.cell_value(8, 3),  # D9 9行4列项目6预计处置费用
            "HoldAssetsForSale_Project7_EstimatedDisposalCost": data.cell_value(9, 3),  # D10 10行4列项目7预计处置费用
            "HoldAssetsForSale_Project8_EstimatedDisposalCost": data.cell_value(10, 3),  # D11 11行4列项目8预计处置费用
            "HoldAssetsForSale_Project9_EstimatedDisposalCost": data.cell_value(11, 3),  # D12 12行4列项目9预计处置费用
            "HoldAssetsForSale_Project10_EstimatedDisposalCost": data.cell_value(12, 3),  # D13 13行4列项目10预计处置费用
            "HoldAssetsForSale_Total_EstimatedDisposalCost": data.cell_value(13, 3),  # D14 14行4列合计预计处置费用
            "HoldAssetsForSale_Project1_RelatedCumulativeAmount": data.cell_value(3, 4),  # E4 4行5列项目1与之相关的其他综合收益累计金额
            "HoldAssetsForSale_Project2_RelatedCumulativeAmount": data.cell_value(4, 4),  # E5 5行5列项目2与之相关的其他综合收益累计金额
            "HoldAssetsForSale_Project3_RelatedCumulativeAmount": data.cell_value(5, 4),  # E6 6行5列项目3与之相关的其他综合收益累计金额
            "HoldAssetsForSale_Project4_RelatedCumulativeAmount": data.cell_value(6, 4),  # E7 7行5列项目4与之相关的其他综合收益累计金额
            "HoldAssetsForSale_Project5_RelatedCumulativeAmount": data.cell_value(7, 4),  # E8 8行5列项目5与之相关的其他综合收益累计金额
            "HoldAssetsForSale_Project6_RelatedCumulativeAmount": data.cell_value(8, 4),  # E9 9行5列项目6与之相关的其他综合收益累计金额
            "HoldAssetsForSale_Project7_RelatedCumulativeAmount": data.cell_value(9, 4),# E10 10行5列项目7与之相关的其他综合收益累计金额
            "HoldAssetsForSale_Project8_RelatedCumulativeAmount": data.cell_value(10, 4),# E11 11行5列项目8与之相关的其他综合收益累计金额
            "HoldAssetsForSale_Project9_RelatedCumulativeAmount": data.cell_value(11, 4),# E12 12行5列项目9与之相关的其他综合收益累计金额
            "HoldAssetsForSale_Project10_RelatedCumulativeAmount": data.cell_value(12, 4),# E13 13行5列项目10与之相关的其他综合收益累计金额
            "HoldAssetsForSale_Total_RelatedCumulativeAmount": data.cell_value(13, 4),  # E14 14行5列合计与之相关的其他综合收益累计金额


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
        dic["HoldAssetsForSale_Remark"] = data.cell_value(15, 1),  # B16 16行2列说明
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
        # 期末账面价值：项目1+项目2+项目3+项目4+项目5+项目6+项目7+项目8+项目9+项目10=合计
        if abs(df["HoldAssetsForSale_Project1_EndingBookValue"].fillna(0).values + df["HoldAssetsForSale_Project2_EndingBookValue"].fillna(0).values + df["HoldAssetsForSale_Project3_EndingBookValue"].fillna(0).values + df["HoldAssetsForSale_Project4_EndingBookValue"].fillna(0).values + df["HoldAssetsForSale_Project5_EndingBookValue"].fillna(0).values + df["HoldAssetsForSale_Project6_EndingBookValue"].fillna(0).values + df["HoldAssetsForSale_Project7_EndingBookValue"].fillna(0).values + df["HoldAssetsForSale_Project8_EndingBookValue"].fillna(0).values + df["HoldAssetsForSale_Project9_EndingBookValue"].fillna(0).values + df["HoldAssetsForSale_Project10_EndingBookValue"].fillna(0).values - df["HoldAssetsForSale_Total_EndingBookValue"].fillna(0).values) > 0.01:
            error = "期末账面价值：项目1+项目2+项目3+项目4+项目5+项目6+项目7+项目8+项目9+项目10<>合计"
            errorlist.append(error)
            # 公允价值：项目1+项目2+项目3+项目4+项目5+项目6+项目7+项目8+项目9+项目10=合计
        if abs(df["HoldAssetsForSale_Project1_FairValue"].fillna(0).values + df["HoldAssetsForSale_Project2_FairValue"].fillna(0).values + df["HoldAssetsForSale_Project3_FairValue"].fillna(0).values + df["HoldAssetsForSale_Project4_FairValue"].fillna(0).values + df["HoldAssetsForSale_Project5_FairValue"].fillna(0).values + df["HoldAssetsForSale_Project6_FairValue"].fillna(0).values + df["HoldAssetsForSale_Project7_FairValue"].fillna(0).values + df["HoldAssetsForSale_Project8_FairValue"].fillna(0).values + df["HoldAssetsForSale_Project9_FairValue"].fillna(0).values + df["HoldAssetsForSale_Project10_FairValue"].fillna(0).values - df["HoldAssetsForSale_Total_FairValue"].fillna(0).values) > 0.01:
            error = "公允价值：项目1+项目2+项目3+项目4+项目5+项目6+项目7+项目8+项目9+项目10<>合计"
            errorlist.append(error)
            # 预计处置费用：项目1+项目2+项目3+项目4+项目5+项目6+项目7+项目8+项目9+项目10=合计
        if abs(df["HoldAssetsForSale_Project1_EstimatedDisposalCost"].fillna(0).values + df["HoldAssetsForSale_Project2_EstimatedDisposalCost"].fillna(0).values + df["HoldAssetsForSale_Project3_EstimatedDisposalCost"].fillna(0).values + df["HoldAssetsForSale_Project4_EstimatedDisposalCost"].fillna(0).values + df["HoldAssetsForSale_Project5_EstimatedDisposalCost"].fillna(0).values + df["HoldAssetsForSale_Project6_EstimatedDisposalCost"].fillna(0).values + df["HoldAssetsForSale_Project7_EstimatedDisposalCost"].fillna(0).values + df["HoldAssetsForSale_Project8_EstimatedDisposalCost"].fillna(0).values + df["HoldAssetsForSale_Project9_EstimatedDisposalCost"].fillna(0).values + df["HoldAssetsForSale_Project10_EstimatedDisposalCost"].fillna(0).values - df["HoldAssetsForSale_Total_EstimatedDisposalCost"].fillna(0).values) > 0.01:
            error = "预计处置费用：项目1+项目2+项目3+项目4+项目5+项目6+项目7+项目8+项目9+项目10<>合计"
            errorlist.append(error)
            # 与之相关的其他综合收益累计金额：项目1+项目2+项目3+项目4+项目5+项目6+项目7+项目8+项目9+项目10=合计
        if abs(df["HoldAssetsForSale_Project1_RelatedCumulativeAmount"].fillna(0).values + df["HoldAssetsForSale_Project2_RelatedCumulativeAmount"].fillna(0).values + df["HoldAssetsForSale_Project3_RelatedCumulativeAmount"].fillna(0).values + df["HoldAssetsForSale_Project4_RelatedCumulativeAmount"].fillna(0).values + df["HoldAssetsForSale_Project5_RelatedCumulativeAmount"].fillna(0).values + df["HoldAssetsForSale_Project6_RelatedCumulativeAmount"].fillna(0).values + df["HoldAssetsForSale_Project7_RelatedCumulativeAmount"].fillna(0).values + df["HoldAssetsForSale_Project8_RelatedCumulativeAmount"].fillna(0).values + df["HoldAssetsForSale_Project9_RelatedCumulativeAmount"].fillna(0).values + df["HoldAssetsForSale_Project10_RelatedCumulativeAmount"].fillna(0).values - df["HoldAssetsForSale_Total_RelatedCumulativeAmount"].fillna(0).values) > 0.01:
            error = "与之相关的其他综合收益累计金额：项目1+项目2+项目3+项目4+项目5+项目6+项目7+项目8+项目9+项目10<>合计"
            errorlist.append(error)











        return df, errorlist


if __name__ == "__main__":
    d = GetHoldAssetsForSale()