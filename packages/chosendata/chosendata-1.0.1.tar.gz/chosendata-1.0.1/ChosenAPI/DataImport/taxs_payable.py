
import pandas as pd
from ChosenAPI.DataImport.ChangeToNum import ChangeData



class GetTaxsPayable(object):#应交税费
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
            "TaxsPayable_EnterpriseIncomeTax_this": data.cell_value(2, 1),  # B3 3行2列企业所得税期末余额
            "TaxsPayable_Vat_this": data.cell_value(3, 1),  # B4 4行2列增值税期末余额
            "TaxsPayable_BusinessTax_this": data.cell_value(4, 1),  # B5 5行2列营业税　期末余额
            "TaxsPayable_ConsumptionTax_this": data.cell_value(5, 1),  # B6 6行2列消费税　期末余额
            "TaxsPayable_ResourceTax_this": data.cell_value(6, 1),  # B7 7行2列资源税　期末余额
            "TaxsPayable_LandValueAddedTax_this": data.cell_value(7, 1),  # B8 8行2列土地增值税　期末余额
            "TaxsPayable_LandUseTax_this": data.cell_value(8, 1),  # B9 9行2列土地使用税期末余额
            "TaxsPayable_PropertyTax_this": data.cell_value(9, 1),  # B10 10行2列房产税　期末余额
            "TaxsPayable_VehicleAndVesselUseTax_this": data.cell_value(10, 1),  # B11 11行2列车船使用税　期末余额
            "TaxsPayable_UrbanMaintenanceAndConstructionTax_this": data.cell_value(11, 1),  # B12 12行2列城市维护建设税期末余额
            "TaxsPayable_EducationSurcharge_this": data.cell_value(12, 1),  # B13 13行2列教育费附加期末余额
            "TaxsPayable_WithholdingOfIndividualIncomeTax_this": data.cell_value(13, 1),  # B14 14行2列代扣代缴个人所得税期末余额
            "TaxsPayable_StampTax_this": data.cell_value(14, 1),  # B15 15行2列印花税期末余额
            "TaxsPayable_Other_this": data.cell_value(15, 1),  # B16 16行2列其他期末余额
            "TaxsPayable_Total_this": data.cell_value(16, 1),  # B17 17行2列合计期末余额
            "TaxsPayable_EnterpriseIncomeTax_last": data.cell_value(2, 2),  # C3 3行3列企业所得税期初余额
            "TaxsPayable_Vat_last": data.cell_value(3, 2),  # C4 4行3列增值税期初余额
            "TaxsPayable_BusinessTax_last": data.cell_value(4, 2),  # C5 5行3列营业税　期初余额
            "TaxsPayable_ConsumptionTax_last": data.cell_value(5, 2),  # C6 6行3列消费税　期初余额
            "TaxsPayable_ResourceTax_last": data.cell_value(6, 2),  # C7 7行3列资源税　期初余额
            "TaxsPayable_LandValueAddedTax_last": data.cell_value(7, 2),  # C8 8行3列土地增值税　期初余额
            "TaxsPayable_LandUseTax_last": data.cell_value(8, 2),  # C9 9行3列土地使用税期初余额
            "TaxsPayable_PropertyTax_last": data.cell_value(9, 2),  # C10 10行3列房产税　期初余额
            "TaxsPayable_VehicleAndVesselUseTax_last": data.cell_value(10, 2),  # C11 11行3列车船使用税　期初余额
            "TaxsPayable_UrbanMaintenanceAndConstructionTax_last": data.cell_value(11, 2),  # C12 12行3列城市维护建设税期初余额
            "TaxsPayable_EducationSurcharge_last": data.cell_value(12, 2),  # C13 13行3列教育费附加期初余额
            "TaxsPayable_WithholdingOfIndividualIncomeTax_last": data.cell_value(13, 2),  # C14 14行3列代扣代缴个人所得税期初余额
            "TaxsPayable_StampTax_last": data.cell_value(14, 2),  # C15 15行3列印花税期初余额
            "TaxsPayable_Other_last": data.cell_value(15, 2),  # C16 16行3列其他期初余额
            "TaxsPayable_Total_last": data.cell_value(16, 2),  # C17 17行3列合计期初余额


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
        dic["TaxsPayable_Remark"] = data.cell_value(18, 1),  # B19 19行2列说明
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
        # 期末余额：企业所得税+增值税+营业税+消费税+资源税+土地增值税+土地使用税+房产税+车船使用税+城市维护建设税+教育费附加+代扣代缴个人所得税+印花税+其他=合计
        if abs(df["TaxsPayable_EnterpriseIncomeTax_this"].fillna(0).values + df["TaxsPayable_Vat_this"].fillna(0).values + df["TaxsPayable_BusinessTax_this"].fillna(0).values + df["TaxsPayable_ConsumptionTax_this"].fillna(0).values + df["TaxsPayable_ResourceTax_this"].fillna(0).values + df["TaxsPayable_LandValueAddedTax_this"].fillna(0).values + df["TaxsPayable_LandUseTax_this"].fillna(0).values + df["TaxsPayable_PropertyTax_this"].fillna(0).values + df["TaxsPayable_VehicleAndVesselUseTax_this"].fillna(0).values + df["TaxsPayable_UrbanMaintenanceAndConstructionTax_this"].fillna(0).values + df["TaxsPayable_EducationSurcharge_this"].fillna(0).values + df["TaxsPayable_WithholdingOfIndividualIncomeTax_this"].fillna(0).values + df["TaxsPayable_StampTax_this"].fillna(0).values + df["TaxsPayable_Other_this"].fillna(0).values - df["TaxsPayable_Total_this"].fillna(0).values) > 0.01:
                error = "期末余额：企业所得税+增值税+营业税+消费税+资源税+土地增值税+土地使用税+房产税+车船使用税+城市维护建设税+教育费附加+代扣代缴个人所得税+印花税+其他<>合计"
                errorlist.append(error)
        # 期初余额：企业所得税+增值税+营业税+消费税+资源税+土地增值税+土地使用税+房产税+车船使用税+城市维护建设税+教育费附加+代扣代缴个人所得税+印花税+其他=合计
        if abs(df["TaxsPayable_EnterpriseIncomeTax_last"].fillna(0).values + df["TaxsPayable_Vat_last"].fillna(0).values + df["TaxsPayable_BusinessTax_last"].fillna(0).values + df["TaxsPayable_ConsumptionTax_last"].fillna(0).values + df["TaxsPayable_ResourceTax_last"].fillna(0).values + df["TaxsPayable_LandValueAddedTax_last"].fillna(0).values + df["TaxsPayable_LandUseTax_last"].fillna(0).values + df["TaxsPayable_PropertyTax_last"].fillna(0).values + df["TaxsPayable_VehicleAndVesselUseTax_last"].fillna(0).values + df["TaxsPayable_UrbanMaintenanceAndConstructionTax_last"].fillna(0).values + df["TaxsPayable_EducationSurcharge_last"].fillna(0).values + df["TaxsPayable_WithholdingOfIndividualIncomeTax_last"].fillna(0).values + df["TaxsPayable_StampTax_last"].fillna(0).values + df["TaxsPayable_Other_last"].fillna(0).values - df["TaxsPayable_Total_last"].fillna(0).values) > 0.01:
                error = "期初余额：企业所得税+增值税+营业税+消费税+资源税+土地增值税+土地使用税+房产税+车船使用税+城市维护建设税+教育费附加+代扣代缴个人所得税+印花税+其他<>合计"
                errorlist.append(error)

        return df, errorlist


if __name__ == "__main__":
    d = GetTaxsPayable()