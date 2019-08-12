# coding: utf-8

"""
@Python         : 3.6.7
@Author         : XuXuepeng-Paul
@Email            : xuepeng_paul_1986@126.com
@Time             : 2019-05-18:15
@File               : control_derive.py
@Project         : general-server
@Licence         : LGPL
@Description  :
"""
from sqlalchemy import desc
from sqlalchemy import or_
from .controller_base import ControllerBase
from model.alchemy.model_derive import *


class ControllerUser(ControllerBase):

    def __init__(self, **kwargs):
        super().__init__(User, **kwargs)
        self.support_model = Company

    def search(self, **kwargs):
        with self.session_scope() as session:
            comments = session.query(self._model_meta, self.support_model).outerjoin(
                self.support_model,
                self._model_meta.company == self.support_model.uid).outerjoin(
            ).filter(
                or_(self._model_meta.deleted.is_(None), self._model_meta.deleted == ""),
                self._model_meta.username == kwargs["username"]).first()
            if comments:
                item_list = self.to_json_list(comments)
                result = item_list[0]
                result[self.support_model.table_name + "_ref"] = item_list[1]
            else:
                result = {}
        return result

    def search_by_id(self, **kwargs):
        with self.session_scope() as session:
            comments = session.query(self._model_meta, self.support_model).outerjoin(
                self.support_model,
                self._model_meta.company == self.support_model.uid).outerjoin(
            ).filter(
                or_(self._model_meta.deleted.is_(None), self._model_meta.deleted == ""),
                self._model_meta.username == kwargs["uid"]).first()
            if comments:
                item_list = self.to_json_list(comments)
                result = item_list[0]
                result[self.support_model.table_name + "_ref"] = item_list[1]
            else:
                result = {}
        return result

    def all(self, start=0, count=0, order_key="-create_time"):
        if order_key.startswith("-"):
            pre = "-"
            order_key = order_key[1:]
        else:
            pre = ""
        with self.session_scope() as session:
            query = session.query(self._model_meta, self.support_model).outerjoin(
                    self.support_model,
                    self._model_meta.company == self.support_model.uid).outerjoin(
                ).filter(
                    or_(self._model_meta.deleted.is_(None), self._model_meta.deleted == "")
                ).order_by(
                    text(pre + self._model_meta.table_name + "." + order_key))
            if count == 0:
                comments = query.all()
            else:
                comments = query.offset(start).limit(count).all()
            item_list = self.to_json_list(comments)
            result = []
            for item in item_list:
                temp = item[0]
                temp[self.support_model.table_name + "_ref"] = item[1]
                result.append(temp)
        return result


class ControllerRole(ControllerBase):

    def __init__(self, **kwargs):
        super().__init__(Role, **kwargs)

    def search(self, **kwargs):
        with self.session_scope() as session:
            comments = session.query(self._model_meta).filter(
                or_(self._model_meta.deleted.is_(None), self._model_meta.deleted == ""),
                self._model_meta.code == kwargs["code"]
            ).all()
            result = self.to_json_list(comments)
        return result


class ControllerCompany(ControllerBase):

    def __init__(self, **kwargs):
        super().__init__(Company, **kwargs)

    def search(self, **kwargs):
        pass


if __name__ == '__main__':
    print("controller_child start")
