#-*- coding=utf-8 -*-
import time

class Task(object):
    __STATE_NEW__=0
    __STATE_WAIT__=1
    __STATE_PROCESS__=2
    __STATE_DONE__=3

    def __init__(self, name, state, log_path, src_path, create_time='', finish_seconds=0):
        self.state=state

        # t = time.localtime(time.time())
        # self.create_time = time.strftime("%d-%b-%Y   %I:%M:%S", t)

        self.name = name
        self.log_path = log_path
        self.src_path = src_path
        self.create_time = create_time
        self.finish_seconds = finish_seconds

if __name__=="__main__":
    print Task.__dict__

