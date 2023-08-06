
import pandas as pd
from ChosenAPI.DataImport.ChangeToNum import ChangeData



class GetNonOperatingRevenue(object):#营业外收入
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
            "NonOperatingRevenue_DebtRestructuring_CurrentPeriod": data.cell_value(2, 1),  # B3 3行2列⑴债务重组利得本期发生额
            "NonOperatingRevenue_AcceptDonations_CurrentPeriod": data.cell_value(3, 1),  # B4 4行2列⑵接受捐赠本期发生额
            "NonOperatingRevenue_GovernmentSubsidy_CurrentPeriod": data.cell_value(4, 1),  # B5 5行2列⑶政府补助本期发生额
            "NonOperatingRevenue_InventorySurplus_CurrentPeriod": data.cell_value(5, 1),  # B6 6行2列⑷盘盈利得本期发生额
            "NonOperatingRevenue_NotTheSame_CurrentPeriod": data.cell_value(6, 1),  # B7 7行2列⑸非同一控制下的企业合并收益本期发生额
            "NonOperatingRevenue_NetPenaltyIncome_CurrentPeriod": data.cell_value(7, 1),  # B8 8行2列⑹罚款净收入本期发生额
            "NonOperatingRevenue_Other_CurrentPeriod": data.cell_value(8, 1),  # B9 9行2列⑺其他本期发生额
            "NonOperatingRevenue_Total_CurrentPeriod": data.cell_value(9, 1),  # B10 10行2列合计本期发生额
            "NonOperatingRevenue_DebtRestructuring_PriorPeriod": data.cell_value(2, 2),  # C3 3行3列⑴债务重组利得上期发生额
            "NonOperatingRevenue_AcceptDonations_PriorPeriod": data.cell_value(3, 2),  # C4 4行3列⑵接受捐赠上期发生额
            "NonOperatingRevenue_GovernmentSubsidy_PriorPeriod": data.cell_value(4, 2),  # C5 5行3列⑶政府补助上期发生额
            "NonOperatingRevenue_InventorySurplus_PriorPeriod": data.cell_value(5, 2),  # C6 6行3列⑷盘盈利得上期发生额
            "NonOperatingRevenue_NotTheSame_PriorPeriod": data.cell_value(6, 2),  # C7 7行3列⑸非同一控制下的企业合并收益上期发生额
            "NonOperatingRevenue_NetPenaltyIncome_PriorPeriod": data.cell_value(7, 2),  # C8 8行3列⑹罚款净收入上期发生额
            "NonOperatingRevenue_Other_PriorPeriod": data.cell_value(8, 2),  # C9 9行3列⑺其他上期发生额
            "NonOperatingRevenue_Total_PriorPeriod": data.cell_value(9, 2),  # C10 10行3列合计上期发生额
            "NonOperatingRevenue_DebtRestructuring_sum": data.cell_value(2, 3),  # D3 3行4列⑴债务重组利得计入当期非经常性损益的金额
            "NonOperatingRevenue_AcceptDonations_sum": data.cell_value(3, 3),  # D4 4行4列⑵接受捐赠计入当期非经常性损益的金额
            "NonOperatingRevenue_GovernmentSubsidy_sum": data.cell_value(4, 3),  # D5 5行4列⑶政府补助计入当期非经常性损益的金额
            "NonOperatingRevenue_InventorySurplus_sum": data.cell_value(5, 3),  # D6 6行4列⑷盘盈利得计入当期非经常性损益的金额
            "NonOperatingRevenue_NotTheSame_sum": data.cell_value(6, 3),  # D7 7行4列⑸非同一控制下的企业合并收益计入当期非经常性损益的金额
            "NonOperatingRevenue_NetPenaltyIncome_sum": data.cell_value(7, 3),  # D8 8行4列⑹罚款净收入计入当期非经常性损益的金额
            "NonOperatingRevenue_Other_sum": data.cell_value(8, 3),  # D9 9行4列⑺其他计入当期非经常性损益的金额
            "NonOperatingRevenue_Total_sum": data.cell_value(9, 3),  # D10 10行4列合计计入当期非经常性损益的金额
            "NonOperatingRevenue_Project1_CurrentPeriod": data.cell_value(13, 1),  # B14 14行2列项目1本期发生金
            "NonOperatingRevenue_Project2_CurrentPeriod": data.cell_value(14, 1),  # B15 15行2列项目2本期发生金
            "NonOperatingRevenue_Project3_CurrentPeriod": data.cell_value(15, 1),  # B16 16行2列项目3本期发生金
            "NonOperatingRevenue_Project4_CurrentPeriod": data.cell_value(16, 1),  # B17 17行2列项目4本期发生金
            "NonOperatingRevenue_Project5_CurrentPeriod": data.cell_value(17, 1),  # B18 18行2列项目5本期发生金
            "NonOperatingRevenue_SubsidyTotal_CurrentPeriod": data.cell_value(18, 1),  # B19 19行2列合计本期发生金
            "NonOperatingRevenue_Project1_PriorPeriod": data.cell_value(13, 2),  # C14 14行3列项目1上期发生额
            "NonOperatingRevenue_Project2_PriorPeriod": data.cell_value(14, 2),  # C15 15行3列项目2上期发生额
            "NonOperatingRevenue_Project3_PriorPeriod": data.cell_value(15, 2),  # C16 16行3列项目3上期发生额
            "NonOperatingRevenue_Project4_PriorPeriod": data.cell_value(16, 2),  # C17 17行3列项目4上期发生额
            "NonOperatingRevenue_Project5_PriorPeriod": data.cell_value(17, 2),  # C18 18行3列项目5上期发生额
            "NonOperatingRevenue_SubsidyTotal_PriorPeriod": data.cell_value(18, 2),  # C19 19行3列合计上期发生额


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
        dic["NonOperatingRevenue_Remark"] = data.cell_value(20, 1),  # B21 21行2列说明
        dic["NonOperatingRevenue_Project1_related"] = data.cell_value(13, 3),  # D14 14行4列项目1与资产相关/与收益相关
        dic["NonOperatingRevenue_Project2_related"] = data.cell_value(14, 3),  # D15 15行4列项目2与资产相关/与收益相关
        dic["NonOperatingRevenue_Project3_related"] = data.cell_value(15, 3),  # D16 16行4列项目3与资产相关/与收益相关
        dic["NonOperatingRevenue_Project4_related"] = data.cell_value(16, 3),  # D17 17行4列项目4与资产相关/与收益相关
        dic["NonOperatingRevenue_Project5_related"] = data.cell_value(17, 3),  # D18 18行4列项目5与资产相关/与收益相关
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
        # 本期发生额：债务重组利得+接受捐赠+政府补助+盘盈利得+非同一控制下的企业合并收益+罚款净收入+其他=合计
        if abs(df["NonOperatingRevenue_DebtRestructuring_CurrentPeriod"].fillna(0).values + df["NonOperatingRevenue_AcceptDonations_CurrentPeriod"].fillna(0).values + df["NonOperatingRevenue_GovernmentSubsidy_CurrentPeriod"].fillna(0).values + df["NonOperatingRevenue_InventorySurplus_CurrentPeriod"].fillna(0).values + df["NonOperatingRevenue_NotTheSame_CurrentPeriod"].fillna(0).values + df["NonOperatingRevenue_NetPenaltyIncome_CurrentPeriod"].fillna(0).values + df["NonOperatingRevenue_Other_CurrentPeriod"].fillna(0).values - df["NonOperatingRevenue_Total_CurrentPeriod"].fillna(0).values) > 0.01:
            error = "本期发生额：债务重组利得+接受捐赠+政府补助+盘盈利得+非同一控制下的企业合并收益+罚款净收入+其他<>合计"
            errorlist.append(error)
        # 上期发生额：债务重组利得+接受捐赠+政府补助+盘盈利得+非同一控制下的企业合并收益+罚款净收入+其他=合计
        if abs(df["NonOperatingRevenue_DebtRestructuring_PriorPeriod"].fillna(0).values + df["NonOperatingRevenue_AcceptDonations_PriorPeriod"].fillna(0).values + df["NonOperatingRevenue_GovernmentSubsidy_PriorPeriod"].fillna(0).values + df["NonOperatingRevenue_InventorySurplus_PriorPeriod"].fillna(0).values + df["NonOperatingRevenue_NotTheSame_PriorPeriod"].fillna(0).values + df["NonOperatingRevenue_NetPenaltyIncome_PriorPeriod"].fillna(0).values + df["NonOperatingRevenue_Other_PriorPeriod"].fillna(0).values - df["NonOperatingRevenue_Total_PriorPeriod"].fillna(0).values) > 0.01:
            error = "上期发生额：债务重组利得+接受捐赠+政府补助+盘盈利得+非同一控制下的企业合并收益+罚款净收入+其他<>合计"
            errorlist.append(error)
        # 计入当期非经常性损益的金额：债务重组利得+接受捐赠+政府补助+盘盈利得+非同一控制下的企业合并收益+罚款净收入+其他=合计
        if abs(df["NonOperatingRevenue_DebtRestructuring_sum"].fillna(0).values + df["NonOperatingRevenue_AcceptDonations_sum"].fillna(0).values + df["NonOperatingRevenue_GovernmentSubsidy_sum"].fillna(0).values + df["NonOperatingRevenue_InventorySurplus_sum"].fillna(0).values + df["NonOperatingRevenue_NotTheSame_sum"].fillna(0).values + df["NonOperatingRevenue_NetPenaltyIncome_sum"].fillna(0).values + df["NonOperatingRevenue_Other_sum"].fillna(0).values - df["NonOperatingRevenue_Total_sum"].fillna(0).values) > 0.01:
            error = "计入当期非经常性损益的金额：债务重组利得+接受捐赠+政府补助+盘盈利得+非同一控制下的企业合并收益+罚款净收入+其他<>合计"
            errorlist.append(error)
        # 计入当期损益的政府补助本期发生额：项目1+项目2+项目3+项目4+项目5=合计
        if abs(df["NonOperatingRevenue_Project1_CurrentPeriod"].fillna(0).values + df["NonOperatingRevenue_Project2_CurrentPeriod"].fillna(0).values + df["NonOperatingRevenue_Project3_CurrentPeriod"].fillna(0).values + df["NonOperatingRevenue_Project4_CurrentPeriod"].fillna(0).values + df["NonOperatingRevenue_Project5_CurrentPeriod"].fillna(0).values - df["NonOperatingRevenue_SubsidyTotal_CurrentPeriod"].fillna(0).values) > 0.01:
            error = "计入当期损益的政府补助本期发生额：项目1+项目2+项目3+项目4+项目5<>合计"
            errorlist.append(error)
        # 计入当期损益的政府补助上期发生额：项目1+项目2+项目3+项目4+项目5=合计
        if abs(df["NonOperatingRevenue_Project1_PriorPeriod"].fillna(0).values + df["NonOperatingRevenue_Project2_PriorPeriod"].fillna(0).values + df["NonOperatingRevenue_Project3_PriorPeriod"].fillna(0).values + df["NonOperatingRevenue_Project4_PriorPeriod"].fillna(0).values + df["NonOperatingRevenue_Project5_PriorPeriod"].fillna(0).values - df["NonOperatingRevenue_SubsidyTotal_PriorPeriod"].fillna(0).values) > 0.01:
            error = "计入当期损益的政府补助上期发生额：项目1+项目2+项目3+项目4+项目5<>合计"
            errorlist.append(error)

        return df, errorlist


if __name__ == "__main__":
    d = GetNonOperatingRevenue()