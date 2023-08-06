
import pandas as pd
from ChosenAPI.DataImport.ChangeToNum import ChangeData


class GetShorttermLoan(object):#短期借款
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
            "ShorttermLoan_Pledge_this": data.cell_value(3, 1),  # B4 4行2列质押借款期末余额
            "ShorttermLoan_Mortgage_this": data.cell_value(4, 1),  # B5 5行2列抵押借款期末余额
            "ShorttermLoan_Ensure_this": data.cell_value(5, 1),  # B6 6行2列保证借款期末余额
            "ShorttermLoan_Credit_this": data.cell_value(6, 1),  # B7 7行2列信用借款期末余额
            "ShorttermLoan_Other_this": data.cell_value(7, 1),  # B8 8行2列其他借款期末余额
            "ShorttermLoan_Total_this": data.cell_value(8, 1),  # B9 9行2列合计期末余额
            "ShorttermLoan_Pledge_last": data.cell_value(3, 2),  # C4 4行3列质押借款期初余额
            "ShorttermLoan_Mortgage_last": data.cell_value(4, 2),  # C5 5行3列抵押借款期初余额
            "ShorttermLoan_Ensure_last": data.cell_value(5, 2),  # C6 6行3列保证借款期初余额
            "ShorttermLoan_Credit_last": data.cell_value(6, 2),  # C7 7行3列信用借款期初余额
            "ShorttermLoan_Other_last": data.cell_value(7, 2),  # C8 8行3列其他借款期初余额
            "ShorttermLoan_Total_last": data.cell_value(8, 2),  # C9 9行3列合计期初余额
            "ShorttermLoan_Company1_this": data.cell_value(12, 1),  # B13 13行2列单位1期末余额
            "ShorttermLoan_Company2_this": data.cell_value(13, 1),  # B14 14行2列单位2期末余额
            "ShorttermLoan_Company3_this": data.cell_value(14, 1),  # B15 15行2列单位3期末余额
            "ShorttermLoan_Company4_this": data.cell_value(15, 1),  # B16 16行2列单位4期末余额
            "ShorttermLoan_Company5_this": data.cell_value(16, 1),  # B17 17行2列单位5期末余额
            "ShorttermLoan_TotalCompany_this": data.cell_value(17, 1),  # B18 18行2列合计期末余额
            "ShorttermLoan_Company1_AnnualInterestRate": data.cell_value(12, 2),  # C13 13行3列单位1借款年利率(%)
            "ShorttermLoan_Company2_AnnualInterestRate": data.cell_value(13, 2),  # C14 14行3列单位2借款年利率(%)
            "ShorttermLoan_Company3_AnnualInterestRate": data.cell_value(14, 2),  # C15 15行3列单位3借款年利率(%)
            "ShorttermLoan_Company4_AnnualInterestRate": data.cell_value(15, 2),  # C16 16行3列单位4借款年利率(%)
            "ShorttermLoan_Company5_AnnualInterestRate": data.cell_value(16, 2),  # C17 17行3列单位5借款年利率(%)
            "ShorttermLoan_Company1_time": data.cell_value(12, 3),  # D13 13行4列单位1逾期时间
            "ShorttermLoan_Company2_time": data.cell_value(13, 3),  # D14 14行4列单位2逾期时间
            "ShorttermLoan_Company3_time": data.cell_value(14, 3),  # D15 15行4列单位3逾期时间
            "ShorttermLoan_Company4_time": data.cell_value(15, 3),  # D16 16行4列单位4逾期时间
            "ShorttermLoan_Company5_time": data.cell_value(16, 3),  # D17 17行4列单位5逾期时间
            "ShorttermLoan_Company1_OverdueInterestRates": data.cell_value(12, 4),  # E13 13行5列单位1逾期利率
            "ShorttermLoan_Company2_OverdueInterestRates": data.cell_value(13, 4),  # E14 14行5列单位2逾期利率
            "ShorttermLoan_Company3_OverdueInterestRates": data.cell_value(14, 4),  # E15 15行5列单位3逾期利率
            "ShorttermLoan_Company4_OverdueInterestRates": data.cell_value(15, 4),  # E16 16行5列单位4逾期利率
            "ShorttermLoan_Company5_OverdueInterestRates": data.cell_value(16, 4),  # E17 17行5列单位5逾期利率


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
        dic["ShorttermLoan_Remark"] = data.cell_value(19, 1),  # B20 20行2列说明
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
        # 短期借款分类期末余额:质押借款+抵押借款+保证借款+信用借款+其他借款=合计
        if abs(df["ShorttermLoan_Pledge_this"].fillna(0).values + df["ShorttermLoan_Mortgage_this"].fillna(0).values + df["ShorttermLoan_Ensure_this"].fillna(0).values + df["ShorttermLoan_Credit_this"].fillna(0).values + df["ShorttermLoan_Other_this"].fillna(0).values - df["ShorttermLoan_Total_this"].fillna(0).values) > 0.01:
            error = "短期借款分类期末余额:质押借款+抵押借款+保证借款+信用借款+其他借款<>合计"
            errorlist.append(error)
        # 短期借款分类期初余额:质押借款+抵押借款+保证借款+信用借款+其他借款=合计
        if abs(df["ShorttermLoan_Pledge_last"].fillna(0).values + df["ShorttermLoan_Mortgage_last"].fillna(0).values + df["ShorttermLoan_Ensure_last"].fillna(0).values + df["ShorttermLoan_Credit_last"].fillna(0).values + df["ShorttermLoan_Other_last"].fillna(0).values - df["ShorttermLoan_Total_last"].fillna(0).values) > 0.01:
            error = "短期借款分类期初余额:质押借款+抵押借款+保证借款+信用借款+其他借款<>合计"
            errorlist.append(error)
        # 已逾期未偿还的短期借款情况期末余额:单位1+单位2+单位3+单位4+单位5=合计
        if abs(df["ShorttermLoan_Company1_this"].fillna(0).values + df["ShorttermLoan_Company2_this"].fillna(0).values + df["ShorttermLoan_Company3_this"].fillna(0).values + df["ShorttermLoan_Company4_this"].fillna(0).values + df["ShorttermLoan_Company5_this"].fillna(0).values - df["ShorttermLoan_TotalCompany_this"].fillna(0).values) > 0.01:
            error = "已逾期未偿还的短期借款情况期末余额:单位1+单位2+单位3+单位4+单位5<>合计"
            errorlist.append(error)

        return df, errorlist


if __name__ == "__main__":
    d = GetShorttermLoan()