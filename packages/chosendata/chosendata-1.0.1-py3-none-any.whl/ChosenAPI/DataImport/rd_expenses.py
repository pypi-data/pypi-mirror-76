
import pandas as pd
import numpy as np
from ChosenAPI.DataImport.ChangeToNum import ChangeData



class GetRdExpenses(object):#研发费用
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
        start, end = 2, 3
        change = ChangeData()
        i = 0
        while i < 41:  # 最大到40行,利用while循环遍历找到起点和终点,但一定要从第二行开始,列数定义为第一列
            i += 1
            if change.Changing(data.cell_value(i, 0)) == "项目": # 定义采集起点
                start = i + 1
                # print(start)

            if change.Changing(data.cell_value(i, 0)) == "合计": # 定义采集终点
                end = i
                # print(end)
                break

        datalist = []
        for i in range(start, end):
            if data.cell_value(i, 0):
                account_name = data.cell_value(i, 0)
                end_value = change.Changing(data.cell_value(i, 1))
                initial_value = change.Changing(data.cell_value(i, 2))
                remark = change.Changing(data.cell_value(i, 3))
                dic = {
                    "ID": identify,
                    "username": username,
                    "account_name": account_name,
                    "end_value": end_value,
                    "initial_value": initial_value,
                    "remark": remark,
                }
                datalist.append(dic)

        df = pd.DataFrame(datalist)
        if len(df) > 0:
            end_total = df["end_value"].sum()
            initial_total = df["initial_value"].sum()
            df["end_ratio"] = df["end_value"]/end_total  # 期末各明细占总金额比例
            df["initial_ratio"] = df["initial_value"]/initial_total  # 期初各明细占总金额比例
            df["value_change_ratio"] = (df["end_value"] - df["initial_value"])/df["initial_value"] # 各科目金额变动
            df["inner_ratio_change"] = df["end_ratio"] - df["initial_ratio"]
            df = df.fillna(0)
            df.replace(-np.inf, -1, inplace=True)
            df.replace(np.inf, 1, inplace=True)
            df = df.drop(df[(df.end_value == 0) & (df.initial_value == 0)].index)
        else:
            pass
        # print(df)
        return df


    def CheckError(self, df):
        """
        资产负债表数据逻辑关系核对
        :param df:
        :return:
        """
        # 建立错误空列表：
        errorlist = []
        if len(df) == 0:
            error = "研发费用明细表未填写,请核查.如果该科目没有数据可忽略"
            errorlist.append(error)
        return df, errorlist


if __name__ == "__main__":
    d = GetRdExpenses()