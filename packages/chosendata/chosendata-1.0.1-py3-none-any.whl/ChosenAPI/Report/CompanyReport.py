

from ChosenAPI.function.common import CommonFunction


class CompanyReport(object):

    def __init__(self, code):
        """
        :param code:
        """
        self.code = code

    def get_listcompany_report(self, start_date, end_date):
        """
        :param start_date:
        :param end_date:
        :return:
        """
        obj = {"code": str(self.code), "startDate": start_date, "endDate": end_date}  # 通过summary控制后台
        func = "listcompany_report"
        data = CommonFunction.send_data_by_get(obj, func)
        return data
        
