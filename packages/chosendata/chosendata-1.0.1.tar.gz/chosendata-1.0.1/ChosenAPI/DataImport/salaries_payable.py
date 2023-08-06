
import pandas as pd
from ChosenAPI.DataImport.ChangeToNum import ChangeData



class GetSalariesPayable(object):#应付职工薪酬
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
            "SalariesPayable_ShortTermCompensation_last": data.cell_value(3, 1),  # B4 4行2列短期薪酬期初余额
            "SalariesPayable_DefinedContributionPlans_last": data.cell_value(4, 1),  # B5 5行2列离职后福利—设定提存计划期初余额
            "SalariesPayable_TerminationBenefits_last": data.cell_value(5, 1),  # B6 6行2列辞退福利期初余额
            "SalariesPayable_OtherBenefits_last": data.cell_value(6, 1),  # B7 7行2列一年内到期的其他福利期初余额
            "SalariesPayable_Total_last": data.cell_value(7, 1),  # B8 8行2列合计期初余额
            "SalariesPayable_ShortTermCompensation_add": data.cell_value(3, 2),  # C4 4行3列短期薪酬本期增加
            "SalariesPayable_DefinedContributionPlans_add": data.cell_value(4, 2),  # C5 5行3列离职后福利—设定提存计划本期增加
            "SalariesPayable_TerminationBenefits_add": data.cell_value(5, 2),  # C6 6行3列辞退福利本期增加
            "SalariesPayable_OtherBenefits_add": data.cell_value(6, 2),  # C7 7行3列一年内到期的其他福利本期增加
            "SalariesPayable_Total_add": data.cell_value(7, 2),  # C8 8行3列合计本期增加
            "SalariesPayable_ShortTermCompensation_reduce": data.cell_value(3, 3),  # D4 4行4列短期薪酬本期减少
            "SalariesPayable_DefinedContributionPlans_reduce": data.cell_value(4, 3),  # D5 5行4列离职后福利—设定提存计划本期减少
            "SalariesPayable_TerminationBenefits_reduce": data.cell_value(5, 3),  # D6 6行4列辞退福利本期减少
            "SalariesPayable_OtherBenefits_reduce": data.cell_value(6, 3),  # D7 7行4列一年内到期的其他福利本期减少
            "SalariesPayable_Total_reduce": data.cell_value(7, 3),  # D8 8行4列合计本期减少
            "SalariesPayable_ShortTermCompensation_this": data.cell_value(3, 4),  # E4 4行5列短期薪酬期末余额
            "SalariesPayable_DefinedContributionPlans_this": data.cell_value(4, 4),  # E5 5行5列离职后福利—设定提存计划期末余额
            "SalariesPayable_TerminationBenefits_this": data.cell_value(5, 4),  # E6 6行5列辞退福利期末余额
            "SalariesPayable_OtherBenefits_this": data.cell_value(6, 4),  # E7 7行5列一年内到期的其他福利期末余额
            "SalariesPayable_TotalBenefits_this": data.cell_value(7, 4),  # E8 8行5列合计期末余额
            "SalariesPayable_Wage_last": data.cell_value(11, 1),  # B12 12行2列工资、奖金、津贴和补贴期初余额
            "SalariesPayable_EmployeeWelfare_last": data.cell_value(12, 1),  # B13 13行2列职工福利费期初余额
            "SalariesPayable_SocialInsurance_last": data.cell_value(13, 1),  # B14 14行2列社会保险费期初余额
            "SalariesPayable_MedicalInsurance_last": data.cell_value(14, 1),  # B15 15行2列医疗保险费期初余额
            "SalariesPayable_InjuryInsurance_last": data.cell_value(15, 1),  # B16 16行2列工伤保险费期初余额
            "SalariesPayable_MaternityInsurance_last": data.cell_value(16, 1),  # B17 17行2列生育保险费期初余额
            "SalariesPayable_HousingAccumulationFund_last": data.cell_value(17, 1),  # B18 18行2列住房公积金期初余额
            "SalariesPayable_UnionFunds_last": data.cell_value(18, 1),  # B19 19行2列工会经费和职工教育经费期初余额
            "SalariesPayable_ShortPaidAbsence_last": data.cell_value(19, 1),  # B20 20行2列短期带薪缺勤期初余额
            "SalariesPayable_ShortTermProfitSharingPlan_last": data.cell_value(20, 1),  # B21 21行2列短期利润分享计划期初余额
            "SalariesPayable_Other_last": data.cell_value(21, 1),  # B22 22行2列其他期初余额
            "SalariesPayable_Total_lastShortTermCompensation": data.cell_value(22, 1),  # B23 23行2列合计期初余额
            "SalariesPayable_Wage_add": data.cell_value(11, 2),  # C12 12行3列工资、奖金、津贴和补贴本期增加
            "SalariesPayable_EmployeeWelfare_add": data.cell_value(12, 2),  # C13 13行3列职工福利费本期增加
            "SalariesPayable_SocialInsurance_add": data.cell_value(13, 2),  # C14 14行3列社会保险费本期增加
            "SalariesPayable_MedicalInsurance_add": data.cell_value(14, 2),  # C15 15行3列医疗保险费本期增加
            "SalariesPayable_InjuryInsurance_add": data.cell_value(15, 2),  # C16 16行3列工伤保险费本期增加
            "SalariesPayable_MaternityInsurance_add": data.cell_value(16, 2),  # C17 17行3列生育保险费本期增加
            "SalariesPayable_HousingAccumulationFund_add": data.cell_value(17, 2),  # C18 18行3列住房公积金本期增加
            "SalariesPayable_UnionFunds_add": data.cell_value(18, 2),  # C19 19行3列工会经费和职工教育经费本期增加
            "SalariesPayable_ShortPaidAbsence_add": data.cell_value(19, 2),  # C20 20行3列短期带薪缺勤本期增加
            "SalariesPayable_ShortTermProfitSharingPlan_add": data.cell_value(20, 2),  # C21 21行3列短期利润分享计划本期增加
            "SalariesPayable_Other_add": data.cell_value(21, 2),  # C22 22行3列其他本期增加
            "SalariesPayable_TotalAdd": data.cell_value(22, 2),  # C23 23行3列合计本期增加
            "SalariesPayable_Wage_reduce": data.cell_value(11, 3),  # D12 12行4列工资、奖金、津贴和补贴本期减少
            "SalariesPayable_EmployeeWelfare_reduce": data.cell_value(12, 3),  # D13 13行4列职工福利费本期减少
            "SalariesPayable_SocialInsurance_reduce": data.cell_value(13, 3),  # D14 14行4列社会保险费本期减少
            "SalariesPayable_MedicalInsurance_reduce": data.cell_value(14, 3),  # D15 15行4列医疗保险费本期减少
            "SalariesPayable_InjuryInsurance_reduce": data.cell_value(15, 3),  # D16 16行4列工伤保险费本期减少
            "SalariesPayable_MaternityInsurance_reduce": data.cell_value(16, 3),  # D17 17行4列生育保险费本期减少
            "SalariesPayable_HousingAccumulationFund_reduce": data.cell_value(17, 3),  # D18 18行4列住房公积金本期减少
            "SalariesPayable_UnionFunds_reduce": data.cell_value(18, 3),  # D19 19行4列工会经费和职工教育经费本期减少
            "SalariesPayable_ShortPaidAbsence_reduce": data.cell_value(19, 3),  # D20 20行4列短期带薪缺勤本期减少
            "SalariesPayable_ShortTermProfitSharingPlan_reduce": data.cell_value(20, 3),  # D21 21行4列短期利润分享计划本期减少
            "SalariesPayable_Other_reduce": data.cell_value(21, 3),  # D22 22行4列其他本期减少
            "SalariesPayable_TotalReduce": data.cell_value(22, 3),  # D23 23行4列合计本期减少
            "SalariesPayable_Wage_this": data.cell_value(11, 4),  # E12 12行5列工资、奖金、津贴和补贴期末余额
            "SalariesPayable_EmployeeWelfare_this": data.cell_value(12, 4),  # E13 13行5列职工福利费期末余额
            "SalariesPayable_SocialInsurance_this": data.cell_value(13, 4),  # E14 14行5列社会保险费期末余额
            "SalariesPayable_MedicalInsurance_this": data.cell_value(14, 4),  # E15 15行5列医疗保险费期末余额
            "SalariesPayable_InjuryInsurance_this": data.cell_value(15, 4),  # E16 16行5列工伤保险费期末余额
            "SalariesPayable_MaternityInsurance_this": data.cell_value(16, 4),  # E17 17行5列生育保险费期末余额
            "SalariesPayable_HousingAccumulationFund_this": data.cell_value(17, 4),  # E18 18行5列住房公积金期末余额
            "SalariesPayable_UnionFunds_this": data.cell_value(18, 4),  # E19 19行5列工会经费和职工教育经费期末余额
            "SalariesPayable_ShortPaidAbsence_this": data.cell_value(19, 4),  # E20 20行5列短期带薪缺勤期末余额
            "SalariesPayable_ShortTermProfitSharingPlan_this": data.cell_value(20, 4),  # E21 21行5列短期利润分享计划期末余额
            "SalariesPayable_Other_this": data.cell_value(21, 4),  # E22 22行5列其他期末余额
            "SalariesPayable_Total_this": data.cell_value(22, 4),  # E23 23行5列合计期末余额
            "SalariesPayable_BasicEndowmentInsurance_last": data.cell_value(26, 1),  # B27 27行2列基本养老保险费期初余额
            "SalariesPayable_UnemploymentInsurance_last": data.cell_value(27, 1),  # B28 28行2列失业保险费期初余额
            "SalariesPayable_EnterpriseAnnuityPayment_last": data.cell_value(28, 1),  # B29 29行2列企业年金缴费期初余额
            "SalariesPayable_Total_lastDefinedContributionPlans": data.cell_value(29, 1),  # B30 30行2列合计期初余额
            "SalariesPayable_BasicEndowmentInsurance_add": data.cell_value(26, 2),  # C27 27行3列基本养老保险费本期增加
            "SalariesPayable_UnemploymentInsurance_add": data.cell_value(27, 2),  # C28 28行3列失业保险费本期增加
            "SalariesPayable_EnterpriseAnnuityPayment_add": data.cell_value(28, 2),  # C29 29行3列企业年金缴费本期增加
            "SalariesPayable_Total_addDefinedContributionPlans": data.cell_value(29, 2),  # C30 30行3列合计本期增加
            "SalariesPayable_BasicEndowmentInsurance_reduce": data.cell_value(26, 3),  # D27 27行4列基本养老保险费本期减少
            "SalariesPayable_UnemploymentInsurance_reduce": data.cell_value(27, 3),  # D28 28行4列失业保险费本期减少
            "SalariesPayable_EnterpriseAnnuityPayment_reduce": data.cell_value(28, 3),  # D29 29行4列企业年金缴费本期减少
            "SalariesPayable_Total_reduceDefinedContributionPlans": data.cell_value(29, 3),  # D30 30行4列合计本期减少
            "SalariesPayable_BasicEndowmentInsurance_this": data.cell_value(26, 4),  # E27 27行5列基本养老保险费期末余额
            "SalariesPayable_UnemploymentInsurance_this": data.cell_value(27, 4),  # E28 28行5列失业保险费期末余额
            "SalariesPayable_EnterpriseAnnuityPayment_this": data.cell_value(28, 4),  # E29 29行5列企业年金缴费期末余额
            "SalariesPayable_Total_thisDefinedContributionPlans": data.cell_value(29, 4),  # E30 30行5列合计期末余额


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
        dic["SalariesPayable_Remark"] = data.cell_value(31, 1),  # B32 32行2列说明
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
        # 应付职工薪酬列示期初余额:短期薪酬+离职后福利—设定提存计划+辞退福利+一年内到期的其他福利=合计
        if abs(df["SalariesPayable_ShortTermCompensation_last"].fillna(0).values + df["SalariesPayable_DefinedContributionPlans_last"].fillna(0).values + df["SalariesPayable_TerminationBenefits_last"].fillna(0).values + df["SalariesPayable_OtherBenefits_last"].fillna(0).values - df["SalariesPayable_Total_last"].fillna(0).values) > 0.01:
            error = "应付职工薪酬列示期初余额:短期薪酬+离职后福利—设定提存计划+辞退福利+一年内到期的其他福利<>合计"
            errorlist.append(error)
        # 应付职工薪酬列示本期增加:短期薪酬+离职后福利—设定提存计划+辞退福利+一年内到期的其他福利=合计
        if abs(df["SalariesPayable_ShortTermCompensation_add"].fillna(0).values + df["SalariesPayable_DefinedContributionPlans_add"].fillna(0).values + df["SalariesPayable_TerminationBenefits_add"].fillna(0).values + df["SalariesPayable_OtherBenefits_add"].fillna(0).values - df["SalariesPayable_Total_add"].fillna(0).values) > 0.01:
            error = "应付职工薪酬列示本期增加:短期薪酬+离职后福利—设定提存计划+辞退福利+一年内到期的其他福利<>合计"
            errorlist.append(error)
        # 应付职工薪酬列示本期减少:短期薪酬+离职后福利—设定提存计划+辞退福利+一年内到期的其他福利=合计
        if abs(df["SalariesPayable_ShortTermCompensation_reduce"].fillna(0).values + df["SalariesPayable_DefinedContributionPlans_reduce"].fillna(0).values + df["SalariesPayable_TerminationBenefits_reduce"].fillna(0).values + df["SalariesPayable_OtherBenefits_reduce"].fillna(0).values - df["SalariesPayable_Total_reduce"].fillna(0).values) > 0.01:
            error = "应付职工薪酬列示本期减少:短期薪酬+离职后福利—设定提存计划+辞退福利+一年内到期的其他福利<>合计"
            errorlist.append(error)
        # 应付职工薪酬列示期末余额:短期薪酬+离职后福利—设定提存计划+辞退福利+一年内到期的其他福利=合计
        if abs(df["SalariesPayable_ShortTermCompensation_this"].fillna(0).values + df["SalariesPayable_DefinedContributionPlans_this"].fillna(0).values + df["SalariesPayable_TerminationBenefits_this"].fillna(0).values + df["SalariesPayable_OtherBenefits_this"].fillna(0).values - df["SalariesPayable_TotalBenefits_this"].fillna(0).values) > 0.01:
            error = "应付职工薪酬列示期末余额:短期薪酬+离职后福利—设定提存计划+辞退福利+一年内到期的其他福利<>合计"
            errorlist.append(error)
        # 短期薪酬期初余额：工资、奖金、津贴和补贴+职工福利费+社会保险费+住房公积金+工会经费和职工教育经费+短期带薪缺勤+短期利润分享计划+其他=合计
        if abs(df["SalariesPayable_Wage_last"].fillna(0).values + df["SalariesPayable_EmployeeWelfare_last"].fillna(0).values + df["SalariesPayable_SocialInsurance_last"].fillna(0).values + df["SalariesPayable_HousingAccumulationFund_last"].fillna(0).values + df["SalariesPayable_UnionFunds_last"].fillna(0).values + df["SalariesPayable_ShortPaidAbsence_last"].fillna(0).values + df["SalariesPayable_ShortTermProfitSharingPlan_last"].fillna(0).values + df["SalariesPayable_Other_last"].fillna(0).values - df["SalariesPayable_Total_lastShortTermCompensation"].fillna(0).values) > 0.01:
            error = "短期薪酬期初余额：工资、奖金、津贴和补贴+职工福利费+社会保险费+住房公积金+工会经费和职工教育经费+短期带薪缺勤+短期利润分享计划+其他<>合计"
            errorlist.append(error)
        # 短期薪酬本期增加：工资、奖金、津贴和补贴+职工福利费+社会保险费+住房公积金+工会经费和职工教育经费+短期带薪缺勤+短期利润分享计划+其他=合计
        if abs(df["SalariesPayable_Wage_add"].fillna(0).values + df["SalariesPayable_EmployeeWelfare_add"].fillna(0).values + df["SalariesPayable_SocialInsurance_add"].fillna(0).values + df["SalariesPayable_HousingAccumulationFund_add"].fillna(0).values + df["SalariesPayable_UnionFunds_add"].fillna(0).values + df["SalariesPayable_ShortPaidAbsence_add"].fillna(0).values + df["SalariesPayable_ShortTermProfitSharingPlan_add"].fillna(0).values + df["SalariesPayable_Other_add"].fillna(0).values - df["SalariesPayable_TotalAdd"].fillna(0).values) > 0.01:
            error = "短期薪酬本期增加：工资、奖金、津贴和补贴+职工福利费+社会保险费+住房公积金+工会经费和职工教育经费+短期带薪缺勤+短期利润分享计划+其他<>合计"
            errorlist.append(error)
        # 短期薪酬本期减少：工资、奖金、津贴和补贴+职工福利费+社会保险费+住房公积金+工会经费和职工教育经费+短期带薪缺勤+短期利润分享计划+其他=合计
        if abs(df["SalariesPayable_Wage_reduce"].fillna(0).values + df["SalariesPayable_EmployeeWelfare_reduce"].fillna(0).values + df["SalariesPayable_SocialInsurance_reduce"].fillna(0).values + df["SalariesPayable_HousingAccumulationFund_reduce"].fillna(0).values + df["SalariesPayable_UnionFunds_reduce"].fillna(0).values + df["SalariesPayable_ShortPaidAbsence_reduce"].fillna(0).values + df["SalariesPayable_ShortTermProfitSharingPlan_reduce"].fillna(0).values + df["SalariesPayable_Other_reduce"].fillna(0).values - df["SalariesPayable_TotalReduce"].fillna(0).values) > 0.01:
            error = "短期薪酬本期减少：工资、奖金、津贴和补贴+职工福利费+社会保险费+住房公积金+工会经费和职工教育经费+短期带薪缺勤+短期利润分享计划+其他<>合计"
            errorlist.append(error)
        # 短期薪酬期末余额：工资、奖金、津贴和补贴+职工福利费+社会保险费+住房公积金+工会经费和职工教育经费+短期带薪缺勤+短期利润分享计划+其他=合计
        if abs(df["SalariesPayable_Wage_this"].fillna(0).values + df["SalariesPayable_EmployeeWelfare_this"].fillna(0).values + df["SalariesPayable_SocialInsurance_this"].fillna(0).values + df["SalariesPayable_HousingAccumulationFund_this"].fillna(0).values + df["SalariesPayable_UnionFunds_this"].fillna(0).values + df["SalariesPayable_ShortPaidAbsence_this"].fillna(0).values + df["SalariesPayable_ShortTermProfitSharingPlan_this"].fillna(0).values + df["SalariesPayable_Other_this"].fillna(0).values - df["SalariesPayable_Total_this"].fillna(0).values) > 0.01:
            error = "短期薪酬期末余额：工资、奖金、津贴和补贴+职工福利费+社会保险费+住房公积金+工会经费和职工教育经费+短期带薪缺勤+短期利润分享计划+其他<>合计"
            errorlist.append(error)
        # 设定提存计划列示期初余额：基本养老保险费+失业保险费+企业年金缴费=合计
        if abs(df["SalariesPayable_BasicEndowmentInsurance_last"].fillna(0).values + df["SalariesPayable_UnemploymentInsurance_last"].fillna(0).values + df["SalariesPayable_EnterpriseAnnuityPayment_last"].fillna(0).values - df["SalariesPayable_Total_lastDefinedContributionPlans"].fillna(0).values) > 0.01:
            error = "设定提存计划列示期初余额：基本养老保险费+失业保险费+企业年金缴费<>合计"
            errorlist.append(error)
        # 设定提存计划列示本期增加：基本养老保险费+失业保险费+企业年金缴费=合计
        if abs(df["SalariesPayable_BasicEndowmentInsurance_add"].fillna(0).values + df["SalariesPayable_UnemploymentInsurance_add"].fillna(0).values + df["SalariesPayable_EnterpriseAnnuityPayment_add"].fillna(0).values - df["SalariesPayable_Total_addDefinedContributionPlans"].fillna(0).values) > 0.01:
            error = "设定提存计划列示本期增加：基本养老保险费+失业保险费+企业年金缴费<>合计"
            errorlist.append(error)
        # 设定提存计划列示本期减少：基本养老保险费+失业保险费+企业年金缴费=合计
        if abs(df["SalariesPayable_BasicEndowmentInsurance_reduce"].fillna(0).values + df["SalariesPayable_UnemploymentInsurance_reduce"].fillna(0).values + df["SalariesPayable_EnterpriseAnnuityPayment_reduce"].fillna(0).values - df["SalariesPayable_Total_reduceDefinedContributionPlans"].fillna(0).values) > 0.01:
            error = "设定提存计划列示本期减少：基本养老保险费+失业保险费+企业年金缴费<>合计"
            errorlist.append(error)
        # 设定提存计划列示期末余额：基本养老保险费+失业保险费+企业年金缴费=合计
        if abs(df["SalariesPayable_BasicEndowmentInsurance_this"].fillna(0).values + df["SalariesPayable_UnemploymentInsurance_this"].fillna(0).values + df["SalariesPayable_EnterpriseAnnuityPayment_this"].fillna(0).values - df["SalariesPayable_Total_thisDefinedContributionPlans"].fillna(0).values) > 0.01:
            error = "设定提存计划列示期末余额：基本养老保险费+失业保险费+企业年金缴费<>合计"
            errorlist.append(error)
        











        return df, errorlist


if __name__ == "__main__":
    d = GetSalariesPayable()