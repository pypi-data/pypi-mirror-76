
import pandas as pd
from ChosenAPI.DataImport.ChangeToNum import ChangeData



class GetTradingAssets(object):#交易性金融资产
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
            "TradingAssets_this": data.cell_value(3, 1),  # B4 4行2列交易性金融资产期末余额
            "TradingAssets_Debt_this": data.cell_value(4, 1),  # B5 5行2列债务工具投资期末余额
            "TradingAssets_Equity_this": data.cell_value(5, 1),  # B6 6行2列权益工具投资期末余额
            "TradingAssets_Derive_this": data.cell_value(6, 1),  # B7 7行2列衍生金融资产期末余额
            "TradingAssets_Other_this": data.cell_value(7, 1),  # B8 8行2列其他期末余额
            "TradingAssets_Assets_this": data.cell_value(8, 1),# B9 9行2列指定以公允价值计量且其变动计入当期损益的金融资产期末余额
            "TradingAssets_Debt_Assets_this": data.cell_value(9, 1),# B10 10行2列债务工具投资期末余额
            "TradingAssets_Equity_Assets_this": data.cell_value(10, 1),# B11 11行2列权益工具投资期末余额
            "TradingAssets_Other_Assets_this": data.cell_value(11, 1),  # B12 12行2列其他期末余额
            "TradingAssets_Total_this": data.cell_value(12, 1),  # B13 13行2列合计期末余额
            "TradingAssets_last": data.cell_value(3, 2),  # C4 4行3列交易性金融资产期初余额
            "TradingAssets_Debt_last": data.cell_value(4, 2),  # C5 5行3列债务工具投资期初余额
            "TradingAssets_Equity_last": data.cell_value(5, 2),  # C6 6行3列权益工具投资期初余额
            "TradingAssets_Derive_last": data.cell_value(6, 2),  # C7 7行3列衍生金融资产期初余额
            "TradingAssets_Other_last": data.cell_value(7, 2),  # C8 8行3列其他期初余额
            "TradingAssets_Assets_last": data.cell_value(8, 2),# C9 9行3列指定以公允价值计量且其变动计入当期损益的金融资产期初余额
            "TradingAssets_Debt_Assets_last": data.cell_value(9, 2),# C10 10行3列债务工具投资期初余额
            "TradingAssets_Equity_Assets_last": data.cell_value(10, 2),# C11 11行3列权益工具投资期初余额
            "TradingAssets_Other_Assets_last": data.cell_value(11, 2),  # C12 12行3列其他期初余额
            "TradingAssets_Total_last": data.cell_value(12, 2),  # C13 13行3列合计期初余额

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
        dic["TradingAssets_Remark_this"] = data.cell_value(14, 1),  # B15 15行2列说明
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
        # 债务工具投资+权益工具投资+衍生金融资产+其他=交易性金融资产
        if abs(df["TradingAssets_Debt_this"].fillna(0).values + df["TradingAssets_Equity_this"].fillna(0).values + df["TradingAssets_Derive_this"].fillna(0).values + df["TradingAssets_Other_this"].fillna(0).values - df["TradingAssets_this"].fillna(0).values) > 0.01:
            error = "交易性金融资产:本期债务工具投资+本期权益工具投资+本期衍生金融资产+本期其他<>本期交易性金融资产"
            errorlist.append(error)
        if abs(df["TradingAssets_Debt_last"].fillna(0).values + df["TradingAssets_Equity_last"].fillna(0).values + df["TradingAssets_Derive_last"].fillna(0).values + df["TradingAssets_Other_last"].fillna(0).values - df["TradingAssets_last"].fillna(0).values) > 0.01:
            error = "交易性金融资产:上期债务工具投资+上期权益工具投资+上期衍生金融资产+上期其他<>上期交易性金融资产"
            errorlist.append(error)
        # 债务工具投资+权益工具投资+衍生金融资产+其他=指定以公允价值计量且其变动计入当期损益的金融资产
        if abs(df["TradingAssets_Debt_Assets_this"].fillna(0).values + df["TradingAssets_Equity_Assets_this"].fillna(0).values + df["TradingAssets_Other_Assets_this"].fillna(0).values - df["TradingAssets_Assets_this"].fillna(0).values) > 0.01:
            error = "交易性金融资产:本期债务工具投资+本期权益工具投资+本期其他<>本期指定以公允价值计量且其变动计入当期损益的金融资产"
            errorlist.append(error)
        if abs(df["TradingAssets_Debt_Assets_last"].fillna(0).values + df["TradingAssets_Equity_Assets_last"].fillna(0).values + df["TradingAssets_Other_Assets_last"].fillna(0).values - df["TradingAssets_Assets_last"].fillna(0).values) > 0.01:
            error = "交易性金融资产:上期债务工具投资+上期权益工具投资+上期其他<>上期指定以公允价值计量且其变动计入当期损益的金融资产"
            errorlist.append(error)
        # 交易性金融资产+指定以公允价值计量且其变动计入当期损益的金融资产=合计
        if abs(df["TradingAssets_this"].fillna(0).values + df["TradingAssets_Assets_this"].fillna(0).values - df["TradingAssets_Total_this"].fillna(0).values) > 0.01:
            error = "交易性金融资产:本期交易性金融资产+本期指定以公允价值计量且其变动计入当期损益的金融资产<>本期合计"
            errorlist.append(error)
        if abs(df["TradingAssets_last"].fillna(0).values + df["TradingAssets_Assets_last"].fillna(0).values - df["TradingAssets_Total_last"].fillna(0).values) > 0.01:
            error = "交易性金融资产:上期交易性金融资产+上期指定以公允价值计量且其变动计入当期损益的金融资产<>上期合计"
            errorlist.append(error)

        return df, errorlist


if __name__ == "__main__":
    d = GetTradingAssets()