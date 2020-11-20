#
# Copyright (C) Gold-Digger, Inc.
#

#!/usr/bin/env python
#-*- coding: utf-8 -*-

import numpy as np
from .date_util import DateUtil


class DataUtil(object):
    @staticmethod
    def get_full_day_data(begin_date, end_date, date2flux, num_point):
        date_list = DateUtil.get_range_between_begin_and_end(begin_date, end_date)
        full_data = list()
        for date in date_list:
            flux = date2flux.get(date.replace('-', ''), np.full(num_point, 0))
            full_data.extend(flux)
        return full_data

    @staticmethod
    def list_of_groups(init_list, children_list_len):
        list_of_groups = zip(*(iter(init_list),) * children_list_len)
        end_list = [list(i) for i in list_of_groups]
        count = len(init_list) % children_list_len
        end_list.append(init_list[-count:]) if count != 0 else end_list
        return end_list
