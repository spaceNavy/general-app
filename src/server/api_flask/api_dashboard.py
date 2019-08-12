# coding: utf-8

"""
@Python         : 3.6.7
@Author         : XuXuepeng-Paul
@Email            : xuepeng_paul_1986@126.com
@Time             : 2019-05-18:15
@File               : flask/api_dashboard.py
@Project         : general-server
@Licence         : LGPL
@Description  :
"""

from flask import Blueprint
from flask_restplus import Api
from .space_admin import api as space_admin
from .space_support import api as space_support
from .space_company import api as space_company


blueprint = Blueprint('api-dashboard', __name__)
api = Api(blueprint, version='1.0', title='Dashboard API',
          description='A AI Platform Dashboard', )

api.add_namespace(space_admin)
api.add_namespace(space_support)
api.add_namespace(space_company)


if __name__ == '__main__':
    print("api_v1 start")
