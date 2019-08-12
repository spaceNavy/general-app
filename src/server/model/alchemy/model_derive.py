# coding: utf-8
"""
@Python         : 3.6.7
@Author         : XuXuepeng-Paul
@Email            : xuepeng_paul_1986@126.com
@Time             : 2019-05-18:15
@File               : model_derive.py
@Project         : general-server
@Licence         : LGPL
@Description  :
"""
from sqlalchemy import Column, ForeignKey, String, TIMESTAMP, text
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.orm import relationship
from .model_base import ModelBase


class Role(ModelBase):
    __tablename__ = 'roles'
    table_name = __tablename__
    key_word = "code"
    unique_list = ["name"]

    name = Column(String(45), nullable=False)
    code = Column(String(32), nullable=False, unique=True)
    level = Column(INTEGER(11), nullable=False, server_default=text("'100'"))


class User(ModelBase):
    __tablename__ = 'users'
    table_name = __tablename__
    key_word = "username"
    unique_list = ["email", "phone"]

    last_time = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))
    username = Column(String(32), nullable=False, unique=True)
    password = Column(String(128))
    email = Column(String(64), nullable=False, unique=True)
    phone = Column(String(16), nullable=False, unique=True)
    name = Column(String(45))
    company = Column(String(64), index=True)
    role = Column(ForeignKey('roles.id'), nullable=False, index=True)
    is_valid = Column(TINYINT(4), nullable=False, server_default=text("'0'"))
    is_login = Column(TINYINT(4), nullable=False, server_default=text("'0'"))

    role_ref = relationship('Role')


class Company(ModelBase):
    __tablename__ = 'companies'
    table_name = __tablename__
    key_word = "name"

    name = Column(String(64), nullable=False, unique=True)
    leader = Column(ForeignKey('users.id'), nullable=False, index=True)
    comment = Column(String(64))
    seller = Column(ForeignKey('users.id'), nullable=False, index=True)
    password = Column(String(64))

    leader_ref = relationship('User', primaryjoin='Company.leader == User.uid')
    seller_ref = relationship('User', primaryjoin='Company.seller == User.uid', backref="company_seller")

