#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from random import choice
import string


def gen_random_password(length=8, chars=string.ascii_letters + string.digits):
    return ''.join([choice(chars) for i in range(length)])


if __name__ == '__main__':
    for i in range(10):
        print(gen_random_password(12))
