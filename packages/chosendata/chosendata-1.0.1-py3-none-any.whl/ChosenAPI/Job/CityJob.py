
from ChosenAPI.function.common import CommonFunction


class CityJob(object):

    def __init__(self):
        pass

    def get_data(self, city, start_date, end_date):
        """
        :param city:
        :param start_date:
        :param end_date:
        :return:
        """
        obj = {"city": city, "startDate": start_date, "endDate": end_date}
        func = "city_job"
        data = CommonFunction.send_data_by_get(obj, func)
        return data