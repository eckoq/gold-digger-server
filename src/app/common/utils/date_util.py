#
# Copyright (C) Gold-Digger, Inc.
#

#!/usr/bin/env python
#-*- coding: utf-8 -*-

import math
import arrow
import pandas as pd

DEFAULT_FULL_FORMAT = 'YYYY-MM-DD HH:mm:ss'
DEFAULT_DATE_FORMAT = 'YYYY-MM-DD'
DEFAULT_MONTH_FORMAT = 'YYYY-MM'


class DateUtil(object):
    @staticmethod
    def curr_time():
        t_time = arrow.now()
        return t_time.format(DEFAULT_FULL_FORMAT)

    @staticmethod
    def full_to_date(date):
        t_time = arrow.get(date, DEFAULT_FULL_FORMAT)
        return t_time.format(DEFAULT_DATE_FORMAT)

    @staticmethod
    def today():
        t_time = arrow.now()
        return t_time.format(DEFAULT_DATE_FORMAT)

    @staticmethod
    def this_month():
        t_time = arrow.now()
        return t_time.format(DEFAULT_MONTH_FORMAT)

    @staticmethod
    def day_shift(date, num):
        t_time = arrow.get(date, DEFAULT_DATE_FORMAT)
        return t_time.shift(days=num).format(DEFAULT_DATE_FORMAT)

    @staticmethod
    def month_shift(date, num):
        t_time = arrow.get(date, DEFAULT_MONTH_FORMAT)
        return t_time.shift(months=num).format(DEFAULT_MONTH_FORMAT)

    @staticmethod
    def get_days_between_begin_and_end(begin_date, end_date):
        return int(
            math.fabs((arrow.get(end_date) - arrow.get(begin_date)).days))

    @staticmethod
    def get_range_between_begin_and_end(begin_date, end_date):
        return pd.date_range(begin_date, end_date,
                             freq='D').strftime("%Y-%m-%d").tolist()

    @staticmethod
    def get_range_month_between_begin_and_end(begin_date, end_date):
        return pd.date_range(begin_date, end_date,
                             freq='MS').strftime("%Y-%m").tolist()

    @staticmethod
    def get_five_min_between_begin_and_end(begin_date, end_date):
        days = DateUtil.get_days_between_begin_and_end(begin_date, end_date)
        return pd.date_range(
            begin_date, periods=288 * (days + 1),
            freq='5min').strftime("%Y-%m-%d %H:%M:%S").tolist()

    @staticmethod
    def get_first_day_in_month(date):
        t_time = arrow.get(date, DEFAULT_DATE_FORMAT)
        return arrow.get(t_time.year, t_time.month, 1).format(DEFAULT_DATE_FORMAT)
