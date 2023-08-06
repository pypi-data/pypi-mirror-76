

from ChosenAPI.function.common import CommonFunction


class RealTimeNewsFromInterface(object):
    def __init__(self):
        pass


    def get_fresh_news(self):
        """
        :return:
        """
        obj = {}
        func = "real_time_news"
        data = CommonFunction.send_data_by_get(obj, func)
        return data

    def get_fresh_news_by_keywords(self, keywords):
        """
        :param keywords:
        :return:
        """
        obj = {"keyWords": "|".join(keywords).rstrip("|")}
        func = "real_time_news_by_keywords"
        data = CommonFunction.send_data_by_get(obj, func)
        return data