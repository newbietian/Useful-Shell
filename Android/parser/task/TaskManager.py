# coding=utf-8
import threading
import time
import tool.tools as tool
from task import Task
from parser.ParserManager import ParserManager
from ui.presenter import dbPresenter

class TaskQueue(object):
    def __init__(self):
        self._queue = []

    def put(self, t):
        self._queue.insert(0, t)

    def getHeaderLoad(self):
        return self._queue[len(self._queue)-1].getLoad()

    def get(self):
        return self._queue.pop(len(self._queue)-1)

    def size(self):
        return len(self._queue)

class ProcessingTaskQueue(TaskQueue):
    def __init__(self):
        super(ProcessingTaskQueue, self).__init__()

    def getLoadSum(self):
        load_sum = 0
        for t in self._queue:
            load_sum+=t.getLoad()
        tool.log("loadsum", "load_sum = %d" % load_sum)
        return load_sum

    def put(self, t):
        if type(t) is Task:
            t.state = Task.__STATE_PROCESSING__
        super(ProcessingTaskQueue, self).put(t)

        # 数据库操作，更新task的状态 => Processing
        dbPresenter.UpdateTaskState(t.log_path, Task.__STATE_PROCESSING__)


    def remove(self, t):
        if t in self._queue:
            self._queue.remove(t)

    def removeById(self, id):
        for t in self._queue:
            if t.name == id:
                self._queue.remove(t)
                return

class WaitingTaskQueue(TaskQueue):
    def __init__(self):
        super(WaitingTaskQueue, self).__init__()

    def put(self, t):
        p=False
        if type(t) is Task and t.state != Task.__STATE_WAITING__:
            t.state = Task.__STATE_WAITING__
            # 数据库操作，更新task的状态 => Waiting
            p = dbPresenter.UpdateTaskState(t.log_path, Task.__STATE_WAITING__)
        super(WaitingTaskQueue, self).put(t)
        return p

#-------------------------------------------------------------------------------
class TaskListener(object):
    '''
        The task state and progress changed listener
        Called By ParserManager
        Realized By Presenter
    '''
    def onTaskProgressChanged(self, task, progress):
        '''
        The callback called when task progress changed
        :param task: target task for identity
        :param progress: the progress of target task
        '''

    def onTaskStateChanged(self, task):
        '''
        The callback called when task state changed
        :param task: the target task
        '''
#-------------------------------------------------------------------------------

class TaskManager(object):

    # 1、当processing queue中没有任务，来任务直接加入其中
    # 2、当processing queue中有任务，判断从waiting queue中取出的task的load和 processing queue中所有task的load和是否大于MAX，
    #    如果是，则waiting
    #    如果否， 则进入processing queue
    # 3、当从ParserManager收到对应Task完成的反馈， 则在processing queue中移除此task

    #TODO 可以从配置文件中获取
    _MAX_PROCESSING_ = 50

    instance=None
    _waitingQueue = None
    _processingQueue = None
    _task_handler = None
    _running = False

    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super(TaskManager, cls).__new__(cls, *args, **kwargs)
            cls._waitingQueue = WaitingTaskQueue()
            cls._processingQueue = ProcessingTaskQueue()
            cls._running = True
            cls._task_handler = None
        return cls.instance

    # public
    def start(self):
        if not self._task_handler:
            self._task_handler = threading.Thread(target=self._handle_tasks)
            self._task_handler.start()

    def addTask(self, task):
        self._waitingQueue.put(task)

    #def onTaskDone(self, id):
    #    self._processingQueue.removeById(id=id)

    def close(self):
        self._running = False
        self._waitingQueue = None
        self._processingQueue = None
        self._task_handler = None
        self.instance = None

    def setTaskListener(self, listener):
        self._task_listener = listener

    # private

    def _handle_tasks(self):
        tool.log("_handle_tasks", "start")
        while self._running:
            # A 0.5 second loop
            time.sleep(0.5)

            if not self._waitingQueue.size() > 0:
                continue

            # calculate current work num
            if self._processingQueue.size() > 0:
                current_load = self._processingQueue.getLoadSum()
                future_load = self._waitingQueue.getHeaderLoad()
                if current_load + future_load <= TaskManager._MAX_PROCESSING_:
                    # put the task to _processingQueue
                    task = self._waitingQueue.get()
                    self._processingQueue.put(task)

                    # 启动进程池执行任务
                    pm = ParserManager(task)
                    if self._task_listener:
                        pm.setTaskListener(self._task_listener)
                    pm.execute()
                    tool.log("start ParserManager 1")
                else:
                    tool.log("_handle_task", "please hold on")
            else:
                task = self._waitingQueue.get()
                task.getLoad()
                self._processingQueue.put(task)

                self._task_listener.onTaskStateChanged(task)

                # 启动进程池执行任务
                pm = ParserManager(task)
                if self._task_listener:
                    pm.setTaskListener(self._task_listener)
                tool.log("ParserManager", "tagggggggggggggggg")
                pm.execute()



