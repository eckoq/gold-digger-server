#
# Copyright (C) Gold-Digger, Inc.
#

#!/usr/bin/env python
#-*- coding: utf-8 -*-


class Err:
    def __init__(self, code, message):
        self.code = code
        self.message = message


ERR_OK = Err(0, '')
ERR_BASE = Err(-10000, 'error')
ERR_PARAMS_ERROR = Err(-10001, 'params error')
ERR_DATABASE_ERROR = Err(-10002, 'handle database error')
ERR_CELERY_ERROR = Err(-10003, 'submit celery async task failed')
ERR_CALL_API_TIMEOUT = Err(-11000, 'call api timeout')
ERR_API_CONNECTION_REFUSED = Err(-11001, 'Third-party api server connection refused')
ERR_API_RETURN_INVALID = Err(-11002, 'Third-party api server return invalid')
ERR_LOGIN = Err(-12000, 'login failed')
