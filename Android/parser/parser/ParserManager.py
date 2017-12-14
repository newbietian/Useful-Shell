# coding=utf-8
import multiprocessing
from parser.Parser import *
import tool.tools as tool
import os

class ParserManager(object):
    '''
        Single Instance
    '''

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

        self._pg_dict = multiprocessing.Manager().dict()
        self._final_result = multiprocessing.Manager().dict()
        self._file_count = len(self.file_path_list)

    def __del__(self):
        self._pool.close()

    def execute(self):
        '''Do job entry'''
        for file_path in self.file_path_list:
            # start a process and do job
            self._pool.apply_async(proxy, (self, file_path, self.modules), callback=self.__callback)

    def __run__(self, log_path, module):
        """
        start a process and do job
        :param log_path: the log to parse
        :param module: the modules we care
        :return: the parse result we get
        """
        tool.log("__start_one_parser", log_path)
        parser = Parser(log_path, module)
        result = parser.parse()
        result["result_path"]=log_path
        return result

    def __progressCallback(self, path, pg_dict, percent):
        # calculate current progress
        pg_dict[path] = percent
        sum_values = sum(pg_dict.values())
        sum_percent = float(sum_values) / self._file_count
        print "sum percent = ", sum_percent

        # send progress to task manager
        self.pg_callback(sum_percent)
        #if sum_percent >=  self._file_count:

    #TODO 在这儿做外部去重
    def __callback(self, result):
        ''''''
        print result

    def close(self):
        return self._pool.close()

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