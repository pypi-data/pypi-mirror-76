
import requests
import json
from ChosenAPI.Config.RootPath import RootDest
from ChosenAPI.Config.Headers import SetHeaders


class VipQuery(object):
    def __init__(self):
        pass

    @staticmethod
    def mongo_query(table_id, condition):
        """
        :param table_id:
        :param condition:
        :return:
        """
        if condition is None or condition == {}:
            print("条件不能为空,请重新定义condition查询条件, 参照mongo")
            return
        func = "vip_mongo_query"
        obj = {"table_id": table_id, "condition": condition}
        url = RootDest().set_path(func=func, select="main")
        headers = SetHeaders().run()
        headers['Content-type'] = "application/json"  # 必须添加,否则后台无法接收json数据
        response = requests.post(url, headers=headers, data=json.dumps(obj))
        res = response.content.decode()
        try:
            data = json.loads(res)
        except Exception as e:
            data = {'result': "查询失败", 'data': e}
        print(data)
        return data
