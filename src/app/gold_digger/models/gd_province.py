#
# Copyright (C) Gold-Digger, Inc.
#

#!/usr/bin/env python
#-*- coding: utf-8 -*-

from app.common.db import db

class GDProvince(db.Model):
  __tablename__ = 'gd_province_t'
  province_id = db.Column(db.Integer, primary_key = True)
  province_name = db.Column(db.String(40))

  def __init__(self, id_, name_):
    self.province_id = id_
    self.province_name = name_

  def to_json(self):
    return {
      'province_id': self.province_id,
      'province_name': self.province_name
    }

  def to_list(self):
    return [self.province_id, self.province_name]
