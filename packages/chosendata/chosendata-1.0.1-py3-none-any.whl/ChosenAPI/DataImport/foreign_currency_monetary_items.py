
import pandas as pd
from ChosenAPI.DataImport.ChangeToNum import ChangeData



class GetFCMonetaryItems(object):#外币货币性项目
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
            "FCMonetaryItems_CE_FC_This": data.cell_value(3, 1),# B4 4行2列货币资金期末外币余额
            "FCMonetaryItems_CE_Dollar_FC_This": data.cell_value(4, 1),# B5 5行2列其中：美元期末外币余额
            "FCMonetaryItems_CE_Euro_FC_This": data.cell_value(5, 1),# B6 6行2列欧元期末外币余额
            "FCMonetaryItems_CE_HongKongDollars_FC_This": data.cell_value(6,1),# B7 7行2列港币期末外币余额
            "FCMonetaryItems_CE_Other_FC_This": data.cell_value(7, 1),# B8 8行2列其他期末外币余额
            "FCMonetaryItems_AR_FC_This": data.cell_value(8, 1),# B9 9行2列应收账款期末外币余额
            "FCMonetaryItems_AR_Dollar_FC_This": data.cell_value(9, 1),# B10 10行2列其中：美元期末外币余额
            "FCMonetaryItems_AR_Euro_FC_This": data.cell_value(10, 1),# B11 11行2列欧元期末外币余额
            "FCMonetaryItems_AR_HongKongDollars_FC_This": data.cell_value(11, 1),  # B12 12行2列港币期末外币余额
            "FCMonetaryItems_AR_Other_FC_This": data.cell_value(12, 1),# B13 13行2列其他期末外币余额
            "FCMonetaryItems_LL_FC_This": data.cell_value(13, 1),# B14 14行2列长期借款期末外币余额
            "FCMonetaryItems_LL_Dollar_FC_This": data.cell_value(14, 1),# B15 15行2列其中：美元期末外币余额
            "FCMonetaryItems_LL_Euro_FC_This": data.cell_value(15, 1),# B16 16行2列欧元期末外币余额
            "FCMonetaryItems_LL_HongKongDollars_FC_This": data.cell_value(16, 1),# B17 17行2列港币期末外币余额
            "FCMonetaryItems_LL_Other_FC_This": data.cell_value(17, 1),# B18 18行2列其他期末外币余额
            "FCMonetaryItems_CE_DiscountRate": data.cell_value(3, 2),  # C4 4行3列货币资金折算汇率
            "FCMonetaryItems_CE_Dollar_DiscountRate": data.cell_value(4, 2),# C5 5行3列其中：美元折算汇率
            "FCMonetaryItems_CE_Euro_DiscountRate": data.cell_value(5, 2),  # C6 6行3列欧元折算汇率
            "FCMonetaryItems_CE_HongKongDollars_DiscountRate": data.cell_value(6, 2),# C7 7行3列港币折算汇率
            "FCMonetaryItems_CE_Other_DiscountRate": data.cell_value(7, 2),# C8 8行3列其他折算汇率
            "FCMonetaryItems_AR_DiscountRate": data.cell_value(8, 2),  # C9 9行3列应收账款折算汇率
            "FCMonetaryItems_AR_Dollar_DiscountRate": data.cell_value(9, 2),# C10 10行3列其中：美元折算汇率
            "FCMonetaryItems_AR_Euro_DiscountRate": data.cell_value(10, 2),# C11 11行3列欧元折算汇率
            "FCMonetaryItems_AR_HongKongDollars_DiscountRate": data.cell_value(11, 2),# C12 12行3列港币折算汇率
            "FCMonetaryItems_AR_Other_DiscountRate": data.cell_value(12, 2),# C13 13行3列其他折算汇率
            "FCMonetaryItems_LL_DiscountRate": data.cell_value(13, 2),  # C14 14行3列长期借款折算汇率
            "FCMonetaryItems_LL_Dollar_DiscountRate": data.cell_value(14, 2),# C15 15行3列其中：美元折算汇率
            "FCMonetaryItems_LL_Euro_DiscountRate": data.cell_value(15, 2),  # C16 16行3列欧元折算汇率
            "FCMonetaryItems_LL_HongKongDollars_DiscountRate": data.cell_value(16, 2),# C17 17行3列港币折算汇率
            "FCMonetaryItems_LL_Other_DiscountRate": data.cell_value(17, 2),# C18 18行3列其他折算汇率
            "FCMonetaryItems_CE_sum": data.cell_value(3, 3),  # D4 4行4列货币资金期末折算人民币余额
            "FCMonetaryItems_CE_Dollar_sum": data.cell_value(4, 3),# D5 5行4列其中：美元期末折算人民币余额
            "FCMonetaryItems_CE_Euro_sum": data.cell_value(5, 3),  # D6 6行4列欧元期末折算人民币余额
            "FCMonetaryItems_CE_HongKongDollars_sum": data.cell_value(6, 3),# D7 7行4列港币期末折算人民币余额
            "FCMonetaryItems_CE_Other_sum": data.cell_value(7, 3),  # D8 8行4列其他期末折算人民币余额
            "FCMonetaryItems_AR_sum": data.cell_value(8, 3),  # D9 9行4列应收账款期末折算人民币余额
            "FCMonetaryItems_AR_Dollar_sum": data.cell_value(9, 3),# D10 10行4列其中：美元期末折算人民币余额
            "FCMonetaryItems_AR_Euro_sum": data.cell_value(10, 3),# D11 11行4列欧元期末折算人民币余额
            "FCMonetaryItems_AR_HongKongDollars_sum": data.cell_value(11, 3),# D12 12行4列港币期末折算人民币余额
            "FCMonetaryItems_AR_Other_sum": data.cell_value(12, 3),# D13 13行4列其他期末折算人民币余额
            "FCMonetaryItems_LL_sum": data.cell_value(13, 3),  # D14 14行4列长期借款期末折算人民币余额
            "FCMonetaryItems_LL_Dollar_sum": data.cell_value(14, 3),# D15 15行4列其中：美元期末折算人民币余额
            "FCMonetaryItems_LL_Euro_sum": data.cell_value(15, 3),  # D16 16行4列欧元期末折算人民币余额
            "FCMonetaryItems_LL_HongKongDollars_sum": data.cell_value(16, 3),# D17 17行4列港币期末折算人民币余额
            "FCMonetaryItems_LL_Other_sum": data.cell_value(17, 3),  # D18 18行4列其他期末折算人民币余额
            "FCMonetaryItems_company1_FC_This": data.cell_value(21, 1),# B22 22行2列公司1期末外币余额
            "FCMonetaryItems_company2_FC_This": data.cell_value(22, 1),# B23 23行2列公司2期末外币余额
            "FCMonetaryItems_company3_FC_This": data.cell_value(23, 1),# B24 24行2列公司3期末外币余额
            "FCMonetaryItems_company4_FC_This": data.cell_value(24, 1),# B25 25行2列公司4期末外币余额
            "FCMonetaryItems_company5_FC_This": data.cell_value(25, 1),# B26 26行2列公司5期末外币余额
            "FCMonetaryItems_company1_FunctionalCurrency": data.cell_value(21, 2),  # C22 22行3列公司1记账本位币
            "FCMonetaryItems_company2_FunctionalCurrency": data.cell_value(22, 2),  # C23 23行3列公司2记账本位币
            "FCMonetaryItems_company3_FunctionalCurrency": data.cell_value(23, 2),  # C24 24行3列公司3记账本位币
            "FCMonetaryItems_company4_FunctionalCurrency": data.cell_value(24, 2),  # C25 25行3列公司4记账本位币
            "FCMonetaryItems_company5_FunctionalCurrency": data.cell_value(25, 2),  # C26 26行3列公司5记账本位币


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
        dic["FCMonetaryItems_Remark_FC_This"] = data.cell_value(27, 1),  # B28 28行2列说明
        dic["FCMonetaryItems_company1_gist"] = data.cell_value(21, 3),  # D22 22行4列公司1记账本位币选择依据
        dic["FCMonetaryItems_company2_gist"] = data.cell_value(22, 3),  # D23 23行4列公司2记账本位币选择依据
        dic["FCMonetaryItems_company3_gist"] = data.cell_value(23, 3),  # D24 24行4列公司3记账本位币选择依据
        dic["FCMonetaryItems_company4_gist"] = data.cell_value(24, 3),  # D25 25行4列公司4记账本位币选择依据
        dic["FCMonetaryItems_company5_gist"] = data.cell_value(25, 3),  # D26 26行4列公司5记账本位币选择依据

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
        # 货币资金期末外币余额：美元+欧元+港币+其他=货币资金
        if abs(df["FCMonetaryItems_CE_Dollar_FC_This"].fillna(0).values + df["FCMonetaryItems_CE_Euro_FC_This"].fillna(0).values + df["FCMonetaryItems_CE_HongKongDollars_FC_This"].fillna(0).values + df["FCMonetaryItems_CE_Other_FC_This"].fillna(0).values - df["FCMonetaryItems_CE_FC_This"].fillna(0).values) > 0.01:
            error = "货币资金期末外币余额：美元+欧元+港币+其他<>货币资金"
            errorlist.append(error)
        # 应收账款期末外币余额：美元+欧元+港币+其他=应收账款
        if abs(df["FCMonetaryItems_AR_Dollar_FC_This"].fillna(0).values + df["FCMonetaryItems_AR_Euro_FC_This"].fillna(0).values + df["FCMonetaryItems_AR_HongKongDollars_FC_This"].fillna(0).values + df["FCMonetaryItems_AR_Other_FC_This"].fillna(0).values - df["FCMonetaryItems_AR_FC_This"].fillna(0).values) > 0.01:
            error = "应收账款期末外币余额：美元+欧元+港币+其他<>应收账款"
            errorlist.append(error)
        # 长期借款期末外币余额：美元+欧元+港币+其他=长期借款
        if abs(df["FCMonetaryItems_LL_Dollar_FC_This"].fillna(0).values + df["FCMonetaryItems_LL_Euro_FC_This"].fillna(0).values + df["FCMonetaryItems_LL_HongKongDollars_FC_This"].fillna(0).values + df["FCMonetaryItems_LL_Other_FC_This"].fillna(0).values - df["FCMonetaryItems_LL_FC_This"].fillna(0).values) > 0.01:
            error = "长期借款期末外币余额：美元+欧元+港币+其他<>长期借款"
            errorlist.append(error)
        # 货币资金期末折算人民币余额：美元+欧元+港币+其他=货币资金
        if abs(df["FCMonetaryItems_CE_Dollar_sum"].fillna(0).values + df["FCMonetaryItems_CE_Euro_sum"].fillna(0).values + df["FCMonetaryItems_CE_HongKongDollars_sum"].fillna(0).values + df["FCMonetaryItems_CE_Other_sum"].fillna(0).values - df["FCMonetaryItems_CE_sum"].fillna(0).values) > 0.01:
            error = "货币资金期末折算人民币余额：美元+欧元+港币+其他<>货币资金"
            errorlist.append(error)
        # 应收账款期末折算人民币余额：美元+欧元+港币+其他=应收账款
        if abs(df["FCMonetaryItems_AR_Dollar_sum"].fillna(0).values + df["FCMonetaryItems_AR_Euro_sum"].fillna(0).values + df["FCMonetaryItems_AR_HongKongDollars_sum"].fillna(0).values + df["FCMonetaryItems_AR_Other_sum"].fillna(0).values - df["FCMonetaryItems_AR_sum"].fillna(0).values) > 0.01:
            error = "应收账款期末折算人民币余额：美元+欧元+港币+其他<>应收账款"
            errorlist.append(error)
        # 长期借款期末折算人民币余额：美元+欧元+港币+其他=长期借款
        if abs(df["FCMonetaryItems_LL_Dollar_sum"].fillna(0).values + df["FCMonetaryItems_LL_Euro_sum"].fillna(0).values + df["FCMonetaryItems_LL_HongKongDollars_sum"].fillna(0).values + df["FCMonetaryItems_LL_Other_sum"].fillna(0).values - df["FCMonetaryItems_LL_sum"].fillna(0).values) > 0.01:
            error = "长期借款期末折算人民币余额：美元+欧元+港币+其他<>长期借款"
            errorlist.append(error)
        











        return df, errorlist



if __name__ == "__main__":
    d = GetFCMonetaryItems()