
import pandas as pd
from ChosenAPI.DataImport.ChangeToNum import ChangeData



class GetOtherNoncurrentLiabilities(object):#其它非流动负债
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
            "OtherNoncurrentLiabilities_Project1_this": data.cell_value(2, 1),  # B3 3行2列项目1期末余额
            "OtherNoncurrentLiabilities_Project2_this": data.cell_value(3, 1),  # B4 4行2列项目2期末余额
            "OtherNoncurrentLiabilities_Project3_this": data.cell_value(4, 1),  # B5 5行2列项目3期末余额
            "OtherNoncurrentLiabilities_Project4_this": data.cell_value(5, 1),  # B6 6行2列项目4期末余额
            "OtherNoncurrentLiabilities_Project5_this": data.cell_value(6, 1),  # B7 7行2列项目5期末余额
            "OtherNoncurrentLiabilities_Total_this": data.cell_value(7, 1),  # B8 8行2列合计期末余额
            "OtherNoncurrentLiabilities_Project1_last": data.cell_value(2, 2),  # C3 3行3列项目1期初余额
            "OtherNoncurrentLiabilities_Project2_last": data.cell_value(3, 2),  # C4 4行3列项目2期初余额
            "OtherNoncurrentLiabilities_Project3_last": data.cell_value(4, 2),  # C5 5行3列项目3期初余额
            "OtherNoncurrentLiabilities_Project4_last": data.cell_value(5, 2),  # C6 6行3列项目4期初余额
            "OtherNoncurrentLiabilities_Project5_last": data.cell_value(6, 2),  # C7 7行3列项目5期初余额
            "OtherNoncurrentLiabilities_Total_last": data.cell_value(7, 2),  # C8 8行3列合计期初余额


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
        dic["OtherNoncurrentLiabilities_Remark"] = data.cell_value(9, 1),  # B10 10行2列说明
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
        # 期末余额:项目1+项目2+项目3+项目4+项目5=合计
        if abs(df["OtherNoncurrentLiabilities_Project1_this"].fillna(0).values + df["OtherNoncurrentLiabilities_Project2_this"].fillna(0).values + df["OtherNoncurrentLiabilities_Project3_this"].fillna(0).values + df["OtherNoncurrentLiabilities_Project4_this"].fillna(0).values + df["OtherNoncurrentLiabilities_Project5_this"].fillna(0).values - df["OtherNoncurrentLiabilities_Total_this"].fillna(0).values) > 0.01:
            error = "期末余额:项目1+项目2+项目3+项目4+项目5<>合计"
            errorlist.append(error)
	    # 期初余额:项目1+项目2+项目3+项目4+项目5=合计
        if abs(df["OtherNoncurrentLiabilities_Project1_last"].fillna(0).values + df["OtherNoncurrentLiabilities_Project2_last"].fillna(0).values + df["OtherNoncurrentLiabilities_Project3_last"].fillna(0).values + df["OtherNoncurrentLiabilities_Project4_last"].fillna(0).values + df["OtherNoncurrentLiabilities_Project5_last"].fillna(0).values - df["OtherNoncurrentLiabilities_Total_last"].fillna(0).values) > 0.01:
            error = "期初余额:项目1+项目2+项目3+项目4+项目5<>合计"
            errorlist.append(error)
        











        return df, errorlist


if __name__ == "__main__":
    d = GetOtherNoncurrentLiabilities()