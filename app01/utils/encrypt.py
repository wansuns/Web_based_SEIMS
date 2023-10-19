import hashlib
from django.conf import settings
from django.contrib.auth.handlers.modwsgi import check_password
from django.contrib.auth.hashers import make_password
import random
import string
import time

def md5(key):
    obj = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
    obj.update(key.encode("utf-8"))
    return obj.hexdigest()


class EncryptionUtilWithDjango:
    @staticmethod
    def encrypt_password(password, salt=None):
        """
        对明文密码进行加盐加密，返回加密后的密码
        :param password: 明文密码
        :param salt: 盐值，不指定则随机生成
        :return: 加密后的密码
        """
        return make_password(password, salt=salt, hasher='default', encoding='utf-8')

    @staticmethod
    def verify_password(password, hashed_password):
        """
        验证密码是否正确
        :param password: 明文密码
        :param hashed_password: 加密后的密码
        :return: True or False
        """
        return check_password(password, hashed_password)


class EncryptionUtilWithoutDjango:
    def sha256_with_salt(key):
        """
        对字符串进行 sha256 加密，并添加随机盐
        :param key: 待加密字符串
        :return: 加密后的字符串
        """
        # 随机生成 10 位字符串作为盐
        salt = ''.join(random.sample(string.ascii_letters + str(time.time()), 10))
        hsobj = hashlib.sha256(key.encode("utf-8"))
        hsobj.update(salt.encode("utf-8"))
        return hsobj.hexdigest()

    def md5_with_salt(key, salt='china'):
        """
        对字符串进行 md5 加密，并添加固定盐
        :param key: 待加密字符串
        :param salt: 固定盐
        :return: 加密后的字符串
        """
        hsobj = hashlib.md5(key.encode("utf-8"))
        hsobj.update(salt.encode("utf-8"))
        return hsobj.hexdigest()

    def verify_password(password, hashed_password):
        """
        验证密码是否正确
        :param password: 用户输入的密码
        :param hashed_password: 数据库中存储的已经加盐加密后的密码
        :return: True or False
        """
        algorithm, salt, stored_password = hashed_password.split('$')
        if algorithm == 'md5':
            # 使用 md5 算法验证密码
            hashed_password = password.md5_with_salt(password, salt)
        elif algorithm == 'sha256':
            # 使用 sha256 算法验证密码
            hashed_password = password.sha256_with_salt(password, salt)
        else:
            raise ValueError('Unsupported algorithm')
        return hashed_password == stored_password










