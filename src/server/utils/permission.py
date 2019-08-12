# coding: utf-8

"""
@Python         : 3.6.7
@Author         : XuXuepeng-Paul
@Email            : xuepeng_paul_1986@126.com
@Time             : 2019-05-18:15
@File               : permission.py
@Project         : general-server
@Licence         : LGPL
@Description  :
"""


class Permission(object):

    @staticmethod
    def check_user_role(cls_roles, user_roles):
        """
        验证用户角色是否有进入某个接口的权限
        :param cls_roles: list 接口定义权限
        :param user_roles: list 用户的权限
        :return: bool
        """
        for role in user_roles:
            if role in cls_roles:
                return True
        else:
            return False

    @staticmethod
    def decorator_check_user_role(cls_roles, user_roles):
        def wrapper_(func):
            def wrapper(*args, **kwargs):
                for role in user_roles:
                    if role in cls_roles:
                        return func(*args, **kwargs)
                else:
                    res = {
                        "err_code": 2009,
                        "result": "fail",
                        "message": "user role is forbidden"
                    }
                    return res
            return wrapper
        return wrapper_


if __name__ == '__main__':
    print("permission start")
