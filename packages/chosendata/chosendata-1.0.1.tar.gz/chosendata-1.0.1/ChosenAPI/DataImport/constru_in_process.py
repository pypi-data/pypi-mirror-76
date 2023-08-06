
import pandas as pd
from ChosenAPI.DataImport.ChangeToNum import ChangeData



class GetConstruInProcess(object):#在建工程
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
            "ConstruInProcess_ConstruInProcess_this": data.cell_value(3, 1),  # B4 4行2列在建工程期末余额
            "ConstruInProcess_CM_this": data.cell_value(4, 1),  # B5 5行2列工程物资
            "ConstruInProcess_Total_this": data.cell_value(5, 1),  # B6 6行2列合计
            "ConstruInProcess_ConstruInProcess_last": data.cell_value(3, 2),  # C4 4行3列在建工程期初余额
            "ConstruInProcess_CM_last": data.cell_value(4, 2),  # C5 5行3列工程物资
            "ConstruInProcess_Total_last": data.cell_value(5, 2),  # C6 6行3列合计
            "ConstruInProcess_CMP1_BB_this": data.cell_value(10, 1),# B11 11行2列项目1期末余额账面余额
            "ConstruInProcess_CMP2_BB_this": data.cell_value(11, 1),# B12 12行2列项目2期末余额账面余额
            "ConstruInProcess_CMP3_BB_this": data.cell_value(12, 1),# B13 13行2列项目3期末余额账面余额
            "ConstruInProcess_CMP4_BB_this": data.cell_value(13, 1),# B14 14行2列项目4期末余额账面余额
            "ConstruInProcess_CMP5_BB_this": data.cell_value(14, 1),# B15 15行2列项目5期末余额账面余额
            "ConstruInProcess_TotalCM_BB_this": data.cell_value(15, 1),# B16 16行2列合计期末余额账面余额
            "ConstruInProcess_CMP1_IL_this": data.cell_value(10, 2),# C11 11行3列项目1期末余额减值准备
            "ConstruInProcess_CMP2_IL_this": data.cell_value(11, 2),# C12 12行3列项目2期末余额减值准备
            "ConstruInProcess_CMP3_IL_this": data.cell_value(12, 2),# C13 13行3列项目3期末余额减值准备
            "ConstruInProcess_CMP4_IL_this": data.cell_value(13, 2),# C14 14行3列项目4期末余额减值准备
            "ConstruInProcess_CMP5_IL_this": data.cell_value(14, 2),# C15 15行3列项目5期末余额减值准备
            "ConstruInProcess_TotalCM_IL_this": data.cell_value(15, 2),# C16 16行3列合计期末余额减值准备
            "ConstruInProcess_CMP1_BV_this": data.cell_value(10, 3),# D11 11行4列项目1期末余额账面净值
            "ConstruInProcess_CMP2_BV_this": data.cell_value(11, 3),# D12 12行4列项目2期末余额账面净值
            "ConstruInProcess_CMP3_BV_this": data.cell_value(12, 3),# D13 13行4列项目3期末余额账面净值
            "ConstruInProcess_CMP4_BV_this": data.cell_value(13, 3),# D14 14行4列项目4期末余额账面净值
            "ConstruInProcess_CMP5_BV_this": data.cell_value(14, 3),# D15 15行4列项目5期末余额账面净值
            "ConstruInProcess_TotalCM_BV_this": data.cell_value(15, 3),# D16 16行4列合计期末余额账面净值
            "ConstruInProcess_CMP1_BB_last": data.cell_value(10, 4),# E11 11行5列项目1期初余额账面余额
            "ConstruInProcess_CMP2_BB_last": data.cell_value(11, 4),# E12 12行5列项目2期初余额账面余额
            "ConstruInProcess_CMP3_BB_last": data.cell_value(12, 4),# E13 13行5列项目3期初余额账面余额
            "ConstruInProcess_CMP4_BB_last": data.cell_value(13, 4),# E14 14行5列项目4期初余额账面余额
            "ConstruInProcess_CMP5_BB_last": data.cell_value(14, 4),# E15 15行5列项目5期初余额账面余额
            "ConstruInProcess_TotalCM_BB_last": data.cell_value(15, 4),# E16 16行5列合计期初余额账面余额
            "ConstruInProcess_CMP1_IL_last": data.cell_value(10, 5),# F11 11行6列项目1期初余额减值准备
            "ConstruInProcess_CMP2_IL_last": data.cell_value(11, 5),# F12 12行6列项目2期初余额减值准备
            "ConstruInProcess_CMP3_IL_last": data.cell_value(12, 5),# F13 13行6列项目3期初余额减值准备
            "ConstruInProcess_CMP4_IL_last": data.cell_value(13, 5),# F14 14行6列项目4期初余额减值准备
            "ConstruInProcess_CMP5_IL_last": data.cell_value(14, 5),# F15 15行6列项目5期初余额减值准备
            "ConstruInProcess_TotalCM_IL_last": data.cell_value(15, 5),# F16 16行6列合计期初余额减值准备
            "ConstruInProcess_CMP1_BV_last": data.cell_value(10, 6),# G11 11行7列项目1期初余额账面净值
            "ConstruInProcess_CMP2_BV_last": data.cell_value(11, 6),# G12 12行7列项目2期初余额账面净值
            "ConstruInProcess_CMP3_BV_last": data.cell_value(12, 6),# G13 13行7列项目3期初余额账面净值
            "ConstruInProcess_CMP4_BV_last": data.cell_value(13, 6),# G14 14行7列项目4期初余额账面净值
            "ConstruInProcess_CMP5_BV_last": data.cell_value(14, 6),# G15 15行7列项目5期初余额账面净值
            "ConstruInProcess_TotalCM_BV_last": data.cell_value(15, 6),# G16 16行7列合计期初余额账面净值
            "ConstruInProcess_ChangeProject1_BudgetNumber": data.cell_value(21, 1),  # B22 22行2列项目1预算数
            "ConstruInProcess_ChangeProject2_BudgetNumber": data.cell_value(22, 1),  # B23 23行2列项目2预算数
            "ConstruInProcess_ChangeProject3_BudgetNumber": data.cell_value(23, 1),  # B24 24行2列项目3预算数
            "ConstruInProcess_ChangeProject4_BudgetNumber": data.cell_value(24, 1),  # B25 25行2列项目4预算数
            "ConstruInProcess_ChangeProject5_BudgetNumber": data.cell_value(25, 1),  # B26 26行2列项目5预算数
            "ConstruInProcess_TotalChange_BudgetNumber": data.cell_value(26, 1),  # B27 27行2列合计预算数
            "ConstruInProcess_ChangeProject1_last": data.cell_value(21, 2),  # C22 22行3列项目1期初余额
            "ConstruInProcess_ChangeProject2_last": data.cell_value(22, 2),  # C23 23行3列项目2期初余额
            "ConstruInProcess_ChangeProject3_last": data.cell_value(23, 2),  # C24 24行3列项目3期初余额
            "ConstruInProcess_ChangeProject4_last": data.cell_value(24, 2),  # C25 25行3列项目4期初余额
            "ConstruInProcess_ChangeProject5_last": data.cell_value(25, 2),  # C26 26行3列项目5期初余额
            "ConstruInProcess_TotalChange_last": data.cell_value(26, 2),  # C27 27行3列合计期初余额
            "ConstruInProcess_ChangeProject1_add": data.cell_value(21, 3),  # D22 22行4列项目1本期增加
            "ConstruInProcess_ChangeProject2_add": data.cell_value(22, 3),  # D23 23行4列项目2本期增加
            "ConstruInProcess_ChangeProject3_add": data.cell_value(23, 3),  # D24 24行4列项目3本期增加
            "ConstruInProcess_ChangeProject4_add": data.cell_value(24, 3),  # D25 25行4列项目4本期增加
            "ConstruInProcess_ChangeProject5_add": data.cell_value(25, 3),  # D26 26行4列项目5本期增加
            "ConstruInProcess_TotalChange_add": data.cell_value(26, 3),  # D27 27行4列合计本期增加
            "ConstruInProcess_ChangeProject1_into": data.cell_value(21, 4),  # E22 22行5列项目1本期减少转入固定资产
            "ConstruInProcess_ChangeProject2_into": data.cell_value(22, 4),  # E23 23行5列项目2本期减少转入固定资产
            "ConstruInProcess_ChangeProject3_into": data.cell_value(23, 4),  # E24 24行5列项目3本期减少转入固定资产
            "ConstruInProcess_ChangeProject4_into": data.cell_value(24, 4),  # E25 25行5列项目4本期减少转入固定资产
            "ConstruInProcess_ChangeProject5_into": data.cell_value(25, 4),  # E26 26行5列项目5本期减少转入固定资产
            "ConstruInProcess_TotalChange_into": data.cell_value(26, 4),  # E27 27行5列合计本期减少转入固定资产
            "ConstruInProcess_ChangeProject1_reduce": data.cell_value(21, 5),  # F22 22行6列项目1本期减少其他减少
            "ConstruInProcess_ChangeProject2_reduce": data.cell_value(22, 5),  # F23 23行6列项目2本期减少其他减少
            "ConstruInProcess_ChangeProject3_reduce": data.cell_value(23, 5),  # F24 24行6列项目3本期减少其他减少
            "ConstruInProcess_ChangeProject4_reduce": data.cell_value(24, 5),  # F25 25行6列项目4本期减少其他减少
            "ConstruInProcess_ChangeProject5_reduce": data.cell_value(25, 5),  # F26 26行6列项目5本期减少其他减少
            "ConstruInProcess_TotalChange_reduce": data.cell_value(26, 5),  # F27 27行6列合计本期减少其他减少
            "ConstruInProcess_ChangeProject1_this": data.cell_value(21, 6),  # G22 22行7列项目1期末余额
            "ConstruInProcess_ChangeProject2_this": data.cell_value(22, 6),  # G23 23行7列项目2期末余额
            "ConstruInProcess_ChangeProject3_this": data.cell_value(23, 6),  # G24 24行7列项目3期末余额
            "ConstruInProcess_ChangeProject4_this": data.cell_value(24, 6),  # G25 25行7列项目4期末余额
            "ConstruInProcess_ChangeProject5_this": data.cell_value(25, 6),  # G26 26行7列项目5期末余额
            "ConstruInProcess_TotalChange_this": data.cell_value(26, 6),  # G27 27行7列合计期末余额
            "ConstruInProcess_ChangeProject1_ratio": data.cell_value(21, 7),  # H22 22行8列项目1工程累计投入占预算比例（%）
            "ConstruInProcess_ChangeProject2_ratio": data.cell_value(22, 7),  # H23 23行8列项目2工程累计投入占预算比例（%）
            "ConstruInProcess_ChangeProject3_ratio": data.cell_value(23, 7),  # H24 24行8列项目3工程累计投入占预算比例（%）
            "ConstruInProcess_ChangeProject4_ratio": data.cell_value(24, 7),  # H25 25行8列项目4工程累计投入占预算比例（%）
            "ConstruInProcess_ChangeProject5_ratio": data.cell_value(25, 7),  # H26 26行8列项目5工程累计投入占预算比例（%）
            "ConstruInProcess_TotalChange_ratio": data.cell_value(26, 7),  # H27 27行8列合计工程累计投入占预算比例（%）
            "ConstruInProcess_ChangeProject1_schedule": data.cell_value(30, 1),  # B31 31行2列项目1工程进度(%)
            "ConstruInProcess_ChangeProject2_schedule": data.cell_value(31, 1),  # B32 32行2列项目2工程进度(%)
            "ConstruInProcess_ChangeProject3_schedule": data.cell_value(32, 1),  # B33 33行2列项目3工程进度(%)
            "ConstruInProcess_ChangeProject4_schedule": data.cell_value(33, 1),  # B34 34行2列项目4工程进度(%)
            "ConstruInProcess_ChangeProject5_schedule": data.cell_value(34, 1),  # B35 35行2列项目5工程进度(%)
            "ConstruInProcess_TotalChange_schedule": data.cell_value(35, 1),  # B36 36行2列合计工程进度(%)
            "ConstruInProcess_ChangeProject1_AccruingAmounts": data.cell_value(30, 2),  # C31 31行3列项目1利息资本化累计金额
            "ConstruInProcess_ChangeProject2_AccruingAmounts": data.cell_value(31, 2),  # C32 32行3列项目2利息资本化累计金额
            "ConstruInProcess_ChangeProject3_AccruingAmounts": data.cell_value(32, 2),  # C33 33行3列项目3利息资本化累计金额
            "ConstruInProcess_ChangeProject4_AccruingAmounts": data.cell_value(33, 2),  # C34 34行3列项目4利息资本化累计金额
            "ConstruInProcess_ChangeProject5_AccruingAmounts": data.cell_value(34, 2),  # C35 35行3列项目5利息资本化累计金额
            "ConstruInProcess_TotalChange_AccruingAmounts": data.cell_value(35, 2),  # C36 36行3列合计利息资本化累计金额
            "ConstruInProcess_ChangeProject1_schedule_sum": data.cell_value(30, 3),  # D31 31行4列项目1其中：本期利息资本化金额
            "ConstruInProcess_ChangeProject2_schedule_sum": data.cell_value(31, 3),  # D32 32行4列项目2其中：本期利息资本化金额
            "ConstruInProcess_ChangeProject3_schedule_sum": data.cell_value(32, 3),  # D33 33行4列项目3其中：本期利息资本化金额
            "ConstruInProcess_ChangeProject4_schedule_sum": data.cell_value(33, 3),  # D34 34行4列项目4其中：本期利息资本化金额
            "ConstruInProcess_ChangeProject5_schedule_sum": data.cell_value(34, 3),  # D35 35行4列项目5其中：本期利息资本化金额
            "ConstruInProcess_TotalChange_schedule_sum": data.cell_value(35, 3),  # D36 36行4列合计其中：本期利息资本化金额
            "ConstruInProcess_ChangeProject1_Capitalizationrate": data.cell_value(30, 4),  # E31 31行5列项目1本期利息资本化率(%)
            "ConstruInProcess_ChangeProject2_Capitalizationrate": data.cell_value(31, 4),  # E32 32行5列项目2本期利息资本化率(%)
            "ConstruInProcess_ChangeProject3_Capitalizationrate": data.cell_value(32, 4),  # E33 33行5列项目3本期利息资本化率(%)
            "ConstruInProcess_ChangeProject4_Capitalizationrate": data.cell_value(33, 4),  # E34 34行5列项目4本期利息资本化率(%)
            "ConstruInProcess_ChangeProject5_Capitalizationrate": data.cell_value(34, 4),  # E35 35行5列项目5本期利息资本化率(%)
            "ConstruInProcess_TotalChange_Capitalizationrate": data.cell_value(35, 4),  # E36 36行5列合计本期利息资本化率(%)
            "ConstruInProcess_ILProject1_sum": data.cell_value(39, 1),  # B40 40行2列项目1本期计提金额
            "ConstruInProcess_ILProject2_sum": data.cell_value(40, 1),  # B41 41行2列项目2本期计提金额
            "ConstruInProcess_ILProject3_sum": data.cell_value(41, 1),  # B42 42行2列项目3本期计提金额
            "ConstruInProcess_ILProject4_sum": data.cell_value(42, 1),  # B43 43行2列项目4本期计提金额
            "ConstruInProcess_ILProject5_sum": data.cell_value(43, 1),  # B44 44行2列项目5本期计提金额
            "ConstruInProcess_TotalIL_sum": data.cell_value(44, 1),  # B45 45行2列合计本期计提金额
            "ConstruInProcess_CMP1_this": data.cell_value(48, 1),  # B49 49行2列项目1期末余额
            "ConstruInProcess_CMP2_this": data.cell_value(49, 1),  # B50 50行2列项目2期末余额
            "ConstruInProcess_CMP3_this": data.cell_value(50, 1),  # B51 51行2列项目3期末余额
            "ConstruInProcess_CMP4_this": data.cell_value(51, 1),  # B52 52行2列项目4期末余额
            "ConstruInProcess_CMP5_this": data.cell_value(52, 1),  # B53 53行2列项目5期末余额
            "ConstruInProcess_TotalCM_this": data.cell_value(53, 1),  # B54 54行2列合计期末余额
            "ConstruInProcess_CMP1_last": data.cell_value(48, 2),  # C49 49行3列项目1期初余额
            "ConstruInProcess_CMP2_last": data.cell_value(49, 2),  # C50 50行3列项目2期初余额
            "ConstruInProcess_CMP3_last": data.cell_value(50, 2),  # C51 51行3列项目3期初余额
            "ConstruInProcess_CMP4_last": data.cell_value(51, 2),  # C52 52行3列项目4期初余额
            "ConstruInProcess_CMP5_last": data.cell_value(52, 2),  # C53 53行3列项目5期初余额
            "ConstruInProcess_TotalCM_last": data.cell_value(53, 2),  # C54 54行3列合计期初余额

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
        dic["ConstruInProcess_Remark"] = data.cell_value(55, 1),  # B56 56行2列说明
        dic["ConstruInProcess_ChangeProject1_source"] = data.cell_value(30, 5),  # F31 31行6列项目1资金来源[注]
        dic["ConstruInProcess_ChangeProject2_source"] = data.cell_value(31, 5),  # F32 32行6列项目2资金来源[注]
        dic["ConstruInProcess_ChangeProject3_source"] = data.cell_value(32, 5),  # F33 33行6列项目3资金来源[注]
        dic["ConstruInProcess_ChangeProject4_source"] = data.cell_value(33, 5),  # F34 34行6列项目4资金来源[注]
        dic["ConstruInProcess_ChangeProject5_source"] = data.cell_value(34, 5),  # F35 35行6列项目5资金来源[注]
        dic["ConstruInProcess_ILProject1_reason"] = data.cell_value(39, 2),  # C40 40行3列项目1计提原因
        dic["ConstruInProcess_ILProject2_reason"] = data.cell_value(40, 2),  # C41 41行3列项目2计提原因
        dic["ConstruInProcess_ILProject3_reason"] = data.cell_value(41, 2),  # C42 42行3列项目3计提原因
        dic["ConstruInProcess_ILProject4_reason"] = data.cell_value(42, 2),  # C43 43行3列项目4计提原因
        dic["ConstruInProcess_ILProject5_reason"] = data.cell_value(43, 2),  # C44 44行3列项目5计提原因
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
        # 分类期末余额:在建工程+工程物资=合计
        if abs(df["ConstruInProcess_ConstruInProcess_this"].fillna(0).values + df["ConstruInProcess_CM_this"].fillna(0).values - df["ConstruInProcess_Total_this"].fillna(0).values) > 0.01:
            error = "分类期末余额:在建工程+工程物资<>合计"
            errorlist.append(error)
        # 分类期初余额:在建工程+工程物资=合计
        if abs(df["ConstruInProcess_ConstruInProcess_last"].fillna(0).values + df["ConstruInProcess_CM_last"].fillna(0).values - df["ConstruInProcess_Total_last"].fillna(0).values) > 0.01:
            error = "分类期初余额:在建工程+工程物资<>合计"
            errorlist.append(error)
        # 在建工程情况期末余额账面余额：项目1+项目2+项目3+项目4+项目5=合计
        if abs(df["ConstruInProcess_CMP1_BB_this"].fillna(0).values + df["ConstruInProcess_CMP2_BB_this"].fillna(0).values + df["ConstruInProcess_CMP3_BB_this"].fillna(0).values + df["ConstruInProcess_CMP4_BB_this"].fillna(0).values + df["ConstruInProcess_CMP5_BB_this"].fillna(0).values - df["ConstruInProcess_TotalCM_BB_this"].fillna(0).values) > 0.01:
            error = "在建工程情况期末余额账面余额：项目1+项目2+项目3+项目4+项目5<>合计"
            errorlist.append(error)
        # 在建工程情况期末余额减值准备：项目1+项目2+项目3+项目4+项目5=合计
        if abs(df["ConstruInProcess_CMP1_IL_this"].fillna(0).values + df["ConstruInProcess_CMP2_IL_this"].fillna(0).values + df["ConstruInProcess_CMP3_IL_this"].fillna(0).values + df["ConstruInProcess_CMP4_IL_this"].fillna(0).values + df["ConstruInProcess_CMP5_IL_this"].fillna(0).values - df["ConstruInProcess_TotalCM_IL_this"].fillna(0).values) > 0.01:
            error = "在建工程情况期末余额减值准备：项目1+项目2+项目3+项目4+项目5<>合计"
            errorlist.append(error)
        # 在建工程情况期末余额账面净值：项目1+项目2+项目3+项目4+项目5=合计
        if abs(df["ConstruInProcess_CMP1_BV_this"].fillna(0).values + df["ConstruInProcess_CMP2_BV_this"].fillna(0).values + df["ConstruInProcess_CMP3_BV_this"].fillna(0).values + df["ConstruInProcess_CMP4_BV_this"].fillna(0).values + df["ConstruInProcess_CMP5_BV_this"].fillna(0).values - df["ConstruInProcess_TotalCM_BV_this"].fillna(0).values) > 0.01:
            error = "在建工程情况期末余额账面净值：项目1+项目2+项目3+项目4+项目5<>合计"
            errorlist.append(error)
        # 在建工程情况期初余额账面余额：项目1+项目2+项目3+项目4+项目5=合计
        if abs(df["ConstruInProcess_CMP1_BB_last"].fillna(0).values + df["ConstruInProcess_CMP2_BB_last"].fillna(0).values + df["ConstruInProcess_CMP3_BB_last"].fillna(0).values + df["ConstruInProcess_CMP4_BB_last"].fillna(0).values + df["ConstruInProcess_CMP5_BB_last"].fillna(0).values - df["ConstruInProcess_TotalCM_BB_last"].fillna(0).values) > 0.01:
            error = "在建工程情况期初余额账面余额：项目1+项目2+项目3+项目4+项目5<>合计"
            errorlist.append(error)
        # 在建工程情况期初余额减值准备：项目1+项目2+项目3+项目4+项目5=合计
        if abs(df["ConstruInProcess_CMP1_IL_last"].fillna(0).values + df["ConstruInProcess_CMP2_IL_last"].fillna(0).values + df["ConstruInProcess_CMP3_IL_last"].fillna(0).values + df["ConstruInProcess_CMP4_IL_last"].fillna(0).values + df["ConstruInProcess_CMP5_IL_last"].fillna(0).values - df["ConstruInProcess_TotalCM_IL_last"].fillna(0).values) > 0.01:
            error = "在建工程情况期初余额减值准备：项目1+项目2+项目3+项目4+项目5<>合计"
            errorlist.append(error)
        # 在建工程情况期初余额账面净值：项目1+项目2+项目3+项目4+项目5=合计
        if abs(df["ConstruInProcess_CMP1_BV_last"].fillna(0).values + df["ConstruInProcess_CMP2_BV_last"].fillna(0).values + df["ConstruInProcess_CMP3_BV_last"].fillna(0).values + df["ConstruInProcess_CMP4_BV_last"].fillna(0).values + df["ConstruInProcess_CMP5_BV_last"].fillna(0).values - df["ConstruInProcess_TotalCM_BV_last"].fillna(0).values) > 0.01:
            error = "在建工程情况期初余额账面净值：项目1+项目2+项目3+项目4+项目5<>合计"
            errorlist.append(error)
        # 重要在建工程项目本期变动情况预算数：项目1+项目2+项目3+项目4+项目5=合计
        if abs(df["ConstruInProcess_ChangeProject1_BudgetNumber"].fillna(0).values + df["ConstruInProcess_ChangeProject2_BudgetNumber"].fillna(0).values + df["ConstruInProcess_ChangeProject3_BudgetNumber"].fillna(0).values + df["ConstruInProcess_ChangeProject4_BudgetNumber"].fillna(0).values + df["ConstruInProcess_ChangeProject5_BudgetNumber"].fillna(0).values - df["ConstruInProcess_TotalChange_BudgetNumber"].fillna(0).values) > 0.01:
            error = "重要在建工程项目本期变动情况预算数：项目1+项目2+项目3+项目4+项目5<>合计"
            errorlist.append(error)
        # 重要在建工程项目本期变动情况期初余额：项目1+项目2+项目3+项目4+项目5=合计
        if abs(df["ConstruInProcess_ChangeProject1_last"].fillna(0).values + df["ConstruInProcess_ChangeProject2_last"].fillna(0).values + df["ConstruInProcess_ChangeProject3_last"].fillna(0).values + df["ConstruInProcess_ChangeProject4_last"].fillna(0).values + df["ConstruInProcess_ChangeProject5_last"].fillna(0).values - df["ConstruInProcess_TotalChange_last"].fillna(0).values) > 0.01:
            error = "重要在建工程项目本期变动情况期初余额：项目1+项目2+项目3+项目4+项目5<>合计"
            errorlist.append(error)
        # 重要在建工程项目本期变动情况本期增加：项目1+项目2+项目3+项目4+项目5=合计
        if abs(df["ConstruInProcess_ChangeProject1_add"].fillna(0).values + df["ConstruInProcess_ChangeProject2_add"].fillna(0).values + df["ConstruInProcess_ChangeProject3_add"].fillna(0).values + df["ConstruInProcess_ChangeProject4_add"].fillna(0).values + df["ConstruInProcess_ChangeProject5_add"].fillna(0).values - df["ConstruInProcess_TotalChange_add"].fillna(0).values) > 0.01:
            error = "重要在建工程项目本期变动情况本期增加：项目1+项目2+项目3+项目4+项目5<>合计"
            errorlist.append(error)
        # 重要在建工程项目本期变动情况本期减少转入固定资产：项目1+项目2+项目3+项目4+项目5=合计
        if abs(df["ConstruInProcess_ChangeProject1_into"].fillna(0).values + df["ConstruInProcess_ChangeProject2_into"].fillna(0).values + df["ConstruInProcess_ChangeProject3_into"].fillna(0).values + df["ConstruInProcess_ChangeProject4_into"].fillna(0).values + df["ConstruInProcess_ChangeProject5_into"].fillna(0).values - df["ConstruInProcess_TotalChange_into"].fillna(0).values) > 0.01:
            error = "重要在建工程项目本期变动情况本期减少转入固定资产：项目1+项目2+项目3+项目4+项目5<>合计"
            errorlist.append(error)
        # 重要在建工程项目本期变动情况本期减少其他减少：项目1+项目2+项目3+项目4+项目5=合计
        if abs(df["ConstruInProcess_ChangeProject1_reduce"].fillna(0).values + df["ConstruInProcess_ChangeProject2_reduce"].fillna(0).values + df["ConstruInProcess_ChangeProject3_reduce"].fillna(0).values + df["ConstruInProcess_ChangeProject4_reduce"].fillna(0).values + df["ConstruInProcess_ChangeProject5_reduce"].fillna(0).values - df["ConstruInProcess_TotalChange_reduce"].fillna(0).values) > 0.01:
            error = "重要在建工程项目本期变动情况本期减少其他减少：项目1+项目2+项目3+项目4+项目5<>合计"
            errorlist.append(error)
        # 重要在建工程项目本期变动情况期末余额：项目1+项目2+项目3+项目4+项目5=合计
        if abs(df["ConstruInProcess_ChangeProject1_this"].fillna(0).values + df["ConstruInProcess_ChangeProject2_this"].fillna(0).values + df["ConstruInProcess_ChangeProject3_this"].fillna(0).values + df["ConstruInProcess_ChangeProject4_this"].fillna(0).values + df["ConstruInProcess_ChangeProject5_this"].fillna(0).values - df["ConstruInProcess_TotalChange_this"].fillna(0).values) > 0.01:
            error = "重要在建工程项目本期变动情况期末余额：项目1+项目2+项目3+项目4+项目5<>合计"
            errorlist.append(error)
        # 重要在建工程项目本期变动情况利息资本化累计金额：项目1+项目2+项目3+项目4+项目5=合计
        if abs(df["ConstruInProcess_ChangeProject1_AccruingAmounts"].fillna(0).values + df["ConstruInProcess_ChangeProject2_AccruingAmounts"].fillna(0).values + df["ConstruInProcess_ChangeProject3_AccruingAmounts"].fillna(0).values + df["ConstruInProcess_ChangeProject4_AccruingAmounts"].fillna(0).values + df["ConstruInProcess_ChangeProject5_AccruingAmounts"].fillna(0).values - df["ConstruInProcess_TotalChange_AccruingAmounts"].fillna(0).values) > 0.01:
            error = "重要在建工程项目本期变动情况利息资本化累计金额：项目1+项目2+项目3+项目4+项目5<>合计"
            errorlist.append(error)
        # 重要在建工程项目本期变动情况本期利息资本化累计金额：项目1+项目2+项目3+项目4+项目5=合计
        if abs(df["ConstruInProcess_ChangeProject1_AccruingAmounts"].fillna(0).values + df["ConstruInProcess_ChangeProject2_AccruingAmounts"].fillna(0).values + df["ConstruInProcess_ChangeProject3_AccruingAmounts"].fillna(0).values + df["ConstruInProcess_ChangeProject4_AccruingAmounts"].fillna(0).values + df["ConstruInProcess_ChangeProject5_AccruingAmounts"].fillna(0).values - df["ConstruInProcess_TotalChange_AccruingAmounts"].fillna(0).values) > 0.01:
            error = "重要在建工程项目本期变动情况本期利息资本化累计金额：项目1+项目2+项目3+项目4+项目5<>合计"
            errorlist.append(error)
        # 本期计提在建工程减值准备情况：项目1+项目2+项目3+项目4+项目5=合计
        if abs(df["ConstruInProcess_ILProject1_sum"].fillna(0).values + df["ConstruInProcess_ILProject2_sum"].fillna(0).values + df["ConstruInProcess_ILProject3_sum"].fillna(0).values + df["ConstruInProcess_ILProject4_sum"].fillna(0).values + df["ConstruInProcess_ILProject5_sum"].fillna(0).values - df["ConstruInProcess_TotalIL_sum"].fillna(0).values) > 0.01:
            error = "本期计提在建工程减值准备情况：项目1+项目2+项目3+项目4+项目5<>合计"
            errorlist.append(error)
        # 工程物资期末余额：项目1+项目2+项目3+项目4+项目5=合计
        if abs(df["ConstruInProcess_CMP1_this"].fillna(0).values + df["ConstruInProcess_CMP2_this"].fillna(0).values + df["ConstruInProcess_CMP3_this"].fillna(0).values + df["ConstruInProcess_CMP4_this"].fillna(0).values + df["ConstruInProcess_CMP5_this"].fillna(0).values - df["ConstruInProcess_TotalCM_this"].fillna(0).values) > 0.01:
            error = "工程物资期末余额：项目1+项目2+项目3+项目4+项目5<>合计"
            errorlist.append(error)
        # 工程物资期初余额：项目1+项目2+项目3+项目4+项目5=合计
        if abs(df["ConstruInProcess_CMP1_last"].fillna(0).values + df["ConstruInProcess_CMP2_last"].fillna(0).values + df["ConstruInProcess_CMP3_last"].fillna(0).values + df["ConstruInProcess_CMP4_last"].fillna(0).values + df["ConstruInProcess_CMP5_last"].fillna(0).values - df["ConstruInProcess_TotalCM_last"].fillna(0).values) > 0.01:
            error = "工程物资期初余额：项目1+项目2+项目3+项目4+项目5<>合计"
            errorlist.append(error)
        











        return df, errorlist


if __name__ == "__main__":
    d = GetConstruInProcess()