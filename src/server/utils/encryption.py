# coding: utf-8

"""
@Python         : 3.6.7
@Author         : XuXuepeng-Paul
@Email            : xuepeng_paul_1986@126.com
@Time             : 2019-05-18:15
@File               : encryption.py
@Project         : general-server
@Licence         : LGPL
@Description  :
"""
import json
import rsa
from binascii import b2a_hex, a2b_hex


class RsaCrypt(object):
    def __init__(self, prime_tuple):
        self.pub_key = rsa.PublicKey(*prime_tuple[:2])
        self.pri_key = rsa.PrivateKey(*prime_tuple)

    def set_key(self, pub, pri):
        self.pub_key = pub
        self.pri_key = pri

    def encrypt(self, text):
        cipher_text = rsa.encrypt(text.encode(), self.pub_key)
        # 因为rsa加密时候得到的字符串不一定是ascii字符集的，输出到终端或者保存时候可能存在问题
        # 所以这里统一把加密后的字符串转化为16进制字符串
        return b2a_hex(cipher_text)

    def decrypt(self, text):
        decrypt_text = rsa.decrypt(a2b_hex(text), self.pri_key)
        return decrypt_text

    @staticmethod
    def new_prime_tuple(bytes_count=256):
        _, prime_obj = rsa.newkeys(bytes_count)
        prime_tuple = (prime_obj.n, prime_obj.e, prime_obj.d, prime_obj.p, prime_obj.q)
        return json.dumps(prime_tuple)


if __name__ == '__main__':
    print("encryption start")
