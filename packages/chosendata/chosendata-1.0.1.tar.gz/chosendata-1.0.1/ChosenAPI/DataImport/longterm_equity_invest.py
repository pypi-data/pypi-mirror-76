from xlrd import xldate_as_tuple
from datetime import datetime
import pandas as pd
from ChosenAPI.DataImport.ChangeToNum import ChangeData



class GetLongtermEquityInvest(object):#长期股权投资
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
            "LongtermEquityInvest_Joint1_last": data.cell_value(3, 1),  # B4 4行2列合营企业1期初余额
            "LongtermEquityInvest_Joint2_last": data.cell_value(4, 1),  # B5 5行2列合营企业2期初余额
            "LongtermEquityInvest_Joint3_last": data.cell_value(5, 1),  # B6 6行2列合营企业3期初余额
            "LongtermEquityInvest_Joint4_last": data.cell_value(6, 1),  # B7 7行2列合营企业4期初余额
            "LongtermEquityInvest_Joint5_last": data.cell_value(7, 1),  # B8 8行2列合营企业5期初余额
            "LongtermEquityInvest_SJoint_last": data.cell_value(8, 1),  # B9 9行2列小计期初余额
            "LongtermEquityInvest_Pool1_last": data.cell_value(10, 1),  # B11 11行2列联营企业1期初余额
            "LongtermEquityInvest_Pool2_last": data.cell_value(11, 1),  # B12 12行2列联营企业2期初余额
            "LongtermEquityInvest_Pool3_last": data.cell_value(12, 1),  # B13 13行2列联营企业3期初余额
            "LongtermEquityInvest_Pool4_last": data.cell_value(13, 1),  # B14 14行2列联营企业4期初余额
            "LongtermEquityInvest_Pool5_last": data.cell_value(14, 1),  # B15 15行2列联营企业5期初余额
            "LongtermEquityInvest_SPool_last": data.cell_value(15, 1),  # B16 16行2列小计期初余额
            "LongtermEquityInvest_Total_last": data.cell_value(16, 1),  # B17 17行2列合计期初余额
            "LongtermEquityInvest_Joint1_Add": data.cell_value(3, 2),  # C4 4行3列合营企业1追加投资
            "LongtermEquityInvest_Joint2_Add": data.cell_value(4, 2),  # C5 5行3列合营企业2追加投资
            "LongtermEquityInvest_Joint3_Add": data.cell_value(5, 2),  # C6 6行3列合营企业3追加投资
            "LongtermEquityInvest_Joint4_Add": data.cell_value(6, 2),  # C7 7行3列合营企业4追加投资
            "LongtermEquityInvest_Joint5_Add": data.cell_value(7, 2),  # C8 8行3列合营企业5追加投资
            "LongtermEquityInvest_SJoint_Add": data.cell_value(8, 2),  # C9 9行3列小计追加投资
            "LongtermEquityInvest_Pool1_Add": data.cell_value(10, 2),  # C11 11行3列联营企业1追加投资
            "LongtermEquityInvest_Pool2_Add": data.cell_value(11, 2),  # C12 12行3列联营企业2追加投资
            "LongtermEquityInvest_Pool3_Add": data.cell_value(12, 2),  # C13 13行3列联营企业3追加投资
            "LongtermEquityInvest_Pool4_Add": data.cell_value(13, 2),  # C14 14行3列联营企业4追加投资
            "LongtermEquityInvest_Pool5_Add": data.cell_value(14, 2),  # C15 15行3列联营企业5追加投资
            "LongtermEquityInvest_SPool_Add": data.cell_value(15, 2),  # C16 16行3列小计追加投资
            "LongtermEquityInvest_Total_Add": data.cell_value(16, 2),  # C17 17行3列合计追加投资
            "LongtermEquityInvest_Joint1_Reduce": data.cell_value(3, 3),  # D4 4行4列合营企业1减少投资
            "LongtermEquityInvest_Joint2_Reduce": data.cell_value(4, 3),  # D5 5行4列合营企业2减少投资
            "LongtermEquityInvest_Joint3_Reduce": data.cell_value(5, 3),  # D6 6行4列合营企业3减少投资
            "LongtermEquityInvest_Joint4_Reduce": data.cell_value(6, 3),  # D7 7行4列合营企业4减少投资
            "LongtermEquityInvest_Joint5_Reduce": data.cell_value(7, 3),  # D8 8行4列合营企业5减少投资
            "LongtermEquityInvest_SJoint_Reduce": data.cell_value(8, 3),  # D9 9行4列小计减少投资
            "LongtermEquityInvest_Pool1_Reduce": data.cell_value(10, 3),  # D11 11行4列联营企业1减少投资
            "LongtermEquityInvest_Pool2_Reduce": data.cell_value(11, 3),  # D12 12行4列联营企业2减少投资
            "LongtermEquityInvest_Pool3_Reduce": data.cell_value(12, 3),  # D13 13行4列联营企业3减少投资
            "LongtermEquityInvest_Pool4_Reduce": data.cell_value(13, 3),  # D14 14行4列联营企业4减少投资
            "LongtermEquityInvest_Pool5_Reduce": data.cell_value(14, 3),  # D15 15行4列联营企业5减少投资
            "LongtermEquityInvest_SPool_Reduce": data.cell_value(15, 3),  # D16 16行4列小计减少投资
            "LongtermEquityInvest_Total_Reduce": data.cell_value(16, 3),  # D17 17行4列合计减少投资
            "LongtermEquityInvest_Joint1_Affirm": data.cell_value(3, 4),  # E4 4行5列
            "LongtermEquityInvest_Joint2_Affirm": data.cell_value(4, 4),  # E5 5行5列
            "LongtermEquityInvest_Joint3_Affirm": data.cell_value(5, 4),  # E6 6行5列
            "LongtermEquityInvest_Joint4_Affirm": data.cell_value(6, 4),  # E7 7行5列
            "LongtermEquityInvest_Joint5_Affirm": data.cell_value(7, 4),  # E8 8行5列
            "LongtermEquityInvest_SJoint_Affirm": data.cell_value(8, 4),  # E9 9行5列
            "LongtermEquityInvest__Affirm": data.cell_value(9, 4),  # E10 10行5列
            "LongtermEquityInvest_Pool1_Affirm": data.cell_value(10, 4),  # E11 11行5列
            "LongtermEquityInvest_Pool2_Affirm": data.cell_value(11, 4),  # E12 12行5列
            "LongtermEquityInvest_Pool3_Affirm": data.cell_value(12, 4),  # E13 13行5列
            "LongtermEquityInvest_Pool4_Affirm": data.cell_value(13, 4),  # E14 14行5列
            "LongtermEquityInvest_Pool5_Affirm": data.cell_value(14, 4),  # E15 15行5列
            "LongtermEquityInvest_SPool_Affirm": data.cell_value(15, 4),  # E16 16行5列
            "LongtermEquityInvest_Total_Affirm": data.cell_value(16, 4),  # E17 17行5列
            "LongtermEquityInvest_Joint1_adjust": data.cell_value(3, 5),  # F4 4行6列合营企业1其他综合收益调整
            "LongtermEquityInvest_Joint2_adjust": data.cell_value(4, 5),  # F5 5行6列合营企业2其他综合收益调整
            "LongtermEquityInvest_Joint3_adjust": data.cell_value(5, 5),  # F6 6行6列合营企业3其他综合收益调整
            "LongtermEquityInvest_Joint4_adjust": data.cell_value(6, 5),  # F7 7行6列合营企业4其他综合收益调整
            "LongtermEquityInvest_Joint5_adjust": data.cell_value(7, 5),  # F8 8行6列合营企业5其他综合收益调整
            "LongtermEquityInvest_SJoint_adjust": data.cell_value(8, 5),  # F9 9行6列小计其他综合收益调整
            "LongtermEquityInvest_Pool1_adjust": data.cell_value(10, 5),  # F11 11行6列联营企业1其他综合收益调整
            "LongtermEquityInvest_Pool2_adjust": data.cell_value(11, 5),  # F12 12行6列联营企业2其他综合收益调整
            "LongtermEquityInvest_Pool3_adjust": data.cell_value(12, 5),  # F13 13行6列联营企业3其他综合收益调整
            "LongtermEquityInvest_Pool4_adjust": data.cell_value(13, 5),  # F14 14行6列联营企业4其他综合收益调整
            "LongtermEquityInvest_Pool5_adjust": data.cell_value(14, 5),  # F15 15行6列联营企业5其他综合收益调整
            "LongtermEquityInvest_SPool_adjust": data.cell_value(15, 5),  # F16 16行6列小计其他综合收益调整
            "LongtermEquityInvest_Total_adjust": data.cell_value(16, 5),  # F17 17行6列合计其他综合收益调整
            "LongtermEquityInvest_Joint1_Change": data.cell_value(3, 6),  # G4 4行7列合营企业1其他权益变动
            "LongtermEquityInvest_Joint2_Change": data.cell_value(4, 6),  # G5 5行7列合营企业2其他权益变动
            "LongtermEquityInvest_Joint3_Change": data.cell_value(5, 6),  # G6 6行7列合营企业3其他权益变动
            "LongtermEquityInvest_Joint4_Change": data.cell_value(6, 6),  # G7 7行7列合营企业4其他权益变动
            "LongtermEquityInvest_Joint5_Change": data.cell_value(7, 6),  # G8 8行7列合营企业5其他权益变动
            "LongtermEquityInvest_SJoint_Change": data.cell_value(8, 6),# G9 9行7列小计其他权益变动
            "LongtermEquityInvest_Pool1_Change": data.cell_value(10, 6),  # G11 11行7列联营企业1其他权益变动
            "LongtermEquityInvest_Pool2_Change": data.cell_value(11, 6),  # G12 12行7列联营企业2其他权益变动
            "LongtermEquityInvest_Pool3_Change": data.cell_value(12, 6),  # G13 13行7列联营企业3其他权益变动
            "LongtermEquityInvest_Pool4_Change": data.cell_value(13, 6),  # G14 14行7列联营企业4其他权益变动
            "LongtermEquityInvest_Pool5_Change": data.cell_value(14, 6),  # G15 15行7列联营企业5其他权益变动
            "LongtermEquityInvest_SPool_Change": data.cell_value(15, 6),# G16 16行7列小计其他权益变动
            "LongtermEquityInvest_Total_Change": data.cell_value(16, 6),  # G17 17行7列合计其他权益变动
            "LongtermEquityInvest_Joint1_issue": data.cell_value(3, 7),  # H4 4行8列合营企业1宣告发放现金股利或利润
            "LongtermEquityInvest_Joint2_issue": data.cell_value(4, 7),  # H5 5行8列合营企业2宣告发放现金股利或利润
            "LongtermEquityInvest_Joint3_issue": data.cell_value(5, 7),  # H6 6行8列合营企业3宣告发放现金股利或利润
            "LongtermEquityInvest_Joint4_issue": data.cell_value(6, 7),  # H7 7行8列合营企业4宣告发放现金股利或利润
            "LongtermEquityInvest_Joint5_issue": data.cell_value(7, 7),  # H8 8行8列合营企业5宣告发放现金股利或利润
            "LongtermEquityInvest_SJoint_issue": data.cell_value(8, 7),  # H9 9行8列小计宣告发放现金股利或利润
            "LongtermEquityInvest_Pool1_issue": data.cell_value(10, 7),  # H11 11行8列联营企业1宣告发放现金股利或利润
            "LongtermEquityInvest_Pool2_issue": data.cell_value(11, 7),  # H12 12行8列联营企业2宣告发放现金股利或利润
            "LongtermEquityInvest_Pool3_issue": data.cell_value(12, 7),  # H13 13行8列联营企业3宣告发放现金股利或利润
            "LongtermEquityInvest_Pool4_issue": data.cell_value(13, 7),  # H14 14行8列联营企业4宣告发放现金股利或利润
            "LongtermEquityInvest_Pool5_issue": data.cell_value(14, 7),  # H15 15行8列联营企业5宣告发放现金股利或利润
            "LongtermEquityInvest_SPool_issue": data.cell_value(15, 7),  # H16 16行8列小计宣告发放现金股利或利润
            "LongtermEquityInvest_Total_issue": data.cell_value(16, 7),  # H17 17行8列合计宣告发放现金股利或利润
            "LongtermEquityInvest_Joint1_Provision": data.cell_value(3, 8),  # I4 4行9列合营企业1计提减值准备
            "LongtermEquityInvest_Joint2_Provision": data.cell_value(4, 8),  # I5 5行9列合营企业2计提减值准备
            "LongtermEquityInvest_Joint3_Provision": data.cell_value(5, 8),  # I6 6行9列合营企业3计提减值准备
            "LongtermEquityInvest_Joint4_Provision": data.cell_value(6, 8),  # I7 7行9列合营企业4计提减值准备
            "LongtermEquityInvest_Joint5_Provision": data.cell_value(7, 8),  # I8 8行9列合营企业5计提减值准备
            "LongtermEquityInvest_SJoint_Provision": data.cell_value(8, 8),# I9 9行9列小计计提减值准备
            "LongtermEquityInvest_Pool1_Provision": data.cell_value(10, 8),  # I11 11行9列联营企业1计提减值准备
            "LongtermEquityInvest_Pool2_Provision": data.cell_value(11, 8),  # I12 12行9列联营企业2计提减值准备
            "LongtermEquityInvest_Pool3_Provision": data.cell_value(12, 8),  # I13 13行9列联营企业3计提减值准备
            "LongtermEquityInvest_Pool4_Provision": data.cell_value(13, 8),  # I14 14行9列联营企业4计提减值准备
            "LongtermEquityInvest_Pool5_Provision": data.cell_value(14, 8),  # I15 15行9列联营企业5计提减值准备
            "LongtermEquityInvest_SPool_Provision": data.cell_value(15, 8),# I16 16行9列小计计提减值准备
            "LongtermEquityInvest_Total_Provision": data.cell_value(16, 8),  # I17 17行9列合计计提减值准备
            "LongtermEquityInvest_Joint1_Other": data.cell_value(3, 9),  # J4 4行10列合营企业1其他
            "LongtermEquityInvest_Joint2_Other": data.cell_value(4, 9),  # J5 5行10列合营企业2其他
            "LongtermEquityInvest_Joint3_Other": data.cell_value(5, 9),  # J6 6行10列合营企业3其他
            "LongtermEquityInvest_Joint4_Other": data.cell_value(6, 9),  # J7 7行10列合营企业4其他
            "LongtermEquityInvest_Joint5_Other": data.cell_value(7, 9),  # J8 8行10列合营企业5其他
            "LongtermEquityInvest_SJoint_Other": data.cell_value(8, 9),  # J9 9行10列小计其他
            "LongtermEquityInvest_Pool1_Other": data.cell_value(10, 9),  # J11 11行10列联营企业1其他
            "LongtermEquityInvest_Pool2_Other": data.cell_value(11, 9),  # J12 12行10列联营企业2其他
            "LongtermEquityInvest_Pool3_Other": data.cell_value(12, 9),  # J13 13行10列联营企业3其他
            "LongtermEquityInvest_Pool4_Other": data.cell_value(13, 9),  # J14 14行10列联营企业4其他
            "LongtermEquityInvest_Pool5_Other": data.cell_value(14, 9),  # J15 15行10列联营企业5其他
            "LongtermEquityInvest_SPool_Other": data.cell_value(15, 9),  # J16 16行10列小计其他
            "LongtermEquityInvest_Total_Other": data.cell_value(16, 9),  # J17 17行10列合计其他
            "LongtermEquityInvest_Joint1_this": data.cell_value(3, 10),  # K4 4行11列合营企业1期末余额
            "LongtermEquityInvest_Joint2_this": data.cell_value(4, 10),  # K5 5行11列合营企业2期末余额
            "LongtermEquityInvest_Joint3_this": data.cell_value(5, 10),  # K6 6行11列合营企业3期末余额
            "LongtermEquityInvest_Joint4_this": data.cell_value(6, 10),  # K7 7行11列合营企业4期末余额
            "LongtermEquityInvest_Joint5_this": data.cell_value(7, 10),  # K8 8行11列合营企业5期末余额
            "LongtermEquityInvest_SJoint_this": data.cell_value(8, 10),  # K9 9行11列小计期末余额
            "LongtermEquityInvest_Pool1_this": data.cell_value(10, 10),  # K11 11行11列联营企业1期末余额
            "LongtermEquityInvest_Pool2_this": data.cell_value(11, 10),  # K12 12行11列联营企业2期末余额
            "LongtermEquityInvest_Pool3_this": data.cell_value(12, 10),  # K13 13行11列联营企业3期末余额
            "LongtermEquityInvest_Pool4_this": data.cell_value(13, 10),  # K14 14行11列联营企业4期末余额
            "LongtermEquityInvest_Pool5_this": data.cell_value(14, 10),  # K15 15行11列联营企业5期末余额
            "LongtermEquityInvest_SPool_this": data.cell_value(15, 10),  # K16 16行11列小计期末余额
            "LongtermEquityInvest_Total_this": data.cell_value(16, 10),  # K17 17行11列合计期末余额
            "LongtermEquityInvest_Joint1_Loss": data.cell_value(3, 11),  # L4 4行12列合营企业1减值准备期末余额
            "LongtermEquityInvest_Joint2_Loss": data.cell_value(4, 11),  # L5 5行12列合营企业2减值准备期末余额
            "LongtermEquityInvest_Joint3_Loss": data.cell_value(5, 11),  # L6 6行12列合营企业3减值准备期末余额
            "LongtermEquityInvest_Joint4_Loss": data.cell_value(6, 11),  # L7 7行12列合营企业4减值准备期末余额
            "LongtermEquityInvest_Joint5_Loss": data.cell_value(7, 11),  # L8 8行12列合营企业5减值准备期末余额
            "LongtermEquityInvest_SJoint_Loss": data.cell_value(8, 11),  # L9 9行12列小计减值准备期末余额
            "LongtermEquityInvest_Pool1_Loss": data.cell_value(10, 11),  # L11 11行12列联营企业1减值准备期末余额
            "LongtermEquityInvest_Pool2_Loss": data.cell_value(11, 11),  # L12 12行12列联营企业2减值准备期末余额
            "LongtermEquityInvest_Pool3_Loss": data.cell_value(12, 11),  # L13 13行12列联营企业3减值准备期末余额
            "LongtermEquityInvest_Pool4_Loss": data.cell_value(13, 11),  # L14 14行12列联营企业4减值准备期末余额
            "LongtermEquityInvest_Pool5_Loss": data.cell_value(14, 11),  # L15 15行12列联营企业5减值准备期末余额
            "LongtermEquityInvest_SPool_Loss": data.cell_value(15, 11),  # L16 16行12列小计减值准备期末余额
            "LongtermEquityInvest_Total_Loss": data.cell_value(16, 11),  # L17 17行12列合计减值准备期末余额


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
        dic["LongtermEquityInvest_Remark"] = data.cell_value(18, 1),  # B19 19行2列说明
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
        # 合营企业期初余额:合营企业1+合营企业2+合营企业3+合营企业4+合营企业5=合计
        if abs(df["LongtermEquityInvest_Joint1_last"].fillna(0).values + df["LongtermEquityInvest_Joint2_last"].fillna(0).values + df["LongtermEquityInvest_Joint3_last"].fillna(0).values + df["LongtermEquityInvest_Joint4_last"].fillna(0).values + df["LongtermEquityInvest_Joint5_last"].fillna(0).values - df["LongtermEquityInvest_SJoint_last"].fillna(0).values) > 0.01:
            error = "合营企业期初余额:合营企业1+合营企业2+合营企业3+合营企业4+合营企业5<>合计"
            errorlist.append(error)
    # 合营企业追加投资:合营企业1+合营企业2+合营企业3+合营企业4+合营企业5=合计
        if abs(df["LongtermEquityInvest_Joint1_Add"].fillna(0).values + df["LongtermEquityInvest_Joint2_Add"].fillna(0).values + df["LongtermEquityInvest_Joint3_Add"].fillna(0).values + df["LongtermEquityInvest_Joint4_Add"].fillna(0).values + df["LongtermEquityInvest_Joint5_Add"].fillna(0).values - df["LongtermEquityInvest_SJoint_Add"].fillna(0).values) > 0.01:
            error = "合营企业追加投资:合营企业1+合营企业2+合营企业3+合营企业4+合营企业5<>合计"
            errorlist.append(error)
    # 合营企业减少投资:合营企业1+合营企业2+合营企业3+合营企业4+合营企业5=合计
        if abs(df["LongtermEquityInvest_Joint1_Reduce"].fillna(0).values + df["LongtermEquityInvest_Joint2_Reduce"].fillna(0).values + df["LongtermEquityInvest_Joint3_Reduce"].fillna(0).values + df["LongtermEquityInvest_Joint4_Reduce"].fillna(0).values + df["LongtermEquityInvest_Joint5_Reduce"].fillna(0).values - df["LongtermEquityInvest_SJoint_Reduce"].fillna(0).values) > 0.01:
            error = "合营企业减少投资:合营企业1+合营企业2+合营企业3+合营企业4+合营企业5<>合计"
            errorlist.append(error)
    # 合营企业权益法下确认的投资损益:合营企业1+合营企业2+合营企业3+合营企业4+合营企业5=合计
        if abs(df["LongtermEquityInvest_Joint1_Affirm"].fillna(0).values + df["LongtermEquityInvest_Joint2_Affirm"].fillna(0).values + df["LongtermEquityInvest_Joint3_Affirm"].fillna(0).values + df["LongtermEquityInvest_Joint4_Affirm"].fillna(0).values + df["LongtermEquityInvest_Joint5_Affirm"].fillna(0).values - df["LongtermEquityInvest_SJoint_Affirm"].fillna(0).values) > 0.01:
            error = "合营企业权益法下确认的投资损益:合营企业1+合营企业2+合营企业3+合营企业4+合营企业5<>合计"
            errorlist.append(error)
    # 合营企业其他综合收益调整:合营企业1+合营企业2+合营企业3+合营企业4+合营企业5=合计
        if abs(df["LongtermEquityInvest_Joint1_adjust"].fillna(0).values + df["LongtermEquityInvest_Joint2_adjust"].fillna(0).values + df["LongtermEquityInvest_Joint3_adjust"].fillna(0).values + df["LongtermEquityInvest_Joint4_adjust"].fillna(0).values + df["LongtermEquityInvest_Joint5_adjust"].fillna(0).values - df["LongtermEquityInvest_SJoint_adjust"].fillna(0).values) > 0.01:
            error = "合营企业其他综合收益调整:合营企业1+合营企业2+合营企业3+合营企业4+合营企业5<>合计"
            errorlist.append(error)
    # 合营企业其他权益变动:合营企业1+合营企业2+合营企业3+合营企业4+合营企业5=合计
        if abs(df["LongtermEquityInvest_Joint1_Change"].fillna(0).values + df["LongtermEquityInvest_Joint2_Change"].fillna(0).values + df["LongtermEquityInvest_Joint3_Change"].fillna(0).values + df["LongtermEquityInvest_Joint4_Change"].fillna(0).values + df["LongtermEquityInvest_Joint5_Change"].fillna(0).values - df["LongtermEquityInvest_SJoint_Change"].fillna(0).values) > 0.01:
            error = "合营企业其他权益变动:合营企业1+合营企业2+合营企业3+合营企业4+合营企业5<>合计"
            errorlist.append(error)
    # 合营企业宣告发放现金股利或利润:合营企业1+合营企业2+合营企业3+合营企业4+合营企业5=合计
        if abs(df["LongtermEquityInvest_Joint1_issue"].fillna(0).values + df["LongtermEquityInvest_Joint2_issue"].fillna(0).values + df["LongtermEquityInvest_Joint3_issue"].fillna(0).values + df["LongtermEquityInvest_Joint4_issue"].fillna(0).values + df["LongtermEquityInvest_Joint5_issue"].fillna(0).values - df["LongtermEquityInvest_SJoint_issue"].fillna(0).values) > 0.01:
            error = "合营企业宣告发放现金股利或利润:合营企业1+合营企业2+合营企业3+合营企业4+合营企业5<>合计"
            errorlist.append(error)
    # 合营企业计提减值准备:合营企业1+合营企业2+合营企业3+合营企业4+合营企业5=合计
        if abs(df["LongtermEquityInvest_Joint1_Provision"].fillna(0).values + df["LongtermEquityInvest_Joint2_Provision"].fillna(0).values + df["LongtermEquityInvest_Joint3_Provision"].fillna(0).values + df["LongtermEquityInvest_Joint4_Provision"].fillna(0).values + df["LongtermEquityInvest_Joint5_Provision"].fillna(0).values - df["LongtermEquityInvest_SJoint_Provision"].fillna(0).values) > 0.01:
            error = "合营企业计提减值准备:合营企业1+合营企业2+合营企业3+合营企业4+合营企业5<>合计"
            errorlist.append(error)
    # 合营企业其他:合营企业1+合营企业2+合营企业3+合营企业4+合营企业5=合计
        if abs(df["LongtermEquityInvest_Joint1_Other"].fillna(0).values + df["LongtermEquityInvest_Joint2_Other"].fillna(0).values + df["LongtermEquityInvest_Joint3_Other"].fillna(0).values + df["LongtermEquityInvest_Joint4_Other"].fillna(0).values + df["LongtermEquityInvest_Joint5_Other"].fillna(0).values - df["LongtermEquityInvest_SJoint_Other"].fillna(0).values) > 0.01:
            error = "合营企业其他:合营企业1+合营企业2+合营企业3+合营企业4+合营企业5<>合计"
            errorlist.append(error)
    # 合营企业期末余额:合营企业1+合营企业2+合营企业3+合营企业4+合营企业5=合计
        if abs(df["LongtermEquityInvest_Joint1_this"].fillna(0).values + df["LongtermEquityInvest_Joint2_this"].fillna(0).values + df["LongtermEquityInvest_Joint3_this"].fillna(0).values + df["LongtermEquityInvest_Joint4_this"].fillna(0).values + df["LongtermEquityInvest_Joint5_this"].fillna(0).values - df["LongtermEquityInvest_SJoint_this"].fillna(0).values) > 0.01:
            error = "合营企业期末余额:合营企业1+合营企业2+合营企业3+合营企业4+合营企业5<>合计"
            errorlist.append(error)
    # 合营企业减值准备期末余额:合营企业1+合营企业2+合营企业3+合营企业4+合营企业5=合计
        if abs(df["LongtermEquityInvest_Joint1_Loss"].fillna(0).values + df["LongtermEquityInvest_Joint2_Loss"].fillna(0).values + df["LongtermEquityInvest_Joint3_Loss"].fillna(0).values + df["LongtermEquityInvest_Joint4_Loss"].fillna(0).values + df["LongtermEquityInvest_Joint5_Loss"].fillna(0).values - df["LongtermEquityInvest_SJoint_Loss"].fillna(0).values) > 0.01:
            error = "合营企业减值准备期末余额:合营企业1+合营企业2+合营企业3+合营企业4+合营企业5<>合计"
            errorlist.append(error)
    # 联营企业期初余额:联营企业1+联营企业2+联营企业3+联营企业4+联营企业5=合计
        if abs(df["LongtermEquityInvest_Pool1_last"].fillna(0).values + df["LongtermEquityInvest_Pool2_last"].fillna(0).values + df["LongtermEquityInvest_Pool3_last"].fillna(0).values + df["LongtermEquityInvest_Pool4_last"].fillna(0).values + df["LongtermEquityInvest_Pool5_last"].fillna(0).values - df["LongtermEquityInvest_SPool_last"].fillna(0).values) > 0.01:
            error = "联营企业期初余额:联营企业1+联营企业2+联营企业3+联营企业4+联营企业5<>合计"
            errorlist.append(error)
    # 联营企业追加投资:联营企业1+联营企业2+联营企业3+联营企业4+联营企业5=合计
        if abs(df["LongtermEquityInvest_Pool1_Add"].fillna(0).values + df["LongtermEquityInvest_Pool2_Add"].fillna(0).values + df["LongtermEquityInvest_Pool3_Add"].fillna(0).values + df["LongtermEquityInvest_Pool4_Add"].fillna(0).values + df["LongtermEquityInvest_Pool5_Add"].fillna(0).values - df["LongtermEquityInvest_SPool_Add"].fillna(0).values) > 0.01:
            error = "联营企业追加投资:联营企业1+联营企业2+联营企业3+联营企业4+联营企业5<>合计"
            errorlist.append(error)
    # 联营企业减少投资:联营企业1+联营企业2+联营企业3+联营企业4+联营企业5=合计
        if abs(df["LongtermEquityInvest_Pool1_Reduce"].fillna(0).values + df["LongtermEquityInvest_Pool2_Reduce"].fillna(0).values + df["LongtermEquityInvest_Pool3_Reduce"].fillna(0).values + df["LongtermEquityInvest_Pool4_Reduce"].fillna(0).values + df["LongtermEquityInvest_Pool5_Reduce"].fillna(0).values - df["LongtermEquityInvest_SPool_Reduce"].fillna(0).values) > 0.01:
            error = "联营企业减少投资:联营企业1+联营企业2+联营企业3+联营企业4+联营企业5<>合计"
            errorlist.append(error)
    # 联营企业权益法下确认的投资损益:联营企业1+联营企业2+联营企业3+联营企业4+联营企业5=合计
        if abs(df["LongtermEquityInvest_Pool1_Affirm"].fillna(0).values + df["LongtermEquityInvest_Pool2_Affirm"].fillna(0).values + df["LongtermEquityInvest_Pool3_Affirm"].fillna(0).values + df["LongtermEquityInvest_Pool4_Affirm"].fillna(0).values + df["LongtermEquityInvest_Pool5_Affirm"].fillna(0).values - df["LongtermEquityInvest_SPool_Affirm"].fillna(0).values) > 0.01:
            error = "联营企业权益法下确认的投资损益:联营企业1+联营企业2+联营企业3+联营企业4+联营企业5<>合计"
            errorlist.append(error)
    # 联营企业其他综合收益调整:联营企业1+联营企业2+联营企业3+联营企业4+联营企业5=合计
        if abs(df["LongtermEquityInvest_Pool1_adjust"].fillna(0).values + df["LongtermEquityInvest_Pool2_adjust"].fillna(0).values + df["LongtermEquityInvest_Pool3_adjust"].fillna(0).values + df["LongtermEquityInvest_Pool4_adjust"].fillna(0).values + df["LongtermEquityInvest_Pool5_adjust"].fillna(0).values - df["LongtermEquityInvest_SPool_adjust"].fillna(0).values) > 0.01:
            error = "联营企业其他综合收益调整:联营企业1+联营企业2+联营企业3+联营企业4+联营企业5<>合计"
            errorlist.append(error)
    # 联营企业其他权益变动:联营企业1+联营企业2+联营企业3+联营企业4+联营企业5=合计
        if abs(df["LongtermEquityInvest_Pool1_Change"].fillna(0).values + df["LongtermEquityInvest_Pool2_Change"].fillna(0).values + df["LongtermEquityInvest_Pool3_Change"].fillna(0).values + df["LongtermEquityInvest_Pool4_Change"].fillna(0).values + df["LongtermEquityInvest_Pool5_Change"].fillna(0).values - df["LongtermEquityInvest_SPool_Change"].fillna(0).values) > 0.01:
            error = "联营企业其他权益变动:联营企业1+联营企业2+联营企业3+联营企业4+联营企业5<>合计"
            errorlist.append(error)
    # 联营企业宣告发放现金股利或利润:联营企业1+联营企业2+联营企业3+联营企业4+联营企业5=合计
        if abs(df["LongtermEquityInvest_Pool1_issue"].fillna(0).values + df["LongtermEquityInvest_Pool2_issue"].fillna(0).values + df["LongtermEquityInvest_Pool3_issue"].fillna(0).values + df["LongtermEquityInvest_Pool4_issue"].fillna(0).values + df["LongtermEquityInvest_Pool5_issue"].fillna(0).values - df["LongtermEquityInvest_SPool_issue"].fillna(0).values) > 0.01:
            error = "联营企业宣告发放现金股利或利润:联营企业1+联营企业2+联营企业3+联营企业4+联营企业5<>合计"
            errorlist.append(error)
    # 联营企业计提减值准备:联营企业1+联营企业2+联营企业3+联营企业4+联营企业5=合计
        if abs(df["LongtermEquityInvest_Pool1_Provision"].fillna(0).values + df["LongtermEquityInvest_Pool2_Provision"].fillna(0).values + df["LongtermEquityInvest_Pool3_Provision"].fillna(0).values + df["LongtermEquityInvest_Pool4_Provision"].fillna(0).values + df["LongtermEquityInvest_Pool5_Provision"].fillna(0).values - df["LongtermEquityInvest_SPool_Provision"].fillna(0).values) > 0.01:
            error = "联营企业计提减值准备:联营企业1+联营企业2+联营企业3+联营企业4+联营企业5<>合计"
            errorlist.append(error)
    # 联营企业其他:联营企业1+联营企业2+联营企业3+联营企业4+联营企业5=合计
        if abs(df["LongtermEquityInvest_Pool1_Other"].fillna(0).values + df["LongtermEquityInvest_Pool2_Other"].fillna(0).values + df["LongtermEquityInvest_Pool3_Other"].fillna(0).values + df["LongtermEquityInvest_Pool4_Other"].fillna(0).values + df["LongtermEquityInvest_Pool5_Other"].fillna(0).values - df["LongtermEquityInvest_SPool_Other"].fillna(0).values) > 0.01:
            error = "联营企业其他:联营企业1+联营企业2+联营企业3+联营企业4+联营企业5<>合计"
            errorlist.append(error)
    # 联营企业期末余额:联营企业1+联营企业2+联营企业3+联营企业4+联营企业5=合计
        if abs(df["LongtermEquityInvest_Pool1_this"].fillna(0).values + df["LongtermEquityInvest_Pool2_this"].fillna(0).values + df["LongtermEquityInvest_Pool3_this"].fillna(0).values + df["LongtermEquityInvest_Pool4_this"].fillna(0).values + df["LongtermEquityInvest_Pool5_this"].fillna(0).values - df["LongtermEquityInvest_SPool_this"].fillna(0).values) > 0.01:
            error = "联营企业期末余额:联营企业1+联营企业2+联营企业3+联营企业4+联营企业5<>合计"
            errorlist.append(error)
    # 联营企业减值准备期末余额:联营企业1+联营企业2+联营企业3+联营企业4+联营企业5=合计
        if abs(df["LongtermEquityInvest_Pool1_Loss"].fillna(0).values + df["LongtermEquityInvest_Pool2_Loss"].fillna(0).values + df["LongtermEquityInvest_Pool3_Loss"].fillna(0).values + df["LongtermEquityInvest_Pool4_Loss"].fillna(0).values + df["LongtermEquityInvest_Pool5_Loss"].fillna(0).values - df["LongtermEquityInvest_SPool_Loss"].fillna(0).values) > 0.01:
            error = "联营企业减值准备期末余额:联营企业1+联营企业2+联营企业3+联营企业4+联营企业5<>合计"
            errorlist.append(error)
	
        











        return df, errorlist


if __name__ == "__main__":
    d = GetLongtermEquityInvest()