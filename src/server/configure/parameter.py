# coding: utf-8

"""
@Python         : 3.6.7
@Author         : XuXuepeng-Paul
@Email            : xuepeng_paul_1986@126.com
@Time             : 2019-05-18:15
@File               : parameter.py
@Project         : general-server
@Licence         : LGPL
@Description  :
"""
import os
from copy import deepcopy


class MysqlParameter(object):
    DB_NAME = 'ai_lab'
    USER = 'root'
    PASSWORD = '123456'
    HOST = 'localhost'
    PORT = 3306


class AppSetting(object):
    BASE_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
    DOWN_FILE_DIR = "mid_data/toDown"
    UP_FILE_DIR = "mid_data/toUpload"
    AUTH_KEY = "Authorization"
    SECRET_KEY = "sdsgsgsfgsddf"
    TOKEN_SECRET = "fdfshjkfhskjkhuihfdhkjdkfjghjkdhjkhkjgfd"
    RES_GENERAL = {"err_code": 2000, "result": "ok", "message": "", "cmd": ""}

    @classmethod
    def general_result(cls):
        return deepcopy(cls.RES_GENERAL)

    GENERATOR_TIME = "%Y-%m-%d %H:%M:%S"
    DB_USER_HASH = "cccdde1@34"

    TOKEN_EXTERNAL = [
        "/api/general/login/",
        "/api/general/db-init/",
        "/api/dashboard/",
        "/api/dashboard/swagger.json",
    ]


class UserRole(object):
    ADMIN = "admin"
    MANAGER = "manager"
    EMPLOYEE = "employee"
    CUSTOM_LEADER = "custom_leader"
    CUSTOM_EMPLOYEE = "custom_employee"


if __name__ == '__main__':
    print("parameter start")
