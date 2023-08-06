
import pandas as pd
from ChosenAPI.DataImport.ChangeToNum import ChangeData



class GetLongtermReceivableAccount(object):#长期应收款
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
            "LongtermReceivableAccount_Lease_BB_this": data.cell_value(4, 1),  # B5 5行2列融资租赁款期末余额账面余额
            "LongtermReceivableAccount_In_BB_this": data.cell_value(5, 1),# B6 6行2列其中：未实现融资收益期末余额账面余额
            "LongtermReceivableAccount_Goods_BB_this": data.cell_value(6, 1),  # B7 7行2列分期收款销售商品期末余额账面余额
            "LongtermReceivableAccount_Labor_BB_this": data.cell_value(7, 1),# B8 8行2列分期收款提供劳务期末余额账面余额
            "LongtermReceivableAccount_Other_BB_this": data.cell_value(8, 1),  # B9 9行2列其他期末余额账面余额
            "LongtermReceivableAccount_Total_BB_this": data.cell_value(9, 1),  # B10 10行2列合计期末余额账面余额
            "LongtermReceivableAccount_Lease_BDP_this": data.cell_value(4, 2),# C5 5行3列融资租赁款期末余额坏账准备
            "LongtermReceivableAccount_In_BDP_this": data.cell_value(5, 2),# C6 6行3列其中：未实现融资收益期末余额坏账准备
            "LongtermReceivableAccount_Goods_BDP_this": data.cell_value(6, 2),# C7 7行3列分期收款销售商品期末余额坏账准备
            "LongtermReceivableAccount_Labor_BDP_this": data.cell_value(7, 2),# C8 8行3列分期收款提供劳务期末余额坏账准备
            "LongtermReceivableAccount_Other_BDP_this": data.cell_value(8, 2),  # C9 9行3列其他期末余额坏账准备
            "LongtermReceivableAccount_Total_BDP_this": data.cell_value(9, 2),  # C10 10行3列合计期末余额坏账准备
            "LongtermReceivableAccount_Lease_BV_this": data.cell_value(4, 3),  # D5 5行4列融资租赁款期末余额账面价值
            "LongtermReceivableAccount_In_BV_this": data.cell_value(5, 3),  # D6 6行4列其中：未实现融资收益期末余额账面价值
            "LongtermReceivableAccount_Goods_BV_this": data.cell_value(6, 3),  # D7 7行4列分期收款销售商品期末余额账面价值
            "LongtermReceivableAccount_Labor_BV_this": data.cell_value(7, 3),# D8 8行4列分期收款提供劳务期末余额账面价值
            "LongtermReceivableAccount_Other_BV_this": data.cell_value(8, 3),  # D9 9行4列其他期末余额账面价值
            "LongtermReceivableAccount_Total_BV_this": data.cell_value(9, 3),  # D10 10行4列合计期末余额账面价值
            "LongtermReceivableAccount_Lease_BB_last": data.cell_value(4, 4),  # E5 5行5列融资租赁款期初余额账面余额
            "LongtermReceivableAccount_In_BB_last": data.cell_value(5, 4),# E6 6行5列其中：未实现融资收益期初余额账面余额
            "LongtermReceivableAccount_Goods_BB_last": data.cell_value(6, 4),  # E7 7行5列分期收款销售商品期初余额账面余额
            "LongtermReceivableAccount_Labor_BB_last": data.cell_value(7, 4),# E8 8行5列分期收款提供劳务期初余额账面余额
            "LongtermReceivableAccount_Other_BB_last": data.cell_value(8, 4),  # E9 9行5列其他期初余额账面余额
            "LongtermReceivableAccount_Total_BB_last": data.cell_value(9, 4),  # E10 10行5列合计期初余额账面余额
            "LongtermReceivableAccount_Lease_BDP_last": data.cell_value(4, 5),# F5 5行6列融资租赁款期初余额坏账准备
            "LongtermReceivableAccount_In_BDP_last": data.cell_value(5, 5),# F6 6行6列其中：未实现融资收益期初余额坏账准备
            "LongtermReceivableAccount_Goods_BDP_last": data.cell_value(6, 5),# F7 7行6列分期收款销售商品期初余额坏账准备
            "LongtermReceivableAccount_Labor_BDP_last": data.cell_value(7, 5),# F8 8行6列分期收款提供劳务期初余额坏账准备
            "LongtermReceivableAccount_Other_BDP_last": data.cell_value(8, 5),  # F9 9行6列其他期初余额坏账准备
            "LongtermReceivableAccount_Total_BDP_last": data.cell_value(9, 5),  # F10 10行6列合计期初余额坏账准备
            "LongtermReceivableAccount_Lease_BV_last": data.cell_value(4, 6),  # G5 5行7列融资租赁款期初余额账面价值
            "LongtermReceivableAccount_In_BV_last": data.cell_value(5, 6),  # G6 6行7列其中：未实现融资收益期初余额账面价值
            "LongtermReceivableAccount_Goods_BV_last": data.cell_value(6, 6),  # G7 7行7列分期收款销售商品期初余额账面价值
            "LongtermReceivableAccount_Labor_BV_last": data.cell_value(7, 6),# G8 8行7列分期收款提供劳务期初余额账面价值
            "LongtermReceivableAccount_Other_BV_last": data.cell_value(8, 6),  # G9 9行7列其他期初余额账面价值
            "LongtermReceivableAccount_Total_BV_last": data.cell_value(9, 6),  # G10 10行7列合计期初余额账面价值
            "LongtermReceivableAccount_Lease_Interval": data.cell_value(4, 7),  # H5 5行8列融资租赁款折现率区间
            "LongtermReceivableAccount_In_Interval": data.cell_value(5, 7),  # H6 6行8列其中：未实现融资收益折现率区间
            "LongtermReceivableAccount_Goods_Interval": data.cell_value(6, 7),  # H7 7行8列分期收款销售商品折现率区间
            "LongtermReceivableAccount_Labor_Interval": data.cell_value(7, 7),# H8 8行8列分期收款提供劳务折现率区间
            "LongtermReceivableAccount_Other_Interval": data.cell_value(8, 7),  # H9 9行8列其他折现率区间
            # "LongtermReceivableAccount_Total": data.cell_value(9, 7),  # H10 10行8列合计折现率区间
            "LongtermReceivableAccount_Debtor1_sum": data.cell_value(13, 2),  # C14 14行3列名称1终止确认的长期应收款金额
            "LongtermReceivableAccount_Debtor2_sum": data.cell_value(14, 2),  # C15 15行3列名称2终止确认的长期应收款金额
            "LongtermReceivableAccount_Debtor3_sum": data.cell_value(15, 2),  # C16 16行3列名称3终止确认的长期应收款金额
            "LongtermReceivableAccount_Debtor4_sum": data.cell_value(16, 2),  # C17 17行3列名称4终止确认的长期应收款金额
            "LongtermReceivableAccount_Debtor5_sum": data.cell_value(17, 2),  # C18 18行3列名称5终止确认的长期应收款金额
            "LongtermReceivableAccount_Total_sum": data.cell_value(18, 2),  # C19 19行3列合计终止确认的长期应收款金额
            "LongtermReceivableAccount_Debtor1_Related": data.cell_value(13, 3),  # D14 14行4列名称1与终止确认相关的利得或损失
            "LongtermReceivableAccount_Debtor2_Related": data.cell_value(14, 3),  # D15 15行4列名称2与终止确认相关的利得或损失
            "LongtermReceivableAccount_Debtor3_Related": data.cell_value(15, 3),  # D16 16行4列名称3与终止确认相关的利得或损失
            "LongtermReceivableAccount_Debtor4_Related": data.cell_value(16, 3),  # D17 17行4列名称4与终止确认相关的利得或损失
            "LongtermReceivableAccount_Debtor5_Related": data.cell_value(17, 3),  # D18 18行4列名称5与终止确认相关的利得或损失
            "LongtermReceivableAccount_Total_Related": data.cell_value(18, 3),  # D19 19行4列合计与终止确认相关的利得或损失


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
        dic["LongtermReceivableAccount_Remark"] = data.cell_value(20, 1),  # B21 21行2列说明
        dic["LongtermReceivableAccount_Debtor1_mode"] = data.cell_value(13, 1),  # B14 14行2列名称1资产转移的方式
        dic["LongtermReceivableAccount_Debtor2_mode"] = data.cell_value(14, 1),  # B15 15行2列名称2资产转移的方式
        dic["LongtermReceivableAccount_Debtor3_mode"] = data.cell_value(15, 1),  # B16 16行2列名称3资产转移的方式
        dic["LongtermReceivableAccount_Debtor4_mode"] = data.cell_value(16, 1),  # B17 17行2列名称4资产转移的方式
        dic["LongtermReceivableAccount_Debtor5_mode"] = data.cell_value(17, 1),  # B18 18行2列名称5资产转移的方式
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
        # 期末余额账面余额:融资租赁款+分期收款销售商品+分期收款提供劳务+其他=合计
        if abs(df["LongtermReceivableAccount_Lease_BB_this"].fillna(0).values + df["LongtermReceivableAccount_Other_BB_this"].fillna(0).values + df["LongtermReceivableAccount_Goods_BB_this"].fillna(0).values + df["LongtermReceivableAccount_Labor_BB_this"].fillna(0).values - df["LongtermReceivableAccount_Total_BB_this"].fillna(0).values) > 0.01:
            error = "期末余额账面余额:融资租赁款+分期收款销售商品+分期收款提供劳务+其他<>合计"
            errorlist.append(error)
        # 期末余额坏账准备:融资租赁款+分期收款销售商品+分期收款提供劳务+其他=合计
        if abs(df["LongtermReceivableAccount_Lease_BDP_this"].fillna(0).values + df["LongtermReceivableAccount_Other_BDP_this"].fillna(0).values + df["LongtermReceivableAccount_Goods_BDP_this"].fillna(0).values + df["LongtermReceivableAccount_Labor_BDP_this"].fillna(0).values - df["LongtermReceivableAccount_Total_BDP_this"].fillna(0).values) > 0.01:
            error = "期末余额坏账准备:融资租赁款+分期收款销售商品+分期收款提供劳务+其他<>合计"
            errorlist.append(error)
        # 期末余额账面价值:融资租赁款+分期收款销售商品+分期收款提供劳务+其他=合计
        if abs(df["LongtermReceivableAccount_Lease_BV_this"].fillna(0).values + df["LongtermReceivableAccount_Other_BV_this"].fillna(0).values + df["LongtermReceivableAccount_Goods_BV_this"].fillna(0).values + df["LongtermReceivableAccount_Labor_BV_this"].fillna(0).values - df["LongtermReceivableAccount_Total_BV_this"].fillna(0).values) > 0.01:
            error = "期末余额账面价值:融资租赁款+分期收款销售商品+分期收款提供劳务+其他<>合计"
            errorlist.append(error)
        # 期初余额账面余额:融资租赁款+分期收款销售商品+分期收款提供劳务+其他=合计
        if abs(df["LongtermReceivableAccount_Lease_BB_last"].fillna(0).values + df["LongtermReceivableAccount_Other_BB_last"].fillna(0).values + df["LongtermReceivableAccount_Goods_BB_last"].fillna(0).values + df["LongtermReceivableAccount_Labor_BB_last"].fillna(0).values - df["LongtermReceivableAccount_Total_BB_last"].fillna(0).values) > 0.01:
            error = "期初余额账面余额:融资租赁款+分期收款销售商品+分期收款提供劳务+其他<>合计"
            errorlist.append(error)
        # 期初余额坏账准备:融资租赁款+分期收款销售商品+分期收款提供劳务+其他=合计
        if abs(df["LongtermReceivableAccount_Lease_BDP_last"].fillna(0).values + df["LongtermReceivableAccount_Other_BDP_last"].fillna(0).values + df["LongtermReceivableAccount_Goods_BDP_last"].fillna(0).values + df["LongtermReceivableAccount_Labor_BDP_last"].fillna(0).values - df["LongtermReceivableAccount_Total_BDP_last"].fillna(0).values) > 0.01:
            error = "期初余额坏账准备:融资租赁款+分期收款销售商品+分期收款提供劳务+其他<>合计"
            errorlist.append(error)
        # 期初余额账面价值:融资租赁款+分期收款销售商品+分期收款提供劳务+其他=合计
        if abs(df["LongtermReceivableAccount_Lease_BV_last"].fillna(0).values + df["LongtermReceivableAccount_Other_BV_last"].fillna(0).values + df["LongtermReceivableAccount_Goods_BV_last"].fillna(0).values + df["LongtermReceivableAccount_Labor_BV_last"].fillna(0).values - df["LongtermReceivableAccount_Total_BV_last"].fillna(0).values) > 0.01:
            error = "期初余额账面价值:融资租赁款+分期收款销售商品+分期收款提供劳务+其他<>合计"
            errorlist.append(error)
        # 终止确认的长期应收款金额:名称1+名称2+名称3+名称4+名称5=合计
        if abs(df["LongtermReceivableAccount_Debtor1_sum"].fillna(0).values + df["LongtermReceivableAccount_Debtor2_sum"].fillna(0).values + df["LongtermReceivableAccount_Debtor3_sum"].fillna(0).values + df["LongtermReceivableAccount_Debtor4_sum"].fillna(0).values + df["LongtermReceivableAccount_Debtor5_sum"].fillna(0).values - df["LongtermReceivableAccount_Total_sum"].fillna(0).values) > 0.01:
            error = "终止确认的长期应收款金额:名称1+名称2+名称3+名称4+名称5<>合计"
            errorlist.append(error)











        return df, errorlist


if __name__ == "__main__":
    d = GetLongtermReceivableAccount()