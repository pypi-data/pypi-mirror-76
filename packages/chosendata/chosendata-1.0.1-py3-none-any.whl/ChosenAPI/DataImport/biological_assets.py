
import pandas as pd
from ChosenAPI.DataImport.ChangeToNum import ChangeData



class GetBiologicalAssets(object):#生产性生物资产
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
            "BiologicalAssets_LastOBV_farming": data.cell_value(4, 1),  # B5 5行2列1.期初余额种植业
            "BiologicalAssets_AddOBV_farming": data.cell_value(5, 1),  # B6 6行2列2.本期增加金额种植业
            "BiologicalAssets_PurchaseOBV_farming": data.cell_value(6, 1),  # B7 7行2列⑴外购种植业
            "BiologicalAssets_CultivateOBV_farming": data.cell_value(7, 1),  # B8 8行2列⑵自行培育种植业
            "BiologicalAssets_MergeOBV_farming": data.cell_value(8, 1),  # B9 9行2列⑶企业合并增加种植业
            "BiologicalAssets_ReduceOBV_farming": data.cell_value(9, 1),  # B10 10行2列3.本期减少金额种植业
            "BiologicalAssets_DisposalOBV_farming": data.cell_value(10, 1),  # B11 11行2列⑴处置种植业
            "BiologicalAssets_CReduceOBV_farming": data.cell_value(11, 1),# B12 12行2列⑵企业合并减少种植业
            "BiologicalAssets_ThisOBV_farming": data.cell_value(12, 1),  # B13 13行2列4.期末余额种植业
            "BiologicalAssets_LastAD_farming": data.cell_value(14, 1),  # B15 15行2列1.期初余额种植业
            "BiologicalAssets_AddAD_farming": data.cell_value(15, 1),  # B16 16行2列2.本期增加金额种植业
            "BiologicalAssets_AmortizationAD_farming": data.cell_value(16, 1),# B17 17行2列     ⑴计提种植业
            "BiologicalAssets_MergeAD_farming": data.cell_value(17, 1),# B18 18行2列     ⑵企业合并增加种植业
            "BiologicalAssets_ReduceAD_farming": data.cell_value(18, 1),  # B19 19行2列3.本期减少金额种植业
            "BiologicalAssets_DisposalAD_farming": data.cell_value(19, 1),  # B20 20行2列     ⑴处置种植业
            "BiologicalAssets_CReduceAD_farming": data.cell_value(20, 1),# B21 21行2列     ⑵企业合并减少种植业
            "BiologicalAssets_ThisAD_farming": data.cell_value(21, 1),  # B22 22行2列4.期末余额种植业
            "BiologicalAssets_LastIL_farming": data.cell_value(23, 1),  # B24 24行2列1.期初余额种植业
            "BiologicalAssets_AddIL_farming": data.cell_value(24, 1),  # B25 25行2列2.本期增加金额种植业
            "BiologicalAssets_AmortizationIL_farming": data.cell_value(25, 1),  # B26 26行2列⑴计提种植业
            "BiologicalAssets_MergeIL_farming": data.cell_value(26, 1),  # B27 27行2列⑵企业合并增加种植业
            "BiologicalAssets_ReduceIL_farming": data.cell_value(27, 1),  # B28 28行2列3.本期减少金额种植业
            "BiologicalAssets_DisposalIL_farming": data.cell_value(28, 1),  # B29 29行2列⑴处置种植业
            "BiologicalAssets_CReduceIL_farming": data.cell_value(29, 1),  # B30 30行2列⑵企业合并减少种植业
            "BiologicalAssets_ThisIL_farming": data.cell_value(30, 1),  # B31 31行2列4.期末余额种植业
            "BiologicalAssets_EBV_farming": data.cell_value(32, 1),  # B33 33行2列1.期末账面价值种植业
            "BiologicalAssets_OBV_farming": data.cell_value(33, 1),  # B34 34行2列2.期初账面价值种植业
            "BiologicalAssets_Last_farming": data.cell_value(37, 1),  # B38 38行2列一、期初余额种植业
            "BiologicalAssets_Change_farming": data.cell_value(38, 1),  # B39 39行2列二、本期变动种植业
            "BiologicalAssets_Purchase_farming": data.cell_value(39, 1),  # B40 40行2列加：外购种植业
            "BiologicalAssets_Cultivate_farming": data.cell_value(40, 1),  # B41 41行2列自行培育种植业
            "BiologicalAssets_Merge_farming": data.cell_value(41, 1),  # B42 42行2列企业合并增加种植业
            "BiologicalAssets_Disposal_farming": data.cell_value(42, 1),  # B43 43行2列减：处置种植业
            "BiologicalAssets_Transfer_farming": data.cell_value(43, 1),  # B44 44行2列其他转出种植业
            "BiologicalAssets_FChange_farming": data.cell_value(44, 1),  # B45 45行2列公允价值变动种植业
            "BiologicalAssets_This_farming": data.cell_value(45, 1),  # B46 46行2列三、期末余额种植业
            "BiologicalAssets_LastOBV_husbandry": data.cell_value(4, 2),  # C5 5行3列1.期初余额畜牧养殖业
            "BiologicalAssets_AddOBV_husbandry": data.cell_value(5, 2),  # C6 6行3列2.本期增加金额畜牧养殖业
            "BiologicalAssets_PurchaseOBV_husbandry": data.cell_value(6, 2),  # C7 7行3列⑴外购畜牧养殖业
            "BiologicalAssets_CultivateOBV_husbandry": data.cell_value(7, 2),  # C8 8行3列⑵自行培育畜牧养殖业
            "BiologicalAssets_MergeOBV_husbandry": data.cell_value(8, 2),  # C9 9行3列⑶企业合并增加畜牧养殖业
            "BiologicalAssets_ReduceOBV_husbandry": data.cell_value(9, 2),  # C10 10行3列3.本期减少金额畜牧养殖业
            "BiologicalAssets_DisposalOBV_husbandry": data.cell_value(10, 2),  # C11 11行3列⑴处置畜牧养殖业
            "BiologicalAssets_CReduceOBV_husbandry": data.cell_value(11, 2),# C12 12行3列⑵企业合并减少畜牧养殖业
            "BiologicalAssets_ThisOBV_husbandry": data.cell_value(12, 2),  # C13 13行3列4.期末余额畜牧养殖业
            "BiologicalAssets_LastAD_husbandry": data.cell_value(14, 2),  # C15 15行3列1.期初余额畜牧养殖业
            "BiologicalAssets_AddAD_husbandry": data.cell_value(15, 2),  # C16 16行3列2.本期增加金额畜牧养殖业
            "BiologicalAssets_AmortizationAD_husbandry": data.cell_value(16, 2),# C17 17行3列     ⑴计提畜牧养殖业
            "BiologicalAssets_MergeAD_husbandry": data.cell_value(17, 2),# C18 18行3列     ⑵企业合并增加畜牧养殖业
            "BiologicalAssets_ReduceAD_husbandry": data.cell_value(18, 2),# C19 19行3列3.本期减少金额畜牧养殖业
            "BiologicalAssets_DisposalAD_husbandry": data.cell_value(19, 2),# C20 20行3列     ⑴处置畜牧养殖业
            "BiologicalAssets_CReduceAD_husbandry": data.cell_value(20, 2),# C21 21行3列     ⑵企业合并减少畜牧养殖业
            "BiologicalAssets_ThisAD_husbandry": data.cell_value(21, 2),  # C22 22行3列4.期末余额畜牧养殖业
            "BiologicalAssets_LastIL_husbandry": data.cell_value(23, 2),  # C24 24行3列1.期初余额畜牧养殖业
            "BiologicalAssets_AddIL_husbandry": data.cell_value(24, 2),  # C25 25行3列2.本期增加金额畜牧养殖业
            "BiologicalAssets_AmortizationIL_husbandry": data.cell_value(25, 2),  # C26 26行3列⑴计提畜牧养殖业
            "BiologicalAssets_MergeIL_husbandry": data.cell_value(26, 2),  # C27 27行3列⑵企业合并增加畜牧养殖业
            "BiologicalAssets_ReduceIL_husbandry": data.cell_value(27, 2),  # C28 28行3列3.本期减少金额畜牧养殖业
            "BiologicalAssets_DisposalIL_husbandry": data.cell_value(28, 2),  # C29 29行3列⑴处置畜牧养殖业
            "BiologicalAssets_CReduceIL_husbandry": data.cell_value(29, 2),# C30 30行3列⑵企业合并减少畜牧养殖业
            "BiologicalAssets_ThisIL_husbandry": data.cell_value(30, 2),  # C31 31行3列4.期末余额畜牧养殖业
            "BiologicalAssets_EBV_husbandry": data.cell_value(32, 2),  # C33 33行3列1.期末账面价值畜牧养殖业
            "BiologicalAssets_OBV_husbandry": data.cell_value(33, 2),  # C34 34行3列2.期初账面价值畜牧养殖业
            "BiologicalAssets_Last_husbandry": data.cell_value(37, 2),  # C38 38行3列一、期初余额畜牧养殖业
            "BiologicalAssets_Change_husbandry": data.cell_value(38, 2),  # C39 39行3列二、本期变动畜牧养殖业
            "BiologicalAssets_Purchase_husbandry": data.cell_value(39, 2),  # C40 40行3列加：外购畜牧养殖业
            "BiologicalAssets_Cultivate_husbandry": data.cell_value(40, 2),  # C41 41行3列自行培育畜牧养殖业
            "BiologicalAssets_Merge_husbandry": data.cell_value(41, 2),  # C42 42行3列企业合并增加畜牧养殖业
            "BiologicalAssets_Disposal_husbandry": data.cell_value(42, 2),  # C43 43行3列减：处置畜牧养殖业
            "BiologicalAssets_Transfer_husbandry": data.cell_value(43, 2),  # C44 44行3列其他转出畜牧养殖业
            "BiologicalAssets_FChange_husbandry": data.cell_value(44, 2),  # C45 45行3列公允价值变动畜牧养殖业
            "BiologicalAssets_This_husbandry": data.cell_value(45, 2),  # C46 46行3列三、期末余额畜牧养殖业
            "BiologicalAssets_LastOBV_forestry": data.cell_value(4, 3),  # D5 5行4列1.期初余额林业
            "BiologicalAssets_AddOBV_forestry": data.cell_value(5, 3),  # D6 6行4列2.本期增加金额林业
            "BiologicalAssets_PurchaseOBV_forestry": data.cell_value(6, 3),  # D7 7行4列⑴外购林业
            "BiologicalAssets_CultivateOBV_forestry": data.cell_value(7, 3),  # D8 8行4列⑵自行培育林业
            "BiologicalAssets_MergeOBV_forestry": data.cell_value(8, 3),  # D9 9行4列⑶企业合并增加林业
            "BiologicalAssets_ReduceOBV_forestry": data.cell_value(9, 3),  # D10 10行4列3.本期减少金额林业
            "BiologicalAssets_DisposalOBV_forestry": data.cell_value(10, 3),  # D11 11行4列⑴处置林业
            "BiologicalAssets_CReduceOBV_forestry": data.cell_value(11, 3),# D12 12行4列⑵企业合并减少林业
            "BiologicalAssets_ThisOBV_forestry": data.cell_value(12, 3),  # D13 13行4列4.期末余额林业
            "BiologicalAssets_LastAD_forestry": data.cell_value(14, 3),  # D15 15行4列1.期初余额林业
            "BiologicalAssets_AddAD_forestry": data.cell_value(15, 3),  # D16 16行4列2.本期增加金额林业
            "BiologicalAssets_AmortizationAD_forestry": data.cell_value(16, 3),# D17 17行4列     ⑴计提林业
            "BiologicalAssets_MergeAD_forestry": data.cell_value(17, 3),# D18 18行4列     ⑵企业合并增加林业
            "BiologicalAssets_ReduceAD_forestry": data.cell_value(18, 3),  # D19 19行4列3.本期减少金额林业
            "BiologicalAssets_DisposalAD_forestry": data.cell_value(19, 3),  # D20 20行4列     ⑴处置林业
            "BiologicalAssets_CReduceAD_forestry": data.cell_value(20, 3),# D21 21行4列     ⑵企业合并减少林业
            "BiologicalAssets_ThisAD_forestry": data.cell_value(21, 3),  # D22 22行4列4.期末余额林业
            "BiologicalAssets_LastIL_forestry": data.cell_value(23, 3),  # D24 24行4列1.期初余额林业
            "BiologicalAssets_AddIL_forestry": data.cell_value(24, 3),  # D25 25行4列2.本期增加金额林业
            "BiologicalAssets_AmortizationIL_forestry": data.cell_value(25, 3),  # D26 26行4列⑴计提林业
            "BiologicalAssets_MergeIL_forestry": data.cell_value(26, 3),  # D27 27行4列⑵企业合并增加林业
            "BiologicalAssets_ReduceIL_forestry": data.cell_value(27, 3),  # D28 28行4列3.本期减少金额林业
            "BiologicalAssets_DisposalIL_forestry": data.cell_value(28, 3),  # D29 29行4列⑴处置林业
            "BiologicalAssets_CReduceIL_forestry": data.cell_value(29, 3),  # D30 30行4列⑵企业合并减少林业
            "BiologicalAssets_ThisIL_forestry": data.cell_value(30, 3),  # D31 31行4列4.期末余额林业
            "BiologicalAssets_EBV_forestry": data.cell_value(32, 3),  # D33 33行4列1.期末账面价值林业
            "BiologicalAssets_OBV_forestry": data.cell_value(33, 3),  # D34 34行4列2.期初账面价值林业
            "BiologicalAssets_Last_forestry": data.cell_value(37, 3),  # D38 38行4列一、期初余额林业
            "BiologicalAssets_Change_forestry": data.cell_value(38, 3),  # D39 39行4列二、本期变动林业
            "BiologicalAssets_Purchase_forestry": data.cell_value(39, 3),  # D40 40行4列加：外购林业
            "BiologicalAssets_Cultivate_forestry": data.cell_value(40, 3),  # D41 41行4列自行培育林业
            "BiologicalAssets_Merge_forestry": data.cell_value(41, 3),  # D42 42行4列企业合并增加林业
            "BiologicalAssets_Disposal_forestry": data.cell_value(42, 3),  # D43 43行4列减：处置林业
            "BiologicalAssets_Transfer_forestry": data.cell_value(43, 3),  # D44 44行4列其他转出林业
            "BiologicalAssets_FChange_forestry": data.cell_value(44, 3),  # D45 45行4列公允价值变动林业
            "BiologicalAssets_This_forestry": data.cell_value(45, 3),  # D46 46行4列三、期末余额林业
            "BiologicalAssets_LastOBV_aquaculture": data.cell_value(4, 4),  # E5 5行5列1.期初余额水产业
            "BiologicalAssets_AddOBV_aquaculture": data.cell_value(5, 4),  # E6 6行5列2.本期增加金额水产业
            "BiologicalAssets_PurchaseOBV_aquaculture": data.cell_value(6, 4),  # E7 7行5列⑴外购水产业
            "BiologicalAssets_CultivateOBV_aquaculture": data.cell_value(7, 4),  # E8 8行5列⑵自行培育水产业
            "BiologicalAssets_MergeOBV_aquaculture": data.cell_value(8, 4),  # E9 9行5列⑶企业合并增加水产业
            "BiologicalAssets_ReduceOBV_aquaculture": data.cell_value(9, 4),  # E10 10行5列3.本期减少金额水产业
            "BiologicalAssets_DisposalOBV_aquaculture": data.cell_value(10, 4),  # E11 11行5列⑴处置水产业
            "BiologicalAssets_CReduceOBV_aquaculture": data.cell_value(11, 4),# E12 12行5列⑵企业合并减少水产业
            "BiologicalAssets_ThisOBV_aquaculture": data.cell_value(12, 4),  # E13 13行5列4.期末余额水产业
            "BiologicalAssets_LastAD_aquaculture": data.cell_value(14, 4),  # E15 15行5列1.期初余额水产业
            "BiologicalAssets_AddAD_aquaculture": data.cell_value(15, 4),  # E16 16行5列2.本期增加金额水产业
            "BiologicalAssets_AmortizationAD_aquaculture": data.cell_value(16, 4),# E17 17行5列     ⑴计提水产业
            "BiologicalAssets_MergeAD_aquaculture": data.cell_value(17, 4),# E18 18行5列     ⑵企业合并增加水产业
            "BiologicalAssets_ReduceAD_aquaculture": data.cell_value(18, 4),# E19 19行5列3.本期减少金额水产业
            "BiologicalAssets_DisposalAD_aquaculture": data.cell_value(19, 4),# E20 20行5列     ⑴处置水产业
            "BiologicalAssets_CReduceAD_aquaculture": data.cell_value(20, 4),# E21 21行5列     ⑵企业合并减少水产业
            "BiologicalAssets_ThisAD_aquaculture": data.cell_value(21, 4),  # E22 22行5列4.期末余额水产业
            "BiologicalAssets_LastIL_aquaculture": data.cell_value(23, 4),  # E24 24行5列1.期初余额水产业
            "BiologicalAssets_AddIL_aquaculture": data.cell_value(24, 4),  # E25 25行5列2.本期增加金额水产业
            "BiologicalAssets_AmortizationIL_aquaculture": data.cell_value(25, 4),  # E26 26行5列⑴计提水产业
            "BiologicalAssets_MergeIL_aquaculture": data.cell_value(26, 4),  # E27 27行5列⑵企业合并增加水产业
            "BiologicalAssets_ReduceIL_aquaculture": data.cell_value(27, 4),  # E28 28行5列3.本期减少金额水产业
            "BiologicalAssets_DisposalIL_aquaculture": data.cell_value(28, 4),  # E29 29行5列⑴处置水产业
            "BiologicalAssets_CReduceIL_aquaculture": data.cell_value(29, 4),# E30 30行5列⑵企业合并减少水产业
            "BiologicalAssets_ThisIL_aquaculture": data.cell_value(30, 4),  # E31 31行5列4.期末余额水产业
            "BiologicalAssets_EBV_aquaculture": data.cell_value(32, 4),  # E33 33行5列1.期末账面价值水产业
            "BiologicalAssets_OBV_aquaculture": data.cell_value(33, 4),  # E34 34行5列2.期初账面价值水产业
            "BiologicalAssets_Last_aquaculture": data.cell_value(37, 4),  # E38 38行5列一、期初余额水产业
            "BiologicalAssets_Change_aquaculture": data.cell_value(38, 4),  # E39 39行5列二、本期变动水产业
            "BiologicalAssets_Purchase_aquaculture": data.cell_value(39, 4),  # E40 40行5列加：外购水产业
            "BiologicalAssets_Cultivate_aquaculture": data.cell_value(40, 4),  # E41 41行5列自行培育水产业
            "BiologicalAssets_Merge_aquaculture": data.cell_value(41, 4),  # E42 42行5列企业合并增加水产业
            "BiologicalAssets_Disposal_aquaculture": data.cell_value(42, 4),  # E43 43行5列减：处置水产业
            "BiologicalAssets_Transfer_aquaculture": data.cell_value(43, 4),  # E44 44行5列其他转出水产业
            "BiologicalAssets_FChange_aquaculture": data.cell_value(44, 4),  # E45 45行5列公允价值变动水产业
            "BiologicalAssets_This_aquaculture": data.cell_value(45, 4),  # E46 46行5列三、期末余额水产业
            "BiologicalAssets_LastOBV_total": data.cell_value(4, 5),  # F5 5行6列1.期初余额合计
            "BiologicalAssets_AddOBV_total": data.cell_value(5, 5),  # F6 6行6列2.本期增加金额合计
            "BiologicalAssets_PurchaseOBV_total": data.cell_value(6, 5),  # F7 7行6列⑴外购合计
            "BiologicalAssets_CultivateOBV_total": data.cell_value(7, 5),  # F8 8行6列⑵自行培育合计
            "BiologicalAssets_MergeOBV_total": data.cell_value(8, 5),  # F9 9行6列⑶企业合并增加合计
            "BiologicalAssets_ReduceOBV_total": data.cell_value(9, 5),  # F10 10行6列3.本期减少金额合计
            "BiologicalAssets_DisposalOBV_total": data.cell_value(10, 5),  # F11 11行6列⑴处置合计
            "BiologicalAssets_CReduceOBV_total": data.cell_value(11, 5),  # F12 12行6列⑵企业合并减少合计
            "BiologicalAssets_ThisOBV_total": data.cell_value(12, 5),  # F13 13行6列4.期末余额合计
            "BiologicalAssets_LastAD_total": data.cell_value(14, 5),  # F15 15行6列1.期初余额合计
            "BiologicalAssets_AddAD_total": data.cell_value(15, 5),  # F16 16行6列2.本期增加金额合计
            "BiologicalAssets_AmortizationAD_total": data.cell_value(16, 5),# F17 17行6列     ⑴计提合计
            "BiologicalAssets_MergeAD_total": data.cell_value(17, 5),  # F18 18行6列     ⑵企业合并增加合计
            "BiologicalAssets_ReduceAD_total": data.cell_value(18, 5),  # F19 19行6列3.本期减少金额合计
            "BiologicalAssets_DisposalAD_total": data.cell_value(19, 5),  # F20 20行6列     ⑴处置合计
            "BiologicalAssets_CReduceAD_total": data.cell_value(20, 5),# F21 21行6列     ⑵企业合并减少合计
            "BiologicalAssets_ThisAD_total": data.cell_value(21, 5),  # F22 22行6列4.期末余额合计
            "BiologicalAssets_LastIL_total": data.cell_value(23, 5),  # F24 24行6列1.期初余额合计
            "BiologicalAssets_AddIL_total": data.cell_value(24, 5),  # F25 25行6列2.本期增加金额合计
            "BiologicalAssets_AmortizationIL_total": data.cell_value(25, 5),  # F26 26行6列⑴计提合计
            "BiologicalAssets_MergeIL_total": data.cell_value(26, 5),  # F27 27行6列⑵企业合并增加合计
            "BiologicalAssets_ReduceIL_total": data.cell_value(27, 5),  # F28 28行6列3.本期减少金额合计
            "BiologicalAssets_DisposalIL_total": data.cell_value(28, 5),  # F29 29行6列⑴处置合计
            "BiologicalAssets_CReduceIL_total": data.cell_value(29, 5),  # F30 30行6列⑵企业合并减少合计
            "BiologicalAssets_ThisIL_total": data.cell_value(30, 5),  # F31 31行6列4.期末余额合计
            "BiologicalAssets_EBV_total": data.cell_value(32, 5),  # F33 33行6列1.期末账面价值合计
            "BiologicalAssets_OBV_total": data.cell_value(33, 5),  # F34 34行6列2.期初账面价值合计
            "BiologicalAssets_Last_total": data.cell_value(37, 5),  # F38 38行6列一、期初余额合计
            "BiologicalAssets_Change_total": data.cell_value(38, 5),  # F39 39行6列二、本期变动合计
            "BiologicalAssets_Purchase_total": data.cell_value(39, 5),  # F40 40行6列加：外购合计
            "BiologicalAssets_Cultivate_total": data.cell_value(40, 5),  # F41 41行6列自行培育合计
            "BiologicalAssets_Merge_total": data.cell_value(41, 5),  # F42 42行6列企业合并增加合计
            "BiologicalAssets_Disposal_total": data.cell_value(42, 5),  # F43 43行6列减：处置合计
            "BiologicalAssets_Transfer_total": data.cell_value(43, 5),  # F44 44行6列其他转出合计
            "BiologicalAssets_FChange_total": data.cell_value(44, 5),  # F45 45行6列公允价值变动合计
            "BiologicalAssets_This_total": data.cell_value(45, 5),  # F46 46行6列三、期末余额合计

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
        dic["BiologicalAssets_Remark"] = data.cell_value(47, 1),  # B48 48行2列说明
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
        # 采用成本计量模式的生产性生物资产账面原值期初余额:种植业+畜牧养殖业+林业+水产业=合计
        if abs(df["BiologicalAssets_LastOBV_farming"].fillna(0).values + df["BiologicalAssets_LastOBV_husbandry"].fillna(0).values + df["BiologicalAssets_LastOBV_forestry"].fillna(0).values + df["BiologicalAssets_LastOBV_aquaculture"].fillna(0).values - df["BiologicalAssets_LastOBV_total"].fillna(0).values) > 0.01:
            error = "采用成本计量模式的生产性生物资产账面原值期初余额:种植业+畜牧养殖业+林业+水产业<>合计"
            errorlist.append(error)
        # 采用成本计量模式的生产性生物资产账面原值本期增加金额:种植业+畜牧养殖业+林业+水产业=合计
        if abs(df["BiologicalAssets_AddOBV_farming"].fillna(0).values + df["BiologicalAssets_AddOBV_husbandry"].fillna(0).values + df["BiologicalAssets_AddOBV_forestry"].fillna(0).values + df["BiologicalAssets_AddOBV_aquaculture"].fillna(0).values - df["BiologicalAssets_AddOBV_total"].fillna(0).values) > 0.01:
            error = "采用成本计量模式的生产性生物资产账面原值本期增加金额:种植业+畜牧养殖业+林业+水产业<>合计"
            errorlist.append(error)
        # 采用成本计量模式的生产性生物资产账面原值本期减少金额:种植业+畜牧养殖业+林业+水产业=合计
        if abs(df["BiologicalAssets_ReduceOBV_farming"].fillna(0).values + df["BiologicalAssets_ReduceOBV_husbandry"].fillna(0).values + df["BiologicalAssets_ReduceOBV_forestry"].fillna(0).values + df["BiologicalAssets_ReduceOBV_aquaculture"].fillna(0).values - df["BiologicalAssets_ReduceOBV_total"].fillna(0).values) > 0.01:
            error = "采用成本计量模式的生产性生物资产账面原值本期减少金额:种植业+畜牧养殖业+林业+水产业<>合计"
            errorlist.append(error)
        # 采用成本计量模式的生产性生物资产账面原值期末余额:种植业+畜牧养殖业+林业+水产业=合计
        if abs(df["BiologicalAssets_ThisOBV_farming"].fillna(0).values + df["BiologicalAssets_ThisOBV_husbandry"].fillna(0).values + df["BiologicalAssets_ThisOBV_forestry"].fillna(0).values + df["BiologicalAssets_ThisOBV_aquaculture"].fillna(0).values - df["BiologicalAssets_ThisOBV_total"].fillna(0).values) > 0.01:
            error = "采用成本计量模式的生产性生物资产账面原值期末余额:种植业+畜牧养殖业+林业+水产业<>合计"
            errorlist.append(error)
        # 采用成本计量模式的生产性生物资产累计折旧期初余额:种植业+畜牧养殖业+林业+水产业=合计
        if abs(df["BiologicalAssets_LastAD_farming"].fillna(0).values + df["BiologicalAssets_LastAD_husbandry"].fillna(0).values + df["BiologicalAssets_LastAD_forestry"].fillna(0).values + df["BiologicalAssets_LastAD_aquaculture"].fillna(0).values - df["BiologicalAssets_LastAD_total"].fillna(0).values) > 0.01:
            error = "采用成本计量模式的生产性生物资产累计折旧期初余额:种植业+畜牧养殖业+林业+水产业<>合计"
            errorlist.append(error)
        # 采用成本计量模式的生产性生物资产累计折旧本期增加金额:种植业+畜牧养殖业+林业+水产业=合计
        if abs(df["BiologicalAssets_AddAD_farming"].fillna(0).values + df["BiologicalAssets_AddAD_husbandry"].fillna(0).values + df["BiologicalAssets_AddAD_forestry"].fillna(0).values + df["BiologicalAssets_AddAD_aquaculture"].fillna(0).values - df["BiologicalAssets_AddAD_total"].fillna(0).values) > 0.01:
            error = "采用成本计量模式的生产性生物资产累计折旧本期增加金额:种植业+畜牧养殖业+林业+水产业<>合计"
            errorlist.append(error)
        # 采用成本计量模式的生产性生物资产累计折旧本期减少金额:种植业+畜牧养殖业+林业+水产业=合计
        if abs(df["BiologicalAssets_ReduceAD_farming"].fillna(0).values + df["BiologicalAssets_ReduceAD_husbandry"].fillna(0).values + df["BiologicalAssets_ReduceAD_forestry"].fillna(0).values + df["BiologicalAssets_ReduceAD_aquaculture"].fillna(0).values - df["BiologicalAssets_ReduceAD_total"].fillna(0).values) > 0.01:
            error = "采用成本计量模式的生产性生物资产累计折旧本期减少金额:种植业+畜牧养殖业+林业+水产业<>合计"
            errorlist.append(error)
        # 采用成本计量模式的生产性生物资产累计折旧期末余额:种植业+畜牧养殖业+林业+水产业=合计
        if abs(df["BiologicalAssets_ThisAD_farming"].fillna(0).values + df["BiologicalAssets_ThisAD_husbandry"].fillna(0).values + df["BiologicalAssets_ThisAD_forestry"].fillna(0).values + df["BiologicalAssets_ThisAD_aquaculture"].fillna(0).values - df["BiologicalAssets_ThisAD_total"].fillna(0).values) > 0.01:
            error = "采用成本计量模式的生产性生物资产累计折旧期末余额:种植业+畜牧养殖业+林业+水产业<>合计"
            errorlist.append(error)
        # 采用成本计量模式的生产性生物资产减值准备期初余额:种植业+畜牧养殖业+林业+水产业=合计
        if abs(df["BiologicalAssets_LastIL_farming"].fillna(0).values + df["BiologicalAssets_LastIL_husbandry"].fillna(0).values + df["BiologicalAssets_LastIL_forestry"].fillna(0).values + df["BiologicalAssets_LastIL_aquaculture"].fillna(0).values - df["BiologicalAssets_LastIL_total"].fillna(0).values) > 0.01:
            error = "采用成本计量模式的生产性生物资产减值准备期初余额:种植业+畜牧养殖业+林业+水产业<>合计"
            errorlist.append(error)
        # 采用成本计量模式的生产性生物资产减值准备本期增加金额:种植业+畜牧养殖业+林业+水产业=合计
        if abs(df["BiologicalAssets_AddIL_farming"].fillna(0).values + df["BiologicalAssets_AddIL_husbandry"].fillna(0).values + df["BiologicalAssets_AddIL_forestry"].fillna(0).values + df["BiologicalAssets_AddIL_aquaculture"].fillna(0).values - df["BiologicalAssets_AddIL_total"].fillna(0).values) > 0.01:
            error = "采用成本计量模式的生产性生物资产减值准备本期增加金额:种植业+畜牧养殖业+林业+水产业<>合计"
            errorlist.append(error)
        # 采用成本计量模式的生产性生物资产减值准备本期减少金额:种植业+畜牧养殖业+林业+水产业=合计
        if abs(df["BiologicalAssets_ReduceIL_farming"].fillna(0).values + df["BiologicalAssets_ReduceIL_husbandry"].fillna(0).values + df["BiologicalAssets_ReduceIL_forestry"].fillna(0).values + df["BiologicalAssets_ReduceIL_aquaculture"].fillna(0).values - df["BiologicalAssets_ReduceIL_total"].fillna(0).values) > 0.01:
            error = "采用成本计量模式的生产性生物资产减值准备本期减少金额:种植业+畜牧养殖业+林业+水产业<>合计"
            errorlist.append(error)
        # 采用成本计量模式的生产性生物资产减值准备期末余额:种植业+畜牧养殖业+林业+水产业=合计
        if abs(df["BiologicalAssets_ThisIL_farming"].fillna(0).values + df["BiologicalAssets_ThisIL_husbandry"].fillna(0).values + df["BiologicalAssets_ThisIL_forestry"].fillna(0).values + df["BiologicalAssets_ThisIL_aquaculture"].fillna(0).values - df["BiologicalAssets_ThisIL_total"].fillna(0).values) > 0.01:
            error = "采用成本计量模式的生产性生物资产减值准备期末余额:种植业+畜牧养殖业+林业+水产业<>合计"
            errorlist.append(error)
        # 采用成本计量模式的生产性生物资产期末账面价值:种植业+畜牧养殖业+林业+水产业=合计
        if abs(df["BiologicalAssets_EBV_farming"].fillna(0).values + df["BiologicalAssets_EBV_husbandry"].fillna(0).values + df["BiologicalAssets_EBV_forestry"].fillna(0).values + df["BiologicalAssets_EBV_aquaculture"].fillna(0).values - df["BiologicalAssets_EBV_total"].fillna(0).values) > 0.01:
            error = "采用成本计量模式的生产性生物资产期末账面价值:种植业+畜牧养殖业+林业+水产业<>合计"
            errorlist.append(error)
        # 采用成本计量模式的生产性生物资产期初账面价值:种植业+畜牧养殖业+林业+水产业=合计
        if abs(df["BiologicalAssets_OBV_farming"].fillna(0).values + df["BiologicalAssets_OBV_husbandry"].fillna(0).values + df["BiologicalAssets_OBV_forestry"].fillna(0).values + df["BiologicalAssets_OBV_aquaculture"].fillna(0).values - df["BiologicalAssets_OBV_total"].fillna(0).values) > 0.01:
            error = "采用成本计量模式的生产性生物资产期初账面价值:种植业+畜牧养殖业+林业+水产业<>合计"
            errorlist.append(error)
        # 采用公允价值计量模式的生产性生物资产期初余额：种植业+畜牧养殖业+林业+水产业=合计
        if abs(df["BiologicalAssets_Last_farming"].fillna(0).values + df["BiologicalAssets_Last_husbandry"].fillna(0).values + df["BiologicalAssets_Last_forestry"].fillna(0).values + df["BiologicalAssets_Last_aquaculture"].fillna(0).values - df["BiologicalAssets_Last_total"].fillna(0).values) > 0.01:
            error = "采用公允价值计量模式的生产性生物资产期初余额：种植业+畜牧养殖业+林业+水产业<>合计"
            errorlist.append(error)
        # 采用公允价值计量模式的生产性生物资产本期变动：种植业+畜牧养殖业+林业+水产业=合计
        if abs(df["BiologicalAssets_Change_farming"].fillna(0).values + df["BiologicalAssets_Change_husbandry"].fillna(0).values + df["BiologicalAssets_Change_forestry"].fillna(0).values + df["BiologicalAssets_Change_aquaculture"].fillna(0).values - df["BiologicalAssets_Change_total"].fillna(0).values) > 0.01:
            error = "采用公允价值计量模式的生产性生物资产本期变动：种植业+畜牧养殖业+林业+水产业<>合计"
            errorlist.append(error)
        # 采用公允价值计量模式的生产性生物资产外购：种植业+畜牧养殖业+林业+水产业=合计
        if abs(df["BiologicalAssets_Purchase_farming"].fillna(0).values + df["BiologicalAssets_Purchase_husbandry"].fillna(0).values + df["BiologicalAssets_Purchase_forestry"].fillna(0).values + df["BiologicalAssets_Purchase_aquaculture"].fillna(0).values - df["BiologicalAssets_Purchase_total"].fillna(0).values) > 0.01:
            error = "采用公允价值计量模式的生产性生物资产外购：种植业+畜牧养殖业+林业+水产业<>合计"
            errorlist.append(error)
        # 采用公允价值计量模式的生产性生物资产自行培育：种植业+畜牧养殖业+林业+水产业=合计
        if abs(df["BiologicalAssets_Cultivate_farming"].fillna(0).values + df["BiologicalAssets_Cultivate_husbandry"].fillna(0).values + df["BiologicalAssets_Cultivate_forestry"].fillna(0).values + df["BiologicalAssets_Cultivate_aquaculture"].fillna(0).values - df["BiologicalAssets_Cultivate_total"].fillna(0).values) > 0.01:
            error = "采用公允价值计量模式的生产性生物资产自行培育：种植业+畜牧养殖业+林业+水产业<>合计"
            errorlist.append(error)
        # 采用公允价值计量模式的生产性生物资产企业合并增加：种植业+畜牧养殖业+林业+水产业=合计
        if abs(df["BiologicalAssets_Merge_farming"].fillna(0).values + df["BiologicalAssets_Merge_husbandry"].fillna(0).values + df["BiologicalAssets_Merge_forestry"].fillna(0).values + df["BiologicalAssets_Merge_aquaculture"].fillna(0).values - df["BiologicalAssets_Merge_total"].fillna(0).values) > 0.01:
            error = "采用公允价值计量模式的生产性生物资产企业合并增加：种植业+畜牧养殖业+林业+水产业<>合计"
            errorlist.append(error)
        # 采用公允价值计量模式的生产性生物资产处置：种植业+畜牧养殖业+林业+水产业=合计
        if abs(df["BiologicalAssets_Disposal_farming"].fillna(0).values + df["BiologicalAssets_Disposal_husbandry"].fillna(0).values + df["BiologicalAssets_Disposal_forestry"].fillna(0).values + df["BiologicalAssets_Disposal_aquaculture"].fillna(0).values - df["BiologicalAssets_Disposal_total"].fillna(0).values) > 0.01:
            error = "采用公允价值计量模式的生产性生物资产处置：种植业+畜牧养殖业+林业+水产业<>合计"
            errorlist.append(error)
        # 采用公允价值计量模式的生产性生物资产其他转出：种植业+畜牧养殖业+林业+水产业=合计
        if abs(df["BiologicalAssets_Transfer_farming"].fillna(0).values + df["BiologicalAssets_Transfer_husbandry"].fillna(0).values + df["BiologicalAssets_Transfer_forestry"].fillna(0).values + df["BiologicalAssets_Transfer_aquaculture"].fillna(0).values - df["BiologicalAssets_Transfer_total"].fillna(0).values) > 0.01:
            error = "采用公允价值计量模式的生产性生物资产其他转出：种植业+畜牧养殖业+林业+水产业<>合计"
            errorlist.append(error)
        # 采用公允价值计量模式的生产性生物资产公允价值变动：种植业+畜牧养殖业+林业+水产业=合计
        if abs(df["BiologicalAssets_FChange_farming"].fillna(0).values + df["BiologicalAssets_FChange_husbandry"].fillna(0).values + df["BiologicalAssets_FChange_forestry"].fillna(0).values + df["BiologicalAssets_FChange_aquaculture"].fillna(0).values - df["BiologicalAssets_FChange_total"].fillna(0).values) > 0.01:
            error = "采用公允价值计量模式的生产性生物资产公允价值变动：种植业+畜牧养殖业+林业+水产业<>合计"
            errorlist.append(error)
        # 采用公允价值计量模式的生产性生物资产期末余额：种植业+畜牧养殖业+林业+水产业=合计
        if abs(df["BiologicalAssets_This_farming"].fillna(0).values + df["BiologicalAssets_This_husbandry"].fillna(0).values + df["BiologicalAssets_This_forestry"].fillna(0).values + df["BiologicalAssets_This_aquaculture"].fillna(0).values - df["BiologicalAssets_This_total"].fillna(0).values) > 0.01:
            error = "采用公允价值计量模式的生产性生物资产期末余额：种植业+畜牧养殖业+林业+水产业<>合计"
            errorlist.append(error)
        











        return df, errorlist


if __name__ == "__main__":
    d = GetBiologicalAssets()