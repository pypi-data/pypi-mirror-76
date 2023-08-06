
import pandas as pd
from ChosenAPI.DataImport.ChangeToNum import ChangeData



class GetAssetImpairmentLoss(object):#资产减值损失
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
            "AssetImpairmentLoss_AccountReceivable_CurrentPeriod": data.cell_value(2, 1),  # B3 3行2列⑴坏账损失本期发生额
            "AssetImpairmentLoss_Inventories_CurrentPeriod": data.cell_value(3, 1),  # B4 4行2列⑵存货跌价损失本期发生额
            "AssetImpairmentLoss_HoldForSaleAssets_CurrentPeriod": data.cell_value(4, 1),  # B5 5行2列⑶可供出售金融资产减值损失本期发生额
            "AssetImpairmentLoss_HoldToMaturityInvestments_CurrentPeriod": data.cell_value(5, 1),# B6 6行2列⑷持有至到期投资减值损失本期发生额
            "AssetImpairmentLoss_LongtermEquityInvest_CurrentPeriod": data.cell_value(6, 1),# B7 7行2列⑸长期股权投资减值损失本期发生额
            "AssetImpairmentLoss_InvestmentProperty_CurrentPeriod": data.cell_value(7, 1),  # B8 8行2列⑹投资性房地产减值损失本期发生额
            "AssetImpairmentLoss_FixedAssets_CurrentPeriod": data.cell_value(8, 1),  # B9 9行2列⑺固定资产减值损失本期发生额
            "AssetImpairmentLoss_ConstructionMaterials_CurrentPeriod": data.cell_value(9, 1),# B10 10行2列⑻工程物资减值损失本期发生额
            "AssetImpairmentLoss_ConstruInProcess_CurrentPeriod": data.cell_value(10, 1),  # B11 11行2列⑼在建工程减值损失本期发生额
            "AssetImpairmentLoss_BiologicalAssets_CurrentPeriod": data.cell_value(11, 1),# B12 12行2列⑽生产性生物资产减值损失本期发生额
            "AssetImpairmentLoss_IntangibleAssets_CurrentPeriod": data.cell_value(12, 1),  # B13 13行2列⑾无形资产减值损失本期发生额
            "AssetImpairmentLoss_GoodWill_CurrentPeriod": data.cell_value(13, 1),  # B14 14行2列⑿商誉减值损失本期发生额
            "AssetImpairmentLoss_Other_CurrentPeriod": data.cell_value(14, 1),  # B15 15行2列⒀其他本期发生额
            "AssetImpairmentLoss_Total_CurrentPeriod": data.cell_value(15, 1),  # B16 16行2列合计本期发生额
            "AssetImpairmentLoss_AccountReceivable_PriorPeriod": data.cell_value(2, 2),  # C3 3行3列⑴坏账损失上期发生额
            "AssetImpairmentLoss_Inventories_PriorPeriod": data.cell_value(3, 2),  # C4 4行3列⑵存货跌价损失上期发生额
            "AssetImpairmentLoss_HoldForSaleAssets_PriorPeriod": data.cell_value(4, 2),  # C5 5行3列⑶可供出售金融资产减值损失上期发生额
            "AssetImpairmentLoss_HoldToMaturityInvestments_PriorPeriod": data.cell_value(5, 2),# C6 6行3列⑷持有至到期投资减值损失上期发生额
            "AssetImpairmentLoss_LongtermEquityInvest_PriorPeriod": data.cell_value(6, 2),  # C7 7行3列⑸长期股权投资减值损失上期发生额
            "AssetImpairmentLoss_InvestmentProperty_PriorPeriod": data.cell_value(7, 2),  # C8 8行3列⑹投资性房地产减值损失上期发生额
            "AssetImpairmentLoss_FixedAssets_PriorPeriod": data.cell_value(8, 2),  # C9 9行3列⑺固定资产减值损失上期发生额
            "AssetImpairmentLoss_ConstructionMaterials_PriorPeriod": data.cell_value(9, 2),  # C10 10行3列⑻工程物资减值损失上期发生额
            "AssetImpairmentLoss_ConstruInProcess_PriorPeriod": data.cell_value(10, 2),  # C11 11行3列⑼在建工程减值损失上期发生额
            "AssetImpairmentLoss_BiologicalAssets_PriorPeriod": data.cell_value(11, 2),  # C12 12行3列⑽生产性生物资产减值损失上期发生额
            "AssetImpairmentLoss_IntangibleAssets_PriorPeriod": data.cell_value(12, 2),  # C13 13行3列⑾无形资产减值损失上期发生额
            "AssetImpairmentLoss_GoodWill_PriorPeriod": data.cell_value(13, 2),  # C14 14行3列⑿商誉减值损失上期发生额
            "AssetImpairmentLoss_Other_PriorPeriod": data.cell_value(14, 2),  # C15 15行3列⒀其他上期发生额
            "AssetImpairmentLoss_Total_PriorPeriod": data.cell_value(15, 2),  # C16 16行3列合计上期发生额


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
        dic["AssetImpairmentLoss_Remark"] = data.cell_value(17, 1),  # B18 18行2列说明]
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
        # 本期发生额:坏账损失+存货跌价损失+可供出售金融资产减值损失+持有至到期投资减值损失+长期股权投资减值损失+投资性房地产减值损失+固定资产减值损失+工程物资减值损失+在建工程减值损失+生产性生物资产减值损失+无形资产减值损失+商誉减值损失+其他=合计
        if abs(df["AssetImpairmentLoss_AccountReceivable_CurrentPeriod"].fillna(0).values + df["AssetImpairmentLoss_Inventories_CurrentPeriod"].fillna(0).values + df["AssetImpairmentLoss_HoldForSaleAssets_CurrentPeriod"].fillna(0).values + df["AssetImpairmentLoss_HoldToMaturityInvestments_CurrentPeriod"].fillna(0).values + df["AssetImpairmentLoss_LongtermEquityInvest_CurrentPeriod"].fillna(0).values + df["AssetImpairmentLoss_InvestmentProperty_CurrentPeriod"].fillna(0).values + df["AssetImpairmentLoss_FixedAssets_CurrentPeriod"].fillna(0).values + df["AssetImpairmentLoss_ConstructionMaterials_CurrentPeriod"].fillna(0).values + df["AssetImpairmentLoss_ConstruInProcess_CurrentPeriod"].fillna(0).values + df["AssetImpairmentLoss_BiologicalAssets_CurrentPeriod"].fillna(0).values + df["AssetImpairmentLoss_IntangibleAssets_CurrentPeriod"].fillna(0).values + df["AssetImpairmentLoss_GoodWill_CurrentPeriod"].fillna(0).values + df["AssetImpairmentLoss_Other_CurrentPeriod"].fillna(0).values - df["AssetImpairmentLoss_Total_CurrentPeriod"].fillna(0).values) > 0.01:
            error = "本期发生额:坏账损失+存货跌价损失+可供出售金融资产减值损失+持有至到期投资减值损失+长期股权投资减值损失+投资性房地产减值损失+固定资产减值损失+工程物资减值损失+在建工程减值损失+生产性生物资产减值损失+无形资产减值损失+商誉减值损失+其他<>合计"
            errorlist.append(error)
        # 上期发生额:坏账损失+存货跌价损失+可供出售金融资产减值损失+持有至到期投资减值损失+长期股权投资减值损失+投资性房地产减值损失+固定资产减值损失+工程物资减值损失+在建工程减值损失+生产性生物资产减值损失+无形资产减值损失+商誉减值损失+其他=合计
        if abs(df["AssetImpairmentLoss_AccountReceivable_PriorPeriod"].fillna(0).values + df["AssetImpairmentLoss_Inventories_PriorPeriod"].fillna(0).values + df["AssetImpairmentLoss_HoldForSaleAssets_PriorPeriod"].fillna(0).values + df["AssetImpairmentLoss_HoldToMaturityInvestments_PriorPeriod"].fillna(0).values + df["AssetImpairmentLoss_LongtermEquityInvest_PriorPeriod"].fillna(0).values + df["AssetImpairmentLoss_InvestmentProperty_PriorPeriod"].fillna(0).values + df["AssetImpairmentLoss_FixedAssets_PriorPeriod"].fillna(0).values + df["AssetImpairmentLoss_ConstructionMaterials_PriorPeriod"].fillna(0).values + df["AssetImpairmentLoss_ConstruInProcess_PriorPeriod"].fillna(0).values + df["AssetImpairmentLoss_BiologicalAssets_PriorPeriod"].fillna(0).values + df["AssetImpairmentLoss_IntangibleAssets_PriorPeriod"].fillna(0).values + df["AssetImpairmentLoss_GoodWill_PriorPeriod"].fillna(0).values + df["AssetImpairmentLoss_Other_PriorPeriod"].fillna(0).values - df["AssetImpairmentLoss_Total_PriorPeriod"].fillna(0).values) > 0.01:
            error = "上期发生额:坏账损失+存货跌价损失+可供出售金融资产减值损失+持有至到期投资减值损失+长期股权投资减值损失+投资性房地产减值损失+固定资产减值损失+工程物资减值损失+在建工程减值损失+生产性生物资产减值损失+无形资产减值损失+商誉减值损失+其他<>合计"
            errorlist.append(error)
        











        return df, errorlist


if __name__ == "__main__":
    d = GetAssetImpairmentLoss()