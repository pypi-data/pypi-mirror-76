
import pandas as pd
from ChosenAPI.DataImport.ChangeToNum import ChangeData



class GetMainTaxesAndRates(object):#主要税种和税率
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
            "MainTaxesAndRates_TheVat_rate1": data.cell_value(3, 2),  # C4 4行3列增值税税率1
            "MainTaxesAndRates_TheConsumptionTax_rate1": data.cell_value(4, 2),  # C5 5行3列消费税税率1
            "MainTaxesAndRates_UrbanTax_rate1": data.cell_value(5, 2),  # C6 6行3列城市维护建设税税率1
            "MainTaxesAndRates_EnterpriseIncomeTax_rate1": data.cell_value(6, 2),  # C7 7行3列企业所得税税率1
            "MainTaxesAndRates_LandValueAddedTax_rate1": data.cell_value(7, 2),  # C8 8行3列土地增值税税率1
            "MainTaxesAndRates_add1_rate1": data.cell_value(8, 2),  # C9 9行3列添加1税率1
            "MainTaxesAndRates_add2_rate1": data.cell_value(9, 2),  # C10 10行3列添加2税率1
            "MainTaxesAndRates_add3_rate1": data.cell_value(10, 2),  # C11 11行3列添加3税率1
            "MainTaxesAndRates_add4_rate1": data.cell_value(11, 2),  # C12 12行3列添加4税率1
            "MainTaxesAndRates_add5_rate1": data.cell_value(12, 2),  # C13 13行3列添加5税率1
            "MainTaxesAndRates_TheVat_rate2": data.cell_value(3, 3),  # D4 4行4列增值税税率2
            "MainTaxesAndRates_TheConsumptionTax_rate2": data.cell_value(4, 3),  # D5 5行4列消费税税率2
            "MainTaxesAndRates_UrbanTax_rate2": data.cell_value(5, 3),  # D6 6行4列城市维护建设税税率2
            "MainTaxesAndRates_EnterpriseIncomeTax_rate2": data.cell_value(6, 3),  # D7 7行4列企业所得税税率2
            "MainTaxesAndRates_LandValueAddedTax_rate2": data.cell_value(7, 3),  # D8 8行4列土地增值税税率2
            "MainTaxesAndRates_add1_rate2": data.cell_value(8, 3),  # D9 9行4列添加1税率2
            "MainTaxesAndRates_add2_rate2": data.cell_value(9, 3),  # D10 10行4列添加2税率2
            "MainTaxesAndRates_add3_rate2": data.cell_value(10, 3),  # D11 11行4列添加3税率2
            "MainTaxesAndRates_add4_rate2": data.cell_value(11, 3),  # D12 12行4列添加4税率2
            "MainTaxesAndRates_add5_rate2": data.cell_value(12, 3),  # D13 13行4列添加5税率2
            "MainTaxesAndRates_TheVat_rate3": data.cell_value(3, 4),  # E4 4行5列增值税税率3
            "MainTaxesAndRates_TheConsumptionTax_rate3": data.cell_value(4, 4),  # E5 5行5列消费税税率3
            "MainTaxesAndRates_UrbanTax_rate3": data.cell_value(5, 4),  # E6 6行5列城市维护建设税税率3
            "MainTaxesAndRates_EnterpriseIncomeTax_rate3": data.cell_value(6, 4),  # E7 7行5列企业所得税税率3
            "MainTaxesAndRates_LandValueAddedTax_rate3": data.cell_value(7, 4),  # E8 8行5列土地增值税税率3
            "MainTaxesAndRates_add1_rate3": data.cell_value(8, 4),  # E9 9行5列添加1税率3
            "MainTaxesAndRates_add2_rate3": data.cell_value(9, 4),  # E10 10行5列添加2税率3
            "MainTaxesAndRates_add3_rate3": data.cell_value(10, 4),  # E11 11行5列添加3税率3
            "MainTaxesAndRates_add4_rate3": data.cell_value(11, 4),  # E12 12行5列添加4税率3
            "MainTaxesAndRates_add5_rate3": data.cell_value(12, 4),  # E13 13行5列添加5税率3
            "MainTaxesAndRates_TheVat_rate4": data.cell_value(3, 5),  # F4 4行6列增值税税率4
            "MainTaxesAndRates_TheConsumptionTax_rate4": data.cell_value(4, 5),  # F5 5行6列消费税税率4
            "MainTaxesAndRates_UrbanTax_rate4": data.cell_value(5, 5),  # F6 6行6列城市维护建设税税率4
            "MainTaxesAndRates_EnterpriseIncomeTax_rate4": data.cell_value(6, 5),  # F7 7行6列企业所得税税率4
            "MainTaxesAndRates_LandValueAddedTax_rate4": data.cell_value(7, 5),  # F8 8行6列土地增值税税率4
            "MainTaxesAndRates_add1_rate4": data.cell_value(8, 5),  # F9 9行6列添加1税率4
            "MainTaxesAndRates_add2_rate4": data.cell_value(9, 5),  # F10 10行6列添加2税率4
            "MainTaxesAndRates_add3_rate4": data.cell_value(10, 5),  # F11 11行6列添加3税率4
            "MainTaxesAndRates_add4_rate4": data.cell_value(11, 5),  # F12 12行6列添加4税率4
            "MainTaxesAndRates_add5_rate4": data.cell_value(12, 5),  # F13 13行6列添加5税率4
            "MainTaxesAndRates_TheVat_rate5": data.cell_value(3, 6),  # G4 4行7列增值税税率5
            "MainTaxesAndRates_TheConsumptionTax_rate5": data.cell_value(4, 6),  # G5 5行7列消费税税率5
            "MainTaxesAndRates_UrbanTax_rate5": data.cell_value(5, 6),  # G6 6行7列城市维护建设税税率5
            "MainTaxesAndRates_EnterpriseIncomeTax_rate5": data.cell_value(6, 6),  # G7 7行7列企业所得税税率5
            "MainTaxesAndRates_LandValueAddedTax_rate5": data.cell_value(7, 6),  # G8 8行7列土地增值税税率5
            "MainTaxesAndRates_add1_rate5": data.cell_value(8, 6),  # G9 9行7列添加1税率5
            "MainTaxesAndRates_add2_rate5": data.cell_value(9, 6),  # G10 10行7列添加2税率5
            "MainTaxesAndRates_add3_rate5": data.cell_value(10, 6),  # G11 11行7列添加3税率5
            "MainTaxesAndRates_add4_rate5": data.cell_value(11, 6),  # G12 12行7列添加4税率5
            "MainTaxesAndRates_add5_rate5": data.cell_value(12, 6),  # G13 13行7列添加5税率5


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
        dic["MainTaxesAndRates_Remark"] = data.cell_value(14, 1),  # B15 15行4列说明
        dic["MainTaxesAndRates_TheVat_PlanTaxBasis"] = data.cell_value(3, 1),  # B4 4行2列增值税计税依据
        dic["MainTaxesAndRates_TheConsumptionTax_PlanTaxBasis"] = data.cell_value(4, 1),  # B5 5行2列消费税计税依据
        dic["MainTaxesAndRates_UrbanTax_PlanTaxBasis"] = data.cell_value(5, 1),  # B6 6行2列城市维护建设税计税依据
        dic["MainTaxesAndRates_EnterpriseIncomeTax_PlanTaxBasis"] = data.cell_value(6, 1),  # B7 7行2列企业所得税计税依据
        dic["MainTaxesAndRates_LandValueAddedTax_PlanTaxBasis"] = data.cell_value(7, 1),  # B8 8行2列土地增值税计税依据
        dic["MainTaxesAndRates_add1_PlanTaxBasis"] = data.cell_value(8, 1),  # B9 9行2列添加1计税依据
        dic["MainTaxesAndRates_add2_PlanTaxBasis"] = data.cell_value(9, 1),  # B10 10行2列添加2计税依据
        dic["MainTaxesAndRates_add3_PlanTaxBasis"] = data.cell_value(10, 1),  # B11 11行2列添加3计税依据
        dic["MainTaxesAndRates_add4_PlanTaxBasis"] = data.cell_value(11, 1),  # B12 12行2列添加4计税依据
        dic["MainTaxesAndRates_add5_PlanTaxBasis"] = data.cell_value(12, 1),  # B13 13行2列添加5计税依据
        dic["ID"] = identify,  # 实例ID号
        dic["username"] = username,  # 用户名
        df = pd.DataFrame(dic, index=[0])  # 打包成DataFram

        return df


    def CheckError(self, df):
        """
        主要税种和税率数据逻辑关系核对
        :param df:
        :return:
        """
        # 建立错误空列表：
        errorlist = []
        # 增值税税率1>0
        if abs(df["MainTaxesAndRates_TheVat_rate1"].fillna(0).values) == 0:
            error = "增值税税率:空"
            errorlist.append(error)
        # 企业所得税>0
        if abs(df["MainTaxesAndRates_EnterpriseIncomeTax_rate1"].fillna(0).values) == 0:
            error = "企业所得税:空"
            errorlist.append(error)
        











        return df, errorlist


if __name__ == "__main__":
    d = GetMainTaxesAndRates()