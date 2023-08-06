
import pandas as pd
from ChosenAPI.DataImport.ChangeToNum import ChangeData



class GetInventories(object):#存货
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
            "Inventories_C_RawMaterials_BB_this": data.cell_value(4, 1),  # B5 5行2列存货分类原材料期末余额账面余额
            "Inventories_C_Product_BB_this": data.cell_value(5, 1),  # B6 6行2列存货分类在产品期末余额账面余额
            "Inventories_C_InventoryGoods_BB_this": data.cell_value(6, 1),# B7 7行2列存货分类库存商品期末余额账面余额
            "Inventories_C_TurnoverMaterials_BB_this": data.cell_value(7, 1),# B8 8行2列存货分类周转材料期末余额账面余额
            "Inventories_C_DBA_BB_this": data.cell_value(8, 1),# B9 9行2列存货分类消耗性生物资产期末余额账面余额
            "Inventories_C_MP_BB_this": data.cell_value(9, 1),# B10 10行2列存货分类材料采购期末余额账面余额
            "Inventories_C_MIT_BB_this": data.cell_value(10, 1),# B11 11行2列存货分类在途物资期末余额账面余额
            "Inventories_C_MCD_BB_this": data.cell_value(11, 1),# B12 12行2列存货分类材料成本差异期末余额账面余额
            "Inventories_C_SendGoods_BB_this": data.cell_value(12, 1),# B13 13行2列存货分类发出商品期末余额账面余额
            "Inventories_C_CPD_BB_this": data.cell_value(13, 1),# B14 14行2列存货分类商品进销差价期末余额账面余额
            "Inventories_C_CPM_BB_this": data.cell_value(14, 1),# B15 15行2列存货分类委托加工物资期末余额账面余额
            "Inventories_C_PackingMaterials_BB_this": data.cell_value(15, 1),# B16 16行2列存货分类包装物期末余额账面余额
            "Inventories_C_LowValueConsumable_BB_this": data.cell_value(16, 1),# B17 17行2列存货分类低值易耗品期末余额账面余额
            "Inventories_C_CostOfProduction_BB_this": data.cell_value(17, 1),# B18 18行2列存货分类生产成本期末余额账面余额
            "Inventories_C_EC_BB_this": data.cell_value(18, 1),# B19 19行2列存货分类工程施工期末余额账面余额
            "Inventories_C_LandDevelopment_BB_this": data.cell_value(19, 1),# B20 20行2列存货分类土地开发期末余额账面余额
            "Inventories_C_HD_BB_this": data.cell_value(20, 1),# B21 21行2列存货分类房屋开发期末余额账面余额
            "Inventories_C_PE_BB_this": data.cell_value(21, 1),# B22 22行2列存货分类开发产品期末余额账面余额
            "Inventories_C_CommercialLand_BB_this": data.cell_value(22, 1),# B23 23行2列存货分类商品性土地期末余额账面余额
            "Inventories_C_LDP_BB_this": data.cell_value(23, 1),# B24 24行2列存货分类出租开发产品期末余额账面余额
            "Inventories_C_RH_BB_this": data.cell_value(24, 1),# B25 25行2列存货分类周转房期末余额账面余额
            "Inventories_C_PEInstallment_BB_this": data.cell_value(25, 1),# B26 26行2列存货分类分期收款开发产品期末余额账面余额
            "Inventories_C_HSFP_BB_this": data.cell_value(26, 1),# B27 27行2列存货分类自制半成品期末余额账面余额
            "Inventories_C_Other_BB_this": data.cell_value(27, 1),  # B28 28行2列存货分类其他期末余额账面余额
            "Inventories_C_Total_BB_this": data.cell_value(28, 1),  # B29 29行2列存货分类合计期末余额账面余额
            "Inventories_C_RawMaterials_provision_this": data.cell_value(4, 2),  # C5 5行3列存货分类原材料期末余额跌价准备
            "Inventories_C_Product_provision_this": data.cell_value(5, 2),  # C6 6行3列存货分类在产品期末余额跌价准备
            "Inventories_C_InventoryGoods_provision_this": data.cell_value(6, 2),# C7 7行3列存货分类库存商品期末余额跌价准备
            "Inventories_C_TurnoverMaterials_provision_this": data.cell_value(7, 2),# C8 8行3列存货分类周转材料期末余额跌价准备
            "Inventories_C_DBA_provision_this": data.cell_value(8, 2),# C9 9行3列存货分类消耗性生物资产期末余额跌价准备
            "Inventories_C_MP_provision_this": data.cell_value(9, 2),# C10 10行3列存货分类材料采购期末余额跌价准备
            "Inventories_C_MIT_provision_this": data.cell_value(10, 2),# C11 11行3列存货分类在途物资期末余额跌价准备
            "Inventories_C_MCD_provision_this": data.cell_value(11, 2),# C12 12行3列存货分类材料成本差异期末余额跌价准备
            "Inventories_C_SendGoods_provision_this": data.cell_value(12, 2),  # C13 13行3列存货分类发出商品期末余额跌价准备
            "Inventories_C_CPD_provision_this": data.cell_value(13, 2),# C14 14行3列存货分类商品进销差价期末余额跌价准备
            "Inventories_C_CPM_provision_this": data.cell_value(14, 2),# C15 15行3列存货分类委托加工物资期末余额跌价准备
            "Inventories_C_PackingMaterials_provision_this": data.cell_value(15, 2),# C16 16行3列存货分类包装物期末余额跌价准备
            "Inventories_C_LowValueConsumable_provision_this": data.cell_value(16, 2),# C17 17行3列存货分类低值易耗品期末余额跌价准备
            "Inventories_C_CostOfProduction_provision_this": data.cell_value(17, 2),# C18 18行3列存货分类生产成本期末余额跌价准备
            "Inventories_C_EC_provision_this": data.cell_value(18, 2),# C19 19行3列存货分类工程施工期末余额跌价准备
            "Inventories_C_LandDevelopment_provision_this": data.cell_value(19, 2),# C20 20行3列存货分类土地开发期末余额跌价准备
            "Inventories_C_HD_provision_this": data.cell_value(20, 2),# C21 21行3列存货分类房屋开发期末余额跌价准备
            "Inventories_C_PE_provision_this": data.cell_value(21, 2),# C22 22行3列存货分类开发产品期末余额跌价准备
            "Inventories_C_CommercialLand_provision_this": data.cell_value(22, 2),# C23 23行3列存货分类商品性土地期末余额跌价准备
            "Inventories_C_LDP_provision_this": data.cell_value(23, 2),# C24 24行3列存货分类出租开发产品期末余额跌价准备
            "Inventories_C_RH_provision_this": data.cell_value(24, 2),# C25 25行3列存货分类周转房期末余额跌价准备
            "Inventories_C_PEInstallment_provision_this": data.cell_value(25, 2),# C26 26行3列存货分类分期收款开发产品期末余额跌价准备
            "Inventories_C_HSFP_provision_this": data.cell_value(26, 2),# C27 27行3列存货分类自制半成品期末余额跌价准备
            "Inventories_C_Other_provision_this": data.cell_value(27, 2),  # C28 28行3列存货分类其他期末余额跌价准备
            "Inventories_C_Total_provision_this": data.cell_value(28, 2),  # C29 29行3列存货分类合计期末余额跌价准备
            "Inventories_C_RawMaterials_BV_this": data.cell_value(4, 3),  # D5 5行4列存货分类原材料期末余额账面价值
            "Inventories_C_Product_BV_this": data.cell_value(5, 3),  # D6 6行4列存货分类在产品期末余额账面价值
            "Inventories_C_InventoryGoods_BV_this": data.cell_value(6, 3),# D7 7行4列存货分类库存商品期末余额账面价值
            "Inventories_C_TurnoverMaterials_BV_this": data.cell_value(7, 3),# D8 8行4列存货分类周转材料期末余额账面价值
            "Inventories_C_DBA_BV_this": data.cell_value(8, 3),# D9 9行4列存货分类消耗性生物资产期末余额账面价值
            "Inventories_C_MP_BV_this": data.cell_value(9, 3),# D10 10行4列存货分类材料采购期末余额账面价值
            "Inventories_C_MIT_BV_this": data.cell_value(10, 3),# D11 11行4列存货分类在途物资期末余额账面价值
            "Inventories_C_MCD_BV_this": data.cell_value(11, 3),# D12 12行4列存货分类材料成本差异期末余额账面价值
            "Inventories_C_SendGoods_BV_this": data.cell_value(12, 3),  # D13 13行4列存货分类发出商品期末余额账面价值
            "Inventories_C_CPD_BV_this": data.cell_value(13, 3),# D14 14行4列存货分类商品进销差价期末余额账面价值
            "Inventories_C_CPM_BV_this": data.cell_value(14, 3),# D15 15行4列存货分类委托加工物资期末余额账面价值
            "Inventories_C_PackingMaterials_BV_this": data.cell_value(15, 3),# D16 16行4列存货分类包装物期末余额账面价值
            "Inventories_C_LowValueConsumable_BV_this": data.cell_value(16, 3),# D17 17行4列存货分类低值易耗品期末余额账面价值
            "Inventories_C_CostOfProduction_BV_this": data.cell_value(17, 3),# D18 18行4列存货分类生产成本期末余额账面价值
            "Inventories_C_EC_BV_this": data.cell_value(18, 3),# D19 19行4列存货分类工程施工期末余额账面价值
            "Inventories_C_LandDevelopment_BV_this": data.cell_value(19, 3),# D20 20行4列存货分类土地开发期末余额账面价值
            "Inventories_C_HD_BV_this": data.cell_value(20, 3),# D21 21行4列存货分类房屋开发期末余额账面价值
            "Inventories_C_PE_BV_this": data.cell_value(21, 3),# D22 22行4列存货分类开发产品期末余额账面价值
            "Inventories_C_CommercialLand_BV_this": data.cell_value(22, 3),# D23 23行4列存货分类商品性土地期末余额账面价值
            "Inventories_C_LDP_BV_this": data.cell_value(23, 3),# D24 24行4列存货分类出租开发产品期末余额账面价值
            "Inventories_C_RH_BV_this": data.cell_value(24, 3),# D25 25行4列存货分类周转房期末余额账面价值
            "Inventories_C_PEInstallment_BV_this": data.cell_value(25, 3),# D26 26行4列存货分类分期收款开发产品期末余额账面价值
            "Inventories_C_HSFP_BV_this": data.cell_value(26, 3),# D27 27行4列存货分类自制半成品期末余额账面价值
            "Inventories_C_Other_BV_this": data.cell_value(27, 3),  # D28 28行4列存货分类其他期末余额账面价值
            "Inventories_C_Total_BV_this": data.cell_value(28, 3),  # D29 29行4列存货分类合计期末余额账面价值
            "Inventories_C_RawMaterials_BB_last": data.cell_value(4, 4),  # E5 5行5列存货分类原材料期初余额账面余额
            "Inventories_C_Product_BB_last": data.cell_value(5, 4),  # E6 6行5列存货分类在产品期初余额账面余额
            "Inventories_C_InventoryGoods_BB_last": data.cell_value(6, 4),# E7 7行5列存货分类库存商品期初余额账面余额
            "Inventories_C_TurnoverMaterials_BB_last": data.cell_value(7, 4),# E8 8行5列存货分类周转材料期初余额账面余额
            "Inventories_C_DBA_BB_last": data.cell_value(8, 4),# E9 9行5列存货分类消耗性生物资产期初余额账面余额
            "Inventories_C_MP_BB_last": data.cell_value(9, 4),# E10 10行5列存货分类材料采购期初余额账面余额
            "Inventories_C_MIT_BB_last": data.cell_value(10, 4),# E11 11行5列存货分类在途物资期初余额账面余额
            "Inventories_C_MCD_BB_last": data.cell_value(11, 4),# E12 12行5列存货分类材料成本差异期初余额账面余额
            "Inventories_C_SendGoods_BB_last": data.cell_value(12, 4),# E13 13行5列存货分类发出商品期初余额账面余额
            "Inventories_C_CPD_BB_last": data.cell_value(13, 4),# E14 14行5列存货分类商品进销差价期初余额账面余额
            "Inventories_C_CPM_BB_last": data.cell_value(14, 4),# E15 15行5列存货分类委托加工物资期初余额账面余额
            "Inventories_C_PackingMaterials_BB_last": data.cell_value(15, 4),# E16 16行5列存货分类包装物期初余额账面余额
            "Inventories_C_LowValueConsumable_BB_last": data.cell_value(16, 4),# E17 17行5列存货分类低值易耗品期初余额账面余额
            "Inventories_C_CostOfProduction_BB_last": data.cell_value(17, 4),# E18 18行5列存货分类生产成本期初余额账面余额
            "Inventories_C_EC_BB_last": data.cell_value(18, 4),# E19 19行5列存货分类工程施工期初余额账面余额
            "Inventories_C_LandDevelopment_BB_last": data.cell_value(19, 4),# E20 20行5列存货分类土地开发期初余额账面余额
            "Inventories_C_HD_BB_last": data.cell_value(20, 4),# E21 21行5列存货分类房屋开发期初余额账面余额
            "Inventories_C_PE_BB_last": data.cell_value(21, 4),# E22 22行5列存货分类开发产品期初余额账面余额
            "Inventories_C_CommercialLand_BB_last": data.cell_value(22, 4),# E23 23行5列存货分类商品性土地期初余额账面余额
            "Inventories_C_LDP_BB_last": data.cell_value(23, 4),# E24 24行5列存货分类出租开发产品期初余额账面余额
            "Inventories_C_RH_BB_last": data.cell_value(24, 4),# E25 25行5列存货分类周转房期初余额账面余额
            "Inventories_C_PEInstallment_BB_last": data.cell_value(25, 4),# E26 26行5列存货分类分期收款开发产品期初余额账面余额
            "Inventories_C_HSFP_BB_last": data.cell_value(26, 4),# E27 27行5列存货分类自制半成品期初余额账面余额
            "Inventories_C_Other_BB_last": data.cell_value(27, 4),  # E28 28行5列存货分类其他期初余额账面余额
            "Inventories_C_Total_BB_last": data.cell_value(28, 4),  # E29 29行5列存货分类合计期初余额账面余额
            "Inventories_C_RawMaterials_provision_last": data.cell_value(4, 5),  # F5 5行6列存货分类原材料期初余额跌价准备
            "Inventories_C_Product_provision_last": data.cell_value(5, 5),  # F6 6行6列存货分类在产品期初余额跌价准备
            "Inventories_C_InventoryGoods_provision_last": data.cell_value(6, 5),# F7 7行6列存货分类库存商品期初余额跌价准备
            "Inventories_C_TurnoverMaterials_provision_last": data.cell_value(7, 5),# F8 8行6列存货分类周转材料期初余额跌价准备
            "Inventories_C_DBA_provision_last": data.cell_value(8, 5),# F9 9行6列存货分类消耗性生物资产期初余额跌价准备
            "Inventories_C_MP_provision_last": data.cell_value(9, 5),# F10 10行6列存货分类材料采购期初余额跌价准备
            "Inventories_C_MIT_provision_last": data.cell_value(10, 5),# F11 11行6列存货分类在途物资期初余额跌价准备
            "Inventories_C_MCD_provision_last": data.cell_value(11, 5),# F12 12行6列存货分类材料成本差异期初余额跌价准备
            "Inventories_C_SendGoods_provision_last": data.cell_value(12, 5),  # F13 13行6列存货分类发出商品期初余额跌价准备
            "Inventories_C_CPD_provision_last": data.cell_value(13, 5),# F14 14行6列存货分类商品进销差价期初余额跌价准备
            "Inventories_C_CPM_provision_last": data.cell_value(14, 5),# F15 15行6列存货分类委托加工物资期初余额跌价准备
            "Inventories_C_PackingMaterials_provision_last": data.cell_value(15, 5),# F16 16行6列存货分类包装物期初余额跌价准备
            "Inventories_C_LowValueConsumable_provision_last": data.cell_value(16, 5),# F17 17行6列存货分类低值易耗品期初余额跌价准备
            "Inventories_C_CostOfProduction_provision_last": data.cell_value(17, 5),# F18 18行6列存货分类生产成本期初余额跌价准备
            "Inventories_C_EC_provision_last": data.cell_value(18, 5),# F19 19行6列存货分类工程施工期初余额跌价准备
            "Inventories_C_LandDevelopment_provision_last": data.cell_value(19, 5),# F20 20行6列存货分类土地开发期初余额跌价准备
            "Inventories_C_HD_provision_last": data.cell_value(20, 5),# F21 21行6列存货分类房屋开发期初余额跌价准备
            "Inventories_C_PE_provision_last": data.cell_value(21, 5),# F22 22行6列存货分类开发产品期初余额跌价准备
            "Inventories_C_CommercialLand_provision_last": data.cell_value(22, 5),# F23 23行6列存货分类商品性土地期初余额跌价准备
            "Inventories_C_LDP_provision_last": data.cell_value(23, 5),# F24 24行6列存货分类出租开发产品期初余额跌价准备
            "Inventories_C_RH_provision_last": data.cell_value(24, 5),# F25 25行6列存货分类周转房期初余额跌价准备
            "Inventories_C_PEInstallment_provision_last": data.cell_value(25, 5),# F26 26行6列存货分类分期收款开发产品期初余额跌价准备
            "Inventories_C_HSFP_provision_last": data.cell_value(26, 5),# F27 27行6列存货分类自制半成品期初余额跌价准备
            "Inventories_C_Other_provision_last": data.cell_value(27, 5),  # F28 28行6列存货分类其他期初余额跌价准备
            "Inventories_C_Total_provision_last": data.cell_value(28, 5),  # F29 29行6列存货分类合计期初余额跌价准备
            "Inventories_C_RawMaterials_BV_last": data.cell_value(4, 6),  # G5 5行7列存货分类原材料期初余额账面价值
            "Inventories_C_Product_BV_last": data.cell_value(5, 6),  # G6 6行7列存货分类在产品期初余额账面价值
            "Inventories_C_InventoryGoods_BV_last": data.cell_value(6, 6),# G7 7行7列存货分类库存商品期初余额账面价值
            "Inventories_C_TurnoverMaterials_BV_last": data.cell_value(7, 6),# G8 8行7列存货分类周转材料期初余额账面价值
            "Inventories_C_DBA_BV_last": data.cell_value(8, 6),# G9 9行7列存货分类消耗性生物资产期初余额账面价值
            "Inventories_C_MP_BV_last": data.cell_value(9, 6),# G10 10行7列存货分类材料采购期初余额账面价值
            "Inventories_C_MIT_BV_last": data.cell_value(10, 6),# G11 11行7列存货分类在途物资期初余额账面价值
            "Inventories_C_MCD_BV_last": data.cell_value(11, 6),# G12 12行7列存货分类材料成本差异期初余额账面价值
            "Inventories_C_SendGoods_BV_last": data.cell_value(12, 6),  # G13 13行7列存货分类发出商品期初余额账面价值
            "Inventories_C_CPD_BV_last": data.cell_value(13, 6),# G14 14行7列存货分类商品进销差价期初余额账面价值
            "Inventories_C_CPM_BV_last": data.cell_value(14, 6),# G15 15行7列存货分类委托加工物资期初余额账面价值
            "Inventories_C_PackingMaterials_BV_last": data.cell_value(15, 6),# G16 16行7列存货分类包装物期初余额账面价值
            "Inventories_C_LowValueConsumable_BV_last": data.cell_value(16, 6),# G17 17行7列存货分类低值易耗品期初余额账面价值
            "Inventories_C_CostOfProduction_BV_last": data.cell_value(17, 6),# G18 18行7列存货分类生产成本期初余额账面价值
            "Inventories_C_EC_BV_last": data.cell_value(18, 6),# G19 19行7列存货分类工程施工期初余额账面价值
            "Inventories_C_LandDevelopment_BV_last": data.cell_value(19, 6),# G20 20行7列存货分类土地开发期初余额账面价值
            "Inventories_C_HD_BV_last": data.cell_value(20, 6),# G21 21行7列存货分类房屋开发期初余额账面价值
            "Inventories_C_PE_BV_last": data.cell_value(21, 6),# G22 22行7列存货分类开发产品期初余额账面价值
            "Inventories_C_CommercialLand_BV_last": data.cell_value(22, 6),# G23 23行7列存货分类商品性土地期初余额账面价值
            "Inventories_C_LDP_BV_last": data.cell_value(23, 6),# G24 24行7列存货分类出租开发产品期初余额账面价值
            "Inventories_C_RH_BV_last": data.cell_value(24, 6),# G25 25行7列存货分类周转房期初余额账面价值
            "Inventories_C_PEInstallment_BV_last": data.cell_value(25, 6),# G26 26行7列存货分类分期收款开发产品期初余额账面价值
            "Inventories_C_HSFP_BV_last": data.cell_value(26, 6),# G27 27行7列存货分类自制半成品期初余额账面价值
            "Inventories_C_Other_BV_last": data.cell_value(27, 6),  # G28 28行7列存货分类其他期初余额账面价值
            "Inventories_C_Total_BV_last": data.cell_value(28, 6),  # G29 29行7列存货分类合计期初余额账面价值
            "Inventories_RawMaterials_last": data.cell_value(33, 1),  # B34 34行2列存货跌价准备原材料期初余额
            "Inventories_Product_last": data.cell_value(34, 1),  # B35 35行2列存货跌价准备在产品期初余额
            "Inventories_InventoryGoods_last": data.cell_value(35, 1),  # B36 36行2列存货跌价准备库存商品期初余额
            "Inventories_TurnoverMaterials_last": data.cell_value(36, 1),  # B37 37行2列存货跌价准备周转材料期初余额
            "Inventories_DBA_last": data.cell_value(37, 1),  # B38 38行2列存货跌价准备消耗性生物资产期初余额
            "Inventories_MP_last": data.cell_value(38, 1),  # B39 39行2列存货跌价准备材料采购期初余额
            "Inventories_MIT_last": data.cell_value(39, 1),  # B40 40行2列存货跌价准备在途物资期初余额
            "Inventories_MCD_last": data.cell_value(40, 1),  # B41 41行2列存货跌价准备材料成本差异期初余额
            "Inventories_SendGoods_last": data.cell_value(41, 1),  # B42 42行2列存货跌价准备发出商品期初余额
            "Inventories_CPD_last": data.cell_value(42, 1),  # B43 43行2列存货跌价准备商品进销差价期初余额
            "Inventories_CPM_last": data.cell_value(43, 1),  # B44 44行2列存货跌价准备委托加工物资期初余额
            "Inventories_PackingMaterials_last": data.cell_value(44, 1),  # B45 45行2列存货跌价准备包装物期初余额
            "Inventories_LowValueConsumable_last": data.cell_value(45, 1),  # B46 46行2列存货跌价准备低值易耗品期初余额
            "Inventories_CostOfProduction_last": data.cell_value(46, 1),  # B47 47行2列存货跌价准备生产成本期初余额
            "Inventories_EC_last": data.cell_value(47, 1),  # B48 48行2列存货跌价准备工程施工期初余额
            "Inventories_LandDevelopment_last": data.cell_value(48, 1),  # B49 49行2列存货跌价准备土地开发期初余额
            "Inventories_HD_last": data.cell_value(49, 1),  # B50 50行2列存货跌价准备房屋开发期初余额
            "Inventories_PE_last": data.cell_value(50, 1),  # B51 51行2列存货跌价准备开发产品期初余额
            "Inventories_CommercialLand_last": data.cell_value(51, 1),  # B52 52行2列存货跌价准备商品性土地期初余额
            "Inventories_LDP_last": data.cell_value(52, 1),  # B53 53行2列存货跌价准备出租开发产品期初余额
            "Inventories_RH_last": data.cell_value(53, 1),  # B54 54行2列存货跌价准备周转房期初余额
            "Inventories_PEInstallment_last": data.cell_value(54, 1),  # B55 55行2列存货跌价准备分期收款开发产品期初余额
            "Inventories_HSFP_last": data.cell_value(55, 1),  # B56 56行2列存货跌价准备自制半成品期初余额
            "Inventories_Other_last": data.cell_value(56, 1),  # B57 57行2列存货跌价准备其他期初余额
            "Inventories_Total_last": data.cell_value(57, 1),  # B58 58行2列存货跌价准备合计期初余额
            "Inventories_RawMaterials_provision_add": data.cell_value(33, 2),  # C34 34行3列存货跌价准备原材料本期增加计提
            "Inventories_Product_provision_add": data.cell_value(34, 2),  # C35 35行3列存货跌价准备在产品本期增加计提
            "Inventories_InventoryGoods_provision_add": data.cell_value(35, 2),  # C36 36行3列存货跌价准备库存商品本期增加计提
            "Inventories_TurnoverMaterials_provision_add": data.cell_value(36, 2),  # C37 37行3列存货跌价准备周转材料本期增加计提
            "Inventories_DBA_provision_add": data.cell_value(37, 2),# C38 38行3列存货跌价准备消耗性生物资产本期增加计提
            "Inventories_MP_provision_add": data.cell_value(38, 2),  # C39 39行3列存货跌价准备材料采购本期增加计提
            "Inventories_MIT_provision_add": data.cell_value(39, 2),  # C40 40行3列存货跌价准备在途物资本期增加计提
            "Inventories_MCD_provision_add": data.cell_value(40, 2),  # C41 41行3列存货跌价准备材料成本差异本期增加计提
            "Inventories_SendGoods_provision_add": data.cell_value(41, 2),  # C42 42行3列存货跌价准备发出商品本期增加计提
            "Inventories_CPD_provision_add": data.cell_value(42, 2),  # C43 43行3列存货跌价准备商品进销差价本期增加计提
            "Inventories_CPM_provision_add": data.cell_value(43, 2),# C44 44行3列存货跌价准备委托加工物资本期增加计提
            "Inventories_PackingMaterials_provision_add": data.cell_value(44, 2),  # C45 45行3列存货跌价准备包装物本期增加计提
            "Inventories_LowValueConsumable_provision_add": data.cell_value(45, 2),  # C46 46行3列存货跌价准备低值易耗品本期增加计提
            "Inventories_CostOfProduction_provision_add": data.cell_value(46, 2),  # C47 47行3列存货跌价准备生产成本本期增加计提
            "Inventories_EC_provision_add": data.cell_value(47, 2),  # C48 48行3列存货跌价准备工程施工本期增加计提
            "Inventories_LandDevelopment_provision_add": data.cell_value(48, 2),  # C49 49行3列存货跌价准备土地开发本期增加计提
            "Inventories_HD_provision_add": data.cell_value(49, 2),  # C50 50行3列存货跌价准备房屋开发本期增加计提
            "Inventories_PE_provision_add": data.cell_value(50, 2),  # C51 51行3列存货跌价准备开发产品本期增加计提
            "Inventories_CommercialLand_provision_add": data.cell_value(51, 2),  # C52 52行3列存货跌价准备商品性土地本期增加计提
            "Inventories_LDP_provision_add": data.cell_value(52, 2),# C53 53行3列存货跌价准备出租开发产品本期增加计提
            "Inventories_RH_provision_add": data.cell_value(53, 2),  # C54 54行3列存货跌价准备周转房本期增加计提
            "Inventories_PEInstallment_provision_add": data.cell_value(54, 2),# C55 55行3列存货跌价准备分期收款开发产品本期增加计提
            "Inventories_HSFP_provision_add": data.cell_value(55, 2),# C56 56行3列存货跌价准备自制半成品本期增加计提
            "Inventories_Other_provision_add": data.cell_value(56, 2),  # C57 57行3列存货跌价准备其他本期增加计提
            "Inventories_Total_provision_add": data.cell_value(57, 2),  # C58 58行3列存货跌价准备合计本期增加计提
            "Inventories_RawMaterials_other_add": data.cell_value(33, 3),  # D34 34行4列存货跌价准备原材料本期增加其他
            "Inventories_Product_other_add": data.cell_value(34, 3),  # D35 35行4列存货跌价准备在产品本期增加其他
            "Inventories_InventoryGoods_other_add": data.cell_value(35, 3),  # D36 36行4列存货跌价准备库存商品本期增加其他
            "Inventories_TurnoverMaterials_other_add": data.cell_value(36, 3),  # D37 37行4列存货跌价准备周转材料本期增加其他
            "Inventories_DBA_other_add": data.cell_value(37, 3),  # D38 38行4列存货跌价准备消耗性生物资产本期增加其他
            "Inventories_MP_other_add": data.cell_value(38, 3),  # D39 39行4列存货跌价准备材料采购本期增加其他
            "Inventories_MIT_other_add": data.cell_value(39, 3),  # D40 40行4列存货跌价准备在途物资本期增加其他
            "Inventories_MCD_other_add": data.cell_value(40, 3),  # D41 41行4列存货跌价准备材料成本差异本期增加其他
            "Inventories_SendGoods_other_add": data.cell_value(41, 3),  # D42 42行4列存货跌价准备发出商品本期增加其他
            "Inventories_CPD_other_add": data.cell_value(42, 3),  # D43 43行4列存货跌价准备商品进销差价本期增加其他
            "Inventories_CPM_other_add": data.cell_value(43, 3),# D44 44行4列存货跌价准备委托加工物资本期增加其他
            "Inventories_PackingMaterials_other_add": data.cell_value(44, 3),  # D45 45行4列存货跌价准备包装物本期增加其他
            "Inventories_LowValueConsumable_other_add": data.cell_value(45, 3),  # D46 46行4列存货跌价准备低值易耗品本期增加其他
            "Inventories_CostOfProduction_other_add": data.cell_value(46, 3),  # D47 47行4列存货跌价准备生产成本本期增加其他
            "Inventories_EC_other_add": data.cell_value(47, 3),  # D48 48行4列存货跌价准备工程施工本期增加其他
            "Inventories_LandDevelopment_other_add": data.cell_value(48, 3),  # D49 49行4列存货跌价准备土地开发本期增加其他
            "Inventories_HD_other_add": data.cell_value(49, 3),  # D50 50行4列存货跌价准备房屋开发本期增加其他
            "Inventories_PE_other_add": data.cell_value(50, 3),  # D51 51行4列存货跌价准备开发产品本期增加其他
            "Inventories_CommercialLand_other_add": data.cell_value(51, 3),  # D52 52行4列存货跌价准备商品性土地本期增加其他
            "Inventories_LDP_other_add": data.cell_value(52, 3),  # D53 53行4列存货跌价准备出租开发产品本期增加其他
            "Inventories_RH_other_add": data.cell_value(53, 3),  # D54 54行4列存货跌价准备周转房本期增加其他
            "Inventories_PEInstallment_other_add": data.cell_value(54, 3),# D55 55行4列存货跌价准备分期收款开发产品本期增加其他
            "Inventories_HSFP_other_add": data.cell_value(55, 3),  # D56 56行4列存货跌价准备自制半成品本期增加其他
            "Inventories_Other_other_add": data.cell_value(56, 3),  # D57 57行4列存货跌价准备其他本期增加其他
            "Inventories_Total_other_add": data.cell_value(57, 3),  # D58 58行4列存货跌价准备合计本期增加其他
            "Inventories_RawMaterials_restitutio_reduce": data.cell_value(33, 4),  # E34 34行5列存货跌价准备原材料本期减少转回或转销
            "Inventories_Product_restitutio_reduce": data.cell_value(34, 4),  # E35 35行5列存货跌价准备在产品本期减少转回或转销
            "Inventories_InventoryGoods_restitutio_reduce": data.cell_value(35, 4),  # E36 36行5列存货跌价准备库存商品本期减少转回或转销
            "Inventories_TurnoverMaterials_restitutio_reduce": data.cell_value(36, 4),  # E37 37行5列存货跌价准备周转材料本期减少转回或转销
            "Inventories_DBA_restitutio_reduce": data.cell_value(37, 4),# E38 38行5列存货跌价准备消耗性生物资产本期减少转回或转销
            "Inventories_MP_restitutio_reduce": data.cell_value(38, 4),  # E39 39行5列存货跌价准备材料采购本期减少转回或转销
            "Inventories_MIT_restitutio_reduce": data.cell_value(39, 4),  # E40 40行5列存货跌价准备在途物资本期减少转回或转销
            "Inventories_MCD_restitutio_reduce": data.cell_value(40, 4),# E41 41行5列存货跌价准备材料成本差异本期减少转回或转销
            "Inventories_SendGoods_restitutio_reduce": data.cell_value(41, 4),  # E42 42行5列存货跌价准备发出商品本期减少转回或转销
            "Inventories_CPD_restitutio_reduce": data.cell_value(42, 4),# E43 43行5列存货跌价准备商品进销差价本期减少转回或转销
            "Inventories_CPM_restitutio_reduce": data.cell_value(43, 4),# E44 44行5列存货跌价准备委托加工物资本期减少转回或转销
            "Inventories_PackingMaterials_restitutio_reduce": data.cell_value(44, 4),  # E45 45行5列存货跌价准备包装物本期减少转回或转销
            "Inventories_LowValueConsumable_restitutio_reduce": data.cell_value(45, 4),  # E46 46行5列存货跌价准备低值易耗品本期减少转回或转销
            "Inventories_CostOfProduction_restitutio_reduce": data.cell_value(46, 4),  # E47 47行5列存货跌价准备生产成本本期减少转回或转销
            "Inventories_EC_restitutio_reduce": data.cell_value(47, 4),# E48 48行5列存货跌价准备工程施工本期减少转回或转销
            "Inventories_LandDevelopment_restitutio_reduce": data.cell_value(48, 4),  # E49 49行5列存货跌价准备土地开发本期减少转回或转销
            "Inventories_HD_restitutio_reduce": data.cell_value(49, 4),  # E50 50行5列存货跌价准备房屋开发本期减少转回或转销
            "Inventories_PE_restitutio_reduce": data.cell_value(50, 4),  # E51 51行5列存货跌价准备开发产品本期减少转回或转销
            "Inventories_CommercialLand_restitutio_reduce": data.cell_value(51, 4),  # E52 52行5列存货跌价准备商品性土地本期减少转回或转销
            "Inventories_LDP_restitutio_reduce": data.cell_value(52, 4),# E53 53行5列存货跌价准备出租开发产品本期减少转回或转销
            "Inventories_RH_restitutio_reduce": data.cell_value(53, 4),  # E54 54行5列存货跌价准备周转房本期减少转回或转销
            "Inventories_PEInstallment_restitutio_reduce": data.cell_value(54, 4),# E55 55行5列存货跌价准备分期收款开发产品本期减少转回或转销
            "Inventories_HSFP_restitutio_reduce": data.cell_value(55, 4),# E56 56行5列存货跌价准备自制半成品本期减少转回或转销
            "Inventories_Other_restitutio_reduce": data.cell_value(56, 4),  # E57 57行5列存货跌价准备其他本期减少转回或转销
            "Inventories_Total_restitutio_reduce": data.cell_value(57, 4),  # E58 58行5列存货跌价准备合计本期减少转回或转销
            "Inventories_RawMaterials_other_reduce": data.cell_value(33, 5),  # F34 34行6列存货跌价准备原材料本期减少其他
            "Inventories_Product_other_reduce": data.cell_value(34, 5),  # F35 35行6列存货跌价准备在产品本期减少其他
            "Inventories_InventoryGoods_other_reduce": data.cell_value(35, 5),  # F36 36行6列存货跌价准备库存商品本期减少其他
            "Inventories_TurnoverMaterials_other_reduce": data.cell_value(36, 5),  # F37 37行6列存货跌价准备周转材料本期减少其他
            "Inventories_DBA_other_reduce": data.cell_value(37, 5),# F38 38行6列存货跌价准备消耗性生物资产本期减少其他
            "Inventories_MP_other_reduce": data.cell_value(38, 5),  # F39 39行6列存货跌价准备材料采购本期减少其他
            "Inventories_MIT_other_reduce": data.cell_value(39, 5),  # F40 40行6列存货跌价准备在途物资本期减少其他
            "Inventories_MCD_other_reduce": data.cell_value(40, 5),  # F41 41行6列存货跌价准备材料成本差异本期减少其他
            "Inventories_SendGoods_other_reduce": data.cell_value(41, 5),  # F42 42行6列存货跌价准备发出商品本期减少其他
            "Inventories_CPD_other_reduce": data.cell_value(42, 5),  # F43 43行6列存货跌价准备商品进销差价本期减少其他
            "Inventories_CPM_other_reduce": data.cell_value(43, 5),# F44 44行6列存货跌价准备委托加工物资本期减少其他
            "Inventories_PackingMaterials_other_reduce": data.cell_value(44, 5),  # F45 45行6列存货跌价准备包装物本期减少其他
            "Inventories_LowValueConsumable_other_reduce": data.cell_value(45, 5),  # F46 46行6列存货跌价准备低值易耗品本期减少其他
            "Inventories_CostOfProduction_other_reduce": data.cell_value(46, 5),  # F47 47行6列存货跌价准备生产成本本期减少其他
            "Inventories_EC_other_reduce": data.cell_value(47, 5),  # F48 48行6列存货跌价准备工程施工本期减少其他
            "Inventories_LandDevelopment_other_reduce": data.cell_value(48, 5),  # F49 49行6列存货跌价准备土地开发本期减少其他
            "Inventories_HD_other_reduce": data.cell_value(49, 5),  # F50 50行6列存货跌价准备房屋开发本期减少其他
            "Inventories_PE_other_reduce": data.cell_value(50, 5),  # F51 51行6列存货跌价准备开发产品本期减少其他
            "Inventories_CommercialLand_other_reduce": data.cell_value(51, 5),  # F52 52行6列存货跌价准备商品性土地本期减少其他
            "Inventories_LDP_other_reduce": data.cell_value(52, 5),# F53 53行6列存货跌价准备出租开发产品本期减少其他
            "Inventories_RH_other_reduce": data.cell_value(53, 5),  # F54 54行6列存货跌价准备周转房本期减少其他
            "Inventories_PEInstallment_other_reduce": data.cell_value(54, 5),# F55 55行6列存货跌价准备分期收款开发产品本期减少其他
            "Inventories_HSFP_other_reduce": data.cell_value(55, 5),# F56 56行6列存货跌价准备自制半成品本期减少其他
            "Inventories_Other_other_reduce": data.cell_value(56, 5),  # F57 57行6列存货跌价准备其他本期减少其他
            "Inventories_Total_other_reduce": data.cell_value(57, 5),  # F58 58行6列存货跌价准备合计本期减少其他
            "Inventories_RawMaterials_this": data.cell_value(33, 6),  # G34 34行7列存货跌价准备原材料期末余额
            "Inventories_Product_this": data.cell_value(34, 6),  # G35 35行7列存货跌价准备在产品期末余额
            "Inventories_InventoryGoods_this": data.cell_value(35, 6),  # G36 36行7列存货跌价准备库存商品期末余额
            "Inventories_TurnoverMaterials_this": data.cell_value(36, 6),  # G37 37行7列存货跌价准备周转材料期末余额
            "Inventories_DBA_this": data.cell_value(37, 6),  # G38 38行7列存货跌价准备消耗性生物资产期末余额
            "Inventories_MP_this": data.cell_value(38, 6),  # G39 39行7列存货跌价准备材料采购期末余额
            "Inventories_MIT_this": data.cell_value(39, 6),  # G40 40行7列存货跌价准备在途物资期末余额
            "Inventories_MCD_this": data.cell_value(40, 6),  # G41 41行7列存货跌价准备材料成本差异期末余额
            "Inventories_SendGoods_this": data.cell_value(41, 6),  # G42 42行7列存货跌价准备发出商品期末余额
            "Inventories_CPD_this": data.cell_value(42, 6),  # G43 43行7列存货跌价准备商品进销差价期末余额
            "Inventories_CPM_this": data.cell_value(43, 6),  # G44 44行7列存货跌价准备委托加工物资期末余额
            "Inventories_PackingMaterials_this": data.cell_value(44, 6),  # G45 45行7列存货跌价准备包装物期末余额
            "Inventories_LowValueConsumable_this": data.cell_value(45, 6),  # G46 46行7列存货跌价准备低值易耗品期末余额
            "Inventories_CostOfProduction_this": data.cell_value(46, 6),  # G47 47行7列存货跌价准备生产成本期末余额
            "Inventories_EC_this": data.cell_value(47, 6),  # G48 48行7列存货跌价准备工程施工期末余额
            "Inventories_LandDevelopment_this": data.cell_value(48, 6),  # G49 49行7列存货跌价准备土地开发期末余额
            "Inventories_HD_this": data.cell_value(49, 6),  # G50 50行7列存货跌价准备房屋开发期末余额
            "Inventories_PE_this": data.cell_value(50, 6),  # G51 51行7列存货跌价准备开发产品期末余额
            "Inventories_CommercialLand_this": data.cell_value(51, 6),  # G52 52行7列存货跌价准备商品性土地期末余额
            "Inventories_LDP_this": data.cell_value(52, 6),  # G53 53行7列存货跌价准备出租开发产品期末余额
            "Inventories_RH_this": data.cell_value(53, 6),  # G54 54行7列存货跌价准备周转房期末余额
            "Inventories_PEInstallment_this": data.cell_value(54, 6),  # G55 55行7列存货跌价准备分期收款开发产品期末余额
            "Inventories_HSFP_this": data.cell_value(55, 6),  # G56 56行7列存货跌价准备自制半成品期末余额
            "Inventories_Other_this": data.cell_value(56, 6),  # G57 57行7列存货跌价准备其他期末余额
            "Inventories_Total_this": data.cell_value(57, 6),  # G58 58行7列存货跌价准备合计期末余额
            "Inventories_CIC_sum": data.cell_value(61, 1),  # B62 62行2列累计已发生成本金额
            "Inventories_CCGP_sum": data.cell_value(62, 1),  # B63 63行2列累计已确认毛利金额
            "Inventories_ExpectedLoss_sum": data.cell_value(63, 1),  # B64 64行2列减：预计损失金额
            "Inventories_AmountSettled_sum": data.cell_value(64, 1),  # B65 65行2列已办理结算的金额金额
            "Inventories_NoSettlement_sum": data.cell_value(65, 1),  # B66 66行2列建造合同形成的已完工未结算资产金额


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
        dic["Inventories_Remark"] = data.cell_value(67, 1),  # B68 68行2列说明
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
        # 存货分类期末余额账面余额:原材料+在产品+库存商品+周转材料+消耗性生物资产+材料采购+在途物资+材料成本差异+发出商品+商品进销差价+委托加工物资+包装物+低值易耗品+生产成本+工程施工+土地开发+房屋开发+开发产品+商品性土地+出租开发产品+周转房+分期收款开发产品+自制半成品+其他=合计
        if abs(df["Inventories_C_RawMaterials_BB_this"].fillna(0).values + df["Inventories_C_Product_BB_this"].fillna(0).values + df["Inventories_C_InventoryGoods_BB_this"].fillna(0).values + df["Inventories_C_TurnoverMaterials_BB_this"].fillna(0).values + df["Inventories_C_DBA_BB_this"].fillna(0).values + df["Inventories_C_MP_BB_this"].fillna(0).values + df["Inventories_C_MIT_BB_this"].fillna(0).values + df["Inventories_C_MCD_BB_this"].fillna(0).values + df["Inventories_C_SendGoods_BB_this"].fillna(0).values + df["Inventories_C_CPD_BB_this"].fillna(0).values + df["Inventories_C_CPM_BB_this"].fillna(0).values + df["Inventories_C_PackingMaterials_BB_this"].fillna(0).values + df["Inventories_C_LowValueConsumable_BB_this"].fillna(0).values + df["Inventories_C_CostOfProduction_BB_this"].fillna(0).values + df["Inventories_C_EC_BB_this"].fillna(0).values + df["Inventories_C_LandDevelopment_BB_this"].fillna(0).values + df["Inventories_C_HD_BB_this"].fillna(0).values + df["Inventories_C_PE_BB_this"].fillna(0).values + df["Inventories_C_CommercialLand_BB_this"].fillna(0).values + df["Inventories_C_LDP_BB_this"].fillna(0).values + df["Inventories_C_RH_BB_this"].fillna(0).values + df["Inventories_C_PEInstallment_BB_this"].fillna(0).values + df["Inventories_C_HSFP_BB_this"].fillna(0).values + df["Inventories_C_Other_BB_this"].fillna(0).values - df["Inventories_C_Total_BB_this"].fillna(0).values) > 0.01:
            error = "存货分类期末余额账面余额:原材料+在产品+库存商品+周转材料+消耗性生物资产+材料采购+在途物资+材料成本差异+发出商品+商品进销差价+委托加工物资+包装物+低值易耗品+生产成本+工程施工+土地开发+房屋开发+开发产品+商品性土地+出租开发产品+周转房+分期收款开发产品+自制半成品+其他<>合计"
            errorlist.append(error)	
        # 存货分类期末余额跌价准备:原材料+在产品+库存商品+周转材料+消耗性生物资产+材料采购+在途物资+材料成本差异+发出商品+商品进销差价+委托加工物资+包装物+低值易耗品+生产成本+工程施工+土地开发+房屋开发+开发产品+商品性土地+出租开发产品+周转房+分期收款开发产品+自制半成品+其他=合计
        if abs(df["Inventories_C_RawMaterials_provision_this"].fillna(0).values + df["Inventories_C_Product_provision_this"].fillna(0).values + df["Inventories_C_InventoryGoods_provision_this"].fillna(0).values + df["Inventories_C_TurnoverMaterials_provision_this"].fillna(0).values + df["Inventories_C_DBA_provision_this"].fillna(0).values + df["Inventories_C_MP_provision_this"].fillna(0).values + df["Inventories_C_MIT_provision_this"].fillna(0).values + df["Inventories_C_MCD_provision_this"].fillna(0).values + df["Inventories_C_SendGoods_provision_this"].fillna(0).values + df["Inventories_C_CPD_provision_this"].fillna(0).values + df["Inventories_C_CPM_provision_this"].fillna(0).values + df["Inventories_C_PackingMaterials_provision_this"].fillna(0).values + df["Inventories_C_LowValueConsumable_provision_this"].fillna(0).values + df["Inventories_C_CostOfProduction_provision_this"].fillna(0).values + df["Inventories_C_EC_provision_this"].fillna(0).values + df["Inventories_C_LandDevelopment_provision_this"].fillna(0).values + df["Inventories_C_HD_provision_this"].fillna(0).values + df["Inventories_C_PE_provision_this"].fillna(0).values + df["Inventories_C_CommercialLand_provision_this"].fillna(0).values + df["Inventories_C_LDP_provision_this"].fillna(0).values + df["Inventories_C_RH_provision_this"].fillna(0).values + df["Inventories_C_PEInstallment_provision_this"].fillna(0).values + df["Inventories_C_HSFP_provision_this"].fillna(0).values + df["Inventories_C_Other_provision_this"].fillna(0).values - df["Inventories_C_Total_provision_this"].fillna(0).values) > 0.01:
            error = "存货分类期末余额跌价准备:原材料+在产品+库存商品+周转材料+消耗性生物资产+材料采购+在途物资+材料成本差异+发出商品+商品进销差价+委托加工物资+包装物+低值易耗品+生产成本+工程施工+土地开发+房屋开发+开发产品+商品性土地+出租开发产品+周转房+分期收款开发产品+自制半成品+其他<>合计"
            errorlist.append(error)
        # 存货分类期末余额账面价值:原材料+在产品+库存商品+周转材料+消耗性生物资产+材料采购+在途物资+材料成本差异+发出商品+商品进销差价+委托加工物资+包装物+低值易耗品+生产成本+工程施工+土地开发+房屋开发+开发产品+商品性土地+出租开发产品+周转房+分期收款开发产品+自制半成品+其他=合计
        if abs(df["Inventories_C_RawMaterials_BV_this"].fillna(0).values + df["Inventories_C_Product_BV_this"].fillna(0).values + df["Inventories_C_InventoryGoods_BV_this"].fillna(0).values + df["Inventories_C_TurnoverMaterials_BV_this"].fillna(0).values + df["Inventories_C_DBA_BV_this"].fillna(0).values + df["Inventories_C_MP_BV_this"].fillna(0).values + df["Inventories_C_MIT_BV_this"].fillna(0).values + df["Inventories_C_MCD_BV_this"].fillna(0).values + df["Inventories_C_SendGoods_BV_this"].fillna(0).values + df["Inventories_C_CPD_BV_this"].fillna(0).values + df["Inventories_C_CPM_BV_this"].fillna(0).values + df["Inventories_C_PackingMaterials_BV_this"].fillna(0).values + df["Inventories_C_LowValueConsumable_BV_this"].fillna(0).values + df["Inventories_C_CostOfProduction_BV_this"].fillna(0).values + df["Inventories_C_EC_BV_this"].fillna(0).values + df["Inventories_C_LandDevelopment_BV_this"].fillna(0).values + df["Inventories_C_HD_BV_this"].fillna(0).values + df["Inventories_C_PE_BV_this"].fillna(0).values + df["Inventories_C_CommercialLand_BV_this"].fillna(0).values + df["Inventories_C_LDP_BV_this"].fillna(0).values + df["Inventories_C_RH_BV_this"].fillna(0).values + df["Inventories_C_PEInstallment_BV_this"].fillna(0).values + df["Inventories_C_HSFP_BV_this"].fillna(0).values + df["Inventories_C_Other_BV_this"].fillna(0).values - df["Inventories_C_Total_BV_this"].fillna(0).values) > 0.01:
            error = "存货分类期末余额账面价值:原材料+在产品+库存商品+周转材料+消耗性生物资产+材料采购+在途物资+材料成本差异+发出商品+商品进销差价+委托加工物资+包装物+低值易耗品+生产成本+工程施工+土地开发+房屋开发+开发产品+商品性土地+出租开发产品+周转房+分期收款开发产品+自制半成品+其他<>合计"
            errorlist.append(error)
        # 存货分类期初余额账面余额:原材料+在产品+库存商品+周转材料+消耗性生物资产+材料采购+在途物资+材料成本差异+发出商品+商品进销差价+委托加工物资+包装物+低值易耗品+生产成本+工程施工+土地开发+房屋开发+开发产品+商品性土地+出租开发产品+周转房+分期收款开发产品+自制半成品+其他=合计
        if abs(df["Inventories_C_RawMaterials_BB_last"].fillna(0).values + df["Inventories_C_Product_BB_last"].fillna(0).values + df["Inventories_C_InventoryGoods_BB_last"].fillna(0).values + df["Inventories_C_TurnoverMaterials_BB_last"].fillna(0).values + df["Inventories_C_DBA_BB_last"].fillna(0).values + df["Inventories_C_MP_BB_last"].fillna(0).values + df["Inventories_C_MIT_BB_last"].fillna(0).values + df["Inventories_C_MCD_BB_last"].fillna(0).values + df["Inventories_C_SendGoods_BB_last"].fillna(0).values + df["Inventories_C_CPD_BB_last"].fillna(0).values + df["Inventories_C_CPM_BB_last"].fillna(0).values + df["Inventories_C_PackingMaterials_BB_last"].fillna(0).values + df["Inventories_C_LowValueConsumable_BB_last"].fillna(0).values + df["Inventories_C_CostOfProduction_BB_last"].fillna(0).values + df["Inventories_C_EC_BB_last"].fillna(0).values + df["Inventories_C_LandDevelopment_BB_last"].fillna(0).values + df["Inventories_C_HD_BB_last"].fillna(0).values + df["Inventories_C_PE_BB_last"].fillna(0).values + df["Inventories_C_CommercialLand_BB_last"].fillna(0).values + df["Inventories_C_LDP_BB_last"].fillna(0).values + df["Inventories_C_RH_BB_last"].fillna(0).values + df["Inventories_C_PEInstallment_BB_last"].fillna(0).values + df["Inventories_C_HSFP_BB_last"].fillna(0).values + df["Inventories_C_Other_BB_last"].fillna(0).values - df["Inventories_C_Total_BB_last"].fillna(0).values) > 0.01:
            error = "存货分类期初余额账面余额:原材料+在产品+库存商品+周转材料+消耗性生物资产+材料采购+在途物资+材料成本差异+发出商品+商品进销差价+委托加工物资+包装物+低值易耗品+生产成本+工程施工+土地开发+房屋开发+开发产品+商品性土地+出租开发产品+周转房+分期收款开发产品+自制半成品+其他<>合计"
            errorlist.append(error)	
        # 存货分类期初余额跌价准备:原材料+在产品+库存商品+周转材料+消耗性生物资产+材料采购+在途物资+材料成本差异+发出商品+商品进销差价+委托加工物资+包装物+低值易耗品+生产成本+工程施工+土地开发+房屋开发+开发产品+商品性土地+出租开发产品+周转房+分期收款开发产品+自制半成品+其他=合计
        if abs(df["Inventories_C_RawMaterials_provision_last"].fillna(0).values + df["Inventories_C_Product_provision_last"].fillna(0).values + df["Inventories_C_InventoryGoods_provision_last"].fillna(0).values + df["Inventories_C_TurnoverMaterials_provision_last"].fillna(0).values + df["Inventories_C_DBA_provision_last"].fillna(0).values + df["Inventories_C_MP_provision_last"].fillna(0).values + df["Inventories_C_MIT_provision_last"].fillna(0).values + df["Inventories_C_MCD_provision_last"].fillna(0).values + df["Inventories_C_SendGoods_provision_last"].fillna(0).values + df["Inventories_C_CPD_provision_last"].fillna(0).values + df["Inventories_C_CPM_provision_last"].fillna(0).values + df["Inventories_C_PackingMaterials_provision_last"].fillna(0).values + df["Inventories_C_LowValueConsumable_provision_last"].fillna(0).values + df["Inventories_C_CostOfProduction_provision_last"].fillna(0).values + df["Inventories_C_EC_provision_last"].fillna(0).values + df["Inventories_C_LandDevelopment_provision_last"].fillna(0).values + df["Inventories_C_HD_provision_last"].fillna(0).values + df["Inventories_C_PE_provision_last"].fillna(0).values + df["Inventories_C_CommercialLand_provision_last"].fillna(0).values + df["Inventories_C_LDP_provision_last"].fillna(0).values + df["Inventories_C_RH_provision_last"].fillna(0).values + df["Inventories_C_PEInstallment_provision_last"].fillna(0).values + df["Inventories_C_HSFP_provision_last"].fillna(0).values + df["Inventories_C_Other_provision_last"].fillna(0).values - df["Inventories_C_Total_provision_last"].fillna(0).values) > 0.01:
            error = "存货分类期初余额跌价准备:原材料+在产品+库存商品+周转材料+消耗性生物资产+材料采购+在途物资+材料成本差异+发出商品+商品进销差价+委托加工物资+包装物+低值易耗品+生产成本+工程施工+土地开发+房屋开发+开发产品+商品性土地+出租开发产品+周转房+分期收款开发产品+自制半成品+其他<>合计"
            errorlist.append(error)
        # 存货分类期初余额账面价值:原材料+在产品+库存商品+周转材料+消耗性生物资产+材料采购+在途物资+材料成本差异+发出商品+商品进销差价+委托加工物资+包装物+低值易耗品+生产成本+工程施工+土地开发+房屋开发+开发产品+商品性土地+出租开发产品+周转房+分期收款开发产品+自制半成品+其他=合计
        if abs(df["Inventories_C_RawMaterials_BV_last"].fillna(0).values + df["Inventories_C_Product_BV_last"].fillna(0).values + df["Inventories_C_InventoryGoods_BV_last"].fillna(0).values + df["Inventories_C_TurnoverMaterials_BV_last"].fillna(0).values + df["Inventories_C_DBA_BV_last"].fillna(0).values + df["Inventories_C_MP_BV_last"].fillna(0).values + df["Inventories_C_MIT_BV_last"].fillna(0).values + df["Inventories_C_MCD_BV_last"].fillna(0).values + df["Inventories_C_SendGoods_BV_last"].fillna(0).values + df["Inventories_C_CPD_BV_last"].fillna(0).values + df["Inventories_C_CPM_BV_last"].fillna(0).values + df["Inventories_C_PackingMaterials_BV_last"].fillna(0).values + df["Inventories_C_LowValueConsumable_BV_last"].fillna(0).values + df["Inventories_C_CostOfProduction_BV_last"].fillna(0).values + df["Inventories_C_EC_BV_last"].fillna(0).values + df["Inventories_C_LandDevelopment_BV_last"].fillna(0).values + df["Inventories_C_HD_BV_last"].fillna(0).values + df["Inventories_C_PE_BV_last"].fillna(0).values + df["Inventories_C_CommercialLand_BV_last"].fillna(0).values + df["Inventories_C_LDP_BV_last"].fillna(0).values + df["Inventories_C_RH_BV_last"].fillna(0).values + df["Inventories_C_PEInstallment_BV_last"].fillna(0).values + df["Inventories_C_HSFP_BV_last"].fillna(0).values + df["Inventories_C_Other_BV_last"].fillna(0).values - df["Inventories_C_Total_BV_last"].fillna(0).values) > 0.01:
            error = "存货分类期初余额账面价值:原材料+在产品+库存商品+周转材料+消耗性生物资产+材料采购+在途物资+材料成本差异+发出商品+商品进销差价+委托加工物资+包装物+低值易耗品+生产成本+工程施工+土地开发+房屋开发+开发产品+商品性土地+出租开发产品+周转房+分期收款开发产品+自制半成品+其他<>合计"
            errorlist.append(error)
        # 存货跌价准备期初余额:原材料+在产品+库存商品+周转材料+消耗性生物资产+材料采购+在途物资+材料成本差异+发出商品+商品进销差价+委托加工物资+包装物+低值易耗品+生产成本+工程施工+土地开发+房屋开发+开发产品+商品性土地+出租开发产品+周转房+分期收款开发产品+自制半成品+其他=合计
        if abs(df["Inventories_RawMaterials_last"].fillna(0).values + df["Inventories_Product_last"].fillna(0).values + df["Inventories_InventoryGoods_last"].fillna(0).values + df["Inventories_TurnoverMaterials_last"].fillna(0).values + df["Inventories_DBA_last"].fillna(0).values + df["Inventories_MP_last"].fillna(0).values + df["Inventories_MIT_last"].fillna(0).values + df["Inventories_MCD_last"].fillna(0).values + df["Inventories_SendGoods_last"].fillna(0).values + df["Inventories_CPD_last"].fillna(0).values + df["Inventories_CPM_last"].fillna(0).values + df["Inventories_PackingMaterials_last"].fillna(0).values + df["Inventories_LowValueConsumable_last"].fillna(0).values + df["Inventories_CostOfProduction_last"].fillna(0).values + df["Inventories_EC_last"].fillna(0).values + df["Inventories_LandDevelopment_last"].fillna(0).values + df["Inventories_HD_last"].fillna(0).values + df["Inventories_PE_last"].fillna(0).values + df["Inventories_CommercialLand_last"].fillna(0).values + df["Inventories_LDP_last"].fillna(0).values + df["Inventories_RH_last"].fillna(0).values + df["Inventories_PEInstallment_last"].fillna(0).values + df["Inventories_HSFP_last"].fillna(0).values + df["Inventories_Other_last"].fillna(0).values - df["Inventories_Total_last"].fillna(0).values) > 0.01:
            error = "存货跌价准备期初余额:原材料+在产品+库存商品+周转材料+消耗性生物资产+材料采购+在途物资+材料成本差异+发出商品+商品进销差价+委托加工物资+包装物+低值易耗品+生产成本+工程施工+土地开发+房屋开发+开发产品+商品性土地+出租开发产品+周转房+分期收款开发产品+自制半成品+其他<>合计"
            errorlist.append(error)
        # 存货跌价准备本期增加计提:原材料+在产品+库存商品+周转材料+消耗性生物资产+材料采购+在途物资+材料成本差异+发出商品+商品进销差价+委托加工物资+包装物+低值易耗品+生产成本+工程施工+土地开发+房屋开发+开发产品+商品性土地+出租开发产品+周转房+分期收款开发产品+自制半成品+其他=合计
        if abs(df["Inventories_RawMaterials_provision_add"].fillna(0).values + df["Inventories_Product_provision_add"].fillna(0).values + df["Inventories_InventoryGoods_provision_add"].fillna(0).values + df["Inventories_TurnoverMaterials_provision_add"].fillna(0).values + df["Inventories_DBA_provision_add"].fillna(0).values + df["Inventories_MP_provision_add"].fillna(0).values + df["Inventories_MIT_provision_add"].fillna(0).values + df["Inventories_MCD_provision_add"].fillna(0).values + df["Inventories_SendGoods_provision_add"].fillna(0).values + df["Inventories_CPD_provision_add"].fillna(0).values + df["Inventories_CPM_provision_add"].fillna(0).values + df["Inventories_PackingMaterials_provision_add"].fillna(0).values + df["Inventories_LowValueConsumable_provision_add"].fillna(0).values + df["Inventories_CostOfProduction_provision_add"].fillna(0).values + df["Inventories_EC_provision_add"].fillna(0).values + df["Inventories_LandDevelopment_provision_add"].fillna(0).values + df["Inventories_HD_provision_add"].fillna(0).values + df["Inventories_PE_provision_add"].fillna(0).values + df["Inventories_CommercialLand_provision_add"].fillna(0).values + df["Inventories_LDP_provision_add"].fillna(0).values + df["Inventories_RH_provision_add"].fillna(0).values + df["Inventories_PEInstallment_provision_add"].fillna(0).values + df["Inventories_HSFP_provision_add"].fillna(0).values + df["Inventories_Other_provision_add"].fillna(0).values - df["Inventories_Total_provision_add"].fillna(0).values) > 0.01:
            error = "存货跌价准备本期增加计提:原材料+在产品+库存商品+周转材料+消耗性生物资产+材料采购+在途物资+材料成本差异+发出商品+商品进销差价+委托加工物资+包装物+低值易耗品+生产成本+工程施工+土地开发+房屋开发+开发产品+商品性土地+出租开发产品+周转房+分期收款开发产品+自制半成品+其他<>合计"
            errorlist.append(error)
        # 存货跌价准备本期增加其他:原材料+在产品+库存商品+周转材料+消耗性生物资产+材料采购+在途物资+材料成本差异+发出商品+商品进销差价+委托加工物资+包装物+低值易耗品+生产成本+工程施工+土地开发+房屋开发+开发产品+商品性土地+出租开发产品+周转房+分期收款开发产品+自制半成品+其他=合计
        if abs(df["Inventories_RawMaterials_other_add"].fillna(0).values + df["Inventories_Product_other_add"].fillna(0).values + df["Inventories_InventoryGoods_other_add"].fillna(0).values + df["Inventories_TurnoverMaterials_other_add"].fillna(0).values + df["Inventories_DBA_other_add"].fillna(0).values + df["Inventories_MP_other_add"].fillna(0).values + df["Inventories_MIT_other_add"].fillna(0).values + df["Inventories_MCD_other_add"].fillna(0).values + df["Inventories_SendGoods_other_add"].fillna(0).values + df["Inventories_CPD_other_add"].fillna(0).values + df["Inventories_CPM_other_add"].fillna(0).values + df["Inventories_PackingMaterials_other_add"].fillna(0).values + df["Inventories_LowValueConsumable_other_add"].fillna(0).values + df["Inventories_CostOfProduction_other_add"].fillna(0).values + df["Inventories_EC_other_add"].fillna(0).values + df["Inventories_LandDevelopment_other_add"].fillna(0).values + df["Inventories_HD_other_add"].fillna(0).values + df["Inventories_PE_other_add"].fillna(0).values + df["Inventories_CommercialLand_other_add"].fillna(0).values + df["Inventories_LDP_other_add"].fillna(0).values + df["Inventories_RH_other_add"].fillna(0).values + df["Inventories_PEInstallment_other_add"].fillna(0).values + df["Inventories_HSFP_other_add"].fillna(0).values + df["Inventories_Other_other_add"].fillna(0).values - df["Inventories_Total_other_add"].fillna(0).values) > 0.01:
            error = "存货跌价准备本期增加其他:原材料+在产品+库存商品+周转材料+消耗性生物资产+材料采购+在途物资+材料成本差异+发出商品+商品进销差价+委托加工物资+包装物+低值易耗品+生产成本+工程施工+土地开发+房屋开发+开发产品+商品性土地+出租开发产品+周转房+分期收款开发产品+自制半成品+其他<>合计"
            errorlist.append(error)
        # 存货跌价准备本期减少转回或转销:原材料+在产品+库存商品+周转材料+消耗性生物资产+材料采购+在途物资+材料成本差异+发出商品+商品进销差价+委托加工物资+包装物+低值易耗品+生产成本+工程施工+土地开发+房屋开发+开发产品+商品性土地+出租开发产品+周转房+分期收款开发产品+自制半成品+其他=合计
        if abs(df["Inventories_RawMaterials_restitutio_reduce"].fillna(0).values + df["Inventories_Product_restitutio_reduce"].fillna(0).values + df["Inventories_InventoryGoods_restitutio_reduce"].fillna(0).values + df["Inventories_TurnoverMaterials_restitutio_reduce"].fillna(0).values + df["Inventories_DBA_restitutio_reduce"].fillna(0).values + df["Inventories_MP_restitutio_reduce"].fillna(0).values + df["Inventories_MIT_restitutio_reduce"].fillna(0).values + df["Inventories_MCD_restitutio_reduce"].fillna(0).values + df["Inventories_SendGoods_restitutio_reduce"].fillna(0).values + df["Inventories_CPD_restitutio_reduce"].fillna(0).values + df["Inventories_CPM_restitutio_reduce"].fillna(0).values + df["Inventories_PackingMaterials_restitutio_reduce"].fillna(0).values + df["Inventories_LowValueConsumable_restitutio_reduce"].fillna(0).values + df["Inventories_CostOfProduction_restitutio_reduce"].fillna(0).values + df["Inventories_EC_restitutio_reduce"].fillna(0).values + df["Inventories_LandDevelopment_restitutio_reduce"].fillna(0).values + df["Inventories_HD_restitutio_reduce"].fillna(0).values + df["Inventories_PE_restitutio_reduce"].fillna(0).values + df["Inventories_CommercialLand_restitutio_reduce"].fillna(0).values + df["Inventories_LDP_restitutio_reduce"].fillna(0).values + df["Inventories_RH_restitutio_reduce"].fillna(0).values + df["Inventories_PEInstallment_restitutio_reduce"].fillna(0).values + df["Inventories_HSFP_restitutio_reduce"].fillna(0).values + df["Inventories_Other_restitutio_reduce"].fillna(0).values - df["Inventories_Total_restitutio_reduce"].fillna(0).values) > 0.01:
            error = "存货跌价准备本期减少转回或转销:原材料+在产品+库存商品+周转材料+消耗性生物资产+材料采购+在途物资+材料成本差异+发出商品+商品进销差价+委托加工物资+包装物+低值易耗品+生产成本+工程施工+土地开发+房屋开发+开发产品+商品性土地+出租开发产品+周转房+分期收款开发产品+自制半成品+其他<>合计"
            errorlist.append(error)
        # 存货跌价准备本期减少其他:原材料+在产品+库存商品+周转材料+消耗性生物资产+材料采购+在途物资+材料成本差异+发出商品+商品进销差价+委托加工物资+包装物+低值易耗品+生产成本+工程施工+土地开发+房屋开发+开发产品+商品性土地+出租开发产品+周转房+分期收款开发产品+自制半成品+其他=合计
        if abs(df["Inventories_RawMaterials_other_reduce"].fillna(0).values + df["Inventories_Product_other_reduce"].fillna(0).values + df["Inventories_InventoryGoods_other_reduce"].fillna(0).values + df["Inventories_TurnoverMaterials_other_reduce"].fillna(0).values + df["Inventories_DBA_other_reduce"].fillna(0).values + df["Inventories_MP_other_reduce"].fillna(0).values + df["Inventories_MIT_other_reduce"].fillna(0).values + df["Inventories_MCD_other_reduce"].fillna(0).values + df["Inventories_SendGoods_other_reduce"].fillna(0).values + df["Inventories_CPD_other_reduce"].fillna(0).values + df["Inventories_CPM_other_reduce"].fillna(0).values + df["Inventories_PackingMaterials_other_reduce"].fillna(0).values + df["Inventories_LowValueConsumable_other_reduce"].fillna(0).values + df["Inventories_CostOfProduction_other_reduce"].fillna(0).values + df["Inventories_EC_other_reduce"].fillna(0).values + df["Inventories_LandDevelopment_other_reduce"].fillna(0).values + df["Inventories_HD_other_reduce"].fillna(0).values + df["Inventories_PE_other_reduce"].fillna(0).values + df["Inventories_CommercialLand_other_reduce"].fillna(0).values + df["Inventories_LDP_other_reduce"].fillna(0).values + df["Inventories_RH_other_reduce"].fillna(0).values + df["Inventories_PEInstallment_other_reduce"].fillna(0).values + df["Inventories_HSFP_other_reduce"].fillna(0).values + df["Inventories_Other_other_reduce"].fillna(0).values - df["Inventories_Total_other_reduce"].fillna(0).values) > 0.01:
            error = "存货跌价准备本期减少其他:原材料+在产品+库存商品+周转材料+消耗性生物资产+材料采购+在途物资+材料成本差异+发出商品+商品进销差价+委托加工物资+包装物+低值易耗品+生产成本+工程施工+土地开发+房屋开发+开发产品+商品性土地+出租开发产品+周转房+分期收款开发产品+自制半成品+其他<>合计"
            errorlist.append(error)
        # 存货跌价准备期末余额:原材料+在产品+库存商品+周转材料+消耗性生物资产+材料采购+在途物资+材料成本差异+发出商品+商品进销差价+委托加工物资+包装物+低值易耗品+生产成本+工程施工+土地开发+房屋开发+开发产品+商品性土地+出租开发产品+周转房+分期收款开发产品+自制半成品+其他=合计
        if abs(df["Inventories_RawMaterials_this"].fillna(0).values + df["Inventories_Product_this"].fillna(0).values + df["Inventories_InventoryGoods_this"].fillna(0).values + df["Inventories_TurnoverMaterials_this"].fillna(0).values + df["Inventories_DBA_this"].fillna(0).values + df["Inventories_MP_this"].fillna(0).values + df["Inventories_MIT_this"].fillna(0).values + df["Inventories_MCD_this"].fillna(0).values + df["Inventories_SendGoods_this"].fillna(0).values + df["Inventories_CPD_this"].fillna(0).values + df["Inventories_CPM_this"].fillna(0).values + df["Inventories_PackingMaterials_this"].fillna(0).values + df["Inventories_LowValueConsumable_this"].fillna(0).values + df["Inventories_CostOfProduction_this"].fillna(0).values + df["Inventories_EC_this"].fillna(0).values + df["Inventories_LandDevelopment_this"].fillna(0).values + df["Inventories_HD_this"].fillna(0).values + df["Inventories_PE_this"].fillna(0).values + df["Inventories_CommercialLand_this"].fillna(0).values + df["Inventories_LDP_this"].fillna(0).values + df["Inventories_RH_this"].fillna(0).values + df["Inventories_PEInstallment_this"].fillna(0).values + df["Inventories_HSFP_this"].fillna(0).values + df["Inventories_Other_this"].fillna(0).values - df["Inventories_Total_this"].fillna(0).values) > 0.01:
            error = "存货跌价准备期末余额:原材料+在产品+库存商品+周转材料+消耗性生物资产+材料采购+在途物资+材料成本差异+发出商品+商品进销差价+委托加工物资+包装物+低值易耗品+生产成本+工程施工+土地开发+房屋开发+开发产品+商品性土地+出租开发产品+周转房+分期收款开发产品+自制半成品+其他<>合计"
            errorlist.append(error)











        return df, errorlist


if __name__ == "__main__":
    d = GetInventories()