
import pandas as pd
from ChosenAPI.DataImport.ChangeToNum import ChangeData



class GetDividendReceivable(object):#应收股利
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
            "DividendReceivable_Project1_this": data.cell_value(3, 1),  # B4 4行2列应收股利项目1期末余额
            "DividendReceivable_Project2_this": data.cell_value(4, 1),  # B5 5行2列应收股利项目2期末余额
            "DividendReceivable_Project3_this": data.cell_value(5, 1),  # B6 6行2列应收股利项目3期末余额
            "DividendReceivable_Project4_this": data.cell_value(6, 1),  # B7 7行2列应收股利项目4期末余额
            "DividendReceivable_Project5_this": data.cell_value(7, 1),  # B8 8行2列应收股利项目5期末余额
            "DividendReceivable_Total_this": data.cell_value(8, 1),  # B9 9行2列应收股利合计期末余额
            "DividendReceivable_Project1_last": data.cell_value(3, 2),  # C4 4行3列应收股利项目1期初余额
            "DividendReceivable_Project2_last": data.cell_value(4, 2),  # C5 5行3列应收股利项目2期初余额
            "DividendReceivable_Project3_last": data.cell_value(5, 2),  # C6 6行3列应收股利项目3期初余额
            "DividendReceivable_Project4_last": data.cell_value(6, 2),  # C7 7行3列应收股利项目4期初余额
            "DividendReceivable_Project5_last": data.cell_value(7, 2),  # C8 8行3列应收股利项目5期初余额
            "DividendReceivable_Total_last": data.cell_value(8, 2),  # C9 9行3列应收股利合计期初余额
            "DividendReceivable_MoreThan1YearProject1_this": data.cell_value(12, 1),  # B13 13行2列重要的账龄超过1年的应收股利项目1期末余额
            "DividendReceivable_MoreThan1YearProject2_this": data.cell_value(13, 1),  # B14 14行2列重要的账龄超过2年的应收股利项目2期末余额
            "DividendReceivable_MoreThan1YearProject3_this": data.cell_value(14, 1),  # B15 15行2列重要的账龄超过3年的应收股利项目3期末余额
            "DividendReceivable_MoreThan1YearProject4_this": data.cell_value(15, 1),  # B16 16行2列重要的账龄超过4年的应收股利项目4期末余额
            "DividendReceivable_MoreThan1YearProject5_this": data.cell_value(16, 1),  # B17 17行2列重要的账龄超过5年的应收股利项目5期末余额
            "DividendReceivable_ImportantTotal_this": data.cell_value(17, 1),  # B18 18行2列重要的账龄超过6年的应收股利合计期末余额
            


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
        dic["DividendReceivable_Remark"] = data.cell_value(19, 1)  # B20 20行2列说明
        dic["DividendReceivable_MoreThan1YearProject1_aging"] = data.cell_value(12, 2),  # C13 13行3列重要的账龄超过1年的应收股利项目1账龄
        dic["DividendReceivable_MoreThan1YearProject2_aging"] = data.cell_value(13, 2),  # C14 14行3列重要的账龄超过2年的应收股利项目2账龄
        dic["DividendReceivable_MoreThan1YearProject3_aging"] = data.cell_value(14, 2),  # C15 15行3列重要的账龄超过3年的应收股利项目3账龄
        dic["DividendReceivable_MoreThan1YearProject4_aging"] = data.cell_value(15, 2),  # C16 16行3列重要的账龄超过4年的应收股利项目4账龄
        dic["DividendReceivable_MoreThan1YearProject5_aging"] = data.cell_value(16, 2),  # C17 17行3列重要的账龄超过5年的应收股利项目5账龄
        dic["DividendReceivable_MoreThan1YearProject1_reason"] = data.cell_value(12,3),  # D13 13行4列重要的账龄超过1年的应收股利项目1未收回的原因
        dic["DividendReceivable_MoreThan1YearProject2_reason"] = data.cell_value(13,3),  # D14 14行4列重要的账龄超过2年的应收股利项目2未收回的原因
        dic["DividendReceivable_MoreThan1YearProject3_reason"] = data.cell_value(14,3),  # D15 15行4列重要的账龄超过3年的应收股利项目3未收回的原因
        dic["DividendReceivable_MoreThan1YearProject4_reason"] = data.cell_value(15,3),  # D16 16行4列重要的账龄超过4年的应收股利项目4未收回的原因
        dic["DividendReceivable_MoreThan1YearProject5_reason"] = data.cell_value(16,3),  # D17 17行4列重要的账龄超过5年的应收股利项目5未收回的原因
        dic["DividendReceivable_MoreThan1YearProject1_judge"] = data.cell_value(12,4),  # E13 13行5列重要的账龄超过1年的应收股利项目1是否发生减值及其判断依据
        dic["DividendReceivable_MoreThan1YearProject2_judge"] = data.cell_value(13,4),  # E14 14行5列重要的账龄超过2年的应收股利项目2是否发生减值及其判断依据
        dic["DividendReceivable_MoreThan1YearProject3_judge"] = data.cell_value(14,4),  # E15 15行5列重要的账龄超过3年的应收股利项目3是否发生减值及其判断依据
        dic["DividendReceivable_MoreThan1YearProject4_judge"] = data.cell_value(15,4),  # E16 16行5列重要的账龄超过4年的应收股利项目4是否发生减值及其判断依据
        dic["DividendReceivable_MoreThan1YearProject5_judge"] = data.cell_value(16,4),  # E17 17行5列重要的账龄超过5年的应收股利项目5是否发生减值及其判断依据

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
        # 应收股利分类期末余额：1+2+3+4+5=合计
        if abs(df["DividendReceivable_Project1_this"].fillna(0).values + df["DividendReceivable_Project2_this"].fillna(0).values + df["DividendReceivable_Project3_this"].fillna(0).values + df["DividendReceivable_Project4_this"].fillna(0).values + df["DividendReceivable_Project5_this"].fillna(0).values - df["DividendReceivable_Total_this"].fillna(0).values) > 0.01:
            error = "应收股利分类期末余额：1+2+3+4+5<>合计"
            errorlist.append(error)
        # 应收股利分类期初余额：1+2+3+4+5=合计
        if abs(df["DividendReceivable_Project1_last"].fillna(0).values + df["DividendReceivable_Project2_last"].fillna(0).values + df["DividendReceivable_Project3_last"].fillna(0).values + df["DividendReceivable_Project4_last"].fillna(0).values + df["DividendReceivable_Project5_last"].fillna(0).values - df["DividendReceivable_Total_last"].fillna(0).values) > 0.01:
            error = "应收股利分类期初余额：1+2+3+4+5<>合计"
            errorlist.append(error)
        # 重要的账龄超过1年的应收股利：1+2+3+4+5=合计
        if abs(df["DividendReceivable_MoreThan1YearProject1_this"].fillna(0).values + df["DividendReceivable_MoreThan1YearProject2_this"].fillna(0).values + df["DividendReceivable_MoreThan1YearProject3_this"].fillna(0).values + df["DividendReceivable_MoreThan1YearProject4_this"].fillna(0).values + df["DividendReceivable_MoreThan1YearProject5_this"].fillna(0).values - df["DividendReceivable_ImportantTotal_this"].fillna(0).values) > 0.01:
            error = "重要的账龄超过1年的应收股利：1+2+3+4+5<>合计"
            errorlist.append(error)
        











        return df, errorlist


if __name__ == "__main__":
    d = GetDividendReceivable()