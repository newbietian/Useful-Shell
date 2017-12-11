# coding=utf-8
import re
from parser.tool import const

# const.TEST1 = "Build fingerprint: 'ASR/aquila_evbcmcc/aquila_evb:8.0.0/OPR5.170623.007/adroid80004.1747_r2:userdebug/dev-keys'"
# pattern = re.compile(r"^Build fingerprint: '(.*)'$")
# match = pattern.match(const.TEST1)
#
# if match:
#     group = match.group(1)
#     print group
# else:
#     print "no match"
#     print const.TEST1

# m = re.match(r'(?P<sign>.*) (\w+)', 'hello world!')
#
# print "m.group(1,2):", m.group(1,2)
# print "m.groupdict:", m.groupdict()

# --------------------------------------------------------------------------------------------------------------------
# JAVA_CRASH

# reason
# 全 group1 = "java.lang.RuntimeException: Unable to start activity ComponentInfo{com.android.simsettings/com.android.simsettings.SimPreferenceDialog}"
# group2 = "java.lang.RuntimeException"
# group3 = "Unable to start activity ComponentInfo{com.android.simsettings/com.android.simsettings.SimPreferenceDialog}"
# 如果存在, 如果不存在，则456为None
# 全 group4 = "java.lang.NullPointerException: Attempt to invoke virtual method 'java.lang.CharSequence android.telephony.SubscriptionInfo.getDisplayName()' on a null object reference"
# group5 = "java.lang.NullPointerException"
# group6 = "Attempt to invoke virtual method 'java.lang.CharSequence android.telephony.SubscriptionInfo.getDisplayName()' on a null object reference"
a = "java.lang.RuntimeException: Unable to start activity ComponentInfo{com.android.simsettings/com.android.simsettings.SimPreferenceDialog}"\
     ": java.lang.NullPointerException: Attempt to invoke virtual method 'java.lang.CharSequence android.telephony.SubscriptionInfo.getDisplayName()' on a null object reference"
pattern = re.compile(r"^(([^\s:]+): ([^:]+))(?:: (([^\s]+): (.*)))?")


# package, pid => group 1,2
# group1 = package
# group2 = pid
a = "Process: com.android.phone, PID: 31866"
pattern = re.compile(r"^Process: ([^,]+), PID: ([\d]+)")

# at 用来判断 if match: then do
a = "	at android.app.ActivityThread.performLaunchActivity(ActivityThread.java:2817)"
pattern = re.compile(r"^\tat .+$")

# # 用来判断at开头，并获取文件和行号
# file and line number => group 1,2
# group1 = filename
# group2 = number
a = "	at android.app.ActivityThread.performLaunchActivity(ActivityThread.java:2817)"
# a = "	at java.lang.reflect.Method.invoke(Native Method)"
# pattern = re.compile(r"^\tat [^(]+\(([^:]+):([\d]+)\).*$")
pattern = re.compile(r"^\tat [^(]+\(([^: ]+?)(?:[: ])([\d]+|[\S]+)\).*$")

# p = "android.app.ActivityThread"
# m = re.search(p, a)
# if m:
#     print m.group()

m = pattern.match(a)
if m:
    # print "matched"
    group = m.group(2)
    if re.match(r"\d+", group):
        print group

# caused by
# group1 = reason2
a = "Caused by: java.util.MissingFormatArgumentException: Format specifier '%H'\n"
pattern = re.compile(r"^Caused by: (.*$)")

# --------------------------------------------------------------------------------------------------------------------
# Native Crash

# signal error
# group1 = signal error
# group2 = tid
# group3 = name
a = "Fatal signal 11 (SIGSEGV), code 1, fault addr 0x28 in tid 671 (Binder:659_2)"
pattern = re.compile(r"^[^(]+\(([^)]+)\)(?:.*tid )([\d]+) \(([^)]+)\)")

# build fingerprint:
# group1 = 'ASR/aquila_evbcmcc/aquila_evb:8.0.0/OPR5.170623.007/adroid80004.1747_r2:userdebug/dev-keys'
a = "Build fingerprint: 'ASR/aquila_evbcmcc/aquila_evb:8.0.0/OPR5.170623.007/adroid80004.1747_r2:userdebug/dev-keys'"
pattern = re.compile(r"^Build fingerprint: (.*)$")

# Revision
# group1 = Revision: = '0'
a = "Revision: '0'"
pattern = re.compile(r"^Revision: (.*)$")

