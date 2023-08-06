

from ChosenAPI.function.common import CommonFunction


class EquityPortfolio(object):
    def __init__(self):
        pass

    def get_best_portfolio_weight(self, code_list, start_date, end_date):
        """
        :param code_list:,
        :param start_date:
        :param end_date:
        :return:
        """
        obj = {"code_list": code_list, "start_date": start_date, "end_date": end_date}
        func = "best_equity_portfolio"
        data = CommonFunction.send_data_by_post(obj, func)
        return data


    def get_related_coefficient(self, code_list, start_date, end_date):
        """
        :param code_list:
        :param start_date:
        :param end_date:
        :return:
        """
        obj = {"code_list": code_list, "start_date": start_date, "end_date": end_date}
        func = "related_coefficient"
        data = CommonFunction.send_data_by_post(obj, func)
        return data

    def get_capm_model_value(self, code, contrast_index, start_date, end_date):
        """
        :param code:
        :param contrast_index:
        :param start_date:
        :param end_date:
        :return:
        """
        obj = {"code": code, "contrast_index": contrast_index, "start_date": start_date, "end_date": end_date}
        func = "CAMP_model_value"
        data = CommonFunction.send_data_by_post(obj, func)
        return data

