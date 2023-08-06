from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5
import base64


def creat_key(prikey, pubkey):
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


def encrypt_file(message, pubkey_file):
    with open(pubkey_file, 'rb+') as f:
        publicKey = f.read()
    pubKeyObj = RSA.importKey(publicKey)
    cipherObj = Cipher_PKCS1_v1_5.new(pubKeyObj)
    data = base64.b64encode(cipherObj.encrypt(message.encode()))
    return data


def decrypt_file(message, prikey):
    with open(prikey, 'rb+') as f:
        privateKey = f.read()
    rsaKeyObj = RSA.importKey(privateKey)
    cipherObj = Cipher_PKCS1_v1_5.new(rsaKeyObj)
    randomGenerator = Random.new().read
    data = cipherObj.decrypt(base64.b64decode(message), randomGenerator)
    data = data.decode()
    return data



