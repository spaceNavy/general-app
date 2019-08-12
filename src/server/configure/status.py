# coding: utf-8

"""
@Python         : 3.6.7
@Author         : XuXuepeng-Paul
@Email            : xuepeng_paul_1986@126.com
@Time             : 2019-05-18:15
@File               : status.py
@Project         : general-server
@Licence         : LGPL
@Description  :
"""


class APIStatus(object):
    UNDEFINED = 0
    SUCCESS = 2000
    DB_ERROR = 2001
    USER_ERROR = 2002
    PASS_WORD_ERROR = 2003
    TOKEN_BROKEN = 2004
    TOKEN_EXPIRED = 2005
    NOT_YET_LOGIN = 2006
    OTHER_USER_LOGIN = 2007
    FIELD_LACK = 2008
    ROLE_FORBIDDEN = 2009
    ALREADY_EXIST = 2010
    FILE_IO_ERROR = 2011
    FILE_FORMAT_ERROR = 2012
    ITEM_LIST_EMPTY = 2013
    FIELD_OUTER = 2014
    INTERFACE_DISABLED = 2015


if __name__ == '__main__':
    print("status start")
