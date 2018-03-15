# coding=utf-8
import re
from crash.crash import *
from tool.tools import Time

class JavaCrashParser(object):

    __ENTRY__ = "FATAL EXCEPTION:"

    # "java.lang.RuntimeException: Unable to start activity ComponentInfo{com.android.simsettings/com.android.simsettings.SimPreferenceDialog}": java.lang.NullPointerException: Attempt to invoke virtual method 'java.lang.CharSequence android.telephony.SubscriptionInfo.getDisplayName()' on a null object reference"
    # reason
    # 全 group1 = "java.lang.RuntimeException: Unable to start activity ComponentInfo{com.android.simsettings/com.android.simsettings.SimPreferenceDialog}"
    # group2 = "java.lang.RuntimeException"
    # group3 = "Unable to start activity ComponentInfo{com.android.simsettings/com.android.simsettings.SimPreferenceDialog}"
    # 如果存在, 如果不存在，则456为None
    # 全 group4 = "java.lang.NullPointerException: Attempt to invoke virtual method 'java.lang.CharSequence android.telephony.SubscriptionInfo.getDisplayName()' on a null object reference"
    # group5 = "java.lang.NullPointerException"
    # group6 = "Attempt to invoke virtual method 'java.lang.CharSequence android.telephony.SubscriptionInfo.getDisplayName()' on a null object reference"
    PAT_REASON = r"^(([^\s:]+): ([^:]+))(?:: (([^\s]+): (.*)))?"

    # "Process: com.android.phone, PID: 31866"
    # package, pid => group 1,2
    # group1 = package
    # group2 = pid
    PAT_NAME_PACKAGE = r"^Process: ([^,]+), PID: ([\d]+)"

    # at 用来判断 if match: then do
    PAT_AT = r"^\tat .+$"

    # 用来判断at开头，并获取文件和行号
    # file and line number => group 1,2
    # group1 = filename
    # group2 = number
    # exception: 	at java.lang.reflect.Method.invoke(Native Method)
    PAT_AT_FILE_LINE = r"^\tat [^(]+\(([^: ]+?)(?:[: ])([\d]+|[\S]+)\).*$"

    # caused by
    # group1 = caused by
    PAT_CAUSED_BY = r"^Caused by: (.*$)"


    # get occurred time
    # "05-10 02:06:16.628 I/NetworkIdentity( 2603): buildNetworkIdentity:"
    PAT_TIME = r"^(\d\d-\d\d\s\d\d:\d\d:\d\d\.\d\d\d)"

    # 支持一下三种格式的log
    #     "08-18 16:52:54.902  5672  5672 E AndroidRuntime: 	at android.app.FragmentManagerImpl.moveToState(FragmentManager.java:1148)"
    #     "11-21 23:02:48.030 E/AndroidRuntime( 9878): 	at com.android.camera.app.CameraController.getCharacteristics(CameraController.java:112)"
    #     "11-22 19:32:36.239 1903-1903/com.asr.note E/AndroidRuntime: FATAL EXCEPTION: main"
    # group1 = ": "前的内容
    # group2 = ": "之后的内容
    PAT_ANDROID_RUNTIME = re.compile(r"^(.*?AndroidRuntime(?:\([\d\s]+\))?: )(.*)$")

    def __init__(self, logfp, start_line):
        self.logfp = logfp
        self.start_line = start_line
        self.result = JavaCrash()

        self.has_caused_by = False

    def parse(self):
        try:
            # self.result.location_in_log = LLocation(self.logfp.name, self.logfp.line_num)
            self.result.base_info.location_in_log = LLocation(self.logfp.name, self.logfp.line_num)

            # get time
            m = re.match(self.PAT_TIME, self.start_line)
            if m:
                # self.result.occurred_time = Time(m.group(1))
                self.result.base_info.occurred_time = Time(m.group(1))
            else:
                echo("occurred time is None")

            # get length of time + (pid) + tag
            header_len = 0
            m = re.match(self.PAT_ANDROID_RUNTIME, self.start_line)
            if m:
                header_len = len(m.group(1))
                #echo("header_len = {0}".format(header_len))

            line = "#"

            while line:
                # TODO
                line = self.logfp.readline().decode("utf-8")

                # 去除time + (pid) + tag, 保留其中的有用内容
                line = line[header_len:]
                #print line

                package_matcher = re.match(self.PAT_NAME_PACKAGE, line)
                if package_matcher:
                    self.result.name_package = package_matcher.group(1)
                    # self.result.p_t_id = package_matcher.group(2)
                    self.result.base_info.p_t_id = package_matcher.group(2)
                    self.result.stack_trace.append(line)
                    continue

                reason_matcher = re.match(self.PAT_REASON, line)
                if reason_matcher:
                    self.result.reason = reason_matcher.group()
                    self.result.stack_trace.append(line)
                    continue

                caused_matcher = re.match(self.PAT_CAUSED_BY, line)
                if caused_matcher:
                    self.has_caused_by = True
                    continue

                at_line_matcher = re.match(self.PAT_AT_FILE_LINE, line)
                if at_line_matcher:
                    self.result.stack_trace.append(line)

                    if self.has_caused_by:
                        self.has_caused_by = False
                        self.result.location_in_src = []

                    # 即使此时length已到src_length， 但包含包名的at句也要被添加
                    if re.search(self.result.name_package, line)\
                            and len(self.result.location_in_src) >= self.result.src_length:
                        sl = SLocation(at_line_matcher.group(1), at_line_matcher.group(2), True)
                        self.result.location_in_src.append(sl)

                    if len(self.result.location_in_src) < self.result.src_length:
                        in_this = False
                        if re.search(self.result.name_package, line):
                            in_this = True
                        sl = SLocation(at_line_matcher.group(1), at_line_matcher.group(2), in_this=in_this)
                        self.result.location_in_src.append(sl)

                    continue

                if not package_matcher and not reason_matcher and not caused_matcher and not at_line_matcher:
                    # TODO
                    self.logfp.rollbackline(-(len(line) + header_len))
                    break
        except Exception as e:
            echo("@@@@@@@@@@@ has Exception : " + e.message)
        finally:
            self.result.base_info_set.append(self.result.base_info)
            return self.result

def echo(s):
    TAG = "JavaCrashParser: "
    print TAG + s