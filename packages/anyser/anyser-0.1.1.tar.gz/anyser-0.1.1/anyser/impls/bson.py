# -*- coding: utf-8 -*-
#
# Copyright (c) 2020~2999 - Cologler <skyoflw@gmail.com>
# ----------
#
# ----------

import bson
import struct

from ..err import SerializeError
from ..abc import *
from ..core import register_format

@register_format('bson', '.bson')
class BsonSerializer(ISerializer):
    format_name = 'bson'

    def loadb(self, b: bytes, options: dict) -> Any:
        kwargs = {}
        kwargs.update(Options.pop_origin_kwargs(options))
        self.check_options(options)
        try:
            return bson.loads(b, **kwargs)
        except Exception as e:
            raise SerializeError(e)

    def dumpb(self, obj, options: dict) -> bytes:
        kwargs = {}
        kwargs.update(Options.pop_origin_kwargs(options))
        self.check_options(options)
        try:
            return bson.dumps(obj, **kwargs)
        except Exception as e:
            raise SerializeError(e)
