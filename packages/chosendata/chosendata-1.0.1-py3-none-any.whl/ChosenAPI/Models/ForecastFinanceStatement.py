

import requests
import json
from ChosenAPI.Config.RootPath import RootDest
from ChosenAPI.Config.Headers import SetHeaders


class ForecastFinanceStatement(object):
    def __init__(self):
        pass

    def forecast_recommendation(self, dic):
        """
        :param dic:
        :return:
        """
        url = RootDest().set_path(func="forecast_statement_recommendation", select='calculate')
        response = requests.post(url, headers=SetHeaders().run(), data={"ID": dic['ID'], "periods": dic['periods'], "recommend": dic['recommend']})
        res = response.content.decode()
        try:
            data = json.loads(res)
        except Exception as e:
            data = {'result': "查询失败", 'data': e}
        print(data)
        return data

    def forecast_statement(self, dic):
        """
        :param dic:
        :return:
        """
        with open('../username.txt', "r", encoding='utf-8') as f:  # 设置文件对象
            username = f.read()
        dic.update({'username': username})  # 添加用户名
        url = RootDest().set_path(func="forecast_finance_statement", select='calculate')
        response = requests.post(url, headers=SetHeaders().run(), data=json.dumps(dic))
        res = response.content.decode()
        try:
            data = json.loads(res)
        except Exception as e:
            data = {'result': "查询失败", 'data': e}
        print(data)


        return data
