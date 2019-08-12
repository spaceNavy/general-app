# coding: utf-8

"""
@Python         : 3.6.7
@Author         : XuXuepeng-Paul
@Email            : xuepeng_paul_1986@126.com
@Time             : 2019-05-18:15
@File               : handle_drive.py
@Project         : general-server
@Licence         : LGPL
@Description  :
"""
import json
import time

import jwt

from werkzeug.security import check_password_hash

from .handle_base import HandlerBase
from controller.alchemy.control_derive import *
from configure.status import APIStatus
from utils.decorator import decor_logger
from configure.parameter import AppSetting


class HandlerLogin(HandlerBase):

    def __init__(self, request_info, **kwargs):
        super().__init__(ControllerUser, request_info, **kwargs)

    @decor_logger
    def get(self, args_, headers):
        res = AppSetting.general_result()

        res["cmd"] = "token_info"
        if AppSetting.AUTH_KEY not in headers:
            res["result"] = "fail"
            res["err_code"] = APIStatus.TOKEN_BROKEN
            res["message"] = "no token"
            return res
        token = headers[AppSetting.AUTH_KEY]
        try:
            user_payload = jwt.decode(token, AppSetting.TOKEN_SECRET, algorithm='HS256')
        except Exception as err:
            res["result"] = "fail"
            res["err_code"] = APIStatus.TOKEN_BROKEN
            res["message"] = str(err)
            return res

        res["data"] = user_payload
        self.request_info["username"] = user_payload["username"]
        res["request_info"] = self.request_info
        res["data"]["token"] = token
        res["err_code"] = APIStatus.SUCCESS
        return res

    @decor_logger
    def put(self, args_, body_, current_user=None):
        res = AppSetting.general_result()
        res["cmd"] = "login"
        self.request_info["username"] = body_["username"]
        res["request_info"] = self.request_info
        if not body_ or "username" not in body_ or body_["username"] == "":
            res["err_code"] = APIStatus.USER_ERROR
            res["result"] = "fail"
            res["message"] = "user name empty"
            return res
        try:
            user = self.controller.search(username=body_["username"])
        except Exception as err:
            res["err_code"] = APIStatus.DB_ERROR
            res["result"] = "fail"
            res["message"] = str(err)
            return res
        if not user:
            res["err_code"] = APIStatus.USER_ERROR
            res["result"] = "fail"
            res["message"] = "user name error"
            return res
        if not check_password_hash(user["password"], body_["password"]):
            res["err_code"] = APIStatus.PASS_WORD_ERROR
            res["result"] = "fail"
            res["message"] = "user password error"
            return res
        roles = [user["role_ref"]["code"]]
        username = body_["username"]
        expire_time = int(time.time() + 3600 * 12)
        encoded = jwt.encode(
            {
                'uid': user["uid"],
                "username": username,
                "name": user["name"],
                "roles": roles,
                'exp': expire_time
            },
            AppSetting.TOKEN_SECRET,
            algorithm='HS256')
        token = str(encoded, encoding='utf-8')
        self.controller.update(user["uid"], is_login=True)
        res["err_code"] = APIStatus.SUCCESS
        res["data"] = {
            "roles": roles,
            "username": username,
            "token": token,
            "name": user["name"],
        }
        return res

    @decor_logger
    def delete(self, headers, current_user=None):
        res = AppSetting.general_result()
        res["cmd"] = "logout"
        if AppSetting.AUTH_KEY not in headers:
            res["result"] = "fail"
            res["err_code"] = APIStatus.TOKEN_BROKEN
            res["message"] = "no token"
            return res
        token = headers[AppSetting.AUTH_KEY]
        try:
            user_payload = jwt.decode(token, AppSetting.TOKEN_SECRET, algorithm='HS256')
        except Exception as err:
            res["result"] = "fail"
            res["err_code"] = APIStatus.TOKEN_BROKEN
            res["message"] = str(err)
            return res
        self.request_info["username"] = user_payload["username"]
        res["request_info"] = self.request_info
        try:
            user = self.controller.search(username=user_payload["username"])
        except Exception as err:
            res["err_code"] = APIStatus.DB_ERROR
            res["result"] = "fail"
            res["message"] = str(err)
            return res
        if not user:
            res["err_code"] = APIStatus.USER_ERROR
            res["result"] = "fail"
            res["message"] = "user name error"
            return res
        self.controller.update(user_payload["uid"], is_login=False)
        res["err_code"] = APIStatus.SUCCESS

        return res


class HandlerUser(HandlerBase):

    fields_require = ["username", "password", "name", "email", "phone", "role"]
    fields_border = ["username", "password", "name", "email", "phone", "role",
                     "laboratory", "is_login", "is_valid", "create_time"]

    def __init__(self, request_info, **kwargs):
        super().__init__(ControllerUser, request_info, **kwargs)


class HandlerUserSingle(HandlerUser):

    def get(self, _args, user):
        pass


class HandlerRole(HandlerBase):

    fields_border = ["name", "code", "level", "create_time"]
    fields_require = ["name", "code", "level"]

    def __init__(self, request_info, **kwargs):
        super().__init__(ControllerRole, request_info, **kwargs)


class HandlerCompany(HandlerBase):

    fields_border = ["name", "leader", "seller", "comment", "password", "create_time"]
    fields_require = ["name", "leader", "seller", "password"]

    def __init__(self, request_info, **kwargs):
        super().__init__(ControllerCompany, request_info, **kwargs)


if __name__ == '__main__':
    print("handle_child start")
