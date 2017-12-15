# # coding=utf-8
# import multiprocessing
# import os
# import tool.tools as tool
#
# def execute(pool, callback, progressCB, dict, log=''):
#     return pool.apply_async(__run__, (log, progressCB, dict), callback=callback)
#
#
# def __run__(log,progressCB, dict):
#     f=open(log,'r')
#     line='#'
#     count = 0
#     totalsize= tool.getFileSize(log)
#     AD=0.1
#     while line:
#         line = f.readline().decode("utf-8")
#         count+=len(line)
#         percent = float(count) / totalsize
#         #TODO need a out way
#         if percent >= AD and percent < 1.0:
#             progressCB(log, dict, percent)
#             AD = AD + 0.09
#             #print "AD = %f" % AD
#     progressCB(log,dict,1.0)
#
#     return 0
#
# def callback(ret):
#     print ret
#
# #进程间共享数据
# m = multiprocessing.Manager()
# daaa=m.dict()
#
# FILE_COUNT=0
#
# def progressBarCallback(path, dict, percent):
#     global aaaaa, FILE_COUNT
#     #print "id = %s" % path, "percent = %f" % percent
#     dict[path]=percent
#     #print dict.values()
#     #os.system("clear")
#     suma = sum(dict.values())
#     # TODO send to task manager
#     print "sum percent = ", suma / FILE_COUNT
#
#     if suma >= FILE_COUNT:
#         print "MUTHER FUCKER"
#
# if __name__ == "__main__":
#     path = "/home/qinsw/pengtian/tmp/cmcc_monkey/asrlog-0037(1122)/asrlog-2017-11-21-17-06-29/1/android"
#     total, filecout = tool.getDirSize(path)
#     FILE_COUNT = filecout
#     pool = multiprocessing.Pool(processes=4)
#     for root, sub_dirs, files in os.walk(path):
#         for file in files:
#             file_path = os.path.join(root, file)
#             #print file_path
#             execute(pool, callback, progressBarCallback,daaa, log=file_path)
#
#     pool.close()
#     pool.join()


# coding=utf-8
import multiprocessing
import os
import tool.tools as tool

def execute(pool, callback, progressCB, log=''):
    return pool.apply_async(__run__, (log, progressCB), callback=callback)


def __run__(log,progressCB):
    f=open(log,'r')
    line='#'
    count = 0
    totalsize= tool.getFileSize(log)
    AD=0.1
    while line:
        line = f.readline().decode("utf-8")
        count+=len(line)
        percent = float(count) / totalsize
        #TODO need a out way
        if percent >= AD and percent < 1.0:
            progressCB(log, percent)
            AD = AD + 0.09
            #print "AD = %f" % AD
    progressCB(log,1.0)

    return 0

def callback(ret):
    print ret

#进程间共享数据
m = multiprocessing.Manager()
daaa=m.dict()

FILE_COUNT=0

def progressBarCallback(path, percent):
    global aaaaa, FILE_COUNT
    #print "id = %s" % path, "percent = %f" % percent
    daaa[path]=percent
    #print dict.values()
    #os.system("clear")
    suma = sum(daaa.values())
    # TODO send to task manager
    print "sum percent = ", suma / FILE_COUNT

    if suma >= FILE_COUNT:
        print "MUTHER FUCKER"

if __name__ == "__main__":
    path = "/home/qinsw/pengtian/tmp/cmcc_monkey/asrlog-0037(1122)/asrlog-2017-11-21-17-06-29/1/android"
    total, filecout = tool.getDirSize(path)
    FILE_COUNT = filecout
    pool = multiprocessing.Pool(processes=4)
    for root, sub_dirs, files in os.walk(path):
        for file in files:
            file_path = os.path.join(root, file)
            #print file_path
            execute(pool, callback, progressBarCallback, log=file_path)

    pool.close()
    pool.join()