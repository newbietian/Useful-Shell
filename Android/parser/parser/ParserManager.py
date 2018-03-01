# coding=utf-8
import multiprocessing
import threading
import threadpool
import os
import re

from Queue import Queue

from parser.Parser import *
from parser.Parser import __M_ANR__, __M_JAVA__, __M_NATIVE__
import tool.tools as tool
from task.task import Task


class NullError(Exception):
    """空指针错误"""

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class ParserManager(object):

    """ ParserManager通过多线程来实现任务的后台执行。
        PS： 以前是多进程，但和ui交互困难~， 多进程的未完成实现见old/ParserManager_Process.py
    """

    def __init__(self, task):
        """ 构造方法
            :param task: 包含此解析任务的信息
        """
        if not task or not len(task.files) > 0:
            raise NullError("Illegl task argument.")
        self.task = task
        # 表明处理状态， True正在处理， False完成处理或其他情况
        self.running = True

        # 用于线程间通信以反馈解析进度的通信队列
        self.com_queue = Queue(maxsize=task.getLoad())

        # 接收通信队列发来消息的线程
        self.com_thread = threading.Thread(target=self.__receiver, args=(self.com_queue,))
        self.com_thread.setDaemon(True)
        self.com_thread.start()

        # 用来最后生成报告的线程
        self.gen_thread = None

        # 根据当前任务量创建线程池
        self.pool = threadpool.ThreadPool(task.getLoad())

        self.file_path_list = task.files
        self.src_path = task.src_path
        self.modules = (__M_JAVA__, __M_NATIVE__, __M_ANR__)

        # init result structure
        self._result_ = multiprocessing.Manager().dict()
        for m in self.modules:
            self._result_[m] = []

        self.task_listener = None

    def setTaskListener(self, tl):
        self.task_listener = tl

    def execute(self):
        '''Do job entry'''
        print multiprocessing.current_process().pid
        for file_path in self.file_path_list:
            # start a process and do job
            print file_path
            self._pool.apply_async(proxy, (self, file_path, self.modules), callback=self.__callback)
        self._pool.close()

    def __run__(self, log_path, modules):
        """
        start a process and do job
        :param log_path: the log to parse
        :param modules: the modules we care
        :return: the parse result we get
        """
        #print multiprocessing.current_process().pid
        tool.log("__start_one_parser", log_path)
        parser = Parser(log_path, modules)
        parser.set_pipe_sender(self.wpipe)
        return parser.parse()

    def __getstate__(self):
        """
        'pool objects cannot be passed between processes or pickled'
         NotImplementedError: pool objects cannot be passed between processes or pickled
        """
        self_dict = self.__dict__.copy()
        # del self_dict['_pool']
        # del self_dict['recvThread']
        return self_dict

    def __receiver(self, com_queue):

        """ 接收工作线程通过queue发送过来的每个文件解析的进度
        :param com_queue: 通信队列
        """

        tool.log("start __receiver")

        if not com_queue:
            raise NullError("com_queue can't be Null")

        while self.running:
            data = com_queue.get()

            print data

            continue

            # get path and percent from data like "path: /home/path/xxx, percent: 0.1341"
            m = re.match(r"^path: (/.+), percent: ([01]\.\d+)?$", data)
            if m:
                path = m.group(1)
                percent = float(m.group(2))
                #print "pid = %d" % multiprocessing.current_process().pid, "path = %s" % path, percent
            else:
                # TODO 由于没有同步机制， 会出现还没写入完成就被读走的情况，仅作为一种大概的反馈
                # __receiver.error : not formatted data : -30 (copy).log, percent: 0.209564000682
                tool.log("__receiver.error", "not formatted data : %s" % data)
                continue

            # calculate current progress
            self._progress_dict_[path] = percent
            # float
            progress = float(sum(self._progress_dict_.values())) / len(self.file_path_list)
            # int
            progress = int(progress * 100)
            print progress

            # send progress to task manager
            if self.task_listener: self.task_listener.onTaskProgressChanged(self.task, progress)

    # TODO 在这儿做外部去重
    # 此处是各进程调用回调返回参数处， 运行在主UI进程中
    def __callback(self, result):
        '''
        The result callback of parser
        :param result: from parser
        '''

        print "pri finished222", self._file_finished_.value
        self._file_finished_.value = self._file_finished_.value + 1
        print "all", len(self.file_path_list)
        print "finished", self._file_finished_.value

        #print "before:", self._result_
        # TODO 将各个进程的结果汇总
        try:
            for m in self.modules:
                if len(result[m]) > 0:
                    self._result_[m]+=result[m]
        except Exception as e:
            print "exception in callback = ", e.message
        #print
        #print "after:", self._result_

        # TODO 去重

        #print multiprocessing.current_process().pid
        #progress = float(sum(self._progress_dict_.values())) / len(self.file_path_list)
        #print "self._progress_ = ", progress
        #if progress >= 1.0:
        print "self._file_finished_.value",self._file_finished_.value
        if self._file_finished_.value == len(self.file_path_list):
            print "Should remove duplicate result"
            print "Start thread to generate result"
            # callback
            self.task.state = Task.__STATE_GENERATING__
            if self.task_listener:
                self.task_listener.onTaskStateChanged(self.task)

            self.gen_thread = threading.Thread(target=self.__start_generator, args=(self._result_,))
            self.gen_thread.start()

    def __start_generator(self, result):
        '''
        The target method for generator thread
        :param result: the result we get after analysis
        '''
        # send the callback state
        print result

def proxy(cls_instance, log, modules):
    return cls_instance.__run__(log, modules)