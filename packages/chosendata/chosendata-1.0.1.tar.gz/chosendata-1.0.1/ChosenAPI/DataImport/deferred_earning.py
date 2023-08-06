
import pandas as pd
from ChosenAPI.DataImport.ChangeToNum import ChangeData



class GetDeferredEarning(object):#递延收益
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
            "DeferredEarning_Project1_last": data.cell_value(2, 1),  # B3 3行2列项目1期初余额
            "DeferredEarning_Project2_last": data.cell_value(3, 1),  # B4 4行2列项目2期初余额
            "DeferredEarning_Project3_last": data.cell_value(4, 1),  # B5 5行2列项目3期初余额
            "DeferredEarning_Project4_last": data.cell_value(5, 1),  # B6 6行2列项目4期初余额
            "DeferredEarning_Project5_last": data.cell_value(6, 1),  # B7 7行2列项目5期初余额
            "DeferredEarning_Total_last": data.cell_value(7, 1),  # B8 8行2列合计期初余额
            "DeferredEarning_Project1_add": data.cell_value(2, 2),  # C3 3行3列项目1本期增加
            "DeferredEarning_Project2_add": data.cell_value(3, 2),  # C4 4行3列项目2本期增加
            "DeferredEarning_Project3_add": data.cell_value(4, 2),  # C5 5行3列项目3本期增加
            "DeferredEarning_Project4_add": data.cell_value(5, 2),  # C6 6行3列项目4本期增加
            "DeferredEarning_Project5_add": data.cell_value(6, 2),  # C7 7行3列项目5本期增加
            "DeferredEarning_Total_add": data.cell_value(7, 2),  # C8 8行3列合计本期增加
            "DeferredEarning_Project1_reduce": data.cell_value(2, 3),  # D3 3行4列项目1本期减少
            "DeferredEarning_Project2_reduce": data.cell_value(3, 3),  # D4 4行4列项目2本期减少
            "DeferredEarning_Project3_reduce": data.cell_value(4, 3),  # D5 5行4列项目3本期减少
            "DeferredEarning_Project4_reduce": data.cell_value(5, 3),  # D6 6行4列项目4本期减少
            "DeferredEarning_Project5_reduce": data.cell_value(6, 3),  # D7 7行4列项目5本期减少
            "DeferredEarning_Total_reduce": data.cell_value(7, 3),  # D8 8行4列合计本期减少
            "DeferredEarning_Project1_this": data.cell_value(2, 4),  # E3 3行5列项目1期末余额
            "DeferredEarning_Project2_this": data.cell_value(3, 4),  # E4 4行5列项目2期末余额
            "DeferredEarning_Project3_this": data.cell_value(4, 4),  # E5 5行5列项目3期末余额
            "DeferredEarning_Project4_this": data.cell_value(5, 4),  # E6 6行5列项目4期末余额
            "DeferredEarning_Project5_this": data.cell_value(6, 4),  # E7 7行5列项目5期末余额
            "DeferredEarning_Total_this": data.cell_value(7, 4),  # E8 8行5列合计期末余额


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
        dic["DeferredEarning_Remark"] = data.cell_value(9, 1),  # B10 10行2列说明
        dic["DeferredEarning_Project1_reason"] = data.cell_value(2, 5),  # F3 3行6列项目1形成原因
        dic["DeferredEarning_Project2_reason"] = data.cell_value(3, 5),  # F4 4行6列项目2形成原因
        dic["DeferredEarning_Project3_reason"] = data.cell_value(4, 5),  # F5 5行6列项目3形成原因
        dic["DeferredEarning_Project4_reason"] = data.cell_value(5, 5),  # F6 6行6列项目4形成原因
        dic["DeferredEarning_Project5_reason"] = data.cell_value(6, 5),  # F7 7行6列项目5形成原因
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
        # 期初余额:项目1+项目2+项目3+项目4+项目5=合计
        if abs(df["DeferredEarning_Project1_last"].fillna(0).values + df["DeferredEarning_Project2_last"].fillna(0).values + df["DeferredEarning_Project3_last"].fillna(0).values + df["DeferredEarning_Project4_last"].fillna(0).values + df["DeferredEarning_Project5_last"].fillna(0).values - df["DeferredEarning_Total_last"].fillna(0).values) > 0.01:
            error = "期初余额:项目1+项目2+项目3+项目4+项目5<>合计"
            errorlist.append(error)
	# 本期增加:项目1+项目2+项目3+项目4+项目5=合计
        if abs(df["DeferredEarning_Project1_add"].fillna(0).values + df["DeferredEarning_Project2_add"].fillna(0).values + df["DeferredEarning_Project3_add"].fillna(0).values + df["DeferredEarning_Project4_add"].fillna(0).values + df["DeferredEarning_Project5_add"].fillna(0).values - df["DeferredEarning_Total_add"].fillna(0).values) > 0.01:
            error = "本期增加:项目1+项目2+项目3+项目4+项目5<>合计"
            errorlist.append(error)
	# 本期减少:项目1+项目2+项目3+项目4+项目5=合计
        if abs(df["DeferredEarning_Project1_reduce"].fillna(0).values + df["DeferredEarning_Project2_reduce"].fillna(0).values + df["DeferredEarning_Project3_reduce"].fillna(0).values + df["DeferredEarning_Project4_reduce"].fillna(0).values + df["DeferredEarning_Project5_reduce"].fillna(0).values - df["DeferredEarning_Total_reduce"].fillna(0).values) > 0.01:
            error = "本期减少:项目1+项目2+项目3+项目4+项目5<>合计"
            errorlist.append(error)
	# 期末余额:项目1+项目2+项目3+项目4+项目5=合计
        if abs(df["DeferredEarning_Project1_this"].fillna(0).values + df["DeferredEarning_Project2_this"].fillna(0).values + df["DeferredEarning_Project3_this"].fillna(0).values + df["DeferredEarning_Project4_this"].fillna(0).values + df["DeferredEarning_Project5_this"].fillna(0).values - df["DeferredEarning_Total_this"].fillna(0).values) > 0.01:
            error = "期末余额:项目1+项目2+项目3+项目4+项目5<>合计"
            errorlist.append(error)
        











        return df, errorlist


if __name__ == "__main__":
    d = GetDeferredEarning()