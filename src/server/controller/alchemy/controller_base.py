# coding: utf-8

"""
@Python         : 3.6.7
@Author         : XuXuepeng-Paul
@Email            : xuepeng_paul_1986@126.com
@Time             : 2019-05-18:15
@File               : controller_base.py
@Project         : general-server
@Licence         : LGPL
@Description  :
"""
import json
import abc
import uuid
from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy import or_, text
from .mysql_pool import alchemy_pool_create
from .model_2_json import AlchemyEncoder


class ControllerBase(object):

    def __init__(self, model_meta, **kwargs):
        self._db_conn = None
        self._model_meta = model_meta
        self._session = sessionmaker()
        self._db_conn = alchemy_pool_create(False, **kwargs)
        if self._db_conn:
            self._session.configure(bind=self._db_conn)

    @contextmanager
    def session_scope(self):
        """Provide a transactional scope around a series of operations."""
        session = scoped_session(self._session)()
        try:
            yield session
            session.commit()
        except Exception as err:
            session.rollback()
            raise err
        finally:
            session.close()

    @staticmethod
    def to_json_dict(model_query):
        return json.loads(json.dumps(model_query, cls=AlchemyEncoder))

    @staticmethod
    def to_json_list(query_iterable):
        return [json.loads(json.dumps(model_query, cls=AlchemyEncoder)) for model_query in query_iterable]

    def get_model(self):
        return self._model_meta

    def create(self, **kwargs):
        model_create = self._model_meta(**kwargs)
        uid = model_create.uid
        with self.session_scope() as session:
            session.add(model_create)
            session.commit()
        return uid

    def delete(self, uid):
        with self.session_scope() as session:
            session.query(self._model_meta).filter(
                self._model_meta.uid == uid
            ).update(values={"deleted": str(uuid.uuid4())})
            session.commit()

    def delete_on_disk(self, uid):
        with self.session_scope() as session:
            session.query(self._model_meta).filter(
                self._model_meta.uid == uid
            ).delete()
            session.commit()

    def update(self, uid, **kwargs):
        with self.session_scope() as session:
            session.query(self._model_meta).filter(
                self._model_meta.uid == uid
            ).update(values={**kwargs})
            session.commit()

    @abc.abstractmethod
    def search(self, **kwargs):
        pass

    def search_keyword_on_create(self, **kwargs):
        with self.session_scope() as session:
            filters = {self._model_meta.key_word: kwargs["key_word"]}
            comments = session.query(self._model_meta).filter_by(
                **filters
            ).first()
            result = self.to_json_dict(comments)
        return result

    def search_uk_on_create(self, key, value):
        with self.session_scope() as session:
            filters = {key: value}
            comments = session.query(self._model_meta).filter_by(
                **filters
            ).first()
            result = self.to_json_dict(comments)
        return result

    def all(self, start=0, count=0, order_key="-create_time"):
        if order_key.startswith("-"):
            pre = "-"
            order_key = order_key[1:]
        else:
            pre = ""
        with self.session_scope() as session:
            query = session.query(self._model_meta).filter(
                    or_(self._model_meta.deleted.is_(None), self._model_meta.deleted == "")
                ).order_by(
                    text(pre + self._model_meta.table_name + "." + order_key))
            if count == 0:
                comments = query.all()
            else:
                comments = query.offset(start).limit(count).all()
            result = self.to_json_list(comments)
        return result

    def count(self):
        with self.session_scope() as session:
            comments = session.query(self._model_meta).filter(
                or_(self._model_meta.deleted.is_(None), self._model_meta.deleted == "")
            ).count()
        return comments


if __name__ == '__main__':
    print("controller_base start")
