
from ChosenAPI.function.common import CommonFunction


class ChinaMacroData(object):
    def __init__(self):
        pass

    @staticmethod
    def show_all_index_name():
        """
        :return:
        """
        obj = {}
        func = "china_macro_all_index"
        data = CommonFunction.send_data_by_get(obj, func)
        return data

    @ staticmethod
    def query_guide(classify_name_key_word):
        """
        :param classify_name_key_word:
        :return:
        """
        obj = {"classifyNameKeyWord": classify_name_key_word}
        func = "china_macro_guide"
        data = CommonFunction.send_data_by_get(obj, func)
        return data

    @ staticmethod
    def data_query(classify_name, index_name, start_date, end_date):
        """
        根据指标名称查询
        :param classify_name:
        :param index_name:
        :param start_date:
        :param end_date:
        :return:
        """
        obj = {"classifyName": classify_name, "indexName": index_name, "startDate": start_date, "endDate": end_date}
        func = "china_macro_query"
        data = CommonFunction.send_data_by_get(obj, func)
        return data


