

from ChosenAPI.function.common import CommonFunction
from ChosenAPI.Config.Headers import SetHeaders


class DeleteClientData(object):

    def __init__(self):
        pass

    @staticmethod
    def delete_finance_data(ID, report_date):
        username = SetHeaders().set_username()
        obj = {'ID': ID, 'report_date': report_date, "username": username}
        func = "delete_client_finance_data"
        data = CommonFunction.send_data_by_post(obj, func)
        return data


