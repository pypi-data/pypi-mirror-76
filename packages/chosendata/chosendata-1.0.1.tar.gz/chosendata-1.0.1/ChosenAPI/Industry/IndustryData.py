
from ChosenAPI.function.common import CommonFunction


class IndustryData(object):
    def __init__(self):
        pass

    def show_index_name(self, key_word):
        """
        :param key_word:
        :return:
        """
        obj = {"keyWord": key_word}
        func = "industry_data_index_name"
        data = CommonFunction.send_data_by_get(obj, func)
        return data

    def get_index_data(self, classify_name, index_name, start_date, end_date):
        """
        :param classify_name:
        :param index_name:
        :param start_date:
        :param end_date:
        :return:
        """
        obj = {"classifyName": classify_name, "indexName": index_name, "startDate": start_date, "endDate": end_date}
        func = "industry_data"
        data = CommonFunction.send_data_by_get(obj, func)
        return data
