# coding=utf-8
import json
import os

from tool.StringPattern import *
from crash.crash import *
from parser.JavaCrashParser import *
from parser.NativeCrashParser import *
import tool.tools as tool

__M_JAVA__ = "Java Crash"
__M_NATIVE__= "Native Crash"
__M_ANR__="ANR"


class LineReader(file):
    def __init__(self, name, mode):
        super(LineReader, self).__init__(name, mode)
        #self.file=open(name, mode)
        self.line_num=0

    def readline(self,size=None):
        if not size:
            line = super(LineReader, self).readline()
        else:
            line = super(LineReader, self).readline(size)
        self.line_num += 1
        return line

    def rollbackline(self, offset):
        try:
            super(LineReader, self).seek(offset, 1)
            self.line_num-=1
        except IOError as ioe:
            tool.log("rollbackline", "IOError: " + ioe.strerror)

class Parser(object):

    __THRESHOLD__ = 10

    def __init__(self, log_path, modules=()):
        self.log_path = log_path
        # TODO
        # self.modules = modules
        self.modules = modules
        self.searcher = StringPattern()

        self.log_size = float(tool.getFileSize(log_path))

        # progress callback for ParserManager
        self.pg_listener = None
        # progress level, can not > __THRESHOLD__
        self.pg_curr_level = 0

        # progress triggers
        t = self.log_size / self.__THRESHOLD__
        self.pg_levels = [t*(x+1) for x in range(self.__THRESHOLD__)]

        #sender
        self.sender = None

    @DeprecationWarning
    # see set_pipe_sender
    def set_progress_listener(self ,listener):
        self.pg_listener = listener

    def set_pipe_sender(self, wpipe):
        self.sender = wpipe

    def parse(self):
        # 打开log文件
        logfp=LineReader(self.log_path, 'r')

        # 所有模块的结果
        all_module_results = {}
        for m in self.modules:
            all_module_results[m] = []

        line = '#'
        #count = 0

        while line:
            # 按行扫描
            line = logfp.readline().decode("utf-8")
            if not line: break

            if __M_JAVA__ in self.modules and line.find(JavaCrashParser.__ENTRY__) > 0:
                #count+=1
                #print "line number = ", logfp.line_num, count
                java_parser = JavaCrashParser(logfp, start_line=line)
                jr = java_parser.parse()
                if jr not in all_module_results[__M_JAVA__]:
                    all_module_results[__M_JAVA__].append(jr)
                    #print jr.occurred_time
                else:
                    p_index = all_module_results[__M_JAVA__].index(jr)
                    p = all_module_results[__M_JAVA__][p_index]
                    # TODO 内部去重
                    #print "exception in line {0} is same as {1}".format(jr.location_in_log.found_line, p.location_in_log)

            elif __M_NATIVE__ in self.modules and line.find(NativeCrashParser.__ENTRY__) > 0:
                print line
                pass

            elif __M_ANR__ in self.modules:
                pass

            # get progress
            # @Deprecated see @self.sender
            if self.pg_listener\
                    and logfp.tell() >= self.pg_levels[self.pg_curr_level]:
                self.pg_curr_level += 1
                percent = logfp.tell() / self.log_size
                self.pg_listener(self.log_path, percent)

            if self.sender\
                    and logfp.tell() >= self.pg_levels[self.pg_curr_level]:
                self.pg_curr_level += 1
                percent = logfp.tell() / self.log_size
                os.write(self.sender, "path: {0}, percent: {1}".format(self.log_path, percent))

        #print "len(all_module_results[__M_JAVA__])", len(all_module_results[__M_JAVA__])
        print all_module_results
        return all_module_results

if __name__ == "__main__":
    import time
    a =  time.time()
    parser = Parser('/home/qinsw/pengtian/tmp/cmcc_monkey/asrlog-0037(1122)/asrlog-2017-11-21-17-06-29/1/android/crash-17-06-30.log', (__M_JAVA__, ))
    parser.parse()
    #parser = Parser('/home/qinsw/pengtian/tmp/cmcc_monkey/asrlog-0037(1122)/asrlog-2017-11-21-17-06-29/1/android/main-17-06-30.log', (__M_JAVA__, ))
    #parser.parse()

    # fp = LineReader('/home/qinsw/Downloads/Python-2.7.3/setup.py','r')
    # fp.rollbackline(-len("1edad"))
    # print fp.line_num
    print time.time() - a
    #print  file.__doc__