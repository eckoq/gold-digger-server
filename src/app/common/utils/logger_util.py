#
# Copyright (C) Gold-Digger, Inc.
#

#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import json
import logging
import logging.config
from app.config import APP_ROOT

LOGGER_CONF_PATH = os.path.join(APP_ROOT, '../conf/logger.json')


class Logger:
    '''
    Logger工具类
    Args:
        name: 创建logger的名字，要对应json配置文件中的loggers配置
    '''
    def __init__(self, name):
        if os.path.exists(LOGGER_CONF_PATH):
            with open(LOGGER_CONF_PATH, "r") as f:
                config = json.load(f)
                logging.config.dictConfig(config)
        else:
            logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(name)

    # 以下方法调用的时候无法正确获取调用文件和行数，只能获取logger_util的行数
    def error(self, message):
        self.logger.error(message)

    def info(self, message):
        self.logger.info(message)

    def debug(self, message):
        self.logger.debug(message)
