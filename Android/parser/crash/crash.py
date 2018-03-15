# coding=utf-8
import time
import tool.tools as tool
import re


class LLocation(object):
    def __init__(self, log_file_path='', found_line=0):
        self.log_file_path = log_file_path
        self.found_line = found_line

    def __str__(self):
        # return "<LLocation>" + "<" + str(hex(self.__hash__())) + ">" + str(self.__dict__)
        return str(self.__dict__)

    def __eq__(self, other):
        if type(other) is not LLocation:
            return False
        if self.log_file_path == '' or \
                other.log_file_path == '':
            return False
        return self.log_file_path == other.log_file_path and self.found_line == other.found_line


class SLocation(object):
    def __init__(self, source_file_name='', occurred_line=0, in_this=False):
        self.source_file_name = source_file_name
        self.occurred_line = occurred_line
        self.in_this_package = in_this

    def __str__(self):
        # return "<SLocation>" + "<" + str(hex(self.__hash__())) + ">" + str(self.__dict__)
        return str(self.__dict__)


class CrashBaseInfo(object):
    def __init__(self):
        # 同一个异常pid集合， 保证顺序和 location_in_log、occurred_time相等
        self.p_t_id = 0
        # 异常在log中位置集合
        self.location_in_log = None
        # 异常发生时间集合
        self.occurred_time = tool.get_format_time()

    def sort(self):
        pass


class Crash(object):
    def __init__(self):
        self.name_package = ''
        self.reason = ''
        # 用于当存在相同时，存储各个Crash发生的基础信息：谁，时间，地点
        self.base_info = CrashBaseInfo()
        self.base_info_set = []
        self.stack_trace = []

    def combine(self, other):
        self.base_info_set.extend(other.base_info_set)

    def __str__(self):
        s = "--|--" + "name_package = " + self.name_package + "\n"\
            + "  |--" + "reason = " + self.reason + "\n"
        if len(self.base_info_set) > 0:
            for l, bis in enumerate(self.base_info_set):
                s += "  |--" + "p_t_id[%d] = %s" % (l, bis.p_t_id) + "\n"
                s += "  |--" + "occurred_time[%d] = %s" % (l, bis.occurred_time) + "\n"
                s += "  |--" + "location_in_log[%d] = %s" % (l, bis.location_in_log) + "\n"
        if len(self.stack_trace) > 0:
            for l, t in enumerate(self.stack_trace):
                s += "  |--" + "stack_trace[%d] = %s" % (l, t)
        return s


class JavaCrash(Crash):
    src_length = 4

    def __init__(self):
        super(JavaCrash, self).__init__()
        self.location_in_src = []

    def __eq__(self, other):
        if type(other) is not JavaCrash:
            return False
        return self.name_package == other.name_package and self.reason == other.reason

    def __str__(self):
        s = super(JavaCrash, self).__str__()
        s += "  |--" + "location_in_src = " + "\n"
        for ls in self.location_in_src:
            s += "      |--" + ls.__str__() + "\n"
        return s


class NativeCrash(Crash):
    def __init__(self):
        super(NativeCrash, self).__init__()
        self.error_signal = ''

    def __eq__(self, other):
        if type(other) is not NativeCrash:
            return False
        if self.reason == '' and other.reason == '':
            return False
        return self.name_package == other.name_package and self.reason == other.reason

    def __str__(self):
        s = super(NativeCrash, self).__str__()
        s += "  |--" + "error_signal = " + str(self.error_signal)
        return s


if __name__ == '__main__':
    a = JavaCrash()
    a.name_package = "a"
    a.reason = "a"

    b = JavaCrash()
    b.name_package = "a"
    b.reason="a"
    #print a
    #print b
    ab = []
    ab.append(a)
    print cmp(a, b)
    if b in ab:
        print "equal"
