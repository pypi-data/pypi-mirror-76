
import pandas as pd
from ChosenAPI.DataImport.ChangeToNum import ChangeData



class GetBussinessComposition(object):#员工情况
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
        change = ChangeData()
        """行业数据"""
        idic = {
            "ID": [identify] * 10,
            "username": [username] * 10,

            "bussiness_name": [data.cell_value(3, 0), data.cell_value(4, 0), data.cell_value(5, 0),
                               data.cell_value(6, 0), data.cell_value(7, 0), data.cell_value(8, 0),
                               data.cell_value(9, 0), data.cell_value(10, 0), data.cell_value(11, 0),
                               data.cell_value(12, 0)],  #A 1列4-13行
            "classify": ["industry"] * 10,
            "revenue_this": [change.Changing(data.cell_value(3, 1)), change.Changing(data.cell_value(4, 1)), change.Changing(data.cell_value(5, 1)),
                               change.Changing(data.cell_value(6, 1)), change.Changing(data.cell_value(7, 1)), change.Changing(data.cell_value(8, 1)),
                               change.Changing(data.cell_value(9, 1)), change.Changing(data.cell_value(10, 1)), change.Changing(data.cell_value(11, 1)),
                               change.Changing(data.cell_value(12, 1))],  # 2列4-13行
            "cost_this": [change.Changing(data.cell_value(3, 2)), change.Changing(data.cell_value(4, 2)), change.Changing(data.cell_value(5, 2)),
                            change.Changing(data.cell_value(6, 2)), change.Changing(data.cell_value(7, 2)), change.Changing(data.cell_value(8, 2)),
                            change.Changing(data.cell_value(9, 2)), change.Changing(data.cell_value(10, 2)), change.Changing(data.cell_value(11, 2)),
                            change.Changing(data.cell_value(12, 2))],  # 3列4-13行
            "revenue_last": [change.Changing(data.cell_value(3, 3)), change.Changing(data.cell_value(4, 3)), change.Changing(data.cell_value(5, 3)),
                            change.Changing(data.cell_value(6, 3)), change.Changing(data.cell_value(7, 3)), change.Changing(data.cell_value(8, 3)),
                            change.Changing(data.cell_value(9, 3)), change.Changing(data.cell_value(10, 3)), change.Changing(data.cell_value(11, 3)),
                            change.Changing(data.cell_value(12, 3))],    # 4列4-13行
            "cost_last": [change.Changing(data.cell_value(3, 4)), change.Changing(data.cell_value(4, 4)), change.Changing(data.cell_value(5, 4)),
                            change.Changing(data.cell_value(6, 4)), change.Changing(data.cell_value(7, 4)), change.Changing(data.cell_value(8, 4)),
                            change.Changing(data.cell_value(9, 4)), change.Changing(data.cell_value(10, 4)), change.Changing(data.cell_value(11, 4)),
                            change.Changing(data.cell_value(12, 4))],   # 5列4-13行

        }
        idf = pd.DataFrame(idic)

        """产品数据"""
        idic = {
            "ID": [identify] * 10,
            "username": [username] * 10,
            "bussiness_name": [data.cell_value(18, 0), data.cell_value(19, 0), data.cell_value(20, 0),
                               data.cell_value(21, 0), data.cell_value(22, 0), data.cell_value(23, 0),
                               data.cell_value(24, 0), data.cell_value(24, 0), data.cell_value(26, 0),
                               data.cell_value(27, 0)],  # 1列19-28行
            "classify": ["production"] * 10,
            "revenue_this": [change.Changing(data.cell_value(18, 1)), change.Changing(data.cell_value(19, 1)),
                             change.Changing(data.cell_value(20, 1)),
                             change.Changing(data.cell_value(21, 1)), change.Changing(data.cell_value(22, 1)),
                             change.Changing(data.cell_value(23, 1)),
                             change.Changing(data.cell_value(24, 1)), change.Changing(data.cell_value(25, 1)),
                             change.Changing(data.cell_value(26, 1)),
                             change.Changing(data.cell_value(27, 1))],  # 2列19-28行
            "cost_this": [change.Changing(data.cell_value(18, 2)), change.Changing(data.cell_value(19, 2)),
                          change.Changing(data.cell_value(20, 2)),
                          change.Changing(data.cell_value(21, 2)), change.Changing(data.cell_value(22, 2)),
                          change.Changing(data.cell_value(23, 2)),
                          change.Changing(data.cell_value(24, 2)), change.Changing(data.cell_value(25, 2)),
                          change.Changing(data.cell_value(26, 2)),
                          change.Changing(data.cell_value(27, 2))],  # 3列19-28行
            "revenue_last": [change.Changing(data.cell_value(18, 3)), change.Changing(data.cell_value(19, 3)),
                             change.Changing(data.cell_value(20, 3)),
                             change.Changing(data.cell_value(21, 3)), change.Changing(data.cell_value(22, 3)),
                             change.Changing(data.cell_value(23, 3)),
                             change.Changing(data.cell_value(24, 3)), change.Changing(data.cell_value(25, 3)),
                             change.Changing(data.cell_value(26, 3)),
                             change.Changing(data.cell_value(27, 3))],  # 4列19-28行
            "cost_last": [change.Changing(data.cell_value(18, 4)), change.Changing(data.cell_value(19, 4)),
                          change.Changing(data.cell_value(20, 4)),
                          change.Changing(data.cell_value(21, 4)), change.Changing(data.cell_value(22, 4)),
                          change.Changing(data.cell_value(23, 4)),
                          change.Changing(data.cell_value(24, 4)), change.Changing(data.cell_value(25, 4)),
                          change.Changing(data.cell_value(26, 4)),
                          change.Changing(data.cell_value(27, 4))],  # 5列19-28行

        }
        pdf = pd.DataFrame(idic)

        """合并"""
        df = pd.concat([idf, pdf])
        df = df[df["revenue_this"] != 0]
        if len(df) > 0:
            df["profit_margin_this"] = 100*(df["revenue_this"] - df["cost_this"]) / df["revenue_this"]
            df["profit_margin_last"] = 100*(df["revenue_last"] - df["cost_last"]) / df["revenue_last"]
            df["profit_margin_change"] = df["profit_margin_this"] - df["profit_margin_last"]
        else:
            pass
        # print(df)
        return df


    def CheckError(self, df):
        """
        业务构成表
        :param df:
        :return:
        """
        # 建立错误空列表：
        errorlist = []
        #
        if len(df) == 0:
            error = "业务构成表未填写数据"
            errorlist.append(error)

        return df, errorlist
