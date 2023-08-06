
import pandas as pd
from ChosenAPI.DataImport.ChangeToNum import ChangeData



class GetInterestReceivable(object):#应收利息
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
            "InterestReceivable_TimeDeposits_this": data.cell_value(3, 1),  # B4 4行2列应收利息分类定期存款期末余额
            "InterestReceivable_EntrustedLoans_this": data.cell_value(4, 1),  # B5 5行2列应收利息分类委托贷款期末余额
            "InterestReceivable_BondInvestment_this": data.cell_value(5, 1),  # B6 6行2列应收利息分类债券投资期末余额
            "InterestReceivable_Other_this": data.cell_value(6, 1),  # B7 7行2列应收利息分类其他期末余额
            "InterestReceivable_Total_this": data.cell_value(7, 1),  # B8 8行2列应收利息分类合计期末余额
            "InterestReceivable_TimeDeposits_last": data.cell_value(3, 2),  # C4 4行3列应收利息分类定期存款期初余额
            "InterestReceivable_EntrustedLoans_last": data.cell_value(4, 2),  # C5 5行3列应收利息分类委托贷款期初余额
            "InterestReceivable_BondInvestment_last": data.cell_value(5, 2),  # C6 6行3列应收利息分类债券投资期初余额
            "InterestReceivable_Other_last": data.cell_value(6, 2),  # C7 7行3列应收利息分类其他期初余额
            "InterestReceivable_Total_last": data.cell_value(7, 2),  # C8 8行3列应收利息分类合计期初余额
            "InterestReceivable_Company1_this": data.cell_value(11, 1),  # B12 12行2列重要逾期利息借款单位名称1期末余额
            "InterestReceivable_Company2_this": data.cell_value(12, 1),  # B13 13行2列重要逾期利息借款单位名称2期末余额
            "InterestReceivable_Total2_this": data.cell_value(13, 1),  # B14 14行2列重要逾期利息借款单位名称3期末余额
            

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
        dic["InterestReceivable_Remark"] = data.cell_value(15, 1),  # B16 16行2列说明
        dic["InterestReceivable_Company1_time"] = data.cell_value(11, 2),  # C12 12行3列重要逾期利息借款单位名称1逾期时间
        dic["InterestReceivable_Company2_time"] = data.cell_value(12, 2),  # C13 13行3列重要逾期利息借款单位名称2逾期时间
        dic["InterestReceivable_Company1_reason_judge"] = data.cell_value(11, 3),  # D12 12行4列重要逾期利息借款单位名称1逾期原因
        dic["InterestReceivable_Company2_reason_judge"] = data.cell_value(12, 3),  # D13 13行4列重要逾期利息借款单位名称2逾期原因
        dic["InterestReceivable_Company1_judge"] = data.cell_value(11, 4),  # E12 12行5列重要逾期利息借款单位名称1是否发生减值及其判断依据
        dic["InterestReceivable_Company2_judge"] = data.cell_value(12, 4),  # E13 13行5列重要逾期利息借款单位名称2是否发生减值及其判断依据
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
        # 应收利息分类期末余额：定期存款+委托贷款+债券投资+其他=合计
        if abs(df["InterestReceivable_TimeDeposits_this"].fillna(0).values + df["InterestReceivable_EntrustedLoans_this"].fillna(0).values + df["InterestReceivable_BondInvestment_this"].fillna(0).values + df["InterestReceivable_Other_this"].fillna(0).values - df["InterestReceivable_Total_this"].fillna(0).values) > 0.01:
            error = "应收利息分类期末余额：定期存款+委托贷款+债券投资+其他<>合计"
            errorlist.append(error)
        # 应收利息分类期初余额：定期存款+委托贷款+债券投资+其他=合计
        if abs(df["InterestReceivable_TimeDeposits_last"].fillna(0).values + df["InterestReceivable_EntrustedLoans_last"].fillna(0).values + df["InterestReceivable_BondInvestment_last"].fillna(0).values + df["InterestReceivable_Other_last"].fillna(0).values - df["InterestReceivable_Total_last"].fillna(0).values) > 0.01:
            error = "应收利息分类期初余额：定期存款+委托贷款+债券投资+其他<>合计"
            errorlist.append(error)
        # 重要逾期利息：1+2=合计
        if abs(df["InterestReceivable_Company1_this"].fillna(0).values + df["InterestReceivable_Company2_this"].fillna(0).values - df["InterestReceivable_Total2_this"].fillna(0).values) > 0.01:
            error = "重要逾期利息：1+2<>合计"
            errorlist.append(error)

        return df, errorlist


if __name__ == "__main__":
    d = GetInterestReceivable()