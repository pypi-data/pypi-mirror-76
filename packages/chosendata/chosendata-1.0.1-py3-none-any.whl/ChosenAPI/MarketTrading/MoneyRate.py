
from ChosenAPI.function.common import CommonFunction


class MoneyRateTrade(object):
    def __init__(self):
        pass

    def get_shibor_trade_daily(self, start_date, end_date):
        """
        :param start_date:
        :param end_date:
        :return:
        """
        obj = {"startDate": start_date, "endDate": end_date, "info": "shibor"}
        func = "money_trade"
        data = CommonFunction.send_data_by_get(obj, func)
        return data

    def get_libor_trade_daily(self, start_date, end_date, currency='USD'):
        """
        :param start_date:
        :param end_date:
        :param currency:
        :return:
        """
        obj = {"startDate": start_date, "endDate": end_date, "currency": currency, "info": "libor"}
        func = "money_trade"
        data = CommonFunction.send_data_by_get(obj, func)
        return data

    def get_hibor_trade_daily(self, start_date, end_date):
        """
        :param start_date:
        :param end_date:
        :return:
        """
        obj = {"startDate": start_date, "endDate": end_date, "info": "hibor"}
        func = "money_trade"
        data = CommonFunction.send_data_by_get(obj, func)
        return data