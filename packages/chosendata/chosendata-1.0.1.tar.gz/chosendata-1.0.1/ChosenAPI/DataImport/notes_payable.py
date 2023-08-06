
import pandas as pd
from ChosenAPI.DataImport.ChangeToNum import ChangeData



class GetNotesPayable(object):#应付票据
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
            "NotesPayable_Bank_this": data.cell_value(3, 1),  # B4 4行2列银行承兑汇票期末余额
            "NotesPayable_Business_this": data.cell_value(4, 1),  # B5 5行2列商业承兑汇票期末余额
            "NotesPayable_Total_this": data.cell_value(5, 1),  # B6 6行2列合计期末余额
            "NotesPayable_Bank_last": data.cell_value(3, 2),  # C4 4行3列银行承兑汇票期初余额
            "NotesPayable_Business_last": data.cell_value(4, 2),  # C5 5行3列商业承兑汇票期初余额
            "NotesPayable_Total_last": data.cell_value(5, 2),  # C6 6行3列合计期初余额


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
        dic["NotesPayable_Remark"] = data.cell_value(7, 1),  # B8 8行2列说明
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
        # 期末余额:银行承兑汇票+商业承兑汇票=合计
        if abs(df["NotesPayable_Bank_this"].fillna(0).values + df["NotesPayable_Business_this"].fillna(0).values - df["NotesPayable_Total_this"].fillna(0).values) > 0.01:
            error = "期末余额:银行承兑汇票+商业承兑汇票<>合计"
            errorlist.append(error)
	    # 期初余额:银行承兑汇票+商业承兑汇票=合计
        if abs(df["NotesPayable_Bank_last"].fillna(0).values + df["NotesPayable_Business_last"].fillna(0).values - df["NotesPayable_Total_last"].fillna(0).values) > 0.01:
            error = "期初余额:银行承兑汇票+商业承兑汇票<>合计"
            errorlist.append(error)

        return df, errorlist


if __name__ == "__main__":
    d = GetNotesPayable()