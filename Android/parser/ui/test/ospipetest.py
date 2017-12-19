#!/usr/bin/python
import time
import os

def child(wpipe):
    print('hello from child', os.getpid())
    while True:
        msg = 'how are you\n'.encode()
        os.write(wpipe, msg)
        time.sleep(1)

def parent():
    rpipe, wpipe = os.pipe()
    pid = os.fork()
    if pid == 0:
        child(wpipe)
        assert False, 'fork child process error!'
    else:
        os.close(wpipe)
        print('hello from parent', os.getpid(), pid)
        fobj = os.fdopen(rpipe, 'r')
        while True:
            recv = os.read(rpipe, 32)
            print recv

parent()