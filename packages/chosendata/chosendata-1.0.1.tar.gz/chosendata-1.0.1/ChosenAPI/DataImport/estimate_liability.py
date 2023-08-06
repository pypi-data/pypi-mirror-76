
import pandas as pd
from ChosenAPI.DataImport.ChangeToNum import ChangeData



class GetEstimateLiability(object):#预计负债
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
            "EstimateLiability_Guarantee_this": data.cell_value(2, 1),  # B3 3行2列对外提供担保期末余额
            "EstimateLiability_PendingLitigation_this": data.cell_value(3, 1),  # B4 4行2列未决诉讼或未决仲裁期末余额
            "EstimateLiability_ProductQualityAssurance_this": data.cell_value(4, 1),  # B5 5行2列产品质量保证期末余额
            "EstimateLiability_RestructuringObligations_this": data.cell_value(5, 1),  # B6 6行2列重组义务期末余额
            "EstimateLiability_OnerousContract_this": data.cell_value(6, 1),  # B7 7行2列待执行的亏损合同期末余额
            "EstimateLiability_Discount_this": data.cell_value(7, 1),  # B8 8行2列商业承兑票据贴现期末余额
            "EstimateLiability_AssetDisposalObligation_this": data.cell_value(8, 1),  # B9 9行2列资产弃置义务期末余额
            "EstimateLiability_Other_this": data.cell_value(9, 1),  # B10 10行2列其他期末余额
            "EstimateLiability_Total_this": data.cell_value(10, 1),  # B11 11行2列合计期末余额
            "EstimateLiability_Guarantee_last": data.cell_value(2, 2),  # C3 3行3列对外提供担保期初余额
            "EstimateLiability_PendingLitigation_last": data.cell_value(3, 2),  # C4 4行3列未决诉讼或未决仲裁期初余额
            "EstimateLiability_ProductQualityAssurance_last": data.cell_value(4, 2),  # C5 5行3列产品质量保证期初余额
            "EstimateLiability_RestructuringObligations_last": data.cell_value(5, 2),  # C6 6行3列重组义务期初余额
            "EstimateLiability_OnerousContract_last": data.cell_value(6, 2),  # C7 7行3列待执行的亏损合同期初余额
            "EstimateLiability_Discount_last": data.cell_value(7, 2),  # C8 8行3列商业承兑票据贴现期初余额
            "EstimateLiability_AssetDisposalObligation_last": data.cell_value(8, 2),  # C9 9行3列资产弃置义务期初余额
            "EstimateLiability_Other_last": data.cell_value(9, 2),  # C10 10行3列其他期初余额
            "EstimateLiability_Total_last": data.cell_value(10, 2),  # C11 11行3列合计期初余额
            "EstimateLiability_Guarantee_reason": data.cell_value(2, 3),  # D3 3行4列对外提供担保形成原因
            "EstimateLiability_PendingLitigation_reason": data.cell_value(3, 3),  # D4 4行4列未决诉讼或未决仲裁形成原因
            "EstimateLiability_ProductQualityAssurance_reason": data.cell_value(4, 3),  # D5 5行4列产品质量保证形成原因
            "EstimateLiability_RestructuringObligations_reason": data.cell_value(5, 3),  # D6 6行4列重组义务形成原因
            "EstimateLiability_OnerousContract_reason": data.cell_value(6, 3),  # D7 7行4列待执行的亏损合同形成原因
            "EstimateLiability_Discount_reason": data.cell_value(7, 3),  # D8 8行4列商业承兑票据贴现形成原因
            "EstimateLiability_AssetDisposalObligation_reason": data.cell_value(8, 3),  # D9 9行4列资产弃置义务形成原因
            "EstimateLiability_Other_reason": data.cell_value(9, 3),  # D10 10行4列其他形成原因


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
        dic["EstimateLiability_Remark"] = data.cell_value(12, 1)  # B13 13行2列说明
        dic["EstimateLiability_Guarantee_reason"] = data.cell_value(2, 3),  # D3 3行4列对外提供担保形成原因
        dic["EstimateLiability_PendingLitigation_reason"] = data.cell_value(3, 3),  # D4 4行4列未决诉讼或未决仲裁形成原因
        dic["EstimateLiability_ProductQualityAssurance_reason"] = data.cell_value(4, 3),  # D5 5行4列产品质量保证形成原因
        dic["EstimateLiability_RestructuringObligations_reason"] = data.cell_value(5, 3),  # D6 6行4列重组义务形成原因
        dic["EstimateLiability_OnerousContract_reason"] = data.cell_value(6, 3),  # D7 7行4列待执行的亏损合同形成原因
        dic["EstimateLiability_Discount_reason"] = data.cell_value(7, 3),  # D8 8行4列商业承兑票据贴现形成原因
        dic["EstimateLiability_AssetDisposalObligation_reason"] = data.cell_value(8, 3),  # D9 9行4列资产弃置义务形成原因
        dic["EstimateLiability_Other_reason"] = data.cell_value(9, 3),  # D10 10行4列其他形成原因
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
        # 期末余额:对外提供担保+未决诉讼或未决仲裁+产品质量保证+重组义务+待执行的亏损合同+商业承兑票据贴现+资产弃置义务+其他=合计
        if abs(df["EstimateLiability_Guarantee_this"].fillna(0).values + df["EstimateLiability_PendingLitigation_this"].fillna(0).values + df["EstimateLiability_ProductQualityAssurance_this"].fillna(0).values + df["EstimateLiability_RestructuringObligations_this"].fillna(0).values + df["EstimateLiability_OnerousContract_this"].fillna(0).values + df["EstimateLiability_Discount_this"].fillna(0).values + df["EstimateLiability_AssetDisposalObligation_this"].fillna(0).values + df["EstimateLiability_Other_this"].fillna(0).values - df["EstimateLiability_Total_this"].fillna(0).values) > 0.01:
                error = "期末余额:对外提供担保+未决诉讼或未决仲裁+产品质量保证+重组义务+待执行的亏损合同+商业承兑票据贴现+资产弃置义务+其他<>合计"
                errorlist.append(error)
            # 期初余额:对外提供担保+未决诉讼或未决仲裁+产品质量保证+重组义务+待执行的亏损合同+商业承兑票据贴现+资产弃置义务+其他=合计
        if abs(df["EstimateLiability_Guarantee_last"].fillna(0).values + df["EstimateLiability_PendingLitigation_last"].fillna(0).values + df["EstimateLiability_ProductQualityAssurance_last"].fillna(0).values + df["EstimateLiability_RestructuringObligations_last"].fillna(0).values + df["EstimateLiability_OnerousContract_last"].fillna(0).values + df["EstimateLiability_Discount_last"].fillna(0).values + df["EstimateLiability_AssetDisposalObligation_last"].fillna(0).values + df["EstimateLiability_Other_last"].fillna(0).values - df["EstimateLiability_Total_last"].fillna(0).values) > 0.01:
                error = "期初余额:对外提供担保+未决诉讼或未决仲裁+产品质量保证+重组义务+待执行的亏损合同+商业承兑票据贴现+资产弃置义务+其他<>合计"
                errorlist.append(error)
        











        return df, errorlist


if __name__ == "__main__":
    d = GetEstimateLiability()