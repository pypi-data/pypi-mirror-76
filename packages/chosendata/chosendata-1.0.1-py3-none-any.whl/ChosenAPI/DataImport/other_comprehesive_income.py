
import pandas as pd
from ChosenAPI.DataImport.ChangeToNum import ChangeData



class GetOtherComprehesiveIncome(object):#其他综合收益
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
            "OtherComprehesiveIncome_CanNot_last": data.cell_value(3, 1),  # B4 4行2列以后不能重分类进损益的其他综合收益期初余额
            "OtherComprehesiveIncome_In_last": data.cell_value(4, 1),  # B5 5行2列重新计算设定受益计划净负债和净资产的变动期初余额
            "OtherComprehesiveIncome_No_last": data.cell_value(5, 1),  # B6 6行2列权益法下在被投资单位不能重分类进损益的其他综合收益中享有的份额期初余额
            "OtherComprehesiveIncome_Reclassify_last": data.cell_value(6, 1),  # B7 7行2列以后将重分类进损益的其他综合收益期初余额
            "OtherComprehesiveIncome_Yes_last": data.cell_value(7, 1),  # B8 8行2列权益法下在被投资单位以后将重分类进损益的其他综合收益中享有的份额期初余额
            "OtherComprehesiveIncome_Loss_last": data.cell_value(8, 1),  # B9 9行2列可供出售金融资产公允价值变动损益期初余额
            "OtherComprehesiveIncome_Hold_last": data.cell_value(9, 1),# B10 10行2列持有至到期投资重分类为可供出售金融资产损益期初余额
            "OtherComprehesiveIncome_Eff_last": data.cell_value(10, 1),  # B11 11行2列现金流量套期损益的有效部分期初余额
            "OtherComprehesiveIncome_Banlance_last": data.cell_value(11, 1),  # B12 12行2列外币财务报表折算差额期初余额
            "OtherComprehesiveIncome_Total_last": data.cell_value(12, 1),  # B13 13行2列其他综合收益合计期初余额
            "OtherComprehesiveIncome_CanNot_accrual": data.cell_value(3, 2),# C4 4行3列以后不能重分类进损益的其他综合收益本期所得税前发生额
            "OtherComprehesiveIncome_In_accrual": data.cell_value(4, 2),# C5 5行3列重新计算设定受益计划净负债和净资产的变动本期所得税前发生额
            "OtherComprehesiveIncome_No_accrual": data.cell_value(5, 2),# C6 6行3列权益法下在被投资单位不能重分类进损益的其他综合收益中享有的份额本期所得税前发生额
            "OtherComprehesiveIncome_Reclassify_accrual": data.cell_value(6, 2),  # C7 7行3列以后将重分类进损益的其他综合收益本期所得税前发生额
            "OtherComprehesiveIncome_Yes_accrual": data.cell_value(7, 2),# C8 8行3列权益法下在被投资单位以后将重分类进损益的其他综合收益中享有的份额本期所得税前发生额
            "OtherComprehesiveIncome_Loss_accrual": data.cell_value(8, 2),# C9 9行3列可供出售金融资产公允价值变动损益本期所得税前发生额
            "OtherComprehesiveIncome_Hold_accrual": data.cell_value(9, 2),# C10 10行3列持有至到期投资重分类为可供出售金融资产损益本期所得税前发生额
            "OtherComprehesiveIncome_Eff_accrual": data.cell_value(10, 2),# C11 11行3列现金流量套期损益的有效部分本期所得税前发生额
            "OtherComprehesiveIncome_Banlance_accrual": data.cell_value(11, 2),  # C12 12行3列外币财务报表折算差额本期所得税前发生额
            "OtherComprehesiveIncome_Total_accrual": data.cell_value(12, 2),  # C13 13行3列其他综合收益合计本期所得税前发生额
            "OtherComprehesiveIncome_CanNot_CT": data.cell_value(3, 3),# D4 4行4列以后不能重分类进损益的其他综合收益前期计入其他综合收益当期转入损益
            "OtherComprehesiveIncome_In_CT": data.cell_value(4, 3),# D5 5行4列重新计算设定受益计划净负债和净资产的变动前期计入其他综合收益当期转入损益
            "OtherComprehesiveIncome_No_CT": data.cell_value(5, 3),# D6 6行4列权益法下在被投资单位不能重分类进损益的其他综合收益中享有的份额前期计入其他综合收益当期转入损益
            "OtherComprehesiveIncome_Reclassify_CT": data.cell_value(6, 3),# D7 7行4列以后将重分类进损益的其他综合收益前期计入其他综合收益当期转入损益
            "OtherComprehesiveIncome_Yes_CT": data.cell_value(7, 3),# D8 8行4列权益法下在被投资单位以后将重分类进损益的其他综合收益中享有的份额前期计入其他综合收益当期转入损益
            "OtherComprehesiveIncome_Loss_CT": data.cell_value(8, 3),# D9 9行4列可供出售金融资产公允价值变动损益前期计入其他综合收益当期转入损益
            "OtherComprehesiveIncome_Hold_CT": data.cell_value(9, 3),# D10 10行4列持有至到期投资重分类为可供出售金融资产损益前期计入其他综合收益当期转入损益
            "OtherComprehesiveIncome_Eff_CT": data.cell_value(10, 3),# D11 11行4列现金流量套期损益的有效部分前期计入其他综合收益当期转入损益
            "OtherComprehesiveIncome_Banlance_CT": data.cell_value(11, 3),# D12 12行4列外币财务报表折算差额前期计入其他综合收益当期转入损益
            "OtherComprehesiveIncome_Total_CT": data.cell_value(12, 3),# D13 13行4列其他综合收益合计前期计入其他综合收益当期转入损益
            "OtherComprehesiveIncome_CanNot_Tax": data.cell_value(3, 4),# E4 4行5列以后不能重分类进损益的其他综合收益所得税费用
            "OtherComprehesiveIncome_In_Tax": data.cell_value(4, 4),# E5 5行5列重新计算设定受益计划净负债和净资产的变动所得税费用
            "OtherComprehesiveIncome_No_Tax": data.cell_value(5, 4),# E6 6行5列权益法下在被投资单位不能重分类进损益的其他综合收益中享有的份额所得税费用
            "OtherComprehesiveIncome_Reclassify_Tax": data.cell_value(6, 4),# E7 7行5列以后将重分类进损益的其他综合收益所得税费用
            "OtherComprehesiveIncome_Yes_Tax": data.cell_value(7, 4),# E8 8行5列权益法下在被投资单位以后将重分类进损益的其他综合收益中享有的份额所得税费用
            "OtherComprehesiveIncome_Loss_Tax": data.cell_value(8, 4),# E9 9行5列可供出售金融资产公允价值变动损益所得税费用
            "OtherComprehesiveIncome_Hold_Tax": data.cell_value(9, 4),# E10 10行5列持有至到期投资重分类为可供出售金融资产损益所得税费用
            "OtherComprehesiveIncome_Eff_Tax": data.cell_value(10, 4),# E11 11行5列现金流量套期损益的有效部分所得税费用
            "OtherComprehesiveIncome_Banlance_Tax": data.cell_value(11, 4),  # E12 12行5列外币财务报表折算差额所得税费用
            "OtherComprehesiveIncome_Total_Tax": data.cell_value(12, 4),  # E13 13行5列其他综合收益合计所得税费用
            "OtherComprehesiveIncome_CanNot_PC": data.cell_value(3, 5),# F4 4行6列以后不能重分类进损益的其他综合收益税后归属于母公司
            "OtherComprehesiveIncome_In_PC": data.cell_value(4, 5),# F5 5行6列重新计算设定受益计划净负债和净资产的变动税后归属于母公司
            "OtherComprehesiveIncome_No_PC": data.cell_value(5, 5),# F6 6行6列权益法下在被投资单位不能重分类进损益的其他综合收益中享有的份额税后归属于母公司
            "OtherComprehesiveIncome_Reclassify_PC": data.cell_value(6, 5),# F7 7行6列以后将重分类进损益的其他综合收益税后归属于母公司
            "OtherComprehesiveIncome_Yes_PC": data.cell_value(7, 5),# F8 8行6列权益法下在被投资单位以后将重分类进损益的其他综合收益中享有的份额税后归属于母公司
            "OtherComprehesiveIncome_Loss_PC": data.cell_value(8, 5),# F9 9行6列可供出售金融资产公允价值变动损益税后归属于母公司
            "OtherComprehesiveIncome_Hold_PC": data.cell_value(9, 5),# F10 10行6列持有至到期投资重分类为可供出售金融资产损益税后归属于母公司
            "OtherComprehesiveIncome_Eff_PC": data.cell_value(10, 5),# F11 11行6列现金流量套期损益的有效部分税后归属于母公司
            "OtherComprehesiveIncome_Banlance_PC": data.cell_value(11, 5),  # F12 12行6列外币财务报表折算差额税后归属于母公司
            "OtherComprehesiveIncome_Total_PC": data.cell_value(12, 5),  # F13 13行6列其他综合收益合计税后归属于母公司
            "OtherComprehesiveIncome_CanNot_MS": data.cell_value(3, 6),# G4 4行7列以后不能重分类进损益的其他综合收益税后归属于少数股东
            "OtherComprehesiveIncome_In_MS": data.cell_value(4, 6),# G5 5行7列重新计算设定受益计划净负债和净资产的变动税后归属于少数股东
            "OtherComprehesiveIncome_No_MS": data.cell_value(5, 6),# G6 6行7列权益法下在被投资单位不能重分类进损益的其他综合收益中享有的份额税后归属于少数股东
            "OtherComprehesiveIncome_Reclassify_MS": data.cell_value(6, 6),# G7 7行7列以后将重分类进损益的其他综合收益税后归属于少数股东
            "OtherComprehesiveIncome_Yes_MS": data.cell_value(7, 6),# G8 8行7列权益法下在被投资单位以后将重分类进损益的其他综合收益中享有的份额税后归属于少数股东
            "OtherComprehesiveIncome_Loss_MS": data.cell_value(8, 6),# G9 9行7列可供出售金融资产公允价值变动损益税后归属于少数股东
            "OtherComprehesiveIncome_Hold_MS": data.cell_value(9, 6),# G10 10行7列持有至到期投资重分类为可供出售金融资产损益税后归属于少数股东
            "OtherComprehesiveIncome_Eff_MS": data.cell_value(10, 6),# G11 11行7列现金流量套期损益的有效部分税后归属于少数股东
            "OtherComprehesiveIncome_Banlance_MS": data.cell_value(11, 6),# G12 12行7列外币财务报表折算差额税后归属于少数股东
            "OtherComprehesiveIncome_Total_MS": data.cell_value(12, 6),# G13 13行7列其他综合收益合计税后归属于少数股东
            "OtherComprehesiveIncome_CanNot_this": data.cell_value(3, 7),  # H4 4行8列以后不能重分类进损益的其他综合收益期末余额
            "OtherComprehesiveIncome_In_this": data.cell_value(4, 7),  # H5 5行8列重新计算设定受益计划净负债和净资产的变动期末余额
            "OtherComprehesiveIncome_No_this": data.cell_value(5, 7),  # H6 6行8列权益法下在被投资单位不能重分类进损益的其他综合收益中享有的份额期末余额
            "OtherComprehesiveIncome_Reclassify_this": data.cell_value(6, 7),  # H7 7行8列以后将重分类进损益的其他综合收益期末余额
            "OtherComprehesiveIncome_Yes_this": data.cell_value(7, 7),  # H8 8行8列权益法下在被投资单位以后将重分类进损益的其他综合收益中享有的份额期末余额
            "OtherComprehesiveIncome_Loss_this": data.cell_value(8, 7),  # H9 9行8列可供出售金融资产公允价值变动损益期末余额
            "OtherComprehesiveIncome_Hold_this": data.cell_value(9, 7),# H10 10行8列持有至到期投资重分类为可供出售金融资产损益期末余额
            "OtherComprehesiveIncome_Eff_this": data.cell_value(10, 7),  # H11 11行8列现金流量套期损益的有效部分期末余额
            "OtherComprehesiveIncome_Banlance_this": data.cell_value(11, 7),  # H12 12行8列外币财务报表折算差额期末余额
            "OtherComprehesiveIncome_Total_this": data.cell_value(12, 7),  # H13 13行8列其他综合收益合计期末余额


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
        dic["OtherComprehesiveIncome_Remark"] = data.cell_value(14, 1),  # B15 15行2列说明
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
        # 期初余额：以后不能重分类进损益的其他综合收益+以后将重分类进损益的其他综合收益=其他综合收益合计
        if abs(df["OtherComprehesiveIncome_CanNot_last"].fillna(0).values + df["OtherComprehesiveIncome_Reclassify_last"].fillna(0).values - df["OtherComprehesiveIncome_Total_last"].fillna(0).values) > 0.01:
            error = "期初余额：以后不能重分类进损益的其他综合收益+以后将重分类进损益的其他综合收益<>其他综合收益合计"
            errorlist.append(error)
        # 本期所得税前发生额：以后不能重分类进损益的其他综合收益+以后将重分类进损益的其他综合收益=其他综合收益合计
        if abs(df["OtherComprehesiveIncome_CanNot_accrual"].fillna(0).values + df["OtherComprehesiveIncome_Reclassify_accrual"].fillna(0).values - df["OtherComprehesiveIncome_Total_accrual"].fillna(0).values) > 0.01:
            error = "本期所得税前发生额：以后不能重分类进损益的其他综合收益+以后将重分类进损益的其他综合收益<>其他综合收益合计"
            errorlist.append(error)
        # 减：前期计入其他综合收益当期转入损益：以后不能重分类进损益的其他综合收益+以后将重分类进损益的其他综合收益=其他综合收益合计
        if abs(df["OtherComprehesiveIncome_CanNot_CT"].fillna(0).values + df["OtherComprehesiveIncome_Reclassify_CT"].fillna(0).values - df["OtherComprehesiveIncome_Total_CT"].fillna(0).values) > 0.01:
            error = "减：前期计入其他综合收益当期转入损益：以后不能重分类进损益的其他综合收益+以后将重分类进损益的其他综合收益<>其他综合收益合计"
            errorlist.append(error)
        # 减：所得税费用：以后不能重分类进损益的其他综合收益+以后将重分类进损益的其他综合收益=其他综合收益合计
        if abs(df["OtherComprehesiveIncome_CanNot_Tax"].fillna(0).values + df["OtherComprehesiveIncome_Reclassify_Tax"].fillna(0).values - df["OtherComprehesiveIncome_Total_Tax"].fillna(0).values) > 0.01:
            error = "减：所得税费用：以后不能重分类进损益的其他综合收益+以后将重分类进损益的其他综合收益<>其他综合收益合计"
            errorlist.append(error)
        # 税后归属于母公司：以后不能重分类进损益的其他综合收益+以后将重分类进损益的其他综合收益=其他综合收益合计
        if abs(df["OtherComprehesiveIncome_CanNot_PC"].fillna(0).values + df["OtherComprehesiveIncome_Reclassify_PC"].fillna(0).values - df["OtherComprehesiveIncome_Total_PC"].fillna(0).values) > 0.01:
            error = "税后归属于母公司：以后不能重分类进损益的其他综合收益+以后将重分类进损益的其他综合收益<>其他综合收益合计"
            errorlist.append(error)
        # 税后归属于少数股东：以后不能重分类进损益的其他综合收益+以后将重分类进损益的其他综合收益=其他综合收益合计
        if abs(df["OtherComprehesiveIncome_CanNot_MS"].fillna(0).values + df["OtherComprehesiveIncome_Reclassify_MS"].fillna(0).values - df["OtherComprehesiveIncome_Total_MS"].fillna(0).values) > 0.01:
            error = "税后归属于少数股东：以后不能重分类进损益的其他综合收益+以后将重分类进损益的其他综合收益<>其他综合收益合计"
            errorlist.append(error)
        # 期末余额：以后不能重分类进损益的其他综合收益+以后将重分类进损益的其他综合收益=其他综合收益合计
        if abs(df["OtherComprehesiveIncome_CanNot_this"].fillna(0).values + df["OtherComprehesiveIncome_Reclassify_this"].fillna(0).values - df["OtherComprehesiveIncome_Total_this"].fillna(0).values) > 0.01:
            error = "期末余额：以后不能重分类进损益的其他综合收益+以后将重分类进损益的其他综合收益<>其他综合收益合计"
            errorlist.append(error)
        











        return df, errorlist


if __name__ == "__main__":
    d = GetOtherComprehesiveIncome()