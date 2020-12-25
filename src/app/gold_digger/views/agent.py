#
# Copyright (c) Gold-Digger, Inc.
#

#!/usr/bin/python
#-*- coding: utf-8 -*-


from flask import Blueprint, request
from flask_restx import Resource
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from app.common.db import db
from app.common.utils import logger_util
from app.common.utils.fix_swagger_api import CustomApi
from app.common.utils.http_util import HttpResponse
from app.common.error import ERR_OK, ERR_DATABASE_ERROR, ERR_PARAMS_ERROR, ERR_API_RETURN_INVALID, ERR_CELERY_ERROR

from app.gold_digger.models import GDConfig
from app.gold_digger.models import GDDevice
from app.gold_digger.models import GDNetflow

# create Blueprint
agent_bp = Blueprint("agent", __name__)

# create log
logger = logger_util.Logger("dashboard").logger

# customApi
api = CustomApi(agent_bp, title='agent API', description='handle agent request', prefix="/")

@api.route('/load_config', doc={"description": "load config"})
class LoadConfig(Resource):
  def post(self):
    try:
      uuid = request.get_json()['uuid']
      logger.debug("load config uuid {}".format(uuid))
      if not uuid:
        return HttpResponse.normal(ERR_OK.code, ERR_OK.message, {"message": "Pls use param uuid"})

      data = []
      configs = GDConfig.query.filter_by(device_uuid=uuid).all()
      for config in configs:
        data.append(config.to_json())
      return HttpResponse.normal(ERR_OK.code, ERR_OK.message, {"configs": data})
    except Exception as e:
      return HttpResponse.normal(ERR_DATABASE_ERROR.code, ERR_DATABASE_ERROR.message, {'message': str(e)})
  def get(self):
    try:
      uuid = request.args.get("uuid")
      logger.debug("load config uuid {}".format(uuid));
      if not uuid:
        return HttpResponse.normal(ERR_OK.code, ERR_OK.message, {"message": "Pls use param uuid"})

      data = []
      configs = GDConfig.query.filter_by(device_uuid=uuid).all()
      for config in configs:
        data.append(config.to_json())
      return HttpResponse.normal(ERR_OK.code, ERR_OK.message, {"configs": data})

    except Exception as e:
      return HttpResponse.normal(ERR_DATABASE_ERROR.code, ERR_DATABASE_ERROR.message, {'message': str(e)})

@api.route('/report_net_flow', doc={"description": "net_flow"})
class ReportNetFlow(Resource):
  def post(self):
    try:
      params = request.get_json()
      logger.debug("netflow {}".format(params))
      uuid = params.get("uuid")
      if not uuid:
        return HttpResponse.normal(ERR_DATABASE_ERROR.code, ERR_DATABASE_ERROR.message, {'message': "uuid is None"})

      device = GDDevice.query.filter_by(dev_uuid=uuid).first()
      if not device:
        return HttpResponse.normal(ERR_DATABASE_ERROR.code, ERR_DATABASE_ERROR.message, {'message': "uuid {} is not exist".format(uuid)})

      now_stamp = datetime.strptime("{} {}".format(params.get("date"), params.get("time")), "%Y-%m-%d %H:%M")
      for interface_name, value in params.get("netflow").items():
        if interface_name.find("em") != -1:
          up = value['up']
          down = value['down']
          netflow = GDNetflow({"date_time":now_stamp, "device_uuid":uuid,
                               "interface_name":interface_name, "netflow_up":up,
                               "netflow_down":down})
          logger.debug("netflow datetime {} uuid {} interface_name {} up {}Kbps down {}kbps".format(str(now_stamp),
                                      uuid, interface_name, up, down))
          db.session.add(netflow)
          db.session.commit()
      return HttpResponse.normal(ERR_OK.code, ERR_OK.message, {"message": "success"})
    except Exception as e:
      return HttpResponse.normal(ERR_DATABASE_ERROR.code, ERR_DATABASE_ERROR.message, {'message': str(e)})
