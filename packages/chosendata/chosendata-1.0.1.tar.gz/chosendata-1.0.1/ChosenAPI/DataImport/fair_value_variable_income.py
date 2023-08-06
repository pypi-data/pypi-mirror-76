
import pandas as pd
from ChosenAPI.DataImport.ChangeToNum import ChangeData



class GetFairValueVariableIncome(object):#公允价值变动损益
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
            "FairValueVariableIncome_Trading_Assets_CurrentPeriod": data.cell_value(2, 1),# B3 3行2列以公允价值计量的且其变动计入当期损益的金融资产本期发生额
            "FairValueVariableIncome_DerivativeInstruments_CurrentPeriod": data.cell_value(3, 1),# B4 4行2列其中：衍生金融工具产生的公允价值变动收益本期发生额
            "FairValueVariableIncome_Trading_Liability_CurrentPeriod": data.cell_value(4, 1),# B5 5行2列以公允价值计量的且其变动计入当期损益的金融负债本期发生额
            "FairValueVariableIncome_Investment_Property_CurrentPeriod": data.cell_value(5, 1),# B6 6行2列按公允价值计量的投资性房地产本期发生额
            "FairValueVariableIncome_Other_CurrentPeriod": data.cell_value(6, 1),  # B7 7行2列其他本期发生额
            "FairValueVariableIncome_Total_CurrentPeriod": data.cell_value(7, 1),  # B8 8行2列合计本期发生额
            "FairValueVariableIncome_Trading_Assets_PriorPeriod": data.cell_value(2, 2),# C3 3行3列以公允价值计量的且其变动计入当期损益的金融资产上期发生额
            "FairValueVariableIncome_DerivativeInstruments_PriorPeriod": data.cell_value(3, 2),# C4 4行3列其中：衍生金融工具产生的公允价值变动收益上期发生额
            "FairValueVariableIncome_Trading_Liability_PriorPeriod": data.cell_value(4, 2),# C5 5行3列以公允价值计量的且其变动计入当期损益的金融负债上期发生额
            "FairValueVariableIncome_Investment_Property_PriorPeriod": data.cell_value(5, 2),# C6 6行3列按公允价值计量的投资性房地产上期发生额
            "FairValueVariableIncome_Other_PriorPeriod": data.cell_value(6, 2),  # C7 7行3列其他上期发生额
            "FairValueVariableIncome_Total_PriorPeriod": data.cell_value(7, 2),  # C8 8行3列合计上期发生额


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
        dic["FairValueVariableIncome_Remark"] = data.cell_value(9, 1),  # B10 10行2列说明
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
        #本期发生额：以公允价值计量的且其变动计入当期损益的金融资产+以公允价值计量的且其变动计入当期损益的金融负债+按公允价值计量的投资性房地产+其他=合计
        if abs(df["FairValueVariableIncome_Trading_Assets_CurrentPeriod"].fillna(0).values + df["FairValueVariableIncome_Trading_Liability_CurrentPeriod"].fillna(0).values + df["FairValueVariableIncome_Investment_Property_CurrentPeriod"].fillna(0).values + df["FairValueVariableIncome_Other_CurrentPeriod"].fillna(0).values - df["FairValueVariableIncome_Total_CurrentPeriod"].fillna(0).values) > 0.01:
            error = "本期发生额：以公允价值计量的且其变动计入当期损益的金融资产+以公允价值计量的且其变动计入当期损益的金融负债+按公允价值计量的投资性房地产+其他<>合计"
            errorlist.append(error)
        #上期发生额：以公允价值计量的且其变动计入当期损益的金融资产+以公允价值计量的且其变动计入当期损益的金融负债+按公允价值计量的投资性房地产+其他=合计
        if abs(df["FairValueVariableIncome_Trading_Assets_PriorPeriod"].fillna(0).values + df["FairValueVariableIncome_Trading_Liability_PriorPeriod"].fillna(0).values + df["FairValueVariableIncome_Investment_Property_PriorPeriod"].fillna(0).values + df["FairValueVariableIncome_Other_PriorPeriod"].fillna(0).values - df["FairValueVariableIncome_Total_PriorPeriod"].fillna(0).values) > 0.01:
            error = "上期发生额：以公允价值计量的且其变动计入当期损益的金融资产+以公允价值计量的且其变动计入当期损益的金融负债+按公允价值计量的投资性房地产+其他<>合计"
            errorlist.append(error)
        











        return df, errorlist


if __name__ == "__main__":
    d = GetFairValueVariableIncome()