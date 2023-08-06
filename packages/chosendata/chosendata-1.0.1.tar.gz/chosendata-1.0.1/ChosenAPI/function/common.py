
import requests
import json
from ChosenAPI.Config.RootPath import RootDest
from ChosenAPI.Config.Headers import SetHeaders
from ChosenAPI.Query.QueryString import QueryStringCreate


class CommonFunction(object):
    def __init__(self):
        pass

    @staticmethod
    def send_data_by_get(obj, func):
        """
        :param obj: dict,
        :param func: str,
        :return: dict,
        """
        query = QueryStringCreate(obj).set_string()  # 生成查询字符串
        url = RootDest().set_path(func=func) + query
        response = requests.get(url, headers=SetHeaders().run())
        res = response.content.decode()
        try:
            data = json.loads(res)
            if func == "china_macro_query" or func == "industry_data" or func == "foreign_macro_query":
                data = CommonFunction.transfer_macro_data_index(data)
        except Exception as e:
            data = {'result': "查询失败", 'data': e}
        print(data)
        return data

    @staticmethod
    def send_data_by_post(obj, func, select='calculate'):
        """
        :param obj:
        :param func:
        :param select:
        :return:
        """
        url = RootDest().set_path(func=func, select=select)
        response = requests.post(url, headers=SetHeaders().run(), data=json.dumps(obj))
        res = response.content.decode()
        try:
            data = json.loads(res)
        except Exception as e:
            data = {'result': "查询失败", 'data': e}
        print(data)
        return data

    @staticmethod
    def transfer_macro_data_index(data_list):
        ndata_list = []
        for data in data_list["data"]:
            obj = {"date_time": data['date_time'], "index_name": list(data.keys())[1], "value": list(data.values())[1]}
            ndata_list.append(obj)
        result = {'result': '查询成功', 'data': ndata_list}
        return result


