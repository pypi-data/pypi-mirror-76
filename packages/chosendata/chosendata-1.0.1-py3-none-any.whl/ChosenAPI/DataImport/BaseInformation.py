from xlrd import xldate_as_tuple
from datetime import datetime
import pandas as pd
from ChosenAPI.upload.ModelTable import ComboxList



class GetBaseInformation(object):
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
            "ID": identify,  # 实例ID号
            "username": username, # 用户名
            "report_date": datetime(*xldate_as_tuple(data.cell_value(6, 1), 0)).strftime('%Y/%m/%d %H:%M:%S'),# B6 5行2列 需要转换成日期型
            "SW_1": data.cell_value(3, 1), # SW1级行业
            "industry": data.cell_value(4, 1),  # B4 4行2列   行业
            "region": data.cell_value(5, 1),  # B5 4行2列   地区
            "totalassets": data.cell_value(7, 1),  # B7 6行2列 总资产
            "totalrevenue": data.cell_value(8, 1),  # B8 7行2列  营业收入
            "checkmark": "未完成",
            "upload_date": datetime.now().strftime('%Y/%m/%d %H:%M:%S') # 上传时间

        }
        df = pd.DataFrame([dic])  # 打包成DataFram
        # print(df)
        report_date = dic["report_date"]
        return df, report_date

    def CheckError(self, df):
        # 建立错误空列表：
        errorlist = []
        industry_dic = ComboxList().List("ResearchReport", "IndustryResearch")
        if df.iloc[0]["ID"] == "-" or df.iloc[0]["ID"] is None:
            error = "基本情况：实例ID号缺失，不要删除原模板的-符号"
            errorlist.append(error)

        if df.iloc[0]["report_date"] == "-" or df.iloc[0]["report_date"] is None:
            error = "基本情况：报告期未填写"
            errorlist.append(error)

        if df.iloc[0]["SW_1"] not in industry_dic.keys():
            error = "申万一级行业填写不符合标准，请按照标准填写，具体见申万行业分类表"
            errorlist.append(error)

        if df.iloc[0]["industry"] == "" or df.iloc[0]["industry"] is None:
            error = "基本情况：行业未填写"
            errorlist.append(error)

        if df.iloc[0]["SW_1"] in industry_dic.keys() and df.iloc[0]["industry"] not in industry_dic.get(df.iloc[0]["SW_1"], ""):
            error = "申万二级行业填写不符合标准，请按照标准填写，具体见申万行业分类表"
            errorlist.append(error)

        if df.iloc[0]["totalrevenue"] == "" or df.iloc[0]["totalrevenue"] is None:
            error = "基本情况：营业收入未填写，不利于您查询实例"
            errorlist.append(error)

        if df.iloc[0]["totalassets"] == "" or df.iloc[0]["totalassets"] is None:
            error = "基本情况：总资产未填写，不利于您查询实例"
            errorlist.append(error)

        return df, errorlist


if __name__ == "__main__":
    d = GetBaseInformation()