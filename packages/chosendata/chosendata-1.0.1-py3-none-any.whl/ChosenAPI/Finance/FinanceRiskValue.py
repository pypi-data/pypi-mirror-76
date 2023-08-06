

from ChosenAPI.function.common import CommonFunction


class FinanceRiskValue(object):

    def __init__(self, code, report_date):
        """
        :param code: str,
        :param report_date: str,
        """
        self.code = code
        self.report_date = report_date

    def model_value(self, model):
        obj = {"code": self.code, "reportDate": self.report_date, "model": model}
        func = "finance_risk_model_value"
        data = CommonFunction.send_data_by_get(obj, func)
        return data
