#
# Copyright (C) Gold-Digger, Inc.
#

#!/usr/bin/env python
#-*- coding: utf-8 -*-

from app.common.db import db

class GDConfig(db.Model):
  __tablename__ = 'gd_config_t'
  device_uuid = db.Column(db.String(64), primary_key=True)
  ppp_id = db.Column(db.Integer, primary_key=True)
  ppp_addr = db.Column(db.String(64))
  ppp_user = db.Column(db.String(128))
  ppp_passwd = db.Column(db.String(128))
  ppp_vlan_id = db.Column(db.Integer)
  ppp_vlan_addr = db.Column(db.String(64))
  ppp_vlan_parent = db.Column(db.String(24))


  def __init__(self, data):
    self.device_uuid = data.get("device_uuid")
    self.ppp_addr = data.get("ppp_id")
    self.ppp_addr = data.get("ppp_addr")
    self.ppp_user = data.get("ppp_user")
    self.ppp_passwd = data.get("ppp_passwd")
    self.ppp_vlan_id = data.get("ppp_vlan_id")
    self.ppp_vlan_addr = data.get("ppp_vlan_addr")
    self.ppp_vlan_parent = data.get("ppp_vlan_parent")

  def to_json(self):
    return {
      "ppp_id" : self.ppp_id,
      "ppp_addr" : self.ppp_addr,
      "ppp_user" : self.ppp_user,
      "ppp_passwd" : self.ppp_passwd,
      "ppp_vlan_id" : self.ppp_vlan_id,
      "ppp_vlan_addr": self.ppp_vlan_addr,
      "ppp_vlan_parent" : self.ppp_vlan_parent,
    }
