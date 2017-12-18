# coding=utf-8
from task import Task
import Queue
import threading
from parser import ParserManager

class TaskQueue(object):
    def __init__(self):
        self._queue = []

    def put(self, t):
        self._queue.insert(0, t)

    def getHeader(self):
        return self._queue[len(self._queue)-1]

    def get(self):
        return self._queue.pop(len(self._queue)-1)

    def size(self):
        return len(self._queue)

class ProcessingTaskQueue(TaskQueue):
    def __init__(self):
        super(ProcessingTaskQueue, self).__init__()

    def loadSum(self):
        load_sum = 0
        for t in self._queue:
            load_sum+=t
        return load_sum

    def put(self, t):
        if type(t) is Task:
            t.state = Task.__STATE_PROCESSING__
        super(ProcessingTaskQueue, self).put(t)

        # TODO 数据库操作，更新task的状态 => Processing
        # TODO 启动线程池执行任务
        pm = ParserManager(t, )

class WaitingTaskQueue(TaskQueue):
    def __init__(self):
        super(WaitingTaskQueue, self).__init__()

    def put(self, t):
        if type(t) is Task:
            t.state = Task.__STATE_WAITING__
        super(WaitingTaskQueue, self).put(t)

        #TODO 数据库操作，更新task的状态 => Waiting


class TaskManager(object):

    # 1、当processing queue中没有任务，来任务直接加入其中
    # 2、当processing queue中有任务，判断从waiting queue中取出的task的load和 processing queue中所有task的load和是否大于MAX，
    #    如果是，则waiting
    #    如果否， 则进入processing queue
    # 3、当从ParserManager收到对应Task完成的反馈， 则在processing queue中移除此task
    _MAX_PROCESSING = 50

    instance=None
    _waitingQueue = None
    _processingQueue = None
    _task_handler = None
    _running = False

    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super(TaskManager, cls).__new__(cls, *args, **kwargs)
            cls._waitingQueue = ProcessingTaskQueue()
            cls._processingQueue = WaitingTaskQueue()
            # TODO
            cls._task_handler = threading.Thread(target=cls._handle_tasks)
            cls._task_handler.start()
            cls._running = True
        return cls.instance

    def addTask(self, task):
        self._waitingQueue.put(task)

    def _handle_tasks(self):
        while self._running:
            # calculate current work num
            if self._processingQueue.size() > 0:
                pass
            else:
                task = self._waitingQueue.get()
                self._processingQueue.put(task)



