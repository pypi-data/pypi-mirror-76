

class ChangeData(object):
    def __init__(self):
        pass

    def Changing(self, data):
        # if data is None:
        #     data = float(0)
        # else:
        #     data = data
        # return data
        if type(data) == str and len(data) == 0:
            data = float(0)
        else:
            data = data
        return data


if __name__ == "__main__":
    ch = ChangeData()
    data = ch.Changing("ch")
    print(data)