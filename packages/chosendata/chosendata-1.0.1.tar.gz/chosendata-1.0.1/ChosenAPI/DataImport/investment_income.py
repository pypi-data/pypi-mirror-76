
import pandas as pd
from ChosenAPI.DataImport.ChangeToNum import ChangeData



class GetInvestmentIncome(object):#投资收益
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
            "InvestmentIncome_EquityMethod_CurrentPeriod": data.cell_value(2, 1),  # B3 3行2列权益法核算的长期股权投资收益本期发生额
            "InvestmentIncome_DisposalLongtermequityinvest_CurrentPeriod": data.cell_value(3, 1),# B4 4行2列处置长期股权投资产生的投资收益本期发生额
            "InvestmentIncome_TradingAssets_CurrentPeriod": data.cell_value(4, 1),# B5 5行2列以公允价值计量的且其变动计入当期损益的金融资产在持有期间取得的投资收益本期发生额
            "InvestmentIncome_DisposalTradingAssets_CurrentPeriod": data.cell_value(5, 1),# B6 6行2列处置以公允价值计量的且其变动计入当期损益的金融资产取得的投资收益本期发生额
            "InvestmentIncome_Holdtomaturityinvestments_CurrentPeriod": data.cell_value(6, 1),# B7 7行2列持有至到期投资持有期间取得的投资收益本期发生额
            "InvestmentIncome_Holdforsaleassets_CurrentPeriod": data.cell_value(7, 1),# B8 8行2列可供出售金融资产持有期间取得的投资收益本期发生额
            "InvestmentIncome_DisposalHoldtomaturityinvestments_CurrentPeriod": data.cell_value(8, 1),# B9 9行2列处置持有至到期投资取得的投资收益本期发生额
            "InvestmentIncome_DisposalHoldforsaleassets_CurrentPeriod": data.cell_value(9, 1),# B10 10行2列处置可供出售金融资产取得的投资收益本期发生额
            "InvestmentIncome_Residue_CurrentPeriod": data.cell_value(10, 1),# B11 11行2列丧失控制权后，剩余股权按公允价值重新计量产生的利得或损失本期发生额
            "InvestmentIncome_Other_CurrentPeriod": data.cell_value(11, 1),  # B12 12行2列其他投资收益本期发生额
            "InvestmentIncome_Total_CurrentPeriod": data.cell_value(12, 1),  # B13 13行2列合计本期发生额
            "InvestmentIncome_EquityMethod_PriorPeriod": data.cell_value(2, 2),  # C3 3行3列权益法核算的长期股权投资收益上期发生额
            "InvestmentIncome_DisposalLongtermequityinvest_PriorPeriod": data.cell_value(3, 2),# C4 4行3列处置长期股权投资产生的投资收益上期发生额
            "InvestmentIncome_TradingAssets_PriorPeriod": data.cell_value(4, 2),# C5 5行3列以公允价值计量的且其变动计入当期损益的金融资产在持有期间取得的投资收益上期发生额
            "InvestmentIncome_DisposalTradingAssets_PriorPeriod": data.cell_value(5, 2),# C6 6行3列处置以公允价值计量的且其变动计入当期损益的金融资产取得的投资收益上期发生额
            "InvestmentIncome_Holdtomaturityinvestments_PriorPeriod": data.cell_value(6, 2),# C7 7行3列持有至到期投资持有期间取得的投资收益上期发生额
            "InvestmentIncome_Holdforsaleassets_PriorPeriod": data.cell_value(7, 2),  # C8 8行3列可供出售金融资产持有期间取得的投资收益上期发生额
            "InvestmentIncome_DisposalHoldtomaturityinvestments_PriorPeriod": data.cell_value(8, 2),# C9 9行3列处置持有至到期投资取得的投资收益上期发生额
            "InvestmentIncome_DisposalHoldforsaleassets_PriorPeriod": data.cell_value(9, 2),# C10 10行3列处置可供出售金融资产取得的投资收益上期发生额
            "InvestmentIncome_Residue_PriorPeriod": data.cell_value(10, 2),# C11 11行3列丧失控制权后，剩余股权按公允价值重新计量产生的利得或损失上期发生额
            "InvestmentIncome_Other_PriorPeriod": data.cell_value(11, 2),  # C12 12行3列其他投资收益上期发生额
            "InvestmentIncome_Total_PriorPeriod": data.cell_value(12, 2),  # C13 13行3列合计上期发生额


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
        dic["InvestmentIncome_Remark"] = data.cell_value(14, 1),  # B15 15行2列说明
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
        # 本期发生额：权益法核算的长期股权投资收益+处置长期股权投资产生的投资收益+以公允价值计量的且其变动计入当期损益的金融资产在持有期间取得的投资收益+处置以公允价值计量的且其变动计入当期损益的金融资产取得的投资收益+持有至到期投资持有期间取得的投资收益+可供出售金融资产持有期间取得的投资收益+处置持有至到期投资取得的投资收益+处置可供出售金融资产取得的投资收益+丧失控制权后，剩余股权按公允价值重新计量产生的利得或损失+其他投资收益=合计
        if abs(df["InvestmentIncome_EquityMethod_CurrentPeriod"].fillna(0).values + df["InvestmentIncome_DisposalLongtermequityinvest_CurrentPeriod"].fillna(0).values + df["InvestmentIncome_TradingAssets_CurrentPeriod"].fillna(0).values + df["InvestmentIncome_DisposalTradingAssets_CurrentPeriod"].fillna(0).values + df["InvestmentIncome_Holdtomaturityinvestments_CurrentPeriod"].fillna(0).values + df["InvestmentIncome_Holdforsaleassets_CurrentPeriod"].fillna(0).values + df["InvestmentIncome_DisposalHoldtomaturityinvestments_CurrentPeriod"].fillna(0).values + df["InvestmentIncome_DisposalHoldforsaleassets_CurrentPeriod"].fillna(0).values + df["InvestmentIncome_Residue_CurrentPeriod"].fillna(0).values + df["InvestmentIncome_Other_CurrentPeriod"].fillna(0).values - df["InvestmentIncome_Total_CurrentPeriod"].fillna(0).values) > 0.01:
            error = "本期发生额：权益法核算的长期股权投资收益+处置长期股权投资产生的投资收益+以公允价值计量的且其变动计入当期损益的金融资产在持有期间取得的投资收益+处置以公允价值计量的且其变动计入当期损益的金融资产取得的投资收益+持有至到期投资持有期间取得的投资收益+可供出售金融资产持有期间取得的投资收益+处置持有至到期投资取得的投资收益+处置可供出售金融资产取得的投资收益+丧失控制权后，剩余股权按公允价值重新计量产生的利得或损失+其他投资收益<>合计"
            errorlist.append(error)
        # 上期发生额：权益法核算的长期股权投资收益+处置长期股权投资产生的投资收益+以公允价值计量的且其变动计入当期损益的金融资产在持有期间取得的投资收益+处置以公允价值计量的且其变动计入当期损益的金融资产取得的投资收益+持有至到期投资持有期间取得的投资收益+可供出售金融资产持有期间取得的投资收益+处置持有至到期投资取得的投资收益+处置可供出售金融资产取得的投资收益+丧失控制权后，剩余股权按公允价值重新计量产生的利得或损失+其他投资收益=合计
        if abs(df["InvestmentIncome_EquityMethod_PriorPeriod"].fillna(0).values + df["InvestmentIncome_DisposalLongtermequityinvest_PriorPeriod"].fillna(0).values + df["InvestmentIncome_TradingAssets_PriorPeriod"].fillna(0).values + df["InvestmentIncome_DisposalTradingAssets_PriorPeriod"].fillna(0).values + df["InvestmentIncome_Holdtomaturityinvestments_PriorPeriod"].fillna(0).values + df["InvestmentIncome_Holdforsaleassets_PriorPeriod"].fillna(0).values + df["InvestmentIncome_DisposalHoldtomaturityinvestments_PriorPeriod"].fillna(0).values + df["InvestmentIncome_DisposalHoldforsaleassets_PriorPeriod"].fillna(0).values + df["InvestmentIncome_Residue_PriorPeriod"].fillna(0).values + df["InvestmentIncome_Other_PriorPeriod"].fillna(0).values - df["InvestmentIncome_Total_PriorPeriod"].fillna(0).values) > 0.01:
            error = "上期发生额：权益法核算的长期股权投资收益+处置长期股权投资产生的投资收益+以公允价值计量的且其变动计入当期损益的金融资产在持有期间取得的投资收益+处置以公允价值计量的且其变动计入当期损益的金融资产取得的投资收益+持有至到期投资持有期间取得的投资收益+可供出售金融资产持有期间取得的投资收益+处置持有至到期投资取得的投资收益+处置可供出售金融资产取得的投资收益+丧失控制权后，剩余股权按公允价值重新计量产生的利得或损失+其他投资收益<>合计"
            errorlist.append(error)
        











        return df, errorlist


if __name__ == "__main__":
    d = GetInvestmentIncome()