import json
import struct
import time
from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5
import base64
import hmac
import socket
from ChosenAPI.Settings.HostAndClientSettings import ClientSettings
from ChosenAPI.Config.Headers import SetHeaders


class RsaEncrypted(object):
    def __init__(self):
        self.file_path_username = '../username.txt'

    def creat_key(self, prikey, pubkey):
        """
        生成密钥
        :param prikey:
        :param pubkey:
        :return:
        """
        # 获取一个伪随机数生成器
        random_generator = Random.new().read
        # 获取一个rsa算法对应的密钥对生成器实例
        rsa = RSA.generate(2048, random_generator)

        # 生成私钥并保存
        private_pem = rsa.exportKey()
        with open(prikey, 'wb') as f:
            f.write(private_pem)

        # 生成公钥并保存
        public_pem = rsa.publickey().exportKey()
        with open(pubkey, 'wb') as f:
            f.write(public_pem)

    def encrypt_file(slef, message, pubkey_file):
        """
        加密信息
        :param message: str, 需要加密的数据
        :param pubkey_file: str, 加密公钥文件路径
        :return:
        """
        with open(pubkey_file, 'rb+') as f:
            publicKey = f.read()
        pubKeyObj = RSA.importKey(publicKey)
        cipherObj = Cipher_PKCS1_v1_5.new(pubKeyObj)
        data = base64.b64encode(cipherObj.encrypt(message.encode()))
        return data

    def decrypt_file(self, message, prikey):
        """
        解密信息
        :param message: str, 需要解密的数据
        :param prikey: str, 解密私钥文件路径
        :return:
        """
        with open(prikey, 'rb+') as f:
            privateKey = f.read()
        rsaKeyObj = RSA.importKey(privateKey)
        cipherObj = Cipher_PKCS1_v1_5.new(rsaKeyObj)
        randomGenerator = Random.new().read
        data = cipherObj.decrypt(base64.b64decode(message), randomGenerator)
        data = data.decode()
        return data


class Client(object):
    def __init__(self, ip_port, fromat='token'):
        self.secret_key = ClientSettings().client_server_secret() # 连接识别码,与服务器Server.py同时更改,否则失效
        self.pubkey,  self.bufsize = "./pubkey", 1024   # ./pubkey
        self.ip_port = ip_port

    def get_info(self):
        return self.pubkey, self.ip_port, self.bufsize

    def conn_auth(self, conn):
        """
        :param conn:
        :return:
        """
        server_bytes = conn.recv(32)  # 接收来自服务端的随机bytes
        client_md5_bytes = hmac.new(self.secret_key.encode(), server_bytes, 'md5').digest()  # md5加密后的bytes
        conn.send(client_md5_bytes)  # 把md5加密后的bytes发送给服务端

    def client_handler(self, message,  format="str"):
        """
        :param message: ,
        :param conn:
        :param prikey:
        :param bufsize:
        :return:
        """
        client = socket.socket()
        client.connect(self.ip_port)
        self.conn_auth(client)
        username = SetHeaders().set_username()
        rsa = RsaEncrypted()
        if format == "str":
            inp = message.strip() + ";" + username
            inp = rsa.encrypt_file(inp, self.pubkey)  # 加密
            client.send(inp)
            server_msg = client.recv(self.bufsize) # 从服务端收到信息
            reply = server_msg.decode("utf-8")
        # 新增Json格式的传输方式和粘包处理方案
        elif format == "json":
            inp = json.dumps(message)  # 使用json函数将字典序列化才能传输，不然不能传输

            # inp = rsa.encrypt_file(inp, self.pubkey)  # 将来分段加密
            inp = inp.encode("utf-8")
            length = len(inp)
            data_length = struct.pack("i", length)
            client.send(data_length) # 发送长度
            client.send(inp) # 发送报文
            # 从服务端收消息，解决粘包
            length_data = client.recv(4)
            length = struct.unpack("i", length_data)[0]
            recv_size = 0
            server_msg = b''
            while recv_size < length:
                server_msg += client.recv(self.bufsize)  # 从服务端收到信息
                recv_size = len(server_msg)
            reply = server_msg.decode("utf-8")
            reply = json.loads(reply)  # 读取字典 统一status字段是状态
            # 新增终点
        else:
            reply = "fail"

        if len(reply) > 0:
            print("服务端消息: ", reply)
            client.close()
        else:
            time.sleep(1)
            client.close()
        return reply





