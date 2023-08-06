

from ChosenAPI.function.common import CommonFunction


class FinanceStatementUS(object):
    def __init__(self, code, period, report_type="end"):
        """
        :param code:
        :param period:
        :param report_type:
        """
        self.code = code
        self.period = period
        self.report_type = report_type

    def get_balance_sheet(self):
        """
        :return:
        """
        obj = {"code": self.code, "period": self.period, "tableName": "BalanceSheetUS", "reportType": "end"}
        func = "finance_statement_us"
        data = CommonFunction.send_data_by_get(obj, func)
        return data

    def get_income_statement(self):
        """
        :return:
        """
        obj = {"code": self.code, "period": self.period, "tableName": "IncomeStatementUS", "reportType": self.report_type}
        func = "finance_statement_us"
        data = CommonFunction.send_data_by_get(obj, func)
        return data

    def get_cash_flow(self):
        """
        :return:
        """
        obj = {"code": self.code, "period": self.period, "tableName": "CashFlowUS", "reportType": self.report_type}
        func = "finance_statement_us"
        data = CommonFunction.send_data_by_get(obj, func)
        return data

