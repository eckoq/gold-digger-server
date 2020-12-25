#
# Copyright (C) Gold-Digger, Inc.
#

#!/usr/bin/env python
#-*- coding: utf-8 -*-

from app.common.db import db

class GDIsp(db.Model):
  __tablename__ = 'gd_isp_t'
  isp_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
  isp_name = db.Column(db.String(128))

  def __init__(self, id_, name_):
    self.isp_id = id_
    self.isp_name = name_

  def to_json(self):
    return {
      "isp_id" : self.isp_id,
      "isp_name" : self.isp_name
    }

  def to_list(self):
    return [self.isp_id, self.isp_name]
