#
# Copyright (c) Gold-Digger, Inc.
#

#!/usr/bin/python
#-*- coding: utf-8 -*-


from flask import Blueprint, request
from flask_restx import Resource
from flask_login import login_required
from sqlalchemy.exc import SQLAlchemyError
from app.common.db import db
from app.common.utils import logger_util
from app.common.utils.fix_swagger_api import CustomApi
from app.common.utils.http_util import HttpResponse
from app.common.error import ERR_OK, ERR_DATABASE_ERROR, ERR_PARAMS_ERROR, ERR_API_RETURN_INVALID, ERR_CELERY_ERROR

from app.gold_digger.models import GDIsp
from app.gold_digger.models import GDProvince
from app.gold_digger.models import GDDevice
from app.gold_digger.models import GDNetflow

# create Blueprint
device_manager_bp = Blueprint("device_manager", __name__)

# create log
logger = logger_util.Logger("dashboard").logger

# customApi
api = CustomApi(device_manager_bp, title='device_manager API', description='handle device manager request', prefix="/")

@api.route('/get_query_configs', doc={"description": "get query config"})
class GetQueryConfigs(Resource):
  decorators = [login_required]
  def post(self):
    try:
      # isps
      result = GDIsp.query.all()
      isps = [isp.to_json() for isp in result]

      # provinces
      result = GDProvince.query.all()
      provinces = [province.to_json() for province in result]

      data = {}
      data['isps'] = isps
      data['provinces'] = provinces

      return HttpResponse.normal(ERR_OK.code, ERR_OK.message, data)
    except Exception as e:
      return HttpResponse.normal(ERR_DATABASE_ERROR.code, ERR_DATABASE_ERROR.message, {'message': str(e)})

@api.route('/get_device', doc={"description": "get device"})
class GetDevice(Resource):
  decorators = [login_required]
  def post(self):
    try:
      params = request.get_json()
      logger.debug(params)
      cur_page = params.get('cur_page')
      page_size = params.get('page_size')
      device_id = params.get('device_id')
      isp_id = params.get('isp_id')
      province_id = params.get('province_id')
      display_column = params.get('display_column')
      columns = display_column.keys()

      filters = []
      if device_id:
        devices = device_id.split('\n')
        devices = map(lambda x: x.strip(), devices)
        logger.debug(devices)
        filters.append(GDDevice.dev_uuid.in_(devices))

      if isp_id:
        filters.append(GDDevice.isp == isp_id)

      if province_id:
        filters.append(GDDevice.province == province_id)

      node_pages = GDDevice.query.filter(*filters).paginate(cur_page, page_size)
      nodes = list()
      for node in node_pages.items:
        node_dict = {}
        node_json = node.to_json()
        for col in columns:
          node_dict[col] = node_json[col]
        nodes.append(node_dict)

      data = {
        'nodes': nodes,
        'count': node_pages.total
      }
      return HttpResponse.normal(ERR_OK.code, ERR_OK.message, data)
    except Exception as e:
      return HttpResponse.normal(ERR_DATABASE_ERROR.code, ERR_DATABASE_ERROR.message, {'message': str(e)})

@api.route('/get_netflow', doc={"description": "get netflow"})
class GetNetflow(Resource):
  decorators = [login_required]
  def post(self):
    try:
      params = request.get_json()
      logger.debug(params)

      dev_uuid = params.get('dev_uuid')
      date_time = params.get('date_time')

      if not dev_uuid:
        return HttpResponse.normal(ERR_PARAMS_ERROR.code, ERR_PARAMS_ERROR.message, {"message": "dev_uuid {} is not fine".format(dev_uuid)})

      if not isinstance(date_time, list):
        return HttpResponse.normal(ERR_PARAMS_ERROR.code, ERR_PARAMS_ERROR.message, {"message": "date_time {} is not fine".format(date_time)})

      filters = []
      if dev_uuid:
        filters.append(GDNetflow.device_uuid == dev_uuid)

      if len(date_time) == 1:
        filters.append(GDNetflow.date_time >= date_time[0])
      elif len(date_time) == 2:
        filters.append(GDNetflow.date_time >= date_time[0])
        filters.append(GDNetflow.date_time <= date_time[1])
      else:
        pass

      data = {}
      items = GDNetflow.query.filter(*filters).order_by(GDNetflow.date_time.asc()).all()
      for item in items:
        item_json = item.to_json()
        interface_name = item_json.get("interface_name")
        if interface_name not in data:
          data[interface_name] = []

        data[interface_name].append([item_json.get("date_time"), item_json.get("netflow_up"), item_json.get("netflow_down")])
      return HttpResponse.normal(ERR_OK.code, ERR_OK.message, data)
    except Exception as e:
      return HttpResponse.normal(ERR_DATABASE_ERROR.code, ERR_DATABASE_ERROR.message, {'message': str(e)})
