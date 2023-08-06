
import pandas as pd
from ChosenAPI.DataImport.ChangeToNum import ChangeData


class GetAdvancePeceipts(object):#预收账款
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
            "AdvancePeceipts_0_1_this": data.cell_value(3, 1),  # B4 4行2列预收款项列示项目1期末余额
            "AdvancePeceipts_1_2_this": data.cell_value(4, 1),  # B5 5行2列预收款项列示项目2期末余额
            "AdvancePeceipts_2_3_this": data.cell_value(5, 1),  # B6 6行2列预收款项列示项目3期末余额
            "AdvancePeceipts_3___this": data.cell_value(6, 1),  # B7 7行2列预收款项列示项目4期末余额

            "AdvancePeceipts_Total_this": data.cell_value(8, 1),  # B9 9行2列预收款项列示合计期末余额
            "AdvancePeceipts_0_1_last": data.cell_value(3, 2),  # C4 4行3列预收款项列示项目1期初余额
            "AdvancePeceipts_1_2_last": data.cell_value(4, 2),  # C5 5行3列预收款项列示项目2期初余额
            "AdvancePeceipts_2_3_last": data.cell_value(5, 2),  # C6 6行3列预收款项列示项目3期初余额
            "AdvancePeceipts_3___last": data.cell_value(6, 2),  # C7 7行3列预收款项列示项目4期初余额

            "AdvancePeceipts_Total_last": data.cell_value(8, 2),  # C9 9行3列预收款项列示合计期初余额
            "AdvancePeceipts_Project1_this": data.cell_value(12, 1),  # B13 13行2列账龄超过1年的重要预收款项项目1期末余额
            "AdvancePeceipts_Project2_this": data.cell_value(13, 1),  # B14 14行2列账龄超过1年的重要预收款项项目2期末余额
            "AdvancePeceipts_Project3_this": data.cell_value(14, 1),  # B15 15行2列账龄超过1年的重要预收款项项目3期末余额
            "AdvancePeceipts_Project4_this": data.cell_value(15, 1),  # B16 16行2列账龄超过1年的重要预收款项项目4期末余额
            "AdvancePeceipts_Project5_this": data.cell_value(16, 1),  # B17 17行2列账龄超过1年的重要预收款项项目5期末余额
            "AdvancePeceipts_TotalImportant_this": data.cell_value(17, 1),  # B18 18行2列账龄超过1年的重要预收款项合计期末余额
            "AdvancePeceipts_Cost_sum": data.cell_value(21, 1),  # B22 22行2列累计已发生成本金额
            "AdvancePeceipts_GrossMargin_sum": data.cell_value(22, 1),  # B23 23行2列累计已确认毛利金额
            "AdvancePeceipts_ExpectedLoss_sum": data.cell_value(23, 1),  # B24 24行2列减：预计损失金额
            "AdvancePeceipts_Sum_sum": data.cell_value(24, 1),  # B25 25行2列已办理结算的金额金额
            "AdvancePeceipts_Project_sum": data.cell_value(25, 1),  # B26 26行2列建造合同形成的已结算未完工项目金额


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
        dic["AdvancePeceipts_Remark"] = data.cell_value(27, 1),  # B28 28行2列说明
        dic["AdvancePeceipts_Project1_reason"] = data.cell_value(12, 2),  # C13 13行3列账龄超过1年的重要预收款项项目1未偿还或结转的原因
        dic["AdvancePeceipts_Project2_reason"] = data.cell_value(13, 2),  # C14 14行3列账龄超过1年的重要预收款项项目2未偿还或结转的原因
        dic["AdvancePeceipts_Project3_reason"] = data.cell_value(14, 2),  # C15 15行3列账龄超过1年的重要预收款项项目3未偿还或结转的原因
        dic["AdvancePeceipts_Project4_reason"] = data.cell_value(15, 2),  # C16 16行3列账龄超过1年的重要预收款项项目4未偿还或结转的原因
        dic["AdvancePeceipts_Project5_reason"] = data.cell_value(16, 2),  # C17 17行3列账龄超过1年的重要预收款项项目5未偿还或结转的原因
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
        # 预收款项列示期末余额：项目1+项目2+项目3+项目4+项目5=合计
        if abs(df["AdvancePeceipts_0_1_this"].fillna(0).values + df["AdvancePeceipts_1_2_this"].fillna(0).values + df["AdvancePeceipts_2_3_this"].fillna(0).values + df["AdvancePeceipts_3___this"].fillna(0).values - df["AdvancePeceipts_Total_this"].fillna(0).values) > 0.01:
            error = "预收款项列示期末余额：项目1+项目2+项目3+项目4+项目5<>合计"
            errorlist.append(error)
	    # 预收款项列示期初余额：项目1+项目2+项目3+项目4+项目5=合计
        if abs(df["AdvancePeceipts_0_1_last"].fillna(0).values + df["AdvancePeceipts_1_2_last"].fillna(0).values + df["AdvancePeceipts_2_3_last"].fillna(0).values + df["AdvancePeceipts_3___last"].fillna(0).values - df["AdvancePeceipts_Total_last"].fillna(0).values) > 0.01:
            error = "预收款项列示期末余额：项目1+项目2+项目3+项目4+项目5<>合计"
            errorlist.append(error)
        # 账龄超过1年的重要预收款项期末余额：项目1+项目2+项目3+项目4+项目5=合计
        if abs(df["AdvancePeceipts_Project1_this"].fillna(0).values + df["AdvancePeceipts_Project2_this"].fillna(0).values + df["AdvancePeceipts_Project3_this"].fillna(0).values + df["AdvancePeceipts_Project4_this"].fillna(0).values + df["AdvancePeceipts_Project5_this"].fillna(0).values - df["AdvancePeceipts_TotalImportant_this"].fillna(0).values) > 0.01:
            error = "账龄超过1年的重要预收款项期末余额：项目1+项目2+项目3+项目4+项目5<>合计"
            errorlist.append(error)











        return df, errorlist


if __name__ == "__main__":
    d = GetAdvancePeceipts()