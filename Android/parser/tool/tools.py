#-*- coding=utf-8 -*-
import os
import sys
import wx
import time

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
    print tag,":",message

import re
def str2secs(time_str):
    """ 将字符串的时间转化为秒 """
    if not re.match(r'\d+-\d+-\d+ \d+:\d+:\d+', time_str):
        log("str2secs", "not match 1")
        return 0

    tmlist = re.split(r'[^\w]', time_str)
    tmlist+=[0,0,0]
    # turn string list to integer list
    tmlist = map(int, tmlist)
    if len(tmlist) !=9:
        log("str2secs", "not match 2")
        return 0
    return int(time.mktime(tmlist))

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


if __name__ == "__main__":
    log("hello is %d" % 1)
    log("hello {} my friends".format("pengtian"))
    log(getAppDataPath())
    log(getHomePath())
    log(checkDirExists(getHomePath()))
    log(checkFileExists(getAppDataPath()+"/app.db"))
    Preference()
    getFileSize("")