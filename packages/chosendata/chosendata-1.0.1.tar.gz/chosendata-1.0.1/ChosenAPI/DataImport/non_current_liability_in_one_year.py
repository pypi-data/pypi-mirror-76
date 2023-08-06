
import pandas as pd
from ChosenAPI.DataImport.ChangeToNum import ChangeData



class GetNonCurrentLiabilityInOneYear(object):#一年内到期的非流动负债
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
            "NonCurrentLiabilityInOneYear_LongTermBorrowing_this": data.cell_value(2, 1),  # B3 3行2列一年内到期的长期借款期末余额
            "NonCurrentLiabilityInOneYear_BondsPayable_this": data.cell_value(3, 1),  # B4 4行2列一年内到期的应付债券
            "NonCurrentLiabilityInOneYear_LongTermPayables_this": data.cell_value(4, 1),  # B5 5行2列一年内到期的长期应付款
            "NonCurrentLiabilityInOneYear_Other_this": data.cell_value(5, 1),  # B6 6行2列其他
            "NonCurrentLiabilityInOneYear_Total_this": data.cell_value(6, 1),  # B7 7行2列合计
            "NonCurrentLiabilityInOneYear_LongTermBorrowing_last": data.cell_value(2, 2),  # C3 3行3列一年内到期的长期借款期初余额
            "NonCurrentLiabilityInOneYear_BondsPayable_last": data.cell_value(3, 2),  # C4 4行3列一年内到期的应付债券
            "NonCurrentLiabilityInOneYear_LongTermPayables_last": data.cell_value(4, 2),  # C5 5行3列一年内到期的长期应付款
            "NonCurrentLiabilityInOneYear_Other_last": data.cell_value(5, 2),  # C6 6行3列其他
            "NonCurrentLiabilityInOneYear_Total_last": data.cell_value(6, 2),  # C7 7行3列合计


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
        dic["NonCurrentLiabilityInOneYear_Remark"] = data.cell_value(8, 1),  # B9 9行2列说明
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
        # 期末余额:一年内到期的长期借款+一年内到期的应付债券+一年内到期的长期应付款+其他=合计
        if abs(df["NonCurrentLiabilityInOneYear_LongTermBorrowing_this"].fillna(0).values + df["NonCurrentLiabilityInOneYear_BondsPayable_this"].fillna(0).values + df["NonCurrentLiabilityInOneYear_LongTermPayables_this"].fillna(0).values + df["NonCurrentLiabilityInOneYear_Other_this"].fillna(0).values - df["NonCurrentLiabilityInOneYear_Total_this"].fillna(0).values) > 0.01:
            error = "期末余额:一年内到期的长期借款+一年内到期的应付债券+一年内到期的长期应付款+其他<>合计"
            errorlist.append(error)
	    # 期初余额:一年内到期的长期借款+一年内到期的应付债券+一年内到期的长期应付款+其他=合计
        if abs(df["NonCurrentLiabilityInOneYear_LongTermBorrowing_last"].fillna(0).values + df["NonCurrentLiabilityInOneYear_BondsPayable_last"].fillna(0).values + df["NonCurrentLiabilityInOneYear_LongTermPayables_last"].fillna(0).values + df["NonCurrentLiabilityInOneYear_Other_last"].fillna(0).values - df["NonCurrentLiabilityInOneYear_Total_last"].fillna(0).values) > 0.01:
            error = "期初余额:一年内到期的长期借款+一年内到期的应付债券+一年内到期的长期应付款+其他<>合计"
            errorlist.append(error)
        











        return df, errorlist


if __name__ == "__main__":
    d = GetNonCurrentLiabilityInOneYear()