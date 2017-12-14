#-*- coding=utf-8 -*-

import sqlite3

cx=sqlite3.connect("/home/qinsw/pengtian/tmp/android_log_analysis_tool.db")
cu = cx.cursor()
#execute()--执行sql语句
#executemany--执行多条sql语句
#close()--关闭游标
#fetchone()--从结果中取一条记录，并将游标指向下一条记录
# fetchmany()--从结果中取多条记录
# fetchall()--从结果中取出所有记录
#scroll()--游标滚动

#create
# 有黄色警告按 Alt+enter进行配置
cu.execute('CREATE TABLE IF NOT EXISTS catalog (id integer PRIMARY KEY AUTOINCREMENT, pid integer, name varchar(10) UNIQUE)')

#insert
cu.execute("INSERT INTO catalog (pid, name) VALUES (0,'name4')")
#cu.execute("INSERT INTO catalog (pid, name) VALUES (1,'name2')")
cx.commit()

#select
#cu.execute("select * from catalog")
#print cu.fetchall()

#update
# cu.execute("update catalog set name='pengtianaaaa' where id = 1")
# cx.commit()

#delete
# cu.execute("delete from catalog where id = 1")
# cx.commit()
# cx.close()

#http://www.runoob.com/sqlite/sqlite-insert.html
#sqlite3 study