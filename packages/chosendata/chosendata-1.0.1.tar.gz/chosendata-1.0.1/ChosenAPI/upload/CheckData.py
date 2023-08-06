

from ChosenAPI.function.common import CommonFunction
from ChosenAPI.Config.Headers import SetHeaders

class CheckClientData(object):

    def __init__(self):
        pass

    @staticmethod
    def check_all_info():
        """
        :return:
        """
        username = SetHeaders().set_username()
        obj = {"username": username}
        func = "check_client_all_info"
        data = CommonFunction.send_data_by_post(obj, func)
        return data
