
import pandas as pd
from ChosenAPI.DataImport.ChangeToNum import ChangeData



class GetCashFlowAdditionalInformation(object):#现金流量表补充资料
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
            "CashFlowAdditionalInformation_net_profit_CP": data.cell_value(4, 1),  # B5 5行2列净利润本期金额
            "CashFlowAdditionalInformation_PFIOA_CP": data.cell_value(5, 1),# B6 6行2列加：资产减值准备本期金额
            "CashFlowAdditionalInformation_depreciation_CP": data.cell_value(6, 1),# B7 7行2列固定资产折旧、油气资产折耗、生产性生物资产折旧本期金额
            "CashFlowAdditionalInformation_AOIA_CP": data.cell_value(7, 1),# B8 8行2列无形资产摊销本期金额
            "CashFlowAdditionalInformation_AOLTDE_CP": data.cell_value(8, 1),  # B9 9行2列长期待摊费用摊销本期金额
            "CashFlowAdditionalInformation_loss_CP": data.cell_value(9, 1),# B10 10行2列处置固定资产、无形资产和其他长期资产的损失(收益以“－”号填列)本期金额
            "CashFlowAdditionalInformation_fixed_assets_CP": data.cell_value(10, 1),# B11 11行2列固定资产报废损失(收益以“－”号填列)本期金额
            "CashFlowAdditionalInformation_FVVI_CP": data.cell_value(11, 1),# B12 12行2列公允价值变动损失(收益以“－”号填列)本期金额
            "CashFlowAdditionalInformation_FE_CP": data.cell_value(12, 1),# B13 13行2列财务费用(收益以“－”号填列)本期金额
            "CashFlowAdditionalInformation_II_CP": data.cell_value(13, 1),# B14 14行2列投资损失(收益以“－”号填列)本期金额
            "CashFlowAdditionalInformation_DTAR_CP": data.cell_value(14, 1),# B15 15行2列递延所得税资产减少(增加以“－”号填列)本期金额
            "CashFlowAdditionalInformation_DTAA_CP": data.cell_value(15, 1),# B16 16行2列递延所得税负债增加(减少以“－”号填列)本期金额
            "CashFlowAdditionalInformation_IR_CP": data.cell_value(16, 1),# B17 17行2列存货的减少(增加以“－”号填列)本期金额
            "CashFlowAdditionalInformation__reduce_CP": data.cell_value(17, 1),# B18 18行2列经营性应收项目的减少(增加以“－”号填列)本期金额
            "CashFlowAdditionalInformation__add_CP": data.cell_value(18, 1),# B19 19行2列经营性应付项目的增加(减少以“－”号填列)本期金额
            "CashFlowAdditionalInformation_Other_CP": data.cell_value(19, 1),  # B20 20行2列其他本期金额
            "CashFlowAdditionalInformation_NOCF_CP": data.cell_value(20, 1),# B21 21行2列经营活动产生的现金流量净额本期金额
            "CashFlowAdditionalInformation_DTC_CP": data.cell_value(22, 1),# B23 23行2列债务转为资本本期金额
            "CashFlowAdditionalInformation_CCB_CP": data.cell_value(23, 1),# B24 24行2列一年内到期的可转换公司债券本期金额
            "CashFlowAdditionalInformation_financing_CP": data.cell_value(24, 1),  # B25 25行2列融资租入固定资产本期金额
            "CashFlowAdditionalInformation__this_CP": data.cell_value(26, 1),  # B27 27行2列现金的期末余额本期金额
            "CashFlowAdditionalInformation__last_CP": data.cell_value(27, 1),  # B28 28行2列减：现金的期初余额本期金额
            "CashFlowAdditionalInformation_CET_CP": data.cell_value(28, 1),# B29 29行2列加：现金等价物的期末余额本期金额
            "CashFlowAdditionalInformation_CEL_CP": data.cell_value(29, 1),# B30 30行2列减：现金等价物的期初余额本期金额
            "CashFlowAdditionalInformation_CEA_CP": data.cell_value(30, 1),# B31 31行2列现金及现金等价物净增加额本期金额
            "CashFlowAdditionalInformation_net_profit_PP": data.cell_value(4, 2),  # C5 5行3列净利润上期金额
            "CashFlowAdditionalInformation_PFIOA_PP": data.cell_value(5, 2),# C6 6行3列加：资产减值准备上期金额
            "CashFlowAdditionalInformation_depreciation_PP": data.cell_value(6, 2),# C7 7行3列固定资产折旧、油气资产折耗、生产性生物资产折旧上期金额
            "CashFlowAdditionalInformation_AOIA_PP": data.cell_value(7, 2),# C8 8行3列无形资产摊销上期金额
            "CashFlowAdditionalInformation_AOLTDE_PP": data.cell_value(8, 2),  # C9 9行3列长期待摊费用摊销上期金额
            "CashFlowAdditionalInformation_loss_PP": data.cell_value(9, 2),# C10 10行3列处置固定资产、无形资产和其他长期资产的损失(收益以“－”号填列)上期金额
            "CashFlowAdditionalInformation_fixed_assets_PP": data.cell_value(10, 2),# C11 11行3列固定资产报废损失(收益以“－”号填列)上期金额
            "CashFlowAdditionalInformation_FVVI_PP": data.cell_value(11, 2),# C12 12行3列公允价值变动损失(收益以“－”号填列)上期金额
            "CashFlowAdditionalInformation_FE_PP": data.cell_value(12, 2),# C13 13行3列财务费用(收益以“－”号填列)上期金额
            "CashFlowAdditionalInformation_II_PP": data.cell_value(13, 2),# C14 14行3列投资损失(收益以“－”号填列)上期金额
            "CashFlowAdditionalInformation_DTAR_PP": data.cell_value(14, 2),# C15 15行3列递延所得税资产减少(增加以“－”号填列)上期金额
            "CashFlowAdditionalInformation_DTAA_PP": data.cell_value(15, 2),# C16 16行3列递延所得税负债增加(减少以“－”号填列)上期金额
            "CashFlowAdditionalInformation_IR_PP": data.cell_value(16, 2),# C17 17行3列存货的减少(增加以“－”号填列)上期金额
            "CashFlowAdditionalInformation__reduce_PP": data.cell_value(17, 2),# C18 18行3列经营性应收项目的减少(增加以“－”号填列)上期金额
            "CashFlowAdditionalInformation__add_PP": data.cell_value(18, 2),# C19 19行3列经营性应付项目的增加(减少以“－”号填列)上期金额
            "CashFlowAdditionalInformation_Other_PP": data.cell_value(19, 2),  # C20 20行3列其他上期金额
            "CashFlowAdditionalInformation_NOCF_PP": data.cell_value(20, 2),# C21 21行3列经营活动产生的现金流量净额上期金额
            "CashFlowAdditionalInformation_Debt to capital_PP": data.cell_value(22, 2),# C23 23行3列债务转为资本上期金额
            "CashFlowAdditionalInformation_CCB_PP": data.cell_value(23, 2),# C24 24行3列一年内到期的可转换公司债券上期金额
            "CashFlowAdditionalInformation_financing_PP": data.cell_value(24, 2),  # C25 25行3列融资租入固定资产上期金额
            "CashFlowAdditionalInformation__this_PP": data.cell_value(26, 2),  # C27 27行3列现金的期末余额上期金额
            "CashFlowAdditionalInformation__last_PP": data.cell_value(27, 2),  # C28 28行3列减：现金的期初余额上期金额
            "CashFlowAdditionalInformation_CET_PP": data.cell_value(28, 2),# C29 29行3列加：现金等价物的期末余额上期金额
            "CashFlowAdditionalInformation_CEL_PP": data.cell_value(29, 2),# C30 30行3列减：现金等价物的期初余额上期金额
            "CashFlowAdditionalInformation_CEA_PP": data.cell_value(30, 2),# C31 31行3列现金及现金等价物净增加额上期金额
            "CashFlowAdditionalInformation_pay_CP_sum": data.cell_value(34, 1),# B35 35行2列本期发生的企业合并在本期支付的现金或现金等价物金额
            "CashFlowAdditionalInformation_C1_pay_CP_sum": data.cell_value(35, 1),# B36 36行2列其中：公司1金额
            "CashFlowAdditionalInformation_C2_pay_CP_sum": data.cell_value(36, 1),# B37 37行2列      公司2金额
            "CashFlowAdditionalInformation_C3_pay_CP_sum": data.cell_value(37, 1),# B38 38行2列      公司3金额
            "CashFlowAdditionalInformation_C4_pay_CP_sum": data.cell_value(38, 1),# B39 39行2列      公司4金额
            "CashFlowAdditionalInformation_C5_pay_CP_sum": data.cell_value(39, 1),# B40 40行2列      公司5金额
            "CashFlowAdditionalInformation_pay_AD_sum": data.cell_value(40, 1),# B41 41行2列减：购买日子公司持有的现金及现金等价物金额
            "CashFlowAdditionalInformation_C1_pay_AD_sum": data.cell_value(41, 1),# B42 42行2列其中：公司1金额
            "CashFlowAdditionalInformation_C2_pay_AD_sum": data.cell_value(42, 1),# B43 43行2列      公司2金额
            "CashFlowAdditionalInformation_C3_pay_AD_sum": data.cell_value(43, 1),# B44 44行2列      公司3金额
            "CashFlowAdditionalInformation_C4_pay_AD_sum": data.cell_value(44, 1),# B45 45行2列      公司4金额
            "CashFlowAdditionalInformation_C5_pay_AD_sum": data.cell_value(45, 1),# B46 46行2列      公司5金额
            "CashFlowAdditionalInformation_pay_DTP_sum": data.cell_value(46, 1),# B47 47行2列加：以前期间发生的企业合并在本期支付的现金或现金等价物金额
            "CashFlowAdditionalInformation_C1_pay_DTP_sum": data.cell_value(47, 1),# B48 48行2列其中：公司1金额
            "CashFlowAdditionalInformation_C2_pay_DTP_sum": data.cell_value(48, 1),# B49 49行2列      公司2金额
            "CashFlowAdditionalInformation_C3_pay_DTP_sum": data.cell_value(49, 1),# B50 50行2列      公司3金额
            "CashFlowAdditionalInformation_C4_pay_DTP_sum": data.cell_value(50, 1),# B51 51行2列      公司4金额
            "CashFlowAdditionalInformation_C5_pay_DTP_sum": data.cell_value(51, 1),# B52 52行2列      公司5金额
            "CashFlowAdditionalInformation_pay_net_sum": data.cell_value(52, 1),  # B53 53行2列取得子公司支付的现金净额金额
            "CashFlowAdditionalInformation_received_CP_sum": data.cell_value(56, 1),# B57 57行2列本期处置子公司在本期收到的现金或现金等价物金额
            "CashFlowAdditionalInformation_C1_received_CP_sum": data.cell_value(57, 1),# B58 58行2列其中：公司1金额
            "CashFlowAdditionalInformation_C2_received_CP_sum": data.cell_value(58, 1),# B59 59行2列      公司2金额
            "CashFlowAdditionalInformation_C3_received_CP_sum": data.cell_value(59, 1),# B60 60行2列      公司3金额
            "CashFlowAdditionalInformation_C4_received_CP_sum": data.cell_value(60, 1),# B61 61行2列      公司4金额
            "CashFlowAdditionalInformation_C5_received_CP_sum": data.cell_value(61, 1),# B62 62行2列      公司5金额
            "CashFlowAdditionalInformation_received_lose_sum": data.cell_value(62, 1),# B63 63行2列减：丧失控制权日子公司持有的现金及现金等价物金额
            "CashFlowAdditionalInformation_C1_received_lose_sum": data.cell_value(63, 1),  # B64 64行2列其中：公司1金额
            "CashFlowAdditionalInformation_C2_received_lose_sum": data.cell_value(64, 1),# B65 65行2列      公司2金额
            "CashFlowAdditionalInformation_C3_received_lose_sum": data.cell_value(65, 1),# B66 66行2列      公司3金额
            "CashFlowAdditionalInformation_C4_received_lose_sum": data.cell_value(66, 1),# B67 67行2列      公司4金额
            "CashFlowAdditionalInformation_C5_received_lose_sum": data.cell_value(67, 1),# B68 68行2列      公司5金额
            "CashFlowAdditionalInformation_received_DTP_sum": data.cell_value(68, 1),# B69 69行2列加：以前期间处置子公司在本期收到的现金或现金等价物金额
            "CashFlowAdditionalInformation_C1_received_DTP_sum": data.cell_value(69, 1),# B70 70行2列其中：公司1金额
            "CashFlowAdditionalInformation_C2_received_DTP_sum": data.cell_value(70, 1),# B71 71行2列      公司2金额
            "CashFlowAdditionalInformation_C3_received_DTP_sum": data.cell_value(71, 1),# B72 72行2列      公司3金额
            "CashFlowAdditionalInformation_C4_received_DTP_sum": data.cell_value(72, 1),# B73 73行2列      公司4金额
            "CashFlowAdditionalInformation_C5_received_DTP_sum": data.cell_value(73, 1),# B74 74行2列      公司5金额
            "CashFlowAdditionalInformation_received_net_sum": data.cell_value(74, 1),  # B75 75行2列处置子公司收到的现金净额金额
            "CashFlowAdditionalInformation_Cash_this": data.cell_value(78, 1),  # B79 79行2列一、现金期末余额
            "CashFlowAdditionalInformation_COH_this": data.cell_value(79, 1),  # B80 80行2列其中：库存现金期末余额
            "CashFlowAdditionalInformation_BD_this": data.cell_value(80, 1),# B81 81行2列　　可随时用于支付的银行存款期末余额
            "CashFlowAdditionalInformation_OCF_this": data.cell_value(81, 1),# B82 82行2列　　可随时用于支付的其他货币资金期末余额
            "CashFlowAdditionalInformation_DFCB_this": data.cell_value(82, 1),# B83 83行2列　　可用于支付的存放中央银行款项期末余额
            "CashFlowAdditionalInformation_DOBF_this": data.cell_value(83, 1),# B84 84行2列　　存放同业款项期末余额
            "CashFlowAdditionalInformation_IP_this": data.cell_value(84, 1),  # B85 85行2列　　拆放同业款项期末余额
            "CashFlowAdditionalInformation_CET": data.cell_value(85, 1),  # B86 86行2列二、现金等价物期末余额
            "CashFlowAdditionalInformation_BI_this": data.cell_value(86, 1),# B87 87行2列其中：三个月内到期的债券投资期末余额
            "CashFlowAdditionalInformation_CET_this": data.cell_value(87, 1),# B88 88行2列三、期末现金及现金等价物余额期末余额
            "CashFlowAdditionalInformation_Restricted_this": data.cell_value(88, 1),# B89 89行2列其中：母公司或集团内子公司使用受限制的现金和现金等价物期末余额
            "CashFlowAdditionalInformation_Cash_last": data.cell_value(78, 2),  # C79 79行3列一、现金期初余额
            "CashFlowAdditionalInformation_COH_last": data.cell_value(79, 2),  # C80 80行3列其中：库存现金期初余额
            "CashFlowAdditionalInformation_BD_last": data.cell_value(80, 2),# C81 81行3列　　可随时用于支付的银行存款期初余额
            "CashFlowAdditionalInformation_OCF_last": data.cell_value(81, 2),# C82 82行3列　　可随时用于支付的其他货币资金期初余额
            "CashFlowAdditionalInformation_DFCB_last": data.cell_value(82, 2),# C83 83行3列　　可用于支付的存放中央银行款项期初余额
            "CashFlowAdditionalInformation_DOBF_last": data.cell_value(83, 2),# C84 84行3列　　存放同业款项期初余额
            "CashFlowAdditionalInformation_IP_last": data.cell_value(84, 2),  # C85 85行3列　　拆放同业款项期初余额
            "CashFlowAdditionalInformation_CEL": data.cell_value(85, 2),  # C86 86行3列二、现金等价物期初余额
            "CashFlowAdditionalInformation_BI_last": data.cell_value(86, 2),# C87 87行3列其中：三个月内到期的债券投资期初余额
            "CashFlowAdditionalInformation_CET_last": data.cell_value(87, 2),# C88 88行3列三、期末现金及现金等价物余额期初余额
            "CashFlowAdditionalInformation_Restricted_last": data.cell_value(88, 2),# C89 89行3列其中：母公司或集团内子公司使用受限制的现金和现金等价物期初余额
            "CashFlowAdditionalInformation_Remark": data.cell_value(90, 1),  # B91 91行2列说明

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
        dic["CashFlowAdditionalInformation_Remark"] = data.cell_value(90, 1),  # B91 91行2列说明
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
        # 本期金额：净利润+资产减值准备+固定资产折旧、油气资产折耗、生产性生物资产折旧+无形资产摊销+长期待摊费用摊销+处置固定资产、无形资产和其他长期资产的损失(收益以“－”号填列)+固定资产报废损失(收益以“－”号填列)+公允价值变动损失(收益以“－”号填列)+财务费用(收益以“－”号填列)+投资损失(收益以“－”号填列)+递延所得税资产减少(增加以“－”号填列)+递延所得税负债增加(减少以“－”号填列)+存货的减少(增加以“－”号填列)+经营性应收项目的减少(增加以“－”号填列)+经营性应付项目的增加(减少以“－”号填列)+其他=经营活动产生的现金流量净额
        if abs(df["CashFlowAdditionalInformation_net_profit_CP"].fillna(0).values + df["CashFlowAdditionalInformation_PFIOA_CP"].fillna(0).values + df["CashFlowAdditionalInformation_depreciation_CP"].fillna(0).values + df["CashFlowAdditionalInformation_AOIA_CP"].fillna(0).values + df["CashFlowAdditionalInformation_AOLTDE_CP"].fillna(0).values + df["CashFlowAdditionalInformation_loss_CP"].fillna(0).values + df["CashFlowAdditionalInformation_fixed_assets_CP"].fillna(0).values + df["CashFlowAdditionalInformation_FVVI_CP"].fillna(0).values + df["CashFlowAdditionalInformation_FE_CP"].fillna(0).values + df["CashFlowAdditionalInformation_II_CP"].fillna(0).values + df["CashFlowAdditionalInformation_DTAR_CP"].fillna(0).values + df["CashFlowAdditionalInformation_DTAA_CP"].fillna(0).values + df["CashFlowAdditionalInformation_IR_CP"].fillna(0).values + df["CashFlowAdditionalInformation__reduce_CP"].fillna(0).values + df["CashFlowAdditionalInformation__add_CP"].fillna(0).values + df["CashFlowAdditionalInformation_Other_CP"].fillna(0).values - df["CashFlowAdditionalInformation_NOCF_CP"].fillna(0).values) > 0.01:
            error = "本期金额：净利润+资产减值准备+固定资产折旧、油气资产折耗、生产性生物资产折旧+无形资产摊销+长期待摊费用摊销+处置固定资产、无形资产和其他长期资产的损失(收益以“－”号填列)+固定资产报废损失(收益以“－”号填列)+公允价值变动损失(收益以“－”号填列)+财务费用(收益以“－”号填列)+投资损失(收益以“－”号填列)+递延所得税资产减少(增加以“－”号填列)+递延所得税负债增加(减少以“－”号填列)+存货的减少(增加以“－”号填列)+经营性应收项目的减少(增加以“－”号填列)+经营性应付项目的增加(减少以“－”号填列)+其他<>经营活动产生的现金流量净额"
            errorlist.append(error)
        # 上期金额：净利润+资产减值准备+固定资产折旧、油气资产折耗、生产性生物资产折旧+无形资产摊销+长期待摊费用摊销+处置固定资产、无形资产和其他长期资产的损失(收益以“－”号填列)+固定资产报废损失(收益以“－”号填列)+公允价值变动损失(收益以“－”号填列)+财务费用(收益以“－”号填列)+投资损失(收益以“－”号填列)+递延所得税资产减少(增加以“－”号填列)+递延所得税负债增加(减少以“－”号填列)+存货的减少(增加以“－”号填列)+经营性应收项目的减少(增加以“－”号填列)+经营性应付项目的增加(减少以“－”号填列)+其他=经营活动产生的现金流量净额
        if abs(df["CashFlowAdditionalInformation_net_profit_PP"].fillna(0).values + df["CashFlowAdditionalInformation_PFIOA_PP"].fillna(0).values + df["CashFlowAdditionalInformation_depreciation_PP"].fillna(0).values + df["CashFlowAdditionalInformation_AOIA_PP"].fillna(0).values + df["CashFlowAdditionalInformation_AOLTDE_PP"].fillna(0).values + df["CashFlowAdditionalInformation_loss_PP"].fillna(0).values + df["CashFlowAdditionalInformation_fixed_assets_PP"].fillna(0).values + df["CashFlowAdditionalInformation_FVVI_PP"].fillna(0).values + df["CashFlowAdditionalInformation_FE_PP"].fillna(0).values + df["CashFlowAdditionalInformation_II_PP"].fillna(0).values + df["CashFlowAdditionalInformation_DTAR_PP"].fillna(0).values + df["CashFlowAdditionalInformation_DTAA_PP"].fillna(0).values + df["CashFlowAdditionalInformation_IR_PP"].fillna(0).values + df["CashFlowAdditionalInformation__reduce_PP"].fillna(0).values + df["CashFlowAdditionalInformation__add_PP"].fillna(0).values + df["CashFlowAdditionalInformation_Other_PP"].fillna(0).values - df["CashFlowAdditionalInformation_NOCF_PP"].fillna(0).values) > 0.01:
            error = "上期金额：净利润+资产减值准备+固定资产折旧、油气资产折耗、生产性生物资产折旧+无形资产摊销+长期待摊费用摊销+处置固定资产、无形资产和其他长期资产的损失(收益以“－”号填列)+固定资产报废损失(收益以“－”号填列)+公允价值变动损失(收益以“－”号填列)+财务费用(收益以“－”号填列)+投资损失(收益以“－”号填列)+递延所得税资产减少(增加以“－”号填列)+递延所得税负债增加(减少以“－”号填列)+存货的减少(增加以“－”号填列)+经营性应收项目的减少(增加以“－”号填列)+经营性应付项目的增加(减少以“－”号填列)+其他<>经营活动产生的现金流量净额"
            errorlist.append(error)
        











        return df, errorlist
        


if __name__ == "__main__":
    d = GetCashFlowAdditionalInformation()