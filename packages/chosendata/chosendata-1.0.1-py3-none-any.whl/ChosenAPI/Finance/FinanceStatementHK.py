

from ChosenAPI.function.common import CommonFunction


class FinanceStatementHK(object):
    def __init__(self, code, report_date, report_type="end"):
        """
        :param code: str,
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
        obj = {"code": self.code, "reportDate": self.report_date, "tableName": "BalanceSheetHK", "reportType": "end"}
        func = "finance_statement_hk"
        data = CommonFunction.send_data_by_get(obj, func)
        return data

    def get_income_statement(self):
        """
        :return:
        """
        obj = {"code": self.code, "reportDate": self.report_date, "tableName": "IncomeStatementHK", "reportType": self.report_type}
        func = "finance_statement_hk"
        data = CommonFunction.send_data_by_get(obj, func)
        return data

    def get_cash_flow(self):
        """
        :return:
        """
        obj = {"code": self.code, "reportDate": self.report_date, "tableName": "CashFlowHK", "reportType": self.report_type}
        func = "finance_statement_hk"
        data = CommonFunction.send_data_by_get(obj, func)
        return data
