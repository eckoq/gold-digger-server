#
# Copyright (C) Gold-Digger, Inc.
#

#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os

from flask import Flask, g
from flask_cors import CORS

from app.common.db import db
from app.config import config
from app.common.utils.json_date_encoder import CJsonEncoder
from app.server.views import dashboard_bp

app_name = 'gold-digger'

def create_app(config_name=None):
  app = Flask(app_name)
  CORS(app, supports_credentials=True)
  app.config.from_object(config[config_name])
  app.config["RESTX_JSON"] = {'cls': CJsonEncoder}
  register_sqlalchemy(app)
  register_blueprints(app)
  return app


def register_blueprints(app):
  app.register_blueprint(dashboard_bp, url_prefix='/dashboard')


def register_sqlalchemy(app):
  db.init_app(app)
