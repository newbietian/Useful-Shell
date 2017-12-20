#-*- coding=utf-8 -*-
from ui.db import sqliteHelper as dbHelper
from task.task import Task

# DB
# ---------------------

def InsertTask(task):
    sql = "INSERT INTO history (log_path, src_path, state) VALUES (?, ?, ?)"
    args=(task.log_path, task.src_path, task.state)
    dbHelper.insert(sql, args)

# ---------------------
def DeleteAll():
    sql = "DELETE FROM history"
    dbHelper.delete(sql)

def DeleteOne(log_path):
    sql = "DELETE FROM history WHERE log_path = ?"
    args = (log_path, )
    dbHelper.delete(sql, args)

# ---------------------
def UpdateTaskResultPath(log_path, path):
    sql = "UPDATE history SET result_path = ? WHERE log_path = ?"
    args = (path, log_path)
    dbHelper.update(sql, args)

def UpdateTaskState(log_path, new_state):
    sql = "UPDATE history SET state = ? WHERE log_path = ?"
    args = (new_state, log_path)
    dbHelper.update(sql, args)

# ---------------------
def SelectALLTask():
    sql = "SELECT * FROM history"
    return dbHelper.select(sql)

def SelectProcessingTask():
    sql = "SELECT * FROM history WHERE state = ?"
    args = (Task.__STATE_PROCESSING__, )
    return dbHelper.select(sql, args)

def SelectWaitingTask():
    sql = "SELECT * FROM history WHERE state = ?"
    args = (Task.__STATE_WAITING__, )
    return dbHelper.select(sql, args)

def SelectDoneTask():
    sql = "SELECT * FROM history WHERE state = ?"
    args = (Task.__STATE_DONE__, )
    return dbHelper.select(sql, args)

# ---------------------
def AddInsertedListener(callback):
    dbHelper.addInsertedListener(callback)

def AddDeletedListener(callback):
    dbHelper.addDeletedListener(callback)

#def addSelectedListener(callback):
#    dbHelper.addSelectedListener(callback)

def AddUpdatedListener(callback):
    dbHelper.addUpdatedListener(callback)