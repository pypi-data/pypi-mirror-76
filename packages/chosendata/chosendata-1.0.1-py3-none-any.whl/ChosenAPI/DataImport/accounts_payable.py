
import pandas as pd
from ChosenAPI.DataImport.ChangeToNum import ChangeData



class GetAccountsPayable(object):#应付账款
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
            "AccountsPayable_ListProject1_this": data.cell_value(3, 1),  # B4 4行2列应付账款列示项目1期末余额
            "AccountsPayable_ListProject2_this": data.cell_value(4, 1),  # B5 5行2列应付账款列示项目2期末余额
            "AccountsPayable_ListProject3_this": data.cell_value(5, 1),  # B6 6行2列应付账款列示项目3期末余额
            "AccountsPayable_ListProject4_this": data.cell_value(6, 1),  # B7 7行2列应付账款列示项目4期末余额
            "AccountsPayable_ListProject5_this": data.cell_value(7, 1),  # B8 8行2列应付账款列示项目5期末余额
            "AccountsPayable_Total_this": data.cell_value(8, 1),  # B9 9行2列应付账款列示合计期末余额
            "AccountsPayable_ListProject1_last": data.cell_value(3, 2),  # C4 4行3列应付账款列示项目1期初余额
            "AccountsPayable_ListProject2_last": data.cell_value(4, 2),  # C5 5行3列应付账款列示项目2期初余额
            "AccountsPayable_ListProject3_last": data.cell_value(5, 2),  # C6 6行3列应付账款列示项目3期初余额
            "AccountsPayable_ListProject4_last": data.cell_value(6, 2),  # C7 7行3列应付账款列示项目4期初余额
            "AccountsPayable_ListProject5_last": data.cell_value(7, 2),  # C8 8行3列应付账款列示项目5期初余额
            "AccountsPayable_Total_last": data.cell_value(8, 2),  # C9 9行3列应付账款列示合计期初余额
            "AccountsPayable_Project1_this": data.cell_value(12, 1),  # B13 13行2列账龄超过1年的重要应付账款项目1期末余额
            "AccountsPayable_Project2_this": data.cell_value(13, 1),  # B14 14行2列账龄超过2年的重要应付账款项目2期末余额
            "AccountsPayable_Project3_this": data.cell_value(14, 1),  # B15 15行2列账龄超过3年的重要应付账款项目3期末余额
            "AccountsPayable_Project4_this": data.cell_value(15, 1),  # B16 16行2列账龄超过4年的重要应付账款项目4期末余额
            "AccountsPayable_Project5_this": data.cell_value(16, 1),  # B17 17行2列账龄超过5年的重要应付账款项目5期末余额
            "AccountsPayable_TotalImportant_this": data.cell_value(17, 1),  # B18 18行2列账龄超过1年的重要应付账款合计期末余额
            "AccountsPayable_0_1_this": data.cell_value(21, 1),  # B22 22行2列账龄1年以内期末余额
            "AccountsPayable_1_2_this": data.cell_value(22, 1),  # B23 23行2列账龄1～2年期末余额
            "AccountsPayable_2_3_this": data.cell_value(23, 1),  # B24 24行2列账龄2～3年期末余额
            "AccountsPayable_3___this": data.cell_value(24, 1),  # B25 25行2列账龄3年以上期末余额
            "AccountsPayable_TotalAging_this": data.cell_value(25, 1),  # B26 26行2列账龄合计期末余额
            "AccountsPayable_0_1_last": data.cell_value(21, 2),  # C22 22行3列账龄1年以内期初余额
            "AccountsPayable_1_2_last": data.cell_value(22, 2),  # C23 23行3列账龄1～2年期初余额
            "AccountsPayable_2_3_last": data.cell_value(23, 2),  # C24 24行3列账龄2～3年期初余额
            "AccountsPayable_3___last": data.cell_value(24, 2),  # C25 25行3列账龄3年以上期初余额
            "AccountsPayable_TotalAging_last": data.cell_value(25, 2),  # C26 26行3列账龄合计期初余额

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
        dic["AccountsPayable_Project1_reason"] = data.cell_value(12, 2),  # C1313行3列账龄超过1年的重要应付账款项目1未偿还或结转的原因
        dic["AccountsPayable_Project2_reason"] = data.cell_value(13, 2),  # C1414行3列账龄超过2年的重要应付账款项目2未偿还或结转的原因
        dic["AccountsPayable_Project3_reason"] = data.cell_value(14, 2),  # C1515行3列账龄超过3年的重要应付账款项目3未偿还或结转的原因
        dic["AccountsPayable_Project4_reason"] = data.cell_value(15, 2),  # C1616行3列账龄超过4年的重要应付账款项目4未偿还或结转的原因
        dic["AccountsPayable_Project5_reason"] = data.cell_value(16, 2),  # C1717行3列账龄超过5年的重要应付账款项目5未偿还或结转的原因
        dic["AccountsPayable_Remark"] = data.cell_value(27, 1),  # B2828行2列说明
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
        # 应付账款列示期末余额:项目1+项目2+项目3+项目4+项目5=合计
        if abs(df["AccountsPayable_ListProject1_this"].fillna(0).values + df["AccountsPayable_ListProject2_this"].fillna(0).values + df["AccountsPayable_ListProject3_this"].fillna(0).values + df["AccountsPayable_ListProject4_this"].fillna(0).values + df["AccountsPayable_ListProject5_this"].fillna(0).values - df["AccountsPayable_Total_this"].fillna(0).values) > 0.01:
            error = "应付账款列示期末余额:项目1+项目2+项目3+项目4+项目5<>合计"
            errorlist.append(error)
	# 应付账款列示期初余额:项目1+项目2+项目3+项目4+项目5=合计
        if abs(df["AccountsPayable_ListProject1_last"].fillna(0).values + df["AccountsPayable_ListProject2_last"].fillna(0).values + df["AccountsPayable_ListProject3_last"].fillna(0).values + df["AccountsPayable_ListProject4_last"].fillna(0).values + df["AccountsPayable_ListProject5_last"].fillna(0).values - df["AccountsPayable_Total_last"].fillna(0).values) > 0.01:
            error = "应付账款列示期初余额:项目1+项目2+项目3+项目4+项目5<>合计"
            errorlist.append(error)
        # 账龄超过1年的重要应付账款期末余额:项目1+项目2+项目3+项目4+项目5=合计
        if abs(df["AccountsPayable_Project1_this"].fillna(0).values + df["AccountsPayable_Project2_this"].fillna(0).values + df["AccountsPayable_Project3_this"].fillna(0).values + df["AccountsPayable_Project4_this"].fillna(0).values + df["AccountsPayable_Project5_this"].fillna(0).values - df["AccountsPayable_TotalImportant_this"].fillna(0).values) > 0.01:
            error = "账龄超过1年的重要应付账款期末余额:项目1+项目2+项目3+项目4+项目5<>合计"
            errorlist.append(error)
	# 账龄期末余额：1年以内+1～2年+2～3年+3年以上=合计
        if abs(df["AccountsPayable_0_1_this"].fillna(0).values + df["AccountsPayable_1_2_this"].fillna(0).values + df["AccountsPayable_2_3_this"].fillna(0).values + df["AccountsPayable_3___this"].fillna(0).values - df["AccountsPayable_TotalAging_this"].fillna(0).values) > 0.01:
            error = "账龄期初余额：1年以内+1～2年+2～3年+3年以上<>合计"
            errorlist.append(error)
	# 账龄期初余额：1年以内+1～2年+2～3年+3年以上=合计
        if abs(df["AccountsPayable_0_1_last"].fillna(0).values + df["AccountsPayable_1_2_last"].fillna(0).values + df["AccountsPayable_2_3_last"].fillna(0).values + df["AccountsPayable_3___last"].fillna(0).values - df["AccountsPayable_TotalAging_last"].fillna(0).values) > 0.01:
            error = "账龄期初余额：1年以内+1～2年+2～3年+3年以上<>合计"
            errorlist.append(error)











        return df, errorlist


if __name__ == "__main__":
    d = GetAccountsPayable()