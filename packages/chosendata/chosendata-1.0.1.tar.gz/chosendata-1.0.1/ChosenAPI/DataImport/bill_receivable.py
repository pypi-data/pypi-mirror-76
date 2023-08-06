
import pandas as pd
from ChosenAPI.DataImport.ChangeToNum import ChangeData



class GetBillReceivable(object):#应收票据
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
            "BillReceivable_BankList_this": data.cell_value(3, 1),  # B 4行2列银行承兑汇票期末余额
            "BillReceivable_TradeList_this": data.cell_value(4, 1),  # B 5行2列商业承兑汇票期末余额
            "BillReceivable_OtherList_this": data.cell_value(5, 1),  # B 6行2列其他票据期末余额
            "BillReceivable_TotalList_this": data.cell_value(6, 1),  # B 7行2列合计期末余额
            "BillReceivable_Bank_pledge": data.cell_value(10, 1),  # B 11行2列银行承兑汇票期末已质押金额
            "BillReceivable_Trade_pledge": data.cell_value(11, 1),  # B 12行2列商业承兑汇票期末已质押金额
            "BillReceivable_Other_pledge": data.cell_value(12, 1),  # B 13行2列其他票据期末已质押金额
            "BillReceivable_Total_pledge": data.cell_value(13, 1),  # B 14行2列合计期末已质押金额
            "BillReceivable_Bank_this": data.cell_value(17, 1),  # B 18行2列银行承兑汇票期末余额
            "BillReceivable_Trade_this": data.cell_value(18, 1),  # B 19行2列商业承兑汇票期末余额
            "BillReceivable_Other_this": data.cell_value(19, 1),  # B 20行2列其他票据期末余额
            "BillReceivable_Total_this": data.cell_value(20, 1),  # B 21行2列合计期末余额
            "BillReceivable_Bank_turn": data.cell_value(24, 1),  # B 25行2列银行承兑汇票期末转应收账款金额
            "BillReceivable_Trade_turn": data.cell_value(25, 1),  # B 26行2列商业承兑汇票
            "BillReceivable_Other_turn": data.cell_value(26, 1),  # B 27行2列其他票据
            "BillReceivable_Total_turn": data.cell_value(27, 1),  # B 28行2列合计
            "BillReceivable_BankList_last": data.cell_value(3, 2),  # C 4行3列银行承兑汇票期初余额
            "BillReceivable_TradeList_last": data.cell_value(4, 2),  # C 5行3列商业承兑汇票期初余额
            "BillReceivable_OtherList_last": data.cell_value(5, 2),  # C 6行3列其他票据期初余额
            "BillReceivable_TotalList_last": data.cell_value(6, 2),  # C 7行3列合计期初余额
            "BillReceivable_Bank_sum": data.cell_value(17, 2),# C 18行3列银行承兑汇票期末未终止确认金额
            "BillReceivable_Trade_sum": data.cell_value(18, 2),# C 19行3列商业承兑汇票期末未终止确认金额
            "BillReceivable_Other_sum": data.cell_value(19, 2),# C 20行3列其他票据期末未终止确认金额
            "BillReceivable_Total_sum": data.cell_value(20, 2),# C 21行3列合计期末未终止确认金额


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
        dic["BillReceivable_Remark"] = data.cell_value(29, 1),  # B 30行2列说明"
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
        # 银行承兑汇票+商业承兑汇票+其他票据=合计
        if abs(df["BillReceivable_BankList_this"].fillna(0).values + df["BillReceivable_TradeList_this"].fillna(0).values + df["BillReceivable_OtherList_this"].fillna(0).values - df["BillReceivable_TotalList_this"].fillna(0).values) > 0.01:
            error = "应收票据分类列示期末余额:银行承兑汇票+商业承兑汇票+其他票据<>合计"
            errorlist.append(error)
        if abs(df["BillReceivable_BankList_last"].fillna(0).values + df["BillReceivable_TradeList_last"].fillna(0).values + df["BillReceivable_OtherList_last"].fillna(0).values - df["BillReceivable_TotalList_last"].fillna(0).values) > 0.01:
            error = "应收票据分类列示期初余额:银行承兑汇票+商业承兑汇票+其他票据<>合计"
            errorlist.append(error)
        if abs(df["BillReceivable_Bank_pledge"].fillna(0).values + df["BillReceivable_Trade_pledge"].fillna(0).values + df["BillReceivable_Other_pledge"].fillna(0).values - df["BillReceivable_Total_pledge"].fillna(0).values) > 0.01:
            error = "期末公司已质押的应收票据期末已质押金额:银行承兑汇票+商业承兑汇票+其他票据<>合计"
            errorlist.append(error)
        if abs(df["BillReceivable_Bank_this"].fillna(0).values + df["BillReceivable_Trade_this"].fillna(0).values + df["BillReceivable_Other_this"].fillna(0).values - df["BillReceivable_Total_this"].fillna(0).values) > 0.01:
            error = "期末公司已背书或贴现且在资产负债表日尚未到期的应收票据期末余额:银行承兑汇票+商业承兑汇票+其他票据<>合计"
            errorlist.append(error)
        if abs(df["BillReceivable_Bank_sum"].fillna(0).values + df["BillReceivable_Trade_sum"].fillna(0).values + df["BillReceivable_Other_sum"].fillna(0).values - df["BillReceivable_Total_sum"].fillna(0).values) > 0.01:
            error = "期末公司已背书或贴现且在资产负债表日尚未到期的应收票据期末未终止确认金额:银行承兑汇票+商业承兑汇票+其他票据<>合计"
            errorlist.append(error)
        if abs(df["BillReceivable_Bank_turn"].fillna(0).values + df["BillReceivable_Trade_turn"].fillna(0).values + df["BillReceivable_Other_turn"].fillna(0).values - df["BillReceivable_Total_turn"].fillna(0).values) > 0.01:
            error = "期末公司因出票人未履约而将其转应收账款的票据期末转应收账款金额:银行承兑汇票+商业承兑汇票+其他票据<>合计"
            errorlist.append(error)

        











        return df, errorlist


if __name__ == "__main__":
    d = GetBillReceivable()