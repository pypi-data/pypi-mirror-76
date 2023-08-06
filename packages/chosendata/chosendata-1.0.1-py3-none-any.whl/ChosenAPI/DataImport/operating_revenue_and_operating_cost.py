
import pandas as pd
from ChosenAPI.DataImport.ChangeToNum import ChangeData



class GetOperatingRevenueAndOperatingCost(object):#营业收入和营业成本
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
            "OperatingRevenueAndOperatingCost_Main_ICP": data.cell_value(3, 1),# B4 4行2列主营业务本期发生额收入
            "OperatingRevenueAndOperatingCost_Other_ICP": data.cell_value(4, 1),# B5 5行2列其他业务本期发生额收入
            "OperatingRevenueAndOperatingCost_Total_ICP": data.cell_value(5, 1),# B6 6行2列合计本期发生额收入
            "OperatingRevenueAndOperatingCost_Main_CCP": data.cell_value(3, 2),# C4 4行3列主营业务本期发生额成本
            "OperatingRevenueAndOperatingCost_Other_CCP": data.cell_value(4, 2),# C5 5行3列其他业务本期发生额成本
            "OperatingRevenueAndOperatingCost_Total_CCP": data.cell_value(5, 2),  # C6 6行3列合计本期发生额成本
            "OperatingRevenueAndOperatingCost_Main_IPP": data.cell_value(3, 3),# D4 4行4列主营业务上期发生额收入
            "OperatingRevenueAndOperatingCost_Other_IPP": data.cell_value(4, 3),# D5 5行4列其他业务上期发生额收入
            "OperatingRevenueAndOperatingCost_Total_IPP": data.cell_value(5, 3),  # D6 6行4列合计上期发生额收入
            "OperatingRevenueAndOperatingCost_Main_CPP": data.cell_value(3, 4),# E4 4行5列主营业务上期发生额成本
            "OperatingRevenueAndOperatingCost_Other_CPP": data.cell_value(4, 4),# E5 5行5列其他业务上期发生额成本
            "OperatingRevenueAndOperatingCost_Total_CPP": data.cell_value(5, 4),  # E6 6行5列合计上期发生额成本
            "OperatingRevenueAndOperatingCost_Top_ICP": data.cell_value(9, 1),# B10 10行2列合计本期发生额收入
            "OperatingRevenueAndOperatingCost_Top_CCP": data.cell_value(9, 2),# C10 10行3列合计本期发生额成本
            "OperatingRevenueAndOperatingCost_Top_IPP": data.cell_value(9, 3),# D10 10行4列合计上期发生额收入
            "OperatingRevenueAndOperatingCost_Top_CPP": data.cell_value(9, 4),# E10 10行5列合计上期发生额成本



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
        dic["OperatingRevenueAndOperatingCost_Remark"] = data.cell_value(11, 1),  # B12 12行2列说明
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
        # 项目本期发生额收入：主营业务+其他业务=合计
        if abs(df["OperatingRevenueAndOperatingCost_Main_ICP"].fillna(0).values + df["OperatingRevenueAndOperatingCost_Other_ICP"].fillna(0).values - df["OperatingRevenueAndOperatingCost_Total_ICP"].fillna(0).values) > 0.01:
            error = "项目本期发生额收入：主营业务+其他业务<>合计"
            errorlist.append(error)
        # 项目本期发生额成本：主营业务+其他业务=合计
        if abs(df["OperatingRevenueAndOperatingCost_Main_CCP"].fillna(0).values + df["OperatingRevenueAndOperatingCost_Other_CCP"].fillna(0).values - df["OperatingRevenueAndOperatingCost_Total_CCP"].fillna(0).values) > 0.01:
            error = "项目本期发生额成本：主营业务+其他业务<>合计"
            errorlist.append(error)
        # 项目上期发生额收入：主营业务+其他业务=合计
        if abs(df["OperatingRevenueAndOperatingCost_Main_IPP"].fillna(0).values + df["OperatingRevenueAndOperatingCost_Other_IPP"].fillna(0).values - df["OperatingRevenueAndOperatingCost_Total_IPP"].fillna(0).values) > 0.01:
            error = "项目上期发生额收入：主营业务+其他业务<>合计"
            errorlist.append(error)
        # 项目上期发生额成本：主营业务+其他业务=合计
        if abs(df["OperatingRevenueAndOperatingCost_Main_CPP"].fillna(0).values + df["OperatingRevenueAndOperatingCost_Other_CPP"].fillna(0).values - df["OperatingRevenueAndOperatingCost_Total_CPP"].fillna(0).values) > 0.01:
            error = "项目上期发生额成本：主营业务+其他业务<>合计"
            errorlist.append(error)

        return df, errorlist


if __name__ == "__main__":
    d = GetOperatingRevenueAndOperatingCost()