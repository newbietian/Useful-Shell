#-*- coding=utf-8 -*-
import os
from ui.db import sqliteHelper as dbHelper

# connect View and Model

# DB
# ---------------------
def insertTask(task):
    sql = "INSERT INTO history (name, state, log_path, src_path) VALUES (?, ?, ?, ?)"
    args=(task.name, task.state, task.log_path, task.src_path)
    dbHelper.insert(sql, args)

# ---------------------
def deleteAll():
    sql = "DELETE FROM history"
    dbHelper.delete(sql)

def deleteOne(name):
    sql = "DELETE FROM history WHERE name = ?"
    args = (name, )
    dbHelper.delete(sql, args)

# ---------------------
def updateTaskName(old_name, new_name):
    sql = "UPDATE history SET name = ? WHERE name = ?"
    args = (new_name, old_name)
    dbHelper.update(sql, args)

def updateTaskResultPath(name, path):
    sql = "UPDATE history SET result_path = ? WHERE name = ?"
    args = (path, name)
    dbHelper.update(sql, args)

# ---------------------
def selectALLTask():
    sql = "SELECT * FROM history"
    return dbHelper.select(sql)

def selectProcessingTask():
    sql = "SELECT * FROM history WHERE state = ?"
    args = (Task.__STATE_PROCESS__, )
    return dbHelper.select(sql, args)

def selectWaitingTask():
    sql = "SELECT * FROM history WHERE state = ?"
    args = (Task.__STATE_WAIT__, )
    return dbHelper.select(sql, args)

def selectDoneTask():
    sql = "SELECT * FROM history WHERE state = ?"
    args = (Task.__STATE_DONE__, )
    return dbHelper.select(sql, args)

# ---------------------
def addInsertedListener(callback):
    dbHelper.addInsertedListener(callback)

def addDeletedListener(callback):
    dbHelper.addDeletedListener(callback)

#def addSelectedListener(callback):
#    dbHelper.addSelectedListener(callback)

def addUpdatedListener(callback):
    dbHelper.addUpdatedListener(callback)

# ----------------------------------------------------------------------------------------------------


if __name__ == '__main__':
    def a(r):
        print r
    #addInsertedListener(a)

    from ui.entity.task import Task
    task = Task("test1", Task.__STATE_PROCESS__, "/home/qinsw/", "/home/qinsw/heh")
    insertTask(task)
    task = Task("test121", Task.__STATE_NEW__, "/home/qinsw/", "/home/qinsw/heh")
    insertTask(task)
    task = Task("te131st1", Task.__STATE_DONE__, "/home/qinsw/", "/home/qinsw/heh")
    insertTask(task)
    task = Task("test1411", Task.__STATE_PROCESS__, "/home/qinsw/", "/home/qinsw/heh")
    insertTask(task)
    task = Task("tes51t1", Task.__STATE_WAIT__, "/home/qinsw/", "/home/qinsw/heh")
    insertTask(task)
    task = Task("test5151", Task.__STATE_PROCESS__, "/home/qinsw/", "/home/qinsw/heh")
    insertTask(task)
    task = Task("tafaest1411", Task.__STATE_PROCESS__, "/home/qinsw/", "/home/qinsw/heh")
    insertTask(task)


    #addDeletedListener(a)
    #deleteAll()

    #deleteOne("test1")

    #addUpdatedListener(a)
    #updateTaskName("test1", "new_test1")

    #updateTaskResultPath("new_test1", "/home/hello")

    from tool import tools as tool
    import re
    ttt = "2017-12-14 16:09:04"
    print tool.str2secs(ttt)

    #addSelectedListener(a)
    selectALLTask()
    selectProcessingTask()
    selectWaitingTask()
    selectDoneTask()