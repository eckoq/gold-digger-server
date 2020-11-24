#
# Copyright (C) Gold-Digger, Inc.
#

#!/usr/bin/env python
#-*- coding: utf-8 -*-

import flask_login
import time
from flask import current_app
from itsdangerous import URLSafeSerializer
from app.common.db import db

class GDUser(db.Model, flask_login.UserMixin):
  __tablename__ = 'gd_user_t'
  id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
  user_name = db.Column(db.String(64), unique=True, nullable=False)
  password = db.Column(db.String(64))
  email = db.Column(db.String(64))
  status = db.Column(db.SmallInteger, nullable=False,
                     default=1, doc="用户状态，0-禁用，1-启动")
  create_datetime = db.Column(db.DateTime,
                              server_default=db.text("CURRENT_TIMESTAMP"), doc="创建时间")
  update_datetime = db.Column(db.DateTime, nullable=False,
                              server_default=db.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
                              doc="更新时间")

  def is_active(self):
    if self.status:
      return True
    return False

  #
  # create token with user id
  #
  def get_id(self):
    key = current_app.secret_key
    s = URLSafeSerializer(key)
    data = {
        'id':self.id,
        'time': time.time()
      }
    token = s.dumps(data)
    return token
