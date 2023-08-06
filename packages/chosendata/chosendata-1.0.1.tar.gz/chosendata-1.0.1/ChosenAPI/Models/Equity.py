

from ChosenAPI.function.common import CommonFunction
import numpy as np


class EquityModel(object):
    def __init__(self):
        pass

    @staticmethod
    def var_risk_valuation(s, code_list, w, n, x, method, start_date=None, end_date=None, risk_date=None, i=10000):
        """
        :param s:
        :param code_list:
        :param w:
        :param n:
        :param x:
        :param method:
        :param start_date:
        :param end_date:
        :param risk_date:
        :param i:
        :return:
        """
        if np.sum(w) != 1:
            print("error:", "组合比例不等于1")
            return
        func = "var_risk_valuation"
        obj = {"s": s, "code_list": code_list, "w": w, "n": n, "x": x, "start_date": start_date, "end_date": end_date, "risk_date": risk_date, "i": i, "method":method}
        data = CommonFunction.send_data_by_post(obj, func)
        return data