
import pandas as pd
from ChosenAPI.DataImport.ChangeToNum import ChangeData



class GetFixedAssets(object):#固定资产
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
            "FixedAssets_FixedAssets_this": data.cell_value(3, 1),  # B4 4行2列固定资产期末余额
            "FixedAssets_FixedAssetsLiquidation_this": data.cell_value(4, 1),  # B5 5行2列固定资产清理期末余额
            "FixedAssets_Total1_this": data.cell_value(5, 1),  # B6 6行2列合计期末余额
            "FixedAssets_FixedAssets_last": data.cell_value(3, 2),  # C4 4行3列固定资产期初余额
            "FixedAssets_FixedAssetsLiquidation_last": data.cell_value(4, 2),  # C5 5行3列固定资产清理期初余额
            "FixedAssets_Total2_last": data.cell_value(5, 2),  # C6 6行3列合计期初余额
            "FixedAssets_LastOBV_Buildings": data.cell_value(10, 1),  # B11 11行2列1.期初余额房屋及建筑物
            "FixedAssets_AddOBV_Buildings": data.cell_value(11, 1),  # B12 12行2列2.本期增加金额房屋及建筑物
            "FixedAssets_PurchaseOBV_Buildings": data.cell_value(12, 1),  # B13 13行2列⑴购置房屋及建筑物
            "FixedAssets_IntoOBV_Buildings": data.cell_value(13, 1),  # B14 14行2列⑵在建工程转入房屋及建筑物
            "FixedAssets_MergeOBV_Buildings": data.cell_value(14, 1),  # B15 15行2列⑶企业合并增加房屋及建筑物
            "FixedAssets_ReduceOBV_Buildings": data.cell_value(15, 1),  # B16 16行2列3.本期减少金额房屋及建筑物
            "FixedAssets_DisposalOBV_Buildings": data.cell_value(16, 1),  # B17 17行2列⑴处置或报废房屋及建筑物
            "FixedAssets_CombinedToReduceOBV_Buildings": data.cell_value(17, 1),# B18 18行2列⑵企业合并减少房屋及建筑物
            "FixedAssets_ThisOBV_Buildings": data.cell_value(18, 1),  # B19 19行2列4.期末余额房屋及建筑物
            "FixedAssets_LastAD_Buildings": data.cell_value(20, 1),  # B21 21行2列1.期初余额房屋及建筑物
            "FixedAssets_AddAD_Buildings": data.cell_value(21, 1),  # B22 22行2列2.本期增加金额房屋及建筑物
            "FixedAssets_AmortizationAD_Buildings": data.cell_value(22, 1),  # B23 23行2列⑴计提房屋及建筑物
            "FixedAssets_MergeAD_Buildings": data.cell_value(23, 1),  # B24 24行2列⑵企业合并增加房屋及建筑物
            "FixedAssets_ReduceAD_Buildings": data.cell_value(24, 1),  # B25 25行2列3.本期减少金额房屋及建筑物
            "FixedAssets_DisposalAD_Buildings": data.cell_value(25, 1),  # B26 26行2列⑴处置或报废房屋及建筑物
            "FixedAssets_CombinedToReduceAD_Buildings": data.cell_value(26, 1),# B27 27行2列⑵企业合并减少房屋及建筑物
            "FixedAssets_ThisAD_Buildings": data.cell_value(27, 1),  # B28 28行2列4.期末余额房屋及建筑物
            "FixedAssets_LastIL_Buildings": data.cell_value(29, 1),  # B30 30行2列1.期初余额房屋及建筑物
            "FixedAssets_AddIL_Buildings": data.cell_value(30, 1),  # B31 31行2列2.本期增加金额房屋及建筑物
            "FixedAssets_AmortizationIL_Buildings": data.cell_value(31, 1),  # B32 32行2列⑴计提房屋及建筑物
            "FixedAssets_MergeIL_Buildings": data.cell_value(32, 1),  # B33 33行2列⑵企业合并增加房屋及建筑物
            "FixedAssets_ReduceIL_Buildings": data.cell_value(33, 1),  # B34 34行2列3.本期减少金额房屋及建筑物
            "FixedAssets_DisposalIL_Buildings": data.cell_value(34, 1),  # B35 35行2列⑴处置或报废房屋及建筑物
            "FixedAssets_CombinedToReduceIL_Buildings": data.cell_value(35, 1),  # B36 36行2列⑵企业合并减少房屋及建筑物
            "FixedAssets_ThisIL_Buildings": data.cell_value(36, 1),  # B37 37行2列期末余额房屋及建筑物
            "FixedAssets_EndingBookValue_Buildings": data.cell_value(38, 1),  # B39 39行2列1.期末账面价值房屋及建筑物
            "FixedAssets_OpeningBookValue_Buildings": data.cell_value(39, 1),  # B40 40行2列2.期初账面价值房屋及建筑物
            "FixedAssets_BuildingsIdle_OBV": data.cell_value(43, 1),  # B44 44行2列房屋及建筑物账面原值
            "FixedAssets_MEIdle_OBV": data.cell_value(44, 1),  # B45 45行2列机器设备账面原值
            "FixedAssets_TransportMachineIdle_OBV": data.cell_value(45, 1),  # B46 46行2列运输工具账面原值
            "FixedAssets_ElectronicEquipmentIdle_OBV": data.cell_value(46, 1),  # B47 47行2列电子设备账面原值
            "FixedAssets_OtherEquipmentIdle_OBV": data.cell_value(47, 1),  # B48 48行2列其他设备账面原值
            "FixedAssets_Total2_OBV": data.cell_value(48, 1),  # B49 49行2列合计账面原值
            "FixedAssets_LastOBV_ME": data.cell_value(10, 2),  # C11 11行3列1.期初余额机器设备
            "FixedAssets_AddOBV_ME": data.cell_value(11, 2),  # C12 12行3列2.本期增加金额机器设备
            "FixedAssets_PurchaseOBV_ME": data.cell_value(12, 2),  # C13 13行3列⑴购置机器设备
            "FixedAssets_IntoOBV_ME": data.cell_value(13, 2),  # C14 14行3列⑵在建工程转入机器设备
            "FixedAssets_MergeOBV_ME": data.cell_value(14, 2),  # C15 15行3列⑶企业合并增加机器设备
            "FixedAssets_ReduceOBV_ME": data.cell_value(15, 2),  # C16 16行3列3.本期减少金额机器设备
            "FixedAssets_DisposalOBV_ME": data.cell_value(16, 2),  # C17 17行3列⑴处置或报废机器设备
            "FixedAssets_CombinedToReduceOBV_ME": data.cell_value(17, 2),# C18 18行3列⑵企业合并减少机器设备
            "FixedAssets_ThisOBV_ME": data.cell_value(18, 2),  # C19 19行3列4.期末余额机器设备
            "FixedAssets_LastAD_ME": data.cell_value(20, 2),# C21 21行3列1.期初余额机器设备
            "FixedAssets_AddAD_ME": data.cell_value(21, 2),# C22 22行3列2.本期增加金额机器设备
            "FixedAssets_AmortizationAD_ME": data.cell_value(22, 2),# C23 23行3列⑴计提机器设备
            "FixedAssets_MergeAD_ME": data.cell_value(23, 2),# C24 24行3列⑵企业合并增加机器设备
            "FixedAssets_ReduceAD_ME": data.cell_value(24, 2),# C25 25行3列3.本期减少金额机器设备
            "FixedAssets_DisposalAD_ME": data.cell_value(25, 2),# C26 26行3列⑴处置或报废机器设备
            "FixedAssets_CombinedToReduceAD_ME": data.cell_value(26, 2),# C27 27行3列⑵企业合并减少机器设备
            "FixedAssets_ThisAD_ME": data.cell_value(27, 2),# C28 28行3列4.期末余额机器设备
            "FixedAssets_LastIL_ME": data.cell_value(29, 2),  # C30 30行3列1.期初余额机器设备
            "FixedAssets_AddIL_ME": data.cell_value(30, 2),  # C31 31行3列2.本期增加金额机器设备
            "FixedAssets_AmortizationIL_ME": data.cell_value(31, 2),  # C32 32行3列⑴计提机器设备
            "FixedAssets_MergeIL_ME": data.cell_value(32, 2),  # C33 33行3列⑵企业合并增加机器设备
            "FixedAssets_ReduceIL_ME": data.cell_value(33, 2),  # C34 34行3列3.本期减少金额机器设备
            "FixedAssets_DisposalIL_ME": data.cell_value(34, 2),  # C35 35行3列⑴处置或报废机器设备
            "FixedAssets_CombinedToReduceIL_ME": data.cell_value(35, 2),# C36 36行3列⑵企业合并减少机器设备
            "FixedAssets_ThisIL_ME": data.cell_value(36, 2),  # C37 37行3期末余额价值机器设备
            "FixedAssets_EndingBookValue_ME": data.cell_value(38, 2),  # C39 39行3列1.期末账面价值机器设备
            "FixedAssets_OpeningBookValue_ME": data.cell_value(39, 2),  # C40 40行3列2.期初账面价值机器设备
            "FixedAssets_BuildingsIdle_AD": data.cell_value(43, 2),  # C44 44行3列房屋及建筑物累计折旧
            "FixedAssets_MEIdle_AD": data.cell_value(44, 2),  # C45 45行3列机器设备累计折旧
            "FixedAssets_TransportMachineIdle_AD": data.cell_value(45, 2),  # C46 46行3列运输工具累计折旧
            "FixedAssets_ElectronicEquipmentIdle_AD": data.cell_value(46, 2),  # C47 47行3列电子设备累计折旧
            "FixedAssets_OtherEquipmentIdle_AD": data.cell_value(47, 2),  # C48 48行3列其他设备累计折旧
            "FixedAssets_Total3_AD": data.cell_value(48, 2),  # C49 49行3列合计累计折旧
            "FixedAssets_LastOBV_TransportMachine": data.cell_value(10, 3),  # D11 11行4列1.期初余额运输设备
            "FixedAssets_AddOBV_TransportMachine": data.cell_value(11, 3),  # D12 12行4列2.本期增加金额运输设备
            "FixedAssets_PurchaseOBV_TransportMachine": data.cell_value(12, 3),  # D13 13行4列⑴购置运输设备
            "FixedAssets_IntoOBV_TransportMachine": data.cell_value(13, 3),  # D14 14行4列⑵在建工程转入运输设备
            "FixedAssets_MergeOBV_TransportMachine": data.cell_value(14, 3),  # D15 15行4列⑶企业合并增加运输设备
            "FixedAssets_ReduceOBV_TransportMachine": data.cell_value(15, 3),  # D16 16行4列3.本期减少金额运输设备
            "FixedAssets_DisposalOBV_TransportMachine": data.cell_value(16, 3),  # D17 17行4列⑴处置或报废运输设备
            "FixedAssets_CombinedToReduceOBV_TransportMachine": data.cell_value(17, 3),# D18 18行4列⑵企业合并减少运输设备
            "FixedAssets_ThisOBV_TransportMachine": data.cell_value(18, 3),  # D19 19行4列4.期末余额运输设备
            "FixedAssets_LastAD_TransportMachine": data.cell_value(20, 3),  # D21 21行4列1.期初余额运输设备
            "FixedAssets_AddAD_TransportMachine": data.cell_value(21, 3),  # D22 22行4列2.本期增加金额运输设备
            "FixedAssets_AmortizationAD_TransportMachine": data.cell_value(22, 3),# D23 23行4列⑴计提运输设备
            "FixedAssets_MergeAD_TransportMachine": data.cell_value(23, 3),# D24 24行4列⑵企业合并增加运输设备
            "FixedAssets_ReduceAD_TransportMachine": data.cell_value(24, 3),# D25 25行4列3.本期减少金额运输设备
            "FixedAssets_DisposalAD_TransportMachine": data.cell_value(25, 3),# D26 26行4列⑴处置或报废运输设备
            "FixedAssets_CombinedToReduceAD_TransportMachine": data.cell_value(26, 3),# D27 27行4列⑵企业合并减少运输设备
            "FixedAssets_ThisAD_TransportMachine": data.cell_value(27, 3),  # D28 28行4列4.期末余额运输设备
            "FixedAssets_LastIL_TransportMachine": data.cell_value(29, 3),  # D30 30行4列1.期初余额运输设备
            "FixedAssets_AddIL_TransportMachine": data.cell_value(30, 3),  # D31 31行4列2.本期增加金额运输设备
            "FixedAssets_AmortizationIL_TransportMachine": data.cell_value(31, 3),  # D32 32行4列⑴计提运输设备
            "FixedAssets_MergeIL_TransportMachine": data.cell_value(32, 3),  # D33 33行4列⑵企业合并增加运输设备
            "FixedAssets_ReduceIL_TransportMachine": data.cell_value(33, 3),  # D34 34行4列3.本期减少金额运输设备
            "FixedAssets_DisposalIL_TransportMachine": data.cell_value(34, 3),  # D35 35行4列⑴处置或报废运输设备
            "FixedAssets_CombinedToReduceIL_TransportMachine": data.cell_value(35, 3),# D36 36行4列⑵企业合并减少运输设备
            "FixedAssets_ThisIL_TransportMachine": data.cell_value(36, 3),  # D37 37行4列期末余额运输设备
            "FixedAssets_EndingBookValue_TransportMachine": data.cell_value(38, 3),  # D39 39行4列1.期末账面价值运输设备
            "FixedAssets_OpeningBookValue_TransportMachine": data.cell_value(39, 3),  # D40 40行4列2.期初账面价值运输设备
            "FixedAssets_BuildingsIdle_IL": data.cell_value(43, 3),  # D44 44行4列房屋及建筑物减值准备
            "FixedAssets_MEIdle_IL": data.cell_value(44, 3),  # D45 45行4列机器设备减值准备
            "FixedAssets_TransportMachineIdle_IL": data.cell_value(45, 3),  # D46 46行4列运输工具减值准备
            "FixedAssets_ElectronicEquipmentIdle_IL": data.cell_value(46, 3),  # D47 47行4列电子设备减值准备
            "FixedAssets_OtherEquipmentIdle_IL": data.cell_value(47, 3),  # D48 48行4列其他设备减值准备
            "FixedAssets_Total4_IL": data.cell_value(48, 3),  # D49 49行4列合计减值准备
            "FixedAssets_LastOBV_ElectronicEquipment": data.cell_value(10, 4),  # E11 11行5列1.期初余额电子设备
            "FixedAssets_AddOBV_ElectronicEquipment": data.cell_value(11, 4),  # E12 12行5列2.本期增加金额电子设备
            "FixedAssets_PurchaseOBV_ElectronicEquipment": data.cell_value(12, 4),  # E13 13行5列⑴购置电子设备
            "FixedAssets_IntoOBV_ElectronicEquipment": data.cell_value(13, 4),  # E14 14行5列⑵在建工程转入电子设备
            "FixedAssets_MergeOBV_ElectronicEquipment": data.cell_value(14, 4),  # E15 15行5列⑶企业合并增加电子设备
            "FixedAssets_ReduceOBV_ElectronicEquipment": data.cell_value(15, 4),  # E16 16行5列3.本期减少金额电子设备
            "FixedAssets_DisposalOBV_ElectronicEquipment": data.cell_value(16, 4),  # E17 17行5列⑴处置或报废电子设备
            "FixedAssets_CombinedToReduceOBV_ElectronicEquipment": data.cell_value(17, 4),# E18 18行5列⑵企业合并减少电子设备
            "FixedAssets_ThisOBV_ElectronicEquipment": data.cell_value(18, 4),  # E19 19行5列4.期末余额电子设备
            "FixedAssets_LastAD_ElectronicEquipment": data.cell_value(20, 4),# E21 21行5列1.期初余额电子设备
            "FixedAssets_AddAD_ElectronicEquipment": data.cell_value(21, 4),# E22 22行5列2.本期增加金额电子设备
            "FixedAssets_AmortizationAD_ElectronicEquipment": data.cell_value(22, 4),# E23 23行5列⑴计提电子设备
            "FixedAssets_MergeAD_ElectronicEquipment": data.cell_value(23, 4),# E24 24行5列⑵企业合并增加电子设备
            "FixedAssets_ReduceAD_ElectronicEquipment": data.cell_value(24, 4),# E25 25行5列3.本期减少金额电子设备
            "FixedAssets_DisposalAD_ElectronicEquipment": data.cell_value(25, 4),# E26 26行5列⑴处置或报废电子设备
            "FixedAssets_CombinedToReduceAD_ElectronicEquipment": data.cell_value(26, 4),# E27 27行5列⑵企业合并减少电子设备
            "FixedAssets_ThisAD_ElectronicEquipment": data.cell_value(27, 4),# E28 28行5列4.期末余额电子设备
            "FixedAssets_LastIL_ElectronicEquipment": data.cell_value(29, 4),  # E30 30行5列1.期初余额电子设备
            "FixedAssets_AddIL_ElectronicEquipment": data.cell_value(30, 4),  # E31 31行5列2.本期增加金额电子设备
            "FixedAssets_AmortizationIL_ElectronicEquipment": data.cell_value(31, 4),  # E32 32行5列⑴计提电子设备
            "FixedAssets_MergeIL_ElectronicEquipment": data.cell_value(32, 4),  # E33 33行5列⑵企业合并增加电子设备
            "FixedAssets_ReduceIL_ElectronicEquipment": data.cell_value(33, 4),  # E34 34行5列3.本期减少金额电子设备
            "FixedAssets_DisposalIL_ElectronicEquipment": data.cell_value(34, 4),  # E35 35行5列⑴处置或报废电子设备
            "FixedAssets_CombinedToReduceIL_ElectronicEquipment": data.cell_value(35, 4),# E36 36行5列⑵企业合并减少电子设备
            "FixedAssets_ThisIL_ElectronicEquipment": data.cell_value(36, 4),  # E37 37行5列期末余额电子设备
            "FixedAssets_EndingBookValue_ElectronicEquipment": data.cell_value(38, 4),  # E39 39行5列1.期末账面价值电子设备
            "FixedAssets_OpeningBookValue_ElectronicEquipment": data.cell_value(39, 4),  # E40 40行5列2.期初账面价值电子设备
            "FixedAssets_BuildingsIdle_BookValue": data.cell_value(43, 4),  # E44 44行5列房屋及建筑物账面价值
            "FixedAssets_MEIdle_BookValue": data.cell_value(44, 4),  # E45 45行5列机器设备账面价值
            "FixedAssets_TransportMachineIdle_BookValue": data.cell_value(45, 4),  # E46 46行5列运输工具账面价值
            "FixedAssets_ElectronicEquipmentIdle_BookValue": data.cell_value(46, 4),  # E47 47行5列电子设备账面价值
            "FixedAssets_OtherEquipmentIdle_BookValue": data.cell_value(47, 4),  # E48 48行5列其他设备账面价值
            "FixedAssets_Total5_BookValue": data.cell_value(48, 4),  # E49 49行5列合计账面价值
            "FixedAssets_LastOBV_OtherEquipment": data.cell_value(10, 5),  # F11 11行6列1.期初余额其他设备
            "FixedAssets_AddOBV_OtherEquipment": data.cell_value(11, 5),  # F12 12行6列2.本期增加金额其他设备
            "FixedAssets_PurchaseOBV_OtherEquipment": data.cell_value(12, 5),  # F13 13行6列⑴购置其他设备
            "FixedAssets_IntoOBV_OtherEquipment": data.cell_value(13, 5),  # F14 14行6列⑵在建工程转入其他设备
            "FixedAssets_MergeOBV_OtherEquipment": data.cell_value(14, 5),  # F15 15行6列⑶企业合并增加其他设备
            "FixedAssets_ReduceOBV_OtherEquipment": data.cell_value(15, 5),  # F16 16行6列3.本期减少金额其他设备
            "FixedAssets_DisposalOBV_OtherEquipment": data.cell_value(16, 5),  # F17 17行6列⑴处置或报废其他设备
            "FixedAssets_CombinedToReduceOBV_OtherEquipment": data.cell_value(17, 5),# F18 18行6列⑵企业合并减少其他设备
            "FixedAssets_ThisOBV_OtherEquipment": data.cell_value(18, 5),  # F19 19行6列4.期末余额其他设备
            "FixedAssets_LastAD_OtherEquipment": data.cell_value(20, 5),  # F21 21行6列1.期初余额其他设备
            "FixedAssets_AddAD_OtherEquipment": data.cell_value(21, 5),  # F22 22行6列2.本期增加金额其他设备
            "FixedAssets_AmortizationAD_OtherEquipment": data.cell_value(22, 5),# F23 23行6列⑴计提其他设备
            "FixedAssets_MergeAD_OtherEquipment": data.cell_value(23, 5),  # F24 24行6列⑵企业合并增加其他设备
            "FixedAssets_ReduceAD_OtherEquipment": data.cell_value(24, 5),# F25 25行6列3.本期减少金额其他设备
            "FixedAssets_DisposalAD_OtherEquipment": data.cell_value(25, 5),# F26 26行6列⑴处置或报废其他设备
            "FixedAssets_CombinedToReduceAD_OtherEquipment": data.cell_value(26, 5),# F27 27行6列⑵企业合并减少其他设备
            "FixedAssets_ThisAD_OtherEquipment": data.cell_value(27, 5),  # F28 28行6列4.期末余额其他设备
            "FixedAssets_LastIL_OtherEquipment": data.cell_value(29, 5),  # F30 30行6列1.期初余额其他设备
            "FixedAssets_AddIL_OtherEquipment": data.cell_value(30, 5),  # F31 31行6列2.本期增加金额其他设备
            "FixedAssets_AmortizationIL_OtherEquipment": data.cell_value(31, 5),  # F32 32行6列⑴计提其他设备
            "FixedAssets_MergeIL_OtherEquipment": data.cell_value(32, 5),  # F33 33行6列⑵企业合并增加其他设备
            "FixedAssets_ReduceIL_OtherEquipment": data.cell_value(33, 5),  # F34 34行6列3.本期减少金额其他设备
            "FixedAssets_DisposalIL_OtherEquipment": data.cell_value(34, 5),  # F35 35行6列⑴处置或报废其他设备
            "FixedAssets_CombinedToReduceIL_OtherEquipment": data.cell_value(35, 5),# F36 36行6列⑵企业合并减少其他设备
            "FixedAssets_ThisIL_OtherEquipment": data.cell_value(36, 5),  # F37 37行6列期末余额其他设备
            "FixedAssets_EndingBookValue_OtherEquipment": data.cell_value(38, 5),  # F39 39行6列1.期末账面价值其他设备
            "FixedAssets_OpeningBookValue_OtherEquipment": data.cell_value(39, 5),  # F40 40行6列2.期初账面价值其他设备
            "FixedAssets_LastOBV_Total": data.cell_value(10, 6),  # G11 11行7列1.期初余额合计
            "FixedAssets_AddOBV_Total": data.cell_value(11, 6),  # G12 12行7列2.本期增加金额合计
            "FixedAssets_PurchaseOBV_Total": data.cell_value(12, 6),  # G13 13行7列⑴购置合计
            "FixedAssets_IntoOBV_Total": data.cell_value(13, 6),  # G14 14行7列⑵在建工程转入合计
            "FixedAssets_MergeOBV_Total": data.cell_value(14, 6),  # G15 15行7列⑶企业合并增加合计
            "FixedAssets_ReduceOBV_Total": data.cell_value(15, 6),  # G16 16行7列3.本期减少金额合计
            "FixedAssets_DisposalOBV_Total": data.cell_value(16, 6),  # G17 17行7列⑴处置或报废合计
            "FixedAssets_CombinedToReduceOBV_Total": data.cell_value(17, 6),  # G18 18行7列⑵企业合并减少合计
            "FixedAssets_ThisOBV_Total": data.cell_value(18, 6),  # G19 19行7列4.期末余额合计
            "FixedAssets_LastAD_Total": data.cell_value(20, 6),  # G21 21行7列1.期初余额合计
            "FixedAssets_AddAD_Total": data.cell_value(21, 6),  # G22 22行7列2.本期增加金额合计
            "FixedAssets_AmortizationAD_Total": data.cell_value(22, 6),  # G23 23行7列⑴计提合计
            "FixedAssets_MergeAD_Total": data.cell_value(23, 6),  # G24 24行7列⑵企业合并增加合计
            "FixedAssets_ReduceAD_Total": data.cell_value(24, 6),  # G25 25行7列3.本期减少金额合计
            "FixedAssets_DisposalAD_Total": data.cell_value(25, 6),  # G26 26行7列⑴处置或报废合计
            "FixedAssets_CombinedToReduceAD_Total": data.cell_value(26, 6),  # G27 27行7列⑵企业合并减少合计
            "FixedAssets_ThisAD_Total": data.cell_value(27, 6),  # G28 28行7列4.期末余额合计
            "FixedAssets_LastIL_Total": data.cell_value(29, 6),  # G30 30行7列1.期初余额合计
            "FixedAssets_AddIL_Total": data.cell_value(30, 6),  # G31 31行7列2.本期增加金额合计
            "FixedAssets_AmortizationIL_Total": data.cell_value(31, 6),  # G32 32行7列⑴计提合计
            "FixedAssets_MergeIL_Total": data.cell_value(32, 6),  # G33 33行7列⑵企业合并增加合计
            "FixedAssets_ReduceIL_Total": data.cell_value(33, 6),  # G34 34行7列3.本期减少金额合计
            "FixedAssets_DisposalIL_Total": data.cell_value(34, 6),  # G35 35行7列⑴处置或报废合计
            "FixedAssets_CombinedToReduceIL_Total": data.cell_value(35, 6),  # G36 36行7列⑵企业合并减少合计
            "FixedAssets_ThisIL_Total": data.cell_value(36, 6),  # G37 37行7列期末余额合计
            "FixedAssets_EndingBookValue_Total": data.cell_value(38, 6),  # G39 39行7列1.期末账面价值合计
            "FixedAssets_OpeningBookValue_Total": data.cell_value(39, 6),  # G40 40行7列2.期初账面价值合计
            "FixedAssets_BuildingsF_OBV": data.cell_value(52, 1),  # B53 53行2列房屋及建筑物账面原值
            "FixedAssets_MEF_OBV": data.cell_value(53, 1),# B54 54行2列机器设备账面原值
            "FixedAssets_TransportMachineF_OBV": data.cell_value(54, 1),# B55 55行2列运输工具账面原值
            "FixedAssets_ElectronicEquipmentF_OBV": data.cell_value(55, 1),# B56 56行2列电子设备账面原值
            "FixedAssets_OtherEquipmentF_OBV": data.cell_value(56, 1),  # B57 57行2列其他设备账面原值
            "FixedAssets_Total_OBV": data.cell_value(57, 1),  # B58 58行2列合计账面原值
            "FixedAssets_BuildingsF_AD": data.cell_value(52, 2),# C53 53行3列房屋及建筑物累计折旧
            "FixedAssets_MEF_AD": data.cell_value(53, 2),# C54 54行3列机器设备累计折旧
            "FixedAssets_TransportMachineF_AD": data.cell_value(54, 2),# C55 55行3列运输工具累计折旧
            "FixedAssets_ElectronicEquipmentF_AD": data.cell_value(55, 2),# C56 56行3列电子设备累计折旧
            "FixedAssets_OtherEquipmentF_AD": data.cell_value(56, 2),# C57 57行3列其他设备累计折旧
            "FixedAssets_Total_AD": data.cell_value(57, 2),  # C58 58行3列合计累计折旧
            "FixedAssets_BuildingsF_IL": data.cell_value(52, 3),  # D53 53行4列房屋及建筑物减值准备
            "FixedAssets_MEF_IL": data.cell_value(53, 3),  # D54 54行4列机器设备减值准备
            "FixedAssets_TransportMachineF_IL": data.cell_value(54, 3),  # D55 55行4列运输工具减值准备
            "FixedAssets_ElectronicEquipmentF_IL": data.cell_value(55, 3),# D56 56行4列电子设备减值准备
            "FixedAssets_OtherEquipmentF_IL": data.cell_value(56, 3),  # D57 57行4列其他设备减值准备
            "FixedAssets_Total_IL": data.cell_value(57, 3),  # D58 58行4列合计减值准备
            "FixedAssets_BuildingsF_BookValue": data.cell_value(52, 4),  # E53 53行5列房屋及建筑物账面价值
            "FixedAssets_MEF_BookValue": data.cell_value(53, 4),  # E54 54行5列机器设备账面价值
            "FixedAssets_TransportMachineF_BookValue": data.cell_value(54, 4),  # E55 55行5列运输工具账面价值
            "FixedAssets_ElectronicEquipmentF_BookValue": data.cell_value(55, 4),  # E56 56行5列电子设备账面价值
            "FixedAssets_OtherEquipmentF_BookValue": data.cell_value(56, 4),  # E57 57行5列其他设备账面价值
            "FixedAssets_Total_BookValue": data.cell_value(57, 4),  # E58 58行5列合计账面价值
            "FixedAssets_BuildingsOLEndingBookValue": data.cell_value(61, 1),  # B62 62行2列房屋及建筑物期末账面价值
            "FixedAssets_MEOLEndingBookValue": data.cell_value(62, 1),# B63 63行2列机器设备期末账面价值
            "FixedAssets_TransportMachineOLEndingBookValue": data.cell_value(63, 1),  # B64 64行2列运输工具期末账面价值
            "FixedAssets_ElectronicEquipmentOLEndingBookValue": data.cell_value(64, 1),# B65 65行2列电子设备期末账面价值
            "FixedAssets_OtherEquipmentOLEndingBookValue": data.cell_value(65, 1),  # B66 66行2列其他设备期末账面价值
            "FixedAssets_TotalEndingBookValue": data.cell_value(66, 1),  # B67 67行2列合计期末账面价值
            "FixedAssets_Project1_BookValue": data.cell_value(70, 1),  # B71 71行2列项目1账面价值
            "FixedAssets_Project2_BookValue": data.cell_value(71, 1),  # B72 72行2列项目2账面价值
            "FixedAssets_Project3_BookValue": data.cell_value(72, 1),  # B73 73行2列项目3账面价值
            "FixedAssets_Project4_BookValue": data.cell_value(73, 1),  # B74 74行2列项目4账面价值
            "FixedAssets_Project5_BookValue": data.cell_value(74, 1),  # B75 75行2列项目5账面价值
            "FixedAssets_FixedAssetsLiquidationProject1_this": data.cell_value(78, 1),  # B79 79行2列项目1期末余额
            "FixedAssets_FixedAssetsLiquidationProject2_this": data.cell_value(79, 1),  # B80 80行2列项目2期末余额
            "FixedAssets_FixedAssetsLiquidationProject3_this": data.cell_value(80, 1),  # B81 81行2列项目3期末余额
            "FixedAssets_FixedAssetsLiquidationProject4_this": data.cell_value(81, 1),  # B82 82行2列项目4期末余额
            "FixedAssets_FixedAssetsLiquidationProject5_this": data.cell_value(82, 1),  # B83 83行2列项目5期末余额
            "FixedAssets_Total_this": data.cell_value(83, 1),  # B84 84行2列合计期末余额
            "FixedAssets_FixedAssetsLiquidationProject1_last": data.cell_value(78, 2),  # C79 79行3列项目1期初余额
            "FixedAssets_FixedAssetsLiquidationProject2_last": data.cell_value(79, 2),  # C80 80行3列项目2期初余额
            "FixedAssets_FixedAssetsLiquidationProject3_last": data.cell_value(80, 2),  # C81 81行3列项目3期初余额
            "FixedAssets_FixedAssetsLiquidationProject4_last": data.cell_value(81, 2),  # C82 82行3列项目4期初余额
            "FixedAssets_FixedAssetsLiquidationProject5_last": data.cell_value(82, 2),  # C83 83行3列项目5期初余额
            "FixedAssets_Total_last": data.cell_value(83, 2),  # C84 84行3列合计期初余额


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
        dic["FixedAssets_Remark"] = data.cell_value(85, 1),  # B86 86行2列说明
        dic["FixedAssets_BuildingsIdle_remark"] = data.cell_value(43, 5),  # F44 44行6列房屋及建筑物备注
        dic["FixedAssets_MEIdle"] = data.cell_value(44, 5),  # F45 45行6列机器设备备注
        dic["FixedAssets_TransportMachineIdle"] = data.cell_value(45, 5),  # F46 46行6列运输工具备注
        dic["FixedAssets_ElectronicEquipmentIdle"] = data.cell_value(46, 5),  # F47 47行6列电子设备备注
        dic["FixedAssets_OtherEquipmentIdle"] = data.cell_value(47, 5),  # F48 48行6列其他设备备注
        dic["FixedAssets_Project1_reason"] = data.cell_value(70, 2),  # C71 71行3列项目1未办妥产权证书原因
        dic["FixedAssets_Project2_reason"] = data.cell_value(71, 2),  # C72 72行3列项目2未办妥产权证书原因
        dic["FixedAssets_Project3_reason"] = data.cell_value(72, 2),  # C73 73行3列项目3未办妥产权证书原因
        dic["FixedAssets_Project4_reason"] = data.cell_value(73, 2),  # C74 74行3列项目4未办妥产权证书原因
        dic["FixedAssets_Project5_reason"] = data.cell_value(74, 2),  # C75 75行3列项目5未办妥产权证书原因
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
        # 分类期末余额:固定资产+固定资产清理=合计
        if abs(df["FixedAssets_FixedAssets_this"].fillna(0).values + df["FixedAssets_FixedAssetsLiquidation_this"].fillna(0).values - df["FixedAssets_Total1_this"].fillna(0).values) > 0.01:
            error = "分类期末余额:固定资产+固定资产清理<>合计"
            errorlist.append(error)
        # 分类期初余额:固定资产+固定资产清理=合计
        if abs(df["FixedAssets_FixedAssets_last"].fillna(0).values + df["FixedAssets_FixedAssetsLiquidation_last"].fillna(0).values - df["FixedAssets_Total2_last"].fillna(0).values) > 0.01:
            error = "分类期初余额:固定资产+固定资产清理<>合计"
            errorlist.append(error)
        # 固定资产情况账面原值期初余额：房屋及建筑物+机器设备+运输设备+电子设备+其他设备=合计
        if abs(df["FixedAssets_LastOBV_Buildings"].fillna(0).values + df["FixedAssets_LastOBV_ME"].fillna(0).values + df["FixedAssets_LastOBV_TransportMachine"].fillna(0).values + df["FixedAssets_LastOBV_ElectronicEquipment"].fillna(0).values + df["FixedAssets_LastOBV_OtherEquipment"].fillna(0).values - df["FixedAssets_LastOBV_Total"].fillna(0).values) > 0.01:
            error = "固定资产情况账面原值期初余额：房屋及建筑物+机器设备+运输设备+电子设备+其他设备<>合计"
            errorlist.append(error)
        # 固定资产情况账面原值本期增加金额：房屋及建筑物+机器设备+运输设备+电子设备+其他设备=合计
        if abs(df["FixedAssets_AddOBV_Buildings"].fillna(0).values + df["FixedAssets_AddOBV_ME"].fillna(0).values + df["FixedAssets_AddOBV_TransportMachine"].fillna(0).values + df["FixedAssets_AddOBV_ElectronicEquipment"].fillna(0).values + df["FixedAssets_AddOBV_OtherEquipment"].fillna(0).values - df["FixedAssets_AddOBV_Total"].fillna(0).values) > 0.01:
            error = "固定资产情况账面原值本期增加金额：房屋及建筑物+机器设备+运输设备+电子设备+其他设备<>合计"
            errorlist.append(error)
        # 固定资产情况账面原值本期减少金额：房屋及建筑物+机器设备+运输设备+电子设备+其他设备=合计
        if abs(df["FixedAssets_ReduceOBV_Buildings"].fillna(0).values + df["FixedAssets_ReduceOBV_ME"].fillna(0).values + df["FixedAssets_ReduceOBV_TransportMachine"].fillna(0).values + df["FixedAssets_ReduceOBV_ElectronicEquipment"].fillna(0).values + df["FixedAssets_ReduceOBV_OtherEquipment"].fillna(0).values - df["FixedAssets_ReduceOBV_Total"].fillna(0).values) > 0.01:
            error = "固定资产情况账面原值本期减少金额：房屋及建筑物+机器设备+运输设备+电子设备+其他设备<>合计"
            errorlist.append(error)
        # 固定资产情况账面原值期末余额：房屋及建筑物+机器设备+运输设备+电子设备+其他设备=合计
        if abs(df["FixedAssets_ThisOBV_Buildings"].fillna(0).values + df["FixedAssets_ThisOBV_ME"].fillna(0).values + df["FixedAssets_ThisOBV_TransportMachine"].fillna(0).values + df["FixedAssets_ThisOBV_ElectronicEquipment"].fillna(0).values + df["FixedAssets_ThisOBV_OtherEquipment"].fillna(0).values - df["FixedAssets_ThisOBV_Total"].fillna(0).values) > 0.01:
            error = "固定资产情况账面原值期末余额：房屋及建筑物+机器设备+运输设备+电子设备+其他设备<>合计"
            errorlist.append(error)
        # 固定资产情况累计折旧期初余额：房屋及建筑物+机器设备+运输设备+电子设备+其他设备=合计
        if abs(df["FixedAssets_LastAD_Buildings"].fillna(0).values + df["FixedAssets_LastAD_ME"].fillna(0).values + df["FixedAssets_LastAD_TransportMachine"].fillna(0).values + df["FixedAssets_LastAD_ElectronicEquipment"].fillna(0).values + df["FixedAssets_LastAD_OtherEquipment"].fillna(0).values - df["FixedAssets_LastAD_Total"].fillna(0).values) > 0.01:
            error = "固定资产情况累计折旧期初余额：房屋及建筑物+机器设备+运输设备+电子设备+其他设备<>合计"
            errorlist.append(error)
        # 固定资产情况累计折旧本期增加金额：房屋及建筑物+机器设备+运输设备+电子设备+其他设备=合计
        if abs(df["FixedAssets_AddAD_Buildings"].fillna(0).values + df["FixedAssets_AddAD_ME"].fillna(0).values + df["FixedAssets_AddAD_TransportMachine"].fillna(0).values + df["FixedAssets_AddAD_ElectronicEquipment"].fillna(0).values + df["FixedAssets_AddAD_OtherEquipment"].fillna(0).values - df["FixedAssets_AddAD_Total"].fillna(0).values) > 0.01:
            error = "固定资产情况累计折旧本期增加金额：房屋及建筑物+机器设备+运输设备+电子设备+其他设备<>合计"
            errorlist.append(error)
        # 固定资产情况累计折旧本期减少金额：房屋及建筑物+机器设备+运输设备+电子设备+其他设备=合计
        if abs(df["FixedAssets_ReduceAD_Buildings"].fillna(0).values + df["FixedAssets_ReduceAD_ME"].fillna(0).values + df["FixedAssets_ReduceAD_TransportMachine"].fillna(0).values + df["FixedAssets_ReduceAD_ElectronicEquipment"].fillna(0).values + df["FixedAssets_ReduceAD_OtherEquipment"].fillna(0).values - df["FixedAssets_ReduceAD_Total"].fillna(0).values) > 0.01:
            error = "固定资产情况累计折旧本期减少金额：房屋及建筑物+机器设备+运输设备+电子设备+其他设备<>合计"
            errorlist.append(error)
        # 固定资产情况累计折旧期末余额：房屋及建筑物+机器设备+运输设备+电子设备+其他设备=合计
        if abs(df["FixedAssets_ThisAD_Buildings"].fillna(0).values + df["FixedAssets_ThisAD_ME"].fillna(0).values + df["FixedAssets_ThisAD_TransportMachine"].fillna(0).values + df["FixedAssets_ThisAD_ElectronicEquipment"].fillna(0).values + df["FixedAssets_ThisAD_OtherEquipment"].fillna(0).values - df["FixedAssets_ThisAD_Total"].fillna(0).values) > 0.01:
            error = "固定资产情况累计折旧期末余额：房屋及建筑物+机器设备+运输设备+电子设备+其他设备<>合计"
            errorlist.append(error)
        # 固定资产情况减值准备期初余额：房屋及建筑物+机器设备+运输设备+电子设备+其他设备=合计
        if abs(df["FixedAssets_LastIL_Buildings"].fillna(0).values + df["FixedAssets_LastIL_ME"].fillna(0).values + df["FixedAssets_LastIL_TransportMachine"].fillna(0).values + df["FixedAssets_LastIL_ElectronicEquipment"].fillna(0).values + df["FixedAssets_LastIL_OtherEquipment"].fillna(0).values - df["FixedAssets_LastIL_Total"].fillna(0).values) > 0.01:
            error = "固定资产情况减值准备期初余额：房屋及建筑物+机器设备+运输设备+电子设备+其他设备<>合计"
            errorlist.append(error)
        # 固定资产情况减值准备本期增加金额：房屋及建筑物+机器设备+运输设备+电子设备+其他设备=合计
        if abs(df["FixedAssets_AddIL_Buildings"].fillna(0).values + df["FixedAssets_AddIL_ME"].fillna(0).values + df["FixedAssets_AddIL_TransportMachine"].fillna(0).values + df["FixedAssets_AddIL_ElectronicEquipment"].fillna(0).values + df["FixedAssets_AddIL_OtherEquipment"].fillna(0).values - df["FixedAssets_AddIL_Total"].fillna(0).values) > 0.01:
            error = "固定资产情况减值准备本期增加金额：房屋及建筑物+机器设备+运输设备+电子设备+其他设备<>合计"
            errorlist.append(error)
        # 固定资产情况减值准备本期减少金额：房屋及建筑物+机器设备+运输设备+电子设备+其他设备=合计
        if abs(df["FixedAssets_ReduceIL_Buildings"].fillna(0).values + df["FixedAssets_ReduceIL_ME"].fillna(0).values + df["FixedAssets_ReduceIL_TransportMachine"].fillna(0).values + df["FixedAssets_ReduceIL_ElectronicEquipment"].fillna(0).values + df["FixedAssets_ReduceIL_OtherEquipment"].fillna(0).values - df["FixedAssets_ReduceIL_Total"].fillna(0).values) > 0.01:
            error = "固定资产情况减值准备本期减少金额：房屋及建筑物+机器设备+运输设备+电子设备+其他设备<>合计"
            errorlist.append(error)
        # 固定资产情况减值准备期末余额：房屋及建筑物+机器设备+运输设备+电子设备+其他设备=合计
        if abs(df["FixedAssets_ThisIL_Buildings"].fillna(0).values + df["FixedAssets_ThisIL_ME"].fillna(0).values + df["FixedAssets_ThisIL_TransportMachine"].fillna(0).values + df["FixedAssets_ThisIL_ElectronicEquipment"].fillna(0).values + df["FixedAssets_ThisIL_OtherEquipment"].fillna(0).values - df["FixedAssets_ThisIL_Total"].fillna(0).values) > 0.01:
            error = "固定资产情况减值准备期末余额：房屋及建筑物+机器设备+运输设备+电子设备+其他设备<>合计"
            errorlist.append(error)
        # 固定资产情况期末账面价值：房屋及建筑物+机器设备+运输设备+电子设备+其他设备=合计
        if abs(df["FixedAssets_EndingBookValue_Buildings"].fillna(0).values + df["FixedAssets_EndingBookValue_ME"].fillna(0).values + df["FixedAssets_EndingBookValue_TransportMachine"].fillna(0).values + df["FixedAssets_EndingBookValue_ElectronicEquipment"].fillna(0).values + df["FixedAssets_EndingBookValue_OtherEquipment"].fillna(0).values - df["FixedAssets_EndingBookValue_Total"].fillna(0).values) > 0.01:
            error = "固定资产情况期末账面价值：房屋及建筑物+机器设备+运输设备+电子设备+其他设备<>合计"
            errorlist.append(error)
        # 固定资产情况期初账面价值：房屋及建筑物+机器设备+运输设备+电子设备+其他设备=合计
        if abs(df["FixedAssets_OpeningBookValue_Buildings"].fillna(0).values + df["FixedAssets_OpeningBookValue_ME"].fillna(0).values + df["FixedAssets_OpeningBookValue_TransportMachine"].fillna(0).values + df["FixedAssets_OpeningBookValue_ElectronicEquipment"].fillna(0).values + df["FixedAssets_OpeningBookValue_OtherEquipment"].fillna(0).values - df["FixedAssets_OpeningBookValue_Total"].fillna(0).values) > 0.01:
            error = "固定资产情况期初账面价值：房屋及建筑物+机器设备+运输设备+电子设备+其他设备<>合计"
            errorlist.append(error)
        # 暂时闲置的固定资产情况账面原值：房屋及建筑物+机器设备+运输设备+电子设备+其他设备=合计
        if abs(df["FixedAssets_BuildingsIdle_OBV"].fillna(0).values + df["FixedAssets_MEIdle_OBV"].fillna(0).values + df["FixedAssets_TransportMachineIdle_OBV"].fillna(0).values + df["FixedAssets_ElectronicEquipmentIdle_OBV"].fillna(0).values + df["FixedAssets_OtherEquipmentIdle_OBV"].fillna(0).values - df["FixedAssets_Total2_OBV"].fillna(0).values) > 0.01:
            error = "暂时闲置的固定资产情况账面原值：房屋及建筑物+机器设备+运输设备+电子设备+其他设备<>合计"
            errorlist.append(error)
        # 暂时闲置的固定资产情况累计折旧：房屋及建筑物+机器设备+运输设备+电子设备+其他设备=合计
        if abs(df["FixedAssets_BuildingsIdle_AD"].fillna(0).values + df["FixedAssets_MEIdle_AD"].fillna(0).values + df["FixedAssets_TransportMachineIdle_AD"].fillna(0).values + df["FixedAssets_ElectronicEquipmentIdle_AD"].fillna(0).values + df["FixedAssets_OtherEquipmentIdle_AD"].fillna(0).values - df["FixedAssets_Total3_AD"].fillna(0).values) > 0.01:
            error = "暂时闲置的固定资产情况累计折旧：房屋及建筑物+机器设备+运输设备+电子设备+其他设备<>合计"
            errorlist.append(error)
        # 暂时闲置的固定资产情况减值准备：房屋及建筑物+机器设备+运输设备+电子设备+其他设备=合计
        if abs(df["FixedAssets_BuildingsIdle_IL"].fillna(0).values + df["FixedAssets_MEIdle_IL"].fillna(0).values + df["FixedAssets_TransportMachineIdle_IL"].fillna(0).values + df["FixedAssets_ElectronicEquipmentIdle_IL"].fillna(0).values + df["FixedAssets_OtherEquipmentIdle_IL"].fillna(0).values - df["FixedAssets_Total4_IL"].fillna(0).values) > 0.01:
            error = "暂时闲置的固定资产情况减值准备：房屋及建筑物+机器设备+运输设备+电子设备+其他设备<>合计"
            errorlist.append(error)
        # 暂时闲置的固定资产情况账面价值：房屋及建筑物+机器设备+运输设备+电子设备+其他设备=合计
        if abs(df["FixedAssets_BuildingsIdle_BookValue"].fillna(0).values + df["FixedAssets_MEIdle_BookValue"].fillna(0).values + df["FixedAssets_TransportMachineIdle_BookValue"].fillna(0).values + df["FixedAssets_ElectronicEquipmentIdle_BookValue"].fillna(0).values + df["FixedAssets_OtherEquipmentIdle_BookValue"].fillna(0).values - df["FixedAssets_Total5_BookValue"].fillna(0).values) > 0.01:
            error = "暂时闲置的固定资产情况账面价值：房屋及建筑物+机器设备+运输设备+电子设备+其他设备<>合计"
            errorlist.append(error)
        # 通过融资租赁租入的固定资产情况账面原值：房屋及建筑物+机器设备+运输设备+电子设备+其他设备=合计
        if abs(df["FixedAssets_BuildingsF_OBV"].fillna(0).values + df["FixedAssets_MEF_OBV"].fillna(0).values + df["FixedAssets_TransportMachineF_OBV"].fillna(0).values + df["FixedAssets_ElectronicEquipmentF_OBV"].fillna(0).values + df["FixedAssets_OtherEquipmentF_OBV"].fillna(0).values - df["FixedAssets_Total_OBV"].fillna(0).values) > 0.01:
            error = "通过融资租赁租入的固定资产情况账面原值：房屋及建筑物+机器设备+运输设备+电子设备+其他设备<>合计"
            errorlist.append(error)
        # 通过融资租赁租入的固定资产情况累计折旧：房屋及建筑物+机器设备+运输设备+电子设备+其他设备=合计
        if abs(df["FixedAssets_BuildingsF_AD"].fillna(0).values + df["FixedAssets_MEF_AD"].fillna(0).values + df["FixedAssets_TransportMachineF_AD"].fillna(0).values + df["FixedAssets_ElectronicEquipmentF_AD"].fillna(0).values + df["FixedAssets_OtherEquipmentF_AD"].fillna(0).values - df["FixedAssets_Total_AD"].fillna(0).values) > 0.01:
            error = "通过融资租赁租入的固定资产情况累计折旧：房屋及建筑物+机器设备+运输设备+电子设备+其他设备<>合计"
            errorlist.append(error)
        # 通过融资租赁租入的固定资产情况减值准备：房屋及建筑物+机器设备+运输设备+电子设备+其他设备=合计
        if abs(df["FixedAssets_BuildingsF_IL"].fillna(0).values + df["FixedAssets_MEF_IL"].fillna(0).values + df["FixedAssets_TransportMachineF_IL"].fillna(0).values + df["FixedAssets_ElectronicEquipmentF_IL"].fillna(0).values + df["FixedAssets_OtherEquipmentF_IL"].fillna(0).values - df["FixedAssets_Total_IL"].fillna(0).values) > 0.01:
            error = "通过融资租赁租入的固定资产情况减值准备：房屋及建筑物+机器设备+运输设备+电子设备+其他设备<>合计"
            errorlist.append(error)
        # 通过融资租赁租入的固定资产情况账面价值：房屋及建筑物+机器设备+运输设备+电子设备+其他设备=合计
        if abs(df["FixedAssets_BuildingsF_BookValue"].fillna(0).values + df["FixedAssets_MEF_BookValue"].fillna(0).values + df["FixedAssets_TransportMachineF_BookValue"].fillna(0).values + df["FixedAssets_ElectronicEquipmentF_BookValue"].fillna(0).values + df["FixedAssets_OtherEquipmentF_BookValue"].fillna(0).values - df["FixedAssets_Total_BookValue"].fillna(0).values) > 0.01:
            error = "通过融资租赁租入的固定资产情况账面价值：房屋及建筑物+机器设备+运输设备+电子设备+其他设备<>合计"
            errorlist.append(error)
        # 通过经营租赁租出的固定资产情况：房屋及建筑物+机器设备+运输设备+电子设备+其他设备=合计
        if abs(df["FixedAssets_BuildingsOLEndingBookValue"].fillna(0).values + df["FixedAssets_MEOLEndingBookValue"].fillna(0).values + df["FixedAssets_TransportMachineOLEndingBookValue"].fillna(0).values + df["FixedAssets_ElectronicEquipmentOLEndingBookValue"].fillna(0).values + df["FixedAssets_OtherEquipmentOLEndingBookValue"].fillna(0).values - df["FixedAssets_TotalEndingBookValue"].fillna(0).values) > 0.01:
            error = "通过经营租赁租出的固定资产情况：房屋及建筑物+机器设备+运输设备+电子设备+其他设备<>合计"
            errorlist.append(error)
        # 固定资产清理期末余额：项目1+项目2+项目3+项目4+项目5=合计
        if abs(df["FixedAssets_FixedAssetsLiquidationProject1_this"].fillna(0).values + df["FixedAssets_FixedAssetsLiquidationProject2_this"].fillna(0).values + df["FixedAssets_FixedAssetsLiquidationProject3_this"].fillna(0).values + df["FixedAssets_FixedAssetsLiquidationProject4_this"].fillna(0).values + df["FixedAssets_FixedAssetsLiquidationProject5_this"].fillna(0).values - df["FixedAssets_Total_this"].fillna(0).values) > 0.01:
            error = "固定资产清理期末余额：项目1+项目2+项目3+项目4+项目5<>合计"
            errorlist.append(error)
        # 固定资产清理期初余额：项目1+项目2+项目3+项目4+项目5=合计
        if abs(df["FixedAssets_FixedAssetsLiquidationProject1_last"].fillna(0).values + df["FixedAssets_FixedAssetsLiquidationProject2_last"].fillna(0).values + df["FixedAssets_FixedAssetsLiquidationProject3_last"].fillna(0).values + df["FixedAssets_FixedAssetsLiquidationProject4_last"].fillna(0).values + df["FixedAssets_FixedAssetsLiquidationProject5_last"].fillna(0).values - df["FixedAssets_Total_last"].fillna(0).values) > 0.01:
            error = "固定资产清理期初余额：项目1+项目2+项目3+项目4+项目5<>合计"
            errorlist.append(error)
	
        











        return df, errorlist


if __name__ == "__main__":
    d = GetFixedAssets()