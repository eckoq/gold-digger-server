#
# Copyright (C) Gold-Digger, Inc.
#

#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import flask_login

from flask import Flask, g
from flask_cors import CORS

from app.common.db import db
from app.config import config
from app.common.utils.json_date_encoder import CJsonEncoder

app_name = 'gold-digger'
app_secret_key = 'a86155229efe1148bae0bc03607591b7'
login_manager = flask_login.LoginManager()

#
# import all views
#
from app.gold_digger import views

#
# import all models
#
from app.gold_digger import models

def create_app(config_name=None):
  app = Flask(app_name)
  app.secret_key = app_secret_key
  CORS(app, supports_credentials=True)
  app.config.from_object(config[config_name])
  app.config["RESTX_JSON"] = {'cls': CJsonEncoder}
  register_sqlalchemy(app)
  register_blueprints(app)
  init_login_manager(app)
  return app

def register_blueprints(app):
  app.register_blueprint(views.dashboard_bp, url_prefix='/gold-digger/dashboard')
  app.register_blueprint(views.user_bp, url_prefix='/gold-digger/user')

def register_sqlalchemy(app):
  db.init_app(app)
  with app.app_context():
    db.create_all()

def init_login_manager(app):
  login_manager.init_app(app)
