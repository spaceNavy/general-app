# coding: utf-8

"""
@Python         : 3.6.7
@Author         : XuXuepeng-Paul
@Email            : xuepeng_paul_1986@126.com
@Time             : 2019-05-18:15
@File               : tornado/api_dashboard.py
@Project         : general-server
@Licence         : LGPL
@Description  :
"""
import json
from werkzeug.security import generate_password_hash
from configure.parameter import MysqlParameter
from .api_base import ApiBase
from handler.handle_drive import *


class ApiUser(ApiBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.handler = HandlerUser(
            self.request_info,
            user=MysqlParameter.USER,
            password=MysqlParameter.PASSWORD,
            host=MysqlParameter.HOST,
            port=MysqlParameter.PORT,
            schema=MysqlParameter.DB_NAME,
        )

    def post(self):
        """
        创建新用户
        """
        if "password" in self.body_:
            self.body_["password"] = generate_password_hash(self.body_["password"])
        if "company" in self.body_ and not self.body_["company"]:
            self.body_["company"] = None
        res = self.handler.post(self.body_, self.current_user)
        self.write(json.dumps(res))
        self.finish()
        return

    def put(self):
        """
        更改用户信息
        :return:
        """
        if "password" in self.body_:
            self.body_["password"] = generate_password_hash(self.body_["password"])
        if self.body_.get("leader", "") == "":
            self.body_["leader"] = None
        res = self.handler.put(self.args_, self.body_, self.current_user)
        self.write(json.dumps(res))
        self.finish()
        return


class ApiRole(ApiBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.handler = HandlerRole(
            self.request_info,
            user=MysqlParameter.USER,
            password=MysqlParameter.PASSWORD,
            host=MysqlParameter.HOST,
            port=MysqlParameter.PORT,
            schema=MysqlParameter.DB_NAME,
        )


class ApiCompany(ApiBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.handler = HandlerCompany(
            self.request_info,
            user=MysqlParameter.USER,
            password=MysqlParameter.PASSWORD,
            host=MysqlParameter.HOST,
            port=MysqlParameter.PORT,
            schema=MysqlParameter.DB_NAME,
        )
        self.user_handler = HandlerUser(
            self.request_info,
            user=MysqlParameter.USER,
            password=MysqlParameter.PASSWORD,
            host=MysqlParameter.HOST,
            port=MysqlParameter.PORT,
            schema=MysqlParameter.DB_NAME,
        )

    def post(self):
        """
        创建一个新的company
        :return:
        """
        self.body_["password"] = ""
        res = self.handler.post(self.body_, self.current_user)
        if res["err_code"] == APIStatus.SUCCESS and self.body_["leader"]:
            user_res = self.user_handler.put(
                {"item": self.body_["leader"]},
                {"company": res["data"]["uid"]},
                self.current_user)
            res["data"]["user"] = user_res
        self.write(json.dumps(res))
        self.finish()
        return


if __name__ == '__main__':
    print("api_dashboard start")
