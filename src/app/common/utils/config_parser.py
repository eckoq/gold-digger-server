#
# Copyright (C) Gold-Digger, Inc.
#

#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import configparser


class ConfigUtil(object):
    '''
    配置文件操作
    '''
    def __init__(self, file_name="../../conf/db.ini"):
        file_path = os.path.join(os.path.dirname(__file__), file_name)
        self.conf = configparser.ConfigParser()
        self.conf.read(file_path)

    # 获取配置模块头信息
    def get_sections(self):
        return self.conf.sections()

    # 获取具体配置模块里面的子项信息 key
    def get_options(self, section):
        return self.conf.options(section)

    # 获取具体配置模块的全量配置信息
    def get_contents(self, section):
        result = {}
        for option in self.get_options(section):
            value = self.conf.get(section, option)
            result[option] = int(value) if value.isdigit() else value
        return (result)

    # 获取具体配置模块里面的key 对应Value值
    def get_items(self, section, option):
        value = self.conf.get(section, option)
        result = int(value) if value.isdigit() else value
        return (result)

    # 获取db信息静态方法
    @staticmethod
    def get_all_mysql_conf(config_path):
        cf = configparser.ConfigParser()
        cf.read(config_path)

        all_mysql_uri = dict()
        for section in cf.sections():
            db_host = cf.get(section, 'db_host')
            db_port = cf.getint(section, 'db_port')
            db_user = cf.get(section, 'db_user')
            db_pass = cf.get(section, 'db_pass')
            db_db_name = cf.get(section, 'db_db_name')
            db_charsets = cf.get(section, 'db_charsets')

            mysql_uri = 'mysql+pymysql://%s:%s@%s:%s/%s?charset=%s' % (db_user, db_pass, db_host, db_port, db_db_name,
                                                                       db_charsets)
            all_mysql_uri[section] = mysql_uri

        return all_mysql_uri
