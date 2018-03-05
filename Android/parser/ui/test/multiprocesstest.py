import wx
import multiprocessing
import os
import threading

#from task.TaskManager import TaskManager
from task.task import Task
import uuid
import time

def proxy(cls, wpipe):
    cls.__run__(wpipe)

class Hello(object):
    def __init__(self):
        self.pool = multiprocessing.Pool()

    def __run__(self, wpipe):
        #wx.CallAfter(self.window.LogMessage, "hahahahahah")
        print "hahahah"
        os.write(wpipe, "nihaohaohaoahaoaoa\n")

    def __getstate__(self):
        self_dict = self.__dict__.copy()
        del self_dict['pool']
        return self_dict

    def addProcess(self, wpipe):
        self.pool.apply_async(proxy, args=(self, wpipe))

    def close(self):
        self.pool.close()
        self.pool.terminate()


class MyFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="Multi-Process GUI")

        panel = wx.Panel(self)
        startBtn = wx.Button(panel, -1, "Start a thread")
        stopBtn = wx.Button(panel, -1, "Stop all threads")
        self.tc = wx.StaticText(panel, -1, "Worker Threads: 00")
        self.log = wx.TextCtrl(panel, -1, "",
                               style=wx.TE_RICH | wx.TE_MULTILINE)

        inner = wx.BoxSizer(wx.HORIZONTAL)
        inner.Add(startBtn, 0, wx.RIGHT, 15)
        inner.Add(stopBtn, 0, wx.RIGHT, 15)
        inner.Add(self.tc, 0, wx.ALIGN_CENTER_VERTICAL)
        main = wx.BoxSizer(wx.VERTICAL)
        main.Add(inner, 0, wx.ALL, 5)
        main.Add(self.log, 1, wx.EXPAND | wx.ALL, 5)
        panel.SetSizer(main)

        self.Bind(wx.EVT_BUTTON, self.OnStartButton, startBtn)
        self.Bind(wx.EVT_BUTTON, self.OnStopButton, stopBtn)
        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

        self.UpdateCount()

        self.tm = TaskManager()
        self.tm.start()

        self.receiver, self.writer = os.pipe()
        self.thread = threading.Thread(target=self.threadTarget, args=(self.receiver, ))
        self.thread.setDaemon(True)
        self.thread.start()

        #self.test = Hello()


    def threadTarget(self, rpipe):
        while True:
            #recv = os.read(rpipe,32)
            #wx.CallAfter(self.LogMessage, recv)

            print "loop"
            if self.tm and len(self.tm._processingQueue._queue) > 0:
                task = self.tm._processingQueue.get()
                print "done = ", task.name

            time.sleep(3)



    def OnStartButton(self, evt):
        #self.test.addProcess(self.writer)
        task = Task(str(uuid.uuid4()),Task.__STATE_NEW__, "", "")
        print "add task = ", task.name
        self.tm.add_task(task)

    def OnStopButton(self, evt):
        self.StopThreads()
        self.UpdateCount()

    def OnCloseWindow(self, evt):
        self.StopThreads()
        #self.test.close()
        self.Destroy()

    def StopThreads(self):
        print "hahahahaha"

    def UpdateCount(self):
        #self.tc.SetLabel("Worker Threads: %d" % len(self.threads))
        pass

    def LogMessage(self, msg):
        self.log.AppendText(msg)

    def ThreadFinished(self, thread):
        #self.threads.remove(thread)
        self.UpdateCount()

app = wx.PySimpleApp()
frm = MyFrame()
frm.Show()
app.MainLoop()