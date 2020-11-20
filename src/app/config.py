# -*- coding: utf-8 -*-

import os
from app.common.utils.config_parser import ConfigUtil

basedir = os.path.dirname(os.path.abspath(__file__))
APP_ROOT = basedir
CONF_PATH = os.path.join(APP_ROOT, '../', 'conf')


class BaseConfig:
    # 主库
    MYSQL_ALL_CONF = ConfigUtil.get_all_mysql_conf(CONF_PATH + '/db.ini')
    # 多库绑定
    SQLALCHEMY_BINDS = MYSQL_ALL_CONF
    # 自动回收连接
    SQLALCHEMY_POOL_RECYCLE = 600
    # 连接池大小
    SQLALCHEMY_POOL_SIZE = 10
    # 连接池超时时间
    SQLALCHEMY_POOL_TIMEOUT = 30
    # 数据库连接最大超出个数
    SQLALCHEMY_MAX_OVERFLOW = 5
    # 是否追踪对象修改
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @classmethod
    def get_config(cls, conf_file):
        config_util = ConfigUtil(CONF_PATH + "/" + conf_file)
        # api
        cls.EXAMPLE_API_URL = config_util.get_items("server", "api_url")
        cls.EXAMPLE_ACCOUNT_API_URL = config_util.get_items("server", "account_api_url")

#
# desc: now we do not use dev env, so db params is the same as production.
#
class DevelopmentConfig(BaseConfig):
    DEBUG = True
    MYSQL_ALL_CONF = ConfigUtil.get_all_mysql_conf(CONF_PATH + '/db.ini')
    SQLALCHEMY_DATABASE_URI = MYSQL_ALL_CONF['db']
    SQLALCHEMY_ECHO = True

    def __init__(self):
        super().get_config('dev.ini')

#
# desc: now we do not use testing env, so db params is the same as production.
#
class TestingConfig(BaseConfig):
    TESTING = True
    MYSQL_ALL_CONF = ConfigUtil.get_all_mysql_conf(CONF_PATH + '/db.ini')
    SQLALCHEMY_DATABASE_URI = MYSQL_ALL_CONF['db']
    SQLALCHEMY_ECHO = True

    def __init__(self):
        super().get_config('test.ini')


class ProductionConfig(BaseConfig):
    DEBUG = False
    MYSQL_ALL_CONF = ConfigUtil.get_all_mysql_conf(CONF_PATH + '/db.ini')
    SQLALCHEMY_DATABASE_URI = MYSQL_ALL_CONF['db']

    def __init__(self):
        super().get_config('pro.ini')


config = {
    'development': DevelopmentConfig(),
    'testing': TestingConfig(),
    'production': ProductionConfig()
}
