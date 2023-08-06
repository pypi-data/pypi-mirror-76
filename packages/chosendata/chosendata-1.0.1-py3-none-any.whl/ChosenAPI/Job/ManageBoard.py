

from ChosenAPI.function.common import CommonFunction


class ManageBoardInfo(object):
    def __init__(self, code):
        self.code = code

    def get_info_by_date(self, start_date, leave_date):
        """
        :param start_date:
        :param leave_date:
        :return:
        """
        obj = {"code": self.code, "startDate": start_date, "leaveDate": leave_date}
        func = "mb_info"
        data = CommonFunction.send_data_by_get(obj, func)
        return data

    def get_info_by_name(self, name):
        """
        :param name: str,
        :return:
        """
        obj = {"code": self.code, "name": name}
        func = "mb_info"
        data = CommonFunction.send_data_by_get(obj, func)
        return data

    def get_info_by_on_job(self, on_job):
        """
        :param on_job:
        :return:
        """
        obj = {"code": self.code, "onJob": on_job}
        func = "mb_info"
        data = CommonFunction.send_data_by_get(obj, func)
        return data

