
from ChosenAPI.function.common import CommonFunction


class CompanyNewsFromInterface(object):
    def __init__(self, code):
        self.code = code

    def get_news_summary(self, start_date, end_date):
        """
        :param start_date:
        :param end_date:
        :return:
        """
        obj = {"code": str(self.code), "startDate": start_date, "endDate": end_date, "info": "summary"}  # 通过summary控制后台
        func = "company_news"
        data = CommonFunction.send_data_by_get(obj, func)
        return data

    def get_news_content(self, start_date, end_date):
        """
        :param start_date:
        :param end_date:
        :return:
        """
        obj = {"code": str(self.code), "startDate": start_date, "endDate": end_date, "info": "content"}  # 通过summary控制后台
        func = "company_news"
        data = CommonFunction.send_data_by_get(obj, func)
        return data

    def get_news_content_by_keywords(self, start_date, end_date, keywords):
        """
        :param start_date:
        :param end_date:
        :param keywords:
        :return:
        """
        obj = {"code": str(self.code), "startDate": start_date, "endDate": end_date, "info": "keywords", "keyWords": "|".join(keywords).rstrip("|")}  # 通过summary控制后台
        func = "company_news_by_keywords"
        data = CommonFunction.send_data_by_get(obj, func)
        return data



