
import pandas as pd
from ChosenAPI.DataImport.ChangeToNum import ChangeData



class GetDevelopmentExpenditure(object):#开发支出
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
            "DevelopmentExpenditure_Project1_last": data.cell_value(3, 1),  # B4 4行2列项目1期初余额
            "DevelopmentExpenditure_Project2_last": data.cell_value(4, 1),  # B5 5行2列项目2期初余额
            "DevelopmentExpenditure_Project3_last": data.cell_value(5, 1),  # B6 6行2列项目3期初余额
            "DevelopmentExpenditure_Project4_last": data.cell_value(6, 1),  # B7 7行2列项目4期初余额
            "DevelopmentExpenditure_Project5_last": data.cell_value(7, 1),  # B8 8行2列项目5期初余额
            "DevelopmentExpenditure_Total_last": data.cell_value(8, 1),  # B9 9行2列合计期初余额
            "DevelopmentExpenditure_Project1_internal": data.cell_value(3, 2),  # C4 4行3列项目1本期增加内部开发支出
            "DevelopmentExpenditure_Project2_internal": data.cell_value(4, 2),  # C5 5行3列项目2本期增加内部开发支出
            "DevelopmentExpenditure_Project3_internal": data.cell_value(5, 2),  # C6 6行3列项目3本期增加内部开发支出
            "DevelopmentExpenditure_Project4_internal": data.cell_value(6, 2),  # C7 7行3列项目4本期增加内部开发支出
            "DevelopmentExpenditure_Project5_internal": data.cell_value(7, 2),  # C8 8行3列项目5本期增加内部开发支出
            "DevelopmentExpenditure_Total_internal": data.cell_value(8, 2),  # C9 9行3列合计本期增加内部开发支出
            "DevelopmentExpenditure_Project1_other": data.cell_value(3, 3),  # D4 4行4列项目1本期增加其他
            "DevelopmentExpenditure_Project2_other": data.cell_value(4, 3),  # D5 5行4列项目2本期增加其他
            "DevelopmentExpenditure_Project3_other": data.cell_value(5, 3),  # D6 6行4列项目3本期增加其他
            "DevelopmentExpenditure_Project4_other": data.cell_value(6, 3),  # D7 7行4列项目4本期增加其他
            "DevelopmentExpenditure_Project5_other": data.cell_value(7, 3),  # D8 8行4列项目5本期增加其他
            "DevelopmentExpenditure_Total_other": data.cell_value(8, 3),  # D9 9行4列合计本期增加其他
            "DevelopmentExpenditure_Project1_confirm": data.cell_value(3, 4),  # E4 4行5列项目1本期减少确认为无形资产
            "DevelopmentExpenditure_Project2_confirm": data.cell_value(4, 4),  # E5 5行5列项目2本期减少确认为无形资产
            "DevelopmentExpenditure_Project3_confirm": data.cell_value(5, 4),  # E6 6行5列项目3本期减少确认为无形资产
            "DevelopmentExpenditure_Project4_confirm": data.cell_value(6, 4),  # E7 7行5列项目4本期减少确认为无形资产
            "DevelopmentExpenditure_Project5_confirm": data.cell_value(7, 4),  # E8 8行5列项目5本期减少确认为无形资产
            "DevelopmentExpenditure_Total_confirm": data.cell_value(8, 4),  # E9 9行5列合计本期减少确认为无形资产
            "DevelopmentExpenditure_Project1_into": data.cell_value(3, 5),  # F4 4行6列项目1本期减少转入当期损益
            "DevelopmentExpenditure_Project2_into": data.cell_value(4, 5),  # F5 5行6列项目2本期减少转入当期损益
            "DevelopmentExpenditure_Project3_into": data.cell_value(5, 5),  # F6 6行6列项目3本期减少转入当期损益
            "DevelopmentExpenditure_Project4_into": data.cell_value(6, 5),  # F7 7行6列项目4本期减少转入当期损益
            "DevelopmentExpenditure_Project5_into": data.cell_value(7, 5),  # F8 8行6列项目5本期减少转入当期损益
            "DevelopmentExpenditure_Total_into": data.cell_value(8, 5),  # F9 9行6列合计本期减少转入当期损益
            "DevelopmentExpenditure_Project1_this": data.cell_value(3, 6),  # G4 4行7列项目1期末余额
            "DevelopmentExpenditure_Project2_this": data.cell_value(4, 6),  # G5 5行7列项目2期末余额
            "DevelopmentExpenditure_Project3_this": data.cell_value(5, 6),  # G6 6行7列项目3期末余额
            "DevelopmentExpenditure_Project4_this": data.cell_value(6, 6),  # G7 7行7列项目4期末余额
            "DevelopmentExpenditure_Project5_this": data.cell_value(7, 6),  # G8 8行7列项目5期末余额
            "DevelopmentExpenditure_Total_this": data.cell_value(8, 6),  # G9 9行7列合计期末余额


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
        dic["DevelopmentExpenditure_Remark"] = data.cell_value(10, 1),  # B11 11行2列说明
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
        # 期初余额：项目1+项目2+项目3+项目4+项目5=合计
        if abs(df["DevelopmentExpenditure_Project1_last"].fillna(0).values + df["DevelopmentExpenditure_Project2_last"].fillna(0).values + df["DevelopmentExpenditure_Project3_last"].fillna(0).values + df["DevelopmentExpenditure_Project4_last"].fillna(0).values + df["DevelopmentExpenditure_Project5_last"].fillna(0).values - df["DevelopmentExpenditure_Total_last"].fillna(0).values) > 0.01:
            error = "期初余额：项目1+项目2+项目3+项目4+项目5<>合计"
            errorlist.append(error)
        # 内部开发支出：项目1+项目2+项目3+项目4+项目5=合计
        if abs(df["DevelopmentExpenditure_Project1_internal"].fillna(0).values + df["DevelopmentExpenditure_Project2_internal"].fillna(0).values + df["DevelopmentExpenditure_Project3_internal"].fillna(0).values + df["DevelopmentExpenditure_Project4_internal"].fillna(0).values + df["DevelopmentExpenditure_Project5_internal"].fillna(0).values - df["DevelopmentExpenditure_Total_internal"].fillna(0).values) > 0.01:
            error = "内部开发支出：项目1+项目2+项目3+项目4+项目5<>合计"
            errorlist.append(error)
        # 其他：项目1+项目2+项目3+项目4+项目5=合计
        if abs(df["DevelopmentExpenditure_Project1_other"].fillna(0).values + df["DevelopmentExpenditure_Project2_other"].fillna(0).values + df["DevelopmentExpenditure_Project3_other"].fillna(0).values + df["DevelopmentExpenditure_Project4_other"].fillna(0).values + df["DevelopmentExpenditure_Project5_other"].fillna(0).values - df["DevelopmentExpenditure_Total_other"].fillna(0).values) > 0.01:
            error = "其他：项目1+项目2+项目3+项目4+项目5<>合计"
            errorlist.append(error)
        # 确认为无形资产：项目1+项目2+项目3+项目4+项目5=合计
        if abs(df["DevelopmentExpenditure_Project1_confirm"].fillna(0).values + df["DevelopmentExpenditure_Project2_confirm"].fillna(0).values + df["DevelopmentExpenditure_Project3_confirm"].fillna(0).values + df["DevelopmentExpenditure_Project4_confirm"].fillna(0).values + df["DevelopmentExpenditure_Project5_confirm"].fillna(0).values - df["DevelopmentExpenditure_Total_confirm"].fillna(0).values) > 0.01:
            error = "确认为无形资产：项目1+项目2+项目3+项目4+项目5<>合计"
            errorlist.append(error)
        # 转入当期损益：项目1+项目2+项目3+项目4+项目5=合计
        if abs(df["DevelopmentExpenditure_Project1_into"].fillna(0).values + df["DevelopmentExpenditure_Project2_into"].fillna(0).values + df["DevelopmentExpenditure_Project3_into"].fillna(0).values + df["DevelopmentExpenditure_Project4_into"].fillna(0).values + df["DevelopmentExpenditure_Project5_into"].fillna(0).values - df["DevelopmentExpenditure_Total_into"].fillna(0).values) > 0.01:
            error = "转入当期损益：项目1+项目2+项目3+项目4+项目5<>合计"
            errorlist.append(error)
        # 期末余额：项目1+项目2+项目3+项目4+项目5=合计
        if abs(df["DevelopmentExpenditure_Project1_this"].fillna(0).values + df["DevelopmentExpenditure_Project2_this"].fillna(0).values + df["DevelopmentExpenditure_Project3_this"].fillna(0).values + df["DevelopmentExpenditure_Project4_this"].fillna(0).values + df["DevelopmentExpenditure_Project5_this"].fillna(0).values - df["DevelopmentExpenditure_Total_this"].fillna(0).values) > 0.01:
            error = "期末余额：项目1+项目2+项目3+项目4+项目5<>合计"
            errorlist.append(error)











        return df, errorlist


if __name__ == "__main__":
    d = GetDevelopmentExpenditure()