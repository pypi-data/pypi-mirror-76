
import pandas as pd
from ChosenAPI.DataImport.ChangeToNum import ChangeData



class GetHoldForSaleAssets(object):#可供出售金融资产
    def _init_(self):
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
            "HoldForSaleAssets_Debt_BookBalance_this": data.cell_value(4, 1),  # B5 5行2列可供出售债务工具期末余额账面余额
            "HoldForSaleAssets_Equities_BookBalance_this": data.cell_value(5, 1),  # B6 6行2列可供出售权益工具期末余额账面余额
            "HoldForSaleAssets_FairValue_BookBalance_this": data.cell_value(6, 1),  # B7 7行2列其中：按公允价值计量的权益工具期末余额账面余额
            "HoldForSaleAssets_Cost_BookBalance_this": data.cell_value(7, 1),  # B8 8行2列      按成本计量的权益工具期末余额账面余额
            "HoldForSaleAssets_Other_BookBalance_this": data.cell_value(8, 1),  # B9 9行2列其他期末余额账面余额
            "HoldForSaleAssets_Total_BookBalance_this": data.cell_value(9, 1),  # B10 10行2列合计期末余额账面余额
            "HoldForSaleAssets_Debt_ImpairmentLoss_this": data.cell_value(4, 2),  # C5 5行3列可供出售债务工具期末余额减值准备
            "HoldForSaleAssets_Equities_ImpairmentLoss_this": data.cell_value(5, 2),  # C6 6行3列可供出售权益工具期末余额减值准备
            "HoldForSaleAssets_FairValue_ImpairmentLoss_this": data.cell_value(6, 2),# C7 7行3列其中：按公允价值计量的权益工具期末余额减值准备
            "HoldForSaleAssets_Cost_ImpairmentLoss_this": data.cell_value(7, 2),  # C8 8行3列      按成本计量的权益工具期末余额减值准备
            "HoldForSaleAssets_Other_ImpairmentLoss_this": data.cell_value(8, 2),  # C9 9行3列其他期末余额减值准备
            "HoldForSaleAssets_Total_ImpairmentLoss_this": data.cell_value(9, 2),  # C10 10行3列合计期末余额减值准备
            "HoldForSaleAssets_Debt_BookValue_this": data.cell_value(4, 3),  # D5 5行4列可供出售债务工具期末余额账面价值
            "HoldForSaleAssets_Equities_BookValue_this": data.cell_value(5, 3),  # D6 6行4列可供出售权益工具期末余额账面价值
            "HoldForSaleAssets_FairValue_BookValue_this": data.cell_value(6, 3),  # D7 7行4列其中：按公允价值计量的权益工具期末余额账面价值
            "HoldForSaleAssets_Cost_BookValue_this": data.cell_value(7, 3),  # D8 8行4列      按成本计量的权益工具期末余额账面价值
            "HoldForSaleAssets_Other_BookValue_this": data.cell_value(8, 3),  # D9 9行4列其他期末余额账面价值
            "HoldForSaleAssets_Total_BookValue_this": data.cell_value(9, 3),  # D10 10行4列合计期末余额账面价值
            "HoldForSaleAssets_Debt_BookBalance_last": data.cell_value(4, 4),  # E5 5行5列可供出售债务工具期初余额账面余额
            "HoldForSaleAssets_Equities_BookBalance_last": data.cell_value(5, 4),  # E6 6行5列可供出售权益工具期初余额账面余额
            "HoldForSaleAssets_FairValue_BookBalance_last": data.cell_value(6, 4),  # E7 7行5列其中：按公允价值计量的权益工具期初余额账面余额
            "HoldForSaleAssets_Cost_BookBalance_last": data.cell_value(7, 4),  # E8 8行5列      按成本计量的权益工具期初余额账面余额
            "HoldForSaleAssets_Other_BookBalance_last": data.cell_value(8, 4),  # E9 9行5列其他期初余额账面余额
            "HoldForSaleAssets_Total_BookBalance_last": data.cell_value(9, 4),  # E10 10行5列合计期初余额账面余额
            "HoldForSaleAssets_Debt_ImpairmentLoss_last": data.cell_value(4, 5),  # F5 5行6列可供出售债务工具期初余额减值准备
            "HoldForSaleAssets_Equities_ImpairmentLoss_last": data.cell_value(5, 5),  # F6 6行6列可供出售权益工具期初余额减值准备
            "HoldForSaleAssets_FairValue_ImpairmentLoss_last": data.cell_value(6, 5),# F7 7行6列其中：按公允价值计量的权益工具期初余额减值准备
            "HoldForSaleAssets_Cost_ImpairmentLoss_last": data.cell_value(7, 5),  # F8 8行6列      按成本计量的权益工具期初余额减值准备
            "HoldForSaleAssets_Other_ImpairmentLoss_last": data.cell_value(8, 5),  # F9 9行6列其他期初余额减值准备
            "HoldForSaleAssets_Total_ImpairmentLoss_last": data.cell_value(9, 5),  # F10 10行6列合计期初余额减值准备
            "HoldForSaleAssets_Debt_BookValue_last": data.cell_value(4, 6),  # G5 5行7列可供出售债务工具期初余额账面价值
            "HoldForSaleAssets_Equities_BookValue_last": data.cell_value(5, 6),  # G6 6行7列可供出售权益工具期初余额账面价值
            "HoldForSaleAssets_FairValue_BookValue_last": data.cell_value(6, 6),  # G7 7行7列其中：按公允价值计量的权益工具期初余额账面价值
            "HoldForSaleAssets_Cost_BookValue_last": data.cell_value(7, 6),  # G8 8行7列      按成本计量的权益工具期初余额账面价值
            "HoldForSaleAssets_Other_BookValue_last": data.cell_value(8, 6),  # G9 9行7列其他期初余额账面价值
            "HoldForSaleAssets_Total_BookValue_last": data.cell_value(9, 6),  # G10 10行7列合计期初余额账面价值
            "HoldForSaleAssets_Cost_debt": data.cell_value(13, 1),  # B14 14行2列权益工具的成本/债务工具的摊余成本可供出售权益工具
            "HoldForSaleAssets_FairValue_debt": data.cell_value(14, 1),  # B15 15行2列公允价值可供出售权益工具
            "HoldForSaleAssets_Change_debt": data.cell_value(15, 1),  # B16 16行2列累计计入其他综合收益的公允价值变动金额可供出售权益工具
            "HoldForSaleAssets_Impairment_debt": data.cell_value(16, 1),  # B17 17行2列已计提减值金额可供出售权益工具
            "HoldForSaleAssets_Cost_equities": data.cell_value(13, 2),  # C14 14行3列权益工具的成本/债务工具的摊余成本可供出售债务工具
            "HoldForSaleAssets_FairValue_equities": data.cell_value(14, 2),  # C15 15行3列公允价值可供出售债务工具
            "HoldForSaleAssets_Change_equities": data.cell_value(15, 2),  # C16 16行3列累计计入其他综合收益的公允价值变动金额可供出售债务工具
            "HoldForSaleAssets_Impairment_equities": data.cell_value(16, 2),  # C17 17行3列已计提减值金额可供出售债务工具
            "HoldForSaleAssets_Cost_total": data.cell_value(13, 3),  # D14 14行4列权益工具的成本/债务工具的摊余成本合计
            "HoldForSaleAssets_FairValue_total": data.cell_value(14, 3),  # D15 15行4列公允价值合计
            "HoldForSaleAssets_Change_total": data.cell_value(15, 3),  # D16 16行4列累计计入其他综合收益的公允价值变动金额合计
            "HoldForSaleAssets_Impairment_total": data.cell_value(16, 3),  # D17 17行4列已计提减值金额合计
            "HoldForSaleAssets_InvesteeUnit1_last_BookBalance": data.cell_value(21, 1),  # B22 22行2列单位1期初余额
            "HoldForSaleAssets_InvesteeUnit2_last_BookBalance": data.cell_value(22, 1),  # B23 23行2列单位2期初余额
            "HoldForSaleAssets_InvesteeUnit3_last_BookBalance": data.cell_value(23, 1),  # B24 24行2列单位3期初余额
            "HoldForSaleAssets_InvesteeUnit4_last_BookBalance": data.cell_value(24, 1),  # B25 25行2列单位4期初余额
            "HoldForSaleAssets_InvesteeUnit5_last_BookBalance": data.cell_value(25, 1),  # B26 26行2列单位5期初余额
            "HoldForSaleAssets_Total_last_BookBalance": data.cell_value(26, 1),  # B27 27行2列合计期初余额
            "HoldForSaleAssets_InvesteeUnit1_add_BookBalance": data.cell_value(21, 2),  # C22 22行3列单位1本期增加
            "HoldForSaleAssets_InvesteeUnit2_add_BookBalance": data.cell_value(22, 2),  # C23 23行3列单位2本期增加
            "HoldForSaleAssets_InvesteeUnit3_add_BookBalance": data.cell_value(23, 2),  # C24 24行3列单位3本期增加
            "HoldForSaleAssets_InvesteeUnit4_add_BookBalance": data.cell_value(24, 2),  # C25 25行3列单位4本期增加
            "HoldForSaleAssets_InvesteeUnit5_add_BookBalance": data.cell_value(25, 2),  # C26 26行3列单位5本期增加
            "HoldForSaleAssets_Total_add_BookBalance": data.cell_value(26, 2),  # C27 27行3列合计本期增加
            "HoldForSaleAssets_InvesteeUnit1_reduce_BookBalance": data.cell_value(21, 3),  # D22 22行4列单位1本期减少
            "HoldForSaleAssets_InvesteeUnit2_reduce_BookBalance": data.cell_value(22, 3),  # D23 23行4列单位2本期减少
            "HoldForSaleAssets_InvesteeUnit3_reduce_BookBalance": data.cell_value(23, 3),  # D24 24行4列单位3本期减少
            "HoldForSaleAssets_InvesteeUnit4_reduce_BookBalance": data.cell_value(24, 3),  # D25 25行4列单位4本期减少
            "HoldForSaleAssets_InvesteeUnit5_reduce_BookBalance": data.cell_value(25, 3),  # D26 26行4列单位5本期减少
            "HoldForSaleAssets_Total_reduce_BookBalance": data.cell_value(26, 3),  # D27 27行4列合计本期减少
            "HoldForSaleAssets_InvesteeUnit1_this_BookBalance": data.cell_value(21, 4),  # E22 22行5列单位1期末余额
            "HoldForSaleAssets_InvesteeUnit2_this_BookBalance": data.cell_value(22, 4),  # E23 23行5列单位2期末余额
            "HoldForSaleAssets_InvesteeUnit3_this_BookBalance": data.cell_value(23, 4),  # E24 24行5列单位3期末余额
            "HoldForSaleAssets_InvesteeUnit4_this_BookBalance": data.cell_value(24, 4),  # E25 25行5列单位4期末余额
            "HoldForSaleAssets_InvesteeUnit5_this_BookBalance": data.cell_value(25, 4),  # E26 26行5列单位5期末余额
            "HoldForSaleAssets_Total_this_BookBalance": data.cell_value(26, 4),  # E27 27行5列合计期末余额
            "HoldForSaleAssets_InvesteeUnit1_last_ImpairmentLoss": data.cell_value(31, 1),  # B32 32行2列单位1期初余额
            "HoldForSaleAssets_InvesteeUnit2_last_ImpairmentLoss": data.cell_value(32, 1),  # B33 33行2列单位2期初余额
            "HoldForSaleAssets_InvesteeUnit3_last_ImpairmentLoss": data.cell_value(33, 1),  # B34 34行2列单位3期初余额
            "HoldForSaleAssets_InvesteeUnit4_last_ImpairmentLoss": data.cell_value(34, 1),  # B35 35行2列单位4期初余额
            "HoldForSaleAssets_InvesteeUnit5_last_ImpairmentLoss": data.cell_value(35, 1),  # B36 36行2列单位5期初余额
            "HoldForSaleAssets_Total_last_ImpairmentLoss": data.cell_value(36, 1),  # B37 37行2列合计期初余额
            "HoldForSaleAssets_InvesteeUnit1_add_ImpairmentLoss": data.cell_value(31, 2),  # C32 32行3列单位1本期增加
            "HoldForSaleAssets_InvesteeUnit2_add_ImpairmentLoss": data.cell_value(32, 2),  # C33 33行3列单位2本期增加
            "HoldForSaleAssets_InvesteeUnit3_add_ImpairmentLoss": data.cell_value(33, 2),  # C34 34行3列单位3本期增加
            "HoldForSaleAssets_InvesteeUnit4_add_ImpairmentLoss": data.cell_value(34, 2),  # C35 35行3列单位4本期增加
            "HoldForSaleAssets_InvesteeUnit5_add_ImpairmentLoss": data.cell_value(35, 2),  # C36 36行3列单位5本期增加
            "HoldForSaleAssets_Total_add_ImpairmentLoss": data.cell_value(36, 2),  # C37 37行3列合计本期增加
            "HoldForSaleAssets_InvesteeUnit1_reduce_ImpairmentLoss": data.cell_value(31, 3),  # D32 32行4列单位1本期减少
            "HoldForSaleAssets_InvesteeUnit2_reduce_ImpairmentLoss": data.cell_value(32, 3),  # D33 33行4列单位2本期减少
            "HoldForSaleAssets_InvesteeUnit3_reduce_ImpairmentLoss": data.cell_value(33, 3),  # D34 34行4列单位3本期减少
            "HoldForSaleAssets_InvesteeUnit4_reduce_ImpairmentLoss": data.cell_value(34, 3),  # D35 35行4列单位4本期减少
            "HoldForSaleAssets_InvesteeUnit5_reduce_ImpairmentLoss": data.cell_value(35, 3),  # D36 36行4列单位5本期减少
            "HoldForSaleAssets_Total_reduce_ImpairmentLoss": data.cell_value(36, 3),  # D37 37行4列合计本期减少
            "HoldForSaleAssets_InvesteeUnit1_this_ImpairmentLoss": data.cell_value(31, 4),  # E32 32行5列单位1期末余额
            "HoldForSaleAssets_InvesteeUnit2_this_ImpairmentLoss": data.cell_value(32, 4),  # E33 33行5列单位2期末余额
            "HoldForSaleAssets_InvesteeUnit3_this_ImpairmentLoss": data.cell_value(33, 4),  # E34 34行5列单位3期末余额
            "HoldForSaleAssets_InvesteeUnit4_this_ImpairmentLoss": data.cell_value(34, 4),  # E35 35行5列单位4期末余额
            "HoldForSaleAssets_InvesteeUnit5_this_ImpairmentLoss": data.cell_value(35, 4),  # E36 36行5列单位5期末余额
            "HoldForSaleAssets_Total_this_ImpairmentLoss": data.cell_value(36, 4),  # E37 37行5列合计期末余额
            "HoldForSaleAssets_InvesteeUnit1_ratio": data.cell_value(31, 5),  # F32 32行6列单位1在被投资单位持股比例（%）
            "HoldForSaleAssets_InvesteeUnit2_ratio": data.cell_value(32, 5),  # F33 33行6列单位2在被投资单位持股比例（%）
            "HoldForSaleAssets_InvesteeUnit3_ratio": data.cell_value(33, 5),  # F34 34行6列单位3在被投资单位持股比例（%）
            "HoldForSaleAssets_InvesteeUnit4_ratio": data.cell_value(34, 5),  # F35 35行6列单位4在被投资单位持股比例（%）
            "HoldForSaleAssets_InvesteeUnit5_ratio": data.cell_value(35, 5),  # F36 36行6列单位5在被投资单位持股比例（%）
            "HoldForSaleAssets_Total_ratio": data.cell_value(36, 5),  # F37 37行6列合计在被投资单位持股比例（%）
            "HoldForSaleAssets_InvesteeUnit1_CashBonus": data.cell_value(31, 6),  # G32 32行7列单位1本期现金红利
            "HoldForSaleAssets_InvesteeUnit2_CashBonus": data.cell_value(32, 6),  # G33 33行7列单位2本期现金红利
            "HoldForSaleAssets_InvesteeUnit3_CashBonus": data.cell_value(33, 6),  # G34 34行7列单位3本期现金红利
            "HoldForSaleAssets_InvesteeUnit4_CashBonus": data.cell_value(34, 6),  # G35 35行7列单位4本期现金红利
            "HoldForSaleAssets_InvesteeUnit5_CashBonus": data.cell_value(35, 6),  # G36 36行7列单位5本期现金红利
            "HoldForSaleAssets_Total_CashBonus": data.cell_value(36, 6),  # G37 37行7列合计本期现金红利
            "HoldForSaleAssets_InitialPlan_debt": data.cell_value(40, 1),  # B41 41行2列期初已计提减值金额可供出售权益工具
            "HoldForSaleAssets_ThisProvision_debt": data.cell_value(41, 1),  # B42 42行2列本年计提可供出售权益工具
            "HoldForSaleAssets_Into_debt": data.cell_value(42, 1),  # B43 43行2列其中：从其他综合收益转入可供出售权益工具
            "HoldForSaleAssets_ThisYearToReduce_debt": data.cell_value(43, 1),  # B44 44行2列本年减少可供出售权益工具
            "HoldForSaleAssets_Restitutio_debt": data.cell_value(44, 1),  # B45 45行2列其中：期后公允价值回升转回可供出售权益工具
            "HoldForSaleAssets_FinalPlan_debt": data.cell_value(45, 1),  # B46 46行2列期末已计提减值金额可供出售权益工具
            "HoldForSaleAssets_InitialPlan_equities": data.cell_value(40, 2),  # C41 41行3列期初已计提减值金额可供出售债务工具
            "HoldForSaleAssets_ThisProvision_equities": data.cell_value(41, 2),  # C42 42行3列本年计提可供出售债务工具
            "HoldForSaleAssets_Into_equities": data.cell_value(42, 2),  # C43 43行3列其中：从其他综合收益转入可供出售债务工具
            "HoldForSaleAssets_ThisYearToReduce_equities": data.cell_value(43, 2),  # C44 44行3列本年减少可供出售债务工具
            "HoldForSaleAssets_Restitutio_equities": data.cell_value(44, 2),  # C45 45行3列其中：期后公允价值回升转回可供出售债务工具
            "HoldForSaleAssets_FinalPlan_equities": data.cell_value(45, 2),  # C46 46行3列期末已计提减值金额可供出售债务工具
            "HoldForSaleAssets_InitialPlan_total": data.cell_value(40, 3),  # D41 41行4列期初已计提减值金额合计
            "HoldForSaleAssets_ThisProvision_total": data.cell_value(41, 3),  # D42 42行4列本年计提合计
            "HoldForSaleAssets_Into_total": data.cell_value(42, 3),  # D43 43行4列其中：从其他综合收益转入合计
            "HoldForSaleAssets_ThisYearToReduce_total": data.cell_value(43, 3),  # D44 44行4列本年减少合计
            "HoldForSaleAssets_Restitutio_total": data.cell_value(44, 3),  # D45 45行4列其中：期后公允价值回升转回合计
            "HoldForSaleAssets_FinalPlan_total": data.cell_value(45, 3),  # D46 46行4列期末已计提减值金额合计
            "HoldForSaleAssets_Project1_CostOfInvestment": data.cell_value(49, 1),  # B50 50行2列项目1投资成本
            "HoldForSaleAssets_Project2_CostOfInvestment": data.cell_value(50, 1),  # B51 51行2列项目2投资成本
            "HoldForSaleAssets_Project3_CostOfInvestment": data.cell_value(51, 1),  # B52 52行2列项目3投资成本
            "HoldForSaleAssets_Project4_CostOfInvestment": data.cell_value(52, 1),  # B53 53行2列项目4投资成本
            "HoldForSaleAssets_Project5_CostOfInvestment": data.cell_value(53, 1),  # B54 54行2列项目5投资成本
            "HoldForSaleAssets_Total_CostOfInvestment": data.cell_value(54, 1),  # B55 55行2列合计投资成本
            "HoldForSaleAssets_Project1_EndingFairValue": data.cell_value(49, 2),  # C50 50行3列项目1期末公允价值
            "HoldForSaleAssets_Project2_EndingFairValue": data.cell_value(50, 2),  # C51 51行3列项目2期末公允价值
            "HoldForSaleAssets_Project3_EndingFairValue": data.cell_value(51, 2),  # C52 52行3列项目3期末公允价值
            "HoldForSaleAssets_Project4_EndingFairValue": data.cell_value(52, 2),  # C53 53行3列项目4期末公允价值
            "HoldForSaleAssets_Project5_EndingFairValue": data.cell_value(53, 2),  # C54 54行3列项目5期末公允价值
            "HoldForSaleAssets_Total_EndingFairValue": data.cell_value(54, 2),  # C55 55行3列合计期末公允价值
            "HoldForSaleAssets_Project1_fall": data.cell_value(49, 3),  # D50 50行4列项目1公允价值相对于成本的下跌幅度（%）
            "HoldForSaleAssets_Project2_fall": data.cell_value(50, 3),  # D51 51行4列项目2公允价值相对于成本的下跌幅度（%）
            "HoldForSaleAssets_Project3_fall": data.cell_value(51, 3),  # D52 52行4列项目3公允价值相对于成本的下跌幅度（%）
            "HoldForSaleAssets_Project4_fall": data.cell_value(52, 3),  # D53 53行4列项目4公允价值相对于成本的下跌幅度（%）
            "HoldForSaleAssets_Project5_fall": data.cell_value(53, 3),  # D54 54行4列项目5公允价值相对于成本的下跌幅度（%）
            "HoldForSaleAssets_Total_fall": data.cell_value(54, 3),  # D55 55行4列合计公允价值相对于成本的下跌幅度（%）
            "HoldForSaleAssets_Project1_sum": data.cell_value(49, 5),  # F50 50行6列项目1已计提减值金额
            "HoldForSaleAssets_Project2_sum": data.cell_value(50, 5),  # F51 51行6列项目2已计提减值金额
            "HoldForSaleAssets_Project3_sum": data.cell_value(51, 5),  # F52 52行6列项目3已计提减值金额
            "HoldForSaleAssets_Project4_sum": data.cell_value(52, 5),  # F53 53行6列项目4已计提减值金额
            "HoldForSaleAssets_Project5_sum": data.cell_value(53, 5),  # F54 54行6列项目5已计提减值金额
            "HoldForSaleAssets_Total_sum": data.cell_value(54, 5),  # F55 55行6列合计已计提减值金额
            


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
        dic["HoldForSaleAssets_Remark"] = data.cell_value(56, 1),  # B57 57行2列说明
        dic["HoldForSaleAssets_Project1_time"] = data.cell_value(49, 4),  # E50 50行5列项目1持续下跌时间（月）
        dic["HoldForSaleAssets_Project2_time"] = data.cell_value(50, 4),  # E51 51行5列项目2持续下跌时间（月）
        dic["HoldForSaleAssets_Project3_time"] = data.cell_value(51, 4),  # E52 52行5列项目3持续下跌时间（月）
        dic["HoldForSaleAssets_Project4_time"] = data.cell_value(52, 4),  # E53 53行5列项目4持续下跌时间（月）
        dic["HoldForSaleAssets_Project5_time"] = data.cell_value(53, 4),  # E54 54行5列项目5持续下跌时间（月）
        dic["HoldForSaleAssets_Total_time"] = data.cell_value(54, 4),  # E55 55行5列合计持续下跌时间（月）
        dic["HoldForSaleAssets_Project1_reason"] = data.cell_value(49, 6),  # G50 50行7列项目1未计提减值原因
        dic["HoldForSaleAssets_Project2_reason"] = data.cell_value(50, 6),  # G51 51行7列项目2未计提减值原因
        dic["HoldForSaleAssets_Project3_reason"] = data.cell_value(51, 6),  # G52 52行7列项目3未计提减值原因
        dic["HoldForSaleAssets_Project4_reason"] = data.cell_value(52, 6),  # G53 53行7列项目4未计提减值原因
        dic["HoldForSaleAssets_Project5_reason"] = data.cell_value(53, 6),  # G54 54行7列项目5未计提减值原因
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
        # 可供出售金融资产情况期末余额账面余额:可供出售债务工具+可供出售权益工具+其他=合计
        if abs(df["HoldForSaleAssets_Debt_BookBalance_this"].fillna(0).values + df["HoldForSaleAssets_Equities_BookBalance_this"].fillna(0).values + df["HoldForSaleAssets_Other_BookBalance_this"].fillna(0).values - df["HoldForSaleAssets_Total_BookBalance_this"].fillna(0).values) > 0.01:
            error = "供出售金融资产情况期末余额账面余额:可供出售债务工具+可供出售权益工具+其他<>合计"
            errorlist.append(error)
        # 可供出售金融资产情况期末余额减值准备:可供出售债务工具+可供出售权益工具+其他=合计
        if abs(df["HoldForSaleAssets_Debt_ImpairmentLoss_this"].fillna(0).values + df["HoldForSaleAssets_Equities_ImpairmentLoss_this"].fillna(0).values + df["HoldForSaleAssets_Other_ImpairmentLoss_this"].fillna(0).values - df["HoldForSaleAssets_Total_ImpairmentLoss_this"].fillna(0).values) > 0.01:
            error = "供出售金融资产情况期末余额减值准备:可供出售债务工具+可供出售权益工具+其他<>合计"
            errorlist.append(error)
        # 可供出售金融资产情况期末余额账面价值:可供出售债务工具+可供出售权益工具+其他=合计
        if abs(df["HoldForSaleAssets_Debt_BookValue_this"].fillna(0).values + df["HoldForSaleAssets_Equities_BookValue_this"].fillna(0).values + df["HoldForSaleAssets_Other_BookValue_this"].fillna(0).values - df["HoldForSaleAssets_Total_BookValue_this"].fillna(0).values) > 0.01:
            error = "供出售金融资产情况期末余额账面价值:可供出售债务工具+可供出售权益工具+其他<>合计"
            errorlist.append(error)
        # 可供出售金融资产情况期初余额账面余额:可供出售债务工具+可供出售权益工具+其他=合计
        if abs(df["HoldForSaleAssets_Debt_BookBalance_last"].fillna(0).values + df["HoldForSaleAssets_Equities_BookBalance_last"].fillna(0).values + df["HoldForSaleAssets_Other_BookBalance_last"].fillna(0).values - df["HoldForSaleAssets_Total_BookBalance_last"].fillna(0).values) > 0.01:
            error = "供出售金融资产情况期初余额账面余额:可供出售债务工具+可供出售权益工具+其他<>合计"
            errorlist.append(error)
        # 可供出售金融资产情况期初余额减值准备:可供出售债务工具+可供出售权益工具+其他=合计
        if abs(df["HoldForSaleAssets_Debt_ImpairmentLoss_last"].fillna(0).values + df["HoldForSaleAssets_Equities_ImpairmentLoss_last"].fillna(0).values + df["HoldForSaleAssets_Other_ImpairmentLoss_last"].fillna(0).values - df["HoldForSaleAssets_Total_ImpairmentLoss_last"].fillna(0).values) > 0.01:
            error = "供出售金融资产情况期初余额减值准备:可供出售债务工具+可供出售权益工具+其他<>合计"
            errorlist.append(error)
        # 可供出售金融资产情况期初余额账面价值:可供出售债务工具+可供出售权益工具+其他=合计
        if abs(df["HoldForSaleAssets_Debt_BookValue_last"].fillna(0).values + df["HoldForSaleAssets_Equities_BookValue_last"].fillna(0).values + df["HoldForSaleAssets_Other_BookValue_last"].fillna(0).values - df["HoldForSaleAssets_Total_BookValue_last"].fillna(0).values) > 0.01:
            error = "供出售金融资产情况期初余额账面价值:可供出售债务工具+可供出售权益工具+其他<>合计"
            errorlist.append(error)
        # 权益工具的成本/债务工具的摊余成本：可供出售债务工具+可供出售权益工具=合计
        if abs(df["HoldForSaleAssets_Cost_debt"].fillna(0).values + df["HoldForSaleAssets_Cost_equities"].fillna(0).values - df["HoldForSaleAssets_Cost_total"].fillna(0).values) > 0.01:
            error = "权益工具的成本/债务工具的摊余成本：可供出售债务工具+可供出售权益工具<>合计"
            errorlist.append(error)
        # 公允价值：可供出售债务工具+可供出售权益工具=合计
        if abs(df["HoldForSaleAssets_FairValue_debt"].fillna(0).values + df["HoldForSaleAssets_FairValue_equities"].fillna(0).values - df["HoldForSaleAssets_FairValue_total"].fillna(0).values) > 0.01:
            error = "公允价值：可供出售债务工具+可供出售权益工具<>合计"
            errorlist.append(error)
        # 累计计入其他综合收益的公允价值变动金额：可供出售债务工具+可供出售权益工具=合计
        if abs(df["HoldForSaleAssets_Change_debt"].fillna(0).values + df["HoldForSaleAssets_Change_equities"].fillna(0).values - df["HoldForSaleAssets_Change_total"].fillna(0).values) > 0.01:
            error = "累计计入其他综合收益的公允价值变动金额：可供出售债务工具+可供出售权益工具<>合计"
            errorlist.append(error)
        # 已计提减值金额：可供出售债务工具+可供出售权益工具=合计
        if abs(df["HoldForSaleAssets_Impairment_debt"].fillna(0).values + df["HoldForSaleAssets_Impairment_equities"].fillna(0).values - df["HoldForSaleAssets_Impairment_total"].fillna(0).values) > 0.01:
            error = "已计提减值金额：可供出售债务工具+可供出售权益工具<>合计"
            errorlist.append(error)
        # 期末按成本计量的可供出售金融资产账面余额期初余额：单位1+单位+单位3+单位4+单位5=合计
        if abs(df["HoldForSaleAssets_InvesteeUnit1_last_BookBalance"].fillna(0).values + df["HoldForSaleAssets_InvesteeUnit2_last_BookBalance"].fillna(0).values + df["HoldForSaleAssets_InvesteeUnit3_last_BookBalance"].fillna(0).values + df["HoldForSaleAssets_InvesteeUnit4_last_BookBalance"].fillna(0).values + df["HoldForSaleAssets_InvesteeUnit5_last_BookBalance"].fillna(0).values - df["HoldForSaleAssets_Total_last_BookBalance"].fillna(0).values) > 0.01:
            error = "期末按成本计量的可供出售金融资产账面余额期初余额：单位1+单位+单位3+单位4+单位5<>合计"
            errorlist.append(error)
        # 期末按成本计量的可供出售金融资产账面余额本期增加：单位1+单位+单位3+单位4+单位5=合计
        if abs(df["HoldForSaleAssets_InvesteeUnit1_add_BookBalance"].fillna(0).values + df["HoldForSaleAssets_InvesteeUnit2_add_BookBalance"].fillna(0).values + df["HoldForSaleAssets_InvesteeUnit3_add_BookBalance"].fillna(0).values + df["HoldForSaleAssets_InvesteeUnit4_add_BookBalance"].fillna(0).values + df["HoldForSaleAssets_InvesteeUnit5_add_BookBalance"].fillna(0).values - df["HoldForSaleAssets_Total_add_BookBalance"].fillna(0).values) > 0.01:
            error = "期末按成本计量的可供出售金融资产账面余额本期增加：单位1+单位+单位3+单位4+单位5<>合计"
            errorlist.append(error)
        # 期末按成本计量的可供出售金融资产账面余额本期减少：单位1+单位+单位3+单位4+单位5=合计
        if abs(df["HoldForSaleAssets_InvesteeUnit1_reduce_BookBalance"].fillna(0).values + df["HoldForSaleAssets_InvesteeUnit2_reduce_BookBalance"].fillna(0).values + df["HoldForSaleAssets_InvesteeUnit3_reduce_BookBalance"].fillna(0).values + df["HoldForSaleAssets_InvesteeUnit4_reduce_BookBalance"].fillna(0).values + df["HoldForSaleAssets_InvesteeUnit5_reduce_BookBalance"].fillna(0).values - df["HoldForSaleAssets_Total_reduce_BookBalance"].fillna(0).values) > 0.01:
            error = "期末按成本计量的可供出售金融资产账面余额本期减少：单位1+单位+单位3+单位4+单位5<>合计"
            errorlist.append(error)
        # 期末按成本计量的可供出售金融资产账面余额期末余额：单位1+单位+单位3+单位4+单位5=合计
        if abs(df["HoldForSaleAssets_InvesteeUnit1_this_BookBalance"].fillna(0).values + df["HoldForSaleAssets_InvesteeUnit2_this_BookBalance"].fillna(0).values + df["HoldForSaleAssets_InvesteeUnit3_this_BookBalance"].fillna(0).values + df["HoldForSaleAssets_InvesteeUnit4_this_BookBalance"].fillna(0).values + df["HoldForSaleAssets_InvesteeUnit5_this_BookBalance"].fillna(0).values - df["HoldForSaleAssets_Total_this_BookBalance"].fillna(0).values) > 0.01:
            error = "期末按成本计量的可供出售金融资产账面余额期末余额：单位1+单位+单位3+单位4+单位5<>合计"
            errorlist.append(error)
        # 期末按成本计量的可供出售金融资产减值准备期初余额：单位1+单位+单位3+单位4+单位5=合计
        if abs(df["HoldForSaleAssets_InvesteeUnit1_last_ImpairmentLoss"].fillna(0).values + df["HoldForSaleAssets_InvesteeUnit2_last_ImpairmentLoss"].fillna(0).values + df["HoldForSaleAssets_InvesteeUnit3_last_ImpairmentLoss"].fillna(0).values + df["HoldForSaleAssets_InvesteeUnit4_last_ImpairmentLoss"].fillna(0).values + df["HoldForSaleAssets_InvesteeUnit5_last_ImpairmentLoss"].fillna(0).values - df["HoldForSaleAssets_Total_last_ImpairmentLoss"].fillna(0).values) > 0.01:
            error = "期末按成本计量的可供出售金融资产减值准备期初余额：单位1+单位+单位3+单位4+单位5<>合计"
            errorlist.append(error)
        # 期末按成本计量的可供出售金融资产减值准备本期增加：单位1+单位+单位3+单位4+单位5=合计
        if abs(df["HoldForSaleAssets_InvesteeUnit1_add_ImpairmentLoss"].fillna(0).values + df["HoldForSaleAssets_InvesteeUnit2_add_ImpairmentLoss"].fillna(0).values + df["HoldForSaleAssets_InvesteeUnit3_add_ImpairmentLoss"].fillna(0).values + df["HoldForSaleAssets_InvesteeUnit4_add_ImpairmentLoss"].fillna(0).values + df["HoldForSaleAssets_InvesteeUnit5_add_ImpairmentLoss"].fillna(0).values - df["HoldForSaleAssets_Total_add_ImpairmentLoss"].fillna(0).values) > 0.01:
            error = "期末按成本计量的可供出售金融资产减值准备本期增加：单位1+单位+单位3+单位4+单位5<>合计"
            errorlist.append(error)
        # 期末按成本计量的可供出售金融资产减值准备本期减少：单位1+单位+单位3+单位4+单位5=合计
        if abs(df["HoldForSaleAssets_InvesteeUnit1_reduce_ImpairmentLoss"].fillna(0).values + df["HoldForSaleAssets_InvesteeUnit2_reduce_ImpairmentLoss"].fillna(0).values + df["HoldForSaleAssets_InvesteeUnit3_reduce_ImpairmentLoss"].fillna(0).values + df["HoldForSaleAssets_InvesteeUnit4_reduce_ImpairmentLoss"].fillna(0).values + df["HoldForSaleAssets_InvesteeUnit5_reduce_ImpairmentLoss"].fillna(0).values - df["HoldForSaleAssets_Total_reduce_ImpairmentLoss"].fillna(0).values) > 0.01:
            error = "期末按成本计量的可供出售金融资产减值准备本期减少：单位1+单位+单位3+单位4+单位5<>合计"
            errorlist.append(error)
        # 期末按成本计量的可供出售金融资产减值准备期末余额：单位1+单位+单位3+单位4+单位5=合计
        if abs(df["HoldForSaleAssets_InvesteeUnit1_this_ImpairmentLoss"].fillna(0).values + df["HoldForSaleAssets_InvesteeUnit2_this_ImpairmentLoss"].fillna(0).values + df["HoldForSaleAssets_InvesteeUnit3_this_ImpairmentLoss"].fillna(0).values + df["HoldForSaleAssets_InvesteeUnit4_this_ImpairmentLoss"].fillna(0).values + df["HoldForSaleAssets_InvesteeUnit5_this_ImpairmentLoss"].fillna(0).values - df["HoldForSaleAssets_Total_this_ImpairmentLoss"].fillna(0).values) > 0.01:
            error = "期末按成本计量的可供出售金融资产减值准备期末余额：单位1+单位+单位3+单位4+单位5<>合计"
            errorlist.append(error)
        # 期末按成本计量的可供出售金融资产本期现金红利：单位1+单位+单位3+单位4+单位5=合计
        if abs(df["HoldForSaleAssets_InvesteeUnit1_CashBonus"].fillna(0).values + df["HoldForSaleAssets_InvesteeUnit2_CashBonus"].fillna(0).values + df["HoldForSaleAssets_InvesteeUnit3_CashBonus"].fillna(0).values + df["HoldForSaleAssets_InvesteeUnit4_CashBonus"].fillna(0).values + df["HoldForSaleAssets_InvesteeUnit5_CashBonus"].fillna(0).values - df["HoldForSaleAssets_Total_CashBonus"].fillna(0).values) > 0.01:
            error = "期末按成本计量的可供出售金融资产本期现金红利：单位1+单位+单位3+单位4+单位5<>合计"
            errorlist.append(error)
        # 期初已计提减值金额：可供出售债务工具+可供出售权益工具=合计
        if abs(df["HoldForSaleAssets_InitialPlan_debt"].fillna(0).values + df["HoldForSaleAssets_InitialPlan_equities"].fillna(0).values - df["HoldForSaleAssets_InitialPlan_total"].fillna(0).values) > 0.01:
            error = "期初已计提减值金额：可供出售债务工具+可供出售权益工具<>合计"
            errorlist.append(error)
        # 本年计提：可供出售债务工具+可供出售权益工具=合计
        if abs(df["HoldForSaleAssets_ThisProvision_debt"].fillna(0).values + df["HoldForSaleAssets_ThisProvision_equities"].fillna(0).values - df["HoldForSaleAssets_ThisProvision_total"].fillna(0).values) > 0.01:
            error = "本年计提：可供出售债务工具+可供出售权益工具<>合计"
            errorlist.append(error)
        # 其中，从其他综合收益转入：可供出售债务工具+可供出售权益工具=合计
        if abs(df["HoldForSaleAssets_Into_debt"].fillna(0).values + df["HoldForSaleAssets_Into_equities"].fillna(0).values - df["HoldForSaleAssets_Into_total"].fillna(0).values) > 0.01:
            error = "其中，从其他综合收益转入：可供出售债务工具+可供出售权益工具<>合计"
            errorlist.append(error)
        # 本年减少：可供出售债务工具+可供出售权益工具=合计
        if abs(df["HoldForSaleAssets_ThisYearToReduce_debt"].fillna(0).values + df["HoldForSaleAssets_ThisYearToReduce_equities"].fillna(0).values - df["HoldForSaleAssets_ThisYearToReduce_total"].fillna(0).values) > 0.01:
            error = "本年减少：可供出售债务工具+可供出售权益工具<>合计"
            errorlist.append(error)
        # 其中，期后公允价值回升转回：可供出售债务工具+可供出售权益工具=合计
        if abs(df["HoldForSaleAssets_Restitutio_debt"].fillna(0).values + df["HoldForSaleAssets_Restitutio_equities"].fillna(0).values - df["HoldForSaleAssets_Restitutio_total"].fillna(0).values) > 0.01:
            error = "其中，期后公允价值回升转回：可供出售债务工具+可供出售权益工具<>合计"
            errorlist.append(error)
        # 期末已计提减值金额：可供出售债务工具+可供出售权益工具=合计
        if abs(df["HoldForSaleAssets_FinalPlan_debt"].fillna(0).values + df["HoldForSaleAssets_FinalPlan_equities"].fillna(0).values - df["HoldForSaleAssets_FinalPlan_total"].fillna(0).values) > 0.01:
            error = "期末已计提减值金额：可供出售债务工具+可供出售权益工具<>合计"
            errorlist.append(error)
        # 投资成本:项目1+项目2+项目3+项目4+项目5=合计
        if abs(df["HoldForSaleAssets_Project1_CostOfInvestment"].fillna(0).values + df["HoldForSaleAssets_Project2_CostOfInvestment"].fillna(0).values + df["HoldForSaleAssets_Project3_CostOfInvestment"].fillna(0).values + df["HoldForSaleAssets_Project4_CostOfInvestment"].fillna(0).values + df["HoldForSaleAssets_Project5_CostOfInvestment"].fillna(0).values - df["HoldForSaleAssets_Total_CostOfInvestment"].fillna(0).values) > 0.01:
            error = "投资成本:项目1+项目2+项目3+项目4+项目5<>合计"
            errorlist.append(error)
        # 期末公允价值:项目1+项目2+项目3+项目4+项目5=合计
        if abs(df["HoldForSaleAssets_Project1_EndingFairValue"].fillna(0).values + df["HoldForSaleAssets_Project2_EndingFairValue"].fillna(0).values + df["HoldForSaleAssets_Project3_EndingFairValue"].fillna(0).values + df["HoldForSaleAssets_Project4_EndingFairValue"].fillna(0).values + df["HoldForSaleAssets_Project5_EndingFairValue"].fillna(0).values - df["HoldForSaleAssets_Total_EndingFairValue"].fillna(0).values) > 0.01:
            error = "期末公允价值:项目1+项目2+项目3+项目4+项目5<>合计"
            errorlist.append(error)
        # 公允价值相对于成本的下跌幅度:项目1+项目2+项目3+项目4+项目5=合计
        if abs(df["HoldForSaleAssets_Project1_fall"].fillna(0).values + df["HoldForSaleAssets_Project2_fall"].fillna(0).values + df["HoldForSaleAssets_Project3_fall"].fillna(0).values + df["HoldForSaleAssets_Project4_fall"].fillna(0).values + df["HoldForSaleAssets_Project5_fall"].fillna(0).values - df["HoldForSaleAssets_Total_fall"].fillna(0).values) > 0.01:
            error = "公允价值相对于成本的下跌幅度:项目1+项目2+项目3+项目4+项目5<>合计"
            errorlist.append(error)
        # 已计提减值金额:项目1+项目2+项目3+项目4+项目5=合计
        if abs(df["HoldForSaleAssets_Project1_sum"].fillna(0).values + df["HoldForSaleAssets_Project2_sum"].fillna(0).values + df["HoldForSaleAssets_Project3_sum"].fillna(0).values + df["HoldForSaleAssets_Project4_sum"].fillna(0).values + df["HoldForSaleAssets_Project5_sum"].fillna(0).values - df["HoldForSaleAssets_Total_sum"].fillna(0).values) > 0.01:
            error = "已计提减值金额:项目1+项目2+项目3+项目4+项目5<>合计"
            errorlist.append(error)

        return df, errorlist

