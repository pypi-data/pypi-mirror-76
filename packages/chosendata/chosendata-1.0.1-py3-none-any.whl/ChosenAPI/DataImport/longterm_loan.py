
import pandas as pd
from ChosenAPI.DataImport.ChangeToNum import ChangeData



class GetLongtermLoan(object):#长期借款
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
            "LongtermLoan_Pledge_this": data.cell_value(2, 1),  # B3 3行2列质押借款期末余额
            "LongtermLoan_Mortgage_this": data.cell_value(3, 1),  # B4 4行2列抵押借款期末余额
            "LongtermLoan_Ensure_this": data.cell_value(4, 1),  # B5 5行2列保证借款期末余额
            "LongtermLoan_Credit_this": data.cell_value(5, 1),  # B6 6行2列信用借款期末余额
            "LongtermLoan_Other_this": data.cell_value(6, 1),  # B7 7行2列其他借款期末余额
            "LongtermLoan_Total_this": data.cell_value(7, 1),  # B8 8行2列合计期末余额
            "LongtermLoan_Pledge_last": data.cell_value(2, 2),  # C3 3行3列质押借款期初余额
            "LongtermLoan_Mortgage_last": data.cell_value(3, 2),  # C4 4行3列抵押借款期初余额
            "LongtermLoan_Ensure_last": data.cell_value(4, 2),  # C5 5行3列保证借款期初余额
            "LongtermLoan_Credit_last": data.cell_value(5, 2),  # C6 6行3列信用借款期初余额
            "LongtermLoan_Other_last": data.cell_value(6, 2),  # C7 7行3列其他借款期初余额
            "LongtermLoan_Total_last": data.cell_value(7, 2),  # C8 8行3列合计期初余额


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
        dic["LongtermLoan_Remark"] = data.cell_value(9, 1),  # B10 10行2列说明
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
        # 期末余额:质押借款+抵押借款+保证借款+信用借款+其他借款=合计
        if abs(df["LongtermLoan_Pledge_this"].fillna(0).values + df["LongtermLoan_Mortgage_this"].fillna(0).values + df["LongtermLoan_Ensure_this"].fillna(0).values + df["LongtermLoan_Credit_this"].fillna(0).values + df["LongtermLoan_Other_this"].fillna(0).values - df["LongtermLoan_Total_this"].fillna(0).values) > 0.01:
            error = "期末余额:质押借款+抵押借款+保证借款+信用借款+其他借款<>合计"
            errorlist.append(error)
        # 期初余额:质押借款+抵押借款+保证借款+信用借款+其他借款=合计
        if abs(df["LongtermLoan_Pledge_last"].fillna(0).values + df["LongtermLoan_Mortgage_last"].fillna(0).values + df["LongtermLoan_Ensure_last"].fillna(0).values + df["LongtermLoan_Credit_last"].fillna(0).values + df["LongtermLoan_Other_last"].fillna(0).values - df["LongtermLoan_Total_last"].fillna(0).values) > 0.01:
            error = "期初余额:质押借款+抵押借款+保证借款+信用借款+其他借款<>合计"
            errorlist.append(error)
        











        return df, errorlist


if __name__ == "__main__":
    d = GetLongtermLoan()