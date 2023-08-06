
import pandas as pd
from ChosenAPI.DataImport.ChangeToNum import ChangeData


class GetDividendPayable(object):  # 应付股利
    def __init__(self):
        pass

    def get_data(self, data, username, identify):  # 定义数据位置
        """
        获取基本数据表格的数据，
        :param data: 传入数据表格
        :param username: 用户名
        :param identify: 实例识别号
        :return:
        """
        dic = {
            "DividendPayable_CommonStockDividend_this": data.cell_value(3, 1),  # B4 4行2列普通股股利期末余额
            "DividendPayable_Division_this": data.cell_value(4, 1),  # B5 5行2列划分为权益工具的优先股\永续债股利期末余额
            "DividendPayable_Tool1_this": data.cell_value(5, 1),  # B6 6行2列工具1期末余额
            "DividendPayable_Tool2_this": data.cell_value(6, 1),  # B7 7行2列工具2期末余额
            "DividendPayable_Total_this": data.cell_value(7, 1),  # B8 8行2列合计期末余额
            "DividendPayable_CommonStockDividend_last": data.cell_value(3, 2),  # C4 4行3列普通股股利期初余额
            "DividendPayable_Division_last": data.cell_value(4, 2),  # C5 5行3列划分为权益工具的优先股\永续债股利期初余额
            "DividendPayable_Tool1_last": data.cell_value(5, 2),  # C6 6行3列工具1期初余额
            "DividendPayable_Tool2_last": data.cell_value(6, 2),  # C7 7行3列工具2期初余额
            "DividendPayable_Total_last": data.cell_value(7, 2),  # C8 8行3列合计期初余额


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
        dic["DividendPayable_Remark"] = data.cell_value(9, 1),  # B10 10行2列说明
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
        # 期末余额:普通股股利+划分为权益工具的优先股\永续债股利=合计
        if abs(df["DividendPayable_CommonStockDividend_this"].fillna(0).values + df[
            "DividendPayable_Division_this"].fillna(0).values - df["DividendPayable_Total_this"].fillna(
                0).values) > 0.01:
            error = "期末余额:普通股股利+划分为权益工具的优先股\永续债股利<>合计"
            errorlist.append(error)
            # 期初余额:普通股股利+划分为权益工具的优先股\永续债股利=合计
        if abs(df["DividendPayable_CommonStockDividend_last"].fillna(0).values + df[
            "DividendPayable_Division_last"].fillna(0).values - df["DividendPayable_Total_last"].fillna(0).values) > 0.01:
            error = "期初余额:普通股股利+划分为权益工具的优先股\永续债股利<>合计"
            errorlist.append(error)

        return df, errorlist


if __name__ == "__main__":
    d = GetDividendPayable()
