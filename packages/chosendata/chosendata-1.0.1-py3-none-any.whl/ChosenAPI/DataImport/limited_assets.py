
import pandas as pd
from ChosenAPI.DataImport.ChangeToNum import ChangeData



class GetLimitedAssets(object):#受限资产
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
            "LimitedAssets_CashEquivalents_this": data.cell_value(3, 1),  # B4 4行2列货币资金期末账面价值
            "LimitedAssets_BillReceivable_this": data.cell_value(4, 1),  # B5 5行2列应收票据期末账面价值
            "LimitedAssets_Inventories_this": data.cell_value(5, 1),  # B6 6行2列存货期末账面价值
            "LimitedAssets_FixedAssets_this": data.cell_value(6, 1),  # B7 7行2列固定资产期末账面价值
            "LimitedAssets_IntangibleAssets_this": data.cell_value(7, 1),  # B8 8行2列无形资产期末账面价值
            "LimitedAssets_Other_this": data.cell_value(8, 1),  # B9 9行2列其他期末账面价值
            "LimitedAssets_Total_this": data.cell_value(9, 1),  # B10 10行2列合计期末账面价值


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
        dic["LimitedAssets_Remark"] = data.cell_value(11, 1),  # B12 12行2列说明
        dic["LimitedAssets_CashEquivalents_reason"] = data.cell_value(3, 2),  # C4 4行3列货币资金受限原因
        dic["LimitedAssets_BillReceivable_reason"] = data.cell_value(4, 2),  # C5 5行3列应收票据受限原因
        dic["LimitedAssets_Inventories_reason"] = data.cell_value(5, 2),  # C6 6行3列存货受限原因
        dic["LimitedAssets_FixedAssets_reason"] = data.cell_value(6, 2),  # C7 7行3列固定资产受限原因
        dic["LimitedAssets_IntangibleAssets_reason"] = data.cell_value(7, 2),  # C8 8行3列无形资产受限原因
        dic["LimitedAssets_Other_reason"] = data.cell_value(8, 2),  # C9 9行3列其他受限原因
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
        # 期末账面价值:货币资金+应收票据+存货+固定资产+无形资产+其他=合计
        if abs(df["LimitedAssets_CashEquivalents_this"].fillna(0).values + df["LimitedAssets_BillReceivable_this"].fillna(0).values + df["LimitedAssets_Inventories_this"].fillna(0).values + df["LimitedAssets_FixedAssets_this"].fillna(0).values + df["LimitedAssets_IntangibleAssets_this"].fillna(0).values + df["LimitedAssets_Other_this"].fillna(0).values - df["LimitedAssets_Total_this"].fillna(0).values) > 0.01:
            error = "期末账面价值:货币资金+应收票据+存货+固定资产+无形资产+其他<>合计"
            errorlist.append(error)
        











        return df, errorlist


if __name__ == "__main__":
    d = GetLimitedAssets()