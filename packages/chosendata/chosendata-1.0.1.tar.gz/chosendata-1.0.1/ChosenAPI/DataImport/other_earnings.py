
import pandas as pd
from ChosenAPI.DataImport.ChangeToNum import ChangeData



class GetOtherEarnings(object):#其他收益
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
            "OtherEarnings_ReckonIn_CurrentPeriod": data.cell_value(2, 1),  # B3 3行2列政府补助计入本期发生额
            "OtherEarnings_SendBack_CurrentPeriod": data.cell_value(3, 1),  # B4 4行2列政府补助退回本期发生额
            "OtherEarnings_Total_CurrentPeriod": data.cell_value(4, 1),  # B5 5行2列合计本期发生额
            "OtherEarnings_ReckonIn_PriorPeriod": data.cell_value(2, 2),  # C3 3行3列政府补助计入上期发生额
            "OtherEarnings_SendBack_PriorPeriod": data.cell_value(3, 2),  # C4 4行3列政府补助退回上期发生额
            "OtherEarnings_Total_PriorPeriod": data.cell_value(4, 2),  # C5 5行3列合计上期发生额
            "OtherEarnings_ReckonIn_sum": data.cell_value(2, 3),  # D3 3行4列政府补助计入计入当期非经常性损益的金额
            "OtherEarnings_SendBack_sum": data.cell_value(3, 3),  # D4 4行4列政府补助退回计入当期非经常性损益的金额
            "OtherEarnings_Total_sum": data.cell_value(4, 3),  # D5 5行4列合计计入当期非经常性损益的金额


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
        dic["OtherEarnings_Remark"] = data.cell_value(6, 1),  # B7 7行2列说明
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
        # 本期发生额：政府补助计入+政府补助退回=合计
        if abs(df["OtherEarnings_ReckonIn_CurrentPeriod"].fillna(0).values + df["OtherEarnings_SendBack_CurrentPeriod"].fillna(0).values - df["OtherEarnings_Total_CurrentPeriod"].fillna(0).values) > 0.01:
            error = "本期发生额：政府补助计入+政府补助退回<>合计"
            errorlist.append(error)
        # 上期发生额：政府补助计入+政府补助退回=合计
        if abs(df["OtherEarnings_ReckonIn_PriorPeriod"].fillna(0).values + df["OtherEarnings_SendBack_PriorPeriod"].fillna(0).values - df["OtherEarnings_Total_PriorPeriod"].fillna(0).values) > 0.01:
            error = "上期发生额：政府补助计入+政府补助退回<>合计"
            errorlist.append(error)
        # 计入当期非经常性损益的金额：政府补助计入+政府补助退回=合计
        if abs(df["OtherEarnings_ReckonIn_sum"].fillna(0).values + df["OtherEarnings_SendBack_sum"].fillna(0).values - df["OtherEarnings_Total_sum"].fillna(0).values) > 0.01:
            error = "计入当期非经常性损益的金额：政府补助计入+政府补助退回<>合计"
            errorlist.append(error)

        return df, errorlist


if __name__ == "__main__":
    d = GetOtherEarnings()