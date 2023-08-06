
import pandas as pd
from ChosenAPI.DataImport.ChangeToNum import ChangeData



class GetAdvancePayment(object):#预付账款
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
            "AdvancePayment_0_1_sum_this": data.cell_value(4, 1),  # B5 5行2列预付款项按账龄列示1年以内期末余额金额
            "AdvancePayment_1_2_sum_this": data.cell_value(5, 1),  # B6 6行2列预付款项按账龄列示1～2年期末余额金额
            "AdvancePayment_2_3_sum_this": data.cell_value(6, 1),  # B7 7行2列预付款项按账龄列示2～3年期末余额金额
            "AdvancePayment_3_4_sum_this": data.cell_value(7, 1),  # B8 8行2列预付款项按账龄列示3～4年期末余额金额
            "AdvancePayment_4_5_sum_this": data.cell_value(8, 1),  # B9 9行2列预付款项按账龄列示4～5年期末余额金额
            "AdvancePayment_5__sum_this": data.cell_value(9, 1),  # B10 10行2列预付款项按账龄列示5年以上期末余额金额
            "AdvancePayment_Total_sum_this": data.cell_value(10, 1),  # B11 11行2列预付款项按账龄列示合计期末余额金额
            "AdvancePayment_0_1_ratio_this": data.cell_value(4, 2),  # C5 5行3列预付款项按账龄列示1年以内期末余额比例(%)
            "AdvancePayment_1_2_ratio_this": data.cell_value(5, 2),  # C6 6行3列预付款项按账龄列示1～2年期末余额比例(%)
            "AdvancePayment_2_3_ratio_this": data.cell_value(6, 2),  # C7 7行3列预付款项按账龄列示2～3年期末余额比例(%)
            "AdvancePayment_3_4_ratio_this": data.cell_value(7, 2),  # C8 8行3列预付款项按账龄列示3～4年期末余额比例(%)
            "AdvancePayment_4_5_ratio_this": data.cell_value(8, 2),  # C9 9行3列预付款项按账龄列示4～5年期末余额比例(%)
            "AdvancePayment_5__ratio_this": data.cell_value(9, 2),  # C10 10行3列预付款项按账龄列示5年以上期末余额比例(%)
            "AdvancePayment_Total_ratio_this": data.cell_value(10, 2),  # C11 11行3列预付款项按账龄列示合计期末余额比例(%)
            "AdvancePayment_0_1_sum_last": data.cell_value(4, 3),  # D5 5行4列预付款项按账龄列示1年以内期初余额金额
            "AdvancePayment_1_2_sum_last": data.cell_value(5, 3),  # D6 6行4列预付款项按账龄列示1～2年期初余额金额
            "AdvancePayment_2_3_sum_last": data.cell_value(6, 3),  # D7 7行4列预付款项按账龄列示2～3年期初余额金额
            "AdvancePayment_3_4_sum_last": data.cell_value(7, 3),  # D8 8行4列预付款项按账龄列示3～4年期初余额金额
            "AdvancePayment_4_5_sum_last": data.cell_value(8, 3),  # D9 9行4列预付款项按账龄列示4～5年期初余额金额
            "AdvancePayment_5__sum_last": data.cell_value(9, 3),  # D10 10行4列预付款项按账龄列示5年以上期初余额金额
            "AdvancePayment_Total_sum_last": data.cell_value(10, 3),  # D11 11行4列预付款项按账龄列示合计期初余额金额
            "AdvancePayment_0_1_ratio_last": data.cell_value(4, 4),  # E5 5行5列预付款项按账龄列示1年以内期初余额比例(%)
            "AdvancePayment_1_2_ratio_last": data.cell_value(5, 4),  # E6 6行5列预付款项按账龄列示1～2年期初余额比例(%)
            "AdvancePayment_2_3_ratio_last": data.cell_value(6, 4),  # E7 7行5列预付款项按账龄列示2～3年期初余额比例(%)
            "AdvancePayment_3_4_ratio_last": data.cell_value(7, 4),  # E8 8行5列预付款项按账龄列示3～4年期初余额比例(%)
            "AdvancePayment_4_5_ratio_last": data.cell_value(8, 4),  # E9 9行5列预付款项按账龄列示4～5年期初余额比例(%)
            "AdvancePayment_5__ratio_last": data.cell_value(9, 4),  # E10 10行5列预付款项按账龄列示5年以上期初余额比例(%)
            "AdvancePayment_Total_ratio_last": data.cell_value(10, 4),  # E11 11行5列预付款项按账龄列示合计期初余额比例(%)
            "AdvancePayment_Company1_this": data.cell_value(15, 1),  # B16 16行2列按预付对象归集的期末余额前五名的预付款情况单位名称期末余额
            "AdvancePayment_Company2_this": data.cell_value(16, 1),  # B17 17行2列按预付对象归集的期末余额前五名的预付款情况单位名称期末余额
            "AdvancePayment_Company3_this": data.cell_value(17, 1),  # B18 18行2列按预付对象归集的期末余额前五名的预付款情况单位名称期末余额
            "AdvancePayment_Company4_this": data.cell_value(18, 1),  # B19 19行2列按预付对象归集的期末余额前五名的预付款情况单位名称期末余额
            "AdvancePayment_Company5_this": data.cell_value(19, 1),  # B20 20行2列按预付对象归集的期末余额前五名的预付款情况单位名称期末余额
            "AdvancePayment_Total_this": data.cell_value(20, 1),  # B21 21行2列按预付对象归集的期末余额前五名的预付款情况单位名称期末余额
            "AdvancePayment_Company1_ratio": data.cell_value(15, 2),# C16 16行3列按预付对象归集的期末余额前五名的预付款情况单位名称占预付款项期末余额合计数的比例(%)
            "AdvancePayment_Company2_ratio": data.cell_value(16, 2),# C17 17行3列按预付对象归集的期末余额前五名的预付款情况单位名称占预付款项期末余额合计数的比例(%)
            "AdvancePayment_Company3_ratio": data.cell_value(17, 2),# C18 18行3列按预付对象归集的期末余额前五名的预付款情况单位名称占预付款项期末余额合计数的比例(%)
            "AdvancePayment_Company4_ratio": data.cell_value(18, 2),# C19 19行3列按预付对象归集的期末余额前五名的预付款情况单位名称占预付款项期末余额合计数的比例(%)
            "AdvancePayment_Company5_ratio": data.cell_value(19, 2),# C20 20行3列按预付对象归集的期末余额前五名的预付款情况单位名称占预付款项期末余额合计数的比例(%)
            "AdvancePayment_Total_ratio": data.cell_value(20, 2),# C21 21行3列按预付对象归集的期末余额前五名的预付款情况单位名称占预付款项期末余额合计数的比例(%)

            












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
        dic["AdvancePayment_Remark"] = data.cell_value(22, 1),  # B23 23行2列说明
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
        # 预付款项按账龄列示期末余额：1年以内+1～2年+2～3年+3～4年+4～5年+5年以上=合计
        if abs(df["AdvancePayment_0_1_sum_this"].fillna(0).values + df["AdvancePayment_1_2_sum_this"].fillna(0).values + df["AdvancePayment_2_3_sum_this"].fillna(0).values + df["AdvancePayment_3_4_sum_this"].fillna(0).values + df["AdvancePayment_4_5_sum_this"].fillna(0).values + df["AdvancePayment_5__sum_this"].fillna(0).values - df["AdvancePayment_Total_sum_this"].fillna(0).values) > 0.01:
            error = "预付款项按账龄列示期末余额：1年以内+1～2年+2～3年+3～4年+4～5年+5年以上<>合计"
            errorlist.append(error)
        # 预付款项按账龄列示期初余额：1年以内+1～2年+2～3年+3～4年+4～5年+5年以上=合计
        if abs(df["AdvancePayment_0_1_sum_last"].fillna(0).values + df["AdvancePayment_1_2_sum_last"].fillna(0).values + df["AdvancePayment_2_3_sum_last"].fillna(0).values + df["AdvancePayment_3_4_sum_last"].fillna(0).values + df["AdvancePayment_4_5_sum_last"].fillna(0).values + df["AdvancePayment_5__sum_last"].fillna(0).values - df["AdvancePayment_Total_sum_last"].fillna(0).values) > 0.01:
            error = "预付款项按账龄列示期初余额：1年以内+1～2年+2～3年+3～4年+4～5年+5年以上<>合计"
            errorlist.append(error)
        # 按预付对象归集的期末余额前五名的预付款情况：1+2+3+4+5=合计
        if abs(df["AdvancePayment_Company1_this"].fillna(0).values + df["AdvancePayment_Company2_this"].fillna(0).values + df["AdvancePayment_Company3_this"].fillna(0).values + df["AdvancePayment_Company4_this"].fillna(0).values + df["AdvancePayment_Company5_this"].fillna(0).values - df["AdvancePayment_Total_this"].fillna(0).values) > 0.01:
            error = "按预付对象归集的期末余额前五名的预付款情况：1+2+3+4+5<>合计"
            errorlist.append(error)
        











        return df, errorlist


if __name__ == "__main__":
    d = GetAdvancePayment()