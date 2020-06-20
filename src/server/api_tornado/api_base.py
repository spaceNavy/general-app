# coding: utf-8

"""
@Python         : 3.6.7
@Author         : XuXuepeng-Paul
@Email            : xuepeng_paul_1986@126.com
@Time             : 2019-05-18:15
@File               : tornado/api_base.py
@Project         : general-server
@Licence         : LGPL
@Description  :
"""
import os
import tornado.web
from werkzeug.security import generate_password_hash
from handler.handle_drive import *
from configure.parameter import AppSetting, MysqlParameter
from configure.status import APIStatus
from utils.decorator import logger


class ApiBase(tornado.web.RequestHandler):
    current_user = None

    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)
        self.args_ = {
            "count": int(self.get_query_argument("count", "0")),
            "start": int(self.get_query_argument("start", "0")),
            "item": self.get_query_argument("item", ""),
            "order_key": self.get_query_argument("order_key", "-create_time"),
        }
        self.request_info = {
            "ip": self.request.remote_ip,
            "method": self.request.method.lower(),
            "path": self.request.uri
        }
        self.handler = None
        if self.request.body:
            try:
                self.body_ = json.loads(self.request.body.decode("utf-8"))
            except (json.JSONDecodeError, UnicodeDecodeError) as err:
                print(err)
                self.body_ = self.request.body
        else:
            self.body_ = "{}"

    def data_received(self, chunk):
        pass

    def get_current_user(self):
        return self.current_user

    def on_finish(self):
        pass

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")  # 这个地方可以写域名
        self.set_header("Access-Control-Allow-Headers", "x-requested-with, content-type, authorization, Authorization")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS, PUT, DELETE')

    def options(self, *args, **kwargs):
        self.set_header('Content-Type', 'text/html')
        self.write("options")
        self.set_status(200)
        self.finish()

    def prepare(self):
        req_path = self.request.uri
        method = self.request.method
        if method == "OPTIONS" or method == "options":
            return
        if req_path.startswith("/api") and (req_path not in AppSetting.TOKEN_EXTERNAL):
            res = AppSetting.general_result()
            if AppSetting.AUTH_KEY not in self.request.headers:
                res["result"] = "fail"
                res["err_code"] = APIStatus.TOKEN_BROKEN
                res["message"] = "no token"
                self.write(json.dumps(res))
                self.finish()
                return
            token = self.request.headers[AppSetting.AUTH_KEY]
            try:
                user_payload = jwt.decode(token, AppSetting.TOKEN_SECRET, algorithm='HS256')
            except Exception as err:
                res["result"] = "fail"
                res["err_code"] = APIStatus.TOKEN_BROKEN
                res["message"] = str(err)
                self.write(json.dumps(res))
                self.finish()
                return
            self.current_user = user_payload
            self.request_info["username"] = self.current_user["username"]

    def get(self):
        res = self.handler.get(self.args_, self.current_user)
        self.write(json.dumps(res))
        self.finish()
        return

    def post(self):
        res = self.handler.post(self.body_, self.current_user)
        self.write(json.dumps(res))
        self.finish()
        return

    def put(self):
        res = self.handler.put(self.args_, self.body_, self.current_user)
        self.write(json.dumps(res))
        self.finish()
        return

    def delete(self):
        res = self.handler.delete(self.args_, self.current_user)
        self.write(json.dumps(res))
        self.finish()
        return


