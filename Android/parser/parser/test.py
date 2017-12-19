# coding=utf-8
# # def echo(s):
# #     TAG = "JavaCrashParser: "
# #     print TAG + s
# #
# # echo ("header_len = {0}".format(1))
#
# from tool.StringPattern import *
# from parser.JavaCrashParser import *
# import difflib
#
# line_number = 0
# def __index_of__(searcher,child, parent):
#     searcher.set_pattern(child)
#     searcher.set_source(parent)
#     return searcher.string_pattern_bm()
#
# def __readline__(file):
#     global line_number
#     line = file.readline().decode("utf-8")
#     if line:
#         line_number += 1
#     return line
#
# f=open("/home/qinsw/Downloads/test1.log", 'r')
# searcher = StringPattern()
# line = "#"
# print f.name
# while line:
#     line = __readline__(f)
#     if __index_of__(searcher,"FATAL EXCEPTION: ", line) > 0:
#         print line
#         jp = JavaCrashParser(f,start_line=line)
#         result = jp.parse()
#         print result
#
# # seq = difflib.SequenceMatcher(None, "com.android.camera2", "com.android.ex.camera2")
# # ratio = seq.ratio()
# # print ratio

#-----------------------------------------------------------------------------------------------------
# test calculate the read percent of file

# print 92346578904294827798427260213765816371 / 88888888888888888888888888
# path = "/home/qinsw/pengtian/tmp/test123.txt"
# a = "aodhjifjbhasifhbaiofhgajskfiahjasjlh你好\n"
# f = open(path, 'w')
# f.write(a)
# f.close()
#
# import os
# import tool.tools as tool
# print tool.getFileSize(path)
#
# print len(a)
# print len(bytes(a))
#
# import time
# a = time.time()
# path = "/home/qinsw/pengtian/tmp/cmcc_monkey/asrlog-0037(1122)/asrlog-2017-11-21-17-06-29/1/android/main-17-06-30.log"
# print tool.getFileSize(path)
# totalsize = tool.getFileSize(path)
# f=open(path,'r')
# line='#'
# count=0
# while line:
#     line = f.readline()
#     count+=len(line)
#     tmp = float(count) / totalsize
# print count
# print time.time() -a

from parser.ParserManager import ParserManager
from parser.Parser import __M_JAVA__,__M_NATIVE__,__M_ANR__
import tool.tools as tool
import multiprocessing

def progress_callback(progress):
    print "progress = ", progress, "pid = " , multiprocessing.current_process().pid
    if progress >= 1:
        print "Task Done"

if __name__ == "__main__":
    path = "/home/qinsw/pengtian/tmp/cmcc_monkey/asrlog-0037(1122)/asrlog-2017-11-21-17-06-29/1/android"
    list = tool.getParseableFileList(path)

    print list
    print "pid = = = = = " , multiprocessing.current_process().pid
    pm = ParserManager(4,list,(__M_JAVA__,))
    pm.setProgressCallback(progress_callback)
    pm.execute()

    import time
    time.sleep(15)
