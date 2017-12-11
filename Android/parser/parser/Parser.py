# coding=utf-8
import json

from parser.tool.StringPattern import *
from parser.crash.crash import *
from parser.parser.JavaCrashParser import *
from parser.parser.NativeCrashParser import *


class Result(object):
    def __init__(self):
        self.java_crash = []
        self.native_crash = []


class Parser(object):
    def __init__(self, cfg_path, log_path, modules):
        self.cfg_path = cfg_path
        self.log_path = log_path
        self.modules = modules
        self.searcher = StringPattern()

    def set_config_path(self, path):
        self.cfg_path = path

    def set_log_path(self, path):
        self.log_path = path

    def __load_config__(self):
        with open(self.cfg_path, 'r') as json_file:
            data = json.load(json_file)
            return data

    def __index_of__(self, child, parent):
        self.searcher.set_pattern(child)
        self.searcher.set_source(parent)
        return self.searcher.string_pattern_bm()

    def _check_is_entry(self, entry, l):
        try:
            if self.__index_of__(entry, l) > 0:
                return True
        except Exception as e:
            return False
        return False

    def parse(self):
        # 打开log文件
        logfp = open(self.log_path, 'r')

        # 所有模块的结果
        all_module_results = Result()

        line = '#'

        while line:
            # 按行扫描
            line = logfp.readline().decode("utf-8")

            # JavaCrashParser
            if self.__index_of__(JavaCrashParser.__ENTRY__, line):
                java_parser = JavaCrashParser(logfp, start_line=line)
                jr = java_parser.parse()
                all_module_results.java_crash.append(jr)
            elif self.__index_of__(NativeCrashParser.__ENTRY__, line):
                pass

