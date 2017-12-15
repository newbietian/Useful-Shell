#-*- coding=utf-8 -*-
import os
import sys
import wx
import time
import re

__DB_NAME__ = "app.db"
__CONFIG_NAME__ = "app.cfg"

__APP_DATA = ".android-log-analysis-tool"

def getHomePath():
    if os.environ['HOME']:
        return os.environ['HOME']
    if os.path.expandvars('$HOME'):
        return os.path.expandvars('$HOME')
    if os.path.expanduser('~'):
        return os.path.expanduser('~')

def getAppDataPath():
    home_path = getHomePath()
    if not home_path.endswith("/"):
        home_path += "/"
    app_path = home_path + __APP_DATA
    if not checkDirExists(app_path):
        os.mkdir(app_path)
    return app_path

def checkFileExists(path):
    return os.path.isfile(path)

def checkDirExists(path):
    return os.path.isdir(path)

def getFileSize(path):
    if not checkFileExists(path):
        log("checkFileExists", "File {} is not exist!".format(path))
        return 0
    return os.path.getsize(path)

def getDirSize(path):
    count = 0
    file_count = 0
    for root, sub_dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            count+=getFileSize(file_path)
            file_count+=1
    return count, file_count

def str2msecs(time_str):
    """ 将字符串的时间转化为ms """
    m = re.match(Time.__PATTERN__, time_str)
    if not m:
        log("str2secs", "not match 1")
        return 0

    tmlist = re.split(r'[\D]', time_str)
    uu = 0
    if len(tmlist[len(tmlist) - 1]) == 3:
        uu = tmlist[len(tmlist) - 1]
        tmlist.pop(len(tmlist) - 1)
        uul = [uu[0], uu[1], uu[2]]
        tmlist += uul
    else:
        tmlist += [0, 0, 0]
    if len(tmlist) != 9:
        al = [0 * x for x in range(9 - len(tmlist))]
        tmlist = al + tmlist
    # turn string list to integer list
    # print tmlist
    tmlist = map(int, tmlist)
    if len(tmlist) != 9:
        log("str2secs", "not match 2")
        return 0
    return int(time.mktime(tmlist)) * 1000 + int(uu)

# TODO
def getParseableFileList(path):
    list=[]
    for root, sub_dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            list.append(file_path)
    return list


def log(tag, message=''):
    def_tag = 'APP'
    if message == '':
        message = tag
        tag = def_tag
    print str(tag),":",str(message)


class Preference(object):
    '''Single instance class for save Preference'''
    __instance=None

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls._instance = super(Preference, cls).__new__(cls, *args, **kwargs)
            cfg=getAppDataPath()+"/"+__CONFIG_NAME__
            if not checkFileExists(cfg):
                log("checkFileExists false")
                os.mknod(cfg)
        return cls.__instance

    def set(self, key, value):
        pass

    def get(self, key):
        pass


class Time(object):
    __PATTERN__=r'(?:(\d{4})[^\w\s])?(?:(\d{2})[^\w\s])?(?:(\d{2}) )?(\d{2}):(\d{2}):(\d{2})(?:\.(\d{3}))?'
    class TimeFormatError(Exception):pass

    def __init__(self, t_str):
        if re.match(Time.__PATTERN__, t_str):
            self.time = t_str

    def __cmp__(self, other):
        if not other or type(other) is not Time:
            print "TIME: is_older_than: error, other is not Type Time"
            return super(Time, self).__cmp__(other)
        return cmp(str2msecs(self.time), str2msecs(other.time))

    def __str__(self):
        return self.time


if __name__ == "__main__":
    log("hello is %d" % 1)
    log("hello {} my friends".format("pengtian"))
    log(getAppDataPath())
    log(getHomePath())
    log(checkDirExists(getHomePath()))
    log(checkFileExists(getAppDataPath()+"/app.db"))
    Preference()
    getFileSize("")
    a = time.time()
    print str2msecs("12-12 13:51:13.413")
    print time.time()-a