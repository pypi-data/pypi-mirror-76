
import pandas as pd
from ChosenAPI.DataImport.ChangeToNum import ChangeData



class GetAssetDealIncome(object):#资产处置收益
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
            "AssetDealIncome_Hold_CurrentPeriod": data.cell_value(2, 1),  # B3 3行2列划分为持有待售的非流动资产或处置组的处置利得或损失本期发生额
            "AssetDealIncome_Fixedassets_CurrentPeriod": data.cell_value(3, 1),  # B4 4行2列固定资产处置利得或损失本期发生额
            "AssetDealIncome_Construinprocess_CurrentPeriod": data.cell_value(4, 1),  # B5 5行2列在建工程处置利得或损失本期发生额
            "AssetDealIncome_Intangibleassets_CurrentPeriod": data.cell_value(5, 1),  # B6 6行2列无形资产处置利得或损失本期发生额
            "AssetDealIncome_Biologicalassets_CurrentPeriod": data.cell_value(6, 1),  # B7 7行2列生产性生物资产处置利得或损失本期发生额
            "AssetDealIncome_DebtRestructuring_CurrentPeriod": data.cell_value(7, 1),  # B8 8行2列债务重组中因处置非流动资产产生的利得或损失本期发生额
            "AssetDealIncome_ExchangeOfNonMonetaryAssets_CurrentPeriod": data.cell_value(8, 1),  # B9 9行2列非货币性资产交换产生的利得或损失本期发生额
            "AssetDealIncome_Other_CurrentPeriod": data.cell_value(9, 1),  # B10 10行2列其他本期发生额
            "AssetDealIncome_Total_CurrentPeriod": data.cell_value(10, 1),  # B11 11行2列合计本期发生额
            "AssetDealIncome_Hold_PriorPeriod": data.cell_value(2, 2),  # C3 3行3列划分为持有待售的非流动资产或处置组的处置利得或损失上期发生额
            "AssetDealIncome_Fixedassets_PriorPeriod": data.cell_value(3, 2),  # C4 4行3列固定资产处置利得或损失上期发生额
            "AssetDealIncome_Construinprocess_PriorPeriod": data.cell_value(4, 2),  # C5 5行3列在建工程处置利得或损失上期发生额
            "AssetDealIncome_Intangibleassets_PriorPeriod": data.cell_value(5, 2),  # C6 6行3列无形资产处置利得或损失上期发生额
            "AssetDealIncome_Biologicalassets_PriorPeriod": data.cell_value(6, 2),  # C7 7行3列生产性生物资产处置利得或损失上期发生额
            "AssetDealIncome_DebtRestructuring_PriorPeriod": data.cell_value(7, 2),# C8 8行3列债务重组中因处置非流动资产产生的利得或损失上期发生额
            "AssetDealIncome_ExchangeOfNonMonetaryAssets_PriorPeriod": data.cell_value(8, 2),# C9 9行3列非货币性资产交换产生的利得或损失上期发生额
            "AssetDealIncome_Other_PriorPeriod": data.cell_value(9, 2),  # C10 10行3列其他上期发生额
            "AssetDealIncome_Total_PriorPeriod": data.cell_value(10, 2),  # C11 11行3列合计上期发生额
            "AssetDealIncome_Hold_sum": data.cell_value(2, 3),  # D3 3行4列划分为持有待售的非流动资产或处置组的处置利得或损失计入当期非经常性损益的金额
            "AssetDealIncome_Fixedassets_sum": data.cell_value(3, 3),  # D4 4行4列固定资产处置利得或损失计入当期非经常性损益的金额
            "AssetDealIncome_Construinprocess_sum": data.cell_value(4, 3),  # D5 5行4列在建工程处置利得或损失计入当期非经常性损益的金额
            "AssetDealIncome_Intangibleassets_sum": data.cell_value(5, 3),  # D6 6行4列无形资产处置利得或损失计入当期非经常性损益的金额
            "AssetDealIncome_Biologicalassets_sum": data.cell_value(6, 3),  # D7 7行4列生产性生物资产处置利得或损失计入当期非经常性损益的金额
            "AssetDealIncome_DebtRestructuring_sum": data.cell_value(7, 3),# D8 8行4列债务重组中因处置非流动资产产生的利得或损失计入当期非经常性损益的金额
            "AssetDealIncome_ExchangeOfNonMonetaryAssets_sum": data.cell_value(8, 3),# D9 9行4列非货币性资产交换产生的利得或损失计入当期非经常性损益的金额
            "AssetDealIncome_Other_sum": data.cell_value(9, 3),  # D10 10行4列其他计入当期非经常性损益的金额
            "AssetDealIncome_Total_sum": data.cell_value(10, 3),  # D11 11行4列合计计入当期非经常性损益的金额


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
        dic["AssetDealIncome_Remark"] = data.cell_value(12, 1),  # B13 13行2列说明]
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
        # 本期发生额:划分为持有待售的非流动资产或处置组的处置利得或损失+固定资产处置利得或损失+在建工程处置利得或损失+无形资产处置利得或损失+生产性生物资产处置利得或损失+债务重组中因处置非流动资产产生的利得或损失+非货币性资产交换产生的利得或损失+其他=合计
        if abs(df["AssetDealIncome_Hold_CurrentPeriod"].fillna(0).values + df["AssetDealIncome_Fixedassets_CurrentPeriod"].fillna(0).values + df["AssetDealIncome_Construinprocess_CurrentPeriod"].fillna(0).values + df["AssetDealIncome_Intangibleassets_CurrentPeriod"].fillna(0).values + df["AssetDealIncome_Biologicalassets_CurrentPeriod"].fillna(0).values + df["AssetDealIncome_DebtRestructuring_CurrentPeriod"].fillna(0).values + df["AssetDealIncome_ExchangeOfNonMonetaryAssets_CurrentPeriod"].fillna(0).values + df["AssetDealIncome_Other_CurrentPeriod"].fillna(0).values - df["AssetDealIncome_Total_CurrentPeriod"].fillna(0).values) > 0.01:
            error = "本期发生额:划分为持有待售的非流动资产或处置组的处置利得或损失+固定资产处置利得或损失+在建工程处置利得或损失+无形资产处置利得或损失+生产性生物资产处置利得或损失+债务重组中因处置非流动资产产生的利得或损失+非货币性资产交换产生的利得或损失+其他<>合计"
            errorlist.append(error)
        # 上期发生额:划分为持有待售的非流动资产或处置组的处置利得或损失+固定资产处置利得或损失+在建工程处置利得或损失+无形资产处置利得或损失+生产性生物资产处置利得或损失+债务重组中因处置非流动资产产生的利得或损失+非货币性资产交换产生的利得或损失+其他=合计
        if abs(df["AssetDealIncome_Hold_PriorPeriod"].fillna(0).values + df["AssetDealIncome_Fixedassets_PriorPeriod"].fillna(0).values + df["AssetDealIncome_Construinprocess_PriorPeriod"].fillna(0).values + df["AssetDealIncome_Intangibleassets_PriorPeriod"].fillna(0).values + df["AssetDealIncome_Biologicalassets_PriorPeriod"].fillna(0).values + df["AssetDealIncome_DebtRestructuring_PriorPeriod"].fillna(0).values + df["AssetDealIncome_ExchangeOfNonMonetaryAssets_PriorPeriod"].fillna(0).values + df["AssetDealIncome_Other_PriorPeriod"].fillna(0).values - df["AssetDealIncome_Total_PriorPeriod"].fillna(0).values) > 0.01:
            error = "上期发生额:划分为持有待售的非流动资产或处置组的处置利得或损失+固定资产处置利得或损失+在建工程处置利得或损失+无形资产处置利得或损失+生产性生物资产处置利得或损失+债务重组中因处置非流动资产产生的利得或损失+非货币性资产交换产生的利得或损失+其他<>合计"
            errorlist.append(error)
        # 计入当期非经常性损益的金额:划分为持有待售的非流动资产或处置组的处置利得或损失+固定资产处置利得或损失+在建工程处置利得或损失+无形资产处置利得或损失+生产性生物资产处置利得或损失+债务重组中因处置非流动资产产生的利得或损失+非货币性资产交换产生的利得或损失+其他=合计
        if abs(df["AssetDealIncome_Hold_sum"].fillna(0).values + df["AssetDealIncome_Fixedassets_sum"].fillna(0).values + df["AssetDealIncome_Construinprocess_sum"].fillna(0).values + df["AssetDealIncome_Intangibleassets_sum"].fillna(0).values + df["AssetDealIncome_Biologicalassets_sum"].fillna(0).values + df["AssetDealIncome_DebtRestructuring_sum"].fillna(0).values + df["AssetDealIncome_ExchangeOfNonMonetaryAssets_sum"].fillna(0).values + df["AssetDealIncome_Other_sum"].fillna(0).values - df["AssetDealIncome_Total_sum"].fillna(0).values) > 0.01:
            error = "计入当期非经常性损益的金额:划分为持有待售的非流动资产或处置组的处置利得或损失+固定资产处置利得或损失+在建工程处置利得或损失+无形资产处置利得或损失+生产性生物资产处置利得或损失+债务重组中因处置非流动资产产生的利得或损失+非货币性资产交换产生的利得或损失+其他<>合计"
            errorlist.append(error)
        











        return df, errorlist


if __name__ == "__main__":
    d = GetAssetDealIncome()