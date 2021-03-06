# coding=utf-8
import json
import os

from tool.StringPattern import *
from crash.crash import *
from parser.JavaCrashParser import *
from parser.NativeCrashParser import *
import tool.tools as tool

__M_JAVA__ = "Java Crash"
__M_NATIVE__ = "Native Crash"
__M_ANR__ = "ANR"


class LineReader(file):
    def __init__(self, name, mode):
        super(LineReader, self).__init__(name, mode)
        # self.file=open(name, mode)
        self.line_num = 0

    def readline(self, size=None):
        if not size:
            line = super(LineReader, self).readline()
        else:
            line = super(LineReader, self).readline(size)
        self.line_num += 1
        return line

    def rollbackline(self, offset):
        try:
            super(LineReader, self).seek(offset, 1)
            self.line_num -= 1
        except IOError as ioe:
            tool.log("rollbackline", "IOError: " + ioe.strerror)


class Parser(object):
    __THRESHOLD__ = 10

    def __init__(self, log_path):
        self.log_path = log_path

        # TODO 从配置文件中读取配置，而不是经过参数传递
        self.modules = (__M_JAVA__, __M_NATIVE__, __M_ANR__)
        self.searcher = StringPattern()

        self.log_size = float(tool.getFileSize(log_path))

        # progress callback for ParserManager
        self.pg_listener = None
        # progress level, can not > __THRESHOLD__
        self.pg_curr_level = 0

        # 由于有的文件太大，不可能有一丝处理进度变化就向上反馈。
        # 此处根据log文件计算一个衡量单位， 超过一个这样的单位，再向上汇报
        t = self.log_size / self.__THRESHOLD__
        self.pg_levels = [t * (x + 1) for x in range(self.__THRESHOLD__)]

        # 负责将处理进度和过程发送给ParserManager进行汇总
        self.send_queue = None

    def set_sender(self, s):
        self.send_queue = s

    def parse(self):
        # 打开log文件
        logfp = LineReader(self.log_path, 'r')

        # 所有模块的结果
        all_module_results = {}
        for m in self.modules:
            all_module_results[m] = []

        line = '#'
        # count = 0

        while line:
            # 按行扫描
            try:
                #line = logfp.readline().decode("utf-8")
                line = logfp.readline()
            except UnicodeDecodeError as e:
                print "FUCK---------------------------------" + self.log_path + "      " + e.message
            if not line:
                break
            # if re.match(r'\s', line):
            #     print "empty line"
            #     continue

            if __M_JAVA__ in self.modules and line.find(JavaCrashParser.__ENTRY__) > 0:
                # count+=1
                # print "line number = ", logfp.line_num, count
                java_parser = JavaCrashParser(logfp, start_line=line)
                jr = java_parser.parse()
                if jr not in all_module_results[__M_JAVA__]:
                    all_module_results[__M_JAVA__].append(jr)
                    # print jr.occurred_time
                else:
                    p_index = all_module_results[__M_JAVA__].index(jr)
                    p = all_module_results[__M_JAVA__][p_index]
                    p.combine(jr)

                    # print p

            elif __M_NATIVE__ in self.modules and line.find(NativeCrashParser.__ENTRY__) > 0:
                # print line
                pass

            elif __M_ANR__ in self.modules:
                pass

            # 如果此时的读取的个数大于计算出的阀值， 则进行上报
            if self.send_queue \
                    and logfp.tell() >= self.pg_levels[self.pg_curr_level]:
                self.pg_curr_level += 1
                percent = logfp.tell() / self.log_size

                # 字典数据类型： {"mode": 1, "log_path": xxx, "percent": xxx}
                self.send_queue.put({"mode": 1, "log_path": self.log_path, "percent": percent})

        # print "len(all_module_results[__M_JAVA__])", len(all_module_results[__M_JAVA__])
        # print all_module_results
        return all_module_results


if __name__ == "__main__":
    import time

    a = time.time()
    parser = Parser(
        '/home/qinsw/pengtian/tmp/cmcc_monkey/asrlog-0037(1122)/asrlog-2017-11-21-17-06-29/1/android/crash-17-06-30.log')
    parser.parse()
    # parser = Parser('/home/qinsw/pengtian/tmp/cmcc_monkey/asrlog-0037(1122)/asrlog-2017-11-21-17-06-29/1/android/main-17-06-30.log', (__M_JAVA__, ))
    # parser.parse()

    # fp = LineReader('/home/qinsw/Downloads/Python-2.7.3/setup.py','r')
    # fp.rollbackline(-len("1edad"))
    # print fp.line_num
    print time.time() - a
    # print  file.__doc__
