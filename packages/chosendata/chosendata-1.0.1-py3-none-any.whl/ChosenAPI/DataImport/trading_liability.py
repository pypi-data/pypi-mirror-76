
import pandas as pd
from ChosenAPI.DataImport.ChangeToNum import ChangeData



class GetTradingLiability(object):#交易性金融负债
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
            "TradingLiability_Transactional_this": data.cell_value(3, 1),  # B4 4行2列交易性金融负债期末余额
            "TradingLiability_Bond_this": data.cell_value(4, 1),  # B5 5行2列其中：发行的交易性债券      期末余额
            "TradingLiability_Derivative_this": data.cell_value(5, 1),  # B6 6行2列衍生金融负债期末余额
            "TradingLiability_Other_this": data.cell_value(6, 1),  # B7 7行2列其他金融负债期末余额
            "TradingLiability_TradingLiability_this": data.cell_value(7, 1),  # B8 8行2列指定为以公允价值计量且其变动计入当期损益的金融负债期末余额
            "TradingLiability_Total_this": data.cell_value(8, 1),  # B9 9行2列合计期末余额
            "TradingLiability_Transactional_last": data.cell_value(3, 2),  # C4 4行3列交易性金融负债期初余额
            "TradingLiability_Bond_last": data.cell_value(4, 2),  # C5 5行3列其中：发行的交易性债券      期初余额
            "TradingLiability_Derivative_last": data.cell_value(5, 2),  # C6 6行3列衍生金融负债期初余额
            "TradingLiability_Other_last": data.cell_value(6, 2),  # C7 7行3列其他金融负债期初余额
            "TradingLiability_TradingLiability_last": data.cell_value(7, 2),  # C8 8行3列指定为以公允价值计量且其变动计入当期损益的金融负债期初余额
            "TradingLiability_Total_last": data.cell_value(8, 2),  # C9 9行3列合计期初余额
            "TradingLiability_Project1_this": data.cell_value(12, 1),  # B13 13行2列项目1期末余额
            "TradingLiability_Project2_this": data.cell_value(13, 1),  # B14 14行2列项目2期末余额
            "TradingLiability_Project3_this": data.cell_value(14, 1),  # B15 15行2列项目3期末余额
            "TradingLiability_Project4_this": data.cell_value(15, 1),  # B16 16行2列项目4期末余额
            "TradingLiability_Project5_this": data.cell_value(16, 1),  # B17 17行2列项目5期末余额
            "TradingLiability_TotalImportant_this": data.cell_value(17, 1),  # B18 18行2列合计期末余额
            "TradingLiability_Project1_last": data.cell_value(12, 2),  # C13 13行3列项目1期初余额
            "TradingLiability_Project2_last": data.cell_value(13, 2),  # C14 14行3列项目2期初余额
            "TradingLiability_Project3_last": data.cell_value(14, 2),  # C15 15行3列项目3期初余额
            "TradingLiability_Project4_last": data.cell_value(15, 2),  # C16 16行3列项目4期初余额
            "TradingLiability_Project5_last": data.cell_value(16, 2),  # C17 17行3列项目5期初余额
            "TradingLiability_TotalImportant_last": data.cell_value(17, 2),  # C18 18行3列合计期初余额


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
        dic["TradingLiability_Remark"] = data.cell_value(19, 1),  # B20 20行2列说明
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
        # 以公允价值计量且其变动计入当期损益的金融负债期末余额:交易性金融负债+衍生金融负债+其他金融负债+指定为以公允价值计量且其变动计入当期损益的金融负债=合计
        if abs(df["TradingLiability_Transactional_this"].fillna(0).values + df["TradingLiability_Derivative_this"].fillna(0).values + df["TradingLiability_Other_this"].fillna(0).values + df["TradingLiability_TradingLiability_this"].fillna(0).values - df["TradingLiability_Total_this"].fillna(0).values) > 0.01:
            error = "以公允价值计量且其变动计入当期损益的金融负债期末余额:交易性金融负债+衍生金融负债+其他金融负债+指定为以公允价值计量且其变动计入当期损益的金融负债<>合计"
            errorlist.append(error)
        # 以公允价值计量且其变动计入当期损益的金融负债期初余额:交易性金融负债+衍生金融负债+其他金融负债+指定为以公允价值计量且其变动计入当期损益的金融负债=合计
        if abs(df["TradingLiability_Transactional_last"].fillna(0).values + df["TradingLiability_Derivative_last"].fillna(0).values + df["TradingLiability_Other_last"].fillna(0).values + df["TradingLiability_TradingLiability_last"].fillna(0).values - df["TradingLiability_Total_last"].fillna(0).values) > 0.01:
            error = "以公允价值计量且其变动计入当期损益的金融负债期初余额:交易性金融负债+衍生金融负债+其他金融负债+指定为以公允价值计量且其变动计入当期损益的金融负债<>合计"
            errorlist.append(error)
	    # 重要的衍生金融工具业务期末余额:项目1+项目2+项目3+项目4+项目5=合计
        if abs(df["TradingLiability_Project1_this"].fillna(0).values + df["TradingLiability_Project2_this"].fillna(0).values + df["TradingLiability_Project3_this"].fillna(0).values + df["TradingLiability_Project4_this"].fillna(0).values + df["TradingLiability_Project5_this"].fillna(0).values - df["TradingLiability_Total_this"].fillna(0).values) > 0.01:
            error = "重要的衍生金融工具业务期末余额:项目1+项目2+项目3+项目4+项目5<>合计"
            errorlist.append(error)
	    # 重要的衍生金融工具业务期初余额:项目1+项目2+项目3+项目4+项目5=合计
        if abs(df["TradingLiability_Project1_last"].fillna(0).values + df["TradingLiability_Project2_last"].fillna(0).values + df["TradingLiability_Project3_last"].fillna(0).values + df["TradingLiability_Project4_last"].fillna(0).values + df["TradingLiability_Project5_last"].fillna(0).values - df["TradingLiability_Total_last"].fillna(0).values) > 0.01:
            error = "重要的衍生金融工具业务期初余额:项目1+项目2+项目3+项目4+项目5<>合计"
            errorlist.append(error)

        return df, errorlist


if __name__ == "__main__":
    d = GetTradingLiability()