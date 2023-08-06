

import requests
import json
from ChosenAPI.Config.RootPath import RootDest
from ChosenAPI.Config.Headers import SetHeaders
from ChosenAPI.function.common import CommonFunction


class GetOption(object):

    def __init__(self):
        pass


    def iv_recommendation(self, ID):
        """
        :param ID:
        :return:
        """
        url = RootDest().set_path(func="option_recommendation", select='calculate')
        response = requests.post(url, headers=SetHeaders().run(), data={"ID": ID})
        res = response.content.decode()
        try:
            data = json.loads(res)
        except Exception as e:
            data = {'result': "查询失败", 'data': e}
        print(data)
        return data

    def option_value(self, s, k, sigma, r, t0, t1, option_type):
        """
        欧式期权价值
        :param s:
        :param k:
        :param sigma:
        :param r:
        :param t0:
        :param t1:
        :param option_type:
        :return:
        """
        obj = {"s": s, "k":k, "sigma": sigma, "r": r, "t0": t0, "t1": t1, "option_type": option_type}
        func = "call_option_value"
        data = CommonFunction.send_data_by_post(obj, func)
        return data

    def option_letter(self, s, k, sigma, r, t0, t1, option_type):
        """
        :param s:
        :param k:
        :param sigma:
        :param r:
        :param t0:
        :param t1:
        :param option_type:
        :return:
        """
        obj = {"s": s, "k": k, "sigma": sigma, "r": r, "t0": t0, "t1": t1, "option_type": option_type}
        func = "option_letter"
        data = CommonFunction.send_data_by_post(obj, func)
        return data

    def option_iv(self, P, S, K, r, t0, t1, option_type):
        """
        :param P:
        :param S:
        :param K:
        :param r:
        :param t0:
        :param t1:
        :param option_type:
        :return:
        """
        obj = {"P": P, "S": S, "K": K, "r": r, "t0": t0, "t1": t1, "option_type": option_type}
        func = "option_iv"
        data = CommonFunction.send_data_by_post(obj, func)
        return data


