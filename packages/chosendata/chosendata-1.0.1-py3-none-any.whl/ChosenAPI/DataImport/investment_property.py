
import pandas as pd
from ChosenAPI.DataImport.ChangeToNum import ChangeData



class GetInvestmentProperty(object):#投资性房地产
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
            "InvestmentProperty_LastOBV_building": data.cell_value(4, 1),  # B5 5行2列1.期初余额房屋、建筑物
            "InvestmentProperty_AddOBV_building": data.cell_value(5, 1),  # B6 6行2列2.本期增加金额房屋、建筑物
            "InvestmentProperty_BuyOBV_building": data.cell_value(6, 1),  # B7 7行2列⑴外购房屋、建筑物
            "InvestmentProperty_IntoOBV_building": data.cell_value(7, 1),  # B8 8行2列⑵存货\固定资产\在建工程转入房屋、建筑物
            "InvestmentProperty_MergeOBV_building": data.cell_value(8, 1),  # B9 9行2列⑶企业合并增加房屋、建筑物
            "InvestmentProperty_ReduceOBV_building": data.cell_value(9, 1),  # B10 10行2列3.本期减少金额房屋、建筑物
            "InvestmentProperty_DisposalOBV_building": data.cell_value(10, 1),  # B11 11行2列⑴处置房屋、建筑物
            "InvestmentProperty_OtherOBV_building": data.cell_value(11, 1),# B12 12行2列⑵其他转出房屋、建筑物
            "InvestmentProperty_ThisOBV_building": data.cell_value(12, 1),  # B13 13行2列4.期末余额房屋、建筑物
            "InvestmentProperty_LastAD_building": data.cell_value(14, 1),  # B15 15行2列1.期初余额房屋、建筑物
            "InvestmentProperty_AddAD_building": data.cell_value(15, 1),# B16 16行2列2.本期增加金额房屋、建筑物
            "InvestmentProperty_LiftAD_building": data.cell_value(16, 1),# B17 17行2列⑴计提或摊销房屋、建筑物
            "InvestmentProperty_MergeAD_building": data.cell_value(17, 1),# B18 18行2列⑵企业合并增加房屋、建筑物
            "InvestmentProperty_ReduceAD_building": data.cell_value(18, 1),# B19 19行2列3.本期减少金额房屋、建筑物
            "InvestmentProperty_DisposalAD_building": data.cell_value(19, 1),# B20 20行2列⑴处置房屋、建筑物
            "InvestmentProperty_OtherAD_building": data.cell_value(20, 1),# B21 21行2列⑵其他转出房屋、建筑物
            "InvestmentProperty_ThisAD_building": data.cell_value(21, 1),  # B22 22行2列4.期末余额房屋、建筑物
            "InvestmentProperty_LastIL_building": data.cell_value(23, 1),  # B24 24行2列1.期初余额房屋、建筑物
            "InvestmentProperty_AddIL_building": data.cell_value(24, 1),  # B25 25行2列2.本期增加金额房屋、建筑物
            "InvestmentProperty_LiftIL_building": data.cell_value(25, 1),  # B26 26行2列⑴计提房屋、建筑物
            "InvestmentProperty_MergeIL_building": data.cell_value(26, 1),  # B27 27行2列⑵企业合并增加房屋、建筑物
            "InvestmentProperty_ReduceIL_building": data.cell_value(27, 1),  # B28 28行2列3、本期减少金额房屋、建筑物
            "InvestmentProperty_DisposalIL_building": data.cell_value(28, 1),  # B29 29行2列⑴处置房屋、建筑物
            "InvestmentProperty_OtherIL_building": data.cell_value(29, 1),  # B30 30行2列⑵其他转出房屋、建筑物
            "InvestmentProperty_ThisIL_building": data.cell_value(30, 1),  # B31 31行2列4.期末余额房屋、建筑物
            "InvestmentProperty_EBV_building": data.cell_value(32, 1),  # B33 33行2列1.期末账面价值房屋、建筑物
            "InvestmentProperty_OBV_building": data.cell_value(33, 1),  # B34 34行2列2.期初账面价值房屋、建筑物
            "InvestmentProperty_Last_building": data.cell_value(37, 1),  # B38 38行2列一、期初余额房屋、建筑物
            "InvestmentProperty_Change_building": data.cell_value(38, 1),  # B39 39行2列二、本期变动房屋、建筑物
            "InvestmentProperty_Buy_building": data.cell_value(39, 1),  # B40 40行2列加：外购房屋、建筑物
            "InvestmentProperty_Into_building": data.cell_value(40, 1),  # B41 41行2列存货\固定资产\在建工程转入房屋、建筑物
            "InvestmentProperty_Merge_building": data.cell_value(41, 1),  # B42 42行2列企业合并增加房屋、建筑物
            "InvestmentProperty_Disposal_building": data.cell_value(42, 1),  # B43 43行2列减：处置房屋、建筑物
            "InvestmentProperty_Other_building": data.cell_value(43, 1),  # B44 44行2列其他转出房屋、建筑物
            "InvestmentProperty_FVChange_building": data.cell_value(44, 1),  # B45 45行2列公允价值变动房屋、建筑物
            "InvestmentProperty_This_building": data.cell_value(45, 1),  # B46 46行2列三、期末余额房屋、建筑物
            "InvestmentProperty_LastOBV_Land": data.cell_value(4, 2),  # C5 5行3列1.期初余额土地使用权
            "InvestmentProperty_AddOBV_Land": data.cell_value(5, 2),  # C6 6行3列2.本期增加金额土地使用权
            "InvestmentProperty_BuyOBV_Land": data.cell_value(6, 2),  # C7 7行3列⑴外购土地使用权
            "InvestmentProperty_IntoOBV_Land": data.cell_value(7, 2),# C8 8行3列⑵存货\固定资产\在建工程转入土地使用权
            "InvestmentProperty_MergeOBV_Land": data.cell_value(8, 2),  # C9 9行3列⑶企业合并增加土地使用权
            "InvestmentProperty_ReduceOBV_Land": data.cell_value(9, 2),  # C10 10行3列3.本期减少金额土地使用权
            "InvestmentProperty_DisposalOBV_Land": data.cell_value(10, 2),  # C11 11行3列⑴处置土地使用权
            "InvestmentProperty_OtherOBV_Land": data.cell_value(11, 2),# C12 12行3列⑵其他转出土地使用权
            "InvestmentProperty_ThisOBV_Land": data.cell_value(12, 2),  # C13 13行3列4.期末余额土地使用权
            "InvestmentProperty_LastAD_Land": data.cell_value(14, 2),# C15 15行3列1.期初余额土地使用权
            "InvestmentProperty_AddAD_Land": data.cell_value(15, 2),# C16 16行3列2.本期增加金额土地使用权
            "InvestmentProperty_LiftAD_Land": data.cell_value(16, 2),# C17 17行3列⑴计提或摊销土地使用权
            "InvestmentProperty_MergeAD_Land": data.cell_value(17, 2),# C18 18行3列⑵企业合并增加土地使用权
            "InvestmentProperty_ReduceAD_Land": data.cell_value(18, 2),# C19 19行3列3.本期减少金额土地使用权
            "InvestmentProperty_DisposalAD_Land": data.cell_value(19, 2),# C20 20行3列⑴处置土地使用权
            "InvestmentProperty_OtherAD_Land": data.cell_value(20, 2),# C21 21行3列⑵其他转出土地使用权
            "InvestmentProperty_ThisAD_Land": data.cell_value(21, 2),# C22 22行3列4.期末余额土地使用权
            "InvestmentProperty_LastIL_Land": data.cell_value(23, 2),  # C24 24行3列1.期初余额土地使用权
            "InvestmentProperty_AddIL_Land": data.cell_value(24, 2),  # C25 25行3列2.本期增加金额土地使用权
            "InvestmentProperty_LiftIL_Land": data.cell_value(25, 2),  # C26 26行3列⑴计提土地使用权
            "InvestmentProperty_MergeIL_Land": data.cell_value(26, 2),  # C27 27行3列⑵企业合并增加土地使用权
            "InvestmentProperty_ReduceIL_Land": data.cell_value(27, 2),  # C28 28行3列3、本期减少金额土地使用权
            "InvestmentProperty_DisposalIL_Land": data.cell_value(28, 2),  # C29 29行3列⑴处置土地使用权
            "InvestmentProperty_OtherIL_Land": data.cell_value(29, 2),# C30 30行3列⑵其他转出土地使用权
            "InvestmentProperty_ThisIL_Land": data.cell_value(30, 2),  # C31 31行3列4.期末余额土地使用权
            "InvestmentProperty_EBV_Land": data.cell_value(32, 2),  # C33 33行3列1.期末账面价值土地使用权
            "InvestmentProperty_OBV_Land": data.cell_value(33, 2),  # C34 34行3列2.期初账面价值土地使用权
            "InvestmentProperty_Last_Land": data.cell_value(37, 2),  # C38 38行3列一、期初余额土地使用权
            "InvestmentProperty_Change_Land": data.cell_value(38, 2),  # C39 39行3列二、本期变动土地使用权
            "InvestmentProperty_Buy_Land": data.cell_value(39, 2),  # C40 40行3列加：外购土地使用权
            "InvestmentProperty_Into_Land": data.cell_value(40, 2),  # C41 41行3列存货\固定资产\在建工程转入土地使用权
            "InvestmentProperty_Merge_Land": data.cell_value(41, 2),  # C42 42行3列企业合并增加土地使用权
            "InvestmentProperty_Disposal_Land": data.cell_value(42, 2),  # C43 43行3列减：处置土地使用权
            "InvestmentProperty_Other_Land": data.cell_value(43, 2),  # C44 44行3列其他转出土地使用权
            "InvestmentProperty_FVChange_Land": data.cell_value(44, 2),  # C45 45行3列公允价值变动土地使用权
            "InvestmentProperty_This_Land": data.cell_value(45, 2),  # C46 46行3列三、期末余额土地使用权
            "InvestmentProperty_LastOBV_UC": data.cell_value(4, 3),  # D5 5行4列1.期初余额在建工程
            "InvestmentProperty_AddOBV_UC": data.cell_value(5, 3),  # D6 6行4列2.本期增加金额在建工程
            "InvestmentProperty_BuyOBV_UC": data.cell_value(6, 3),# D7 7行4列⑴外购在建工程
            "InvestmentProperty_IntoOBV_UC": data.cell_value(7, 3),# D8 8行4列⑵存货\固定资产\在建工程转入在建工程
            "InvestmentProperty_MergeOBV_UC": data.cell_value(8, 3),  # D9 9行4列⑶企业合并增加在建工程
            "InvestmentProperty_ReduceOBV_UC": data.cell_value(9, 3),# D10 10行4列3.本期减少金额在建工程
            "InvestmentProperty_DisposalOBV_UC": data.cell_value(10, 3),# D11 11行4列⑴处置在建工程
            "InvestmentProperty_OtherOBV_UC": data.cell_value(11, 3),# D12 12行4列⑵其他转出在建工程
            "InvestmentProperty_ThisOBV_UC": data.cell_value(12, 3),  # D13 13行4列4.期末余额在建工程
            "InvestmentProperty_LastAD_UC": data.cell_value(14, 3),# D15 15行4列1.期初余额在建工程
            "InvestmentProperty_AddAD_UC": data.cell_value(15, 3),# D16 16行4列2.本期增加金额在建工程
            "InvestmentProperty_LiftAD_UC": data.cell_value(16, 3),# D17 17行4列⑴计提或摊销在建工程
            "InvestmentProperty_MergeAD_UC": data.cell_value(17, 3),# D18 18行4列⑵企业合并增加在建工程
            "InvestmentProperty_ReduceAD_UC": data.cell_value(18, 3),# D19 19行4列3.本期减少金额在建工程
            "InvestmentProperty_DisposalAD_UC": data.cell_value(19, 3),# D20 20行4列⑴处置在建工程
            "InvestmentProperty_OtherAD_UC": data.cell_value(20, 3),# D21 21行4列⑵其他转出在建工程
            "InvestmentProperty_ThisAD_UC": data.cell_value(21, 3),# D22 22行4列4.期末余额在建工程
            "InvestmentProperty_LastIL_UC": data.cell_value(23, 3),  # D24 24行4列1.期初余额在建工程
            "InvestmentProperty_AddIL_UC": data.cell_value(24, 3),  # D25 25行4列2.本期增加金额在建工程
            "InvestmentProperty_LiftIL_UC": data.cell_value(25, 3),# D26 26行4列⑴计提在建工程
            "InvestmentProperty_MergeIL_UC": data.cell_value(26, 3),  # D27 27行4列⑵企业合并增加在建工程
            "InvestmentProperty_ReduceIL_UC": data.cell_value(27, 3),# D28 28行4列3、本期减少金额在建工程
            "InvestmentProperty_DisposalIL_UC": data.cell_value(28, 3),  # D29 29行4列⑴处置在建工程
            "InvestmentProperty_OtherIL_UC": data.cell_value(29, 3),# D30 30行4列⑵其他转出在建工程
            "InvestmentProperty_ThisIL_UC": data.cell_value(30, 3),  # D31 31行4列4.期末余额在建工程
            "InvestmentProperty_EBV_UC": data.cell_value(32, 3),  # D33 33行4列1.期末账面价值在建工程
            "InvestmentProperty_OBV_UC": data.cell_value(33, 3),  # D34 34行4列2.期初账面价值在建工程
            "InvestmentProperty_Last_UC": data.cell_value(37, 3),  # D38 38行4列一、期初余额在建工程
            "InvestmentProperty_Change_UC": data.cell_value(38, 3),  # D39 39行4列二、本期变动在建工程
            "InvestmentProperty_Buy_UC": data.cell_value(39, 3),  # D40 40行4列加：外购在建工程
            "InvestmentProperty_Into_UC": data.cell_value(40, 3),  # D41 41行4列存货\固定资产\在建工程转入在建工程
            "InvestmentProperty_Merge_UC": data.cell_value(41, 3),  # D42 42行4列企业合并增加在建工程
            "InvestmentProperty_Disposal_UC": data.cell_value(42, 3),  # D43 43行4列减：处置在建工程
            "InvestmentProperty_Other_UC": data.cell_value(43, 3),  # D44 44行4列其他转出在建工程
            "InvestmentProperty_FVChange_UC": data.cell_value(44, 3),  # D45 45行4列公允价值变动在建工程
            "InvestmentProperty_This_UC": data.cell_value(45, 3),  # D46 46行4列三、期末余额在建工程
            "InvestmentProperty_LastOBV_Total": data.cell_value(4, 4),  # E5 5行5列1.期初余额合计
            "InvestmentProperty_AddOBV_Total": data.cell_value(5, 4),  # E6 6行5列2.本期增加金额合计
            "InvestmentProperty_BuyOBV_Total": data.cell_value(6, 4),  # E7 7行5列⑴外购合计
            "InvestmentProperty_IntoOBV_Total": data.cell_value(7, 4),  # E8 8行5列⑵存货\固定资产\在建工程转入合计
            "InvestmentProperty_MergeOBV_Total": data.cell_value(8, 4),  # E9 9行5列⑶企业合并增加合计
            "InvestmentProperty_ReduceOBV_Total": data.cell_value(9, 4),  # E10 10行5列3.本期减少金额合计
            "InvestmentProperty_DisposalOBV_Total": data.cell_value(10, 4),  # E11 11行5列⑴处置合计
            "InvestmentProperty_OtherOBV_Total": data.cell_value(11, 4),  # E12 12行5列⑵其他转出合计
            "InvestmentProperty_ThisOBV_Total": data.cell_value(12, 4),  # E13 13行5列4.期末余额合计
            "InvestmentProperty_LastAD_Total": data.cell_value(14, 4),  # E15 15行5列1.期初余额合计
            "InvestmentProperty_AddAD_Total": data.cell_value(15, 4),  # E16 16行5列2.本期增加金额合计
            "InvestmentProperty_LiftAD_Total": data.cell_value(16, 4),# E17 17行5列⑴计提或摊销合计
            "InvestmentProperty_MergeAD_Total": data.cell_value(17, 4),  # E18 18行5列⑵企业合并增加合计
            "InvestmentProperty_ReduceAD_Total": data.cell_value(18, 4),  # E19 19行5列3.本期减少金额合计
            "InvestmentProperty_DisposalAD_Total": data.cell_value(19, 4),  # E20 20行5列⑴处置合计
            "InvestmentProperty_OtherAD_Total": data.cell_value(20, 4),# E21 21行5列⑵其他转出合计
            "InvestmentProperty_ThisAD_Total": data.cell_value(21, 4),  # E22 22行5列4.期末余额合计
            "InvestmentProperty_LastIL_Total": data.cell_value(23, 4),  # E24 24行5列1.期初余额合计
            "InvestmentProperty_AddIL_Total": data.cell_value(24, 4),  # E25 25行5列2.本期增加金额合计
            "InvestmentProperty_LiftIL_Total": data.cell_value(25, 4),  # E26 26行5列⑴计提合计
            "InvestmentProperty_MergeIL_Total": data.cell_value(26, 4),  # E27 27行5列⑵企业合并增加合计
            "InvestmentProperty_ReduceIL_Total": data.cell_value(27, 4),  # E28 28行5列3、本期减少金额合计
            "InvestmentProperty_DisposalIL_Total": data.cell_value(28, 4),  # E29 29行5列⑴处置合计
            "InvestmentProperty_OtherIL_Total": data.cell_value(29, 4),  # E30 30行5列⑵其他转出合计
            "InvestmentProperty_ThisIL_Total": data.cell_value(30, 4),  # E31 31行5列4.期末余额合计
            "InvestmentProperty_EBV_Total": data.cell_value(32, 4),  # E33 33行5列1.期末账面价值合计
            "InvestmentProperty_OBV_Total": data.cell_value(33, 4),  # E34 34行5列2.期初账面价值合计
            "InvestmentProperty_Last_Total": data.cell_value(37, 4),  # E38 38行5列一、期初余额合计
            "InvestmentProperty_Change_Total": data.cell_value(38, 4),  # E39 39行5列二、本期变动合计
            "InvestmentProperty_Buy_Total": data.cell_value(39, 4),  # E40 40行5列加：外购合计
            "InvestmentProperty_Into_Total": data.cell_value(40, 4),  # E41 41行5列存货\固定资产\在建工程转入合计
            "InvestmentProperty_Merge_Total": data.cell_value(41, 4),  # E42 42行5列企业合并增加合计
            "InvestmentProperty_Disposal_Total": data.cell_value(42, 4),  # E43 43行5列减：处置合计
            "InvestmentProperty_Other_Total": data.cell_value(43, 4),  # E44 44行5列其他转出合计
            "InvestmentProperty_FVChange_Total": data.cell_value(44, 4),  # E45 45行5列公允价值变动合计
            "InvestmentProperty_This_Total": data.cell_value(45, 4),  # E46 46行5列三、期末余额合计
            "InvestmentProperty_Project1_BV": data.cell_value(49, 1),  # B50 50行2列项目1账面价值
            "InvestmentProperty_Project2_BV": data.cell_value(50, 1),  # B51 51行2列项目2账面价值
            "InvestmentProperty_Project3_BV": data.cell_value(51, 1),  # B52 52行2列项目3账面价值
            "InvestmentProperty_Project4_BV": data.cell_value(52, 1),  # B53 53行2列项目4账面价值
            "InvestmentProperty_Project5_BV": data.cell_value(53, 1),  # B54 54行2列项目5账面价值
            


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
        dic["InvestmentProperty_Remark"] = data.cell_value(55, 1),  # B56 56行2列说明
        dic["InvestmentProperty_Project1_Reason"] = data.cell_value(49, 2),  # C50 50行3列项目1未办妥产权证书原因
        dic["InvestmentProperty_Project2_Reason"] = data.cell_value(50, 2),  # C51 51行3列项目2未办妥产权证书原因
        dic["InvestmentProperty_Project3_Reason"] = data.cell_value(51, 2),  # C52 52行3列项目3未办妥产权证书原因
        dic["InvestmentProperty_Project4_Reason"] = data.cell_value(52, 2),  # C53 53行3列项目4未办妥产权证书原因
        dic["InvestmentProperty_Project5_Reason"] = data.cell_value(53, 2),  # C54 54行3列项目5未办妥产权证书原因
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
        # 采用成本模式计量的投资性房地产账面原值房屋、建筑物：期初余额+本期增加金额-本期减少金额=期末余额
        if abs(df["InvestmentProperty_LastOBV_building"].fillna(0).values + df["InvestmentProperty_AddOBV_building"].fillna(0).values - df["InvestmentProperty_ReduceOBV_building"].fillna(0).values - df["InvestmentProperty_ThisOBV_building"].fillna(0).values) > 0.01:
            error = "采用成本模式计量的投资性房地产账面原值房屋、建筑物：期初余额+本期增加金额-本期减少金额<>期末余额"
            errorlist.append(error)
        # 采用成本模式计量的投资性房地产累计折旧和累计摊销房屋、建筑物：期初余额+本期增加金额-本期减少金额=期末余额
        if abs(df["InvestmentProperty_LastAD_building"].fillna(0).values + df["InvestmentProperty_AddAD_building"].fillna(0).values - df["InvestmentProperty_ReduceAD_building"].fillna(0).values - df["InvestmentProperty_ThisAD_building"].fillna(0).values) > 0.01:
            error = "采用成本模式计量的投资性房地产累计折旧和累计摊销房屋、建筑物：期初余额+本期增加金额-本期减少金额<>期末余额"
            errorlist.append(error)
        # 采用成本模式计量的投资性房地产减值准备房屋、建筑物：期初余额+本期增加金额-本期减少金额=期末余额
        if abs(df["InvestmentProperty_LastIL_building"].fillna(0).values + df["InvestmentProperty_AddIL_building"].fillna(0).values - df["InvestmentProperty_ReduceIL_building"].fillna(0).values - df["InvestmentProperty_ThisIL_building"].fillna(0).values) > 0.01:
            error = "采用成本模式计量的投资性房地产减值准备房屋、建筑物：期初余额+本期增加金额-本期减少金额<>期末余额"
            errorlist.append(error)
        # 采用成本模式计量的投资性房地产账面原值土地使用权：期初余额+本期增加金额-本期减少金额=期末余额
        if abs(df["InvestmentProperty_LastOBV_Land"].fillna(0).values + df["InvestmentProperty_AddOBV_Land"].fillna(0).values - df["InvestmentProperty_ReduceOBV_Land"].fillna(0).values - df["InvestmentProperty_ThisOBV_Land"].fillna(0).values) > 0.01:
            error = "采用成本模式计量的投资性房地产账面原值土地使用权：期初余额+本期增加金额-本期减少金额<>期末余额"
            errorlist.append(error)
        # 采用成本模式计量的投资性房地产累计折旧和累计摊销土地使用权：期初余额+本期增加金额-本期减少金额=期末余额
        if abs(df["InvestmentProperty_LastAD_Land"].fillna(0).values + df["InvestmentProperty_AddAD_Land"].fillna(0).values - df["InvestmentProperty_ReduceAD_Land"].fillna(0).values - df["InvestmentProperty_ThisAD_Land"].fillna(0).values) > 0.01:
            error = "采用成本模式计量的投资性房地产累计折旧和累计摊销土地使用权：期初余额+本期增加金额-本期减少金额<>期末余额"
            errorlist.append(error)
        # 采用成本模式计量的投资性房地产减值准备土地使用权：期初余额+本期增加金额-本期减少金额=期末余额
        if abs(df["InvestmentProperty_LastIL_Land"].fillna(0).values + df["InvestmentProperty_AddIL_Land"].fillna(0).values - df["InvestmentProperty_ReduceIL_Land"].fillna(0).values - df["InvestmentProperty_ThisIL_Land"].fillna(0).values) > 0.01:
            error = "采用成本模式计量的投资性房地产减值准备土地使用权：期初余额+本期增加金额-本期减少金额<>期末余额"
            errorlist.append(error)
        # 采用成本模式计量的投资性房地产账面原值在建工程：期初余额+本期增加金额-本期减少金额=期末余额
        if abs(df["InvestmentProperty_LastOBV_UC"].fillna(0).values + df["InvestmentProperty_AddOBV_UC"].fillna(0).values - df["InvestmentProperty_ReduceOBV_UC"].fillna(0).values - df["InvestmentProperty_ThisOBV_UC"].fillna(0).values) > 0.01:
            error = "采用成本模式计量的投资性房地产账面原值在建工程：期初余额+本期增加金额-本期减少金额<>期末余额"
            errorlist.append(error)
        # 采用成本模式计量的投资性房地产累计折旧和累计摊销在建工程：期初余额+本期增加金额-本期减少金额=期末余额
        if abs(df["InvestmentProperty_LastAD_UC"].fillna(0).values + df["InvestmentProperty_AddAD_UC"].fillna(0).values - df["InvestmentProperty_ReduceAD_UC"].fillna(0).values - df["InvestmentProperty_ThisAD_UC"].fillna(0).values) > 0.01:
            error = "采用成本模式计量的投资性房地产累计折旧和累计摊销在建工程：期初余额+本期增加金额-本期减少金额<>期末余额"
            errorlist.append(error)
        # 采用成本模式计量的投资性房地产减值准备在建工程：期初余额+本期增加金额-本期减少金额=期末余额
        if abs(df["InvestmentProperty_LastIL_UC"].fillna(0).values + df["InvestmentProperty_AddIL_UC"].fillna(0).values - df["InvestmentProperty_ReduceIL_UC"].fillna(0).values - df["InvestmentProperty_ThisIL_UC"].fillna(0).values) > 0.01:
            error = "采用成本模式计量的投资性房地产减值准备在建工程：期初余额+本期增加金额-本期减少金额<>期末余额"
            errorlist.append(error)
        # 采用成本模式计量的投资性房地产账面原值期初余额：房屋、建筑物+土地使用权+在建工程=合计
        if abs(df["InvestmentProperty_LastOBV_building"].fillna(0).values + df["InvestmentProperty_LastOBV_Land"].fillna(0).values + df["InvestmentProperty_LastOBV_UC"].fillna(0).values - df["InvestmentProperty_LastOBV_Total"].fillna(0).values) > 0.01:
            error = "采用成本模式计量的投资性房地产账面原值期初余额：房屋、建筑物+土地使用权+在建工程<>合计"
            errorlist.append(error)
        # 采用成本模式计量的投资性房地产账面原值本期增加金额：房屋、建筑物+土地使用权+在建工程=合计
        if abs(df["InvestmentProperty_AddOBV_building"].fillna(0).values + df["InvestmentProperty_AddOBV_Land"].fillna(0).values + df["InvestmentProperty_AddOBV_UC"].fillna(0).values - df["InvestmentProperty_AddOBV_Total"].fillna(0).values) > 0.01:
            error = "采用成本模式计量的投资性房地产账面原值本期增加金额：房屋、建筑物+土地使用权+在建工程<>合计"
            errorlist.append(error)
        # 采用成本模式计量的投资性房地产账面原值本期减少金额：房屋、建筑物+土地使用权+在建工程=合计
        if abs(df["InvestmentProperty_ReduceOBV_building"].fillna(0).values + df["InvestmentProperty_ReduceOBV_Land"].fillna(0).values + df["InvestmentProperty_ReduceOBV_UC"].fillna(0).values - df["InvestmentProperty_ReduceOBV_Total"].fillna(0).values) > 0.01:
            error = "采用成本模式计量的投资性房地产账面原值本期减少金额：房屋、建筑物+土地使用权+在建工程<>合计"
            errorlist.append(error)
        # 采用成本模式计量的投资性房地产账面原值期末余额：房屋、建筑物+土地使用权+在建工程=合计
        if abs(df["InvestmentProperty_ThisOBV_building"].fillna(0).values + df["InvestmentProperty_ThisOBV_Land"].fillna(0).values + df["InvestmentProperty_ThisOBV_UC"].fillna(0).values - df["InvestmentProperty_ThisOBV_Total"].fillna(0).values) > 0.01:
            error = "采用成本模式计量的投资性房地产账面原值期末余额：房屋、建筑物+土地使用权+在建工程<>合计"
            errorlist.append(error)
        # 采用成本模式计量的投资性房地产累计折旧和累计摊销期初余额：房屋、建筑物+土地使用权+在建工程=合计
        if abs(df["InvestmentProperty_LastAD_building"].fillna(0).values + df["InvestmentProperty_LastAD_Land"].fillna(0).values + df["InvestmentProperty_LastAD_UC"].fillna(0).values - df["InvestmentProperty_LastAD_Total"].fillna(0).values) > 0.01:
            error = "采用成本模式计量的投资性房地产累计折旧和累计摊销期初余额：房屋、建筑物+土地使用权+在建工程<>合计"
            errorlist.append(error)
        # 采用成本模式计量的投资性房地产累计折旧和累计摊销本期增加金额：房屋、建筑物+土地使用权+在建工程=合计
        if abs(df["InvestmentProperty_AddAD_building"].fillna(0).values + df["InvestmentProperty_AddAD_Land"].fillna(0).values + df["InvestmentProperty_AddAD_UC"].fillna(0).values - df["InvestmentProperty_AddAD_Total"].fillna(0).values) > 0.01:
            error = "采用成本模式计量的投资性房地产累计折旧和累计摊销本期增加金额：房屋、建筑物+土地使用权+在建工程<>合计"
            errorlist.append(error)
        # 采用成本模式计量的投资性房地产累计折旧和累计摊销本期减少金额：房屋、建筑物+土地使用权+在建工程=合计
        if abs(df["InvestmentProperty_ReduceAD_building"].fillna(0).values + df["InvestmentProperty_ReduceAD_Land"].fillna(0).values + df["InvestmentProperty_ReduceAD_UC"].fillna(0).values - df["InvestmentProperty_ReduceAD_Total"].fillna(0).values) > 0.01:
            error = "采用成本模式计量的投资性房地产累计折旧和累计摊销本期减少金额：房屋、建筑物+土地使用权+在建工程<>合计"
            errorlist.append(error)
        # 采用成本模式计量的投资性房地产累计折旧和累计摊销期末余额：房屋、建筑物+土地使用权+在建工程=合计
        if abs(df["InvestmentProperty_ThisAD_building"].fillna(0).values + df["InvestmentProperty_ThisAD_Land"].fillna(0).values + df["InvestmentProperty_ThisAD_UC"].fillna(0).values - df["InvestmentProperty_ThisAD_Total"].fillna(0).values) > 0.01:
            error = "采用成本模式计量的投资性房地产累计折旧和累计摊销期末余额：房屋、建筑物+土地使用权+在建工程<>合计"
            errorlist.append(error)
        # 采用成本模式计量的投资性房地产减值准备期初余额：房屋、建筑物+土地使用权+在建工程=合计
        if abs(df["InvestmentProperty_LastIL_building"].fillna(0).values + df["InvestmentProperty_LastIL_Land"].fillna(0).values + df["InvestmentProperty_LastIL_UC"].fillna(0).values - df["InvestmentProperty_LastIL_Total"].fillna(0).values) > 0.01:
            error = "采用成本模式计量的投资性房地产减值准备期初余额：房屋、建筑物+土地使用权+在建工程<>合计"
            errorlist.append(error)
        # 采用成本模式计量的投资性房地产减值准备本期增加金额：房屋、建筑物+土地使用权+在建工程=合计
        if abs(df["InvestmentProperty_AddIL_building"].fillna(0).values + df["InvestmentProperty_AddIL_Land"].fillna(0).values + df["InvestmentProperty_AddIL_UC"].fillna(0).values - df["InvestmentProperty_AddIL_Total"].fillna(0).values) > 0.01:
            error = "采用成本模式计量的投资性房地产减值准备本期增加金额：房屋、建筑物+土地使用权+在建工程<>合计"
            errorlist.append(error)
        # 采用成本模式计量的投资性房地产减值准备本期减少金额：房屋、建筑物+土地使用权+在建工程=合计
        if abs(df["InvestmentProperty_ReduceIL_building"].fillna(0).values + df["InvestmentProperty_ReduceIL_Land"].fillna(0).values + df["InvestmentProperty_ReduceIL_UC"].fillna(0).values - df["InvestmentProperty_ReduceIL_Total"].fillna(0).values) > 0.01:
            error = "采用成本模式计量的投资性房地产减值准备本期减少金额：房屋、建筑物+土地使用权+在建工程<>合计"
            errorlist.append(error)
        # 采用成本模式计量的投资性房地产减值准备期末余额：房屋、建筑物+土地使用权+在建工程=合计
        if abs(df["InvestmentProperty_ThisIL_building"].fillna(0).values + df["InvestmentProperty_ThisIL_Land"].fillna(0).values + df["InvestmentProperty_ThisIL_UC"].fillna(0).values - df["InvestmentProperty_ThisIL_Total"].fillna(0).values) > 0.01:
            error = "采用成本模式计量的投资性房地产减值准备期末余额：房屋、建筑物+土地使用权+在建工程<>合计"
            errorlist.append(error)
        # 采用公允价值模式计量的投资性房地产房屋、建筑物：期初余额+本期变动=期末余额
        if abs(df["InvestmentProperty_Last_building"].fillna(0).values + df["InvestmentProperty_Change_building"].fillna(0).values - df["InvestmentProperty_This_building"].fillna(0).values) > 0.01:
            error = "采用公允价值模式计量的投资性房地产房屋、建筑物：期初余额+本期变动<>期末余额"
            errorlist.append(error)
        # 采用公允价值模式计量的投资性房地产土地使用权：期初余额+本期变动=期末余额
        if abs(df["InvestmentProperty_Last_Land"].fillna(0).values + df["InvestmentProperty_Change_Land"].fillna(0).values - df["InvestmentProperty_This_Land"].fillna(0).values) > 0.01:
            error = "采用公允价值模式计量的投资性房地产土地使用权：期初余额+本期变动<>期末余额"
            errorlist.append(error)
        # 采用公允价值模式计量的投资性房地产在建工程：期初余额+本期变动=期末余额
        if abs(df["InvestmentProperty_Last_UC"].fillna(0).values + df["InvestmentProperty_Change_UC"].fillna(0).values - df["InvestmentProperty_This_UC"].fillna(0).values) > 0.01:
            error = "采用公允价值模式计量的投资性房地产在建工程：期初余额+本期变动<>期末余额"
            errorlist.append(error)
        # 本期变动房屋、建筑物：外购+存货\固定资产\在建工程转入+企业合并增加-处置-其他转出+公允价值变动=本期变动
        if abs(df["InvestmentProperty_Buy_building"].fillna(0).values + df["InvestmentProperty_Into_building"].fillna(0).values + df["InvestmentProperty_Merge_building"].fillna(0).values - df["InvestmentProperty_Disposal_building"].fillna(0).values - df["InvestmentProperty_Other_building"].fillna(0).values + df["InvestmentProperty_FVChange_building"].fillna(0).values - df["InvestmentProperty_Change_building"].fillna(0).values) > 0.01:
            error = "本期变动房屋、建筑物：外购+存货\固定资产\在建工程转入+企业合并增加-处置-其他转出+公允价值变动<>本期变动"
            errorlist.append(error)
        # 本期变动土地使用权：外购+存货\固定资产\在建工程转入+企业合并增加-处置-其他转出+公允价值变动=本期变动
        if abs(df["InvestmentProperty_Buy_Land"].fillna(0).values + df["InvestmentProperty_Into_Land"].fillna(0).values + df["InvestmentProperty_Merge_Land"].fillna(0).values - df["InvestmentProperty_Disposal_Land"].fillna(0).values - df["InvestmentProperty_Other_Land"].fillna(0).values + df["InvestmentProperty_FVChange_Land"].fillna(0).values - df["InvestmentProperty_Change_Land"].fillna(0).values) > 0.01:
            error = "本期变动土地使用权：外购+存货\固定资产\在建工程转入+企业合并增加-处置-其他转出+公允价值变动<>本期变动"
            errorlist.append(error)
        # 本期变动在建工程：外购+存货\固定资产\在建工程转入+企业合并增加-处置-其他转出+公允价值变动=本期变动
        if abs(df["InvestmentProperty_Buy_UC"].fillna(0).values + df["InvestmentProperty_Into_UC"].fillna(0).values + df["InvestmentProperty_Merge_UC"].fillna(0).values - df["InvestmentProperty_Disposal_UC"].fillna(0).values - df["InvestmentProperty_Other_UC"].fillna(0).values + df["InvestmentProperty_FVChange_UC"].fillna(0).values - df["InvestmentProperty_Change_UC"].fillna(0).values) > 0.01:
            error = "本期变动在建工程：外购+存货\固定资产\在建工程转入+企业合并增加-处置-其他转出+公允价值变动<>本期变动"
            errorlist.append(error)
        











        return df, errorlist


if __name__ == "__main__":
    d = GetInvestmentProperty()