#-*- coding=utf-8 -*-
from tool.const import Const
import sys

reload(sys)
sys.setdefaultencoding('utf8')

class Lang(object):
    __Lang = {
        "app_name": {
            "zh": "安卓日志分析工具",
            "en": "Android Log Analysis Tool"
        },
        "finished": {
            "zh": "已完成",
            "en": "Finished"
        },
        "task_log_path": {
            "zh": "日志路径",
            "en": "Log Path"
        },
        "task_status": {
            "zh": "状态",
            "en": "Status"
        },
        "task_state_processing": {
            "zh": "处理中",
            "en": "Processing"
        },
        "task_state_waiting": {
            "zh": "等待中",
            "en": "Waiting"
        },
        "task_state_generating": {
            "zh": "生成结果中",
            "en": "Generating result"
        },
        "task_state_paused": {
            "zh": "未完成，重新开始 ",
            "en": "Not Finished， Restart it, "
        },

    }
    __LangType = 'zh'

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
