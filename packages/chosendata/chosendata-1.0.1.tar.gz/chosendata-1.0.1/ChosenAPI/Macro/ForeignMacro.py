
from ChosenAPI.function.common import CommonFunction


class ForeignMacroData(object):
    def __init__(self, region):
        self.region = region


    def show_all_index_name(self):
        """
        :return:
        """
        obj = {"region": self.region}
        func = "foreign_macro_all_index"
        data = CommonFunction.send_data_by_get(obj, func)
        return data


    def query_guide(self, classify_name_key_word):
        """
        :param classify_name_key_word:
        :return:
        """
        obj = {"classifyNameKeyWord": classify_name_key_word, "region": self.region}
        func = "foreign_macro_guide"
        data = CommonFunction.send_data_by_get(obj, func)
        return data

    def data_query(self, classify_name, index_name, start_date, end_date):
        """
        根据指标名称查询
        :param classify_name
        :param index_name:
        :param start_date:
        :param end_date:
        :return:
        """
        obj = {"classifyName": classify_name, "indexName": index_name, "startDate": start_date, "endDate": end_date, "region": self.region}
        func = "foreign_macro_query"
        data = CommonFunction.send_data_by_get(obj, func)
        return data


