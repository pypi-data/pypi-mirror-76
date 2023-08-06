
import pandas as pd
from ChosenAPI.DataImport.ChangeToNum import ChangeData



class GetGoodWill(object):#商誉
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
            "GoodWill_OriginalValue1_last": data.cell_value(3, 1),  # B4 4行2列单位1期初余额
            "GoodWill_OriginalValue2_last": data.cell_value(4, 1),  # B5 5行2列单位2期初余额
            "GoodWill_OriginalValue3_last": data.cell_value(5, 1),  # B6 6行2列单位3期初余额
            "GoodWill_OriginalValue4_last": data.cell_value(6, 1),  # B7 7行2列单位4期初余额
            "GoodWill_OriginalValue5_last": data.cell_value(7, 1),  # B8 8行2列单位5期初余额
            "GoodWill_TotalOriginalCost_last": data.cell_value(8, 1),  # B9 9行2列合计期初余额
            "GoodWill_OriginalValue1_merge": data.cell_value(3, 2),  # C4 4行3列单位1本期增加企业合并形成的
            "GoodWill_OriginalValue2_merge": data.cell_value(4, 2),  # C5 5行3列单位2本期增加企业合并形成的
            "GoodWill_OriginalValue3_merge": data.cell_value(5, 2),  # C6 6行3列单位3本期增加企业合并形成的
            "GoodWill_OriginalValue4_merge": data.cell_value(6, 2),  # C7 7行3列单位4本期增加企业合并形成的
            "GoodWill_OriginalValue5_merge": data.cell_value(7, 2),  # C8 8行3列单位5本期增加企业合并形成的
            "GoodWill_TotalOriginalCost_merge": data.cell_value(8, 2),  # C9 9行3列合计本期增加企业合并形成的
            "GoodWill_OriginalValue1_OtherIncrease": data.cell_value(3, 3),  # D4 4行4列单位1本期增加其他
            "GoodWill_OriginalValue2_OtherIncrease": data.cell_value(4, 3),  # D5 5行4列单位2本期增加其他
            "GoodWill_OriginalValue3_OtherIncrease": data.cell_value(5, 3),  # D6 6行4列单位3本期增加其他
            "GoodWill_OriginalValue4_OtherIncrease": data.cell_value(6, 3),  # D7 7行4列单位4本期增加其他
            "GoodWill_OriginalValue5_OtherIncrease": data.cell_value(7, 3),  # D8 8行4列单位5本期增加其他
            "GoodWill_TotalOriginalCost_OtherIncrease": data.cell_value(8, 3),  # D9 9行4列合计本期增加其他
            "GoodWill_OriginalValue1_disposal": data.cell_value(3, 4),  # E4 4行5列单位1本期减少处置
            "GoodWill_OriginalValue2_disposal": data.cell_value(4, 4),  # E5 5行5列单位2本期减少处置
            "GoodWill_OriginalValue3_disposal": data.cell_value(5, 4),  # E6 6行5列单位3本期减少处置
            "GoodWill_OriginalValue4_disposal": data.cell_value(6, 4),  # E7 7行5列单位4本期减少处置
            "GoodWill_OriginalValue5_disposal": data.cell_value(7, 4),  # E8 8行5列单位5本期减少处置
            "GoodWill_TotalOriginalCost_disposal": data.cell_value(8, 4),  # E9 9行5列合计本期减少处置
            "GoodWill_OriginalValue1_OtherLess": data.cell_value(3, 5),  # F4 4行6列单位1本期增加其他
            "GoodWill_OriginalValue2_OtherLess": data.cell_value(4, 5),  # F5 5行6列单位2本期增加其他
            "GoodWill_OriginalValue3_OtherLess": data.cell_value(5, 5),  # F6 6行6列单位3本期增加其他
            "GoodWill_OriginalValue4_OtherLess": data.cell_value(6, 5),  # F7 7行6列单位4本期增加其他
            "GoodWill_OriginalValue5_OtherLess": data.cell_value(7, 5),  # F8 8行6列单位5本期增加其他
            "GoodWill_TotalOriginalCost_OtherLess": data.cell_value(8, 5),  # F9 9行6列合计本期增加其他
            "GoodWill_OriginalValue1_this": data.cell_value(3, 6),  # G4 4行7列单位1期末余额
            "GoodWill_OriginalValue2_this": data.cell_value(4, 6),  # G5 5行7列单位2期末余额
            "GoodWill_OriginalValue3_this": data.cell_value(5, 6),  # G6 6行7列单位3期末余额
            "GoodWill_OriginalValue4_this": data.cell_value(6, 6),  # G7 7行7列单位4期末余额
            "GoodWill_OriginalValue5_this": data.cell_value(7, 6),  # G8 8行7列单位5期末余额
            "GoodWill_TotalOriginalCost_this": data.cell_value(8, 6),  # G9 9行7列合计期末余额
            "GoodWill_ImpairmentLoss1_last": data.cell_value(13, 1),  # B14 14行2列单位1期初余额
            "GoodWill_ImpairmentLoss2_last": data.cell_value(14, 1),  # B15 15行2列单位2期初余额
            "GoodWill_ImpairmentLoss3_last": data.cell_value(15, 1),  # B16 16行2列单位3期初余额
            "GoodWill_ImpairmentLoss4_last": data.cell_value(16, 1),  # B17 17行2列单位4期初余额
            "GoodWill_ImpairmentLoss5_last": data.cell_value(17, 1),  # B18 18行2列单位5期初余额
            "GoodWill_Total_last": data.cell_value(18, 1),  # B19 19行2列合计期初余额
            "GoodWill_ImpairmentLoss1_provision": data.cell_value(13, 2),  # C14 14行3列单位1本期增加本期增加
            "GoodWill_ImpairmentLoss2_provision": data.cell_value(14, 2),  # C15 15行3列单位2本期增加本期增加
            "GoodWill_ImpairmentLoss3_provision": data.cell_value(15, 2),  # C16 16行3列单位3本期增加本期增加
            "GoodWill_ImpairmentLoss4_provision": data.cell_value(16, 2),  # C17 17行3列单位4本期增加本期增加
            "GoodWill_ImpairmentLoss5_provision": data.cell_value(17, 2),  # C18 18行3列单位5本期增加本期增加
            "GoodWill_Total_provision": data.cell_value(18, 2),  # C19 19行3列合计本期增加本期增加
            "GoodWill_ImpairmentLoss1_OtherIncrease": data.cell_value(13, 3),  # D14 14行4列单位1本期增加其他
            "GoodWill_ImpairmentLoss2_OtherIncrease": data.cell_value(14, 3),  # D15 15行4列单位2本期增加其他
            "GoodWill_ImpairmentLoss3_OtherIncrease": data.cell_value(15, 3),  # D16 16行4列单位3本期增加其他
            "GoodWill_ImpairmentLoss4_OtherIncrease": data.cell_value(16, 3),  # D17 17行4列单位4本期增加其他
            "GoodWill_ImpairmentLoss5_OtherIncrease": data.cell_value(17, 3),  # D18 18行4列单位5本期增加其他
            "GoodWill_Total_OtherIncrease": data.cell_value(18, 3),  # D19 19行4列合计本期增加其他
            "GoodWill_ImpairmentLoss1_disposal": data.cell_value(13, 4),  # E14 14行5列单位1本期减少处置
            "GoodWill_ImpairmentLoss2_disposal": data.cell_value(14, 4),  # E15 15行5列单位2本期减少处置
            "GoodWill_ImpairmentLoss3_disposal": data.cell_value(15, 4),  # E16 16行5列单位3本期减少处置
            "GoodWill_ImpairmentLoss4_disposal": data.cell_value(16, 4),  # E17 17行5列单位4本期减少处置
            "GoodWill_ImpairmentLoss5_disposal": data.cell_value(17, 4),  # E18 18行5列单位5本期减少处置
            "GoodWill_Total_disposal": data.cell_value(18, 4),  # E19 19行5列合计本期减少处置
            "GoodWill_ImpairmentLoss1_OtherLess": data.cell_value(13, 5),  # F14 14行6列单位1本期增加其他
            "GoodWill_ImpairmentLoss2_OtherLess": data.cell_value(14, 5),  # F15 15行6列单位2本期增加其他
            "GoodWill_ImpairmentLoss3_OtherLess": data.cell_value(15, 5),  # F16 16行6列单位3本期增加其他
            "GoodWill_ImpairmentLoss4_OtherLess": data.cell_value(16, 5),  # F17 17行6列单位4本期增加其他
            "GoodWill_ImpairmentLoss5_OtherLess": data.cell_value(17, 5),  # F18 18行6列单位5本期增加其他
            "GoodWill_Total_OtherLess": data.cell_value(18, 5),  # F19 19行6列合计本期增加其他
            "GoodWill_ImpairmentLoss1_this": data.cell_value(13, 6),  # G14 14行7列单位1期末余额
            "GoodWill_ImpairmentLoss2_this": data.cell_value(14, 6),  # G15 15行7列单位2期末余额
            "GoodWill_ImpairmentLoss3_this": data.cell_value(15, 6),  # G16 16行7列单位3期末余额
            "GoodWill_ImpairmentLoss4_this": data.cell_value(16, 6),  # G17 17行7列单位4期末余额
            "GoodWill_ImpairmentLoss5_this": data.cell_value(17, 6),  # G18 18行7列单位5期末余额
            "GoodWill_Total_this": data.cell_value(18, 6),  # G19 19行7列合计期末余额


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
        dic["GoodWill_Remark"] = data.cell_value(20, 1),  # B21 21行2列说明
        dic["GoodWill_OriginalValue1_nature"] = data.cell_value(3, 7),  # H4 4行8列单位1单位性质
        dic["GoodWill_OriginalValue2_nature"] = data.cell_value(4, 7),  # H5 5行8列单位2单位性质
        dic["GoodWill_OriginalValue3_nature"] = data.cell_value(5, 7),  # H6 6行8列单位3单位性质
        dic["GoodWill_OriginalValue4_nature"] = data.cell_value(6, 7),  # H7 7行8列单位4单位性质
        dic["GoodWill_OriginalValue5_nature"] = data.cell_value(7, 7),  # H8 8行8列单位5单位性质
        dic["GoodWill_ImpairmentLoss1_nature"] = data.cell_value(13, 7),  # H14 14行8列单位1单位性质
        dic["GoodWill_ImpairmentLoss2_nature"] = data.cell_value(14, 7),  # H15 15行8列单位2单位性质
        dic["GoodWill_ImpairmentLoss3_nature"] = data.cell_value(15, 7),  # H16 16行8列单位3单位性质
        dic["GoodWill_ImpairmentLoss4_nature"] = data.cell_value(16, 7),  # H17 17行8列单位4单位性质
        dic["GoodWill_ImpairmentLoss5_nature"] = data.cell_value(17, 7),  # H18 18行8列单位5单位性质
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
        # 商誉账面原值期初余额:单位1+单位2+单位3+单位4+单位5=合计
        if abs(df["GoodWill_OriginalValue1_last"].fillna(0).values + df["GoodWill_OriginalValue2_last"].fillna(0).values + df["GoodWill_OriginalValue3_last"].fillna(0).values + df["GoodWill_OriginalValue4_last"].fillna(0).values + df["GoodWill_OriginalValue5_last"].fillna(0).values - df["GoodWill_TotalOriginalCost_last"].fillna(0).values) > 0.01:
            error = "商誉账面原值期初余额:单位1+单位2+单位3+单位4+单位5<>合计"
            errorlist.append(error)
        # 商誉账面原值本期增加企业合并形成的:单位1+单位2+单位3+单位4+单位5=合计
        if abs(df["GoodWill_OriginalValue1_merge"].fillna(0).values + df["GoodWill_OriginalValue2_merge"].fillna(0).values + df["GoodWill_OriginalValue3_merge"].fillna(0).values + df["GoodWill_OriginalValue4_merge"].fillna(0).values + df["GoodWill_OriginalValue5_merge"].fillna(0).values - df["GoodWill_TotalOriginalCost_merge"].fillna(0).values) > 0.01:
            error = "商誉账面原值本期增加企业合并形成的:单位1+单位2+单位3+单位4+单位5<>合计"
            errorlist.append(error)
        # 商誉账面原值本期增加其他:单位1+单位2+单位3+单位4+单位5=合计
        if abs(df["GoodWill_OriginalValue1_OtherIncrease"].fillna(0).values + df["GoodWill_OriginalValue2_OtherIncrease"].fillna(0).values + df["GoodWill_OriginalValue3_OtherIncrease"].fillna(0).values + df["GoodWill_OriginalValue4_OtherIncrease"].fillna(0).values + df["GoodWill_OriginalValue5_OtherIncrease"].fillna(0).values - df["GoodWill_TotalOriginalCost_OtherIncrease"].fillna(0).values) > 0.01:
            error = "商誉账面原值本期增加其他:单位1+单位2+单位3+单位4+单位5<>合计"
            errorlist.append(error)
        # 商誉账面原值本期减少处置:单位1+单位2+单位3+单位4+单位5=合计
        if abs(df["GoodWill_OriginalValue1_disposal"].fillna(0).values + df["GoodWill_OriginalValue2_disposal"].fillna(0).values + df["GoodWill_OriginalValue3_disposal"].fillna(0).values + df["GoodWill_OriginalValue4_disposal"].fillna(0).values + df["GoodWill_OriginalValue5_disposal"].fillna(0).values - df["GoodWill_TotalOriginalCost_disposal"].fillna(0).values) > 0.01:
            error = "商誉账面原值本期减少处置:单位1+单位2+单位3+单位4+单位5<>合计"
            errorlist.append(error)
        # 商誉账面原值本期减少其他:单位1+单位2+单位3+单位4+单位5=合计
        if abs(df["GoodWill_OriginalValue1_OtherLess"].fillna(0).values + df["GoodWill_OriginalValue2_OtherLess"].fillna(0).values + df["GoodWill_OriginalValue3_OtherLess"].fillna(0).values + df["GoodWill_OriginalValue4_OtherLess"].fillna(0).values + df["GoodWill_OriginalValue5_OtherLess"].fillna(0).values - df["GoodWill_TotalOriginalCost_OtherLess"].fillna(0).values) > 0.01:
            error = "商誉账面原值本期减少其他:单位1+单位2+单位3+单位4+单位5<>合计"
            errorlist.append(error)
        # 商誉账面原值期末余额:单位1+单位2+单位3+单位4+单位5=合计
        if abs(df["GoodWill_OriginalValue1_this"].fillna(0).values + df["GoodWill_OriginalValue2_this"].fillna(0).values + df["GoodWill_OriginalValue3_this"].fillna(0).values + df["GoodWill_OriginalValue4_this"].fillna(0).values + df["GoodWill_OriginalValue5_this"].fillna(0).values - df["GoodWill_TotalOriginalCost_this"].fillna(0).values) > 0.01:
            error = "商誉账面原值期末余额:单位1+单位2+单位3+单位4+单位5<>合计"
            errorlist.append(error)
        # 商誉减值准备期初余额:单位1+单位2+单位3+单位4+单位5=合计
        if abs(df["GoodWill_ImpairmentLoss1_last"].fillna(0).values + df["GoodWill_ImpairmentLoss2_last"].fillna(0).values + df["GoodWill_ImpairmentLoss3_last"].fillna(0).values + df["GoodWill_ImpairmentLoss4_last"].fillna(0).values + df["GoodWill_ImpairmentLoss5_last"].fillna(0).values - df["GoodWill_Total_last"].fillna(0).values) > 0.01:
            error = "商誉减值准备期初余额:单位1+单位2+单位3+单位4+单位5<>合计"
            errorlist.append(error)
        # 商誉减值准备本期增加企业合并形成的:单位1+单位2+单位3+单位4+单位5=合计
        if abs(df["GoodWill_ImpairmentLoss1_provision"].fillna(0).values + df["GoodWill_ImpairmentLoss2_provision"].fillna(0).values + df["GoodWill_ImpairmentLoss3_provision"].fillna(0).values + df["GoodWill_ImpairmentLoss4_provision"].fillna(0).values + df["GoodWill_ImpairmentLoss5_provision"].fillna(0).values - df["GoodWill_Total_provision"].fillna(0).values) > 0.01:
            error = "商誉减值准备本期增加企业合并形成的:单位1+单位2+单位3+单位4+单位5<>合计"
            errorlist.append(error)
        # 商誉减值准备本期增加其他:单位1+单位2+单位3+单位4+单位5=合计
        if abs(df["GoodWill_ImpairmentLoss1_OtherIncrease"].fillna(0).values + df["GoodWill_ImpairmentLoss2_OtherIncrease"].fillna(0).values + df["GoodWill_ImpairmentLoss3_OtherIncrease"].fillna(0).values + df["GoodWill_ImpairmentLoss4_OtherIncrease"].fillna(0).values + df["GoodWill_ImpairmentLoss5_OtherIncrease"].fillna(0).values - df["GoodWill_Total_OtherIncrease"].fillna(0).values) > 0.01:
            error = "商誉减值准备本期增加其他:单位1+单位2+单位3+单位4+单位5<>合计"
            errorlist.append(error)
        # 商誉减值准备本期减少处置:单位1+单位2+单位3+单位4+单位5=合计
        if abs(df["GoodWill_ImpairmentLoss1_disposal"].fillna(0).values + df["GoodWill_ImpairmentLoss2_disposal"].fillna(0).values + df["GoodWill_ImpairmentLoss3_disposal"].fillna(0).values + df["GoodWill_ImpairmentLoss4_disposal"].fillna(0).values + df["GoodWill_ImpairmentLoss5_disposal"].fillna(0).values - df["GoodWill_Total_disposal"].fillna(0).values) > 0.01:
            error = "商誉减值准备本期减少处置:单位1+单位2+单位3+单位4+单位5<>合计"
            errorlist.append(error)
        # 商誉减值准备本期减少其他:单位1+单位2+单位3+单位4+单位5=合计
        if abs(df["GoodWill_ImpairmentLoss1_OtherLess"].fillna(0).values + df["GoodWill_ImpairmentLoss2_OtherLess"].fillna(0).values + df["GoodWill_ImpairmentLoss3_OtherLess"].fillna(0).values + df["GoodWill_ImpairmentLoss4_OtherLess"].fillna(0).values + df["GoodWill_ImpairmentLoss5_OtherLess"].fillna(0).values - df["GoodWill_Total_OtherLess"].fillna(0).values) > 0.01:
            error = "商誉减值准备本期减少其他:单位1+单位2+单位3+单位4+单位5<>合计"
            errorlist.append(error)
        # 商誉减值准备期末余额:单位1+单位2+单位3+单位4+单位5=合计
        if abs(df["GoodWill_ImpairmentLoss1_this"].fillna(0).values + df["GoodWill_ImpairmentLoss2_this"].fillna(0).values + df["GoodWill_ImpairmentLoss3_this"].fillna(0).values + df["GoodWill_ImpairmentLoss4_this"].fillna(0).values + df["GoodWill_ImpairmentLoss5_this"].fillna(0).values - df["GoodWill_Total_this"].fillna(0).values) > 0.01:
            error = "商誉减值准备期末余额:单位1+单位2+单位3+单位4+单位5<>合计"
            errorlist.append(error)
        











        return df, errorlist


if __name__ == "__main__":
    d = GetGoodWill()