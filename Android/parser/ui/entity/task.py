#-*- coding=utf-8 -*-
import time

class Task(object):
    __STATE_NEW__=0
    __STATE_WAIT__=1
    __STATE_PROCESS__=2
    __STATE_DONE__=3

    def __init__(self,create_time='',log_path='',src_path=''):
        self.state=self.__STATE_NEW__

        # t = time.localtime(time.time())
        # self.create_time = time.strftime("%d-%b-%Y   %I:%M:%S", t)
        self.create_time = create_time
        self.log_path = log_path
        self.src_path = src_path
        self.finish_seconds=0

