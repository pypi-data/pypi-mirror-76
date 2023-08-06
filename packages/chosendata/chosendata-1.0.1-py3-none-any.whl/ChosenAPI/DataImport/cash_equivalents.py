
import pandas as pd
from ChosenAPI.DataImport.ChangeToNum import ChangeData



class GetCashEquivalents(object):#货币资金
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
            "CashEquivalents_CashOnHand_this": data.cell_value(3, 1),  # B4 4行2列#库存现金期末余额
            "CashEquivalents_BankDeposits_this": data.cell_value(4, 1),  # B5 5行2列#银行存款期末余额
            "CashEquivalents_OtherCurrencyFunds_this": data.cell_value(5, 1),  # B6 6行2列#其他货币资金期末余额
            "CashEquivalents_Total_this": data.cell_value(6, 1),  # B7 7行2列#合计期末余额
            "CashEquivalents_TotalAmountOfMoneyDepositedAbroad_this": data.cell_value(7, 1),# B8 8行2列#其中：存放在境外的款项总额期末余额
            "CashEquivalents_CashOnHand_last": data.cell_value(3, 2),  # C4 4行3列#库存现金期初余额
            "CashEquivalents_BankDeposits_last": data.cell_value(4, 2),  # C5 5行3列#银行存款期初余额
            "CashEquivalents_OtherCurrencyFunds_last": data.cell_value(5, 2),  # C6 6行3列#其他货币资金期初余额
            "CashEquivalents_Total_last": data.cell_value(6, 2),  # C7 7行3列#合计期初余额
            "CashEquivalents_TotalAmountOfMoneyDepositedAbroad_last": data.cell_value(7, 2),# C8 8行3列#其中：存放在境外的款项总额期初余额
            "CashEquivalents_limited_this": data.cell_value(8, 1),  # B9 9行2列#受限期末余额
            "CashEquivalents_limited_last": data.cell_value(8, 2),  # C9 9行3列#受限期初余额
            

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
        dic["CashEquivalents_Remark"] = data.cell_value(9, 1),  # B11 11行2列#说明
        dic["ID"] = identify,  # 实例ID号
        dic["username"] = username,  # 用户名
        df = pd.DataFrame(dic, index=[0])  # 打包成DataFram

        return df


    def CheckError(self, df):
        """
        货币资金数据逻辑关系核对
        :param df:
        :return:
        """
        # 建立错误空列表：
        errorlist = []
        # 库存现金+银行存款+其他货币资金=合计
        if abs(df["CashEquivalents_CashOnHand_this"].fillna(0).values + df["CashEquivalents_BankDeposits_this"].fillna(0).values + df["CashEquivalents_OtherCurrencyFunds_this"].fillna(0).values - df["CashEquivalents_Total_this"].fillna(0).values) > 0.01:
            error = "货币资金:期末库存现金+期末银行存款+期末其他货币资金<>期末合计"
            errorlist.append(error)
        if abs(df["CashEquivalents_CashOnHand_last"].fillna(0).values + df["CashEquivalents_BankDeposits_last"].fillna(0).values + df["CashEquivalents_OtherCurrencyFunds_last"].fillna(0).values - df["CashEquivalents_Total_last"].fillna(0).values) > 0.01:
            error = "货币资金:期初库存现金+期初银行存款+期初其他货币资金<>期初合计"
            errorlist.append(error)
        











        return df, errorlist


if __name__ == "__main__":
    d = GetCashEquivalents()