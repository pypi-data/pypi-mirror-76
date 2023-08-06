
from ChosenAPI.function.common import CommonFunction

class OptionTrade(object):
    def __init__(self):
        pass

    def get_ch_option_info(self, exchange, option_type, exercise_type):
        """
        :param exchange:
        :param option_type:
        :param exercise_type:
        :return:
        """
        obj = {"exchange": exchange, "optionType": option_type, "exerciseType": exercise_type}
        func = "ch_option_info"
        data = CommonFunction.send_data_by_get(obj, func)
        return data

    def get_ch_option_trade_daily_by_code(self, code):
        """
        :param code:
        :return:
        """
        obj = {"code": code, "method": "code"}
        func = "ch_option_trade"
        data = CommonFunction.send_data_by_get(obj, func)
        return data

    def get_ch_option_trade_daily_by_date(self, exchange, start_date, end_date):
        """
        :param exchange:
        :param start_date:
        :param end_date:
        :return:
        """
        obj = {"exchange": exchange, "startDate": start_date, "endDate": end_date, "method": "exchange"}
        func = "ch_option_trade"
        data = CommonFunction.send_data_by_get(obj, func)
        return data
