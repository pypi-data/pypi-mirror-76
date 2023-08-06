
import pandas as pd
from ChosenAPI.DataImport.ChangeToNum import ChangeData



class GetInterestPayable(object):#应付利息
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
            "InterestPayable_LongTermLoanInterest_this": data.cell_value(3, 1),  # B4 4行2列分期付息到期还本的长期借款利息期末余额
            "InterestPayable_CorporateBonds_this": data.cell_value(4, 1),  # B5 5行2列企业债券利息期末余额
            "InterestPayable_ShortTermBorrowing_this": data.cell_value(5, 1),  # B6 6行2列短期借款应付利息期末余额
            "InterestPayable_Division_this": data.cell_value(6, 1),  # B7 7行2列划分为金融负债的优先股/永续债利息期末余额
            "InterestPayable_Tool1_this": data.cell_value(7, 1),  # B8 8行2列工具1期末余额
            "InterestPayable_Tool2_this": data.cell_value(8, 1),  # B9 9行2列工具2期末余额
            "InterestPayable_Total_this": data.cell_value(9, 1),  # B10 10行2列合计期末余额
            "InterestPayable_LongTermLoanInterest_last": data.cell_value(3, 2),  # C4 4行3列分期付息到期还本的长期借款利息期初余额
            "InterestPayable_CorporateBonds_last": data.cell_value(4, 2),  # C5 5行3列企业债券利息期初余额
            "InterestPayable_ShortTermBorrowing_last": data.cell_value(5, 2),  # C6 6行3列短期借款应付利息期初余额
            "InterestPayable_Division_last": data.cell_value(6, 2),  # C7 7行3列划分为金融负债的优先股/永续债利息期初余额
            "InterestPayable_Tool1_last": data.cell_value(7, 2),  # C8 8行3列工具1期初余额
            "InterestPayable_Tool2_last": data.cell_value(8, 2),  # C9 9行3列工具2期初余额
            "InterestPayable_Total_last": data.cell_value(9, 2),  # C10 10行3列合计期初余额
            "InterestPayable_Company1_this": data.cell_value(13, 1),  # B14 14行2列公司1期末余额
            "InterestPayable_Company2_this": data.cell_value(14, 1),  # B15 15行2列公司2期末余额
            "InterestPayable_Company3_this": data.cell_value(15, 1),  # B16 16行2列公司3期末余额
            "InterestPayable_Company4_this": data.cell_value(16, 1),  # B17 17行2列公司4期末余额
            "InterestPayable_Company5_this": data.cell_value(17, 1),  # B18 18行2列公司5期末余额
            "InterestPayable_TotalImportant_this": data.cell_value(18, 1),  # B19 19行2列合计期末余额


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
        dic["InterestPayable_Remark"] = data.cell_value(20, 1),  # B21 21行2列说明
        dic["InterestPayable_Company1_reason"] = data.cell_value(13, 2),  # C14 14行3列公司1逾期原因
        dic["InterestPayable_Company2_reason"] = data.cell_value(14, 2),  # C15 15行3列公司2逾期原因
        dic["InterestPayable_Company3_reason"] = data.cell_value(15, 2),  # C16 16行3列公司3逾期原因
        dic["InterestPayable_Company4_reason"] = data.cell_value(16, 2),  # C17 17行3列公司4逾期原因
        dic["InterestPayable_Company5_reason"] = data.cell_value(17, 2),  # C18 18行3列公司5逾期原因
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
        # 期末余额:分期付息到期还本的长期借款利息+企业债券利息+短期借款应付利息+划分为金融负债的优先股/永续债利息=合计
        if abs(df["InterestPayable_LongTermLoanInterest_this"].fillna(0).values + df["InterestPayable_CorporateBonds_this"].fillna(0).values + df["InterestPayable_ShortTermBorrowing_this"].fillna(0).values + df["InterestPayable_Division_this"].fillna(0).values - df["InterestPayable_Total_this"].fillna(0).values) > 0.01:
            error = "期末余额:分期付息到期还本的长期借款利息+企业债券利息+短期借款应付利息+划分为金融负债的优先股/永续债利息<>合计"
            errorlist.append(error)
	# 期初余额:分期付息到期还本的长期借款利息+企业债券利息+短期借款应付利息+划分为金融负债的优先股/永续债利息=合计
        if abs(df["InterestPayable_LongTermLoanInterest_last"].fillna(0).values + df["InterestPayable_CorporateBonds_last"].fillna(0).values + df["InterestPayable_ShortTermBorrowing_last"].fillna(0).values + df["InterestPayable_Division_last"].fillna(0).values - df["InterestPayable_Total_last"].fillna(0).values) > 0.01:
            error = "期初余额:分期付息到期还本的长期借款利息+企业债券利息+短期借款应付利息+划分为金融负债的优先股/永续债利息<>合计"
            errorlist.append(error)
	# 重要的已逾期未支付的利息情况期末余额:项目1+项目2+项目3+项目4+项目5=合计
        if abs(df["InterestPayable_Company1_this"].fillna(0).values + df["InterestPayable_Company2_this"].fillna(0).values + df["InterestPayable_Company3_this"].fillna(0).values + df["InterestPayable_Company4_this"].fillna(0).values + df["InterestPayable_Company5_this"].fillna(0).values - df["InterestPayable_Total_this"].fillna(0).values) > 0.01:
            error = "重要的已逾期未支付的利息情况期末余额:项目1+项目2+项目3+项目4+项目5<>合计"
            errorlist.append(error)
        











        return df, errorlist


if __name__ == "__main__":
    d = GetInterestPayable()