
import pandas as pd
from ChosenAPI.DataImport.ChangeToNum import ChangeData



class GetNonOperatingExpense(object):#营业外支出
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
            "NonOperatingExpense_Debtrestructuring_CurrentPeriod": data.cell_value(2, 1),  # B3 3行2列⑴债务重组损失本期发生额
            "NonOperatingExpense_Acceptdonations_CurrentPeriod": data.cell_value(3, 1),  # B4 4行2列⑵捐赠支出本期发生额
            "NonOperatingExpense_Very_CurrentPeriod": data.cell_value(4, 1),  # B5 5行2列⑶非常损失本期发生额
            "NonOperatingExpense_DishDeficient_CurrentPeriod": data.cell_value(5, 1),  # B6 6行2列⑷盘亏损失本期发生额
            "NonOperatingExpense_Netpenaltyincome_CurrentPeriod": data.cell_value(6, 1),  # B7 7行2列⑸罚款支出本期发生额
            "NonOperatingExpense_Guaranty_CurrentPeriod": data.cell_value(7, 1),  # B8 8行2列⑹确认的对外担保损失本期发生额
            "NonOperatingExpense_PendingLitigation_CurrentPeriod": data.cell_value(8, 1),  # B9 9行2列⑺确认的未决诉讼本期发生额
            "NonOperatingExpense_PendingTheArbitration_CurrentPeriod": data.cell_value(9, 1),# B10 10行2列⑻确认的未决仲裁本期发生额
            "NonOperatingExpense_OnerousContract_CurrentPeriod": data.cell_value(10, 1),  # B11 11行2列⑼确认的亏损合同本期发生额
            "NonOperatingExpense_RestructuringObligations_CurrentPeriod": data.cell_value(11, 1),# B12 12行2列⑽确认的重组义务本期发生额
            "NonOperatingExpense_Other_CurrentPeriod": data.cell_value(12, 1),  # B13 13行2列⑾其他本期发生额
            "NonOperatingExpense_Total_CurrentPeriod": data.cell_value(13, 1),  # B14 14行2列合计本期发生额
            "NonOperatingExpense_Debtrestructuring_PriorPeriod": data.cell_value(2, 2),  # C3 3行3列⑴债务重组损失上期发生额
            "NonOperatingExpense_Acceptdonations_PriorPeriod": data.cell_value(3, 2),  # C4 4行3列⑵捐赠支出上期发生额
            "NonOperatingExpense_Very_PriorPeriod": data.cell_value(4, 2),  # C5 5行3列⑶非常损失上期发生额
            "NonOperatingExpense_DishDeficient_PriorPeriod": data.cell_value(5, 2),  # C6 6行3列⑷盘亏损失上期发生额
            "NonOperatingExpense_Netpenaltyincome_PriorPeriod": data.cell_value(6, 2),  # C7 7行3列⑸罚款支出上期发生额
            "NonOperatingExpense_Guaranty_PriorPeriod": data.cell_value(7, 2),  # C8 8行3列⑹确认的对外担保损失上期发生额
            "NonOperatingExpense_PendingLitigation_PriorPeriod": data.cell_value(8, 2),  # C9 9行3列⑺确认的未决诉讼上期发生额
            "NonOperatingExpense_PendingTheArbitration_PriorPeriod": data.cell_value(9, 2),  # C10 10行3列⑻确认的未决仲裁上期发生额
            "NonOperatingExpense_OnerousContract_PriorPeriod": data.cell_value(10, 2),  # C11 11行3列⑼确认的亏损合同上期发生额
            "NonOperatingExpense_RestructuringObligations_PriorPeriod": data.cell_value(11, 2),# C12 12行3列⑽确认的重组义务上期发生额
            "NonOperatingExpense_Other_PriorPeriod": data.cell_value(12, 2),  # C13 13行3列⑾其他上期发生额
            "NonOperatingExpense_Total_PriorPeriod": data.cell_value(13, 2),  # C14 14行3列合计上期发生额
            "NonOperatingExpense_Debtrestructuring_sum": data.cell_value(2, 3),  # D3 3行4列⑴债务重组损失计入当期非经常性损益的金额
            "NonOperatingExpense_Acceptdonations_sum": data.cell_value(3, 3),  # D4 4行4列⑵捐赠支出计入当期非经常性损益的金额
            "NonOperatingExpense_Very_sum": data.cell_value(4, 3),  # D5 5行4列⑶非常损失计入当期非经常性损益的金额
            "NonOperatingExpense_DishDeficient_sum": data.cell_value(5, 3),  # D6 6行4列⑷盘亏损失计入当期非经常性损益的金额
            "NonOperatingExpense_Netpenaltyincome_sum": data.cell_value(6, 3),  # D7 7行4列⑸罚款支出计入当期非经常性损益的金额
            "NonOperatingExpense_Guaranty_sum": data.cell_value(7, 3),  # D8 8行4列⑹确认的对外担保损失计入当期非经常性损益的金额
            "NonOperatingExpense_PendingLitigation_sum": data.cell_value(8, 3),  # D9 9行4列⑺确认的未决诉讼计入当期非经常性损益的金额
            "NonOperatingExpense_PendingTheArbitration_sum": data.cell_value(9, 3),  # D10 10行4列⑻确认的未决仲裁计入当期非经常性损益的金额
            "NonOperatingExpense_OnerousContract_sum": data.cell_value(10, 3),  # D11 11行4列⑼确认的亏损合同计入当期非经常性损益的金额
            "NonOperatingExpense_RestructuringObligations_sum": data.cell_value(11, 3),# D12 12行4列⑽确认的重组义务计入当期非经常性损益的金额
            "NonOperatingExpense_Other_sum": data.cell_value(12, 3),  # D13 13行4列⑾其他计入当期非经常性损益的金额
            "NonOperatingExpense_Total_sum": data.cell_value(13, 3),  # D14 14行4列合计计入当期非经常性损益的金额


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
        dic["NonOperatingExpense_Remark"] = data.cell_value(15, 1),  # B16 16行2列说明
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
        # 本期发生额：债务重组损失+捐赠支出+非常损失+盘亏损失+罚款支出+确认的对外担保损失+确认的未决诉讼+确认的未决仲裁+确认的亏损合同+确认的重组义务+其他=合计
        if abs(df["NonOperatingExpense_Debtrestructuring_CurrentPeriod"].fillna(0).values + df["NonOperatingExpense_Acceptdonations_CurrentPeriod"].fillna(0).values + df["NonOperatingExpense_Very_CurrentPeriod"].fillna(0).values + df["NonOperatingExpense_DishDeficient_CurrentPeriod"].fillna(0).values + df["NonOperatingExpense_Netpenaltyincome_CurrentPeriod"].fillna(0).values + df["NonOperatingExpense_Guaranty_CurrentPeriod"].fillna(0).values + df["NonOperatingExpense_PendingLitigation_CurrentPeriod"].fillna(0).values + df["NonOperatingExpense_PendingTheArbitration_CurrentPeriod"].fillna(0).values + df["NonOperatingExpense_OnerousContract_CurrentPeriod"].fillna(0).values + df["NonOperatingExpense_RestructuringObligations_CurrentPeriod"].fillna(0).values + df["NonOperatingExpense_Other_CurrentPeriod"].fillna(0).values - df["NonOperatingExpense_Total_CurrentPeriod"].fillna(0).values) > 0.01:
            error = "本期发生额：债务重组损失+捐赠支出+非常损失+盘亏损失+罚款支出+确认的对外担保损失+确认的未决诉讼+确认的未决仲裁+确认的亏损合同+确认的重组义务+其他<>合计"
            errorlist.append(error)
        # 上期发生额：债务重组损失+捐赠支出+非常损失+盘亏损失+罚款支出+确认的对外担保损失+确认的未决诉讼+确认的未决仲裁+确认的亏损合同+确认的重组义务+其他=合计
        if abs(df["NonOperatingExpense_Debtrestructuring_PriorPeriod"].fillna(0).values + df["NonOperatingExpense_Acceptdonations_PriorPeriod"].fillna(0).values + df["NonOperatingExpense_Very_PriorPeriod"].fillna(0).values + df["NonOperatingExpense_DishDeficient_PriorPeriod"].fillna(0).values + df["NonOperatingExpense_Netpenaltyincome_PriorPeriod"].fillna(0).values + df["NonOperatingExpense_Guaranty_PriorPeriod"].fillna(0).values + df["NonOperatingExpense_PendingLitigation_PriorPeriod"].fillna(0).values + df["NonOperatingExpense_PendingTheArbitration_PriorPeriod"].fillna(0).values + df["NonOperatingExpense_OnerousContract_PriorPeriod"].fillna(0).values + df["NonOperatingExpense_RestructuringObligations_PriorPeriod"].fillna(0).values + df["NonOperatingExpense_Other_PriorPeriod"].fillna(0).values - df["NonOperatingExpense_Total_PriorPeriod"].fillna(0).values) > 0.01:
            error = "上期发生额：债务重组损失+捐赠支出+非常损失+盘亏损失+罚款支出+确认的对外担保损失+确认的未决诉讼+确认的未决仲裁+确认的亏损合同+确认的重组义务+其他<>合计"
            errorlist.append(error)
        # 计入当期非经常性损益的金额：债务重组损失+捐赠支出+非常损失+盘亏损失+罚款支出+确认的对外担保损失+确认的未决诉讼+确认的未决仲裁+确认的亏损合同+确认的重组义务+其他=合计
        if abs(df["NonOperatingExpense_Debtrestructuring_sum"].fillna(0).values + df["NonOperatingExpense_Acceptdonations_sum"].fillna(0).values + df["NonOperatingExpense_Very_sum"].fillna(0).values + df["NonOperatingExpense_DishDeficient_sum"].fillna(0).values + df["NonOperatingExpense_Netpenaltyincome_sum"].fillna(0).values + df["NonOperatingExpense_Guaranty_sum"].fillna(0).values + df["NonOperatingExpense_PendingLitigation_sum"].fillna(0).values + df["NonOperatingExpense_PendingTheArbitration_sum"].fillna(0).values + df["NonOperatingExpense_OnerousContract_sum"].fillna(0).values + df["NonOperatingExpense_RestructuringObligations_sum"].fillna(0).values + df["NonOperatingExpense_Other_sum"].fillna(0).values - df["NonOperatingExpense_Total_sum"].fillna(0).values) > 0.01:
            error = "计入当期非经常性损益的金额：债务重组损失+捐赠支出+非常损失+盘亏损失+罚款支出+确认的对外担保损失+确认的未决诉讼+确认的未决仲裁+确认的亏损合同+确认的重组义务+其他<>合计"
            errorlist.append(error)

        return df, errorlist


if __name__ == "__main__":
    d = GetNonOperatingExpense()