# coding: utf-8

"""
@Python         : 3.6.7
@Author         : XuXuepeng-Paul
@Email            : xuepeng_paul_1986@126.com
@Time             : 2019-05-18:15
@File               : model_2_json.py
@Project         : general-server
@Licence         : LGPL
@Description  :
"""
import datetime
import decimal
import json
from sqlalchemy.ext.declarative import DeclarativeMeta


class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                if field in ["table_name", "unique_list", "key_word", "deleted"]:
                    continue
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data)
                    fields[field] = data
                except TypeError:
                    if isinstance(data, datetime.datetime):
                        fields[field] = data.strftime("%Y-%m-%d %H:%M:%S")
                    elif isinstance(data, datetime.date):
                        fields[field] = data.strftime("%Y-%m-%d")
                    elif isinstance(data, decimal.Decimal):
                        fields[field] = float(data)
                    elif isinstance(data.__class__, DeclarativeMeta):
                        fields[field] = AlchemyEncoder.default(self, data)
                    else:
                        fields[field] = None
            return fields

        return json.JSONEncoder.default(self, obj)


if __name__ == '__main__':
    print("alchemy_translate start")
