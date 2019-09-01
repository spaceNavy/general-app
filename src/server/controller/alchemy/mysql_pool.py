# coding: utf-8

"""
@Python         : 3.6.7
@Author         : XuXuepeng-Paul
@Email            : xuepeng_paul_1986@126.com
@Time             : 2019-05-18:15
@File               : mysql_pool.py
@Project         : general-server
@Licence         : LGPL
@Description  :
"""
from sqlalchemy import create_engine
from configure.parameter import MysqlParameter
g_alchemy_pool = None


def alchemy_pool_create(change=False, **kwargs):
    global g_alchemy_pool
    db_uri_format = "mysql+mysqlconnector://{user}:{password}@{host}:{port}/{schema}?charset={encode}"
    db_uri = db_uri_format.format(
        user=kwargs.get("user", MysqlParameter.USER),
        password=kwargs.get("password", MysqlParameter.PASSWORD),
        host=kwargs.get("host", MysqlParameter.HOST),
        port=kwargs.get("port", MysqlParameter.PORT),
        schema=kwargs.get("schema", MysqlParameter.DB_NAME),
        encode=kwargs.get("encode", "utf8mb4")
    )
    if change:
        alchemy_pool_close()
        g_alchemy_pool = create_engine(db_uri)
        return g_alchemy_pool
    if not g_alchemy_pool:
        g_alchemy_pool = create_engine(db_uri)
    return g_alchemy_pool


def alchemy_pool_close():
    global g_alchemy_pool
    if g_alchemy_pool:
        g_alchemy_pool.dispose()


if __name__ == '__main__':
    print("make_alchemy_connect start")
