# coding: utf-8

"""
@Python         : 3.6.7
@Author         : XuXuepeng-Paul
@Email            : xuepeng_paul_1986@126.com
@Time             : 2019-05-18:15
@File               : decorator.py
@Project         : general-server
@Licence         : LGPL
@Description  :
"""
import json
import sys
from functools import wraps
import logging
import os
from logging.handlers import TimedRotatingFileHandler


class ContextFilter(logging.Filter):

    def __init__(self, name):
        super().__init__(name)

    def filter(self, record):
        print(record.role)
        if record.role == self.name:
            return True
        else:
            return False


class Logger(object):

    def __init__(self):
        self.base_dir = os.path.join(os.path.dirname(os.path.abspath(os.path.dirname(__file__))), "logs")
        if not os.path.exists(self.base_dir):  # 创建路径
            os.makedirs(self.base_dir)
        for root, dirs, files in os.walk(os.path.dirname(self.base_dir)):  # 删除空文件
            for i in files:
                file_path = os.path.join(root, i)
                if os.path.getsize(file_path) == 0:
                    os.remove(file_path)
        formatter = logging.Formatter("%(asctime)s-%(levelname)s:::: %(message)s")

        info_record = TimedRotatingFileHandler(
            os.path.join(self.base_dir, "server-info.log"),
            when="D",
            encoding="utf-8")
        info_record.setLevel(logging.INFO)
        info_record.setFormatter(formatter)

        error_record = TimedRotatingFileHandler(
            os.path.join(self.base_dir, "server-error.log"),
            when="D",
            encoding="utf-8")
        error_record.setLevel(logging.ERROR)
        error_record.setFormatter(formatter)

        self.logger_info = logging.getLogger("info")
        self.logger_info.setLevel(logging.INFO)
        self.logger_info.addHandler(info_record)

        self.logger_error = logging.getLogger("error")
        self.logger_error.setLevel(logging.ERROR)
        self.logger_error.addHandler(error_record)

        sh = logging.StreamHandler(sys.stdout)
        sh_filter = ContextFilter("console")
        self.logger_sh = logging.getLogger("console")
        self.logger_sh.setLevel(logging.DEBUG)
        self.logger_sh.addHandler(sh)
        self.logger_sh.addFilter(sh_filter)

    def info(self, message):
        self.logger_info.info(message)

    def warning(self, message):
        self.logger_info.warning(message)

    def error(self, message):
        self.logger_error.error(message)


logger = Logger()


# def decor_logger(params):
def decor_logger(func):
    @wraps(func)
    def wrapper(*args, **kw):
        res = func(*args, **kw)
        log_info = res.get("request_info", {})
        if res["err_code"] == 2000:
            if log_info["method"] == "delete":
                log_info["data"] = res["data"]
                logger.warning(json.dumps(log_info))
            else:
                logger.info(json.dumps(log_info))
        else:
            log_info["message"] = res["message"]
            log_info["err_code"] = res["err_code"]
            logger.error(json.dumps(log_info))
        if "request_info" in res:
            res.pop("request_info")
        return res
    return wrapper
    # return decorator


if __name__ == '__main__':
    print("decorator start")
