

from ChosenAPI.function.common import CommonFunction

class AbsoluteValuation(object):
    def __init__(self):
        pass

    def valuation_recommendation(self, dic):
        """
        :param dic:
        :return:
        """
        func = "absolute_valuation_recommendation"
        data = CommonFunction.send_data_by_post(dic, func)
        return data

    def valuation(self, dic):
        """
        :param dic:
        :return:
        """
        func = "absolute_valuation"
        data = CommonFunction.send_data_by_post(dic, func)
        return data