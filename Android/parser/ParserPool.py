# coding=utf-8
import multiprocessing

from parser.parser.Parser import *


class ParserPool(object):
    '''
        Single Instance
    '''

    _instance = None
    _pool = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ParserPool, cls).__new__(cls, *args, **kwargs)
            cls._pool = multiprocessing.Pool(processes=50)
        return cls._instance

    def __del__(self):
        self._pool.close()

    def execute(self, callback, cfg='', log='', *modules):
        return self._pool.apply_async(proxy, (self, cfg, log, modules), callback=callback)

    def __run__(self, cfg, log, module):
        parser = Parser(cfg, log, module)
        result = parser.parse()
        result["result_path"]=log
        return result

    def close(self):
        return self._pool.close()


def proxy(cls_instance, cfg, log, modules):
    return cls_instance.__run__(cfg, log, modules)


_ParserPool = ParserPool()


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