
import pandas as pd
from ChosenAPI.DataImport.ChangeToNum import ChangeData



class GetEmployeeSituation(object):#员工情况
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
            # 职能类别
            "EmployeeSituation_management_number": data.cell_value(2, 1),  # B3 3行2列管理层人数
            "EmployeeSituation_administrative_number": data.cell_value(3, 1),  # B4 4行2列行政人事人员人数
            "EmployeeSituation_financial_number": data.cell_value(4, 1),  # B5 5行2列财务人员人数
            "EmployeeSituation_production_number": data.cell_value(5, 1),  # B6 6行2列生产人员人数
            "EmployeeSituation_ResearchAndDevelopment_number": data.cell_value(6, 1),  # B7 7行2列研发人员人数
            "EmployeeSituation_sales_number": data.cell_value(7, 1),  # B8 8行2列销售人员人数
            "EmployeeSituation_others_number": data.cell_value(8, 1),  # B9 9行2列其他人员人数
            "EmployeeSituation_Total_number": data.cell_value(9, 1),  # B10 10行2列合计人数
            "EmployeeSituation_management_ratio": data.cell_value(2, 2),  # C3 3行3列管理层比例
            "EmployeeSituation_administrative_ratio": data.cell_value(3, 2),  # C4 4行3列行政人事人员比例
            "EmployeeSituation_financial_ratio": data.cell_value(4, 2),  # C5 5行3列财务人员比例
            "EmployeeSituation_production_ratio": data.cell_value(5, 2),  # C6 6行3列生产人员比例
            "EmployeeSituation_ResearchAndDevelopment_ratio": data.cell_value(6, 2),  # C7 7行3列研发人员比例
            "EmployeeSituation_sales_ratio": data.cell_value(7, 2),  # C8 8行3列销售人员比例
            "EmployeeSituation_others_ratio": data.cell_value(8, 2),  # C9 9行3列其他人员比例
            "EmployeeSituation_Total_ratio": data.cell_value(9, 2),  # C10 10行3列合计比例

            # 学历情况
            "EmployeeSituation_postdoctor_number": data.cell_value(12, 1),  # B3 13行2列博士后人数
            "EmployeeSituation_doctor_number": data.cell_value(13, 1),  # B3 14行2列博士人数
            "EmployeeSituation_master_number": data.cell_value(14, 1),  # B3 15行2列硕士人数
            "EmployeeSituation_bachelor_number": data.cell_value(15, 1),  # B3 16行2列本科人数
            "EmployeeSituation_specialty_number": data.cell_value(16, 1),  # B3 17行2列大专人数
            "EmployeeSituation_othereducation_number": data.cell_value(17, 1),  # B3 18行2列其他学历人数
            "EmployeeSituation_postdoctor_ratio": data.cell_value(12, 2),  # B3 13行3列博士后比例
            "EmployeeSituation_doctor_ratio": data.cell_value(13, 2),  # B3 14行3列博士比例
            "EmployeeSituation_master_ratio": data.cell_value(14, 2),  # B3 15行3列硕士比例
            "EmployeeSituation_bachelor_ratio": data.cell_value(15, 2),  # B3 16行3列本科比例
            "EmployeeSituation_specialty_ratio": data.cell_value(16, 2),  # B3 17行3列大专比例
            "EmployeeSituation_othereducation_ratio": data.cell_value(17, 2),  # B3 18行3列其他学历比例

            # 工资总额
            "avg_salary": data.cell_value(20, 1),  # B3 21行2列博士后人数


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
        dic["EmployeeSituation_Remark"] = data.cell_value(22, 1),  # B23 21行2列#说明
        dic["ID"] = identify,  # 实例ID号
        dic["username"] = username,  # 用户名
        df = pd.DataFrame(dic, index=[0])  # 打包成DataFram

        return df


    def CheckError(self, df):
        """
        员工情况数据逻辑关系核对
        :param df:
        :return:
        """
        # 建立错误空列表：
        errorlist = []
        # 人数：管理层+行政人事人员+财务人员+生产人员+研发人员+销售人员+外包人员=合计
        if abs(df["EmployeeSituation_management_number"].fillna(0).values + df["EmployeeSituation_administrative_number"].fillna(0).values + df["EmployeeSituation_financial_number"].fillna(0).values + df["EmployeeSituation_production_number"].fillna(0).values + df["EmployeeSituation_ResearchAndDevelopment_number"].fillna(0).values + df["EmployeeSituation_sales_number"].fillna(0).values + df["EmployeeSituation_others_number"].fillna(0).values - df["EmployeeSituation_Total_number"].fillna(0).values) > 0.01:
            error = "人数：管理层+行政人事人员+财务人员+生产人员+研发人员+销售人员+外包人员=合计<>期末合计"
            errorlist.append(error)
        # 职工薪酬总额：管理层+行政人事人员+财务人员+生产人员+研发人员+销售人员+外包人员=合计
        if abs(df["EmployeeSituation_management_ratio"].fillna(0).values + df["EmployeeSituation_administrative_ratio"].fillna(0).values + df["EmployeeSituation_financial_ratio"].fillna(0).values + df["EmployeeSituation_production_ratio"].fillna(0).values + df["EmployeeSituation_ResearchAndDevelopment_ratio"].fillna(0).values + df["EmployeeSituation_sales_ratio"].fillna(0).values + df["EmployeeSituation_others_ratio"].fillna(0).values - df["EmployeeSituation_Total_ratio"].fillna(0).values) > 0.01:
            error = "职工薪酬总额：管理层+行政人事人员+财务人员+生产人员+研发人员+销售人员+外包人员=合计<>期末合计"
            errorlist.append(error)
        











        return df, errorlist


if __name__ == "__main__":
    d = GetEmployeeSituation()