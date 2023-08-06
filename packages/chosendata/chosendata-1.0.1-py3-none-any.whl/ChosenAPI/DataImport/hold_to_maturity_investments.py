
import pandas as pd
from ChosenAPI.DataImport.ChangeToNum import ChangeData



class GetHoldToMaturityInvestments(object):#持有至到期投资
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
            "HoldToMaturityInvestments_Project1_BookBalance_this": data.cell_value(4, 1),  # B5 5行2列项目1期末余额账面余额
            "HoldToMaturityInvestments_Project2_BookBalance_this": data.cell_value(5, 1),  # B6 6行2列项目2期末余额账面余额
            "HoldToMaturityInvestments_Project3_BookBalance_this": data.cell_value(6, 1),  # B7 7行2列项目3期末余额账面余额
            "HoldToMaturityInvestments_Project4_BookBalance_this": data.cell_value(7, 1),  # B8 8行2列项目4期末余额账面余额
            "HoldToMaturityInvestments_Project5_BookBalance_this": data.cell_value(8, 1),  # B9 9行2列项目5期末余额账面余额
            "HoldToMaturityInvestments_Total_BookBalance_this": data.cell_value(9, 1),  # B10 10行2列合计期末余额账面余额
            "HoldToMaturityInvestments_Project1_ImpairmentLoss_this": data.cell_value(4, 2),  # C5 5行3列项目1期末余额减值准备
            "HoldToMaturityInvestments_Project2_ImpairmentLoss_this": data.cell_value(5, 2),  # C6 6行3列项目2期末余额减值准备
            "HoldToMaturityInvestments_Project3_ImpairmentLoss_this": data.cell_value(6, 2),  # C7 7行3列项目3期末余额减值准备
            "HoldToMaturityInvestments_Project4_ImpairmentLoss_this": data.cell_value(7, 2),  # C8 8行3列项目4期末余额减值准备
            "HoldToMaturityInvestments_Project5_ImpairmentLoss_this": data.cell_value(8, 2),  # C9 9行3列项目5期末余额减值准备
            "HoldToMaturityInvestments_Total_ImpairmentLoss_this": data.cell_value(9, 2),  # C10 10行3列合计期末余额减值准备
            "HoldToMaturityInvestments_Project1_BookValue_this": data.cell_value(4, 3),  # D5 5行4列项目1期末余额账面价值
            "HoldToMaturityInvestments_Project2_BookValue_this": data.cell_value(5, 3),  # D6 6行4列项目2期末余额账面价值
            "HoldToMaturityInvestments_Project3_BookValue_this": data.cell_value(6, 3),  # D7 7行4列项目3期末余额账面价值
            "HoldToMaturityInvestments_Project4_BookValue_this": data.cell_value(7, 3),  # D8 8行4列项目4期末余额账面价值
            "HoldToMaturityInvestments_Project5_BookValue_this": data.cell_value(8, 3),  # D9 9行4列项目5期末余额账面价值
            "HoldToMaturityInvestments_Total_BookValue_this": data.cell_value(9, 3),  # D10 10行4列合计期末余额账面价值
            "HoldToMaturityInvestments_Project1_BookBalance_last": data.cell_value(4, 4),  # E5 5行5列项目1期初余额账面余额
            "HoldToMaturityInvestments_Project2_BookBalance_last": data.cell_value(5, 4),  # E6 6行5列项目2期初余额账面余额
            "HoldToMaturityInvestments_Project3_BookBalance_last": data.cell_value(6, 4),  # E7 7行5列项目3期初余额账面余额
            "HoldToMaturityInvestments_Project4_BookBalance_last": data.cell_value(7, 4),  # E8 8行5列项目4期初余额账面余额
            "HoldToMaturityInvestments_Project5_BookBalance_last": data.cell_value(8, 4),  # E9 9行5列项目5期初余额账面余额
            "HoldToMaturityInvestments_Total_BookBalance_last": data.cell_value(9, 4),  # E10 10行5列合计期初余额账面余额
            "HoldToMaturityInvestments_Project1_ImpairmentLoss_last": data.cell_value(4, 5),  # F5 5行6列项目1期初余额减值准备
            "HoldToMaturityInvestments_Project2_ImpairmentLoss_last": data.cell_value(5, 5),  # F6 6行6列项目2期初余额减值准备
            "HoldToMaturityInvestments_Project3_ImpairmentLoss_last": data.cell_value(6, 5),  # F7 7行6列项目3期初余额减值准备
            "HoldToMaturityInvestments_Project4_ImpairmentLoss_last": data.cell_value(7, 5),  # F8 8行6列项目4期初余额减值准备
            "HoldToMaturityInvestments_Project5_ImpairmentLoss_last": data.cell_value(8, 5),  # F9 9行6列项目5期初余额减值准备
            "HoldToMaturityInvestments_Total_ImpairmentLoss_last": data.cell_value(9, 5),  # F10 10行6列合计期初余额减值准备
            "HoldToMaturityInvestments_Project1_BookValue_last": data.cell_value(4, 6),  # G5 5行7列项目1期初余额账面价值
            "HoldToMaturityInvestments_Project2_BookValue_last": data.cell_value(5, 6),  # G6 6行7列项目2期初余额账面价值
            "HoldToMaturityInvestments_Project3_BookValue_last": data.cell_value(6, 6),  # G7 7行7列项目3期初余额账面价值
            "HoldToMaturityInvestments_Project4_BookValue_last": data.cell_value(7, 6),  # G8 8行7列项目4期初余额账面价值
            "HoldToMaturityInvestments_Project5_BookValue_last": data.cell_value(8, 6),  # G9 9行7列项目5期初余额账面价值
            "HoldToMaturityInvestments_Total_BookValue_last": data.cell_value(9, 6),  # G10 10行7列合计期初余额账面价值
            "HoldToMaturityInvestments_BondProgram1_FaceValue": data.cell_value(13, 1),  # B14 14行2列债券项目1面值
            "HoldToMaturityInvestments_BondProgram2_FaceValue": data.cell_value(14, 1),  # B15 15行2列债券项目2面值
            "HoldToMaturityInvestments_BondProgram3_FaceValue": data.cell_value(15, 1),  # B16 16行2列债券项目3面值
            "HoldToMaturityInvestments_BondProgram4_FaceValue": data.cell_value(16, 1),  # B17 17行2列债券项目4面值
            "HoldToMaturityInvestments_BondProgram5_FaceValue": data.cell_value(17, 1),  # B18 18行2列债券项目5面值
            "HoldToMaturityInvestments_Total_FaceValue": data.cell_value(18, 1),  # B19 19行2列合计面值
            "HoldToMaturityInvestments_BondProgram1_CouponRate": data.cell_value(13, 2),  # C14 14行3列债券项目1票面利率
            "HoldToMaturityInvestments_BondProgram2_CouponRate": data.cell_value(14, 2),  # C15 15行3列债券项目2票面利率
            "HoldToMaturityInvestments_BondProgram3_CouponRate": data.cell_value(15, 2),  # C16 16行3列债券项目3票面利率
            "HoldToMaturityInvestments_BondProgram4_CouponRate": data.cell_value(16, 2),  # C17 17行3列债券项目4票面利率
            "HoldToMaturityInvestments_BondProgram5_CouponRate": data.cell_value(17, 2),  # C18 18行3列债券项目5票面利率
            "HoldToMaturityInvestments_BondProgram1_ActualInterestRate": data.cell_value(13, 3),# D14 14行4列债券项目1实际利率
            "HoldToMaturityInvestments_BondProgram2_ActualInterestRate": data.cell_value(14, 3),# D15 15行4列债券项目2实际利率
            "HoldToMaturityInvestments_BondProgram3_ActualInterestRate": data.cell_value(15, 3),# D16 16行4列债券项目3实际利率
            "HoldToMaturityInvestments_BondProgram4_ActualInterestRate": data.cell_value(16, 3),# D17 17行4列债券项目4实际利率
            "HoldToMaturityInvestments_BondProgram5_ActualInterestRate": data.cell_value(17, 3),# D18 18行4列债券项目5实际利率
            "HoldToMaturityInvestments_BondProgram1_DueDate": data.cell_value(13, 4),  # E14 14行5列债券项目1到期日
            "HoldToMaturityInvestments_BondProgram2_DueDate": data.cell_value(14, 4),  # E15 15行5列债券项目2到期日
            "HoldToMaturityInvestments_BondProgram3_DueDate": data.cell_value(15, 4),  # E16 16行5列债券项目3到期日
            "HoldToMaturityInvestments_BondProgram4_DueDate": data.cell_value(16, 4),  # E17 17行5列债券项目4到期日
            "HoldToMaturityInvestments_BondProgram5_DueDate": data.cell_value(17, 4),  # E18 18行5列债券项目5到期日


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
        dic["HoldToMaturityInvestments_Remark"] = data.cell_value(20, 1),  # B21 21行2列说明
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
        # 期末余额账面余额:项目1+项目2+项目3+项目4+项目5=合计
        if abs(df["HoldToMaturityInvestments_Project1_BookBalance_this"].fillna(0).values + df["HoldToMaturityInvestments_Project2_BookBalance_this"].fillna(0).values + df["HoldToMaturityInvestments_Project3_BookBalance_this"].fillna(0).values + df["HoldToMaturityInvestments_Project4_BookBalance_this"].fillna(0).values + df["HoldToMaturityInvestments_Project5_BookBalance_this"].fillna(0).values - df["HoldToMaturityInvestments_Total_BookBalance_this"].fillna(0).values) > 0.01:
            error = "期末余额账面余额:项目1+项目2+项目3+项目4+项目5<>合计"
            errorlist.append(error)
        # 期末余额减值准备:项目1+项目2+项目3+项目4+项目5=合计
        if abs(df["HoldToMaturityInvestments_Project1_ImpairmentLoss_this"].fillna(0).values + df["HoldToMaturityInvestments_Project2_ImpairmentLoss_this"].fillna(0).values + df["HoldToMaturityInvestments_Project3_ImpairmentLoss_this"].fillna(0).values + df["HoldToMaturityInvestments_Project4_ImpairmentLoss_this"].fillna(0).values + df["HoldToMaturityInvestments_Project5_ImpairmentLoss_this"].fillna(0).values - df["HoldToMaturityInvestments_Total_ImpairmentLoss_this"].fillna(0).values) > 0.01:
            error = "期末余额减值准备:项目1+项目2+项目3+项目4+项目5<>合计"
            errorlist.append(error)
        # 期末余额账面价值:项目1+项目2+项目3+项目4+项目5=合计
        if abs(df["HoldToMaturityInvestments_Project1_BookValue_this"].fillna(0).values + df["HoldToMaturityInvestments_Project2_BookValue_this"].fillna(0).values + df["HoldToMaturityInvestments_Project3_BookValue_this"].fillna(0).values + df["HoldToMaturityInvestments_Project4_BookValue_this"].fillna(0).values + df["HoldToMaturityInvestments_Project5_BookValue_this"].fillna(0).values - df["HoldToMaturityInvestments_Total_BookValue_this"].fillna(0).values) > 0.01:
            error = "期末余额账面价值:项目1+项目2+项目3+项目4+项目5<>合计"
            errorlist.append(error)
        # 期初余额账面余额:项目1+项目2+项目3+项目4+项目5=合计
        if abs(df["HoldToMaturityInvestments_Project1_BookBalance_last"].fillna(0).values + df["HoldToMaturityInvestments_Project2_BookBalance_last"].fillna(0).values + df["HoldToMaturityInvestments_Project3_BookBalance_last"].fillna(0).values + df["HoldToMaturityInvestments_Project4_BookBalance_last"].fillna(0).values + df["HoldToMaturityInvestments_Project5_BookBalance_last"].fillna(0).values - df["HoldToMaturityInvestments_Total_BookBalance_last"].fillna(0).values) > 0.01:
            error = "期初余额账面余额:项目1+项目2+项目3+项目4+项目5<>合计"
            errorlist.append(error)
        # 期初余额减值准备:项目1+项目2+项目3+项目4+项目5=合计
        if abs(df["HoldToMaturityInvestments_Project1_ImpairmentLoss_last"].fillna(0).values + df["HoldToMaturityInvestments_Project2_ImpairmentLoss_last"].fillna(0).values + df["HoldToMaturityInvestments_Project3_ImpairmentLoss_last"].fillna(0).values + df["HoldToMaturityInvestments_Project4_ImpairmentLoss_last"].fillna(0).values + df["HoldToMaturityInvestments_Project5_ImpairmentLoss_last"].fillna(0).values - df["HoldToMaturityInvestments_Total_ImpairmentLoss_last"].fillna(0).values) > 0.01:
            error = "期初余额减值准备:项目1+项目2+项目3+项目4+项目5<>合计"
            errorlist.append(error)
        # 期初余额账面价值:项目1+项目2+项目3+项目4+项目5=合计
        if abs(df["HoldToMaturityInvestments_Project1_BookValue_last"].fillna(0).values + df["HoldToMaturityInvestments_Project2_BookValue_last"].fillna(0).values + df["HoldToMaturityInvestments_Project3_BookValue_last"].fillna(0).values + df["HoldToMaturityInvestments_Project4_BookValue_last"].fillna(0).values + df["HoldToMaturityInvestments_Project5_BookValue_last"].fillna(0).values - df["HoldToMaturityInvestments_Total_BookValue_last"].fillna(0).values) > 0.01:
            error = "期初余额账面价值:项目1+项目2+项目3+项目4+项目5<>合计"
            errorlist.append(error)
        # 面值:债券项目1+债券项目2+债券项目3+债券项目4+债券项目5=合计
        if abs(df["HoldToMaturityInvestments_BondProgram1_FaceValue"].fillna(0).values + df["HoldToMaturityInvestments_BondProgram2_FaceValue"].fillna(0).values + df["HoldToMaturityInvestments_BondProgram3_FaceValue"].fillna(0).values + df["HoldToMaturityInvestments_BondProgram4_FaceValue"].fillna(0).values + df["HoldToMaturityInvestments_BondProgram5_FaceValue"].fillna(0).values - df["HoldToMaturityInvestments_Total_FaceValue"].fillna(0).values) > 0.01:
            error = "面值:债券项目1+债券项目2+债券项目3+债券项目4+债券项目5<>合计"
            errorlist.append(error)










        return df, errorlist


if __name__ == "__main__":
    d = GetHoldToMaturityInvestments()