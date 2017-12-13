#-*- coding=utf-8 -*-
from tool.const import Const
import sys


class Lang(object):
    __Lang = {
        "app_name": {
            "zh": "安卓日志分析工具",
            "en": "Android Log Analysis Tool"
        },
        "": (),
    }
    __LangType = 'en'

    class ConstError(TypeError): pass
    class IdError(TypeError): pass

    def __setattr__(self, key, value):
        raise self.ConstError, "Const Class"

    def __getattr__(self, key):
        if self.__Lang.has_key(key):
            return self.__Lang[key][self.__LangType]
        else:
            raise self.IdError, "No such lang id %s" % key

    def SetLangType(self, type='zh'):
        self.__LangType = type

    def GetLangType(self):
        return self.__LangType


sys.modules[__name__] = Lang()