class ApiFileTransform(ApiBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.args_["filename"] = self.get_query_argument("filename", "download")

    def get(self):
        res = AppSetting.general_result()
        log_info = self.request_info
        if not self.args_["filename"]:
            res["err_code"] = APIStatus.FIELD_LACK
            res["message"] = "no such params: filename"
            res["result"] = "fail"
            log_info["message"] = res["message"]
            log_info["err_code"] = res["err_code"]
            self.write(json.dumps(res))
            self.finish()
            logger.error(json.dumps(log_info))
            return
        full_path = os.path.join(AppSetting.BASE_DIR, AppSetting.DOWN_FILE_DIR, self.args_["filename"])
        if not os.path.exists(full_path):
            res["err_code"] = APIStatus.FILE_IO_ERROR
            res["message"] = "file not exist: {filename}".format(filename=self.args_["filename"])
            res["result"] = "fail"
            log_info["message"] = res["message"]
            log_info["err_code"] = res["err_code"]
            self.write(json.dumps(res))
            self.finish()
            logger.error(json.dumps(log_info))
            return
        self.set_header('Content-Type', 'application/octet-stream')
        self.set_header('Content-Disposition', 'attachment; filename="{name}"'
                        .format(name=self.args_["filename"].encode("utf-8")))
        with open(full_path, 'rb') as f:
            while True:
                data = f.read(4096)
                if not data:
                    break
                self.write(data)
        self.finish()
        logger.info(json.dumps(log_info))
        return

    def post(self):
        res = AppSetting.general_result()
        res["cmd"] = "upload-file"
        log_info = self.request_info
        file_list = self.request.files.get('file', "")
        if not file_list:
            res["err_code"] = APIStatus.FIELD_LACK
            res["message"] = "no such params: file"
            res["result"] = "fail"
            log_info["message"] = res["message"]
            log_info["err_code"] = res["err_code"]
            self.write(json.dumps(res))
            self.finish()
            logger.error(json.dumps(log_info))
            return
        file_obj = self.request.files['file'][0]
        filename = file_obj['filename']
        upload_path = os.path.join(AppSetting.BASE_DIR, AppSetting.UP_FILE_DIR)
        try:
            with open(os.path.join(upload_path, filename), 'wb') as fh:
                fh.write(file_obj['body'])
            print("success")
            res["err_code"] = APIStatus.SUCCESS
            res["data"] = {
                "filename": filename
            }
        except IOError as e:
            res["err_code"] = APIStatus.FILE_IO_ERROR
            res["message"] = str(e)
            log_info["message"] = res["message"]
            log_info["err_code"] = res["err_code"]
            logger.error(json.dumps(log_info))
        else:
            logger.info(json.dumps(log_info))
        self.write(json.dumps(res))
        self.finish()

    def put(self):
        res = AppSetting.general_result()
        res["err_code"] = APIStatus.INTERFACE_DISABLED
        res["message"] = "this interface is disabled."
        res["result"] = "fail"
        self.write(json.dumps(res))
        self.finish()

    def delete(self):
        res = AppSetting.general_result()
        res["err_code"] = APIStatus.INTERFACE_DISABLED
        res["message"] = "this interface is disabled."
        res["result"] = "fail"
        self.write(json.dumps(res))
        self.finish()


class ApiDBInit(ApiBase):

    def post(self):
        """
        初始化数据库，创建一个用户和一个角色
        """
        init_user = {
            "roles": ["admin"],
            "username": "init_db",
            "token": ""
        }

        role_handler = HandlerRole(
            self.request_info,
            user=MysqlParameter.USER,
            password=MysqlParameter.PASSWORD,
            host=MysqlParameter.HOST,
            port=MysqlParameter.PORT,
            schema=MysqlParameter.DB_NAME,
        )
        role_handler.edit_roles = ["admin"]
        role_handler.view_roles = ["admin"]
        role_handler.fields_border = ["name", "code", "level"]
        role_body = {
          "name": "初始管理员",
          "code": "admin",
          "level": 0
        }
        res_role = role_handler.search({"code": role_body["code"]}, init_user)
        if res_role["err_code"] != APIStatus.SUCCESS:
            res = {"role": res_role, "user": None}
            self.write(json.dumps(res))
            self.finish()
            return
        if len(res_role["data"]) == 0:
            res_role = role_handler.post(role_body, init_user)
            role_uid = res_role["data"]["uid"]
        else:
            role_uid = res_role["data"][0]["uid"]

        if res_role["err_code"] != APIStatus.SUCCESS:
            res = {"role": res_role, "user": None}
            self.write(json.dumps(res))
            self.finish()
            return
        user_handler = HandlerUser(
            self.request_info,
            user=MysqlParameter.USER,
            password=MysqlParameter.PASSWORD,
            host=MysqlParameter.HOST,
            port=MysqlParameter.PORT,
            schema=MysqlParameter.DB_NAME,
        )
        user_handler.fields_border = ["username", "password", "name", "email",
                                      "phone", "role", "leader", "is_login", "is_valid"]
        user_handler.edit_roles = ["admin"]
        user_handler.view_roles = ["admin"]
        user_body = {
            "username": "admin",
            "password": "admin",
            "name": "初始管理员",
            "email": "admin@gitlab.cn",
            "phone": "15900000000",
            "role": role_uid,
            "is_login": False,
            "is_valid": True
        }

        res_user = user_handler.search({"username": user_body["username"]}, init_user)
        if res_user["err_code"] != APIStatus.SUCCESS:
            res = {"role": res_role, "user": res_user}
            self.write(json.dumps(res))
            self.finish()
            return
        if len(res_user["data"]) == 0:
            if "password" in user_body:
                user_body["password"] = generate_password_hash(user_body["password"])
            res_user = user_handler.post(user_body, init_user)
        res = {"role": res_role, "user": res_user}
        self.write(json.dumps(res))
        self.finish()
        return

    def get(self):
        res = AppSetting.general_result()
        res["err_code"] = APIStatus.INTERFACE_DISABLED
        res["message"] = "this api is not use"
        res["result"] = "fail"
        self.write(json.dumps(res))
        self.finish()

    def put(self):
        res = AppSetting.general_result()
        res["err_code"] = APIStatus.INTERFACE_DISABLED
        res["message"] = "this api is not use"
        res["result"] = "fail"
        self.write(json.dumps(res))
        self.finish()

    def delete(self):
        res = AppSetting.general_result()
        res["err_code"] = APIStatus.INTERFACE_DISABLED
        res["message"] = "this api is not use"
        res["result"] = "fail"
        self.write(json.dumps(res))
        self.finish()


class ApiHome(ApiBase):

    def get(self):
        res = AppSetting.general_result()
        res["err_code"] = APIStatus.SUCCESS
        res["message"] = ""
        res["result"] = "ok"
        res["data"] = "Deepcyto KaryoType Restful"
        self.write(json.dumps(res))
        self.finish()

    def post(self):
        res = AppSetting.general_result()
        res["err_code"] = APIStatus.INTERFACE_DISABLED
        res["message"] = "this api is not use"
        res["result"] = "fail"
        self.write(json.dumps(res))
        self.finish()

    def put(self):
        res = AppSetting.general_result()
        res["err_code"] = APIStatus.INTERFACE_DISABLED
        res["message"] = "this api is not use"
        res["result"] = "fail"
        self.write(json.dumps(res))
        self.finish()

    def delete(self):
        res = AppSetting.general_result()
        res["err_code"] = APIStatus.INTERFACE_DISABLED
        res["message"] = "this api is not use"
        res["result"] = "fail"
        self.write(json.dumps(res))
        self.finish()


class ApiLogin(ApiBase):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.handler = HandlerLogin(
            self.request_info,
            user=MysqlParameter.USER,
            password=MysqlParameter.PASSWORD,
            host=MysqlParameter.HOST,
            port=MysqlParameter.PORT,
            schema=MysqlParameter.DB_NAME,
        )

    def get(self):
        res = self.handler.get(self.args_, self.request.headers)
        self.write(json.dumps(res))
        self.finish()

    def post(self):
        res = AppSetting.general_result()
        res["err_code"] = APIStatus.INTERFACE_DISABLED
        res["message"] = "this api is not use"
        res["result"] = "fail"
        self.write(json.dumps(res))
        self.finish()

    def put(self):
        """
        登录
        :return:
        """
        res = self.handler.put(self.args_, self.body_)
        self.write(json.dumps(res))
        self.finish()

    def delete(self):
        """
        登出
        :return:
        """
        res = self.handler.delete(self.request.headers)
        self.write(json.dumps(res))
        self.finish()


if __name__ == '__main__':
    print("api_base start")
