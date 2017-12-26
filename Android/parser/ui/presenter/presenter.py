#-*- coding=utf-8 -*-
from task.TaskManager import TaskManager
from task.TaskManager import TaskListener
from task.task import Task
import tool.tools as tool
import dbPresenter
import wx


class UIActionInterface(object):
    def AddTaskToProcessPanel(self, task):
        '''
        :param task: target task
        '''

    def AddTaskFailed(self, task, msg):
        '''
        Error occurred in insert db
        :param task:
        '''

    def UpdateTaskProgress(self, task, progress):
        '''
        Update the processing task progress
        :param task: identity
        :param progress: 1-100 integer
        '''

    def UpdateTaskInProcessPanel(self, task):
        '''
        :param task:
        '''

    def RemoveTaskFromProcessing(self, task):
        '''
        :param task:
        '''

    def AddTaskToDone(self, task):
        '''
        :param task:
        '''

    def RemoveTaskFromDone(self, task):
        '''
        :param task:
        '''
# ----------------------------------------------------------------------------------------------------
mUI = None

def setUI(ui):
    global mUI
    mUI = ui

def getUI():
    global mUI
    return mUI

class Presenter(TaskListener):
    def __init__(self):
        #self.ui = ui
        self.taskManager = TaskManager()
        self.taskManager.setTaskListener(self)
        self.taskManager.start()

        # Interface with 2 args:
        # dbPresenter.AddInsertedListener(self.OnTaskDeletedListener)
        # dbPresenter.AddUpdatedListener(self.OnTaskUpdatedListener)
        # dbPresenter.AddDeletedListener(self.OnTaskDeletedListener)

    # def __getstate__(self):
    #     '''
    #     PicklingError: Can't pickle <type 'PySwigObject'>: attribute lookup __builtin__.PySwigObject failed
    #     wxPython中，ui类型的object不能被其他进程共享
    #     '''
    #     self_dict = self.__dict__.copy()
    #     del self_dict['ui']
    #     return self_dict

    #def __call__(self, *args, **kwargs):
    #    pass

    # called by ui
    def CreateTask(self, log_path, src_path=''):
        task = Task(log_path, src_path)
        # insert to db
        suc = dbPresenter.InsertTask(task)
        print suc
        if not suc[0] and suc[1]:
            #self.ui.AddTaskFailed(task, suc[1])
            if mUI: mUI.AddTaskFailed(task, suc[1])
            return

        # show in ui
        #self.ui.AddTaskToProcessPanel(task)
        if mUI: mUI.AddTaskToProcessPanel(task)

        # put into task manager
        self.taskManager.addTask(task)

    # Called by ParserManager
    def onTaskStateChanged(self, task):
        if mUI:
            tool.log("onTaskStateChanged", mUI)
            # wx.CallAfter(self.ui.UpdateTaskInProcessPanel(task))
            wx.CallAfter(mUI.UpdateTaskInProcessPanel(task))

    def onTaskProgressChanged(self, task, progress):
        if mUI:
            tool.log("onTaskProgressChanged", mUI)
            #wx.CallAfter(self.ui.UpdateTaskProgress(task, progress))
            wx.CallAfter(mUI.UpdateTaskProgress(task, progress))



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