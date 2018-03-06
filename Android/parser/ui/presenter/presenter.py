# -*- coding=utf-8 -*-
from task.TaskManager import TaskManager
from task.TaskManager import TaskListener
from task.task import Task
import tool.tools as tool
import dbPresenter
import wx


class UIActionInterface(object):
    """
    UI的回调接口， UI会继承此接口
    """

    def AddTaskToProcessPanel(self, task):
        """ 将任务添加到处理面板 """

    def AddTaskFailed(self, task, msg):
        """ 添加任务失败的时候，调用已更新UI """

    def UpdateTaskProgress(self, task, progress):
        """
        更新Task的进度
        :param task: 标识，用来区分更新哪个Task
        :param progress: 1-100 整数
        """

    def UpdateTaskInProcessPanel(self, task):
        """ 更新Task的状态 """

    def RemoveTaskFromProcessing(self, task):
        """ 将Task从正在处理面板里移除 """

    def AddTaskToDone(self, task):
        """ 将Task添加到处理完成面板 """

    def RemoveTaskFromDone(self, task):
        """ 移除完成面板里的指定任务 """

# ----------------------------------------------------------------------------------------------------


class Presenter(TaskListener):
    """ UI和TaskManager交互的Presenter """
    def __init__(self, ui):
        self.ui = ui
        self.task_manager = TaskManager()
        self.task_manager.set_task_listener(self)
        self.task_manager.start()

    # 由UI界面调用
    def create_task(self, log_path, src_path=''):
        task = Task(log_path, src_path)
        # 添加到ui的任务处理队列
        self.ui.AddTaskToProcessPanel(task)
        # 添加到TaskManager中处理
        self.task_manager.add_task(task)

    # 由TaskManager调用，回调，用以更新UI
    def on_task_state_changed(self, task):
        if task.state >= Task.__STATE_DONE__:
            # 此时将任务从正在处理列表移除， 放入已经完成任务列表
            wx.CallAfter(self.ui.RemoveTaskFromProcessing, task=task)
            wx.CallAfter(self.ui.AddTaskToDone, task=task)

            # TODO 将已经完成任务记录入数据库
        else:
            wx.CallAfter(self.ui.UpdateTaskInProcessPanel,task=task)

    def on_task_progress_changed(self, task, progress):
        wx.CallAfter(self.ui.UpdateTaskProgress, task=task, progress=progress)

# ----------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    def a(r):
        print r
    #addInsertedListener(a)

    from task.task import Task
    # task = Task("test1", Task.__STATE_PROCESS__, "/home/qinsw/", "/home/qinsw/heh")
    # InsertTask(task)
    # task = Task("test121", Task.__STATE_NEW__, "/home/qinsw/", "/home/qinsw/heh")
    # InsertTask(task)
    # task = Task("te131st1", Task.__STATE_DONE__, "/home/qinsw/", "/home/qinsw/heh")
    # InsertTask(task)
    # task = Task("test1411", Task.__STATE_PROCESS__, "/home/qinsw/", "/home/qinsw/heh")
    # InsertTask(task)
    # task = Task("tes51t1", Task.__STATE_WAIT__, "/home/qinsw/", "/home/qinsw/heh")
    # InsertTask(task)
    # task = Task("test5151", Task.__STATE_PROCESS__, "/home/qinsw/", "/home/qinsw/heh")
    # InsertTask(task)
    # task = Task("tafaest1411", Task.__STATE_PROCESS__, "/home/qinsw/", "/home/qinsw/heh")
    # InsertTask(task)


    #addDeletedListener(a)
    #deleteAll()

    #deleteOne("test1")

    #addUpdatedListener(a)
    #updateTaskName("test1", "new_test1")

    #updateTaskResultPath("new_test1", "/home/hello")

    from tool import tools as tool

    ttt = "2017-12-14 16:09:04"
    print tool.str2msecs(ttt)

    #addSelectedListener(a)
    # SelectALLTask()
    # SelectProcessingTask()
    # SelectWaitingTask()
    # SelectDoneTask()