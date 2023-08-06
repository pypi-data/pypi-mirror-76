
import pandas as pd
from ChosenAPI.DataImport.ChangeToNum import ChangeData



class GetOtherReceivable(object):#其他应收款
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
            "OtherReceivable_SignificantAmount_sum_BB_this": data.cell_value(5, 1),# B6 6行2列应收账款分类披露单项金额重大并单独计提坏账准备的应收账款期末余额账面余额金额
            "OtherReceivable_CreditRisk_sum_BB_this": data.cell_value(6, 1),# B7 7行2列应收账款分类披露按信用风险特征组合计提坏账准备的应收账款期末余额账面余额金额
            "OtherReceivable_AgingCombination_sum_BB_this": data.cell_value(7, 1),# B8 8行2列应收账款分类披露其中：账龄组合期末余额账面余额金额
            "OtherReceivable_OtherCombinations_sum_BB_this": data.cell_value(8, 1),# B9 9行2列应收账款分类披露其他组合期末余额账面余额金额
            "OtherReceivable_SeparateProvision_sum_BB_this": data.cell_value(9, 1),# B10 10行2列应收账款分类披露单项金额不重大但单独计提坏账准备的应收账款期末余额账面余额金额
            "OtherReceivable_Total_sum_BB_this": data.cell_value(10, 1),  # B11 11行2列应收账款分类披露合计期末余额账面余额金额
            "OtherReceivable_SignificantAmount_ratio_BB_this": data.cell_value(5, 2),# C6 6行3列应收账款分类披露单项金额重大并单独计提坏账准备的应收账款期末余额账面余额比例(%)
            "OtherReceivable_CreditRisk_ratio_BB_this": data.cell_value(6, 2),# C7 7行3列应收账款分类披露按信用风险特征组合计提坏账准备的应收账款期末余额账面余额比例(%)
            "OtherReceivable_AgingCombination_ratio_BB_this": data.cell_value(7, 2),# C8 8行3列应收账款分类披露其中：账龄组合期末余额账面余额比例(%)
            "OtherReceivable_OtherCombinations_ratio_BB_this": data.cell_value(8, 2),# C9 9行3列应收账款分类披露其他组合期末余额账面余额比例(%)
            "OtherReceivable_SeparateProvision_ratio_BB_this": data.cell_value(9, 2),# C10 10行3列应收账款分类披露单项金额不重大但单独计提坏账准备的应收账款期末余额账面余额比例(%)
            "OtherReceivable_SignificantAmount_sum_BDP_this": data.cell_value(5, 3),# D6 6行4列应收账款分类披露单项金额重大并单独计提坏账准备的应收账款期末余额坏账准备金额
            "OtherReceivable_CreditRisk_sum_BDP_this": data.cell_value(6, 3),# D7 7行4列应收账款分类披露按信用风险特征组合计提坏账准备的应收账款期末余额坏账准备金额
            "OtherReceivable_AgingCombination_sum_BDP_this": data.cell_value(7, 3),# D8 8行4列应收账款分类披露其中：账龄组合期末余额坏账准备金额
            "OtherReceivable_OtherCombinations_sum_BDP_this": data.cell_value(8, 3),# D9 9行4列应收账款分类披露其他组合期末余额坏账准备金额
            "OtherReceivable_SeparateProvision_sum_BDP_this": data.cell_value(9, 3),# D10 10行4列应收账款分类披露单项金额不重大但单独计提坏账准备的应收账款期末余额坏账准备金额
            "OtherReceivable_Total_sum_BDP_this": data.cell_value(10, 3),  # D11 11行4列应收账款分类披露合计期末余额坏账准备金额
            "OtherReceivable_SignificantAmount_ratio_BDP_this": data.cell_value(5, 4),# E6 6行5列应收账款分类披露单项金额重大并单独计提坏账准备的应收账款期末余额坏账准备比例(%)
            "OtherReceivable_CreditRisk_ratio_BDP_this": data.cell_value(6, 4),# E7 7行5列应收账款分类披露按信用风险特征组合计提坏账准备的应收账款期末余额坏账准备比例(%)
            "OtherReceivable_AgingCombination_ratio_BDP_this": data.cell_value(7, 4),# E8 8行5列应收账款分类披露其中：账龄组合期末余额坏账准备比例(%)
            "OtherReceivable_OtherCombinations_ratio_BDP_this": data.cell_value(8, 4),# E9 9行5列应收账款分类披露其他组合期末余额坏账准备比例(%)
            "OtherReceivable_SeparateProvision_ratio_BDP_this": data.cell_value(9, 4),# E10 10行5列应收账款分类披露单项金额不重大但单独计提坏账准备的应收账款期末余额坏账准备比例(%)
            "OtherReceivable_SignificantAmount_BV_this": data.cell_value(5, 5),# F6 6行6列应收账款分类披露单项金额重大并单独计提坏账准备的应收账款期末余额账面价值
            "OtherReceivable_CreditRisk_BV_this": data.cell_value(6, 5),# F7 7行6列应收账款分类披露按信用风险特征组合计提坏账准备的应收账款期末余额账面价值
            "OtherReceivable_AgingCombination_BV_this": data.cell_value(7, 5),  # F8 8行6列应收账款分类披露其中：账龄组合期末余额账面价值
            "OtherReceivable_OtherCombinations_BV_this": data.cell_value(8, 5),  # F9 9行6列应收账款分类披露其他组合期末余额账面价值
            "OtherReceivable_SeparateProvision_BV_this": data.cell_value(9, 5),# F10 10行6列应收账款分类披露单项金额不重大但单独计提坏账准备的应收账款期末余额账面价值
            "OtherReceivable_Total_BV_this": data.cell_value(10, 5),  # F11 11行6列应收账款分类披露合计期末余额账面价值
            "OtherReceivable_SignificantAmount_sum_BB_last": data.cell_value(16, 1),# B17 17行2列应收账款分类披露续表单项金额重大并单独计提坏账准备的应收账款期初余额账面余额金额
            "OtherReceivable_CreditRisk_sum_BB_last": data.cell_value(17, 1),# B18 18行2列应收账款分类披露续表按信用风险特征组合计提坏账准备的应收账款期初余额账面余额金额
            "OtherReceivable_AgingCombination_sum_BB_last": data.cell_value(18, 1),# B19 19行2列应收账款分类披露续表其中：账龄组合期初余额账面余额金额
            "OtherReceivable_OtherCombinations_sum_BB_last": data.cell_value(19, 1),# B20 20行2列应收账款分类披露续表其他组合期初余额账面余额金额
            "OtherReceivable_SeparateProvision_sum_BB_last": data.cell_value(20, 1),# B21 21行2列应收账款分类披露续表单项金额不重大但单独计提坏账准备的应收账款期初余额账面余额金额
            "OtherReceivable_Total_sum_BB_last": data.cell_value(21, 1),  # B22 22行2列应收账款分类披露续表合计期初余额账面余额金额
            "OtherReceivable_SignificantAmount_ratio_BB_last": data.cell_value(16, 2),# C17 17行3列应收账款分类披露续表单项金额重大并单独计提坏账准备的应收账款期初余额账面余额比例(%)
            "OtherReceivable_CreditRisk_ratio_BB_last": data.cell_value(17, 2),# C18 18行3列应收账款分类披露续表按信用风险特征组合计提坏账准备的应收账款期初余额账面余额比例(%)
            "OtherReceivable_AgingCombination_ratio_BB_last": data.cell_value(18, 2),# C19 19行3列应收账款分类披露续表其中：账龄组合期初余额账面余额比例(%)
            "OtherReceivable_OtherCombinations_ratio_BB_last": data.cell_value(19, 2),# C20 20行3列应收账款分类披露续表其他组合期初余额账面余额比例(%)
            "OtherReceivable_SeparateProvision_ratio_BB_last": data.cell_value(20, 2),# C21 21行3列应收账款分类披露续表单项金额不重大但单独计提坏账准备的应收账款期初余额账面余额比例(%)
            "OtherReceivable_SignificantAmount_sum_BDP_last": data.cell_value(16, 3),# D17 17行4列应收账款分类披露续表单项金额重大并单独计提坏账准备的应收账款期初余额坏账准备金额
            "OtherReceivable_CreditRisk_sum_BDP_last": data.cell_value(17, 3),# D18 18行4列应收账款分类披露续表按信用风险特征组合计提坏账准备的应收账款期初余额坏账准备金额
            "OtherReceivable_AgingCombination_sum_BDP_last": data.cell_value(18, 3),# D19 19行4列应收账款分类披露续表其中：账龄组合期初余额坏账准备金额
            "OtherReceivable_OtherCombinations_sum_BDP_last": data.cell_value(19, 3),# D20 20行4列应收账款分类披露续表其他组合期初余额坏账准备金额
            "OtherReceivable_SeparateProvision_sum_BDP_last": data.cell_value(20, 3),# D21 21行4列应收账款分类披露续表单项金额不重大但单独计提坏账准备的应收账款期初余额坏账准备金额
            "OtherReceivable_Total_sum_BDP_last": data.cell_value(21, 3),# D22 22行4列应收账款分类披露续表合计期初余额坏账准备金额
            "OtherReceivable_SignificantAmount_ratio_BDP_last": data.cell_value(16, 4),# E17 17行5列应收账款分类披露续表单项金额重大并单独计提坏账准备的应收账款期初余额坏账准备比例(%)
            "OtherReceivable_CreditRisk_ratio_BDP_last": data.cell_value(17, 4),# E18 18行5列应收账款分类披露续表按信用风险特征组合计提坏账准备的应收账款期初余额坏账准备比例(%)
            "OtherReceivable_AgingCombination_ratio_BDP_last": data.cell_value(18, 4),# E19 19行5列应收账款分类披露续表其中：账龄组合期初余额坏账准备比例(%)
            "OtherReceivable_OtherCombinations_ratio_BDP_last": data.cell_value(19, 4),# E20 20行5列应收账款分类披露续表其他组合期初余额坏账准备比例(%)
            "OtherReceivable_SeparateProvision_ratio_BDP_last": data.cell_value(20, 4),# E21 21行5列应收账款分类披露续表单项金额不重大但单独计提坏账准备的应收账款期初余额坏账准备比例(%)
            "OtherReceivable_SignificantAmount_BV_last": data.cell_value(16, 5),# F17 17行6列应收账款分类披露续表单项金额重大并单独计提坏账准备的应收账款期初余额账面价值
            "OtherReceivable_CreditRisk_BV_last": data.cell_value(17, 5),# F18 18行6列应收账款分类披露续表按信用风险特征组合计提坏账准备的应收账款期初余额账面价值
            "OtherReceivable_AgingCombination_BV_last": data.cell_value(18, 5),# F19 19行6列应收账款分类披露续表其中：账龄组合期初余额账面价值
            "OtherReceivable_OtherCombinations_BV_last": data.cell_value(19, 5),# F20 20行6列应收账款分类披露续表其他组合期初余额账面价值
            "OtherReceivable_SeparateProvision_BV_last": data.cell_value(20, 5),# F21 21行6列应收账款分类披露续表单项金额不重大但单独计提坏账准备的应收账款期初余额账面价值
            "OtherReceivable_Total_BV_last": data.cell_value(21, 5),  # F22 22行6列应收账款分类披露续表合计期初余额账面价值
            "OtherReceivable_Company1_OtherReceivable_this": data.cell_value(26, 1),# B27 27行2列期末单项金额重大并单项计提坏账准备的应收账款company1期末余额应收账款
            "OtherReceivable_Company2_OtherReceivable_this": data.cell_value(27, 1),# B28 28行2列期末单项金额重大并单项计提坏账准备的应收账款company2期末余额应收账款
            "OtherReceivable_Company3_OtherReceivable_this": data.cell_value(28, 1),# B29 29行2列期末单项金额重大并单项计提坏账准备的应收账款company3期末余额应收账款
            "OtherReceivable_Company4_OtherReceivable_this": data.cell_value(29, 1),# B30 30行2列期末单项金额重大并单项计提坏账准备的应收账款company4期末余额应收账款
            "OtherReceivable_Company5_OtherReceivable_this": data.cell_value(30, 1),# B31 31行2列期末单项金额重大并单项计提坏账准备的应收账款company5期末余额应收账款
            "OtherReceivable_Total_OtherReceivable_this": data.cell_value(31, 1),# B32 32行2列期末单项金额重大并单项计提坏账准备的应收账款合计期末余额应收账款
            "OtherReceivable_Company1_BDP_this": data.cell_value(26, 2),# C27 27行3列期末单项金额重大并单项计提坏账准备的应收账款company1期末余额坏账准备
            "OtherReceivable_Company2_BDP_this": data.cell_value(27, 2),# C28 28行3列期末单项金额重大并单项计提坏账准备的应收账款company2期末余额坏账准备
            "OtherReceivable_Company3_BDP_this": data.cell_value(28, 2),# C29 29行3列期末单项金额重大并单项计提坏账准备的应收账款company3期末余额坏账准备
            "OtherReceivable_Company4_BDP_this": data.cell_value(29, 2),# C30 30行3列期末单项金额重大并单项计提坏账准备的应收账款company4期末余额坏账准备
            "OtherReceivable_Company5_BDP_this": data.cell_value(30, 2),# C31 31行3列期末单项金额重大并单项计提坏账准备的应收账款company5期末余额坏账准备
            "OtherReceivable_Total_BDP_this": data.cell_value(31, 2),# C32 32行3列期末单项金额重大并单项计提坏账准备的应收账款合计期末余额坏账准备
            "OtherReceivable_Company1_ratio_this": data.cell_value(26, 3),# D27 27行4列期末单项金额重大并单项计提坏账准备的应收账款company1期末余额计提比例(%)
            "OtherReceivable_Company2_ratio_this": data.cell_value(27, 3),# D28 28行4列期末单项金额重大并单项计提坏账准备的应收账款company2期末余额计提比例(%)
            "OtherReceivable_Company3_ratio_this": data.cell_value(28, 3),# D29 29行4列期末单项金额重大并单项计提坏账准备的应收账款company3期末余额计提比例(%)
            "OtherReceivable_Company4_ratio_this": data.cell_value(29, 3),# D30 30行4列期末单项金额重大并单项计提坏账准备的应收账款company4期末余额计提比例(%)
            "OtherReceivable_Company5_ratio_this": data.cell_value(30, 3),# D31 31行4列期末单项金额重大并单项计提坏账准备的应收账款company5期末余额计提比例(%)
            "OtherReceivable_Total_ratio_this": data.cell_value(31, 3),  # D32 32行4列期末单项金额重大并单项计提坏账准备的应收账款合计期末余额计提比例(%)
            "OtherReceivable_0_1_OtherReceivable_this": data.cell_value(37, 1),# B38 38行2列组合中，按账龄分析法计提坏账准备的应收账款1年以内期末余额应收账款
            "OtherReceivable_1_2_OtherReceivable_this": data.cell_value(38, 1),# B39 39行2列组合中，按账龄分析法计提坏账准备的应收账款1～2年期末余额应收账款
            "OtherReceivable_2_3_OtherReceivable_this": data.cell_value(39, 1),# B40 40行2列组合中，按账龄分析法计提坏账准备的应收账款2～3年期末余额应收账款
            "OtherReceivable_3_4_OtherReceivable_this": data.cell_value(40, 1),# B41 41行2列组合中，按账龄分析法计提坏账准备的应收账款3～4年期末余额应收账款
            "OtherReceivable_4_5_OtherReceivable_this": data.cell_value(41, 1),# B42 42行2列组合中，按账龄分析法计提坏账准备的应收账款4～5年期末余额应收账款
            "OtherReceivable_5__OtherReceivable_this": data.cell_value(42, 1),# B43 43行2列组合中，按账龄分析法计提坏账准备的应收账款5年以上期末余额应收账款
            "OtherReceivable_AgingTotal_OtherReceivable_this": data.cell_value(43, 1),# B44 44行2列组合中，按账龄分析法计提坏账准备的应收账款合计期末余额应收账款
            "OtherReceivable_0_1_BDP_this": data.cell_value(37, 2),# C38 38行3列组合中，按账龄分析法计提坏账准备的应收账款1年以内期末余额坏账准备
            "OtherReceivable_1_2_BDP_this": data.cell_value(38, 2),# C39 39行3列组合中，按账龄分析法计提坏账准备的应收账款1～2年期末余额坏账准备
            "OtherReceivable_2_3_BDP_this": data.cell_value(39, 2),# C40 40行3列组合中，按账龄分析法计提坏账准备的应收账款2～3年期末余额坏账准备
            "OtherReceivable_3_4_BDP_this": data.cell_value(40, 2),# C41 41行3列组合中，按账龄分析法计提坏账准备的应收账款3～4年期末余额坏账准备
            "OtherReceivable_4_5_BDP_this": data.cell_value(41, 2),# C42 42行3列组合中，按账龄分析法计提坏账准备的应收账款4～5年期末余额坏账准备
            "OtherReceivable_5__BDP_this": data.cell_value(42, 2),# C43 43行3列组合中，按账龄分析法计提坏账准备的应收账款5年以上期末余额坏账准备
            "OtherReceivable_AgingTotal_BDP_this": data.cell_value(43, 2),# C44 44行3列组合中，按账龄分析法计提坏账准备的应收账款合计期末余额坏账准备
            "OtherReceivable_0_1_ratio_this": data.cell_value(37, 3),  # D38 38行4列组合中，按账龄分析法计提坏账准备的应收账款1年以内期末余额计提比例(%)
            "OtherReceivable_1_2_ratio_this": data.cell_value(38, 3),  # D39 39行4列组合中，按账龄分析法计提坏账准备的应收账款1～2年期末余额计提比例(%)
            "OtherReceivable_2_3_ratio_this": data.cell_value(39, 3),  # D40 40行4列组合中，按账龄分析法计提坏账准备的应收账款2～3年期末余额计提比例(%)
            "OtherReceivable_3_4_ratio_this": data.cell_value(40, 3),  # D41 41行4列组合中，按账龄分析法计提坏账准备的应收账款3～4年期末余额计提比例(%)
            "OtherReceivable_4_5_ratio_this": data.cell_value(41, 3),  # D42 42行4列组合中，按账龄分析法计提坏账准备的应收账款4～5年期末余额计提比例(%)
            "OtherReceivable_5__ratio_this": data.cell_value(42, 3),  # D43 43行4列组合中，按账龄分析法计提坏账准备的应收账款5年以上期末余额计提比例(%)
            "OtherReceivable_AgingTotal_ratio_this": data.cell_value(43, 3),# D44 44行4列组合中，按账龄分析法计提坏账准备的应收账款合计期末余额计提比例(%)
            "OtherReceivable_0_1_OtherReceivable_last": data.cell_value(37, 4),# E38 38行5列组合中，按账龄分析法计提坏账准备的应收账款1年以内期初余额应收账款
            "OtherReceivable_1_2_OtherReceivable_last": data.cell_value(38, 4),# E39 39行5列组合中，按账龄分析法计提坏账准备的应收账款1～2年期初余额应收账款
            "OtherReceivable_2_3_OtherReceivable_last": data.cell_value(39, 4),# E40 40行5列组合中，按账龄分析法计提坏账准备的应收账款2～3年期初余额应收账款
            "OtherReceivable_3_4_OtherReceivable_last": data.cell_value(40, 4),# E41 41行5列组合中，按账龄分析法计提坏账准备的应收账款3～4年期初余额应收账款
            "OtherReceivable_4_5_OtherReceivable_last": data.cell_value(41, 4),# E42 42行5列组合中，按账龄分析法计提坏账准备的应收账款4～5年期初余额应收账款
            "OtherReceivable_5__OtherReceivable_last": data.cell_value(42, 4),# E43 43行5列组合中，按账龄分析法计提坏账准备的应收账款5年以上期初余额应收账款
            "OtherReceivable_AgingTotal_OtherReceivable_last": data.cell_value(43, 4),# E44 44行5列组合中，按账龄分析法计提坏账准备的应收账款合计期初余额应收账款
            "OtherReceivable_0_1_BDP_last": data.cell_value(37, 5),# F38 38行6列组合中，按账龄分析法计提坏账准备的应收账款1年以内期初余额坏账准备
            "OtherReceivable_1_2_BDP_last": data.cell_value(38, 5),# F39 39行6列组合中，按账龄分析法计提坏账准备的应收账款1～2年期初余额坏账准备
            "OtherReceivable_2_3_BDP_last": data.cell_value(39, 5),# F40 40行6列组合中，按账龄分析法计提坏账准备的应收账款2～3年期初余额坏账准备
            "OtherReceivable_3_4_BDP_last": data.cell_value(40, 5),# F41 41行6列组合中，按账龄分析法计提坏账准备的应收账款3～4年期初余额坏账准备
            "OtherReceivable_4_5_BDP_last": data.cell_value(41, 5),# F42 42行6列组合中，按账龄分析法计提坏账准备的应收账款4～5年期初余额坏账准备
            "OtherReceivable_5__BDP_last": data.cell_value(42, 5),# F43 43行6列组合中，按账龄分析法计提坏账准备的应收账款5年以上期初余额坏账准备
            "OtherReceivable_AgingTotal_BDP_last": data.cell_value(43, 5),# F44 44行6列组合中，按账龄分析法计提坏账准备的应收账款合计期初余额坏账准备
            "OtherReceivable_0_1_ratio_last": data.cell_value(37, 6),  # G38 38行7列组合中，按账龄分析法计提坏账准备的应收账款1年以内期初余额计提比例(%)
            "OtherReceivable_1_2_ratio_last": data.cell_value(38, 6),  # G39 39行7列组合中，按账龄分析法计提坏账准备的应收账款1～2年期初余额计提比例(%)
            "OtherReceivable_2_3_ratio_last": data.cell_value(39, 6),  # G40 40行7列组合中，按账龄分析法计提坏账准备的应收账款2～3年期初余额计提比例(%)
            "OtherReceivable_3_4_ratio_last": data.cell_value(40, 6),  # G41 41行7列组合中，按账龄分析法计提坏账准备的应收账款3～4年期初余额计提比例(%)
            "OtherReceivable_4_5_ratio_last": data.cell_value(41, 6),  # G42 42行7列组合中，按账龄分析法计提坏账准备的应收账款4～5年期初余额计提比例(%)
            "OtherReceivable_5__ratio_last": data.cell_value(42, 6),  # G43 43行7列组合中，按账龄分析法计提坏账准备的应收账款5年以上期初余额计提比例(%)
            "OtherReceivable_AgingTotal_ratio_last": data.cell_value(43, 6),# G44 44行7列组合中，按账龄分析法计提坏账准备的应收账款合计期初余额计提比例(%)
            "OtherReceivable_BG1_OtherReceivable_this": data.cell_value(48, 1),# B49 49行2列组合中，采用余额百分比法计提坏账准备的应收账款组合1期末余额应收账款
            "OtherReceivable_BG2_OtherReceivable_this": data.cell_value(49, 1),# B50 50行2列组合中，采用余额百分比法计提坏账准备的应收账款组合2期末余额应收账款
            "OtherReceivable_BalanceTotal_OtherReceivable_this": data.cell_value(50, 1),# B51 51行2列组合中，采用余额百分比法计提坏账准备的应收账款合计期末余额应收账款
            "OtherReceivable_BG1_BDP_this": data.cell_value(48, 2),# C49 49行3列组合中，采用余额百分比法计提坏账准备的应收账款组合1期末余额坏账准备
            "OtherReceivable_BG2_BDP_this": data.cell_value(49, 2),# C50 50行3列组合中，采用余额百分比法计提坏账准备的应收账款组合2期末余额坏账准备
            "OtherReceivable_BalanceTotal_BDP_this": data.cell_value(50, 2),# C51 51行3列组合中，采用余额百分比法计提坏账准备的应收账款合计期末余额坏账准备
            "OtherReceivable_BG1_ratio_this": data.cell_value(48, 3),# D49 49行4列组合中，采用余额百分比法计提坏账准备的应收账款组合1期末余额计提比例(%)
            "OtherReceivable_BG2_ratio_this": data.cell_value(49, 3),# D50 50行4列组合中，采用余额百分比法计提坏账准备的应收账款组合2期末余额计提比例(%)
            "OtherReceivable_BalanceTotal_ratio_this": data.cell_value(50, 3),# D51 51行4列组合中，采用余额百分比法计提坏账准备的应收账款合计期末余额计提比例(%)
            "OtherReceivable_OtherGroup1_OtherReceivable_this": data.cell_value(55, 1),# B56 56行2列组合中，采用其他方法计提坏账准备的应收账款组合1期末余额应收账款
            "OtherReceivable_OtherGroup2_OtherReceivable_this": data.cell_value(56, 1),# B57 57行2列组合中，采用其他方法计提坏账准备的应收账款组合2期末余额应收账款
            "OtherReceivable_OtherTotal_OtherReceivable_this": data.cell_value(57, 1),# B58 58行2列组合中，采用其他方法计提坏账准备的应收账款合计期末余额应收账款
            "OtherReceivable_OtherGroup1_BDP_this": data.cell_value(55, 2),# C56 56行3列组合中，采用其他方法计提坏账准备的应收账款组合1期末余额坏账准备
            "OtherReceivable_OtherGroup2_BDP_this": data.cell_value(56, 2),# C57 57行3列组合中，采用其他方法计提坏账准备的应收账款组合2期末余额坏账准备
            "OtherReceivable_OtherTotal_BDP_this": data.cell_value(57, 2),# C58 58行3列组合中，采用其他方法计提坏账准备的应收账款合计期末余额坏账准备
            "OtherReceivable_OtherGroup1_ratio_this": data.cell_value(55, 3),# D56 56行4列组合中，采用其他方法计提坏账准备的应收账款组合1期末余额计提比例(%)
            "OtherReceivable_OtherGroup2_ratio_this": data.cell_value(56, 3),# D57 57行4列组合中，采用其他方法计提坏账准备的应收账款组合2期末余额计提比例(%)
            "OtherReceivable_OtherTotal_ratio_this": data.cell_value(57, 3),# D58 58行4列组合中，采用其他方法计提坏账准备的应收账款合计期末余额计提比例(%)
            "OtherReceivable_WithdrawCompany1_sum": data.cell_value(61, 1),# B62 62行2列其中本期坏账准备收回或转回金额重要的：company1收回或转回金额
            "OtherReceivable_WithdrawCompany2_sum": data.cell_value(62, 1),# B63 63行2列其中本期坏账准备收回或转回金额重要的：company2收回或转回金额
            "OtherReceivable_WithdrawCompany3_sum": data.cell_value(63, 1),# B64 64行2列其中本期坏账准备收回或转回金额重要的：company3收回或转回金额
            "OtherReceivable_WithdrawCompany4_sum": data.cell_value(64, 1),# B65 65行2列其中本期坏账准备收回或转回金额重要的：company4收回或转回金额
            "OtherReceivable_WithdrawCompany5_sum": data.cell_value(65, 1),# B66 66行2列其中本期坏账准备收回或转回金额重要的：company5收回或转回金额
            "OtherReceivable_Total_sum": data.cell_value(66, 1),  # B67 67行2列其中本期坏账准备收回或转回金额重要的：合计收回或转回金额
            "OtherReceivable_Can_sum": data.cell_value(70, 1),# B71 71行2列本期实际核销的应收账款情况实际核销的应收账款核销金额
            "OtherReceivable_CanCompany1_sum": data.cell_value(75, 2),# C76 76行3列其中重要的应收账款核销情况：company1核销金额
            "OtherReceivable_CanCompany2_sum": data.cell_value(76, 2),# C77 77行3列其中重要的应收账款核销情况：company2核销金额
            "OtherReceivable_CanCompany3_sum": data.cell_value(77, 2),# C78 78行3列其中重要的应收账款核销情况：company3核销金额
            "OtherReceivable_CanCompany4_sum": data.cell_value(78, 2),# C79 79行3列其中重要的应收账款核销情况：company4核销金额
            "OtherReceivable_CanCompany5_sum": data.cell_value(79, 2),# C80 80行3列其中重要的应收账款核销情况：company5核销金额
            "OtherReceivable_ImportantTotal_sum": data.cell_value(80, 2),  # C81 81行3列其中重要的应收账款核销情况：合计核销金额
            "OtherReceivable_Debtor1_this": data.cell_value(84, 1),  # B85 85行2列按欠款方归集的期末余额前五名的应收账款情况company1期末余额
            "OtherReceivable_Debtor2_this": data.cell_value(85, 1),  # B86 86行2列按欠款方归集的期末余额前五名的应收账款情况company2期末余额
            "OtherReceivable_Debtor3_this": data.cell_value(86, 1),  # B87 87行2列按欠款方归集的期末余额前五名的应收账款情况company3期末余额
            "OtherReceivable_Debtor4_this": data.cell_value(87, 1),  # B88 88行2列按欠款方归集的期末余额前五名的应收账款情况company4期末余额
            "OtherReceivable_Debtor5_this": data.cell_value(88, 1),  # B89 89行2列按欠款方归集的期末余额前五名的应收账款情况company5期末余额
            "OtherReceivable_DebtorTotal_this": data.cell_value(89, 1),  # B90 90行2列按欠款方归集的期末余额前五名的应收账款情况合计期末余额
            "OtherReceivable_Debtor1_ratio": data.cell_value(84, 2),# C85 85行3列按欠款方归集的期末余额前五名的应收账款情况company1占应收账款期末余额合计数的比例(%)
            "OtherReceivable_Debtor2_ratio": data.cell_value(85, 2),# C86 86行3列按欠款方归集的期末余额前五名的应收账款情况company2占应收账款期末余额合计数的比例(%)
            "OtherReceivable_Debtor3_ratio": data.cell_value(86, 2),# C87 87行3列按欠款方归集的期末余额前五名的应收账款情况company3占应收账款期末余额合计数的比例(%)
            "OtherReceivable_Debtor4_ratio": data.cell_value(87, 2),# C88 88行3列按欠款方归集的期末余额前五名的应收账款情况company4占应收账款期末余额合计数的比例(%)
            "OtherReceivable_Debtor5_ratio": data.cell_value(88, 2),# C89 89行3列按欠款方归集的期末余额前五名的应收账款情况company5占应收账款期末余额合计数的比例(%)
            "OtherReceivable_DebtorTotal_ratio": data.cell_value(89, 2),# C90 90行3列按欠款方归集的期末余额前五名的应收账款情况合计占应收账款期末余额合计数的比例(%)
            "OtherReceivable_Debtor1_BDP": data.cell_value(84, 3),# D85 85行4列按欠款方归集的期末余额前五名的应收账款情况company1坏账准备金额
            "OtherReceivable_Debtor2_BDP": data.cell_value(85, 3),# D86 86行4列按欠款方归集的期末余额前五名的应收账款情况company2坏账准备金额
            "OtherReceivable_Debtor3_BDP": data.cell_value(86, 3),# D87 87行4列按欠款方归集的期末余额前五名的应收账款情况company3坏账准备金额
            "OtherReceivable_Debtor4_BDP": data.cell_value(87, 3),# D88 88行4列按欠款方归集的期末余额前五名的应收账款情况company4坏账准备金额
            "OtherReceivable_Debtor5_BDP": data.cell_value(88, 3),# D89 89行4列按欠款方归集的期末余额前五名的应收账款情况company5坏账准备金额
            "OtherReceivable_DebtorTotal_BDP": data.cell_value(89, 3),# D90 90行4列按欠款方归集的期末余额前五名的应收账款情况合计坏账准备金额
            "OtherReceivable_GSCompany1_this": data.cell_value(93, 2),  # C94 94行3列公司1期末余额
            "OtherReceivable_GSCompany2_this": data.cell_value(94, 2),  # C95 95行3列公司2期末余额
            "OtherReceivable_GSCompany3_this": data.cell_value(95, 2),  # C96 96行3列公司3期末余额
            "OtherReceivable_GSCompany4_this": data.cell_value(96, 2),  # C97 97行3列公司4期末余额
            "OtherReceivable_GSCompany5_this": data.cell_value(97, 2),  # C98 98行3列公司5期末余额
            "OtherReceivable_Total_this": data.cell_value(98, 2),  # C99 99行3列合计期末余额

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
        dic["OtherReceivable_Remark"] = data.cell_value(100, 1),  # B101 101行2列说明
        dic["OtherReceivable_Company1_reason_this"] = data.cell_value(26,4),  # E27 27行5列期末单项金额重大并单项计提坏账准备的应收账款company1计提理由
        dic["OtherReceivable_Company2_reason_this"] = data.cell_value(27,4),  # E28 28行5列期末单项金额重大并单项计提坏账准备的应收账款company2计提理由
        dic["OtherReceivable_Company3_reason_this"] = data.cell_value(28,4),  # E29 29行5列期末单项金额重大并单项计提坏账准备的应收账款company3计提理由
        dic["OtherReceivable_Company4_reason_this"] = data.cell_value(29,4),  # E30 30行5列期末单项金额重大并单项计提坏账准备的应收账款company4计提理由
        dic["OtherReceivable_Company5_reason_this"] = data.cell_value(30,4),  # E31 31行5列期末单项金额重大并单项计提坏账准备的应收账款company5计提理由
        dic["OtherReceivable_WithdrawCompany1_mode"] = data.cell_value(61,2),  # C62 62行3列其中本期坏账准备收回或转回金额重要的：company1收回方式
        dic["OtherReceivable_WithdrawCompany2_mode"] = data.cell_value(62,2),  # C63 63行3列其中本期坏账准备收回或转回金额重要的：company2收回方式
        dic["OtherReceivable_WithdrawCompany3_mode"] = data.cell_value(63,2),  # C64 64行3列其中本期坏账准备收回或转回金额重要的：company3收回方式
        dic["OtherReceivable_WithdrawCompany4_mode"] = data.cell_value(64,2),  # C65 65行3列其中本期坏账准备收回或转回金额重要的：company4收回方式
        dic["OtherReceivable_WithdrawCompany5_mode"] = data.cell_value(65,2),  # C66 66行3列其中本期坏账准备收回或转回金额重要的：company5收回方式
        dic["OtherReceivable_CanCompany1_nature"] = data.cell_value(75, 1),  # B76 76行2列其中重要的应收账款核销情况：company1应收账款性质
        dic["OtherReceivable_CanCompany2_nature"] = data.cell_value(76, 1),  # B77 77行2列其中重要的应收账款核销情况：company2应收账款性质
        dic["OtherReceivable_CanCompany3_nature"] = data.cell_value(77, 1),  # B78 78行2列其中重要的应收账款核销情况：company3应收账款性质
        dic["OtherReceivable_CanCompany4_nature"] = data.cell_value(78, 1),  # B79 79行2列其中重要的应收账款核销情况：company4应收账款性质
        dic["OtherReceivable_CanCompany5_nature"] = data.cell_value(79, 1),  # B80 80行2列其中重要的应收账款核销情况：company5应收账款性质
        dic["OtherReceivable_CanCompany1_reason"] = data.cell_value(75, 3),  # D76 76行4列其中重要的应收账款核销情况：company1核销原因
        dic["OtherReceivable_CanCompany2_reason"] = data.cell_value(76, 3),  # D77 77行4列其中重要的应收账款核销情况：company2核销原因
        dic["OtherReceivable_CanCompany3_reason"] = data.cell_value(77, 3),  # D78 78行4列其中重要的应收账款核销情况：company3核销原因
        dic["OtherReceivable_CanCompany4_reason"] = data.cell_value(78, 3),  # D79 79行4列其中重要的应收账款核销情况：company4核销原因
        dic["OtherReceivable_CanCompany5_reason"] = data.cell_value(79, 3),  # D80 80行4列其中重要的应收账款核销情况：company5核销原因
        dic["OtherReceivable_CanCompany1_program"] = data.cell_value(75, 4),  # E76 76行5列其中重要的应收账款核销情况：company1履行的核销程序
        dic["OtherReceivable_CanCompany2_program"] = data.cell_value(76, 4),  # E77 77行5列其中重要的应收账款核销情况：company2履行的核销程序
        dic["OtherReceivable_CanCompany3_program"] = data.cell_value(77, 4),  # E78 78行5列其中重要的应收账款核销情况：company3履行的核销程序
        dic["OtherReceivable_CanCompany4_program"] = data.cell_value(78, 4),  # E79 79行5列其中重要的应收账款核销情况：company4履行的核销程序
        dic["OtherReceivable_CanCompany5_program"] = data.cell_value(79, 4),  # E80 80行5列其中重要的应收账款核销情况：company5履行的核销程序
        dic["OtherReceivable_CanCompany1_RelatedTransaction"] = data.cell_value(75,5),  # F766列其中重要的应收账款核销情况：company1款项是否因关联交易产生
        dic["OtherReceivable_CanCompany2_RelatedTransaction"] = data.cell_value(76,5),  # F776列其中重要的应收账款核销情况：company2款项是否因关联交易产生
        dic["OtherReceivable_CanCompany3_RelatedTransaction"] = data.cell_value(77,5),  # F786列其中重要的应收账款核销情况：company3款项是否因关联交易产生
        dic["OtherReceivable_CanCompany4_RelatedTransaction"] = data.cell_value(78,5),  # F796列其中重要的应收账款核销情况：company4款项是否因关联交易产生
        dic["OtherReceivable_CanCompany5_RelatedTransaction"] = data.cell_value(79,5),  # F806列其中重要的应收账款核销情况：company5款项是否因关联交易产生
        dic["OtherReceivable_CanCompany1_CompanyNature"] = data.cell_value(75,6),  # G76 76行7列其中重要的应收账款核销情况：company1公司性质
        dic["OtherReceivable_CanCompany2_CompanyNature"] = data.cell_value(76,6),  # G77 77行7列其中重要的应收账款核销情况：company2公司性质
        dic["OtherReceivable_CanCompany3_CompanyNature"] = data.cell_value(77,6),  # G78 78行7列其中重要的应收账款核销情况：company3公司性质
        dic["OtherReceivable_CanCompany4_CompanyNature"] = data.cell_value(78,6),  # G79 79行7列其中重要的应收账款核销情况：company4公司性质
        dic["OtherReceivable_CanCompany5_CompanyNature"] = data.cell_value(79,6),  # G80 80行7列其中重要的应收账款核销情况：company5公司性质
        dic["OtherReceivable_Debtor1_CompanyNature"] = data.cell_value(84,4),  # E85 85行5列按欠款方归集的期末余额前五名的应收账款情况company1公司性质
        dic["OtherReceivable_Debtor2_CompanyNature"] = data.cell_value(85,4),  # E86 86行5列按欠款方归集的期末余额前五名的应收账款情况company2公司性质
        dic["OtherReceivable_Debtor3_CompanyNature"] = data.cell_value(86,4),  # E87 87行5列按欠款方归集的期末余额前五名的应收账款情况company3公司性质
        dic["OtherReceivable_Debtor4_CompanyNature"] = data.cell_value(87,4),  # E88 88行5列按欠款方归集的期末余额前五名的应收账款情况company4公司性质
        dic["OtherReceivable_Debtor5_CompanyNature"] = data.cell_value(88,4),  # E89 89行5列按欠款方归集的期末余额前五名的应收账款情况company5公司性质
        dic["OtherReceivable_GSCompany1_project"] = data.cell_value(93, 1),  # B94 94行2列公司1政府补助项目名称
        dic["OtherReceivable_GSCompany2_project"] = data.cell_value(94, 1),  # B95 95行2列公司2政府补助项目名称
        dic["OtherReceivable_GSCompany3_project"] = data.cell_value(95, 1),  # B96 96行2列公司3政府补助项目名称
        dic["OtherReceivable_GSCompany4_project"] = data.cell_value(96, 1),  # B97 97行2列公司4政府补助项目名称
        dic["OtherReceivable_GSCompany5_project"] = data.cell_value(97, 1),  # B98 98行2列公司5政府补助项目名称
        dic["OtherReceivable_GSCompany1_aging"] = data.cell_value(93, 3),  # D94 94行4列公司1期末账龄
        dic["OtherReceivable_GSCompany2_aging"] = data.cell_value(94, 3),  # D95 95行4列公司2期末账龄
        dic["OtherReceivable_GSCompany3_aging"] = data.cell_value(95, 3),  # D96 96行4列公司3期末账龄
        dic["OtherReceivable_GSCompany4_aging"] = data.cell_value(96, 3),  # D97 97行4列公司4期末账龄
        dic["OtherReceivable_GSCompany5_aging"] = data.cell_value(97, 3),  # D98 98行4列公司5期末账龄
        dic["OtherReceivable_GSCompany1_gist"] = data.cell_value(93, 4),  # E94 94行5列公司1预计收取的依据
        dic["OtherReceivable_GSCompany2_gist"] = data.cell_value(94, 4),  # E95 95行5列公司2预计收取的依据
        dic["OtherReceivable_GSCompany3_gist"] = data.cell_value(95, 4),  # E96 96行5列公司3预计收取的依据
        dic["OtherReceivable_GSCompany4_gist"] = data.cell_value(96, 4),  # E97 97行5列公司4预计收取的依据
        dic["OtherReceivable_GSCompany5_gist"] = data.cell_value(97, 4),  # E98 98行5列公司5预计收取的依据
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
        # 其他应账款分类披露:单项金额重大并单独计提坏账准备的其他应账款期末余额账面余额金额+按信用风险特征组合计提坏账准备的其他应账款期末余额账面余额金额+其他组合期末余额账面余额金额+单项金额不重大但单独计提坏账准备的其他应账款期末余额账面余额金额=合计期末余额账面余额金额
        if abs(df["OtherReceivable_SignificantAmount_sum_BB_this"].fillna(0).values + df["OtherReceivable_CreditRisk_sum_BB_this"].fillna(0).values + df["OtherReceivable_OtherCombinations_sum_BB_this"].fillna(0).values + df["OtherReceivable_SeparateProvision_sum_BB_this"].fillna(0).values - df["OtherReceivable_Total_sum_BB_this"].fillna(0).values) > 0.01:
            error = "其他应账款分类披露:单项金额重大并单独计提坏账准备的其他应账款期末余额账面余额金额+按信用风险特征组合计提坏账准备的其他应账款期末余额账面余额金额+其他组合期末余额账面余额金额+单项金额不重大但单独计提坏账准备的其他应账款期末余额账面余额金额<>合计期末余额账面余额金额"
            errorlist.append(error)
        # 其他应账款分类披露:单项金额重大并单独计提坏账准备的其他应账款期末余额坏账准备金额+按信用风险特征组合计提坏账准备的其他应账款期末余额坏账准备金额+其他组合期末余额坏账准备金额+单项金额不重大但单独计提坏账准备的其他应账款期末余额坏账准备金额=合计期末余额坏账准备金额
        if abs(df["OtherReceivable_SignificantAmount_sum_BDP_this"].fillna(0).values + df["OtherReceivable_CreditRisk_sum_BDP_this"].fillna(0).values + df["OtherReceivable_OtherCombinations_sum_BDP_this"].fillna(0).values + df["OtherReceivable_SeparateProvision_sum_BDP_this"].fillna(0).values - df["OtherReceivable_Total_sum_BDP_this"].fillna(0).values) > 0.01:
            error = "其他应账款分类披露:单项金额重大并单独计提坏账准备的其他应账款期末余额坏账准备金额+按信用风险特征组合计提坏账准备的其他应账款期末余额坏账准备金额+其他组合期末余额坏账准备金额+单项金额不重大但单独计提坏账准备的其他应账款期末余额坏账准备金额<>合计期末余额坏账准备金额"
            errorlist.append(error)
        # 其他应账款分类披露:单项金额重大并单独计提坏账准备的其他应账款期初余额账面余额金额+按信用风险特征组合计提坏账准备的其他应账款期初余额账面余额金额+其他组合期初余额账面余额金额+单项金额不重大但单独计提坏账准备的其他应账款期初余额账面余额金额=合计期初余额账面余额金额
        if abs(df["OtherReceivable_SignificantAmount_sum_BB_last"].fillna(0).values + df["OtherReceivable_CreditRisk_sum_BB_last"].fillna(0).values + df["OtherReceivable_OtherCombinations_sum_BB_last"].fillna(0).values + df["OtherReceivable_SeparateProvision_sum_BB_last"].fillna(0).values - df["OtherReceivable_Total_sum_BB_last"].fillna(0).values) > 0.01:
            error = "其他应账款分类披露:单项金额重大并单独计提坏账准备的其他应账款期初余额账面余额金额+按信用风险特征组合计提坏账准备的其他应账款期初余额账面余额金额+其他组合期初余额账面余额金额+单项金额不重大但单独计提坏账准备的其他应账款期初余额账面余额金额<>合计期初余额账面余额金额"
            errorlist.append(error)
        # 其他应账款分类披露:单项金额重大并单独计提坏账准备的其他应账款期初余额账面余额金额+按信用风险特征组合计提坏账准备的其他应账款期初余额账面余额金额+其他组合期初余额账面余额金额+单项金额不重大但单独计提坏账准备的其他应账款期初余额账面余额金额=合计期初余额账面余额金额
        if abs(df["OtherReceivable_SignificantAmount_sum_BDP_last"].fillna(0).values + df["OtherReceivable_CreditRisk_sum_BDP_last"].fillna(0).values + df["OtherReceivable_OtherCombinations_sum_BDP_last"].fillna(0).values + df["OtherReceivable_SeparateProvision_sum_BDP_last"].fillna(0).values - df["OtherReceivable_Total_sum_BDP_last"].fillna(0).values) > 0.01:
            error = "其他应账款分类披露:单项金额重大并单独计提坏账准备的其他应账款期初余额账面余额金额+按信用风险特征组合计提坏账准备的其他应账款期初余额账面余额金额+其他组合期初余额账面余额金额+单项金额不重大但单独计提坏账准备的其他应账款期初余额账面余额金额<>合计期初余额账面余额金额"
            errorlist.append(error)
        # 其他应账款分类披露:单项金额重大并单独计提坏账准备的其他应账款期末余额账面价值+按信用风险特征组合计提坏账准备的其他应账款期末余额账面价值+其他组合期末余额账面价值+单项金额不重大但单独计提坏账准备的其他应账款期末余额账面价值=合计期末余额账面价值
        if abs(df["OtherReceivable_SignificantAmount_BV_this"].fillna(0).values + df["OtherReceivable_CreditRisk_BV_this"].fillna(0).values + df["OtherReceivable_OtherCombinations_BV_this"].fillna(0).values + df["OtherReceivable_SeparateProvision_BV_this"].fillna(0).values - df["OtherReceivable_Total_BV_this"].fillna(0).values) > 0.01:
            error = "其他应账款分类披露:单项金额重大并单独计提坏账准备的其他应账款期末余额账面价值+按信用风险特征组合计提坏账准备的其他应账款期末余额账面价值+其他组合期末余额账面价值+单项金额不重大但单独计提坏账准备的其他应账款期末余额账面价值<>合计期末余额账面价值"
            errorlist.append(error)
        # 其他应账款分类披露:单项金额重大并单独计提坏账准备的其他应账款期初余额账面价值+按信用风险特征组合计提坏账准备的其他应账款期初余额账面价值+其他组合期初余额账面价值+单项金额不重大但单独计提坏账准备的其他应账款期初余额账面价值=合计期初余额账面价值
        if abs(df["OtherReceivable_SignificantAmount_BV_last"].fillna(0).values + df["OtherReceivable_CreditRisk_BV_last"].fillna(0).values + df["OtherReceivable_OtherCombinations_BV_last"].fillna(0).values + df["OtherReceivable_SeparateProvision_BV_last"].fillna(0).values - df["OtherReceivable_Total_BV_last"].fillna(0).values) > 0.01:
            error = "其他应账款分类披露:单项金额重大并单独计提坏账准备的其他应账款期初余额账面价值+按信用风险特征组合计提坏账准备的其他应账款期初余额账面价值+其他组合期初余额账面价值+单项金额不重大但单独计提坏账准备的其他应账款期初余额账面价值<>合计期初余额账面价值"
            errorlist.append(error)
        # 期末单项金额重大并单项计提坏账准备的其他应账款期末余额其他应账款:1+2+3+4+5=合计
        if abs(df["OtherReceivable_Company1_OtherReceivable_this"].fillna(0).values + df["OtherReceivable_Company2_OtherReceivable_this"].fillna(0).values + df["OtherReceivable_Company3_OtherReceivable_this"].fillna(0).values + df["OtherReceivable_Company4_OtherReceivable_this"].fillna(0).values + df["OtherReceivable_Company5_OtherReceivable_this"].fillna(0).values - df["OtherReceivable_Total_OtherReceivable_this"].fillna(0).values) > 0.01:
            error = "期末单项金额重大并单项计提坏账准备的其他应账款期末余额其他应账款:1+2+3+4+5<>合计"
            errorlist.append(error)
        # 期末单项金额重大并单项计提坏账准备的其他应账款期末余额坏账准备:1+2+3+4+5=合计
        if abs(df["OtherReceivable_Company1_BDP_this"].fillna(0).values + df["OtherReceivable_Company2_BDP_this"].fillna(0).values + df["OtherReceivable_Company3_BDP_this"].fillna(0).values + df["OtherReceivable_Company4_BDP_this"].fillna(0).values + df["OtherReceivable_Company5_BDP_this"].fillna(0).values - df["OtherReceivable_Total_BDP_this"].fillna(0).values) > 0.01:
            error = "期末单项金额重大并单项计提坏账准备的其他应账款期末余额坏账准备:1+2+3+4+5<>合计"
            errorlist.append(error)
        # 组合中，按账龄分析法计提坏账准备的其他应账款期末余额其他应账款：1年以内+1～2年+2～3年+3～4年+4～5年+5年以上=合计
        if abs(df["OtherReceivable_0_1_OtherReceivable_this"].fillna(0).values + df["OtherReceivable_1_2_OtherReceivable_this"].fillna(0).values + df["OtherReceivable_2_3_OtherReceivable_this"].fillna(0).values + df["OtherReceivable_3_4_OtherReceivable_this"].fillna(0).values + df["OtherReceivable_4_5_OtherReceivable_this"].fillna(0).values + df["OtherReceivable_5__OtherReceivable_this"].fillna(0).values - df["OtherReceivable_AgingTotal_OtherReceivable_this"].fillna(0).values) > 0.01:
            error = "组合中，按账龄分析法计提坏账准备的其他应账款期末余额其他应账款：1年以内+1～2年+2～3年+3～4年+4～5年+5年以上<>合计"
            errorlist.append(error)
        # 组合中，按账龄分析法计提坏账准备的其他应账款期末余额坏账准备：1年以内+1～2年+2～3年+3～4年+4～5年+5年以上=合计
        if abs(df["OtherReceivable_0_1_BDP_this"].fillna(0).values + df["OtherReceivable_1_2_BDP_this"].fillna(0).values + df["OtherReceivable_2_3_BDP_this"].fillna(0).values + df["OtherReceivable_3_4_BDP_this"].fillna(0).values + df["OtherReceivable_4_5_BDP_this"].fillna(0).values + df["OtherReceivable_5__BDP_this"].fillna(0).values - df["OtherReceivable_AgingTotal_BDP_this"].fillna(0).values) > 0.01:
            error = "组合中，按账龄分析法计提坏账准备的其他应账款期末余额坏账准备：1年以内+1～2年+2～3年+3～4年+4～5年+5年以上<>合计"
            errorlist.append(error)
        # 组合中，按账龄分析法计提坏账准备的其他应账款期初余额其他应账款：1年以内+1～2年+2～3年+3～4年+4～5年+5年以上=合计
        if abs(df["OtherReceivable_0_1_OtherReceivable_last"].fillna(0).values + df["OtherReceivable_1_2_OtherReceivable_last"].fillna(0).values + df["OtherReceivable_2_3_OtherReceivable_last"].fillna(0).values + df["OtherReceivable_3_4_OtherReceivable_last"].fillna(0).values + df["OtherReceivable_4_5_OtherReceivable_last"].fillna(0).values + df["OtherReceivable_5__OtherReceivable_last"].fillna(0).values - df["OtherReceivable_AgingTotal_OtherReceivable_last"].fillna(0).values) > 0.01:
            error = "组合中，按账龄分析法计提坏账准备的其他应账款期初余额其他应账款：1年以内+1～2年+2～3年+3～4年+4～5年+5年以上<>合计"
            errorlist.append(error)
        # 组合中，按账龄分析法计提坏账准备的其他应账款期初余额坏账准备：1年以内+1～2年+2～3年+3～4年+4～5年+5年以上=合计
        if abs(df["OtherReceivable_0_1_BDP_last"].fillna(0).values + df["OtherReceivable_1_2_BDP_last"].fillna(0).values + df["OtherReceivable_2_3_BDP_last"].fillna(0).values + df["OtherReceivable_3_4_BDP_last"].fillna(0).values + df["OtherReceivable_4_5_BDP_last"].fillna(0).values + df["OtherReceivable_5__BDP_last"].fillna(0).values - df["OtherReceivable_AgingTotal_BDP_last"].fillna(0).values) > 0.01:
            error = "组合中，按账龄分析法计提坏账准备的其他应账款期初余额坏账准备：1年以内+1～2年+2～3年+3～4年+4～5年+5年以上<>合计"
            errorlist.append(error)
        # 组合中，采用余额百分比法计提坏账准备的其他应账款期末余额其他应账款：组合1+组合2=合计
        if abs(df["OtherReceivable_BG1_OtherReceivable_this"].fillna(0).values + df["OtherReceivable_BG2_OtherReceivable_this"].fillna(0).values - df["OtherReceivable_BalanceTotal_OtherReceivable_this"].fillna(0).values) > 0.01:
            error = "组合中，采用余额百分比法计提坏账准备的其他应账款期末余额其他应账款：组合1+组合2<>合计"
            errorlist.append(error)
        # 组合中，采用余额百分比法计提坏账准备的其他应账款期末余额坏账准备：组合1+组合2=合计
        if abs(df["OtherReceivable_BG1_BDP_this"].fillna(0).values + df["OtherReceivable_BG2_BDP_this"].fillna(0).values - df["OtherReceivable_BalanceTotal_BDP_this"].fillna(0).values) > 0.01:
            error = "组合中，采用余额百分比法计提坏账准备的其他应账款期末余额坏账准备：组合1+组合2<>合计"
            errorlist.append(error)
        # 组合中，采用其他方法计提坏账准备的其他应账款期末余额其他应账款：组合1+组合2=合计
        if abs(df["OtherReceivable_OtherGroup1_OtherReceivable_this"].fillna(0).values + df["OtherReceivable_OtherGroup2_OtherReceivable_this"].fillna(0).values - df["OtherReceivable_OtherTotal_OtherReceivable_this"].fillna(0).values) > 0.01:
            error = "组合中，采用其他方法计提坏账准备的其他应账款期末余额其他应账款：组合1+组合2<>合计"
            errorlist.append(error)
        # 组合中，采用其他方法计提坏账准备的其他应账款期末余额坏账准备：组合1+组合2=合计
        if abs(df["OtherReceivable_OtherGroup1_BDP_this"].fillna(0).values + df["OtherReceivable_OtherGroup2_BDP_this"].fillna(0).values - df["OtherReceivable_OtherTotal_BDP_this"].fillna(0).values) > 0.01:
            error = "组合中，采用其他方法计提坏账准备的其他应账款期末余额坏账准备：组合1+组合2<>合计"
            errorlist.append(error)
        # 其中本期坏账准备收回或转回金额重要的：1+2+3+4+5=合计
        if abs(df["OtherReceivable_WithdrawCompany1_sum"].fillna(0).values + df["OtherReceivable_WithdrawCompany2_sum"].fillna(0).values + df["OtherReceivable_WithdrawCompany3_sum"].fillna(0).values + df["OtherReceivable_WithdrawCompany4_sum"].fillna(0).values + df["OtherReceivable_WithdrawCompany5_sum"].fillna(0).values - df["OtherReceivable_Total_sum"].fillna(0).values) > 0.01:
            error = "其中本期坏账准备收回或转回金额重要的：1+2+3+4+5<>合计"
            errorlist.append(error)
        # 其中重要的其他应账款核销情况：1+2+3+4+5=合计
        if abs(df["OtherReceivable_CanCompany1_sum"].fillna(0).values + df["OtherReceivable_CanCompany2_sum"].fillna(0).values + df["OtherReceivable_CanCompany3_sum"].fillna(0).values + df["OtherReceivable_CanCompany4_sum"].fillna(0).values + df["OtherReceivable_CanCompany5_sum"].fillna(0).values - df["OtherReceivable_ImportantTotal_sum"].fillna(0).values) > 0.01:
            error = "其中重要的其他应账款核销情况：1+2+3+4+5<>合计"
            errorlist.append(error)
        # 按欠款方归集的期末余额前五名的其他应账款情况期末余额：1+2+3+4+5=合计
        if abs(df["OtherReceivable_Debtor1_this"].fillna(0).values + df["OtherReceivable_Debtor2_this"].fillna(0).values + df["OtherReceivable_Debtor3_this"].fillna(0).values + df["OtherReceivable_Debtor4_this"].fillna(0).values + df["OtherReceivable_Debtor5_this"].fillna(0).values - df["OtherReceivable_DebtorTotal_this"].fillna(0).values) > 0.01:
            error = "按欠款方归集的期末余额前五名的其他应账款情况期末余额：1+2+3+4+5<>合计"
            errorlist.append(error)
        # 按欠款方归集的期末余额前五名的其他应账款情况坏账准备金额：1+2+3+4+5=合计
        if abs(df["OtherReceivable_Debtor1_BDP"].fillna(0).values + df["OtherReceivable_Debtor2_BDP"].fillna(0).values + df["OtherReceivable_Debtor3_BDP"].fillna(0).values + df["OtherReceivable_Debtor4_BDP"].fillna(0).values + df["OtherReceivable_Debtor5_BDP"].fillna(0).values - df["OtherReceivable_DebtorTotal_BDP"].fillna(0).values) > 0.01:
            error = "按欠款方归集的期末余额前五名的其他应账款情况坏账准备金额：1+2+3+4+5<>合计"
            errorlist.append(error)
        # 涉及政府补助的其他应收款:1+2+3+4+5=合计
        if abs(df["OtherReceivable_GSCompany1_this"].fillna(0).values + df["OtherReceivable_GSCompany2_this"].fillna(0).values + df["OtherReceivable_GSCompany3_this"].fillna(0).values + df["OtherReceivable_GSCompany4_this"].fillna(0).values + df["OtherReceivable_GSCompany5_this"].fillna(0).values - df["OtherReceivable_Total_this"].fillna(0).values) > 0.01:
            error = "涉及政府补助的其他应收款:1+2+3+4+5<>合计"
            errorlist.append(error)

        return df, errorlist


if __name__ == "__main__":
    d = GetOtherReceivable()