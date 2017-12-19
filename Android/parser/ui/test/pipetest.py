# -*- coding:utf-8 -*-
import os
import multiprocessing
import threading
def proc1(pipe):
    try:
        s = "message from haha"
        os.write(pipe, s)
    except IOError as e:
        print "error", e.message

def proc2(pipe):
    try:
        #os.fdopen(pipe,'r')
        while True:
            print "proc2 recieve:", os.read(pipe,32)
    except IOError as e:
        print "error", e.message

if __name__ == "__main__":
    r, w = os.pipe()
    thread = threading.Thread(target=proc2, args=(r,))
    thread.setDaemon(True)
    thread.start()
    pool = multiprocessing.Pool()
    pool.apply_async(proc1, args=(w,))
    pool.apply_async(proc1, args=(w,))
    pool.apply_async(proc1, args=(w,))
    pool.apply_async(proc1, args=(w,))

    #pool.apply_async(proc1, args=(pipe[0],))
    #pool.apply_async(proc1, args=(pipe[0],))


    #p1 = Process(target=proc1, args=(pipe[0],))
    #p2 = Process(target=proc2, args=(pipe[1],))
    #p1.start()
    #p2.start()
    #p1.join()
    #p2.join()   #限制执行时间最多为2秒
    pool.close()
    pool.join()
    print '\nend all processes.'

    import re
    s = "path: /home/path/xxx, percent: 0.1341"
    m = re.match(r"^path: (/.+), percent: ([01]\.\d+)?$", s)
    if m:
        print m.group(1), m.group(2)