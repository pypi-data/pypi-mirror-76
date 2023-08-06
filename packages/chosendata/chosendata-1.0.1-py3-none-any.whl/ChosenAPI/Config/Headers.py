

class SetHeaders(object):

    def __init__(self):
        self.base_header = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",

        }
        self.file_path_token = '../token.txt'
        self.file_path_username = '../username.txt'

    def set_authorization(self):
        try:
            with open(self.file_path_token, "r", encoding='utf-8') as f:  # 设置文件对象
                content = f.read()
                self.base_header.update({'Authorization': "Bearer " + content})
        except Exception as e:
            print(e)
            self.base_header.update({'Authorization': ''})

    def set_username(self):
        try:
            with open(self.file_path_username, "r", encoding='utf-8') as f:  # 设置文件对象
                content = f.read()
                self.base_header.update({'username': content})
        except Exception as e:
            print(e)
            self.base_header.update({'username': ''})
        return content

    def run(self):
        h = SetHeaders()
        h.set_authorization()
        h.set_username()
        return h.base_header
