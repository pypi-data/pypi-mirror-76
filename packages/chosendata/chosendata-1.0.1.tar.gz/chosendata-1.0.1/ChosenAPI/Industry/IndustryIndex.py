

from ChosenAPI.function.common import CommonFunction


class IndustryIndex(object):
    def __init__(self):
        pass


    def show_index_name(self, SW1, SW2):
        """
        :param SW1:
        :param SW2:
        :return:
        """
        obj = {"SW1": SW1, "SW2": SW2, "method": "industry"}
        func = "industry_index_name"
        data = CommonFunction.send_data_by_get(obj, func)
        return data

    def show_index_name_by_keyword(self, key_word):
        """
        :param key_word:
        :return:
        """
        obj = {"keyWord": key_word, "method": "keyWord"}
        func = "industry_index_name"
        data = CommonFunction.send_data_by_get(obj, func)
        return data


class IndustryIndexData(object):

    def __init__(self, index_name, start_date, end_date):
        """
        :param index_name:
        :param start_date:
        :param end_date:
        """
        self.index_name = index_name
        self.start_date = start_date
        self.end_date = end_date

    def get_index_data(self):
        """
        :return:
        """
        obj = {"indexName": self.index_name, "startDate": self.start_date, "endDate": self.end_date}
        func = "industry_index_data"
        data = CommonFunction.send_data_by_get(obj, func)
        return data

