#
# Copyright (c) Gold-Digger, Inc.
#

#!/usr/bin/python
#-*- coding: utf-8 -*-


from flask import Blueprint
from flask_restx import Resource
from sqlalchemy.exc import SQLAlchemyError
from app.common.db import db
from app.common.utils import logger_util
from app.common.utils.fix_swagger_api import CustomApi
from app.common.utils.http_util import HttpResponse
from app.common.error import ERR_OK, ERR_DATABASE_ERROR, ERR_PARAMS_ERROR, ERR_API_RETURN_INVALID, ERR_CELERY_ERROR

# create Blueprint
dashboard_bp = Blueprint("dashboard", __name__)

# create log
logger = logger_util.Logger("dashboard").logger

# customApi
api = CustomApi(dashboard_bp, title='dashboard API', description='handle dashboard request', prefix="/")

@api.route('/hello', doc={"description": "Test"})
class Hello(Resource):
  def post(self):
    logger.debug("hello world");
    try:
      data = {"value": "hello world"}
      return HttpResponse.normal(ERR_OK.code, ERR_OK.message, data)
    except Exception as e:
      return HttpResponse.normal(ERR_DATABASE_ERROR.code, ERR_DATABASE_ERROR.message, {'message': str(e)})
