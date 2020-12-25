#
# Copyright (c) Gold-Digger, Inc.
#

#!/usr/bin/python
#-*- coding: utf-8 -*-

import json, datetime
from flask import Blueprint, request, current_app, session
from flask_restx import Resource
from flask_login import login_user, login_required, logout_user, current_user
from itsdangerous import URLSafeSerializer
from sqlalchemy.exc import SQLAlchemyError
from app import login_manager
from app.common.db import db
from app.common.utils import logger_util
from app.common.utils.fix_swagger_api import CustomApi
from app.common.utils.http_util import HttpResponse
from app.common.error import ERR_OK, ERR_LOGIN, ERR_PARAMS_ERROR
from app.gold_digger.models import GDUser

# create Blueprint
user_bp = Blueprint("user", __name__)

# create log
logger = logger_util.Logger("dashboard").logger

# customApi
api = CustomApi(user_bp, title='User API', description='handle user request', prefix="/")

@login_manager.user_loader
def load_user(token):
  try:
    key = current_app.secret_key
    s = URLSafeSerializer(key)
    id = s.loads(token)['id']
    logger.debug('load user id {} token {}'.format(id, token))
    user = GDUser.query.get(id)
    if user:
      return user
    return None
  except BadData:
    logger.debug('load user faild token {}'.format(token))
    return None

@api.route('/login', doc={"description": "login"})
class login(Resource):
  def post(self):
    try:
      user_name = request.get_json()['username']
      password = request.get_json()['password']
      logger.debug("user {} password {}".format(user_name, password))
      user = GDUser.query.filter_by(user_name=user_name, password=password).first()
      if not user:
        result = {'message':'user_name or password not allow'}
        return HttpResponse.normal(ERR_LOGIN.code, ERR_LOGIN.message, result)
      else:
        session.permanent = True
        current_app.permanent_session_lifetime = datetime.timedelta(minutes=10)
        login_status = login_user(user)
        token = user.get_id()
        result = {'token':token}
        logger.debug("user {} token {} status {} curuser {}".format(user_name, token, login_status, current_user));
        return HttpResponse.normal(ERR_OK.code, ERR_OK.message, result)

    except Exception as e:
      return HttpResponse.normal(ERR_LOGIN.code, ERR_LOGIN.message, {'message': str(e)})

@api.route('/info', doc={"description": "info"})
class UserInfo(Resource):
  decorators = [login_required]
  def get(self):
    try:
      token = request.args.get("token")

      key = current_app.secret_key
      s = URLSafeSerializer(key)
      id = s.loads(token)['id']

      logger.debug("curuser {}".format(current_user));
      user = GDUser.query.get(id)
      if user:
        return HttpResponse.normal(ERR_OK.code, ERR_OK.message, {'name': user.user_name, "avatar":""})
      return HttpResponse.normal(ERR_LOGIN.code, ERR_LOGIN.message, {'message': "No user"})
    except Exception as e:
      return HttpResponse.normal(ERR_LOGIN.code, ERR_LOGIN.message, {'message': str(e)})

@api.route('/logout', doc={"description": "logout"})
class logout(Resource):
  decorators = [login_required]
  def get(self):
    try:
      if logout_user():
        return HttpResponse.normal(ERR_OK.code, ERR_OK.message, {'name': user.user_name, "avatar":""})
      return HttpResponse.normal(ERR_LOGIN.code, ERR_LOGIN.message, {'message': "No user"})
    except Exception as e:
      return HttpResponse.normal(ERR_LOGIN.code, ERR_LOGIN.message, {'message': str(e)})

  def post(self):
    try:
      if logout_user():
        return HttpResponse.normal(ERR_OK.code, ERR_OK.message, {'message': "logout success"})
      return HttpResponse.normal(ERR_LOGIN.code, ERR_LOGIN.message, {'message': "logout failed"})
    except Exception as e:
      return HttpResponse.normal(ERR_LOGIN.code, ERR_LOGIN.message, {'message': str(e)})
