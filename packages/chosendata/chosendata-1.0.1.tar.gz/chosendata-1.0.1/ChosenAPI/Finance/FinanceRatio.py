

from ChosenAPI.function.common import CommonFunction


class FinanceRatio(object):
    def __init__(self, code, report_date, username="Public"):
        """
        :param username:
        :param code:
        :param report_date:
        """
        self.code = code
        self.report_date = report_date
        self.username = username


    def get_all_data(self):
        """
        :return:
        """
        obj = {"code": self.code, "reportDate": self.report_date, "classify": "all", "username": self.username}
        func = "finance_ratio"
        data = CommonFunction.send_data_by_get(obj, func)
        return data

    def get_given_data(self, classify):
        """
        :param classify:
        :return:
        """
        pass
