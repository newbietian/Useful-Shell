# def echo(s):
#     TAG = "JavaCrashParser: "
#     print TAG + s
#
# echo ("header_len = {0}".format(1))

from parser.tool.StringPattern import *
from parser.parser.JavaCrashParser import *
import difflib

line_number = 0
def __index_of__(searcher,child, parent):
    searcher.set_pattern(child)
    searcher.set_source(parent)
    return searcher.string_pattern_bm()

def __readline__(file):
    global line_number
    line = file.readline().decode("utf-8")
    if line:
        line_number += 1
    return line

f=open("/home/qinsw/Downloads/test1.log", 'r')
searcher = StringPattern()
line = "#"
print f.name
while line:
    line = __readline__(f)
    if __index_of__(searcher,"FATAL EXCEPTION: ", line) > 0:
        print line
        jp = JavaCrashParser(f,start_line=line)
        result = jp.parse()
        print result

# seq = difflib.SequenceMatcher(None, "com.android.camera2", "com.android.ex.camera2")
# ratio = seq.ratio()
# print ratio