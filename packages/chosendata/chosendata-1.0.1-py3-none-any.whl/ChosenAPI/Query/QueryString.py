
class QueryStringCreate(object):

    def __init__(self, obj):
        self.obj = obj

    def set_string(self):
        """
        :return:
        """
        query_string = '?'
        for key, value in self.obj.items():
            query_string += key + '=' + value + '&'
        query_string = query_string.rstrip('&')
        # print(query_string)
        return query_string
