from xlrd import xldate_as_tuple
from datetime import datetime
import pandas as pd
from ChosenAPI.DataImport.ChangeToNum import ChangeData



class GetLongtermAccountPayable(object):#长期应付款
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
            "LongtermAccountPayable_this": data.cell_value(3, 1),  # B4 4行2列长期应付款期末余额
            "LongtermAccountPayable_SP_this": data.cell_value(4, 1),  # B5 5行2列专项应付款期末余额
            "LongtermAccountPayable_Pay_this": data.cell_value(5, 1),# B6 6行2列长期应付职工薪酬期末余额
            "LongtermAccountPayable_Total_this": data.cell_value(6, 1),  # B7 7行2列合计期末余额
            "LongtermAccountPayable_last": data.cell_value(3, 2),  # C4 4行3列长期应付款期初余额
            "LongtermAccountPayable_SP_last": data.cell_value(4, 2),  # C5 5行3列专项应付款期初余额
            "LongtermAccountPayable_Pay_last": data.cell_value(5, 2),# C6 6行3列长期应付职工薪酬期初余额
            "LongtermAccountPayable_Total_last": data.cell_value(6, 2),  # C7 7行3列合计期初余额
            "LongtermAccountPayable_ListProject1_this": data.cell_value(10, 1),  # B11 11行2列项目1期末余额
            "LongtermAccountPayable_ListProject2_this": data.cell_value(11, 1),  # B12 12行2列项目2期末余额
            "LongtermAccountPayable_ListProject3_this": data.cell_value(12, 1),  # B13 13行2列项目3期末余额
            "LongtermAccountPayable_ListProject4_this": data.cell_value(13, 1),  # B14 14行2列项目4期末余额
            "LongtermAccountPayable_ListProject5_this": data.cell_value(14, 1),  # B15 15行2列项目5期末余额
            "LongtermAccountPayable_ListTotal_this": data.cell_value(15, 1),  # B16 16行2列合计期末余额
            "LongtermAccountPayable_ListProject1_last": data.cell_value(10, 2),  # C11 11行3列项目1期初余额
            "LongtermAccountPayable_ListProject2_last": data.cell_value(11, 2),  # C12 12行3列项目2期初余额
            "LongtermAccountPayable_ListProject3_last": data.cell_value(12, 2),  # C13 13行3列项目3期初余额
            "LongtermAccountPayable_ListProject4_last": data.cell_value(13, 2),  # C14 14行3列项目4期初余额
            "LongtermAccountPayable_ListProject5_last": data.cell_value(14, 2),  # C15 15行3列项目5期初余额
            "LongtermAccountPayable_ListTotal_last": data.cell_value(15, 2),  # C16 16行3列合计期初余额
            "LongtermAccountPayable_SPProject1_last": data.cell_value(19, 1),  # B20 20行2列项目1期初余额
            "LongtermAccountPayable_SPProject2_last": data.cell_value(20, 1),  # B21 21行2列项目2期初余额
            "LongtermAccountPayable_SPProject3_last": data.cell_value(21, 1),  # B22 22行2列项目3期初余额
            "LongtermAccountPayable_SPProject4_last": data.cell_value(22, 1),  # B23 23行2列项目4期初余额
            "LongtermAccountPayable_SPProject5_last": data.cell_value(23, 1),  # B24 24行2列项目5期初余额
            "LongtermAccountPayable_SPTotal_last": data.cell_value(24, 1),  # B25 25行2列合计期初余额
            "LongtermAccountPayable_SPProject1_add": data.cell_value(19, 2),  # C20 20行3列项目1本期增加
            "LongtermAccountPayable_SPProject2_add": data.cell_value(20, 2),  # C21 21行3列项目2本期增加
            "LongtermAccountPayable_SPProject3_add": data.cell_value(21, 2),  # C22 22行3列项目3本期增加
            "LongtermAccountPayable_SPProject4_add": data.cell_value(22, 2),  # C23 23行3列项目4本期增加
            "LongtermAccountPayable_SPProject5_add": data.cell_value(23, 2),  # C24 24行3列项目5本期增加
            "LongtermAccountPayable_SPTotal_add": data.cell_value(24, 2),  # C25 25行3列合计本期增加
            "LongtermAccountPayable_SPProject1_reduce": data.cell_value(19, 3),  # D20 20行4列项目1本期减少
            "LongtermAccountPayable_SPProject2_reduce": data.cell_value(20, 3),  # D21 21行4列项目2本期减少
            "LongtermAccountPayable_SPProject3_reduce": data.cell_value(21, 3),  # D22 22行4列项目3本期减少
            "LongtermAccountPayable_SPProject4_reduce": data.cell_value(22, 3),  # D23 23行4列项目4本期减少
            "LongtermAccountPayable_SPProject5_reduce": data.cell_value(23, 3),  # D24 24行4列项目5本期减少
            "LongtermAccountPayable_SPTotal_reduce": data.cell_value(24, 3),  # D25 25行4列合计本期减少
            "LongtermAccountPayable_SPProject1_this": data.cell_value(19, 4),  # E20 20行5列项目1期末余额
            "LongtermAccountPayable_SPProject2_this": data.cell_value(20, 4),  # E21 21行5列项目2期末余额
            "LongtermAccountPayable_SPProject3_this": data.cell_value(21, 4),  # E22 22行5列项目3期末余额
            "LongtermAccountPayable_SPProject4_this": data.cell_value(22, 4),  # E23 23行5列项目4期末余额
            "LongtermAccountPayable_SPProject5_this": data.cell_value(23, 4),  # E24 24行5列项目5期末余额
            "LongtermAccountPayable_SPTotal_this": data.cell_value(24, 4),  # E25 25行5列合计期末余额
            "LongtermAccountPayable_Post_this": data.cell_value(28, 1),  # B29 29行2列离职后福利-设定受益计划净负债期末余额
            "LongtermAccountPayable_Ter_this": data.cell_value(29, 1),  # B30 30行2列辞退福利期末余额
            "LongtermAccountPayable_OtherLong_this": data.cell_value(30, 1),  # B31 31行2列其他长期福利期末余额
            "LongtermAccountPayable_Paytotal_this": data.cell_value(31, 1),# B32 32行2列合计期末余额
            "LongtermAccountPayable_Post_last": data.cell_value(28, 2),  # C29 29行3列离职后福利-设定受益计划净负债期初余额
            "LongtermAccountPayable_Ter_last": data.cell_value(29, 2),  # C30 30行3列辞退福利期初余额
            "LongtermAccountPayable_OtherLong_last": data.cell_value(30, 2),  # C31 31行3列其他长期福利期初余额
            "LongtermAccountPayable_Paytotal_last": data.cell_value(31, 2),# C32 32行3列合计期初余额
            "LongtermAccountPayable_LastA_CP": data.cell_value(35, 1),  # B36 36行2列设定受益计划义务现值期初余额本期发生额
            "LongtermAccountPayable_SetA_CP": data.cell_value(36, 1),# B37 37行2列设定受益计划义务现值计入当期损益的设定受益成本本期发生额
            "LongtermAccountPayable_CPA_CP": data.cell_value(37, 1),# B38 38行2列设定受益计划义务现值当期服务成本本期发生额
            "LongtermAccountPayable_FormerlyA_CP": data.cell_value(38, 1),# B39 39行2列设定受益计划义务现值过去服务成本本期发生额
            "LongtermAccountPayable_ClearingGainsA_CP": data.cell_value(39, 1),# B40 40行2列设定受益计划义务现值结算利得（损失以“－”表示）本期发生额
            "LongtermAccountPayable_NetInterestA_CP": data.cell_value(40, 1),# B41 41行2列设定受益计划义务现值利息净额本期发生额
            "LongtermAccountPayable_SetRA_CP": data.cell_value(41, 1),# B42 42行2列设定受益计划义务现值计入其他综合收益的设定收益成本本期发生额
            "LongtermAccountPayable_ActA_CP": data.cell_value(42, 1),# B43 43行2列设定受益计划义务现值精算利得（损失以“－”表示）本期发生额
            "LongtermAccountPayable_OtherChangesA_CP": data.cell_value(43, 1),# B44 44行2列设定受益计划义务现值其他变动本期发生额
            "LongtermAccountPayable_ForThePriceA_CP": data.cell_value(44, 1),# B45 45行2列设定受益计划义务现值结算时支付的对价本期发生额
            "LongtermAccountPayable_WelfareA_CP": data.cell_value(45, 1),  # B46 46行2列设定受益计划义务现值已支付的福利本期发生额
            "LongtermAccountPayable_ThisA_CP": data.cell_value(46, 1),  # B47 47行2列设定受益计划义务现值期末余额本期发生额
            "LongtermAccountPayable_LastA_PP": data.cell_value(35, 2),  # C36 36行3列设定受益计划义务现值期初余额上期发生额
            "LongtermAccountPayable_SetA_PP": data.cell_value(36, 2),# C37 37行3列设定受益计划义务现值计入当期损益的设定受益成本上期发生额
            "LongtermAccountPayable_CPA_PP": data.cell_value(37, 2),# C38 38行3列设定受益计划义务现值当期服务成本上期发生额
            "LongtermAccountPayable_FormerlyA_PP": data.cell_value(38, 2),  # C39 39行3列设定受益计划义务现值过去服务成本上期发生额
            "LongtermAccountPayable_ClearingGainsA_PP": data.cell_value(39, 2),# C40 40行3列设定受益计划义务现值结算利得（损失以“－”表示）上期发生额
            "LongtermAccountPayable_NetInterestA_PP": data.cell_value(40, 2),  # C41 41行3列设定受益计划义务现值利息净额上期发生额
            "LongtermAccountPayable_SetRA_PP": data.cell_value(41, 2),# C42 42行3列设定受益计划义务现值计入其他综合收益的设定收益成本上期发生额
            "LongtermAccountPayable_ActA_PP": data.cell_value(42, 2),# C43 43行3列设定受益计划义务现值精算利得（损失以“－”表示）上期发生额
            "LongtermAccountPayable_OtherChangesA_PP": data.cell_value(43, 2),# C44 44行3列设定受益计划义务现值其他变动上期发生额
            "LongtermAccountPayable_ForThePriceA_PP": data.cell_value(44, 2),# C45 45行3列设定受益计划义务现值结算时支付的对价上期发生额
            "LongtermAccountPayable_WelfareA_PP": data.cell_value(45, 2),  # C46 46行3列设定受益计划义务现值已支付的福利上期发生额
            "LongtermAccountPayable_ThisA_PP": data.cell_value(46, 2),  # C47 47行3列设定受益计划义务现值期末余额上期发生额
            "LongtermAccountPayable_LastB_CP": data.cell_value(50, 1),  # B51 51行2列计划资产期初余额本期发生额
            "LongtermAccountPayable_SetB_CP": data.cell_value(51, 1),# B52 52行2列计划资产计入当期损益的设定受益成本本期发生额
            "LongtermAccountPayable_NetInterestB_CP": data.cell_value(52, 1),  # B53 53行2列计划资产利息净额本期发生额
            "LongtermAccountPayable_SetRB_CP": data.cell_value(53, 1),# B54 54行2列计划资产计入其他综合收益的设定收益成本本期发生额
            "LongtermAccountPayable_PlanB_CP": data.cell_value(54, 1),# B55 55行2列计划资产计划资产回报（计入利息净额的除外）本期发生额
            "LongtermAccountPayable_LastB_PP": data.cell_value(50, 2),  # C51 51行3列计划资产期初余额上期发生额
            "LongtermAccountPayable_SetB_PP": data.cell_value(51, 2),# C52 52行3列计划资产计入当期损益的设定受益成本上期发生额
            "LongtermAccountPayable_NetInterestB_PP": data.cell_value(52, 2),  # C53 53行3列计划资产利息净额上期发生额
            "LongtermAccountPayable_SetRB_PP": data.cell_value(53, 2),# C54 54行3列计划资产计入其他综合收益的设定收益成本上期发生额
            "LongtermAccountPayable_PlanB_PP": data.cell_value(54, 2),# C55 55行3列计划资产计划资产回报（计入利息净额的除外）上期发生额
            "LongtermAccountPayable_ChangeB_CP": data.cell_value(55, 1),# B56 56行2列计划资产资产上限影响的变动（计入利息净额的除外）本期发生额
            "LongtermAccountPayable_OtherChangesB_CP": data.cell_value(56, 1),  # B57 57行2列计划资产其他变动本期发生额
            "LongtermAccountPayable_ThisB_CP": data.cell_value(57, 1),  # B58 58行2列计划资产期末余额本期发生额
            "LongtermAccountPayable_ChangeB_PP": data.cell_value(55, 2),# C56 56行3列计划资产资产上限影响的变动（计入利息净额的除外）上期发生额
            "LongtermAccountPayable_OtherChangesB_PP": data.cell_value(56, 2),  # C57 57行3列计划资产其他变动上期发生额
            "LongtermAccountPayable_ThisB_PP": data.cell_value(57, 2),  # C58 58行3列计划资产期末余额上期发生额
            "LongtermAccountPayable_LastC_CP": data.cell_value(61, 1),  # B62 62行2列设定受益计划净负债期初余额本期发生额
            "LongtermAccountPayable_SetC_CP": data.cell_value(62, 1),# B63 63行2列设定受益计划净负债计入当期损益的设定受益成本本期发生额
            "LongtermAccountPayable_SetRC_CP": data.cell_value(63, 1),# B64 64行2列设定受益计划净负债计入其他综合收益的设定收益成本本期发生额
            "LongtermAccountPayable_OtherChangesC_CP": data.cell_value(64, 1),# B65 65行2列设定受益计划净负债其他变动本期发生额
            "LongtermAccountPayable_ThisC_CP": data.cell_value(65, 1),  # B66 66行2列设定受益计划净负债期末余额本期发生额
            "LongtermAccountPayable_LastC_PP": data.cell_value(61, 2),  # C62 62行3列设定受益计划净负债期初余额上期发生额
            "LongtermAccountPayable_SetC_PP": data.cell_value(62, 2),# C63 63行3列设定受益计划净负债计入当期损益的设定受益成本上期发生额
            "LongtermAccountPayable_SetRC_PP": data.cell_value(63, 2),# C64 64行3列设定受益计划净负债计入其他综合收益的设定收益成本上期发生额
            "LongtermAccountPayable_OtherChangesC_PP": data.cell_value(64, 2),  # C65 65行3列设定受益计划净负债其他变动上期发生额
            "LongtermAccountPayable_ThisC_PP": data.cell_value(65, 2),  # C66 66行3列设定受益计划净负债期末余额上期发生额


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
        dic["LongtermAccountPayable_Remark"] = data.cell_value(67, 1),  # B68 68行2列说明
        dic["LongtermAccountPayable_SPProject1_reason"] = data.cell_value(19, 5),  # F20 20行6列项目1形成原因
        dic["LongtermAccountPayable_SPProject2_reason"] = data.cell_value(20, 5),  # F21 21行6列项目2形成原因
        dic["LongtermAccountPayable_SPProject3_reason"] = data.cell_value(21, 5),  # F22 22行6列项目3形成原因
        dic["LongtermAccountPayable_SPProject4_reason"] = data.cell_value(22, 5),  # F23 23行6列项目4形成原因
        dic["LongtermAccountPayable_SPProject5_reason"] = data.cell_value(23, 5),  # F24 24行6列项目5形成原因
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
        # 分类期末余额:长期应付款+专项应付款+长期应付职工薪酬=合计
        if abs(df["LongtermAccountPayable_this"].fillna(0).values + df["LongtermAccountPayable_SP_this"].fillna(0).values + df["LongtermAccountPayable_Pay_this"].fillna(0).values - df["LongtermAccountPayable_Total_this"].fillna(0).values) > 0.01:
            error = "分类期末余额:长期应付款+专项应付款+长期应付职工薪酬<>合计"
            errorlist.append(error)
        # 分类期初余额:长期应付款+专项应付款+长期应付职工薪酬=合计
        if abs(df["LongtermAccountPayable_last"].fillna(0).values + df["LongtermAccountPayable_SP_last"].fillna(0).values + df["LongtermAccountPayable_Pay_last"].fillna(0).values - df["LongtermAccountPayable_Total_last"].fillna(0).values) > 0.01:
            error = "分类期初余额:长期应付款+专项应付款+长期应付职工薪酬<>合计"
            errorlist.append(error)
        # 按款项性质列示的长期应付款期末余额 :项目1+项目2+项目3+项目4+项目5=合计
        if abs(df["LongtermAccountPayable_ListProject1_this"].fillna(0).values + df["LongtermAccountPayable_ListProject2_this"].fillna(0).values + df["LongtermAccountPayable_ListProject3_this"].fillna(0).values + df["LongtermAccountPayable_ListProject4_this"].fillna(0).values + df["LongtermAccountPayable_ListProject5_this"].fillna(0).values - df["LongtermAccountPayable_ListTotal_this"].fillna(0).values) > 0.01:
            error = "按款项性质列示的长期应付款期末余额:项目1+项目2+项目3+项目4+项目5<>合计"
            errorlist.append(error)
        # 按款项性质列示的长期应付款期初余额 :项目1+项目2+项目3+项目4+项目5=合计
        if abs(df["LongtermAccountPayable_ListProject1_last"].fillna(0).values + df["LongtermAccountPayable_ListProject2_last"].fillna(0).values + df["LongtermAccountPayable_ListProject3_last"].fillna(0).values + df["LongtermAccountPayable_ListProject4_last"].fillna(0).values + df["LongtermAccountPayable_ListProject5_last"].fillna(0).values - df["LongtermAccountPayable_ListTotal_last"].fillna(0).values) > 0.01:
            error = "按款项性质列示的长期应付款期初余额:项目1+项目2+项目3+项目4+项目5<>合计"
            errorlist.append(error)
        # 专项应付款期初余额:项目1+项目2+项目3+项目4+项目5=合计
        if abs(df["LongtermAccountPayable_SPProject1_last"].fillna(0).values + df["LongtermAccountPayable_SPProject2_last"].fillna(0).values + df["LongtermAccountPayable_SPProject3_last"].fillna(0).values + df["LongtermAccountPayable_SPProject4_last"].fillna(0).values + df["LongtermAccountPayable_SPProject5_last"].fillna(0).values - df["LongtermAccountPayable_SPTotal_last"].fillna(0).values) > 0.01:
            error = "专项应付款期初余额:项目1+项目2+项目3+项目4+项目5<>合计"
            errorlist.append(error)
        # 专项应付款本期增加:项目1+项目2+项目3+项目4+项目5=合计
        if abs(df["LongtermAccountPayable_SPProject1_add"].fillna(0).values + df["LongtermAccountPayable_SPProject2_add"].fillna(0).values + df["LongtermAccountPayable_SPProject3_add"].fillna(0).values + df["LongtermAccountPayable_SPProject4_add"].fillna(0).values + df["LongtermAccountPayable_SPProject5_add"].fillna(0).values - df["LongtermAccountPayable_SPTotal_add"].fillna(0).values) > 0.01:
            error = "专项应付款本期增加:项目1+项目2+项目3+项目4+项目5<>合计"
            errorlist.append(error)
        # 专项应付款本期减少:项目1+项目2+项目3+项目4+项目5=合计
        if abs(df["LongtermAccountPayable_SPProject1_reduce"].fillna(0).values + df["LongtermAccountPayable_SPProject2_reduce"].fillna(0).values + df["LongtermAccountPayable_SPProject3_reduce"].fillna(0).values + df["LongtermAccountPayable_SPProject4_reduce"].fillna(0).values + df["LongtermAccountPayable_SPProject5_reduce"].fillna(0).values - df["LongtermAccountPayable_SPTotal_reduce"].fillna(0).values) > 0.01:
            error = "专项应付款本期减少:项目1+项目2+项目3+项目4+项目5<>合计"
            errorlist.append(error)
        # 专项应付款期末余额:项目1+项目2+项目3+项目4+项目5=合计
        if abs(df["LongtermAccountPayable_SPProject1_this"].fillna(0).values + df["LongtermAccountPayable_SPProject2_this"].fillna(0).values + df["LongtermAccountPayable_SPProject3_this"].fillna(0).values + df["LongtermAccountPayable_SPProject4_this"].fillna(0).values + df["LongtermAccountPayable_SPProject5_this"].fillna(0).values - df["LongtermAccountPayable_SPTotal_this"].fillna(0).values) > 0.01:
            error = "专项应付款期末余额:项目1+项目2+项目3+项目4+项目5<>合计"
            errorlist.append(error)
        # 长期应付职工薪酬表期末余额：离职后福利-设定受益计划净负债+辞退福利+其他长期福利=合计
        if abs(df["LongtermAccountPayable_Post_this"].fillna(0).values + df["LongtermAccountPayable_Ter_this"].fillna(0).values + df["LongtermAccountPayable_OtherLong_this"].fillna(0).values - df["LongtermAccountPayable_Paytotal_this"].fillna(0).values) > 0.01:
            error = "长期应付职工薪酬表期末余额：离职后福利-设定受益计划净负债+辞退福利+其他长期福利<>合计"
            errorlist.append(error)
        # 长期应付职工薪酬表期初余额：离职后福利-设定受益计划净负债+辞退福利+其他长期福利=合计
        if abs(df["LongtermAccountPayable_Post_last"].fillna(0).values + df["LongtermAccountPayable_Ter_last"].fillna(0).values + df["LongtermAccountPayable_OtherLong_last"].fillna(0).values - df["LongtermAccountPayable_Paytotal_last"].fillna(0).values) > 0.01:
            error = "长期应付职工薪酬表期初余额：离职后福利-设定受益计划净负债+辞退福利+其他长期福利<>合计"
            errorlist.append(error)











        return df, errorlist


if __name__ == "__main__":
    d = GetLongtermAccountPayable()