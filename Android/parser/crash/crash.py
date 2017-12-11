class Time(object):
    def __init__(self, MON, DAY, H, M, S, U, string):
        self.MON = MON
        self.DAY = DAY
        self.H = H
        self.M = M
        self.S = S
        self.U = U
        self.string = string

    def is_older_than(self, other):
        if other: pass
        else: return True

        if type(other) is not Time:
            print "TIME: is_older_than: error, other is not Type Time"
            return False
        if self.MON > other.MON: return True
        elif self.MON < other.MON: return False
        elif self.DAY > other.DAY: return True
        elif self.DAY < other.DAY: return False
        elif self.H > other.H: return True
        elif self.H < other.H: return False
        elif self.M > other.M: return True
        elif self.M < other.M: return False
        elif self.S > other.S: return True
        elif self.S < other.S: return False
        elif self.U > other.U: return True
        else: return False

    def __str__(self):
        return self.string

class LLocation(object):
    def __init__(self, log_file_path='', found_line=0):
        self.log_file_path = log_file_path
        self.found_line = found_line

    def __str__(self):
        return "<LLocation>" + "<" + str(hex(self.__hash__())) + ">" + str(self.__dict__)


class SLocation(object):
    def __init__(self, source_file_name='', occurred_line=0, in_this=False):
        self.source_file_name = source_file_name
        self.occurred_line = occurred_line
        self.in_this_package = in_this

    def __str__(self):
        return "<SLocation>" + "<" + str(hex(self.__hash__())) + ">" + str(self.__dict__)

class Crash(object):
    def __init__(self):
        self.name_package = ''
        self.reason = ''
        self.p_t_id = 0
        self.location_in_log = None
        self.occurred_time = None
        self.stack_trace = []

    def __str__(self):
        s =   "--|--" + "name_package = " + self.name_package + "\n"\
            + "  |--" + "reason = " + self.reason + "\n" \
            + "  |--" + "p_t_id = " + bytes(self.p_t_id) + "\n" \
            + "  |--" + "occurred_time = " + self.occurred_time.__str__() + "\n" \
            + "  |--" + "location_in_log = " + self.location_in_log.__str__() + "\n"
        if len(self.stack_trace) > 0:
            s += "  |--" + "stack_trace[0] = " + self.stack_trace[0] + "\n"
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
        s +=  "  |--" + "location_in_src = " + "\n"
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