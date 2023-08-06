

from ChosenAPI.function.common import CommonFunction


class CompanyJob(object):
    def __init__(self):
        pass

    def get_data(self, company_name, start_date, end_date, method='actual'):
        """
        :param company_name:
        :param method:
        :param start_date:
        :param end_date:
        :return:
        """
        obj = {"companyName": company_name, "method": method, "startDate": start_date, "endDate": end_date}
        func = "company_job"
        data = CommonFunction.send_data_by_get(obj, func)
        return data