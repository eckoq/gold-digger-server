#
# Copyright (C) Gold-Digger, Inc.
#

#!/usr/bin/env python
#-*- coding: utf-8 -*-


class _const:
    class ConstError(TypeError):
        pass

    class ConstCaseError(ConstError):
        pass

    def __setattr__(self, key, value):
        if key in self.__dict__:
            raise self.ConstError("Can't change const.%s" % key)
        # if not key.isupper():
        #     raise self.ConstCaseError('Const name "%s" is not all uppercase' % key)
        self.__dict__[key] = value


const = _const()
