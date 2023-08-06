import datetime
import random


class CreateID(object):
    def __init__(self):
        pass

    def creation(self):
        """
        :return:
        """
        nowstamp = datetime.datetime.now().timestamp() # 获取系统时间的时间戳
        print(type(nowstamp))
        nowstamp_str = str(nowstamp).replace(".", "")  # 转换成str
        ran = random.randint(1000, 9999) # 1000-9999产生随机数
        ran_str = str(ran)
        sample_id = ran_str + nowstamp_str
        return sample_id


