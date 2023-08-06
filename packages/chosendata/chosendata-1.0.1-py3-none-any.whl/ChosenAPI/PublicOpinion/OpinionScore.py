

from ChosenAPI.function.common import CommonFunction


class CompanyOpinionScore(object):
    def __init__(self, code, start_date, end_date):
        self.code = code
        self.start_date = start_date
        self.end_date = end_date

    def get_score(self):
        """

        :return:
        """
        obj = {"code": self.code, "startDate": self.start_date, "endDate": self.end_date}
        func = "company_opinion_score"
        data = CommonFunction.send_data_by_get(obj, func)
        return data

class IndustryOpinionScore(object):
    def __init__(self):
        pass
