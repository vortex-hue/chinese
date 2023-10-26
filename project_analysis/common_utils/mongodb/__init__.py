# -*- coding: UTF-8 -*-
import os, base64
from pymongo import MongoClient


class MongoCLS(object):

    MONGODB_CONF_VARS = (
        "MONGODB_DB",
        "MONGODB_URI",
        "MONGODB_HOST",
        "MONGODB_PORT",
        "MONGODB_USERNAME",
        "MONGODB_PASSWORD",
        "MONGODB_CONNECT",
    )

    @classmethod
    def create_key(cls, length):
        random_str = os.urandom(length)
        byte_ret = base64.b64encode(random_str)
        result = byte_ret.decode('unicode_escape')
        return result

    @classmethod
    def connect_func(cls, config):
        connect = MongoClient(
            host=config.MONGODB_HOST,
            port=config.MONGODB_PORT
            # connect=True, retryWrites=True,
            # authSource=config.MONGODB_USERNAME,
            # username=config.MONGODB_USERNAME,
            # password=config.MONGODB_PASSWORD,
        )
        database = getattr(connect, config.MONGODB_DB)
        return database

    def init_app(self, project_config):
        try:
            self.database = self.connect_func(project_config)
        except Exception as e:
            raise SystemExit('MondoDB数据库链接失败: %s'%str(e))
        setattr(self, 'project_name', project_config.PROJECT_NAME)

