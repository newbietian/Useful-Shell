#-*- coding=utf-8 -*-
import time
import tool.tools as tool


class Task(object):

    __LOAD_UNIT__ = 100 #(MB)

    __STATE_BASE__ = 0
    __STATE_WAITING__= __STATE_BASE__ + 0
    __STATE_PROCESSING__ = __STATE_BASE__ + 1
    __STATE_PAUSED__ = __STATE_BASE__ + 2
    __STATE_GENERATING__ = __STATE_BASE__ + 3
    __STATE_DONE__= __STATE_BASE__ + 4


    def __init__(self, log_path, src_path, state=__STATE_WAITING__, create_time='', finish_seconds=0):
        self.state=state

        # t = time.localtime(time.time())
        # self.create_time = time.strftime("%d-%b-%Y   %I:%M:%S", t)

        self.log_path = log_path
        self.src_path = src_path
        self.create_time = create_time
        self.finish_seconds = finish_seconds

        self.load = None
        self.files = None


    def __eq__(self, other):
        if not other or type(other) is not Task:
            return False
        if self.log_path == '' and other.log_path == '':
            return False
        return self.log_path == self.log_path
        #if self.name == '' and other.name == '':
        #    return False
        #return self.name == other.name


    #TODO
    def __cmp__(self, other):
        return 1

    def getLoad(self):
        #return 10
        if not self.load:
            # TODO 1 需要去除文件夹中不需要解析的文件，再求合
            # TODO 2 self.load = min(load_cal, files_count)
            self.files = file_list = tool.getParseableFileList(self.log_path)
            self.load = tool.getFilesSizeMB(file_list) / Task.__LOAD_UNIT__ + 1
            self.load = min(self.load, len(file_list))
        return self.load


if __name__=="__main__":
    a = time.time()
    task = Task("hah", Task.__STATE_WAITING__, "/home/qinsw/pengtian/tmp/cmcc_monkey/", '')
    task.getLoad()

    print  time.time() -a
    a = time.time()
    print task.getLoad()
    print time.time() -a
