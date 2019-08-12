# coding: utf-8

"""
@Python         : 3.6.7
@Author         : XuXuepeng-Paul
@Email            : xuepeng_paul_1986@126.com
@Time             : 2019-05-18:15
@File               : model_base.py
@Project         : general-server
@Licence         : LGPL
@Description  :
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import TIMESTAMP
from sqlalchemy import text
import uuid

Base = declarative_base()


class ModelBase(Base):
    __abstract__ = True
    __tablename__ = "base"
    uid = Column("id", String(64), primary_key=True, unique=True)
    deleted = Column(String(64))
    create_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    __table_args__ = {
        "mysql_charset": "utf8"
    }

    table_name = __tablename__
    key_word = ""
    unique_list = []

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.uid = str(uuid.uuid4()).replace("-", "")


if __name__ == '__main__':
    print("model_base start")
