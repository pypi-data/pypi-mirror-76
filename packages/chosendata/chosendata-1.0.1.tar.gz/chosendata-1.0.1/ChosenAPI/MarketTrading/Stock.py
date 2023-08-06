

from ChosenAPI.function.common import CommonFunction

class StockTrade(object):
    def __init__(self):
        pass

    def get_ch_stock_trade_daily(self, code, start_date, end_date):
        """
        :param code:
        :param start_date:
        :param end_date:
        :return:
        """
        obj = {"code": code, "startDate": start_date, "endDate": end_date}
        func = "ch_stock_trade_daily"
        data = CommonFunction.send_data_by_get(obj, func)
        return data


