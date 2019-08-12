# coding: utf-8

"""
@Python         : 3.6.7
@Author         : XuXuepeng-Paul
@Email            : xuepeng_paul_1986@126.com
@Time             : 2019-05-18:15
@File               : handle_base.py
@Project         : general-server
@Licence         : LGPL
@Description  :
"""
import json
import uuid
from copy import deepcopy

from configure.parameter import AppSetting, UserRole
from configure.status import APIStatus
from utils.permission import Permission
from sqlalchemy.exc import SQLAlchemyError
from utils.decorator import decor_logger


class HandlerBase(object):

    fields_require = []
    fields_border = []
    view_roles = [UserRole.ADMIN, UserRole.MANAGER, UserRole.EMPLOYEE]
    edit_roles = [UserRole.ADMIN, UserRole.MANAGER]
    request_info = {}

    def __init__(self, controller_meta, request_info, **kwargs):
        self.controller = controller_meta(**kwargs)
        self.request_info = request_info

    @decor_logger
    def get(self, args_, current_user):
        """
        获取用户信息
        :return:
        """
        res = AppSetting.general_result()
        res["request_info"] = self.request_info
        if not Permission.check_user_role(self.view_roles, current_user["roles"]):
            res["err_code"] = APIStatus.ROLE_FORBIDDEN
            res["message"] = "user role is forbidden: {}".format(current_user["username"])
            res["result"] = "fail"
            return res

        order_key = args_.get("order_key", "-create_time")
        if order_key:
            if order_key.startswith("-"):
                key_check = order_key[1:]
            else:
                key_check = order_key
            if key_check not in self.fields_border:
                res["err_code"] = APIStatus.FIELD_OUTER
                res["message"] = "order_key: [{}] is unknown field".format(key_check)
                res["result"] = "fail"
                return res

        start = args_.get("start", 0)
        count = args_.get("count", 0)

        start = start if isinstance(start, int) and start >= 0 else 0
        count = count if isinstance(count, int) and count >= 0 else 0
        try:
            total = self.controller.count()
            res["data"] = self.controller.all(start=start, count=count, order_key=order_key) or []
        except SQLAlchemyError as err:
            # print(err.orig.args)
            res["err_code"] = APIStatus.DB_ERROR
            res["message"] = json.dumps(err.orig.args)
            res["result"] = "fail"
        except Exception as err:
            res["err_code"] = APIStatus.UNDEFINED
            res["message"] = str(err)
            res["result"] = "fail"
        else:
            res["err_code"] = APIStatus.SUCCESS
            res["total"] = total
        return res

    def _check_unique_field(self, body_, unique_list):
        for key in unique_list:
            if key not in body_ or not body_[key]:
                continue
            search_res = self.controller.search_uk_on_create(key, body_[key])
            if search_res:
                if search_res["deleted"] is None or search_res["deleted"] == "":
                    raise Exception("{key} field has exist value {value}".format(key=key, value=body_[key]))
                else:
                    uid = search_res["uid"]
                    new_body = {
                        key: str(uuid.uuid4()).replace("-", "")
                    }
                    self.controller.update(uid, **new_body)

    @decor_logger
    def post(self, body_, current_user):
        """
        创建新用户
        """
        res = AppSetting.general_result()
        res["request_info"] = self.request_info
        if not Permission.check_user_role(self.edit_roles, current_user["roles"]):
            res["err_code"] = APIStatus.ROLE_FORBIDDEN
            res["message"] = "user role is forbidden: {}".format(current_user["username"])
            res["result"] = "fail"
            return res
        # print(body_)
        for field in self.fields_require:
            if field not in body_:
                res["err_code"] = APIStatus.FIELD_LACK
                res["message"] = "field lack: {}".format(field)
                res["result"] = "fail"
                return res
        for field in list(body_.keys()):
            if field not in self.fields_border:
                body_.pop(field)
        try:
            self._check_unique_field(body_, self.controller.get_model().unique_list)
        except Exception as err:
            res["err_code"] = APIStatus.ALREADY_EXIST
            res["message"] = str(err)
            res["result"] = "fail"
            return res
        try:
            key_word = self.controller.get_model().key_word
            table_name = self.controller.get_model().table_name
            search_res = self.controller.search_keyword_on_create(key_word=body_[key_word])
            if search_res:
                if search_res["deleted"] is None or search_res["deleted"] == "":
                    res["err_code"] = APIStatus.ALREADY_EXIST
                    res["message"] = "{table_name} [{key_word}] is already exist".format(
                        table_name=table_name,
                        key_word=body_[key_word])
                    res["result"] = "fail"
                    return res
                else:
                    uid = search_res["uid"]
                    body_["deleted"] = None
                    self.controller.update(uid, **body_)
                    res["data"] = {"uid": uid}
            else:
                res["data"] = {"uid": self.controller.create(**body_)}
        except SQLAlchemyError as err:
            res["err_code"] = APIStatus.DB_ERROR
            res["message"] = json.dumps(err.orig.args)
            res["result"] = "fail"
        except Exception as err:
            res["err_code"] = APIStatus.UNDEFINED
            res["message"] = str(err)
            res["result"] = "fail"
        else:
            res["err_code"] = APIStatus.SUCCESS
        return res

    @decor_logger
    def put(self, args_, body_, current_user):
        """
        更改用户信息
        :return:
        """
        res = AppSetting.general_result()
        res["request_info"] = self.request_info
        if not Permission.check_user_role(self.edit_roles, current_user["roles"]):
            res["err_code"] = APIStatus.ROLE_FORBIDDEN
            res["message"] = "user role is forbidden: {}".format(current_user["username"])
            res["result"] = "fail"
            return res
        if "item" not in args_ or not args_["item"]:
            res["err_code"] = APIStatus.FIELD_LACK
            res["message"] = "no such params: item"
            res["result"] = "fail"
            return res

        res["data"] = {
            "uid": args_.get("item", "")
        }
        for field in list(body_.keys()):
            if field not in self.fields_border:
                body_.pop(field)
        # print(body_)
        unique_list = deepcopy(self.controller.get_model().unique_list)
        unique_list.append(self.controller.get_model().key_word)
        try:
            self._check_unique_field(body_, unique_list)
        except Exception as err:
            res["err_code"] = APIStatus.ALREADY_EXIST
            res["message"] = str(err)
            res["result"] = "fail"
            return res
        try:
            self.controller.update(args_["item"], **body_)
        except SQLAlchemyError as err:
            res["err_code"] = APIStatus.DB_ERROR
            res["message"] = json.dumps(err.orig.args)
            res["result"] = "fail"
        except Exception as err:
            res["err_code"] = APIStatus.UNDEFINED
            res["message"] = str(err)
            res["result"] = "fail"
        else:
            res["err_code"] = APIStatus.SUCCESS
        res["err_code"] = APIStatus.SUCCESS
        return res

    @decor_logger
    def delete(self, args_, current_user):
        """
        删除用户，逻辑删除
        :return:
        """
        res = AppSetting.general_result()
        res["request_info"] = self.request_info
        if not Permission.check_user_role(self.edit_roles, current_user["roles"]):
            res["err_code"] = APIStatus.ROLE_FORBIDDEN
            res["message"] = "user role is forbidden: {}".format(current_user["username"])
            res["result"] = "fail"
            return res
        if "item" not in args_ or not args_["item"]:
            res["err_code"] = APIStatus.FIELD_LACK
            res["message"] = "no such params: item"
            res["result"] = "fail"
            return res
        res["data"] = {
            "uid": args_.get("item", "")
        }
        try:
            self.controller.delete(args_["item"])
        except SQLAlchemyError as err:
            # print(err.orig.args)
            res["err_code"] = APIStatus.DB_ERROR
            res["message"] = json.dumps(err.orig.args)
            res["result"] = "fail"
        except Exception as err:
            res["err_code"] = APIStatus.UNDEFINED
            res["message"] = str(err)
            res["result"] = "fail"
        else:
            res["err_code"] = APIStatus.SUCCESS
        return res

    @decor_logger
    def search(self, body_, current_user):
        res = AppSetting.general_result()
        res["request_info"] = self.request_info
        if not Permission.check_user_role(self.view_roles, current_user["roles"]):
            res["err_code"] = APIStatus.ROLE_FORBIDDEN
            res["message"] = "user role is forbidden: {}".format(current_user["username"])
            res["result"] = "fail"
            return res
        try:
            res["data"] = self.controller.search(**body_) or []
        except SQLAlchemyError as err:
            # print(err.orig.args)
            res["err_code"] = APIStatus.DB_ERROR
            res["message"] = json.dumps(err.orig.args)
            res["result"] = "fail"
        except Exception as err:
            res["err_code"] = APIStatus.UNDEFINED
            res["message"] = str(err)
            res["result"] = "fail"
        else:
            res["err_code"] = APIStatus.SUCCESS
        return res


if __name__ == '__main__':
    print("handle_base start")
