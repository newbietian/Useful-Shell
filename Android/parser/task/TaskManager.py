# coding=utf-8
import threading
import time
import tool.tools as tool
from task import Task
from parser.ParserManager import ParserManager
from ui.presenter import dbPresenter

LOG_TAG = "TaskManager"

class TaskQueue(object):
    """
    任务队列，基类
    """
    def __init__(self):
        self._queue = []

    def put(self, t):
        self._queue.insert(0, t)

    def get_header_load(self):
        return self._queue[len(self._queue)-1].getLoad()

    def get(self):
        return self._queue.pop(len(self._queue)-1)

    def size(self):
        return len(self._queue)


class ProcessingTaskQueue(TaskQueue):
    """
    正在处理任务队列
    """
    def __init__(self):
        super(ProcessingTaskQueue, self).__init__()

    def get_load_sum(self):
        """
        获取任务总量
        """
        load_sum = 0
        for t in self._queue:
            load_sum += t.getLoad()

        tool.log(LOG_TAG, "load_sum = %d" % load_sum)

        return load_sum

    def put(self, t):
        if type(t) is Task:
            t.state = Task.__STATE_PROCESSING__
        super(ProcessingTaskQueue, self).put(t)

        # 数据库操作，更新task的状态 => Processing
        # dbPresenter.UpdateTaskState(t.log_path, Task.__STATE_PROCESSING__)

    def remove(self, t):
        if t in self._queue:
            self._queue.remove(t)

    def remove_by_id(self, qid):
        for t in self._queue:
            if t.name == qid:
                self._queue.remove(t)
                return


class WaitingTaskQueue(TaskQueue):
    """
    正在等待任务队列
    """
    def __init__(self):
        super(WaitingTaskQueue, self).__init__()

    def put(self, t):
        p = False
        if type(t) is Task and t.state != Task.__STATE_WAITING__:
            t.state = Task.__STATE_WAITING__
            # 数据库操作，更新task的状态 => Waiting
            # p = dbPresenter.UpdateTaskState(t.log_path, Task.__STATE_WAITING__)
        super(WaitingTaskQueue, self).put(t)
        return p

# -------------------------------------------------------------------------------


class TaskListener(object):
    """
        The task state and progress changed listener
        Called By ParserManager
        Realized By Presenter
        Task 状态和进度监听
        由ParserManager调用，由Presenter实现
    """

    def on_task_progress_changed(self, task, progress):
        """
        The callback called when task progress changed
        :param task: target task for identity
        :param progress: the progress of target task
        """

    def on_task_state_changed(self, task):
        """
        The callback called when task state changed
        :param task: the target task
        """
# -------------------------------------------------------------------------------


class TaskManager(object):

    """
    单例模式：TaskManager， 用于统一管理和调度任务

    流程：
    1、当processing queue中没有任务，来任务直接加入其中
    2、当processing queue中有任务，判断从waiting queue中取出的task的load和 processing queue中所有task的load和是否大于MAX，
       如果是，则waiting
       如果否， 则进入processing queue
    3、当从ParserManager收到对应Task完成的反馈， 则在processing queue中移除此task
    """

    # TODO 可以从配置文件中获取
    # 代表着最多可同时开启50个线程处理任务。
    _MAX_PROCESSING_ = 50

    instance = None
    _waitingQueue = None
    _processingQueue = None
    _task_handler = None
    _running = False
    _task_listener = None

    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super(TaskManager, cls).__new__(cls, *args, **kwargs)
            cls._waitingQueue = WaitingTaskQueue()
            cls._processingQueue = ProcessingTaskQueue()
            cls._running = True
            cls._task_handler = None
            cls._task_listener = None
        return cls.instance

    # public
    def start(self):
        if not self._task_handler:
            self._task_handler = threading.Thread(target=self._handle_tasks)
            self._task_handler.start()

    def add_task(self, task):
        self._waitingQueue.put(task)

    def close(self):
        self._running = False
        self._waitingQueue = None
        self._processingQueue = None
        self._task_handler = None
        self.instance = None

    def set_task_listener(self, l):
        self._task_listener = l

    # private

    def _handle_tasks(self):
        tool.log(LOG_TAG, "_handle_tasks start")
        while self._running:
            # 1秒一次的轮询
            time.sleep(1)

            # 如果等待队列中没有任务， 则继续
            if self._waitingQueue.size() <= 0:
                continue

            # 当处理队列中有任务的时候，计算当前的总工作量，用以确定TaskManager是否还能承受
            if self._processingQueue.size() > 0:
                # 当前任务量
                current_load = self._processingQueue.get_load_sum()
                # 下一个任务的任务量
                future_load = self._waitingQueue.get_header_load()

                # 如果两者相加没超过总任务量， 则运行
                if current_load + future_load <= TaskManager._MAX_PROCESSING_:
                    # 将等待队列的任务放入处理队列，并启动进程池执行任务
                    t = self._waitingQueue.get()
                    self._processingQueue.put(t)
                    pm = ParserManager(t)
                    if self._task_listener:
                        pm.set_task_listener(self._task_listener)
                    pm.execute()
                    tool.log(LOG_TAG, "_handle_tasks: start ParserManager 1")
                else:
                    tool.log(LOG_TAG, "_handle_tasks: please hold on")
            else:
                # 如果当前处理队列中没有任务， 直接从等待队列中拿出一个任务放到处理队列
                task = self._waitingQueue.get()
                # 计算任务量
                task.getLoad()
                self._processingQueue.put(task)

                if self._task_listener:
                    self._task_listener.on_task_state_changed(task)

                tool.log(LOG_TAG, "tagggggggggggggggg")
                tool.log(LOG_TAG, "state = %d" % task.state)
                # 启动任务
                pm = ParserManager(task)
                pm.set_task_listener(self._task_listener)
                pm.execute()



