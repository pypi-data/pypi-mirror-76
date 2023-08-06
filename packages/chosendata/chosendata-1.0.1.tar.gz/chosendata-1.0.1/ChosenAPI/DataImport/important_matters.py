
import pandas as pd
from ChosenAPI.DataImport.ChangeToNum import ChangeData



class GetImportantMatters(object):#重大事项
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
            "ImportantMatters_Guarantee_matters1_sum": data.cell_value(3, 2),  # C4 4行3列#担保事项1金额
            "ImportantMatters_Guarantee_matters2_sum": data.cell_value(4, 2),  # C5 5行3列#担保事项2金额
            "ImportantMatters_Guarantee_matters3_sum": data.cell_value(5, 2),  # C6 6行3列#担保事项3金额
            "ImportantMatters_Guarantee_matters4_sum": data.cell_value(6, 2),  # C7 7行3列#担保事项4金额
            "ImportantMatters_Guarantee_matters5_sum": data.cell_value(7, 2),  # C8 8行3列#担保事项5金额
            "ImportantMatters_Guarantee_Total_sum": data.cell_value(8, 2),  # C9 9行3列#担保合计金额


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
        dic["ImportantMatters_Guarantee_Remark"] = data.cell_value(10, 1),  # B11 11行2列说明
        dic["ImportantMatters_Guarantee_matters1_WhetherTheGuarantee"] = data.cell_value(3, 1),  # B4 4行2列#担保事项1是否担保
        dic["ImportantMatters_Guarantee_matters2_WhetherTheGuarantee"] = data.cell_value(4, 1),  # B5 5行2列#担保事项2是否担保
        dic["ImportantMatters_Guarantee_matters3_WhetherTheGuarantee"] = data.cell_value(5, 1),  # B6 6行2列#担保事项3是否担保
        dic["ImportantMatters_Guarantee_matters4_WhetherTheGuarantee"] = data.cell_value(6, 1),  # B7 7行2列#担保事项4是否担保
        dic["ImportantMatters_Guarantee_matters5_WhetherTheGuarantee"] = data.cell_value(7, 1),  # B8 8行2列#担保事项5是否担保
        dic["ImportantMatters_Guarantee_matters1_note"] = data.cell_value(3, 3),  # D4 4行4列#担保事项1备注
        dic["ImportantMatters_Guarantee_matters2_note"] = data.cell_value(4, 3),  # D5 5行4列#担保事项2备注
        dic["ImportantMatters_Guarantee_matters3_note"] = data.cell_value(5, 3),  # D6 6行4列#担保事项3备注
        dic["ImportantMatters_Guarantee_matters4_note"] = data.cell_value(6, 3),  # D7 7行4列#担保事项4备注
        dic["ImportantMatters_Guarantee_matters5_note"] = data.cell_value(7, 3),  # D8 8行4列#担保事项5备注
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
        # 担保金额合计：事项1+事项2+事项3+事项4+事项5=合计
        if abs(df["ImportantMatters_Guarantee_matters1_sum"].fillna(0).values + df["ImportantMatters_Guarantee_matters2_sum"].fillna(0).values + df["ImportantMatters_Guarantee_matters3_sum"].fillna(0).values + df["ImportantMatters_Guarantee_matters4_sum"].fillna(0).values + df["ImportantMatters_Guarantee_matters5_sum"].fillna(0).values - df["ImportantMatters_Guarantee_Total_sum"].fillna(0).values) > 0.01:
            error = "担保金额合计：事项1+事项2+事项3+事项4+事项5<>合计"
            errorlist.append(error)
        











        return df, errorlist




if __name__ == "__main__":
    d = GetImportantMatters()