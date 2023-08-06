
import pandas as pd
from ChosenAPI.DataImport.ChangeToNum import ChangeData



class GetIntangibleAssets(object):#无形资产
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
            "IntangibleAssets_LastOBV_Land": data.cell_value(3, 1),  # B4 4行2列1.期初余额土地使用权
            "IntangibleAssets_AddOBV_Land": data.cell_value(4, 1),  # B5 5行2列2.本期增加金额土地使用权
            "IntangibleAssets_PurchaseOBV_Land": data.cell_value(5, 1),  # B6 6行2列⑴购置土地使用权
            "IntangibleAssets_Dev_Land": data.cell_value(6, 1),  # B7 7行2列⑵内部研发土地使用权
            "IntangibleAssets_MergeOBV_Land": data.cell_value(7, 1),  # B8 8行2列⑶企业合并增加土地使用权
            "IntangibleAssets_ReduceOBV_Land": data.cell_value(8, 1),  # B9 9行2列3.本期减少金额土地使用权
            "IntangibleAssets_DisposalOBV_Land": data.cell_value(9, 1),  # B10 10行2列⑴处置土地使用权
            "IntangibleAssets_CReduceOBV_Land": data.cell_value(10, 1),# B11 11行2列⑵企业合并减少土地使用权
            "IntangibleAssets_ThisOBV_Land": data.cell_value(11, 1),  # B12 12行2列4.期末余额土地使用权
            "IntangibleAssets_LastAD_Land": data.cell_value(13, 1),# B14 14行2列1.期初余额土地使用权
            "IntangibleAssets_AddAD_Land": data.cell_value(14, 1),# B15 15行2列2.本期增加金额土地使用权
            "IntangibleAssets_AmortizationAD_Land": data.cell_value(15, 1),# B16 16行2列⑴计提土地使用权
            "IntangibleAssets_MergeAD_Land": data.cell_value(16, 1),# B17 17行2列⑵企业合并增加土地使用权
            "IntangibleAssets_ReduceAD_Land": data.cell_value(17, 1),# B18 18行2列3.本期减少金额土地使用权
            "IntangibleAssets_DisposalAD_Land": data.cell_value(18, 1),# B19 19行2列⑴处置土地使用权
            "IntangibleAssets_CReduceAD_Land": data.cell_value(19, 1),# B20 20行2列⑵企业合并减少土地使用权
            "IntangibleAssets_ThisAD_Land": data.cell_value(20, 1),# B21 21行2列4.期末余额土地使用权
            "IntangibleAssets_LastIL_Land": data.cell_value(22, 1),  # B23 23行2列1.期初余额土地使用权
            "IntangibleAssets_AddIL_Land": data.cell_value(23, 1),  # B24 24行2列2.本期增加金额土地使用权
            "IntangibleAssets_AmortizationIL_Land": data.cell_value(24, 1),  # B25 25行2列⑴计提土地使用权
            "IntangibleAssets_MergeIL_Land": data.cell_value(25, 1),  # B26 26行2列⑵企业合并增加土地使用权
            "IntangibleAssets_ReduceIL_Land": data.cell_value(26, 1),  # B27 27行2列3.本期减少金额土地使用权
            "IntangibleAssets_DisposalIL_Land": data.cell_value(27, 1),  # B28 28行2列⑴处置土地使用权
            "IntangibleAssets_CReduceIL_Land": data.cell_value(28, 1),# B29 29行2列⑵企业合并减少土地使用权
            "IntangibleAssets_ThisIL_Land": data.cell_value(29, 1),  # B30 30行2列4.期末余额土地使用权
            "IntangibleAssets_EndingBV_Land": data.cell_value(31, 1),  # B32 32行2列1.期末账面价值土地使用权
            "IntangibleAssets_OpeningBV_Land": data.cell_value(32, 1),  # B33 33行2列2.期初账面价值土地使用权
            "IntangibleAssets_LastOBV_Patent": data.cell_value(3, 2),  # C4 4行3列1.期初余额专利权
            "IntangibleAssets_AddOBV_Patent": data.cell_value(4, 2),  # C5 5行3列2.本期增加金额专利权
            "IntangibleAssets_PurchaseOBV_Patent": data.cell_value(5, 2),  # C6 6行3列⑴购置专利权
            "IntangibleAssets_Dev_Patent": data.cell_value(6, 2),  # C7 7行3列⑵内部研发专利权
            "IntangibleAssets_MergeOBV_Patent": data.cell_value(7, 2),  # C8 8行3列⑶企业合并增加专利权
            "IntangibleAssets_ReduceOBV_Patent": data.cell_value(8, 2),  # C9 9行3列3.本期减少金额专利权
            "IntangibleAssets_DisposalOBV_Patent": data.cell_value(9, 2),  # C10 10行3列⑴处置专利权
            "IntangibleAssets_CReduceOBV_Patent": data.cell_value(10, 2),  # C11 11行3列⑵企业合并减少专利权
            "IntangibleAssets_ThisOBV_Patent": data.cell_value(11, 2),  # C12 12行3列4.期末余额专利权
            "IntangibleAssets_LastAD_Patent": data.cell_value(13, 2),  # C14 14行3列1.期初余额专利权
            "IntangibleAssets_AddAD_Patent": data.cell_value(14, 2),  # C15 15行3列2.本期增加金额专利权
            "IntangibleAssets_AmortizationAD_Patent": data.cell_value(15, 2),  # C16 16行3列⑴计提专利权
            "IntangibleAssets_MergeAD_Patent": data.cell_value(16, 2),  # C17 17行3列⑵企业合并增加专利权
            "IntangibleAssets_ReduceAD_Patent": data.cell_value(17, 2),  # C18 18行3列3.本期减少金额专利权
            "IntangibleAssets_DisposalAD_Patent": data.cell_value(18, 2),  # C19 19行3列⑴处置专利权
            "IntangibleAssets_CReduceAD_Patent": data.cell_value(19, 2),# C20 20行3列⑵企业合并减少专利权
            "IntangibleAssets_ThisAD_Patent": data.cell_value(20, 2),  # C21 21行3列4.期末余额专利权
            "IntangibleAssets_LastIL_Patent": data.cell_value(22, 2),  # C23 23行3列1.期初余额专利权
            "IntangibleAssets_AddIL_Patent": data.cell_value(23, 2),  # C24 24行3列2.本期增加金额专利权
            "IntangibleAssets_AmortizationIL_Patent": data.cell_value(24, 2),  # C25 25行3列⑴计提专利权
            "IntangibleAssets_MergeIL_Patent": data.cell_value(25, 2),  # C26 26行3列⑵企业合并增加专利权
            "IntangibleAssets_ReduceIL_Patent": data.cell_value(26, 2),  # C27 27行3列3.本期减少金额专利权
            "IntangibleAssets_DisposalIL_Patent": data.cell_value(27, 2),  # C28 28行3列⑴处置专利权
            "IntangibleAssets_CReduceIL_Patent": data.cell_value(28, 2),  # C29 29行3列⑵企业合并减少专利权
            "IntangibleAssets_ThisIL_Patent": data.cell_value(29, 2),  # C30 30行3列4.期末余额专利权
            "IntangibleAssets_EndingBV_Patent": data.cell_value(31, 2),  # C32 32行3列1.期末账面价值专利权
            "IntangibleAssets_OpeningBV_Patent": data.cell_value(32, 2),  # C33 33行3列2.期初账面价值专利权
            "IntangibleAssets_LastOBV_Tec": data.cell_value(3, 3),# D4 4行4列1.期初余额非专利技术
            "IntangibleAssets_AddOBV_Tec": data.cell_value(4, 3),# D5 5行4列2.本期增加金额非专利技术
            "IntangibleAssets_PurchaseOBV_Tec": data.cell_value(5, 3),# D6 6行4列⑴购置非专利技术
            "IntangibleAssets_Dev_Tec": data.cell_value(6, 3),# D7 7行4列⑵内部研发非专利技术
            "IntangibleAssets_MergeOBV_Tec": data.cell_value(7, 3),# D8 8行4列⑶企业合并增加非专利技术
            "IntangibleAssets_ReduceOBV_Tec": data.cell_value(8, 3),# D9 9行4列3.本期减少金额非专利技术
            "IntangibleAssets_DisposalOBV_Tec": data.cell_value(9, 3),# D10 10行4列⑴处置非专利技术
            "IntangibleAssets_CReduceOBV_Tec": data.cell_value(10, 3),# D11 11行4列⑵企业合并减少非专利技术
            "IntangibleAssets_ThisOBV_Tec": data.cell_value(11, 3),# D12 12行4列4.期末余额非专利技术
            "IntangibleAssets_LastAD_Tec": data.cell_value(13, 3),# D14 14行4列1.期初余额非专利技术
            "IntangibleAssets_AddAD_Tec": data.cell_value(14, 3),# D15 15行4列2.本期增加金额非专利技术
            "IntangibleAssets_AmortizationAD_Tec": data.cell_value(15, 3),# D16 16行4列⑴计提非专利技术
            "IntangibleAssets_MergeAD_Tec": data.cell_value(16, 3),# D17 17行4列⑵企业合并增加非专利技术
            "IntangibleAssets_ReduceAD_Tec": data.cell_value(17, 3),# D18 18行4列3.本期减少金额非专利技术
            "IntangibleAssets_DisposalAD_Tec": data.cell_value(18, 3),# D19 19行4列⑴处置非专利技术
            "IntangibleAssets_CReduceAD_Tec": data.cell_value(19, 3),# D20 20行4列⑵企业合并减少非专利技术
            "IntangibleAssets_ThisAD_Tec": data.cell_value(20, 3),# D21 21行4列4.期末余额非专利技术
            "IntangibleAssets_LastIL_Tec": data.cell_value(22, 3),# D23 23行4列1.期初余额非专利技术
            "IntangibleAssets_AddIL_Tec": data.cell_value(23, 3),# D24 24行4列2.本期增加金额非专利技术
            "IntangibleAssets_AmortizationIL_Tec": data.cell_value(24, 3),# D25 25行4列⑴计提非专利技术
            "IntangibleAssets_MergeIL_Tec": data.cell_value(25, 3),# D26 26行4列⑵企业合并增加非专利技术
            "IntangibleAssets_ReduceIL_Tec": data.cell_value(26, 3),# D27 27行4列3.本期减少金额非专利技术
            "IntangibleAssets_DisposalIL_Tec": data.cell_value(27, 3),# D28 28行4列⑴处置非专利技术
            "IntangibleAssets_CReduceIL_Tec": data.cell_value(28, 3),# D29 29行4列⑵企业合并减少非专利技术
            "IntangibleAssets_ThisIL_Tec": data.cell_value(29, 3),# D30 30行4列4.期末余额非专利技术
            "IntangibleAssets_EndingBV_Tec": data.cell_value(31, 3),  # D32 32行4列1.期末账面价值非专利技术
            "IntangibleAssets_OpeningBV_Tec": data.cell_value(32, 3),# D33 33行4列2.期初账面价值非专利技术
            "IntangibleAssets_LastOBV_Other": data.cell_value(3, 4),  # E4 4行5列1.期初余额其他
            "IntangibleAssets_AddOBV_Other": data.cell_value(4, 4),  # E5 5行5列2.本期增加金额其他
            "IntangibleAssets_PurchaseOBV_Other": data.cell_value(5, 4),  # E6 6行5列⑴购置其他
            "IntangibleAssets_Dev_Other": data.cell_value(6, 4),  # E7 7行5列⑵内部研发其他
            "IntangibleAssets_MergeOBV_Other": data.cell_value(7, 4),  # E8 8行5列⑶企业合并增加其他
            "IntangibleAssets_ReduceOBV_Other": data.cell_value(8, 4),  # E9 9行5列3.本期减少金额其他
            "IntangibleAssets_DisposalOBV_Other": data.cell_value(9, 4),  # E10 10行5列⑴处置其他
            "IntangibleAssets_CReduceOBV_Other": data.cell_value(10, 4),  # E11 11行5列⑵企业合并减少其他
            "IntangibleAssets_ThisOBV_Other": data.cell_value(11, 4),  # E12 12行5列4.期末余额其他
            "IntangibleAssets_LastAD_Other": data.cell_value(13, 4),  # E14 14行5列1.期初余额其他
            "IntangibleAssets_AddAD_Other": data.cell_value(14, 4),  # E15 15行5列2.本期增加金额其他
            "IntangibleAssets_AmortizationAD_Other": data.cell_value(15, 4),  # E16 16行5列⑴计提其他
            "IntangibleAssets_MergeAD_Other": data.cell_value(16, 4),  # E17 17行5列⑵企业合并增加其他
            "IntangibleAssets_ReduceAD_Other": data.cell_value(17, 4),  # E18 18行5列3.本期减少金额其他
            "IntangibleAssets_DisposalAD_Other": data.cell_value(18, 4),  # E19 19行5列⑴处置其他
            "IntangibleAssets_CReduceAD_Other": data.cell_value(19, 4),# E20 20行5列⑵企业合并减少其他
            "IntangibleAssets_ThisAD_Other": data.cell_value(20, 4),  # E21 21行5列4.期末余额其他
            "IntangibleAssets_LastIL_Other": data.cell_value(22, 4),  # E23 23行5列1.期初余额其他
            "IntangibleAssets_AddIL_Other": data.cell_value(23, 4),  # E24 24行5列2.本期增加金额其他
            "IntangibleAssets_AmortizationIL_Other": data.cell_value(24, 4),  # E25 25行5列⑴计提其他
            "IntangibleAssets_MergeIL_Other": data.cell_value(25, 4),  # E26 26行5列⑵企业合并增加其他
            "IntangibleAssets_ReduceIL_Other": data.cell_value(26, 4),  # E27 27行5列3.本期减少金额其他
            "IntangibleAssets_DisposalIL_Other": data.cell_value(27, 4),  # E28 28行5列⑴处置其他
            "IntangibleAssets_CReduceIL_Other": data.cell_value(28, 4),  # E29 29行5列⑵企业合并减少其他
            "IntangibleAssets_ThisIL_Other": data.cell_value(29, 4),  # E30 30行5列4.期末余额其他
            "IntangibleAssets_EndingBV_Other": data.cell_value(31, 4),  # E32 32行5列1.期末账面价值其他
            "IntangibleAssets_OpeningBV_Other": data.cell_value(32, 4),  # E33 33行5列2.期初账面价值其他
            "IntangibleAssets_LastOBV_Total": data.cell_value(3, 5),  # F4 4行6列1.期初余额合计
            "IntangibleAssets_AddOBV_Total": data.cell_value(4, 5),  # F5 5行6列2.本期增加金额合计
            "IntangibleAssets_PurchaseOBV_Total": data.cell_value(5, 5),  # F6 6行6列⑴购置合计
            "IntangibleAssets_Dev_Total": data.cell_value(6, 5),  # F7 7行6列⑵内部研发合计
            "IntangibleAssets_MergeOBV_Total": data.cell_value(7, 5),  # F8 8行6列⑶企业合并增加合计
            "IntangibleAssets_ReduceOBV_Total": data.cell_value(8, 5),  # F9 9行6列3.本期减少金额合计
            "IntangibleAssets_DisposalOBV_Total": data.cell_value(9, 5),  # F10 10行6列⑴处置合计
            "IntangibleAssets_CReduceOBV_Total": data.cell_value(10, 5),  # F11 11行6列⑵企业合并减少合计
            "IntangibleAssets_ThisOBV_Total": data.cell_value(11, 5),  # F12 12行6列4.期末余额合计
            "IntangibleAssets_LastAD_Total": data.cell_value(13, 5),  # F14 14行6列1.期初余额合计
            "IntangibleAssets_AddAD_Total": data.cell_value(14, 5),  # F15 15行6列2.本期增加金额合计
            "IntangibleAssets_AmortizationAD_Total": data.cell_value(15, 5),  # F16 16行6列⑴计提合计
            "IntangibleAssets_MergeAD_Total": data.cell_value(16, 5),  # F17 17行6列⑵企业合并增加合计
            "IntangibleAssets_ReduceAD_Total": data.cell_value(17, 5),  # F18 18行6列3.本期减少金额合计
            "IntangibleAssets_DisposalAD_Total": data.cell_value(18, 5),  # F19 19行6列⑴处置合计
            "IntangibleAssets_CReduceAD_Total": data.cell_value(19, 5),# F20 20行6列⑵企业合并减少合计
            "IntangibleAssets_ThisAD_Total": data.cell_value(20, 5),  # F21 21行6列4.期末余额合计
            "IntangibleAssets_LastIL_Total": data.cell_value(22, 5),  # F23 23行6列1.期初余额合计
            "IntangibleAssets_AddIL_Total": data.cell_value(23, 5),  # F24 24行6列2.本期增加金额合计
            "IntangibleAssets_AmortizationIL_Total": data.cell_value(24, 5),  # F25 25行6列⑴计提合计
            "IntangibleAssets_MergeIL_Total": data.cell_value(25, 5),  # F26 26行6列⑵企业合并增加合计
            "IntangibleAssets_ReduceIL_Total": data.cell_value(26, 5),  # F27 27行6列3.本期减少金额合计
            "IntangibleAssets_DisposalIL_Total": data.cell_value(27, 5),  # F28 28行6列⑴处置合计
            "IntangibleAssets_CReduceIL_Total": data.cell_value(28, 5),  # F29 29行6列⑵企业合并减少合计
            "IntangibleAssets_ThisIL_Total": data.cell_value(29, 5),  # F30 30行6列4.期末余额合计
            "IntangibleAssets_EndingBV_Total": data.cell_value(31, 5),  # F32 32行6列1.期末账面价值合计
            "IntangibleAssets_OpeningBV_Total": data.cell_value(32, 5),  # F33 33行6列2.期初账面价值合计
            "IntangibleAssets_Project1_BV": data.cell_value(36, 1),  # B37 37行2列项目1账面价值
            "IntangibleAssets_Project2_BV": data.cell_value(37, 1),  # B38 38行2列项目2账面价值
            "IntangibleAssets_Project3_BV": data.cell_value(38, 1),  # B39 39行2列项目3账面价值
            "IntangibleAssets_Project4_BV": data.cell_value(39, 1),  # B40 40行2列项目4账面价值
            "IntangibleAssets_Project5_BV": data.cell_value(40, 1),  # B41 41行2列项目5账面价值


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
        dic["IntangibleAssets_Remark"] = data.cell_value(42, 1),  # B43 43行2列说明
        dic["IntangibleAssets_Project1_Reason"] = data.cell_value(36, 2),  # C37 37行3列项目1未办妥产权证书原因
        dic["IntangibleAssets_Project2_Reason"] = data.cell_value(37, 2),  # C38 38行3列项目2未办妥产权证书原因
        dic["IntangibleAssets_Project3_Reason"] = data.cell_value(38, 2),  # C39 39行3列项目3未办妥产权证书原因
        dic["IntangibleAssets_Project4_Reason"] = data.cell_value(39, 2),  # C40 40行3列项目4未办妥产权证书原因
        dic["IntangibleAssets_Project5_Reason"] = data.cell_value(40, 2),  # C41 41行3列项目5未办妥产权证书原因
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
        # 无形资产情况账面原值期初余额：土地使用权+专利权+非专利技术+其他=合计
        if abs(df["IntangibleAssets_LastOBV_Land"].fillna(0).values + df["IntangibleAssets_LastOBV_Patent"].fillna(0).values + df["IntangibleAssets_LastOBV_Tec"].fillna(0).values + df["IntangibleAssets_LastOBV_Other"].fillna(0).values - df["IntangibleAssets_LastOBV_Total"].fillna(0).values) > 0.01:
            error = "无形资产情况账面原值期初余额：土地使用权+专利权+非专利技术+其他<>合计"
            errorlist.append(error)
        # 无形资产情况账面原值本期增加金额：土地使用权+专利权+非专利技术+其他=合计
        if abs(df["IntangibleAssets_AddOBV_Land"].fillna(0).values + df["IntangibleAssets_AddOBV_Patent"].fillna(0).values + df["IntangibleAssets_AddOBV_Tec"].fillna(0).values + df["IntangibleAssets_AddOBV_Other"].fillna(0).values - df["IntangibleAssets_AddOBV_Total"].fillna(0).values) > 0.01:
            error = "无形资产情况账面原值本期增加金额：土地使用权+专利权+非专利技术+其他<>合计"
            errorlist.append(error)
        # 无形资产情况账面原值本期减少金额：土地使用权+专利权+非专利技术+其他=合计
        if abs(df["IntangibleAssets_ReduceOBV_Land"].fillna(0).values + df["IntangibleAssets_ReduceOBV_Patent"].fillna(0).values + df["IntangibleAssets_ReduceOBV_Tec"].fillna(0).values + df["IntangibleAssets_ReduceOBV_Other"].fillna(0).values - df["IntangibleAssets_ReduceOBV_Total"].fillna(0).values) > 0.01:
            error = "无形资产情况账面原值本期减少金额：土地使用权+专利权+非专利技术+其他<>合计"
            errorlist.append(error)
        # 无形资产情况账面原值期末余额：土地使用权+专利权+非专利技术+其他=合计
        if abs(df["IntangibleAssets_ThisOBV_Land"].fillna(0).values + df["IntangibleAssets_ThisOBV_Patent"].fillna(0).values + df["IntangibleAssets_ThisOBV_Tec"].fillna(0).values + df["IntangibleAssets_ThisOBV_Other"].fillna(0).values - df["IntangibleAssets_ThisOBV_Total"].fillna(0).values) > 0.01:
            error = "无形资产情况账面原值期末余额：土地使用权+专利权+非专利技术+其他<>合计"
            errorlist.append(error)
        # 无形资产情况累计摊销期初余额：土地使用权+专利权+非专利技术+其他=合计
        if abs(df["IntangibleAssets_LastAD_Land"].fillna(0).values + df["IntangibleAssets_LastAD_Patent"].fillna(0).values + df["IntangibleAssets_LastAD_Tec"].fillna(0).values + df["IntangibleAssets_LastAD_Other"].fillna(0).values - df["IntangibleAssets_LastAD_Total"].fillna(0).values) > 0.01:
            error = "无形资产情况累计摊销期初余额：土地使用权+专利权+非专利技术+其他<>合计"
            errorlist.append(error)
        # 无形资产情况累计摊销本期增加金额：土地使用权+专利权+非专利技术+其他=合计
        if abs(df["IntangibleAssets_AddAD_Land"].fillna(0).values + df["IntangibleAssets_AddAD_Patent"].fillna(0).values + df["IntangibleAssets_AddAD_Tec"].fillna(0).values + df["IntangibleAssets_AddAD_Other"].fillna(0).values - df["IntangibleAssets_AddAD_Total"].fillna(0).values) > 0.01:
            error = "无形资产情况累计摊销本期增加金额：土地使用权+专利权+非专利技术+其他<>合计"
            errorlist.append(error)
        # 无形资产情况累计摊销本期减少金额：土地使用权+专利权+非专利技术+其他=合计
        if abs(df["IntangibleAssets_ReduceAD_Land"].fillna(0).values + df["IntangibleAssets_ReduceAD_Patent"].fillna(0).values + df["IntangibleAssets_ReduceAD_Tec"].fillna(0).values + df["IntangibleAssets_ReduceAD_Other"].fillna(0).values - df["IntangibleAssets_ReduceAD_Total"].fillna(0).values) > 0.01:
            error = "无形资产情况累计摊销本期减少金额：土地使用权+专利权+非专利技术+其他<>合计"
            errorlist.append(error)
        # 无形资产情况累计摊销期末余额：土地使用权+专利权+非专利技术+其他=合计
        if abs(df["IntangibleAssets_ThisAD_Land"].fillna(0).values + df["IntangibleAssets_ThisAD_Patent"].fillna(0).values + df["IntangibleAssets_ThisAD_Tec"].fillna(0).values + df["IntangibleAssets_ThisAD_Other"].fillna(0).values - df["IntangibleAssets_ThisAD_Total"].fillna(0).values) > 0.01:
            error = "无形资产情况累计摊销期末余额：土地使用权+专利权+非专利技术+其他<>合计"
            errorlist.append(error)
        # 无形资产情况减值准备期初余额：土地使用权+专利权+非专利技术+其他=合计
        if abs(df["IntangibleAssets_LastIL_Land"].fillna(0).values + df["IntangibleAssets_LastIL_Patent"].fillna(0).values + df["IntangibleAssets_LastIL_Tec"].fillna(0).values + df["IntangibleAssets_LastIL_Other"].fillna(0).values - df["IntangibleAssets_LastIL_Total"].fillna(0).values) > 0.01:
            error = "无形资产情况减值准备期初余额：土地使用权+专利权+非专利技术+其他<>合计"
            errorlist.append(error)
        # 无形资产情况减值准备本期增加金额：土地使用权+专利权+非专利技术+其他=合计
        if abs(df["IntangibleAssets_AddIL_Land"].fillna(0).values + df["IntangibleAssets_AddIL_Patent"].fillna(0).values + df["IntangibleAssets_AddIL_Tec"].fillna(0).values + df["IntangibleAssets_AddIL_Other"].fillna(0).values - df["IntangibleAssets_AddIL_Total"].fillna(0).values) > 0.01:
            error = "无形资产情况减值准备本期增加金额：土地使用权+专利权+非专利技术+其他<>合计"
            errorlist.append(error)
        # 无形资产情况减值准备本期减少金额：土地使用权+专利权+非专利技术+其他=合计
        if abs(df["IntangibleAssets_ReduceIL_Land"].fillna(0).values + df["IntangibleAssets_ReduceIL_Patent"].fillna(0).values + df["IntangibleAssets_ReduceIL_Tec"].fillna(0).values + df["IntangibleAssets_ReduceIL_Other"].fillna(0).values - df["IntangibleAssets_ReduceIL_Total"].fillna(0).values) > 0.01:
            error = "无形资产情况减值准备本期减少金额：土地使用权+专利权+非专利技术+其他<>合计"
            errorlist.append(error)
        # 无形资产情况减值准备期末余额：土地使用权+专利权+非专利技术+其他=合计
        if abs(df["IntangibleAssets_ThisIL_Land"].fillna(0).values + df["IntangibleAssets_ThisIL_Patent"].fillna(0).values + df["IntangibleAssets_ThisIL_Tec"].fillna(0).values + df["IntangibleAssets_ThisIL_Other"].fillna(0).values - df["IntangibleAssets_ThisIL_Total"].fillna(0).values) > 0.01:
            error = "无形资产情况减值准备期末余额：土地使用权+专利权+非专利技术+其他<>合计"
            errorlist.append(error)
        # 无形资产情况期末账面价值：土地使用权+专利权+非专利技术+其他=合计
        if abs(df["IntangibleAssets_EndingBV_Land"].fillna(0).values + df["IntangibleAssets_EndingBV_Patent"].fillna(0).values + df["IntangibleAssets_EndingBV_Tec"].fillna(0).values + df["IntangibleAssets_EndingBV_Other"].fillna(0).values - df["IntangibleAssets_EndingBV_Total"].fillna(0).values) > 0.01:
            error = "无形资产情况期末账面价值：土地使用权+专利权+非专利技术+其他<>合计"
            errorlist.append(error)
        # 无形资产情况期初账面价值：土地使用权+专利权+非专利技术+其他=合计
        if abs(df["IntangibleAssets_OpeningBV_Land"].fillna(0).values + df["IntangibleAssets_OpeningBV_Patent"].fillna(0).values + df["IntangibleAssets_OpeningBV_Tec"].fillna(0).values + df["IntangibleAssets_OpeningBV_Other"].fillna(0).values - df["IntangibleAssets_OpeningBV_Total"].fillna(0).values) > 0.01:
            error = "无形资产情况期初账面价值：土地使用权+专利权+非专利技术+其他<>合计"
            errorlist.append(error)
        











        return df, errorlist


if __name__ == "__main__":
    d = GetIntangibleAssets()