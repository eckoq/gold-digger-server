#
# Copyright (C) Gold-Digger, Inc.
#

#!/usr/bin/env python
#-*- coding: utf-8 -*-

from app.common.db import db

class GDNetflow(db.Model):
  __tablename__ = 'gd_netflow_t'
  date_time = db.Column(db.DateTime, primary_key=True)
  device_uuid = db.Column(db.String(64), primary_key=True)
  interface_name  = db.Column(db.String(64), primary_key=True)
  netflow_up = db.Column(db.Integer)
  netflow_down = db.Column(db.Integer)

  def __init__(self, data):
    self.date_time = data.get("date_time")
    self.device_uuid = data.get("device_uuid")
    self.interface_name = data.get("interface_name")
    self.netflow_up = data.get("netflow_up")
    self.netflow_down = data.get("netflow_down")

  def to_json(self):
    return {
      "date_time" : self.date_time,
      "device_uuid" : self.device_uuid,
      "interface_name" : self.interface_name,
      "netflow_up" : self.netflow_up,
      "netflow_down" : self.netflow_down
    }
