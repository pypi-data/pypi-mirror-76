

import requests
import json
from ChosenAPI.Config.RootPath import RootDest
from ChosenAPI.Config.Headers import SetHeaders
from ChosenAPI.function.common import CommonFunction


class GetAuth(object):

    def __init__(self, username, password):
        """
        :param username: str,
        :param password: str,
        """
        self.username = username
        self.password = password

    def login(self):
        """
        :return:
        """
        url = RootDest().set_path(func="login")
        response = requests.post(url, headers=SetHeaders().run(), data={"username": self.username, "password": self.password})
        res = response.content.decode()
        data = json.loads(res)
        if data["result"] == "登陆成功":
            with open('../token.txt', 'w', encoding='utf-8') as wf:
                wf.write(data["token"])
            with open('../username.txt', 'w', encoding='utf-8') as wu:
                wu.write(self.username)
        print(data)

    def check_user(self):
        """
        :return:
        """
        obj = {"username": self.username, "password": self.password}
        func = "check_user"
        data = CommonFunction.send_data_by_get(obj, func)
        return data

