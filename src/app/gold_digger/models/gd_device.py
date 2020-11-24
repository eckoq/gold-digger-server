#
# Copyright (C) Gold-Digger, Inc.
#

#!/usr/bin/env python
#-*- coding: utf-8 -*-

from app.common.db import db

class GDDevice(db.Model):
  __tablename__ = 'gd_device_t'
  mac_addr = db.Column(db.String(64), unique=True, nullable=False, primary_key=True)
  provider = db.Column(db.Integer)
  cpu_model = db.Column(db.String(64))
  cpu_cores = db.Column(db.Integer)
  total_mem = db.Column(db.Integer)
  nic_type = db.Column(db.String(64))
  nic_count = db.Column(db.Integer)
  total_storage = db.Column(db.Integer)
  disk_details = db.Column(db.String(64))
  system_version = db.Column(db.String(64))
  kernel_version = db.Column(db.String(64))
  isp = db.Column(db.Integer)
  province = db.Column(db.Integer)
  city = db.Column(db.String(32))
  up_bandwidth = db.Column(db.Integer)
  ip = db.Column(db.String(64))
  web_port = db.Column(db.Integer)
  online_time = db.Column(db.Integer)
  upstream_traffic = db.Column(db.Integer)
  downstream_traffic = db.Column(db.Integer)
  pass_time = db.Column(db.DateTime)

  def __init__(self, data):
    self.mac_addr = data.get("mac_addr")
    self.provider = data.get("provider")
    self.cpu_model = data.get("cpu_model")
    self.cpu_cores = data.get("cpu_cores")
    self.total_mem = data.get("total_mem")
    self.nic_type = data.get("nic_type")
    self.nic_count = data.get("nic_count")
    self.total_storage = data.get("total_storage")
    self.disk_details = data.get("disk_details")
    self.system_version = data.get("system_version")
    self.kernel_version = data.get("kernel_version")
    self.isp = data.get("isp")
    self.province = data.get("province")
    self.city = data.get("city")
    self.up_bandwidth = data.get("up_bandwidth")
    self.ip = data.get("ip")
    self.web_port = data.get("web_port")
    self.online_time = data.get("online_time")
    self.upstream_traffic = data.get("upstream_traffic")
    self.downstream_traffic = data.get("downstream_traffic")
    self.pass_time = data.get("pass_time")

  def to_json(self):
    return {
      "mac_addr" : self.mac_addr,
      "provider" : self.provider,
      "cpu_model" : self.cpu_model,
      "cpu_cores" : self.cpu_cores,
      "total_mem" : self.total_mem,
      "nic_type" : self.nic_type,
      "nic_count": self.nic_count,
      "total_storage" : self.total_storage,
      "disk_details" : self.disk_details,
      "system_version" : self.system_version,
      "kernel_version" : self.kernel_version,
      "isp" : self.isp,
      "province" : self.province,
      "city" : self.city,
      "up_bandwidth" : self.up_bandwidth,
      "ip" : self.ip,
      "web_port" : self.web_port,
      "online_time" : self.online_time,
      "upstream_traffic" : self.upstream_traffic,
      "downstream_traffic" : self.downstream_traffic,
      "pass_time": self.pass_time,
    }
