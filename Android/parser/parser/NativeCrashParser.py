# coding=utf-8
import re

class NativeCrashParser(object):

    __ENTRY__ = "Fatal signal"

    # "Fatal signal 11 (SIGSEGV), code 1, fault addr 0x28 in tid 671 (Binder:659_2)"
    # signal error
    # group1 = signal error
    # group2 = tid
    # group3 = name
    PAT_ERROR_TID_NAME = r"^[^(]+\(([^)]+)\)(?:.*tid )([\d]+) \(([^)]+)\)"

    # "Build fingerprint: 'ASR/aquila_evbcmcc/aquila_evb:8.0.0/OPR5.170623.007/adroid80004.1747_r2:userdebug/dev-keys'"
    # build fingerprint:
    # group1 = 'ASR/aquila_evbcmcc/aquila_evb:8.0.0/OPR5.170623.007/adroid80004.1747_r2:userdebug/dev-keys'
    PAT_FINGERPRINT = r"^Build fingerprint: (.*)$"

    # Revision
    # group1 = Revision: = '0'
    PAT_REVISION = r"^Revision: (.*)$"

    # ABI:
    # group1 = ABI: = 'arm64'
    PAT_ABI = r"^ABI: (.*)$"

    # pid, tid, name, package
    # group1 = pid
    # group2 = tid
    # group3 = name
    # group4 = package
    # "pid: 809, tid: 809, name: ndroid.systemui  >>> com.android.systemui <<<"
    PAT_IDENTITY = (r"^pid: (\d+), tid: (\d+), name: (.+)? >>> (\S+) <<<$")

    # Abort Message
    # group1 = abort message
    # "Abort message: 'sp<> assignment detected data race'"
    PAT_ABORT_MESSAGE = r"^Abort message: (.*?)$"

    # pattern addr
    # "    x0   0000007270fd4000  x1   0000000000000000  x2   0000000000000190  x3   0000007270fd4000"
    PAT_ADDR = r"^ {4}(\S+?\s+?[0-9a-f]+\s+?){2}"

    # pattern trace
    # "    #00 pc 000000000001c93c  /system/lib64/libc.so (memset+140)"
    PAT_TRACE = r"^ {4}#\d+?\s+?\S+?\s+?[0-9a-f]+\s+?.*$"

    # FORTIFY: vsprintf: prevented 132-byte write into 128-byte buffer
    # group1 = vsprintf: prevented 132-byte write into 128-byte buffer
    # "FORTIFY: vsprintf: prevented 132-byte write into 128-byte buffer"
    PAT_FORTIFY = r"^FORTIFY: (.*)$"

    def __init__(self, logfp):
        self.logfp = logfp

    def parse(self):
        pass