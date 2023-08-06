

from ChosenAPI.function.common import CommonFunction


class HotSearchEvent(object):
    def __init__(self):
        pass

    def show_event_info(self, platform, keyword, start_date, end_date):
        """
        获取热搜的主要信息
        :param platform:
        :param keyword:
        :param start_date:
        :param end_date:
        :return:
        """
        obj = {'classify': 'data', 'parameter': {'filter': {'pubdate': {'$gte': start_date + 'T00:00:00Z', "$lte": end_date + "T23:59:59Z"}, 'title': {'$regex': keyword, '$options': 'i'}}, 'platform': platform}}
        func = "hot_search_event"
        data = CommonFunction.send_data_by_post(obj, func)
        return data

    def show_event_score(self, platform, title):
        """
        :param platform:
        :param title:
        :return:
        """
        obj = {'classify': 'paint', 'parameter': {'filter': {'title': title}, 'platform': platform}}
        func = "hot_search_event"
        data = CommonFunction.send_data_by_post(obj, func)
        return data