

from ChosenAPI.function.common import CommonFunction


class IndustryReport(object):
    def __init__(self):
        pass

    def get_summary(self, industry, method, start_date, end_date):
        """
        :param industry:
        :param method:
        :param start_date:
        :param end_date:
        :return:
        """
        obj = {"industry": industry, "method": method, "startDate": start_date, "endDate": end_date, "info": "summary"}
        func = "industry_report"
        data = CommonFunction.send_data_by_get(obj, func)
        return data


    def get_content(self, industry, method, start_date, end_date):
        """
        :param industry:
        :param method:
        :param start_date:
        :param end_date:
        :return:
        """
        obj = {"industry": industry, "method": method, "startDate": start_date, "endDate": end_date, "info": "content"}
        func = "industry_report"
        data = CommonFunction.send_data_by_get(obj, func)
        return data