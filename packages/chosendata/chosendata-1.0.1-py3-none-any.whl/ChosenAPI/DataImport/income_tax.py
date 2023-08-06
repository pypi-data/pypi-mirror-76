
import pandas as pd
from ChosenAPI.DataImport.ChangeToNum import ChangeData



class GetIncomeTax(object):#所得税费用
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
            "IncomeTax_CurrentPeriod_CurrentPeriod": data.cell_value(3, 1),  # B4 4行2列当期所得税费用本期发生额
            "IncomeTax_Deferred_CurrentPeriod": data.cell_value(4, 1),  # B5 5行2列递延所得税费用本期发生额
            "IncomeTax_Total_CurrentPeriod": data.cell_value(5, 1),  # B6 6行2列合计本期发生额
            "IncomeTax_CurrentPeriod_PriorPeriod": data.cell_value(3, 2),  # C4 4行3列当期所得税费用上期发生额
            "IncomeTax_Deferred_PriorPeriod": data.cell_value(4, 2),  # C5 5行3列递延所得税费用上期发生额
            "IncomeTax_Total_PriorPeriod": data.cell_value(5, 2),  # C6 6行3列合计上期发生额
            "IncomeTax_TotalProfit_CurrentPeriod": data.cell_value(9, 1),  # B10 10行2列利润总额本期发生额
            "IncomeTax_Statutory_CurrentPeriod": data.cell_value(10, 1),  # B11 11行2列按法定/适用税率计算的所得税费用本期发生额
            "IncomeTax_Subsidiary_CurrentPeriod": data.cell_value(11, 1),  # B12 12行2列子公司适用不同税率的影响本期发生额
            "IncomeTax_Adjust_CurrentPeriod": data.cell_value(12, 1),  # B13 13行2列调整以前期间所得税的影响本期发生额
            "IncomeTax_Non-TaxableIncome_CurrentPeriod": data.cell_value(13, 1),  # B14 14行2列非应税收入的影响本期发生额
            "IncomeTax_Non-Deductible_CurrentPeriod": data.cell_value(14, 1),  # B15 15行2列不可抵扣的成本、费用和损失的影响本期发生额
            "IncomeTax_DeductibleLoss_CurrentPeriod": data.cell_value(15, 1),  # B16 16行2列使用前期未确认递延所得税资产的可抵扣亏损的影响本期发生额
            "IncomeTax_TemporaryDifference_CurrentPeriod": data.cell_value(16, 1),# B17 17行2列本期未确认递延所得税资产的可抵扣暂时性差异或可抵扣亏损的影响本期发生额
            "IncomeTax_Other_CurrentPeriod": data.cell_value(17, 1),  # B18 18行2列其他本期发生额
            "IncomeTax_IncomeTax_CurrentPeriod": data.cell_value(18, 1),  # B19 19行2列所得税费用本期发生额


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
        dic["IncomeTax_Remark"] = data.cell_value(20, 1),  # B21 21行2列说明
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
        # 本期发生额:当期所得税费用+递延所得税费用=合计
        if abs(df["IncomeTax_CurrentPeriod_CurrentPeriod"].fillna(0).values + df["IncomeTax_Deferred_CurrentPeriod"].fillna(0).values - df["IncomeTax_Total_CurrentPeriod"].fillna(0).values) > 0.01:
            error = "本期发生额:当期所得税费用+递延所得税费用<>合计"
            errorlist.append(error)
        # 上期发生额:当期所得税费用+递延所得税费用=合计
        if abs(df["IncomeTax_CurrentPeriod_PriorPeriod"].fillna(0).values + df["IncomeTax_Deferred_PriorPeriod"].fillna(0).values - df["IncomeTax_Total_PriorPeriod"].fillna(0).values) > 0.01:
            error = "上期发生额:当期所得税费用+递延所得税费用<>合计"
            errorlist.append(error)

        return df, errorlist


if __name__ == "__main__":
    d = GetIncomeTax()