
import requests
import json
from ChosenAPI.Config.RootPath import RootDest
from ChosenAPI.Config.Headers import SetHeaders
from ChosenAPI.Query.QueryString import QueryStringCreate

class CompanyMainInfo(object):
    def __init__(self):
        pass

    def get_data(self, company_name):
        """
        :param company_name:
        :return:
        """
        obj = {"companyName": company_name}
        query = QueryStringCreate(obj).set_string()  # 生成查询字符串
        url = RootDest().set_path(func="company_main_info") + query
        response = requests.get(url, headers=SetHeaders().run())
        res = response.content.decode()
        try:
            data = json.loads(res)
        except Exception as e:
            data = {'result': "查询失败", 'data': e}
        print(data)
        return data