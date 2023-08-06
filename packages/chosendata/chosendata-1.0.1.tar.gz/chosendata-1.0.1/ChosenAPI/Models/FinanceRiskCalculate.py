

from ChosenAPI.function.common import CommonFunction


class FinanceRiskCalculate(object):
    def __init__(self):
        pass

    @staticmethod
    def calculate_request(ID, report_date, method='c'):
        """
        :param ID:
        :param report_date:
        :param method: str,
        :return:
        """
        func = "finance_risk_calculate"
        obj = {"ID": ID, "report_date": report_date, "method": method}
        data = CommonFunction.send_data_by_post(obj, func)
        return data

    @staticmethod
    def get_client_risk_detail(ID, report_date):
        """
        :param ID:
        :param report_date:
        :return:
        """
        func = "finance_risk_client_query"
        obj = {"ID": ID, "report_date": report_date}
        data = CommonFunction.send_data_by_post(obj, func)
        return data

    @staticmethod
    def get_public_risk_detail(ID, report_date):
        """
        :param ID:
        :param report_date:
        :return:
        """
        func = "finance_risk_public_query"
        obj = {"ID": ID, "report_date": report_date}
        data = CommonFunction.send_data_by_post(obj, func)
        return data

    @staticmethod
    def update_client_risk_detail(ID, report_date, _id):
        """
        :param ID:
        :param report_date:
        :return:
        """
        func = "update_risk_client_query"
        obj = {"ID": ID, "report_date": report_date, "_id": _id}
        data = CommonFunction.send_data_by_post(obj, func)
        return data