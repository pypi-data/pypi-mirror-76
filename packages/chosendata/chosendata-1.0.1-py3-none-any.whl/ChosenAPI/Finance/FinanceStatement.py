
from ChosenAPI.function.common import CommonFunction


class FinanceStatement(object):
    def __init__(self, code, report_date, report_type="end"):
        """
        :param code:
        :param report_date:
        :param report_type:
        """
        self.code = code
        self.report_date = report_date
        self.report_type = report_type

    def get_balance_sheet(self):
        """
        :return:
        """
        obj = {"code": self.code, "reportDate": self.report_date, "tableName": "BalanceSheet", "reportType": "end"}
        func = "finance_statement"
        data = CommonFunction.send_data_by_get(obj, func)
        return data

    def get_income_statement(self):
        """
        :return:
        """
        obj = {"code": self.code, "reportDate": self.report_date, "tableName": "IncomeStatement", "reportType": self.report_type}
        func = "finance_statement"
        data = CommonFunction.send_data_by_get(obj, func)
        return data

    def get_cash_flow(self):
        """
        :return:
        """
        obj = {"code": self.code, "reportDate": self.report_date, "tableName": "CashFlow", "reportType": self.report_type}
        func = "finance_statement"
        data = CommonFunction.send_data_by_get(obj, func)
        return data


class BussinessComposition(object):
    def __init__(self):
        pass

    @ staticmethod
    def get_data(code, report_date, classify):
        """
        :param code:
        :param report_date:
        :param classify:
        :return:
        """
        obj = {"code": code, "reportDate": report_date, "tableName": "BussinessComposition", "classify": classify}
        func = "bussiness_composition"
        data = CommonFunction.send_data_by_get(obj, func)
        return data