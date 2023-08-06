
import pandas as pd
from ChosenAPI.DataImport.ChangeToNum import ChangeData



class GetOtherCurrentLiabilities(object):#其他流动负债
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
            "OtherCurrentLiabilities_ShortTermBondsPayable_this": data.cell_value(3, 1),  # B4 4行2列短期应付债券期末余额
            "OtherCurrentLiabilities_Project1_this": data.cell_value(4, 1),  # B5 5行2列项目1期末余额
            "OtherCurrentLiabilities_Project2_this": data.cell_value(5, 1),  # B6 6行2列项目2期末余额
            "OtherCurrentLiabilities_Project3_this": data.cell_value(6, 1),  # B7 7行2列项目3期末余额
            "OtherCurrentLiabilities_Project4_this": data.cell_value(7, 1),  # B8 8行2列项目4期末余额
            "OtherCurrentLiabilities_Total_this": data.cell_value(8, 1),  # B9 9行2列合计期末余额
            "OtherCurrentLiabilities_ShortTermBondsPayable_last": data.cell_value(3, 2),  # C4 4行3列短期应付债券期初余额
            "OtherCurrentLiabilities_Project1_last": data.cell_value(4, 2),  # C5 5行3列项目1期初余额
            "OtherCurrentLiabilities_Project2_last": data.cell_value(5, 2),  # C6 6行3列项目2期初余额
            "OtherCurrentLiabilities_Project3_last": data.cell_value(6, 2),  # C7 7行3列项目3期初余额
            "OtherCurrentLiabilities_Project4_last": data.cell_value(7, 2),  # C8 8行3列项目4期初余额
            "OtherCurrentLiabilities_Total_last": data.cell_value(8, 2),  # C9 9行3列合计期初余额
            "OtherCurrentLiabilities_Bond1_FaceValue": data.cell_value(13, 1),  # B14 14行2列债券1面值
            "OtherCurrentLiabilities_Bond2_FaceValue": data.cell_value(14, 1),  # B15 15行2列债券2面值
            "OtherCurrentLiabilities_Bond3_FaceValue": data.cell_value(15, 1),  # B16 16行2列债券3面值
            "OtherCurrentLiabilities_Bond4_FaceValue": data.cell_value(16, 1),  # B17 17行2列债券4面值
            "OtherCurrentLiabilities_Bond5_FaceValue": data.cell_value(17, 1),  # B18 18行2列债券5面值
            "OtherCurrentLiabilities_Bond1_sum": data.cell_value(13, 4),  # E14 14行5列债券1发行金额
            "OtherCurrentLiabilities_Bond2_sum": data.cell_value(14, 4),  # E15 15行5列债券2发行金额
            "OtherCurrentLiabilities_Bond3_sum": data.cell_value(15, 4),  # E16 16行5列债券3发行金额
            "OtherCurrentLiabilities_Bond4_sum": data.cell_value(16, 4),  # E17 17行5列债券4发行金额
            "OtherCurrentLiabilities_Bond5_sum": data.cell_value(17, 4),  # E18 18行5列债券5发行金额
            "OtherCurrentLiabilities_Total_sum": data.cell_value(18, 4),  # E19 19行5列合计发行金额
            "OtherCurrentLiabilities_Bond1_last": data.cell_value(13, 5),  # F14 14行6列债券1期初余额
            "OtherCurrentLiabilities_Bond2_last": data.cell_value(14, 5),  # F15 15行6列债券2期初余额
            "OtherCurrentLiabilities_Bond3_last": data.cell_value(15, 5),  # F16 16行6列债券3期初余额
            "OtherCurrentLiabilities_Bond4_last": data.cell_value(16, 5),  # F17 17行6列债券4期初余额
            "OtherCurrentLiabilities_Bond5_last": data.cell_value(17, 5),  # F18 18行6列债券5期初余额
            "OtherCurrentLiabilities_TotalChange_last": data.cell_value(18, 5),  # F19 19行6列合计期初余额
            "OtherCurrentLiabilities_Bond1_add": data.cell_value(13, 6),  # G14 14行7列债券1本期发行
            "OtherCurrentLiabilities_Bond2_add": data.cell_value(14, 6),  # G15 15行7列债券2本期发行
            "OtherCurrentLiabilities_Bond3_add": data.cell_value(15, 6),  # G16 16行7列债券3本期发行
            "OtherCurrentLiabilities_Bond4_add": data.cell_value(16, 6),  # G17 17行7列债券4本期发行
            "OtherCurrentLiabilities_Bond5_add": data.cell_value(17, 6),  # G18 18行7列债券5本期发行
            "OtherCurrentLiabilities_Total_add": data.cell_value(18, 6),  # G19 19行7列合计本期发行
            "OtherCurrentLiabilities_Bond1_interest": data.cell_value(13, 7),  # H14 14行8列债券1按面值计提利息
            "OtherCurrentLiabilities_Bond2_interest": data.cell_value(14, 7),  # H15 15行8列债券2按面值计提利息
            "OtherCurrentLiabilities_Bond3_interest": data.cell_value(15, 7),  # H16 16行8列债券3按面值计提利息
            "OtherCurrentLiabilities_Bond4_interest": data.cell_value(16, 7),  # H17 17行8列债券4按面值计提利息
            "OtherCurrentLiabilities_Bond5_interest": data.cell_value(17, 7),  # H18 18行8列债券5按面值计提利息
            "OtherCurrentLiabilities_Total_interest": data.cell_value(18, 7),  # H19 19行8列合计按面值计提利息
            "OtherCurrentLiabilities_Bond1_amortization": data.cell_value(13, 8),  # I14 14行9列债券1溢折价摊销
            "OtherCurrentLiabilities_Bond2_amortization": data.cell_value(14, 8),  # I15 15行9列债券2溢折价摊销
            "OtherCurrentLiabilities_Bond3_amortization": data.cell_value(15, 8),  # I16 16行9列债券3溢折价摊销
            "OtherCurrentLiabilities_Bond4_amortization": data.cell_value(16, 8),  # I17 17行9列债券4溢折价摊销
            "OtherCurrentLiabilities_Bond5_amortization": data.cell_value(17, 8),  # I18 18行9列债券5溢折价摊销
            "OtherCurrentLiabilities_Total_amortization": data.cell_value(18, 8),  # I19 19行9列合计溢折价摊销
            "OtherCurrentLiabilities_Bond1_repay": data.cell_value(13, 9),  # J14 14行10列债券1本期偿还
            "OtherCurrentLiabilities_Bond2_repay": data.cell_value(14, 9),  # J15 15行10列债券2本期偿还
            "OtherCurrentLiabilities_Bond3_repay": data.cell_value(15, 9),  # J16 16行10列债券3本期偿还
            "OtherCurrentLiabilities_Bond4_repay": data.cell_value(16, 9),  # J17 17行10列债券4本期偿还
            "OtherCurrentLiabilities_Bond5_repay": data.cell_value(17, 9),  # J18 18行10列债券5本期偿还
            "OtherCurrentLiabilities_Total_repay": data.cell_value(18, 9),  # J19 19行10列合计本期偿还
            "OtherCurrentLiabilities_Bond1_this": data.cell_value(13, 10),  # K14 14行11列债券1期末余额
            "OtherCurrentLiabilities_Bond2_this": data.cell_value(14, 10),  # K15 15行11列债券2期末余额
            "OtherCurrentLiabilities_Bond3_this": data.cell_value(15, 10),  # K16 16行11列债券3期末余额
            "OtherCurrentLiabilities_Bond4_this": data.cell_value(16, 10),  # K17 17行11列债券4期末余额
            "OtherCurrentLiabilities_Bond5_this": data.cell_value(17, 10),  # K18 18行11列债券5期末余额
            "OtherCurrentLiabilities_TotalChange_this": data.cell_value(18, 10),  # K19 19行11列合计期末余额


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
        dic["OtherCurrentLiabilities_Remark"] = data.cell_value(20, 1),  # B21 21行2列说明
        dic["OtherCurrentLiabilities_Bond1_date"] = data.cell_value(13, 2),  # C14 14行3列债券1发行日期
        dic["OtherCurrentLiabilities_Bond2_date"] = data.cell_value(14, 2),  # C15 15行3列债券2发行日期
        dic["OtherCurrentLiabilities_Bond3_date"] = data.cell_value(15, 2),  # C16 16行3列债券3发行日期
        dic["OtherCurrentLiabilities_Bond4_date"] = data.cell_value(16, 2),  # C17 17行3列债券4发行日期
        dic["OtherCurrentLiabilities_Bond5_date"] = data.cell_value(17, 2),  # C18 18行3列债券5发行日期
        dic["OtherCurrentLiabilities_Bond1_TimeLimit"] = data.cell_value(13, 3),  # D14 14行4列债券1债券期限
        dic["OtherCurrentLiabilities_Bond2_TimeLimit"] = data.cell_value(14, 3),  # D15 15行4列债券2债券期限
        dic["OtherCurrentLiabilities_Bond3_TimeLimit"] = data.cell_value(15, 3),  # D16 16行4列债券3债券期限
        dic["OtherCurrentLiabilities_Bond4_TimeLimit"] = data.cell_value(16, 3),  # D17 17行4列债券4债券期限
        dic["OtherCurrentLiabilities_Bond5_TimeLimit"] = data.cell_value(17, 3),  # D18 18行4列债券5债券期限
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
        # 期末余额:短期应付债券+项目1+项目2+项目3+项目4=合计
        if abs(df["OtherCurrentLiabilities_ShortTermBondsPayable_this"].fillna(0).values + df["OtherCurrentLiabilities_Project1_this"].fillna(0).values + df["OtherCurrentLiabilities_Project2_this"].fillna(0).values + df["OtherCurrentLiabilities_Project3_this"].fillna(0).values + df["OtherCurrentLiabilities_Project4_this"].fillna(0).values - df["OtherCurrentLiabilities_Total_this"].fillna(0).values) > 0.01:
            error = "期末余额:短期应付债券+项目1+项目2+项目3+项目4<>合计"
            errorlist.append(error)
	    # 期初余额:短期应付债券+项目1+项目2+项目3+项目4=合计
        if abs(df["OtherCurrentLiabilities_ShortTermBondsPayable_last"].fillna(0).values + df["OtherCurrentLiabilities_Project1_last"].fillna(0).values + df["OtherCurrentLiabilities_Project2_last"].fillna(0).values + df["OtherCurrentLiabilities_Project3_last"].fillna(0).values + df["OtherCurrentLiabilities_Project4_last"].fillna(0).values - df["OtherCurrentLiabilities_Total_last"].fillna(0).values) > 0.01:
            error = "期初余额:短期应付债券+项目1+项目2+项目3+项目4<>合计"
            errorlist.append(error)












        return df, errorlist


if __name__ == "__main__":
    d = GetOtherCurrentLiabilities()