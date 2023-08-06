
import pandas as pd
from ChosenAPI.DataImport.ChangeToNum import ChangeData



class GetDeferredTaxAssetsAndDeferredTaxLiability(object):#递延所得税资产和递延所得税费用
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
            "DeferredTaxAssetsAndDeferredTaxLiability_DTA_PFIOA_TD_this": data.cell_value(4, 1),  # B5 5行2列未经抵销的递延所得税资产资产减值准备可抵扣暂时性差异
            "DeferredTaxAssetsAndDeferredTaxLiability_DTA_OC_TD_this": data.cell_value(5, 1),  # B6 6行2列未经抵销的递延所得税资产开办费可抵扣暂时性差异
            "DeferredTaxAssetsAndDeferredTaxLiability_DTA_DL_TD_this": data.cell_value(6, 1),  # B7 7行2列未经抵销的递延所得税资产可抵扣亏损可抵扣暂时性差异
            "DeferredTaxAssetsAndDeferredTaxLiability_DTA_TaxD_TD_this": data.cell_value(7, 1),  # B8 8行2列未经抵销的递延所得税资产税款抵减可抵扣暂时性差异
            "DeferredTaxAssetsAndDeferredTaxLiability_DTA_U_TD_this": data.cell_value(8, 1),  # B9 9行2列未经抵销的递延所得税资产内部交易未实现利润可抵扣暂时性差异
            "DeferredTaxAssetsAndDeferredTaxLiability_DTA_PFAL_TD_this": data.cell_value(9, 1),  # B10 10行2列未经抵销的递延所得税资产因计提预计负债而确认的费用或损失可抵扣暂时性差异
            "DeferredTaxAssetsAndDeferredTaxLiability_DTA_PAWDW_TD_this": data.cell_value(10, 1),  # B11 11行2列未经抵销的递延所得税资产因计提辞退福利而确认的成本或费用可抵扣暂时性差异
            "DeferredTaxAssetsAndDeferredTaxLiability_DTA_AE_TD_this": data.cell_value(11, 1),  # B12 12行2列未经抵销的递延所得税资产超过税前扣除标准的广告费和业务宣传费支出可抵扣暂时性差异
            "DeferredTaxAssetsAndDeferredTaxLiability_DTA_EEF_TD_this": data.cell_value(12, 1),  # B13 13行2列未经抵销的递延所得税资产超过税前扣除标准的职工教育经费支出可抵扣暂时性差异
            "DeferredTaxAssetsAndDeferredTaxLiability_DTA_Total_TD_this": data.cell_value(13, 1),  # B14 14行2列未经抵销的递延所得税资产合计可抵扣暂时性差异
            "DeferredTaxAssetsAndDeferredTaxLiability_DTA_PFIOA_A_this": data.cell_value(4, 2),  # C5 5行3列未经抵销的递延所得税资产资产减值准备递延所得税资产
            "DeferredTaxAssetsAndDeferredTaxLiability_DTA_OC_A_this": data.cell_value(5, 2),  # C6 6行3列未经抵销的递延所得税资产开办费递延所得税资产
            "DeferredTaxAssetsAndDeferredTaxLiability_DTA_DL_A_this": data.cell_value(6, 2),  # C7 7行3列未经抵销的递延所得税资产可抵扣亏损递延所得税资产
            "DeferredTaxAssetsAndDeferredTaxLiability_DTA_TaxD_A_this": data.cell_value(7, 2),  # C8 8行3列未经抵销的递延所得税资产税款抵减递延所得税资产
            "DeferredTaxAssetsAndDeferredTaxLiability_DTA_U_A_this": data.cell_value(8,2),# C9 9行3列未经抵销的递延所得税资产内部交易未实现利润递延所得税资产
            "DeferredTaxAssetsAndDeferredTaxLiability_DTA_PFAL_A_this": data.cell_value(9, 2),  # C10 10行3列未经抵销的递延所得税资产因计提预计负债而确认的费用或损失递延所得税资产
            "DeferredTaxAssetsAndDeferredTaxLiability_DTA_PAWDW_A_this": data.cell_value(10, 2),  # C11 11行3列未经抵销的递延所得税资产因计提辞退福利而确认的成本或费用递延所得税资产
            "DeferredTaxAssetsAndDeferredTaxLiability_DTA_AE_A_this": data.cell_value(11, 2),  # C12 12行3列未经抵销的递延所得税资产超过税前扣除标准的广告费和业务宣传费支出递延所得税资产
            "DeferredTaxAssetsAndDeferredTaxLiability_DTA_EEF_A_this": data.cell_value(12, 2),  # C13 13行3列未经抵销的递延所得税资产超过税前扣除标准的职工教育经费支出递延所得税资产
            "DeferredTaxAssetsAndDeferredTaxLiability_DTA_Total_A_this": data.cell_value(13, 2),# C14 14行3列未经抵销的递延所得税资产合计递延所得税资产
            "DeferredTaxAssetsAndDeferredTaxLiability_DTA_PFIOA_TD_last": data.cell_value(4, 3),  # D5 5行4列未经抵销的递延所得税资产资产减值准备期末余额
            "DeferredTaxAssetsAndDeferredTaxLiability_DTA_OC_TD_last": data.cell_value(5, 3),  # D6 6行4列未经抵销的递延所得税资产开办费期末余额
            "DeferredTaxAssetsAndDeferredTaxLiability_DTA_DL_TD_last": data.cell_value(6, 3),  # D7 7行4列未经抵销的递延所得税资产可抵扣亏损期末余额
            "DeferredTaxAssetsAndDeferredTaxLiability_DTA_TaxD_TD_last": data.cell_value(7, 3),  # D8 8行4列未经抵销的递延所得税资产税款抵减期末余额
            "DeferredTaxAssetsAndDeferredTaxLiability_DTA_U_TD_last": data.cell_value(8, 3),  # D9 9行4列未经抵销的递延所得税资产内部交易未实现利润期末余额
            "DeferredTaxAssetsAndDeferredTaxLiability_DTA_PFAL_TD_last": data.cell_value(9, 3),  # D10 10行4列未经抵销的递延所得税资产因计提预计负债而确认的费用或损失期末余额
            "DeferredTaxAssetsAndDeferredTaxLiability_DTA_PAWDW_TD_last": data.cell_value(10, 3),  # D11 11行4列未经抵销的递延所得税资产因计提辞退福利而确认的成本或费用期末余额
            "DeferredTaxAssetsAndDeferredTaxLiability_DTA_AE_TD_last": data.cell_value(11, 3),  # D12 12行4列未经抵销的递延所得税资产超过税前扣除标准的广告费和业务宣传费支出期末余额
            "DeferredTaxAssetsAndDeferredTaxLiability_DTA_EEF_TD_last": data.cell_value(12, 3),  # D13 13行4列未经抵销的递延所得税资产超过税前扣除标准的职工教育经费支出期末余额
            "DeferredTaxAssetsAndDeferredTaxLiability_DTA_Total_TD_last": data.cell_value(13, 3),  # D14 14行4列未经抵销的递延所得税资产合计期末余额
            "DeferredTaxAssetsAndDeferredTaxLiability_DTA_PFIOA_A_last": data.cell_value(4, 4),  # E5 5行5列未经抵销的递延所得税资产资产减值准备期初余额
            "DeferredTaxAssetsAndDeferredTaxLiability_DTA_OC_A_last": data.cell_value(5, 4),  # E6 6行5列未经抵销的递延所得税资产开办费期初余额
            "DeferredTaxAssetsAndDeferredTaxLiability_DTA_DL_A_last": data.cell_value(6, 4),  # E7 7行5列未经抵销的递延所得税资产可抵扣亏损期初余额
            "DeferredTaxAssetsAndDeferredTaxLiability_DTA_TaxD_A_last": data.cell_value(7, 4),  # E8 8行5列未经抵销的递延所得税资产税款抵减期初余额
            "DeferredTaxAssetsAndDeferredTaxLiability_DTA_U_A_last": data.cell_value(8,4),# E9 9行5列未经抵销的递延所得税资产内部交易未实现利润期初余额
            "DeferredTaxAssetsAndDeferredTaxLiability_DTA_PFAL_A_last": data.cell_value(9, 4),  # E10 10行5列未经抵销的递延所得税资产因计提预计负债而确认的费用或损失期初余额
            "DeferredTaxAssetsAndDeferredTaxLiability_DTA_PAWDW_A_last": data.cell_value(10, 4),  # E11 11行5列未经抵销的递延所得税资产因计提辞退福利而确认的成本或费用期初余额
            "DeferredTaxAssetsAndDeferredTaxLiability_DTA_AE_A_last": data.cell_value(11, 4),  # E12 12行5列未经抵销的递延所得税资产超过税前扣除标准的广告费和业务宣传费支出期初余额
            "DeferredTaxAssetsAndDeferredTaxLiability_DTA_EEF_A_last": data.cell_value(12, 4),  # E13 13行5列未经抵销的递延所得税资产超过税前扣除标准的职工教育经费支出期初余额
            "DeferredTaxAssetsAndDeferredTaxLiability_DTA_Total_A_last": data.cell_value(13, 4),# E14 14行5列未经抵销的递延所得税资产合计期初余额
            "DeferredTaxAssetsAndDeferredTaxLiability_DTL_NI_TD_this": data.cell_value(18, 1),  # B19 19行2列未经抵销的递延所得税负债非同一控制企业合并资产评估增值应纳税暂时性差异
            "DeferredTaxAssetsAndDeferredTaxLiability_DTL_V_TD_this": data.cell_value(19, 1),  # B20 20行2列未经抵销的递延所得税负债交易性金融工具、衍生金融工具的估值应纳税暂时性差异
            "DeferredTaxAssetsAndDeferredTaxLiability_DTL_Change_TD_this": data.cell_value(20, 1),  # B21 21行2列未经抵销的递延所得税负债可供出售金融资产公允价值变动应纳税暂时性差异
            "DeferredTaxAssetsAndDeferredTaxLiability_DTL_Other_TD_this": data.cell_value(21, 1),  # B22 22行2列未经抵销的递延所得税负债其他应纳税暂时性差异
            "DeferredTaxAssetsAndDeferredTaxLiability_DTL_Total_TD_this": data.cell_value(22, 1),  # B23 23行2列未经抵销的递延所得税负债合计应纳税暂时性差异
            "DeferredTaxAssetsAndDeferredTaxLiability_DTL_NI_L_this": data.cell_value(18, 2),  # C19 19行3列未经抵销的递延所得税负债非同一控制企业合并资产评估增值递延所得税负债
            "DeferredTaxAssetsAndDeferredTaxLiability_DTL_V_L_this": data.cell_value(19, 2),  # C20 20行3列未经抵销的递延所得税负债交易性金融工具、衍生金融工具的估值递延所得税负债
            "DeferredTaxAssetsAndDeferredTaxLiability_DTL_Change_L_this": data.cell_value(20, 2),  # C21 21行3列未经抵销的递延所得税负债可供出售金融资产公允价值变动递延所得税负债
            "DeferredTaxAssetsAndDeferredTaxLiability_DTL_Other_L_this": data.cell_value(21, 2),  # C22 22行3列未经抵销的递延所得税负债其他递延所得税负债
            "DeferredTaxAssetsAndDeferredTaxLiability_DTL_Total_L_this": data.cell_value(22, 2),  # C23 23行3列未经抵销的递延所得税负债合计递延所得税负债
            "DeferredTaxAssetsAndDeferredTaxLiability_DTL_NI_TD_last": data.cell_value(18, 3),  # D19 19行4列未经抵销的递延所得税负债非同一控制企业合并资产评估增值期末余额
            "DeferredTaxAssetsAndDeferredTaxLiability_DTL_V_TD_last": data.cell_value(19, 3),  # D20 20行4列未经抵销的递延所得税负债交易性金融工具、衍生金融工具的估值期末余额
            "DeferredTaxAssetsAndDeferredTaxLiability_DTL_Change_TD_last": data.cell_value(20, 3),  # D21 21行4列未经抵销的递延所得税负债可供出售金融资产公允价值变动期末余额
            "DeferredTaxAssetsAndDeferredTaxLiability_DTL_Other_TD_last": data.cell_value(21, 3),  # D22 22行4列未经抵销的递延所得税负债其他期末余额
            "DeferredTaxAssetsAndDeferredTaxLiability_DTL_Total_TD_last": data.cell_value(22, 3),  # D23 23行4列未经抵销的递延所得税负债合计期末余额
            "DeferredTaxAssetsAndDeferredTaxLiability_DTL_NI_L_last": data.cell_value(18, 4),  # E19 19行5列未经抵销的递延所得税负债非同一控制企业合并资产评估增值期初余额
            "DeferredTaxAssetsAndDeferredTaxLiability_DTL_V_L_last": data.cell_value(19, 4),  # E20 20行5列未经抵销的递延所得税负债交易性金融工具、衍生金融工具的估值期初余额
            "DeferredTaxAssetsAndDeferredTaxLiability_DTL_Change_L_last": data.cell_value(20, 4),  # E21 21行5列未经抵销的递延所得税负债可供出售金融资产公允价值变动期初余额
            "DeferredTaxAssetsAndDeferredTaxLiability_DTL_Other_L_last": data.cell_value(21, 4),  # E22 22行5列未经抵销的递延所得税负债其他期初余额
            "DeferredTaxAssetsAndDeferredTaxLiability_DTL_Total_L_last": data.cell_value(22, 4),  # E23 23行5列未经抵销的递延所得税负债合计期初余额
            "DeferredTaxAssetsAndDeferredTaxLiability_O_A_SetOff_this": data.cell_value(27, 1),# B28 28行2列以抵销后净额列示的递延所得税资产或负债递延所得税资产递延所得税资产和负债期末互抵金额
            "DeferredTaxAssetsAndDeferredTaxLiability_O_L_SetOff_this": data.cell_value(28, 1),# B29 29行2列以抵销后净额列示的递延所得税资产或负债递延所得税负债递延所得税资产和负债期末互抵金额
            "DeferredTaxAssetsAndDeferredTaxLiability_O_A_ATO_this2": data.cell_value(27, 2),# C28 28行3列以抵销后净额列示的递延所得税资产或负债递延所得税资产抵销后递延所得税资产或负债期末金额
            "DeferredTaxAssetsAndDeferredTaxLiability_O_L_ATO_this2": data.cell_value(28,2),# C29 29行3列以抵销后净额列示的递延所得税资产或负债递延所得税负债抵销后递延所得税资产或负债期末金额
            "DeferredTaxAssetsAndDeferredTaxLiability_O_A_SetOff_last": data.cell_value(27, 3),# D28 28行4列以抵销后净额列示的递延所得税资产或负债递延所得税资产递延所得税资产和负债期初互抵金额
            "DeferredTaxAssetsAndDeferredTaxLiability_O_L_SetOff_last": data.cell_value(28, 3),# D29 29行4列以抵销后净额列示的递延所得税资产或负债递延所得税负债递延所得税资产和负债期初互抵金额
            "DeferredTaxAssetsAndDeferredTaxLiability_O_A_ATO_this": data.cell_value(27, 4),# E28 28行5列以抵销后净额列示的递延所得税资产或负债递延所得税资产抵销后递延所得税资产或负债期初金额
            "DeferredTaxAssetsAndDeferredTaxLiability_O_L_ATO_this": data.cell_value(28,4),# E29 29行5列以抵销后净额列示的递延所得税资产或负债递延所得税负债抵销后递延所得税资产或负债期初金额
            "DeferredTaxAssetsAndDeferredTaxLiability_Detail_TD_this": data.cell_value(32, 1),# B33 33行2列未确认递延所得税资产明细可抵扣暂时性差异期末余额
            "DeferredTaxAssetsAndDeferredTaxLiability_Detail_Loss_this": data.cell_value(33, 1),# B34 34行2列未确认递延所得税资产明细可抵扣亏损期末余额
            "DeferredTaxAssetsAndDeferredTaxLiability_Detail_TaxD_this": data.cell_value(34, 1),# B35 35行2列未确认递延所得税资产明细税款抵减期末余额
            "DeferredTaxAssetsAndDeferredTaxLiability_Detail_Total_this": data.cell_value(35, 1),# B36 36行2列未确认递延所得税资产明细合计期末余额
            "DeferredTaxAssetsAndDeferredTaxLiability_Detail_TD_last": data.cell_value(32, 2),# C33 33行3列未确认递延所得税资产明细可抵扣暂时性差异期初余额
            "DeferredTaxAssetsAndDeferredTaxLiability_Detail_Loss_last": data.cell_value(33, 2),# C34 34行3列未确认递延所得税资产明细可抵扣亏损期初余额
            "DeferredTaxAssetsAndDeferredTaxLiability_Detail_TaxD_last": data.cell_value(34, 2),# C35 35行3列未确认递延所得税资产明细税款抵减期初余额
            "DeferredTaxAssetsAndDeferredTaxLiability_Detail_Total_last": data.cell_value(35, 2),# C36 36行3列未确认递延所得税资产明细合计期初余额
            "DeferredTaxAssetsAndDeferredTaxLiability_Expire_20X1_this": data.cell_value(39, 1),# B40 40行2列未确认递延所得税资产的可抵扣亏损将于以下年度到期20XX期末余额
            "DeferredTaxAssetsAndDeferredTaxLiability_Expire_20X2_this": data.cell_value(40, 1),# B41 41行2列未确认递延所得税资产的可抵扣亏损将于以下年度到期20XX期末余额
            "DeferredTaxAssetsAndDeferredTaxLiability_Expire_20X3_this": data.cell_value(41, 1),# B42 42行2列未确认递延所得税资产的可抵扣亏损将于以下年度到期20XX期末余额
            "DeferredTaxAssetsAndDeferredTaxLiability_Expire_20X4_this": data.cell_value(42, 1),# B43 43行2列未确认递延所得税资产的可抵扣亏损将于以下年度到期20XX期末余额
            "DeferredTaxAssetsAndDeferredTaxLiability_Expire_20X5_this": data.cell_value(43, 1),# B44 44行2列未确认递延所得税资产的可抵扣亏损将于以下年度到期20XX期末余额
            "DeferredTaxAssetsAndDeferredTaxLiability_Expire_Total_this": data.cell_value(44, 1),# B45 45行2列未确认递延所得税资产的可抵扣亏损将于以下年度到期合计期末余额
            "DeferredTaxAssetsAndDeferredTaxLiability_Expire_20X1_last": data.cell_value(39, 2),# C40 40行3列未确认递延所得税资产的可抵扣亏损将于以下年度到期20XX期初余额
            "DeferredTaxAssetsAndDeferredTaxLiability_Expire_20X2_last": data.cell_value(40, 2),# C41 41行3列未确认递延所得税资产的可抵扣亏损将于以下年度到期20XX期初余额
            "DeferredTaxAssetsAndDeferredTaxLiability_Expire_20X3_last": data.cell_value(41, 2),# C42 42行3列未确认递延所得税资产的可抵扣亏损将于以下年度到期20XX期初余额
            "DeferredTaxAssetsAndDeferredTaxLiability_Expire_20X4_last": data.cell_value(42, 2),# C43 43行3列未确认递延所得税资产的可抵扣亏损将于以下年度到期20XX期初余额
            "DeferredTaxAssetsAndDeferredTaxLiability_Expire_20X5_last": data.cell_value(43, 2),# C44 44行3列未确认递延所得税资产的可抵扣亏损将于以下年度到期20XX期初余额
            "DeferredTaxAssetsAndDeferredTaxLiability_Expire_Total_last": data.cell_value(44, 2),# C45 45行3列未确认递延所得税资产的可抵扣亏损将于以下年度到期合计期初余额


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
        dic["DeferredTaxAssetsAndDeferredTaxLiability_Remark"] = data.cell_value(46, 1),  # B47 47行2列说明
        dic["DeferredTaxAssetsAndDeferredTaxLiability_Expire_20X1_note"] = data.cell_value(39,3),  # D40 40行4列未确认递延所得税资产的可抵扣亏损将于以下年度到期20XX备注
        dic["DeferredTaxAssetsAndDeferredTaxLiability_Expire_20X2_note"] = data.cell_value(40,3),  # D41 41行4列未确认递延所得税资产的可抵扣亏损将于以下年度到期20XX备注
        dic["DeferredTaxAssetsAndDeferredTaxLiability_Expire_20X3_note"] = data.cell_value(41,3),  # D42 42行4列未确认递延所得税资产的可抵扣亏损将于以下年度到期20XX备注
        dic["DeferredTaxAssetsAndDeferredTaxLiability_Expire_20X4_note"] = data.cell_value(42,3),  # D43 43行4列未确认递延所得税资产的可抵扣亏损将于以下年度到期20XX备注
        dic["DeferredTaxAssetsAndDeferredTaxLiability_Expire_20X5_note"] = data.cell_value(43,3),  # D44 44行4列未确认递延所得税资产的可抵扣亏损将于以下年度到期20XX备注
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
        # 未经抵销的递延所得税资产期末余额可抵扣暂时性差异：资产减值准备+开办费+可抵扣亏损+税款抵减+内部交易未实现利润+因计提预计负债而确认的费用或损失+因计提辞退福利而确认的成本或费用+超过税前扣除标准的广告费和业务宣传费支出+超过税前扣除标准的职工教育经费支出=合计
        if abs(df["DeferredTaxAssetsAndDeferredTaxLiability_DTA_PFIOA_TD_this"].fillna(0).values + df["DeferredTaxAssetsAndDeferredTaxLiability_DTA_OC_TD_this"].fillna(0).values + df["DeferredTaxAssetsAndDeferredTaxLiability_DTA_DL_TD_this"].fillna(0).values + df["DeferredTaxAssetsAndDeferredTaxLiability_DTA_TaxD_TD_this"].fillna(0).values + df["DeferredTaxAssetsAndDeferredTaxLiability_DTA_U_TD_this"].fillna(0).values + df["DeferredTaxAssetsAndDeferredTaxLiability_DTA_PFAL_TD_this"].fillna(0).values + df["DeferredTaxAssetsAndDeferredTaxLiability_DTA_PAWDW_TD_this"].fillna(0).values + df["DeferredTaxAssetsAndDeferredTaxLiability_DTA_AE_TD_this"].fillna(0).values + df["DeferredTaxAssetsAndDeferredTaxLiability_DTA_EEF_TD_this"].fillna(0).values - df["DeferredTaxAssetsAndDeferredTaxLiability_DTA_Total_TD_this"].fillna(0).values) > 0.01:
            error = "未经抵销的递延所得税资产期末余额可抵扣暂时性差异：资产减值准备+开办费+可抵扣亏损+税款抵减+内部交易未实现利润+因计提预计负债而确认的费用或损失+因计提辞退福利而确认的成本或费用+超过税前扣除标准的广告费和业务宣传费支出+超过税前扣除标准的职工教育经费支出<>合计"
            errorlist.append(error)
            # 未经抵销的递延所得税资产期末余额递延所得税资产：资产减值准备+开办费+可抵扣亏损+税款抵减+内部交易未实现利润+因计提预计负债而确认的费用或损失+因计提辞退福利而确认的成本或费用+超过税前扣除标准的广告费和业务宣传费支出+超过税前扣除标准的职工教育经费支出=合计
        if abs(df["DeferredTaxAssetsAndDeferredTaxLiability_DTA_PFIOA_A_this"].fillna(0).values + df["DeferredTaxAssetsAndDeferredTaxLiability_DTA_OC_A_this"].fillna(0).values + df["DeferredTaxAssetsAndDeferredTaxLiability_DTA_DL_A_this"].fillna(0).values + df["DeferredTaxAssetsAndDeferredTaxLiability_DTA_TaxD_A_this"].fillna(0).values + df["DeferredTaxAssetsAndDeferredTaxLiability_DTA_U_A_this"].fillna(0).values + df["DeferredTaxAssetsAndDeferredTaxLiability_DTA_PFAL_A_this"].fillna(0).values + df["DeferredTaxAssetsAndDeferredTaxLiability_DTA_PAWDW_A_this"].fillna(0).values + df["DeferredTaxAssetsAndDeferredTaxLiability_DTA_AE_A_this"].fillna(0).values + df["DeferredTaxAssetsAndDeferredTaxLiability_DTA_EEF_A_this"].fillna(0).values - df["DeferredTaxAssetsAndDeferredTaxLiability_DTA_Total_A_this"].fillna(0).values) > 0.01:
            error = "未经抵销的递延所得税资产期末余额递延所得税资产：资产减值准备+开办费+可抵扣亏损+税款抵减+内部交易未实现利润+因计提预计负债而确认的费用或损失+因计提辞退福利而确认的成本或费用+超过税前扣除标准的广告费和业务宣传费支出+超过税前扣除标准的职工教育经费支出<>合计"
            errorlist.append(error)
            # 未经抵销的递延所得税资产期初余额可抵扣暂时性差异：资产减值准备+开办费+可抵扣亏损+税款抵减+内部交易未实现利润+因计提预计负债而确认的费用或损失+因计提辞退福利而确认的成本或费用+超过税前扣除标准的广告费和业务宣传费支出+超过税前扣除标准的职工教育经费支出=合计
        if abs(df["DeferredTaxAssetsAndDeferredTaxLiability_DTA_PFIOA_TD_last"].fillna(0).values + df["DeferredTaxAssetsAndDeferredTaxLiability_DTA_OC_TD_last"].fillna(0).values + df["DeferredTaxAssetsAndDeferredTaxLiability_DTA_DL_TD_last"].fillna(0).values + df["DeferredTaxAssetsAndDeferredTaxLiability_DTA_TaxD_TD_last"].fillna(0).values + df["DeferredTaxAssetsAndDeferredTaxLiability_DTA_U_TD_last"].fillna(0).values + df["DeferredTaxAssetsAndDeferredTaxLiability_DTA_PFAL_TD_last"].fillna(0).values + df["DeferredTaxAssetsAndDeferredTaxLiability_DTA_PAWDW_TD_last"].fillna(0).values + df["DeferredTaxAssetsAndDeferredTaxLiability_DTA_AE_TD_last"].fillna(0).values + df["DeferredTaxAssetsAndDeferredTaxLiability_DTA_EEF_TD_last"].fillna(0).values - df["DeferredTaxAssetsAndDeferredTaxLiability_DTA_Total_TD_last"].fillna(0).values) > 0.01:
            error = "未经抵销的递延所得税资产期初余额可抵扣暂时性差异：资产减值准备+开办费+可抵扣亏损+税款抵减+内部交易未实现利润+因计提预计负债而确认的费用或损失+因计提辞退福利而确认的成本或费用+超过税前扣除标准的广告费和业务宣传费支出+超过税前扣除标准的职工教育经费支出<>合计"
            errorlist.append(error)
            # 未经抵销的递延所得税资产期初余额递延所得税资产：资产减值准备+开办费+可抵扣亏损+税款抵减+内部交易未实现利润+因计提预计负债而确认的费用或损失+因计提辞退福利而确认的成本或费用+超过税前扣除标准的广告费和业务宣传费支出+超过税前扣除标准的职工教育经费支出=合计
        if abs(df["DeferredTaxAssetsAndDeferredTaxLiability_DTA_PFIOA_A_last"].fillna(0).values + df["DeferredTaxAssetsAndDeferredTaxLiability_DTA_OC_A_last"].fillna(0).values + df["DeferredTaxAssetsAndDeferredTaxLiability_DTA_DL_A_last"].fillna(0).values + df["DeferredTaxAssetsAndDeferredTaxLiability_DTA_TaxD_A_last"].fillna(0).values + df["DeferredTaxAssetsAndDeferredTaxLiability_DTA_U_A_last"].fillna(0).values + df["DeferredTaxAssetsAndDeferredTaxLiability_DTA_PFAL_A_last"].fillna(0).values + df["DeferredTaxAssetsAndDeferredTaxLiability_DTA_PAWDW_A_last"].fillna(0).values + df["DeferredTaxAssetsAndDeferredTaxLiability_DTA_AE_A_last"].fillna(0).values + df["DeferredTaxAssetsAndDeferredTaxLiability_DTA_EEF_A_last"].fillna(0).values - df["DeferredTaxAssetsAndDeferredTaxLiability_DTA_Total_A_last"].fillna(0).values) > 0.01:
            error = "未经抵销的递延所得税资产期初余额递延所得税资产：资产减值准备+开办费+可抵扣亏损+税款抵减+内部交易未实现利润+因计提预计负债而确认的费用或损失+因计提辞退福利而确认的成本或费用+超过税前扣除标准的广告费和业务宣传费支出+超过税前扣除标准的职工教育经费支出<>合计"
            errorlist.append(error)
        # 未经抵销的递延所得税负债期末余额应纳税暂时性差异：非同一控制企业合并资产评估增值+交易性金融工具、衍生金融工具的估值+可供出售金融资产公允价值变动+其他=合计
        if abs(df["DeferredTaxAssetsAndDeferredTaxLiability_DTL_NI_TD_this"].fillna(0).values + df["DeferredTaxAssetsAndDeferredTaxLiability_DTL_V_TD_this"].fillna(0).values + df["DeferredTaxAssetsAndDeferredTaxLiability_DTL_Change_TD_this"].fillna(0).values + df["DeferredTaxAssetsAndDeferredTaxLiability_DTL_Other_TD_this"].fillna(0).values - df["DeferredTaxAssetsAndDeferredTaxLiability_DTL_Total_TD_this"].fillna(0).values) > 0.01:
            error = "未经抵销的递延所得税负债期末余额应纳税暂时性差异：非同一控制企业合并资产评估增值+交易性金融工具、衍生金融工具的估值+可供出售金融资产公允价值变动+其他<>合计"
            errorlist.append(error)
        # 未经抵销的递延所得税负债期末余额递延所得税负债：非同一控制企业合并资产评估增值+交易性金融工具、衍生金融工具的估值+可供出售金融资产公允价值变动+其他=合计
        if abs(df["DeferredTaxAssetsAndDeferredTaxLiability_DTL_NI_L_this"].fillna(0).values + df["DeferredTaxAssetsAndDeferredTaxLiability_DTL_V_L_this"].fillna(0).values + df["DeferredTaxAssetsAndDeferredTaxLiability_DTL_Change_L_this"].fillna(0).values + df["DeferredTaxAssetsAndDeferredTaxLiability_DTL_Other_L_this"].fillna(0).values - df["DeferredTaxAssetsAndDeferredTaxLiability_DTL_Total_L_this"].fillna(0).values) > 0.01:
            error = "未经抵销的递延所得税负债期末余额递延所得税负债：非同一控制企业合并资产评估增值+交易性金融工具、衍生金融工具的估值+可供出售金融资产公允价值变动+其他<>合计"
            errorlist.append(error)
        # 未经抵销的递延所得税负债期初余额应纳税暂时性差异：非同一控制企业合并资产评估增值+交易性金融工具、衍生金融工具的估值+可供出售金融资产公允价值变动+其他=合计
        if abs(df["DeferredTaxAssetsAndDeferredTaxLiability_DTL_NI_TD_last"].fillna(0).values + df["DeferredTaxAssetsAndDeferredTaxLiability_DTL_V_TD_last"].fillna(0).values + df["DeferredTaxAssetsAndDeferredTaxLiability_DTL_Change_TD_last"].fillna(0).values + df["DeferredTaxAssetsAndDeferredTaxLiability_DTL_Other_TD_last"].fillna(0).values - df["DeferredTaxAssetsAndDeferredTaxLiability_DTL_Total_TD_last"].fillna(0).values) > 0.01:
            error = "未经抵销的递延所得税负债期初余额应纳税暂时性差异：非同一控制企业合并资产评估增值+交易性金融工具、衍生金融工具的估值+可供出售金融资产公允价值变动+其他<>合计"
            errorlist.append(error)
        # 未经抵销的递延所得税负债期初余额递延所得税负债：非同一控制企业合并资产评估增值+交易性金融工具、衍生金融工具的估值+可供出售金融资产公允价值变动+其他=合计
        if abs(df["DeferredTaxAssetsAndDeferredTaxLiability_DTL_NI_L_last"].fillna(0).values + df["DeferredTaxAssetsAndDeferredTaxLiability_DTL_V_L_last"].fillna(0).values + df["DeferredTaxAssetsAndDeferredTaxLiability_DTL_Change_L_last"].fillna(0).values + df["DeferredTaxAssetsAndDeferredTaxLiability_DTL_Other_L_last"].fillna(0).values - df["DeferredTaxAssetsAndDeferredTaxLiability_DTL_Total_L_last"].fillna(0).values) > 0.01:
            error = "未经抵销的递延所得税负债期初余额递延所得税负债：非同一控制企业合并资产评估增值+交易性金融工具、衍生金融工具的估值+可供出售金融资产公允价值变动+其他<>合计"
            errorlist.append(error)
        # 未确认递延所得税资产明细期末余额：可抵扣暂时性差异+可抵扣亏损+税款抵减=合计
        if abs(df["DeferredTaxAssetsAndDeferredTaxLiability_Detail_TD_this"].fillna(0).values + df["DeferredTaxAssetsAndDeferredTaxLiability_Detail_Loss_this"].fillna(0).values + df["DeferredTaxAssetsAndDeferredTaxLiability_Detail_TaxD_this"].fillna(0).values - df["DeferredTaxAssetsAndDeferredTaxLiability_Detail_Total_this"].fillna(0).values) > 0.01:
            error = "未确认递延所得税资产明细期末余额：可抵扣暂时性差异+可抵扣亏损+税款抵减<>合计"
            errorlist.append(error)
        # 未确认递延所得税资产明细期初余额：可抵扣暂时性差异+可抵扣亏损+税款抵减=合计
        if abs(df["DeferredTaxAssetsAndDeferredTaxLiability_Detail_TD_last"].fillna(0).values + df["DeferredTaxAssetsAndDeferredTaxLiability_Detail_Loss_last"].fillna(0).values + df["DeferredTaxAssetsAndDeferredTaxLiability_Detail_TaxD_last"].fillna(0).values - df["DeferredTaxAssetsAndDeferredTaxLiability_Detail_Total_last"].fillna(0).values) > 0.01:
            error = "未确认递延所得税资产明细期初余额：可抵扣暂时性差异+可抵扣亏损+税款抵减<>合计"
            errorlist.append(error)
        # 未确认递延所得税资产的可抵扣亏损将于以下年度到期期末余额：第一年+第二年+第三年+第四年+第五年=合计
        if abs(df["DeferredTaxAssetsAndDeferredTaxLiability_Expire_20X1_this"].fillna(0).values + df["DeferredTaxAssetsAndDeferredTaxLiability_Expire_20X2_this"].fillna(0).values + df["DeferredTaxAssetsAndDeferredTaxLiability_Expire_20X4_this"].fillna(0).values + df["DeferredTaxAssetsAndDeferredTaxLiability_Expire_20X3_this"].fillna(0).values + df["DeferredTaxAssetsAndDeferredTaxLiability_Expire_20X5_this"].fillna(0).values - df["DeferredTaxAssetsAndDeferredTaxLiability_Expire_Total_this"].fillna(0).values) > 0.01:
            error = "未确认递延所得税资产的可抵扣亏损将于以下年度到期期末余额：第一年+第二年+第三年+第四年+第五年<>合计"
            errorlist.append(error)
        # 未确认递延所得税资产的可抵扣亏损将于以下年度到期期初余额：第一年+第二年+第三年+第四年+第五年=合计
        if abs(df["DeferredTaxAssetsAndDeferredTaxLiability_Expire_20X1_last"].fillna(0).values + df["DeferredTaxAssetsAndDeferredTaxLiability_Expire_20X2_last"].fillna(0).values + df["DeferredTaxAssetsAndDeferredTaxLiability_Expire_20X4_last"].fillna(0).values + df["DeferredTaxAssetsAndDeferredTaxLiability_Expire_20X3_last"].fillna(0).values + df["DeferredTaxAssetsAndDeferredTaxLiability_Expire_20X5_last"].fillna(0).values - df["DeferredTaxAssetsAndDeferredTaxLiability_Expire_Total_last"].fillna(0).values) > 0.01:
            error = "未确认递延所得税资产的可抵扣亏损将于以下年度到期期初余额：第一年+第二年+第三年+第四年+第五年<>合计"
            errorlist.append(error)
	
        











        return df, errorlist


if __name__ == "__main__":
    d = GetDeferredTaxAssetsAndDeferredTaxLiability()