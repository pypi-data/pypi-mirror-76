
import requests
import json
from ChosenAPI.Config.RootPath import RootDest
from ChosenAPI.Config.Headers import SetHeaders

class RelativeValuation(object):
    def __init__(self):
        pass

    def valuation_recommendation(self, dic):
        """
        :param dic:
        :return:
        """
        url = RootDest().set_path(func="relative_valuation_recommendation", select='calculate')
        response = requests.post(url, headers=SetHeaders().run(), data=json.dumps(dic))
        res = response.content.decode()
        try:
            data = json.loads(res)
        except Exception as e:
            data = {'result': "查询失败", 'data': e}
        print(data)
        return data

    def valuation(self, dic):
        """
        :param dic:
        :return:
        """
        url = RootDest().set_path(func="relative_valuation", select='calculate')
        response = requests.post(url, headers=SetHeaders().run(), data=json.dumps(dic))
        res = response.content.decode()
        try:
            data = json.loads(res)
        except Exception as e:
            data = {'result': "查询失败", 'data': e}
        print(data)
        return data