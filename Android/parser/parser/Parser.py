# coding=utf-8
import json

from tool.StringPattern import *
from crash.crash import *
from parser.JavaCrashParser import *
from parser.NativeCrashParser import *


class Result(object):
    def __init__(self):
        self.java_crash = []
        self.native_crash = []

__M_JAVA__ = "Java Crash"
__M_NATIVE__= "Native Crash"
__M_ANR__="ANR"


class Parser(object):
    def __init__(self, log_path, modules=()):
        self.log_path = log_path
        self.modules = modules
        self.searcher = StringPattern()

    def set_log_path(self, path):
        self.log_path = path

    def parse(self):
        # 打开log文件
        logfp = open(self.log_path, 'r')

        # 所有模块的结果
        all_module_results = Result()

        line = '#'
        count = 0

        while line:
            # 按行扫描
            line = logfp.readline().decode("utf-8")

            if __M_JAVA__ in self.modules and line.find(JavaCrashParser.__ENTRY__) > 0:
                java_parser = JavaCrashParser(logfp, start_line=line)
                jr = java_parser.parse()
                all_module_results.java_crash.append(jr)

            elif __M_NATIVE__ in self.modules and line.find(NativeCrashParser.__ENTRY__) > 0:
                print line
                count+=1
                pass

            elif __M_ANR__ in self.modules:
                pass
        print count

if __name__ == "__main__":
    import time
    a =  time.time()
    parser = Parser('', '/home/qinsw/pengtian/tmp/cmcc_monkey/asrlog-0037(1122)/asrlog-2017-11-21-17-06-29/1/android/events-17-06-30.log', (__M_JAVA__, ))
    parser.parse()
    parser = Parser('', '/home/qinsw/pengtian/tmp/cmcc_monkey/asrlog-0037(1122)/asrlog-2017-11-21-17-06-29/1/android/radio-17-06-30.log', (__M_JAVA__, ))
    parser.parse()
    print time.time() - a