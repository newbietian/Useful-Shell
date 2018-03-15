# coding=utf-8
import threading
import threadpool

from Queue import Queue

from parser.Parser import *
from parser.Parser import __M_ANR__, __M_JAVA__, __M_NATIVE__
import tool.tools as tool
from task.task import Task


LOG_TAG = "ParserManager"


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

        self.task = task
        # 表明处理状态， True正在处理， False完成处理或其他情况
        self.running = True

        # 用于线程间通信以反馈解析进度的通信队列
        self.com_queue = Queue(maxsize=task.getLoad())

        # 接收通信队列发来消息的线程
        self.com_thread = threading.Thread(target=self._receiver)
        self.com_thread.setDaemon(True)
        self.com_thread.start()

        # 用来最后生成报告的线程
        self.gen_thread = None

        # 根据当前任务量创建线程池
        self.pool = threadpool.ThreadPool(task.getLoad())

        self.file_path_list = task.files
        self.src_path = task.src_path

        # TODO 从配置文件，而不是经过参数传递
        self.modules = (__M_JAVA__, __M_NATIVE__, __M_ANR__)

        # 用来存储最终结果的字典
        self._result_ = {}
        for m in self.modules:
            self._result_[m] = []

        # 当前任务进度
        self.percent = 0
        # 存储每个文件的进度
        self.percent_files = {}
        # 完成file计数
        self.files_done = 0

        # 状态反馈回调和监听
        self.task_listener = None

    def set_task_listener(self, tl):
        """
        回调设置函数
        :param tl: 回调， 用来和TaskManager沟通
        """
        self.task_listener = tl

    def execute(self):
        """
        接口：暴露给外部调用
        """

        # 检查是否有可解析的文件，如果没有，直接返回失败状态
        if not self.task or not len(self.task.files) > 0:
            tool.log("Illegal task argument.")

            self.task.state = Task.__STATE_FAILED__
            self.task.finish_time_millis \
                , self.task.finish_time = tool.get_time_local_and_format()
            if self.task_listener:
                self.task_listener.on_task_state_changed(self.task)

            self.running = False
            return

        # 形成任务列表
        task_list = []
        for l in self.task.files:
            l_tmp = ([l], None)
            task_list.append(l_tmp)

        # 生成多线程任务
        reqs = threadpool.makeRequests(self._execute, task_list, callback=self._callback)
        [self.pool.putRequest(req) for req in reqs]

    def _execute(self, log_path):
        """
        在子线程中运行的代码块
        :param log_path: 解析log文件的路径
        :return: 解析后的结果
        """
        tool.log("__start_one_parser", log_path)

        # 通知状态变化： 正在处理
        self.com_queue.put({"mode": 0, "state": Task.__STATE_PROCESSING__})

        p = Parser(log_path)
        p.set_sender(self.com_queue)
        return p.parse()

    # def __getstate__(self):
    #     """
    #     'pool objects cannot be passed between processes or pickled'
    #      NotImplementedError: pool objects cannot be passed between processes or pickled
    #     """
    #     self_dict = self.__dict__.copy()
    #     # del self_dict['_pool']
    #     # del self_dict['recvThread']
    #     return self_dict

    def _receiver(self):
        """ 接收工作线程通过queue发送过来的每个文件解析的进度， 处于“运行时”状态 """
        tool.log("start __receiver")
        if not self.com_queue:
            raise NullError("com_queue can't be Null")

        while self.running:
            # data 是字典类型的数据，
            # task状态消息 {"mode": 0, "state": xx}
            # parser子线程的消息 {"mode": 1, "log_path": xxx, "percent": 99}， 进度反馈
            data = self.com_queue.get()
            # print data

            if data["mode"] == 0:
                # 生成完成
                self.task.state = data["state"]
                if self.task.state == Task.__STATE_DONE__:
                    self.task.finish_time_millis \
                        , self.task.finish_time = tool.get_time_local_and_format()
                if self.task_listener:
                    self.task_listener.on_task_state_changed(self.task)

            elif data["mode"] == 1:
                # 存储当前log文件进度
                log_path = data["log_path"]
                percent = float(data["percent"])
                self.percent_files[log_path] = percent

                # 所有文件进度之和 = sum(self.percent_files.values())
                # 所有文件总个数 = len(self.file_path_list)或len(self.task.files)
                # 进度 = 所有文件进度之和 / 所有文件总个数
                self.percent = int((float(sum(self.percent_files.values())) / len(self.file_path_list)) * 100)

                # 调用 self.pool 的wait方法，迫使线程调用callback
                if self.percent >= 100:
                    self.pool.wait()

                # 将当前任务总体进度反馈给TaskManager
                if self.task_listener:
                    self.task_listener.on_task_progress_changed(self.task, self.percent)

    def _callback(self, wq, result):
        """
        子线程回调函数
        在所有解析完成后调用， 用来进一步去重， 进入：生成结果状态
        同时，启动图标数据生成线程
        :param wq WorkRequest 子线程的任务的封装类实例，包含子线程参数信息
        :param result: 从Parser返回的每个文件对应的结果
        """

        self.files_done += 1

        # 将文件的结果汇总
        try:
            for m in self.modules:
                if len(result[m]) > 0:
                    # 遍历每个result
                    for i, r in enumerate(result[m]):
                        # 如果已经在列表中，就合并。如果没有，就添加到列表中
                        if r in self._result_[m]:
                            r_already = self._result_[m][i]
                            r_already.combine(r)
                        else:
                            self._result_[m].append(r)

        except Exception as e:
            print "exception in callback = %s , %s" % (wq, e.message)

        # for r in self._result_[__M_JAVA__]:
        #    print r

        if self.files_done >= len(self.task.files):
            print "Should remove duplicate result"
            print "Start thread to generate result"
            # callback
            self.task.state = Task.__STATE_GENERATING__
            if self.task_listener:
                self.task_listener.on_task_state_changed(self.task)

            self.gen_thread = threading.Thread(target=self._run_generator, args=(self._result_,))
            self.gen_thread.start()

    def _run_generator(self, result):
        """ 结果生成线程的执行代码段
            :param result: 经过Parser内部去重和ParserManager外部去重后的结果
        """

        # 通知状态变化：正在生成
        self.com_queue.put({"mode": 0, "state": Task.__STATE_GENERATING__})

        # TODO 未完成
        print result
        print "Generating..."
        time.sleep(2)

        # 通知状态变化：任务完成
        self.com_queue.put({"mode": 0, "state": Task.__STATE_DONE__})
