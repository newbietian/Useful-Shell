# coding=utf-8
import multiprocessing
from parser.Parser import *
import tool.tools as tool
import os

class ParserManager(object):

    '''
        Single Instance
    '''

    _pool = None
    def __init__(self, parsers, file_path_list, modules=(), pg_callback=None):
        '''
        :param parsers: the number of the pool processes
        :param file_path_list: the log list this manager to parser
        :param modules: the modules we want to get. e.g Parser.__M_JAVA__
        :param pg_callback: the progress callback
        '''
        self._pool = multiprocessing.Pool(processes=parsers)
        self.pg_callback = pg_callback
        self.file_path_list = file_path_list
        self.modules = modules

        self._progress_dict_ = multiprocessing.Manager().dict()

        # init result structure
        self._result_ = multiprocessing.Manager().dict()
        for m in self.modules:
            self._result_[m] = []

    def execute(self):
        '''Do job entry'''
        print multiprocessing.current_process().pid
        for file_path in self.file_path_list:
            # start a process and do job
            self._pool.apply_async(proxy, (self, file_path, self.modules), callback=self.__callback)
        self._pool.close()

    def __run__(self, log_path, modules):
        """
        start a process and do job
        :param log_path: the log to parse
        :param modules: the modules we care
        :return: the parse result we get
        """
        print multiprocessing.current_process().pid
        tool.log("__start_one_parser", log_path)
        parser = Parser(log_path, modules)
        parser.set_progress_listener(self.__progressCallback__)
        return parser.parse()

    def __getstate__(self):
        '''
        'pool objects cannot be passed between processes or pickled'
         NotImplementedError: pool objects cannot be passed between processes or pickled
        '''
        self_dict = self.__dict__.copy()
        del self_dict['_pool']
        return self_dict

    # Run in different process
    def __progressCallback__(self, path, percent):
        # calculate current progress
        self._progress_dict_[path] = percent
        progress = float(sum(self._progress_dict_.values())) / len(self.file_path_list)

        # send progress to task manager
        if self.pg_callback: self.pg_callback(progress)

    # TODO 在这儿做外部去重
    # 此处是各进程调用回调返回参数处， 运行在主进程中
    def __callback(self, result):
        '''
        The result callback of parser
        :param result: from parser
        '''
        print "before:", self._result_
        for m in self.modules:
            if len(result[m]) > 0:
                self._result_[m]+=result[m]
        print "after:", self._result_

        print multiprocessing.current_process().pid
        progress = float(sum(self._progress_dict_.values())) / len(self.file_path_list)
        print "self._progress_ = ", progress
        if progress >= 1.0:
            print "Should remove duplicate result"
            print "Start thread to generate result"

def proxy(cls_instance, log, modules):
    return cls_instance.__run__(log, modules)


'''
    #_listeners={}
    # For UI
    def add_parser_listener(self, func, id):
        self._listeners[id] = func

    def remove_parser_listener(self, id):
        del self._listeners[id]

    def print_listeners(self):
        for key in self._listeners:
            print key, " => ", self._listeners[key]
'''