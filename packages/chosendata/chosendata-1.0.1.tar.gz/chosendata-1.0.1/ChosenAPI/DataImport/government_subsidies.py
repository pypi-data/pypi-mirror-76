
import pandas as pd
from ChosenAPI.DataImport.ChangeToNum import ChangeData



class GetGovernmentSubsidies(object):#政府补助
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
            "GovernmentSubsidies_SAT_CP_sum": data.cell_value(3, 2),  # C4 4行3列科技项目经费当期损益金额
            "GovernmentSubsidies_Other_CP_sum": data.cell_value(4, 2),  # C5 5行3列其他当期损益金额
            "GovernmentSubsidies_Into_CP_sum": data.cell_value(5, 2),  # C6 6行3列本期递延收益转入当期损益金额
            "GovernmentSubsidies_SendBack_CP_sum": data.cell_value(6, 2),  # C7 7行3列本期政府补助退回当期损益金额
            "GovernmentSubsidies_Total_CP_sum": data.cell_value(7, 2),  # C8 8行3列合计当期损益金额
            "GovernmentSubsidies_SAT_CP_CPS": data.cell_value(3, 4),# E4 4行5列科技项目经费当期损益计入当期损益的金额
            "GovernmentSubsidies_Other_CP_CPS": data.cell_value(4, 4),# E5 5行5列其他当期损益计入当期损益的金额
            "GovernmentSubsidies_Into_CP_CPS": data.cell_value(5, 4),# E6 6行5列本期递延收益转入当期损益计入当期损益的金额
            "GovernmentSubsidies_SendBack_CP_CPS": data.cell_value(6, 4),# E7 7行5列本期政府补助退回当期损益计入当期损益的金额
            "GovernmentSubsidies_Total_CP_CPS": data.cell_value(7, 4),# E8 8行5列合计当期损益计入当期损益的金额
            "GovernmentSubsidies_SAT_DI_add": data.cell_value(12, 3),# D13 13行4列科技项目经费递延收益本期新增金额
            "GovernmentSubsidies_Other_DI_add": data.cell_value(13, 3),  # D14 14行4列其他递延收益本期新增金额
            "GovernmentSubsidies_Total_DI_add": data.cell_value(14, 3),  # D15 15行4列合计递延收益本期新增金额
            "GovernmentSubsidies_SAT_DI_CarryForward": data.cell_value(12, 4),# E13 13行5列科技项目经费递延收益本期结转计入损益或冲减相关成本的金额
            "GovernmentSubsidies_Other_DI_CarryForward": data.cell_value(13, 4),# E14 14行5列其他递延收益本期结转计入损益或冲减相关成本的金额
            "GovernmentSubsidies_Total_DI_CarryForward": data.cell_value(14, 4),# E15 15行5列合计递延收益本期结转计入损益或冲减相关成本的金额
            "GovernmentSubsidies_SAT_DI_OtherChanges": data.cell_value(12, 5),# F13 13行6列科技项目经费递延收益其他变动
            "GovernmentSubsidies_Other_DI_OtherChanges": data.cell_value(13, 5),  # F14 14行6列其他递延收益其他变动
            "GovernmentSubsidies_Total_DI_OtherChanges": data.cell_value(14, 5),  # F15 15行6列合计递延收益其他变动
            "GovernmentSubsidies_SAT_DI_this": data.cell_value(12, 6),# G13 13行7列科技项目经费递延收益期末余额
            "GovernmentSubsidies_Other_DI_this": data.cell_value(13, 6),  # G14 14行7列其他递延收益期末余额
            "GovernmentSubsidies_Total_DI_this": data.cell_value(14, 6),  # G15 15行7列合计递延收益期末余额
            "GovernmentSubsidies_Project1_sum": data.cell_value(18, 1),  # B19 19行2列项目1金额
            "GovernmentSubsidies_Project2_sum": data.cell_value(19, 1),  # B20 20行2列项目2金额
            "GovernmentSubsidies_Project3_sum": data.cell_value(20, 1),  # B21 21行2列项目3金额
            "GovernmentSubsidies_Project4_sum": data.cell_value(21, 1),  # B22 22行2列项目4金额
            "GovernmentSubsidies_Project5_sum": data.cell_value(22, 1),  # B23 23行2列项目5金额
            "GovernmentSubsidies_Total_sum": data.cell_value(23, 1),  # B24 24行2列合计金额


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
        dic["GovernmentSubsidies_Remark"] = data.cell_value(25, 1),  # B26 26行2列说明
        dic["GovernmentSubsidies_SAT_CP_kind"] = data.cell_value(3, 1),  # B4 4行2列科技项目经费当期损益种类（与资产相关/与收益相关）
        dic["GovernmentSubsidies_Other_CP_kind"] = data.cell_value(4, 1),  # B5 5行2列其他当期损益种类（与资产相关/与收益相关）
        dic["GovernmentSubsidies_Into_CP_kind"] = data.cell_value(5, 1),  # B6 6行2列本期递延收益转入当期损益种类（与资产相关/与收益相关）
        dic["GovernmentSubsidies_SendBack_CP_kind"] = data.cell_value(6, 1),  # B7 7行2列本期政府补助退回当期损益种类（与资产相关/与收益相关）
        dic["GovernmentSubsidies_SAT_CP_project"] = data.cell_value(3, 3),  # D4 4行4列科技项目经费当期损益列报项目
        dic["GovernmentSubsidies_Other_CP_project"] = data.cell_value(4, 3),  # D5 5行4列其他当期损益列报项目
        dic["GovernmentSubsidies_Into_CP_project"] = data.cell_value(5, 3),  # D6 6行4列本期递延收益转入当期损益列报项目
        dic["GovernmentSubsidies_SendBack_CP_project"] = data.cell_value(6, 3),  # D7 7行4列本期政府补助退回当期损益列报项目
        dic["GovernmentSubsidies_SAT_DI_kind"] = data.cell_value(12, 1),  # B13 13行2列科技项目经费递延收益种类（与资产相关/与收益相关）
        dic["GovernmentSubsidies_Other_DI_kind"] = data.cell_value(13, 1),  # B14 14行2列其他递延收益种类（与资产相关/与收益相关）
        dic["GovernmentSubsidies_SAT_DI_project"] = data.cell_value(12, 7),  # H13 13行8列科技项目经费递延收益本期结转计入损益或冲减相关成本的列报项目
        dic["GovernmentSubsidies_Other_DI_project"] = data.cell_value(13, 7),  # H14 14行8列其他递延收益本期结转计入损益或冲减相关成本的列报项目
        dic["GovernmentSubsidies_Project1_reason"] = data.cell_value(18, 2),  # C19 19行3列项目1退回原因
        dic["GovernmentSubsidies_Project2_reason"] = data.cell_value(19, 2),  # C20 20行3列项目2退回原因
        dic["GovernmentSubsidies_Project3_reason"] = data.cell_value(20, 2),  # C21 21行3列项目3退回原因
        dic["GovernmentSubsidies_Project4_reason"] = data.cell_value(21, 2),  # C22 22行3列项目4退回原因
        dic["GovernmentSubsidies_Project5_reason"] = data.cell_value(22, 2),  # C23 23行3列项目5退回原因
        dic["GovernmentSubsidies_Project1_project"] = data.cell_value(18, 3),  # D19 19行4列项目1列报项目
        dic["GovernmentSubsidies_Project2_project"] = data.cell_value(19, 3),  # D20 20行4列项目2列报项目
        dic["GovernmentSubsidies_Project3_project"] = data.cell_value(20, 3),  # D21 21行4列项目3列报项目
        dic["GovernmentSubsidies_Project4_project"] = data.cell_value(21, 3),  # D22 22行4列项目4列报项目
        dic["GovernmentSubsidies_Project5_project"] = data.cell_value(22, 3),  # D23 23行4列项目5列报项目
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
        # 补助项目金额：项目1+项目2+项目3+项目4+项目5=合计
        if abs(df["GovernmentSubsidies_Project1_sum"].fillna(0).values + df["GovernmentSubsidies_Project2_sum"].fillna(0).values + df["GovernmentSubsidies_Project3_sum"].fillna(0).values + df["GovernmentSubsidies_Project4_sum"].fillna(0).values + df["GovernmentSubsidies_Project5_sum"].fillna(0).values - df["GovernmentSubsidies_Total_sum"].fillna(0).values) > 0.01:
            error = "补助项目金额：项目1+项目2+项目3+项目4+项目5<>合计"
            errorlist.append(error)
        











        return df, errorlist



if __name__ == "__main__":
    d = GetGovernmentSubsidies()