# ABI:
# group1 = ABI: = 'arm64'
a = "ABI: 'arm64'"
pattern = re.compile(r"^ABI: (.*)$")

# pid, tid, name, package
# group1 = pid
# group2 = tid
# group3 = name
# group4 = package

a = "pid: 809, tid: 809, name: ndroid.systemui  >>> com.android.systemui <<<"
pattern = re.compile(r"^pid: (\d+), tid: (\d+), name: (.+)? >>> (\S+) <<<$")

# Abort Message
# group1 = abort message
a = "Abort message: 'sp<> assignment detected data race'"
pattern = re.compile(r"^Abort message: (.*?)$")

# pattern addr
a = "    x0   0000007270fd4000  x1   0000000000000000  x2   0000000000000190  x3   0000007270fd4000"
# pattern = re.compile(r"^ {4}(?:(?:\S+?)(?:\s+?)(?:[0-9a-f]+)(?:\s+?)){2}")
pattern = re.compile(r"^ {4}(\S+?\s+?[0-9a-f]+\s+?){2}")


# pattern trace
a = "    #00 pc 000000000001c93c  /system/lib64/libc.so (memset+140)"
a = "    #13 pc 000000000009eb4c  /system/lib64/libhwui.so (_ZN7android10uirenderer12TextureCache3getEPNS_6BitmapE+20)"
pattern = re.compile(r"^ {4}#\d+?\s+?\S+?\s+?[0-9a-f]+\s+?.*$")

# FORTIFY: vsprintf: prevented 132-byte write into 128-byte buffer
# group1 = vsprintf: prevented 132-byte write into 128-byte buffer
a = "FORTIFY: vsprintf: prevented 132-byte write into 128-byte buffer"
pattern = re.compile(r"^FORTIFY: (.*)$")

# --------------------------------------------------------------------------------------------------------------------
# ANR

# --------------------------------------------------------------------------------------------------------------------
# time
# group1 = time
# group2 = mon
# group3 = day
# group4 = h
# group5 = m
# group6 = h
# group7 = u
# "05-10 02:06:16.628 I/NetworkIdentity( 2603): buildNetworkIdentity:"
a =  "05-10 02:06:16.123 I/NetworkIdentity( 2603): buildNetworkIdentity:"
a = "08-18 16:52:54.902  5672  5672"
# pattern = re.compile(r"^((\d\d)-(\d\d)\s(\d\d):(\d\d):(\d\d)\.(\d\d\d))")

from parser.crash.crash import *
m = re.match(r"^((\d\d)-(\d\d)\s(\d\d):(\d\d):(\d\d)\.(\d\d\d))", a)
if m:
    # print "matched"

    t = Time(int(m.group(2)), int(m.group(3)), int(m.group(4)),
                                     int(m.group(5)), int(m.group(6)), int(m.group(7)), m.group(1))
    print t


# from parser.crash.crash import *

# l = NativeCrash()
# l.name_package = "adad"
# l.reason = "adada"
# l.p_t_id = 1
#
# l.location_in_log = LLocation("log_file_path", "found_line")
# # l.occurred_time = Time(02, 11, 1, 2, 3, 4, "02-11 01:02:03.004")
# l.stack_trace.append("adadad")
# l.error_signal = "SIGBV"
# print l

# a = "08-18 16:52:54.902  5672  5672 E AndroidRuntime: 	at android.app.FragmentManagerImpl.moveToState(FragmentManager.java:1148)"
# #a = "11-21 23:02:48.030 E/AndroidRuntime( 9878): 	at com.android.camera.app.CameraController.getCharacteristics(CameraController.java:112)"
# #a = "11-22 19:32:36.239 1903-1903/com.asr.note E/AndroidRuntime: FATAL EXCEPTION: main"
#
# pattern = re.compile(r"^(.*?AndroidRuntime(?:\([\d\s]+\))?: )(.*)$")

# m = pattern.match(a)
# lennn=0
# if m:
#     # print "matched"
#     group = m.group(1)
#     print group, len(group)
#     lennn = len(group)
#     group = m.group(2)
#     print group
#
# print a[lennn:]

# def _cut_line_left(flag, l):
#     try:
#         first_colon_index = l.index(flag)
#         print "first_colon_index = %d" % first_colon_index
#
#         l = l[first_colon_index + len(flag):]
#         print l
#         return l
#     except Exception as e:
#         print "Exception = ", e.message
#         return l.lstrip()
#
# _cut_line_left(": ","FATAL EXCEPTION: main")