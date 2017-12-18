#-*- coding=utf-8 -*-
import time
import tool.tools as tool


class Task(object):

    __LOAD_UNIT__ = 100 #(MB)

    __STATE_NEW__=0
    __STATE_WAITING__=1
    __STATE_PROCESSING__=2
    __STATE_GENERATING__=3
    __STATE_DONE__=4

    def __init__(self, name, state, log_path, src_path, create_time='', finish_seconds=0):
        self.state=state

        # t = time.localtime(time.time())
        # self.create_time = time.strftime("%d-%b-%Y   %I:%M:%S", t)

        self.name = name
        self.log_path = log_path
        self.src_path = src_path
        self.create_time = create_time
        self.finish_seconds = finish_seconds

        self.load = None

    def __eq__(self, other):
        if not other or type(other) is not Task:
            return False
        if self.name == '' and other.name == '':
            return False
        return self.name == other.name

    def getLoad(self):
        if not self.load:
            # TODO 1 需要去除文件夹中不需要解析的文件，再求合
            # TODO 2 self.load = min(load_cal, files_count)
            file_list = tool.getParseableFileList(self.log_path)
            self.load = tool.getFilesSizeMB(file_list) / Task.__LOAD_UNIT__ + 1
            self.load = min(self.load, len(file_list))
        return self.load


if __name__=="__main__":
    a = time.time()
    task = Task("hah", Task.__STATE_NEW__, "/home/qinsw/pengtian/tmp/cmcc_monkey/", '')
    task.getLoad()

    print  time.time() -a
    a = time.time()
    print task.getLoad()
    print time.time() -a
