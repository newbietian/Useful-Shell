#-*- coding=utf-8 -*-
import sqlite3
from tool import tools as __tool

__TABLE_NAME__='history'

DO_CREATE_DB = False

def __getDbPath():
    app_path = __tool.getAppDataPath()
    if not app_path.endswith("/"):
        app_path+="/"
    db_path = app_path + __tool.__DB_NAME__
    return db_path

# create database in $HOME path
def tryCreateTables():
    global DO_CREATE_DB
    if DO_CREATE_DB:
        return
    DO_CREATE_DB = True

    db = sqlite3.connect(__getDbPath())
    cursor = db.cursor()

    cursor.execute("CREATE TABLE IF NOT EXISTS history ("
                    " id integer PRIMARY KEY AUTOINCREMENT,"
                    " name varchar UNIQUE,"
                    " state integer,"
                    " log_path varchar,"
                    " src_path varchar,"
                    " result_path varchar,"
                    " create_time TimeStamp NOT NULL DEFAULT (DATETIME('now','localtime')) )")

    db.commit()
    db.close()

#---INSERT-------------------------------------------------------
__INSERT_LISTENERS=[]

def insert(sql, args=()):
    if sql is None or sql == '':
        __notifyInsert(False, "sql is null")
        __tool.log("select.error", "sql is null")
        return False
    tryCreateTables()
    db = sqlite3.connect(__getDbPath())
    cursor = db.cursor()
    try:
        cursor.execute(
            #'''INSERT INTO history (name, state, log_path, src_path, create_time) VALUES (?,?,?,?,?)'''
            #,(task.name, task.state, task.log_path, task.src_path, task.create_time)
            sql, args
        )
        db.commit()
        __notifyInsert(True)

        __tool.log("sqlite3.insert success", sql + str(args))
        return True
    except sqlite3.IntegrityError as e:
        __notifyInsert(False, e.message)

        __tool.log("sqlite3.IntegrityError", e.message)
        return False, e.message
    finally:
        db.close()

def addInsertedListener(callback):
    if callback not in __INSERT_LISTENERS:
        __INSERT_LISTENERS.append(callback)
        __tool.log("add callback" + str(callback))
    else:
        __tool.log("callback exists")

def __notifyInsert(result, msg=''):
    try:
        for c in __INSERT_LISTENERS:
            c(result, msg)
    except Exception as e:
        __tool.log("__notifyInsert.error", e.message)

#--------SELECT----------------------------------------------------------------------

__SELECTED_LISTENER=[]
def select(sql, args=()):
    if sql is None or sql == '':
        __notifySelected(None)
        __tool.log("select.error", "sql is null")
        return None

    tryCreateTables()
    db = sqlite3.connect(__getDbPath())
    cursor = db.cursor()
    try:
        cursor.execute(sql, args)
        ret = cursor.fetchall()
        __notifySelected(ret)
        return ret
    except Exception as e:
        __notifySelected(None)
        __tool.log("select.error", e.message)
        return None
    finally:
        db.close()

def addSelectedListener(callback):
    if callback not in __SELECTED_LISTENER:
        __SELECTED_LISTENER.append(callback)
        __tool.log("sqlite.addSelectedListener " + str(callback))
    else:
        __tool.log("sqlite.addSelectedListener callback exists")

def __notifySelected(data):
    try:
        for c in __SELECTED_LISTENER:
            c(data)
    except Exception as e:
        __tool.log("__notifySelected.error", e.message)

# -------------DELETE---------------------------------------------------------------------
__DELETE_LISTENER=[]
def delete(sql, args=()):
    if sql is None or sql == '':
        __notifyDeleted(False, "sql is null")
        __tool.log("delete.error", "sql is null")
        return
    tryCreateTables()
    db = sqlite3.connect(__getDbPath())
    cursor = db.cursor()
    try:
        cursor.execute(sql, args)
        db.commit()

        __notifyDeleted(True)
        return True
    except Exception as e:
        __notifyDeleted(False, e.message)
        __tool.log("delete.error", e.message)
        return False
    finally:
        db.close()

def addDeletedListener(callback):
    if callback not in __DELETE_LISTENER:
        __DELETE_LISTENER.append(callback)
        __tool.log("sqlite.addDeletedListener " + str(callback))
    else:
        __tool.log("sqlite.addDeletedListener callback exists")

def __notifyDeleted(result, msg=''):
    try:
        for c in __DELETE_LISTENER:
            c(result, msg)
    except Exception as e:
        __tool.log("__notifyDeleted.error", e.message)


# ----UPDATE--------------------------------------------------------------------------
__UPDATED_LISTENER=[]
def update(sql, args=()):
    if sql is None or sql == '':
        __notifyUpdated(False, "sql is null")
        __tool.log("update", "sqlite is null")
        return False
    tryCreateTables()
    db = sqlite3.connect(__getDbPath())
    cursor = db.cursor()
    try:
        print args
        cursor.execute(sql, args)
        db.commit()
        __notifyUpdated(True)

        __tool.log("sqlite3.update", sql + str(args) + " success")
        return True
    except sqlite3.IntegrityError as e:
        __notifyUpdated(False, e.message)

        __tool.log("update.IntegrityError", e.message)
        return False, e.message
    finally:
        db.close()


def addUpdatedListener(callback):
    if callback not in __UPDATED_LISTENER:
        __tool.log("addUpdatedListener", "add callback" + str(callback))
        __UPDATED_LISTENER.append(callback)
    else:
        __tool.log("addUpdatedListener", "call back existed")

def __notifyUpdated(result, msg=''):
    try:
        for c in __UPDATED_LISTENER:
            c(result, msg)
    except Exception as e:
        __tool.log("__notifyUpdated.error", e.message)

# --------------Test--------------------------------------------------------------------------

if __name__ == "__main__":
    __tool.log(__getDbPath())
    tryCreateTables()
    def a(r,m):
        print "__notifyUpdated a ", r, m
    # def b(r):
    #     print "addSelectedListener b ", r
    #addInsertedListener(a)
    #addInsertedListener(b)

    # addSelectedListener(a)
    # addSelectedListener(b)
    # addSelectedListener(b)
    # addDeletedListener(a)
    # addDeletedListener(a)

    addUpdatedListener(a)
    addUpdatedListener(a)

    # test insert
    #from ui.entity.task import Task
    #print insert(Task("suye",Task.__STATE_NEW__, "haha", "hehe"))
    # task = Task("suye12331afaqeqe21", Task.__STATE_DONE__, "haha", "hehe")
    # sql = '''INSERT INTO history (name, state, log_path, src_path) VALUES (?,?,?,?)'''
    # args = (task.name, task.state, task.log_path, task.src_path)
    # insert(sql, args)

    # test select
    #select("SELECT * FROM history WHERE state = ?", (3,))
    #select("SELECT * FROM history")
    #select("SELECT * FROM history WHERE state = ?", (3,))


    # test delete
    #delete("DELETE FROM history WHERE id = ?", (1,))

    # test update
    # update("UPDATE history SET name = ? WHERE name = 'pengtian'",("pengtian0528",))





