#-*- coding=utf-8 -*-
from task.TaskManager import TaskManager
import dbPresenter

# connect View and Model


# ----------------------------------------------------------------------------------------------------

class Presenter(object):
    def __init__(self, window):
        self.window = window
        self.taskManager = TaskManager()

        # Interface with 2 args:
        dbPresenter.AddInsertedListener(self.OnTaskDeletedListener)
        dbPresenter.AddUpdatedListener(self.OnTaskUpdatedListener)
        dbPresenter.AddDeletedListener(self.OnTaskDeletedListener)

    # called for ui
    def CreateTask(self, log_path, src_path=''):
        task = Task(log_path, src_path)
        # insert to db
        dbPresenter.InsertTask(task)

        # show in ui
        # self.window.


    def OnTaskInsertedListener(self, success, msg):
        if success:
            pass
        else:
            tool.log("OnTaskInsertedListener.error", "Insert Error")

    def OnTaskUpdatedListener(self):
        pass

    def OnTaskDeletedListener(self):
        pass






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