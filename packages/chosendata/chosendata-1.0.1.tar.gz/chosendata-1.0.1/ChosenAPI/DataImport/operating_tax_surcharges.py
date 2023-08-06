
import pandas as pd
from ChosenAPI.DataImport.ChangeToNum import ChangeData



class GetOperatingTaxSurcharges(object):#税金和附加
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
            "OperatingTaxSurcharges_ConTax_CP": data.cell_value(2, 1),  # B3 3行2列消费税本期发生额
            "OperatingTaxSurcharges_BusTax_CP": data.cell_value(3, 1),  # B4 4行2列营业税本期发生额
            "OperatingTaxSurcharges_UrbTax_CP": data.cell_value(4, 1),# B5 5行2列城市维护建设税本期发生额
            "OperatingTaxSurcharges_Edu_CP": data.cell_value(5, 1),  # B6 6行2列教育费附加本期发生额
            "OperatingTaxSurcharges_LocalEdu_CP": data.cell_value(6, 1),# B7 7行2列地方教育附加本期发生额
            "OperatingTaxSurcharges_ResourceTax_CP": data.cell_value(7, 1),  # B8 8行2列资源税本期发生额
            "OperatingTaxSurcharges_PropertyTax_CP": data.cell_value(8, 1),  # B9 9行2列房产税本期发生额
            "OperatingTaxSurcharges_LandUseTax_CP": data.cell_value(9, 1),  # B10 10行2列土地使用税本期发生额
            "OperatingTaxSurcharges_VehTax_CP": data.cell_value(10, 1),# B11 11行2列车船使用税本期发生额
            "OperatingTaxSurcharges_StampDuty_CP": data.cell_value(11, 1),  # B12 12行2列印花税本期发生额
            "OperatingTaxSurcharges_LandTax_CP": data.cell_value(12, 1),  # B13 13行2列土地增值税本期发生额
            "OperatingTaxSurcharges_Pro_CP": data.cell_value(13, 1),# B14 14行2列与投资性房地产相关的房产税本期发生额
            "OperatingTaxSurcharges_Land_CP": data.cell_value(14, 1),# B15 15行2列与投资性房地产相关的土地使用税本期发生额
            "OperatingTaxSurcharges_Other_CP": data.cell_value(15, 1),  # B16 16行2列其他本期发生额
            "OperatingTaxSurcharges_Total_CP": data.cell_value(16, 1),  # B17 17行2列合计本期发生额
            "OperatingTaxSurcharges_ConTax_PP": data.cell_value(2, 2),  # C3 3行3列消费税上期发生额
            "OperatingTaxSurcharges_BusTax_PP": data.cell_value(3, 2),  # C4 4行3列营业税上期发生额
            "OperatingTaxSurcharges_UrbTax_PP": data.cell_value(4, 2),# C5 5行3列城市维护建设税上期发生额
            "OperatingTaxSurcharges_Edu_PP": data.cell_value(5, 2),  # C6 6行3列教育费附加上期发生额
            "OperatingTaxSurcharges_LocalEdu_PP": data.cell_value(6, 2),  # C7 7行3列地方教育附加上期发生额
            "OperatingTaxSurcharges_ResourceTax_PP": data.cell_value(7, 2),  # C8 8行3列资源税上期发生额
            "OperatingTaxSurcharges_PropertyTax_PP": data.cell_value(8, 2),  # C9 9行3列房产税上期发生额
            "OperatingTaxSurcharges_LandUseTax_PP": data.cell_value(9, 2),  # C10 10行3列土地使用税上期发生额
            "OperatingTaxSurcharges_VehTax_PP": data.cell_value(10, 2),# C11 11行3列车船使用税上期发生额
            "OperatingTaxSurcharges_StampDuty_PP": data.cell_value(11, 2),  # C12 12行3列印花税上期发生额
            "OperatingTaxSurcharges_LandTax_PP": data.cell_value(12, 2),  # C13 13行3列土地增值税上期发生额
            "OperatingTaxSurcharges_Pro_PP": data.cell_value(13, 2),# C14 14行3列与投资性房地产相关的房产税上期发生额
            "OperatingTaxSurcharges_Land_PP": data.cell_value(14, 2),# C15 15行3列与投资性房地产相关的土地使用税上期发生额
            "OperatingTaxSurcharges_Other_PP": data.cell_value(15, 2),  # C16 16行3列其他上期发生额
            "OperatingTaxSurcharges_Total_PP": data.cell_value(16, 2),  # C17 17行3列合计上期发生额



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
        dic["OperatingTaxSurcharges_Remark"] = data.cell_value(18, 1),  # B19 19行2列说明
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
        # 本期发生额:消费税+营业税+城市维护建设+税教育费附加+地方教育附加+资源税+房产税+土地使用税+车船使用税+印花税+土地增值税+与投资性房地产相关的房产税+与投资性房地产相关的土地使用税+其他=合计
        if abs(df["OperatingTaxSurcharges_ConTax_CP"].fillna(0).values + df["OperatingTaxSurcharges_BusTax_CP"].fillna(0).values + df["OperatingTaxSurcharges_UrbTax_CP"].fillna(0).values + df["OperatingTaxSurcharges_Edu_CP"].fillna(0).values + df["OperatingTaxSurcharges_LocalEdu_CP"].fillna(0).values + df["OperatingTaxSurcharges_ResourceTax_CP"].fillna(0).values + df["OperatingTaxSurcharges_PropertyTax_CP"].fillna(0).values + df["OperatingTaxSurcharges_LandUseTax_CP"].fillna(0).values + df["OperatingTaxSurcharges_VehTax_CP"].fillna(0).values + df["OperatingTaxSurcharges_StampDuty_CP"].fillna(0).values + df["OperatingTaxSurcharges_LandTax_CP"].fillna(0).values + df["OperatingTaxSurcharges_Pro_CP"].fillna(0).values + df["OperatingTaxSurcharges_Land_CP"].fillna(0).values + df["OperatingTaxSurcharges_Other_CP"].fillna(0).values - df["OperatingTaxSurcharges_Total_CP"].fillna(0).values) > 0.01:
                error = "本期发生额:消费税+营业税+城市维护建设+税教育费附加+地方教育附加+资源税+房产税+土地使用税+车船使用税+印花税+土地增值税+与投资性房地产相关的房产税+与投资性房地产相关的土地使用税+其他<>合计"
                errorlist.append(error)
            # 上期发生额:消费税+营业税+城市维护建设+税教育费附加+地方教育附加+资源税+房产税+土地使用税+车船使用税+印花税+土地增值税+与投资性房地产相关的房产税+与投资性房地产相关的土地使用税+其他=合计
        if abs(df["OperatingTaxSurcharges_ConTax_PP"].fillna(0).values + df["OperatingTaxSurcharges_BusTax_PP"].fillna(0).values + df["OperatingTaxSurcharges_UrbTax_PP"].fillna(0).values + df["OperatingTaxSurcharges_Edu_PP"].fillna(0).values + df["OperatingTaxSurcharges_LocalEdu_PP"].fillna(0).values + df["OperatingTaxSurcharges_ResourceTax_PP"].fillna(0).values + df["OperatingTaxSurcharges_PropertyTax_PP"].fillna(0).values + df["OperatingTaxSurcharges_LandUseTax_PP"].fillna(0).values + df["OperatingTaxSurcharges_VehTax_PP"].fillna(0).values + df["OperatingTaxSurcharges_StampDuty_PP"].fillna(0).values + df["OperatingTaxSurcharges_LandTax_PP"].fillna(0).values + df["OperatingTaxSurcharges_Pro_PP"].fillna(0).values + df["OperatingTaxSurcharges_Land_PP"].fillna(0).values + df["OperatingTaxSurcharges_Other_PP"].fillna(0).values - df["OperatingTaxSurcharges_Total_PP"].fillna(0).values) > 0.01:
                error = "上期发生额:消费税+营业税+城市维护建设+税教育费附加+地方教育附加+资源税+房产税+土地使用税+车船使用税+印花税+土地增值税+与投资性房地产相关的房产税+与投资性房地产相关的土地使用税+其他<>合计"
                errorlist.append(error)
        











        return df, errorlist


if __name__ == "__main__":
    d = GetOperatingTaxSurcharges()